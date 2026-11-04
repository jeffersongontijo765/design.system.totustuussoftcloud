# Planejamento de desenvolvimento de pessoas

- Portal: Gestão (`gestao.`)
- Área: Planejamento acadêmico, institucional e de desenvolvimento
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 4; [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 6; [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 8
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

PDI dos colaboradores e trilhas de desenvolvimento.

## 3. Telas

- **PDIs** (lista).
- **PDI — detalhe** (metas, ações, evidências).

## 4. Permissões por portal (extraídas do SDD)

Do [37](../../../docs/v2/37-planejamento-e-empenho.md):

| Portal | Planejamento acadêmico | Planejamento institucional | Desenvolvimento de pessoas | Empenho |
|---|---|---|---|---|
| Gestão | Completo, por permissão | Completo, por permissão | Completo, por permissão | Completo, para entidade pública, por permissão |

## 5. Papéis

- `unit.hr`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 4.

## 7. Dados

- Tabelas e campos conforme a seção 13 e o DDL do [51](../../../docs/v2/51-ddl-modulos-novos.md), quando o módulo estiver lá. Toda tabela tem `entidade_id`, `unidade_id`, `created_at`, `updated_at`, `created_by` e exclusão lógica com `deleted_at` e `deleted_by` ([03](../../../docs/v2/03-dominio-tenancy.md), seção 6; [15](../../../docs/v2/15-validacoes.md); [19](../../../docs/v2/19-regras-modulos-3.md), seção 14).

## 8. Integrações

- Ver a seção de integrações do documento de origem, na seção 13.

## 9. Exportação, auditoria e privacidade

- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Toda criação, alteração, aprovação, exclusão lógica, exportação e leitura de dado sensível gera evento de auditoria no banco da unidade ([29](../../../docs/v2/29-auditoria.md)).
- Dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md): mínimo necessário, mascaramento em listas, base legal registrada.

## 10. Estados de interface

- Carregando (skeleton), vazio com chamada para ação, sem resultado de filtro, erro com nova tentativa, acesso negado, registro bloqueado, fechado ou baixado (somente leitura), conflito de edição (versão).

## 11. Requisitos de frontend

- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`): página de lista com DataTable, KPIs, drawer de detalhe, formulário em página ou modal, kanban quando houver fluxo de estados.
- Seletor de unidade no topo quando o usuário tiver mais de uma; a troca reemite o token com o novo contexto ([06](../../../docs/v2/06-identidade-acesso.md), seção 12).

## 12. Critérios de aceite e pendências

- Critérios de aceite: os do documento de origem (seção 13) e os de [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 6.
- Testes de isolamento: usuário de outra unidade ou entidade recebe 404 em toda rota do módulo ([03](../../../docs/v2/03-dominio-tenancy.md)).
- As pendências do documento de origem estão na seção 13 e consolidadas no [45](../../../docs/v2/45-pendencias-consolidadas.md).

## 13. Regras da v2 (texto integral das fontes, sem corte)

### 13.1 [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 4

#### 4. Planejamento de desenvolvimento de pessoas

##### 4.1 Entidades

| Entidade | Função |
|---|---|
| Plano de desenvolvimento | Por colaborador, com período e metas de formação e carreira |
| Ação de formação | Curso, treinamento ou certificação, com carga horária |
| Trilha | Conjunto de ações para um cargo |
| Avaliação de competência | Resultado por competência, vinculado ao ciclo de avaliação de desempenho |

##### 4.2 Estados

Plano: `rascunho` → `pactuado` → `em_execucao` → `concluido`. Pactuado exige assinatura do colaborador e do gestor. Ação de formação: `prevista` → `realizada` → `comprovada`.

##### 4.3 Regras

- Plano sem assinatura do colaborador não entra em execução.
- Ação `realizada` sem comprovante não vira `comprovada`.
- Carga horária comprovada alimenta o registro de formação do colaborador ([18](../../../docs/v2/18-regras-modulos-2.md), seção 3).
- Avaliação de competência não altera nota de desempenho. Os dois são registros separados.
- Dado de saúde ou de afastamento não entra no plano ([07](../../../docs/v2/07-privacidade-lgpd.md), seção 2).

### 13.2 [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 6

#### 6. Portais

| Portal | Planejamento acadêmico | Planejamento institucional | Desenvolvimento de pessoas | Empenho |
|---|---|---|---|---|
| Desenvolvedor | Nenhum | Plano institucional da própria empresa, se houver | Nenhum | Nenhum |
| Gestão | Completo, por permissão | Completo, por permissão | Completo, por permissão | Completo, para entidade pública, por permissão |
| Professor | Carga e turmas próprias, somente leitura | Nenhum | Plano próprio | Nenhum |
| Aluno | Oferta publicada e calendário, somente leitura | Nenhum | Nenhum | Nenhum |
| Responsáveis | Calendário e oferta publicada, somente leitura | Nenhum | Nenhum | Nenhum |
| Terceiros | Nenhum | Nenhum | Nenhum | Recebe pagamento liquidado. Ver [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 8 |

### 13.3 [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 8

#### 8. Estrutura de dados mínima

Tabelas com `tenant_id` e índice composto ([03](../../../docs/v2/03-dominio-tenancy.md)). Valores monetários em centavos ([20](../../../docs/v2/20-pagamentos-seguranca.md), seção 4).

```sql
CREATE TABLE plan_strategic_goals (
  id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid         CHAR(36)     NOT NULL,
  tenant_id    CHAR(36)     NOT NULL,
  plan_id      BIGINT UNSIGNED NOT NULL,
  title        VARCHAR(200) NOT NULL,
  status       VARCHAR(30)  NOT NULL,
  owner_uuid   CHAR(36)     NULL,
  created_at   DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  UNIQUE KEY uk_goal_uuid (uuid),
  INDEX idx_tenant_plan (tenant_id, plan_id, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE budget_commitments (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36)     NOT NULL,
  tenant_id       CHAR(36)     NOT NULL,
  unit_id         CHAR(36)     NOT NULL,
  fiscal_year     SMALLINT     NOT NULL,
  budget_line     VARCHAR(40)  NOT NULL,
  modality        ENUM('ordinario','estimativo','global') NOT NULL,
  creditor_uuid   CHAR(36)     NOT NULL,
  amount_cents    BIGINT       NOT NULL,
  status          VARCHAR(30)  NOT NULL,
  supporting_doc  VARCHAR(255) NULL,
  created_by      CHAR(36)     NOT NULL,
  approved_by     CHAR(36)     NULL,
  created_at      DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  UNIQUE KEY uk_commitment_uuid (uuid),
  INDEX idx_tenant_year_line (tenant_id, fiscal_year, budget_line),
  CHECK (amount_cents > 0),
  CHECK (created_by <> approved_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Notas:

- `CHECK (created_by <> approved_by)` garante a segregação. A aplicação também valida, para dar mensagem clara.
- Liquidação e pagamento são tabelas próprias, com chave para o empenho, e não colunas de `budget_commitments`.
- Restos a pagar processado ou não processado não é coluna: sai da existência de liquidação do empenho em 31 de dezembro (seção 5.3).
- Dotação é tabela própria, por exercício e rubrica. A soma de empenhos ativos não pode passar da dotação. Essa regra é validada na transação de emissão.
