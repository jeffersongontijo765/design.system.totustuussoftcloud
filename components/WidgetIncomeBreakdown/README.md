# WidgetIncomeBreakdown

Card “Income breakdown”: percentual da receita já gasto, saldo restante e uma barra segmentada por categoria com legenda de valores e percentuais.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só o card `breakdown`. Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Mostrar como a receita recebida no mês/trimestre foi alocada em despesas por categoria.
- Quando as partes somam um todo conhecido (a receita do período) e o “não alocado” importa.
- Para comparar gasto contra limite use [WidgetCategoryLimit](../WidgetCategoryLimit/README.md); para evolução no tempo, [WidgetIncomeStatistics](../WidgetIncomeStatistics/README.md).

## Anatomia

```
┌ ícone · Income breakdown (i) ───────── [ajustes] [⋯] ┐
│ 37% spent   (↗ 12%)                                 │  #breakdown-percent, #breakdown-change
│ $4,166.00 remaining in this period                  │  #breakdown-left
│ [████████|████|██|░░░░░░░░]                          │  #allocation-bar (.allocation-segment)
│ ● Needs $2,975.85 · 45%   ● Transportation …        │  ul#allocation-legend
│ Allocated income            $6,613.00 total · sample│
└─────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Resumo | `.breakdown-summary` (`#breakdown-percent`, `.metric-change#breakdown-change`) | sim |
| Restante | `p.breakdown-left > #breakdown-left` | sim |
| Barra | `div.allocation-bar#allocation-bar[role="img"]` > `span.allocation-segment[tabindex="0"][data-tip]` + `.unallocated` | sim |
| Legenda | `ul.allocation-legend#allocation-legend` | sim |
| Rodapé | `#breakdown-total` | sim |
| Configurações | `dialog#settings-breakdown` | sim |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('breakdown')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Após “Apply settings” o diálogo grava em `state.breakdown` e re-renderiza só este widget; o toast `#widget-toast` confirma. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Sem percentuais | `state.breakdown.showPercent = false` tira “· 45%” da legenda. |

## API

### Dados esperados

Lista de categorias com a fatia percentual sobre a receita do período; receita e gasto totais hoje são constantes no render (6613 e 2447, × 3 no trimestre).

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `name` | `string` | texto | Categoria. |
| `percent` | `number` | % inteiro | Fatia da receita (`flex-grow` do segmento). |
| `color` | `string` | hex | Cor do segmento e da legenda. |
| receita / gasto | `number` | moeda | Constantes `income`/`spent` em `renderBreakdown()`; com dados reais vêm do provider. |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js
breakdown: [
  { name: 'Needs', percent: 45, color: COLORS.blue },
  { name: 'Transportation', percent: 20, color: COLORS.cyan },
  { name: 'Entertainment', percent: 10, color: COLORS.amber }
]
```

### Configurações do widget

Padrão em `state.breakdown`: `{ period: 'month', showPercent: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `period` | select | `month` (Current month) · `quarter` (Current quarter) | Reporting period | Mês ou trimestre (multiplicador 3 na amostra). |
| `showPercent` | input checkbox | booleano | Show category percentages | Mostra o percentual ao lado do valor. |

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
| `renderBreakdown()` | Percentual gasto, restante, segmentos focáveis com `data-tip`, linha “Unallocated” e `aria-label` da barra. |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- Recebimentos: `GET /api/v1/domain/records/financial/receivable`; despesas: `/financial/payable` — ambos permissão `admin.financial.view` (a mesma das rotas `/financial/*` em `app/Config/page-domain-sources.php`).
- **Recomendado:** provider com a consulta abaixo → `{ "income": 6613.00, "spent": 2447.00, "rows": [{ "name", "color", "percent" }] }`.

## Acessibilidade

- Cada segmento é focável (`tabindex="0"`) e tem `aria-label` com nome e percentual; o tooltip abre no foco.
- O segmento “não alocado” é `aria-hidden` porque a legenda já traz a linha “Unallocated”.
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
$endpoint = '/api/v1/domain/records/financial/payable';
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="breakdown"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="breakdown-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget" data-widget="breakdown" aria-labelledby="breakdown-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-blue" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="breakdown-title">Income breakdown</h2>
          <button class="info-button" type="button" data-tip="Income allocation by budget category for the chosen period." aria-label="About income breakdown">
            i
          </button>
        </div>
        <p>Where the available income goes</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="breakdown" aria-label="Adjust income breakdown">
        <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" aria-label="More income breakdown actions" aria-expanded="false" data-menu="breakdown">
          <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="breakdown">Download CSV</button>
          <button type="button" data-reset="breakdown">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="breakdown-summary">
    <div><strong id="breakdown-percent">37%</strong><span>spent</span></div>
    <span class="metric-change is-positive" id="breakdown-change">
      <svg viewBox="0 0 16 16" aria-hidden="true">…</svg>
      <span data-change-value>12%</span>
    </span>
    <span class="metric-context">last month</span>
  </div>
  <p class="breakdown-left"><strong id="breakdown-left">$2,450.00</strong> remaining in this period</p>
  <div class="allocation-bar" id="allocation-bar" role="img" aria-label="Income allocation by category"></div>
  <ul class="allocation-legend" id="allocation-legend"></ul>
  <footer class="ttsc-analytics-foot widget-foot">
    <span>Allocated income</span>
    <span id="breakdown-total">$6,613.00 total · sample</span>
  </footer>
  <dialog class="widget-settings" id="settings-breakdown" aria-labelledby="settings-breakdown-title">
    <form method="dialog">
      <header>
        <div>
          <span class="settings-icon"><svg viewBox="0 0 20 20" aria-hidden="true">…</svg></span>
          <div>
            <h3 id="settings-breakdown-title">Income breakdown settings</h3>
            <p>Settings apply to this widget only.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close settings">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Reporting period
          <select data-setting="breakdown" data-key="period">
            <option value="month" selected>Current month</option>
            <option value="quarter">Current quarter</option>
          </select>
        </label>
        <label class="settings-check">
          <input type="checkbox" data-setting="breakdown" data-key="showPercent" checked>
          Show category percentages
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
.breakdown-summary { display: flex; align-items: center; gap: 7px; min-height: 33px; }
.breakdown-summary > div { display: flex; align-items: baseline; gap: 7px; }
.breakdown-summary > div strong { color: var(--w-text); font-size: 25px; font-weight: 600; letter-spacing: -.03em; line-height: 1; }
.breakdown-summary > div span { color: var(--w-muted); font-size: 11px; }
.breakdown-summary .metric-change { margin-left: auto; }
.breakdown-left { margin: 8px 0 16px; color: var(--w-muted); font-size: 12px; }
.breakdown-left strong { color: var(--w-secondary); font-size: 14px; font-variant-numeric: tabular-nums; font-weight: 600; }
.allocation-bar { display: flex; height: 32px; overflow: hidden; gap: 4px; border-radius: 10px; background: var(--w-grid); }
.allocation-segment { position: relative; min-width: 4px; border-radius: 7px; transition: flex-grow .25s ease, opacity .15s ease; }
.allocation-segment:hover, .allocation-segment:focus-visible { opacity: .8; outline: 2px solid var(--w-text); outline-offset: 2px; }
.allocation-legend { display: grid; gap: 10px; margin: 17px 0 0; padding: 0; list-style: none; }
.allocation-legend li { display: grid; grid-template-columns: 9px minmax(0,1fr) auto; align-items: center; gap: 8px; color: var(--w-secondary); font-size: 11px; }
.allocation-legend i { width: 9px; height: 9px; border-radius: 3px; background: var(--series-color); }
.allocation-legend strong { color: var(--w-text); font-size: 11px; font-variant-numeric: tabular-nums; font-weight: 600; }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Barra mais alta em painéis largos e foco visível com o anel do produto */
[data-widget="breakdown"] .allocation-bar { height: 14px; }
[data-widget="breakdown"] .allocation-segment:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
```

### JS

Render real em `widgets.js`:

```js
function renderBreakdown() {
  const multiplier = state.breakdown.period === 'quarter' ? 3 : 1;
  const income = 6613 * multiplier;
  const spent = 2447 * multiplier;
  const remaining = income - spent;
  const percent = spent / income * 100;
  const breakdown = data.breakdown;
  byId('breakdown-percent').textContent = `${percent.toFixed(0)}%`;
  byId('breakdown-left').textContent = fmtMoney(remaining);
  byId('breakdown-total').textContent = `${fmtMoney(income)} allocated · sample`;
  setChange(byId('breakdown-change'), 12);
  byId('allocation-bar').setAttribute('aria-label', `Category share: ${breakdown.map(item => `${item.name} ${item.percent}%`).join(', ')}; remaining ${100 - sum(breakdown.map(item => item.percent))} percent.`);
  byId('allocation-bar').innerHTML = breakdown.map(item => `<span class="allocation-segment" tabindex="0" style="--series-color:${item.color};background:${item.color};flex-grow:${item.percent}" aria-label="${item.name}, ${item.percent} percent of allocated income" data-tip="${item.name}: ${item.percent}% · ${fmtMoney(income * item.percent / 100)}"></span>`).join('') + `<span class="allocation-segment unallocated" style="flex-grow:${100 - sum(breakdown.map(item => item.percent))}" aria-hidden="true"></span>`;
  const rows = breakdown.map(item => `<li style="--series-color:${item.color}"><i aria-hidden="true"></i><span>${item.name}</span><strong>${fmtMoney(income * item.percent / 100)}${state.breakdown.showPercent ? ` · ${item.percent}%` : ''}</strong></li>`);
  rows.push(`<li style="--series-color:#cbd5e1"><i aria-hidden="true"></i><span>Unallocated</span><strong>${fmtMoney(income * .25)}${state.breakdown.showPercent ? ' · 25%' : ''}</strong></li>`);
  byId('allocation-legend').innerHTML = rows.join('');
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

// payload = { income: '6613.00', rows: [{ name: 'Folha', color: '#2684e8', spent: '2975.85', percent: '45.0' }, …] }
loadWidget('breakdown', (rows, payload) => {
  data.breakdown = rows.map(row => ({ name: row.name, percent: Math.round(Number(row.percent) || 0), color: row.color || '#cbd5e1' }));
  data.breakdownIncome = Number(payload.income ?? rows[0]?.income) || 0;
  // Na cópia de produção, troque `const income = 6613 * multiplier` por `data.breakdownIncome`,
  // `spent` pela soma de row.spent e a linha fixa “Unallocated … 25%” por 100 − soma dos percentuais.
});
```

O menu “Download CSV” chama `downloadCsv('breakdown')`, que serializa a **série de amostra** (`breakdown-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Receita recebida no período (`financial_receivables.amount_paid` por `payment_date`) e o quanto dela foi para cada categoria de despesa paga (`financial_payables` + `financial_categories`). Testado no MariaDB local com `:from`/`:to` literais.

```sql
-- Receita recebida no período e parcela gasta por categoria (barra segmentada)
WITH income AS (
  SELECT COALESCE(SUM(r.amount_paid), 0) AS total
    FROM financial_receivables r
   WHERE r.deleted_at IS NULL AND r.status <> 'cancelled'
     AND r.payment_date BETWEEN :from AND :to          -- mês: '2026-10-01'..'2026-10-31'; trimestre: 3 meses
)
SELECT c.name, c.color,
       SUM(p.amount_paid)                                     AS spent,
       ROUND(SUM(p.amount_paid) / NULLIF(i.total, 0) * 100, 1) AS percent,
       i.total                                                AS income
  FROM financial_payables p
  JOIN financial_categories c ON c.id = p.category_id AND c.deleted_at IS NULL
  CROSS JOIN income i
 WHERE p.deleted_at IS NULL AND p.status <> 'cancelled'
   AND p.payment_date BETWEEN :from AND :to
 GROUP BY c.id, c.name, c.color, i.total
 ORDER BY spent DESC
 LIMIT 3;
```

O trimestre é só `:from` = primeiro dia de três meses atrás. O provider devolve `income` separado para o card mostrar o restante (`income − Σ spent`).

## Faça / Não faça

- **Faça:** garantir que a soma dos segmentos ≤ 100% e que o restante seja calculado, não fixo;
- **Faça:** manter a legenda com valor e percentual.
- **Não faça:** usar a barra para mais de 4–5 categorias (agrupe em “Outras”);
- **Não faça:** deixar as constantes 6613/2447 do modelo em produção.
