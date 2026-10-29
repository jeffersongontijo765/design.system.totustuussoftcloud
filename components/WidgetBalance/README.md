# WidgetBalance

Card “Total balance”: saldo de fechamento do último mês, variação contra o mês anterior e colunas mensais (Chart.js) com linha de média tracejada.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só o card `balance`. Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Mostrar o saldo de caixa da instituição mês a mês (razão `financial_transactions`) num painel financeiro.
- Quando a pergunta é “quanto temos agora e como chegamos aqui” em 6, 7 ou 12 meses.
- Para a evolução contínua de uma receita use [WidgetIncomeStatistics](../WidgetIncomeStatistics/README.md) (linha); para um único número sem série use [KpiView](../KpiView/README.md).
- Não use para comparar categorias (colunas aqui são tempo, não categorias).

## Anatomia

```
┌ ícone · Total balance (i) ───────────────── [ajustes] [⋯] ┐
│ $120,467.00  (↗ 12%)  vs prior month                       │
│ ▁ ▃ ▂ ▅ ▄ ▅ █   - - - Avg $…                               │  canvas#balance-chart
│ ■ Closing balance                      Jan–Jul · sample    │
└────────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Card | `article.ttsc-analytics-card.widget.demo-widget[data-widget="balance"]` | sim |
| Cabeçalho | `header.ttsc-analytics-head.widget-head` > `.widget-heading` (ícone `.widget-icon.tone-blue`, `h2#balance-title`, `.info-button[data-tip]`) | sim |
| Ações | `.widget-actions` > `.widget-config[data-open-settings]` + `.widget-menu-wrap` (`.widget-more[data-menu]`, `.widget-menu`) | sim |
| Métrica | `.metric-row` > `strong.widget-value#balance-value`, `span.metric-change#balance-change` (`[data-change-value]`), `.metric-context` | sim |
| Gráfico | `.ttsc-analytics-plot.widget-plot.balance-plot` > `canvas#balance-chart[role="img"]` | sim |
| Rodapé | `footer.ttsc-analytics-foot.widget-foot` (legenda `.legend-swatch` + `#balance-period-label`) | sim |
| Configurações | `dialog.widget-settings#settings-balance` | sim |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('balance')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Após “Apply settings” o diálogo grava em `state.balance` e re-renderiza só este widget; o toast `#widget-toast` confirma. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Variação negativa | `setChange()` aplica `.is-negative` em `.metric-change` (vermelho) quando o último mês fecha abaixo do anterior. |
| Sem média | `state.balance.average = false` esconde a linha do plugin `widgetReferenceLine`. |

## API

### Dados esperados

Uma série mensal de saldos de fechamento, em ordem cronológica; o widget usa os últimos `state.balance.period` valores e destaca o último.

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `data.balance[]` | `number[]` | moeda, 2 casas (`fmtMoney`) | Saldo de fechamento de cada mês; o último é o valor do card. |
| rótulos | `string[]` | mês abreviado | Hoje vêm da constante `months` (`Jan`…`Dec`); com dados reais, envie o mês junto (ver JS). |
| variação | derivado | % | `(atual − anterior) / anterior × 100`. |
| média | derivado | moeda | `mean(values)` desenhada como referência. |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js
balance: [88560, 92770, 90850, 104250, 97480, 103920, 100840, 111950, 108600, 119780, 114350, 120467]
```

### Configurações do widget

Padrão em `state.balance`: `{ period: 7, average: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `period` | select | `6` (Last 6 months) · `7` (Last 7 months) · `12` (Last 12 months) | Reporting period | Quantos meses entram no gráfico e no rótulo do rodapé. |
| `average` | input checkbox | booleano | Show average reference | Liga a linha `Avg $…` (plugin `widgetReferenceLine`). |

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
| `renderBalance()` | Atualiza valor, variação, rótulo do período e a instância `charts.balance` (cria na 1ª vez, depois `update()`). |
| `chartBase()` | Opções comuns Chart.js: tooltip externo `renderCanvasTooltip`, eixos com `tone()`, `interaction.mode = index`. |
| Plugin `widgetReferenceLine` | Registrado com `Chart.register`; desenha a média tracejada com rótulo. |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- **Fonte pronta mais próxima:** `GET /api/v1/domain/records/financial/analytics/cash-flow?per_page=12` (view `inst_fin_cash_flow`: `month`, `inflow`, `outflow`, `net_flow`), permissão `admin.financial.view` (a mesma das rotas `/financial/*` em `app/Config/page-domain-sources.php`). Ela dá o fluxo líquido, não o saldo; o saldo de fechamento sai da consulta SQL abaixo.
- **Recomendado:** expor a consulta SQL num provider do módulo financeiro com o mesmo guard e devolver `{ "rows": [{ "month": "2026-04", "closing_balance": 104250.00 }, …] }`.
- Exportação real: `GET /api/v1/domain/records/financial/analytics/cash-flow/export?format=csv`.

## Acessibilidade

- O canvas tem `tabindex="0"` e `aria-label` “Use arrow keys to inspect values”: as setas navegam pelos pontos com o tooltip do `ttsc.chart-defaults.js`.
- A cor de destaque (último mês, `#2684e8`) nunca é a única pista: valor e variação estão em texto no topo.
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
$endpoint = '/api/v1/domain/records/financial/analytics/cash-flow?per_page=12';
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="balance"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="balance-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget" data-widget="balance" aria-labelledby="balance-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-blue" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="balance-title">Total balance</h2>
          <button class="info-button" type="button" data-tip="Current balance across connected accounts for the selected period." aria-label="About total balance">
            i
          </button>
        </div>
        <p>Monthly balance movement</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="balance" aria-label="Adjust total balance chart">
        <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" aria-label="More total balance actions" aria-expanded="false" data-menu="balance">
          <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="balance">Download CSV</button>
          <button type="button" data-reset="balance">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="metric-row">
    <strong class="widget-value" id="balance-value">$120,467.00</strong>
    <span class="metric-change is-positive" id="balance-change">
      <svg viewBox="0 0 16 16" aria-hidden="true">…</svg>
      <span data-change-value>12%</span>
    </span>
    <span class="metric-context">vs prior month</span>
  </div>
  <div class="ttsc-analytics-plot widget-plot balance-plot">
    <canvas id="balance-chart" tabindex="0" role="img" aria-label="Monthly account balances. Use arrow keys to inspect values."></canvas>
  </div>
  <footer class="ttsc-analytics-foot widget-foot">
    <span class="widget-legend"><i class="legend-swatch tone-blue"></i>Closing balance</span>
    <span id="balance-period-label">Jan–Jul · sample</span>
  </footer>
  <dialog class="widget-settings" id="settings-balance" aria-labelledby="settings-balance-title">
    <form method="dialog">
      <header>
        <div>
          <span class="settings-icon"><svg viewBox="0 0 20 20" aria-hidden="true">…</svg></span>
          <div>
            <h3 id="settings-balance-title">Total balance settings</h3>
            <p>Settings apply to this chart only.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close settings">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Reporting period
          <select data-setting="balance" data-key="period">
            <option value="6">Last 6 months</option>
            <option value="7" selected>Last 7 months</option>
            <option value="12">Last 12 months</option>
          </select>
        </label>
        <label class="settings-check">
          <input type="checkbox" data-setting="balance" data-key="average" checked>
          Show average reference
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
.widget-value { display: block; color: var(--w-text); font-size: 25px; font-variant-numeric: tabular-nums; font-weight: 600; letter-spacing: -.035em; line-height: 1.15; }
.metric-row, .income-summary { display: flex; min-height: 34px; align-items: center; gap: 9px; }
.metric-change { display: inline-flex; align-items: center; gap: 3px; padding: 3px 7px; border: 1px solid #a7f3d0; border-radius: 999px; background: var(--w-green-soft); color: #047857; font-size: 10px; font-weight: 600; line-height: 1.2; /* … */ }
.metric-change.is-negative { border-color: #fecaca; background: #fef2f2; color: #b91c1c; }
.metric-change > svg { width: 12px; height: 12px; fill: none; stroke: currentColor; stroke-width: 1.3; stroke-linecap: round; stroke-linejoin: round; }
.metric-change.is-negative > svg { transform: rotate(90deg); }
.balance-plot.ttsc-analytics-plot { height: 205px; margin-top: 8px; }
.widget-legend { display: inline-flex; align-items: center; gap: 6px; margin-right: 12px; color: var(--w-muted); font-size: 10px; }
.legend-swatch { display: inline-block; width: 8px; height: 8px; border-radius: 3px; background: var(--w-blue); }
.legend-swatch.is-dashed { width: 15px; height: 0; border-top: 1px dashed var(--w-muted); border-radius: 0; background: transparent; }
.breakdown-summary .metric-change { margin-left: auto; }
.metric-row > div { display: flex; align-items: baseline; gap: 7px; }
.metric-row > div .widget-value { display: inline; }
.metric-row > div .metric-context { white-space: nowrap; }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Painel financeiro mais alto e destaque no verde da marca */
.balance-plot.ttsc-analytics-plot { height: 240px; }
[data-widget="balance"] .legend-swatch.tone-blue { background: var(--ttsc-accent); }
/* As cores das barras vêm do JS (COLORS.blue / #dbe4ed / #323745 no escuro): para trocar, altere COLORS na cópia de produção. */
```

### JS

Render real em `widgets.js`:

```js
function renderBalance() {
  const count = Number(state.balance.period);
  const values = data.balance.slice(-count);
  const labels = months.slice(-count);
  const current = values[values.length - 1] || 0;
  const previous = values[values.length - 2] || current;
  const change = previous ? ((current - previous) / previous) * 100 : 0;
  byId('balance-value').textContent = fmtMoney(current);
  setChange(byId('balance-change'), change);
  byId('balance-period-label').textContent = `${labels[0]}–${labels[labels.length - 1]} · sample`;
  if (!chartAvailable) return;
  const average = mean(values);
  const config = Object.assign(chartBase(), {
    plugins: Object.assign(chartBase().plugins, { widgetReferenceLine: { display: state.balance.average, value: average, label: `Avg ${fmtMoney(average, 0)}` } }),
    scales: Object.assign(chartBase().scales, { y: Object.assign(chartBase().scales.y, { beginAtZero: true, ticks: Object.assign(chartBase().scales.y.ticks, { callback: value => `$${fmtCompact(value)}` }) }) })
  });
  const dataset = { label: 'Closing balance', data: values, backgroundColor: values.map((_, index) => index === values.length - 1 ? COLORS.blue : '#dbe4ed'), borderColor: values.map((_, index) => index === values.length - 1 ? COLORS.blue : '#dbe4ed'), borderWidth: 1, borderRadius: 6, borderSkipped: false, maxBarThickness: 28 };
  if (charts.balance) { charts.balance.data.labels = labels; charts.balance.data.datasets = [dataset]; charts.balance.options.plugins.widgetReferenceLine = config.plugins.widgetReferenceLine; charts.balance.options.scales.y.beginAtZero = true; charts.balance.options.scales.y.ticks.callback = config.scales.y.ticks.callback; charts.balance.update(); }
  else charts.balance = new Chart(byId('balance-chart'), { type: 'bar', data: { labels, datasets: [dataset] }, options: config });
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

// Saldo: rows = [{ month: '2026-04', closing_balance: '104250.00' }, …] (consulta SQL abaixo)
// Na cópia de produção troque, em renderBalance(), `const labels = months.slice(-count);`
// por `const labels = (data.balanceLabels || months).slice(-count);`
loadWidget('balance', rows => {
  const ordered = rows.slice().sort((a, b) => String(a.month).localeCompare(String(b.month)));
  data.balance = ordered.map(row => Number(row.closing_balance ?? row.net_flow) || 0);
  data.balanceLabels = ordered.map(row => new Intl.DateTimeFormat('pt-BR', { month: 'short' })
    .format(new Date(`${row.month}-01T00:00:00`)).replace('.', ''));
  return data.balance.length > 0;
});
```

O menu “Download CSV” chama `downloadCsv('balance')`, que serializa a **série de amostra** (`balance-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Saldo de fechamento por mês a partir do razão (`financial_transactions`, `type` = `credit`/`debit`, mesma convenção da view `inst_fin_cash_flow`). A soma acumulada (`SUM() OVER`) usa todo o histórico e o filtro de meses vem depois, para o primeiro mês já sair com o saldo correto. Testado no MariaDB 10.11 local; roda também em MySQL 8.

```sql
-- Saldo de fechamento por mês (razão financeiro): saldo acumulado até o fim de cada mês
WITH monthly AS (
  SELECT DATE_FORMAT(t.transaction_date, '%Y-%m') AS month,
         SUM(CASE WHEN t.type = 'credit' THEN t.amount ELSE -t.amount END) AS net_flow
    FROM financial_transactions t
   WHERE t.transaction_date IS NOT NULL
     AND t.transaction_date < DATE_FORMAT(CURDATE() + INTERVAL 1 MONTH, '%Y-%m-01')
   GROUP BY DATE_FORMAT(t.transaction_date, '%Y-%m')
), running AS (
  SELECT month, net_flow, SUM(net_flow) OVER (ORDER BY month) AS closing_balance
    FROM monthly
)
SELECT month, closing_balance, net_flow
  FROM running
 WHERE month >= DATE_FORMAT(CURDATE() - INTERVAL (:months - 1) MONTH, '%Y-%m')   -- :months = 6 | 7 | 12
 ORDER BY month;
```

O provider executa com `:months` = `state.balance.period` (ou sempre 12, deixando o corte para o JS), converte `DECIMAL` em número e responde JSON; a view PHP só grava `data-endpoint`. Saldos por conta ficam em `financial_bank_accounts.balance` quando o card for de uma conta só.

## Faça / Não faça

- **Faça:** manter `aria-label` do canvas e textos de topo atualizados a cada render;
- **Faça:** enviar o mês com o valor (rótulos reais) quando a série não terminar em dezembro;
- **Faça:** usar o período configurado também na exportação.
- **Não faça:** gravar os números de amostra em controller, seed ou default;
- **Não faça:** misturar moedas na mesma série;
- **Não faça:** reaproveitar o card para categorias — use barras horizontais ([WidgetTimeByCategory](../WidgetTimeByCategory/README.md)).
