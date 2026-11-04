# Medicina e segurança do trabalho da empresa

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Pessoas da plataforma
- Domínio: plataforma (banco master), instância separada do módulo das entidades ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2.1)
- Status: detalhado; especificação da v1 absorvida integralmente (seção 13), com as correções da v2 e as decisões por padrão (seções 1 a 12)
- Fonte da v1: [spec_gestao_seguranca_medicina_trabalho_completo.md](../../../docs/v2/anexo-v1/spec_gestao_seguranca_medicina_trabalho_completo.md) (1581 linhas)

## 1. Regra de leitura
As seções 1 a 12 prevalecem sobre a seção 13. A seção 13 é o texto integral da v1, sem corte, para que nenhum detalhe se perca. Quando a seção 13 disser algo diferente das seções 1 a 12, vale o que está nas seções 1 a 12.

## 2. Objetivo e escopo
Gerir a saúde e a segurança do trabalho dos funcionários da própria empresa desenvolvedora: ASO, PCMSO, PGR, LTCAT, CAT, EPI, CIPA, ergonomia e treinamentos de NR, com dado de saúde sob acesso restrito.

## 3. Telas
- **ASO** (datatable): colaborador, tipo de exame, validade, resultado (apto ou inapto); CID só para o médico do trabalho.
- **Ocorrências de SST** (datatable): registro, CAT, afastamento, providências.
**Títulos da v1 (referência, não são telas):**

- Sumário
- 1. Visão Geral
  - 1.1 Objetivos Funcionais
  - 1.2 Módulos de Tela
- 2. Perfis e Permissões (RBAC)
- 3. Dashboard — SMT
  - 3.1 Widgets KPI (linha superior — 6 cards)
  - 3.2 Widgets Operacionais (linha intermediária — 4 cards)
  - 3.3 Charts amCharts 5
  - 3.4 Controles do Dashboard
- 4. Gestão de Funcionários e ASO
  - 4.1 Página `/smt/funcionarios`
  - 4.2 Drawer — Ficha de Saúde do Funcionário
  - 4.3 Drawer — Agendar / Registrar Exame (ASO)
- 5. PCMSO — Programa de Controle Médico
  - 5.1 Página `/smt/pcmso`
  - 5.2 Drawer — Cadastro de PCMSO
  - 5.3 Sub-tela: Cronograma PCMSO
- 6. PGR / PPRA — Gestão de Riscos
  - 6.1 Página `/smt/pgr`
  - 6.2 Datatable — GHE (Grupos Homogêneos de Exposição)
  - 6.3 Drawer — Cadastro de GHE
  - 6.4 Drawer — Inventário de Risco (por GHE)
  - 6.5 Datatable — Plano de Ação
  - 6.6 Drawer — Plano de Ação
- 7. LTCAT — Laudo Técnico
  - 7.1 Página `/smt/ltcat`
  - 7.2 Drawer — Cadastro de Laudo
- 8. Acidentes de Trabalho (CAT)
  - 8.1 Página `/smt/cat`
  - 8.2 Drawer — Emitir CAT
  - 8.3 Drawer — Investigação de Acidente
- 9. EPI — Equipamentos de Proteção
  - 9.1 Página `/smt/epi`
  - 9.2 Drawer — Entrega de EPI (FIEPI)
  - 9.3 Drawer — Entrada de Estoque EPI
- 10. Treinamentos e NR
  - 10.1 Página `/smt/treinamentos`
  - 10.2 Drawer — Cadastro de Treinamento
  - 10.3 Drawer — Turma de Treinamento
- 11. Absenteísmo e Afastamentos
  - 11.1 Página `/smt/afastamentos`
  - 11.2 Drawer — Registrar Afastamento
  - 11.3 Widget — Taxa de Absenteísmo
- 12. CIPA — Comissão Interna
  - 12.1 Página `/smt/cipa`
  - 12.2 Drawer — Registrar Reunião CIPA
- 13. Ergonomia e Laudos
  - 13.1 Página `/smt/ergonomia`
  - 13.2 Drawer — Análise Ergonômica
- 14. eSocial — Integração
  - 14.1 Página `/smt/esocial`
- 15. Relatórios e Analytics
  - 15.1 Página `/smt/relatorios`
  - 15.2 Charts na Página de Relatórios
- 16. Kanban Operacional
  - 16.1 Kanban — Exames Agendados
  - 16.2 Kanban — Plano de Ação (PGR)
  - 16.3 Kanban — CAT / Investigação
  - 16.4 Kanban — eSocial
- 17. Automações e Alertas
  - 17.1 Engine de Automação
  - 17.2 Gatilhos e Ações
  - 17.3 Central de Automações
- 18. Configurações e Gerenciamentos
  - 18.1 Página `/smt/configuracoes`
  - 18.2 Drawer — Cadastro de Médico / Clínica
  - 18.3 Gerenciamento de Templates de Documentos
- 19. Schema SQL
- 20. API REST — Endpoints
  - Exames / ASO
  - PGR / Riscos
  - CAT
  - EPI
  - Treinamentos
  - Afastamentos
  - eSocial
  - Dashboard
- 21. Controles Globais
  - 21.1 Controles Presentes em Todas as Páginas
  - 21.2 Controles Específicos de SMT
- 22. LGPD e Segurança de Dados
  - 22.1 Dados Sensíveis (art. 11 LGPD — Dado de Saúde)
  - 22.2 Controles Implementados
  - 22.3 Controles de Acesso
- 23. Critérios de Aceite
  - 23.1 Funcionais
  - 23.2 Não Funcionais
  - 23.3 Checklist de Entrega

## 4. Correções da v2 que prevalecem
- **Regra central de privacidade** ([39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 5.1, e HCM-06): RH e gestão **nunca** veem CID, diagnóstico ou prontuário; veem apenas apto, inapto ou apto com restrição, validade do ASO, restrição funcional sem motivo clínico e afastamento sem CID. A permissão "SST — Gerenciar" da v1 **não existe**: cada papel tem permissão própria.
- **PCMSO, PGR, LTCAT, CIPA e ergonomia:** seguem o [52](../../../docs/v2/52-medicina-do-trabalho-especificacao.md), que prevalece sobre a v1, inclusive o DDL proposto da seção 9.
- **Guarda do prontuário e do ASO:** no mínimo 20 anos após o desligamento (HCM-08; NR-7, 7.6.1.1).
- **Regras do [17](../../../docs/v2/17-regras-modulos.md), seção 5** (ASO, CAT, EPI, NR, afastamento) prevalecem sobre a v1.
- **Resultado de exame:** registrado só pelo profissional responsável ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5).
- **Instância da empresa:** sem filtro de unidade; dados no banco master, com acesso restrito.

## 5. Decisões por padrão aplicadas
- Nenhuma decisão nova: privacidade e papéis já decididos (HCM-06, HCM-08).

## 6. Permissões e papéis
Papéis do [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 11 (HCM-06), na empresa (códigos em [78](../../../docs/v2/78-permissoes-e-papeis.md), seção 4.1):
- `platform.sst.doctor` (médico do trabalho): ASO completo, prontuário, CID, restrição detalhada.
- `platform.sst.technician` (técnico de SESMT): ocorrências, EPI, NR, PGR, CAT, sem diagnóstico.
- `platform.people`, `platform.hr` e `platform.manager`: só o resultado sem CID nem motivo clínico.
- Funcionário: o próprio ASO e o próprio resultado.
- Auditor: leitura com motivo registrado, sem conteúdo de dado de saúde ([29](../../../docs/v2/29-auditoria.md), seção 5).

## 7. Dados
- Modelo de dados da v1 (seção 13) e DDL proposto do [52](../../../docs/v2/52-medicina-do-trabalho-especificacao.md), seção 9, com `tenant_id`. Dado de saúde cifrado ([05](../../../docs/v2/05-seguranca.md)).

## 8. Integrações
- `smt.cat.created` → Pessoas (afastamento); `hcm.employee.created` → agenda do exame admissional ([39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 8).
- eSocial S-2220, S-2230 e S-2240, conforme D-08 ([16](../../../docs/v2/16-integracoes-externas.md), seção 6).
- Clínica de ASO pelo portal de terceiros: recebe agendamento e devolve resultado ([38](../../../docs/v2/38-portal-de-terceiros-prestadores.md), seção 3.11).

## 9. Exportação, auditoria e privacidade
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Auditoria conforme [29](../../../docs/v2/29-auditoria.md); dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md).
- Dado de saúde é dado sensível (LGPD, art. 11): necessidade, acesso por papel, cifragem, registro de leitura e guarda mínima de 20 anos para prontuário e ASO.

## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
- CAT com CID emitida pelo médico, não pela gestão **(verificar)**, no [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 5.1.
- Revisão do owner do [52](../../../docs/v2/52-medicina-do-trabalho-especificacao.md) (HCM-07).

## 13. Conteúdo integral da v1 (absorvido)

### SPEC — Módulo Segurança e Medicina do Trabalho (SMT)
> **Versão:** 1.0 | **Status:** Draft Funcional Completo
> **Plataforma:** TotusTuusSoftCloud — SaaS multi-entidade · multi-unidade · multi-usuário
> **Stack:** PHP 8 puro · MariaDB · Tailwind CSS 4.2 · Supabase · amCharts 5 · API REST (fetch)
> **Padrão de ID:** `id` (PK ordenação) · `uuid` (ID interno) · `code` (ID externo)
> **Conformidade:** LGPD · NR-01 a NR-38 · eSocial S-2220 · S-2240 · S-2210 · PCMSO · PPRA · PGR · LTCAT

- Language Standard: Global English
---

#### Sumário

1. [Visão Geral](#1-visao-geral)
2. [Perfis e Permissões (RBAC)](#2-perfis-e-permissoes-rbac)
3. [Dashboard — SMT](#3-dashboard--smt)
4. [Gestão de Funcionários e ASO](#4-gestao-de-funcionarios-e-aso)
5. [PCMSO — Programa de Controle Médico](#5-pcmso--programa-de-controle-medico)
6. [PGR / PPRA — Gestão de Riscos](#6-pgr--ppra--gestao-de-riscos)
7. [LTCAT — Laudo Técnico](#7-ltcat--laudo-tecnico)
8. [Acidentes de Trabalho (CAT)](#8-acidentes-de-trabalho-cat)
9. [EPI — Equipamentos de Proteção](#9-epi--equipamentos-de-protecao)
10. [Treinamentos e NR](#10-treinamentos-e-nr)
11. [Absenteísmo e Afastamentos](#11-absenteismo-e-afastamentos)
12. [CIPA — Comissão Interna](#12-cipa--comissao-interna)
13. [Ergonomia e Laudos](#13-ergonomia-e-laudos)
14. [eSocial — Integração](#14-esocial--integracao)
15. [Relatórios e Analytics](#15-relatorios-e-analytics)
16. [Kanban Operacional](#16-kanban-operacional)
17. [Automações e Alertas](#17-automacoes-e-alertas)
18. [Configurações e Gerenciamentos](#18-configuracoes-e-gerenciamentos)
19. [Schema SQL](#19-schema-sql)
20. [API REST — Endpoints](#20-api-rest--endpoints)
21. [Controles Globais](#21-controles-globais)
22. [LGPD e Segurança de Dados](#22-lgpd-e-seguranca-de-dados)
23. [Critérios de Aceite](#23-criterios-de-aceite)

---

#### 1. Visão Geral

O módulo **Segurança e Medicina do Trabalho (SMT)** gerencia toda a conformidade ocupacional da organização, incluindo exames médicos (ASO/PCMSO), gestão de riscos (PGR/PPRA), controle de EPI, acidentes de trabalho, laudos técnicos (LTCAT/Ergonomia), treinamentos de NR, CIPA e integração com eSocial.

##### 1.1 Objetivos Funcionais

- Controle completo do ciclo de vida dos exames ocupacionais (admissional, periódico, retorno, mudança de função, demissional)
- Gestão de riscos ocupacionais conforme PGR (NR-01) e PPRA (NR-09)
- Emissão e controle de CAT (Comunicação de Acidente de Trabalho)
- Rastreabilidade de entrega e devolução de EPIs por funcionário
- Controle de validade de treinamentos obrigatórios por NR
- Integração automática com eSocial (S-2210, S-2220, S-2240)
- Alertas e automações para vencimentos críticos

##### 1.2 Módulos de Tela

| Rota | Módulo | Descrição |
|------|--------|-----------|
| `/smt/dashboard` | Dashboard | KPIs, widgets e charts |
| `/smt/funcionarios` | Funcionários | Ficha de saúde e histórico |
| `/smt/exames` | Exames / ASO | Agendamento e controle de ASO |
| `/smt/pcmso` | PCMSO | Programa médico anual |
| `/smt/pgr` | PGR / PPRA | Gestão de riscos |
| `/smt/ltcat` | LTCAT | Laudos técnicos de condições ambientais |
| `/smt/cat` | Acidentes (CAT) | Comunicação e investigação |
| `/smt/epi` | EPI | Estoque, entrega e devolução |
| `/smt/treinamentos` | Treinamentos | NRs, validade e certificados |
| `/smt/afastamentos` | Afastamentos | INSS, B15, B31, B91 |
| `/smt/cipa` | CIPA | Eleição, atas e gestão |
| `/smt/ergonomia` | Ergonomia | Laudos e planos de ação |
| `/smt/esocial` | eSocial | Fila de envio e monitoramento |
| `/smt/relatorios` | Relatórios | Exportações e analytics |
| `/smt/configuracoes` | Configurações | CIDs, riscos, cargos, médicos |

---

#### 2. Perfis e Permissões (RBAC)

| Permissão | SA | GE | SESMT | MED | RH | AUD | VIS |
|-----------|----|----|-------|-----|----|-----|-----|
| Dashboard | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Exames — visualizar | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Exames — criar/editar | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Exames — excluir | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ASO — assinar digitalmente | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| PGR — criar/editar | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| CAT — emitir | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| EPI — entregar/devolver | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| EPI — estoque | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Treinamentos — criar | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Afastamentos — aprovar | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| eSocial — enviar | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Configurações | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Relatórios | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| LGPD — exportar dados | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Audit logs | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |

> **Perfis:** SA = Super Admin · GE = Gestor de Entidade · SESMT = Técnico/Engenheiro de Segurança · MED = Médico do Trabalho · RH = Recursos Humanos · AUD = Auditor · VIS = Visitante

---

#### 3. Dashboard — SMT

##### 3.1 Widgets KPI (linha superior — 6 cards)

| Widget | Dado | Cor de alerta |
|--------|------|---------------|
| Exames vencendo em 30 dias | Contagem | Amarelo ≥10, Vermelho ≥20 |
| Exames vencidos | Contagem | Vermelho >0 |
| CATs no mês | Contagem total + graves | Vermelho se graves>0 |
| EPIs vencendo (CA) | Itens c/ CA expirando em 60 dias | Amarelo |
| Treinamentos vencidos | Funcionários c/ NR vencida | Vermelho >0 |
| Afastamentos ativos | INSS + empresa | Neutro azul |

##### 3.2 Widgets Operacionais (linha intermediária — 4 cards)

| Widget | Conteúdo |
|--------|----------|
| Agenda do dia | Exames agendados para hoje (lista compacta) |
| Riscos críticos | Top 5 GHE com risco alto/crítico |
| Ações vencidas (PGR) | Plano de ação com prazo expirado |
| CIPA — próxima reunião | Countdown + pauta |

##### 3.3 Charts amCharts 5

| Chart | Tipo | Dados | Filtros |
|-------|------|-------|---------|
| Exames por mês (12 meses) | Line dual-axis | Realizados vs Vencidos | Ano, Unidade |
| Distribuição por tipo de exame | Donut | Admissional, Periódico, Retorno, Mudança, Demissional | Período |
| Acidentes por mês | Bar grouped | Total, Típico, Doença, Trajeto | Ano |
| Riscos por GHE | Bar horizontal | Funcionários expostos por grau de risco | Setor |
| Taxa de absenteísmo | Line | % mensal | Ano, Tipo afastamento |
| EPIs mais entregues | Bar | Top 10 itens | Período |

##### 3.4 Controles do Dashboard

- **Filtro global:** `entity_id` · `unit_id` · Período (date-range picker)
- **Botão Atualizar** + timestamp da última atualização
- **Exportar Dashboard** → PDF com todos os widgets e charts
- **Alertas fixados:** banner vermelho se houver exames vencidos > 0 ou CAT grave aberta

---

#### 4. Gestão de Funcionários e ASO

##### 4.1 Página `/smt/funcionarios`

**Datatable — Funcionários SMT**

| Coluna | Tipo | Ordenável | Filtrável |
|--------|------|-----------|-----------|
| Código (code) | text | ✅ | ✅ |
| Nome | text | ✅ | ✅ |
| CPF (mascarado) | text | ❌ | ✅ |
| Cargo / Função | text | ✅ | ✅ |
| Setor / GHE | text | ✅ | ✅ |
| Data admissão | date | ✅ | ✅ |
| Último ASO | date | ✅ | ✅ |
| Próximo ASO | date | ✅ | ✅ |
| Status ASO | badge | ✅ | ✅ |
| Risco | badge | ✅ | ✅ |
| Ações | buttons | ❌ | ❌ |

**Badges de Status ASO:**
- 🟢 `Em dia` — vence em >60 dias
- 🟡 `Vencendo` — vence em 1–60 dias
- 🔴 `Vencido` — data passada
- 🔵 `Agendado` — possui agendamento futuro

**Filtros do Datatable:**
- Busca geral (nome, CPF, código)
- Setor / GHE (select)
- Status ASO (multiselect)
- Grau de risco (select)
- Tipo de contrato (CLT, PJ, Terceiro, Estagiário)
- Data de admissão (range)

**Ações por linha:**
- 👁 Visualizar ficha completa
- 📋 Novo exame / ASO
- 📦 Entregar EPI
- 📜 Histórico médico
- 📤 Exportar prontuário (PDF) — somente MED e SA

##### 4.2 Drawer — Ficha de Saúde do Funcionário

**Tamanho:** fullscreen drawer (lateral direita, 60% largura)

**Abas da Ficha:**
1. **Dados Gerais** — nome, CPF, cargo, admissão, data nascimento, tipo sanguíneo, alergias conhecidas (criptografado)
2. **Histórico de Exames** — datatable de todos os ASOs com link para PDF
3. **EPIs Entregues** — datatable de entregas e devoluções
4. **Afastamentos** — histórico de INSS e afastamentos internos
5. **Treinamentos** — NRs concluídas e vencidas
6. **CATs** — acidentes registrados
7. **Restrições Médicas** — lista de restrições ativas (acesso somente MED/SA)
8. **Audit Log** — todas as ações sobre este registro

##### 4.3 Drawer — Agendar / Registrar Exame (ASO)

**Campos:**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Funcionário | select-search | ✅ | Ativo no sistema |
| Tipo de exame | select | ✅ | Admissional, Periódico, Retorno, Mudança de Função, Demissional |
| Data agendada | datetime | ✅ | Não retroativa para agendamentos |
| Clínica / Local | select | ✅ | Cadastro de clínicas |
| Médico responsável | select | ✅ | CRM ativo |
| Exames solicitados | checkbox-list | ✅ | Hemograma, audiometria, espirometria, raio-x, etc. |
| Observações | textarea | ❌ | Max 1000 chars |
| Custo estimado | currency | ❌ | — |

**Após realização — campos adicionais:**

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| Data de realização | date | ✅ |
| Resultado (apto/inapto) | radio | ✅ |
| Apto com restrição | checkbox | ❌ |
| Descrição da restrição | textarea | Condicional |
| Próximo exame em (meses) | number | ✅ |
| CID relacionado | select | ❌ |
| Upload ASO (PDF) | file | ✅ |
| Assinar digitalmente | button | MED only |

---

#### 5. PCMSO — Programa de Controle Médico

##### 5.1 Página `/smt/pcmso`

**Datatable — Programas PCMSO**

| Coluna | Tipo |
|--------|------|
| Código | text |
| Ano de referência | number |
| Responsável técnico (médico) | text |
| CRM | text |
| Data elaboração | date |
| Vigência | date range |
| Status | badge (Ativo, Revisão, Arquivado) |
| Unidade | text |
| Ações | buttons |

**Ações:** Visualizar · Editar · Imprimir · Arquivar · Versionar

##### 5.2 Drawer — Cadastro de PCMSO

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| Ano de referência | number | ✅ |
| Médico coordenador | select | ✅ |
| CRM | text (auto-fill) | ✅ |
| Unidade | select | ✅ |
| Data elaboração | date | ✅ |
| Vigência início/fim | date-range | ✅ |
| Objetivo geral | textarea | ✅ |
| Riscos identificados (tags) | tag-input | ✅ |
| Exames previstos por cargo | table inline | ✅ |
| Cronograma anual | calendar-grid | ✅ |
| Observações legais | textarea | ❌ |
| Anexo (PDF assinado) | file | ❌ |
| Status | select | ✅ |

##### 5.3 Sub-tela: Cronograma PCMSO

- View **calendario mensal** com eventos de exames previstos
- View **lista** com datatable de exames previstos vs realizados
- Indicador de % de cumprimento do programa
- Exportar cronograma em Excel / PDF

---

#### 6. PGR / PPRA — Gestão de Riscos

##### 6.1 Página `/smt/pgr`

**Abas da Página:**
1. **GHE — Grupos Homogêneos de Exposição**
2. **Inventário de Riscos**
3. **Plano de Ação**
4. **Histórico de Programas**

##### 6.2 Datatable — GHE (Grupos Homogêneos de Exposição)

| Coluna | Tipo |
|--------|------|
| Código GHE | text |
| Descrição | text |
| Setor | text |
| Nº de Funcionários | number |
| Riscos identificados | badges |
| Nível de risco (maior) | badge colorido |
| Última avaliação | date |
| Próxima avaliação | date |
| Responsável | text |
| Ações | buttons |

##### 6.3 Drawer — Cadastro de GHE

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| Código GHE | text | ✅ |
| Descrição | text | ✅ |
| Setor / Área | select | ✅ |
| Atividades desenvolvidas | textarea | ✅ |
| Funcionários do grupo | multi-select | ✅ |
| Agentes de risco | checkbox-list | ✅ |

**Agentes de risco (NR-01 / GRO):**
- ☐ Físicos (ruído, calor, frio, vibração, radiação)
- ☐ Químicos (poeiras, fumos, névoas, gases, vapores)
- ☐ Biológicos (vírus, bactérias, fungos, parasitas)
- ☐ Ergonômicos (postura, esforço, jornada)
- ☐ Mecânicos/Acidente (máquinas, eletricidade, queda)

##### 6.4 Drawer — Inventário de Risco (por GHE)

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| GHE | select | ✅ |
| Agente de risco | select | ✅ |
| Fonte/processo gerador | text | ✅ |
| Trajetória de exposição | textarea | ✅ |
| Medidas de controle existentes | textarea | ✅ |
| Probabilidade (1-5) | slider | ✅ |
| Severidade (1-5) | slider | ✅ |
| Nível de risco calculado | read-only | — |
| Nível de ação exigido | read-only | — |
| Medições disponíveis | file-multi | ❌ |
| Responsável pela avaliação | select | ✅ |
| Data da avaliação | date | ✅ |

**Matriz de Risco (display visual):**
```
              Severidade
              1    2    3    4    5
Probabilidade
     1       [ 1][ 2][ 3][ 4][ 5]
     2       [ 2][ 4][ 6][ 8][10]
     3       [ 3][ 6][ 9][12][15]
     4       [ 4][ 8][12][16][20]
     5       [ 5][10][15][20][25]
```
- 1–4: 🟢 Baixo | 5–9: 🟡 Médio | 10–15: 🟠 Alto | 16–25: 🔴 Crítico

##### 6.5 Datatable — Plano de Ação

| Coluna | Tipo |
|--------|------|
| Nº da ação | text |
| GHE relacionado | text |
| Risco endereçado | text |
| Ação proposta | text |
| Responsável | text |
| Prazo | date |
| Status | badge (Pendente, Em andamento, Concluída, Vencida) |
| % Progresso | progress bar |
| Evidência | link |
| Ações | buttons |

##### 6.6 Drawer — Plano de Ação

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| GHE / Risco | select | ✅ |
| Tipo de controle | select | ✅ (Eliminação, Substituição, Controle engenharia, Controle adm., EPI) |
| Ação proposta | textarea | ✅ |
| Responsável | select | ✅ |
| Prazo | date | ✅ |
| Prioridade | radio (Alta/Média/Baixa) | ✅ |
| Recurso necessário | text | ❌ |
| Custo estimado | currency | ❌ |
| Upload evidência | file-multi | ❌ |
| Status | select | ✅ |
| Data de conclusão | date | Condicional |

---

#### 7. LTCAT — Laudo Técnico

##### 7.1 Página `/smt/ltcat`

**Datatable — Laudos LTCAT**

| Coluna | Tipo |
|--------|------|
| Código | text |
| Título / Descrição | text |
| Tipo | badge (LTCAT, PPP, Ergonômico, Ambiental) |
| Responsável técnico | text |
| CREA/CRM | text |
| Data elaboração | date |
| Vigência | date |
| Status | badge |
| Unidade | text |
| Ações | buttons |

##### 7.2 Drawer — Cadastro de Laudo

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| Tipo de laudo | select | ✅ |
| Unidade / Setor | select | ✅ |
| Responsável técnico | select | ✅ |
| Registro profissional (CREA/CRM) | text | ✅ |
| Data elaboração | date | ✅ |
| Validade | date | ✅ |
| Agentes nocivos avaliados | tag-input | ✅ |
| GHEs contemplados | multi-select | ✅ |
| Metodologia utilizada | textarea | ✅ |
| Resultados e conclusões | textarea | ✅ |
| Grau de insalubridade | select (10%, 20%, 40%, Nenhum) | ✅ |
| Grau de periculosidade | select (30%, Nenhum) | ✅ |
| Arquivo do laudo (PDF) | file | ✅ |
| Status | select | ✅ |

---

#### 8. Acidentes de Trabalho (CAT)

##### 8.1 Página `/smt/cat`

**Abas:**
1. **CATs** — Comunicações de Acidentes
2. **Investigação** — Análise de causa raiz
3. **Estatísticas** — Taxas e indicadores

**Datatable — CATs**

| Coluna | Tipo |
|--------|------|
| Nº CAT | text |
| Funcionário | text |
| Data do acidente | datetime |
| Tipo | badge (Típico, Doença, Trajeto, Óbito) |
| Parte do corpo atingida | text |
| CID | text |
| Dias perdidos | number |
| Status eSocial | badge |
| Status investigação | badge |
| Ações | buttons |

**Filtros:**
- Período (range)
- Tipo de acidente
- Setor / GHE
- Status eSocial
- Com/Sem afastamento

##### 8.2 Drawer — Emitir CAT

**Aba 1: Dados do Acidente**

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| Funcionário | select-search | ✅ |
| Data e hora do acidente | datetime | ✅ |
| Tipo de acidente | select | ✅ |
| Local do acidente | select (Dentro/Fora da empresa/Trajeto) | ✅ |
| Descrição do acidente | textarea | ✅ |
| Parte do corpo atingida | select | ✅ |
| Natureza da lesão | select | ✅ |
| Agente causador | select | ✅ |
| Houve afastamento | radio | ✅ |
| Dias de afastamento estimados | number | Condicional |
| Óbito | checkbox | ❌ |

**Aba 2: Atendimento Médico**

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| CID principal | select | ✅ |
| CID secundário | select | ❌ |
| Médico assistente | text | ✅ |
| CRM | text | ✅ |
| Local de atendimento | text | ✅ |
| Data do atendimento | date | ✅ |
| Internação | checkbox | ❌ |
| Período de internação | date-range | Condicional |

**Aba 3: Testemunhas**

| Campo | Tipo |
|-------|------|
| Nome testemunha 1 | text |
| CPF testemunha 1 | text |
| Nome testemunha 2 | text |
| CPF testemunha 2 | text |
| Declaração | textarea |

##### 8.3 Drawer — Investigação de Acidente

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| CAT relacionada | read-only | — |
| Equipe investigadora | multi-select | ✅ |
| Método de análise | select (Diagrama de Árvore, 5 Porquês, Ishikawa, FMEA) | ✅ |
| Causa imediata | textarea | ✅ |
| Causa básica | textarea | ✅ |
| Causa raiz | textarea | ✅ |
| Ações corretivas | repeat-group | ✅ |
| Ações preventivas | repeat-group | ✅ |
| Upload de fotos/evidências | file-multi | ❌ |
| Responsável pela investigação | select | ✅ |
| Data conclusão | date | ✅ |

---

#### 9. EPI — Equipamentos de Proteção

##### 9.1 Página `/smt/epi`

**Abas:**
1. **Estoque de EPIs** — cadastro e saldos
2. **Entregas** — controle de entrega por funcionário
3. **Devoluções** — registro de devoluções
4. **Certificados CA** — controle de validade dos CAs

**Datatable — Catálogo de EPIs**

| Coluna | Tipo |
|--------|------|
| Código | text |
| Descrição | text |
| Tipo / Categoria | text |
| Marca / Fabricante | text |
| Nº CA (Certificado de Aprovação) | text |
| Vencimento CA | date |
| Estoque atual | number |
| Estoque mínimo | number |
| Status estoque | badge |
| Ações | buttons |

**Datatable — Entregas de EPI**

| Coluna | Tipo |
|--------|------|
| Nº ficha | text |
| Funcionário | text |
| Data entrega | date |
| EPI entregue | text |
| Quantidade | number |
| Motivo | text |
| Assinatura digital | badge (Assinado/Pendente) |
| Devolução prevista | date |
| Status | badge |
| Ações | buttons |

##### 9.2 Drawer — Entrega de EPI (FIEPI)

**Aba 1: Identificação**

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| Funcionário | select-search | ✅ |
| Data da entrega | date | ✅ |
| Responsável pela entrega | select | ✅ |
| Motivo da entrega | select (Admissão, Reposição, Desgaste, Mudança de função, Periódico) | ✅ |

**Aba 2: Itens Entregues**

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| EPI | select-search (por CA) | ✅ |
| Quantidade | number | ✅ |
| Nº CA | read-only | — |
| Validade CA | read-only | — |
| Prazo de troca (dias) | number | ✅ |
| Observação | text | ❌ |
| + Adicionar item | button | — |

**Aba 3: Comprovante**

- Preview do FIEPI (Ficha de EPI) gerado automaticamente
- Botão **Coletar Assinatura Digital** (canvas touchscreen / upload de assinatura)
- Botão **Imprimir FIEPI**
- Botão **Salvar e Enviar por e-mail**

##### 9.3 Drawer — Entrada de Estoque EPI

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| EPI | select | ✅ |
| Quantidade recebida | number | ✅ |
| Nº da Nota Fiscal | text | ✅ |
| Fornecedor | select | ✅ |
| Data de recebimento | date | ✅ |
| Nº CA (lote) | text | ✅ |
| Validade CA | date | ✅ |
| Custo unitário | currency | ❌ |
| Upload NF | file | ❌ |

---

#### 10. Treinamentos e NR

##### 10.1 Página `/smt/treinamentos`

**Abas:**
1. **Catálogo de Treinamentos** — NRs e cursos disponíveis
2. **Turmas** — agendamento e execução
3. **Certificados** — emissão e validade
4. **Conformidade** — matriz de atendimento por cargo/NR

**Datatable — Catálogo de Treinamentos**

| Coluna | Tipo |
|--------|------|
| Código | text |
| Nome do treinamento | text |
| NR relacionada | badge |
| Carga horária (h) | number |
| Periodicidade (meses) | number |
| Modalidade | badge (Presencial, EAD, Híbrido) |
| Obrigatório para | text |
| Status | badge |
| Ações | buttons |

**Datatable — Turmas**

| Coluna | Tipo |
|--------|------|
| Código turma | text |
| Treinamento | text |
| Data início | date |
| Data fim | date |
| Instrutor | text |
| Vagas / Inscritos | fraction |
| Local | text |
| Status | badge |
| Ações | buttons |

**Datatable — Conformidade por Cargo (Matriz NR)**

| Coluna | Tipo |
|--------|------|
| Funcionário | text |
| Cargo | text |
| NR-05 CIPA | badge |
| NR-06 EPI | badge |
| NR-10 Elétrica | badge |
| NR-11 Transporte | badge |
| NR-12 Máquinas | badge |
| NR-17 Ergonomia | badge |
| NR-20 Inflamáveis | badge |
| NR-35 Altura | badge |
| NR-38 Trabalho Telhado | badge |
| Ações | buttons |

> Badges: ✅ Em dia · ⚠️ Vencendo (30 dias) · ❌ Vencido · ➖ Não aplicável

##### 10.2 Drawer — Cadastro de Treinamento

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| Nome | text | ✅ |
| NR relacionada | select-multi | ✅ |
| Código interno | text | ✅ |
| Carga horária | number | ✅ |
| Periodicidade (meses) | number | ✅ |
| Modalidade | select | ✅ |
| Conteúdo programático | textarea rich | ✅ |
| Cargos obrigatórios | multi-select | ✅ |
| Setores obrigatórios | multi-select | ❌ |
| Aprovação mínima (%) | number | ✅ |
| Emite certificado | toggle | ✅ |
| Validade do certificado (meses) | number | Condicional |
| Instrutor padrão | select | ❌ |

##### 10.3 Drawer — Turma de Treinamento

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| Treinamento | select | ✅ |
| Código da turma | text | ✅ |
| Data início | date | ✅ |
| Data fim | date | ✅ |
| Horário | time-range | ✅ |
| Local / Plataforma | text | ✅ |
| Instrutor | select | ✅ |
| Vagas | number | ✅ |
| Participantes | multi-select | ✅ |
| Upload lista de presença | file | ❌ |
| Upload avaliação (gabarito) | file | ❌ |
| Resultado (notas) | table inline | ❌ |

---

#### 11. Absenteísmo e Afastamentos

##### 11.1 Página `/smt/afastamentos`

**Abas:**
1. **Afastamentos Ativos**
2. **Histórico de Afastamentos**
3. **INSS / Perícias**
4. **Indicadores de Absenteísmo**

**Datatable — Afastamentos**

| Coluna | Tipo |
|--------|------|
| Código | text |
| Funcionário | text |
| Tipo | badge (B15, B31, B61, B91, B94, Empresa, Licença) |
| CID | text |
| Data início | date |
| Data fim prevista | date |
| Dias afastados | number (calculado) |
| Status | badge |
| eSocial enviado | badge |
| Ações | buttons |

##### 11.2 Drawer — Registrar Afastamento

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| Funcionário | select-search | ✅ |
| Tipo de afastamento | select | ✅ |
| CID principal | select | ✅ |
| CID secundário | select | ❌ |
| Data de início | date | ✅ |
| Data fim prevista | date | ✅ |
| Médico responsável | text | ✅ |
| CRM | text | ✅ |
| Relacionado a acidente de trabalho | toggle | ❌ |
| CAT relacionada | select | Condicional |
| Observações | textarea | ❌ |
| Atestado médico | file | ✅ |
| Enviar para eSocial (S-2230) | toggle | ✅ |

##### 11.3 Widget — Taxa de Absenteísmo

**Fórmula:**
```
Taxa (%) = (Horas perdidas / Horas esperadas) × 100
```

- Visualização por: mês, setor, CID, tipo de afastamento
- Benchmark: alerta se taxa > 3,5%

---

#### 12. CIPA — Comissão Interna

##### 12.1 Página `/smt/cipa`

**Abas:**
1. **Composição da CIPA** — membros eleitos e designados
2. **Reuniões** — atas e pautas
3. **Gestão de Eleições**
4. **Atividades e Campanhas**

**Datatable — Membros da CIPA**

| Coluna | Tipo |
|--------|------|
| Nome | text |
| Cargo empresa | text |
| Setor | text |
| Função CIPA | badge (Presidente, Vice, Secretário, Titular, Suplente) |
| Representação | badge (Empregador, Empregado) |
| Mandato início | date |
| Mandato fim | date |
| Status | badge |
| Ações | buttons |

**Datatable — Reuniões CIPA**

| Coluna | Tipo |
|--------|------|
| Nº reunião | text |
| Data | datetime |
| Tipo | badge (Ordinária, Extraordinária) |
| Quórum | fraction |
| Status | badge |
| Ata | link |
| Ações | buttons |

##### 12.2 Drawer — Registrar Reunião CIPA

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| Tipo de reunião | select | ✅ |
| Data e hora | datetime | ✅ |
| Local | text | ✅ |
| Pauta | repeat-group (tópicos) | ✅ |
| Presentes | multi-select | ✅ |
| Deliberações | textarea rich | ✅ |
| Ações definidas | repeat-group (ação, responsável, prazo) | ❌ |
| Upload ata assinada | file | ✅ |

---

#### 13. Ergonomia e Laudos

##### 13.1 Página `/smt/ergonomia`

**Datatable — Laudos Ergonômicos**

| Coluna | Tipo |
|--------|------|
| Código | text |
| Setor / GHE | text |
| Tipo de análise | badge (RULA, REBA, OWAS, NR-17) |
| Responsável | text |
| Data | date |
| Grau de risco | badge |
| Plano de ação | badge (Com plano / Sem plano) |
| Status | badge |
| Ações | buttons |

##### 13.2 Drawer — Análise Ergonômica

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| Setor / GHE | select | ✅ |
| Função analisada | text | ✅ |
| Tipo de análise | select | ✅ |
| Metodologia | select (RULA, REBA, OWAS, Checklist NR-17) | ✅ |
| Descrição da atividade | textarea | ✅ |
| Fatores de risco encontrados | checkbox-list | ✅ |
| Score de risco (1-7) | number | ✅ |
| Medidas recomendadas | textarea | ✅ |
| Plano de ação | repeat-group | ✅ |
| Fotos/vídeos | file-multi | ❌ |
| Laudo em PDF | file | ✅ |
| Próxima avaliação | date | ✅ |

---

#### 14. eSocial — Integração

##### 14.1 Página `/smt/esocial`

**Abas:**
1. **Fila de Envio** — eventos pendentes
2. **Histórico de Transmissões**
3. **Inconsistências**
4. **Configurações eSocial**

**Datatable — Fila de Envio**

| Coluna | Tipo |
|--------|------|
| Evento | badge (S-2210, S-2220, S-2230, S-2240) |
| Funcionário | text |
| Descrição | text |
| Data do fato gerador | date |
| Prazo de envio | date |
| Status | badge (Pendente, Em fila, Enviado, Rejeitado, Processado) |
| Protocolo | text |
| Mensagem retorno | text |
| Ações | buttons |

**Eventos eSocial SMT:**

| Evento | Descrição | Prazo |
|--------|-----------|-------|
| S-2210 | Comunicação de Acidente de Trabalho (CAT) | Até 1 dia útil |
| S-2220 | Monitoramento da Saúde do Trabalhador (ASO) | Até 15 dias após exame |
| S-2230 | Afastamento Temporário | 1º dia útil seguinte |
| S-2240 | Condições Ambientais do Trabalho | Antes do início da atividade |

**Controles da Fila:**
- **Enviar selecionados** (checkbox + batch action)
- **Reenviar rejeitado** (por linha)
- **Consultar protocolo** (por linha)
- **Download XML** (por linha)
- **Filtro por evento, status, prazo**
- **Alerta de prazo crítico** (< 24h destacado em vermelho)

---

#### 15. Relatórios e Analytics

##### 15.1 Página `/smt/relatorios`

**Relatórios disponíveis:**

| Relatório | Filtros | Formatos |
|-----------|---------|----------|
| Exames vencidos / a vencer | Setor, período, tipo | PDF · Excel |
| ASOs realizados no período | Tipo, setor, médico | PDF · Excel |
| CATs por período | Tipo, setor, gravidade | PDF · Excel |
| Taxa de frequência e gravidade | Período, setor | PDF |
| Inventário de EPIs | EPI, estoque, validade CA | PDF · Excel |
| Ficha individual de EPI (FIEPI) | Funcionário | PDF |
| Conformidade de treinamentos | Cargo, NR, setor | PDF · Excel |
| Absenteísmo por CID | Período, setor | PDF · Excel |
| CIPA — membros e reuniões | Ano, mandato | PDF |
| PGR — riscos e ações | GHE, status, risco | PDF · Excel |
| Prontuário individual | Funcionário | PDF (criptografado) |
| Relatório gerencial SMT | Período, unidade | PDF |

##### 15.2 Charts na Página de Relatórios

- **Pirâmide de Bird** — visualização de acidentes por gravidade
- **Curva ABC de absenteísmo** — CIDs mais frequentes
- **Radar de conformidade** — aderência às NRs por setor
- **Evolução de acidentes** — line chart 24 meses

---

#### 16. Kanban Operacional

##### 16.1 Kanban — Exames Agendados

**Colunas:**
| Status | Descrição |
|--------|-----------|
| 📅 Agendado | Exame com data definida |
| 🔔 Confirmado | Clínica confirmou presença |
| 🏥 Em andamento | Funcionário na clínica |
| ✅ Realizado | Exame realizado, aguardando resultado |
| 📄 Laudo recebido | ASO disponível |
| ❌ Não compareceu | Falta ao exame |

**Cards de Exame:**
- Nome do funcionário
- Tipo de exame
- Clínica / Médico
- Data/hora agendada
- Badge de urgência (vencimento próximo)
- Ações: Ver · Editar · Reagendar · Marcar como realizado

##### 16.2 Kanban — Plano de Ação (PGR)

**Colunas:**
| Status |
|--------|
| 📋 Pendente |
| 🚧 Em Execução |
| 🔍 Em Verificação |
| ✅ Concluída |
| ⏰ Vencida |

**Cards de Ação:**
- Nº da ação
- GHE relacionado
- Responsável (avatar)
- Prazo (countdown)
- Prioridade (badge colorido)
- % de progresso (mini progress bar)

##### 16.3 Kanban — CAT / Investigação

**Colunas:**
| Status |
|--------|
| 🚨 CAT Emitida |
| 🔍 Em Investigação |
| 📝 Ações Definidas |
| 🔄 Ações em Andamento |
| ✅ Encerrada |

##### 16.4 Kanban — eSocial

**Colunas:**
| Status |
|--------|
| 📋 Pendente |
| ⏳ Em Fila |
| 📤 Enviado |
| ✅ Processado |
| ❌ Rejeitado |

---

#### 17. Automações e Alertas

##### 17.1 Engine de Automação

Todas as automações rodam via **cron job** (`/cron/smt_worker.php`) com registro em `smt_automation_logs`.

##### 17.2 Gatilhos e Ações

| # | Gatilho | Condição | Ação Automática |
|---|---------|----------|-----------------|
| 1 | Diário 07:00 | Exames vencendo em 30 dias | Notificação push + e-mail para RH e SESMT |
| 2 | Diário 07:00 | Exames vencidos | Notificação crítica + widget vermelho no dashboard |
| 3 | Diário 07:00 | CA de EPI vencendo em 60 dias | Notificação para SESMT |
| 4 | Diário 07:00 | Treinamento NR vencido | Notificação para gestor e RH |
| 5 | Ao registrar acidente | Tipo = grave ou óbito | Alerta imediato por e-mail + SMS para GE e SA |
| 6 | Ao registrar CAT | Sempre | Criar evento na fila eSocial S-2210 automaticamente |
| 7 | Ao salvar ASO | Apto = true | Criar evento na fila eSocial S-2220 automaticamente |
| 8 | Ao registrar afastamento | Sempre | Criar evento na fila eSocial S-2230 automaticamente |
| 9 | Ao salvar GHE com risco | Sempre | Criar evento na fila eSocial S-2240 automaticamente |
| 10 | Diário 08:00 | eSocial com prazo < 24h | Alerta urgente para responsável eSocial |
| 11 | Ao criar agendamento | Sempre | Envio de e-mail de confirmação para funcionário |
| 12 | Diário 06:00 | Reunião CIPA em 3 dias | Lembrete por e-mail para todos os membros |
| 13 | Semanal domingo | Ações PGR vencidas | Relatório de ações vencidas para GE |
| 14 | Mensal dia 1 | — | Gerar relatório de absenteísmo do mês anterior |
| 15 | Ao atingir estoque mínimo EPI | Saldo ≤ mínimo | Notificação para SESMT + criar solicitação de compra no Suprimentos |

##### 17.3 Central de Automações

- **Listagem** de automações com toggle ativo/inativo
- **Logs de execução** (última execução, status, erros)
- **Configuração de destinatários** por automação
- **Histórico** de notificações enviadas

---

#### 18. Configurações e Gerenciamentos

##### 18.1 Página `/smt/configuracoes`

**Abas:**

1. **Médicos e Clínicas** — cadastro de parceiros
2. **CIDs Frequentes** — CIDs predefinidos mais usados
3. **Tipos de Exame** — configuração de exames por cargo
4. **NRs Aplicáveis** — quais NRs se aplicam à empresa
5. **GHE — Configuração** — setores e grupos
6. **Cargos e Periodicidade** — prazo de exame por cargo/risco
7. **Fornecedores de EPI** — cadastro
8. **Configurações eSocial** — CNPJ, certificado digital
9. **Templates de Documentos** — ASO, FIEPI, Ata CIPA
10. **Automações** — gerenciamento de gatilhos

##### 18.2 Drawer — Cadastro de Médico / Clínica

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| Tipo | select (Médico, Clínica, Laboratório) | ✅ |
| Nome | text | ✅ |
| CRM / CNPJ | text | ✅ |
| Especialidade | select | Médico |
| Endereço | fields completos | ✅ |
| Telefone | text | ✅ |
| E-mail | email | ✅ |
| Especialidades da clínica | checkbox-list | Clínica |
| Valor médio consulta | currency | ❌ |
| Contrato vigente | toggle | ❌ |
| Validade contrato | date | Condicional |
| Status | select | ✅ |

##### 18.3 Gerenciamento de Templates de Documentos

- Editor visual (rich text) para customizar:
  - ASO (Atestado de Saúde Ocupacional)
  - FIEPI (Ficha de Entrega de EPI)
  - Ata de Reunião CIPA
  - Termo de Responsabilidade EPI
  - Laudo de Inapto com Restrição
- Preview em tempo real
- Variáveis disponíveis: `{{funcionario.nome}}` · `{{empresa.razao_social}}` · `{{exame.tipo}}` · `{{data_atual}}`

---

#### 19. Schema SQL

```sql
-- ============================================================
-- Módulo: Segurança e Medicina do Trabalho (SMT)
-- Banco: por entidade/unidade (ex: dbcoldev01)
-- Padrão: id (PK) · uuid (ID interno) · code (ID externo)
-- ============================================================

-- Exames / ASO
CREATE TABLE smt_exams (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid        CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code        VARCHAR(30) NOT NULL UNIQUE,
    entity_id   BIGINT UNSIGNED NOT NULL,
    unit_id     BIGINT UNSIGNED NOT NULL,
    employee_id BIGINT UNSIGNED NOT NULL,
    type        ENUM('admissional','periodico','retorno','mudanca_funcao','demissional') NOT NULL,
    scheduled_at DATETIME,
    performed_at DATETIME,
    clinic_id   BIGINT UNSIGNED,
    doctor_id   BIGINT UNSIGNED,
    result      ENUM('apto','apto_restricao','inapto') DEFAULT NULL,
    restriction TEXT DEFAULT NULL,
    next_exam_months TINYINT UNSIGNED,
    cid_code    VARCHAR(10),
    file_path   VARCHAR(500),
    signed_at   DATETIME,
    esocial_status ENUM('pending','queued','sent','processed','rejected') DEFAULT 'pending',
    esocial_protocol VARCHAR(100),
    status      ENUM('scheduled','confirmed','performed','cancelled') DEFAULT 'scheduled',
    notes       TEXT,
    created_by  BIGINT UNSIGNED NOT NULL,
    updated_by  BIGINT UNSIGNED,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME ON UPDATE CURRENT_TIMESTAMP,
    deleted_at  DATETIME DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- GHE — Grupos Homogêneos de Exposição
CREATE TABLE smt_ghe (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid        CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code        VARCHAR(30) NOT NULL UNIQUE,
    entity_id   BIGINT UNSIGNED NOT NULL,
    unit_id     BIGINT UNSIGNED NOT NULL,
    name        VARCHAR(200) NOT NULL,
    description TEXT,
    sector      VARCHAR(150),
    activities  TEXT,
    last_evaluated_at DATE,
    next_evaluation_at DATE,
    responsible_id BIGINT UNSIGNED,
    status      ENUM('active','inactive') DEFAULT 'active',
    created_by  BIGINT UNSIGNED NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME ON UPDATE CURRENT_TIMESTAMP,
    deleted_at  DATETIME DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Inventário de Riscos
CREATE TABLE smt_risk_inventory (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code            VARCHAR(30) NOT NULL UNIQUE,
    ghe_id          BIGINT UNSIGNED NOT NULL,
    risk_type       ENUM('fisico','quimico','biologico','ergonomico','mecanico') NOT NULL,
    agent           VARCHAR(200) NOT NULL,
    source          TEXT,
    trajectory      TEXT,
    existing_controls TEXT,
    probability     TINYINT(1) NOT NULL COMMENT '1-5',
    severity        TINYINT(1) NOT NULL COMMENT '1-5',
    risk_level      TINYINT(2) AS (probability * severity) STORED,
    risk_grade      VARCHAR(20) AS (
        CASE
            WHEN (probability * severity) BETWEEN 1 AND 4 THEN 'baixo'
            WHEN (probability * severity) BETWEEN 5 AND 9 THEN 'medio'
            WHEN (probability * severity) BETWEEN 10 AND 15 THEN 'alto'
            ELSE 'critico'
        END
    ) STORED,
    measurement_files JSON,
    evaluated_by    BIGINT UNSIGNED,
    evaluated_at    DATE,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Plano de Ação (PGR)
CREATE TABLE smt_action_plans (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code            VARCHAR(30) NOT NULL UNIQUE,
    risk_inventory_id BIGINT UNSIGNED NOT NULL,
    ghe_id          BIGINT UNSIGNED NOT NULL,
    control_type    ENUM('eliminacao','substituicao','eng_controle','adm_controle','epi') NOT NULL,
    action          TEXT NOT NULL,
    responsible_id  BIGINT UNSIGNED NOT NULL,
    due_date        DATE NOT NULL,
    priority        ENUM('alta','media','baixa') NOT NULL,
    progress        TINYINT(3) DEFAULT 0 COMMENT '0-100%',
    evidence_files  JSON,
    status          ENUM('pendente','em_andamento','verificacao','concluida','vencida') DEFAULT 'pendente',
    completed_at    DATE,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- CAT — Comunicação de Acidente de Trabalho
CREATE TABLE smt_cats (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code            VARCHAR(30) NOT NULL UNIQUE,
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    employee_id     BIGINT UNSIGNED NOT NULL,
    accident_type   ENUM('tipico','doenca','trajeto','obito') NOT NULL,
    occurred_at     DATETIME NOT NULL,
    location_type   ENUM('interno','externo','trajeto') NOT NULL,
    description     TEXT NOT NULL,
    body_part       VARCHAR(150),
    injury_nature   VARCHAR(150),
    causal_agent    VARCHAR(150),
    has_absence     TINYINT(1) DEFAULT 0,
    absence_days    INT DEFAULT 0,
    death           TINYINT(1) DEFAULT 0,
    cid_primary     VARCHAR(10),
    cid_secondary   VARCHAR(10),
    doctor_name     VARCHAR(150),
    doctor_crm      VARCHAR(30),
    treatment_place VARCHAR(200),
    treated_at      DATE,
    hospitalized    TINYINT(1) DEFAULT 0,
    hospitalization_start DATE,
    hospitalization_end   DATE,
    investigation_status ENUM('pending','in_progress','completed') DEFAULT 'pending',
    esocial_status  ENUM('pending','queued','sent','processed','rejected') DEFAULT 'pending',
    esocial_protocol VARCHAR(100),
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME ON UPDATE CURRENT_TIMESTAMP,
    deleted_at      DATETIME DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- EPI — Catálogo
CREATE TABLE smt_epis (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code            VARCHAR(30) NOT NULL UNIQUE,
    entity_id       BIGINT UNSIGNED NOT NULL,
    name            VARCHAR(200) NOT NULL,
    category        VARCHAR(100) NOT NULL,
    brand           VARCHAR(100),
    ca_number       VARCHAR(20) NOT NULL COMMENT 'Certificado de Aprovação',
    ca_expires_at   DATE NOT NULL,
    stock_current   INT DEFAULT 0,
    stock_minimum   INT DEFAULT 0,
    unit_cost       DECIMAL(10,2),
    status          ENUM('active','inactive') DEFAULT 'active',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- EPI — Entregas (FIEPI)
CREATE TABLE smt_epi_deliveries (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code            VARCHAR(30) NOT NULL UNIQUE,
    employee_id     BIGINT UNSIGNED NOT NULL,
    epi_id          BIGINT UNSIGNED NOT NULL,
    delivered_by    BIGINT UNSIGNED NOT NULL,
    delivered_at    DATE NOT NULL,
    reason          ENUM('admissao','reposicao','desgaste','mudanca_funcao','periodico') NOT NULL,
    quantity        INT NOT NULL,
    replacement_days INT,
    expected_return DATE,
    signature_data  TEXT COMMENT 'base64 da assinatura',
    signed_at       DATETIME,
    returned_at     DATE,
    return_condition VARCHAR(100),
    notes           TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Treinamentos
CREATE TABLE smt_trainings (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code            VARCHAR(30) NOT NULL UNIQUE,
    entity_id       BIGINT UNSIGNED NOT NULL,
    name            VARCHAR(200) NOT NULL,
    nr_references   JSON COMMENT '["NR-10","NR-35"]',
    workload_hours  DECIMAL(5,1) NOT NULL,
    validity_months INT NOT NULL,
    modality        ENUM('presencial','ead','hibrido') NOT NULL,
    curriculum      TEXT,
    min_approval_pct TINYINT DEFAULT 70,
    issues_certificate TINYINT(1) DEFAULT 1,
    status          ENUM('active','inactive') DEFAULT 'active',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Treinamentos — Participações
CREATE TABLE smt_training_participants (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    training_id     BIGINT UNSIGNED NOT NULL,
    session_id      BIGINT UNSIGNED NOT NULL,
    employee_id     BIGINT UNSIGNED NOT NULL,
    status          ENUM('enrolled','attended','passed','failed','absent') DEFAULT 'enrolled',
    score           DECIMAL(5,2),
    certificate_code VARCHAR(50),
    certificate_issued_at DATETIME,
    expires_at      DATE,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Afastamentos
CREATE TABLE smt_absences (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code            VARCHAR(30) NOT NULL UNIQUE,
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    employee_id     BIGINT UNSIGNED NOT NULL,
    absence_type    ENUM('B15','B31','B61','B91','B94','empresa','licenca') NOT NULL,
    cid_primary     VARCHAR(10) NOT NULL,
    cid_secondary   VARCHAR(10),
    start_date      DATE NOT NULL,
    end_date_expected DATE NOT NULL,
    end_date_actual DATE,
    doctor_name     VARCHAR(150) NOT NULL,
    doctor_crm      VARCHAR(30) NOT NULL,
    work_accident   TINYINT(1) DEFAULT 0,
    cat_id          BIGINT UNSIGNED,
    certificate_file VARCHAR(500),
    esocial_status  ENUM('pending','queued','sent','processed','rejected') DEFAULT 'pending',
    esocial_protocol VARCHAR(100),
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- CIPA — Membros
CREATE TABLE smt_cipa_members (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    employee_id     BIGINT UNSIGNED NOT NULL,
    cipa_role       ENUM('presidente','vice','secretario','titular','suplente') NOT NULL,
    representation  ENUM('empregador','empregado') NOT NULL,
    mandate_start   DATE NOT NULL,
    mandate_end     DATE NOT NULL,
    status          ENUM('active','inactive') DEFAULT 'active',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- eSocial Fila
CREATE TABLE smt_esocial_queue (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    entity_id       BIGINT UNSIGNED NOT NULL,
    event_type      ENUM('S-2210','S-2220','S-2230','S-2240') NOT NULL,
    reference_table VARCHAR(100) NOT NULL,
    reference_id    BIGINT UNSIGNED NOT NULL,
    employee_id     BIGINT UNSIGNED NOT NULL,
    due_date        DATE NOT NULL,
    xml_payload     LONGTEXT,
    status          ENUM('pending','queued','sent','processed','rejected') DEFAULT 'pending',
    protocol        VARCHAR(100),
    return_message  TEXT,
    sent_at         DATETIME,
    processed_at    DATETIME,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- LTCAT / Laudos Técnicos
CREATE TABLE smt_technical_reports (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code            VARCHAR(30) NOT NULL UNIQUE,
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    report_type     ENUM('ltcat','ppp','ergonomico','ambiental') NOT NULL,
    title           VARCHAR(300) NOT NULL,
    responsible_id  BIGINT UNSIGNED NOT NULL,
    professional_reg VARCHAR(30) NOT NULL,
    elaborated_at   DATE NOT NULL,
    expires_at      DATE,
    insalubrity_degree ENUM('none','10','20','40') DEFAULT 'none',
    periculosity_degree ENUM('none','30') DEFAULT 'none',
    file_path       VARCHAR(500),
    status          ENUM('active','revision','archived') DEFAULT 'active',
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Audit Log SMT
CREATE TABLE smt_audit_logs (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    user_id         BIGINT UNSIGNED NOT NULL,
    action          VARCHAR(100) NOT NULL,
    table_name      VARCHAR(100) NOT NULL,
    record_id       BIGINT UNSIGNED NOT NULL,
    record_uuid     CHAR(36),
    old_data        JSON,
    new_data        JSON,
    ip_address      VARCHAR(45),
    user_agent      TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

#### 20. API REST — Endpoints

Base: `/api/v1/smt/`

##### Exames / ASO

| Método | Rota | Descrição | Permissão |
|--------|------|-----------|-----------|
| GET | `/exams` | Listar exames (paginado, filtros) | SESMT, MED, RH, GE, SA |
| POST | `/exams` | Criar agendamento de exame | SESMT, MED, RH, GE, SA |
| GET | `/exams/{uuid}` | Detalhe do exame | SESMT, MED, RH, GE, SA |
| PUT | `/exams/{uuid}` | Atualizar exame | SESMT, MED, GE, SA |
| DELETE | `/exams/{uuid}` | Soft delete | GE, SA |
| PATCH | `/exams/{uuid}/result` | Registrar resultado/ASO | MED, SA |
| PATCH | `/exams/{uuid}/sign` | Assinar digitalmente | MED, SA |
| GET | `/exams/{uuid}/download` | Download PDF do ASO | SESMT, MED, RH, GE, SA |

##### PGR / Riscos

| Método | Rota | Descrição | Permissão |
|--------|------|-----------|-----------|
| GET | `/ghe` | Listar GHEs | Todos |
| POST | `/ghe` | Criar GHE | SESMT, GE, SA |
| PUT | `/ghe/{uuid}` | Editar GHE | SESMT, GE, SA |
| GET | `/risk-inventory` | Listar inventário de riscos | Todos |
| POST | `/risk-inventory` | Criar item de risco | SESMT, GE, SA |
| PUT | `/risk-inventory/{uuid}` | Editar risco | SESMT, GE, SA |
| GET | `/action-plans` | Listar planos de ação | Todos |
| POST | `/action-plans` | Criar ação | SESMT, GE, SA |
| PUT | `/action-plans/{uuid}` | Atualizar ação | SESMT, GE, SA |
| PATCH | `/action-plans/{uuid}/progress` | Atualizar progresso | SESMT, GE, SA |

##### CAT

| Método | Rota | Descrição | Permissão |
|--------|------|-----------|-----------|
| GET | `/cats` | Listar CATs | SESMT, MED, RH, GE, SA |
| POST | `/cats` | Emitir CAT | SESMT, MED, RH, GE, SA |
| GET | `/cats/{uuid}` | Detalhe da CAT | SESMT, MED, RH, GE, SA |
| PUT | `/cats/{uuid}` | Editar CAT | SESMT, MED, GE, SA |
| POST | `/cats/{uuid}/investigation` | Registrar investigação | SESMT, GE, SA |

##### EPI

| Método | Rota | Descrição | Permissão |
|--------|------|-----------|-----------|
| GET | `/epis` | Listar catálogo EPIs | Todos |
| POST | `/epis` | Cadastrar EPI | SESMT, GE, SA |
| PUT | `/epis/{uuid}` | Editar EPI | SESMT, GE, SA |
| POST | `/epis/stock-in` | Entrada de estoque | SESMT, GE, SA, RH |
| GET | `/epi-deliveries` | Listar entregas | Todos |
| POST | `/epi-deliveries` | Registrar entrega | SESMT, GE, SA |
| PATCH | `/epi-deliveries/{uuid}/sign` | Assinar FIEPI | SESMT, GE, SA |
| GET | `/epi-deliveries/{uuid}/pdf` | Download FIEPI PDF | Todos |
| POST | `/epi-deliveries/{uuid}/return` | Registrar devolução | SESMT, GE, SA |

##### Treinamentos

| Método | Rota | Descrição | Permissão |
|--------|------|-----------|-----------|
| GET | `/trainings` | Listar treinamentos | Todos |
| POST | `/trainings` | Criar treinamento | SESMT, RH, GE, SA |
| POST | `/training-sessions` | Criar turma | SESMT, RH, GE, SA |
| POST | `/training-sessions/{uuid}/enroll` | Inscrever participantes | SESMT, RH, GE, SA |
| PATCH | `/training-sessions/{uuid}/results` | Lançar resultados | SESMT, RH, GE, SA |
| GET | `/training-compliance` | Matriz de conformidade | Todos |

##### Afastamentos

| Método | Rota | Descrição | Permissão |
|--------|------|-----------|-----------|
| GET | `/absences` | Listar afastamentos | MED, RH, GE, SA |
| POST | `/absences` | Registrar afastamento | MED, RH, GE, SA |
| PUT | `/absences/{uuid}` | Editar | MED, RH, GE, SA |
| PATCH | `/absences/{uuid}/close` | Encerrar afastamento | MED, RH, GE, SA |

##### eSocial

| Método | Rota | Descrição | Permissão |
|--------|------|-----------|-----------|
| GET | `/esocial/queue` | Fila de envio | SESMT, GE, SA |
| POST | `/esocial/send` | Transmitir selecionados | SESMT, GE, SA |
| POST | `/esocial/{uuid}/resend` | Reenviar rejeitado | SESMT, GE, SA |
| GET | `/esocial/{uuid}/xml` | Download XML | SESMT, GE, SA |
| GET | `/esocial/stats` | Estatísticas da fila | Todos |

##### Dashboard

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/dashboard/kpis` | Todos os KPIs |
| GET | `/dashboard/exams-chart` | Dados gráfico exames/mês |
| GET | `/dashboard/accidents-chart` | Dados gráfico acidentes |
| GET | `/dashboard/risks-chart` | Dados gráfico riscos por GHE |
| GET | `/dashboard/absenteeism-chart` | Taxa de absenteísmo |

---

#### 21. Controles Globais

##### 21.1 Controles Presentes em Todas as Páginas

| Controle | Comportamento |
|----------|---------------|
| **Filtro de entidade/unidade** | Persiste na sessão; SA vê todas |
| **Date-range picker** | Padrão: mês corrente; persiste por página |
| **Busca global** | Debounce 400ms; busca em campos indexados |
| **Colunas configuráveis** | Drag para reordenar; visibilidade toggle; salvo em localStorage |
| **Paginação** | 10/25/50/100 registros; controles prev/next/first/last |
| **Exportar datatable** | CSV · Excel · PDF — considera filtros ativos |
| **Importar em lote** | Upload CSV/Excel com template; validação antes de importar |
| **Ordenação** | Clique no cabeçalho; multi-coluna com Shift+clique |
| **Ações em lote** | Checkbox + dropdown de ações (excluir, exportar, enviar eSocial) |
| **Breadcrumb** | Navegação contextual em todos os drawers |
| **Confirmação de exclusão** | Modal com nome do registro; input de confirmação para exclusão crítica |
| **Toast de feedback** | Sucesso, erro e aviso para todas as operações |
| **Loading states** | Skeleton loaders para datatables e charts |
| **Responsividade** | Breakpoints Tailwind; drawer fullscreen em mobile |

##### 21.2 Controles Específicos de SMT

| Controle | Página |
|----------|--------|
| **Semáforo de vencimento** | Exames, EPI, Treinamentos — cores dinâmicas por prazo |
| **Contador de dias restantes** | Tooltip em qualquer campo de data |
| **Print FIEPI / ASO** | Botão dedicado com preview |
| **Assinatura digital canvas** | Drawer de entrega EPI e ASO |
| **Botão "Enviar para eSocial"** | CAT, ASO, Afastamento — com confirmação |
| **Matriz de risco visual** | PGR — grid interativo clicável |
| **Progress tracker** | Plano de ação — barra + % editável inline |
| **Timeline de histórico** | Ficha do funcionário — visualização cronológica |

---

#### 22. LGPD e Segurança de Dados

##### 22.1 Dados Sensíveis (art. 11 LGPD — Dado de Saúde)

- CID codes · diagnósticos · restrições médicas
- Resultados de exames · ASO completo
- Histórico de afastamentos · laudos médicos

##### 22.2 Controles Implementados

| Controle | Implementação |
|----------|---------------|
| Criptografia em repouso | AES-256 para campos de diagnóstico e restrições |
| Acesso por papel | Restrições médicas visíveis apenas MED e SA |
| Mascaramento CPF | Exibido como `***.***.***-**` em telas não autorizadas |
| Audit log completo | Toda leitura/escrita em dados de saúde registrada |
| Consentimento | Registro de `consent_at` + `consent_ip` na admissão |
| Portabilidade | Endpoint `/api/v1/smt/employees/{uuid}/export` — ZIP com todos os dados |
| Anonimização | Cron mensal para funcionários desligados há 5 anos |
| Retenção | Dados de saúde retidos por 20 anos conforme CFM + CLT |
| Hash de senha | Argon2id para credenciais de acesso ao módulo |
| Rate limiting | 100 req/min por IP em endpoints de dados de saúde |

##### 22.3 Controles de Acesso

- **MFA obrigatório** para perfis MED e SA
- **JWT com expiração de 2h** para sessões no módulo
- **Log de acesso a prontuários** com IP, user-agent e timestamp
- **Alerta de acesso incomum** (IP diferente + horário atípico)

---

#### 23. Critérios de Aceite

##### 23.1 Funcionais

- [ ] Dashboard carrega em < 2s com todos os widgets e charts
- [ ] Datatable de funcionários suporta 10.000+ registros sem degradação
- [ ] Agendamento de exame cria evento automático no eSocial
- [ ] CAT de acidente grave dispara alerta por e-mail em < 1 minuto
- [ ] FIEPI gerado em PDF com assinatura digital válida
- [ ] Matriz de conformidade NR atualiza em tempo real após lançar treinamento
- [ ] Kanban de exames atualiza por drag-and-drop com persistência
- [ ] Exportação de prontuário individual gera PDF criptografado

##### 23.2 Não Funcionais

- [ ] LGPD: dados de saúde criptografados em repouso (AES-256)
- [ ] Performance: endpoints críticos < 300ms (P95)
- [ ] Disponibilidade: 99,5% mensal
- [ ] Auditoria: 100% das operações em dados de saúde logadas
- [ ] eSocial: integração testada com ambiente de homologação
- [ ] Responsivo: funcional em telas a partir de 320px
- [ ] Acessibilidade: WCAG 2.1 AA para cores e contraste
- [ ] Testes: cobertura mínima de 80% nas regras de negócio críticas

##### 23.3 Checklist de Entrega

- [ ] Todas as páginas implementadas com controles documentados neste spec
- [ ] Schema SQL aplicado e indexes criados
- [ ] Todos os endpoints REST funcionais e documentados
- [ ] Automações configuradas e testadas em staging
- [ ] Templates de ASO, FIEPI e Ata CIPA configurados
- [ ] Integração eSocial testada em homologação
- [ ] Testes de RBAC por perfil executados
- [ ] Audit logs validados para todas as operações
- [ ] LGPD: DPO revisou e aprovou o módulo

---

*Documento gerado por TotusTuusSoftCloud — Arquitetura SaaS*
*Versão 1.0 — Junho/2026*
