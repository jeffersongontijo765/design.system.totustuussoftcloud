# WidgetIncomeStatistics

Card largo “Income statistics”: total recebido no período e linha histórica mensal (Chart.js, área preenchida) com média de referência.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só o card `income` (largo, `widget-wide`). Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Mostrar a receita efetivamente recebida mês a mês (baixas em `billing_payments`) em 6 ou 12 meses.
- Quando a forma da curva (sazonalidade de matrícula, rematrícula, férias) importa mais que cada valor.
- Para saldo acumulado use [WidgetBalance](../WidgetBalance/README.md); para comparar períodos fechados (semana/mês/ano) use [WidgetSalesReport](../WidgetSalesReport/README.md).

## Anatomia

```
┌ ícone · Income statistics (i) ───────────────────────────── [ajustes] [⋯] ┐
│ $12,596.98  (↗ …)                                                        │  #income-value
│      ╱╲    ╱╲  ╱‾‾╲      - - - Avg $1,050                                │  canvas#income-chart
│ ╱‾‾‾╯  ╲__╱  ╲╱    ╲__•                                                  │
│ ■ Recorded income                                    12 months · sample  │
└──────────────────────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Card largo | `article.ttsc-analytics-card.widget.demo-widget.widget-wide[data-widget="income"]` (ocupa 2 colunas do `.widgets-grid`) | sim |
| Resumo | `.income-summary` > `strong.widget-value#income-value` + `.metric-change` | sim |
| Gráfico | `.ttsc-analytics-plot.income-plot` > `canvas#income-chart[role="img"][tabindex="0"]` | sim |
| Rodapé | `.widget-legend` + `#income-period-label` | sim |
| Configurações | `dialog#settings-income` | sim |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('income')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Após “Apply settings” o diálogo grava em `state.income` e re-renderiza só este widget; o toast `#widget-toast` confirma. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Último ponto | Só o último mês tem ponto visível (`pointRadius` 3); os demais aparecem em hover/teclado. |

## API

### Dados esperados

Série mensal cronológica de valores recebidos; o card soma os últimos `state.income.period` meses.

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `data.income[]` | `number[]` | moeda, 2 casas | Valor recebido no mês. |
| rótulos | `string[]` | mês | Constante `months.slice(-count)`; com dados reais, envie o mês. |
| total | derivado | moeda | `sum(values)` no topo. |
| média | derivado | moeda | Linha `widgetReferenceLine`. |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js
income: [920, 1035, 870, 1175, 980, 1220, 1150, 940, 1275, 1080, 1340, 611.98]
```

### Configurações do widget

Padrão em `state.income`: `{ period: 12, average: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `period` | select | `6` (Last 6 months) · `12` (Last 12 months) | Reporting period | 6 ou 12 meses. |
| `average` | input checkbox | booleano | Show period average | Mostra a média tracejada. |

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
| `renderIncome()` | Total, rótulo e `charts.income` (`type: "line"`, `fill: true`, `tension: .18`). |
| `chartBase()` | Opções comuns (tooltip externo, eixos, `tone()`). |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- **Pronto:** `GET /api/v1/domain/records/financial/analytics/revenue?per_page=12` (view `inst_billing_reports`: `competence`, `invoices`, `billed`, `received`, `collection_rate`), permissão `admin.financial.view` (a mesma das rotas `/financial/*` em `app/Config/page-domain-sources.php`). Use `received` por `competence`.
- Alternativa por data de baixa: consulta SQL abaixo exposta num provider do módulo de cobrança.
- Exportação: `GET /api/v1/domain/records/financial/analytics/revenue/export?format=csv`.

## Acessibilidade

- Canvas focável com navegação por setas (`ttsc.chart-defaults.js`); o total está em texto acima do gráfico.
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
<article class="ttsc-analytics-card widget demo-widget widget-wide" data-widget="income"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="income-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget widget-wide" data-widget="income" aria-labelledby="income-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-blue" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="income-title">Income statistics</h2>
          <button class="info-button" type="button" data-tip="Recorded income observations by month. The dotted reference is the average for the selected period." aria-label="About income statistics">
            i
          </button>
        </div>
        <p>Recorded income across the selected period</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="income" aria-label="Adjust income statistics">
        <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" aria-label="More income statistics actions" aria-expanded="false" data-menu="income">
          <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="income">Download CSV</button>
          <button type="button" data-reset="income">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="income-summary">
    <strong class="widget-value" id="income-value">$12,596.98</strong>
    <span class="metric-change is-positive" id="income-change">
      <svg viewBox="0 0 16 16" aria-hidden="true">…</svg>
      <span data-change-value>12%</span>
    </span>
    <span class="metric-context">sample comparison</span>
  </div>
  <div class="ttsc-analytics-plot income-plot">
    <canvas id="income-chart" tabindex="0" role="img" aria-label="Monthly income history. Use arrow keys to inspect values."></canvas>
  </div>
  <footer class="ttsc-analytics-foot widget-foot">
    <span>
      <span class="widget-legend"><i class="legend-swatch tone-blue"></i>Recorded income</span>
      <span class="widget-legend"><i class="legend-swatch is-dashed"></i>Period average</span>
    </span>
    <span id="income-period-label">12 months · sample</span>
  </footer>
  <dialog class="widget-settings" id="settings-income" aria-labelledby="settings-income-title">
    <form method="dialog">
      <header>
        <div>
          <span class="settings-icon"><svg viewBox="0 0 20 20" aria-hidden="true">…</svg></span>
          <div>
            <h3 id="settings-income-title">Income statistics settings</h3>
            <p>Settings apply to this chart only.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close settings">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Reporting period
          <select data-setting="income" data-key="period">
            <option value="6">Last 6 months</option>
            <option value="12" selected>Last 12 months</option>
          </select>
        </label>
        <label class="settings-check">
          <input type="checkbox" data-setting="income" data-key="average" checked>
          Show period average
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
.metric-row, .income-summary { display: flex; min-height: 34px; align-items: center; gap: 9px; }
.widget-wide { grid-column: span 2; }
.income-summary { margin: -1px 0 0; }
.income-plot.ttsc-analytics-plot { height: 260px; margin-top: 2px; }
.widget-wide { grid-column: auto; }
.income-plot.ttsc-analytics-plot { height: 230px; }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Linha na cor de destaque do produto: o JS usa COLORS.blue; em produção, ajuste o dataset e mantenha a área com 10% de opacidade */
[data-widget="income"] .income-plot.ttsc-analytics-plot { height: 260px; }
```

### JS

Render real em `widgets.js`:

```js
function renderIncome() {
  const count = Number(state.income.period);
  const values = data.income.slice(-count);
  const labels = months.slice(-count);
  const average = mean(values);
  const total = sum(values);
  byId('income-value').textContent = fmtMoney(total);
  byId('income-period-label').textContent = `${count} months · sample`;
  if (!chartAvailable) return;
  const config = chartBase();
  config.scales.y.beginAtZero = true;
  config.scales.y.ticks.callback = value => `$${fmtCompact(value)}`;
  config.plugins.widgetReferenceLine = { display: state.income.average, value: average, label: `Avg ${fmtMoney(average, 0)}` };
  const dataset = { label: 'Recorded income', data: values, borderColor: COLORS.blue, backgroundColor: 'rgba(38,132,232,.10)', fill: true, tension: .18, pointRadius: values.map((_, index) => index === values.length - 1 ? 3 : 0), pointHoverRadius: 5, pointBackgroundColor: COLORS.blue, pointBorderColor: '#fff', pointBorderWidth: 2, borderWidth: 2 };
  if (charts.income) { charts.income.data.labels = labels; charts.income.data.datasets = [dataset]; charts.income.options.plugins.widgetReferenceLine = config.plugins.widgetReferenceLine; charts.income.options.scales.y.beginAtZero = true; charts.income.update(); }
  else charts.income = new Chart(byId('income-chart'), { type: 'line', data: { labels, datasets: [dataset] }, options: config });
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

// records do DomainCrudController (inst_billing_reports): [{ competence: '2026-09', received: '1340.00', … }]
// Na cópia de produção troque `const labels = months.slice(-count)` por `(data.incomeLabels || months).slice(-count)`.
loadWidget('income', rows => {
  const ordered = rows.slice().sort((a, b) => String(a.competence ?? a.month).localeCompare(String(b.competence ?? b.month)));
  data.income = ordered.map(row => Number(row.received) || 0);
  data.incomeLabels = ordered.map(row => String(row.competence ?? row.month).slice(5) + '/' + String(row.competence ?? row.month).slice(2, 4));
});
```

O menu “Download CSV” chama `downloadCsv('income')`, que serializa a **série de amostra** (`income-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Recebimentos por mês de baixa (`billing_payments.paid_at`, valor líquido). Testado no MariaDB local; para a visão por competência, a view `inst_billing_reports` já faz o agrupamento.

```sql
-- Receita recebida por mês (baixas de faturas), últimos :months meses
SELECT DATE_FORMAT(bp.paid_at, '%Y-%m') AS month,
       SUM(bp.net_amount)               AS received,
       COUNT(*)                         AS payments
  FROM billing_payments bp
 WHERE bp.paid_at >= DATE_FORMAT(CURDATE() - INTERVAL (:months - 1) MONTH, '%Y-%m-01')   -- :months = 6 | 12
 GROUP BY DATE_FORMAT(bp.paid_at, '%Y-%m')
 ORDER BY month;
```

O provider responde `{ "rows": [{ "month", "received", "payments" }] }`; meses sem baixa não aparecem — preencha com 0 no PHP para a linha não “pular” meses.

## Faça / Não faça

- **Faça:** preencher meses vazios com zero;
- **Faça:** manter o total do topo igual à soma exibida no gráfico.
- **Não faça:** misturar competência e data de pagamento na mesma série;
- **Não faça:** usar o card estreito: ele foi desenhado como `widget-wide`.
