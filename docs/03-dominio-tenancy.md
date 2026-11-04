# 03 — Domínio e Multi-Tenancy

> Parte do [SDD v2](00-README.md).

---

## 1. Hierarquia

```
Plataforma (host)
 └─ Mantenedora (client)          — contratante do SaaS
     └─ Entidade (entity)         — instituição / razão social
         └─ Unidade (unit)        — campus, filial, polo
             └─ Usuários, papéis e vínculos
```

- A **plataforma** é um tenant reservado, identificado por código de seed. Seus administradores são **contas de plataforma** (ver [06](06-identidade-acesso.md), seção 10), não usuários comuns com flag.
- Cada nível herda configuração do nível superior e pode sobrescrevê-la onde a política permitir.

## 1.1 Bancos de dados

**Decisão do autor (02/11/2026, D-16):** um banco por unidade. A entidade não tem banco próprio de dados operacionais.

**Banco master (desenvolvedor):**

- Nome lógico: `totustuus.matriz.bd`. Único, da plataforma.
- Contém: catálogo de entidades e unidades, registro de bancos (seção abaixo), contas de plataforma, conexões de integração de plataforma, CRM da plataforma ([22](22-crm-canais-e-papeis.md)) e índice de pessoas (`person_id`, e-mail verificado).
- Não contém cadastro civil nem dado operacional de unidade. O cadastro civil fica no banco de identidade da entidade (D-19, [14](14-integracao-modulos.md), seção 3). Notas, financeiro, matrícula, folha e arquivos ficam no banco da unidade.

**Banco de unidade (um por entidade + unidade):**

- Nome lógico: `{entidade}.{unidade}.bd.{uuid}`. Exemplos:

| Entidade | Unidade | Número operacional | Nome lógico |
|---|---|---|---|
| Colégio Santo Antonio | Sede | 001 | `colegio-santo-antonio.sede.bd.{uuid}` |
| Colégio Santo Antonio | Mateus Leme | 002 | `colegio-santo-antonio.mateus-leme.bd.{uuid}` |
| Colégio Santo Agostinho | Sede | 003 | `colegio-santo-agostinho.sede.bd.{uuid}` |

- Nome físico no servidor: `tt_001`, `tt_002`, `tt_003`. O ponto do nome lógico não é usado no servidor, porque complica ferramentas, permissões e backup. O mapeamento fica no registro do master.
- Conteúdo: alunos, colaboradores, financeiro, acadêmico, CRM do tenant ([22](22-crm-canais-e-papeis.md)), metadados de arquivos ([21](21-busca-e-armazenamento.md)), auditoria local e outbox de eventos ([14](14-integracao-modulos.md)).

**Registro de bancos (no master):**

| Campo | Regra |
|---|---|
| `uuid` | UUIDv4 gerado pela aplicação |
| `entity_uuid`, `unit_uuid` | Obrigatórios; único por par entidade e unidade |
| `logical_name` | Único |
| `physical_name` | Único no servidor, no formato `tt_<seq>` |
| `seq` | Sequencial de três dígitos, único |
| `host` | Servidor onde o banco está |
| `status` | `ativo`, `migrando`, `suspenso` |
| `schema_version` | Versão de esquema aplicada |

**Resolução de conexão:**

1. Usuário autentica no master, com conta global ([06](06-identidade-acesso.md), seção 12).
2. O master lista os vínculos ativos da conta (entidade, unidade e papel).
3. A requisição escolhe uma unidade. Sem unidade permitida, a resposta é `403`.
4. A conexão é aberta somente no banco dessa unidade.

**Consequências que dependem de decisão:**

- **Relatório consolidado da entidade** (todas as unidades): não é consulta entre bancos. É um modelo de leitura alimentado por eventos ([14](14-integracao-modulos.md)).
- **Pessoa única entre unidades** (D-06): bancos separados impedem unicidade direta. Ver D-19 em [14](14-integracao-modulos.md), seção 3.
- **Eventos entre unidades:** a outbox fica no banco da unidade emissora. A entrega ao consumidor de outra unidade passa por fila central, com destino por `unit_uuid`.
- **Migrações:** rodam em cada banco de unidade, com registro de versão por banco ([10](10-implantacao-operacao.md), seção 5).
- **Operação:** o número de bancos cresce com as unidades. Limites de conexão, backup e monitoramento são por banco.

**Testes:**

- Usuário com acesso à unidade 001 não lê dado da unidade 002, mesmo com identificador exato.
- Consulta que tenta trocar o banco por parâmetro é recusada.
- Migração que falha em um banco não bloqueia os demais, e o banco fica em `migrando` até concluir.

## 2. Identificadores

- Chaves públicas são **UUIDv4** gerados com CSPRNG (`random_bytes(16)`), nunca sequenciais.
- Identificadores internos de seed (códigos de tenant, entidade, unidade da plataforma) são definidos em **registro privado de seed**, não no SDD. A v1 reproduzia esses valores e os e-mails dos administradores; a v2 os remove (ver [13-achados-v1.md](13-achados-v1.md), ACH-03).
- UUIDs nulos ou fixos só são permitidos em fixtures de teste, nunca em dados de produção.

## 3. Isolamento de tenant

Regras obrigatórias:

1. **Toda tabela multi-tenant tem `tenant_id` NOT NULL** e índice composto que começa por `tenant_id`.
2. **Toda consulta** aplica `tenant_id = :current` no repositório. Não existe consulta "global" sem uma classe de exceção nomeada e auditada.
3. **Chave de tenant vem do contexto autenticado**, nunca de cabeçalho ou parâmetro livre (`X-Tenant-ID` não é aceito como fonte de verdade). Na tela de entrada, o tenant informado por subdomínio ou formulário é validado contra a lista de hosts permitidos; host desconhecido retorna `404`.
4. **Conta global com vínculos.** A pessoa tem uma conta no master e recebe contexto de uma entidade e unidade só por vínculo ativo (ver [06](06-identidade-acesso.md), seção 12). Autenticar não concede acesso a nenhuma unidade.
5. **Cache, filas, uploads e logs** carregam `tenant_id` na chave ou no registro.
6. **Teste de isolamento obrigatório:** para cada endpoint de leitura e escrita, um teste com usuário de tenant B tentando acessar recurso de tenant A deve retornar `404` (não `403`, para não revelar existência).

## 4. Escopo de unidade

- `UserUnit` limita o usuário a unidades específicas. Acesso `full` cobre todas as unidades da entidade.
- Permissões de unidade são avaliadas junto com a permissão de módulo. Permissão de módulo sem vínculo de unidade não basta para dados daquela unidade.

## 5. Configuração por tenant

| Configuração | Escopo | Observação |
|---|---|---|
| Marca (logo, cores, nome) | Entidade | Validação de imagem (ver [05](05-seguranca.md)) |
| Locale padrão e moeda | Entidade | Moeda USD/BRL é **[Declarado]**; outras moedas dependem de requisito |
| Política de senha e MFA | Mantenedora ou entidade | Não pode ser menos restritiva que a política da plataforma |
| Retenção de dados | Entidade | Mínimo e máximo definidos pela plataforma ([07](07-privacidade-lgpd.md)) |
| Limites de API | Tenant | Ver [04](04-api.md) |

## 6. Regras de negócio transversais

- Exclusão é **lógica** por padrão (`deleted_at`). Exclusão física só pelo processo de retenção ou pedido do titular.
- Toda alteração de vínculo (papel, unidade, permissão) gera registro de auditoria com antes e depois.
- Um usuário pode ter vínculos em mais de um tenant, mas cada sessão opera em um único tenant por vez.

## 7. Testes de tenancy (critério de aceite)

- [ ] Matriz de isolamento: todos os endpoints × dois tenants × papéis relevantes.
- [ ] Teste de regressão para cada incidente de cross-tenant registrado.
- [ ] Teste de enumeração de identificadores (UUIDs de outro tenant não retornam dados nem mensagens diferentes de "não encontrado").
