# WidgetsXL

Seção “XL size widgets”: 42 painéis extragrandes — heatmaps com KPIs e regiões, painéis de linhas, radiais e radares, tendência CCR/TTM e oito dashboards completos (receita recorrente, finanças pessoais, carteira, portfólio, plataformas, ocupação, medicamentos, qualidade do ar).

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só a seção `.xl-widget-section` (o script do preview recebe `section = ".xl-widget-section"` em vez de uma lista de widgets). Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Página de análise dedicada, quando um único card deve reunir KPIs, gráfico principal, lista de regiões e interações próprias.
- Reaproveitáveis no TotusTuus: painéis de receita por campus (`sales-*`, `radial-dashboard`, `radar-dashboard`), receita recorrente (`saas-dashboard` → mensalidades) e ocupação (`room-occupancy` → salas da biblioteca).
- Sem equivalente acadêmico (manter só como referência visual): `medicine-distribution`, `air-quality-dashboard`; `personal-finance` e `wallet-dashboard` exigem adaptação ao portal do responsável/cartões.
- Para um gráfico só, use [WidgetsLarge](../WidgetsLarge/README.md) ou os widgets individuais.

## Anatomia

```
article.ttsc-analytics-card.xl-heatmap-card[data-widget]   (+ .xl-virtual-wide / .xl-virtual-dashboard)
  .widget-lazy-placeholder            ← até entrar na viewport
  ┌ Sales Report        Select a cell to inspect the sample value ┐  .xl-heatmap-head (#<id>-selected aria-live)
  │ ✦ Weekly $2,197 ↑19.6% │ ✦ Monthly $8,903 │ ♟ Yearly …       │  .xl-heatmap-kpis
  │ [ heatmap / linhas / radial / radar SVG 760×260 ]             │  .xl-heatmap-plot | .xl-sales-trend-chart | .xl-radial-chart
  │ Los Angeles $20,030 $50,331 $270,120 …                        │  .xl-heatmap-regions
  └───────────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Card | `article.ttsc-analytics-card.xl-heatmap-card[data-widget]` (+ `.xl-virtual-wide`, `.xl-virtual-dashboard`) | sim |
| Placeholder | `.widget-lazy-placeholder[aria-hidden]` (substituído na 1ª renderização; `data-widget-mounted="true"`) | sim |
| Cabeçalho | `header.xl-heatmap-head` + `span#<id>-selected[aria-live="polite"]` | sim (layouts de gráfico) |
| KPIs | `.xl-heatmap-kpis` (`xlKpis()`) | conforme layout |
| Regiões | `.xl-heatmap-regions` (`xlRegions()`) | conforme layout |
| Dashboards | `.pf-dashboard`, `[data-wallet-dashboard]`, `[data-saas-dashboard]`, `[data-platform-dashboard]`, `[data-portfolio-breakdown]`… com controles próprios | layouts de dashboard |

## Variantes

42 tipos de widget, gerados de `xlWidgetDefinitions` em `widgets.js` (mesma ordem do catálogo):

| # | Widget (`data-widget`) | Nome no catálogo | Tipo | Visual | Quando usar |
|---|---|---|---|---|---|
| 1 | `xlHexFlow` | Hex heatmap · revenue flow | `sales-flow` | Heatmap de receita com KPIs semana/mês/ano (heatmap hexagonal em fluxo) | Painel de receita com intensidade diária. |
| 2 | `xlHexFlowTable` | Hex heatmap · regional table | `sales-flow-table` | Heatmap + KPIs + tabela de regiões (heatmap hexagonal em fluxo) | Receita com detalhamento por campus. |
| 3 | `xlHexRadialSplit` | Hex heatmap · regional split | `hex-split` | Resumo · heatmap · lateral mensal/anual (heatmap hexagonal radial) | Resumo executivo com intensidade no centro. |
| 4 | `xlHexRadialDashboard` | Hex heatmap · income dashboard | `hex-dashboard` | Heatmap + KPIs + regiões lado a lado (heatmap hexagonal radial) | Painel de receita compacto em duas colunas. |
| 5 | `xlBasicKpis` | Basic heatmap · KPI overview | `basic-kpis` | Heatmap básico com KPIs (heatmap de grade básico) | Visão geral de intensidade com três totais. |
| 6 | `xlBasicReport` | Basic heatmap · sales report | `basic-report` | Heatmap básico + regiões (heatmap de grade básico) | Relatório de intensidade por campus. |
| 7 | `xlIndicator` | Heatmap indicator · cities | `indicator` | Heatmap indicador por cidade (heatmap indicador (linhas por item)) | Comparar unidades ao longo do período. |
| 8 | `xlGradientIncome` | Gradient heatmap · income | `gradient-income` | Heatmap gradiente de receita (heatmap com gradiente contínuo) | Receita diária com escala contínua. |
| 9 | `xlGradientReport` | Gradient heatmap · sales report | `gradient-report` | Heatmap gradiente + regiões (heatmap com gradiente contínuo) | Relatório com escala contínua e campus. |
| 10 | `xlGradientColumns` | Gradient columns · sales report | `gradient-columns` | Colunas com gradiente (20 pontos) + KPIs | Receita por período com destaque de picos. |
| 11 | `xlInverseRainfall` | Inverse rainfall line chart | `sales-line-dashboard` | Painel de linhas (KPIs + gráfico + regiões) · linha de chuva invertida | Receita mensal por campus com tendência. |
| 12 | `xlSmoothedLineRace` | Smoothed line race | `sales-line-dashboard` | Painel de linhas (KPIs + gráfico + regiões) · corrida de linhas suavizadas | Receita mensal por campus com tendência. |
| 13 | `xlAreaPieceLine` | Area piece line chart | `sales-line-dashboard` | Painel de linhas (KPIs + gráfico + regiões) · área por trechos | Receita mensal por campus com tendência. |
| 14 | `xlSmoothedArea` | Smoothed area chart | `sales-line-dashboard` | Painel de linhas (KPIs + gráfico + regiões) · área suavizada | Receita mensal por campus com tendência. |
| 15 | `xlAreaPieces` | Area pieces | `sales-line-dashboard` | Painel de linhas (KPIs + gráfico + regiões) · peças de área | Receita mensal por campus com tendência. |
| 16 | `xlRainfallLine` | Rainfall line chart | `sales-line-dashboard` | Painel de linhas (KPIs + gráfico + regiões) · linha de chuva | Receita mensal por campus com tendência. |
| 17 | `xlMultipleRadialsSoft` | Multiple radials · soft dashboard | `radial-dashboard` | Painel com radial central, resumo e lateral · múltiplos radiais (suave) | Metas e proporções com contexto de receita. |
| 18 | `xlMultipleRadialsOrange` | Multiple radials · orange dashboard | `radial-dashboard` | Painel com radial central, resumo e lateral · múltiplos radiais (laranja) | Metas e proporções com contexto de receita. |
| 19 | `xlMultipleRadialsTriple` | Multiple radials · triple dashboard | `radial-dashboard` | Painel com radial central, resumo e lateral · múltiplos radiais (triplo) | Metas e proporções com contexto de receita. |
| 20 | `xlStrokedGauge` | Stroked gauge dashboard | `radial-dashboard` | Painel com radial central, resumo e lateral · medidor tracejado | Metas e proporções com contexto de receita. |
| 21 | `xlHalfDoughnut` | Half doughnut dashboard | `radial-dashboard` | Painel com radial central, resumo e lateral · meia rosca | Metas e proporções com contexto de receita. |
| 22 | `xlMultipleRadialsGreen` | Multiple radials · green dashboard | `radial-dashboard` | Painel com radial central, resumo e lateral · múltiplos radiais (verde) | Metas e proporções com contexto de receita. |
| 23 | `xlCircularPoints` | Circular points dashboard | `radial-dashboard` | Painel com radial central, resumo e lateral · pontos circulares mistos | Metas e proporções com contexto de receita. |
| 24 | `xlGradientGauge` | Gradient gauge dashboard | `radial-dashboard` | Painel com radial central, resumo e lateral · medidor com gradiente | Metas e proporções com contexto de receita. |
| 25 | `xlCircularPointsWide` | Circular points · wide dashboard | `radial-dashboard` | Painel com radial central, resumo e lateral · pontos circulares | Metas e proporções com contexto de receita. |
| 26 | `xlBasicRadar` | Basic radar chart | `radar-dashboard` | Painel com radar · radar basic | Comparar campus/itens em várias dimensões. |
| 27 | `xlBasicRadarMetrics` | Basic radar chart · metrics | `radar-dashboard` | Painel com radar · radar basic | Comparar campus/itens em várias dimensões. |
| 28 | `xlMultipleRadar` | Multiple radar chart | `radar-dashboard` | Painel com radar · radar multiple | Comparar campus/itens em várias dimensões. |
| 29 | `xlMultipleRadarMetrics` | Multiple radar chart · metrics | `radar-dashboard` | Painel com radar · radar multiple | Comparar campus/itens em várias dimensões. |
| 30 | `xlSimpleRadar` | Simple radar chart | `radar-dashboard` | Painel com radar · radar simple | Comparar campus/itens em várias dimensões. |
| 31 | `xlSimpleRadarReport` | Simple radar chart · sales report | `radar-dashboard` | Painel com radar · radar simple | Comparar campus/itens em várias dimensões. |
| 32 | `xlCustomizedRadar` | Customized radar chart | `radar-dashboard` | Painel com radar · radar customized | Comparar campus/itens em várias dimensões. |
| 33 | `xlCustomizedRadarMetrics` | Customized radar chart · metrics | `radar-dashboard` | Painel com radar · radar customized | Comparar campus/itens em várias dimensões. |
| 34 | `xlCcrMccrTtm` | #CCRs/MCCRs & TTM trends | `ccr-ttm` | Colunas + linhas de tendência TTM com botão “Details” | Indicador mensal com média móvel de 12 meses. |
| 35 | `xlSaasRevenue` | SaaS subscription revenue dashboard | `saas-dashboard` | Painel de receita recorrente (abas, intervalo, distribuição, atividade) | Receita de assinaturas/mensalidades (MRR). |
| 36 | `xlPersonalFinance` | Personal finance and savings dashboard | `personal-finance` | Painel de finanças pessoais (receita diária, bolhas de despesa, metas) | Portal do responsável: gastos e metas — sem equivalente direto no ERP. |
| 37 | `xlWalletDashboard` | Wallet and total wealth dashboard | `wallet-dashboard` | Carteira: saldo, limite de cartão, lucro e patrimônio | Conta/cartão corporativo (`banks_cards`); exige adaptação. |
| 38 | `xlPortfolioBreakdown` | Portfolio breakdown and health score | `portfolio-breakdown` | Composição de portfólio e índice de saúde (gauge) | Saúde financeira por métrica. |
| 39 | `xlPlatformPerformance` | Platform sales and lead performance | `platform-performance` | Vendas por plataforma e leads (filtros, tags) | CRM: origem de leads × receita. |
| 40 | `xlRoomOccupancy` | Room occupancy trend and room distribution | `room-occupancy` | Ocupação de quartos (tendência + distribuição por tipo) | Ocupação de salas da biblioteca (`lib_room_bookings`). |
| 41 | `xlMedicineDistribution` | Medicine distribution and stock forecast | `medicine-distribution` | Distribuição de medicamentos e previsão de estoque | Sem equivalente acadêmico; manter apenas como referência visual. |
| 42 | `xlAirQuality` | Air quality monitoring and forecast dashboard | `air-quality-dashboard` | Monitoramento de qualidade do ar | Sem equivalente acadêmico; manter apenas como referência visual. |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Placeholder | Antes de entrar na viewport o card só existe montado (ou, no XL, com `.widget-lazy-placeholder`); `renderAll()` registra o `IntersectionObserver` (margem 420px) e renderiza ao aparecer. |
| Ponto selecionado | `state[id].selectedPoint`; a marca recebe `.is-selected` + `aria-pressed="true"` e o valor/legenda do card mudam para o ponto. |
| Filtrado | Botão “Filter” (criado por `addFilterAction`) abre a gaveta; marcas fora do filtro recebem `.widget-filtered-out`. |
| Carregando / vazio / erro | Mesmo padrão dos widgets individuais: `aria-busy` + bloco `.ttsc-analytics-empty[data-widget-state]` no lugar do slot do gráfico (ver JS). |

## API

### Definição de cada widget

| Campo | Tipo | Uso |
|---|---|---|
| `id` | `string` | `data-widget` e chave de `state`. |
| `label` | `string` | Nome e `aria-label` do card. |
| `layout` | `string` | Estrutura do painel (`xlWidgetMarkup` decide por ele). |
| `visual` | `string` | Tipo do heatmap/linha. |
| `chart` | `string` | Gráfico interno (`multiSoft`, `strokedGauge`, `smoothedRace`…). |
| `radar` | `string` | `basic`, `multiple`, `simple`, `customized`. |
| `radarMetrics` | `boolean` | Variante do radar com métricas laterais. |
| `colors` | `string[]` | Paleta. |

Estado inicial: por layout — `{ selectedPoint }` nos gráficos; objetos ricos nos dashboards (ex.: `room-occupancy`: `{ range: 'Weekly', selectedPoint: 4, selectedRoomType: 'Deluxe', showOccupied: true, showAvailable: true }`; `saas-dashboard`: `{ range: 'Week', metric: 'Gross Revenue', distribution: 'plans', … }`).

### Dados

Todos os números são constantes de amostra: `xlKpis()`, `xlRegions()`, `xlRevenueValues`, `ccrTtmRows`, `saasRevenueSeries`, `personalFinance*`, `wallet*`, `portfolioBreakdownMetrics`, `performance*`, `roomOccupancyData`/`roomTypes`, `medicineDistributionData`, `air*`. Cada dashboard tem seu próprio par `…Markup(widget)` + `mount…(card, widget)`; substitua os dados no mesmo par.

### Atributos `data-*`

| Atributo | Onde / efeito |
|---|---|
| `data-heatmap-widget` / `data-heatmap-point` | Células, marcas radiais e eixos de radar selecionáveis (roving tabindex). |
| `data-ccr-details` | Botão “Details” do CCR/TTM (`aria-pressed`). |
| `data-room-point`, `data-room-type`, `data-room-series-toggle` | Ocupação: ponto da tendência, tipo de sala, séries visíveis. |
| `data-saas-tab`, `data-saas-range`, `data-saas-review`, `data-saas-scroll` | Receita recorrente: abas, intervalo, revisão e rolagem da atividade. |
| `data-pf-*`, `data-wallet-*`, `data-performance-*`, `data-portfolio-metric`, `data-medicine-point`, `data-air-*` | Controles internos dos demais dashboards. |
| `data-widget` | No `<article>` gerado: id da definição (chave de `state` e de `renderWidget`). |
| `data-widget-filter` | Botão “Filter” criado pelo JS em cada card. |

### Funções e eventos

| Função / evento | O que faz |
|---|---|
| `mountXLWidgets()` | Cria só os `<article>` com placeholder (o conteúdo é gerado sob demanda). |
| `renderXLWidget(def)` | Na 1ª vez injeta `xlWidgetMarkup(def)`; dashboards são remontados por `…Markup` + `mount…`; gráficos trocam só o SVG. |
| `xlWidgetMarkup(def)` | HTML por `layout`. |
| `xlChartSvg(def, size)` | SVG do gráfico (heatmap, colunas gradiente, linhas, radial, radar, CCR). |
| `renderWidget(id)` | Despacha para o render da seção (entradas geradas com `Object.fromEntries(<defs>.map(…))`). |
| `renderAll()` | Observa todos os cards e renderiza sob demanda. |
| `click` / `keydown` globais | Selecionam o ponto (`selectedPoint`) e re-renderizam só aquele widget. |

### Endpoints

Sem rota pronta. Cada painel adaptado ganha um provider do módulo de origem: receita por campus e MRR (`admin.financial.view`), ocupação de salas (permissão das reservas da biblioteca). URL em `data-endpoint` da seção ou do card.

## Acessibilidade

- Cada marca selecionável é `<g role="button" tabindex="0" aria-pressed>` com `aria-label` “Mês: $valor” e `<title>`; `Enter`/`Espaço` selecionam (tratador global de `keydown`).
- Nos heatmaps só a célula selecionada tem `tabindex="0"` (as demais `-1`): as setas movem a seleção entre células (roving tabindex).
- O rótulo “: Nome” acima de cada card é texto visível (`.…-widget-label`), e o `<article>` tem `aria-label` com o nome do tipo.
- O tooltip comum abre em hover e foco; a gaveta “Filter” (`#widget-filter-drawer`) filtra marcas por texto e faixa e anuncia a contagem em `aria-live`.
- As paletas são fixas por definição (`colors`); confira contraste das marcas finas no tema escuro e nunca use cor como único portador do valor — o valor do ponto selecionado está em texto no card.

## Modelos

### HTML

**1. Na view PHP.** Nenhum partial do chassi gera estas seções; elas são o contêiner vazio de `index.html` que `mountXLWidgets()` preenche. Numa view Plates do módulo:

```php
<?php
$e = static fn ($v) => htmlspecialchars((string) $v, ENT_QUOTES, 'UTF-8');   // helper de domain_page.php
?>
<!-- widgets.js monta os cards dentro de #xl-widgets-grid; data-endpoint é lido pelo provider -->
<section class="xl-widget-section" aria-labelledby="xl-widgets-grid-title" data-endpoint="<?= $e('/financial/widgets/xl' /* provider a criar */) ?>">
  <h2 class="xl-widget-section-title" id="xl-widgets-grid-title"><?= $e($titulo) ?></h2>
  <div class="widgets-grid xl-widgets-grid" id="xl-widgets-grid" aria-label="<?= $e($descricao) ?>"></div>
</section>
```

**2. Contêiner real** (`docs/model/widgets/index.html`):

```html
<section class="xl-widget-section" aria-labelledby="xl-widgets-title">
  <h2 class="xl-widget-section-title" id="xl-widgets-title">XL size widgets</h2>
  <div class="widgets-grid xl-widgets-grid" id="xl-widgets-grid" aria-label="Forty-two extra large dashboard examples"></div>
</section>
```

**3. HTML gerado** (capturado do preview renderizado com Playwright; marcas repetidas resumidas):

```html
<article class="ttsc-analytics-card xl-heatmap-card xl-virtual-dashboard" data-widget="xlRoomOccupancy" aria-label="Room occupancy trend and room distribution" style="position: relative;" data-widget-mounted="true">
  <div class="room-occupancy-dashboard">
    <section class="room-trend-panel panel" aria-label="Room occupancy trend">
      <header class="room-panel-head room-trend-head">
        <div class="room-heading">
          <h3>Room Occupancy Trend</h3>
          <span class="room-sync"><span aria-hidden="true">⟳</span> Last sync 1h ago</span>
        </div>
        <div class="room-trend-actions">
          <div class="room-series-legend">
            <button type="button" data-room-series-toggle="occupied" aria-pressed="true">
              <i class="occupied-dot"></i>
              Occupied
            </button>
            <button type="button" data-room-series-toggle="available" aria-pressed="true">
              <i class="available-dot"></i>
              Available
            </button>
          </div>
          <div class="ttsc-select-wrapper relative w-full select-none" data-ttsc-wired="true">
            <select data-room-range="" aria-label="Trend period" data-ttsc-enhanced="true" style="position: absolute; opacity: 0; pointer-events: none; width: 0px; height: 0px; margin: -1px; z-index: -1;">
              <option selected="">Weekly</option>
              <option>Monthly</option>
              <option>Yearly</option>
            </select>
            <button type="button" class="ttsc-select-trigger w-full flex items-center justify-between text-xs border border-slate-200 bg-white rounded-xl py-2 px-3 text-slate-800 hover:border-slate-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 shadow-xs transition cursor-pointer select-none text-left" aria-haspopup="listbox" aria-expanded="false">
              <div class="flex items-center space-x-2 min-w-0 flex-1 mr-2">
                <i class="fa-light fa-circle-dot text-emerald-600 text-xs shrink-0 ttsc-trigger-icon"></i>
                <span class="ttsc-trigger-label truncate font-medium text-slate-800">Weekly</span>
              </div>
              <i class="fa-light fa-chevron-down text-[10px] text-slate-400 transition-transform duration-200 shrink-0 ml-1.5 ttsc-trigger-chevron"></i>
            </button>
            <div class="ttsc-select-dropdown absolute top-full left-0 mt-1.5 w-full min-w-[220px] bg-white rounded-2xl shadow-2xl border border-slate-200 z-[80] p-2 text-xs flex flex-col hidden" role="listbox">
              <div class="px-2.5 py-1.5 text-[10px] uppercase font-bold tracking-wider text-slate-400 border-b border-slate-100 mb-1 select-none flex items-center justify-between shrink-0">
                <span class="truncate">Opções Disponíveis</span>
                <i class="fa-light fa-list-check text-emerald-600 text-[10px]"></i>
              </div>
              <div class="ttsc-select-options space-y-0.5 overflow-y-auto max-h-60 pr-0.5">
                <button type="button" data-index="0" data-val="Weekly" role="option" aria-selected="true" class="ttsc-select-item w-full flex items-center justify-between px-2.5 py-2 rounded-xl text-xs transition text-left cursor-pointer select-none is-selected bg-emerald-50 text-emerald-700 font-semibold border border-emerald-200">
                  <div class="flex items-center space-x-2 min-w-0 flex-1 mr-2">
                    <i class="fa-light fa-circle-dot text-emerald-600 text-xs shrink-0"></i>
                    <span class="truncate">Weekly</span>
                  </div>
                  <i class="fa-light fa-check text-emerald-600 text-xs shrink-0"></i>
                </button>
                <button type="button" data-index="1" data-val="Monthly" role="option" aria-selected="false" class="ttsc-select-item w-full flex items-center justify-between px-2.5 py-2 rounded-xl text-xs transition text-left cursor-pointer select-none text-slate-600 hover:bg-slate-50 transition border border-transparent">
                  <div class="flex items-center space-x-2 min-w-0 flex-1 mr-2">
                    <i class="fa-light fa-calendar-day text-slate-400 text-xs shrink-0"></i>
                    <span class="truncate">Monthly</span>
                  </div>
                </button>
                <button type="button" data-index="2" data-val="Yearly" role="option" aria-selected="false" class="ttsc-select-item w-full flex items-center justify-between px-2.5 py-2 rounded-xl text-xs transition text-left cursor-pointer select-none text-slate-600 hover:bg-slate-50 transition border border-transparent">
                  <div class="flex items-center space-x-2 min-w-0 flex-1 mr-2">
                    <i class="fa-light fa-circle-dot text-slate-400 text-xs shrink-0"></i>
                    <span class="truncate">Yearly</span>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>
      <div class="room-trend-plot">
        <svg class="room-trend-svg" viewBox="0 0 720 248" role="group" aria-label="Weekly room occupancy trend chart">
          <defs>
            <lineargradient id="xlRoomOccupancy-occupied-fill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#8bc85e" stop-opacity=".27"></stop>
              <stop offset="1" stop-color="#8bc85e" stop-opacity=".02"></stop>
            </lineargradient>
            <lineargradient id="xlRoomOccupancy-available-fill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#f4cf44" stop-opacity=".25"></stop>
              <stop offset="1" stop-color="#f4cf44" stop-opacity=".02"></stop>
            </lineargradient>
          </defs>
          <g>
            <line class="room-grid-line" x1="38" x2="702" y1="196" y2="196"></line>
            <text class="room-axis-label" x="28" y="200" text-anchor="end">0</text>
          </g>
          <g>
            <line class="room-grid-line" x1="38" x2="702" y1="156.88888888888889" y2="156.88888888888889"></line>
            <text class="room-axis-label" x="28" y="160.88888888888889" text-anchor="end">20</text>
          </g>
          <!-- … +16 elemento(s) iguais gerados pelo JS -->
        </svg>
      </div>
      <span class="room-occupancy-live" aria-live="polite">15 Fri · 61 occupied and 47 available</span>
    </section>
    <section class="room-distribution panel" aria-label="Room distribution">
      <header class="room-panel-head">
        <h3>Room Distribution</h3>
        <div class="ttsc-select-wrapper relative w-full select-none" data-ttsc-wired="true">
          <select data-room-range="" aria-label="Distribution period" data-ttsc-enhanced="true" style="position: absolute; opacity: 0; pointer-events: none; width: 0px; height: 0px; margin: -1px; z-index: -1;">
            <option selected="">Weekly</option>
            <option>Monthly</option>
            <option>Yearly</option>
          </select>
          <button type="button" class="ttsc-select-trigger w-full flex items-center justify-between text-xs border border-slate-200 bg-white rounded-xl py-2 px-3 text-slate-800 hover:border-slate-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 shadow-xs transition cursor-pointer select-none text-left" aria-haspopup="listbox" aria-expanded="false">
            <div class="flex items-center space-x-2 min-w-0 flex-1 mr-2">
              <i class="fa-light fa-circle-dot text-emerald-600 text-xs shrink-0 ttsc-trigger-icon"></i>
              <span class="ttsc-trigger-label truncate font-medium text-slate-800">Weekly</span>
            </div>
            <i class="fa-light fa-chevron-down text-[10px] text-slate-400 transition-transform duration-200 shrink-0 ml-1.5 ttsc-trigger-chevron"></i>
          </button>
          <div class="ttsc-select-dropdown absolute top-full left-0 mt-1.5 w-full min-w-[220px] bg-white rounded-2xl shadow-2xl border border-slate-200 z-[80] p-2 text-xs flex flex-col hidden" role="listbox">
            <div class="px-2.5 py-1.5 text-[10px] uppercase font-bold tracking-wider text-slate-400 border-b border-slate-100 mb-1 select-none flex items-center justify-between shrink-0">
              <span class="truncate">Opções Disponíveis</span>
              <i class="fa-light fa-list-check text-emerald-600 text-[10px]"></i>
            </div>
            <div class="ttsc-select-options space-y-0.5 overflow-y-auto max-h-60 pr-0.5">
              <button type="button" data-index="0" data-val="Weekly" role="option" aria-selected="true" class="ttsc-select-item w-full flex items-center justify-between px-2.5 py-2 rounded-xl text-xs transition text-left cursor-pointer select-none is-selected bg-emerald-50 text-emerald-700 font-semibold border border-emerald-200">
                <div class="flex items-center space-x-2 min-w-0 flex-1 mr-2">
                  <i class="fa-light fa-circle-dot text-emerald-600 text-xs shrink-0"></i>
                  <span class="truncate">Weekly</span>
                </div>
                <i class="fa-light fa-check text-emerald-600 text-xs shrink-0"></i>
              </button>
              <button type="button" data-index="1" data-val="Monthly" role="option" aria-selected="false" class="ttsc-select-item w-full flex items-center justify-between px-2.5 py-2 rounded-xl text-xs transition text-left cursor-pointer select-none text-slate-600 hover:bg-slate-50 transition border border-transparent">
                <div class="flex items-center space-x-2 min-w-0 flex-1 mr-2">
                  <i class="fa-light fa-calendar-day text-slate-400 text-xs shrink-0"></i>
                  <span class="truncate">Monthly</span>
                </div>
              </button>
              <button type="button" data-index="2" data-val="Yearly" role="option" aria-selected="false" class="ttsc-select-item w-full flex items-center justify-between px-2.5 py-2 rounded-xl text-xs transition text-left cursor-pointer select-none text-slate-600 hover:bg-slate-50 transition border border-transparent">
                <div class="flex items-center space-x-2 min-w-0 flex-1 mr-2">
                  <i class="fa-light fa-circle-dot text-slate-400 text-xs shrink-0"></i>
                  <span class="truncate">Yearly</span>
                </div>
              </button>
            </div>
          </div>
        </div>
      </header>
      <div class="room-donut-wrap">
        <svg class="room-donut-svg" viewBox="0 0 220 220" role="group" aria-label="Distribution of 102 rooms">
          <path class="room-distribution-segment is-selected" data-room-type="Deluxe" d="M 113.25433547820326 17.056956685315555 A 93 93 0 0 1 161.69509910553435 187.3085812084854 L 151.68959605285028 172.34563000684307 A 75 75 0 0 0 112.62446409532521 35.04593281073835 Z" style="--room-color:#83bf4d" tabindex="0" role="button" aria-pressed="true" aria-label="Deluxe: 42 rooms"></path>
          <path class="room-distribution-segment " data-room-type="Standard" d="M 156.16131552757187 190.73495493752353 A 93 93 0 0 1 17.153163126981937 104.66475092660393 L 35.123518650791894 105.6973797795193 A 75 75 0 0 0 147.22686736094505 175.1088346270351 Z" style="--room-color:#b4ef70" tabindex="0" role="button" aria-pressed="false" aria-label="Standard: 36 rooms"></path>
          <path class="room-distribution-segment " data-room-type="Suite" d="M 17.753707518416007 98.18384481305104 A 93 93 0 0 1 106.7456645217967 17.056956685315555 L 107.37553590467476 35.04593281073835 A 75 75 0 0 0 35.60782864388388 100.4708425911702 Z" style="--room-color:#f1c833" tabindex="0" role="button" aria-pressed="false" aria-label="Suite: 24 rooms"></path>
          <!-- … +2 elemento(s) iguais gerados pelo JS -->
        </svg>
      </div>
      <div class="room-type-legend">
        <button type="button" class="room-type-button is-selected" data-room-type="Deluxe" aria-pressed="true">
          <i style="--room-color:#83bf4d"></i>
          Deluxe
          <span>42</span>
        </button>
        <button type="button" class="room-type-button " data-room-type="Standard" aria-pressed="false">
          <i style="--room-color:#b4ef70"></i>
          Standard
          <span>36</span>
        </button>
        <button type="button" class="room-type-button " data-room-type="Suite" aria-pressed="false">
          <i style="--room-color:#f1c833"></i>
          Suite
          <span>24</span>
        </button>
      </div>
    </section>
  </div>
  <button class="widget-filter-trigger" type="button" data-widget-filter="xlRoomOccupancy" aria-label="Filter Room Occupancy Trend" aria-expanded="false">
    <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
    <span>Filter</span>
    <b hidden=""></b>
  </button>
</article>
```

### CSS

Arquivo: `docs/model/widgets/widgets.css` (sobre `ttsc.analytics-panels.css`). Tema escuro por `html[data-theme="dark"]` (variáveis `--w-*`) e `html.dark` no app, sincronizados por `TTSCModelKit.syncTheme()`. Regras reais da seção:

```css
.room-occupancy-dashboard { display: grid; min-width: 0; grid-template-columns: minmax(0, 2fr) minmax(285px, .95fr); align-items: stretch; gap: 16px; color: var(--w-text); }
.room-occupancy-dashboard .panel { min-width: 0; overflow: hidden; border: 1px solid var(--w-border); border-radius: 18px; background: var(--w-surface); box-shadow: 0 2px 7px rgb(29 40 60 / .035); }
.room-trend-panel { display: flex; min-height: 340px; flex-direction: column; padding: 16px 18px 11px; }
.room-panel-head { display: flex; min-width: 0; align-items: center; justify-content: space-between; gap: 14px; }
.room-panel-head h3 { margin: 0; color: var(--w-text); font-size: 16px; font-weight: 600; letter-spacing: -.02em; white-space: nowrap; }
.room-heading, .room-trend-actions, .room-series-legend { display: flex; min-width: 0; align-items: center; gap: 14px; }
.room-sync { display: inline-flex; align-items: center; gap: 5px; color: var(--w-muted); font-size: 10px; white-space: nowrap; }
.room-sync span { font-size: 15px; }
.room-trend-actions { gap: 18px; }
.room-series-legend { gap: 13px; }
.room-series-legend button { display: inline-flex; align-items: center; gap: 6px; padding: 4px 0; border: 0; background: transparent; color: var(--w-secondary); cursor: pointer; font: 550 12px var(--w-font); white-space: nowrap; }
.room-series-legend button[aria-pressed="false"] { opacity: .45; }
.room-series-legend i, .room-type-button i { width: 9px; height: 9px; flex: 0 0 auto; border-radius: 50%; }
.room-series-legend .occupied-dot, .occupied-dot { background: #83bf4d; }
.room-series-legend .available-dot, .available-dot { background: #f1c833; }
.room-panel-head select { min-height: 32px; padding: 0 28px 0 11px; border: 1px solid var(--w-border); border-radius: 9px; background: var(--w-surface); color: var(--w-text); cursor: pointer; font: 500 11px var(--w-font); }
.room-trend-plot { min-width: 0; flex: 1; margin-top: 7px; }
.room-trend-svg { display: block; width: 100%; height: 100%; min-height: 260px; overflow: visible; }
.room-grid-line { stroke: var(--w-grid); stroke-width: 1; }
.room-axis-label, .room-date-label { fill: var(--w-muted); font: 11px var(--w-font); }
.room-date-label { fill: var(--w-text); font-size: 13px; font-weight: 550; }
.room-date-label .room-weekday { fill: var(--w-muted); font-size: 12px; font-weight: 400; }
.room-crosshair { stroke: #25272b; stroke-width: 1.4; }
.room-selected-guide { stroke: #303238; stroke-width: 1.25; stroke-dasharray: 4 4; }
```

Customização legítima:

```css
/* Painéis XL ocupando a largura toda numa página de análise */
.widgets-grid.xl-widgets-grid { grid-template-columns: 1fr; }
.xl-heatmap-head span { color: var(--ttsc-text-muted); }
.xl-heatmap-kpis em { color: var(--ttsc-accent-text); font-style: normal; }
```

### JS

Definições, montagem e render reais em `widgets.js`:

```js
const xlWidgetDefinitions = [
  { id: 'xlHexFlow', label: 'Hex heatmap · revenue flow', visual: 'hexFlow', layout: 'sales-flow' },
  { id: 'xlHexFlowTable', label: 'Hex heatmap · regional table', visual: 'hexFlow', layout: 'sales-flow-table' },
  { id: 'xlHexRadialSplit', label: 'Hex heatmap · regional split', visual: 'hexRadial', layout: 'hex-split' },
  { id: 'xlHexRadialDashboard', label: 'Hex heatmap · income dashboard', visual: 'hexRadial', layout: 'hex-dashboard' },
  { id: 'xlBasicKpis', label: 'Basic heatmap · KPI overview', visual: 'basic', layout: 'basic-kpis' },
  { id: 'xlBasicReport', label: 'Basic heatmap · sales report', visual: 'basic', layout: 'basic-report' },
  { id: 'xlIndicator', label: 'Heatmap indicator · cities', visual: 'indicator', layout: 'indicator' },
  { id: 'xlGradientIncome', label: 'Gradient heatmap · income', visual: 'gradient', layout: 'gradient-income' },
  { id: 'xlGradientReport', label: 'Gradient heatmap · sales report', visual: 'gradient', layout: 'gradient-report' },
  { id: 'xlGradientColumns', label: 'Gradient columns · sales report', visual: 'gradient', layout: 'gradient-columns' },
  { id: 'xlInverseRainfall', label: 'Inverse rainfall line chart', visual: 'line', layout: 'sales-line-dashboard', chart: 'inverseRainfall', colors: ['#1689e8', '#7046df', '#c026d3', '#f97316', '#f59e0b', '#06b6d4', '#14d6b1'] },
  { id: 'xlSmoothedLineRace', label: 'Smoothed line race', visual: 'line', layout: 'sales-line-dashboard', chart: 'smoothedRace', colors: ['#22c55e', '#1689e8', '#7046df', '#fb477c', '#f97316', '#f59e0b', '#c026d3'] },
  { id: 'xlAreaPieceLine', label: 'Area piece line chart', visual: 'line', layout: 'sales-line-dashboard', chart: 'areaPieceLine', colors: ['#22c55e', '#cbd5e1'] },
  { id: 'xlSmoothedArea', label: 'Smoothed area chart', visual: 'line', layout: 'sales-line-dashboard', chart: 'smoothedArea', colors: ['#22c55e'] },
  { id: 'xlAreaPieces', label: 'Area pieces', visual: 'line', layout: 'sales-line-dashboard', chart: 'areaPieces', colors: ['#a855f7'] },
  { id: 'xlRainfallLine', label: 'Rainfall line chart', visual: 'line', layout: 'sales-line-dashboard', chart: 'rainfallLine', colors: ['#f59e0b', '#f97316', '#ec4899', '#7046df', '#06b6d4', '#14d6b1'] },
  { id: 'xlMultipleRadialsSoft', label: 'Multiple radials · soft dashboard', layout: 'radial-dashboard', chart: 'multiSoft', colors: ['#7653f9', '#c4b5fd', '#22c55e'] },
  { id: 'xlMultipleRadialsOrange', label: 'Multiple radials · orange dashboard', layout: 'radial-dashboard', chart: 'multiOrange', colors: ['#7653f9', '#f97316', '#fbbf24'] },
  { id: 'xlMultipleRadialsTriple', label: 'Multiple radials · triple dashboard', layout: 'radial-dashboard', chart: 'multiTriple', colors: ['#7653f9', '#f97316', '#22c55e', '#fb477c'] },
  { id: 'xlStrokedGauge', label: 'Stroked gauge dashboard', layout: 'radial-dashboard', chart: 'strokedGauge', colors: ['#f97316', '#cbd5e1'] },
  { id: 'xlHalfDoughnut', label: 'Half doughnut dashboard', layout: 'radial-dashboard', chart: 'half', colors: ['#8b5cf6', '#f97316'] },
  { id: 'xlMultipleRadialsGreen', label: 'Multiple radials · green dashboard', layout: 'radial-dashboard', chart: 'multiGreen', colors: ['#7653f9', '#f97316', '#22c55e'] },
  { id: 'xlCircularPoints', label: 'Circular points dashboard', layout: 'radial-dashboard', chart: 'pointsMixed', colors: ['#8b5cf6', '#fb923c', '#fed7aa'] },
  { id: 'xlGradientGauge', label: 'Gradient gauge dashboard', layout: 'radial-dashboard', chart: 'gradientGauge', colors: ['#14d6b1', '#a3e635', '#facc15', '#fb7185', '#7c3aed'] },
  { id: 'xlCircularPointsWide', label: 'Circular points · wide dashboard', layout: 'radial-dashboard', chart: 'points', colors: ['#8b5cf6', '#c4b5fd'] },
  { id: 'xlBasicRadar', label: 'Basic radar chart', layout: 'radar-dashboard', radar: 'basic', colors: ['#7653f9'] },
  { id: 'xlBasicRadarMetrics', label: 'Basic radar chart · metrics', layout: 'radar-dashboard', radar: 'basic', colors: ['#7653f9'], radarMetrics: true },
  { id: 'xlMultipleRadar', label: 'Multiple radar chart', layout: 'radar-dashboard', radar: 'multiple', colors: ['#7653f9', '#f97316'] },
  { id: 'xlMultipleRadarMetrics', label: 'Multiple radar chart · metrics', layout: 'radar-dashboard', radar: 'multiple', colors: ['#7653f9', '#f97316'], radarMetrics: true },
  { id: 'xlSimpleRadar', label: 'Simple radar chart', layout: 'radar-dashboard', radar: 'simple', colors: ['#7653f9', '#f97316'], radarMetrics: true },
  { id: 'xlSimpleRadarReport', label: 'Simple radar chart · sales report', layout: 'radar-dashboard', radar: 'simple', colors: ['#7653f9', '#f97316'] },
  { id: 'xlCustomizedRadar', label: 'Customized radar chart', layout: 'radar-dashboard', radar: 'customized', colors: ['#7653f9'] },
  { id: 'xlCustomizedRadarMetrics', label: 'Customized radar chart · metrics', layout: 'radar-dashboard', radar: 'customized', colors: ['#7653f9'], radarMetrics: true },
  { id: 'xlCcrMccrTtm', label: '#CCRs/MCCRs & TTM trends', layout: 'ccr-ttm' },
  { id: 'xlSaasRevenue', label: 'SaaS subscription revenue dashboard', layout: 'saas-dashboard' },
  { id: 'xlPersonalFinance', label: 'Personal finance and savings dashboard', layout: 'personal-finance' },
  { id: 'xlWalletDashboard', label: 'Wallet and total wealth dashboard', layout: 'wallet-dashboard' },
  { id: 'xlPortfolioBreakdown', label: 'Portfolio breakdown and health score', layout: 'portfolio-breakdown' },
  { id: 'xlPlatformPerformance', label: 'Platform sales and lead performance', layout: 'platform-performance' },
  { id: 'xlRoomOccupancy', label: 'Room occupancy trend and room distribution', layout: 'room-occupancy' },
  { id: 'xlMedicineDistribution', label: 'Medicine distribution and stock forecast', layout: 'medicine-distribution' },
  { id: 'xlAirQuality', label: 'Air quality monitoring and forecast dashboard', layout: 'air-quality-dashboard' }
];
```

```js
function mountXLWidgets() {
  const grid = byId('xl-widgets-grid');
  if (!grid) return;
  const dashboardLayouts = new Set(['saas-dashboard', 'personal-finance', 'wallet-dashboard', 'platform-performance', 'room-occupancy', 'air-quality-dashboard']);
  grid.innerHTML = xlWidgetDefinitions.map(widget => {
    const wide = ['gradient-columns', 'ccr-ttm', 'medicine-distribution'].includes(widget.layout);
    const dashboard = dashboardLayouts.has(widget.layout);
    return `<article class="ttsc-analytics-card xl-heatmap-card${wide ? ' xl-virtual-wide' : ''}${dashboard ? ' xl-virtual-dashboard' : ''}${widget.layout === 'medicine-distribution' ? ' xl-virtual-dashboard xl-virtual-wide' : ''}" data-widget="${widget.id}" aria-label="${widget.label}"><div class="widget-lazy-placeholder" aria-hidden="true"></div></article>`;
  }).join('');
}
```

```js
function xlKpis() {
  return `<div class="xl-heatmap-kpis"><div><small>✦ Weekly</small><strong>$2,197</strong><em>↑19.6%</em><span>Compared to $1,340 last week</span></div><div><small>✦ Monthly</small><strong>$8,903</strong><em>↑1.9%</em><span>Compared to $5,441 last month</span></div><div><small>♟ Yearly</small><strong>$98,134</strong><em>↑22%</em><span>Compared to $76,330 last year</span></div></div>`;
}
```

```js
function xlRegions() {
  return `<div class="xl-heatmap-regions"><span>Los Angeles <b>$20,030</b><b>$50,331</b><b>$270,120</b></span><span>New York <b>$18,782</b><b>$40,795</b><b>$210,650</b></span><span>Canada <b>$14,221</b><b>$30,123</b><b>$200,080</b></span></div>`;
}
```

```js
function roomOccupancyMarkup(widget) {
  const s = state[widget.id];
  const series = roomOccupancyData[s.range];
  return `<div class="room-occupancy-dashboard"><section class="room-trend-panel panel" aria-label="Room occupancy trend"><header class="room-panel-head room-trend-head"><div class="room-heading"><h3>Room Occupancy Trend</h3><span class="room-sync"><span aria-hidden="true">⟳</span> Last sync 1h ago</span></div><div class="room-trend-actions"><div class="room-series-legend"><button type="button" data-room-series-toggle="occupied" aria-pressed="${s.showOccupied}"><i class="occupied-dot"></i>Occupied</button><button type="button" data-room-series-toggle="available" aria-pressed="${s.showAvailable}"><i class="available-dot"></i>Available</button></div><select data-room-range aria-label="Trend period">${['Weekly', 'Monthly', 'Yearly'].map(range => `<option ${s.range === range ? 'selected' : ''}>${range}</option>`).join('')}</select></div></header><div class="room-trend-plot">${roomTrendSvg(widget)}</div><span class="room-occupancy-live" aria-live="polite">${series.labels[s.selectedPoint].join(' ')} · ${series.occupied[s.selectedPoint]} occupied and ${series.available[s.selectedPoint]} available</span></section>${roomDistributionMarkup(widget)}</div>`;
}
```

Dados de amostra do painel de ocupação (o mais aproveitável no TotusTuus):

```js
const roomTypes = [
  { name: 'Deluxe', count: 42, color: '#83bf4d' },
  { name: 'Standard', count: 36, color: '#b4ef70' },
  { name: 'Suite', count: 24, color: '#f1c833' }
];
```

Trocando os valores de amostra pelo endpoint (dentro do IIFE da cópia de produção):

```js
// Provider do módulo — trecho a colocar DENTRO do IIFE da cópia de produção de widgets.js
// (lá `data`, `state` e `renderWidget` são visíveis; o arquivo de referência não exporta nada).
function widgetCard(widget) { return document.querySelector(`[data-widget="${CSS.escape(widget)}"]`); }
function widgetState(card, kind, title, detail) {
  card.querySelector('[data-widget-state]')?.remove();
  card.querySelectorAll('.ttsc-analytics-plot, [data-widget-body]').forEach(node => { node.hidden = kind !== 'ready'; });
  if (kind === 'ready') return;
  const box = document.createElement('div');
  box.className = 'ttsc-analytics-empty';            // classe real de ttsc.analytics-panels.css (tem variante html.dark)
  box.dataset.widgetState = kind;                     // 'loading' | 'empty' | 'error'
  box.setAttribute('role', kind === 'error' ? 'alert' : 'status');
  box.innerHTML = `<strong></strong><span${kind === 'error' ? ' class="ttsc-analytics-error"' : ''}></span>`;
  box.querySelector('strong').textContent = title;
  box.querySelector('span').textContent = detail;
  const foot = card.querySelector('.ttsc-analytics-foot');
  if (foot) foot.before(box); else card.append(box);
}
async function loadWidget(widget, apply) {
  const card = widgetCard(widget);
  const endpoint = card?.dataset.endpoint;           // a view PHP grava a URL autorizada no card
  if (!endpoint) return;
  card.setAttribute('aria-busy', 'true');
  widgetState(card, 'loading', 'Carregando…', 'Buscando os dados do período.');
  try {
    const response = await fetch(endpoint, { credentials: 'same-origin', headers: { Accept: 'application/json' } });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    const rows = payload.records ?? payload.rows ?? [];   // DomainCrudController::index → records
    if (!rows.length || apply(rows, payload) === false) {
      widgetState(card, 'empty', 'Sem dados no período', 'Nenhum lançamento corresponde aos filtros deste widget.');
      return;
    }
    widgetState(card, 'ready');
    renderWidget(widget);
  } catch (error) {
    console.error(`[widgets] ${widget}`, error);
    widgetState(card, 'error', 'Não foi possível carregar', 'Tente novamente; se persistir, verifique a permissão da página.');
  } finally {
    card.removeAttribute('aria-busy');
  }
}

// Em produção, cada definição ganha `values` (série real) e os geradores de valor passam a lê-la:
//   compactPoint(): const value = widget.values?.[index] ?? compactWidgetValues[index % compactWidgetValues.length];
//   verticalValue()/mediumValue(): return widget.values?.[index] ?? Math.round(widget.value * ratios[index % ratios.length]);
//   largeValue(index) → largeValue(index, widget) com widget.values?.[index]
async function loadSection(sectionSelector, definitions, mapRow) {
  const section = document.querySelector(sectionSelector);
  const endpoint = section?.dataset.endpoint;
  if (!endpoint) return;
  section.setAttribute('aria-busy', 'true');
  try {
    const response = await fetch(endpoint, { credentials: 'same-origin', headers: { Accept: 'application/json' } });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    definitions.forEach(definition => {
      const series = mapRow(definition, payload);              // devolve number[] ou null
      const card = widgetCard(definition.id);
      if (!series || !series.length) { widgetState(card, 'empty', 'Sem dados', 'Nenhum registro no período.'); return; }
      definition.values = series;
      definition.value = series.at(-1);
      widgetState(card, 'ready');
      renderWidget(definition.id);
    });
  } catch (error) {
    definitions.forEach(definition => widgetState(widgetCard(definition.id), 'error', 'Não foi possível carregar', 'Tente novamente.'));
  } finally {
    section.removeAttribute('aria-busy');
  }
}

// Ocupação de salas: payload = { rows: [{ day: '2026-10-19', room_type, occupied_hours, available_hours }] }
// roomOccupancyData e roomTypes são `const`, mas objetos/arrays mutáveis: preencha-os antes de renderWidget().
const ROOM_COLORS = ['#83bf4d', '#b4ef70', '#f1c833'];
loadWidget('xlRoomOccupancy', rows => {
  const days = [...new Set(rows.map(row => row.day))].sort();
  const sumBy = (day, key) => rows.filter(row => row.day === day).reduce((t, row) => t + (Number(row[key]) || 0), 0);
  Object.assign(roomOccupancyData.Weekly, {
    labels: days.map(day => [day.slice(8, 10), new Intl.DateTimeFormat('pt-BR', { weekday: 'short' }).format(new Date(`${day}T00:00:00`)).replace('.', '')]),
    occupied: days.map(day => sumBy(day, 'occupied_hours')),
    available: days.map(day => sumBy(day, 'available_hours') - sumBy(day, 'occupied_hours')),
  });
  const types = [...new Set(rows.map(row => row.room_type))];
  roomTypes.splice(0, roomTypes.length, ...types.map((name, index) => ({
    name, count: rows.filter(row => row.room_type === name).reduce((t, row) => t + (Number(row.occupied_hours) || 0), 0), color: ROOM_COLORS[index % 3],
  })));
  state.xlRoomOccupancy.selectedRoomType = roomTypes[0]?.name;
  return days.length > 0;
});
```

CSV: `downloadCsv()` não tem ramo para os widgets de seção (o menu “Download CSV” não existe nesses cards). Para exportar, use a exportação da página de origem dos dados (`GET /api/v1/domain/records{rota}/export?format=csv|xlsx|pdf|json|xml|sql`).

### SQL

Três agregados para os painéis reaproveitáveis: ocupação diária de salas por tipo (`lib_room_bookings` + `lib_rooms`, 12 h de funcionamento por sala), receita recorrente por plano com novas e canceladas no mês (`billing_subscriptions`) e recebido por campus e mês (`financial_receivables` + `financial_cost_centers`) para os painéis de linhas/radiais/radar/heatmaps. Testados no MariaDB local.

```sql
-- (a) Ocupação de salas (xlRoomOccupancy): horas reservadas × disponíveis por dia e tipo de sala, semana corrente
SELECT b.booking_date                                  AS day,
       r.room_type,
       ROUND(SUM(b.duration_minutes) / 60, 1)           AS occupied_hours,
       COUNT(DISTINCT r.id) * 12                        AS available_hours      -- 12 h de funcionamento por sala
  FROM lib_room_bookings b
  JOIN lib_rooms r ON r.id = b.room_id AND r.deleted_at IS NULL AND r.is_active = 1
 WHERE b.deleted_at IS NULL AND b.status <> 'cancelled'
   AND b.booking_date BETWEEN CURDATE() - INTERVAL WEEKDAY(CURDATE()) DAY AND CURDATE() + INTERVAL (6 - WEEKDAY(CURDATE())) DAY
 GROUP BY b.booking_date, r.room_type
 ORDER BY day, r.room_type;

-- (b) Receita recorrente (xlSaasRevenue): MRR por plano e novas/canceladas no mês
SELECT s.plan_id,
       SUM(CASE WHEN s.status = 'active' THEN s.negotiated_amount ELSE 0 END)                                  AS mrr,
       SUM(s.starts_at >= DATE_FORMAT(CURDATE(), '%Y-%m-01'))                                                   AS new_this_month,
       SUM(s.cancelled_at >= DATE_FORMAT(CURDATE(), '%Y-%m-01'))                                                AS cancelled_this_month
  FROM billing_subscriptions s
 WHERE s.deleted_at IS NULL
 GROUP BY s.plan_id
 ORDER BY mrr DESC;

-- (c) Painéis “sales report” (linhas, radiais, radar, heatmaps XL): recebido por campus e mês
SELECT cc.name AS region, DATE_FORMAT(r.payment_date, '%Y-%m') AS month, SUM(r.amount_paid) AS received
  FROM financial_receivables r
  JOIN financial_cost_centers cc ON cc.id = r.cost_center_id AND cc.deleted_at IS NULL
 WHERE r.deleted_at IS NULL AND r.status <> 'cancelled'
   AND r.payment_date >= DATE_FORMAT(CURDATE() - INTERVAL 11 MONTH, '%Y-%m-01')
 GROUP BY cc.name, DATE_FORMAT(r.payment_date, '%Y-%m')
 ORDER BY region, month;
```

As horas disponíveis (12 h × salas ativas) são uma premissa: se a biblioteca tiver horário cadastrado, troque pela soma real. Os painéis de medicamentos e qualidade do ar não têm tabela correspondente no esquema do TotusTuus.

## Faça / Não faça

- **Faça:** montar só os painéis que têm fonte real no módulo;
- **Faça:** manter a renderização preguiçosa (placeholder + `IntersectionObserver`) — são cards pesados.
- **Não faça:** publicar `medicine-distribution`/`air-quality-dashboard` com dados inventados;
- **Não faça:** renderizar todos os 42 painéis numa mesma página de produto.
