# SPEC — Módulo Cobrança e Mensalidades
**Versão:** 1.0  
**Status:** Draft Funcional Completo  
**Módulo:** Billing / Subscriptions / Receivables  
**Contexto:** SaaS multi-entidade, multi-unidade e multi-usuário — banco segregado por entidade/unidade  
**Padrão de Identidade:** `id` (PK ordenação) · `uuid` (global) · `code` (negócio, ex.: `INV-2026-000001`)  
**Stack:** PHP 8 puro · MariaDB · Tailwind CSS 4.2 · Supabase · amCharts 5 · fetch API  
**Prefixo CSS:** `ttsc-` (substituindo `kt-`)  
**Naming:** inglês snake_case em banco/código; português nos labels de UI  

- Language Standard: Global English
---

## Índice

1. [Visão Geral e Objetivos](#1-visão-geral-e-objetivos)
2. [Arquitetura e Banco de Dados](#2-arquitetura-e-banco-de-dados)
3. [Mapa de Páginas](#3-mapa-de-páginas)
4. [Dashboard — Cobrança e Mensalidades](#4-dashboard--cobrança-e-mensalidades)
5. [Gestão de Planos e Tabelas de Preço](#5-gestão-de-planos-e-tabelas-de-preço)
6. [Gestão de Assinaturas](#6-gestão-de-assinaturas)
7. [Cobrança — Faturas e Boletos](#7-cobrança--faturas-e-boletos)
8. [Mensalidades — Gestão Escolar](#8-mensalidades--gestão-escolar)
9. [Pagamentos e Baixas](#9-pagamentos-e-baixas)
10. [Descontos, Bolsas e Isenções](#10-descontos-bolsas-e-isenções)
11. [Inadimplência e Régua de Cobrança](#11-inadimplência-e-régua-de-cobrança)
12. [Kanban de Cobranças](#12-kanban-de-cobranças)
13. [Automações e Régua Inteligente](#13-automações-e-régua-inteligente)
14. [Notas Fiscais de Serviço (NFSe)](#14-notas-fiscais-de-serviço-nfse)
15. [Conciliação Bancária](#15-conciliação-bancária)
16. [Relatórios e Exportações](#16-relatórios-e-exportações)
17. [Configurações do Módulo](#17-configurações-do-módulo)
18. [APIs REST — Endpoints](#18-apis-rest--endpoints)
19. [Schema SQL](#19-schema-sql)
20. [RBAC — Permissões por Perfil](#20-rbac--permissões-por-perfil)
21. [Auditoria e LGPD](#21-auditoria-e-lgpd)
22. [Critérios de Aceite](#22-critérios-de-aceite)

---

## 1. Visão Geral e Objetivos

### 1.1 Escopo
O módulo **Billing / Cobrança e Mensalidades** gerencia todo o ciclo financeiro de receita da instituição:
- Planos e tabelas de preço configuráveis por unidade
- Assinaturas e contratos de mensalidade por aluno/responsável
- Emissão de faturas (boleto, Pix, cartão, débito automático)
- Controle de inadimplência com régua de cobrança automatizada
- Integração com NFSe (Nota Fiscal de Serviço Eletrônica)
- Conciliação bancária e baixa automática de pagamentos
- Dashboards, KPIs e relatórios gerenciais

### 1.2 Objetivos de Negócio
| Objetivo | Métrica-alvo |
|---|---|
| Reduzir inadimplência | < 5% da carteira ativa |
| Automatizar cobranças | ≥ 80% das faturas emitidas sem intervenção |
| Conciliação bancária automatizada | ≥ 95% de match automático |
| Emissão de NFSe | < 2 min após confirmação de pagamento |
| Prazo de baixa de boleto | ≤ 2 horas após pagamento |

### 1.3 Integrações Externas
- **Gateways:** PagSeguro, Mercado Pago, Asaas, Gerencianet/EFÍ, Stripe
- **NFSe:** Prefeituras via API (padrão ABRASF / NFS-e Nacional)
- **Banco Central:** Open Finance (extrato, PIX, débito automático)
- **Email/SMS/WhatsApp:** Envio de faturas e notificações
- **ERP Financeiro:** Lançamentos contábeis automáticos

---

## 2. Arquitetura e Banco de Dados

### 2.1 Multi-tenant
- Cada unidade possui banco físico próprio (`dbcoldev01`, `dbcolsec01`, etc.)
- O `db_core` armazena planos globais, gateways e configurações master
- Conexão resolvida em runtime via `TenantResolver` → `ConnectionManager`
- Todas as queries filtradas por `unit_id` + `entity_id`

### 2.2 Convenções de Banco
- Tabelas: `snake_case` em inglês, prefixo por domínio (`billing_`, `payment_`, `invoice_`)
- PKs: `id BIGINT UNSIGNED AUTO_INCREMENT`
- UUID global: `uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID())`
- Código de negócio: `code VARCHAR(30) NOT NULL UNIQUE` (ex.: `INV-2026-000001`)
- Soft delete: `deleted_at DATETIME NULL DEFAULT NULL`
- Auditoria: `created_by`, `updated_by`, `deleted_by` (FK → users.id)
- Timestamps: `created_at`, `updated_at` em `DATETIME DEFAULT CURRENT_TIMESTAMP`

---

## 3. Mapa de Páginas

```
/billing/
├── dashboard                          → Dashboard principal
├── plans/
│   ├── index                          → Lista de planos
│   └── pricing-tables                 → Tabelas de preço
├── subscriptions/
│   ├── index                          → Lista de assinaturas
│   └── [uuid]/details                 → Detalhe da assinatura
├── invoices/
│   ├── index                          → Faturas (datatable)
│   ├── generate                       → Geração em lote
│   └── [uuid]/view                    → Visualizar fatura
├── tuitions/
│   ├── index                          → Mensalidades (datatable)
│   ├── matrix                         → Matriz de mensalidades por turma
│   └── negotiation                    → Negociação e parcelamento
├── payments/
│   ├── index                          → Pagamentos recebidos
│   ├── write-off                      → Baixa manual
│   └── conciliation                   → Conciliação bancária
├── discounts/
│   ├── index                          → Descontos e bolsas
│   └── scholarships                   → Gestão de bolsas
├── delinquency/
│   ├── index                          → Painel de inadimplência
│   └── collection-rules               → Régua de cobrança
├── kanban                             → Kanban de cobranças
├── automations/
│   ├── index                          → Lista de automações
│   └── [uuid]/logs                    → Logs de execução
├── nfse/
│   ├── index                          → Notas fiscais emitidas
│   └── config                         → Configuração NFSe
├── conciliation/
│   └── index                          → Conciliação bancária
├── reports/
│   ├── revenue                        → Relatório de receita
│   ├── delinquency-aging              → Aging de inadimplência
│   ├── cash-flow                      → Fluxo de caixa
│   └── forecast                       → Previsão de recebimento
└── settings/
    ├── gateways                       → Configuração de gateways
    ├── payment-methods                → Métodos de pagamento
    ├── due-dates                      → Calendário de vencimentos
    └── notifications                  → Templates de notificação
```

---

## 4. Dashboard — Cobrança e Mensalidades

**Arquivo:** `/resources/views/pages/billing/dashboard/index.php`  
**Rota:** `GET /billing/dashboard`

### 4.1 Toolbar e Breadcrumb
```
Início > Billing > Dashboard
[Botão: Gerar Faturas em Lote]  [Botão: Exportar]  [Filtro: Período ▼]  [Filtro: Unidade ▼]
```

### 4.2 Widgets KPI — Linha 1 (Cards Estatísticos)

| Widget | Valor exibido | Ícone | Cor | Tendência |
|---|---|---|---|---|
| Receita Prevista (mês) | R$ 248.500,00 | `ki-dollar` | azul | ↑ +5,2% vs mês ant. |
| Receita Realizada | R$ 198.200,00 | `ki-check-circle` | verde | ↑ +3,1% |
| A Receber (em aberto) | R$ 50.300,00 | `ki-time` | laranja | ↓ -2,4% |
| Inadimplência | 4,8% | `ki-warning` | vermelho | ↓ -0,6pp |
| Faturas Emitidas | 1.240 | `ki-document` | roxo | — |
| Boletos Vencidos | 87 | `ki-close-circle` | vermelho | ↑ +12 hoje |

Cada card: valor principal, variação percentual vs período anterior, link para drilldown, tooltip com fórmula de cálculo.

### 4.3 Widgets KPI — Linha 2 (Indicadores Operacionais)

| Widget | Descrição |
|---|---|
| **Taxa de Cobrança Automática** | % de faturas emitidas sem intervenção manual |
| **Tempo Médio de Pagamento** | Média de dias entre emissão e quitação |
| **Taxa de Conversão PIX** | % de boletos convertidos para PIX |
| **NFSe Emitidas** | Quantidade de notas fiscais emitidas no período |
| **Conciliação Pendente** | Qtd. transações aguardando match |
| **Automações Ativas** | Qtd. e status das automações em execução |

### 4.4 Charts amCharts 5

#### Chart 1 — Receita Mensal (Coluna empilhada + linha de meta)
```
Tipo: XYChart (ColumnSeries empilhado + LineSeries)
Eixo X: meses (jan–dez)
Séries: Mensalidades | Outros Serviços | Multas/Juros
Linha: Meta mensal (tracejada)
Interatividade: tooltip detalhado, zoom, exportar PNG/CSV
```

#### Chart 2 — Aging de Inadimplência (Barras horizontais)
```
Tipo: XYChart horizontal
Faixas: 1-30d | 31-60d | 61-90d | 91-180d | +180d
Valor: R$ e % da carteira
Cor: gradiente verde→vermelho por faixa de risco
```

#### Chart 3 — Distribuição por Método de Pagamento (Donut)
```
Tipo: PieChart (donut)
Fatias: Boleto | PIX | Cartão Crédito | Cartão Débito | Débito Automático | Outros
Legenda: percentual e valor absoluto
```

#### Chart 4 — Fluxo de Caixa Previsto vs Realizado (Linha dupla)
```
Tipo: XYChart (LineSeries duplo)
Período: 30 dias rolling
Série 1: Previsto (tracejado azul)
Série 2: Realizado (sólido verde)
Área: fill entre as linhas (desvio)
```

#### Chart 5 — Funil de Cobrança (Funnel)
```
Tipo: SlicedChart (FunnelSeries)
Etapas: Fatura Emitida → Enviada → Visualizada → Paga → Atrasada → Negociada → Cancelada
```

#### Chart 6 — Heatmap de Vencimentos (Calendar Heatmap)
```
Tipo: XYChart com CellSeries
Eixo X: dias do mês
Eixo Y: semanas
Cor: intensidade = valor a vencer por dia
Tooltip: lista de faturas do dia
```

### 4.5 Datatable — Faturas Recentes
Colunas: `#Code` | `Aluno/Responsável` | `Tipo` | `Vencimento` | `Valor` | `Status` | `Método` | `Ações`

Filtros inline: Status (chips) | Período | Unidade | Método de Pagamento

Ações por linha: Ver | Enviar | Baixar | Cancelar | Reenviar

### 4.6 Seção — Alertas e Ações Rápidas
```
┌─────────────────────────────────────────────────────┐
│ ⚠  87 boletos venceram hoje          [Ver lista]   │
│ 🔔 12 automações falharam nas 2h     [Ver logs]    │
│ ✅ R$ 18.200 conciliados agora        [Detalhar]    │
│ 📄 34 NFSe pendentes de emissão      [Emitir]      │
└─────────────────────────────────────────────────────┘
```

---

## 5. Gestão de Planos e Tabelas de Preço

**Arquivo:** `/resources/views/pages/billing/plans/index.php`  
**Rota:** `GET /billing/plans`

### 5.1 Datatable de Planos

Colunas: `Code` | `Nome do Plano` | `Tipo` (Mensalidade/Serviço/Matrícula/Avulso) | `Valor Base` | `Periodicidade` | `Vigência` | `Status` | `Assinantes` | `Ações`

Filtros: Tipo | Status | Periodicidade | Faixa de valor (range slider)

Ações: Editar | Duplicar | Desativar | Tabela de Preços | Histórico

### 5.2 CRUD Drawer — Plano

**Trigger:** Botão `Novo Plano` ou ícone Editar na linha  
**Largura:** 600px  
**Título dinâmico:** "Novo Plano" | "Editar Plano"

#### Campos do Drawer

**Aba: Dados Gerais**
| Campo | Tipo | Regras |
|---|---|---|
| Nome do Plano | text | required, max:120 |
| Código (code) | text | required, unique, uppercase, auto-sugerido |
| Descrição | textarea | max:500 |
| Tipo | select | Mensalidade / Serviço / Matrícula / Material / Avulso |
| Periodicidade | select | Mensal / Bimestral / Trimestral / Semestral / Anual / Único |
| Valor Base | money | required, ≥ 0 |
| Valor Mínimo | money | opcional |
| Valor Máximo | money | opcional |
| Moeda | select | BRL / USD (default BRL) |
| Status | toggle | Ativo / Inativo |
| Vigência Início | date | required |
| Vigência Fim | date | opcional |
| Aplicável a | multiselect | Alunos / Responsáveis / Empresas |
| Nível de Ensino | multiselect | EI / EF1 / EF2 / EM / Superior / Livre |
| Observações | textarea | max:1000 |

**Aba: Composição de Valor**
- Tabela de itens: Serviço | Quantidade | Valor Unitário | Desconto | Total
- Botão `+ Adicionar Item`
- Totalizador automático

**Aba: Regras de Desconto**
- Desconto pontualidade (%) — dias antes do vencimento
- Desconto irmão (%) — por número de dependentes
- Desconto convênio (%) — vinculado a empresa/associação
- Desconto bolsa (%) — vinculado a programa de bolsa
- Regras combinadas: checkboxes de acumulatividade

**Aba: Configuração de Cobrança**
| Campo | Tipo |
|---|---|
| Método de cobrança padrão | select (Boleto/PIX/Cartão/Débito Auto.) |
| Dia de vencimento padrão | number (1–28) |
| Dias de tolerância | number |
| Juros ao mês (%) | decimal |
| Multa (%) | decimal |
| Máximo de parcelas | number |
| Gerar NFSe automático | toggle |
| Gateway de pagamento | select |

**Rodapé do Drawer:** `[Cancelar]` `[Salvar Rascunho]` `[Salvar e Publicar]`

### 5.3 Página — Tabelas de Preço

**Arquivo:** `/resources/views/pages/billing/plans/pricing-tables.php`

- Datatable com filtros por nível, turno, ano letivo
- Importação via CSV/Excel com validação e preview
- Exportação em XLSX
- Versioning: cada tabela tem version_number e effective_date
- Comparativo entre duas versões (diff visual lado a lado)

---

## 6. Gestão de Assinaturas

**Arquivo:** `/resources/views/pages/billing/subscriptions/index.php`  
**Rota:** `GET /billing/subscriptions`

### 6.1 Datatable de Assinaturas

Colunas: `Code` | `Aluno` | `Responsável Financeiro` | `Plano` | `Valor` | `Próx. Vencimento` | `Status` | `Gateway` | `Parcelas` | `Ações`

Filtros: Status | Plano | Unidade | Turma | Período | Gateway

Ações: Ver Detalhes | Editar | Suspender | Cancelar | Histórico | Gerar Fatura Avulsa

### 6.2 CRUD Drawer — Assinatura

**Largura:** 700px

**Aba: Dados da Assinatura**
| Campo | Tipo | Regras |
|---|---|---|
| Aluno | autocomplete | busca por nome/matrícula/CPF, required |
| Responsável Financeiro | autocomplete | busca por nome/CPF, required |
| Plano | select | required |
| Data de Início | date | required |
| Data de Término | date | opcional (NULL = indeterminado) |
| Valor Negociado | money | pode diferir do plano |
| Desconto aplicado (%) | decimal | 0–100 |
| Motivo do desconto | text | required se desconto > 0 |
| Dia de vencimento | number | 1–28 |
| Número de parcelas | number | 1–24 |
| Método de pagamento | select | |
| Gateway | select | |
| Observação interna | textarea | |

**Aba: Parcelas Geradas**
- Tabela preview de parcelas: nº | vencimento | valor | desconto | valor final | status
- Botão "Regenerar Parcelas"
- Edição inline de vencimento e valor por parcela
- Total do contrato em destaque

**Aba: Responsáveis**
- Responsável financeiro principal
- Responsáveis adicionais (co-devedores)
- E-mails e telefones de cobrança

**Aba: Histórico de Status**
- Timeline de mudanças de status com data, usuário e motivo

### 6.3 Página Detalhe da Assinatura

**Arquivo:** `/resources/views/pages/billing/subscriptions/detail.php`

Seções:
- Header: identificação do aluno + status badge + ações rápidas
- Cards KPI: total contrato | pago | em aberto | atrasado
- Tabela de parcelas com status por linha
- Timeline de eventos (pagamentos, notificações, ajustes)
- Aba Documentos: contrato assinado, comprovantes
- Aba Comunicações: histórico de e-mails/SMS/WhatsApp enviados

---

## 7. Cobrança — Faturas e Boletos

**Arquivo:** `/resources/views/pages/billing/invoices/index.php`  
**Rota:** `GET /billing/invoices`

### 7.1 Toolbar
```
[+ Nova Fatura]  [⚡ Gerar em Lote]  [📤 Exportar]  [🖨 Imprimir Selecionadas]
Filtros: Status | Vencimento | Método | Gateway | Unidade | Turma | Responsável
```

### 7.2 Datatable de Faturas

Colunas: `Selecionar` | `Code` | `Aluno` | `Responsável` | `Descrição` | `Emissão` | `Vencimento` | `Valor` | `Desconto` | `Valor Final` | `Status` | `Método` | `Pago em` | `Ações`

**Status (badges coloridos):**
- `draft` — Rascunho (cinza)
- `pending` — Pendente (azul)
- `sent` — Enviado (roxo)
- `overdue` — Vencido (laranja)
- `paid` — Pago (verde)
- `partial` — Parcialmente Pago (amarelo)
- `cancelled` — Cancelado (vermelho)
- `refunded` — Estornado (rosa)
- `negotiated` — Negociado (índigo)

Seleção múltipla → ações em lote: Enviar | Cancelar | Reenviar | Exportar PDF | Gerar NFSe

### 7.3 CRUD Drawer — Fatura Avulsa

**Largura:** 650px  
**Título:** "Nova Fatura" | "Editar Fatura"

| Campo | Tipo | Regras |
|---|---|---|
| Tipo de Fatura | select | Mensalidade / Matrícula / Material / Serviço / Multa / Avulso |
| Aluno | autocomplete | required |
| Responsável Financeiro | autocomplete | required |
| Assinatura vinculada | autocomplete | opcional |
| Descrição | text | required, max:200 |
| Competência (mês/ano) | month | required |
| Data de Emissão | date | default hoje |
| Data de Vencimento | date | required |
| Valor Bruto | money | required |
| Desconto (R$ ou %) | money/pct | toggle R$/% |
| Acréscimos | money | juros + multa calculados |
| Valor Final | money | readonly, calculado |
| Método de Pagamento | select | |
| Gateway | select | |
| Observação | textarea | |
| Enviar ao responsável | checkbox | default marcado |
| Gerar NFSe | checkbox | |

**Itens da Fatura (tabela):**
- Serviço | Qtd | Valor Unit. | Desconto | Total
- Botão `+ Item`

### 7.4 Página — Geração em Lote

**Arquivo:** `/resources/views/pages/billing/invoices/generate.php`

**Wizard em 4 passos:**

**Passo 1 — Seleção de Alunos**
- Filtros: Unidade | Turma | Nível | Situação de matrícula | Plano
- Datatable de seleção múltipla com checkbox
- Preview: qtd selecionados, valor estimado total

**Passo 2 — Parâmetros da Cobrança**
- Competência | Vencimento | Método | Gateway
- Aplicar desconto de pontualidade? (toggle + dias)
- Gerar NFSe automaticamente? (toggle)

**Passo 3 — Revisão e Confirmação**
- Tabela de preview das faturas a gerar
- Alertas: alunos sem responsável financeiro, plano não configurado
- Total de faturas | Valor total

**Passo 4 — Processamento**
- Barra de progresso em tempo real (WebSocket/SSE)
- Log de erros inline
- Resumo final: sucesso | erros | ignorados

---

## 8. Mensalidades — Gestão Escolar

**Arquivo:** `/resources/views/pages/billing/tuitions/index.php`  
**Rota:** `GET /billing/tuitions`

### 8.1 Controles de Filtro Avançados

```
Turma ▼  |  Nível ▼  |  Turno ▼  |  Situação ▼  |  Mês/Ano ▼  |  Status Financeiro ▼
[🔍 Buscar por aluno/CPF/matrícula]
```

### 8.2 Datatable de Mensalidades

Colunas: `Matrícula` | `Aluno` | `Turma` | `Plano` | `Valor Base` | `Desconto` | `Valor Final` | `Vencimento` | `Status` | `Dias Atraso` | `Multa/Juros` | `Método` | `Ações`

Totalizador por coluna (rodapé): soma de valor base, descontos, valor final, multa acumulada

**Exportação:** Excel (XLSX) | PDF | CSV | Impressão

### 8.3 Matriz de Mensalidades por Turma

**Arquivo:** `/resources/views/pages/billing/tuitions/matrix.php`

- Grid: linhas = alunos, colunas = meses (jan–dez)
- Célula colorida por status: verde=pago, amarelo=a vencer, laranja=vencido, vermelho=inadimplente
- Click na célula: drawer rápido com detalhes da fatura
- Exportação do grid completo
- Totais por linha (aluno) e por coluna (mês)
- Legenda de cores no header

### 8.4 Negociação e Parcelamento

**Arquivo:** `/resources/views/pages/billing/tuitions/negotiation.php`

**CRUD Drawer — Negociação**
| Campo | Tipo |
|---|---|
| Faturas selecionadas | tabela readonly |
| Total em débito | money readonly |
| Tipo de negociação | select (Parcelamento / Desconto / Renegociação) |
| Número de parcelas novas | number |
| Desconto concedido (%) | decimal |
| Entrada | money |
| Vencimento 1ª parcela | date |
| Motivo / justificativa | textarea |
| Aprovador | select (usuário com perfil Gestor+) |
| Documentos anexos | file upload |

Preview das novas parcelas antes de confirmar.

---

## 9. Pagamentos e Baixas

**Arquivo:** `/resources/views/pages/billing/payments/index.php`  
**Rota:** `GET /billing/payments`

### 9.1 Datatable de Pagamentos

Colunas: `Code` | `Fatura` | `Aluno` | `Data Pagamento` | `Valor Pago` | `Desconto` | `Juros/Multa` | `Método` | `Gateway` | `NSU/TID` | `Comprovante` | `Tipo Baixa` | `Ações`

Filtros: Período | Método | Gateway | Tipo de Baixa (Auto/Manual) | Unidade

### 9.2 Drawer — Baixa Manual

| Campo | Tipo | Regras |
|---|---|---|
| Fatura | autocomplete | required |
| Data do Pagamento | date | required |
| Valor Pago | money | required |
| Desconto concedido | money | |
| Juros/Multa cobrados | money | |
| Acréscimos | money | |
| Método de Pagamento | select | required |
| Gateway | select | |
| NSU / TID / Código | text | |
| Banco / Conta | select | |
| Comprovante | file | PDF/JPG/PNG, max 10MB |
| Observação | textarea | |
| Gerar NFSe? | checkbox | |

### 9.3 Conciliação Bancária

**Arquivo:** `/resources/views/pages/billing/payments/conciliation.php`

**Layout em 3 colunas:**
```
┌──────────────────────┬──────────┬──────────────────────┐
│  Extrato Bancário    │  Match   │  Faturas em Aberto   │
│  (OFX/CSV importado) │  Status  │  (sistema)           │
├──────────────────────┼──────────┼──────────────────────┤
│ Data | Valor | Desc  │ ✅/⚠/❌  │ Code | Aluno | Valor │
│ Drag or click match  │          │ Filtros avançados    │
└──────────────────────┴──────────┴──────────────────────┘
```

Funcionalidades:
- Importação OFX / CSV / CNAB 240 / CNAB 400
- Match automático por valor + data + identificador
- Match manual por drag-and-drop
- Regras de conciliação configuráveis
- Histórico de conciliações por data/banco
- Relatório de pendências

---

## 10. Descontos, Bolsas e Isenções

**Arquivo:** `/resources/views/pages/billing/discounts/index.php`

### 10.1 Datatable de Descontos

Colunas: `Code` | `Tipo` | `Nome` | `Percentual/Valor` | `Planos` | `Vigência` | `Beneficiários` | `Status` | `Ações`

**Tipos de Desconto:**
- Pontualidade (automático por data)
- Irmão / Dependente
- Convênio Empresarial
- Funcionário da Instituição
- Bolsa Social / PROUNI
- Bolsa Mérito Acadêmico
- Isenção Total
- Desconto Negociado (manual, aprovação)
- Desconto Campanha

### 10.2 CRUD Drawer — Desconto/Bolsa

| Campo | Tipo |
|---|---|
| Nome do Desconto | text |
| Tipo | select |
| Modalidade | select (% / R$ fixo) |
| Valor | decimal |
| Planos aplicáveis | multiselect |
| Acumulável com outros? | toggle |
| Requer aprovação? | toggle |
| Aprovador responsável | select |
| Documentação exigida | multiselect (checkboxes) |
| Vigência início/fim | date range |
| Cota máxima de beneficiários | number |
| Critérios de elegibilidade | textarea |
| Status | toggle |

### 10.3 Gestão de Bolsas

**Arquivo:** `/resources/views/pages/billing/discounts/scholarships.php`

- Datatable de beneficiários de bolsa com status de renovação
- Widget: % de bolsas concedidas vs cota disponível
- Workflow de aprovação: Solicitado → Em análise → Aprovado → Ativo → Renovação pendente → Expirado
- Documentos de comprovação por beneficiário
- Alertas de bolsas a vencer em 30/60/90 dias

---

## 11. Inadimplência e Régua de Cobrança

**Arquivo:** `/resources/views/pages/billing/delinquency/index.php`  
**Rota:** `GET /billing/delinquency`

### 11.1 Widgets de Inadimplência

| Widget | Conteúdo |
|---|---|
| **Total Inadimplente** | R$ e % da carteira |
| **Aging 1–30 dias** | Qtd alunos + valor |
| **Aging 31–90 dias** | Qtd alunos + valor |
| **Aging 91–180 dias** | Qtd alunos + valor |
| **Aging +180 dias** | Qtd alunos + valor (risco crítico) |
| **Taxa de Recuperação** | % recuperado no mês |

### 11.2 Chart — Evolução da Inadimplência

```
Tipo: XYChart linha dupla
Séries: % Inadimplência (eixo Y esquerdo) + R$ Recuperado (eixo Y direito)
Período: 12 meses rolling
```

### 11.3 Datatable de Inadimplentes

Colunas: `Aluno` | `Turma` | `Responsável` | `Contato` | `Faturas` | `Valor Total` | `Maior Atraso` | `Faixa Aging` | `Última Ação` | `Régua` | `Ações`

Ações: Ligar | Enviar Mensagem | Negociar | Acionar Régua | Bloquear Acesso | Ver Histórico

### 11.4 Régua de Cobrança — Configuração

**Arquivo:** `/resources/views/pages/billing/delinquency/collection-rules.php`

**CRUD Drawer — Régua de Cobrança**
| Campo | Tipo |
|---|---|
| Nome da Régua | text |
| Descrição | textarea |
| Planos aplicáveis | multiselect |
| Disparar a partir de X dias de atraso | number |
| Status | toggle |

**Etapas da Régua (configuráveis):**

Cada etapa: D+X dias | Canal (E-mail/SMS/WhatsApp/Ligação/Carta) | Template | Ação automática | Próxima etapa

Exemplo de régua padrão:
| Etapa | Dia | Canal | Ação |
|---|---|---|---|
| 1 | D+1 | E-mail | Lembrete amigável |
| 2 | D+5 | WhatsApp | Aviso de atraso |
| 3 | D+10 | SMS + E-mail | Notificação formal |
| 4 | D+20 | Ligação automática | Proposta de negociação |
| 5 | D+30 | E-mail jurídico | Aviso de negativação |
| 6 | D+60 | Carta registrada | Notificação extrajudicial |
| 7 | D+90 | Sistema | Bloquear acesso ao portal |

---

## 12. Kanban de Cobranças

**Arquivo:** `/resources/views/pages/billing/kanban/index.php`  
**Rota:** `GET /billing/kanban`

### 12.1 Colunas do Kanban

| Coluna | Status | Cor | Descrição |
|---|---|---|---|
| 📋 Rascunho | `draft` | cinza | Faturas não enviadas |
| 📤 Enviado | `sent` | azul | Enviado ao responsável |
| 👁 Visualizado | `viewed` | roxo | Responsável abriu |
| ⏰ A Vencer | `pending` | amarelo | Vence em ≤ 5 dias |
| ❌ Vencido | `overdue` | laranja | Passou do vencimento |
| 🤝 Negociando | `negotiating` | índigo | Em processo de negociação |
| ✅ Pago | `paid` | verde | Quitado |
| 🚫 Cancelado | `cancelled` | vermelho | Cancelado/Inativo |

### 12.2 Controles do Kanban

**Toolbar:**
```
[Filtro: Unidade ▼]  [Filtro: Turma ▼]  [Filtro: Responsável ▼]
[Período ▼]  [🔍 Buscar]  [⚙ Configurar Colunas]  [📊 Modo Lista]
```

**Cards no Kanban:**
```
┌─────────────────────────────┐
│ 👤 João da Silva            │
│ 📚 3º Ano A                 │
│ 📅 Vence: 15/06/2026        │
│ 💰 R$ 850,00                │
│ [PIX] [Boleto]              │
│ 🔴 3 dias de atraso         │
│ ──────────────────          │
│ [Ver] [Enviar] [Negociar]   │
└─────────────────────────────┘
```

### 12.3 Interatividade
- Drag & drop de cards entre colunas com confirmação de mudança de status
- Click no card: drawer lateral com detalhes da fatura
- Ações rápidas no hover: Enviar lembrete | Baixar | Negociar
- Contador e total financeiro no header de cada coluna
- Scroll infinito ou paginação por coluna
- Modo compacto (lista) / modo expandido (cards)

---

## 13. Automações e Régua Inteligente

**Arquivo:** `/resources/views/pages/billing/automations/index.php`  
**Rota:** `GET /billing/automations`

### 13.1 Datatable de Automações

Colunas: `Code` | `Nome` | `Tipo` | `Gatilho` | `Última Execução` | `Próxima Execução` | `Sucesso` | `Erros` | `Status` | `Ações`

### 13.2 CRUD Drawer — Automação

**Aba: Configuração Geral**
| Campo | Tipo |
|---|---|
| Nome da Automação | text |
| Descrição | textarea |
| Tipo | select (ver abaixo) |
| Status | toggle Ativo/Pausado |
| Prioridade | select (Alta/Média/Baixa) |
| Responsável | select usuário |

**Tipos de Automação:**
1. **Geração de Faturas** — automática por plano/data
2. **Envio de Boleto/PIX** — X dias antes do vencimento
3. **Lembrete de Vencimento** — D-5, D-2, D-1
4. **Notificação de Atraso** — conforme régua de cobrança
5. **Baixa Automática** — retorno de gateway (webhook)
6. **Emissão de NFSe** — após confirmação de pagamento
7. **Renegociação Automática** — proposta após X dias
8. **Bloqueio de Acesso** — inadimplência > X dias
9. **Relatório Automático** — envio de resumo periódico
10. **Conciliação Bancária** — OFX importado automaticamente

**Aba: Gatilho (Trigger)**
| Campo | Tipo |
|---|---|
| Tipo de Gatilho | select (Cron / Evento / Webhook / Manual) |
| Expressão Cron | text (com validador visual) |
| Evento disparador | select (Fatura criada / Pagamento / Vencimento / etc.) |
| Condições adicionais | builder visual (campo + operador + valor) |

**Aba: Ação**
| Campo | Tipo |
|---|---|
| Canal de envio | multiselect (Email/SMS/WhatsApp/Push) |
| Template de mensagem | select |
| Variáveis disponíveis | lista de tokens {{nome}}, {{valor}}, etc. |
| Preview do template | área de renderização |
| Ação no sistema | select (Atualizar status / Bloquear / Gerar doc) |

**Aba: Filtros de Público**
- Unidades | Planos | Status de inadimplência | Faixa de valor | Tags de aluno

**Aba: Logs**
- Tabela: Data | Status | Público impactado | Mensagens enviadas | Erros
- Link para detalhe por execução

### 13.3 Página de Logs de Automação

**Arquivo:** `/resources/views/pages/billing/automations/logs.php`

- Timeline de execuções
- Detalhamento por registro processado
- Reprocessar erros individualmente
- Exportar log em CSV

---

## 14. Notas Fiscais de Serviço (NFSe)

**Arquivo:** `/resources/views/pages/billing/nfse/index.php`  
**Rota:** `GET /billing/nfse`

### 14.1 Datatable de NFSe

Colunas: `Número NF` | `Aluno/Tomador` | `Competência` | `Serviço` | `Valor` | `ISS` | `Data Emissão` | `Status` | `XML` | `PDF` | `Ações`

**Status NFSe:** Pendente | Processando | Emitida | Cancelada | Rejeitada (com erro)

### 14.2 Drawer — Emissão Manual NFSe

| Campo | Tipo |
|---|---|
| Fatura vinculada | autocomplete |
| Tomador (Nome/CNPJ/CPF) | autocomplete |
| Endereço do tomador | form address |
| Código do Serviço LC116 | select |
| Discriminação do Serviço | textarea |
| Competência | month |
| Valor do Serviço | money readonly |
| Deduções | money |
| Base de Cálculo ISS | money readonly |
| Alíquota ISS (%) | decimal |
| ISS a Reter? | toggle |
| Regime Especial | select |
| Informações Complementares | textarea |

### 14.3 Configuração NFSe

**Arquivo:** `/resources/views/pages/billing/nfse/config.php`

- Dados da empresa prestadora (razão, CNPJ, IM, CNAE)
- Configuração por prefeitura (API endpoint, certificado A1)
- Alíquotas de ISS por serviço
- Regime tributário
- E-mail padrão de envio da NF ao tomador
- Teste de integração com prefeitura

---

## 15. Conciliação Bancária

**Arquivo:** `/resources/views/pages/billing/conciliation/index.php`

### 15.1 Widgets de Conciliação

| Widget | Valor |
|---|---|
| Transações Importadas | Qtd no período |
| Match Automático | Qtd + % |
| Match Manual | Qtd |
| Pendentes | Qtd + R$ (alerta) |
| Saldo Extrato | R$ |
| Saldo Sistema | R$ |
| Diferença | R$ (deve ser zero) |

### 15.2 Importação de Extrato

- Upload de arquivo: OFX / CSV / CNAB 240 / CNAB 400
- Preview automático antes de importar
- Validação de duplicidade
- Histórico de importações

### 15.3 Regras de Conciliação Automática

**CRUD Drawer — Regra**
| Campo | Tipo |
|---|---|
| Nome da Regra | text |
| Campo de match | select (Valor / Descrição / NSU / Código de barras) |
| Tolerância de valor (R$) | decimal |
| Tolerância de data (dias) | number |
| Prioridade | number |
| Status | toggle |

---

## 16. Relatórios e Exportações

**Arquivo:** `/resources/views/pages/billing/reports/`

### 16.1 Relatório de Receita

**Filtros:** Período | Unidade | Plano | Nível | Método | Status

**Seções:**
- KPIs no topo: Previsto | Realizado | Inadimplente | Cancelado
- Chart de receita mensal (coluna)
- Chart de composição por tipo (donut)
- Datatable detalhado com exportação

### 16.2 Aging de Inadimplência

- Faixas: 1-30 / 31-60 / 61-90 / 91-180 / +180 dias
- Filtros: Unidade | Turma | Nível | Responsável
- Exportação para cobrança terceirizada (CSV padrão)

### 16.3 Relatório de Fluxo de Caixa

- Previsto x Realizado por dia/semana/mês
- Gráfico de linha dupla amCharts 5
- Tabela com entradas por data

### 16.4 Previsão de Recebimento (Forecast)

- Projeção baseada em histórico + faturas em aberto
- Cenários: Otimista / Realista / Conservador
- Chart de área com bandas de confiança

### 16.5 Exportações Disponíveis em Todas as Telas
- Excel (XLSX) — formatado com totais
- CSV — padrão UTF-8 BOM para Excel BR
- PDF — layout relatório com logo da instituição
- Impressão direta

---

## 17. Configurações do Módulo

**Arquivo:** `/resources/views/pages/billing/settings/`

### 17.1 Gateways de Pagamento

**Arquivo:** `gateways.php`

Datatable: Gateway | Ambiente | Status | Webhooks | Última sync | Ações

**Drawer — Configurar Gateway:**
- Asaas: API Key | Carteira | Webhook URL
- PagSeguro: Token | E-mail | Sandbox toggle
- Mercado Pago: Access Token | Public Key
- Gerencianet/EFÍ: Client ID | Client Secret | Certificado PIX (upload .p12/.pem)
- Stripe: Secret Key | Publishable Key | Webhook Secret
- Teste de conectividade com resultado imediato

### 17.2 Métodos de Pagamento

**Arquivo:** `payment-methods.php`

- Ativar/desativar por método: Boleto | PIX | Cartão Crédito | Cartão Débito | Débito Automático | Transferência | Dinheiro
- Configurar juros e multa por método
- Configurar prazo de compensação

### 17.3 Calendário de Vencimentos

**Arquivo:** `due-dates.php`

- Definir dias úteis vs dias corridos
- Feriados cadastrados (federal + estadual + municipal)
- Regra de vencimento em final de semana/feriado: avançar ou recuar
- Dias de vencimento padrão por plano

### 17.4 Templates de Notificação

**Arquivo:** `notifications.php`

| Template | Canal | Variáveis |
|---|---|---|
| Fatura emitida | E-mail, WhatsApp | {{nome}}, {{valor}}, {{vencimento}}, {{link}} |
| Lembrete vencimento | SMS, E-mail | {{dias_restantes}}, {{link_boleto}} |
| Fatura vencida | E-mail, WhatsApp | {{dias_atraso}}, {{multa}}, {{juros}} |
| Pagamento confirmado | E-mail, WhatsApp | {{valor_pago}}, {{data_pagamento}} |
| Negociação aprovada | E-mail | {{parcelas}}, {{novo_vencimento}} |
| NFSe emitida | E-mail | {{numero_nf}}, {{link_nfse}} |

- Editor HTML inline para e-mail
- Preview em dispositivo (desktop/mobile)
- Variáveis disponíveis com documentação

---

## 18. APIs REST — Endpoints

**Base URL:** `/api/v1/billing/`  
**Auth:** Bearer JWT — header `Authorization: Bearer {token}`  
**Rate Limit:** 120 req/min por usuário

### 18.1 Planos
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/plans` | Listar planos (paginado) |
| POST | `/plans` | Criar plano |
| GET | `/plans/{uuid}` | Detalhar plano |
| PUT | `/plans/{uuid}` | Atualizar plano |
| DELETE | `/plans/{uuid}` | Soft delete |
| GET | `/plans/{uuid}/pricing` | Tabela de preços do plano |

### 18.2 Assinaturas
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/subscriptions` | Listar assinaturas |
| POST | `/subscriptions` | Criar assinatura |
| GET | `/subscriptions/{uuid}` | Detalhar |
| PUT | `/subscriptions/{uuid}` | Atualizar |
| POST | `/subscriptions/{uuid}/suspend` | Suspender |
| POST | `/subscriptions/{uuid}/cancel` | Cancelar |
| GET | `/subscriptions/{uuid}/invoices` | Faturas da assinatura |

### 18.3 Faturas
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/invoices` | Listar faturas |
| POST | `/invoices` | Criar fatura |
| POST | `/invoices/batch` | Geração em lote |
| GET | `/invoices/{uuid}` | Detalhar |
| PUT | `/invoices/{uuid}` | Atualizar |
| POST | `/invoices/{uuid}/send` | Enviar ao responsável |
| POST | `/invoices/{uuid}/cancel` | Cancelar |
| POST | `/invoices/{uuid}/write-off` | Baixa manual |
| GET | `/invoices/{uuid}/pdf` | Download PDF |

### 18.4 Pagamentos
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/payments` | Listar pagamentos |
| POST | `/payments` | Registrar pagamento manual |
| GET | `/payments/{uuid}` | Detalhar |
| POST | `/payments/{uuid}/refund` | Estornar |
| POST | `/webhooks/{gateway}` | Webhook do gateway |

### 18.5 Descontos e Bolsas
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/discounts` | Listar descontos |
| POST | `/discounts` | Criar desconto |
| PUT | `/discounts/{uuid}` | Atualizar |
| DELETE | `/discounts/{uuid}` | Soft delete |
| GET | `/scholarships` | Listar bolsas |
| POST | `/scholarships` | Conceder bolsa |
| PUT | `/scholarships/{uuid}/renew` | Renovar bolsa |

### 18.6 NFSe
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/nfse` | Listar notas |
| POST | `/nfse` | Emitir nota |
| GET | `/nfse/{uuid}` | Detalhar |
| POST | `/nfse/{uuid}/cancel` | Cancelar nota |
| GET | `/nfse/{uuid}/pdf` | Download PDF |
| GET | `/nfse/{uuid}/xml` | Download XML |

### 18.7 Automações
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/automations` | Listar automações |
| POST | `/automations` | Criar automação |
| PUT | `/automations/{uuid}` | Atualizar |
| POST | `/automations/{uuid}/run` | Executar manualmente |
| POST | `/automations/{uuid}/pause` | Pausar |
| GET | `/automations/{uuid}/logs` | Logs de execução |

### 18.8 Payload Padrão de Resposta
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 25,
    "total": 1240,
    "last_page": 50
  },
  "errors": null,
  "timestamp": "2026-06-07T03:00:00-03:00"
}
```

---

## 19. Schema SQL

### 19.1 Tabelas do Banco de Unidade

```sql
-- PLANOS
CREATE TABLE billing_plans (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID()),
    code VARCHAR(30) NOT NULL,
    name VARCHAR(120) NOT NULL,
    description TEXT,
    type ENUM('tuition','enrollment','material','service','fee','other') NOT NULL,
    periodicity ENUM('monthly','bimonthly','quarterly','semiannual','annual','one_time') NOT NULL,
    base_amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    min_amount DECIMAL(12,2),
    max_amount DECIMAL(12,2),
    currency CHAR(3) NOT NULL DEFAULT 'BRL',
    status ENUM('active','inactive','archived') NOT NULL DEFAULT 'active',
    valid_from DATE NOT NULL,
    valid_until DATE,
    metadata JSON,
    created_by BIGINT UNSIGNED,
    updated_by BIGINT UNSIGNED,
    deleted_by BIGINT UNSIGNED,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uk_plans_uuid (uuid),
    UNIQUE KEY uk_plans_code (code),
    INDEX idx_plans_status (status),
    INDEX idx_plans_type (type)
);

-- ASSINATURAS
CREATE TABLE billing_subscriptions (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID()),
    code VARCHAR(30) NOT NULL,
    student_id BIGINT UNSIGNED NOT NULL,
    payer_id BIGINT UNSIGNED NOT NULL,
    plan_id BIGINT UNSIGNED NOT NULL,
    negotiated_amount DECIMAL(12,2) NOT NULL,
    discount_percent DECIMAL(5,2) DEFAULT 0.00,
    discount_reason TEXT,
    due_day TINYINT UNSIGNED NOT NULL DEFAULT 10,
    installments SMALLINT UNSIGNED DEFAULT 12,
    payment_method ENUM('boleto','pix','credit_card','debit_card','direct_debit','transfer','cash') NOT NULL,
    gateway_id BIGINT UNSIGNED,
    gateway_subscription_id VARCHAR(120),
    status ENUM('active','suspended','cancelled','completed','pending') NOT NULL DEFAULT 'pending',
    starts_at DATE NOT NULL,
    ends_at DATE,
    cancelled_at DATETIME,
    cancellation_reason TEXT,
    metadata JSON,
    created_by BIGINT UNSIGNED,
    updated_by BIGINT UNSIGNED,
    deleted_at DATETIME NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_sub_uuid (uuid),
    UNIQUE KEY uk_sub_code (code),
    INDEX idx_sub_student (student_id),
    INDEX idx_sub_status (status),
    INDEX idx_sub_plan (plan_id)
);

-- FATURAS
CREATE TABLE billing_invoices (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID()),
    code VARCHAR(30) NOT NULL,
    subscription_id BIGINT UNSIGNED,
    student_id BIGINT UNSIGNED NOT NULL,
    payer_id BIGINT UNSIGNED NOT NULL,
    type ENUM('tuition','enrollment','material','service','fine','other') NOT NULL,
    description VARCHAR(200) NOT NULL,
    competence_month TINYINT UNSIGNED,
    competence_year SMALLINT UNSIGNED,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    gross_amount DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(12,2) DEFAULT 0.00,
    fine_amount DECIMAL(12,2) DEFAULT 0.00,
    interest_amount DECIMAL(12,2) DEFAULT 0.00,
    net_amount DECIMAL(12,2) NOT NULL,
    paid_amount DECIMAL(12,2) DEFAULT 0.00,
    payment_method ENUM('boleto','pix','credit_card','debit_card','direct_debit','transfer','cash'),
    gateway_id BIGINT UNSIGNED,
    gateway_invoice_id VARCHAR(120),
    barcode VARCHAR(100),
    pix_key VARCHAR(200),
    pix_qrcode TEXT,
    boleto_url VARCHAR(500),
    status ENUM('draft','pending','sent','viewed','paid','partial','overdue','negotiated','cancelled','refunded') NOT NULL DEFAULT 'draft',
    sent_at DATETIME,
    paid_at DATETIME,
    cancelled_at DATETIME,
    nfse_id BIGINT UNSIGNED,
    metadata JSON,
    created_by BIGINT UNSIGNED,
    updated_by BIGINT UNSIGNED,
    deleted_at DATETIME NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_inv_uuid (uuid),
    UNIQUE KEY uk_inv_code (code),
    INDEX idx_inv_student (student_id),
    INDEX idx_inv_due_date (due_date),
    INDEX idx_inv_status (status),
    INDEX idx_inv_competence (competence_year, competence_month)
);

-- PAGAMENTOS
CREATE TABLE billing_payments (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID()),
    code VARCHAR(30) NOT NULL,
    invoice_id BIGINT UNSIGNED NOT NULL,
    paid_at DATETIME NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(12,2) DEFAULT 0.00,
    fine_amount DECIMAL(12,2) DEFAULT 0.00,
    interest_amount DECIMAL(12,2) DEFAULT 0.00,
    net_amount DECIMAL(12,2) NOT NULL,
    payment_method ENUM('boleto','pix','credit_card','debit_card','direct_debit','transfer','cash') NOT NULL,
    gateway_id BIGINT UNSIGNED,
    gateway_payment_id VARCHAR(120),
    nsu VARCHAR(60),
    tid VARCHAR(60),
    write_off_type ENUM('automatic','manual') NOT NULL DEFAULT 'automatic',
    bank_account_id BIGINT UNSIGNED,
    receipt_path VARCHAR(500),
    conciliation_id BIGINT UNSIGNED,
    notes TEXT,
    created_by BIGINT UNSIGNED,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_pay_uuid (uuid),
    INDEX idx_pay_invoice (invoice_id),
    INDEX idx_pay_paid_at (paid_at),
    INDEX idx_pay_gateway (gateway_payment_id)
);

-- DESCONTOS
CREATE TABLE billing_discounts (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID()),
    code VARCHAR(30) NOT NULL,
    name VARCHAR(120) NOT NULL,
    type ENUM('punctuality','sibling','agreement','employee','scholarship','merit','exemption','negotiated','campaign') NOT NULL,
    modality ENUM('percent','fixed') NOT NULL DEFAULT 'percent',
    value DECIMAL(10,2) NOT NULL,
    is_cumulative TINYINT(1) DEFAULT 0,
    requires_approval TINYINT(1) DEFAULT 0,
    approver_id BIGINT UNSIGNED,
    max_beneficiaries INT UNSIGNED,
    valid_from DATE,
    valid_until DATE,
    criteria TEXT,
    status ENUM('active','inactive') NOT NULL DEFAULT 'active',
    created_by BIGINT UNSIGNED,
    updated_by BIGINT UNSIGNED,
    deleted_at DATETIME NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_disc_uuid (uuid),
    UNIQUE KEY uk_disc_code (code)
);

-- AUTOMAÇÕES DE COBRANÇA
CREATE TABLE billing_automations (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID()),
    code VARCHAR(30) NOT NULL,
    name VARCHAR(120) NOT NULL,
    description TEXT,
    type ENUM('invoice_generation','send_boleto','due_reminder','overdue_notification','auto_write_off','nfse_emission','renegotiation','access_block','report','bank_conciliation') NOT NULL,
    trigger_type ENUM('cron','event','webhook','manual') NOT NULL,
    cron_expression VARCHAR(60),
    trigger_event VARCHAR(80),
    conditions JSON,
    action_config JSON,
    audience_filters JSON,
    status ENUM('active','paused','error') NOT NULL DEFAULT 'active',
    last_run_at DATETIME,
    next_run_at DATETIME,
    run_count INT UNSIGNED DEFAULT 0,
    error_count INT UNSIGNED DEFAULT 0,
    priority ENUM('high','medium','low') DEFAULT 'medium',
    created_by BIGINT UNSIGNED,
    updated_by BIGINT UNSIGNED,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_aut_uuid (uuid)
);

-- NOTAS FISCAIS (NFSe)
CREATE TABLE billing_nfse (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID()),
    invoice_id BIGINT UNSIGNED,
    numero VARCHAR(20),
    serie VARCHAR(5),
    payer_id BIGINT UNSIGNED NOT NULL,
    service_code VARCHAR(20),
    service_description TEXT,
    competence_month TINYINT UNSIGNED,
    competence_year SMALLINT UNSIGNED,
    gross_amount DECIMAL(12,2) NOT NULL,
    deductions DECIMAL(12,2) DEFAULT 0.00,
    iss_base DECIMAL(12,2) NOT NULL,
    iss_rate DECIMAL(5,4) NOT NULL,
    iss_amount DECIMAL(12,2) NOT NULL,
    iss_retained TINYINT(1) DEFAULT 0,
    status ENUM('pending','processing','issued','cancelled','rejected') NOT NULL DEFAULT 'pending',
    issue_date DATETIME,
    cancel_date DATETIME,
    verification_code VARCHAR(50),
    pdf_path VARCHAR(500),
    xml_path VARCHAR(500),
    gateway_response JSON,
    error_message TEXT,
    created_by BIGINT UNSIGNED,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_nfse_uuid (uuid),
    INDEX idx_nfse_invoice (invoice_id),
    INDEX idx_nfse_status (status)
);

-- RÉGUA DE COBRANÇA
CREATE TABLE billing_collection_rules (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID()),
    name VARCHAR(120) NOT NULL,
    description TEXT,
    trigger_after_days TINYINT UNSIGNED NOT NULL DEFAULT 1,
    status ENUM('active','inactive') NOT NULL DEFAULT 'active',
    created_by BIGINT UNSIGNED,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE billing_collection_rule_steps (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    rule_id BIGINT UNSIGNED NOT NULL,
    step_order TINYINT UNSIGNED NOT NULL,
    day_offset TINYINT UNSIGNED NOT NULL,
    channel ENUM('email','sms','whatsapp','call','letter','system') NOT NULL,
    template_id BIGINT UNSIGNED,
    system_action ENUM('none','block_access','send_to_legal','propose_negotiation') DEFAULT 'none',
    PRIMARY KEY (id),
    INDEX idx_steps_rule (rule_id)
);
```

---

## 20. RBAC — Permissões por Perfil

| Funcionalidade | Super Admin | Admin Entidade | Gestor Unidade | Coord. Financeiro | Operador | Consulta |
|---|---|---|---|---|---|---|
| Dashboard Billing | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (readonly) |
| Criar/Editar Planos | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Criar Assinaturas | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Gerar Faturas em Lote | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Baixa Manual | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Cancelar Faturas | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Conceder Desconto > 30% | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Negociação/Parcelamento | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Emitir NFSe | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Cancelar NFSe | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Configurar Gateways | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Configurar Automações | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Conciliação Bancária | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Ver Relatórios | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| Exportar Dados | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Acessar Dados LGPD | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## 21. Auditoria e LGPD

### 21.1 Eventos Auditados (audit_logs)

| Evento | Dados Capturados |
|---|---|
| `invoice.created` | invoice_id, student_id, amount, user_id, ip |
| `invoice.sent` | invoice_id, channel, recipient |
| `invoice.paid` | invoice_id, payment_id, amount, gateway |
| `invoice.cancelled` | invoice_id, reason, user_id |
| `payment.manual_write_off` | payment_id, invoice_id, amount, user_id |
| `discount.granted` | discount_id, student_id, value, approver_id |
| `scholarship.approved` | scholarship_id, student_id, approver_id |
| `nfse.issued` | nfse_id, invoice_id, numero, user_id |
| `nfse.cancelled` | nfse_id, reason, user_id |
| `automation.executed` | automation_id, affected_count, errors |
| `gateway.configured` | gateway_id, user_id (sem dados sensíveis) |
| `data.exported` | endpoint, filters, user_id, ip, record_count |

### 21.2 Proteção de Dados (LGPD/GDPR)

- **Dados financeiros** classificados como sensíveis — acesso restrito por perfil
- **CPF/CNPJ** mascarados em interfaces de menor privilégio (`***.xxx.xxx-**`)
- **Dados de cartão** NUNCA armazenados localmente (PCI DSS compliance via gateway tokenização)
- **Exportações** registradas em audit_log com justificativa obrigatória
- **Retenção:** dados financeiros retidos por 10 anos (obrigação fiscal)
- **Consentimento:** responsável financeiro deve consentir envio de cobranças por canal digital (LGPD art. 7)
- **Anonimização:** após cancelamento e expiração de retenção, dados pessoais anonimizados

---

## 22. Critérios de Aceite

### 22.1 Funcionais
- [ ] Dashboard carrega em < 2s com 10.000+ faturas
- [ ] Geração em lote de 500+ faturas em < 60s com feedback em tempo real
- [ ] Kanban suporta drag & drop com confirmação de status
- [ ] Automações executam no horário configurado com tolerância ≤ 5min
- [ ] Baixa automática via webhook processa em < 30s após confirmação do gateway
- [ ] NFSe emitida em < 2min após acionamento
- [ ] Conciliação automática com match ≥ 95% em base padrão
- [ ] Todos os formulários validam client-side E server-side
- [ ] Exportações funcionam para Excel/CSV/PDF em todas as telas de listagem

### 22.2 Segurança
- [ ] Todas as rotas verificam permissão RBAC antes de processar
- [ ] Webhooks de gateway validados por assinatura HMAC
- [ ] Dados de cartão nunca trafegam pelo backend (tokenização no frontend via SDK do gateway)
- [ ] Chaves de API de gateway armazenadas criptografadas (AES-256)
- [ ] Rate limiting ativo em todos os endpoints da API
- [ ] Audit log gravado para cada operação financeira crítica

### 22.3 UX / Interface
- [ ] Todos os drawers têm loading state, tratamento de erro e feedback de sucesso
- [ ] Datatable com paginação server-side, busca e ordenação por coluna
- [ ] Charts responsivos para telas ≥ 768px
- [ ] Kanban responsivo com scroll horizontal em mobile
- [ ] Ações em lote sempre precedidas de modal de confirmação com contagem de registros
- [ ] Status badges consistentes com o design system ttsc-/Supabase

### 22.4 Performance
- [ ] Queries indexadas por unit_id, status, due_date, student_id
- [ ] Cache de dashboard KPIs com TTL de 5 minutos
- [ ] Paginação server-side em todos os datatables (max 50 registros/página)
- [ ] Lazy load de charts (só renderiza quando visível no viewport)

---

*Documento gerado em: 2026-06-07 — TotusTuusSoftCloud — Módulo: Billing / Cobrança e Mensalidades*
