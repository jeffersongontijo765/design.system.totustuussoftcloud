# WidgetIncomeFlow

Card “Income”: total recebido no período, variação contra o período anterior e um fluxo em três camadas roxas que cresce até o total, com marcos (semana 1, semana 2, total).

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só o card `incomeFlow`. Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Mostrar como a receita do mês (ou trimestre) foi se acumulando até o total — útil na semana de vencimento das mensalidades.
- Três marcos cumulativos crescentes (o último é o total).
- Para meses lado a lado use [WidgetIncomeTrend](../WidgetIncomeTrend/README.md); para regiões, [WidgetSalesReport](../WidgetSalesReport/README.md).

## Anatomia

```
┌ ícone · Income · Last 30 days ─────── [ajustes] [⋯] ┐
│ $32,134  (↗ 2.5%)  vs $31,348 prior period          │
│   ╭─$6,341─╮═══╭─$20,441─╮════╭─$32,134─╮            │  svg#income-flow-chart (3 faixas + marcos)
│   Week 1        Week 2         Month total           │
│ Checkpoint values build to the total  Month to date │
└─────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Resumo | `.flow-income-summary` > `#income-flow-value`, `.metric-change#income-flow-change`, `#income-flow-context` | sim |
| Subtítulo | `p#income-flow-subtitle` (Last 30/90 days) | sim |
| Fluxo | `.income-stream-wrap > svg#income-flow-chart` (halo radial, 3 `<path>`, `g.income-flow-marker` × 3) | sim |
| Rodapé | `#income-flow-period-label` | sim |
| Configurações | `dialog#settings-incomeFlow` | sim |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('incomeFlow')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Após “Apply settings” o diálogo grava em `state.incomeFlow` e re-renderiza só este widget; o toast `#widget-toast` confirma. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Sem marcos | `state.incomeFlow.showMilestones = false` mantém as pílulas mas sem valor. |

## API

### Dados esperados

Por período (`month`, `quarter`): total, total anterior, três marcos cumulativos e seus rótulos. As proporções das camadas são fixas (`shares = [.27, .43, .30]`).

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `total` | `number` | moeda, 0 casas | Receita do período (= último marco). |
| `previous` | `number` | moeda | Período anterior (variação). |
| `checkpoints[3]` | `number[]` | moeda, cumulativo | Valores acumulados em cada marco. |
| `labels[3]` | `string[]` | texto | Rótulo de cada marco. |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js
incomeFlow: {
  month: { total: 32134, previous: 31348, checkpoints: [6341, 20441, 32134], labels: ['Week 1', 'Week 2', 'Month total'] },
  quarter: { total: 94800, previous: 90000, checkpoints: [22100, 60400, 94800], labels: ['Month 1', 'Month 2', 'Quarter total'] }
}
```

### Configurações do widget

Padrão em `state.incomeFlow`: `{ period: 'month', showMilestones: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `period` | select | `month` (Last 30 days) · `quarter` (Last 90 days) | Reporting period | `month` ou `quarter`. |
| `showMilestones` | input checkbox | booleano | Show checkpoint labels | Escreve os valores nas pílulas. |

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
| `renderIncomeFlow()` | Valor, variação, contexto, subtítulo, faixas (`streamPath`) e marcos; `aria-label` com os marcos. |
| `streamPath()` / `smoothBoundary()` | Geometria das faixas suaves. |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- Não há rota pronta com marcos semanais. Exponha a consulta abaixo num provider do módulo financeiro (permissão `admin.financial.view` (a mesma das rotas `/financial/*` em `app/Config/page-domain-sources.php`)); para o trimestre, mesma forma com marcos mês 1, mês 2 e total.

## Acessibilidade

- O `aria-label` do SVG diz total, variação e os três marcos; os valores também estão nas pílulas.
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
$endpoint = '/financial/analytics/widgets/income-flow' /* rota do provider do módulo, a criar */;
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="incomeFlow"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="incomeFlow-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget income-flow-widget" data-widget="incomeFlow" aria-labelledby="income-flow-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-purple" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="income-flow-title">Income</h2>
          <button class="info-button" type="button" data-tip="Cumulative income checkpoints for the selected period. Checkpoints build to the headline total." aria-label="About income flow">
            i
          </button>
        </div>
        <p id="income-flow-subtitle">Last 30 days</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="incomeFlow" aria-label="Adjust income flow">
        <svg viewBox="0 0 20 20">…</svg>
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" aria-label="More income flow actions" aria-expanded="false" data-menu="incomeFlow">
          <svg viewBox="0 0 20 20">…</svg>
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="incomeFlow">Download CSV</button>
          <button type="button" data-reset="incomeFlow">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="flow-income-summary">
    <strong class="widget-value" id="income-flow-value"></strong>
    <span class="metric-change is-positive" id="income-flow-change">
      <svg viewBox="0 0 16 16">…</svg>
      <span data-change-value></span>
    </span>
    <span class="metric-context" id="income-flow-context"></span>
  </div>
  <div class="income-stream-wrap">
    <svg id="income-flow-chart" viewBox="0 0 440 220" role="img" aria-label="Cumulative income flow"></svg>
  </div>
  <footer class="ttsc-analytics-foot widget-foot">
    <span>Checkpoint values build to the total</span>
    <span id="income-flow-period-label"></span>
  </footer>
  <dialog class="widget-settings" id="settings-incomeFlow" aria-labelledby="settings-income-flow-title">
    <form method="dialog">
      <header>
        <div>
          <span class="settings-icon">↗</span>
          <div>
            <h3 id="settings-income-flow-title">Income flow settings</h3>
            <p>Settings apply to this widget only.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close settings">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Reporting period
          <select data-setting="incomeFlow" data-key="period">
            <option value="month" selected>Last 30 days</option>
            <option value="quarter">Last 90 days</option>
          </select>
        </label>
        <label class="settings-check">
          <input type="checkbox" data-setting="incomeFlow" data-key="showMilestones" checked>
          Show checkpoint labels
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
.income-flow-widget, .income-trend-widget { display: flex; min-height: 330px; flex-direction: column; }
.flow-income-summary { display: flex; min-height: 39px; align-items: center; gap: 9px; margin: -2px 0 0; }
.flow-income-summary .widget-value { font-size: 27px; }
.income-stream-wrap { min-height: 165px; flex: 1 1 auto; margin: 3px -5px 0; }
.income-flow-marker line, .trend-marker line { stroke: var(--w-surface); stroke-width: 1.5; }
.income-flow-marker rect, .trend-marker rect { fill: var(--w-surface); stroke: #eef2f7; filter: drop-shadow(0 2px 3px rgb(15 23 42 / .10)); }
.income-flow-marker text, .trend-marker text { fill: var(--w-text); font: 600 9px var(--ttsc-font-mono, ui-monospace, monospace); text-anchor: middle; }
.income-flow-marker .income-flow-step { fill: var(--w-muted); font: 9px var(--ttsc-font-sans, Inter, sans-serif); }
.income-flow-widget, .income-trend-widget { min-height: 340px; }
.income-flow-widget, .income-trend-widget { min-height: 310px; }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Pílulas de marco com superfície e borda do tema */
.income-flow-marker rect { fill: var(--ttsc-surface); stroke: var(--ttsc-border); }
.income-flow-marker text { fill: var(--ttsc-text); }
```

### JS

Render real em `widgets.js` (`tipAttrs()` devolve `tabindex="0" data-tip="…" aria-label="…"` para a marca abrir o tooltip comum em hover e foco):

```js
function renderIncomeFlow() {
  const selected = data.incomeFlow[state.incomeFlow.period];
  const change = percentChange(selected.total, selected.previous);
  const colors = ['#c7b6ff', '#9475f6', '#6544ec'];
  const xs = [24, 214, 416];
  const maxTotal = selected.total;
  const shares = [.27, .43, .30];
  const totals = selected.checkpoints;
  const bands = colors.map((color, index) => `<path class="income-flow-band" role="img" ${tipAttrs(`Income layer ${index + 1}: ${Math.round(shares[index] * 100)}% of each checkpoint · ${fmtWhole(selected.total * shares[index])} by ${selected.labels[selected.labels.length - 1]}`)} d="${streamPath(totals, shares, index, maxTotal, xs, 112, 78)}" fill="${color}"/>`).join('');
  const labels = selected.checkpoints.map((value, index) => {
    const x = xs[index];
    const width = 75;
    return `<g class="income-flow-marker" role="img" ${tipAttrs(`${selected.labels[index]}: ${fmtWhole(value)} cumulative`)}><line x1="${x}" y1="28" x2="${x}" y2="190"/><rect x="${x - width / 2}" y="92" width="${width}" height="28" rx="14"/><text x="${x}" y="110">${state.incomeFlow.showMilestones ? fmtWhole(value) : ''}</text><text class="income-flow-step" x="${x}" y="205">${selected.labels[index]}</text></g>`;
  }).join('');
  byId('income-flow-value').textContent = fmtWhole(selected.total);
  setChange(byId('income-flow-change'), change);
  byId('income-flow-context').textContent = `vs ${fmtWhole(selected.previous)} prior period`;
  byId('income-flow-subtitle').textContent = state.incomeFlow.period === 'quarter' ? 'Last 90 days' : 'Last 30 days';
  byId('income-flow-period-label').textContent = state.incomeFlow.period === 'quarter' ? 'Quarter to date · sample' : 'Month to date · sample';
  byId('income-flow-chart').innerHTML = `<defs><radialGradient id="income-halo"><stop stop-color="#8b5cf6" stop-opacity=".18"/><stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/></radialGradient></defs><ellipse cx="220" cy="112" rx="212" ry="106" fill="url(#income-halo)"/>${bands}${labels}`;
  byId('income-flow-chart').setAttribute('aria-label', `Income ${fmtWhole(selected.total)}, up ${change.toFixed(1)} percent compared with ${fmtWhole(selected.previous)}. Checkpoints ${selected.checkpoints.map((value, index) => `${selected.labels[index]} ${fmtWhole(value)}`).join('; ')}.`);
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

// rows = [{ checkpoint_1: '6341.00', checkpoint_2: '20441.00', total: '32134.00', previous: '31348.00' }]
loadWidget('incomeFlow', rows => {
  const r = rows[0];
  const total = Number(r.total) || 0;
  if (!total) return false;
  data.incomeFlow.month = {
    total, previous: Number(r.previous) || 0,
    checkpoints: [Number(r.checkpoint_1) || 0, Number(r.checkpoint_2) || 0, total],
    labels: ['Semana 1', 'Semana 2', 'Total do mês'],
  };
});
```

O menu “Download CSV” chama `downloadCsv('incomeFlow')`, que serializa a **série de amostra** (`incomeFlow-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Receita recebida no mês corrente acumulada até o 7º e o 14º dia e no total, mais o total do mês anterior (subconsulta). Testado no MariaDB local.

```sql
-- Receita acumulada no mês corrente em três marcos (semana 1, semana 2, total) e total do mês anterior
SELECT SUM(CASE WHEN r.payment_date <  DATE_FORMAT(CURDATE(), '%Y-%m-01') + INTERVAL 7 DAY  THEN r.amount_paid ELSE 0 END) AS checkpoint_1,
       SUM(CASE WHEN r.payment_date <  DATE_FORMAT(CURDATE(), '%Y-%m-01') + INTERVAL 14 DAY THEN r.amount_paid ELSE 0 END) AS checkpoint_2,
       SUM(r.amount_paid)                                                                                              AS total,
       (SELECT COALESCE(SUM(p.amount_paid), 0)
          FROM financial_receivables p
         WHERE p.deleted_at IS NULL AND p.status <> 'cancelled'
           AND p.payment_date BETWEEN DATE_FORMAT(CURDATE() - INTERVAL 1 MONTH, '%Y-%m-01')
                                  AND LAST_DAY(CURDATE() - INTERVAL 1 MONTH))                                          AS previous
  FROM financial_receivables r
 WHERE r.deleted_at IS NULL AND r.status <> 'cancelled'
   AND r.payment_date BETWEEN DATE_FORMAT(CURDATE(), '%Y-%m-01') AND LAST_DAY(CURDATE());
```

Os marcos precisam ser crescentes; com `SUM` cumulativo isso é garantido. Se `total` for nulo (mês sem recebimento), o provider devolve vazio.

## Faça / Não faça

- **Faça:** usar valores cumulativos (o desenho assume crescimento);
- **Faça:** mostrar o período anterior no contexto.
- **Não faça:** passar valores por semana não acumulados;
- **Não faça:** usar mais de três marcos (as posições `xs` são fixas).
