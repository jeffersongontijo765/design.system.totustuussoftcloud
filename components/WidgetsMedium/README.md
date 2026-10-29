# WidgetsMedium

Seção “Medium size widgets”: 19 cards médios com cabeçalho, valor (ou bloco duplo mensal/anual) e gráfico maior — colunas agrupadas, empilhadas 100%, cascata, heatmaps, círculos, treemaps e tiles de KPI.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só a seção `.medium-widget-section` (o script do preview recebe `section = ".medium-widget-section"` em vez de uma lista de widgets). Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Painéis de duas ou três colunas em que cada card responde a uma pergunta com um gráfico legível (composição, comparação, intensidade).
- `dual: true` quando o card deve mostrar mensal e anual lado a lado.
- Para gráficos com eixo, configurações e CSV use os widgets individuais; para dashboards completos, [WidgetsXL](../WidgetsXL/README.md).

## Anatomia

```
article.medium-widget-card[data-widget]
  ┌ Income ↑2.5%                          ⋮ ┐  .medium-widget-head
  │ $32,134                                  │  .medium-widget-value  (ou .medium-widget-dual)
  │ Compared to $21,340 last month           │  .medium-widget-context
  │ [ gráfico SVG 220×145 ]                  │  .medium-widget-plot#<id>-chart
  └──────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Card | `article…medium-widget-card[data-widget]` (+ `.medium-treemap-card` no treemap) | sim |
| Cabeçalho | `header.medium-widget-head` (título, `.medium-widget-change`) | sim |
| Valor simples | `.medium-widget-value#<id>-value` + `p.medium-widget-context#<id>-context` | um dos dois |
| Valor duplo | `.medium-widget-dual` (Monthly/Yearly) | um dos dois |
| Gráfico | `.medium-widget-plot#<id>-chart` | sim |

## Variantes

19 tipos de widget, gerados de `mediumWidgetDefinitions` em `widgets.js` (mesma ordem do catálogo):

| # | Widget (`data-widget`) | Nome no catálogo | Tipo | Visual | Quando usar |
|---|---|---|---|---|---|
| 1 | `mediumGroupedColumns` | Grouped bar chart | `groupedColumns` | Colunas agrupadas (3–4 séries por período) | Comparar séries no mesmo período (ex.: pago × aberto × vencido por mês). |
| 2 | `mediumGroupedHorizontal` | Grouped bar chart | `groupedHorizontal` | Barras horizontais agrupadas | Comparar séries por categoria com rótulos longos (cursos, campus). |
| 3 | `mediumStackedHorizontal` | Stacked horizontal bar | `stackedHorizontal` | Barra horizontal empilhada (parte × restante) | Mostrar parte de um total por linha (meta atingida, ocupação). |
| 4 | `mediumBasicBars` | Basic bar | `columns` | Colunas simples com destaque do ponto selecionado | Série curta de um único indicador (recebido por mês). |
| 5 | `mediumLabeledColumns` | Column with data labels | `labelsColumns` | Colunas com rótulos de valor | Quando cada valor precisa estar legível sem tooltip. |
| 6 | `mediumStackedColumns` | Stacked columns 100% | `stacked100` | Colunas 100% empilhadas (5 séries) | Composição percentual por período (modalidade, turno). |
| 7 | `mediumWaterfallPurple` | Waterfall chart | `waterfall` | Cascata: barras flutuantes de variação acumulada | Explicar como o saldo do mês chegou ao valor final (entradas e saídas). |
| 8 | `mediumWaterfallAmber` | Waterfall chart | `waterfall` | Cascata: barras flutuantes de variação acumulada | Explicar como o saldo do mês chegou ao valor final (entradas e saídas). |
| 9 | `mediumDenseBars` | Detailed bar chart | `denseColumns` | Colunas finas e densas (detalhe diário) | Até ~30 pontos, leitura de tendência e picos. |
| 10 | `mediumLineColumns` | Line and column chart | `lineColumns` | Colunas + linha sobreposta | Volume (colunas) contra uma taxa ou média (linha). |
| 11 | `mediumHexFlow` | Hex heatmap | `heatmap` | Heatmap hexagonal em fluxo | Intensidade por período × faixa (semana × dia). |
| 12 | `mediumHexRadial` | Hex heatmap | `heatmap` | Heatmap hexagonal radial | Intensidade concentrada em torno de um centro (picos). |
| 13 | `mediumBasicHeatmap` | Basic heatmap | `heatmap` | Heatmap de grade básico | Matriz semana × dia da semana (presença, atendimentos). |
| 14 | `mediumHeatmapIndicator` | Heatmap indicator | `heatmap` | Heatmap indicador (linhas por item) | Intensidade por item (cidade, campus) ao longo do tempo. |
| 15 | `mediumGradientHeatmap` | Gradient heatmap | `heatmap` | Heatmap com gradiente contínuo | Matriz com escala contínua de valores. |
| 16 | `mediumCirclePacking` | Circle | `circlePacking` | Empacotamento de círculos | Pesos relativos de muitas categorias sem ordem. |
| 17 | `mediumTreemap` | Basic | `treemap` | Treemap básico | Participação de categorias num total (aberto por categoria). |
| 18 | `mediumTreemapDetailed` | Detailed | `treemapDetailed` | Treemap detalhado com rótulos | Participação com valor escrito em cada bloco. |
| 19 | `mediumKpiTiles` | Tiles | `kpiTiles` | Tiles de KPI proporcionais | Top 5 de uma métrica (matrículas por curso). |

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
| `title` | `string` | Título do cabeçalho. |
| `value` | `number` | Valor base; `mediumValue()` aplica ratios. |
| `dual` | `boolean` | Usa o bloco Monthly/Yearly. |

Estado inicial: `{ selectedPoint: 5 }`, exceto `circlePacking` e `kpiTiles` (`0`).

### Dados

Valores sintéticos: `mediumValue()` (ratios sobre `value`), vetor local `[46, 62, 39, 78, …]` dentro de `mediumChartSvg` e textos fixos dos tiles (“Design 509”, “Marketing 380”…). Treemaps, círculos e tiles mantêm o valor do topo fixo e mudam só o contexto ao selecionar.

### Atributos `data-*`

| Atributo | Onde / efeito |
|---|---|
| `data-medium-widget` / `data-medium-point` | Marca selecionável (colunas, blocos do treemap, círculos, tiles). |
| `data-heatmap-widget` / `data-heatmap-point` | Células dos heatmaps. |
| `data-widget` | No `<article>` gerado: id da definição (chave de `state` e de `renderWidget`). |
| `data-widget-filter` | Botão “Filter” criado pelo JS em cada card. |

### Funções e eventos

| Função / evento | O que faz |
|---|---|
| `mountMediumWidgets()` | Gera os cards (cabeçalho, valor simples ou duplo, slot do gráfico). |
| `renderMediumWidget(def)` | Limita `selectedPoint` ao máximo do tipo, atualiza valor/contexto e SVG. |
| `mediumChartSvg(def)` | Gerador por `kind`; delega a `mediumTreemapSvg`, `mediumCirclePackingSvg`, `mediumKpiTilesSvg`, `heatmapSvg`. |
| `renderWidget(id)` | Despacha para o render da seção (entradas geradas com `Object.fromEntries(<defs>.map(…))`). |
| `renderAll()` | Observa todos os cards e renderiza sob demanda. |
| `click` / `keydown` globais | Selecionam o ponto (`selectedPoint`) e re-renderizam só aquele widget. |

### Endpoints

Sem rota pronta para os agregados. Provider do módulo (`admin.financial.view` para receitas; a permissão de matrículas da secretaria para `enrollments`). Listas de conferência: `/api/v1/domain/records/financial/receivable`.

## Acessibilidade

- Cada marca selecionável é `<g role="button" tabindex="0" aria-pressed>` com `aria-label` “Mês: $valor” e `<title>`; `Enter`/`Espaço` selecionam (tratador global de `keydown`).
- Nos heatmaps só a célula selecionada tem `tabindex="0"` (as demais `-1`): as setas movem a seleção entre células (roving tabindex).
- O rótulo “: Nome” acima de cada card é texto visível (`.…-widget-label`), e o `<article>` tem `aria-label` com o nome do tipo.
- O tooltip comum abre em hover e foco; a gaveta “Filter” (`#widget-filter-drawer`) filtra marcas por texto e faixa e anuncia a contagem em `aria-live`.
- As paletas são fixas por definição (`colors`); confira contraste das marcas finas no tema escuro e nunca use cor como único portador do valor — o valor do ponto selecionado está em texto no card.

## Modelos

### HTML

**1. Na view PHP.** Nenhum partial do chassi gera estas seções; elas são o contêiner vazio de `index.html` que `mountMediumWidgets()` preenche. Numa view Plates do módulo:

```php
<?php
$e = static fn ($v) => htmlspecialchars((string) $v, ENT_QUOTES, 'UTF-8');   // helper de domain_page.php
?>
<!-- widgets.js monta os cards dentro de #medium-widgets-grid; data-endpoint é lido pelo provider -->
<section class="medium-widget-section" aria-labelledby="medium-widgets-grid-title" data-endpoint="<?= $e('/academic/widgets/medium' /* provider a criar */) ?>">
  <h2 class="medium-widget-section-title" id="medium-widgets-grid-title"><?= $e($titulo) ?></h2>
  <div class="widgets-grid medium-widgets-grid" id="medium-widgets-grid" aria-label="<?= $e($descricao) ?>"></div>
</section>
```

**2. Contêiner real** (`docs/model/widgets/index.html`):

```html
<section class="medium-widget-section" aria-labelledby="medium-widgets-title">
  <h2 class="medium-widget-section-title" id="medium-widgets-title">Medium size widgets</h2>
  <div class="widgets-grid medium-widgets-grid" id="medium-widgets-grid" aria-label="Nineteen medium chart widget examples"></div>
</section>
```

**3. HTML gerado** (capturado do preview renderizado com Playwright; marcas repetidas resumidas):

```html
<div class="medium-widget-item">
  <div class="medium-widget-label">: Grouped bar chart</div>
  <article class="ttsc-analytics-card widget demo-widget medium-widget-card " data-widget="mediumGroupedColumns" aria-label="Grouped bar chart medium widget" style="position: relative;">
    <header class="medium-widget-head">
      <div><strong>Income</strong><span class="medium-widget-change">↑ 2.5%</span></div>
      <span class="vertical-widget-dots" aria-hidden="true">⋮</span>
    </header>
    <div class="medium-widget-value" id="mediumGroupedColumns-value">$32,134</div>
    <p class="medium-widget-context" id="mediumGroupedColumns-context">Jun · compared to prior period</p>
    <div class="medium-widget-plot" id="mediumGroupedColumns-chart">
      <svg class="medium-widget-chart medium-chart-groupedColumns" viewBox="0 0 220 128" role="group" aria-label="Grouped bar chart, select a mark to inspect values">
        <path class="medium-chart-gridline" d="M2 15H218"></path>
        <path class="medium-chart-gridline" d="M2 45H218"></path>
        <path class="medium-chart-gridline" d="M2 75H218"></path>
        <!-- … +14 elemento(s) iguais gerados pelo JS -->
      </svg>
    </div>
    <button class="widget-filter-trigger" type="button" data-widget-filter="mediumGroupedColumns" aria-label="Filter Income" aria-expanded="false">
      <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
      <span>Filter</span>
      <b hidden=""></b>
    </button>
  </article>
</div>
```

```html
<div class="medium-widget-item">
  <div class="medium-widget-label">: Tiles</div>
  <article class="ttsc-analytics-card widget demo-widget medium-widget-card " data-widget="mediumKpiTiles" aria-label="Tiles medium widget" style="position: relative;">
    <header class="medium-widget-head">
      <div><strong>Income</strong><span class="medium-widget-change">↑ 2.5%</span></div>
      <span class="vertical-widget-dots" aria-hidden="true">⋮</span>
    </header>
    <div class="medium-widget-value" id="mediumKpiTiles-value">$32,134</div>
    <p class="medium-widget-context" id="mediumKpiTiles-context">Design 509 · selected tile</p>
    <div class="medium-widget-plot" id="mediumKpiTiles-chart">
      <svg class="medium-widget-chart medium-kpi-tiles-chart" viewBox="0 0 220 128" role="group" aria-label="Department KPI tiles; select a tile to inspect its value">
        <g class="medium-chart-mark is-selected" role="button" tabindex="0" data-medium-widget="mediumKpiTiles" data-medium-point="0" aria-pressed="true" aria-label="DESIGN: 509, 4.53% of total">
          <rect x="0" y="0" width="96" height="65" rx="8" fill="#ffb900"></rect>
          <text x="9" y="12" class="medium-tile-label">● DESIGN</text>
          <text x="9" y="57" class="medium-tile-value">509</text>
          <text x="88" y="58" text-anchor="end" class="medium-tile-pct">4.53%</text>
          <title>DESIGN: 509, 4.53% of total</title>
        </g>
        <g class="medium-chart-mark" role="button" tabindex="0" data-medium-widget="mediumKpiTiles" data-medium-point="1" aria-pressed="false" aria-label="MARKETING: 380, 12% of total">
          <rect x="100" y="0" width="116" height="40" rx="8" fill="#d1d0d9"></rect>
          <text x="109" y="12" class="medium-tile-label">● MARKETING</text>
          <text x="109" y="32" class="medium-tile-value is-dark">380</text>
          <text x="208" y="33" text-anchor="end" class="medium-tile-pct">12%</text>
          <title>MARKETING: 380, 12% of total</title>
        </g>
        <g class="medium-chart-mark" role="button" tabindex="0" data-medium-widget="mediumKpiTiles" data-medium-point="2" aria-pressed="false" aria-label="DEVOPS: 551, 1.32% of total">
          <rect x="0" y="69" width="96" height="55" rx="8" fill="#9881ff"></rect>
          <text x="9" y="81" class="medium-tile-label">● DEVOPS</text>
          <text x="9" y="116" class="medium-tile-value">551</text>
          <text x="88" y="117" text-anchor="end" class="medium-tile-pct">1.32%</text>
          <title>DEVOPS: 551, 1.32% of total</title>
        </g>
        <!-- … +2 elemento(s) iguais gerados pelo JS -->
      </svg>
    </div>
    <button class="widget-filter-trigger" type="button" data-widget-filter="mediumKpiTiles" aria-label="Filter Income" aria-expanded="false">
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

```

Customização legítima:

```css
/* Bloco duplo com separador do tema */
.medium-widget-dual > div + div { border-left: 1px solid var(--ttsc-border-soft); }
.medium-widget-context { color: var(--ttsc-text-muted); }
```

### JS

Definições, montagem e render reais em `widgets.js`:

```js
const mediumWidgetDefinitions = [
  { id: 'mediumGroupedColumns', label: 'Grouped bar chart', kind: 'groupedColumns', title: 'Income', value: 32134, colors: ['#3b82f6', '#fb7185', '#f59e0b', '#8b5cf6'] },
  { id: 'mediumGroupedHorizontal', label: 'Grouped bar chart', kind: 'groupedHorizontal', title: 'Income', value: 8097, dual: true, colors: ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b'] },
  { id: 'mediumStackedHorizontal', label: 'Stacked horizontal bar', kind: 'stackedHorizontal', title: 'Income', value: 32134, colors: ['#6d5dfc', '#c4b5fd'] },
  { id: 'mediumBasicBars', label: 'Basic bar', kind: 'columns', title: 'Income', value: 32134, colors: ['#22c55e', '#bbf7d0'] },
  { id: 'mediumLabeledColumns', label: 'Column with data labels', kind: 'labelsColumns', title: 'Income', value: 32134, colors: ['#22c55e', '#3b82f6'] },
  { id: 'mediumStackedColumns', label: 'Stacked columns 100%', kind: 'stacked100', title: 'Income', value: 32134, colors: ['#3b82f6', '#8b5cf6', '#ec4899', '#f97316', '#f59e0b'] },
  { id: 'mediumWaterfallPurple', label: 'Waterfall chart', kind: 'waterfall', title: 'Income', value: 8097, dual: true, colors: ['#8b5cf6', '#c4b5fd'] },
  { id: 'mediumWaterfallAmber', label: 'Waterfall chart', kind: 'waterfall', title: 'Income', value: 32134, colors: ['#f59e0b', '#fb923c'] },
  { id: 'mediumDenseBars', label: 'Detailed bar chart', kind: 'denseColumns', title: 'Income', value: 32134, colors: ['#22c55e'] },
  { id: 'mediumLineColumns', label: 'Line and column chart', kind: 'lineColumns', title: 'Income', value: 8097, dual: true, colors: ['#8b5cf6', '#fbbf24'] },
  { id: 'mediumHexFlow', label: 'Hex heatmap', kind: 'heatmap', visual: 'hexFlow', title: 'Income', value: 32134 },
  { id: 'mediumHexRadial', label: 'Hex heatmap', kind: 'heatmap', visual: 'hexRadial', title: 'Income', value: 32134 },
  { id: 'mediumBasicHeatmap', label: 'Basic heatmap', kind: 'heatmap', visual: 'basic', title: 'Income', value: 32134 },
  { id: 'mediumHeatmapIndicator', label: 'Heatmap indicator', kind: 'heatmap', visual: 'indicator', title: 'Income', value: 32134 },
  { id: 'mediumGradientHeatmap', label: 'Gradient heatmap', kind: 'heatmap', visual: 'gradient', title: 'Income', value: 32134 },
  { id: 'mediumCirclePacking', label: 'Circle', kind: 'circlePacking', title: 'Income', value: 32134, colors: ['#9b55f7', '#fb7a3d'] },
  { id: 'mediumTreemap', label: 'Basic', kind: 'treemap', title: 'Income', value: 8097, dual: true, colors: ['#ffb900', '#9b75ff', '#d2d0dc'] },
  { id: 'mediumTreemapDetailed', label: 'Detailed', kind: 'treemapDetailed', title: 'Income', value: 32134, colors: ['#ffb900', '#ff8c00', '#ff6b24'] },
  { id: 'mediumKpiTiles', label: 'Tiles', kind: 'kpiTiles', title: 'Income', value: 32134, colors: ['#ffb900', '#d1d0d9', '#9881ff', '#3385f7', '#f50076'] }
];
```

```js
function mountMediumWidgets() {
  const grid = byId('medium-widgets-grid');
  if (!grid) return;
  grid.innerHTML = mediumWidgetDefinitions.map(widget => {
    const head = `<header class="medium-widget-head"><div><strong>${widget.title}</strong><span class="medium-widget-change">↑ 2.5%</span></div><span class="vertical-widget-dots" aria-hidden="true">⋮</span></header>`;
    const dual = `<div class="medium-widget-dual${widget.kind === 'treemap' ? ' medium-widget-dual-footer' : ''}"><div><small>✦ Monthly</small><strong id="${widget.id}-value">${fmtMoney(widget.value, 0)}</strong><span>↑ 19.6% · 44,214 USD</span></div><div><small>♟ Yearly</small><strong>$312,134</strong><span>↑ 2.5% · 301,002 USD</span></div></div>`;
    const chart = `<div class="medium-widget-plot" id="${widget.id}-chart"></div>`;
    const content = widget.kind === 'treemap' ? `${head}${chart}${dual}` : `${head}${widget.dual ? dual : `<div class="medium-widget-value" id="${widget.id}-value">${fmtMoney(widget.value, 0)}</div><p class="medium-widget-context" id="${widget.id}-context">Compared to $21,340 last month</p>`}${chart}`;
    return `<div class="medium-widget-item"><div class="medium-widget-label">: ${widget.label}</div><article class="ttsc-analytics-card widget demo-widget medium-widget-card ${widget.kind === 'treemap' ? 'medium-treemap-card' : ''}" data-widget="${widget.id}" aria-label="${widget.label} medium widget">${content}</article></div>`;
  }).join('');
}
```

```js
function renderMediumWidget(widget) {
  const maximum = widget.kind === 'circlePacking' ? 29 : widget.kind === 'treemap' ? 9 : widget.kind === 'treemapDetailed' ? 10 : widget.kind === 'kpiTiles' ? 4 : 11;
  const index = Math.max(0, Math.min(maximum, state[widget.id].selectedPoint));
  state[widget.id].selectedPoint = index;
  const fixedKpi = ['circlePacking', 'treemap', 'treemapDetailed', 'kpiTiles'].includes(widget.kind);
  if (!fixedKpi) byId(`${widget.id}-value`).textContent = fmtMoney(mediumValue(widget, index), 0);
  const context = byId(`${widget.id}-context`);
  if (context) context.textContent = widget.kind === 'kpiTiles' ? `${['Design 509', 'Marketing 380', 'DevOps 551', 'Research 353', 'Sales 331'][index]} · selected tile` : widget.kind === 'circlePacking' ? `Circle sample ${index + 1} selected` : widget.kind === 'treemapDetailed' ? `Tile ${index + 1} selected · regional income` : `${months[index % 12]} · compared to prior period`;
  byId(`${widget.id}-chart`).innerHTML = mediumChartSvg(widget);
}
```

```js
function mediumKpiTilesSvg(widget) {
  const tiles = [
    { x: 0, y: 0, w: 96, h: 65, label: 'DESIGN', value: '509', pct: '4.53%' },
    { x: 100, y: 0, w: 116, h: 40, label: 'MARKETING', value: '380', pct: '12%' },
    { x: 0, y: 69, w: 96, h: 55, label: 'DEVOPS', value: '551', pct: '1.32%' },
    { x: 100, y: 43, w: 116, h: 37, label: 'RESEARCH', value: '353', pct: '25%' },
    { x: 100, y: 83, w: 116, h: 41, label: 'SALES', value: '331', pct: '5.21%' }
  ];
  const content = tiles.map((tile, index) => mediumChartPoint(widget, index, `<rect x="${tile.x}" y="${tile.y}" width="${tile.w}" height="${tile.h}" rx="8" fill="${widget.colors[index % widget.colors.length]}"/><text x="${tile.x + 9}" y="${tile.y + 12}" class="medium-tile-label">● ${tile.label}</text><text x="${tile.x + 9}" y="${tile.y + tile.h - 8}" class="medium-tile-value${index === 1 ? ' is-dark' : ''}">${tile.value}</text><text x="${tile.x + tile.w - 8}" y="${tile.y + tile.h - 7}" text-anchor="end" class="medium-tile-pct">${tile.pct}</text>`, `${tile.label}: ${tile.value}, ${tile.pct} of total`)).join('');
  return `<svg class="medium-widget-chart medium-kpi-tiles-chart" viewBox="0 0 220 128" role="group" aria-label="Department KPI tiles; select a tile to inspect its value">${content}</svg>`;
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

// payload = { open_by_category: [{ category, open_amount }], top_courses: [{ course, active_enrollments }], by_modality: [...] }
loadSection('.medium-widget-section', mediumWidgetDefinitions, (definition, payload) => {
  if (definition.kind.startsWith('treemap') || definition.kind === 'circlePacking') return (payload.open_by_category ?? []).map(r => Number(r.open_amount) || 0);
  if (definition.kind === 'kpiTiles') return (payload.top_courses ?? []).map(r => Number(r.active_enrollments) || 0);
  return (payload.by_modality ?? []).map(r => Number(r.total) || 0);
});
// Os rótulos fixos de mediumKpiTilesSvg/renderMediumWidget ('Design 509'…) também precisam vir de payload.top_courses.
```

CSV: `downloadCsv()` não tem ramo para os widgets de seção (o menu “Download CSV” não existe nesses cards). Para exportar, use a exportação da página de origem dos dados (`GET /api/v1/domain/records{rota}/export?format=csv|xlsx|pdf|json|xml|sql`).

### SQL

Três agregados cobrem os tipos médios: aberto por categoria (treemaps/círculos), matrículas ativas por curso (tiles) e matrículas por mês × modalidade (colunas 100%/agrupadas). Testados no MariaDB local.

```sql
-- (a) Treemap: valor em aberto por categoria de receita
SELECT c.name AS category, c.color, SUM(r.net_amount - COALESCE(r.amount_paid, 0)) AS open_amount
  FROM financial_receivables r
  JOIN financial_categories c ON c.id = r.category_id AND c.deleted_at IS NULL
 WHERE r.deleted_at IS NULL AND r.status IN ('open', 'partial', 'overdue')
 GROUP BY c.id, c.name, c.color
 ORDER BY open_amount DESC
 LIMIT 10;

-- (b) Tiles de KPI: matrículas ativas por curso (top 5)
SELECT co.name AS course, COUNT(*) AS active_enrollments
  FROM enrollments e
  JOIN courses co ON co.uuid = e.course_uuid AND co.deleted_at IS NULL
 WHERE e.deleted_at IS NULL AND e.status = 'active'
 GROUP BY co.uuid, co.name
 ORDER BY active_enrollments DESC
 LIMIT 5;

-- (c) Colunas 100% empilhadas: matrículas por mês e modalidade
SELECT DATE_FORMAT(e.enrollment_date, '%Y-%m') AS month, e.modality, COUNT(*) AS total
  FROM enrollments e
 WHERE e.deleted_at IS NULL
   AND e.enrollment_date >= DATE_FORMAT(CURDATE() - INTERVAL 11 MONTH, '%Y-%m-01')
 GROUP BY DATE_FORMAT(e.enrollment_date, '%Y-%m'), e.modality
 ORDER BY month, e.modality;
```

`enrollments.status = 'active'` segue a convenção das views acadêmicas; troque pelo status real do tenant se diferente. Os nomes de curso vêm de `courses.name` — passe-os como rótulos dos tiles.

## Faça / Não faça

- **Faça:** usar `dual` só quando mensal e anual forem da mesma métrica;
- **Faça:** substituir os rótulos fixos dos tiles.
- **Não faça:** usar treemap para séries temporais;
- **Não faça:** misturar moeda e contagem no mesmo card.
