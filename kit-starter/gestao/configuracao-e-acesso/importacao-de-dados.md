# Importação de dados

- Portal: Gestão (`gestao.`)
- Área: Configuração e acesso
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13); especificação da v1 absorvida integralmente (seção 14)
- Fonte da v2: [70](../../../docs/v2/70-importacao-de-dados-por-portal.md) (integral); [19](../../../docs/v2/19-regras-modulos-3.md), seção 13
- Fonte da v1: [client-migration-module-spec-completo.md](../../../docs/v2/anexo-v1/client-migration-module-spec-completo.md) (1207 linhas) — absorvida integralmente na seção 14

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. A seção 14 é o texto integral da v1, guardado para que nenhum detalhe se perca; quando ela disser algo diferente das seções 1 a 13, vale a v2. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Importar dados de sistema anterior em ordem de dependência, com modelos de arquivo, validação, pré-visualização e relatório.

## 3. Telas

- **Importações** (lista).
- **Nova importação** (assistente: tipo, modelo, upload, validação, pré-visualização, confirmação).
- **Relatório de erros** (download).

## 4. Permissões por portal (extraídas do SDD)

Do [70](../../../docs/v2/70-importacao-de-dados-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Autorizar a importação inicial. Ver o relatório de lote | Importar sem a secretaria. Ver dado sensível do arquivo | E |
| **Secretaria** | Importar pessoas, estrutura, turmas, matrículas, documentos e acervo. Desfazer lote | Importar histórico sem a coordenação. Importar saldo sem o financeiro | E |
| **Coordenação** | Importar histórico de período fechado, com aprovação | Importar pessoa ou matrícula | E |

## 5. Papéis

- `entity.admin`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- [70](../../../docs/v2/70-importacao-de-dados-por-portal.md); migração de clientes ([19](../../../docs/v2/19-regras-modulos-3.md), seção 13).

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

### 13.1 [70 — Importação de Dados e Carga Inicial, por Portal](../../../docs/v2/70-importacao-de-dados-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Décima terceira e última lacuna da ordem de [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), seção 3. Regra geral de importação (simulação, erro por linha, limite e idempotência) em [15](../../../docs/v2/15-validacoes.md), seção 5. Carga de sistema legado por arquivo, sem acesso direto ao banco de terceiros, em [16](../../../docs/v2/16-integracoes-externas.md). Cada tipo de dado segue o módulo de origem: estrutura ([59](../../../docs/v2/59-estrutura-academica-por-portal.md)), turmas ([60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md)), matrícula ([46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md)), diário e boletim ([61](../../../docs/v2/61-diario-escolar-por-portal.md), [62](../../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md)), prontuário ([66](../../../docs/v2/66-prontuario-e-portfolio-do-aluno-por-portal.md)), biblioteca ([68](../../../docs/v2/68-biblioteca-por-portal.md)) e financeiro ([18](../../../docs/v2/18-regras-modulos-2.md)). Notificação em massa em [57](../../../docs/v2/57-notificacoes-por-portal.md). Auditoria em [29](../../../docs/v2/29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna 13 do acadêmico. A v1 tem importação em lote por CSV com validação e relatório de erros ([`spec_gestao_academica_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_academica_completo.md), seção 15). Esta versão define a ordem, as regras de domínio e o que a importação não pode fazer.

---

#### 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Importação tem regra? | **Parcial.** A regra geral de [15](../../../docs/v2/15-validacoes.md) existe. Falta ordem por tipo, regra de domínio e tratamento do histórico |
| Carga de sistema anterior? | **Parcial.** [16](../../../docs/v2/16-integracoes-externas.md) proíbe acesso direto ao banco de terceiro. Falta o processo |
| Importação pode contornar regra? | **Não, por regra desta especificação.** Ver seção 3 |

---

#### 2. Tipos e ordem

A ordem segue a dependência. Nenhum tipo entra antes do que ele referencia.

| Ordem | Tipo | Depende de | Módulo |
|---|---|---|---|
| 1 | Pessoas: alunos, responsáveis, professores, servidores | Nada | [14](../../../docs/v2/14-integracao-modulos.md), seção 3 e [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md) |
| 2 | Estrutura: tipos de curso, cursos, disciplinas, grades, sistema avaliativo, períodos | 1 | [59](../../../docs/v2/59-estrutura-academica-por-portal.md) |
| 3 | Calendário e salas | 2 | [58](../../../docs/v2/58-calendario-e-eventos-por-portal.md), [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md) |
| 4 | Turmas e enturmação | 2 e 3 | [60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md) |
| 5 | Matrículas ativas | 1, 2 e 4 | [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md) |
| 6 | Histórico: notas, faltas, situação final de períodos fechados | 4 e 5 | [61](../../../docs/v2/61-diario-escolar-por-portal.md), [62](../../../docs/v2/62-boletim-e-conselho-de-classe-por-portal.md) |
| 7 | Documentos e prontuário | 1 | [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), [66](../../../docs/v2/66-prontuario-e-portfolio-do-aluno-por-portal.md) |
| 8 | Acervo da biblioteca | 2 | [68](../../../docs/v2/68-biblioteca-por-portal.md) |
| 9 | Saldos e parcelas em aberto | 5 | [18](../../../docs/v2/18-regras-modulos-2.md) |

---

#### 3. O que a importação não faz

A importação entra pelos mesmos caminhos de regra que a tela. Por isso:

- **Nota fora da escala** é recusada, como na tela ([59](../../../docs/v2/59-estrutura-academica-por-portal.md), seção 4).
- **Matrícula acima da capacidade** vai para a lista de espera ou é recusada com motivo ([60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md), seção 2.4).
- **Aluno sem vínculo válido** de responsável não é importado como ativo ([07](../../../docs/v2/07-privacidade-lgpd.md)).
- **Histórico não recalcula regra de período fechado.** A situação final vem do arquivo, com a versão do sistema avaliativo que o arquivo declara. Se a versão não existe no sistema, a linha é rejeitada.
- **Não gera cobrança retroativa.** Parcela já paga na origem entra como paga. Parcela em aberto entra com a data da origem, sem nova multa.
- **Não dispara aviso em massa.** Carga histórica entra com flag de histórico, e nenhuma notificação é enviada por ela ([57](../../../docs/v2/57-notificacoes-por-portal.md)).

---

#### 4. Processo

1. **Modelo.** A plataforma publica um modelo de arquivo por tipo, com cabeçalho, tipos de campo e chave externa de origem. Ver seção 4.1.
2. **Envio.** O arquivo é enviado com tamanho e tipo validados ([15](../../../docs/v2/15-validacoes.md), seção 5).
3. **Simulação.** O sistema valida tudo e mostra o relatório, sem gravar. Mostra quantas linhas entram, quantas são rejeitadas e por quê.
4. **Confirmação.** A pessoa que importa confirma o lote. A confirmação fica em auditoria.
5. **Gravação.** O lote grava em transação por lote. Linha rejeitada não bloqueia as outras, mas o lote fica marcado como parcial.
6. **Desfazer.** O lote pode ser desfeito enquanto não houver registro posterior dependente dele. Depois disso, só correção por novo lote.
7. **Rejeitados.** Relatório de rejeitados, com linha e motivo, para correção e novo envio.
8. **Descarte do arquivo.** O arquivo de origem é apagado após a gravação, e fica só o hash e o relatório. Prazo em IMP-04.

**Idempotência:** a chave externa de origem evita duplicar o mesmo registro em reenvio. Reenvio do mesmo lote não cria registro novo.

##### 4.1 Modelos de arquivo (IMP-05)

**Formato comum a todos os modelos:**

| Item | Regra |
|---|---|
| Arquivos | Planilha (`.xlsx`, uma aba por modelo) e CSV. Os dois têm as mesmas colunas, na mesma ordem |
| CSV | UTF-8, separador ponto e vírgula, primeira linha com o nome das colunas |
| Data | `AAAA-MM-DD`. Data em outro formato é recusada, para não confundir dia e mês |
| Número | Vírgula como separador decimal, sem separador de milhar |
| Valor em dinheiro | Reais com duas casas. O sistema converte para centavos ([71](../../../docs/v2/71-financeiro-completo-por-portal.md)) |
| CPF | Só dígitos, com dígito verificador conferido ([15](../../../docs/v2/15-validacoes.md)) |
| Chave externa | Coluna `chave_origem` obrigatória em todo modelo. É o identificador no sistema anterior e garante a idempotência |
| Versão | Cada modelo tem versão no nome do arquivo e numa linha de comentário da planilha. Arquivo de versão que já saiu do prazo de aceitação (ver Publicação, abaixo) é recusado com aviso da versão atual |
| Coluna a mais | Recusada, para não esconder dado que não tem destino. Campo personalizado entra pela coluna com a chave do campo ([72](../../../docs/v2/72-campos-personalizados-por-portal.md)) |

**Colunas obrigatórias por modelo**, na ordem da seção 2:

| Modelo | Colunas obrigatórias | Observação |
|---|---|---|
| 1. Pessoas | `chave_origem`, `tipo_pessoa`, `nome`, `cpf` ou `documento_estrangeiro`, `nascimento`, `email` ou `telefone` | Responsável tem `chave_origem_dependente` e `tipo_vinculo`. Aluno menor sem responsável não fica ativo (seção 3) |
| 2. Estrutura | `chave_origem`, `tipo_registro` (curso, disciplina, grade, período), `codigo`, `nome`, `carga_horaria` | Sistema avaliativo é configurado na tela, não importado |
| 3. Calendário e salas | `chave_origem`, `tipo_registro` (dia, período, sala), `data_ou_codigo`, `descricao` | Sala tem `capacidade` |
| 4. Turmas e enturmação | `chave_origem`, `codigo_turma`, `curso`, `periodo`, `turno`, `capacidade`, `chave_origem_aluno` | Enturmação usa uma linha por aluno |
| 5. Matrículas | `chave_origem`, `chave_origem_aluno`, `codigo_turma`, `data_matricula`, `situacao` | Só matrícula ativa. Capacidade segue a seção 3 |
| 6. Histórico | `chave_origem`, `chave_origem_aluno`, `periodo`, `disciplina`, `nota_final`, `faltas`, `situacao_final`, `versao_sistema_avaliativo` | Só período fechado. Aprovação da coordenação (seção 6) |
| 7. Documentos | `chave_origem`, `chave_origem_pessoa`, `tipo_documento`, `nome_arquivo` | O arquivo vai num pacote compactado junto, com o mesmo nome. Dado de saúde segue IMP-03 |
| 8. Acervo | `chave_origem`, `titulo`, `autor`, `isbn` ou `codigo_interno`, `exemplares` | Item sem ISBN usa código interno |
| 9. Saldos e parcelas | `chave_origem`, `chave_origem_matricula`, `vencimento`, `valor`, `situacao` (paga, em aberto), `data_pagamento` | Sem multa nova (seção 3). Aprovação do financeiro |

**Publicação:** o portal do desenvolvedor publica os modelos, sem dado. A empresa aprova cada versão antes da publicação. Mudança de coluna gera nova versão, e a anterior continua aceita por 90 dias.

---

#### 5. Dado sensível e dado de terceiros

- Laudos, diagnósticos e dados de saúde só são importados se a regra de [66](../../../docs/v2/66-prontuario-e-portfolio-do-aluno-por-portal.md), seção 2.3, permitir. Ver IMP-03.
- Arquivo de origem tem dado pessoal. Fica em armazenamento restrito, cifrado, pelo tempo do processo.
- Nenhum acesso direto ao banco do sistema anterior ([16](../../../docs/v2/16-integracoes-externas.md)).

---

#### 6. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelos de arquivo, sem dado. Orientar a importação | Importar ou ver dado de entidade, nem o conteúdo de lote | P |
| **Gestão** | Autorizar a importação inicial. Ver o relatório de lote | Importar sem a secretaria. Ver dado sensível do arquivo | E |
| **Secretaria** | Importar pessoas, estrutura, turmas, matrículas, documentos e acervo. Desfazer lote | Importar histórico sem a coordenação. Importar saldo sem o financeiro | E |
| **Coordenação** | Importar histórico de período fechado, com aprovação | Importar pessoa ou matrícula | E |
| **Financeiro** (perfil da unidade) | Importar saldos e parcelas em aberto | Importar notas ou documentos | E |
| **Professor** | Nada | Qualquer item de importação | E |
| **Aluno** | Nada | Qualquer item de importação | E |
| **Responsáveis** | Nada | Qualquer item de importação | E |
| **Terceiros** | Nada | Qualquer item de importação | E |

---

#### 7. Pendências

| # | Pendência | Tipo |
|---|---|---|
| IMP-01 | Quem executa a importação inicial (seção 6) | **Decidido** em 03/11/2026: a entidade, pela secretaria. A equipe da empresa só orienta |
| IMP-02 | Histórico importado gera notificação (seção 3) | **Decidido** em 03/11/2026: não |
| IMP-03 | Laudos e dados de saúde na importação: aceitar, ou bloquear e tratar na seção de saúde | (jurídico) |
| IMP-04 | Prazo de retenção do arquivo de origem depois da gravação (seção 4, passo 8) | (jurídico) |
| IMP-05 | Modelos de arquivo por tipo: publicar em planilha e em CSV | **Escrito** na seção 4.1. Revisão do owner pendente: a empresa aprova cada versão |
| IMP-06 | DDL: lote, linha, erro, chave externa, mapeamento de campo e histórico de desfazer | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 15.15. Revisão do owner pendente (DDL-01) |

---

#### 8. Critérios de aceite

- [ ] Simulação não grava nenhuma linha (teste).
- [ ] Reenvio do mesmo lote não duplica registro (teste de idempotência).
- [ ] Nota fora da escala é rejeitada na importação (teste de integração com [59](../../../docs/v2/59-estrutura-academica-por-portal.md)).
- [ ] Matrícula acima da capacidade não entra como ativa (teste).
- [ ] Histórico com versão de sistema avaliativo inexistente é rejeitado (teste).
- [ ] Importação de histórico não dispara notificação (teste de integração com [57](../../../docs/v2/57-notificacoes-por-portal.md)).
- [ ] Arquivo de origem é apagado depois da gravação e fica só o hash (teste).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).

### 13.2 [19](../../../docs/v2/19-regras-modulos-3.md), seção 13

#### 13. Client migration

| Regra | Detalhe |
|---|---|
| Checksum | Hash de cada arquivo enviado (linha 316). Divergência é erro (linha 353). |
| Segredos | Credenciais não são migradas em texto. Hash ou recadastro (linha 553). |
| Idempotência | Token por execução de job (linha 687) e chave por registro (linha 869). |
| Isolamento | Migração de dados entre tenants exige revisão de isolamento ([17](../../../docs/v2/17-regras-modulos.md), seção 1). |

**Defeito:** sem DDL (T-02).

## 14. Conteúdo integral da v1 (absorvido)

### Client Migration Module Specification

#### 1. Document Control

- Document Name: Client Migration Module Specification
- Product Context: Multi-tenant SaaS platform using Supabase-inspired admin UX patterns
- Target Stack: PHP, Fetch API, MariaDB, JSON-based migration intake
- Language Standard: Global English
- Primary Audience: Product owner, backend engineers, frontend engineers, database engineers, QA, DevOps, security reviewers
- Module Type: Admin-only operational module
- Status: Draft v1.0

#### 2. Purpose

This module enables an administrator to onboard a new client that is migrating from a legacy system into the platform.

The client provides a structured JSON migration package containing source schema metadata, table definitions, field definitions, relationships when available, and optionally sample records or transformation hints. The module presents a dual-schema mapping workspace where the platform schema appears in one column and the client legacy schema appears in a second column, allowing controlled mapping of tables, columns, keys, enums, reference values, and transformation rules.

The module must support semi-automated matching so that the system proposes likely mappings first, and the administrator performs a review and final approval pass before execution.

#### 3. Goals

- Standardize onboarding migrations for new clients.
- Reduce manual mapping effort by auto-suggesting table and field matches.
- Preserve data integrity during legacy-to-platform conversion.
- Provide a visual schema exploration experience similar to a schema visualizer.
- Support repeatable, auditable, and reversible migration planning.
- Minimize migration errors caused by naming mismatches, datatype mismatches, enum drift, and broken foreign-key relationships.
- Produce a clear migration execution plan before any production write occurs.

#### 4. Non-Goals

- This module is not intended to replace raw DBA tooling for unrestricted database administration.
- This module is not a generic ETL studio for arbitrary third-party destinations.
- This module is not a no-code workflow engine.
- This module should not allow direct execution against production targets without validation, review, and authorization gates.

#### 5. Business Context

A new client often comes from a different software vendor, internal legacy application, spreadsheets, or custom databases. Their data model rarely matches the platform model one-to-one. The migration module must bridge this gap by creating explicit mappings between:

- Source tables and target tables.
- Source columns and target columns.
- Source coded values and target normalized values.
- Source relationships and target foreign keys.
- Source identifiers and target UUID or internal ID strategy.

The module must support highly structured enterprise onboarding where traceability, reproducibility, and compliance are mandatory.

#### 6. Primary Users

##### 6.1 Platform Super Admin

Can create migration projects, upload JSON packages, review schema suggestions, approve execution, monitor jobs, and download audit artifacts.

##### 6.2 Migration Analyst

Can inspect mappings, adjust transforms, validate referential integrity issues, run dry runs, and submit for approval.

##### 6.3 Client Technical Contact

May provide the JSON package and optionally review non-sensitive mapping previews, but should not have unrestricted administrative permissions by default.

##### 6.4 Compliance / Audit Reviewer

Can read migration logs, validation reports, and execution evidence.

#### 7. Module Scope

The module includes:

- Migration project creation.
- JSON import and schema parsing.
- Source schema visualization.
- Target schema visualization.
- Automated mapping suggestions.
- Manual mapping review and override.
- Transformation rule management.
- Validation engine.
- Dry run engine.
- Execution orchestration.
- Logging, audit, rollback metadata, and reporting.

#### 8. High-Level Workflow

1. Admin creates a new migration project.
2. Admin selects tenant/client context.
3. Admin uploads or pastes the JSON migration package.
4. System validates JSON structure and required metadata.
5. System parses source schema, tables, fields, indexes, relationships, enums, and source constraints.
6. System loads the current target platform schema from MariaDB metadata.
7. System renders a dual-column schema workspace.
8. System generates automatic table match suggestions.
9. System generates automatic column match suggestions within each mapped table pair.
10. Admin reviews unmatched, low-confidence, and conflict items.
11. Admin defines transforms, defaults, lookups, enum remaps, and key strategies.
12. System runs validation.
13. System runs dry run against staging or isolated migration schema.
14. Admin reviews reports.
15. Authorized admin approves live execution.
16. System executes migration in controlled phases.
17. System stores complete audit trail and post-migration report.

#### 9. Functional Overview

The module should behave like a Supabase-style schema visualizer plus a guided migration planner.

Core UX idea:

- Left workspace: full target system schema.
- Right workspace: full client source schema.
- Connection layer: visual lines or link cards showing mapped table pairs.
- Within a selected table pair: side-by-side field mapping grid.
- Confidence badges: auto-match confidence shown as High, Medium, Low.
- Review queue: unresolved or risky items listed separately.

#### 10. UI Architecture

##### 10.1 Main Screens

- Migration Projects List
- Create Migration Project
- Migration Project Overview
- Schema Visualizer and Mapping Workspace
- Field Mapping Editor
- Transformation Rules Editor
- Validation Report Screen
- Dry Run Results Screen
- Execution Console
- Audit and Reports Screen

##### 10.2 Migration Project Overview

Sections:

- Client identity
- Migration package metadata
- Source system name and version
- Source database type
- Import timestamp
- Mapping completion percentage
- Validation status
- Dry run status
- Execution status
- Last updated by
- Risk summary

##### 10.3 Schema Visualizer Workspace

Layout recommendation:

- Left panel: target schema tree
- Center canvas: mapping graph / relationship lines
- Right panel: source schema tree
- Bottom panel: details inspector or mapping queue
- Top bar: search, filter, confidence filter, status filter, auto-match actions, save draft, validate, dry run, execute

##### 10.4 Table Mapping View

Each side shows:

- Table name
- Schema/group
- Row estimate if available
- Primary key
- Foreign keys count
- Columns count
- Last import timestamp for source
- Tags such as core, financial, academic, identity, medical, lookup, audit

Actions:

- Map table
- Ignore table
- Mark table as derived
- Mark table as archival only
- Split source table into multiple target tables
- Merge multiple source tables into one target table

##### 10.5 Field Mapping View

Each row in the mapping grid should support:

- Target field name
- Target datatype
- Required flag
- Unique flag
- FK target if applicable
- Source field suggestion
- Source datatype
- Transform type
- Default value
- Null handling
- Confidence score
- Validation notes
- Approval status

#### 11. JSON Migration Package Specification

##### 11.1 Supported Input Modes

- JSON file upload.
- JSON paste in text area.
- SQL file upload.
- XML file upload.
- CSV file upload.
- XLS or XLSX file upload.
- API submission from secure client endpoint.

##### 11.2 Top-Level JSON Structure

```json
{
  "meta": {
    "source_system": "Legacy ERP",
    "source_version": "4.2.1",
    "database_type": "mysql",
    "exported_at": "2026-07-10T09:00:00Z",
    "timezone": "UTC",
    "locale": "en-US"
  },
  "client": {
    "external_client_code": "ACME-001",
    "client_name": "Acme Health Group"
  },
  "schema": {
    "tables": []
  },
  "data": {
    "tables": []
  },
  "mapping_hints": {
    "table_aliases": [],
    "field_aliases": [],
    "enum_maps": []
  }
}
```

##### 11.3 Minimum Required Source Schema Elements

- Source table name
- Source column name
- Source datatype
- Nullable flag if available
- Primary key indication if available
- Foreign key reference if available
- Source row count estimate if available

##### 11.4 Recommended Optional Elements

- Column description
- Friendly label
- Sample values
- Enum values
- Index metadata
- Relationship cardinality
- Legacy code meanings
- Deprecated field markers
- Source timezone metadata
- Source encoding metadata

#### 11.5 Additional Accepted Source Formats

The migration module must also accept the following source formats in addition to JSON:

- SQL scripts.
- XML files.
- CSV files.
- XLS or XLSX spreadsheets.

Each format must be converted into the same internal migration package model before mapping, validation, and execution. The UI must keep the same dual-schema workspace regardless of source format.

##### 11.6 Format-Specific Parsing Rules

- SQL: Parse DDL and optionally DML to extract tables, columns, constraints, indexes, and seed rows when allowed.
- XML: Parse hierarchical nodes into tabular source entities using configurable XPath or node-path rules.
- CSV: Infer headers, delimiters, quoting, encoding, and data types from uploaded files.
- XLS/XLSX: Read worksheet names, header rows, merged cells where relevant, and detect table-like ranges.

##### 11.7 Normalization Pipeline

All supported file types must be normalized into:

- source tables.
- source columns.
- sample values.
- relationship hints.
- enum/value candidates.
- metadata tags.

This normalization step must happen before auto-matching.

##### 11.8 Format Validation

The import layer must validate each format before parsing completes:

- SQL files must be checked for supported dialect and dangerous statements.
- XML files must be checked for well-formed structure.
- CSV files must be checked for delimiter consistency and header integrity.
- XLS/XLSX files must be checked for readable sheets and non-empty headers.

#### 12.1 Upload Security and File Integrity

All uploads must be treated as untrusted input until proven otherwise.

Requirements:

- Validate file extension, MIME type, and declared format.
- Enforce size limits per file type and per migration project.
- Store uploaded files in a temporary quarantine area before parsing.
- Scan files for malware or suspicious payloads when the pipeline supports it.
- Reject executable content, embedded scripts, and active content where applicable.
- Compute and store a checksum or hash for each uploaded file.
- Log upload source, uploader identity, timestamp, and correlation ID.
- Prevent public access to raw uploaded files.

#### 12.2 Parsing Error Handling

The parser must fail safely and return structured error feedback.

Error handling rules:

- Stop parsing immediately when a fatal format error is detected.
- Capture file name, format, project ID, and a stable error code.
- Include line, column, sheet, node, or statement references when available.
- Distinguish between recoverable warnings and blocking parsing errors.
- Store parsing errors in the migration audit trail.
- Keep the original upload untouched for review and reprocessing.

Recommended parser error categories:

- INVALID_JSON
- INVALID_XML
- INVALID_CSV_HEADER
- INVALID_CSV_DELIMITER
- INVALID_XLS_STRUCTURE
- UNSUPPORTED_SQL_DIALECT
- SQL_SYNTAX_ERROR
- EMPTY_FILE
- UNREADABLE_FILE
- INCONSISTENT_ENCODING

#### 12.3 Corrupted File Handling

The system must detect and isolate corrupted files before they enter the mapping workflow.

Corruption signals include:

- Truncated file content.
- Hash mismatch.
- Broken archive structure.
- Unreadable workbook sheets.
- Invalid XML tree structure.
- Incomplete CSV rows due to file damage.
- Missing table or worksheet metadata expected for the declared format.

When corruption is detected:

- Mark the upload as corrupted.
- Block parsing and mapping.
- Preserve technical evidence for audit.
- Notify the admin with a clear remediation message.
- Allow the user to re-upload a corrected file.

#### 12.4 Upload Threat Model

The module must protect against common upload threats:

- Path traversal.
- Content spoofing.
- Zip bombs or decompression abuse.
- Oversized payload attacks.
- Formula injection in spreadsheets.
- XML entity expansion abuse.
- SQL payloads containing destructive statements when disallowed.
- XSS through file names, sheet names, or legacy labels rendered in the UI.

#### 28.4 Mapping Workspace Wireframe

Textual wireframe for the mapping screen:

```text
+----------------------------------------------------------------------------------+
| Client Migration Workspace                                                       |
| [Project Name] [Import Format] [Status] [Validate] [Dry Run] [Approve] [Execute] |
+----------------------------------------------------------------------------------+
| Search Target... | Search Source... | Auto-Match Tables | Auto-Match Fields      |
| Confidence Filter | Show Unmapped | Show Conflicts | Show Corrupted | Save Draft  |
+----------------------------------------------------------------------------------+
| TARGET SYSTEM SCHEMA                     |     LINKING / REVIEW CANVAS            |
|------------------------------------------|----------------------------------------|
| Table A                                  |  Target Table A  ===>  Source Table X  |
|  - id                                   |  Match confidence badge                 |
|  - name                                 |  Suggested fields list                  |
|  - status                               |  Conflict notes                         |
|                                          |                                        |
| Table B                                  |  Target Table B  ===>  Source Table Y  |
|  - id                                   |  Auto-match accepted / rejected         |
|  - client_id                             |  Required fields missing                |
|  - created_at                            |  Enum remap suggestions                 |
|                                          |                                        |
| Table C                                  |  Table split / merge actions            |
|  - id                                   |  Relationship warnings                  |
|  - parent_id                             |  Dry-run preview link                   |
+----------------------------------------------------------------------------------+
| SOURCE CLIENT SCHEMA                                                             |
|------------------------------------------|----------------------------------------|
| Legacy Table X                           | Mapping Details                         |
|  - legacy_id                             | Target Field: name                      |
|  - full_name                             | Source Field: fullname                  |
|  - state_code                            | Transform: trim -> normalize_case       |
|                                          | Confidence: 92%                         |
| Legacy Table Y                           | Validation Notes                        |
|  - ext_id                               | Required field resolved                  |
|  - description                          | No FK issues                             |
+----------------------------------------------------------------------------------+
| Issues Queue: Missing field | Bad type | Unmapped enum | Corrupted file | SQL risk |
+----------------------------------------------------------------------------------+
```

#### 12. Metadata Extraction from Target System

The system must inspect MariaDB metadata and build an internal representation of the current platform schema, including:

- Tables
- Columns
- Types
- PKs
- FKs
- Unique constraints
- Indexes
- Default values
- Nullability
- Enum-like lookup references
- Standard audit columns
- Tenant isolation columns such as tenant_id, company_id, organization_id, school_id, unit_id when applicable

Recommended metadata sources:

- `information_schema.tables`
- `information_schema.columns`
- `information_schema.key_column_usage`
- `information_schema.referential_constraints`
- `information_schema.statistics`

#### 13. Auto-Matching Strategy

The module should provide automated suggestions but never fully trust them without review.

##### 13.1 Table Auto-Match Inputs

- Exact normalized name match
- Singular/plural normalization
- Prefix and suffix stripping
- Alias dictionary match
- Description similarity
- Shared key patterns
- Shared business-domain tags
- Similar column composition
- Similar foreign-key neighborhood
- Historical mappings from prior projects

##### 13.2 Column Auto-Match Inputs

- Exact normalized field name
- Alias dictionary match
- Datatype compatibility
- Length compatibility
- Nullability compatibility
- Enum similarity
- Sample value similarity
- Position relevance
- Parent table confidence
- Relationship context

##### 13.3 Confidence Scoring

Suggested confidence bands:

- High: 0.90 to 1.00
- Medium: 0.70 to 0.89
- Low: 0.40 to 0.69
- Reject / No Suggestion: below 0.40

##### 13.4 Matching Heuristics

Normalize names before comparison:

- Lowercase all names
- Remove accents
- Replace spaces, dashes, and dots with underscore
- Convert camelCase to snake_case
- Remove common prefixes like `tb_`, `tbl_`, `cad_`, `sys_`, `legacy_`
- Remove common suffixes like `_tbl`, `_temp`, `_backup`
- Singularize/pluralize candidate names

##### 13.5 Alias Dictionary

The system must support an internal dictionary for common business synonyms, for example:

| Source Term | Target Term |
|---|---|
| customer | client |
| user | person |
| class | course_class |
| doctor | professional |
| invoice | billing_document |
| branch | unit |
| company | organization |
| tenant | tenant |
| status_code | status |

This dictionary must be configurable by admins and reusable across projects.

##### 13.6 Historical Learning

The module should store approved mappings as reusable suggestions for future migrations, with safeguards so that historical mappings boost confidence but never silently override current project review.

#### 14. Supported Mapping Types

- One source table to one target table
- One source table to many target tables
- Many source tables to one target table
- Source field to target field
- Source computed field to target field
- Constant value to target field
- Generated UUID to target field
- Lookup remap to target foreign key
- Enum remap to normalized enum or lookup table
- Ignored source field
- Derived target field

#### 15. Transformation Rules

Each field mapping may include zero or more transforms executed in order.

##### 15.1 Transform Categories

- Trim whitespace
- Normalize case
- Remove formatting characters
- Date parsing and timezone conversion
- Numeric casting
- Boolean normalization
- Enum remapping
- String concatenation
- String split
- Reference lookup
- UUID generation
- Hashing when explicitly authorized for secrets or credentials
- Default fallback assignment
- Custom PHP transform hook

##### 15.2 Example Transform Pipeline

```json
{
  "target_field": "document_number",
  "source_field": "cpf_raw",
  "transforms": [
    { "type": "trim" },
    { "type": "digits_only" },
    { "type": "validate_document_br" },
    { "type": "assign_if_valid" }
  ]
}
```

##### 15.3 Custom Rules Governance

Custom transform hooks must be versioned, auditable, tenant-scoped where applicable, and approved before execution in production.

#### 16. Data Integrity Rules

The module must validate:

- Required target fields are satisfied.
- Target unique constraints are not violated.
- Foreign keys resolve successfully.
- Datatype casts are safe.
- Date formats are valid.
- Enum and lookup values are mapped.
- Duplicate records are detected according to configurable matching rules.
- Circular dependency handling is defined.
- Parent-child load order is respected.

#### 17. Referential Migration Planning

The execution engine must compute dependency order across mapped tables.

Recommended load phases:

1. Foundational lookups and reference tables
2. Core identities and organizations
3. Parent entities
4. Child entities
5. Bridge / many-to-many tables
6. Audit or historical extensions
7. Post-load reconciliation and backfilling

Where circular references exist, the engine should support staged inserts followed by deferred foreign-key resolution.

#### 18. Duplicate Resolution

The module must support duplicate handling strategies per entity type:

- Strict insert only
- Upsert by external ID
- Upsert by natural key
- Fuzzy review queue
- Manual conflict resolution
- Skip duplicates and log

Example duplicate keys:

- Email
- National ID
- Legacy external ID
- Organization code
- Composite natural key

#### 19. Validation Engine

##### 19.1 Validation Layers

- JSON structure validation
- Source schema semantic validation
- Target compatibility validation
- Table mapping completeness validation
- Field mapping completeness validation
- Transformation validation
- Referential integrity simulation
- Duplicate detection validation
- Security validation
- Execution readiness validation

##### 19.2 Validation Severity

- Error: blocks progression
- Warning: allows progression with approval
- Info: advisory only

##### 19.3 Example Errors

- Required target field has no mapped source or default.
- FK target cannot be resolved.
- Target enum has unmapped legacy value.
- Transform output type does not match target column type.
- Source table marked mapped but all columns unresolved.

#### 20. Dry Run Requirements

The module must support dry run execution before live migration.

Dry run outputs:

- Insert count by table
- Update count by table
- Skipped rows by rule
- Transformation failures
- Duplicate conflicts
- FK failures
- Sample before/after preview
- Execution duration estimate
- Rollback feasibility note

Dry run should execute against a safe isolated target, never directly against live tenant data.

#### 21. Live Execution Controls

##### 21.1 Preconditions

- Migration project status = Approved for Execution
- Validation status = Passed or Passed with approved warnings
- Dry run status = Passed
- Authorized role confirmation
- Optional second approver for high-risk clients
- Backup snapshot confirmation

##### 21.2 Execution Safety Controls

- Transaction batching
- Checkpoints per phase
- Idempotency token for job execution
- Pause and resume support
- Failure isolation by table batch
- Post-batch commit logging
- Retry policy with capped attempts
- Rollback metadata generation

#### 22. Audit and Compliance

Every migration action must be auditable.

Required audit records:

- Project creation
- JSON upload
- Schema parse version
- Mapping changes
- Auto-match suggestions accepted or rejected
- Validation runs
- Dry run runs
- Approval events
- Execution start and end
- Errors and exceptions
- User identity and timestamp for each action

Compliance considerations:

- Sensitive fields must be masked in previews where required.
- PII access must be role-controlled.
- Logs must avoid storing secrets in plain text.
- Audit data retention must follow platform policy.
- Exported reports must be traceable and integrity-protected.

#### 23. Security Requirements

- Admin-only or explicitly permissioned access.
- CSRF protection for state-changing endpoints.
- Strict server-side authorization checks.
- File upload validation for JSON MIME and size.
- Malware scanning if file upload pipeline supports it.
- Rate limiting on import endpoints.
- Output encoding in UI to prevent XSS from legacy labels or sample values.
- Signed action logs for sensitive approvals where applicable.
- Secrets and credentials must never be migrated in raw reversible form unless a separate approved security process exists.

#### 24. Suggested Status Model

##### 24.1 Project Status

- Draft
- Imported
- Mapping In Progress
- Validation Failed
- Ready for Dry Run
- Dry Run Failed
- Ready for Approval
- Approved
- Executing
- Partially Completed
- Completed
- Completed With Warnings
- Cancelled

##### 24.2 Mapping Status

- Unmapped
- Suggested
- Reviewed
- Approved
- Ignored
- Blocked

#### 25. Recommended Database Design

Suggested core tables for the migration module:

##### 25.1 `migration_projects`

- id
- tenant_id or platform scope field
- client_id
- name
- source_system
- source_version
- source_db_type
- status
- risk_level
- created_by
- approved_by
- executed_by
- created_at
- updated_at
- executed_at

##### 25.2 `migration_imports`

- id
- migration_project_id
- file_name
- file_hash
- import_format
- raw_json_path or blob reference
- parsed_schema_version
- imported_by
- imported_at

##### 25.3 `migration_source_tables`

- id
- migration_project_id
- source_table_name
- normalized_name
- description
- row_estimate
- primary_key_json
- metadata_json

##### 25.4 `migration_source_columns`

- id
- source_table_id
- source_column_name
- normalized_name
- source_data_type
- length_value
- precision_value
- scale_value
- nullable_flag
- default_value
- sample_values_json
- metadata_json

##### 25.5 `migration_target_tables_cache`

Cache snapshot of current platform schema at project creation time.

##### 25.6 `migration_table_mappings`

- id
- migration_project_id
- target_table_name
- source_table_id
- mapping_type
- confidence_score
- suggestion_source
- status
- approved_by
- approved_at
- notes

##### 25.7 `migration_column_mappings`

- id
- table_mapping_id
- target_column_name
- source_column_id
- transform_pipeline_json
- default_value_json
- null_strategy
- confidence_score
- status
- validation_notes

##### 25.8 `migration_value_maps`

For enum and lookup remaps.

##### 25.9 `migration_validation_runs`

- id
- migration_project_id
- run_type
- status
- summary_json
- started_at
- finished_at
- triggered_by

##### 25.10 `migration_execution_jobs`

- id
- migration_project_id
- idempotency_key
- environment
- execution_mode
- status
- progress_json
- error_summary_json
- started_at
- finished_at

##### 25.11 `migration_audit_logs`

- id
- migration_project_id
- actor_user_id
- action_type
- entity_type
- entity_id
- before_json
- after_json
- ip_address
- user_agent
- created_at

#### 26. API Design Proposal

Base namespace recommendation:

`/api/admin/migrations`

##### 26.1 Project Endpoints

- `POST /api/admin/migrations/projects`
- `GET /api/admin/migrations/projects`
- `GET /api/admin/migrations/projects/{id}`
- `PATCH /api/admin/migrations/projects/{id}`

##### 26.2 Import Endpoints

- `POST /api/admin/migrations/projects/{id}/import-json`
- `POST /api/admin/migrations/projects/{id}/parse`
- `GET /api/admin/migrations/projects/{id}/source-schema`
- `GET /api/admin/migrations/projects/{id}/target-schema`

##### 26.3 Mapping Endpoints

- `POST /api/admin/migrations/projects/{id}/auto-match-tables`
- `POST /api/admin/migrations/projects/{id}/auto-match-columns`
- `GET /api/admin/migrations/projects/{id}/table-mappings`
- `PUT /api/admin/migrations/projects/{id}/table-mappings/{mappingId}`
- `GET /api/admin/migrations/projects/{id}/column-mappings`
- `PUT /api/admin/migrations/projects/{id}/column-mappings/{mappingId}`
- `POST /api/admin/migrations/projects/{id}/value-maps`

##### 26.4 Validation and Execution Endpoints

- `POST /api/admin/migrations/projects/{id}/validate`
- `POST /api/admin/migrations/projects/{id}/dry-run`
- `POST /api/admin/migrations/projects/{id}/approve`
- `POST /api/admin/migrations/projects/{id}/execute`
- `POST /api/admin/migrations/projects/{id}/pause`
- `POST /api/admin/migrations/projects/{id}/resume`
- `GET /api/admin/migrations/projects/{id}/jobs`
- `GET /api/admin/migrations/projects/{id}/reports`

#### 27. Frontend Behavior Proposal

##### 27.1 Technology Notes

- PHP-rendered admin shell or PHP API backend with modular frontend pages
- Fetch API for async actions
- MariaDB as operational database
- Optional canvas or SVG layer for schema relationship drawing
- Search-first UX for large schemas

##### 27.2 Key Frontend Components

- Schema tree panel
- Table card
- Relationship line layer
- Mapping drawer
- Field mapping grid
- Confidence badge
- Validation issue list
- Diff viewer for before/after mapping changes
- Dry run summary widgets
- Execution log stream panel

##### 27.3 UX Expectations

- Fast filter by table name, domain tag, mapped status, confidence, relationship count
- Side-by-side synchronized scrolling option
- Click a target table highlights suggested source candidates
- Click a source table highlights suggested target candidates
- Selecting a mapping opens field-level details
- Unmatched required target fields must be visually prioritized
- Warnings should be grouped by severity and entity

#### 28. Schema Visualizer Requirements

The visualizer should emulate the clarity of a schema exploration tool.

##### 28.1 Visual Node Contents

Each table node should show:

- Table name
- Key icon for PK fields
- Distinct style for nullable vs non-nullable fields
- Unique markers
- FK markers
- Field datatype labels
- Optional row count estimate

##### 28.2 Visual Relationships

- Target schema relationships visible in one mode
- Source schema relationships visible in another mode
- Mapping lines between source and target tables visible in mapping mode
- Toggle clutter reduction for dense schemas
- Auto layout plus manual pinning

##### 28.3 Filters

- Show mapped only
- Show unmapped only
- Show warnings only
- Show high-risk only
- Show core domain only
- Search by table or column

#### 29. Automation Opportunities

The module should maximize automation while preserving human approval.

##### 29.1 Recommended Automatic Features

- Auto-detect table names using normalization rules
- Auto-detect columns using names, types, and samples
- Auto-suggest enum remaps from observed legacy values
- Auto-detect common audit fields like created_at, updated_at, deleted_at
- Auto-classify identity fields such as email, phone, national ID, external ID
- Auto-detect lookup tables by low cardinality and repeated references
- Auto-propose migration order based on FK graph
- Auto-generate default transforms for formatting cleanup

##### 29.2 Admin Fine-Tuning Layer

Automation should produce a first draft. The admin then performs a “fine comb” review focused on:

- Low confidence mappings
- Required target fields still unresolved
- Sensitive fields
- Complex relation splits and merges
- Enum and code translations
- Duplicates and ambiguous identities

#### 30. Matching Engine Proposal

A lightweight scoring engine can be implemented first, with future expansion to ML-assisted ranking.

##### 30.1 Initial Deterministic Scoring Example

Score components:

- 35% name similarity
- 20% alias dictionary hit
- 15% datatype compatibility
- 10% nullability compatibility
- 10% sample value pattern similarity
- 10% relationship neighborhood similarity

##### 30.2 Future Enhancements

- Project-history-assisted ranking
- Embedding-based semantic label similarity
- Domain-specific model packs for education, healthcare, finance
- Explainable suggestion cards showing why a match was proposed

#### 31. Error Handling

The module must provide explicit error messages and actionable next steps.

Examples:

- Invalid JSON format: show row/character hint when possible.
- Unsupported datatype: show source field and recommended custom transform.
- FK resolution failure: show missing parent mapping.
- Duplicate conflict: show matching rule and conflicting keys.
- Permission error: show missing role or approval state.

#### 32. Performance Requirements

- Must support large schemas with at least hundreds of tables and thousands of columns in the workspace.
- UI rendering should use virtualization for large lists.
- Schema layout should support lazy expansion by domain or module.
- Auto-match operations should run asynchronously with job progress.
- Heavy validation and dry run operations should run in background jobs.

#### 33. Observability Requirements

- Structured logs for every import, mapping update, validation run, and execution phase
- Correlation ID per migration project and per execution job
- Metrics for parse time, match time, validation error counts, execution throughput, failure rates
- Admin-visible timeline of major actions

#### 34. Notifications

Recommended notification events:

- Import completed
- Validation completed
- Dry run completed
- Approval required
- Execution started
- Execution paused
- Execution completed
- Execution failed

Delivery channels may include:

- In-app notifications
- Email for high-risk approvals
- Webhook for external orchestration

#### 35. Permissions Matrix

| Action | Super Admin | Migration Analyst | Client Technical Contact | Auditor |
|---|---|---|---|---|
| Create project | Yes | Yes | No | No |
| Upload JSON | Yes | Yes | Limited optional | No |
| Edit mappings | Yes | Yes | No by default | No |
| Run validation | Yes | Yes | No | No |
| Run dry run | Yes | Yes | No | No |
| Approve execution | Yes | Optional by policy | No | No |
| Execute live migration | Yes | Optional by policy | No | No |
| View audit logs | Yes | Yes | No | Yes |
| Download reports | Yes | Yes | Limited optional | Yes |

#### 36. Suggested Project States and Gates

| Stage | Required Conditions | Output |
|---|---|---|
| Import | Valid JSON package | Parsed source schema |
| Mapping | Table and field pairings reviewed | Saved mapping draft |
| Validation | Required fields and relationships checked | Validation report |
| Dry Run | Validation passed | Dry run report |
| Approval | Risk and report review completed | Approval record |
| Execution | Authorized approval present | Execution log and result report |

#### 37. Example Admin Review Checklist

- Are all mandatory target tables mapped or intentionally ignored?
- Are all required target fields mapped or provided by defaults/generators?
- Are all FK relationships resolvable?
- Are enum/code translations complete?
- Are duplicate rules defined for identity-bearing entities?
- Are sensitive fields handled securely?
- Has dry run completed without blocking errors?
- Has rollback and backup readiness been confirmed?

#### 38. Recommended Implementation Phases

##### Phase 1

- Create migration project
- Import JSON
- Parse source schema
- Snapshot target schema
- Basic table and column auto-match
- Manual review UI

##### Phase 2

- Transform pipelines
- Validation engine
- Dry run engine
- Reports and audit logs

##### Phase 3

- Advanced visualizer
- Historical mapping reuse
- Multi-table merge/split support
- Background job orchestration
- Approval workflow

##### Phase 4

- Domain templates by industry
- Semantic matching improvements
- External orchestration hooks
- Migration playbook library

#### 39. Acceptance Criteria

##### 39.1 Import

- Admin can create a migration project and upload a valid JSON package.
- System parses the source schema and stores a normalized internal representation.
- System shows parse errors clearly when package structure is invalid.

##### 39.2 Visualization

- Admin can view full target schema and full source schema side by side.
- Admin can search, filter, and inspect tables and fields from both sides.
- Admin can create, edit, and remove table mappings and column mappings.

##### 39.3 Automation

- System proposes automatic table and field mappings with visible confidence scores.
- System clearly differentiates accepted, suggested, rejected, and unresolved mappings.
- Admin can override any automatic suggestion.

##### 39.4 Validation and Execution

- System blocks execution when blocking validation errors exist.
- System supports dry run before live execution.
- System logs all critical actions and produces a migration report.

#### 40. Open Technical Decisions

- Whether raw imported JSON is stored in database, object storage, or both.
- Whether transform hooks are purely configuration-driven or can execute approved PHP classes.
- Whether execution uses direct SQL batches, ORM-assisted writes, or a dedicated migration worker service.
- Whether the visualizer is built with SVG, Canvas, or DOM-based layout engine.
- Whether approval requires one or two authorized users based on risk level.

#### 41. Recommended Next Deliverables

- UI wireframe spec for the schema visualizer and mapping workspace
- Database DDL spec for migration module tables
- API contract spec with request/response examples
- JSON schema definition for client migration package
- Validation rules catalog
- Execution engine technical design

#### 42. Summary Statement

This module should be treated as a controlled migration orchestration system, not just an import screen. The best implementation is a guided admin workspace that combines schema visualization, automatic matching, manual review, validation, dry run simulation, and audited execution so new client onboarding becomes faster, safer, and repeatable.
