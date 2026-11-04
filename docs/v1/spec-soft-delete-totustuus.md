# SPEC: Soft Delete (Exclusão Lógica) — TotusTuusSoftCloud

- Language Standard: Global English
## 1. Objetivo
Implementar exclusão lógica (soft delete) em todas as entidades multi-tenant
do sistema, garantindo que nenhum registro seja removido fisicamente do
banco, preservando histórico, auditoria e possibilidade de restauração
(undo), em conformidade com LGPD (retenção controlada) e requisitos de
auditoria corporativa.

## 2. Conceito
- Soft Delete = marcar o registro como "excluído" via flag/coluna,
  sem executar DELETE físico no SQL.
- Registro permanece na tabela, mas fica invisível nas consultas padrão.
- Pode ser restaurado (undo delete) ou purgado definitivamente após
  período de retenção (hard delete programado / GC job).

## 3. Estrutura de Banco de Dados

### 3.1 Colunas obrigatórias em toda tabela "soft-deletable"
| Coluna          | Tipo         | Descrição                                    |
|-----------------|--------------|-----------------------------------------------|
| deleted_at      | DATETIME NULL| Timestamp da exclusão lógica (NULL = ativo)   |
| deleted_by      | BIGINT NULL  | FK para usuário que executou a exclusão       |
| deleted_reason  | VARCHAR(255) | Motivo/observação da exclusão (opcional)      |
| is_deleted      | TINYINT(1)   | Flag redundante indexada para performance     |

### 3.2 Índices
- Índice composto: (entity_id, unit_id, is_deleted) — para queries
  multi-tenant filtrando ativos rapidamente.
- Índice em deleted_at para jobs de purga automática.

### 3.3 Migration exemplo (MySQL/MariaDB)
```sql
ALTER TABLE alunos
  ADD COLUMN deleted_at DATETIME NULL DEFAULT NULL,
  ADD COLUMN deleted_by BIGINT NULL,
  ADD COLUMN deleted_reason VARCHAR(255) NULL,
  ADD COLUMN is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  ADD INDEX idx_soft_delete (entity_id, unit_id, is_deleted),
  ADD INDEX idx_deleted_at (deleted_at);
```

## 4. Regras de Negócio
1. Nenhum endpoint de API deve executar `DELETE FROM` diretamente em
   tabelas marcadas como soft-deletable.
2. Todo `SELECT` padrão via Repository/DAO deve incluir automaticamente
   `WHERE is_deleted = 0` (ou `deleted_at IS NULL`).
3. Deve existir um scope/flag explícito `withTrashed()` / `onlyTrashed()`
   para consultas administrativas e auditoria.
4. Exclusão lógica deve registrar: quem excluiu, quando, motivo, e
   IP/sessão (via módulo de auditoria já existente no sistema).
5. Restauração (`restore()`) deve limpar deleted_at/deleted_by e logar
   a ação de restauração no módulo de auditoria.
6. Hard delete (purga física) só deve ocorrer via job administrativo,
   após N dias de retenção configuráveis por entidade (LGPD compliance),
   e requer aprovação de superadmin.
7. Relacionamentos (FKs) devem usar soft delete em cascata lógica
   (aplicação, não banco), nunca `ON DELETE CASCADE` físico.

## 4.1 Validação Pré-Delete (Obrigatória)

Antes de qualquer soft delete ou hard delete, o sistema DEVE executar
uma cadeia de validações. Se qualquer validação falhar, a operação é
abortada e retorna erro 409 (Conflict) com mensagem explicativa.

### Checklist de validação (ordem de execução)
1. **Existência**: registro existe e pertence à entity_id/unit_id do
   usuário autenticado (evita IDOR / cross-tenant delete).
2. **Permissão**: usuário possui role/permissão RBAC para deletar este
   recurso específico (não apenas a rota).
3. **Integridade referencial (uso em outras tabelas)**: verificar se o
   ID está referenciado em tabelas dependentes antes de excluir.
4. **Regras de negócio específicas**: ex. não permitir excluir aluno
   com matrícula ativa, não permitir excluir fatura já paga, não
   permitir excluir usuário com sessão ativa.
5. **Janela de tempo/estado**: ex. não excluir registro com menos de
   X minutos para um evento agendado (trigger de validação temporal).
6. **Confirmação explícita do usuário**: front-end exige modal de
   confirmação (ex. SweetAlert2) antes de enviar o DELETE; back-end
   pode exigir header/flag `X-Confirm-Delete: true` como segunda
   camada de proteção contra chamadas automatizadas acidentais.

### Exemplo de validação de integridade referencial (PHP)
```php
public function validarPodeDeletar(int $id): void {
    $emUso = $this->pdo->prepare(
        "SELECT COUNT(*) FROM matriculas WHERE aluno_id = :id AND is_deleted = 0"
    );
    $emUso->execute(['id' => $id]);
    if ($emUso->fetchColumn() > 0) {
        throw new BusinessRuleException(
            "Não é possível excluir: aluno possui matrícula(s) ativa(s)."
        );
    }
}

public function softDelete(int $id, int $userId, ?string $reason = null): bool {
    $this->validarPodeDeletar($id);   // <-- validação obrigatória antes
    // ... segue lógica de soft delete já definida na seção 5.2
}
```

### Exemplo Node.js/Sequelize (com hook)
```js
Aluno.beforeDestroy(async (aluno) => {
  const emUso = await Matricula.count({
    where: { alunoId: aluno.id, isDeleted: false }
  });
  if (emUso > 0) {
    throw new Error('Aluno possui matrícula ativa. Exclusão bloqueada.');
  }
});
```

## 4.2 Testes adicionais obrigatórios (validação)
- [ ] Delete é bloqueado quando registro está em uso em tabela relacionada.
- [ ] Delete é bloqueado quando usuário não tem permissão RBAC específica.
- [ ] Delete é bloqueado quando registro pertence a outra entity_id (cross-tenant).
- [ ] Front-end exige confirmação explícita antes de disparar o DELETE.
- [ ] Mensagem de erro de validação é clara e específica (não genérica).

## 4.3 Tratamento de Unique Constraints com Soft Delete

### Problema
UNIQUE constraints tradicionais falham quando um registro soft-deleted
mantém o mesmo valor único (email, CPF, matrícula) que um novo registro
tenta usar.

### Solução (MySQL/MariaDB) — Virtual Column
```sql
ALTER TABLE <tabela>
  ADD COLUMN unarchived BOOLEAN
    GENERATED ALWAYS AS (IF(deleted_at IS NULL, 1, NULL)) VIRTUAL,
  ADD UNIQUE KEY uk_<campo>_unarchived (<campo_unico>, unarchived);
```

### Solução (PostgreSQL) — Índice Parcial
```sql
CREATE UNIQUE INDEX uk_<campo>_ativo
  ON <tabela>(<campo_unico>)
  WHERE deleted_at IS NULL;
```

### Regra de negócio complementar
- Ao tentar criar um registro com valor único já existente em um
  registro soft-deleted, o sistema deve oferecer opção de "restaurar"
  o registro antigo em vez de criar um novo (evita duplicação de
  histórico).

## 4.4 Cascata Lógica em Relacionamentos
- Ao soft-deletar uma entidade "pai", disparar soft delete em cascata
  (via transação/hook, nunca via FK física) em todas as entidades
  "filhas" diretamente dependentes.
- Registrar essa cascata como uma única operação de auditoria (batch)
  para rastreabilidade.

## 4.5 Critério de Aplicação (Evitar Anti-Pattern)
- Soft delete deve ser aplicado apenas a entidades que exigem
  histórico/auditoria/restauração (alunos, matrículas, faturas,
  usuários).
- Tabelas de log, cache, ou dados puramente transacionais sem valor
  de auditoria devem usar hard delete direto, evitando inchar o
  banco sem necessidade.

## 4.6 Testes adicionais (unique constraint / cascata)
- [ ] Criar novo registro com valor igual a um soft-deleted não gera erro de UNIQUE.
- [ ] Restaurar registro com valor único já reservado por outro ativo é bloqueado.
- [ ] Soft delete do pai propaga corretamente para todos os filhos.
- [ ] Cascata gera um único evento de auditoria (não N eventos fragmentados).

## 5. Camada de Aplicação (PHP/Node.js)

### 5.1 Interface padrão do Repository
```php
interface SoftDeletableRepository {
    public function softDelete(int $id, int $userId, ?string $reason = null): bool;
    public function restore(int $id, int $userId): bool;
    public function findAllActive(array $filters = []): array;
    public function findAllTrashed(array $filters = []): array;
    public function purge(int $id): bool; // hard delete real, restrito
}
```

### 5.2 Exemplo de implementação (PHP puro/PDO)
```php
public function softDelete(int $id, int $userId, ?string $reason = null): bool {
    $sql = "UPDATE alunos
            SET is_deleted = 1, deleted_at = NOW(),
                deleted_by = :userId, deleted_reason = :reason
            WHERE id = :id AND entity_id = :entityId";
    $stmt = $this->pdo->prepare($sql);
    $result = $stmt->execute([
        'userId' => $userId, 'reason' => $reason,
        'id' => $id, 'entityId' => $this->currentEntityId
    ]);
    $this->auditLogger->log('soft_delete', 'alunos', $id, $userId);
    return $result;
}

public function restore(int $id, int $userId): bool {
    $sql = "UPDATE alunos
            SET is_deleted = 0, deleted_at = NULL, deleted_by = NULL
            WHERE id = :id";
    $stmt = $this->pdo->prepare($sql);
    $result = $stmt->execute(['id' => $id]);
    $this->auditLogger->log('restore', 'alunos', $id, $userId);
    return $result;
}
```

### 5.3 Node.js (Sequelize) — nativo
```js
Aluno.init({...}, {
  sequelize,
  paranoid: true,        // ativa soft delete automático
  deletedAt: 'deleted_at'
});

// Uso:
await aluno.destroy();               // soft delete
await aluno.restore();               // restaura
await Aluno.findAll({ paranoid: false }); // inclui excluídos
```

## 6. API REST — Endpoints
| Método | Rota                          | Ação                              |
|--------|-------------------------------|-------------------------------------|
| DELETE | /api/alunos/{id}              | Soft delete (marca deleted_at)      |
| PATCH  | /api/alunos/{id}/restore      | Restaura registro                   |
| GET    | /api/alunos?trashed=true      | Lista registros excluídos           |
| DELETE | /api/alunos/{id}/purge        | Hard delete real (superadmin only)  |

## 7. Segurança e Compliance (LGPD)
- Registros soft-deleted contendo dados pessoais devem ter acesso
  restrito por RBAC (apenas admin/auditor).
- Definir política de retenção (ex: 90 dias) após a qual dados podem
  ser anonimizados ou purgados via job agendado.
- Toda operação de soft delete/restore deve gerar log de auditoria
  imutável (append-only), com hash de integridade.

## 8. Testes obrigatórios (gerais)
- [ ] Soft delete não remove linha física da tabela.
- [ ] Consulta padrão não retorna registros com is_deleted = 1.
- [ ] Restore reativa corretamente o registro.
- [ ] Multi-tenant: soft delete em uma entidade não afeta outras.
- [ ] Job de purga respeita período de retenção configurado.
- [ ] Auditoria registra usuário, timestamp e motivo corretamente.
