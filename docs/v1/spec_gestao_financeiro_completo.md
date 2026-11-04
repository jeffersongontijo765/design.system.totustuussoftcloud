# SPEC — Módulo Financeiro
**Projeto:** TotusTuusSoftCloud  
**Stack:** PHP 8 (puro) · JavaScript · Tailwind CSS 4.2 · Supabase · amCharts 5 · MariaDB/InnoDB  
**Arquitetura:** Multi-tenant · Multi-entity · Multi-unit · Multi-user  
**Padrão de ID:** `id` (PK ordenação) · `uuid` (interno) · `code` (externo)  
**Versão:** 1.0.0  
**Data:** 2026-06-06  

- Language Standard: Global English
---

## Índice

1. [Visão Geral](#1-visão-geral)  
2. [Estrutura de Páginas](#2-estrutura-de-páginas)  
3. [Dashboard Financeiro](#3-dashboard-financeiro)  
4. [Contas a Receber](#4-contas-a-receber)  
5. [Contas a Pagar](#5-contas-a-pagar)  
6. [Fluxo de Caixa](#6-fluxo-de-caixa)  
7. [Conciliação Bancária](#7-conciliação-bancária)  
8. [Centros de Custo](#8-centros-de-custo)  
9. [Orçamentos](#9-orçamentos)  
10. [Contratos Financeiros](#10-contratos-financeiros)  
11. [Cobranças e Inadimplência](#11-cobranças-e-inadimplência)  
12. [Relatórios Financeiros](#12-relatórios-financeiros)  
13. [Automações](#13-automações)  
14. [Gerenciamentos](#14-gerenciamentos)  
15. [Controles Globais](#15-controles-globais)  
16. [Esquema SQL Base](#16-esquema-sql-base)  
17. [Rotas da API REST](#17-rotas-da-api-rest)  
18. [Permissões por Perfil](#18-permissões-por-perfil)  
19. [Checklist de Entrega](#19-checklist-de-entrega)  

---

## 1. Visão Geral

O módulo **Financeiro** é responsável por toda a gestão de receitas, despesas, fluxo de caixa, cobranças, contratos, orçamentos e conciliação bancária da plataforma SaaS. Opera de forma isolada por unidade (banco de dados por unidade) e sincroniza consolidações no banco da entidade.

### 1.1 Domínios do Módulo

| Domínio              | Responsabilidade                                              |
|----------------------|---------------------------------------------------------------|
| Contas a Receber     | Títulos, parcelas, boletos, PIX, cartão                      |
| Contas a Pagar       | Despesas, fornecedores, NF-e, pagamentos                     |
| Fluxo de Caixa       | Projeção, realizado, saldo, gaps                             |
| Conciliação Bancária | OFX, extrato, matching automático                            |
| Centros de Custo     | Rateio, alocação, controle orçamentário                      |
| Orçamentos           | Previsão anual/mensal, desvios, alertas                      |
| Contratos            | Recorrências, reajustes, vencimentos                         |
| Cobranças            | Régua de cobrança, notificações, inadimplência               |
| Relatórios           | DRE, Balanço resumido, Fluxo projetado                       |

### 1.2 Entidades Principais

```
financial_receivables      → Contas a receber
financial_payables         → Contas a pagar
financial_transactions     → Transações realizadas
financial_bank_accounts    → Contas bancárias
financial_bank_statements  → Extratos / OFX
financial_reconciliations  → Conciliações
financial_cost_centers     → Centros de custo
financial_budgets          → Orçamentos
financial_contracts        → Contratos financeiros
financial_charges          → Régua de cobranças
financial_categories       → Categorias financeiras
financial_payment_methods  → Métodos de pagamento
```

---

## 2. Estrutura de Páginas

```
/financial
├── /dashboard                    → Dashboard principal
├── /receivables
│   ├── /list                     → Datatable contas a receber
│   ├── /kanban                   → Kanban por status
│   └── /overdue                  → Inadimplência
├── /payables
│   ├── /list                     → Datatable contas a pagar
│   └── /kanban                   → Kanban por status
├── /cash-flow
│   ├── /daily                    → Fluxo diário
│   └── /projected                → Fluxo projetado
├── /bank
│   ├── /accounts                 → Contas bancárias
│   ├── /statements               → Extratos
│   └── /reconciliation           → Conciliação OFX
├── /cost-centers                 → Centros de custo
├── /budgets                      → Orçamentos
├── /contracts                    → Contratos financeiros
├── /charges                      → Régua de cobrança
├── /reports
│   ├── /dre                      → DRE
│   ├── /balance                  → Balanço resumido
│   └── /cash-flow-report         → Relatório de fluxo
└── /settings
    ├── /categories                → Categorias financeiras
    ├── /payment-methods           → Métodos de pagamento
    └── /automations               → Automações
```

---

## 3. Dashboard Financeiro

**Rota:** `GET /financial/dashboard`  
**Componente:** `financial_dashboard.php`

### 3.1 Widgets — Linha 1 (KPIs Principais)

| Widget                  | Valor                  | Ícone      | Cor       | Variação |
|-------------------------|------------------------|------------|-----------|----------|
| Saldo em Caixa          | R$ total consolidado   | wallet     | primary   | vs mês anterior |
| A Receber (30 dias)     | R$ a vencer            | arrow-up   | success   | % crescimento |
| A Pagar (30 dias)       | R$ a pagar             | arrow-down | danger    | % crescimento |
| Inadimplência           | R$ em atraso           | alert      | warning   | Δ vs mês |
| Receita do Mês          | R$ recebido no mês     | trending-up| info      | vs mês ant. |
| Despesa do Mês          | R$ pago no mês         | trending-down| dark    | vs mês ant. |

> Todos os widgets são clicáveis e redirecionam para a página relacionada.  
> Período configurável: Hoje / 7d / 30d / 90d / Personalizado.

### 3.2 Widgets — Linha 2 (Operacional)

| Widget                  | Tipo            | Descrição                             |
|-------------------------|-----------------|---------------------------------------|
| Próximos Vencimentos    | Lista compacta  | Top 5 títulos a vencer em 7 dias     |
| Alertas de Saldo        | Badges + lista  | Contas abaixo do limite mínimo        |
| Aprovações Pendentes    | Counter badge   | Pagamentos aguardando aprovação       |
| Conciliação Pendente    | Counter badge   | Lançamentos não conciliados           |

### 3.3 Charts

#### Chart 1 — Fluxo de Caixa (Linha dupla)
```
Tipo: amCharts 5 — XYChart (line)
Séries:
  - Receitas realizadas (verde)
  - Despesas realizadas (vermelho)
  - Saldo acumulado (azul — linha tracejada)
Período: últimos 12 meses
Drill-down: clique no mês abre modal com lançamentos do período
Controles: toggle por série, exportar PNG/CSV
```

#### Chart 2 — Composição de Receitas (Donut)
```
Tipo: amCharts 5 — PieChart (donut)
Dados: receitas agrupadas por categoria
Legenda: lateral com valores e percentuais
Filtro: mês atual / trimestre / ano
```

#### Chart 3 — Contas a Receber vs Pagar (Barras agrupadas)
```
Tipo: amCharts 5 — XYChart (column)
Séries:
  - A Receber (azul)
  - A Pagar (laranja)
Eixo X: próximos 6 meses
Tooltip: valor + qtd de títulos
```

#### Chart 4 — Inadimplência por Faixa de Atraso (Barras horizontais)
```
Tipo: amCharts 5 — XYChart (bar horizontal)
Faixas: 1-30d / 31-60d / 61-90d / 90d+
Dados: valor e quantidade por faixa
Cor: gradiente warning → danger
```

#### Chart 5 — Orçado vs Realizado (Gauge + Barras)
```
Tipo: amCharts 5 — XYChart (column) + GaugeChart
Dados: % de execução do orçamento mensal
Indicadores: abaixo / dentro / acima do orçamento
```

### 3.4 Kanban Rápido — Aprovações do Dia

```
Colunas:
  [Pendente] → [Em Análise] → [Aprovado] → [Rejeitado]

Card de Aprovação:
  - Fornecedor / Beneficiário
  - Valor
  - Vencimento
  - Centro de custo
  - Ações: [Aprovar] [Rejeitar] [Ver Detalhes]
```

### 3.5 Controles do Dashboard

```
[ Período ▼ ] [ Unidade ▼ ] [ Centro de Custo ▼ ] [ Exportar ▼ ] [ Atualizar ]
```

---

## 4. Contas a Receber

**Rota:** `GET /financial/receivables/list`  
**Componente:** `financial_receivables_list.php`

### 4.1 Controles da Página

```
Barra superior:
[ + Novo Título ]  [ Importar ▼ ]  [ Exportar ▼ ]  [ Ações em Lote ▼ ]

Filtros:
[ Status ▼ ]  [ Categoria ▼ ]  [ Vencimento: De___ Até___ ]
[ Método de Pagamento ▼ ]  [ Centro de Custo ▼ ]  [ Cliente 🔍 ]
[ Valor: Min___ Max___ ]  [ Parcela ▼ ]  [ Busca Geral 🔍 ]  [ Limpar ]
```

### 4.2 Datatable — Contas a Receber

| Coluna          | Tipo         | Ordenável | Filtro | Observação                          |
|-----------------|--------------|-----------|--------|-------------------------------------|
| ☐               | Checkbox     | —         | —      | Seleção múltipla                    |
| Código          | text         | ✓         | ✓      | `code` externo                     |
| Cliente         | text+avatar  | ✓         | ✓      | Link para cadastro                  |
| Descrição       | text         | ✓         | ✓      |                                     |
| Categoria       | badge        | ✓         | ✓      |                                     |
| Emissão         | date         | ✓         | ✓      |                                     |
| Vencimento      | date+badge   | ✓         | ✓      | Badge vermelho se vencido           |
| Parcelas        | text         | —         | —      | 1/3, 2/3, etc.                      |
| Valor           | currency     | ✓         | —      |                                     |
| Desconto        | currency     | —         | —      |                                     |
| Juros/Multa     | currency     | —         | —      |                                     |
| Valor Líquido   | currency     | ✓         | —      | Negrito                             |
| Status          | badge        | ✓         | ✓      | Aberto/Parcial/Pago/Cancelado/Atrasado |
| Método Pgto     | icon+text    | ✓         | ✓      |                                     |
| Recebido em     | date         | ✓         | ✓      |                                     |
| Ações           | buttons      | —         | —      | Ver / Editar / Receber / Cancelar   |

**Linha de Totais (rodapé fixo):**
```
Total Selecionado: R$ ___  |  Total Página: R$ ___  |  Total Filtro: R$ ___
```

### 4.3 Ações em Lote

```
[ Marcar como Recebido ] [ Cancelar Selecionados ] [ Gerar Boletos ]
[ Enviar Notificação ] [ Exportar Selecionados ] [ Renegociar ]
```

### 4.4 Drawer — Novo / Editar Título a Receber

```
Drawer lateral direito (largura: 680px)
Título: "Novo Título a Receber" / "Editar Título #CODE"

Seção 1 — Identificação
  [ Código (auto) ]        [ Categoria * ▼ ]
  [ Cliente * 🔍 ]         [ Centro de Custo ▼ ]
  [ Descrição * ]          [ Tags (multi-select) ]

Seção 2 — Valores
  [ Valor Total * ]        [ Desconto (R$ ou %) ]
  [ Juros (% a.m.) ]       [ Multa (%) ]
  [ Valor Líquido (calc) ]

Seção 3 — Datas e Parcelas
  [ Data de Emissão * ]    [ Data de Vencimento * ]
  [ Parcelar? ⬜ ]
    Se sim:
    [ Nº de Parcelas ]     [ Intervalo (dias) ]
    [ 1ª Parcela em ]      [ Preview de parcelas (table) ]

Seção 4 — Pagamento
  [ Método de Pagamento * ▼ ]
  [ Conta Bancária ▼ ]
  [ Código de Barras / PIX (se aplicável) ]
  [ Observações ]
  [ Arquivos Anexos 📎 (drag-and-drop, max 5 arquivos 10MB cada) ]

Seção 5 — Recebimento (colapsável, se status = recebido)
  [ Data de Recebimento ]  [ Valor Recebido ]
  [ Juros Recebidos ]      [ Desconto Concedido ]
  [ Conta Bancária Destino ▼ ]

Footer do Drawer:
  [ Salvar ] [ Salvar e Receber ] [ Cancelar ]
  Histórico de alterações (accordion)
```

### 4.5 Drawer — Baixa / Recebimento

```
Título: "Registrar Recebimento — #CODE"

[ Valor Original: R$ ___ ]
[ Desconto Concedido: R$ ___ ]
[ Juros/Multa: R$ ___ ]
[ Valor a Receber (calc): R$ ___ ]
[ Data do Recebimento * ]
[ Conta Bancária Destino * ▼ ]
[ Método de Pagamento * ▼ ]
[ Comprovante Anexo 📎 ]
[ Observações ]

[ Confirmar Recebimento ] [ Cancelar ]
```

### 4.6 Kanban — Contas a Receber

**Rota:** `GET /financial/receivables/kanban`

```
Colunas:
  [ A Vencer ]  [ Vence Hoje ]  [ Atrasado ]  [ Pago Parcial ]  [ Pago ]  [ Cancelado ]

Card:
  ┌──────────────────────────────┐
  │ #CODE  📅 DD/MM/AAAA        │
  │ Cliente: Nome               │
  │ Valor: R$ 1.250,00          │
  │ Categoria: [badge]          │
  │ [Receber] [Ver] [•••]       │
  └──────────────────────────────┘

Drag-and-drop entre colunas → atualiza status via API
Filtro por período / cliente / categoria
Contador + soma de valor por coluna
```

### 4.7 Página — Inadimplência

**Rota:** `GET /financial/receivables/overdue`

#### Widgets
| Widget               | Dados                             |
|----------------------|-----------------------------------|
| Total em Atraso      | R$ + quantidade de títulos        |
| Atraso 1-30 dias     | R$ + %                            |
| Atraso 31-90 dias    | R$ + %                            |
| Atraso 90+ dias      | R$ + % (provável perda)           |

#### Chart — Evolução da Inadimplência
```
Tipo: amCharts 5 — XYChart (area)
Séries: valor inadimplente por dia (últimos 90 dias)
Benchmark: linha de meta de inadimplência
```

#### Datatable Inadimplência
- Mesmas colunas de Recebíveis + coluna **Dias em Atraso** e **Tentativas de Cobrança**
- Ações extras: [Acionar Régua] [Renegociar] [Enviar WhatsApp] [Protestar]

---

## 5. Contas a Pagar

**Rota:** `GET /financial/payables/list`  
**Componente:** `financial_payables_list.php`

### 5.1 Controles da Página

```
[ + Nova Despesa ]  [ Importar NF-e ▼ ]  [ Exportar ▼ ]  [ Ações em Lote ▼ ]

Filtros:
[ Status ▼ ] [ Categoria ▼ ] [ Fornecedor 🔍 ] [ Vencimento: De___ Até___ ]
[ Centro de Custo ▼ ] [ Aprovação ▼ ] [ Valor: Min___ Max___ ] [ Busca 🔍 ]
```

### 5.2 Datatable — Contas a Pagar

| Coluna          | Tipo         | Ordenável | Observação                           |
|-----------------|--------------|-----------|--------------------------------------|
| ☐               | Checkbox     | —         | Seleção múltipla                     |
| Código          | text         | ✓         |                                      |
| Fornecedor      | text+avatar  | ✓         | Link para cadastro                   |
| Descrição       | text         | ✓         |                                      |
| Categoria       | badge        | ✓         |                                      |
| NF-e / Doc      | text         | ✓         | Ícone de visualização                |
| Emissão         | date         | ✓         |                                      |
| Vencimento      | date+badge   | ✓         | Badge vermelho se vencido            |
| Valor           | currency     | ✓         |                                      |
| Centro de Custo | text         | ✓         |                                      |
| Aprovação       | badge        | ✓         | Pendente / Aprovado / Rejeitado      |
| Status          | badge        | ✓         | Aberto/Parcial/Pago/Cancelado/Atrasado|
| Método Pgto     | icon+text    | ✓         |                                      |
| Pago em         | date         | ✓         |                                      |
| Ações           | buttons      | —         | Ver/Editar/Pagar/Aprovar/Cancelar    |

### 5.3 Drawer — Nova / Editar Despesa

```
Drawer lateral direito (680px)
Título: "Nova Despesa" / "Editar Despesa #CODE"

Seção 1 — Identificação
  [ Código (auto) ]         [ Categoria * ▼ ]
  [ Fornecedor * 🔍 ]       [ Centro de Custo * ▼ ]
  [ Descrição * ]           [ Nº Documento / NF-e ]

Seção 2 — Valores
  [ Valor Bruto * ]         [ Desconto (R$ ou %) ]
  [ Juros/Multa ]           [ Valor Líquido (calc) ]
  [ Rateio por Centro de Custo? ⬜ ]
    Se sim: tabela de rateio (centro de custo + % + R$)

Seção 3 — Datas e Parcelas
  [ Data de Emissão * ]     [ Data de Vencimento * ]
  [ Parcelar? ⬜ ]
    [ Nº de Parcelas ]      [ Intervalo (dias) ]

Seção 4 — Aprovação
  [ Requer Aprovação? ⬜ ]
  [ Aprovador Responsável ▼ ]
  [ Justificativa ]

Seção 5 — Pagamento
  [ Método de Pagamento ▼ ]
  [ Conta Bancária Origem ▼ ]
  [ Chave PIX / Dados Bancários ]
  [ Observações ]
  [ Arquivos Anexos 📎 ]

Footer: [ Salvar ] [ Salvar e Enviar p/ Aprovação ] [ Cancelar ]
```

### 5.4 Drawer — Pagamento de Despesa

```
Título: "Registrar Pagamento — #CODE"

[ Valor Original: R$ ___ ]
[ Desconto Obtido: R$ ___ ]
[ Juros/Multa: R$ ___ ]
[ Valor Pago (calc): R$ ___ ]
[ Data do Pagamento * ]
[ Conta Bancária Origem * ▼ ]
[ Método de Pagamento * ▼ ]
[ Comprovante Anexo 📎 ]
[ Observações ]

[ Confirmar Pagamento ] [ Cancelar ]
```

### 5.5 Kanban — Contas a Pagar

```
Colunas:
[ Pendente ] → [ Aguard. Aprovação ] → [ Aprovado ] → [ Pago ] → [ Vencido ] → [ Cancelado ]

Card:
  ┌──────────────────────────────┐
  │ #CODE  📅 DD/MM/AAAA        │
  │ Fornecedor: Nome            │
  │ Valor: R$ 3.500,00          │
  │ Centro: [badge]             │
  │ Aprov: [badge]              │
  │ [Pagar] [Aprovar] [•••]     │
  └──────────────────────────────┘
```

---

## 6. Fluxo de Caixa

**Rota:** `GET /financial/cash-flow/daily`  
**Componente:** `financial_cashflow.php`

### 6.1 Widgets

| Widget              | Dados                                  |
|---------------------|----------------------------------------|
| Saldo Atual         | Soma de todas as contas bancárias      |
| Entradas Hoje       | R$ recebido no dia                     |
| Saídas Hoje         | R$ pago no dia                         |
| Projeção 30 dias    | Saldo projetado + semáforo             |

### 6.2 Charts

#### Chart 1 — Fluxo Diário (Barras + Linha de Saldo)
```
Tipo: amCharts 5 — XYChart
Série 1 (barras verdes): Entradas por dia
Série 2 (barras vermelhas): Saídas por dia
Série 3 (linha azul): Saldo acumulado
Período: 30 / 60 / 90 dias (toggle)
Drill-down: dia → lista de transações
```

#### Chart 2 — Projeção de Caixa (Area Chart)
```
Tipo: amCharts 5 — XYChart (area)
Linha 1 (sólida): Saldo realizado
Linha 2 (tracejada): Saldo projetado
Zona de risco: área abaixo de zero destacada em vermelho
Projeção: 60 dias futuros
```

### 6.3 Datatable — Lançamentos do Fluxo

| Coluna       | Tipo       | Observação                              |
|--------------|------------|-----------------------------------------|
| Data         | date       | Ordenação padrão DESC                   |
| Tipo         | badge      | Entrada (verde) / Saída (vermelho)      |
| Descrição    | text       |                                         |
| Categoria    | badge      |                                         |
| Origem       | text       | Recebível / Despesa / Transferência     |
| Conta Banc.  | text       |                                         |
| Valor        | currency   | Verde = entrada / Vermelho = saída      |
| Saldo Acum.  | currency   |                                         |
| Status       | badge      | Realizado / Previsto                    |
| Ações        | buttons    | Ver / Estornar / Conciliar              |

### 6.4 Controles

```
[ Período ▼ ] [ Conta Bancária ▼ ] [ Tipo ▼ ] [ Categoria ▼ ]
[ Mostrar Previstos ⬜ ] [ Exportar ▼ ] [ + Lançamento Manual ]
```

### 6.5 Drawer — Lançamento Manual

```
[ Tipo * (Entrada / Saída / Transferência) ]
[ Data * ]                [ Valor * ]
[ Descrição * ]           [ Categoria * ▼ ]
[ Conta Bancária * ▼ ]    [ Centro de Custo ▼ ]
[ Se Transferência: Conta Destino * ▼ ]
[ Observações ]           [ Comprovante 📎 ]
[ Salvar ] [ Cancelar ]
```

---

## 7. Conciliação Bancária

**Rota:** `GET /financial/bank/reconciliation`  
**Componente:** `financial_reconciliation.php`

### 7.1 Widgets

| Widget                  | Dados                           |
|-------------------------|---------------------------------|
| Lançamentos no Sistema  | Qtd + R$ no período             |
| Lançamentos no Extrato  | Qtd + R$ no período             |
| Conciliados             | Qtd + R$ (badge verde)          |
| Pendentes               | Qtd + R$ (badge warning)        |
| Divergências            | Qtd + R$ (badge danger)         |

### 7.2 Chart — Status da Conciliação (Donut)

```
Tipo: amCharts 5 — PieChart (donut)
Segmentos: Conciliado / Pendente / Divergente / Ignorado
Centro: % conciliado total
```

### 7.3 Datatable — Extrato Bancário vs Sistema

Layout em duas colunas paralelas (split view):

```
| EXTRATO BANCÁRIO          | SISTEMA                    | STATUS       |
|---------------------------|----------------------------|--------------|
| Data | Descrição | Valor  | Data | Descrição | Valor     | Match/Pendente|
```

Ações por linha:
- [Conciliar] → abre modal de matching manual
- [Ignorar] → marca como ignorado
- [Criar Lançamento] → cria lançamento no sistema baseado no extrato
- [Ver Detalhes]

### 7.4 Drawer — Importar Extrato OFX

```
[ Banco * ▼ ]             [ Conta Bancária * ▼ ]
[ Período: De___ Até___ ]
[ Arquivo OFX / CSV 📎 (drag-and-drop) ]
[ Preview da importação (datatable 10 linhas) ]
[ Iniciar Conciliação Automática ⬜ ]
[ Importar ] [ Cancelar ]
```

### 7.5 Automação de Conciliação

```
Regras de matching automático:
  - Valor exato + data ± 1 dia → Match automático (confiança: alta)
  - Valor exato + data ± 3 dias → Match sugerido (confiança: média)
  - Valor ± R$ 0,01 (arredondamento) + data ± 1 dia → Match sugerido
  - Sem match → Pendente manual
```

---

## 8. Centros de Custo

**Rota:** `GET /financial/cost-centers`  
**Componente:** `financial_cost_centers.php`

### 8.1 Widgets

| Widget              | Dados                              |
|---------------------|------------------------------------|
| Total de Centros    | Quantidade ativa                   |
| Maior Gasto         | Centro com maior despesa no mês    |
| % do Orçamento      | Execução orçamentária consolidada  |
| Rateios Pendentes   | Qtd de lançamentos sem alocação    |

### 8.2 Chart — Despesa por Centro de Custo

```
Tipo: amCharts 5 — XYChart (bar horizontal)
Dados: R$ gasto por centro no mês atual
Linha de referência: orçamento previsto
Cor: verde se abaixo / laranja se acima do orçado
```

### 8.3 Datatable — Centros de Custo

| Coluna        | Tipo     | Observação                          |
|---------------|----------|-------------------------------------|
| Código        | text     |                                     |
| Nome          | text     |                                     |
| Tipo          | badge    | Resultado / Investimento / Overhead |
| Responsável   | avatar   |                                     |
| Orçado (mês)  | currency |                                     |
| Gasto (mês)   | currency | Vermelho se acima do orçado         |
| % Exec.       | progress |                                     |
| Status        | badge    | Ativo / Inativo                     |
| Ações         | buttons  | Ver / Editar / Desativar            |

### 8.4 Drawer — Novo / Editar Centro de Custo

```
[ Código (auto) ]          [ Nome * ]
[ Tipo * ▼ ]               [ Centro Pai ▼ (hierarquia) ]
[ Responsável * 🔍 ]       [ Descrição ]
[ Orçamento Mensal ]       [ Orçamento Anual ]
[ Alerta em (%): ___ ]     [ Status * ▼ ]
[ Salvar ] [ Cancelar ]
```

---

## 9. Orçamentos

**Rota:** `GET /financial/budgets`  
**Componente:** `financial_budgets.php`

### 9.1 Widgets

| Widget              | Dados                            |
|---------------------|----------------------------------|
| Orçamento Total     | R$ previsto no ano               |
| Realizado           | R$ executado no ano              |
| Saldo Disponível    | R$ restante                      |
| Desvio (%)          | % acima/abaixo do orçado         |

### 9.2 Chart — Orçado vs Realizado por Mês (Barras agrupadas)

```
Tipo: amCharts 5 — XYChart (column grouped)
Série 1 (cinza): Orçado
Série 2 (azul): Realizado
Linha de desvio (vermelho tracejada): % de desvio
Período: ano atual + projeção até dezembro
```

### 9.3 Datatable — Orçamento por Categoria

| Coluna          | Tipo     | Observação                           |
|-----------------|----------|--------------------------------------|
| Categoria       | text     |                                      |
| Centro de Custo | text     |                                      |
| Jan             | currency |                                      |
| Fev             | currency |                                      |
| ...             | currency | (todos os meses)                     |
| Total Orçado    | currency | Negrito                              |
| Total Realizado | currency |                                      |
| Desvio          | badge    | Verde se ok / Vermelho se acima      |
| Ações           | buttons  | Editar / Histórico                   |

> Linha editável inline (click para editar valor orçado).

### 9.4 Drawer — Novo Orçamento

```
[ Ano * ]                   [ Categoria * ▼ ]
[ Centro de Custo * ▼ ]     [ Tipo * (Receita / Despesa) ]
[ Distribuição * (▼ Igual / Manual) ]
  Se igual: [ Valor Total ] → divide por 12
  Se manual: tabela com campo por mês
[ Observações ]
[ Salvar ] [ Cancelar ]
```

---

## 10. Contratos Financeiros

**Rota:** `GET /financial/contracts`  
**Componente:** `financial_contracts.php`

### 10.1 Widgets

| Widget               | Dados                              |
|----------------------|------------------------------------|
| Contratos Ativos     | Qtd + R$ recorrente/mês            |
| Renov. Próx. 30 dias | Qtd a renovar / expirar            |
| Ticket Médio         | R$ médio por contrato              |
| Reajuste Pendente    | Qtd de contratos p/ reajuste       |

### 10.2 Chart — Contratos por Status (Donut)

```
Tipo: amCharts 5 — PieChart (donut)
Segmentos: Ativo / A Renovar / Expirado / Cancelado / Em Negociação
```

### 10.3 Datatable — Contratos

| Coluna           | Tipo     | Observação                             |
|------------------|----------|----------------------------------------|
| Código           | text     |                                        |
| Cliente/Forn.    | text     |                                        |
| Tipo             | badge    | Receita / Despesa                      |
| Modalidade       | badge    | Mensal / Trimestral / Anual            |
| Valor Mensal     | currency |                                        |
| Início           | date     |                                        |
| Término          | date     |                                        |
| Reajuste         | text     | IPCA / IGPM / % fixo                  |
| Status           | badge    |                                        |
| Próx. Cobrança   | date     |                                        |
| Ações            | buttons  | Ver / Editar / Renovar / Cancelar      |

### 10.4 Drawer — Novo / Editar Contrato

```
Seção 1 — Identificação
  [ Código (auto) ]          [ Tipo * ▼ (Receita/Despesa) ]
  [ Cliente / Fornecedor * 🔍 ] [ Modalidade * ▼ ]
  [ Objeto do Contrato * ]   [ Categoria * ▼ ]

Seção 2 — Valores e Vigência
  [ Valor Total do Contrato ] [ Valor da Parcela * ]
  [ Data de Início * ]        [ Data de Término * ]
  [ Dia de Vencimento * ]     [ Tolerância (dias) ]

Seção 3 — Reajuste
  [ Índice de Reajuste ▼ ] (IPCA / IGPM / INPC / % Fixo)
  [ % Fixo (se aplicável) ]
  [ Periodicidade do Reajuste ▼ ] (Anual / Semestral)
  [ Data do Próximo Reajuste ]

Seção 4 — Cobrança
  [ Gerar Parcelas Automaticamente ⬜ ]
  [ Método de Pagamento ▼ ]
  [ Conta Bancária ▼ ]
  [ Régua de Cobrança ▼ ]

Seção 5 — Documentos
  [ Contrato em PDF 📎 ]
  [ Observações ]

Footer: [ Salvar ] [ Salvar e Gerar Parcelas ] [ Cancelar ]
```

### 10.5 Kanban — Contratos

```
Colunas:
[ Em Negociação ] → [ Ativo ] → [ A Renovar ] → [ Expirado ] → [ Cancelado ]

Card:
  ┌──────────────────────────────┐
  │ #CODE  📅 Vence DD/MM/AAAA  │
  │ Cliente/Forn.: Nome         │
  │ Valor: R$ 1.500,00/mês      │
  │ [Renovar] [Ver] [•••]       │
  └──────────────────────────────┘
```

---

## 11. Cobranças e Inadimplência

**Rota:** `GET /financial/charges`  
**Componente:** `financial_charges.php`

### 11.1 Régua de Cobrança

```
Linha do tempo visual (timeline horizontal):

  D-10     D-5      D0        D+3      D+7      D+15     D+30
  |         |        |         |         |         |        |
[Email]  [Email]  [Venc.]  [Email]   [WhatsApp] [SMS]  [Protestar]
                            [Push]
```

### 11.2 Widgets Cobrança

| Widget                  | Dados                         |
|-------------------------|-------------------------------|
| Em Cobrança Ativa       | Qtd de títulos na régua       |
| Enviados Hoje           | Qtd de notificações           |
| Taxa de Retorno         | % que pagaram após notificação|
| Protestados             | Qtd + R$                      |

### 11.3 Datatable — Histórico de Cobranças

| Coluna           | Tipo     | Observação                          |
|------------------|----------|-------------------------------------|
| Título           | text     | Link para o recebível               |
| Cliente          | text     |                                     |
| Valor            | currency |                                     |
| Dias em Atraso   | number   | Badge colorido por faixa            |
| Última Ação      | text     |                                     |
| Próx. Ação       | date     |                                     |
| Canal            | badge    | Email/SMS/WhatsApp/Push             |
| Status           | badge    | Ativo / Pausado / Quitado           |
| Ações            | buttons  | Pausar / Forçar Ação / Histórico    |

### 11.4 Drawer — Régua de Cobrança (Configuração)

```
[ Nome da Régua * ]         [ Descrição ]
[ Ativa ⬜ ]                 [ Padrão ⬜ ]

Ações da Régua (lista editável, drag-and-drop):
  + Adicionar Ação
  ┌─────────────────────────────────────────────────────┐
  │ Momento: [ D-10 ▼ ]   Canal: [ Email ▼ ]           │
  │ Template: [ ▼ ]        Ativo: [ ⬜ ]                │
  │ [ ✏ Editar Template ] [ 🗑 Remover ]               │
  └─────────────────────────────────────────────────────┘

[ Salvar ] [ Cancelar ]
```

---

## 12. Relatórios Financeiros

### 12.1 DRE — Demonstrativo de Resultado

**Rota:** `GET /financial/reports/dre`

#### Controles
```
[ Período: De___ Até___ ] [ Unidade ▼ ] [ Centro de Custo ▼ ]
[ Comparar com período anterior ⬜ ] [ Exportar: PDF / Excel / CSV ▼ ]
```

#### Estrutura do DRE

```
RECEITA BRUTA
  (+) Receitas de Serviços
  (+) Receitas de Produtos
  (-) Deduções e Cancelamentos
= RECEITA LÍQUIDA
  (-) Custos dos Serviços/Produtos (CMV/CSV)
= LUCRO BRUTO
  (-) Despesas Operacionais
      Despesas Administrativas
      Despesas Comerciais
      Despesas Financeiras
      Outras Despesas
  (+) Receitas Financeiras
  (+) Outras Receitas
= EBITDA
  (-) Depreciação / Amortização
= EBIT
  (-) Resultado Financeiro Líquido
= LAIR (Lucro antes do IR)
  (-) IRPJ / CSLL (estimado)
= LUCRO LÍQUIDO
```

#### Chart DRE — Waterfall

```
Tipo: amCharts 5 — XYChart (waterfall)
Barras positivas: verde / negativas: vermelho / totais: azul
Comparativo: mesmo período ano anterior (linhas pontilhadas)
```

### 12.2 Relatório de Fluxo de Caixa

**Rota:** `GET /financial/reports/cash-flow-report`

```
Estrutura tabular com:
  - Saldo inicial do período
  - (+) Entradas por categoria
  - (-) Saídas por categoria
  - Saldo final do período
  - Projeção próximos 30/60/90 dias
```

### 12.3 Relatório de Inadimplência

**Rota:** `GET /financial/reports/overdue`

```
Filtros: período / faixa de atraso / cliente / categoria
Exportação: PDF / Excel
Agrupamento: por cliente / por categoria / por faixa
```

---

## 13. Automações

**Rota:** `GET /financial/settings/automations`

### 13.1 Lista de Automações Disponíveis

| ID  | Nome                              | Gatilho                        | Ação                              | Status   |
|-----|-----------------------------------|--------------------------------|-----------------------------------|----------|
| A01 | Geração de Parcelas de Contrato   | Contrato ativado               | Gerar parcelas no recebível       | ativo    |
| A02 | Envio de Boleto por Email         | Parcela gerada                 | Email com boleto PDF              | ativo    |
| A03 | Lembrete de Vencimento D-3        | 3 dias antes do vencimento     | Email + Push para cliente         | ativo    |
| A04 | Notificação de Atraso D+1         | 1 dia após vencimento          | Email + SMS                       | ativo    |
| A05 | Aplicação de Juros/Multa          | Vencimento ultrapassado        | Atualiza valor do título          | ativo    |
| A06 | Alerta de Saldo Mínimo            | Saldo < limite configurado     | Push + Email para financeiro      | ativo    |
| A07 | Conciliação Automática            | Importação de extrato OFX      | Matching automático por valor/data| ativo    |
| A08 | Reajuste de Contrato              | Data de reajuste atingida      | Atualiza valor + notifica cliente | ativo    |
| A09 | Aprovação por Alçada              | Despesa acima do limite        | Notifica aprovador responsável    | ativo    |
| A10 | Renovação de Contrato             | 30 dias antes do término       | Notifica gestor + cria tarefa     | ativo    |
| A11 | Protestar Título                  | Atraso > X dias (configurável) | Envia para cartório (integração)  | inativo  |
| A12 | Relatório Financeiro Diário       | Todo dia às 08h                | Email com resumo para gestores    | ativo    |
| A13 | Backup de Dados Financeiros       | Semanalmente (domingo 02h)     | Exporta e armazena backup         | ativo    |

### 13.2 Drawer — Configurar Automação

```
[ Nome * ]                    [ Descrição ]
[ Ativo ⬜ ]

Seção — Gatilho
  [ Tipo de Gatilho * ▼ ]
  (Parâmetros dinâmicos conforme tipo)
  Ex. Atraso: [ Dias após vencimento: ___ ]
  Ex. Saldo: [ Conta ▼ ] [ Limite R$: ___ ]
  Ex. Agendado: [ Recorrência ▼ ] [ Horário ]

Seção — Condições (opcionais)
  + Adicionar Condição
  [ Campo ▼ ] [ Operador ▼ ] [ Valor ]

Seção — Ações
  + Adicionar Ação
  [ Tipo ▼ ] (Email / SMS / Push / Webhook / Função interna)
  [ Template ▼ / Configuração da ação ]

Seção — Log
  Últimas 10 execuções (datatable compacto)

[ Salvar ] [ Testar Agora ] [ Cancelar ]
```

---

## 14. Gerenciamentos

### 14.1 Gerenciamento de Categorias Financeiras

**Rota:** `GET /financial/settings/categories`

#### Datatable

| Coluna      | Tipo   | Observação                         |
|-------------|--------|------------------------------------|
| Código      | text   |                                    |
| Nome        | text   |                                    |
| Tipo        | badge  | Receita / Despesa / Neutro         |
| Categoria Pai | text | Hierarquia (1 nível)               |
| DRE         | badge  | Linha do DRE relacionada           |
| Status      | badge  | Ativo / Inativo                    |
| Ações       | buttons| Editar / Desativar                 |

#### Drawer — Categoria

```
[ Código (auto) ]       [ Nome * ]
[ Tipo * ▼ ]            [ Categoria Pai ▼ ]
[ Linha DRE * ▼ ]       [ Cor (color picker) ]
[ Ícone ▼ ]             [ Status ▼ ]
[ Salvar ] [ Cancelar ]
```

### 14.2 Gerenciamento de Contas Bancárias

**Rota:** `GET /financial/bank/accounts`

#### Datatable

| Coluna         | Tipo     | Observação                     |
|----------------|----------|--------------------------------|
| Banco          | logo+text|                                |
| Agência        | text     |                                |
| Conta          | text     |                                |
| Tipo           | badge    | Corrente / Poupança / Caixa    |
| Saldo Atual    | currency |                                |
| Saldo Mínimo   | currency |                                |
| Status         | badge    |                                |
| Ações          | buttons  | Editar / Extrato / Transferir  |

#### Drawer — Conta Bancária

```
[ Banco * ▼ ]           [ Tipo * ▼ ]
[ Agência * ]           [ Conta * ]
[ Dígito ]              [ Nome de Identificação * ]
[ Saldo Inicial ]       [ Data do Saldo Inicial ]
[ Saldo Mínimo ]        [ Alerta Saldo Mínimo ⬜ ]
[ PIX habilitado ⬜ ]   [ Chave PIX ]
[ Status ▼ ]
[ Salvar ] [ Cancelar ]
```

### 14.3 Gerenciamento de Métodos de Pagamento

**Rota:** `GET /financial/settings/payment-methods`

```
Datatable + Drawer:
Campos: Nome / Tipo (Dinheiro/Boleto/PIX/Cartão/TED/DOC/Cheque) /
        Taxa (%) / Prazo de Liquidação (dias) / Ativo
```

### 14.4 Gerenciamento de Integrações

**Rota:** `GET /financial/settings/integrations`

| Integração        | Tipo         | Status     | Ações                   |
|-------------------|--------------|------------|-------------------------|
| Asaas             | Gateway Pgto | Ativo      | Configurar / Testar     |
| PagSeguro         | Gateway Pgto | Inativo    | Ativar                  |
| Efí Bank (Gerencianet) | Boleto  | Ativo      | Configurar / Testar     |
| Febraban OFX      | Extrato      | Ativo      | Configurar              |
| Contabilidade     | Exportação   | Configurar | Configurar              |
| SPED Contábil     | Fiscal       | Inativo    | Ativar                  |

---

## 15. Controles Globais

### 15.1 Barra de Navegação do Módulo

```
[ Dashboard ] [ A Receber ] [ A Pagar ] [ Fluxo de Caixa ]
[ Bancário ▼ ] [ Orçamentos ] [ Contratos ] [ Cobranças ]
[ Relatórios ▼ ] [ Configurações ▼ ]
```

### 15.2 Filtros Globais (Persistentes por sessão)

```
[ 🏢 Entidade ▼ ] [ 🏭 Unidade ▼ ] [ 📅 Período ▼ ] [ 💰 Moeda ▼ ]
```

### 15.3 Atalhos de Teclado

| Atalho       | Ação                        |
|--------------|-----------------------------|
| `N`          | Novo título/despesa         |
| `F`          | Foco na busca               |
| `Esc`        | Fechar drawer/modal         |
| `Ctrl+S`     | Salvar formulário ativo     |
| `Ctrl+E`     | Exportar datatable          |

### 15.4 Auditoria e Log

- Todo CRUD gera registro em `audit_logs` (uuid, user, action, entity, before, after, ip, timestamp)
- Exclusão lógica: campo `deleted_at` + `deleted_by`
- Rastreabilidade: cada transação financeira mantém `origin_type` e `origin_id`

### 15.5 Permissões de Interface

```
Elementos que respeitam permissões RBAC:
  - Botões de ação (ocultos se sem permissão)
  - Colunas sensíveis (valor, saldo) → ocultadas por perfil
  - Campos de aprovação → visíveis apenas para aprovadores
  - Exportação → permissão específica
  - Configurações → somente admin financeiro
```

---

## 16. Esquema SQL Base

```sql
-- ================================================
-- Tabela: financial_categories
-- ================================================
CREATE TABLE financial_categories (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid        CHAR(36)        NOT NULL UNIQUE,
    code        VARCHAR(30)     NOT NULL UNIQUE,
    name        VARCHAR(100)    NOT NULL,
    type        ENUM('revenue','expense','neutral') NOT NULL,
    parent_id   BIGINT UNSIGNED DEFAULT NULL,
    dre_line    VARCHAR(100)    DEFAULT NULL,
    color       VARCHAR(7)      DEFAULT NULL,
    icon        VARCHAR(50)     DEFAULT NULL,
    is_active   TINYINT(1)      DEFAULT 1,
    created_at  DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME        ON UPDATE CURRENT_TIMESTAMP,
    deleted_at  DATETIME        DEFAULT NULL,
    CONSTRAINT fk_fc_parent FOREIGN KEY (parent_id) REFERENCES financial_categories(id)
) ENGINE=InnoDB;

-- ================================================
-- Tabela: financial_bank_accounts
-- ================================================
CREATE TABLE financial_bank_accounts (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36)        NOT NULL UNIQUE,
    code            VARCHAR(30)     NOT NULL UNIQUE,
    name            VARCHAR(100)    NOT NULL,
    bank_name       VARCHAR(100)    DEFAULT NULL,
    bank_code       VARCHAR(10)     DEFAULT NULL,
    agency          VARCHAR(20)     DEFAULT NULL,
    account_number  VARCHAR(30)     DEFAULT NULL,
    account_digit   VARCHAR(5)      DEFAULT NULL,
    type            ENUM('checking','savings','cash','investment') NOT NULL,
    balance         DECIMAL(15,2)   DEFAULT 0.00,
    min_balance     DECIMAL(15,2)   DEFAULT 0.00,
    pix_key         VARCHAR(100)    DEFAULT NULL,
    is_active       TINYINT(1)      DEFAULT 1,
    created_at      DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        ON UPDATE CURRENT_TIMESTAMP,
    deleted_at      DATETIME        DEFAULT NULL
) ENGINE=InnoDB;

-- ================================================
-- Tabela: financial_cost_centers
-- ================================================
CREATE TABLE financial_cost_centers (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36)        NOT NULL UNIQUE,
    code            VARCHAR(30)     NOT NULL UNIQUE,
    name            VARCHAR(100)    NOT NULL,
    type            ENUM('result','investment','overhead') NOT NULL,
    parent_id       BIGINT UNSIGNED DEFAULT NULL,
    responsible_id  BIGINT UNSIGNED DEFAULT NULL,
    budget_monthly  DECIMAL(15,2)   DEFAULT 0.00,
    budget_yearly   DECIMAL(15,2)   DEFAULT 0.00,
    alert_threshold TINYINT UNSIGNED DEFAULT 80,
    is_active       TINYINT(1)      DEFAULT 1,
    created_at      DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        ON UPDATE CURRENT_TIMESTAMP,
    deleted_at      DATETIME        DEFAULT NULL
) ENGINE=InnoDB;

-- ================================================
-- Tabela: financial_receivables
-- ================================================
CREATE TABLE financial_receivables (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid                CHAR(36)        NOT NULL UNIQUE,
    code                VARCHAR(30)     NOT NULL UNIQUE,
    customer_id         BIGINT UNSIGNED NOT NULL,
    category_id         BIGINT UNSIGNED NOT NULL,
    cost_center_id      BIGINT UNSIGNED DEFAULT NULL,
    description         VARCHAR(255)    NOT NULL,
    gross_amount        DECIMAL(15,2)   NOT NULL,
    discount_amount     DECIMAL(15,2)   DEFAULT 0.00,
    interest_rate       DECIMAL(5,4)    DEFAULT 0.0000,
    fine_rate           DECIMAL(5,4)    DEFAULT 0.0000,
    net_amount          DECIMAL(15,2)   NOT NULL,
    issue_date          DATE            NOT NULL,
    due_date            DATE            NOT NULL,
    payment_date        DATE            DEFAULT NULL,
    amount_paid         DECIMAL(15,2)   DEFAULT NULL,
    installment_number  SMALLINT        DEFAULT 1,
    total_installments  SMALLINT        DEFAULT 1,
    parent_id           BIGINT UNSIGNED DEFAULT NULL,
    payment_method_id   BIGINT UNSIGNED DEFAULT NULL,
    bank_account_id     BIGINT UNSIGNED DEFAULT NULL,
    status              ENUM('open','partial','paid','cancelled','overdue') DEFAULT 'open',
    notes               TEXT            DEFAULT NULL,
    created_by          BIGINT UNSIGNED NOT NULL,
    created_at          DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME        ON UPDATE CURRENT_TIMESTAMP,
    deleted_at          DATETIME        DEFAULT NULL,
    deleted_by          BIGINT UNSIGNED DEFAULT NULL,
    INDEX idx_due_date (due_date),
    INDEX idx_status (status),
    INDEX idx_customer (customer_id)
) ENGINE=InnoDB;

-- ================================================
-- Tabela: financial_payables
-- ================================================
CREATE TABLE financial_payables (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid                CHAR(36)        NOT NULL UNIQUE,
    code                VARCHAR(30)     NOT NULL UNIQUE,
    supplier_id         BIGINT UNSIGNED NOT NULL,
    category_id         BIGINT UNSIGNED NOT NULL,
    cost_center_id      BIGINT UNSIGNED DEFAULT NULL,
    description         VARCHAR(255)    NOT NULL,
    document_number     VARCHAR(60)     DEFAULT NULL,
    gross_amount        DECIMAL(15,2)   NOT NULL,
    discount_amount     DECIMAL(15,2)   DEFAULT 0.00,
    interest_amount     DECIMAL(15,2)   DEFAULT 0.00,
    net_amount          DECIMAL(15,2)   NOT NULL,
    issue_date          DATE            NOT NULL,
    due_date            DATE            NOT NULL,
    payment_date        DATE            DEFAULT NULL,
    amount_paid         DECIMAL(15,2)   DEFAULT NULL,
    installment_number  SMALLINT        DEFAULT 1,
    total_installments  SMALLINT        DEFAULT 1,
    parent_id           BIGINT UNSIGNED DEFAULT NULL,
    payment_method_id   BIGINT UNSIGNED DEFAULT NULL,
    bank_account_id     BIGINT UNSIGNED DEFAULT NULL,
    approval_status     ENUM('not_required','pending','approved','rejected') DEFAULT 'not_required',
    approver_id         BIGINT UNSIGNED DEFAULT NULL,
    approved_at         DATETIME        DEFAULT NULL,
    status              ENUM('open','partial','paid','cancelled','overdue') DEFAULT 'open',
    notes               TEXT            DEFAULT NULL,
    created_by          BIGINT UNSIGNED NOT NULL,
    created_at          DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME        ON UPDATE CURRENT_TIMESTAMP,
    deleted_at          DATETIME        DEFAULT NULL,
    deleted_by          BIGINT UNSIGNED DEFAULT NULL,
    INDEX idx_due_date (due_date),
    INDEX idx_status (status),
    INDEX idx_supplier (supplier_id)
) ENGINE=InnoDB;

-- ================================================
-- Tabela: financial_transactions
-- ================================================
CREATE TABLE financial_transactions (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36)        NOT NULL UNIQUE,
    code            VARCHAR(30)     NOT NULL UNIQUE,
    type            ENUM('credit','debit','transfer') NOT NULL,
    origin_type     VARCHAR(50)     NOT NULL,
    origin_id       BIGINT UNSIGNED NOT NULL,
    bank_account_id BIGINT UNSIGNED NOT NULL,
    dest_account_id BIGINT UNSIGNED DEFAULT NULL,
    category_id     BIGINT UNSIGNED DEFAULT NULL,
    cost_center_id  BIGINT UNSIGNED DEFAULT NULL,
    description     VARCHAR(255)    NOT NULL,
    amount          DECIMAL(15,2)   NOT NULL,
    transaction_date DATE           NOT NULL,
    balance_after   DECIMAL(15,2)   DEFAULT NULL,
    reconciled      TINYINT(1)      DEFAULT 0,
    reconciled_at   DATETIME        DEFAULT NULL,
    notes           TEXT            DEFAULT NULL,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME        DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_transaction_date (transaction_date),
    INDEX idx_bank_account (bank_account_id),
    INDEX idx_reconciled (reconciled)
) ENGINE=InnoDB;

-- ================================================
-- Tabela: financial_contracts
-- ================================================
CREATE TABLE financial_contracts (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid                CHAR(36)        NOT NULL UNIQUE,
    code                VARCHAR(30)     NOT NULL UNIQUE,
    type                ENUM('revenue','expense') NOT NULL,
    party_id            BIGINT UNSIGNED NOT NULL,
    party_type          VARCHAR(50)     NOT NULL,
    description         TEXT            NOT NULL,
    category_id         BIGINT UNSIGNED DEFAULT NULL,
    modality            ENUM('monthly','quarterly','semiannual','annual') NOT NULL,
    installment_amount  DECIMAL(15,2)   NOT NULL,
    total_amount        DECIMAL(15,2)   DEFAULT NULL,
    start_date          DATE            NOT NULL,
    end_date            DATE            DEFAULT NULL,
    due_day             TINYINT UNSIGNED NOT NULL,
    tolerance_days      TINYINT UNSIGNED DEFAULT 0,
    adjustment_index    ENUM('IPCA','IGPM','INPC','fixed','none') DEFAULT 'none',
    adjustment_rate     DECIMAL(6,4)    DEFAULT 0.0000,
    next_adjustment_date DATE           DEFAULT NULL,
    payment_method_id   BIGINT UNSIGNED DEFAULT NULL,
    charge_rule_id      BIGINT UNSIGNED DEFAULT NULL,
    auto_generate       TINYINT(1)      DEFAULT 1,
    status              ENUM('negotiating','active','to_renew','expired','cancelled') DEFAULT 'active',
    notes               TEXT            DEFAULT NULL,
    created_by          BIGINT UNSIGNED NOT NULL,
    created_at          DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME        ON UPDATE CURRENT_TIMESTAMP,
    deleted_at          DATETIME        DEFAULT NULL
) ENGINE=InnoDB;

-- ================================================
-- Tabela: financial_budgets
-- ================================================
CREATE TABLE financial_budgets (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36)        NOT NULL UNIQUE,
    code            VARCHAR(30)     NOT NULL UNIQUE,
    year            YEAR            NOT NULL,
    category_id     BIGINT UNSIGNED NOT NULL,
    cost_center_id  BIGINT UNSIGNED DEFAULT NULL,
    type            ENUM('revenue','expense') NOT NULL,
    jan             DECIMAL(15,2)   DEFAULT 0.00,
    feb             DECIMAL(15,2)   DEFAULT 0.00,
    mar             DECIMAL(15,2)   DEFAULT 0.00,
    apr             DECIMAL(15,2)   DEFAULT 0.00,
    may             DECIMAL(15,2)   DEFAULT 0.00,
    jun             DECIMAL(15,2)   DEFAULT 0.00,
    jul             DECIMAL(15,2)   DEFAULT 0.00,
    aug             DECIMAL(15,2)   DEFAULT 0.00,
    sep             DECIMAL(15,2)   DEFAULT 0.00,
    oct             DECIMAL(15,2)   DEFAULT 0.00,
    nov             DECIMAL(15,2)   DEFAULT 0.00,
    dec_month       DECIMAL(15,2)   DEFAULT 0.00,
    total_budgeted  DECIMAL(15,2)   GENERATED ALWAYS AS (
        jan+feb+mar+apr+may+jun+jul+aug+sep+oct+nov+dec_month
    ) STORED,
    notes           TEXT            DEFAULT NULL,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ================================================
-- Tabela: financial_charge_rules
-- ================================================
CREATE TABLE financial_charge_rules (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid        CHAR(36)        NOT NULL UNIQUE,
    code        VARCHAR(30)     NOT NULL UNIQUE,
    name        VARCHAR(100)    NOT NULL,
    description TEXT            DEFAULT NULL,
    is_default  TINYINT(1)      DEFAULT 0,
    is_active   TINYINT(1)      DEFAULT 1,
    created_by  BIGINT UNSIGNED NOT NULL,
    created_at  DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME        ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ================================================
-- Tabela: financial_charge_actions
-- ================================================
CREATE TABLE financial_charge_actions (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36)        NOT NULL UNIQUE,
    rule_id         BIGINT UNSIGNED NOT NULL,
    trigger_days    SMALLINT        NOT NULL,
    channel         ENUM('email','sms','whatsapp','push','internal') NOT NULL,
    template_id     BIGINT UNSIGNED DEFAULT NULL,
    is_active       TINYINT(1)      DEFAULT 1,
    sort_order      SMALLINT        DEFAULT 0,
    created_at      DATETIME        DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fca_rule FOREIGN KEY (rule_id) REFERENCES financial_charge_rules(id)
) ENGINE=InnoDB;

-- ================================================
-- Tabela: financial_bank_statements
-- ================================================
CREATE TABLE financial_bank_statements (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36)        NOT NULL UNIQUE,
    bank_account_id BIGINT UNSIGNED NOT NULL,
    transaction_date DATE           NOT NULL,
    description     VARCHAR(255)    NOT NULL,
    amount          DECIMAL(15,2)   NOT NULL,
    balance         DECIMAL(15,2)   DEFAULT NULL,
    ofx_id          VARCHAR(100)    DEFAULT NULL,
    transaction_id  BIGINT UNSIGNED DEFAULT NULL,
    status          ENUM('pending','matched','ignored','manual') DEFAULT 'pending',
    imported_at     DATETIME        DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_bank_account (bank_account_id)
) ENGINE=InnoDB;
```

---

## 17. Rotas da API REST

```
GET    /api/v1/financial/dashboard              → Dados do dashboard
GET    /api/v1/financial/receivables            → Listar (paginado, filtros)
POST   /api/v1/financial/receivables            → Criar
GET    /api/v1/financial/receivables/{uuid}     → Detalhar
PUT    /api/v1/financial/receivables/{uuid}     → Atualizar
DELETE /api/v1/financial/receivables/{uuid}     → Excluir (soft)
POST   /api/v1/financial/receivables/{uuid}/pay → Registrar recebimento
GET    /api/v1/financial/payables               → Listar
POST   /api/v1/financial/payables               → Criar
GET    /api/v1/financial/payables/{uuid}        → Detalhar
PUT    /api/v1/financial/payables/{uuid}        → Atualizar
DELETE /api/v1/financial/payables/{uuid}        → Excluir (soft)
POST   /api/v1/financial/payables/{uuid}/pay    → Registrar pagamento
POST   /api/v1/financial/payables/{uuid}/approve → Aprovar
POST   /api/v1/financial/payables/{uuid}/reject  → Rejeitar
GET    /api/v1/financial/cash-flow              → Fluxo de caixa
GET    /api/v1/financial/cash-flow/projected    → Projeção
GET    /api/v1/financial/bank-accounts          → Contas bancárias
POST   /api/v1/financial/bank-accounts          → Criar
PUT    /api/v1/financial/bank-accounts/{uuid}   → Atualizar
POST   /api/v1/financial/bank-statements/import → Importar OFX
GET    /api/v1/financial/reconciliation         → Pendências
POST   /api/v1/financial/reconciliation/match   → Conciliar manual
POST   /api/v1/financial/reconciliation/auto    → Conciliar automático
GET    /api/v1/financial/cost-centers           → Listar
POST   /api/v1/financial/cost-centers           → Criar
PUT    /api/v1/financial/cost-centers/{uuid}    → Atualizar
GET    /api/v1/financial/budgets                → Listar
POST   /api/v1/financial/budgets                → Criar
PUT    /api/v1/financial/budgets/{uuid}         → Atualizar
GET    /api/v1/financial/contracts              → Listar
POST   /api/v1/financial/contracts              → Criar
PUT    /api/v1/financial/contracts/{uuid}       → Atualizar
POST   /api/v1/financial/contracts/{uuid}/renew → Renovar
GET    /api/v1/financial/charge-rules           → Listar réguas
POST   /api/v1/financial/charge-rules           → Criar
PUT    /api/v1/financial/charge-rules/{uuid}    → Atualizar
GET    /api/v1/financial/reports/dre            → DRE (parâmetros: period, unit)
GET    /api/v1/financial/reports/cash-flow      → Relatório fluxo
GET    /api/v1/financial/reports/overdue        → Relatório inadimplência
GET    /api/v1/financial/categories             → Categorias
POST   /api/v1/financial/categories             → Criar
PUT    /api/v1/financial/categories/{uuid}      → Atualizar
GET    /api/v1/financial/payment-methods        → Métodos de pagamento
POST   /api/v1/financial/automations/trigger    → Disparar automação manual
GET    /api/v1/financial/automations/logs       → Log de automações
```

Padrão de resposta:
```json
{
    "success": true,
    "data": { ... },
    "meta": {
        "pagination": { "page": 1, "per_page": 25, "total": 340 },
        "filters_applied": { ... }
    },
    "message": null
}
```

---

## 18. Permissões por Perfil

| Permissão                       | Admin | Financeiro | Gerente | Operador | Auditor |
|---------------------------------|-------|------------|---------|----------|---------|
| Ver Dashboard                   | ✓     | ✓          | ✓       | ✓        | ✓       |
| Ver Contas a Receber            | ✓     | ✓          | ✓       | ✓        | ✓       |
| Criar/Editar Recebíveis         | ✓     | ✓          | ✓       | ✓        | —       |
| Baixar Recebível                | ✓     | ✓          | ✓       | —        | —       |
| Ver Contas a Pagar              | ✓     | ✓          | ✓       | ✓        | ✓       |
| Criar/Editar Despesas           | ✓     | ✓          | ✓       | ✓        | —       |
| Pagar Despesa                   | ✓     | ✓          | —       | —        | —       |
| Aprovar Despesa                 | ✓     | ✓          | ✓       | —        | —       |
| Ver Fluxo de Caixa              | ✓     | ✓          | ✓       | —        | ✓       |
| Gerenciar Contas Bancárias      | ✓     | ✓          | —       | —        | —       |
| Conciliação Bancária            | ✓     | ✓          | —       | —        | ✓       |
| Gerenciar Centros de Custo      | ✓     | ✓          | ✓       | —        | —       |
| Gerenciar Orçamentos            | ✓     | ✓          | ✓       | —        | —       |
| Gerenciar Contratos             | ✓     | ✓          | ✓       | —        | ✓       |
| Configurar Régua de Cobrança    | ✓     | ✓          | —       | —        | —       |
| Ver Relatórios                  | ✓     | ✓          | ✓       | —        | ✓       |
| Exportar Dados                  | ✓     | ✓          | ✓       | —        | ✓       |
| Configurar Automações           | ✓     | ✓          | —       | —        | —       |
| Configurar Integrações          | ✓     | —          | —       | —        | —       |
| Excluir Registros               | ✓     | —          | —       | —        | —       |
| Ver Auditoria                   | ✓     | —          | —       | —        | ✓       |

---

## 19. Checklist de Entrega

### Frontend
- [ ] Dashboard com widgets, 5 charts e kanban de aprovações
- [ ] Página de Contas a Receber: datatable + kanban + página de inadimplência
- [ ] Página de Contas a Pagar: datatable + kanban
- [ ] Página de Fluxo de Caixa: diário + projetado
- [ ] Página Conciliação Bancária: split view + import OFX
- [ ] Página de Centros de Custo: datatable + chart
- [ ] Página de Orçamentos: datatable editável + chart
- [ ] Página de Contratos: datatable + kanban
- [ ] Página de Cobranças: régua visual + datatable
- [ ] Relatórios: DRE (waterfall chart) + Fluxo + Inadimplência
- [ ] Todos os drawers de CRUD implementados
- [ ] Drawer de baixa de recebível
- [ ] Drawer de pagamento de despesa
- [ ] Filtros persistentes por sessão
- [ ] Ações em lote nos datatables
- [ ] Exportação PDF/Excel/CSV em todas as páginas
- [ ] Controles RBAC por perfil (ocultar botões/colunas)
- [ ] Atalhos de teclado

### Backend
- [ ] Migrations para todas as tabelas
- [ ] Seeders para categorias e métodos de pagamento padrão
- [ ] Controllers REST para todos os endpoints
- [ ] Lógica de cálculo de juros/multa automático
- [ ] Processamento de parcelas
- [ ] Motor de automações (cron + regras)
- [ ] Parser OFX para importação de extrato
- [ ] Algoritmo de conciliação automática
- [ ] Engine de geração de DRE
- [ ] Geração de relatórios PDF (mPDF ou TCPDF)
- [ ] Job de geração automática de parcelas de contratos
- [ ] Log de auditoria em todos os endpoints
- [ ] Cobertura de permissões RBAC na API

### Integrações
- [ ] Gateway de boleto (Efí Bank ou Asaas)
- [ ] Gateway de PIX
- [ ] Importação OFX Febraban
- [ ] Envio de email (SMTP configurável)
- [ ] Envio de SMS (provider configurável)
- [ ] WhatsApp Business API (opcional)

---

*Documento gerado em: 2026-06-06 | TotusTuusSoftCloud | Módulo Financeiro v1.0.0*
