# WidgetMarket

Card largo de série de preço/saldo: valor atual com variação, três visões (linha, colunas de desvio da média, candles OHLC) e cinco intervalos (24 H, 1W, 1M, 1Y, ALL) em SVG com seleção de ponto.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só o card `marketChart` (largo). Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Mostrar a evolução diária de um valor com abertura/máxima/mínima/fechamento — no TotusTuus, o saldo de uma conta bancária (`banks_transactions.balance_before/after`).
- Quando o usuário precisa alternar granularidade e forma (linha × candles) no próprio card.
- Para séries mensais simples use [WidgetBalance](../WidgetBalance/README.md) ou [WidgetIncomeStatistics](../WidgetIncomeStatistics/README.md).

## Anatomia

```
┌ ícone · Bitcoin USD (BTC-USD)                             [⋯] ┐
│ $23,097.00 (↗ 3.4%) vs $22,330 · last 7 days                   │  #market-price-value / -change / -context
│ [Line][Column][Japanese candles]      [24 H][1W][1M][1Y][ALL]  │  data-market-view / data-market-range
│  ▕▏ ▕█▏ ▕▏  (Max $23,240)  …  (Min $21,580)                    │  svg#market-price-chart (1100×430)
│ 12 Oct – 18 Oct · 1 week                Range $…–$…            │
└────────────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Card largo | `article.widget-wide.market-chart-widget[data-widget="marketChart"]` | sim |
| Resumo | `.market-price-summary` > `#market-price-value`, `.metric-change#market-price-change`, `#market-change-context` | sim |
| Barra de ferramentas | `.market-chart-toolbar` > `.market-view-toggle` (`button[data-market-view]`) + `.market-range-toggle` (`button[data-market-range]`), ambos com `aria-pressed` | sim |
| Gráfico | `.market-chart-plot > svg#market-price-chart[role="img"]` (grade, `g[data-market-point][role="button"][tabindex="0"]`, `.market-callout`) | sim |
| Rodapé | `.market-chart-foot` (`#market-chart-range-label`, `#market-chart-high-low`) | sim |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('marketChart')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Sem diálogo de configurações: os controles do próprio card gravam em `state.marketChart` e re-renderizam só este widget; “Reset widget” volta aos padrões. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Ponto selecionado | `state.marketChart.selectedIndex`: faixa `.market-selection-band` e coluna `.is-selected`. |
| Extremos | Na visão coluna, máxima e mínima recebem `.is-extreme` e pílulas “Max/Min”. |
| Candles | `.market-candle.is-rising` / `.is-falling`. |

## API

### Dados esperados

Série diária OHLC e, para 24 H, uma série horária de 24 pontos. Sem diálogo: visão e intervalo são botões no card.

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `date` | `Date` | UTC | Dia (ou hora em 24 H). |
| `open`, `high`, `low`, `close` | `number` | moeda | OHLC do período. |
| `volume` | `number` | contagem | Exportado no CSV (`volume_btc` na amostra). |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js

marketHourly: buildMarketHourly(marketDaily)
```

### Configurações do widget

_Este widget não tem diálogo de configurações; os controles ficam no próprio card (ver atributos abaixo)._

### Atributos `data-*`

| Atributo | Onde / efeito |
|---|---|
| `data-widget` | No `<article>`: chave do widget em `state`/`renderWidget()`; também é o alvo do filtro e do observador de renderização preguiçosa. |
| `data-menu` | Botão “mais ações”: alterna o `.widget-menu` irmão e `aria-expanded`. |
| `data-download` | Item do menu: chama `downloadCsv(widget)`. |
| `data-reset` | Item do menu: restaura os padrões do widget e chama `renderWidget(widget)`. |
| `data-tip` | Texto do tooltip comum (`#widget-tooltip`) em hover/foco. |
| `data-change-value` | Span que `setChange()` preenche com a variação percentual. |
| `data-market-view` | `line` \| `column` \| `candles` → `state.marketChart.view`. |
| `data-market-range` | `24h` \| `1w` \| `1m` \| `1y` \| `all` → `state.marketChart.range` (zera a seleção). |
| `data-market-point` | Gerado: índice do ponto; clique/Enter seleciona. |
| `data-widget-filter` | Criado pelo JS (`addFilterAction`): botão “Filter” no canto do card, abre a gaveta `#widget-filter-drawer` com busca e faixa mín./máx. |

### Funções e eventos

| Função / evento | O que faz |
|---|---|
| `renderMarketChart()` | Escala, grade, visão escolhida, pílulas, textos e `aria-label` com último preço, variação, máxima, mínima e seleção. |
| `marketRangeRows()` | Recorta a série pelo intervalo. |
| `marketDateLabel(date, range)` | Rótulo de eixo (`en-GB`, UTC). |
| `marketPill(...)` | Pílula Max/Min posicionada dentro da área. |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- Não há rota de domínio que agregue `banks_transactions` por dia; a view `inst_banks_transactions` (com `counterparty_name`, `category`, `type`, `amount`) é a fonte de leitura do módulo Bancos. Exponha as consultas abaixo num provider desse módulo, com a permissão da página de transações bancárias e o filtro de `tenant_id` que o `BanksController` já aplica. Resposta: `{ "rows": [{ "date", "open", "high", "low", "close", "volume" }] }` por conta (`?account=<uuid>&days=7|30|365`).

## Acessibilidade

- Cada coluna/candle/ponto é `role="button"` focável com `aria-label` (data e valores OHLC); `Enter` seleciona via o tratador global.
- Os grupos de botões têm `role="group"` + `aria-label` e `aria-pressed` no ativo.
- O `<article>` usa `aria-labelledby` apontando para o `<h2>` do título; o gráfico tem `role="img"` (ou `role="group"`) e um `aria-label` que o render **reescreve com os valores atuais** — mantenha isso ao trocar a fonte de dados.
- Diálogos de configuração são `<dialog>` nativos abertos com `showModal()` (foco preso, `Esc` fecha); o rótulo vem de `aria-labelledby`.
- Menu “mais ações”: `aria-expanded` sincronizado, fecha com `Esc` ou clique fora.
- Tooltip comum `#widget-tooltip` (`role="tooltip"`) abre em hover **e** em foco (`focusin`), lendo `data-tip`/`aria-label`/`<title>` da marca.
- Toast `#widget-toast` é `role="status"` + `aria-live="polite"`.
- Ao localizar, traduza também os textos gerados pelo JS (rótulos de `aria-label`, “sample”, “vs prior month”) e use `Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' })` no lugar de `fmtMoney` (que é `en-US`/USD).

## Modelos

### HTML

**1. Na view PHP.** Não existe partial do chassi para widgets: `resources/views/app/partials/chassis/*` e `dashboard.php` não emitem `data-widget`. A integração é colar o `<article>` aprovado numa view Plates do módulo, protegida pela mesma permissão da página, e informar ao provider a URL dos dados:

```php
<?php
// mesmo helper de escape de partials/chassis/domain_page.php
$e = static fn ($v) => htmlspecialchars((string) $v, ENT_QUOTES, 'UTF-8');
$endpoint = '/banks/accounts/widgets/balance-ohlc?account=' . rawurlencode($accountUuid) /* rota do provider, a criar */;
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="marketChart"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="marketChart-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget widget-wide market-chart-widget" data-widget="marketChart" aria-labelledby="market-chart-title">
  <header class="ttsc-analytics-head widget-head market-chart-header">
    <div class="widget-heading">
      <span class="widget-icon tone-blue" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="market-chart-title">Bitcoin USD (BTC-USD)</h2>
          <button class="info-button" type="button" data-tip="Illustrative BTC/USD daily and hourly OHLC data. Price and period change are calculated from the selected range." aria-label="About Bitcoin market chart">
            i
          </button>
        </div>
        <p id="market-chart-subtitle">Market price · sample data</p>
      </div>
    </div>
    <div class="widget-actions">
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" aria-label="More Bitcoin chart actions" aria-expanded="false" data-menu="marketChart">
          <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="marketChart">Download CSV</button>
          <button type="button" data-reset="marketChart">Reset chart</button>
        </div>
      </div>
    </div>
  </header>
  <div class="market-price-summary">
    <strong id="market-price-value"></strong>
    <span class="metric-change is-positive" id="market-price-change">
      <svg viewBox="0 0 16 16" aria-hidden="true">…</svg>
      <span data-change-value></span>
    </span>
    <span class="metric-context" id="market-change-context"></span>
  </div>
  <div class="market-chart-toolbar">
    <div class="market-view-toggle" role="group" aria-label="Chart style">
      <button type="button" data-market-view="line" aria-pressed="false">
        <svg viewBox="0 0 20 20">…</svg>
        <span>Line</span>
      </button>
      <button type="button" data-market-view="column" aria-pressed="true">
        <svg viewBox="0 0 20 20">…</svg>
        <span>Column</span>
      </button>
      <button type="button" data-market-view="candles" aria-pressed="false">
        <svg viewBox="0 0 20 20">…</svg>
        <span>Japanese candles</span>
      </button>
    </div>
    <div class="market-range-toggle" role="group" aria-label="Price range">
      <button type="button" data-market-range="24h" aria-pressed="false">24 H</button>
      <button type="button" data-market-range="1w" aria-pressed="true">1W</button>
      <!-- … +3 elemento(s) iguais gerados pelo JS -->
    </div>
  </div>
  <div class="market-chart-plot">
    <svg id="market-price-chart" viewBox="0 0 1100 430" role="img" aria-label="Bitcoin USD column chart for the last week"></svg>
  </div>
  <footer class="ttsc-analytics-foot widget-foot market-chart-foot">
    <span id="market-chart-range-label">12 Oct – 18 Oct · 1 week</span>
    <span><i class="market-legend-dot"></i> BTC-USD <span id="market-chart-high-low"></span></span>
  </footer>
</article>
```

### CSS

Arquivos: `ttsc.analytics-panels.css` (`.ttsc-analytics-card`, `-head`, `-plot`, `-foot`, `-empty`) + `docs/model/widgets/widgets.css` (layout e regras deste widget). O tema escuro de `widgets.css` é `html[data-theme="dark"]` (redefine `--w-surface`, `--w-text`, `--w-border`, `--w-grid`…); o de `ttsc.analytics-panels.css` é `html.dark` — `TTSCModelKit.syncTheme()` mantém os dois em sincronia.

Regras reais deste widget em `widgets.css`:

```css
.market-widgets-grid { grid-template-columns: minmax(0, 1fr); margin-top: 16px; }
.market-chart-widget { min-width: 0; grid-column: auto; }
.market-chart-header { align-items: center; }
.market-price-summary { display: flex; min-height: 48px; align-items: center; gap: 12px; margin: -3px 0 8px 42px; }
.market-price-summary > strong { color: var(--w-text); font-size: 30px; font-variant-numeric: tabular-nums; font-weight: 600; letter-spacing: -.045em; }
.market-price-summary .metric-change { background: transparent; border: 0; font-size: 14px; }
.market-price-summary .metric-change > svg { width: 15px; height: 15px; }
.market-price-summary .metric-context { font-size: 10px; }
.market-chart-toolbar { display: flex; align-items: center; justify-content: space-between; gap: 14px; margin: 2px 0 14px 42px; }
.market-view-toggle, .market-range-toggle { display: inline-flex; max-width: 100%; align-items: center; gap: 2px; padding: 3px; border-radius: 12px; background: var(--w-canvas); }
.market-view-toggle button, .market-range-toggle button { display: inline-flex; min-height: 34px; align-items: center; justify-content: center; gap: 7px; padding: 0 13px; border: 1px solid transparent; border-radius: 9px; background: transparent; /* … */ }
.market-view-toggle button[aria-pressed="true"], .market-range-toggle button[aria-pressed="true"] { border-color: var(--w-border); background: var(--w-surface); box-shadow: 0 1px 3px rgb(15 23 42 / .08); color: var(--w-text); font-weight: 600; }
.market-view-toggle button:hover, .market-range-toggle button:hover { color: var(--w-text); }
.market-view-toggle svg { width: 16px; height: 16px; fill: none; stroke: currentColor; stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }
.market-range-toggle button { min-width: 48px; padding: 0 12px; }
.market-chart-plot { height: clamp(290px, 38vw, 430px); min-height: 290px; border-top: 1px solid var(--w-grid); }
.market-chart-plot svg { display: block; width: 100%; height: 100%; overflow: visible; }
.market-gridline { stroke: var(--w-grid); stroke-width: 1; }
.market-gridline-vertical { stroke-opacity: .72; }
.market-axis-value, .market-axis-date { fill: var(--w-muted); font: 10px var(--ttsc-font-sans, Inter, sans-serif); }
.market-axis-value { text-anchor: end; }
.market-axis-date { text-anchor: middle; }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Candles e seleção com tokens semânticos */
.market-candle.is-rising  { color: var(--ttsc-success); }
.market-candle.is-falling { color: var(--ttsc-danger); }
.market-selection-band { fill: var(--ttsc-accent-soft); }
```

### JS

Render real em `widgets.js`:

```js
function marketRangeRows() {
  const range = state.marketChart.range;
  if (range === '24h') return data.marketHourly;
  if (range === '1w') return data.marketDaily.slice(-7);
  if (range === '1m') return data.marketDaily.slice(-30);
  if (range === '1y') return data.marketDaily.slice(-365);
  return data.marketDaily;
}
```

```js
function renderMarketChart() {
  const rows = marketRangeRows();
  const { range, view } = state.marketChart;
  const current = rows[rows.length - 1];
  const firstValue = range === '24h' ? rows[0].open : rows[0].close;
  const change = percentChange(current.close, firstValue);
  const high = Math.max(...rows.map(row => row.high));
  const low = Math.min(...rows.map(row => row.low));
  const highIndex = rows.findIndex(row => row.high === high);
  const lowIndex = rows.findIndex(row => row.low === low);
  const minPrice = low - (high - low) * .08;
  const maxPrice = high + (high - low) * .08;
  const width = 1100, height = 430, left = 62, right = 1080, top = 20, bottom = 374;
  const plotHeight = bottom - top;
  const slot = (right - left) / rows.length;
  const xFor = index => left + (index + .5) * slot;
  const yFor = value => bottom - (value - minPrice) / (maxPrice - minPrice) * plotHeight;
  const selectedIndex = Math.max(0, Math.min(rows.length - 1, state.marketChart.selectedIndex ?? Math.floor(rows.length / 2)));
  state.marketChart.selectedIndex = selectedIndex;
  const selectedX = xFor(selectedIndex);
  const bandWidth = Math.max(10, Math.min(slot, 150));
  const selectedBand = `<rect class="market-selection-band" x="${(selectedX - bandWidth / 2).toFixed(1)}" y="${top}" width="${bandWidth.toFixed(1)}" height="${plotHeight}"/>`;
  const grid = Array.from({ length: 5 }, (_, index) => {
    const ratio = index / 4;
    const y = top + plotHeight * ratio;
    const value = maxPrice - (maxPrice - minPrice) * ratio;
    return `<line class="market-gridline" x1="${left}" y1="${y.toFixed(1)}" x2="${right}" y2="${y.toFixed(1)}"/><text class="market-axis-value" x="${left - 10}" y="${(y + 3).toFixed(1)}">${fmtCompact(value)}</text>`;
  }).join('');
  const verticalGrid = Array.from({ length: 7 }, (_, index) => {
    const x = left + (right - left) * index / 6;
    const rowIndex = Math.min(rows.length - 1, Math.round((rows.length - 1) * index / 6));
    return `<line class="market-gridline market-gridline-vertical" x1="${x.toFixed(1)}" y1="${top}" x2="${x.toFixed(1)}" y2="${bottom}"/><text class="market-axis-date" x="${x.toFixed(1)}" y="${height - 8}">${marketDateLabel(rows[rowIndex].date, range)}</text>`;
  }).join('');
  let chart = '';
  if (view === 'line') {
    const points = rows.map((row, index) => ({ x: xFor(index), y: yFor(row.close) }));
    const path = smoothBoundary(points);
    const area = `${path} L ${right} ${bottom} L ${left} ${bottom} Z`;
    const selected = points[selectedIndex];
    const hitTargets = points.map((point, index) => `<g data-market-point="${index}" tabindex="0" role="button" aria-label="${marketDateLabel(rows[index].date, range)}: ${fmtMoney(rows[index].close)}"><title>${marketDateLabel(rows[index].date, range)} · ${fmtMoney(rows[index].close)}</title><circle class="market-line-hit" cx="${point.x.toFixed(1)}" cy="${point.y.toFixed(1)}" r="${Math.max(7, Math.min(15, slot / 2))}"/></g>`).join('');
    chart = `<defs><linearGradient id="market-line-fill" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#35b8db" stop-opacity=".25"/><stop offset="1" stop-color="#35b8db" stop-opacity="0"/></linearGradient></defs><path d="${area}" fill="url(#market-line-fill)"/><path class="market-line-path" d="${path}"/><circle class="market-selected-point" cx="${selected.x.toFixed(1)}" cy="${selected.y.toFixed(1)}" r="5"/>${hitTargets}`;
  } else if (view === 'column') {
    const average = mean(rows.map(row => row.close));
    const maxDelta = Math.max(...rows.map(row => Math.abs(row.close - average)), 1);
    const baseline = yFor(average);
    const barWidth = Math.max(2, Math.min(19, slot * .6));
    const bars = rows.map((row, index) => {
      const deviation = row.close - average;
      const barHeight = Math.max(2, Math.abs(deviation) / maxDelta * plotHeight * .42);
      const x = xFor(index) - barWidth / 2;
      const y = deviation >= 0 ? baseline - barHeight : baseline;
      const tone = index === selectedIndex ? ' is-selected' : index === highIndex || index === lowIndex ? ' is-extreme' : '';
      return `<g data-market-point="${index}" tabindex="0" role="button" aria-label="${marketDateLabel(row.date, range)}: ${fmtMoney(row.close)}"><title>${marketDateLabel(row.date, range)} · ${fmtMoney(row.close)} · H ${fmtMoney(row.high)} · L ${fmtMoney(row.low)}</title><rect class="market-column${tone}" x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${barWidth.toFixed(1)}" height="${barHeight.toFixed(1)}" rx="${Math.min(6, barWidth / 2).toFixed(1)}"/></g>`;
    }).join('');
    const highY = yFor(high), lowY = yFor(low);
    chart = `<line class="market-reference-line" x1="${left}" y1="${baseline.toFixed(1)}" x2="${right}" y2="${baseline.toFixed(1)}"/>${selectedBand}${bars}<line class="market-extreme-line" x1="${xFor(highIndex).toFixed(1)}" y1="${top + 8}" x2="${xFor(highIndex).toFixed(1)}" y2="${highY.toFixed(1)}"/><line class="market-extreme-line" x1="${xFor(lowIndex).toFixed(1)}" y1="${lowY.toFixed(1)}" x2="${xFor(lowIndex).toFixed(1)}" y2="${bottom - 8}"/>${marketPill(xFor(highIndex), Math.max(top + 4, highY - 42), 'Max', high, left, right, top, bottom)}${marketPill(xFor(lowIndex), Math.min(bottom - 30, lowY + 13), 'Min', low, left, right, top, bottom)}`;
  } else {
    const candles = rows.map((row, index) => {
      const x = xFor(index), candleWidth = Math.max(2, Math.min(15, slot * .55));
      const rising = row.close >= row.open;
      const bodyTop = yFor(Math.max(row.open, row.close));
      const bodyBottom = yFor(Math.min(row.open, row.close));
      const bodyHeight = Math.max(2, bodyBottom - bodyTop);
      const tone = rising ? 'is-rising' : 'is-falling';
      return `<g class="market-candle ${tone}" data-market-point="${index}" tabindex="0" role="button" aria-label="${marketDateLabel(row.date, range)}: O ${fmtMoney(row.open)}, H ${fmtMoney(row.high)}, L ${fmtMoney(row.low)}, C ${fmtMoney(row.close)}"><title>${marketDateLabel(row.date, range)} · O ${fmtMoney(row.open)} · H ${fmtMoney(row.high)} · L ${fmtMoney(row.low)} · C ${fmtMoney(row.close)}</title><line x1="${x.toFixed(1)}" y1="${yFor(row.high).toFixed(1)}" x2="${x.toFixed(1)}" y2="${yFor(row.low).toFixed(1)}"/><rect x="${(x - candleWidth / 2).toFixed(1)}" y="${bodyTop.toFixed(1)}" width="${candleWidth.toFixed(1)}" height="${bodyHeight.toFixed(1)}" rx="1"/></g>`;
    }).join('');
    chart = `${selectedBand}${candles}`;
  }
  const selected = rows[selectedIndex];
  const rangeLabel = range === '24h' ? 'Last 24 hours' : range === '1w' ? 'Last 7 days' : range === '1m' ? 'Last 30 days' : range === '1y' ? 'Last 12 months' : 'All available history';
  const firstDate = marketDateLabel(rows[0].date, range), lastDate = marketDateLabel(rows.at(-1).date, range);
  byId('market-price-value').textContent = fmtMoney(current.close);
  setChange(byId('market-price-change'), change);
  byId('market-change-context').textContent = `vs ${fmtMoney(firstValue)} · ${rangeLabel.toLowerCase()}`;
  byId('market-chart-subtitle').textContent = `${view === 'candles' ? 'OHLC' : view === 'column' ? 'Price movement' : 'Closing price'} · ${rows.length} ${range === '24h' ? 'hourly' : 'daily'} points`;
  byId('market-chart-range-label').textContent = `${firstDate} – ${lastDate} · ${rangeLabel}`;
  byId('market-chart-high-low').textContent = `Range ${fmtMoney(low)}–${fmtMoney(high)}`;
  byId('market-price-chart').innerHTML = `${grid}${verticalGrid}${chart}`;
  byId('market-price-chart').setAttribute('aria-label', `Bitcoin USD ${view} chart for ${rangeLabel}. Last price ${fmtMoney(current.close)}, ${change >= 0 ? 'up' : 'down'} ${Math.abs(change).toFixed(1)} percent. High ${fmtMoney(high)}; low ${fmtMoney(low)}. Selected ${marketDateLabel(selected.date, range)} at ${fmtMoney(selected.close)}.`);
  document.querySelectorAll('[data-market-range]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.marketRange === range)));
  document.querySelectorAll('[data-market-view]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.marketView === view)));
}
```

Trocando a amostra pelo endpoint (o README de `docs/model/widgets` exige: provider autorizado do módulo, mesma semântica de campos, formatação, unidades, estados e configurações isoladas):

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

// rows = [{ date: '2026-10-15', open: '21700.00', high: '21980.00', low: '21510.00', close: '21808.00', volume: 34 }, …]
loadWidget('marketChart', rows => {
  data.marketDaily = rows.map(row => ({
    date: new Date(`${row.date}T00:00:00Z`),
    open: Number(row.open), high: Number(row.high), low: Number(row.low), close: Number(row.close), volume: Number(row.volume) || 0,
  }));
  data.marketHourly = data.marketDaily.slice(-24);   // sem série horária: troque o botão 24 H por outro intervalo ou remova-o
  return data.marketDaily.length >= 2;              // o render usa rows[0] e o último ponto
});
```

O menu “Download CSV” chama `downloadCsv('marketChart')`, que serializa a **série de amostra** (`marketChart-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

OHLC diário do saldo de uma conta: abertura = `balance_before` do primeiro lançamento do dia, fechamento = `balance_after` do último (`FIRST_VALUE … OVER`), máxima/mínima sobre `balance_after`, volume = nº de lançamentos. Testado no MariaDB local; funções de janela existem em MariaDB 10.2+ e MySQL 8.

```sql
-- OHLC diário do saldo de uma conta bancária (abertura, máxima, mínima, fechamento, nº de lançamentos)
SELECT d.day                         AS date,
       MAX(d.open_balance)           AS open,
       MAX(d.balance_after)          AS high,
       MIN(d.balance_after)          AS low,
       MAX(d.close_balance)          AS close,
       COUNT(*)                      AS volume
  FROM (
        SELECT t.transaction_date AS day, t.balance_after,
               FIRST_VALUE(t.balance_before) OVER (PARTITION BY t.transaction_date ORDER BY t.created_at, t.id) AS open_balance,
               FIRST_VALUE(t.balance_after)  OVER (PARTITION BY t.transaction_date ORDER BY t.created_at DESC, t.id DESC) AS close_balance
          FROM banks_transactions t
         WHERE t.tenant_id = :tenant_id
           AND t.account_id = :account_id
           AND t.status NOT IN ('reversed', 'failed', 'cancelled')
           AND t.transaction_date >= CURDATE() - INTERVAL :days DAY     -- 1w = 7, 1m = 30, 1y = 365
       ) d
 GROUP BY d.day
 ORDER BY d.day;
```

Dias sem lançamento não aparecem; para candles contínuos, repita o fechamento anterior no PHP. O rótulo “Bitcoin USD” do `aria-label` é fixo no render — troque pelo nome da conta na cópia de produção.

## Faça / Não faça

- **Faça:** garantir pelo menos 2 pontos por intervalo;
- **Faça:** trocar textos fixos (“Bitcoin USD”) pelos do domínio.
- **Não faça:** oferecer 24 H sem série horária real;
- **Não faça:** usar candles para dados sem abertura/fechamento.
