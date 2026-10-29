# WidgetPurchases

Card “Total purchases”: total de compras da semana, barras por dia (seg–dom) em SVG com balão de valor no dia destacado e troca de moeda USD/BRL.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só o card `purchases`. Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Mostrar o volume diário de pedidos de compra (`purchase_orders.total_amount`) dos últimos 7 dias.
- Quando a moeda de exibição pode mudar (configuração `currency`).
- Para séries mensais longas use [WidgetMonthlyConversions](../WidgetMonthlyConversions/README.md) ou [WidgetBalance](../WidgetBalance/README.md).

## Anatomia

```
┌ ícone · Total purchases (i) ────────── [ajustes] [⋯] ┐
│ $5,217  (↗ …)  vs last week                          │  #purchases-value, #purchases-change
│               ┌$820┐                                 │  balão (dia 4 = sexta)
│   █   █   █   █   █   █   █                          │  svg#purchases-chart rect.purchase-bar
│   M   T   W   T   F   S   S                          │
│ Recorded purchases                  Mon–Sun · sample │
└──────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Resumo | `.purchase-summary` > `strong.widget-value#purchases-value` + `.metric-change#purchases-change` | sim |
| Gráfico | `.ttsc-analytics-plot.activity-bar-plot.purchase-plot` > `svg#purchases-chart.purchase-chart` (`line.purchase-gridline`, `rect.purchase-bar`, `text.purchase-day`) | sim |
| Balão | `<g aria-hidden="true">` com `rect` + seta + texto (fundo `#111318`) | sim |
| Rodapé | `#purchases-period-label` | sim |
| Configurações | `dialog#settings-purchases` (moeda, comparação) | sim |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('purchases')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Após “Apply settings” o diálogo grava em `state.purchases` e re-renderiza só este widget; o toast `#widget-toast` confirma. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| BRL | `state.purchases.currency = "BRL"`: `fmtPurchase()` usa `pt-BR` e multiplica pelo fator fixo **5.2** da amostra — em produção use a cotação persistida (`invoice_documents.exchange_rate` ou a fonte de câmbio do módulo). |
| Destaque fixo | O índice 4 (sexta) é sempre o destacado na referência; com dados reais, destaque o dia atual ou o maior. |

## API

### Dados esperados

Sete valores, de segunda a domingo, na moeda base (USD na amostra).

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `data.purchases[]` | `number[7]` | moeda base, 0 casas | Total comprado em cada dia. |
| rótulos | fixos | `M T W T F S S` | Constante no render. |
| moeda | `USD` \| `BRL` | ISO 4217 | Configuração do widget. |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js
purchases: [500, 980, 1330, 620, 820, 510, 457]
```

### Configurações do widget

Padrão em `state.purchases`: `{ currency: 'USD', showComparison: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `currency` | select | `USD` (US dollar (USD)) · `BRL` (Brazilian real (BRL)) | Currency display | Moeda de exibição. |
| `showComparison` | input checkbox | booleano | Show comparison | Mostra a pílula de variação. |

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
| `renderPurchases()` | Total, barras (raio 12), balão do dia destacado e `aria-label`. |
| `fmtPurchase(value)` | Formata na moeda configurada (fator de conversão de amostra 5.2). |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- **Recomendado:** provider do módulo de compras com a consulta abaixo e a permissão da página de pedidos; resposta `{ "currency": "BRL", "rows": [{ "weekday_index": 0, "total_amount": "500.00" }] }`.
- A conversão de moeda deve acontecer no servidor com a cotação gravada, não no JS.

## Acessibilidade

- O balão é `aria-hidden`; o valor de cada dia está no `<title>` da barra e no `aria-label` do SVG.
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
$endpoint = '/purchasing/orders/widgets/weekly-purchases' /* rota do provider do módulo, a criar */;
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="purchases"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="purchases-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget activity-widget" data-widget="purchases" aria-labelledby="purchases-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-purple" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="purchases-title">Total purchases</h2>
          <button class="info-button" type="button" data-tip="Purchase amounts recorded for each day of the selected week." aria-label="About total purchases">
            i
          </button>
        </div>
        <p>Last 7 days</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="purchases" aria-label="Adjust total purchases chart">
        <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" aria-label="More purchase actions" aria-expanded="false" data-menu="purchases">
          <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="purchases">Download CSV</button>
          <button type="button" data-reset="purchases">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="purchase-summary">
    <strong class="widget-value" id="purchases-value">$5,217.00</strong>
    <span class="metric-change is-positive" id="purchases-change">
      <svg viewBox="0 0 16 16" aria-hidden="true">…</svg>
      <span data-change-value>15.1%</span>
    </span>
    <span class="metric-context">vs prior 7 days</span>
  </div>
  <div class="ttsc-analytics-plot activity-bar-plot purchase-plot">
    <svg id="purchases-chart" class="purchase-chart" viewBox="0 0 440 190" role="img" aria-label="Purchases total $5,217 for the last seven days. Monday $500; Tuesday $980; Wednesday $1,330; Thursday $620; Friday $820; Saturday $510; Sunday $457.">
      <line class="purchase-gridline" x1="8" y1="64" x2="432" y2="64"/>
      <line class="purchase-gridline" x1="8" y1="108" x2="432" y2="108"/>
      <line class="purchase-gridline" x1="8" y1="154" x2="432" y2="154"/>
      <!-- … +8 elemento(s) iguais gerados pelo JS -->
    </svg>
  </div>
  <footer class="ttsc-analytics-foot widget-foot">
    <span>Recorded purchases</span>
    <span id="purchases-period-label">Mon–Sun · sample</span>
  </footer>
  <dialog class="widget-settings" id="settings-purchases" aria-labelledby="settings-purchases-title">
    <form method="dialog">
      <header>
        <div>
          <span class="settings-icon"><svg viewBox="0 0 20 20" aria-hidden="true">…</svg></span>
          <div>
            <h3 id="settings-purchases-title">Purchase chart settings</h3>
            <p>Settings apply to this widget only.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close settings">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Currency display
          <select data-setting="purchases" data-key="currency">
            <option value="USD" selected>US dollar (USD)</option>
            <option value="BRL">Brazilian real (BRL)</option>
          </select>
        </label>
        <label class="settings-check">
          <input type="checkbox" data-setting="purchases" data-key="showComparison" checked>
          Show comparison
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
.purchase-summary { display: flex; min-height: 43px; align-items: center; gap: 9px; flex-wrap: wrap; }
.purchase-summary .widget-value { font-size: 29px; }
.purchase-plot.ttsc-analytics-plot { height: 224px; margin-top: 4px; }
.purchase-chart { display: block; width: 100%; height: 100%; overflow: visible; }
.purchase-gridline { stroke: var(--w-grid); stroke-width: 1; }
.purchase-bar { fill: #ded6ff; }
.purchase-bar.is-highlight { fill: #7653f9; }
.purchase-day { fill: var(--w-muted); font: 11px var(--ttsc-font-sans, Inter, sans-serif); text-anchor: middle; }
.purchase-day.is-highlight { fill: #7653f9; font-weight: 700; }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Barra destacada com o token de destaque */
[data-widget="purchases"] .purchase-bar.is-highlight { fill: var(--ttsc-accent); }
[data-widget="purchases"] .purchase-day.is-highlight { fill: var(--ttsc-text); font-weight: 600; }
```

### JS

Render real em `widgets.js`:

```js
function renderPurchases() {
  const values = data.purchases;
  const labels = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
  const total = sum(values);
  byId('purchases-value').textContent = fmtPurchase(total);
  byId('purchases-change').hidden = !state.purchases.showComparison;
  byId('purchases-period-label').textContent = 'Mon–Sun · sample';
  const max = Math.max(...values, 1);
  const baseline = 154;
  const chartTop = 20;
  const barWidth = 31;
  const slot = 58;
  const bars = values.map((value, index) => {
    const height = Math.max(value ? 7 : 3, (value / max) * (baseline - chartTop));
    const x = 18 + index * slot;
    const y = baseline - height;
    return `<g><title>${labels[index]}: ${fmtPurchase(value)}</title><rect class="purchase-bar${index === 4 ? ' is-highlight' : ''}" x="${x}" y="${y.toFixed(1)}" width="${barWidth}" height="${height.toFixed(1)}" rx="12"/><text class="purchase-day${index === 4 ? ' is-highlight' : ''}" x="${x + barWidth / 2}" y="178">${labels[index]}</text></g>`;
  }).join('');
  const selectedX = 18 + 4 * slot + barWidth / 2;
  const selectedY = baseline - (values[4] / max) * (baseline - chartTop);
  const bubbleX = selectedX - 39;
  const bubbleY = Math.max(1, selectedY - 42);
  const callout = `<g aria-hidden="true"><rect x="${bubbleX}" y="${bubbleY}" width="78" height="27" rx="6" fill="#111318"/><path d="M ${selectedX - 5} ${bubbleY + 26} L ${selectedX + 5} ${bubbleY + 26} L ${selectedX} ${bubbleY + 32} Z" fill="#111318"/><text x="${selectedX}" y="${bubbleY + 17}" fill="#fff" font-family="Inter, sans-serif" font-size="11" text-anchor="middle">${fmtPurchase(values[4])}</text></g>`;
  byId('purchases-chart').innerHTML = `<line class="purchase-gridline" x1="8" y1="64" x2="432" y2="64"/><line class="purchase-gridline" x1="8" y1="108" x2="432" y2="108"/><line class="purchase-gridline" x1="8" y1="${baseline}" x2="432" y2="${baseline}"/>${bars}${callout}`;
  byId('purchases-chart').setAttribute('aria-label', `Purchases total ${fmtPurchase(total)} for the last seven days. ${values.map((value, index) => `${labels[index]} ${fmtPurchase(value)}`).join('; ')}.`);
}
```

Formatador real (o fator `5.2` é de amostra):

```js
const fmtPurchase = value => new Intl.NumberFormat(state.purchases.currency === 'BRL' ? 'pt-BR' : 'en-US', { style: 'currency', currency: state.purchases.currency, minimumFractionDigits: 0, maximumFractionDigits: 0 }).format((Number(value) || 0) * (state.purchases.currency === 'BRL' ? 5.2 : 1));
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

// payload = { currency: 'BRL', rows: [{ weekday_index: 0, total_amount: '500.00' }, …] } — moeda já convertida no servidor
loadWidget('purchases', (rows, payload) => {
  const week = Array(7).fill(0);
  rows.forEach(row => { week[Number(row.weekday_index)] += Number(row.total_amount) || 0; });
  data.purchases = week;
  state.purchases.currency = payload.currency || 'BRL';
  // Na cópia de produção remova o fator `* (state.purchases.currency === 'BRL' ? 5.2 : 1)` de fmtPurchase.
});
```

O menu “Download CSV” chama `downloadCsv('purchases')`, que serializa a **série de amostra** (`purchases-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Pedidos de compra emitidos nos últimos 7 dias, somados por dia da semana (`WEEKDAY`: 0 = segunda) e moeda, ignorando rascunhos e cancelados. Testado no MariaDB local.

```sql
-- Pedidos de compra emitidos nos últimos 7 dias, por dia da semana (seg..dom)
SELECT WEEKDAY(po.issue_date)  AS weekday_index,      -- 0 = segunda … 6 = domingo
       po.currency,
       SUM(po.total_amount)    AS total_amount,
       COUNT(*)                AS orders
  FROM purchase_orders po
 WHERE po.deleted_at IS NULL
   AND po.status NOT IN ('draft', 'cancelled')
   AND po.issue_date BETWEEN CURDATE() - INTERVAL 6 DAY AND CURDATE()
 GROUP BY WEEKDAY(po.issue_date), po.currency
 ORDER BY weekday_index;
```

Se houver mais de uma moeda, converta no SQL/PHP com a cotação do dia antes de somar. Dias sem pedido devem chegar como 0 (o provider completa o vetor de 7).

## Faça / Não faça

- **Faça:** converter moeda no servidor com cotação persistida;
- **Faça:** destacar um dia com significado (hoje ou o maior).
- **Não faça:** deixar o fator 5.2 da amostra;
- **Não faça:** somar moedas diferentes.
