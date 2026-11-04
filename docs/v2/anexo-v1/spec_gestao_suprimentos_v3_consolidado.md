# SPEC — Módulo Suprimentos
**Versão:** 3.0 — Consolidado
**Status:** Completo
**Módulo:** Suprimentos / Procurement / Purchasing / Receiving / Replenishment
**Sistema:** TotusTuusSoftCloud
- Language Standard: Global English
**Idioma técnico:** inglês | **Idioma documental:** pt-BR
**Arquitetura:** SaaS multi-entidade, multi-unidade e multi-usuário, banco segregado por entidade/unidade, padrão `id` + `uuid` + `code`
**Stack:** PHP 8 puro · Tailwind CSS 4.2 · Supabase · JavaScript fetch · amCharts 5

---

# 1. Visão Geral

O módulo de Suprimentos controla o ciclo completo de abastecimento institucional e corporativo, cobrindo:

- Solicitação interna, aprovação, cotação, negociação, emissão de pedido, contrato, entrega, recebimento, inspeção, entrada em estoque, devolução, reposição, análise de consumo, avaliação de fornecedor, compliance e auditoria.

Atende cenários de compras centralizadas, descentralizadas por unidade, emergenciais, sob contrato, de estoque, de serviço, de ativo e recorrentes.

**Integrações obrigatórias:**
- Financeiro · Estoque · Patrimônio · Fiscal · Auditoria · Notificações · IAM/RBAC · Documentos/Anexos

---

# 2. Objetivos

## 2.1 Operacionais
- Padronizar o processo de compras.
- Reduzir compras fora de política.
- Evitar ruptura de estoque.
- Melhorar lead time de abastecimento.
- Formalizar aprovações.
- Registrar histórico completo do processo.
- Reduzir retrabalho entre solicitante, comprador e recebimento.
- Controlar divergências físicas e documentais.

## 2.2 Gerenciais
- Medir gasto por unidade, categoria, fornecedor e centro de custo.
- Identificar fornecedores críticos.
- Medir economia em cotações.
- Medir SLA do processo.
- Medir atrasos de entrega.
- Medir conformidade contratual.
- Medir consumo e cobertura de estoque.
- Identificar compras emergenciais e desvios de orçamento.

## 2.3 Controle
- Garantir segregação de função.
- Garantir alçada de aprovação.
- Impedir emissão de pedido sem política aprovada, quando aplicável.
- Garantir rastreabilidade ponta a ponta.
- Registrar trilha de auditoria imutável.
- Aplicar bloqueios automáticos para fornecedores e operações não conformes.

---

# 3. Escopo

## 3.1 Dentro do escopo
Dashboard executivo e operacional · Requisições internas · Requisições automáticas por estoque mínimo · Aprovações multinível · Cotações e mapa comparativo · Seleção e adjudicação de fornecedor · Pedidos de compra · Contratos e atas de fornecimento · Agenda de entregas · Recebimento físico · Conferência quantitativa e qualitativa · Inspeção · Divergências · Devoluções ao fornecedor · Entrada em estoque · Reposição e ressuprimento · Avaliação de fornecedor · Ranking de fornecedores · Controle de SLA · Relatórios e exportações · Automações, filas e jobs · Parametrizações · Controles e compliance.

## 3.2 Fora do escopo primário
MRP industrial avançado · Planejamento de produção · WMS de endereçamento caótico completo · Escrituração fiscal avançada · AP/contas a pagar completo · Transporte e roteirização logística.

---

# 4. Arquitetura

## 4.1 Multi-tenant
- Cada entidade/unidade possui base transacional própria.
- Isolamento obrigatório por `entity_uuid` e `unit_uuid` em todas as queries.
- `uuid` → referência interna segura.
- `code` → exibição e referência externa.
- `id` → ordenação técnica, paginação e joins locais.

## 4.2 Padrão de implementação
- Backend PHP 8 puro.
- Frontend Tailwind CSS 4.2 + Supabase.
- JavaScript com `fetch`.
- Charts com amCharts 5.
- Listagens com paginação server-side.
- Mutações via API REST.
- Ações sensíveis geram auditoria.

## 4.3 Padrão visual e de layout
- Layout principal padrão do sistema (`layout('app::layouts/main')`).
- Cabeçalho com breadcrumbs + ações + filtros globais.
- KPIs no topo.
- Datatable ou cards no corpo principal.
- Drawers laterais para CRUD.
- Kanban onde o fluxo visual for relevante.
- Charts com drill-down quando aplicável.
- Desktop-first com responsividade para tablet e mobile.

---

# 5. Perfis e Papéis

## 5.1 Perfis base
Super Admin · Admin Entidade · Admin Unidade · Solicitante · Comprador · Gestor Aprovador · Financeiro · Fiscal · Almoxarife · Recebedor · Qualidade · Gestor de Estoque · Gestor de Contrato · Auditor · Compliance.

## 5.2 Escopo dos papéis

| Perfil | Escopo |
|---|---|
| Super Admin | Acesso total multi-tenant conforme política de suporte/implantação |
| Admin Entidade | Acesso total da entidade + parametrizações globais |
| Admin Unidade | Gestão operacional e parametrizações limitadas da unidade |
| Solicitante | Cria e acompanha requisições; não aprova a própria em faixas bloqueadas |
| Comprador | Conduz cotações, negocia, emite pedido, acompanha entrega |
| Gestor Aprovador | Aprova ou reprova por alçada |
| Almoxarife | Acompanha itens críticos, sugere reposição, recebe entrada em estoque |
| Recebedor | Registra recebimento e divergência |
| Qualidade | Valida inspeção de itens críticos |
| Financeiro | Valida orçamento, centro de custo e aderência financeira |
| Fiscal | Valida aspectos fiscais/documentais integráveis |
| Gestor de Contrato | Administra contratos, saldo e vigência |
| Auditor / Compliance | Consulta trilhas, exceções, exportações e políticas |

---

# 6. Matriz de Permissões

## 6.1 Permissões por domínio

```
supplies.dashboard.view

supplies.requisition.view
supplies.requisition.create
supplies.requisition.update_draft
supplies.requisition.submit
supplies.requisition.cancel
supplies.requisition.approve
supplies.requisition.reject
supplies.requisition.return_adjustment
supplies.requisition.bulk_approve
supplies.requisition.export

supplies.quotation.view
supplies.quotation.create
supplies.quotation.update
supplies.quotation.invite_suppliers
supplies.quotation.register_proposal
supplies.quotation.compare
supplies.quotation.award
supplies.quotation.cancel
supplies.quotation.export

supplies.purchase_order.view
supplies.purchase_order.create
supplies.purchase_order.issue
supplies.purchase_order.confirm
supplies.purchase_order.cancel
supplies.purchase_order.resend
supplies.purchase_order.update_delivery_forecast
supplies.purchase_order.export

supplies.receipt.view
supplies.receipt.create
supplies.receipt.update
supplies.receipt.inspect
supplies.receipt.approve
supplies.receipt.reject
supplies.receipt.return_supplier
supplies.receipt.close_divergence
supplies.receipt.export

supplies.supplier.view
supplies.supplier.create
supplies.supplier.update
supplies.supplier.block
supplies.supplier.unblock
supplies.supplier.homologate
supplies.supplier.evaluate
supplies.supplier.export

supplies.contract.view
supplies.contract.create
supplies.contract.update
supplies.contract.renew
supplies.contract.suspend
supplies.contract.close
supplies.contract.export

supplies.stock_planning.view
supplies.stock_planning.generate_requisition
supplies.stock_planning.adjust_parameters
supplies.stock_planning.transfer

supplies.automation.view
supplies.automation.retry
supplies.automation.pause
supplies.automation.activate
supplies.automation.update_rules

supplies.controls.view
supplies.controls.update
supplies.audit.view
supplies.audit.export
supplies.settings.manage
```

## 6.2 Restrições obrigatórias
- Bloqueio de autoaprovação acima da política.
- Bloqueio de solicitante = aprovador em cenários sensíveis.
- Bloqueio de emissão de pedido por usuário sem permissão.
- Bloqueio de recebimento por fornecedor bloqueado quando política exigir.
- Bloqueio de edição após encerramento.
- Sem exclusão física — usar cancelamento/soft delete.

---

# 7. Mapa de Navegação

```
Suprimentos
├── Dashboard
├── Requisições
├── Aprovações
├── Cotações
├── Pedidos de Compra
├── Agenda de Entregas
├── Recebimentos
├── Divergências
├── Almoxarifado & Ressuprimento
├── Itens Críticos
├── Fornecedores
├── Avaliações de Fornecedor
├── Contratos & Atas
├── Kanban Operacional
├── Relatórios
├── Automações
├── Controles & Compliance
└── Gerenciamentos
```

---

# 8. Dashboard de Suprimentos

## 8.1 Objetivo
Consolidar em uma única view todas as métricas estratégicas e operacionais do ciclo de suprimentos, permitindo ao gestor identificar gargalos, priorizar ações, monitorar fornecedores, controlar orçamento e acompanhar automações ativas.

## 8.2 Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Cabeçalho: Breadcrumb | Título | Ações | Período               │
├─────────────────────────────────────────────────────────────────┤
│  Filtros Globais: Entidade | Unidade | Categoria | Comprador    │
├──────────┬──────────┬──────────┬──────────┬────────────────────┤
│  KPI 1   │  KPI 2   │  KPI 3   │  KPI 4   │  KPI 5             │
├──────────┴──────────┴──────────┴──────────┴────────────────────┤
│  KPI 6   │  KPI 7   │  KPI 8   │  KPI 9   │  KPI 10            │
├──────────────────────────┬──────────────────────────────────────┤
│  Chart: Spend Evolution  │  Chart: Spend por Unidade/Categoria  │
├──────────────────────────┼──────────────────────────────────────┤
│  Chart: Top Fornecedores │  Chart: Funnel PR > Recebimento      │
├──────────────────────────┴──────────────────────────────────────┤
│  Widgets Operacionais: 4 cards lado a lado                      │
├──────────────────────────┬──────────────────────────────────────┤
│  Datatable: Pendências   │  Datatable: Pedidos em atraso        │
├──────────────────────────┼──────────────────────────────────────┤
│  Datatable: Itens        │  Datatable: Contratos a vencer       │
│  Críticos                │                                      │
├──────────────────────────┴──────────────────────────────────────┤
│  Chart: Heatmap Itens Críticos por Unidade                      │
├──────────────────────────┬──────────────────────────────────────┤
│  Chart: Radar Fornecedor │  Chart: Lead Time Médio              │
├──────────────────────────┴──────────────────────────────────────┤
│  Timeline de Eventos Recentes                                   │
├─────────────────────────────────────────────────────────────────┤
│  Painel de Automações: Jobs com erro | Alertas ativos           │
└─────────────────────────────────────────────────────────────────┘
```

**Regras de layout:**
- Título: `Suprimentos — Dashboard` | Breadcrumb: `Início > Suprimentos > Dashboard`
- Botões fixos no header: Exportar PDF, Exportar Excel, Salvar Visão, Compartilhar, Atualizar
- KPIs: 5 por linha desktop, 2 por linha mobile
- Charts: 2 colunas desktop, 1 coluna mobile
- Tabelas operacionais: 2 colunas desktop, 1 coluna mobile
- Filtros globais em barra colapsável fixada abaixo do header
- Auto refresh configurável: 1 min / 5 min / 15 min / desativado
- Chips de filtros ativos visíveis

## 8.3 Controles do header
- Seletor de período: hoje / esta semana / este mês / trimestre / semestre / ano / personalizado
- Botões: Exportar PDF · Exportar Excel · Salvar visão · Compartilhar · Resetar filtros · Atualizar agora
- Toggle: Auto refresh
- Chip de última atualização com timestamp

## 8.4 Filtros globais (persistidos por usuário)
Entidade (multi) · Unidade (multi, dependente da entidade) · Categoria de item · Grupo de item · Família · Centro de custo · Comprador responsável · Fornecedor · Contrato · Tipo (produto / serviço / ativo / consumo) · Urgência (normal / urgente / crítica) · Status geral · Período de referência.

Comportamento: todos os widgets, charts e datatables reagem aos filtros; chips de filtros ativos com botão X individual e "Limpar tudo".

## 8.5 KPIs — Faixa 1: Estratégicos

| KPI | Label | Métrica | Cor |
|---|---|---|---|
| 1 | Gasto Total | Soma total do gasto no período com delta vs anterior | Primária |
| 2 | Sob Contrato | Gasto com fornecedores em contrato ativo | Verde ≥ meta, amarelo abaixo |
| 3 | Fora de Contrato (Maverick) | Gasto sem contrato | Vermelho acima do threshold |
| 4 | Saving | Economia obtida em cotações vs referência | Verde |
| 5 | Compliance Contratual | % compras realizadas conforme contratos | Gauge/barra com meta configurável |

## 8.6 KPIs — Faixa 2: Operacionais

| KPI | Label | Métrica | Cor |
|---|---|---|---|
| 6 | Req. Abertas | Total requisições com status ativo; badge de pendentes de aprovação | Azul |
| 7 | Pedidos Atrasados | POs com expected_delivery < hoje sem recebimento total | Vermelho > 0 |
| 8 | PO Accuracy | % pedidos corretos (sem divergência); meta ≥ 95% | Semântica |
| 9 | Fill Rate | % itens entregues no prazo e completos | Semântica, meta configurável |
| 10 | Lead Time Médio | Dias médios PR → recebimento; sub-label PR>PO vs PO>Recebimento | Delta vs anterior |

## 8.7 KPIs — Faixa 3: Estoque e Fornecedores

| KPI | Label | Métrica |
|---|---|---|
| 11 | Em Ruptura | Itens com estoque zero ou abaixo do mínimo crítico; ação rápida "gerar requisição" |
| 12 | Abaixo do Mínimo | Itens com cobertura abaixo do threshold |
| 13 | Taxa de Defeito | % itens recebidos com defeito; meta ≤ 2% |
| 14 | Entrega no Prazo | % pedidos entregues dentro do prazo; meta ≥ 90% |
| 15 | Contratos a Vencer | Contratos com end_date ≤ 30 dias; urgente ≤ 7 dias |

## 8.8 Cards operacionais

**Card 1 — Pendências de aprovação:** Top 5 mais antigas · código, solicitante, valor, dias pendente, SLA status · ações Aprovar/Reprovar · link "Ver todas".

**Card 2 — Próximas entregas:** Entregas previstas hoje e amanhã · código, fornecedor, itens, hora · badge de atraso · link "Ver agenda".

**Card 3 — Divergências abertas:** Top 5 por severidade · tipo, fornecedor, dias em aberto, responsável · ações Atribuir/Ver detalhe.

**Card 4 — Automações com erro:** Jobs com erro · nome, último erro, retries, last_run_at · ação Reprocessar · link "Ver automações".

## 8.9 Charts

| # | Tipo | Descrição | API |
|---|---|---|---|
| 1 | Line chart | Evolução do Spend: séries Gasto Total, Sob Contrato, Fora de Contrato; drill-down no mês | `/charts/spend-evolution` |
| 2 | Stacked column | Spend por Unidade × Categoria; drill-down por categoria | `/charts/spend-by-unit-category` |
| 3 | Donut | Distribuição de gasto; máx 8 fatias + "Outros"; centro mostra total | `/charts/spend-distribution` |
| 4 | Horizontal bar | Top 10 fornecedores por valor; cor por tier A/B/C | `/charts/top-suppliers` |
| 5 | Funnel | Pipeline: Requisição → Aprovação → Cotação → Pedido → Recebimento | `/charts/funnel` |
| 6 | Line | Lead Time médio por mês: PR>PO, PO>Receipt, Receipt>Stock | `/charts/lead-time` |
| 7 | Column | Pedidos atrasados por fornecedor; cor por nível de atraso | `/charts/late-orders-by-supplier` |
| 8 | Radar | Score de fornecedor: preço, prazo, qualidade, compliance, atendimento; top 3 | `/charts/supplier-radar` |
| 9 | Heatmap | Itens críticos por unidade × criticidade; gradiente vermelho→amarelo→verde | `/charts/items-heatmap` |
| 10 | Area | Cobertura de estoque por família; linha de threshold tracejada | `/charts/coverage` |

**Regras globais de charts:** tooltip enriquecido · drill-down · exportação (PNG/PDF/CSV) · clique filtra grids · comparação com período anterior · cores padronizadas por status.

## 8.10 Datatables de apoio do dashboard

**Pendências de aprovação:** code, tipo, solicitante, unidade, valor, dias pendente, SLA status, aprovador atual, ações (aprovar/reprovar em lote).

**Pedidos em atraso:** code, fornecedor, unidade, valor, data prevista, atraso em dias, status, responsável, ações (contatar/escalar/cancelar).

**Itens críticos:** item_code, descrição, unidade, estoque atual, mínimo, cobertura em dias, risco, fornecedor preferencial, ações (gerar req./transferir).

**Contratos a vencer:** code, fornecedor, título, end_date, dias restantes, saldo, gestor, status, ações (renovar/encerrar).

## 8.11 Timeline de eventos
Últimos eventos em ordem cronológica reversa: nova requisição · aprovação/reprovação · cotação aberta/encerrada · pedido emitido/atrasado · recebimento · divergência · fornecedor bloqueado · contrato renovado · automação com erro · item em ruptura.

Campos por evento: ícone, timestamp relativo, código do documento, usuário, entidade/unidade, link para detalhe.
Controles: filtrar por tipo/unidade · carregar mais · marcar como lido · exportar.

## 8.12 Painel de automações
- Jobs com erro: nome, último erro, retries, botão reprocessar.
- Jobs pausados: nome, motivo, ativado/pausado por.
- Alertas ativos: gatilhos de estoque mínimo, SLA vencido, contrato a vencer.
- Próximas execuções: jobs agendados para 24h.

## 8.13 APIs do dashboard

Prefixo: `GET /api/v1/supplies/dashboard`

```
/                         payload completo
/widgets                  todos os KPIs em batch
/widgets/spend-total
/widgets/spend-contract
/widgets/spend-maverick
/widgets/saving
/widgets/requisitions-open
/widgets/orders-late
/widgets/po-accuracy
/widgets/fill-rate
/widgets/lead-time
/widgets/items-rupture
/widgets/items-below-min
/widgets/defect-rate
/widgets/on-time-delivery
/widgets/contracts-expiring
/charts/spend-evolution
/charts/spend-by-unit-category
/charts/spend-distribution
/charts/top-suppliers
/charts/funnel
/charts/lead-time
/charts/late-orders-by-supplier
/charts/supplier-radar
/charts/items-heatmap
/charts/coverage
/tables/pending-approvals
/tables/late-orders
/tables/critical-items
/tables/expiring-contracts
/timeline
/automations/alerts
```

**Padrão de resposta:**
```json
{
  "data": {},
  "meta": {
    "period": "2026-01",
    "entity_uuid": "...",
    "unit_uuid": "...",
    "generated_at": "2026-06-06T20:00:00Z"
  }
}
```

## 8.14 Performance e UX do dashboard
- Widgets carregados em batch único na abertura.
- Charts em paralelo via fetch.
- Skeleton loading em todos os blocos.
- Datatables com paginação server-side, máx 10 linhas no dashboard.
- Lazy load de charts abaixo da dobra.
- Cache de KPIs configurável (padrão 5 min).
- Estados de erro com retry automático.

## 8.15 Responsividade do dashboard
- **Desktop ≥ 1280px:** 5 KPIs/linha · 2 charts/linha · 2 datatables/linha.
- **Tablet 768–1279px:** 3 KPIs/linha · 1 chart/linha · 2 datatables/linha.
- **Mobile < 768px:** 2 KPIs/linha · 1 chart simplificado · datatables → cards compactos · aprovações rápidas habilitadas.

## 8.16 Segurança do dashboard
- Permissão mínima: `supplies.dashboard.view`.
- Filtros entity_uuid/unit_uuid obrigatórios nas queries.
- Dados sensíveis mascarados por RBAC.
- Exportações auditadas.
- Rate limit no batch de widgets.
- CSRF em ações POST (aprovações rápidas).
- Logs de acesso por usuário.

---

# 9. Páginas do Módulo

## 9.1 Requisições

**Objetivo:** Criar, editar, aprovar, acompanhar e converter requisições internas.

**Blocos:** cabeçalho com ações · datatable principal · kanban opcional · drawer CRUD · painel lateral de histórico · painel de orçamento · painel de estoque atual · timeline de aprovação.

**Controles:** nova requisição · importar itens · duplicar · enviar para aprovação · cancelar · comentar · anexar · aprovar em lote · exportar · mudar visualização · salvar filtros.

**Estados:**
`draft` → `submitted` → `under_review` → `approved` / `partially_approved` / `rejected` / `returned_for_adjustment` → `sourcing` → `converted` / `cancelled` / `closed`

**Colunas do datatable:**
id · code · title · requester · department · unit · cost_center · request_type · category · priority · total_items · estimated_total_amount · budget_status · workflow_status · current_approver · sla_status · created_at · needed_at · updated_at

**Filtros:** período · solicitante · unidade · departamento · centro de custo · categoria · prioridade · status · workflow · orçamento · anexo · urgente · tipo (estoque/serviço/ativo).

**Ações em linha:** visualizar · editar · duplicar · comentar · anexar · enviar aprovação · aprovar · reprovar · solicitar ajuste · gerar cotação · cancelar · auditar.

**Ações em lote:** exportar · aprovar · reprovar · atribuir comprador · marcar prioridade · cancelar · etiquetar.

---

## 9.2 Aprovações

**Objetivo:** Centralizar pendências de aprovação do usuário ou da fila do setor.

**Blocos:** cards de pendência · datatable · painel de regras aplicadas · timeline do fluxo · comparativo orçado × solicitado.

**Controles:** aprovar · reprovar · solicitar ajuste · delegar · reenviar notificação · aprovar em lote · visualizar detalhes da política.

**Colunas:** code · tipo · solicitante · unidade · valor · política aplicada · etapa atual · data limite SLA · dias pendente · urgência · risco · ações.

---

## 9.3 Cotações

**Objetivo:** Controlar RFQs, propostas, comparação e adjudicação.

**Blocos:** datatable · cards de fornecedores convidados · comparativo lado a lado · score automático · drawer de proposta · painel de savings · anexos · timeline.

**Controles:** nova cotação · convidar fornecedor · reenviar convite · registrar proposta · encerrar · comparar · adjudicar · gerar pedido · exportar comparativo.

**Estados:**
`draft` → `open` → `waiting_proposals` → `under_analysis` → `awarded` / `not_awarded` / `expired` / `cancelled` / `closed`

**Colunas:** code · requisição vinculada · comprador · fornecedores convidados · propostas recebidas · menor preço · melhor score · saving estimado · deadline · status · created_at · updated_at.

**Quadro comparativo por item:** fornecedor · valor unitário · valor total · frete · prazo de entrega · condição de pagamento · validade · marca/modelo · aderência técnica · score qualidade/preço/prazo/compliance/total.

**Regras:** exigir número mínimo de cotações por faixa; single source somente com justificativa; registrar motivo da adjudicação; armazenar snapshot do comparativo no fechamento.

---

## 9.4 Pedidos de Compra

**Objetivo:** Gerir emissão e acompanhamento do pedido até a entrega.

**Blocos:** datatable · status board · drawer · entregas vinculadas · documentos · saldo contratual · tracking · timeline.

**Controles:** emitir · reenviar para fornecedor · confirmar aceite · alterar previsão · cancelar · encerrar · exportar PDF/Excel.

**Estados:**
`draft` → `issued` → `supplier_confirmed` → `partially_received` / `fully_received` / `delayed` / `diverged` / `cancelled` / `closed`

**Colunas:** code · fornecedor · unidade · origem · contrato · comprador · valor total · moeda · expected_delivery_date · real_delivery_date · receipt_progress · divergence_flag · invoice_status · status · created_at · updated_at.

**Abas do drawer:** Resumo · Itens · Entrega · Financeiro · Documentos · Recebimentos · Divergências · Auditoria.

---

## 9.5 Agenda de Entregas

**Objetivo:** Visualizar previsões e atrasos de entrega.

**Visualizações:** calendário · agenda · lista · kanban de entrega.

**Filtros:** período · fornecedor · unidade · status · atrasado/no prazo · tipo de item.

**Campos por linha/card:** pedido · fornecedor · data prevista · quantidade pendente · status · atraso em dias · contato do fornecedor · prioridade.

---

## 9.6 Recebimentos

**Objetivo:** Registrar a entrada física e documental do pedido.

**Blocos:** datatable · agenda do dia · drawer · checklist · conferência por item · evidências · integração com estoque · painel de divergência.

**Controles:** iniciar recebimento · registrar parcial/total · aprovar inspeção · reprovar item · gerar devolução · encerrar · anexar evidência · imprimir comprovante · exportar.

**Estados:**
`pending` → `in_progress` → `received_partial` / `received_total` → `under_inspection` → `approved` / `rejected` / `returned` / `closed`

**Colunas:** code · pedido · fornecedor · data entrega · conferente · doc fiscal · qty_ordered · qty_received · qty_rejected · warehouse_status · inspection_status · divergence_status · closed_at.

---

## 9.7 Divergências

**Objetivo:** Controlar problemas de quantidade, qualidade, documento e prazo.

**Tipos:** quantidade menor · quantidade maior · item incorreto · item avariado · validade inadequada · lote divergente · documento fiscal divergente · entrega parcial · atraso · embalagem inadequada · especificação divergente.

**Controles:** abrir ocorrência · classificar severidade · atribuir responsável · notificar fornecedor · anexar foto · registrar tratativa · encerrar · gerar devolução.

**Colunas:** code · origem · pedido · recebimento · fornecedor · tipo · severidade · status · responsável · opened_at · sla_due_at · closed_at.

---

## 9.8 Almoxarifado & Ressuprimento

**Objetivo:** Monitorar estoque operacional e disparar reposição.

**Blocos:** itens críticos · estoque abaixo do mínimo · cobertura por família · curva ABC · consumo médio · sugestão de compra · sugestão de transferência · histórico de ressuprimento.

**Controles:** gerar requisição · aprovar sugestão · simular cobertura · ajustar mínimo/máximo · consolidar demanda · exportar plano.

**Colunas:** item_code · descrição · unidade · estoque atual · estoque mínimo · estoque máximo · ponto de pedido · consumo médio diário · cobertura em dias · última compra · último preço · fornecedor preferencial · risco.

---

## 9.9 Itens Críticos

**Critérios:** ruptura · cobertura abaixo do limite · alta variação de consumo · fornecedor único · lead time alto · alta taxa de defeito · uso crítico assistencial/operacional · contrato próximo do fim.

**Controles:** gerar requisição · transferir entre unidades · marcar contingência · abrir fornecedor alternativo · acompanhar plano de ação.

---

## 9.10 Fornecedores

**Objetivo:** Gerenciar cadastro, homologação, documentos, bloqueios e performance.

**Blocos:** datatable · drawer · documentação · categorias atendidas · contratos · score · ocorrências · histórico de pedidos · avaliações.

**Controles:** cadastrar · editar · homologar · bloquear · desbloquear · solicitar atualização documental · vincular categoria · registrar avaliação · exportar.

**Colunas:** code · legal_name · trade_name · tax_document · cidade · UF · categoria · homologation_status · risk_level · score_total · late_rate · defect_rate · active_contracts · blocked_flag · updated_at.

---

## 9.11 Avaliações de Fornecedor

**Critérios base:** qualidade · prazo · preço · aderência documental · atendimento · taxa de divergência · flexibilidade · cumprimento contratual.

**Blocos:** datatable · histórico por período · radar comparativo · evolução de score · ranking.

---

## 9.12 Contratos & Atas

**Objetivo:** Gerenciar contratos, atas, vigências, saldo e reajustes.

**Blocos:** datatable · drawer · saldos · vigências · cronograma de reajuste · documentos · pedidos vinculados · fornecedores vinculados.

**Controles:** criar · renovar · suspender · encerrar · reajustar · vincular pedido · anexar termo · exportar.

**Colunas:** code · supplier · tipo · título · start_date · end_date · amount_ceiling · consumed_amount · balance_amount · manager · status · documents_status.

---

## 9.13 Kanban Operacional

**Visões disponíveis:** Requisições · Cotações · Pedidos · Ocorrências · Contratos.

**Regras:** cards com ações rápidas · drag-and-drop apenas quando a política permitir · mudança de coluna gera auditoria · colunas bloqueadas não aceitam drop · cards exibem SLA, prioridade e responsáveis.

**Kanban de requisições:** Rascunho → Enviada → Em aprovação → Aguardando ajuste → Aprovada → Em cotação → Convertida → Cancelada → Encerrada.

**Kanban de pedidos:** Emitido → Confirmado → Em preparação → Em trânsito → Recebido parcial → Em inspeção → Divergência → Recebido total → Encerrado.

**Kanban de divergências:** Aberta → Em análise → Aguardando fornecedor → Aguardando unidade → Em devolução → Resolvida → Encerrada.

**Cards exibem:** code · título · unidade · responsável · prioridade · valor · badge SLA · dias em aberto · fornecedor · progresso.

**Ações rápidas no card:** abrir drawer · comentar · anexar · aprovar · reprovar · atribuir · mover (se permitido) · marcar urgência.

---

## 9.14 Relatórios

**Relatórios mínimos:**
- Gasto por período / unidade / categoria / fornecedor / centro de custo.
- Compras emergenciais · compras fora de contrato.
- Requisições por status · tempo médio por etapa.
- Cotações por comprador · savings por processo.
- Pedidos por fornecedor · atraso de entrega.
- Divergências por tipo · desempenho de fornecedores.
- Contratos a vencer · itens críticos · cobertura de estoque.
- Requisições automáticas geradas · auditoria de aprovações · log de exportações.

**Recursos:** filtros avançados · exportação CSV/Excel/PDF · agendamento · snapshot · compartilhamento por perfil.

---

## 9.15 Automações

**Blocos:** jobs ativos · jobs com erro · logs · retries · cronogramas · filas por evento · webhooks · consumo de integração.

**Controles:** pausar job · ativar job · reprocessar · editar regra · baixar log · visualizar payload · reenviar webhook.

---

## 9.16 Controles & Compliance

**Objetivo:** Centralizar políticas, alçadas, bloqueios, segregação e exceções.

**Blocos:** políticas de compras · alçadas · segregação de função · exceções · single source · compras emergenciais · exportações · trilhas de auditoria · bloqueios automáticos.

**Controles:** editar política · simular workflow · revisar/aprovar/rejeitar exceção · exportar evidência.

---

## 9.17 Gerenciamentos

**Cadastros mestres:** categorias · subcategorias · famílias · unidades de medida · tipos de requisição · motivos de urgência/devolução/bloqueio · SLA por processo · alçadas · templates de email · tipos de contrato · critérios de score · tolerâncias de recebimento · políticas de cotação mínima · armazéns · locais de entrega · calendários de abastecimento · regras de automação · numeração `code`.

---

# 10. KPIs Completos

## 10.1 Estratégicos
Spend Total · Spend sob Gestão · Spend fora de Contrato · Saving do Período · Procurement ROI · Contract Compliance · Compras Emergenciais · Maverick Spend.

## 10.2 Operacionais
Requisições Abertas · Requisições Pendentes de Aprovação · Cotações em Aberto · Pedidos Aguardando Entrega · Pedidos Atrasados · Recebimentos com Divergência · Itens Abaixo do Mínimo · Itens em Ruptura.

## 10.3 Fornecedor
Fornecedores Ativos · Fornecedores Bloqueados · Lead Time Médio · On-Time Delivery Rate · Supplier Defect Rate · Fill Rate · Score Médio de Fornecedor.

## 10.4 Estoque e Reposição
Cobertura Média · Itens com Reposição Automática · Requisições Automáticas Geradas · Cobertura crítica < X dias.

---

# 11. Datatables — Regras Globais

Todos os datatables devem ter:
- Paginação server-side · ordenação · busca global · filtros avançados.
- Colunas configuráveis e persistidas por usuário.
- Exportação auditada.
- Ações em lote.
- Totalizadores quando aplicável.
- Drawer ao clicar na linha.

---

# 12. Drawers CRUD

## 12.1 Padrão
- Lateral direita, largura lg/xl.
- Cabeçalho com `code`, status e ações.
- Abas.
- Botões fixos no rodapé.
- Validação inline.
- Confirmação em ações críticas.
- Histórico, comentários, anexos, auditoria.
- Loading states.
- Concorrência otimista.

## 12.2 Drawer Requisição
**Abas:** Dados Gerais · Itens · Orçamento · Aprovação · Anexos · Comentários · Auditoria.

**Campos — Dados Gerais:** uuid · code · requester_user_uuid · requester_department_uuid · entity_uuid · unit_uuid · title · description · request_type · priority · urgency_reason · needed_at · cost_center_uuid · budget_account_uuid · project_uuid · contract_reference_uuid · justification · stock_related_flag · service_related_flag · asset_related_flag · status.

**Campos — Itens:** item_uuid · item_code · item_description · technical_specification · category_uuid · quantity · uom · estimated_unit_price · estimated_total_price · preferred_brand · preferred_supplier_uuid · delivery_unit_uuid · delivery_location · needed_at · stock_item_flag · asset_flag · service_flag · notes.

**Ações:** salvar rascunho · submeter · aprovar · reprovar · solicitar ajuste · duplicar · cancelar · gerar cotação.

## 12.3 Drawer Cotação
**Abas:** Cabeçalho · Fornecedores · Propostas · Comparativo · Decisão · Anexos · Auditoria.

**Campos:** uuid · code · requisition_uuid · buyer_user_uuid · quotation_deadline · minimum_quotes_required · payment_terms_default · delivery_terms_default · evaluation_criteria_json · invited_suppliers_json · award_supplier_uuid · award_reason · single_source_justification · status.

## 12.4 Drawer Proposta
**Campos:** supplier_uuid · quotation_uuid · valid_until · delivery_days · payment_terms · freight_terms · item_lines_json · total_amount · commercial_notes · compliance_notes · attachments.

## 12.5 Drawer Pedido de Compra
**Abas:** Resumo · Itens · Entrega · Financeiro · Documentos · Recebimentos · Divergências · Auditoria.

**Campos:** uuid · code · supplier_uuid · quotation_uuid · contract_uuid · issue_date · expected_delivery_date · buyer_user_uuid · payment_terms · freight_type · currency · subtotal_amount · tax_amount · freight_amount · total_amount · billing_address_json · shipping_address_json · approval_snapshot_json · status.

## 12.6 Drawer Recebimento
**Abas:** Dados · Quantidades · Qualidade · Fiscal · Estoque · Evidências · Divergências · Auditoria.

**Campos:** uuid · code · purchase_order_uuid · supplier_uuid · receiver_user_uuid · delivered_at · invoice_number · invoice_series · invoice_date · warehouse_uuid · line_received_qty · line_rejected_qty · batch_number · expiry_date · serial_number · inspection_result · divergence_reason · return_required · notes · status.

## 12.7 Drawer Fornecedor
**Abas:** Cadastro · Fiscal/Jurídico · Bancário · Categorias · SLA/Performance · Documentos · Bloqueios · Auditoria.

**Campos:** uuid · code · legal_name · trade_name · tax_document · state_registration · municipal_registration · email · phone · website · address_json · bank_account_json · homologation_status · risk_level · blocked_flag · blocked_reason · status.

## 12.8 Drawer Contrato
**Abas:** Dados Gerais · Vigência · Itens e Saldos · Reajustes · SLA · Documentos · Fornecedores · Auditoria.

**Campos:** uuid · code · supplier_uuid · contract_type · title · description · start_date · end_date · amount_ceiling · consumed_amount · balance_amount · reajust_rule · manager_user_uuid · status.

---

# 13. Fluxos de Negócio

## 13.1 Fluxo da requisição
1. Usuário cria requisição.
2. Sistema valida campos obrigatórios.
3. Sistema consulta política de aprovação.
4. Sistema verifica orçamento, categoria, urgência e tipo.
5. Requisição entra em workflow.
6. Aprovadores recebem notificação.
7. Após aprovação, segue para cotação ou pedido direto.
8. Processo é convertido.
9. Requisição é encerrada.

## 13.2 Fluxo de aprovação
1. Documento entra em fila.
2. Aprovador analisa.
3. Pode aprovar, reprovar ou solicitar ajuste.
4. Se multi-step, segue para a próxima etapa.
5. Se estourar SLA, sistema escala.
6. Se houver delegação ativa, encaminha ao delegado.

## 13.3 Fluxo de cotação
1. Comprador cria RFQ.
2. Convida fornecedores.
3. Registra propostas.
4. Sistema calcula score.
5. Comprador compara.
6. Registra justificativa.
7. Adjudica fornecedor.
8. Gera pedido.

## 13.4 Fluxo do pedido
1. Pedido é emitido.
2. Fornecedor confirma.
3. Sistema monitora previsão.
4. Se atrasar, gera alerta.
5. Segue para recebimento.

## 13.5 Fluxo de recebimento
1. Recebedor inicia conferência.
2. Registra quantidade.
3. Qualidade inspeciona, se necessário.
4. Divergência abre ocorrência.
5. Itens aprovados entram em estoque.
6. Processo é encerrado.

## 13.6 Fluxo de devolução
1. Divergência exige devolução.
2. Sistema gera registro de retorno.
3. Fornecedor é notificado.
4. Itens retornam ao status apropriado.
5. Caso encerrado após evidência.

## 13.7 Fluxo de ressuprimento automático
1. Sistema monitora estoque mínimo e cobertura.
2. Identifica item crítico.
3. Gera sugestão ou requisição automática.
4. Gestor valida.
5. Processo segue fluxo normal.

---

# 14. Automações

## 14.1 Gatilhos operacionais
- Estoque abaixo do mínimo · cobertura abaixo do limite.
- Pedido atrasado · contrato a vencer · documento de fornecedor vencendo.
- Aprovação em atraso · divergência aberta · fornecedor bloqueado.
- Variação de preço acima da tolerância · compra sem cotações mínimas.
- Compra fora de contrato · single source sem justificativa.

## 14.2 Ações automáticas
- Gerar requisição automática · notificar aprovador · escalar SLA.
- Bloquear fornecedor · recalcular score de fornecedor.
- Recalcular curva ABC · recalcular cobertura.
- Sugerir consolidação de compra · sugerir fornecedor preferencial.
- Enviar e-mail/webhook · reprocessar integração.

## 14.3 Jobs agendados
- Consolidar KPIs · recalcular rankings · fechar SLAs.
- Validar documentos · atualizar contratos · atualizar métricas de estoque.
- Reprocessar filas órfãs · gerar snapshots de auditoria.

---

# 15. Controles de Negócio

## 15.1 Políticas
- Exigir orçamento por categoria.
- Exigir mínimo de cotações por faixa de valor.
- Permitir compra direta só com justificativa.
- Exigir contrato para categorias estratégicas.
- Exigir inspeção para itens críticos.
- Exigir lote/validade para itens controlados.
- Exigir segregação de função.
- Impedir recebimento acima da tolerância.
- Impedir pedido acima da alçada.
- Impedir fornecedor bloqueado.

## 15.2 Tolerâncias
- Quantidade recebida a maior · quantidade recebida a menor.
- Preço · prazo · validade mínima.

## 15.3 Exceções
- Compra emergencial · fornecedor único.
- Contrato expirando com renovação em andamento.
- Recebimento sem doc final em contingência.
- Override financeiro com justificativa.

---

# 16. Controles de Segurança

- Autenticação via IAM do sistema.
- Autorização RBAC + escopo.
- Validação server-side obrigatória.
- Proteção CSRF.
- Sanitização de entrada.
- Rate limit em endpoints críticos.
- Logs estruturados.
- Trilha de auditoria imutável.
- Hash de anexos.
- Mascaramento de dados sensíveis.
- Concorrência otimista em atualização.
- Segregação por entity_uuid e unit_uuid.
- Retenção configurável de logs.

---

# 17. Auditoria

## 17.1 Eventos auditáveis
Criar/editar/submeter/aprovar/reprovar/solicitar ajuste/alterar item/alterar valor em requisição · Convidar fornecedor · Registrar proposta · Adjudicar · Emitir pedido · Alterar previsão · Registrar recebimento · Abrir/fechar divergência · Devolver ao fornecedor · Bloquear/desbloquear fornecedor · Alterar contrato · Exportar · Imprimir · Reprocessar job · Alterar política.

## 17.2 Campos de auditoria
```
actor_user_uuid
actor_user_code
action
entity_type
entity_uuid
entity_code
before_json
after_json
reason
ip_address
user_agent
request_id
entity_uuid_scope
unit_uuid_scope
created_at_utc
```

---

# 18. Estrutura de Dados

## 18.1 purchase_requisitions
id · uuid · code · entity_uuid · unit_uuid · requester_user_uuid · requester_department_uuid · title · description · request_type · priority · urgency_reason · cost_center_uuid · budget_account_uuid · project_uuid · estimated_total_amount · currency · needed_at · workflow_status · status · approval_policy_uuid · source_type · source_reference_uuid · created_at · updated_at · deleted_at.

## 18.2 purchase_requisition_items
id · uuid · code · requisition_uuid · item_uuid · item_code · description · technical_specification · category_uuid · quantity · uom · estimated_unit_price · estimated_total_price · preferred_brand · preferred_supplier_uuid · stock_item_flag · service_flag · asset_flag · delivery_unit_uuid · delivery_location · needed_at · notes · status.

## 18.3 approval_workflows
id · uuid · code · module · name · condition_json · active_flag · created_at · updated_at.

## 18.4 approval_workflow_steps
id · uuid · code · workflow_uuid · step_order · approver_type · approver_reference_uuid · sla_hours · required_flag · created_at · updated_at.

## 18.5 approval_instances
id · uuid · code · workflow_uuid · document_type · document_uuid · current_step · status · started_at · finished_at.

## 18.6 supplier_quotations
id · uuid · code · requisition_uuid · buyer_user_uuid · quotation_deadline · minimum_quotes_required · single_source_justification · award_supplier_uuid · award_reason · status · created_at · updated_at.

## 18.7 supplier_quotation_suppliers
id · uuid · code · quotation_uuid · supplier_uuid · invited_at · responded_at · response_status.

## 18.8 supplier_quotation_proposals
id · uuid · code · quotation_uuid · supplier_uuid · proposed_total_amount · delivery_days · payment_terms · validity_until · freight_terms · score_price · score_delivery · score_quality · score_compliance · score_total · status · created_at · updated_at.

## 18.9 purchase_orders
id · uuid · code · requisition_uuid · quotation_uuid · supplier_uuid · contract_uuid · buyer_user_uuid · issue_date · expected_delivery_date · supplier_confirmation_at · subtotal_amount · tax_amount · freight_amount · total_amount · currency · payment_terms · shipping_address_json · billing_address_json · approval_snapshot_json · status · created_at · updated_at.

## 18.10 purchase_order_items
id · uuid · code · purchase_order_uuid · source_requisition_item_uuid · item_uuid · description · quantity_ordered · quantity_received · quantity_rejected · unit_price · total_price · uom · delivery_unit_uuid · status.

## 18.11 goods_receipts
id · uuid · code · purchase_order_uuid · supplier_uuid · receiver_user_uuid · delivered_at · invoice_number · invoice_series · invoice_date · warehouse_uuid · inspection_status · divergence_status · status · notes · created_at · updated_at.

## 18.12 goods_receipt_items
id · uuid · code · goods_receipt_uuid · purchase_order_item_uuid · quantity_ordered · quantity_received · quantity_rejected · batch_number · expiry_date · serial_number · inspection_result · divergence_reason · stock_entry_status.

## 18.13 supplier_master
id · uuid · code · legal_name · trade_name · tax_document · state_registration · municipal_registration · email · phone · website · country · state · city · address_json · bank_account_json · homologation_status · risk_level · blocked_flag · blocked_reason · status · created_at · updated_at.

## 18.14 supplier_documents
id · uuid · code · supplier_uuid · document_type · file_uuid · issued_at · expires_at · validation_status · notes.

## 18.15 procurement_contracts
id · uuid · code · supplier_uuid · contract_type · title · description · start_date · end_date · amount_ceiling · consumed_amount · balance_amount · reajust_rule · manager_user_uuid · status · created_at · updated_at.

## 18.16 supplier_evaluations
id · uuid · code · supplier_uuid · related_receipt_uuid · period_reference · score_quality · score_delivery · score_price · score_service · score_compliance · score_total · evaluator_user_uuid · notes · created_at.

## 18.17 replenishment_rules
id · uuid · code · item_uuid · unit_uuid · min_stock · max_stock · reorder_point · safety_stock · avg_daily_consumption · lead_time_days · auto_requisition_flag · active_flag.

## 18.18 supply_automation_jobs
id · uuid · code · job_name · trigger_event · scope_type · scope_reference_uuid · payload_json · status · retries · last_run_at · next_run_at · last_error · created_at · updated_at.

---

# 19. Campos Obrigatórios por Formulário

## 19.1 Nova requisição
unit_uuid · title · request_type · priority · cost_center_uuid · needed_at · ao menos 1 item.

## 19.2 Novo item da requisição
description ou item_uuid · category_uuid · quantity · uom · needed_at.

## 19.3 Nova cotação
requisition_uuid · quotation_deadline · minimum_quotes_required (ou justificativa single source) · ao menos 1 fornecedor.

## 19.4 Nova proposta
supplier_uuid · validity_until · delivery_days · total_amount · ao menos 1 item cotado.

## 19.5 Novo pedido
supplier_uuid · issue_date · expected_delivery_date · payment_terms · ao menos 1 item.

## 19.6 Novo recebimento
purchase_order_uuid · delivered_at · receiver_user_uuid · ao menos 1 item recebido.

## 19.7 Novo fornecedor
legal_name · tax_document · email ou phone · status inicial.

## 19.8 Novo contrato
supplier_uuid · contract_type · title · start_date · end_date · status inicial.

---

# 20. Regras de Validação

- Quantidade deve ser > 0.
- Valor monetário deve ser >= 0.
- Data necessária não pode ser inválida.
- Pedido não pode ser emitido sem itens.
- Recebimento não pode exceder tolerância configurada.
- Fornecedor bloqueado não pode ser selecionado, salvo exceção autorizada.
- Contrato vencido não pode ser vinculado, salvo contingência autorizada.
- Requisição cancelada não pode voltar para edição comum.
- Alteração de valor após aprovação deve reabrir workflow se política exigir.
- Proposta vencida não pode ser adjudicada.
- Item crítico pode exigir inspeção obrigatória.
- Documentos vencidos do fornecedor podem bloquear contratação.

---

# 21. APIs REST

Prefixo base: `/api/v1/supplies`

## 21.1 Dashboard
```
GET  /dashboard
GET  /dashboard/widgets
GET  /dashboard/charts/spend-evolution
GET  /dashboard/charts/spend-by-unit-category
GET  /dashboard/charts/top-suppliers
GET  /dashboard/charts/funnel
GET  /dashboard/charts/lead-time
GET  /dashboard/charts/items-heatmap
```

## 21.2 Requisições
```
GET    /requisitions
POST   /requisitions
GET    /requisitions/{uuid}
PUT    /requisitions/{uuid}
PATCH  /requisitions/{uuid}
POST   /requisitions/{uuid}/submit
POST   /requisitions/{uuid}/approve
POST   /requisitions/{uuid}/reject
POST   /requisitions/{uuid}/return-adjustment
POST   /requisitions/{uuid}/cancel
POST   /requisitions/{uuid}/duplicate
POST   /requisitions/{uuid}/generate-quotation
GET    /requisitions/{uuid}/timeline
GET    /requisitions/{uuid}/audit
```

## 21.3 Aprovações
```
GET   /approvals/pending
GET   /approvals/history
POST  /approvals/{uuid}/approve
POST  /approvals/{uuid}/reject
POST  /approvals/{uuid}/delegate
POST  /approvals/{uuid}/request-adjustment
```

## 21.4 Cotações
```
GET   /quotations
POST  /quotations
GET   /quotations/{uuid}
PUT   /quotations/{uuid}
POST  /quotations/{uuid}/invite-suppliers
POST  /quotations/{uuid}/register-proposal
GET   /quotations/{uuid}/comparison
POST  /quotations/{uuid}/award
POST  /quotations/{uuid}/cancel
POST  /quotations/{uuid}/generate-po
```

## 21.5 Pedidos
```
GET   /purchase-orders
POST  /purchase-orders
GET   /purchase-orders/{uuid}
PUT   /purchase-orders/{uuid}
POST  /purchase-orders/{uuid}/issue
POST  /purchase-orders/{uuid}/confirm
POST  /purchase-orders/{uuid}/resend
POST  /purchase-orders/{uuid}/cancel
POST  /purchase-orders/{uuid}/update-forecast
GET   /purchase-orders/{uuid}/receipts
GET   /purchase-orders/{uuid}/audit
```

## 21.6 Entregas
```
GET   /deliveries/calendar
GET   /deliveries/list
GET   /deliveries/late
POST  /deliveries/{uuid}/notify
```

## 21.7 Recebimentos
```
GET   /receipts
POST  /receipts
GET   /receipts/{uuid}
PUT   /receipts/{uuid}
POST  /receipts/{uuid}/inspect
POST  /receipts/{uuid}/approve
POST  /receipts/{uuid}/reject
POST  /receipts/{uuid}/return-supplier
POST  /receipts/{uuid}/close
```

## 21.8 Divergências
```
GET   /divergences
POST  /divergences
GET   /divergences/{uuid}
PUT   /divergences/{uuid}
POST  /divergences/{uuid}/assign
POST  /divergences/{uuid}/resolve
POST  /divergences/{uuid}/close
```

## 21.9 Fornecedores
```
GET   /suppliers
POST  /suppliers
GET   /suppliers/{uuid}
PUT   /suppliers/{uuid}
POST  /suppliers/{uuid}/homologate
POST  /suppliers/{uuid}/block
POST  /suppliers/{uuid}/unblock
GET   /suppliers/{uuid}/evaluations
POST  /suppliers/{uuid}/evaluate
```

## 21.10 Contratos
```
GET   /contracts
POST  /contracts
GET   /contracts/{uuid}
PUT   /contracts/{uuid}
POST  /contracts/{uuid}/renew
POST  /contracts/{uuid}/suspend
POST  /contracts/{uuid}/close
```

## 21.11 Ressuprimento
```
GET   /replenishment/rules
POST  /replenishment/rules
PUT   /replenishment/rules/{uuid}
GET   /replenishment/items-critical
POST  /replenishment/generate-requisition
POST  /replenishment/simulate-coverage
```

## 21.12 Automações e Auditoria
```
GET   /automations/jobs
POST  /automations/jobs/{uuid}/retry
POST  /automations/jobs/{uuid}/pause
POST  /automations/jobs/{uuid}/activate
GET   /audit-logs
GET   /exports/logs
```

---

# 22. Notificações

## 22.1 Eventos
Requisição criada · requisição enviada · aprovação pendente · aprovação vencida · requisição reprovada · ajuste solicitado · cotação criada · proposta recebida · cotação encerrando · pedido emitido · pedido atrasado · entrega prevista hoje · recebimento com divergência · contrato a vencer · documento de fornecedor vencendo · fornecedor bloqueado · item em ruptura · job com erro.

## 22.2 Canais
- In-app · e-mail · webhook · fila externa (opcional).

---

# 23. Indicadores e Fórmulas

| Indicador | Fórmula |
|---|---|
| PO Accuracy | pedidos corretos / total pedidos × 100 |
| PO Cycle Time | data emissão PO − data criação PR |
| Supplier Lead Time | data recebimento − data emissão PO |
| Supplier Defect Rate | unidades com defeito / unidades recebidas × 100 |
| Vendor Late Delivery Rate | pedidos com atraso / total pedidos × 100 |
| Fill Rate | itens entregues completos e no prazo / itens pedidos × 100 |
| Spend Under Management | gasto gerido / gasto total × 100 |
| Contract Compliance | compras em contrato / compras elegíveis × 100 |
| Maverick Spend | compras fora de política ou contrato / gasto total × 100 |
| Inventory Coverage Days | estoque atual / consumo médio diário |
| SLA Compliance | etapas dentro do SLA / total etapas × 100 |
| Saving | valor referência − valor adjudicado |

---

# 24. Requisitos Não Funcionais

- Isolamento multi-tenant obrigatório.
- Performance de grids com paginação server-side.
- Indexação adequada para filtros frequentes.
- Transações consistentes em emissão e recebimento.
- Jobs idempotentes.
- Logs estruturados.
- Observabilidade.
- Retenção de auditoria configurável.
- Suporte a anexos com hash de integridade.
- Timezone em UTC no banco.
- UI responsiva (desktop-first).
- Acessibilidade básica (WCAG AA mínimo).
- Segurança em todas as APIs.
- Exportações rastreáveis.

---

# 25. Critérios de Aceite

O módulo será aceito quando:
- Permitir rastrear o processo ponta a ponta.
- Suportar workflow multinível configurável.
- Fornecer dashboard com KPIs e charts relevantes.
- Possuir páginas completas com datatables, drawers e kanban.
- Controlar fornecedores, contratos, pedidos, recebimentos e divergências.
- Aplicar RBAC e segregação de função.
- Registrar auditoria completa.
- Suportar automações e monitoramento operacional.
- Disponibilizar relatórios e exportações consistentes.

---

# 26. Checklist de Implementação

## Frontend
- [ ] Dashboard completo (15 KPIs, 10 charts, 4 datatables, timeline, painel de automações)
- [ ] Datatables de todos os domínios
- [ ] Drawers CRUD (requisição, cotação, pedido, recebimento, fornecedor, contrato)
- [ ] Kanbans (requisições, cotações, pedidos, divergências, contratos)
- [ ] Filtros globais com chips e persistência
- [ ] Exportações (CSV, Excel, PDF)
- [ ] Timeline
- [ ] Comentários e anexos
- [ ] Auditoria visual
- [ ] Skeleton loading em todos os blocos
- [ ] Responsividade desktop / tablet / mobile

## Backend
- [ ] APIs REST completas (seção 21)
- [ ] RBAC + permissões (seção 6)
- [ ] Workflow engine (multi-step, SLA, delegação)
- [ ] Automações e jobs (seção 14)
- [ ] Notificações (seção 22)
- [ ] Auditoria (seção 17)
- [ ] Integrações (Financeiro, Estoque, Patrimônio, Fiscal)
- [ ] Validações server-side (seção 20)
- [ ] Rate limit e segurança

## Banco de Dados
- [ ] Tabelas principais (seção 18)
- [ ] Índices em campos de filtro frequente
- [ ] Relacionamentos por uuid
- [ ] Tabelas de histórico/auditoria
- [ ] Tabelas de anexos e comentários
- [ ] Tabelas de workflows e automações
- [ ] Soft delete em todas as entidades

## Governança
- [ ] Matriz de permissões implementada
- [ ] Políticas de compra configuráveis
- [ ] Alçadas de aprovação
- [ ] Tolerâncias de recebimento
- [ ] Retenção de auditoria
- [ ] Templates de e-mail
- [ ] Catálogo de motivos (urgência, bloqueio, devolução)
