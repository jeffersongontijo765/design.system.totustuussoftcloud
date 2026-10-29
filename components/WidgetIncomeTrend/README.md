# WidgetIncomeTrend

Card “Income · Monthly income trend”: valor do último mês, variação contra o anterior e fluxo azul em quatro camadas ao longo de 8 ou 12 meses, com marcos no início, meio e fim.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só o card `incomeTrend`. Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Mostrar a tendência do faturamento por competência (`billing_invoices`) com ênfase visual no volume.
- Quando 8–12 pontos mensais bastam e os valores exatos ficam nos marcos/tooltip.
- Para leitura precisa de cada mês use [WidgetIncomeStatistics](../WidgetIncomeStatistics/README.md) (linha com eixo); para acumulado dentro do mês, [WidgetIncomeFlow](../WidgetIncomeFlow/README.md).

## Anatomia

```
┌ ícone · Income · Monthly income trend ─ [ajustes] [⋯] ┐
│ $32,134  (↗ 2.5%)                                      │
│ ($4,212)═══════════($16,000)══════════════($32,134)    │  svg#income-trend-chart
│ Apr May Jun Jul Aug Sep Oct Nov                        │  text.trend-month
│ Monthly recorded income                  Apr–Nov       │
└────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Resumo | `.flow-income-summary` > `#income-trend-value`, `.metric-change#income-trend-change` | sim |
| Fluxo | `.income-stream-wrap.trend-stream-wrap > svg#income-trend-chart` (4 `<path>`, `g.trend-marker`, `text.trend-month`) | sim |
| Rodapé | `#income-trend-period-label` | sim |
| Configurações | `dialog#settings-incomeTrend` | sim |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('incomeTrend')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Após “Apply settings” o diálogo grava em `state.incomeTrend` e re-renderiza só este widget; o toast `#widget-toast` confirma. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Sem marcos | `state.incomeTrend.showMilestones = false` remove as pílulas. |

## API

### Dados esperados

Lista cronológica `{ month, value }`; o card usa os últimos `state.incomeTrend.period` itens. Proporções das camadas fixas (`[.16, .28, .34, .22]`).

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `month` | `string` | mês abreviado | Rótulo do eixo. |
| `value` | `number` | moeda, 0 casas | Receita do mês; o último é o valor do card. |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js
incomeTrend: [
  { month: 'Apr', value: 4212 }, { month: 'May', value: 6650 }, { month: 'Jun', value: 9400 }, { month: 'Jul', value: 12800 },
  { month: 'Aug', value: 16000 }, { month: 'Sep', value: 18000 }, { month: 'Oct', value: 20441 }, { month: 'Nov', value: 24900 },
  { month: 'Dec', value: 32134 }, { month: 'Jan', value: 29800 }, { month: 'Feb', value: 31348 }, { month: 'Mar', value: 32134 }
]
```

### Configurações do widget

Padrão em `state.incomeTrend`: `{ period: 8, showMilestones: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `period` | select | `8` (Last 8 months) · `12` (Last 12 months) | Visible range | 8 ou 12 meses. |
| `showMilestones` | input checkbox | booleano | Show value markers | Pílulas no 1º, no meio e no último mês. |

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
| `data-change-value` | Span que `setChange()` preenche com a variação percentual. |
| `data-widget-filter` | Criado pelo JS (`addFilterAction`): botão “Filter” no canto do card, abre a gaveta `#widget-filter-drawer` com busca e faixa mín./máx. |

### Funções e eventos

| Função / evento | O que faz |
|---|---|
| `renderIncomeTrend()` | Valor, variação, faixas, marcos, rótulos de mês e `aria-label` com todos os meses. |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- **Pronto:** `GET /api/v1/domain/records/financial/analytics/revenue?per_page=12` (view `inst_billing_reports`: `competence`, `billed`, `received`), permissão `admin.financial.view` (a mesma das rotas `/financial/*` em `app/Config/page-domain-sources.php`).
- Exportação: `…/financial/analytics/revenue/export?format=csv`.

## Acessibilidade

- O `aria-label` lista todos os meses e valores — o fluxo em si não tem eixo Y, então essa é a alternativa textual.
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
$endpoint = '/api/v1/domain/records/financial/analytics/revenue?per_page=12';
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="incomeTrend"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="incomeTrend-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget income-trend-widget" data-widget="incomeTrend" aria-labelledby="income-trend-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-blue" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="income-trend-title">Income</h2>
          <button class="info-button" type="button" data-tip="Monthly income values across the selected number of months. The latest value matches the headline total." aria-label="About monthly income trend">
            i
          </button>
        </div>
        <p>Monthly income trend</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="incomeTrend" aria-label="Adjust income trend">
        <svg viewBox="0 0 20 20">…</svg>
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" aria-label="More income trend actions" aria-expanded="false" data-menu="incomeTrend">
          <svg viewBox="0 0 20 20">…</svg>
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="incomeTrend">Download CSV</button>
          <button type="button" data-reset="incomeTrend">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="flow-income-summary">
    <strong class="widget-value" id="income-trend-value"></strong>
    <span class="metric-change is-positive" id="income-trend-change">
      <svg viewBox="0 0 16 16">…</svg>
      <span data-change-value></span>
    </span>
    <span class="metric-context">vs previous month</span>
  </div>
  <div class="income-stream-wrap trend-stream-wrap">
    <svg id="income-trend-chart" viewBox="0 0 440 220" role="img" aria-label="Monthly income trend"></svg>
  </div>
  <footer class="ttsc-analytics-foot widget-foot">
    <span>Monthly recorded income</span>
    <span id="income-trend-period-label"></span>
  </footer>
  <dialog class="widget-settings" id="settings-incomeTrend" aria-labelledby="settings-income-trend-title">
    <form method="dialog">
      <header>
        <div>
          <span class="settings-icon">↗</span>
          <div>
            <h3 id="settings-income-trend-title">Income trend settings</h3>
            <p>Settings apply to this widget only.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close settings">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Visible range
          <select data-setting="incomeTrend" data-key="period">
            <option value="8" selected>Last 8 months</option>
            <option value="12">Last 12 months</option>
          </select>
        </label>
        <label class="settings-check">
          <input type="checkbox" data-setting="incomeTrend" data-key="showMilestones" checked>
          Show value markers
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
.sales-flow-wrap svg, .income-stream-wrap svg { display: block; width: 100%; height: 100%; overflow: visible; }
.flow-income-summary { display: flex; min-height: 39px; align-items: center; gap: 9px; margin: -2px 0 0; }
.flow-income-summary .widget-value { font-size: 27px; }
.income-stream-wrap { min-height: 165px; flex: 1 1 auto; margin: 3px -5px 0; }
.trend-stream-wrap { min-height: 175px; }
.income-flow-marker line, .trend-marker line { stroke: var(--w-surface); stroke-width: 1.5; }
.income-flow-marker rect, .trend-marker rect { fill: var(--w-surface); stroke: #eef2f7; filter: drop-shadow(0 2px 3px rgb(15 23 42 / .10)); }
.income-flow-marker text, .trend-marker text { fill: var(--w-text); font: 600 9px var(--ttsc-font-mono, ui-monospace, monospace); text-anchor: middle; }
.trend-month { fill: var(--w-muted); font: 9px var(--ttsc-font-sans, Inter, sans-serif); text-anchor: middle; }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Marcos e meses com tokens do tema */
.trend-marker rect { fill: var(--ttsc-surface); stroke: var(--ttsc-border); }
.trend-month { fill: var(--ttsc-text-muted); }
```

### JS

Render real em `widgets.js`:

```js
function renderIncomeTrend() {
  const count = Number(state.incomeTrend.period);
  const rows = data.incomeTrend.slice(-count);
  const values = rows.map(row => row.value);
  const total = values[values.length - 1] || 0;
  const previous = values[values.length - 2] || total;
  const change = percentChange(total, previous);
  const maxTotal = Math.max(...values, 1);
  const xs = values.map((_, index) => 18 + index * (404 / Math.max(1, values.length - 1)));
  const colors = ['#d4e8ff', '#a6d0ff', '#6fb0fa', '#347fe8'];
  const shares = [.16, .28, .34, .22];
  const bands = colors.map((color, index) => `<path d="${streamPath(values, shares, index, maxTotal, xs, 108, 66)}" fill="${color}"/>`).join('');
  const markerIndices = [...new Set([0, Math.floor((rows.length - 1) / 2), rows.length - 1])];
  const markers = state.incomeTrend.showMilestones ? markerIndices.map(index => {
    const x = xs[index];
    return `<g class="trend-marker"><line x1="${x.toFixed(1)}" y1="28" x2="${x.toFixed(1)}" y2="178"/><rect x="${(x - 38).toFixed(1)}" y="93" width="76" height="26" rx="13"/><text x="${x.toFixed(1)}" y="110">${fmtWhole(values[index])}</text></g>`;
  }).join('') : '';
  const labels = rows.map((row, index) => `<text class="trend-month" x="${xs[index].toFixed(1)}" y="203">${row.month}</text>`).join('');
  byId('income-trend-value').textContent = fmtWhole(total);
  setChange(byId('income-trend-change'), change);
  byId('income-trend-period-label').textContent = `${rows[0].month}–${rows[rows.length - 1].month} · sample`;
  byId('income-trend-chart').innerHTML = `<defs><radialGradient id="trend-halo"><stop stop-color="#2684e8" stop-opacity=".16"/><stop offset="1" stop-color="#2684e8" stop-opacity="0"/></radialGradient></defs><ellipse cx="220" cy="108" rx="218" ry="102" fill="url(#trend-halo)"/>${bands}${markers}${labels}`;
  byId('income-trend-chart').setAttribute('aria-label', `Monthly income from ${rows[0].month} through ${rows[rows.length - 1].month}. ${rows.map(row => `${row.month}: ${fmtWhole(row.value)}`).join('; ')}.`);
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

// records (inst_billing_reports): [{ competence: '2026-09', billed: '31348.00', received: '29800.00' }, …]
loadWidget('incomeTrend', rows => {
  data.incomeTrend = rows
    .slice().sort((a, b) => String(a.competence).localeCompare(String(b.competence)))
    .map(row => ({
      month: new Intl.DateTimeFormat('pt-BR', { month: 'short' }).format(new Date(`${row.competence}-01T00:00:00`)).replace('.', ''),
      value: Number(row.billed) || 0,
    }));
});
```

O menu “Download CSV” chama `downloadCsv('incomeTrend')`, que serializa a **série de amostra** (`incomeTrend-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Faturamento por competência, com a mesma regra da view `inst_billing_reports` (exclui `cancelled`/`draft`). Testado no MariaDB local.

```sql
-- Faturamento por competência (mesma regra da view inst_billing_reports), últimos :months meses
SELECT CONCAT(i.competence_year, '-', LPAD(i.competence_month, 2, '0')) AS competence,
       SUM(i.net_amount)                                                 AS billed,
       SUM(COALESCE(i.paid_amount, 0))                                    AS received
  FROM billing_invoices i
 WHERE i.deleted_at IS NULL
   AND i.status NOT IN ('cancelled', 'draft')
   AND i.competence_year IS NOT NULL
   AND MAKEDATE(i.competence_year, 1) + INTERVAL (i.competence_month - 1) MONTH
       >= DATE_FORMAT(CURDATE() - INTERVAL (:months - 1) MONTH, '%Y-%m-01')   -- :months = 8 | 12
 GROUP BY i.competence_year, i.competence_month
 ORDER BY i.competence_year, i.competence_month;
```

O endpoint de domínio já devolve esse resultado (ordenado por `created_at DESC`): o JS reordena por `competence`.

## Faça / Não faça

- **Faça:** ordenar cronologicamente antes de renderizar;
- **Faça:** manter `aria-label` com todos os valores.
- **Não faça:** usar o fluxo quando o usuário precisa ler valores intermediários exatos;
- **Não faça:** misturar faturado e recebido na mesma série.
