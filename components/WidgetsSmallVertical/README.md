# WidgetsSmallVertical

Seção “Vertical small widgets”: 21 cards compactos em coluna — título, valor, variação e mini-gráfico abaixo (cascata, barras, chuva, heatmaps, fluxo de receita), alguns com bloco de detalhes.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só a seção `.vertical-small-section` (o script do preview recebe `section = ".vertical-small-section"` em vez de uma lista de widgets). Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Grades de painel em que o gráfico precisa de mais altura que largura (colunas mensais, heatmaps semanais).
- Cards “Income”/“Sales Report” resumidos em painéis de diretoria.
- Para a versão horizontal (faixa de KPIs) veja [WidgetsSmallHorizontal](../WidgetsSmallHorizontal/README.md); com configurações e menu, use os widgets individuais.

## Anatomia

```
.vertical-widget-item
  .vertical-widget-label ": Waterfall chart"
  article.vertical-widget-card[data-widget]
    ┌ Income                      ⋮ ┐  .vertical-widget-head
    │ $32,134                       │  #<id>-value
    │ ↑ 2.5%  301,982 USD           │  .vertical-widget-change
    │ ▂▅▃█▆▇▄▆  (SVG)               │  #<id>-chart
    └───────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Seção | `section.vertical-small-section` | sim |
| Grade | `#vertical-small-grid` | sim |
| Card | `article…vertical-widget-card[data-widget]` | sim |
| Cabeçalho | `header.vertical-widget-head` (título, `.vertical-widget-spark` em “Sales Report”, `.vertical-widget-dots` decorativo) | sim |
| Valor | `.vertical-widget-value#<id>-value` + `.vertical-widget-change` | sim |
| Gráfico | `#<id>-chart` > `svg.vertical-widget-chart` | sim |
| Detalhes | Bloco extra quando `details: true` | não |

## Variantes

21 tipos de widget, gerados de `verticalWidgetDefinitions` em `widgets.js` (mesma ordem do catálogo):

| # | Widget (`data-widget`) | Nome no catálogo | Tipo | Visual | Quando usar |
|---|---|---|---|---|---|
| 1 | `verticalWaterfallPurple` | Waterfall chart | `waterfall` | Cascata: barras flutuantes de variação acumulada | Explicar como o saldo do mês chegou ao valor final (entradas e saídas). |
| 2 | `verticalWaterfallAmber` | Waterfall chart | `waterfall` | Cascata: barras flutuantes de variação acumulada | Explicar como o saldo do mês chegou ao valor final (entradas e saídas). |
| 3 | `verticalGroupedColumns` | Grouped bar chart | `groupedColumns` | Colunas agrupadas (3–4 séries por período) | Comparar séries no mesmo período (ex.: pago × aberto × vencido por mês). |
| 4 | `verticalGroupedHorizontal` | Grouped bar chart | `groupedHorizontal` | Barras horizontais agrupadas | Comparar séries por categoria com rótulos longos (cursos, campus). |
| 5 | `verticalStackedHorizontal` | Stacked horizontal bar | `stackedHorizontal` | Barra horizontal empilhada (parte × restante) | Mostrar parte de um total por linha (meta atingida, ocupação). |
| 6 | `verticalBasicGreen` | Basic bar | `columns` | Colunas simples com destaque do ponto selecionado | Série curta de um único indicador (recebido por mês). |
| 7 | `verticalBasicSpectrum` | Basic bar | `columns` | Colunas simples com destaque do ponto selecionado | Série curta de um único indicador (recebido por mês). |
| 8 | `verticalDetailedBars` | Detailed bar chart | `denseColumns` | Colunas finas e densas (detalhe diário) | Até ~30 pontos, leitura de tendência e picos. |
| 9 | `verticalRainfall` | Column rainfall | `rainfall` | Colunas “chuva” finas e coloridas por faixa | Série densa diária em pouco espaço. |
| 10 | `verticalSparseBars` | Basic bar | `sparseColumns` | Colunas espaçadas com trilha de fundo | Poucos pontos (5–7) com ênfase no valor relativo. |
| 11 | `verticalBubbles` | Bubble bar chart | `bubbles` | Barras em bolhas (pontos empilhados) | Contagens pequenas (eventos, ocorrências) por período. |
| 12 | `verticalStackedColumns` | Stacked columns | `stackedColumns` | Colunas empilhadas em duas séries | Total por período e a composição entre duas partes. |
| 13 | `verticalDenseBars` | Detailed bar chart | `denseColumns` | Colunas finas e densas (detalhe diário) | Até ~30 pontos, leitura de tendência e picos. |
| 14 | `verticalLineColumns` | Line and column chart | `lineColumns` | Colunas + linha sobreposta | Volume (colunas) contra uma taxa ou média (linha). |
| 15 | `verticalGradientBars` | Detailed bar chart | `gradientColumns` | Colunas com gradiente por intensidade | Destacar picos dentro da série. |
| 16 | `verticalHexFlow` | Hex heatmap | `heatmap` | Heatmap hexagonal em fluxo | Intensidade por período × faixa (semana × dia). |
| 17 | `verticalHexRadial` | Hex heatmap | `heatmap` | Heatmap hexagonal radial | Intensidade concentrada em torno de um centro (picos). |
| 18 | `verticalBasicHeatmap` | Basic heatmap | `heatmap` | Heatmap de grade básico | Matriz semana × dia da semana (presença, atendimentos). |
| 19 | `verticalHeatmapIndicator` | Heatmap indicator | `heatmap` | Heatmap indicador (linhas por item) | Intensidade por item (cidade, campus) ao longo do tempo. |
| 20 | `verticalGradientHeatmap` | Gradient heatmap | `heatmap` | Heatmap com gradiente contínuo | Matriz com escala contínua de valores. |
| 21 | `verticalIncomeFlow` | Layered income flow | `incomeFlow` | Fluxo de receita em camadas | Acúmulo de receita em marcos (versão compacta do [WidgetIncomeFlow](../WidgetIncomeFlow/README.md)). |

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
| `title` | `string` | “Income” ou “Sales Report” no cabeçalho. |
| `value` | `number` | Base dos valores: `verticalValue()` = `value × ratios[i]`. |
| `details` | `boolean` | Mostra o bloco de detalhes. |

Estado inicial: `{ selectedPoint: 5 }`.

### Dados

O valor de cada ponto é `Math.round(widget.value * [.84, .91, .87, .96, .93, 1, .9, .97][i % 8])` (`verticalValue`), com rótulo `months[i]`. Não há série real por card no modelo: o provider precisa acrescentar `values` (ver JS).

### Atributos `data-*`

| Atributo | Onde / efeito |
|---|---|
| `data-vertical-widget` / `data-vertical-point` | Marca selecionável dos gráficos de barra/linha. |
| `data-heatmap-widget` / `data-heatmap-point` | Células dos heatmaps. |
| `data-widget` | No `<article>` gerado: id da definição (chave de `state` e de `renderWidget`). |
| `data-widget-filter` | Botão “Filter” criado pelo JS em cada card. |

### Funções e eventos

| Função / evento | O que faz |
|---|---|
| `mountVerticalWidgets()` | Gera os cards em `#vertical-small-grid`. |
| `renderVerticalWidget(def)` | Valor do ponto e SVG. |
| `verticalChartSvg(def)` | Gerador por `kind` (heatmaps via `heatmapSvg`, fluxo via `verticalIncomeFlowSvg`). |
| `verticalValue(def, i)` | Valor sintético do ponto. |
| `renderWidget(id)` | Despacha para o render da seção (entradas geradas com `Object.fromEntries(<defs>.map(…))`). |
| `renderAll()` | Observa todos os cards e renderiza sob demanda. |
| `click` / `keydown` globais | Selecionam o ponto (`selectedPoint`) e re-renderizam só aquele widget. |

### Endpoints

Sem rota pronta. Provider do módulo financeiro (`admin.financial.view`) com as consultas abaixo; URL em `data-endpoint` da seção.

## Acessibilidade

- Cada marca selecionável é `<g role="button" tabindex="0" aria-pressed>` com `aria-label` “Mês: $valor” e `<title>`; `Enter`/`Espaço` selecionam (tratador global de `keydown`).
- Nos heatmaps só a célula selecionada tem `tabindex="0"` (as demais `-1`): as setas movem a seleção entre células (roving tabindex).
- O rótulo “: Nome” acima de cada card é texto visível (`.…-widget-label`), e o `<article>` tem `aria-label` com o nome do tipo.
- O tooltip comum abre em hover e foco; a gaveta “Filter” (`#widget-filter-drawer`) filtra marcas por texto e faixa e anuncia a contagem em `aria-live`.
- As paletas são fixas por definição (`colors`); confira contraste das marcas finas no tema escuro e nunca use cor como único portador do valor — o valor do ponto selecionado está em texto no card.

## Modelos

### HTML

**1. Na view PHP.** Nenhum partial do chassi gera estas seções; elas são o contêiner vazio de `index.html` que `mountVerticalWidgets()` preenche. Numa view Plates do módulo:

```php
<?php
$e = static fn ($v) => htmlspecialchars((string) $v, ENT_QUOTES, 'UTF-8');   // helper de domain_page.php
?>
<!-- widgets.js monta os cards dentro de #vertical-small-grid; data-endpoint é lido pelo provider -->
<section class="vertical-small-section" aria-labelledby="vertical-small-grid-title" data-endpoint="<?= $e('/financial/widgets/vertical-series' /* provider a criar */) ?>">
  <h2 class="vertical-small-section-title" id="vertical-small-grid-title"><?= $e($titulo) ?></h2>
  <div class="widgets-grid vertical-small-grid" id="vertical-small-grid" aria-label="<?= $e($descricao) ?>"></div>
</section>
```

**2. Contêiner real** (`docs/model/widgets/index.html`):

```html
<section class="vertical-small-section" aria-labelledby="vertical-small-title">
  <h2 class="vertical-small-section-title" id="vertical-small-title">Vertical small widgets</h2>
  <div class="widgets-grid vertical-small-grid" id="vertical-small-grid" aria-label="Twenty-one vertical compact chart widget examples"></div>
</section>
```

**3. HTML gerado** (capturado do preview renderizado com Playwright; marcas repetidas resumidas):

```html
<div class="vertical-widget-item">
  <div class="vertical-widget-label">: Waterfall chart</div>
  <article class="ttsc-analytics-card widget demo-widget vertical-widget-card" data-widget="verticalWaterfallPurple" aria-label="Waterfall chart vertical compact widget" style="position: relative;">
    <header class="vertical-widget-head">
      <div><strong>Income</strong></div>
      <span class="vertical-widget-dots" aria-hidden="true">⋮</span>
    </header>
    <div class="vertical-widget-value" id="verticalWaterfallPurple-value">$32,134</div>
    <div class="vertical-widget-change">↑ 2.5% <span>301,982 USD</span></div>
    <div class="vertical-widget-chart" id="verticalWaterfallPurple-chart">
      <svg class="vertical-widget-chart vertical-chart-waterfall" viewBox="0 0 120 84" role="group" aria-label="Waterfall chart, select a chart mark to inspect the value">
        <path class="vertical-chart-baseline" d="M2 75.5H118"></path>
        <g class="vertical-chart-mark" role="button" tabindex="0" data-vertical-widget="verticalWaterfallPurple" data-vertical-point="0" aria-pressed="false" aria-label="Jan: $26,993">
          <rect x="5" y="38" width="5" height="8" rx="2.5" fill="#8b5cf6"></rect>
          <title>Jan · $26,993</title>
        </g>
        <g class="vertical-chart-mark" role="button" tabindex="0" data-vertical-widget="verticalWaterfallPurple" data-vertical-point="1" aria-pressed="false" aria-label="Feb: $29,242">
          <rect x="19" y="50.99718893446164" width="5" height="9" rx="2.5" fill="#c4b5fd"></rect>
          <title>Feb · $29,242</title>
        </g>
        <!-- … +6 elemento(s) iguais gerados pelo JS -->
      </svg>
    </div>
    <button class="widget-filter-trigger" type="button" data-widget-filter="verticalWaterfallPurple" aria-label="Filter Income" aria-expanded="false">
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
/* Valor e variação com tokens */
.vertical-widget-value { color: var(--ttsc-text); }
.vertical-widget-change { color: var(--ttsc-accent-text); }
.vertical-widget-change span { color: var(--ttsc-text-muted); }
```

### JS

Definições, montagem e render reais em `widgets.js`:

```js
const verticalWidgetDefinitions = [
  { id: 'verticalWaterfallPurple', label: 'Waterfall chart', kind: 'waterfall', title: 'Income', value: 32134, colors: ['#8b5cf6', '#c4b5fd'] },
  { id: 'verticalWaterfallAmber', label: 'Waterfall chart', kind: 'waterfall', title: 'Income', value: 32134, colors: ['#f59e0b', '#fcd34d'] },
  { id: 'verticalGroupedColumns', label: 'Grouped bar chart', kind: 'groupedColumns', title: 'Income', value: 32134, colors: ['#3b82f6', '#fb7185', '#f59e0b', '#8b5cf6'] },
  { id: 'verticalGroupedHorizontal', label: 'Grouped bar chart', kind: 'groupedHorizontal', title: 'Sales Report', value: 8438, colors: ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b'] },
  { id: 'verticalStackedHorizontal', label: 'Stacked horizontal bar', kind: 'stackedHorizontal', title: 'Income', value: 32134, colors: ['#6d5dfc', '#c4b5fd'] },
  { id: 'verticalBasicGreen', label: 'Basic bar', kind: 'columns', title: 'Income', value: 32134, colors: ['#22c55e', '#bbf7d0'] },
  { id: 'verticalBasicSpectrum', label: 'Basic bar', kind: 'columns', title: 'Sales Report', value: 8438, details: true, colors: ['#10b981', '#38bdf8', '#6366f1'] },
  { id: 'verticalDetailedBars', label: 'Detailed bar chart', kind: 'denseColumns', title: 'Sales Report', value: 8438, details: true, colors: ['#22c55e'] },
  { id: 'verticalRainfall', label: 'Column rainfall', kind: 'rainfall', title: 'Sales Report', value: 8438, details: true, colors: ['#f59e0b', '#06b6d4', '#8b5cf6'] },
  { id: 'verticalSparseBars', label: 'Basic bar', kind: 'sparseColumns', title: 'Income', value: 32134, colors: ['#8b5cf6', '#d8b4fe'] },
  { id: 'verticalBubbles', label: 'Bubble bar chart', kind: 'bubbles', title: 'Income', value: 32134, colors: ['#f59e0b', '#fb923c'] },
  { id: 'verticalStackedColumns', label: 'Stacked columns', kind: 'stackedColumns', title: 'Sales Report', value: 8438, colors: ['#f97316', '#8b5cf6'] },
  { id: 'verticalDenseBars', label: 'Detailed bar chart', kind: 'denseColumns', title: 'Income', value: 32134, colors: ['#22c55e', '#86efac'] },
  { id: 'verticalLineColumns', label: 'Line and column chart', kind: 'lineColumns', title: 'Sales Report', value: 8438, details: true, colors: ['#8b5cf6', '#fbbf24'] },
  { id: 'verticalGradientBars', label: 'Detailed bar chart', kind: 'gradientColumns', title: 'Income', value: 32134, colors: ['#94a3b8', '#f97316', '#fbbf24'] },
  { id: 'verticalHexFlow', label: 'Hex heatmap', kind: 'heatmap', visual: 'hexFlow', title: 'Income', value: 32134 },
  { id: 'verticalHexRadial', label: 'Hex heatmap', kind: 'heatmap', visual: 'hexRadial', title: 'Income', value: 32134 },
  { id: 'verticalBasicHeatmap', label: 'Basic heatmap', kind: 'heatmap', visual: 'basic', title: 'Income', value: 32134 },
  { id: 'verticalHeatmapIndicator', label: 'Heatmap indicator', kind: 'heatmap', visual: 'indicator', title: 'Income', value: 32134 },
  { id: 'verticalGradientHeatmap', label: 'Gradient heatmap', kind: 'heatmap', visual: 'gradient', title: 'Income', value: 32134 },
  { id: 'verticalIncomeFlow', label: 'Layered income flow', kind: 'incomeFlow', title: 'Income', value: 32134 }
];
```

```js
function mountVerticalWidgets() {
  const grid = byId('vertical-small-grid');
  if (!grid) return;
  grid.innerHTML = verticalWidgetDefinitions.map(widget => `<div class="vertical-widget-item"><div class="vertical-widget-label">: ${widget.label}</div><article class="ttsc-analytics-card widget demo-widget vertical-widget-card" data-widget="${widget.id}" aria-label="${widget.label} vertical compact widget"><header class="vertical-widget-head"><div><strong>${widget.title}</strong>${widget.title === 'Sales Report' ? '<span class="vertical-widget-spark" aria-hidden="true">✦</span>' : ''}</div><span class="vertical-widget-dots" aria-hidden="true">⋮</span></header><div class="vertical-widget-value" id="${widget.id}-value"></div><div class="vertical-widget-change">↑ 2.5% <span>301,982 USD</span></div><div class="vertical-widget-chart" id="${widget.id}-chart"></div>${widget.details ? `<div class="vertical-widget-details"><span>Monthly <strong>$${(widget.value === 8438 ? '22,098' : '32,221')}</strong></span><span>Yearly <strong>$62,134</strong></span></div>` : ''}</article></div>`).join('');
}
```

```js
function verticalValue(widget, index) {
  const ratios = [.84, .91, .87, .96, .93, 1, .9, .97];
  return Math.round(widget.value * ratios[index % ratios.length]);
}
```

```js
function renderVerticalWidget(widget) {
  const index = Math.max(0, Math.min(7, state[widget.id].selectedPoint));
  byId(`${widget.id}-value`).textContent = fmtMoney(verticalValue(widget, index), 0);
  byId(`${widget.id}-chart`).innerHTML = verticalChartSvg(widget);
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

// payload = { net: [{ month, net_change }], receivables: [{ month, paid, open_amount, overdue, partial_amount }] }
loadSection('.vertical-small-section', verticalWidgetDefinitions, (definition, payload) =>
  definition.kind === 'waterfall' || definition.kind === 'incomeFlow'
    ? (payload.net ?? []).map(row => Number(row.net_change) || 0)
    : (payload.receivables ?? []).map(row => Number(row.paid) || 0));
```

CSV: `downloadCsv()` não tem ramo para os widgets de seção (o menu “Download CSV” não existe nesses cards). Para exportar, use a exportação da página de origem dos dados (`GET /api/v1/domain/records{rota}/export?format=csv|xlsx|pdf|json|xml|sql`).

### SQL

Cascata a partir da variação líquida mensal do razão (`financial_transactions`) e barras agrupadas a partir das mensalidades por situação (`financial_receivables`). Testadas no MariaDB local.

```sql
-- (a) Cascata (waterfall): variação líquida do caixa por mês, últimos 8 meses
SELECT DATE_FORMAT(t.transaction_date, '%Y-%m')                                AS month,
       SUM(CASE WHEN t.type = 'credit' THEN t.amount ELSE -t.amount END)      AS net_change
  FROM financial_transactions t
 WHERE t.transaction_date >= DATE_FORMAT(CURDATE() - INTERVAL 7 MONTH, '%Y-%m-01')
 GROUP BY DATE_FORMAT(t.transaction_date, '%Y-%m')
 ORDER BY month;

-- (b) Barras agrupadas: mensalidades por mês de vencimento e situação
SELECT DATE_FORMAT(r.due_date, '%Y-%m') AS month,
       SUM(CASE WHEN r.status = 'paid'    THEN r.net_amount ELSE 0 END) AS paid,
       SUM(CASE WHEN r.status = 'open'    THEN r.net_amount ELSE 0 END) AS open_amount,
       SUM(CASE WHEN r.status = 'overdue' THEN r.net_amount ELSE 0 END) AS overdue,
       SUM(CASE WHEN r.status = 'partial' THEN r.net_amount ELSE 0 END) AS partial_amount
  FROM financial_receivables r
 WHERE r.deleted_at IS NULL AND r.status <> 'cancelled'
   AND r.due_date >= DATE_FORMAT(CURDATE() - INTERVAL 7 MONTH, '%Y-%m-01')
 GROUP BY DATE_FORMAT(r.due_date, '%Y-%m')
 ORDER BY month;
```

Para os tipos de uma série use a coluna `paid`; para `groupedColumns`/`groupedHorizontal` envie as quatro colunas (uma por cor da definição).

## Faça / Não faça

- **Faça:** usar `title` coerente com o indicador (“Recebido”, “Mensalidades”);
- **Faça:** acrescentar `values` reais em vez de ratios.
- **Não faça:** usar os ratios sintéticos de `verticalValue` com dados reais;
- **Não faça:** tratar `.vertical-widget-dots` como menu (é decorativo, `aria-hidden`).
