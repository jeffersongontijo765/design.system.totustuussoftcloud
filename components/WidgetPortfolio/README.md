# WidgetPortfolio

Card de atividade de portfólio (“Total value”): patrimônio total, saudação ao usuário, mapa hexagonal de atividade diária (nível 0–4) com seleção de dia e lista das últimas transações com menu por linha e diálogo de detalhes.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só o card `portfolioActivity`. Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Resumo pessoal/financeiro: saldo das contas (`financial_bank_accounts`), intensidade de lançamentos por dia e as últimas contas pagas.
- Quando o padrão de atividade (dias mais movimentados) importa tanto quanto o total.
- Para um calendário mensal de eventos use os calendários de [WidgetsLarge](../WidgetsLarge/README.md); para tabela de transações completa, [RecordsTable](../RecordsTable/README.md).

## Anatomia

```
┌ (carteira) Total value                           [↗ ⋯] ┐
│ $120,467.00                                            │  #portfolio-total-value
│ (JD) Welcome back …                                    │
│   ⬡⬡⬢⬢⬡                                               │  #portfolio-activity-map > button.portfolio-hex.level-0..4
│  ⬡⬢⬢⬢⬢⬡   16 Aug 2024 · 12 activities                 │  #portfolio-activity-selected
│ Autopay   06 Jun 2024  ● House and bills   -$120.00 ⋮ │  #portfolio-transaction-list
└────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Cabeçalho | `header.portfolio-total-head` (`.portfolio-title`, menu `.portfolio-open-button[data-menu]`) | sim |
| Total | `#portfolio-total-value` | sim |
| Saudação | `.portfolio-welcome-row` (`.portfolio-avatar` com iniciais) | não |
| Mapa | `.portfolio-heatmap-wrap > .portfolio-heatmap#portfolio-activity-map[role="group"]` > `button.portfolio-hex.level-N[data-portfolio-day][aria-pressed]` (`--hex-column`, `--hex-row`) | sim |
| Transações | `section.portfolio-transactions` > `ul#portfolio-transaction-list > li.portfolio-transaction-row` (menu `[data-menu="transaction-<id>"]`) | sim |
| Detalhes | `dialog.widget-settings.portfolio-transaction-dialog#portfolio-transaction-details` | sim |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('portfolioActivity')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Sem diálogo de configurações: os controles do próprio card gravam em `state.portfolioActivity` e re-renderizam só este widget; “Reset widget” volta aos padrões. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Dia selecionado | Hexágono `.is-selected` + `aria-pressed="true"`; texto “dd Mmm aaaa · N activities”. |
| Nenhum dia | “Select a hexagon to inspect daily activity”. |

## API

### Dados esperados

Total do patrimônio, lista de dias com contagem e nível (0–4) e posição na grade hexagonal, e as últimas transações.

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `totalValue` | `number` | moeda | Patrimônio exibido no topo. |
| `days[] {row, column, count, level, date}` | `array` | contagem; nível 0–4 | Um hexágono por dia; `row`/`column` posicionam na grade (17×13 na amostra). |
| `transactions[] {id, name, date, category, amount, color}` | `array` | moeda (negativo = saída) | Lista recente; `id` liga menu e diálogo. |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js
portfolioActivity: {
  totalValue: 120467,
  days: buildPortfolioActivity(),
  transactions: [
    { id: 'autopay', name: 'Autopay', date: '2024-06-06', category: 'House and bills', amount: -120, color: '#8b5cf6' },
    { id: 'netflix', name: 'Netflix', date: '2024-06-04', category: 'Multimedia', amount: -32, color: '#a3e635' },
    { id: 'internet', name: 'Internet', date: '2024-06-04', category: 'Multimedia', amount: -50, color: '#a3e635' }
  ]
}
```

### Configurações do widget

_Este widget não tem diálogo de configurações; os controles ficam no próprio card (ver atributos abaixo)._

### Atributos `data-*`

| Atributo | Onde / efeito |
|---|---|
| `data-widget` | No `<article>`: chave do widget em `state`/`renderWidget()`; também é o alvo do filtro e do observador de renderização preguiçosa. |
| `data-menu` | Botão “mais ações”: alterna o `.widget-menu` irmão e `aria-expanded`. |
| `data-download` | Item do menu: chama `downloadCsv(widget)`. |
| `data-reset` | Item do menu: restaura os padrões do widget e chama `renderWidget(widget)`. |
| `data-portfolio-day` | Gerado: índice do dia; clique seleciona. |
| `data-view-transaction` | Gerado no menu da linha: abre `#portfolio-transaction-details` preenchido. |
| `data-copy-transaction` | Gerado: copia o valor (Clipboard API; fallback em toast). |
| `data-widget-filter` | Criado pelo JS (`addFilterAction`): botão “Filter” no canto do card, abre a gaveta `#widget-filter-drawer` com busca e faixa mín./máx. |

### Funções e eventos

| Função / evento | O que faz |
|---|---|
| `renderPortfolioActivity()` | Hexágonos, `aria-label` do mapa, total, texto do dia e lista de transações. |
| `buildPortfolioActivity()` | Gerador da grade de amostra (substituir pelos dias reais). |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- O saldo das contas está em `financial_bank_accounts` (sem rota de domínio própria). Pagas recentes: `GET /api/v1/domain/records/financial/payable?status=paid&per_page=10`, permissão `admin.financial.view` (a mesma das rotas `/financial/*` em `app/Config/page-domain-sources.php`).
- **Recomendado:** provider com as três consultas abaixo → `{ "total_value", "days": [...], "transactions": [...] }`.

## Acessibilidade

- Cada hexágono é `<button>` com `aria-pressed` e `aria-label` “data: N activity events”; o nível também está no texto do dia selecionado.
- Menus de linha têm `aria-label` “Actions for <nome>” e `aria-expanded`.
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
$endpoint = '/financial/widgets/portfolio-activity' /* rota do provider do módulo, a criar */;
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="portfolioActivity"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="portfolioActivity-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget portfolio-activity-widget" data-widget="portfolioActivity" aria-labelledby="portfolio-activity-title">
  <header class="portfolio-total-head">
    <div class="portfolio-title">
      <span class="portfolio-wallet-icon" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <h2 id="portfolio-activity-title">Total value</h2>
    </div>
    <div class="widget-menu-wrap">
      <button class="portfolio-open-button" type="button" aria-label="More portfolio activity actions" aria-expanded="false" data-menu="portfolioActivity">
        <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
      </button>
      <div class="widget-menu" hidden>
        <button type="button" data-download="portfolioActivity">Download CSV</button>
        <button type="button" data-reset="portfolioActivity">Reset widget</button>
      </div>
    </div>
  </header>
  <div class="portfolio-total-value" id="portfolio-total-value">$120,467.00</div>
  <div class="portfolio-welcome-row">
    <div class="portfolio-avatar" aria-hidden="true">JD</div>
    <div class="portfolio-welcome">
      <strong>Welcome, James <span aria-hidden="true">👋</span></strong>
      <span>Today you are in Italy</span>
    </div>
    <time id="portfolio-current-date" datetime="2024-08-16">16 Aug, 2024</time>
  </div>
  <div class="portfolio-heatmap-wrap">
    <div class="portfolio-heatmap" id="portfolio-activity-map" role="group" aria-label="Daily activity heatmap"></div>
    <div class="portfolio-heatmap-caption">
      <span id="portfolio-activity-selected" aria-live="polite">Select a hexagon to inspect daily activity</span>
      <span class="portfolio-heatmap-legend">
        <span>Less</span>
        <i class="activity-level-1"></i>
        <i class="activity-level-2"></i>
        <i class="activity-level-3"></i>
        <i class="activity-level-4"></i>
        <span>More</span>
      </span>
    </div>
  </div>
  <section class="portfolio-transactions" id="portfolio-activity-transactions" aria-label="Recent transactions">
    <ul class="portfolio-transaction-list" id="portfolio-transaction-list"></ul>
  </section>
  <dialog class="widget-settings portfolio-transaction-dialog" id="portfolio-transaction-details" aria-labelledby="portfolio-transaction-detail-title">
    <form method="dialog">
      <header>
        <div>
          <div>
            <h3 id="portfolio-transaction-detail-title">Transaction details</h3>
            <p id="portfolio-transaction-detail-subtitle"></p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close transaction details">×</button>
        </div>
      </header>
      <div class="portfolio-transaction-detail-body">
        <strong id="portfolio-transaction-detail-amount"></strong>
        <span id="portfolio-transaction-detail-category"></span>
        <time id="portfolio-transaction-detail-date"></time>
      </div>
      <footer><button class="button-secondary" value="cancel">Close</button></footer>
    </form>
  </dialog>
</article>
```

### CSS

Arquivos: `ttsc.analytics-panels.css` (`.ttsc-analytics-card`, `-head`, `-plot`, `-foot`, `-empty`) + `docs/model/widgets/widgets.css` (layout e regras deste widget). O tema escuro de `widgets.css` é `html[data-theme="dark"]` (redefine `--w-surface`, `--w-text`, `--w-border`, `--w-grid`…); o de `ttsc.analytics-panels.css` é `html.dark` — `TTSCModelKit.syncTheme()` mantém os dois em sincronia.

Regras reais deste widget em `widgets.css`:

```css
.portfolio-activity-widget { width: min(100%, 540px); min-width: 0; padding: 20px !important; border-color: #ece7f7 !important; border-radius: 20px !important; }
.portfolio-total-head { display: flex; min-height: 35px; align-items: center; justify-content: space-between; margin-bottom: 4px; }
.portfolio-title { display: flex; min-width: 0; align-items: center; gap: 11px; }
.portfolio-wallet-icon { display: grid; width: 24px; height: 24px; place-items: center; color: var(--w-text); }
.portfolio-wallet-icon svg { width: 21px; height: 21px; fill: none; stroke: currentColor; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }
.portfolio-title h2 { margin: 0; font-size: 19px; font-weight: 600; letter-spacing: -.025em; }
.portfolio-open-button { display: grid; width: 32px; height: 32px; place-items: center; border: 1px solid transparent; border-radius: 50%; background: var(--w-canvas); color: var(--w-text); cursor: pointer; }
.portfolio-open-button:hover, .portfolio-open-button[aria-expanded="true"] { border-color: var(--w-border); background: var(--w-surface); }
.portfolio-open-button svg { width: 18px; height: 18px; fill: none; stroke: currentColor; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }
.portfolio-total-value { margin: 5px 0 12px; color: var(--w-text); font-size: 31px; font-variant-numeric: tabular-nums; font-weight: 600; letter-spacing: -.04em; line-height: 1.15; }
.portfolio-welcome-row { display: flex; min-width: 0; align-items: center; gap: 11px; margin: 12px 0 3px; }
.portfolio-avatar { display: grid; width: 42px; height: 42px; flex: 0 0 auto; place-items: center; border: 2px solid var(--w-surface); border-radius: 50%; background: #e9e2fa; color: #5127a8; font-size: 12px; font-weight: 700; box-shadow: 0 0 0 1px #e5dff1; }
.portfolio-welcome { display: grid; min-width: 0; gap: 1px; }
.portfolio-welcome strong { overflow: hidden; color: var(--w-text); font-size: 14px; font-weight: 600; text-overflow: ellipsis; white-space: nowrap; }
.portfolio-welcome strong span { margin-left: 2px; font-size: 13px; }
.portfolio-welcome > span, .portfolio-welcome-row time { color: var(--w-muted); font-size: 11px; }
.portfolio-welcome-row time { margin-left: auto; flex: 0 0 auto; color: var(--w-secondary); font-size: 12px; font-weight: 600; }
.portfolio-heatmap-wrap { padding: 14px 2px 15px; }
.portfolio-heatmap { display: grid; width: min(100%, 430px); grid-template-columns: repeat(17, minmax(0, 1fr)); grid-template-rows: repeat(13, clamp(15px, 4.25vw, 23px)); gap: clamp(2px, .65vw, 4px); justify-items: center; margin: 0 auto; }
.portfolio-hex { width: 100%; height: 100%; grid-column: var(--hex-column); grid-row: var(--hex-row); padding: 0; clip-path: polygon(25% 4%, 75% 4%, 100% 50%, 75% 96%, 25% 96%, 0 50%); border: 0; background: #f1ebfb; cursor: pointer; /* … */ }
.portfolio-hex.is-offset { transform: translateX(50%); }
.portfolio-hex.level-1 { background: #d7c8f5; }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Níveis do mapa a partir da cor de destaque */
.portfolio-hex.level-1 { background: color-mix(in srgb, var(--ttsc-accent) 25%, transparent); }
.portfolio-hex.level-4 { background: var(--ttsc-accent); }
```

### JS

Render real em `widgets.js`:

```js
function renderPortfolioActivity() {
  const widgetData = data.portfolioActivity;
  const days = widgetData.days;
  const map = byId('portfolio-activity-map');
  map.innerHTML = days.map((day, index) => {
    const dateLabel = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' }).format(day.date);
    const pressed = state.portfolioActivity.selectedDay === index;
    return `<button type="button" class="portfolio-hex level-${day.level}${day.row % 2 ? ' is-offset' : ''}${pressed ? ' is-selected' : ''}" style="--hex-column:${day.column + 1};--hex-row:${day.row + 1}" data-portfolio-day="${index}" aria-pressed="${pressed}" aria-label="${dateLabel}: ${day.count} activity events" title="${dateLabel} · ${day.count} activities"></button>`;
  }).join('');
  map.setAttribute('aria-label', `Daily activity heatmap with ${days.length} days, ${days[0] ? new Intl.DateTimeFormat('en-GB', { dateStyle: 'medium', timeZone: 'UTC' }).format(days[0].date) : ''} to ${days.length ? new Intl.DateTimeFormat('en-GB', { dateStyle: 'medium', timeZone: 'UTC' }).format(days.at(-1).date) : ''}.`);
  byId('portfolio-total-value').textContent = fmtMoney(widgetData.totalValue);
  const selected = days[state.portfolioActivity.selectedDay];
  byId('portfolio-activity-selected').textContent = selected
    ? `${new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(selected.date)} · ${selected.count} ${selected.count === 1 ? 'activity' : 'activities'}`
    : 'Select a hexagon to inspect daily activity';
  byId('portfolio-transaction-list').innerHTML = widgetData.transactions.map(transaction => `<li class="portfolio-transaction-row"><span class="portfolio-transaction-name">${transaction.name}</span><time datetime="${transaction.date}">${new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${transaction.date}T00:00:00Z`))}</time><span class="portfolio-transaction-category"><i style="--transaction-color:${transaction.color}"></i>${transaction.category}</span><strong class="portfolio-transaction-amount">${fmtMoney(transaction.amount)}</strong><div class="widget-menu-wrap"><button class="portfolio-transaction-more" type="button" aria-label="Actions for ${transaction.name}" aria-expanded="false" data-menu="transaction-${transaction.id}"><svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="4" r="1"/><circle cx="10" cy="10" r="1"/><circle cx="10" cy="16" r="1"/></svg></button><div class="widget-menu" hidden><button type="button" data-view-transaction="${transaction.id}">View details</button><button type="button" data-copy-transaction="${transaction.id}">Copy amount</button></div></div></li>`).join('');
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

// payload = { total_value: '120467.00', days: [{ day: '2026-10-01', events: 9, level: 3 }], transactions: [{ uuid, name, date, category, color, amount }] }
loadWidget('portfolioActivity', (rows, payload) => {
  const COLUMNS = 17;
  data.portfolioActivity = {
    totalValue: Number(payload.total_value) || 0,
    days: (payload.days ?? []).map((d, index) => ({ row: Math.floor(index / COLUMNS), column: index % COLUMNS, count: Number(d.events) || 0, level: Number(d.level) || 0, date: new Date(`${d.day}T00:00:00Z`) })),
    transactions: (payload.transactions ?? []).map(t => ({ id: t.uuid, name: t.name, date: t.date, category: t.category ?? '—', amount: Number(t.amount) || 0, color: t.color || '#94a3b8' })),
  };
  return data.portfolioActivity.days.length > 0;
});
```

O menu “Download CSV” chama `downloadCsv('portfolioActivity')`, que serializa a **série de amostra** (`portfolioActivity-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Três consultas: patrimônio (soma de contas ativas), atividade diária dos últimos 180 dias (`financial_transactions`, nível 0–4 por `CEIL(n/3)`) e as três últimas contas pagas com categoria e cor. Testado no MariaDB local.

```sql
-- Patrimônio: saldo das contas ativas
SELECT SUM(a.balance) AS total_value
  FROM financial_bank_accounts a
 WHERE a.deleted_at IS NULL AND a.is_active = 1;

-- Atividade diária (hexágonos): lançamentos por dia, com nível 0–4
SELECT t.transaction_date AS day,
       COUNT(*)           AS events,
       LEAST(4, CEIL(COUNT(*) / 3)) AS level
  FROM financial_transactions t
 WHERE t.transaction_date >= CURDATE() - INTERVAL 180 DAY
 GROUP BY t.transaction_date
 ORDER BY t.transaction_date;

-- Transações recentes (lista): três últimas contas pagas
SELECT p.uuid, p.description AS name, p.payment_date AS date, c.name AS category, c.color, -p.amount_paid AS amount
  FROM financial_payables p
  LEFT JOIN financial_categories c ON c.id = p.category_id
 WHERE p.deleted_at IS NULL AND p.status = 'paid'
 ORDER BY p.payment_date DESC, p.id DESC
 LIMIT 3;
```

O provider devolve as três partes num JSON; dias sem lançamento devem entrar com `events = 0` para a grade não ter buracos.

## Faça / Não faça

- **Faça:** preencher dias vazios com nível 0;
- **Faça:** manter o valor da transação com sinal (saída negativa).
- **Não faça:** mostrar dados pessoais de terceiros na saudação, nem manter o emoji de aceno do modelo (`<span aria-hidden="true">` após o nome) — o design system não usa emoji;
- **Não faça:** usar o mapa sem a legenda textual do dia selecionado.
