# WidgetsSmallHorizontal

Seção “Horizontal small widgets”: 24 cards compactos em linha — título, valor, variação e legenda à esquerda e um mini-gráfico SVG à direita (barras, cascata, heatmaps, medidor, sparkline…).

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só a seção `.horizontal-small-section` (o script do preview recebe `section = ".horizontal-small-section"` em vez de uma lista de widgets). Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Faixas de KPI no topo de um painel, quando cada número precisa de uma tendência mínima ao lado (recebido no mês, presença, inadimplência).
- Escolha um tipo por indicador; não misture mais de 4–6 cards na mesma faixa.
- Se o card precisa de configurações, menu e CSV, use um widget individual (ex.: [WidgetBalance](../WidgetBalance/README.md)); para números sem gráfico, [KpiView](../KpiView/README.md).

## Anatomia

```
.horizontal-small-section
  h2 Horizontal small widgets
  #horizontal-small-grid (4–6 colunas)
    .compact-widget-item
      .compact-widget-label  ": Waterfall chart"
      article.compact-widget-card[data-widget]
        ┌ Sales Report  $9,134  ↗2.5%  Jun · selected ┬ [mini SVG] ┐
        └──────────────────────────────────────────────┴───────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Seção | `section.horizontal-small-section` + `h2.horizontal-small-section-title` | sim |
| Grade | `div.widgets-grid.horizontal-small-grid#horizontal-small-grid` | sim |
| Item | `.compact-widget-item` > `.compact-widget-label` | sim |
| Card | `article.ttsc-analytics-card.widget.demo-widget.compact-widget-card[data-widget]` | sim |
| Métrica | `.compact-widget-metric` (`h3`, `strong#<id>-value`, `.compact-widget-change`, `small#<id>-caption`) | sim |
| Gráfico | `.compact-widget-chart-slot#<id>-chart` > `svg.compact-widget-chart.compact-chart-<kind>` | sim |

## Variantes

24 tipos de widget, gerados de `compactWidgetDefinitions` em `widgets.js` (mesma ordem do catálogo):

| # | Widget (`data-widget`) | Nome no catálogo | Tipo | Visual | Quando usar |
|---|---|---|---|---|---|
| 1 | `smallWaterfallPurple` | Waterfall chart | `waterfall` | Cascata: barras flutuantes de variação acumulada | Explicar como o saldo do mês chegou ao valor final (entradas e saídas). |
| 2 | `smallWaterfallAmber` | Waterfall chart | `waterfall` | Cascata: barras flutuantes de variação acumulada | Explicar como o saldo do mês chegou ao valor final (entradas e saídas). |
| 3 | `smallGroupedColumns` | Grouped bar chart | `groupedColumns` | Colunas agrupadas (3–4 séries por período) | Comparar séries no mesmo período (ex.: pago × aberto × vencido por mês). |
| 4 | `smallGroupedHorizontal` | Grouped bar chart | `groupedHorizontal` | Barras horizontais agrupadas | Comparar séries por categoria com rótulos longos (cursos, campus). |
| 5 | `smallStackedHorizontal` | Stacked horizontal bar | `stackedHorizontal` | Barra horizontal empilhada (parte × restante) | Mostrar parte de um total por linha (meta atingida, ocupação). |
| 6 | `smallBasicGreen` | Basic bar | `columns` | Colunas simples com destaque do ponto selecionado | Série curta de um único indicador (recebido por mês). |
| 7 | `smallBasicSpectrum` | Basic bar | `columns` | Colunas simples com destaque do ponto selecionado | Série curta de um único indicador (recebido por mês). |
| 8 | `smallDetailedBars` | Detailed bar chart | `columns` | Colunas simples com destaque do ponto selecionado | Série curta de um único indicador (recebido por mês). |
| 9 | `smallRainfall` | Rainfall | `rainfall` | Colunas “chuva” finas e coloridas por faixa | Série densa diária em pouco espaço. |
| 10 | `smallSparseBars` | Basic bar | `sparseColumns` | Colunas espaçadas com trilha de fundo | Poucos pontos (5–7) com ênfase no valor relativo. |
| 11 | `smallBubbles` | Bubble bar chart | `bubbles` | Barras em bolhas (pontos empilhados) | Contagens pequenas (eventos, ocorrências) por período. |
| 12 | `smallStackedColumns` | Stacked columns | `stackedColumns` | Colunas empilhadas em duas séries | Total por período e a composição entre duas partes. |
| 13 | `smallDenseBars` | Detailed bar chart | `denseColumns` | Colunas finas e densas (detalhe diário) | Até ~30 pontos, leitura de tendência e picos. |
| 14 | `smallLineColumns` | Line and column chart | `lineColumns` | Colunas + linha sobreposta | Volume (colunas) contra uma taxa ou média (linha). |
| 15 | `smallGradientBars` | Detailed bar chart | `gradientColumns` | Colunas com gradiente por intensidade | Destacar picos dentro da série. |
| 16 | `smallHexFlow` | Hex heatmap | `heatmap` | Heatmap hexagonal em fluxo | Intensidade por período × faixa (semana × dia). |
| 17 | `smallHexRadial` | Hex heatmap | `heatmap` | Heatmap hexagonal radial | Intensidade concentrada em torno de um centro (picos). |
| 18 | `smallBasicHeatmap` | Basic heatmap | `heatmap` | Heatmap de grade básico | Matriz semana × dia da semana (presença, atendimentos). |
| 19 | `smallHeatmapIndicator` | Heatmap indicator | `heatmap` | Heatmap indicador (linhas por item) | Intensidade por item (cidade, campus) ao longo do tempo. |
| 20 | `smallGradientHeatmap` | Gradient heatmap | `heatmap` | Heatmap com gradiente contínuo | Matriz com escala contínua de valores. |
| 21 | `smallScatter` | Bubble scatter | `scatter` | Dispersão em bolhas | Distribuição de valores sem ordem temporal. |
| 22 | `smallGauge` | Radial gauge | `gauge` | Medidor radial com gradiente | Percentual de meta (adimplência, ocupação). |
| 23 | `smallGreenSparkline` | Area sparkline | `sparkline` | Área sparkline | Tendência sem eixo, ao lado do valor. |
| 24 | `smallDotIndicator` | Dot indicator | `dotIndicator` | Indicador de pontos (matriz) | Progresso discreto (N de M). |

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

Estado inicial: `{ selectedPoint: 5 }` para todos (sexto ponto selecionado).

### Dados

Os valores vêm de `compactWidgetValues = [6720, 8120, 7310, 9560, 8840, 9134, 8620]` (barras/linhas) e de `heatmapValue(index)` (heatmaps); o card mostra o valor do ponto selecionado e o mês (`months[index]`). Título “Sales Report”, variação “↗ 2.5%” e “Avg. score” são texto fixo de `mountCompactWidgets()` — em produção passe `title`, `change` e `caption` na definição.

### Atributos `data-*`

| Atributo | Onde / efeito |
|---|---|
| `data-small-widget` | Na marca SVG: id do widget dono. |
| `data-small-point` | Índice do ponto; clique/Enter grava `selectedPoint`. |
| `data-heatmap-widget` / `data-heatmap-point` | Mesmo papel nos tipos `heatmap` (setas navegam entre células). |
| `data-widget` | No `<article>` gerado: id da definição (chave de `state` e de `renderWidget`). |
| `data-widget-filter` | Botão “Filter” criado pelo JS em cada card. |

### Funções e eventos

| Função / evento | O que faz |
|---|---|
| `mountCompactWidgets()` | Gera o HTML de todos os cards em `#horizontal-small-grid`. |
| `renderCompactWidget(def)` | Atualiza valor, legenda e o SVG do card. |
| `compactChartSvg(def)` | Desenha o mini-gráfico conforme `kind` (heatmaps via `heatmapSvg(def, 112, 62)`). |
| `compactPoint(def, index, shape)` | Envolve uma marca em `<g role="button">` selecionável. |
| `renderWidget(id)` | Despacha para o render da seção (entradas geradas com `Object.fromEntries(<defs>.map(…))`). |
| `renderAll()` | Observa todos os cards e renderiza sob demanda. |
| `click` / `keydown` globais | Selecionam o ponto (`selectedPoint`) e re-renderizam só aquele widget. |

### Endpoints

Não há rota pronta que devolva séries curtas por indicador. Exponha as consultas SQL abaixo num provider do módulo (permissão `admin.financial.view` para as financeiras; a da página de frequência para `attendance`) e grave a URL em `data-endpoint` da seção. Para conferência, as listas de origem estão em `GET /api/v1/domain/records/financial/receivable` e nas rotas de frequência do portal.

## Acessibilidade

- Cada marca selecionável é `<g role="button" tabindex="0" aria-pressed>` com `aria-label` “Mês: $valor” e `<title>`; `Enter`/`Espaço` selecionam (tratador global de `keydown`).
- Nos heatmaps só a célula selecionada tem `tabindex="0"` (as demais `-1`): as setas movem a seleção entre células (roving tabindex).
- O rótulo “: Nome” acima de cada card é texto visível (`.…-widget-label`), e o `<article>` tem `aria-label` com o nome do tipo.
- O tooltip comum abre em hover e foco; a gaveta “Filter” (`#widget-filter-drawer`) filtra marcas por texto e faixa e anuncia a contagem em `aria-live`.
- As paletas são fixas por definição (`colors`); confira contraste das marcas finas no tema escuro e nunca use cor como único portador do valor — o valor do ponto selecionado está em texto no card.

## Modelos

### HTML

**1. Na view PHP.** Nenhum partial do chassi gera estas seções; elas são o contêiner vazio de `index.html` que `mountCompactWidgets()` preenche. Numa view Plates do módulo:

```php
<?php
$e = static fn ($v) => htmlspecialchars((string) $v, ENT_QUOTES, 'UTF-8');   // helper de domain_page.php
?>
<!-- widgets.js monta os cards dentro de #horizontal-small-grid; data-endpoint é lido pelo provider -->
<section class="horizontal-small-section" aria-labelledby="horizontal-small-grid-title" data-endpoint="<?= $e('/financial/widgets/compact-series' /* provider a criar */) ?>">
  <h2 class="horizontal-small-section-title" id="horizontal-small-grid-title"><?= $e($titulo) ?></h2>
  <div class="widgets-grid horizontal-small-grid" id="horizontal-small-grid" aria-label="<?= $e($descricao) ?>"></div>
</section>
```

**2. Contêiner real** (`docs/model/widgets/index.html`):

```html
<section class="horizontal-small-section" aria-labelledby="horizontal-small-title">
  <h2 class="horizontal-small-section-title" id="horizontal-small-title">Horizontal small widgets</h2>
  <div class="widgets-grid horizontal-small-grid" id="horizontal-small-grid" aria-label="Twenty-four compact chart widget examples"></div>
</section>
```

**3. HTML gerado** (capturado do preview renderizado com Playwright; marcas repetidas resumidas):

```html
<div class="compact-widget-item">
  <div class="compact-widget-label">: Waterfall chart</div>
  <article class="ttsc-analytics-card widget demo-widget compact-widget-card" data-widget="smallWaterfallPurple" aria-label="Waterfall chart compact widget" style="position: relative;">
    <div class="compact-widget-body">
      <div class="compact-widget-metric">
        <h3>Sales Report</h3>
        <strong id="smallWaterfallPurple-value">$9,134</strong>
        <span class="compact-widget-change">↗ 2.5%</span>
        <small id="smallWaterfallPurple-caption">Jun · selected sample</small>
      </div>
      <div class="compact-widget-chart-slot" id="smallWaterfallPurple-chart">
        <svg class="compact-widget-chart compact-chart-waterfall" viewBox="0 0 84 60" role="group" aria-label="Waterfall chart sample, select a mark to inspect its monthly value">
          <path class="compact-chart-baseline" d="M2 55.5H82"></path>
          <g class="compact-chart-mark" role="button" tabindex="0" data-small-widget="smallWaterfallPurple" data-small-point="0" aria-pressed="false" aria-label="Jan: $6,720">
            <rect x="3" y="46.6" width="5" height="8" rx="2.5" fill="#8b5cf6" opacity="0.62"></rect>
            <title>Jan · $6,720</title>
          </g>
          <g class="compact-chart-mark" role="button" tabindex="0" data-small-widget="smallWaterfallPurple" data-small-point="1" aria-pressed="false" aria-label="Feb: $8,120">
            <rect x="13" y="22.82" width="5" height="13.600000000000001" rx="2.5" fill="#bd8cff" opacity="0.74"></rect>
            <title>Feb · $8,120</title>
          </g>
          <!-- … +6 elemento(s) iguais gerados pelo JS -->
        </svg>
      </div>
    </div>
    <button class="widget-filter-trigger" type="button" data-widget-filter="smallWaterfallPurple" aria-label="Filter Sales Report" aria-expanded="false">
      <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
      <span>Filter</span>
      <b hidden=""></b>
    </button>
  </article>
</div>
```

```html
<div class="compact-widget-item">
  <div class="compact-widget-label">: Hex heatmap</div>
  <article class="ttsc-analytics-card widget demo-widget compact-widget-card" data-widget="smallHexFlow" aria-label="Hex heatmap compact widget" style="position: relative;">
    <div class="compact-widget-body">
      <div class="compact-widget-metric">
        <h3>Sales Report</h3>
        <strong id="smallHexFlow-value">$9,134</strong>
        <span class="compact-widget-change">↗ 2.5%</span>
        <small id="smallHexFlow-caption">Jun · selected sample</small>
      </div>
      <div class="compact-widget-chart-slot" id="smallHexFlow-chart">
        <svg class="heatmap-svg heatmap-hexFlow" viewBox="0 0 112 62" role="group" aria-label="Hex heatmap; select a cell to inspect its value">
          <g class="heatmap-mark" role="button" tabindex="-1" data-heatmap-widget="smallHexFlow" data-heatmap-point="0" aria-pressed="false" aria-label="Heatmap cell 1: $6,720">
            <polygon points="15.24,8.62 12.43,13.49 6.81,13.49 4.00,8.62 6.81,3.75 12.43,3.75" fill="rgb(251,153,85)" stroke="white" stroke-width=".65"></polygon>
            <title>Cell 1 · $6,720</title>
          </g>
          <g class="heatmap-mark" role="button" tabindex="-1" data-heatmap-widget="smallHexFlow" data-heatmap-point="1" aria-pressed="false" aria-label="Heatmap cell 2: $8,120">
            <polygon points="25.47,13.34 22.66,18.21 17.04,18.21 14.23,13.34 17.04,8.48 22.66,8.48" fill="rgb(251,146,15)" stroke="white" stroke-width=".65"></polygon>
            <title>Cell 2 · $8,120</title>
          </g>
          <g class="heatmap-mark" role="button" tabindex="-1" data-heatmap-widget="smallHexFlow" data-heatmap-point="2" aria-pressed="false" aria-label="Heatmap cell 3: $7,310">
            <polygon points="35.71,8.62 32.90,13.49 27.27,13.49 24.46,8.62 27.27,3.75 32.90,3.75" fill="rgb(250,137,58)" stroke="white" stroke-width=".65"></polygon>
            <title>Cell 3 · $7,310</title>
          </g>
          <!-- … +47 elemento(s) iguais gerados pelo JS -->
        </svg>
      </div>
    </div>
    <button class="widget-filter-trigger" type="button" data-widget-filter="smallHexFlow" aria-label="Filter Sales Report" aria-expanded="false">
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
/* Faixa de KPIs com 3 cards no painel e valor na cor de texto do tema */
.widgets-grid.horizontal-small-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.compact-widget-metric strong { color: var(--ttsc-text); }
.compact-widget-change { color: var(--ttsc-accent-text); }
```

### JS

Definições, montagem e render reais em `widgets.js`:

```js
const compactWidgetDefinitions = [
  { id: 'smallWaterfallPurple', label: 'Waterfall chart', kind: 'waterfall', colors: ['#8b5cf6', '#bd8cff'] },
  { id: 'smallWaterfallAmber', label: 'Waterfall chart', kind: 'waterfall', colors: ['#f59e0b', '#ffc247'] },
  { id: 'smallGroupedColumns', label: 'Grouped bar chart', kind: 'groupedColumns', colors: ['#7c3aed', '#f43f8e', '#f59e0b', '#06b6d4'] },
  { id: 'smallGroupedHorizontal', label: 'Grouped bar chart', kind: 'groupedHorizontal', colors: ['#7c3aed', '#f43f8e', '#f59e0b'] },
  { id: 'smallStackedHorizontal', label: 'Stacked horizontal bar', kind: 'stackedHorizontal', colors: ['#6d5dfc', '#c4b5fd'] },
  { id: 'smallBasicGreen', label: 'Basic bar', kind: 'columns', colors: ['#22c55e', '#bbf7d0'] },
  { id: 'smallBasicSpectrum', label: 'Basic bar', kind: 'columns', colors: ['#10b981', '#38bdf8', '#6366f1'] },
  { id: 'smallDetailedBars', label: 'Detailed bar chart', kind: 'columns', colors: ['#22c55e'] },
  { id: 'smallRainfall', label: 'Rainfall', kind: 'rainfall', colors: ['#f59e0b', '#06b6d4', '#8b5cf6'] },
  { id: 'smallSparseBars', label: 'Basic bar', kind: 'sparseColumns', colors: ['#8b5cf6', '#d8b4fe'] },
  { id: 'smallBubbles', label: 'Bubble bar chart', kind: 'bubbles', colors: ['#f59e0b', '#fb923c'] },
  { id: 'smallStackedColumns', label: 'Stacked columns', kind: 'stackedColumns', colors: ['#f97316', '#8b5cf6'] },
  { id: 'smallDenseBars', label: 'Detailed bar chart', kind: 'denseColumns', colors: ['#22c55e', '#86efac'] },
  { id: 'smallLineColumns', label: 'Line and column chart', kind: 'lineColumns', colors: ['#8b5cf6', '#fbbf24'] },
  { id: 'smallGradientBars', label: 'Detailed bar chart', kind: 'gradientColumns', colors: ['#6366f1', '#f59e0b', '#22c55e'] },
  { id: 'smallHexFlow', label: 'Hex heatmap', kind: 'heatmap', visual: 'hexFlow' },
  { id: 'smallHexRadial', label: 'Hex heatmap', kind: 'heatmap', visual: 'hexRadial' },
  { id: 'smallBasicHeatmap', label: 'Basic heatmap', kind: 'heatmap', visual: 'basic' },
  { id: 'smallHeatmapIndicator', label: 'Heatmap indicator', kind: 'heatmap', visual: 'indicator' },
  { id: 'smallGradientHeatmap', label: 'Gradient heatmap', kind: 'heatmap', visual: 'gradient' },
  { id: 'smallScatter', label: 'Bubble scatter', kind: 'scatter', colors: ['#8b5cf6', '#c4b5fd'] },
  { id: 'smallGauge', label: 'Radial gauge', kind: 'gauge', colors: ['#14d6b1', '#facc15', '#ec4899', '#7c3aed'] },
  { id: 'smallGreenSparkline', label: 'Area sparkline', kind: 'sparkline', colors: ['#22c55e'] },
  { id: 'smallDotIndicator', label: 'Dot indicator', kind: 'dotIndicator', colors: ['#f97316', '#fed7aa'] }
];
```

```js
function mountCompactWidgets() {
  const grid = byId('horizontal-small-grid');
  if (!grid) return;
  grid.innerHTML = compactWidgetDefinitions.map(widget => `<div class="compact-widget-item"><div class="compact-widget-label">: ${widget.label}</div><article class="ttsc-analytics-card widget demo-widget compact-widget-card" data-widget="${widget.id}" aria-label="${widget.label} compact widget"><div class="compact-widget-body"><div class="compact-widget-metric"><h3>Sales Report</h3><strong id="${widget.id}-value">$9,134</strong><span class="compact-widget-change">↗ 2.5%</span><small id="${widget.id}-caption">Avg. score $185,301</small></div><div class="compact-widget-chart-slot" id="${widget.id}-chart"></div></div></article></div>`).join('');
}
```

```js
function renderCompactWidget(widget) {
  const index = Math.max(0, Math.min(compactWidgetValues.length - 1, state[widget.id].selectedPoint));
  byId(`${widget.id}-value`).textContent = fmtMoney(widget.kind === 'heatmap' ? heatmapValue(index) : compactWidgetValues[index], 0);
  byId(`${widget.id}-caption`).textContent = `${months[index]} · selected sample`;
  byId(`${widget.id}-chart`).innerHTML = compactChartSvg(widget);
}
```

```js
function compactPoint(widget, index, shape) {
  const value = compactWidgetValues[index % compactWidgetValues.length];
  const selected = state[widget.id].selectedPoint === index;
  return `<g class="compact-chart-mark${selected ? ' is-selected' : ''}" role="button" tabindex="0" data-small-widget="${widget.id}" data-small-point="${index}" aria-pressed="${selected}" aria-label="${months[index % 12]}: ${fmtMoney(value, 0)}">${shape}<title>${months[index % 12]} · ${fmtMoney(value, 0)}</title></g>`;
}
```

Início do gerador por tipo (`compactChartSvg`), para localizar onde cada `kind` é desenhado:

```js
function compactChartSvg(widget) {
  if (widget.kind === 'heatmap') return heatmapSvg(widget, 112, 62);
  if (widget.kind === 'scatter') {
    const dots = Array.from({ length: 24 }, (_, index) => {
      const x = 5 + (index * 17 % 68) + Math.sin(index * 1.9) * 4;
      const y = 8 + (index * 23 % 39) + Math.cos(index * 1.1) * 3;
  // … um ramo por kind (waterfall, groupedColumns, …, dotIndicator)
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

// payload = { series: { received: [{ month, value }], presence: [{ iso_week, weekday_index, presence_rate }] } }
loadSection('.horizontal-small-section', compactWidgetDefinitions, (definition, payload) =>
  definition.kind === 'heatmap'
    ? (payload.series?.presence ?? []).map(cell => Number(cell.presence_rate) || 0)
    : (payload.series?.received ?? []).map(row => Number(row.value) || 0));
```

CSV: `downloadCsv()` não tem ramo para os widgets de seção (o menu “Download CSV” não existe nesses cards). Para exportar, use a exportação da página de origem dos dados (`GET /api/v1/domain/records{rota}/export?format=csv|xlsx|pdf|json|xml|sql`).

### SQL

Duas formas de dado cobrem os 24 tipos: uma série curta (7 meses de recebimento, `billing_payments`) para barras/linhas/medidor e uma matriz semana × dia (presença em `attendance`, status `present`/`late`) para os heatmaps. Testadas no MariaDB local.

```sql
-- (a) Série de 7 pontos para os cards de barras/linha: recebido por mês (baixas de faturas)
SELECT DATE_FORMAT(bp.paid_at, '%Y-%m') AS month, SUM(bp.net_amount) AS value
  FROM billing_payments bp
 WHERE bp.paid_at >= DATE_FORMAT(CURDATE() - INTERVAL 6 MONTH, '%Y-%m-01')
 GROUP BY DATE_FORMAT(bp.paid_at, '%Y-%m')
 ORDER BY month;

-- (b) Células dos heatmaps: taxa de presença por semana × dia da semana (últimas 8 semanas)
SELECT YEARWEEK(a.lesson_date, 3)                                         AS iso_week,
       WEEKDAY(a.lesson_date)                                             AS weekday_index,
       ROUND(SUM(a.status IN ('present', 'late')) / COUNT(*) * 100, 1)    AS presence_rate,
       COUNT(*)                                                           AS records
  FROM attendance a
 WHERE a.lesson_date >= CURDATE() - INTERVAL 8 WEEK
 GROUP BY YEARWEEK(a.lesson_date, 3), WEEKDAY(a.lesson_date)
 ORDER BY iso_week, weekday_index;
```

O provider devolve as duas listas; o JS escolhe por `kind`. Meses ou células sem registro devem chegar com 0 para manter a posição das marcas.

## Faça / Não faça

- **Faça:** dar a cada card um indicador e uma unidade explícitos;
- **Faça:** manter o valor do ponto selecionado em texto.
- **Não faça:** deixar “Sales Report”/“↗ 2.5%” fixos do modelo em produção;
- **Não faça:** usar heatmap compacto para menos de ~20 células.
