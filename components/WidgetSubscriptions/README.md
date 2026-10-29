# WidgetSubscriptions

Card “Subscriptions”: custo/receita recorrente total e a participação de três provedores (ou planos) em anéis concêntricos SVG com legenda de valores.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só o card `subscriptions`. Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Mostrar a receita recorrente mensal (MRR) por plano de cobrança (`billing_subscriptions`), por mês, trimestre ou ano.
- Até três séries: cada anel é uma proporção do total; mais itens viram anéis finos ilegíveis.
- Para composição com “sobra” (gasto × disponível) use [WidgetIncomeBreakdown](../WidgetIncomeBreakdown/README.md); para muitos planos, uma tabela ([RecordsTable](../RecordsTable/README.md)).

## Anatomia

```
┌ ícone · Subscriptions (i) ──────────── [ajustes] [⋯] ┐
│ $156.98  per month                                  │
│   ◯◯◯  +17%          ● Figma      $96.07            │  svg#subscriptions-chart + #ring-center
│  (anéis) vs last     ● Netflix    $23.01            │  ul#subscriptions-legend
│          month       ● ChatGPT    $37.90            │
│ Recurring cost by provider          USD · sample    │
└─────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Card | `article.ttsc-analytics-card.widget.demo-widget[data-widget="subscriptions"]` | sim |
| Valor | `.metric-row` > `strong.widget-value#subscriptions-value` + `#subscriptions-period-label` | sim |
| Anéis | `.subscription-layout` > `.ring-chart-wrap` > `.ttsc-analytics-plot.ring-plot` > `svg#subscriptions-chart.ring-svg` (`.ring-track` + `.ring-progress`) | sim |
| Centro | `#ring-center` (comparação ou nº de serviços) | sim |
| Legenda | `ul#subscriptions-legend` (`li[style="--series-color"]`) | sim |
| Configurações | `dialog.widget-settings#settings-subscriptions` | sim |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('subscriptions')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Após “Apply settings” o diálogo grava em `state.subscriptions` e re-renderiza só este widget; o toast `#widget-toast` confirma. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Sem comparação | `state.subscriptions.comparison = false`: o centro mostra “N active services” em vez de “+17% vs last month”. |

## API

### Dados esperados

Lista de até três itens com valor mensal; o período multiplica por 1, 3 ou 12 (`subscriptionValues()`).

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `name` | `string` | texto | Plano ou provedor (legenda e `aria-label`). |
| `monthly` | `number` | moeda/mês | Valor recorrente mensal. |
| `color` | `string` | hex | Cor do anel e do marcador da legenda (`--series-color`). |
| comparação | `number` | % | Hoje o “+17%” é fixo no markup do render; com dados reais, calcule a partir de `current_mrr`/`previous_mrr`. |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js
subscriptions: [
  { name: 'Figma', monthly: 96.07, color: COLORS.blue },
  { name: 'Netflix', monthly: 23.01, color: '#8ec5fb' },
  { name: 'ChatGPT', monthly: 37.9, color: COLORS.amber }
]
```

### Configurações do widget

Padrão em `state.subscriptions`: `{ period: 'month', comparison: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `period` | select | `month` (Monthly) · `quarter` (Quarterly) · `year` (Annual) | Billing view | Multiplicador 1/3/12 e o rótulo “per month/quarter/year”. |
| `comparison` | input checkbox | booleano | Show month-over-month change | Troca o conteúdo de `#ring-center`. |

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
| `renderSubscriptions()` | Total, rótulo, centro, legenda, anéis e `aria-label` do SVG. |
| `subscriptionValues()` | Aplica o multiplicador do período. |
| `subscriptionRingMarkup(values, total)` | Gera um `circle.ring-track` + `circle.ring-progress` por item (raio 91 − 13·i, `stroke-dasharray` proporcional). |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- **Lista pronta:** `GET /api/v1/domain/records/billing/subscriptions?status=active&per_page=100` (view `inst_billing_subscriptions`: `plan_name`, `negotiated_amount`, `discount_percent`, `status`…), permissão `admin.financial.view` (a mesma das rotas `/financial/*` em `app/Config/page-domain-sources.php`). Serve para poucos registros; o agregado deve vir do SQL.
- **Agregado pronto por plano:** a view `inst_billing_plans` (no banco do tenant) já soma `active_subscriptions` e `monthly_amount` por `plan_id`.
- **Recomendado:** provider do módulo de cobrança com as duas consultas abaixo → `{ "rows": [{ "plan_name", "monthly_amount" }], "current_mrr", "previous_mrr" }`.

## Acessibilidade

- O SVG tem `role="img"` e `aria-label` com o total e o valor de cada item; a legenda repete os valores em texto, então a cor não carrega informação sozinha.
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
$endpoint = '/api/v1/domain/records/billing/subscriptions?status=active&per_page=100';
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="subscriptions"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="subscriptions-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget" data-widget="subscriptions" aria-labelledby="subscriptions-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-blue" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="subscriptions-title">Subscriptions</h2>
          <button class="info-button" type="button" data-tip="Recurring subscription charges grouped by connected service." aria-label="About subscriptions">
            i
          </button>
        </div>
        <p>Connected services and monthly cost</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="subscriptions" aria-label="Adjust subscriptions chart">
        <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" aria-label="More subscription actions" aria-expanded="false" data-menu="subscriptions">
          <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="subscriptions">Download CSV</button>
          <button type="button" data-reset="subscriptions">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="metric-row">
    <strong class="widget-value" id="subscriptions-value">$156.98</strong>
    <span class="metric-context" id="subscriptions-period-label">per month</span>
  </div>
  <div class="subscription-layout">
    <div class="ring-chart-wrap">
      <div class="ttsc-analytics-plot ring-plot">
        <svg id="subscriptions-chart" class="ring-svg" viewBox="0 0 220 220" role="img" aria-label="Subscription cost distribution by service."></svg>
        <div class="ring-center" id="ring-center"><strong>+17%</strong><span>vs last month</span></div>
      </div>
    </div>
    <ul class="service-legend" id="subscriptions-legend" aria-label="Subscription services"></ul>
  </div>
  <footer class="ttsc-analytics-foot widget-foot">
    <span>Recurring cost by provider</span>
    <span>USD · sample</span>
  </footer>
  <dialog class="widget-settings" id="settings-subscriptions" aria-labelledby="settings-subscriptions-title">
    <form method="dialog">
      <header>
        <div>
          <span class="settings-icon"><svg viewBox="0 0 20 20" aria-hidden="true">…</svg></span>
          <div>
            <h3 id="settings-subscriptions-title">Subscriptions settings</h3>
            <p>Settings apply to this chart only.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close settings">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Billing view
          <select data-setting="subscriptions" data-key="period">
            <option value="month" selected>Monthly</option>
            <option value="quarter">Quarterly</option>
            <option value="year">Annual</option>
          </select>
        </label>
        <label class="settings-check">
          <input type="checkbox" data-setting="subscriptions" data-key="comparison" checked>
          Show month-over-month change
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
.subscription-layout { display: grid; grid-template-columns: minmax(140px, 1fr) minmax(110px, .72fr); align-items: center; gap: 8px; min-height: 214px; }
.ring-chart-wrap { min-width: 0; }
.ring-plot.ttsc-analytics-plot { height: 210px; }
.ring-svg { display: block; width: 100%; height: 100%; overflow: visible; }
.ring-track { fill: none; stroke: var(--w-grid); stroke-width: 1; }
.ring-progress { fill: none; stroke-width: 8; stroke-linecap: round; transform: rotate(-90deg); transform-origin: 110px 110px; transition: stroke-dasharray .3s ease; }
.ring-center { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; pointer-events: none; text-align: center; }
.ring-center strong { color: var(--w-text); font-size: 22px; font-variant-numeric: tabular-nums; font-weight: 650; letter-spacing: -.035em; }
.ring-center span { max-width: 90px; margin-top: 3px; color: var(--w-muted); font-size: 10px; }
.subscription-layout { grid-template-columns: minmax(135px, 1fr) minmax(100px, .75fr); min-height: 200px; }
.ring-plot.ttsc-analytics-plot { height: 194px; }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Anéis com a paleta do produto: a cor de cada item vem do campo `color`; aqui só a trilha e a espessura */
[data-widget="subscriptions"] .ring-track { stroke: var(--ttsc-border-soft); }
[data-widget="subscriptions"] .ring-progress { stroke-width: 7; }
```

### JS

Render real em `widgets.js`:

```js
function subscriptionValues() {
  const multiplier = state.subscriptions.period === 'quarter' ? 3 : state.subscriptions.period === 'year' ? 12 : 1;
  return data.subscriptions.map(item => Number((item.monthly * multiplier).toFixed(2)));
}
```

```js
function subscriptionRingMarkup(values, total) {
  return data.subscriptions.map((item, index) => {
    const radius = 91 - index * 13;
    const length = 2 * Math.PI * radius;
    const ratio = total > 0 ? Math.min(1, values[index] / total) : 0;
    return `<circle class="ring-track" cx="110" cy="110" r="${radius}" stroke-dasharray="2 4"/><circle class="ring-progress" cx="110" cy="110" r="${radius}" stroke="${item.color}" stroke-dasharray="${(length * ratio).toFixed(2)} ${(length * (1 - ratio)).toFixed(2)}"/>`;
  }).join('');
}
```

```js
function renderSubscriptions() {
  const values = subscriptionValues();
  const labels = data.subscriptions.map(item => item.name);
  const total = sum(values);
  const period = state.subscriptions.period;
  byId('subscriptions-value').textContent = fmtMoney(total);
  byId('subscriptions-period-label').textContent = period === 'year' ? 'per year' : period === 'quarter' ? 'per quarter' : 'per month';
  byId('ring-center').hidden = false;
  byId('ring-center').innerHTML = state.subscriptions.comparison ? '<strong>+17%</strong><span>vs last month</span>' : `<strong>${values.length}</strong><span>active services</span>`;
  byId('subscriptions-legend').innerHTML = data.subscriptions.map((item, index) => `<li style="--series-color:${item.color}"><i aria-hidden="true"></i><span>${item.name}</span><strong>${fmtMoney(values[index])}</strong></li>`).join('');
  byId('subscriptions-chart').innerHTML = subscriptionRingMarkup(values, total);
  byId('subscriptions-chart').setAttribute('aria-label', `Monthly subscriptions total ${fmtMoney(total)}. ${data.subscriptions.map((item, index) => `${item.name}: ${fmtMoney(values[index])}`).join('; ')}.`);
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

// rows = [{ plan_name: 'Mensalidade Graduação', monthly_amount: '182340.00' }, …] (até 3)
const PLAN_COLORS = ['#2684e8', '#8ec5fb', '#f5b942'];                // mesmas cores da amostra (COLORS)
loadWidget('subscriptions', (rows, payload) => {
  data.subscriptions = rows.slice(0, 3).map((row, index) => ({
    name: row.plan_name ?? `Plano ${row.plan_id}`,
    monthly: Number(row.monthly_amount) || 0,
    color: PLAN_COLORS[index],
  }));
  data.subscriptionsChange = payload.previous_mrr ? (payload.current_mrr - payload.previous_mrr) / payload.previous_mrr * 100 : null;
  // Na cópia de produção, use data.subscriptionsChange no lugar do texto fixo '+17%' de renderSubscriptions().
});
```

O menu “Download CSV” chama `downloadCsv('subscriptions')`, que serializa a **série de amostra** (`subscriptions-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Assinaturas ativas agrupadas por plano, com o desconto negociado aplicado, e a receita recorrente do mês anterior para a comparação do centro. No banco do tenant não há tabela `billing_plans` (só a view `inst_billing_plans`, que agrupa por `plan_id`), por isso o nome do plano vem dela quando existir. Testado no MariaDB local.

```sql
-- Três planos com maior receita recorrente mensal (assinaturas ativas)
SELECT s.plan_id,
       COUNT(*)                                                          AS active_subscriptions,
       ROUND(SUM(s.negotiated_amount * (1 - COALESCE(s.discount_percent, 0) / 100)), 2) AS monthly_amount
  FROM billing_subscriptions s
 WHERE s.deleted_at IS NULL
   AND s.status = 'active'
 GROUP BY s.plan_id
 ORDER BY monthly_amount DESC
 LIMIT 3;

-- Comparação com o mês anterior (centro do anel: "+17% vs mês anterior")
SELECT ROUND(SUM(CASE WHEN s.status = 'active' THEN s.negotiated_amount ELSE 0 END), 2) AS current_mrr,
       ROUND(SUM(CASE WHEN s.starts_at <= LAST_DAY(CURDATE() - INTERVAL 1 MONTH)
                       AND (s.cancelled_at IS NULL OR s.cancelled_at > LAST_DAY(CURDATE() - INTERVAL 1 MONTH))
                      THEN s.negotiated_amount ELSE 0 END), 2)          AS previous_mrr
  FROM billing_subscriptions s
 WHERE s.deleted_at IS NULL;
```

`negotiated_amount` é o valor por parcela mensal; se o plano tiver periodicidade diferente, normalize antes de somar. O provider devolve no máximo 3 linhas (o card não foi desenhado para mais).

## Faça / Não faça

- **Faça:** limitar a 3 séries e manter a legenda com valor em texto;
- **Faça:** calcular a comparação no servidor, com o mesmo período do card.
- **Não faça:** deixar o “+17%” fixo do modelo em produção;
- **Não faça:** usar anéis para valores que não somam um total.
