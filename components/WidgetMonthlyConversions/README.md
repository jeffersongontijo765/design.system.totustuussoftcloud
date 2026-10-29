# WidgetMonthlyConversions

Card “Monthly conversions”: total de conversões no período e barras mensais em SVG com eixo, rótulo de valor e destaque no mês de maior resultado.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só o card `monthlyConversion`. Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Contar eventos de conversão por mês: leads do CRM convertidos em negociação (`crm_leads.converted_at`), matrículas confirmadas.
- Séries de 6 ou 12 meses de contagens inteiras.
- Para valores monetários use [WidgetBalance](../WidgetBalance/README.md) ou [WidgetIncomeStatistics](../WidgetIncomeStatistics/README.md); para a fotografia do funil, [WidgetConversionRate](../WidgetConversionRate/README.md).

## Anatomia

```
┌ ícone · Monthly conversions (i) ────── [ajustes] [⋯] ┐
│ 312  total conversions  (↗ …)                         │  #monthly-conversion-value
│ 150┤        105                                       │  svg#monthly-conversion-chart
│  50┤  86 99 ██ 78 96 88                               │  rect.conversion-bar(.is-highlight)
│     Jan Feb Mar Apr May Jun                           │
│ Completed conversions               Jan–Jun · sample  │
└───────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Resumo | `.metric-row` > `strong.widget-value#monthly-conversion-value` + `.metric-change#monthly-conversion-change` | sim |
| Gráfico | `.ttsc-analytics-plot.activity-bar-plot` > `svg#monthly-conversion-chart.monthly-conversion-chart` (`line.conversion-gridline`, `text.conversion-axis-label`, `rect.conversion-bar`, `text.conversion-value`, `text.conversion-month`) | sim |
| Rodapé | `#monthly-conversion-period-label` | sim |
| Configurações | `dialog#settings-monthlyConversion` | sim |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('monthlyConversion')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Após “Apply settings” o diálogo grava em `state.monthlyConversion` e re-renderiza só este widget; o toast `#widget-toast` confirma. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Destaque | O maior valor recebe `.is-highlight` (barra e textos). |
| Sem comparação | `state.monthlyConversion.showChange = false` esconde `#monthly-conversion-change`. |

## API

### Dados esperados

Vetor de 12 contagens (Jan…Dez). Atenção: o render usa `data.monthlyConversions.slice(-count)` para os valores, mas `months.slice(0, values.length)` para os rótulos — com dados reais, envie os rótulos junto.

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `data.monthlyConversions[]` | `number[]` | contagem inteira | Conversões do mês. |
| eixo | derivado | múltiplos de 50 | `axisMax = max(50, ceil(max/50)·50)`. |
| total | derivado | inteiro `en-US` | Soma exibida no topo. |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js
monthlyConversions: [86, 99, 105, 78, 96, 88, 20, 98, 32, 42, 120, 0]
```

### Configurações do widget

Padrão em `state.monthlyConversion`: `{ period: 6, showChange: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `period` | select | `6` (Last 6 months) · `12` (Last 12 months) | Reporting period | 6 ou 12 meses. |
| `showChange` | input checkbox | booleano | Show period comparison | Mostra a pílula de variação. |

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
| `renderMonthlyConversions()` | Total, grade de 4 linhas, barras com `<title>` por mês e `aria-label` completo. |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- **Pronto (lista):** `GET /api/v1/domain/records/developer/commercial/leads` (fonte `crm_leads`, permissão `commercial.developer.leads.view`).
- **Recomendado:** provider do CRM com a consulta abaixo (`?months=6|12`) → `{ "rows": [{ "month": "2026-05", "conversions": 96 }] }`.

## Acessibilidade

- Cada barra tem `<title>` “Mês: N conversions” e o SVG um `aria-label` com todos os meses; o destaque também é indicado pelo valor em texto.
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
$endpoint = '/api/v1/domain/records/developer/commercial/leads';
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="monthlyConversion"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="monthlyConversion-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget activity-widget" data-widget="monthlyConversion" aria-labelledby="monthly-conversion-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-purple" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="monthly-conversion-title">Monthly conversions</h2>
          <button class="info-button" type="button" data-tip="Completed conversions recorded in each month of the selected period." aria-label="About monthly conversions">
            i
          </button>
        </div>
        <p>Completed conversions by month</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="monthlyConversion" aria-label="Adjust monthly conversions chart">
        <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" aria-label="More monthly conversions actions" aria-expanded="false" data-menu="monthlyConversion">
          <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="monthlyConversion">Download CSV</button>
          <button type="button" data-reset="monthlyConversion">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="metric-row">
    <div>
      <strong class="widget-value" id="monthly-conversion-value">312</strong>
      <span class="metric-context">total conversions</span>
    </div>
    <span class="metric-change is-positive" id="monthly-conversion-change">
      <svg viewBox="0 0 16 16" aria-hidden="true">…</svg>
      <span data-change-value>29.3%</span>
    </span>
  </div>
  <div class="ttsc-analytics-plot activity-bar-plot">
    <svg id="monthly-conversion-chart" class="monthly-conversion-chart" viewBox="0 0 440 190" role="img" aria-label="Monthly conversions by month."></svg>
  </div>
  <footer class="ttsc-analytics-foot widget-foot">
    <span>Completed conversions</span>
    <span id="monthly-conversion-period-label">Jan–Jun · sample</span>
  </footer>
  <dialog class="widget-settings" id="settings-monthlyConversion" aria-labelledby="settings-monthly-conversion-title">
    <form method="dialog">
      <header>
        <div>
          <span class="settings-icon"><svg viewBox="0 0 20 20" aria-hidden="true">…</svg></span>
          <div>
            <h3 id="settings-monthly-conversion-title">Monthly conversions settings</h3>
            <p>Settings apply to this chart only.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close settings">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Reporting period
          <select data-setting="monthlyConversion" data-key="period">
            <option value="6" selected>Last 6 months</option>
            <option value="12">Last 12 months</option>
          </select>
        </label>
        <label class="settings-check">
          <input type="checkbox" data-setting="monthlyConversion" data-key="showChange" checked>
          Show period comparison
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
.activity-bar-plot.ttsc-analytics-plot { height: 245px; margin-top: 9px; }
.monthly-conversion-chart { display: block; width: 100%; height: 100%; overflow: visible; }
.conversion-gridline { stroke: var(--w-grid); stroke-width: 1; }
.conversion-axis-label { fill: var(--w-muted); font: 9px var(--ttsc-font-sans, Inter, sans-serif); text-anchor: end; }
.conversion-month { fill: var(--w-muted); font: 10px var(--ttsc-font-sans, Inter, sans-serif); text-anchor: middle; }
.conversion-month.is-highlight, .conversion-value.is-highlight { fill: #7653f9; font-weight: 700; }
.conversion-value { fill: var(--w-text); font: 10px var(--ttsc-font-sans, Inter, sans-serif); text-anchor: middle; }
.conversion-bar { fill: #ded6ff; }
.conversion-bar.is-highlight { fill: #7653f9; }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Destaque com o verde da marca */
[data-widget="monthlyConversion"] .conversion-bar.is-highlight { fill: var(--ttsc-accent); }
[data-widget="monthlyConversion"] .conversion-value.is-highlight { fill: var(--ttsc-accent-text); }
```

### JS

Render real em `widgets.js`:

```js
function renderMonthlyConversions() {
  const count = Number(state.monthlyConversion.period);
  const values = data.monthlyConversions.slice(-count);
  const labels = months.slice(0, values.length);
  const total = sum(values);
  byId('monthly-conversion-value').textContent = new Intl.NumberFormat('en-US').format(total);
  byId('monthly-conversion-change').hidden = !state.monthlyConversion.showChange;
  byId('monthly-conversion-period-label').textContent = `${labels[0]}–${labels[labels.length - 1]} · sample`;
  const max = Math.max(...values, 1);
  const axisMax = Math.max(50, Math.ceil(max / 50) * 50);
  const left = 38, right = 432, top = 24, baseline = 154, height = baseline - top;
  const slot = (right - left) / values.length;
  const barWidth = Math.min(34, slot * .52);
  const highlight = values.reduce((best, value, index) => value >= values[best] ? index : best, 0);
  const grid = [0, 1, 2, 3].map(index => {
    const value = axisMax * (3 - index) / 3;
    const y = top + height * index / 3;
    return `<line class="conversion-gridline" x1="${left}" y1="${y}" x2="${right}" y2="${y}"/><text class="conversion-axis-label" x="${left - 7}" y="${y + 3}">${Math.round(value)}</text>`;
  }).join('');
  const bars = values.map((value, index) => {
    const barHeight = value > 0 ? Math.max(3, value / axisMax * height) : 2;
    const x = left + index * slot + (slot - barWidth) / 2;
    const y = baseline - barHeight;
    const highlighted = index === highlight;
    const valueY = Math.max(top - 1, y - 6);
    return `<g><title>${labels[index]}: ${value} conversions</title><rect class="conversion-bar${highlighted ? ' is-highlight' : ''}" x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${barWidth.toFixed(1)}" height="${barHeight.toFixed(1)}" rx="${Math.min(14, barWidth / 2).toFixed(1)}"/><text class="conversion-value${highlighted ? ' is-highlight' : ''}" x="${(x + barWidth / 2).toFixed(1)}" y="${valueY.toFixed(1)}">${value}</text><text class="conversion-month${highlighted ? ' is-highlight' : ''}" x="${(x + barWidth / 2).toFixed(1)}" y="176">${labels[index]}</text></g>`;
  }).join('');
  byId('monthly-conversion-chart').innerHTML = `${grid}${bars}`;
  byId('monthly-conversion-chart').setAttribute('aria-label', `${total} completed conversions. ${labels.map((label, index) => `${label}: ${values[index]}`).join('; ')}.`);
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

// rows = [{ month: '2026-05', conversions: 96 }, …]  (meses sem conversão preenchidos com 0 no provider)
// Na cópia de produção troque `const labels = months.slice(0, values.length)` por `(data.monthlyConversionLabels || months).slice(-count)`.
loadWidget('monthlyConversion', rows => {
  const ordered = rows.slice().sort((a, b) => a.month.localeCompare(b.month));
  data.monthlyConversions = ordered.map(row => Number(row.conversions) || 0);
  data.monthlyConversionLabels = ordered.map(row => new Intl.DateTimeFormat('pt-BR', { month: 'short' }).format(new Date(`${row.month}-01T00:00:00`)).replace('.', ''));
});
```

O menu “Download CSV” chama `downloadCsv('monthlyConversion')`, que serializa a **série de amostra** (`monthlyConversion-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Leads marcados como convertidos (`converted_to_deal = 1`) agrupados pelo mês de `converted_at`. Testado no MariaDB local.

```sql
-- Leads do CRM convertidos em negociação por mês
SELECT DATE_FORMAT(l.converted_at, '%Y-%m') AS month,
       COUNT(*)                             AS conversions
  FROM crm_leads l
 WHERE l.deleted_at IS NULL
   AND l.converted_to_deal = 1
   AND l.converted_at >= DATE_FORMAT(CURDATE() - INTERVAL (:months - 1) MONTH, '%Y-%m-01')   -- 6 | 12
 GROUP BY DATE_FORMAT(l.converted_at, '%Y-%m')
 ORDER BY month;
```

Para matrículas confirmadas, a mesma forma vale com `enrollment_requests.confirmed_at` e `status = 'confirmed'`.

## Faça / Não faça

- **Faça:** corrigir os rótulos quando a série não começar em janeiro;
- **Faça:** preencher meses sem conversão com 0.
- **Não faça:** usar para valores monetários (o eixo é inteiro);
- **Não faça:** remover o `<title>` das barras.
