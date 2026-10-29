# WidgetCategoryLimit

Card “Category limit”: medidor semicircular do quanto do limite do período já foi consumido, com estado (dentro/perto/acima do limite) e barras de progresso por categoria.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só o card `category`. Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Acompanhar despesa do mês contra orçamento (`financial_payables` × `financial_budgets`) por categoria ou centro de custo.
- Quando existe um limite explícito e um limiar de alerta (`financial_cost_centers.alert_threshold`).
- Sem limite definido, não use medidor — use [WidgetIncomeBreakdown](../WidgetIncomeBreakdown/README.md) ou barras ([WidgetTimeByCategory](../WidgetTimeByCategory/README.md)).

## Anatomia

```
┌ ícone · Category limit (i) ─────────── [ajustes] [⋯] ┐
│        ╭──────────╮        [Within limit]           │  #category-state
│       ╱  $19,500   ╲       of $25,000 limit         │  svg#category-chart.gauge-svg
│ Needs           $8,775  ███████░░░                  │  #limit-categories (até 3)
│ Transportation  $3,900  ███░░░░░░░                  │
│ Current period utilization              78% used    │
└─────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Card | `article…[data-widget="category"]` | sim |
| Medidor | `.gauge-wrap` > `.gauge-plot` > `svg#category-chart.gauge-svg` (`path.gauge-track` + `path.gauge-progress`) | sim |
| Valor e limite | `#category-value` + irmão “of $… limit” | sim |
| Estado | `span.safe-pill#category-state` com `.is-warning` / `.is-danger` | sim |
| Categorias | `#limit-categories` > `.limit-row-head` + `.limit-track > span` (`.is-over` ≥ 80%) | sim |
| Rodapé | `#category-ratio` | sim |
| Configurações | `dialog#settings-category` (categoria, limite, limiar) | sim |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('category')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Após “Apply settings” o diálogo grava em `state.category` e re-renderiza só este widget; o toast `#widget-toast` confirma. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Perto do limite | `ratio ≥ threshold` e `< 1`: `#category-state.is-warning`, texto “Near limit”. |
| Acima do limite | `ratio ≥ 1`: `.is-danger`, texto “Limit exceeded”, arco âmbar `#f59e0b`. |

## API

### Dados esperados

Lista de categorias com o gasto do período; o limite vem da configuração (todas) ou de um mapa por categoria (`categoryLimit` dentro do render).

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `id` | `string` | slug | Valor do `<select>` de categoria. |
| `name` | `string` | texto | Rótulo da barra. |
| `value` | `number` | moeda, 0 casas | Gasto acumulado no período. |
| `color` | `string` | hex | Cor da barra. |
| limite por categoria | `number` | moeda | Hoje fixo em `categoryLimit = { needs: 12000, … }` no render; com dados reais vem de `monthly_limit`. |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js
categories: [
  { id: 'needs', name: 'Needs', value: 8775, color: COLORS.blue },
  { id: 'transport', name: 'Transportation', value: 3900, color: COLORS.cyan },
  { id: 'fun', name: 'Entertainment', value: 1950, color: COLORS.amber },
  { id: 'other', name: 'Other', value: 4875, color: '#cbd5e1' }
]
```

### Configurações do widget

Padrão em `state.category`: `{ category: 'all', limit: 25000, threshold: .8 }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `category` | select | `all` (All categories) · `needs` (Needs) · `transport` (Transportation) · `fun` (Entertainment) | Category | `all` soma tudo contra `limit`; uma categoria usa o limite dela. |
| `limit` | input number | min 100, step 100 | Monthly limit (USD) | Limite total (quando `category = all`). |
| `threshold` | select | `0.7` (70%) · `0.8` (80%) · `0.9` (90%) | Alert when used | Fração 0–1 que dispara “Near limit”. |

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
| `renderCategory()` | Calcula uso, estado, rótulos, até 3 barras e o arco (`stroke-dasharray` sobre π·112). |
| `selectedCategories()` | Filtra `data.categories` pela configuração. |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- Orçamentos: `GET /api/v1/domain/records/financial/budget` (view `inst_fin_budgets`), permissão `admin.financial.view` (a mesma das rotas `/financial/*` em `app/Config/page-domain-sources.php`).
- Despesas: `GET /api/v1/domain/records/financial/payable` (view `inst_fin_payables`).
- **Recomendado:** provider que roda a consulta abaixo e devolve `{ "rows": [{ "uuid", "name", "color", "spent", "monthly_limit" }], "threshold": 0.8 }`.

## Acessibilidade

- O `aria-label` do medidor diz gasto, limite e percentual; o estado também é texto (“Near limit”), não só cor.
- Barras `.limit-track` são decorativas; o valor está em texto na `.limit-row-head`.
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
$endpoint = '/api/v1/domain/records/financial/budget';
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="category"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="category-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget" data-widget="category" aria-labelledby="category-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-blue" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="category-title">Category limit</h2>
          <button class="info-button" type="button" data-tip="Category spending compared with the configured safe limit." aria-label="About category limits">
            i
          </button>
        </div>
        <p>Spending against your selected limit</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="category" aria-label="Adjust category limit">
        <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" aria-label="More category actions" aria-expanded="false" data-menu="category">
          <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="category">Download CSV</button>
          <button type="button" data-reset="category">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="gauge-wrap">
    <div class="gauge-plot">
      <svg id="category-chart" class="gauge-svg" viewBox="0 0 300 162" role="img" aria-label="Category spending compared with limit."></svg>
      <div class="gauge-center">
        <span class="safe-pill" id="category-state">Within limit</span>
        <strong id="category-value">$19,500</strong>
        <small>of $25,000 limit</small>
      </div>
    </div>
  </div>
  <div class="limit-categories" id="limit-categories"></div>
  <footer class="ttsc-analytics-foot widget-foot">
    <span>Current period utilization</span>
    <span id="category-ratio">78% used</span>
  </footer>
  <dialog class="widget-settings" id="settings-category" aria-labelledby="settings-category-title">
    <form method="dialog">
      <header>
        <div>
          <span class="settings-icon"><svg viewBox="0 0 20 20" aria-hidden="true">…</svg></span>
          <div>
            <h3 id="settings-category-title">Category limit settings</h3>
            <p>Change the limit and alert threshold for this widget.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close settings">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Category
          <select data-setting="category" data-key="category">
            <option value="all">All categories</option>
            <option value="needs">Needs</option>
            <!-- … +2 elemento(s) iguais gerados pelo JS -->
          </select>
        </label>
        <label class="settings-field">
          Monthly limit (USD)
          <input type="number" min="100" step="100" value="25000" data-setting="category" data-key="limit">
        </label>
        <label class="settings-field">
          Alert when used
          <select data-setting="category" data-key="threshold">
            <option value="0.7">70%</option>
            <option value="0.8" selected>80%</option>
            <option value="0.9">90%</option>
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
.gauge-wrap { display: grid; min-height: 184px; place-items: center; padding-top: 2px; }
.gauge-plot { position: relative; width: min(100%, 300px); height: 162px; }
.gauge-svg { display: block; width: 100%; height: 100%; overflow: visible; }
.gauge-track, .gauge-progress { fill: none; stroke-width: 18; stroke-linecap: round; }
.gauge-track { stroke: var(--w-grid); }
.gauge-progress { transition: stroke-dasharray .3s ease; }
.gauge-center { position: absolute; right: 0; bottom: 7px; left: 0; display: flex; align-items: center; flex-direction: column; pointer-events: none; }
.safe-pill { margin-bottom: 7px; padding: 4px 10px; border-radius: 999px; background: var(--w-green-soft); color: #047857; font-size: 10px; }
.safe-pill.is-warning { background: #fffbeb; color: #b45309; }
.safe-pill.is-danger { background: #fef2f2; color: #b91c1c; }
.gauge-center strong { color: var(--w-text); font-size: 24px; font-variant-numeric: tabular-nums; font-weight: 600; letter-spacing: -.04em; }
.gauge-center small { margin-top: 2px; color: var(--w-muted); font-size: 10px; }
.limit-categories { display: grid; gap: 11px; margin-top: 4px; }
.limit-row-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; color: var(--w-muted); font-size: 10px; }
.limit-row-head strong { color: var(--w-secondary); font-size: 11px; font-variant-numeric: tabular-nums; font-weight: 500; white-space: nowrap; }
.limit-track { height: 6px; overflow: hidden; margin-top: 5px; border-radius: 999px; background: var(--w-grid); }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Limiares com os tokens semânticos do produto */
[data-widget="category"] .safe-pill.is-warning { color: var(--ttsc-warning-text); }
[data-widget="category"] .safe-pill.is-danger  { color: var(--ttsc-danger-text); }
.limit-track > span.is-over { box-shadow: inset 0 0 0 1px var(--ttsc-warning); }
```

### JS

Render real em `widgets.js`:

```js
function selectedCategories() {
  return state.category.category === 'all' ? data.categories : data.categories.filter(item => item.id === state.category.category);
}
```

```js
function renderCategory() {
  const rows = selectedCategories();
  const used = sum(rows.map(item => item.value));
  const categoryLimit = { needs: 12000, transport: 5000, fun: 2500, other: 5000 };
  const limit = state.category.category === 'all' ? (Number(state.category.limit) || 1) : categoryLimit[state.category.category];
  const ratio = used / limit;
  const remainder = Math.max(0, limit - used);
  const status = byId('category-state');
  status.classList.toggle('is-warning', ratio >= state.category.threshold && ratio < 1);
  status.classList.toggle('is-danger', ratio >= 1);
  status.textContent = ratio >= 1 ? 'Limit exceeded' : ratio >= state.category.threshold ? 'Near limit' : 'Within limit';
  byId('category-value').textContent = fmtMoney(used, 0);
  byId('category-value').nextElementSibling.textContent = `of ${fmtMoney(limit, 0)} limit`;
  byId('category-ratio').textContent = `${(ratio * 100).toFixed(0)}% used`;
  byId('limit-categories').innerHTML = rows.slice(0, 3).map(item => {
    const itemRatio = Math.min(100, item.value / limit * 100);
    return `<div><div class="limit-row-head"><span>${item.name}</span><strong>${fmtMoney(item.value, 0)}</strong></div><div class="limit-track"><span class="${itemRatio >= 80 ? 'is-over' : ''}" style="width:${itemRatio}%;background:${item.color}"></span></div></div>`;
  }).join('');
  const gaugeLength = Math.PI * 112;
  const gaugeRatio = Math.min(1, Math.max(0, ratio));
  const gaugeColor = ratio >= 1 ? '#f59e0b' : COLORS.blue;
  byId('category-chart').innerHTML = `<path class="gauge-track" d="M 38 145 A 112 112 0 0 1 262 145"/><path class="gauge-progress" d="M 38 145 A 112 112 0 0 1 262 145" stroke="${gaugeColor}" stroke-dasharray="${(gaugeLength * gaugeRatio).toFixed(2)} ${gaugeLength.toFixed(2)}"/>`;
  byId('category-chart').setAttribute('aria-label', `Category spending ${fmtMoney(used, 0)} of ${fmtMoney(limit, 0)} limit, ${(ratio * 100).toFixed(0)} percent used.`);
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

// rows = [{ uuid, name: 'Material didático', color: '#2684e8', spent: '8775.00', monthly_limit: '12000.00' }, …]
loadWidget('category', (rows, payload) => {
  data.categories = rows.map(row => ({ id: row.uuid, name: row.name, value: Number(row.spent) || 0, color: row.color || '#cbd5e1', limit: Number(row.monthly_limit) || null }));
  if (payload.threshold) state.category.threshold = Number(payload.threshold);
  // Na cópia de produção, troque o mapa fixo `categoryLimit` por:
  // const categoryLimit = Object.fromEntries(data.categories.map(item => [item.id, item.limit]));
  // e gere as <option> do diálogo a partir de data.categories.
});
```

O menu “Download CSV” chama `downloadCsv('category')`, que serializa a **série de amostra** (`category-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Despesa do mês corrente por categoria (`financial_payables` não canceladas, por `due_date`) contra o orçamento do mês em `financial_budgets` (uma coluna por mês: `jan` … `dec_month`). O orçamento é pré-agrupado para não duplicar quando há vários centros de custo. Testado no MariaDB local.

```sql
-- Despesa do mês por categoria contra o orçamento do mês (financial_budgets.jan … dec_month)
SELECT c.uuid, c.name, c.color,
       COALESCE(SUM(p.net_amount), 0) AS spent,
       b.monthly_limit
  FROM financial_categories c
  JOIN financial_payables p
    ON p.category_id = c.id
   AND p.deleted_at IS NULL
   AND p.status <> 'cancelled'
   AND p.due_date BETWEEN DATE_FORMAT(CURDATE(), '%Y-%m-01') AND LAST_DAY(CURDATE())
  LEFT JOIN (
        SELECT category_id,
               SUM(CASE MONTH(CURDATE())
                     WHEN 1 THEN jan WHEN 2 THEN feb WHEN 3 THEN mar WHEN 4 THEN apr
                     WHEN 5 THEN may WHEN 6 THEN jun WHEN 7 THEN jul WHEN 8 THEN aug
                     WHEN 9 THEN sep WHEN 10 THEN oct WHEN 11 THEN nov ELSE dec_month END) AS monthly_limit
          FROM financial_budgets
         WHERE year = YEAR(CURDATE()) AND type = 'expense'
         GROUP BY category_id
       ) b ON b.category_id = c.id
 WHERE c.deleted_at IS NULL
 GROUP BY c.id, c.uuid, c.name, c.color, b.monthly_limit
 ORDER BY spent DESC;

-- Limiar de alerta (state.category.threshold) vem do centro de custo
SELECT cc.name, cc.budget_monthly, cc.alert_threshold / 100 AS threshold
  FROM financial_cost_centers cc
 WHERE cc.deleted_at IS NULL AND cc.is_active = 1 AND cc.uuid = :cost_center_uuid;
```

`alert_threshold` é inteiro (0–100) em `financial_cost_centers`; o provider divide por 100 para casar com `state.category.threshold`. Para o card “todas as categorias”, o limite é a soma de `monthly_limit`.

## Faça / Não faça

- **Faça:** mostrar o estado em texto e cor;
- **Faça:** usar o limiar do centro de custo em vez de um número fixo.
- **Não faça:** aplicar um limite inventado quando não há orçamento cadastrado — mostre o estado vazio;
- **Não faça:** mostrar mais de 3 categorias no card (o render corta em 3).
