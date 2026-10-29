# WidgetSalesReport

Família “Sales report”: receita por período (semana, mês, ano) e por região em sete variações — fluxo empilhado com tabela, multi-série, compacto, área, linha, snapshot com marcador e compacto “glow”.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só os sete cards de relatório de vendas (`sales`, `salesMulti`, `salesCompact`, `salesArea`, `salesLine`, `salesSplit`, `salesGlow`). Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Relatar receita recebida por campus/centro de custo (`financial_receivables` × `financial_cost_centers`) em semana, mês e ano, com o período anterior.
- `sales` (fluxo + tabela) para a página de relatório; `salesCompact`/`salesGlow`/`salesSplit` para painéis com pouco espaço; `salesArea`/`salesLine` quando a série mensal do ano é o foco; `salesMulti` para comparar regiões no mês e no ano.
- Para uma única série histórica sem regiões use [WidgetIncomeStatistics](../WidgetIncomeStatistics/README.md); para marcos dentro do mês, [WidgetIncomeFlow](../WidgetIncomeFlow/README.md).

## Anatomia

```
sales (largo)                                         salesCompact / salesGlow
┌ Sales report ─────────────── [ajustes] [⋯] ┐        ┌ Sales report [⋯] ┐
│ Weekly $2,197 ↑19.6% │ Monthly │ Yearly    │        │ $8,903 ↑1.9%  ╱╲ │
│ ══╗ fluxo empilhado (3 regiões) ╔═══       │        │ Annual revenue … │
│ Region   Weekly  Monthly  Yearly           │        └──────────────────┘
│ Los Angeles  $890  $3,600  $40,000         │
└────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Relatório completo | `article.sales-report-widget[data-widget="sales"]` > `#sales-kpis` (`.sales-period-kpi.is-selected`), `.sales-flow-wrap > svg#sales-flow-chart`, `#sales-table-wrap > table.sales-region-table` | sim (variação `sales`) |
| Multi-série | `.sales-multi-widget` > `.sales-multi-plots` (`svg#sales-multi-monthly`, `svg#sales-multi-yearly`) + `#sales-multi-regions` | variação |
| Compacto | `.sales-compact-widget` > `.compact-sales-layout` (`#sales-compact-value`, `#sales-compact-change`, `svg#sales-compact-chart`) | variação |
| Área / linha | `.sales-area-widget` / `.sales-line-widget` > `.variant-chart-area > svg` + `.variant-region-list` | variação |
| Snapshot | `.sales-split-widget` > `.split-sales-layout` + `svg#sales-split-chart` (marcador opcional) | variação |
| Glow | `.sales-glow-widget` > `.glow-sales-layout` + `svg#sales-glow-chart` | variação |
| Configurações | `dialog#settings-<widget>` (um por variação, isolados) | sim |

## Variantes

| Variação (`data-widget`) | Visual | Configurações | Render |
|---|---|---|---|
| `sales` | Três KPIs de período, fluxo empilhado SVG (3 regiões, 4 marcos) e tabela região × período | `period` (destaque), `showTable` | `renderSales()` |
| `salesMulti` | Duas linhas multi-série (mês e ano) por região + lista de regiões | `showRegions` | `renderSalesMulti()` |
| `salesCompact` | Valor + variação + mini área azul | `period` | `renderSalesCompact('salesCompact')` |
| `salesArea` | Área com totais mês/ano + regiões (ver defeito abaixo) | `period`, `showRegions` | `renderSalesArea('salesArea')` |
| `salesLine` | Linha/área com totais mês/ano + regiões (ver defeito abaixo) | `period`, `showRegions` | `renderSalesArea('salesLine')` |
| `salesSplit` | Snapshot do mês com área verde e marcador do último ponto | `showMarkers` | `renderSalesSplit()` |
| `salesGlow` | Igual ao compacto, área verde com brilho | `period` | `renderSalesCompact('salesGlow')` |

**Defeito conhecido no modelo:** em `renderSalesArea(widget)` a linha `const line = widget === 'salesArea'` está invertida. Resultado: `renderSalesArea('salesArea')` escreve em `#sales-line-chart`, `#sales-line-month`… (que estão no card `salesLine`) e vice-versa — o diálogo de `salesArea` altera o outro card, quebrando o isolamento de configurações. Na cópia de produção use `const line = widget === 'salesLine';` (troque também as cores, se quiser manter a área laranja no card “revenue growth”).

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('sales')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Após “Apply settings” o diálogo grava em `state.sales` e re-renderiza só este widget; o toast `#widget-toast` confirma. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Período destacado | `state.sales.period` marca o KPI com `.is-selected` e o marco do fluxo. |
| Sem tabela/regiões | `showTable`/`showRegions = false` escondem a tabela ou a lista de regiões. |

## API

### Dados esperados

Totais de semana, mês e ano com o período anterior e o detalhamento por região (as regiões devem ser as mesmas e na mesma ordem nos três períodos), mais a série mensal do ano para as variações em área/linha.

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `sales.<week|month|year>.total` | `number` | moeda, 0 casas | Receita do período. |
| `…previous` | `number` | moeda | Período anterior (variação ↑/↓). |
| `…label` | `string` | texto | `Weekly`/`Monthly`/`Yearly`. |
| `…rows[] {name, value}` | `array` | moeda | Três regiões; `value / total` dá a espessura de cada faixa do fluxo. |
| `salesMonthlyTrend[]` | `number[12]` | moeda | Série mensal usada por compact/area/line/split/glow. |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js
sales: {
  week: { total: 2197, previous: 1836, label: 'Weekly', rows: [{ name: 'Los Angeles', value: 890 }, { name: 'New York', value: 750 }, { name: 'Canada', value: 557 }] },
  month: { total: 8903, previous: 8737, label: 'Monthly', rows: [{ name: 'Los Angeles', value: 3600 }, { name: 'New York', value: 2900 }, { name: 'Canada', value: 2403 }] },
  year: { total: 98134, previous: 80438, label: 'Yearly', rows: [{ name: 'Los Angeles', value: 40000 }, { name: 'New York', value: 32000 }, { name: 'Canada', value: 26134 }] }
}
salesMonthlyTrend: [7600, 7700, 7800, 7900, 8000, 8100, 8200, 8300, 8400, 8500, 8731, 8903]
```

### Configurações do widget

**`sales`**

Padrão em `state.sales`: `{ period: 'month', showTable: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `period` | select | `week` (Weekly) · `month` (Monthly) · `year` (Yearly) | Highlight period | Período destacado ou número de meses (variações de área/linha). |
| `showTable` | input checkbox | booleano | Show regional revenue table | Mostra a tabela por região. |

**`salesMulti`**

Padrão em `state.salesMulti`: `{ showRegions: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `showRegions` | input checkbox | booleano | Show regional details | Mostra a lista de regiões. |

**`salesCompact`**

Padrão em `state.salesCompact`: `{ period: 'month' }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `period` | select | `month` (Monthly) · `year` (Yearly) | Period | Período destacado ou número de meses (variações de área/linha). |

**`salesArea`**

Padrão em `state.salesArea`: `{ period: 12, showRegions: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `period` | select | `6` (Last 6 months) · `12` (Last 12 months) | Visible months | Período destacado ou número de meses (variações de área/linha). |
| `showRegions` | input checkbox | booleano | Show annual regional values | Mostra a lista de regiões. |

**`salesLine`**

Padrão em `state.salesLine`: `{ period: 12, showRegions: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `period` | select | `6` (Last 6 months) · `12` (Last 12 months) | Visible months | Período destacado ou número de meses (variações de área/linha). |
| `showRegions` | input checkbox | booleano | Show regional details | Mostra a lista de regiões. |

**`salesSplit`**

Padrão em `state.salesSplit`: `{ showMarkers: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `showMarkers` | input checkbox | booleano | Show chart markers | Ponto e valor no último mês. |

**`salesGlow`**

Padrão em `state.salesGlow`: `{ period: 'month' }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `period` | select | `month` (Monthly) · `year` (Yearly) | Period | Período destacado ou número de meses (variações de área/linha). |

### Atributos `data-*`

| Atributo | Onde / efeito |
|---|---|
| `data-widget` | No `<article>`: chave do widget em `state`/`renderWidget()`; também é o alvo do filtro e do observador de renderização preguiçosa. |
| `data-open-settings` | Botão de ajuste: abre `<dialog id="settings-<widget>">` e copia `state[widget]` para os campos. |
| `data-setting` | Campo do diálogo: widget dono da configuração (isolamento: cada widget só lê os seus campos). |
| `data-key` | Campo do diálogo: chave dentro de `state[widget]` (checkbox vira booleano, `number` vira número). |
| `data-menu` | Botão “mais ações”: alterna o `.widget-menu` irmão e `aria-expanded`. |
| `data-download` | Item do menu: chama `downloadCsv(widget)`. |
| `data-reset` | Item do menu: restaura os padrões do widget e chama `renderWidget(widget)`. |
| `data-tip` | Texto do tooltip comum (`#widget-tooltip`) em hover/foco. |
| `data-widget-filter` | Criado pelo JS (`addFilterAction`): botão “Filter” no canto do card, abre a gaveta `#widget-filter-drawer` com busca e faixa mín./máx. |

### Funções e eventos

| Função / evento | O que faz |
|---|---|
| `renderSales()` | KPIs, fluxo (`streamPath`) com marcos e tabela; `aria-label` com os três totais. |
| `streamPath(totals, shares, i, max, xs, cy, h)` | Faixa i do fluxo empilhado com curvas suaves (`smoothBoundary`). |
| `chartMarkup(values, options)` | Área + linha SVG genérica das variações (grade, gradiente, rótulos, marcador). |
| `renderSalesMulti()`, `renderSalesCompact(w)`, `renderSalesArea(w)`, `renderSalesSplit()` | Render de cada variação. |
| `renderVariantRegionList(node, period)` | Lista “Região  $valor” das variações. |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- Lista pronta: `GET /api/v1/domain/records/financial/receivable` (view `inst_fin_receivables`), permissão `admin.financial.view` (a mesma das rotas `/financial/*` em `app/Config/page-domain-sources.php`) — serve para conferência, não para o agregado.
- **Recomendado:** provider do módulo financeiro com as duas consultas abaixo → `{ "regions": [...], "trend": [...] }`; todas as sete variações leem a mesma resposta.

## Acessibilidade

- O fluxo `#sales-flow-chart` tem `aria-label` com os três totais e o anual de cada região; a tabela `.sales-region-table` (com `th scope`) é a alternativa textual completa.
- As setas ↑/↓ dos KPIs acompanham a classe `.is-negative`, então a direção não depende só da cor.
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
$endpoint = '/financial/reports/revenue/widgets/sales-report' /* rota do provider do módulo, a criar */;
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="sales"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="sales-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget sales-report-widget" data-widget="sales" aria-labelledby="sales-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-amber" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="sales-title">Sales report</h2>
          <button class="info-button" type="button" data-tip="Sales totals are grouped by region. Each table column reconciles with its weekly, monthly or yearly KPI." aria-label="About sales report">
            i
          </button>
        </div>
        <p>Revenue by period and region</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="sales" aria-label="Adjust sales report">
        <svg viewBox="0 0 20 20">…</svg>
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" aria-label="More sales report actions" aria-expanded="false" data-menu="sales">
          <svg viewBox="0 0 20 20">…</svg>
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="sales">Download CSV</button>
          <button type="button" data-reset="sales">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="sales-period-kpis" id="sales-kpis"></div>
  <div class="sales-flow-wrap">
    <svg id="sales-flow-chart" viewBox="0 0 900 290" role="img" aria-label="Sales revenue flow by region and period"></svg>
  </div>
  <div class="sales-table-wrap" id="sales-table-wrap">
    <table class="sales-region-table">
      <thead>
        <tr>
          <th scope="col">Region</th>
          <th scope="col">Weekly</th>
          <th scope="col">Monthly</th>
          <th scope="col">Yearly</th>
        </tr>
      </thead>
      <tbody id="sales-region-rows"></tbody>
    </table>
  </div>
  <footer class="ttsc-analytics-foot widget-foot">
    <span>Revenue values reconcile to the period totals</span>
    <span id="sales-period-label">Monthly view · sample</span>
  </footer>
  <dialog class="widget-settings" id="settings-sales" aria-labelledby="settings-sales-title">
    <form method="dialog">
      <header>
        <div>
          <span class="settings-icon">↗</span>
          <div>
            <h3 id="settings-sales-title">Sales report settings</h3>
            <p>Settings apply to this widget only.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close settings">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Highlight period
          <select data-setting="sales" data-key="period">
            <option value="week">Weekly</option>
            <option value="month" selected>Monthly</option>
            <option value="year">Yearly</option>
          </select>
        </label>
        <label class="settings-check">
          <input type="checkbox" data-setting="sales" data-key="showTable" checked>
          Show regional revenue table
        </label>
      </div>
      <footer>
        <button class="button-secondary" value="cancel">Cancel</button>
        <button class="button-primary" value="save">Apply settings</button>
      </footer>
    </form>
  </dialog>
</article>
```

```html
<article class="ttsc-analytics-card widget demo-widget sales-variant sales-multi-widget" data-widget="salesMulti" aria-labelledby="sales-multi-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-amber" aria-hidden="true">↗</span>
      <div>
        <div class="title-line">
          <h2 id="sales-multi-title">Sales report · multi-series</h2>
          <button class="info-button" type="button" data-tip="Monthly and annual revenue bands with regional totals from the sales dataset." aria-label="About multi-series sales report">
            i
          </button>
        </div>
        <p>Revenue movement with regional detail</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="salesMulti" aria-label="Adjust multi-series report">
        ⚙
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" data-menu="salesMulti" aria-label="More multi-series report actions" aria-expanded="false">
          •••
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="salesMulti">Download CSV</button>
          <button type="button" data-reset="salesMulti">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="sales-multi-plots">
    <div>
      <svg id="sales-multi-monthly" viewBox="0 0 440 150" role="img" aria-label="Monthly revenue by region"></svg>
      <strong>Monthly revenue <span id="sales-multi-month-total"></span></strong>
    </div>
    <div>
      <svg id="sales-multi-yearly" viewBox="0 0 440 150" role="img" aria-label="Annual revenue by region"></svg>
      <strong>Annual revenue <span id="sales-multi-year-total"></span></strong>
    </div>
  </div>
  <div class="variant-region-list" id="sales-multi-regions"></div>
  <footer class="ttsc-analytics-foot widget-foot">
    <span>Regional values match the yearly total</span>
    <span>Sample data</span>
  </footer>
  <dialog class="widget-settings" id="settings-salesMulti">
    <form method="dialog">
      <header>
        <div>
          <div>
            <h3>Multi-series report settings</h3>
            <p>Settings apply to this widget only.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-check">
          <input type="checkbox" data-setting="salesMulti" data-key="showRegions" checked>
          Show regional details
        </label>
      </div>
      <footer>
        <button class="button-secondary" value="cancel">Cancel</button>
        <button class="button-primary" value="save">Apply settings</button>
      </footer>
    </form>
  </dialog>
</article>
```

```html
<article class="ttsc-analytics-card widget demo-widget sales-variant sales-compact-widget" data-widget="salesCompact" aria-labelledby="sales-compact-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <div>
        <div class="title-line"><h2 id="sales-compact-title">Sales report</h2></div>
        <p>Current month</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="salesCompact" aria-label="Adjust compact report">
        ⚙
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" data-menu="salesCompact" aria-label="More compact report actions" aria-expanded="false">
          •••
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="salesCompact">Download CSV</button>
          <button type="button" data-reset="salesCompact">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="compact-sales-layout">
    <div>
      <strong class="widget-value" id="sales-compact-value"></strong>
      <span class="metric-change is-positive" id="sales-compact-change">
        <svg viewBox="0 0 16 16">…</svg>
        <span data-change-value></span>
      </span>
      <p id="sales-compact-context"></p>
    </div>
    <svg id="sales-compact-chart" viewBox="0 0 220 100" role="img" aria-label="Sales revenue sparkline"></svg>
  </div>
  <dialog class="widget-settings" id="settings-salesCompact">
    <form method="dialog">
      <header>
        <div>
          <div><h3>Compact report settings</h3><p>Settings apply to this widget only.</p></div>
          <button class="dialog-close" value="cancel" aria-label="Close">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Period
          <select data-setting="salesCompact" data-key="period">
            <option value="month" selected>Monthly</option>
            <option value="year">Yearly</option>
          </select>
        </label>
      </div>
      <footer>
        <button class="button-secondary" value="cancel">Cancel</button>
        <button class="button-primary" value="save">Apply settings</button>
      </footer>
    </form>
  </dialog>
</article>
```

```html
<article class="ttsc-analytics-card widget demo-widget sales-variant sales-area-widget" data-widget="salesArea" aria-labelledby="sales-area-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <div>
        <div class="title-line"><h2 id="sales-area-title">Sales report · revenue growth</h2></div>
        <p>Monthly revenue and cumulative annual sales</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="salesArea" aria-label="Adjust revenue growth chart">
        ⚙
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" data-menu="salesArea" aria-label="More revenue growth actions" aria-expanded="false">
          •••
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="salesArea">Download CSV</button>
          <button type="button" data-reset="salesArea">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="variant-chart-area">
    <svg id="sales-area-chart" viewBox="0 0 500 230" role="img" aria-label="Monthly revenue area chart"></svg>
  </div>
  <div class="variant-kpi-row">
    <div><span>Monthly</span><strong id="sales-area-month"></strong><small id="sales-area-month-change"></small></div>
    <div><span>Yearly</span><strong id="sales-area-year"></strong><small id="sales-area-year-change"></small></div>
  </div>
  <div class="variant-region-list" id="sales-area-regions"></div>
  <dialog class="widget-settings" id="settings-salesArea">
    <form method="dialog">
      <header>
        <div>
          <div><h3>Revenue growth settings</h3><p>Settings apply to this widget only.</p></div>
          <button class="dialog-close" value="cancel" aria-label="Close">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Visible months
          <select data-setting="salesArea" data-key="period">
            <option value="6">Last 6 months</option>
            <option value="12" selected>Last 12 months</option>
          </select>
        </label>
        <label class="settings-check">
          <input type="checkbox" data-setting="salesArea" data-key="showRegions" checked>
          Show annual regional values
        </label>
      </div>
      <footer>
        <button class="button-secondary" value="cancel">Cancel</button>
        <button class="button-primary" value="save">Apply settings</button>
      </footer>
    </form>
  </dialog>
</article>
```

```html
<article class="ttsc-analytics-card widget demo-widget sales-variant sales-line-widget" data-widget="salesLine" aria-labelledby="sales-line-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <div>
        <div class="title-line"><h2 id="sales-line-title">Sales report · monthly trend</h2></div>
        <p>Revenue collected each month</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="salesLine" aria-label="Adjust monthly trend">
        ⚙
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" data-menu="salesLine" aria-label="More monthly trend actions" aria-expanded="false">
          •••
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="salesLine">Download CSV</button>
          <button type="button" data-reset="salesLine">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="variant-chart-area">
    <svg id="sales-line-chart" viewBox="0 0 500 230" role="img" aria-label="Monthly sales trend"></svg>
  </div>
  <div class="variant-kpi-row">
    <div><span>Monthly</span><strong id="sales-line-month"></strong><small id="sales-line-month-change"></small></div>
    <div><span>Yearly</span><strong id="sales-line-year"></strong><small id="sales-line-year-change"></small></div>
  </div>
  <div class="variant-region-list" id="sales-line-regions"></div>
  <dialog class="widget-settings" id="settings-salesLine">
    <form method="dialog">
      <header>
        <div>
          <div><h3>Monthly trend settings</h3><p>Settings apply to this widget only.</p></div>
          <button class="dialog-close" value="cancel" aria-label="Close">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Visible months
          <select data-setting="salesLine" data-key="period">
            <option value="6">Last 6 months</option>
            <option value="12" selected>Last 12 months</option>
          </select>
        </label>
        <label class="settings-check">
          <input type="checkbox" data-setting="salesLine" data-key="showRegions" checked>
          Show regional details
        </label>
      </div>
      <footer>
        <button class="button-secondary" value="cancel">Cancel</button>
        <button class="button-primary" value="save">Apply settings</button>
      </footer>
    </form>
  </dialog>
</article>
```

```html
<article class="ttsc-analytics-card widget demo-widget sales-variant sales-split-widget" data-widget="salesSplit" aria-labelledby="sales-split-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <div>
        <div class="title-line"><h2 id="sales-split-title">Sales report</h2></div>
        <p>Monthly revenue · snapshot</p>
      </div>
    </div>
    <div class="widget-actions">
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" data-menu="salesSplit" aria-label="More split report actions" aria-expanded="false">
          •••
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="salesSplit">Download CSV</button>
          <button type="button" data-reset="salesSplit">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="split-sales-layout">
    <div>
      <strong class="widget-value" id="sales-split-value"></strong>
      <span class="metric-change is-positive" id="sales-split-change">
        <svg viewBox="0 0 16 16">…</svg>
        <span data-change-value></span>
      </span>
      <p>Compared with the previous month</p>
    </div>
    <svg id="sales-split-chart" viewBox="0 0 240 130" role="img" aria-label="Monthly revenue detail chart"></svg>
  </div>
  <dialog class="widget-settings" id="settings-salesSplit">
    <form method="dialog">
      <header>
        <div>
          <div><h3>Snapshot settings</h3><p>Settings apply to this widget only.</p></div>
          <button class="dialog-close" value="cancel" aria-label="Close">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-check">
          <input type="checkbox" data-setting="salesSplit" data-key="showMarkers" checked>
          Show chart markers
        </label>
      </div>
      <footer>
        <button class="button-secondary" value="cancel">Cancel</button>
        <button class="button-primary" value="save">Apply settings</button>
      </footer>
    </form>
  </dialog>
</article>
```

```html
<article class="ttsc-analytics-card widget demo-widget sales-variant sales-glow-widget" data-widget="salesGlow" aria-labelledby="sales-glow-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <div>
        <div class="title-line"><h2 id="sales-glow-title">Sales report</h2></div>
        <p>Current month</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="salesGlow" aria-label="Adjust sales snapshot">
        ⚙
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" data-menu="salesGlow" aria-label="More sales snapshot actions" aria-expanded="false">
          •••
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="salesGlow">Download CSV</button>
          <button type="button" data-reset="salesGlow">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="glow-sales-layout">
    <div>
      <strong class="widget-value" id="sales-glow-value"></strong>
      <span class="metric-change is-positive" id="sales-glow-change">
        <svg viewBox="0 0 16 16">…</svg>
        <span data-change-value></span>
      </span>
      <p id="sales-glow-context"></p>
    </div>
    <svg id="sales-glow-chart" viewBox="0 0 220 100" role="img" aria-label="Sales revenue sparkline"></svg>
  </div>
  <dialog class="widget-settings" id="settings-salesGlow">
    <form method="dialog">
      <header>
        <div>
          <div><h3>Sales snapshot settings</h3><p>Settings apply to this widget only.</p></div>
          <button class="dialog-close" value="cancel" aria-label="Close">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Period
          <select data-setting="salesGlow" data-key="period">
            <option value="month" selected>Monthly</option>
            <option value="year">Yearly</option>
          </select>
        </label>
      </div>
      <footer>
        <button class="button-secondary" value="cancel">Cancel</button>
        <button class="button-primary" value="save">Apply settings</button>
      </footer>
    </form>
  </dialog>
</article>
```

### CSS

Arquivos: `ttsc.analytics-panels.css` (`.ttsc-analytics-card`, `-head`, `-plot`, `-foot`, `-empty`) + `docs/model/widgets/widgets.css` (layout e regras deste widget). O tema escuro de `widgets.css` é `html[data-theme="dark"]` (redefine `--w-surface`, `--w-text`, `--w-border`, `--w-grid`…); o de `ttsc.analytics-panels.css` é `html.dark` — `TTSCModelKit.syncTheme()` mantém os dois em sincronia.

Regras reais deste widget em `widgets.css`:

```css
.sales-report-widget { grid-row: span 2; display: flex; min-height: 690px; flex-direction: column; }
.sales-period-kpis { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin: 8px 0 0; }
.sales-period-kpi { display: grid; min-width: 0; grid-template-columns: minmax(0, 1fr) auto; align-items: baseline; column-gap: 8px; padding: 0 4px 9px; border-bottom: 1px solid var(--w-grid); }
.sales-period-kpi > span { overflow: hidden; color: var(--w-muted); font-size: 11px; font-weight: 550; text-overflow: ellipsis; white-space: nowrap; }
.sales-period-kpi > strong { grid-column: 1; grid-row: 2; color: var(--w-text); font-size: clamp(16px, 1.7vw, 23px); font-weight: 650; font-variant-numeric: tabular-nums; letter-spacing: -.035em; }
.sales-period-kpi > small { grid-column: 2; grid-row: 2; color: #059669; font-size: 10px; font-weight: 650; white-space: nowrap; }
.sales-period-kpi > small.is-negative { color: #dc2626; }
.sales-period-kpi > p { overflow: hidden; grid-column: 1 / -1; margin: 3px 0 0; color: var(--w-muted); font-size: 10px; text-overflow: ellipsis; white-space: nowrap; }
.sales-period-kpi.is-selected { border-bottom: 2px solid #f97316; }
.sales-flow-wrap { min-height: 300px; flex: 1 1 auto; margin: 7px -3px 3px; }
.sales-flow-wrap svg, .income-stream-wrap svg { display: block; width: 100%; height: 100%; overflow: visible; }
.sales-stream-band { opacity: .9; transition: opacity .18s ease; }
.sales-checkpoint line { stroke: var(--w-surface); stroke-width: 2; opacity: .9; }
.sales-checkpoint rect { fill: var(--w-surface); stroke: var(--w-border); }
.sales-checkpoint-value { fill: var(--w-text); font: 600 11px var(--ttsc-font-mono, ui-monospace, monospace); text-anchor: middle; }
.sales-checkpoint-label { fill: var(--w-muted); font: 10px var(--ttsc-font-sans, Inter, sans-serif); text-anchor: middle; }
.sales-checkpoint.is-selected rect { fill: #fff7ed; stroke: #fdba74; }
.sales-checkpoint.is-selected .sales-checkpoint-value { fill: #c2410c; }
.sales-region-table { width: 100%; border-collapse: collapse; color: var(--w-secondary); font-size: 11px; font-variant-numeric: tabular-nums; }
.sales-region-table th, .sales-region-table td { padding: 9px 6px; border-bottom: 1px solid var(--w-grid); text-align: right; }
.sales-region-table thead th { color: var(--w-muted); font-size: 10px; font-weight: 550; }
.sales-region-table th:first-child { text-align: left; }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Faixas do fluxo usam cores do JS (streamColors). Ajuste de densidade da tabela com tokens: */
.sales-region-table th, .sales-region-table td { padding-block: var(--ttsc-space-2); border-color: var(--ttsc-border-soft); }
.sales-period-kpi.is-selected { border-color: var(--ttsc-accent-border); background: var(--ttsc-accent-soft); }
```

### JS

Render real em `widgets.js`:

```js
function renderSales() {
  const periods = ['week', 'month', 'year'];
  const selected = state.sales.period;
  const selectedLabel = data.sales[selected].label;
  byId('sales-kpis').innerHTML = periods.map(period => {
    const item = data.sales[period];
    return `<div class="sales-period-kpi${period === selected ? ' is-selected' : ''}"><span>${item.label}</span><strong>${fmtWhole(item.total)}</strong><small class="${percentChange(item.total, item.previous) < 0 ? 'is-negative' : ''}">${percentChange(item.total, item.previous) >= 0 ? '↑' : '↓'} ${Math.abs(percentChange(item.total, item.previous)).toFixed(1)}%</small><p>vs ${fmtWhole(item.previous)} prior ${period === 'week' ? 'week' : period === 'month' ? 'month' : 'year'}</p></div>`;
  }).join('');
  const xs = [22, 288, 574, 878];
  const totals = [Math.max(1000, data.sales.week.total * .08), ...periods.map(period => data.sales[period].total)];
  const finalTotal = data.sales.year.total;
  const shares = data.sales.year.rows.map((_, regionIndex) => [
    data.sales.week.rows[regionIndex].value / data.sales.week.total,
    ...periods.map(period => data.sales[period].rows[regionIndex].value / data.sales[period].total)
  ]);
  const streamColors = ['#ffad66', '#ff8b26', '#f05a12'];
  const bands = streamColors.map((color, index) => `<path class="sales-stream-band" d="${streamPath(totals, shares, index, finalTotal, xs, 141, 116)}" fill="${color}"/>`).join('');
  const checkpoints = periods.map((period, index) => {
    const x = xs[index + 1];
    const item = data.sales[period];
    return `<g class="sales-checkpoint${period === selected ? ' is-selected' : ''}"><line x1="${x}" y1="37" x2="${x}" y2="247"/><rect x="${x - 56}" y="18" width="112" height="26" rx="13"/><text class="sales-checkpoint-value" x="${x}" y="35">${fmtWhole(item.total)}</text><text class="sales-checkpoint-label" x="${x}" y="270">${item.label}</text></g>`;
  }).join('');
  byId('sales-flow-chart').innerHTML = `<defs><linearGradient id="sales-glow" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#ffb454" stop-opacity=".15"/><stop offset="1" stop-color="#ff7a18" stop-opacity="0"/></linearGradient></defs><rect x="0" y="0" width="900" height="260" fill="url(#sales-glow)"/>${bands}${checkpoints}`;
  const rows = data.sales.year.rows.map((row, index) => `<tr><th scope="row"><i style="--region-color:${streamColors[index]}"></i>${row.name}</th>${periods.map(period => `<td>${fmtWhole(data.sales[period].rows[index].value)}</td>`).join('')}</tr>`).join('');
  byId('sales-region-rows').innerHTML = rows;
  byId('sales-table-wrap').hidden = !state.sales.showTable;
  byId('sales-period-label').textContent = `${selectedLabel} highlighted · sample`;
  byId('sales-flow-chart').setAttribute('aria-label', `Regional revenue flow. Weekly ${fmtWhole(data.sales.week.total)}, monthly ${fmtWhole(data.sales.month.total)}, yearly ${fmtWhole(data.sales.year.total)}. ${data.sales.year.rows.map(row => `${row.name}: ${fmtWhole(row.value)} yearly`).join('; ')}.`);
}
```

```js
function chartMarkup(values, options) {
  const width = options.width || 500;
  const height = options.height || 230;
  const left = options.left || 20;
  const right = width - (options.right || 14);
  const top = options.top || 20;
  const bottom = height - (options.bottom || 25);
  const max = Math.max(...values, 1) * 1.14;
  const xs = values.map((_, index) => left + index * ((right - left) / Math.max(1, values.length - 1)));
  const points = values.map((value, index) => ({ x: xs[index], y: bottom - (value / max) * (bottom - top) }));
  const line = smoothChartPath(points);
  const area = `${line} L ${right.toFixed(1)} ${bottom.toFixed(1)} L ${left.toFixed(1)} ${bottom.toFixed(1)} Z`;
  const grid = [0, 1, 2, 3].map(index => {
    const y = top + (bottom - top) * index / 3;
    return `<line class="variant-grid" x1="${left}" y1="${y.toFixed(1)}" x2="${right}" y2="${y.toFixed(1)}"/>`;
  }).join('');
  const labels = options.labels ? options.labels.map((label, index) => `<text class="variant-axis-label" x="${xs[index].toFixed(1)}" y="${height - 4}">${label}</text>`).join('') : '';
  const marker = options.marker ? `<circle class="variant-point" cx="${points.at(-1).x.toFixed(1)}" cy="${points.at(-1).y.toFixed(1)}" r="4"/><text class="variant-value-label" x="${points.at(-1).x.toFixed(1)}" y="${Math.max(12, points.at(-1).y - 9).toFixed(1)}">${fmtWhole(values.at(-1))}</text>` : '';
  const lineMarkup = `<path d="${area}" fill="url(#${options.gradient})"/><path class="variant-line" d="${line}" stroke="${options.color}"/>${marker}`;
  return { markup: `<defs><linearGradient id="${options.gradient}" x1="0" x2="0" y1="0" y2="1"><stop stop-color="${options.color}" stop-opacity=".27"/><stop offset="1" stop-color="${options.color}" stop-opacity="0"/></linearGradient></defs>${grid}${lineMarkup}${labels}`, points, xs, bottom };
}
```

```js
function renderSalesCompact(widget) {
  const period = state[widget].period;
  const item = data.sales[period];
  const sourceValues = period === 'year' ? data.salesMonthlyTrend : data.salesMonthlyTrend.slice(-6);
  const chartId = widget === 'salesCompact' ? 'sales-compact-chart' : 'sales-glow-chart';
  const valueId = widget === 'salesCompact' ? 'sales-compact-value' : 'sales-glow-value';
  const changeId = widget === 'salesCompact' ? 'sales-compact-change' : 'sales-glow-change';
  const contextId = widget === 'salesCompact' ? 'sales-compact-context' : 'sales-glow-context';
  const chart = chartMarkup(sourceValues, { width: 220, height: 100, left: 4, right: 4, top: 12, bottom: 8, gradient: `${widget}-gradient`, color: widget === 'salesGlow' ? '#25b85a' : '#286ee8' });
  byId(chartId).innerHTML = chart.markup;
  byId(valueId).textContent = fmtWhole(item.total);
  setChange(byId(changeId), percentChange(item.total, item.previous));
  byId(contextId).textContent = widget === 'salesCompact' ? `Annual revenue ${fmtWhole(data.sales.year.total)}` : `Annual revenue ${fmtWhole(data.sales.year.total)}`;
}
```

```js
function renderSalesArea(widget) {
  const count = Number(state[widget].period);
  const values = data.salesMonthlyTrend.slice(-count);
  const labels = months.slice(-count);
  const line = widget === 'salesArea';
  const id = line ? 'sales-line-chart' : 'sales-area-chart';
  const color = line ? '#9247ed' : '#f08a00';
  const chart = chartMarkup(values, { width: 500, height: 230, top: 19, bottom: 28, gradient: `${widget}-gradient`, color, labels });
  byId(id).innerHTML = chart.markup;
  const prefix = line ? 'sales-line' : 'sales-area';
  byId(`${prefix}-month`).textContent = fmtWhole(data.sales.month.total);
  byId(`${prefix}-year`).textContent = fmtWhole(data.sales.year.total);
  byId(`${prefix}-month-change`).textContent = `↑ ${Math.max(0, percentChange(data.sales.month.total, data.sales.month.previous)).toFixed(1)}% vs prior month`;
  byId(`${prefix}-year-change`).textContent = `↑ ${Math.max(0, percentChange(data.sales.year.total, data.sales.year.previous)).toFixed(1)}% vs prior year`;
  const regionNode = byId(`${prefix}-regions`);
  regionNode.hidden = !state[widget].showRegions;
  if (state[widget].showRegions) renderVariantRegionList(regionNode, 'year');
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

// payload = { regions: [{ region, week_total, week_previous, month_total, month_previous, year_total, year_previous }], trend: [{ month, received }] }
loadWidget('sales', (rows, payload) => {
  const regions = payload.regions ?? rows;
  const period = (key, label) => ({
    label,
    total: regions.reduce((t, r) => t + Number(r[`${key}_total`] || 0), 0),
    previous: regions.reduce((t, r) => t + Number(r[`${key}_previous`] || 0), 0),
    rows: regions.map(r => ({ name: r.region, value: Number(r[`${key}_total`]) || 0 })),
  });
  data.sales = { week: period('week', 'Semanal'), month: period('month', 'Mensal'), year: period('year', 'Anual') };
  data.salesMonthlyTrend = (payload.trend ?? []).map(row => Number(row.received) || 0);
  if (data.sales.year.total === 0) return false;                               // estado vazio
  ['salesMulti', 'salesCompact', 'salesArea', 'salesLine', 'salesSplit', 'salesGlow'].forEach(renderWidget);
});
```

O menu “Download CSV” chama `downloadCsv('sales')`, que serializa a **série de amostra** (`sales-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Receita recebida (`amount_paid` por `payment_date`) por centro de custo — o “campus/região” do TotusTuus — em semana, mês e ano, com os períodos anteriores numa só leitura (`SUM(CASE …)`), e a série mensal do ano. Testado no MariaDB local.

```sql
-- Receita recebida por centro de custo (campus) na semana, no mês e no ano, com o período anterior
SELECT cc.name AS region,
       SUM(CASE WHEN r.payment_date >= CURDATE() - INTERVAL 6 DAY THEN r.amount_paid ELSE 0 END)                        AS week_total,
       SUM(CASE WHEN r.payment_date BETWEEN CURDATE() - INTERVAL 13 DAY AND CURDATE() - INTERVAL 7 DAY THEN r.amount_paid ELSE 0 END) AS week_previous,
       SUM(CASE WHEN r.payment_date >= DATE_FORMAT(CURDATE(), '%Y-%m-01') THEN r.amount_paid ELSE 0 END)                AS month_total,
       SUM(CASE WHEN r.payment_date BETWEEN DATE_FORMAT(CURDATE() - INTERVAL 1 MONTH, '%Y-%m-01')
                                        AND LAST_DAY(CURDATE() - INTERVAL 1 MONTH) THEN r.amount_paid ELSE 0 END)       AS month_previous,
       SUM(CASE WHEN YEAR(r.payment_date) = YEAR(CURDATE()) THEN r.amount_paid ELSE 0 END)                              AS year_total,
       SUM(CASE WHEN YEAR(r.payment_date) = YEAR(CURDATE()) - 1 THEN r.amount_paid ELSE 0 END)                          AS year_previous
  FROM financial_receivables r
  JOIN financial_cost_centers cc ON cc.id = r.cost_center_id AND cc.deleted_at IS NULL
 WHERE r.deleted_at IS NULL
   AND r.status <> 'cancelled'
   AND r.payment_date >= MAKEDATE(YEAR(CURDATE()) - 1, 1)
 GROUP BY cc.id, cc.name
 ORDER BY year_total DESC
 LIMIT 3;

-- Série mensal do ano (salesMonthlyTrend das variações)
SELECT DATE_FORMAT(r.payment_date, '%Y-%m') AS month, SUM(r.amount_paid) AS received
  FROM financial_receivables r
 WHERE r.deleted_at IS NULL AND r.status <> 'cancelled'
   AND r.payment_date >= DATE_FORMAT(CURDATE() - INTERVAL 11 MONTH, '%Y-%m-01')
 GROUP BY DATE_FORMAT(r.payment_date, '%Y-%m')
 ORDER BY month;
```

O card foi desenhado para 3 regiões (`LIMIT 3`); se houver mais, some as restantes em “Outras” no PHP, mantendo a mesma ordem nos três períodos. A divisão `value / total` do fluxo exige total > 0: devolva o estado vazio quando o ano não tiver receita.

## Faça / Não faça

- **Faça:** alimentar as sete variações com a mesma resposta (os números batem entre cards);
- **Faça:** manter regiões na mesma ordem em todos os períodos.
- **Não faça:** levar para produção a inversão `widget === 'salesArea'` de `renderSalesArea` (corrija para `salesLine`);
- **Não faça:** usar o fluxo com mais de 3 regiões;
- **Não faça:** manter o caractere de engrenagem dos botões de ajuste das variações compactas — use o ícone Font Awesome Light (`<i class="fa-light fa-sliders"></i>`) como nos demais cards.
