# WidgetsLarge

Seção “Large size widgets”: 51 cards grandes — barras e chuvas diárias, heatmaps, quatro calendários, linhas e corridas, 15 radiais, perspectivas 3D e quatro gráficos de categoria (barras por divisão, rosca, pizza, radar).

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só a seção `.large-widget-section` (o script do preview recebe `section = ".large-widget-section"` em vez de uma lista de widgets). Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Um gráfico principal por card, com 12–31 pontos, em painéis de análise (receita diária, presença por dia, composição por categoria).
- Calendários para atividade diária de um mês (eventos, aulas, atendimentos); radiais para metas e proporções; radar para comparar até 3 itens em 5 dimensões.
- Para painéis compostos com KPIs e tabelas use [WidgetsXL](../WidgetsXL/README.md); evite as variações 3D em telas operacionais (são para apresentação).

## Anatomia

```
article.large-widget-card[data-widget]              (calendário: + .large-calendar-card)
  ┌ Sales Report                                   ┐  .large-widget-head
  │ $8,097                                          │  #<id>-value
  │ [ gráfico SVG 300×172 | grade de calendário ]   │  #<id>-chart  /  .large-calendar-grid
  └─────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Card | `article…large-widget-card[data-widget]` | sim |
| Cabeçalho | `header.large-widget-head` (título por tipo: “Sales Report”, “Income”, “Sales by division”…) | sim |
| Valor | `#<id>-value` (+ `#<id>-context` nos calendários) | sim |
| Gráfico | `#<id>-chart` > `svg` (removido nos calendários) | sim |
| Calendário | `.large-calendar-grid[role="group"]` > `button.large-calendar-day.<kind>[data-large-point][aria-pressed]` | calendários |

## Variantes

51 tipos de widget, gerados de `largeWidgetDefinitions` em `widgets.js` (mesma ordem do catálogo):

| # | Widget (`data-widget`) | Nome no catálogo | Tipo | Visual | Quando usar |
|---|---|---|---|---|---|
| 1 | `largeBasicBars` | Basic bar | `basic` | Colunas básicas (12 pontos) | Série mensal de um indicador. |
| 2 | `largeStackedColumns` | Stacked columns | `stacked` | Colunas empilhadas | Composição de duas partes por mês. |
| 3 | `largeRainfall` | Rainfall | `rainfall` | Colunas “chuva” finas e coloridas por faixa | Série densa diária em pouco espaço. |
| 4 | `largeDoubleRainfall` | Double rainfall | `doubleRainfall` | Chuva dupla (duas séries espelhadas) | Entradas × saídas por dia. |
| 5 | `largeDetailedBars` | Detailed bar chart | `detailed` | Barras detalhadas diárias (31) | Indicador diário do mês. |
| 6 | `largeDetailedOrange` | Detailed bar chart | `detailedOrange` | Barras detalhadas com trilha | Indicador diário contra a capacidade. |
| 7 | `largeStackedAverage` | Stacked bar with average line | `stackedAverage` | Empilhadas com linha de média | Composição por período e média de referência. |
| 8 | `largeMultiBars` | Multiple bars chart | `multiBars` | Múltiplas barras por dia | Três séries diárias lado a lado. |
| 9 | `largeBubbles` | Bubble bar chart | `bubbles` | Barras em bolhas (pontos empilhados) | Contagens pequenas (eventos, ocorrências) por período. |
| 10 | `largeDoubleBubbles` | Double bubble bar chart | `doubleBubbles` | Bolhas duplas | Duas contagens pequenas por período. |
| 11 | `largeHexFlow` | Hex heatmap | `heatmap` | Heatmap hexagonal em fluxo | Intensidade por período × faixa (semana × dia). |
| 12 | `largeHexRadial` | Hex heatmap | `heatmap` | Heatmap hexagonal radial | Intensidade concentrada em torno de um centro (picos). |
| 13 | `largeBasicHeatmap` | Basic heatmap | `heatmap` | Heatmap de grade básico | Matriz semana × dia da semana (presença, atendimentos). |
| 14 | `largeHeatmapIndicator` | Heatmap indicator | `heatmap` | Heatmap indicador (linhas por item) | Intensidade por item (cidade, campus) ao longo do tempo. |
| 15 | `largeGradientHeatmap` | Gradient heatmap | `heatmap` | Heatmap com gradiente contínuo | Matriz com escala contínua de valores. |
| 16 | `largeCalendarSimple` | Simple calendar | `calendarSimple` | Calendário mensal simples | Dias com atividade (eventos, aulas) num mês. |
| 17 | `largeCalendarHeatmap` | Heatmap calendar | `calendarHeatmap` | Calendário com cor por intensidade | Intensidade diária (presenças, atendimentos). |
| 18 | `largeCalendarPie` | Calendar pie | `calendarPie` | Calendário com mini-pizza por dia | Proporção diária (presença/ausência). |
| 19 | `largeCalendarCustom` | Customized calendar | `calendarCustom` | Calendário com bolha proporcional | Volume diário com destaque de picos. |
| 20 | `largeGreenSalesReport` | Basic green bar · sales report | `basicGreenReport` | Colunas verdes com cabeçalho de relatório | Relatório mensal compacto. |
| 21 | `largeSmoothLine` | Smoothed line chart | `smoothLine` | Linha suavizada | Tendência contínua de um indicador. |
| 22 | `largeBasicLine` | Basic line chart | `basicLine` | Linha básica | Série com pontos exatos. |
| 23 | `largeSmoothLineRace` | Smoothed line race | `smoothLineRace` | Várias linhas suavizadas (corrida) | Comparar 5–7 séries no tempo (cursos, campus). |
| 24 | `largeLineRace` | Line race | `lineRace` | Linha de corrida única | Evolução de um item com destaque do líder. |
| 25 | `largeLineWithPoint` | Line with selected point | `lineWithPoint` | Linha com ponto selecionado | Inspecionar um mês específico. |
| 26 | `largeRisingFallingArea` | Rising and falling area | `riseFallArea` | Área de subida e descida | Variação positiva/negativa contra a base. |
| 27 | `largeMultipleAxes` | Multiple axes | `multipleAxes` | Múltiplos eixos | Séries com unidades diferentes (valor × quantidade). |
| 28 | `largeLineRaceDetail` | Line race · detail | `lineRaceDetail` | Corrida com detalhe | Série principal com referências secundárias. |
| 29 | `largeTransformLine` | Data transform line chart | `transformLine` | Linha com transformação de dados | Comparar série real e série tratada (média móvel). |
| 30 | `largeAreaPieceLine` | Area piece line chart | `areaPieceLine` | Área por trechos | Destacar faixas do período (ex.: período letivo). |
| 31 | `largeSimpleDonut` | Simple donut chart | `radial` | Rosca simples | Proporções e metas. |
| 32 | `largeNestedPies` | Nested pies | `radial` | Pizzas aninhadas | Proporções e metas. |
| 33 | `largeHalfDoughnut` | Half doughnut chart | `radial` | Meia rosca | Proporções e metas. |
| 34 | `largeGradientGauge` | Gradient gauge | `radial` | Medidor com gradiente | Proporções e metas. |
| 35 | `largeCircularPoints` | Circular points | `radial` | Pontos circulares | Proporções e metas. |
| 36 | `largeCircularPointsMixed` | Circular points · mixed | `radial` | Pontos circulares mistos | Proporções e metas. |
| 37 | `largeNightingale` | Nightingale chart | `radial` | Rosa de Nightingale | Proporções e metas. |
| 38 | `largeSegmentDonut` | Segmented donut chart | `radial` | Rosca segmentada | Proporções e metas. |
| 39 | `largeStrokedGauge` | Stroked gauge | `radial` | Medidor tracejado | Proporções e metas. |
| 40 | `largeDonutMarkers` | Doughnut chart with markers | `radial` | Rosca com marcadores | Proporções e metas. |
| 41 | `largeMultipleRadialsSoft` | Multiple radials · soft | `radial` | Múltiplos radiais (suave) | Proporções e metas. |
| 42 | `largeMultipleRadialsOrange` | Multiple radials · orange | `radial` | Múltiplos radiais (laranja) | Proporções e metas. |
| 43 | `largeMultipleRadialsTriple` | Multiple radials · triple | `radial` | Múltiplos radiais (triplo) | Proporções e metas. |
| 44 | `largeCircularPointsDense` | Circular points · dense | `radial` | Pontos circulares densos | Proporções e metas. |
| 45 | `largeBubble3D` | Bubble chart · 3D | `bubble3d` | Bolhas em perspectiva 3D | Peças de destaque/apresentação com 3 dimensões. |
| 46 | `largeFlyingIndicators` | Flying indicators | `flyingIndicators` | Indicadores em perspectiva | Destaque visual de uma série em apresentações. |
| 47 | `largeLineArea3D` | Line area chart · 3D | `lineArea3d` | Área em perspectiva 3D | Camadas de volume em apresentações. |
| 48 | `largeDivisionBars` | Stacked bars · division sales | `divisionBars` | Barras empilhadas por divisão | Desempenho por unidade/divisão contra meta. |
| 49 | `largePopularCategories` | Donut · popular categories | `categoryDonut` | Rosca de categorias populares | Participação das 5 categorias principais. |
| 50 | `largeCategoryBreakdown` | Pie · category breakdown | `categoryPie` | Pizza de categorias | Composição de um total em até 5 partes. |
| 51 | `largeCategoryRadar` | Radar · category comparison | `categoryRadar` | Radar de categorias | Comparar 2–3 itens em 5 dimensões. |

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
| `id` | `string` | Vira `data-widget`, chave de `state` e prefixo dos ids internos (`<id>-value`, `<id>-chart`). |
| `label` | `string` | Nome do tipo, exibido acima do card (“: Waterfall chart”) e no `aria-label`. |
| `kind` | `string` | Escolhe o desenho no gerador de SVG da seção. |
| `visual` | `string` | Só em `kind: 'heatmap'`: `hexFlow`, `hexRadial`, `basic`, `indicator`, `gradient`. |
| `colors` | `string[]` | Paleta das marcas (hex). Mantém-se fixa por tipo. |
| `radial` | `string` | Em `kind: 'radial'`: `donut`, `nested`, `half`, `gradientGauge`, `points`, `nightingale`, `segmentDonut`, `strokedGauge`, `donutMarkers`, `multi*`, `points*`. |

Estado inicial: `selectedPoint` = 15 nos calendários, 0 nos de categoria, 1 nos radiais e 5 nos demais.

### Dados

Valores: `largeValue(index)` (vetor de 12 valores), `radialMetric(def, i)`, `largeCategoryData` (5 categorias com `%`) e, nos calendários, um vetor local de 31 contagens de “August 2024”. Tudo isso é amostra a substituir.

### Atributos `data-*`

| Atributo | Onde / efeito |
|---|---|
| `data-large-widget` / `data-large-point` | Marca selecionável (barras, pontos, fatias radiais, dias do calendário). |
| `data-heatmap-widget` / `data-heatmap-point` | Células dos heatmaps. |
| `data-widget` | No `<article>` gerado: id da definição (chave de `state` e de `renderWidget`). |
| `data-widget-filter` | Botão “Filter” criado pelo JS em cada card. |

### Funções e eventos

| Função / evento | O que faz |
|---|---|
| `mountLargeWidgets()` | Gera os cards (cabeçalho por tipo; calendário com grade). |
| `renderLargeWidget(def)` | Calendário: só atualiza seleção/contexto; demais: valor e SVG. |
| `largeChartSvg(def)` | Despacha: `heatmapSvg`, `radialSvg`, `largePerspectiveSvg`, `largeCategorySvg`, `largeSalesLineSvg` ou barras. |
| `largeCalendar(def)` | Grade mensal de botões com cor/pizza/bolha por intensidade. |
| `renderWidget(id)` | Despacha para o render da seção (entradas geradas com `Object.fromEntries(<defs>.map(…))`). |
| `renderAll()` | Observa todos os cards e renderiza sob demanda. |
| `click` / `keydown` globais | Selecionam o ponto (`selectedPoint`) e re-renderizam só aquele widget. |

### Endpoints

Sem rota pronta. Provider do módulo de cada fonte: eventos (agenda institucional), cobrança (`admin.financial.view`), matrículas e frequência (permissões da secretaria/portal). URL em `data-endpoint`.

## Acessibilidade

- Cada marca selecionável é `<g role="button" tabindex="0" aria-pressed>` com `aria-label` “Mês: $valor” e `<title>`; `Enter`/`Espaço` selecionam (tratador global de `keydown`).
- Nos heatmaps só a célula selecionada tem `tabindex="0"` (as demais `-1`): as setas movem a seleção entre células (roving tabindex).
- O rótulo “: Nome” acima de cada card é texto visível (`.…-widget-label`), e o `<article>` tem `aria-label` com o nome do tipo.
- O tooltip comum abre em hover e foco; a gaveta “Filter” (`#widget-filter-drawer`) filtra marcas por texto e faixa e anuncia a contagem em `aria-live`.
- As paletas são fixas por definição (`colors`); confira contraste das marcas finas no tema escuro e nunca use cor como único portador do valor — o valor do ponto selecionado está em texto no card.

## Modelos

### HTML

**1. Na view PHP.** Nenhum partial do chassi gera estas seções; elas são o contêiner vazio de `index.html` que `mountLargeWidgets()` preenche. Numa view Plates do módulo:

```php
<?php
$e = static fn ($v) => htmlspecialchars((string) $v, ENT_QUOTES, 'UTF-8');   // helper de domain_page.php
?>
<!-- widgets.js monta os cards dentro de #large-widgets-grid; data-endpoint é lido pelo provider -->
<section class="large-widget-section" aria-labelledby="large-widgets-grid-title" data-endpoint="<?= $e('/academic/widgets/large' /* provider a criar */) ?>">
  <h2 class="large-widget-section-title" id="large-widgets-grid-title"><?= $e($titulo) ?></h2>
  <div class="widgets-grid large-widgets-grid" id="large-widgets-grid" aria-label="<?= $e($descricao) ?>"></div>
</section>
```

**2. Contêiner real** (`docs/model/widgets/index.html`):

```html
<section class="large-widget-section" aria-labelledby="large-widgets-title">
  <h2 class="large-widget-section-title" id="large-widgets-title">Large size widgets</h2>
  <div class="widgets-grid large-widgets-grid" id="large-widgets-grid" aria-label="Fifty-one large chart, heatmap and calendar examples"></div>
</section>
```

**3. HTML gerado** (capturado do preview renderizado com Playwright; marcas repetidas resumidas):

```html
<div class="large-widget-item">
  <div class="large-widget-label">: Basic bar</div>
  <article class="ttsc-analytics-card widget demo-widget large-widget-card " data-widget="largeBasicBars" aria-label="Basic bar large widget" style="position: relative;">
    <header class="large-widget-head"><strong>Sales Report</strong></header>
    <div class="large-widget-plot" id="largeBasicBars-chart">
      <svg class="large-widget-chart" viewBox="0 0 300 172" role="group" aria-label="Basic bar; select a mark to inspect its value">
        <path class="large-chart-gridline" d="M5 28H295"></path>
        <path class="large-chart-gridline" d="M5 56H295"></path>
        <path class="large-chart-gridline" d="M5 84H295"></path>
        <!-- … +29 elemento(s) iguais gerados pelo JS -->
      </svg>
    </div>
    <div class="large-widget-dual">
      <div>
        <small>✦ Monthly</small>
        <strong id="largeBasicBars-value">$8,097</strong>
        <span>↑ 19.6% &nbsp; 44,214 USD</span>
      </div>
      <div><small>♟ Yearly</small><strong>$312,134</strong><span>↑ 2.5% &nbsp; 301,002 USD</span></div>
    </div>
    <div class="large-widget-regions">
      <span>Los Angeles <b>201,192</b></span>
      <span>New York <b>192,054</b></span>
      <span>Canada <b>166,401</b></span>
    </div>
    <button class="widget-filter-trigger" type="button" data-widget-filter="largeBasicBars" aria-label="Filter Sales Report" aria-expanded="false">
      <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
      <span>Filter</span>
      <b hidden=""></b>
    </button>
  </article>
</div>
```

```html
<div class="large-widget-item">
  <div class="large-widget-label">: Simple calendar</div>
  <article class="ttsc-analytics-card widget demo-widget large-widget-card large-calendar-card" data-widget="largeCalendarSimple" aria-label="Simple calendar large widget" style="position: relative;">
    <header class="large-widget-head"><strong>Income</strong><span class="medium-widget-change">↑ 2.5%</span></header>
    <div class="large-calendar-value" id="largeCalendarSimple-value">$32,134 <span>↑ 2.5%</span></div>
    <p class="large-widget-context" id="largeCalendarSimple-context">16 Aug 2024 · 13 activity events</p>
    <div class="large-calendar-grid" role="group" aria-label="August 2024 activity calendar">
      <span class="large-calendar-weekday" style="grid-column:1">Sun</span>
      <span class="large-calendar-weekday" style="grid-column:2">Mon</span>
      <span class="large-calendar-weekday" style="grid-column:3">Tue</span>
      <!-- … +35 elemento(s) iguais gerados pelo JS -->
    </div>
    <button class="widget-filter-trigger" type="button" data-widget-filter="largeCalendarSimple" aria-label="Filter Income" aria-expanded="false">
      <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
      <span>Filter</span>
      <b hidden=""></b>
    </button>
  </article>
</div>
```

### CSS

Arquivo: `docs/model/widgets/widgets.css` (sobre `ttsc.analytics-panels.css`). Tema escuro por `html[data-theme="dark"]` (variáveis `--w-*`) e `html.dark` no app, sincronizados por `TTSCModelKit.syncTheme()`. Regras reais da seção:

```css
.large-radial-chart .radial-mark { cursor: pointer; outline: none; }
.large-radial-chart .radial-mark path, .large-radial-chart .radial-mark circle { transition: opacity .15s ease, filter .15s ease; }
.large-radial-chart .radial-mark:hover path, .large-radial-chart .radial-mark:hover circle, .large-radial-chart .radial-mark:focus path, .large-radial-chart .radial-mark:focus circle, .large-radial-chart .radial-mark.is-selected path, .large-radial-c; /* … */ }
.large-radial-chart .radial-mark:focus-visible { outline: none; }
.large-radial-chart .radial-mark:hover path, .large-radial-chart .radial-mark:hover circle,
```

Customização legítima:

```css
/* Dia selecionado do calendário com o anel do produto */
.large-calendar-day[aria-pressed="true"] { outline: 2px solid var(--ttsc-accent); outline-offset: 1px; }
.large-calendar-weekday { color: var(--ttsc-text-muted); }
```

### JS

Definições, montagem e render reais em `widgets.js`:

```js
const largeWidgetDefinitions = [
  { id: 'largeBasicBars', label: 'Basic bar', kind: 'basic', colors: ['#7c3aed', '#c4b5fd'] },
  { id: 'largeStackedColumns', label: 'Stacked columns', kind: 'stacked', colors: ['#8b5cf6', '#f97316'] },
  { id: 'largeRainfall', label: 'Rainfall', kind: 'rainfall', colors: ['#fbbf24', '#8b5cf6'] },
  { id: 'largeDoubleRainfall', label: 'Double rainfall', kind: 'doubleRainfall', colors: ['#fbbf24', '#8b5cf6'] },
  { id: 'largeDetailedBars', label: 'Detailed bar chart', kind: 'detailed', colors: ['#22c55e', '#bbf7d0'] },
  { id: 'largeDetailedOrange', label: 'Detailed bar chart', kind: 'detailedOrange', colors: ['#f97316', '#cbd5e1'] },
  { id: 'largeStackedAverage', label: 'Stacked bar with average line', kind: 'stackedAverage', colors: ['#3b82f6', '#ec4899', '#f59e0b', '#8b5cf6'] },
  { id: 'largeMultiBars', label: 'Multiple bars chart', kind: 'multiBars', colors: ['#8b5cf6', '#22c55e', '#f97316'] },
  { id: 'largeBubbles', label: 'Bubble bar chart', kind: 'bubbles', colors: ['#f97316', '#fbbf24'] },
  { id: 'largeDoubleBubbles', label: 'Double bubble bar chart', kind: 'doubleBubbles', colors: ['#f97316', '#fbbf24'] },
  { id: 'largeHexFlow', label: 'Hex heatmap', kind: 'heatmap', visual: 'hexFlow' },
  { id: 'largeHexRadial', label: 'Hex heatmap', kind: 'heatmap', visual: 'hexRadial' },
  { id: 'largeBasicHeatmap', label: 'Basic heatmap', kind: 'heatmap', visual: 'basic' },
  { id: 'largeHeatmapIndicator', label: 'Heatmap indicator', kind: 'heatmap', visual: 'indicator' },
  { id: 'largeGradientHeatmap', label: 'Gradient heatmap', kind: 'heatmap', visual: 'gradient' },
  { id: 'largeCalendarSimple', label: 'Simple calendar', kind: 'calendarSimple', colors: ['#7c3aed'] },
  { id: 'largeCalendarHeatmap', label: 'Heatmap calendar', kind: 'calendarHeatmap', colors: ['#f97316', '#a855f7'] },
  { id: 'largeCalendarPie', label: 'Calendar pie', kind: 'calendarPie', colors: ['#7c3aed', '#fb923c'] },
  { id: 'largeCalendarCustom', label: 'Customized calendar', kind: 'calendarCustom', colors: ['#f97316'] },
  { id: 'largeGreenSalesReport', label: 'Basic green bar · sales report', kind: 'basicGreenReport', colors: ['#22c55e', '#bbf7d0'] },
  { id: 'largeSmoothLine', label: 'Smoothed line chart', kind: 'smoothLine', colors: ['#22c55e'] },
  { id: 'largeBasicLine', label: 'Basic line chart', kind: 'basicLine', colors: ['#fb477c'] },
  { id: 'largeSmoothLineRace', label: 'Smoothed line race', kind: 'smoothLineRace', colors: ['#22c55e', '#1689e8', '#7046df', '#fb477c', '#f97316', '#f59e0b', '#c026d3'] },
  { id: 'largeLineRace', label: 'Line race', kind: 'lineRace', colors: ['#fb477c'] },
  { id: 'largeLineWithPoint', label: 'Line with selected point', kind: 'lineWithPoint', colors: ['#22c55e', '#f59e0b', '#f97316'] },
  { id: 'largeRisingFallingArea', label: 'Rising and falling area', kind: 'riseFallArea', colors: ['#f97316', '#ec4899'] },
  { id: 'largeMultipleAxes', label: 'Multiple axes', kind: 'multipleAxes', colors: ['#7046df', '#fb477c', '#06b6d4', '#22c55e'] },
  { id: 'largeLineRaceDetail', label: 'Line race · detail', kind: 'lineRaceDetail', colors: ['#22c55e', '#f59e0b', '#94a3b8'] },
  { id: 'largeTransformLine', label: 'Data transform line chart', kind: 'transformLine', colors: ['#22c55e', '#94a3b8'] },
  { id: 'largeAreaPieceLine', label: 'Area piece line chart', kind: 'areaPieceLine', colors: ['#22c55e', '#cbd5e1'] },
  { id: 'largeSimpleDonut', label: 'Simple donut chart', kind: 'radial', radial: 'donut', colors: ['#7653f9', '#fb923c', '#22c55e'] },
  { id: 'largeNestedPies', label: 'Nested pies', kind: 'radial', radial: 'nested', colors: ['#7653f9', '#f97316', '#ef4444', '#06b6d4', '#22c55e'] },
  { id: 'largeHalfDoughnut', label: 'Half doughnut chart', kind: 'radial', radial: 'half', colors: ['#8b5cf6', '#f97316'] },
  { id: 'largeGradientGauge', label: 'Gradient gauge', kind: 'radial', radial: 'gradientGauge', colors: ['#14d6b1', '#a3e635', '#facc15', '#fb7185', '#7c3aed'] },
  { id: 'largeCircularPoints', label: 'Circular points', kind: 'radial', radial: 'points', colors: ['#8b5cf6', '#c4b5fd'] },
  { id: 'largeCircularPointsMixed', label: 'Circular points · mixed', kind: 'radial', radial: 'pointsMixed', colors: ['#8b5cf6', '#fb923c', '#fed7aa'] },
  { id: 'largeNightingale', label: 'Nightingale chart', kind: 'radial', radial: 'nightingale', colors: ['#f59e0b', '#fb477c', '#7c3aed', '#3b82f6'] },
  { id: 'largeSegmentDonut', label: 'Segmented donut chart', kind: 'radial', radial: 'segmentDonut', colors: ['#fb477c', '#f59e0b', '#3b82f6', '#cbd5e1'] },
  { id: 'largeStrokedGauge', label: 'Stroked gauge', kind: 'radial', radial: 'strokedGauge', colors: ['#f97316', '#cbd5e1'] },
  { id: 'largeDonutMarkers', label: 'Doughnut chart with markers', kind: 'radial', radial: 'donutMarkers', colors: ['#7c3aed', '#fb477c', '#fbbf24'] },
  { id: 'largeMultipleRadialsSoft', label: 'Multiple radials · soft', kind: 'radial', radial: 'multiSoft', colors: ['#7653f9', '#c4b5fd', '#22c55e'] },
  { id: 'largeMultipleRadialsOrange', label: 'Multiple radials · orange', kind: 'radial', radial: 'multiOrange', colors: ['#7653f9', '#f97316', '#fbbf24'] },
  { id: 'largeMultipleRadialsTriple', label: 'Multiple radials · triple', kind: 'radial', radial: 'multiTriple', colors: ['#7653f9', '#f97316', '#22c55e', '#fb477c'] },
  { id: 'largeCircularPointsDense', label: 'Circular points · dense', kind: 'radial', radial: 'pointsDense', colors: ['#8b5cf6', '#fb923c', '#e9d5ff'] },
  { id: 'largeBubble3D', label: 'Bubble chart · 3D', kind: 'bubble3d', colors: ['#22c55e', '#1689e8', '#f59e0b', '#ef4444', '#8b5cf6'] },
  { id: 'largeFlyingIndicators', label: 'Flying indicators', kind: 'flyingIndicators', colors: ['#ff5b12'] },
  { id: 'largeLineArea3D', label: 'Line area chart · 3D', kind: 'lineArea3d', colors: ['#ff5b12', '#ff7b0d', '#ff9e0c', '#ffbd16'] },
  { id: 'largeDivisionBars', label: 'Stacked bars · division sales', kind: 'divisionBars', colors: ['#a855f7', '#4c0b8c'] },
  { id: 'largePopularCategories', label: 'Donut · popular categories', kind: 'categoryDonut', colors: ['#250044', '#4c0b8c', '#7614bd', '#b34be8', '#dfb4f4'] },
  { id: 'largeCategoryBreakdown', label: 'Pie · category breakdown', kind: 'categoryPie', colors: ['#250044', '#4c0b8c', '#7614bd', '#b34be8', '#dfb4f4'] },
  { id: 'largeCategoryRadar', label: 'Radar · category comparison', kind: 'categoryRadar', colors: ['#a735e9', '#0879dc', '#158d79'] }
];
```

```js
function mountLargeWidgets() {
  const grid = byId('large-widgets-grid');
  if (!grid) return;
  grid.innerHTML = largeWidgetDefinitions.map(widget => `<div class="large-widget-item"><div class="large-widget-label">: ${widget.label}</div><article class="ttsc-analytics-card widget demo-widget large-widget-card ${widget.kind.startsWith('calendar') ? 'large-calendar-card' : ''}" data-widget="${widget.id}" aria-label="${widget.label} large widget"><header class="large-widget-head"><strong>${widget.kind.startsWith('calendar') ? 'Income' : ({ divisionBars: 'Sales by division', categoryDonut: 'Popular categories', categoryPie: 'Category breakdown', categoryRadar: 'Category comparison' }[widget.kind] || 'Sales Report')}</strong>${widget.kind.startsWith('calendar') ? '<span class="medium-widget-change">↑ 2.5%</span>' : ''}</header>${widget.kind.startsWith('calendar') ? `<div class="large-calendar-value" id="${widget.id}-value">$32,134 <span>↑ 2.5%</span></div><p class="large-widget-context" id="${widget.id}-context">Compared to $21,340 last month</p>${largeCalendar(widget)}` : `<div class="large-widget-plot" id="${widget.id}-chart"></div><div class="large-widget-dual"><div><small>✦ Monthly</small><strong id="${widget.id}-value">$8,097</strong><span>↑ 19.6% &nbsp; 44,214 USD</span></div><div><small>♟ Yearly</small><strong>$312,134</strong><span>↑ 2.5% &nbsp; 301,002 USD</span></div></div><div class="large-widget-regions"><span>Los Angeles <b>201,192</b></span><span>New York <b>192,054</b></span><span>Canada <b>166,401</b></span></div>`}</article></div>`).join('');
}
```

```js
function renderLargeWidget(widget) {
  const index = Math.max(0, Math.min(30, state[widget.id].selectedPoint));
  const value = largeValue(index);
  if (widget.kind.startsWith('calendar')) {
    const calendarActivity = [0, 0, 0, 5, 12, 18, 22, 7, 9, 13, 16, 24, 17, 21, 20, 13, 18, 25, 27, 21, 28, 17, 23, 26, 15, 11, 8, 3, 2, 1, 0];
    byId(`${widget.id}-value`).innerHTML = '$32,134 <span>↑ 2.5%</span>';
    const context = byId(`${widget.id}-context`);
    if (context) context.textContent = `${index + 1} Aug 2024 · ${calendarActivity[index]} activity events`;
    byId(`${widget.id}-chart`)?.remove();
    const card = byId(`${widget.id}-value`).closest('.large-widget-card');
    card.querySelectorAll('.large-calendar-day').forEach(day => day.setAttribute('aria-pressed', String(Number(day.dataset.largePoint) === index)));
    return;
  }
  const categorySelection = ['divisionBars', 'categoryDonut', 'categoryPie', 'categoryRadar'].includes(widget.kind)
    ? widget.kind === 'divisionBars'
      ? `${[84, 76, 63, 85][index % 4]}%`
      : widget.kind === 'categoryRadar'
        ? `${[82, 48, 72, 44, 69][index % 5]}%`
        : `${largeCategoryData[index % largeCategoryData.length].value}%`
    : null;
  byId(`${widget.id}-value`).textContent = categorySelection || fmtMoney(value, 0);
  byId(`${widget.id}-chart`).innerHTML = largeChartSvg(widget);
}
```

```js
function largeCalendar(widget) {
  const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const values = [0, 0, 0, 5, 12, 18, 22, 7, 9, 13, 16, 24, 17, 21, 20, 13, 18, 25, 27, 21, 28, 17, 23, 26, 15, 11, 8, 3, 2, 1, 0];
  const offset = 0;
  const max = Math.max(...values);
  const header = weekdays.map((day, index) => `<span class="large-calendar-weekday" style="grid-column:${index + 1}">${day}</span>`).join('');
  const cells = values.map((value, index) => {
    const day = index + 1;
    const column = (index + offset) % 7 + 1;
    const row = Math.floor((index + offset) / 7) + 2;
    let content = String(day), style = '';
    if (widget.kind === 'calendarHeatmap') style = `--day-color:${value ? (value > 20 ? '#a855f7' : value > 14 ? '#f97316' : value > 7 ? '#f59e0b' : '#fbbf24') : '#f1f3f6'};--day-ink:${value ? '#fff' : '#b7bec9'}`;
    if (widget.kind === 'calendarPie') content = `<i style="--pie:${Math.max(8, value / max * 100)}%;--pie-a:${widget.colors[0]};--pie-b:${widget.colors[1]}"></i>`;
    if (widget.kind === 'calendarCustom') content = `<i style="--bubble:${Math.max(3, value / max * 18)}px"></i>`;
    const label = `${day} Aug 2024 · activity value ${value}`;
    return `<button type="button" class="large-calendar-day ${widget.kind}" style="grid-column:${column};grid-row:${row};${style}" data-large-widget="${widget.id}" data-large-point="${day - 1}" aria-pressed="${state[widget.id].selectedPoint === day - 1}" aria-label="${label}">${content}</button>`;
  }).join('');
  return `<div class="large-calendar-grid" role="group" aria-label="August 2024 activity calendar">${header}${cells}</div>`;
}
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

// payload = { events_by_day: [{ day, events }], subscriptions_by_status: [{ status, percent }], presence_by_subject: [{ subject, presence_rate }], received: [{ month, value }] }
loadSection('.large-widget-section', largeWidgetDefinitions, (definition, payload) => {
  if (definition.kind.startsWith('calendar')) {
    const days = Array(31).fill(0);
    (payload.events_by_day ?? []).forEach(row => { days[Number(row.day) - 1] = Number(row.events) || 0; });
    return days;                                   // largeCalendar() deve ler definition.values no lugar do vetor local
  }
  if (definition.kind === 'radial') return (payload.subscriptions_by_status ?? []).map(r => Number(r.percent) || 0);
  if (definition.kind === 'categoryRadar') return (payload.presence_by_subject ?? []).map(r => Number(r.presence_rate) || 0);
  return (payload.received ?? []).map(r => Number(r.value) || 0);
});
```

CSV: `downloadCsv()` não tem ramo para os widgets de seção (o menu “Download CSV” não existe nesses cards). Para exportar, use a exportação da página de origem dos dados (`GET /api/v1/domain/records{rota}/export?format=csv|xlsx|pdf|json|xml|sql`).

### SQL

Quatro agregados reais cobrem as famílias grandes: eventos por dia do mês (calendários, `events`), assinaturas por situação (radiais, `billing_subscriptions`), matrículas por curso e mês (corridas de linhas, `enrollments` + `courses`) e presença por disciplina (radar, `attendance` + `subjects`). Testados no MariaDB local com `:month = '2026-10'`.

```sql
-- (a) Calendários: eventos publicados por dia do mês (:month = '2026-10')
SELECT DAY(ev.start_date) AS day, COUNT(*) AS events
  FROM events ev
 WHERE ev.deleted_at IS NULL
   AND ev.status <> 'cancelled'
   AND ev.start_date BETWEEN STR_TO_DATE(CONCAT(:month, '-01'), '%Y-%m-%d') AND LAST_DAY(STR_TO_DATE(CONCAT(:month, '-01'), '%Y-%m-%d'))
 GROUP BY DAY(ev.start_date)
 ORDER BY day;

-- (b) Radiais (rosca, meia rosca, gauge): assinaturas por situação
SELECT s.status, COUNT(*) AS total, ROUND(COUNT(*) / SUM(COUNT(*)) OVER () * 100, 1) AS percent
  FROM billing_subscriptions s
 WHERE s.deleted_at IS NULL
 GROUP BY s.status
 ORDER BY total DESC;

-- (c) Line race / múltiplas linhas: matrículas por curso e mês (5 cursos com mais matrículas)
SELECT co.name AS course, DATE_FORMAT(e.enrollment_date, '%Y-%m') AS month, COUNT(*) AS total
  FROM enrollments e
  JOIN courses co ON co.uuid = e.course_uuid AND co.deleted_at IS NULL
  JOIN (SELECT course_uuid FROM enrollments WHERE deleted_at IS NULL
         GROUP BY course_uuid ORDER BY COUNT(*) DESC LIMIT 5) top5 ON top5.course_uuid = e.course_uuid
 WHERE e.deleted_at IS NULL
   AND e.enrollment_date >= DATE_FORMAT(CURDATE() - INTERVAL 11 MONTH, '%Y-%m-01')
 GROUP BY co.name, DATE_FORMAT(e.enrollment_date, '%Y-%m')
 ORDER BY course, month;

-- (d) Radar / comparação por categoria: taxa de presença por disciplina
SELECT su.name AS subject, ROUND(SUM(a.status IN ('present', 'late')) / COUNT(*) * 100, 1) AS presence_rate
  FROM attendance a
  JOIN subjects su ON su.uuid = a.subject_uuid AND su.deleted_at IS NULL
 WHERE a.lesson_date >= CURDATE() - INTERVAL 90 DAY
 GROUP BY su.uuid, su.name
 ORDER BY presence_rate DESC
 LIMIT 6;
```

Os calendários do modelo assumem um mês que começa no domingo (`offset = 0`); com dados reais calcule `offset = (DAYOFWEEK(primeiro_dia) - 1)` e passe para `largeCalendar`.

## Faça / Não faça

- **Faça:** corrigir o deslocamento do primeiro dia do mês nos calendários;
- **Faça:** limitar radar a 3 itens e 5–6 eixos.
- **Não faça:** usar as perspectivas 3D para leitura de valores;
- **Não faça:** deixar o rótulo “August 2024” fixo do calendário.
