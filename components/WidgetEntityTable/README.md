# WidgetEntityTable

Card “Entity connections”: tabela de contrapartes com tipo (ícone de status), recebido e enviado, alternância Todas/Diretas, chips de filtros ativos e diálogo de filtros (datas, valor enviado, tipo, entidade).

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só os cards `entityTable` e `entityTableFiltered` (este com filtros ativos). Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Listar as conexões por contraparte que compõem o [WidgetEntityMap](../WidgetEntityMap/README.md), com filtros rápidos.
- Tabelas curtas dentro de um painel (sem paginação real; o rodapé mostra “Showing 1–N of N”).
- Para listas longas, paginadas e com busca use a tabela do chassi ([RecordsTable](../RecordsTable/README.md) / [DataTable](../DataTable/README.md)).

## Anatomia

```
┌ ícone · Entity connections (i)          [Filter (4)] ┐  data-open-settings + data-filter-count
│ [All] [Direct]   (25 Dec–24 Jan ×) (Sent < $3,000 ×) [x]│  #entity-table-chips
│ Entity   Type            Received      Sent           │  table.entity-connection-table
│ Binance  ✓ Exchange     $235,500.00   $50,150.50      │
│ Showing 1–9 of 9 connections · $… received · $… sent  │  #entity-table-footer
└───────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Botão de filtros | `button[data-open-settings="entityTable"]` com badge `[data-filter-count]` (contagem de chips) | sim |
| Alternância | `.entity-table-switch > .entity-view-toggle > button[data-table-view][data-view="all|direct"]` | sim |
| Chips | `.filter-chips#entity-table-chips` > `button.filter-chip[data-remove-filter][data-filter-key]` + `.filter-chip-clear[data-clear-filters]` | sim |
| Tabela | `.entity-table-scroll > table.entity-connection-table` (`thead th[scope="col"]`, `tbody#entity-table-rows`) | sim |
| Tipo | `.entity-type-cell > i.is-good|is-warning|is-danger` + texto | sim |
| Rodapé | `#entity-table-footer` | sim |
| Filtros | `dialog.widget-settings.entity-filter-dialog#settings-entityTable` | sim |

## Variantes

| Variação | Estado inicial |
|---|---|
| `entityTable` | Sem filtros (`from`, `to`, `sentMax`, `type`, `entity` vazios) |
| `entityTableFiltered` | `from: 2025-12-25`, `to: 2026-01-24`, `sentMax: 3000`, `type: Exchange`, `entity: ByBit` |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('entityTable')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Após “Apply settings” o diálogo grava em `state.entityTable` e re-renderiza só este widget; o toast `#widget-toast` confirma. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Sem resultados | Linha única `td.entity-empty-cell[colspan="4"]` “No connections match these filters.” |
| Filtros ativos | Chips por filtro, botão de limpar tudo e badge com a contagem; o botão de filtro ganha `.is-active`. |

## API

### Dados esperados

As mesmas linhas de `data.entityConnections` do mapa; a tabela filtra no cliente por visão, intervalo de datas, enviado < máximo, tipo e entidade.

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `entity` | `string` | texto | Coluna Entity. |
| `type` | `string` | texto | Coluna Type; define o ícone (`Exchange` ✓, `Sanctions` −, `Unnamed Service`/`Infrastructure` !). |
| `received` / `sent` | `number` | moeda USD, 2 casas (`entityMoney`) | Colunas de valor e somas do rodapé. |
| `date` | `string` | `YYYY-MM-DD` | Filtro de datas (comparação de string). |
| `direct` | `boolean` | — | Visão “Direct”. |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js
entityConnections: [
  { entity: 'Binance', type: 'Exchange', group: 'Exchange', received: 235500, sent: 50150.50, date: '2026-01-02', direct: true },
  { entity: 'Binance', type: 'Market', group: 'Dark Market', received: 20000, sent: 100, date: '2026-01-04', direct: true },
  { entity: 'Binance', type: 'Market', group: 'Market', received: 12000, sent: 375, date: '2026-01-10', direct: true },
  { entity: 'Binance', type: 'Market', group: 'Market', received: 7000, sent: 2350, date: '2026-01-19', direct: false },
  { entity: 'ByBit', type: 'Exchange', group: 'Exchange', received: 1500, sent: 2500.70, date: '2025-12-30', direct: true },
  { entity: 'ByBit', type: 'Exchange', group: 'Exchange', received: 21500, sent: 0, date: '2026-01-17', direct: true },
  { entity: 'Private', type: 'Unnamed Service', group: 'Unnamed Service', received: 20000, sent: 700, date: '2025-12-24', direct: false },
  { entity: 'Unnamed', type: 'Sanctions', group: 'Sanctions', received: 0, sent: 50150.50, date: '2026-01-06', direct: false },
  { entity: 'Unnamed', type: 'Infrastructure', group: 'Infrastructure', received: 9000, sent: 2200, date: '2026-01-13', direct: false }
]
```

### Configurações do widget

**`entityTable`**

Padrão em `state.entityTable`: `{ view: 'all', from: '', to: '', sentMax: '', type: '', entity: '' }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `from` | input date | — | From date | Data inicial (inclusive). |
| `to` | input date | — | To date | Data final (inclusive). |
| `sentMax` | input number | min 0, step 100 | Sent amount below (USD) | Mantém linhas com enviado **menor** que o valor. |
| `type` | select | `""` (Any type) · `Exchange` · `Market` · `Sanctions` · `Infrastructure` · `Unnamed Service` | Type | Tipo exato. |
| `entity` | select | `""` (Any entity) · `Binance` · `ByBit` · `Private` · `Unnamed` | Entity | Entidade exata. |

**`entityTableFiltered`**

Padrão em `state.entityTableFiltered`: `{ view: 'all', from: '2025-12-25', to: '2026-01-24', sentMax: 3000, type: 'Exchange', entity: 'ByBit' }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `from` | input date | — | From date | Data inicial (inclusive). |
| `to` | input date | — | To date | Data final (inclusive). |
| `sentMax` | input number | min 0, step 100 | Sent amount below (USD) | Mantém linhas com enviado **menor** que o valor. |
| `type` | select | `""` (Any type) · `Exchange` · `Market` · `Sanctions` · `Infrastructure` · `Unnamed Service` | Type | Tipo exato. |
| `entity` | select | `""` (Any entity) · `Binance` · `ByBit` · `Private` · `Unnamed` | Entity | Entidade exata. |

### Atributos `data-*`

| Atributo | Onde / efeito |
|---|---|
| `data-widget` | No `<article>`: chave do widget em `state`/`renderWidget()`; também é o alvo do filtro e do observador de renderização preguiçosa. |
| `data-open-settings` | Botão de ajuste: abre `<dialog id="settings-<widget>">` e copia `state[widget]` para os campos. |
| `data-setting` | Campo do diálogo: widget dono da configuração (isolamento: cada widget só lê os seus campos). |
| `data-key` | Campo do diálogo: chave dentro de `state[widget]` (checkbox vira booleano, `number` vira número). |
| `data-filter-count` | Badge do botão de filtros: nº de chips; escondido quando 0. |
| `data-table-view` | Botão da alternância: widget alvo; com `data-view="all|direct"`. |
| `data-view` | Valor da visão. |
| `data-remove-filter` | Gerado no chip: widget; com `data-filter-key` (`date`, `sentMax`, `type`, `entity`) remove um filtro. |
| `data-clear-filters` | Gerado: limpa todos os filtros e os campos do diálogo. |
| `data-widget-filter` | Criado pelo JS (`addFilterAction`): botão “Filter” no canto do card, abre a gaveta `#widget-filter-drawer` com busca e faixa mín./máx. |

### Funções e eventos

| Função / evento | O que faz |
|---|---|
| `renderEntityTable(widget)` | Filtra, monta linhas, chips, badge, `aria-pressed` da alternância e rodapé com somas. |
| `activeEntityFilters(widget)` | Lista de chips `{ key, label }` a partir do `state`. |
| clique `[data-remove-filter]` / `[data-clear-filters]` | Atualiza `state` e re-renderiza. |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- Não há rota de domínio que agregue `banks_transactions` por contraparte; a view `inst_banks_transactions` (com `counterparty_name`, `category`, `type`, `amount`) é a fonte de leitura do módulo Bancos. Exponha as consultas abaixo num provider desse módulo, com a permissão da página de transações bancárias e o filtro de `tenant_id` que o `BanksController` já aplica.
- Para filtrar no servidor (listas grandes), o provider aceita os mesmos nomes de filtro (`from`, `to`, `sent_max`, `type`, `entity`, `direct`) — ver a segunda consulta.

## Acessibilidade

- Tabela semântica com `th scope="col"`; o ícone de tipo é `aria-hidden` e o tipo também está em texto.
- Chips são `<button>`; o de limpar tudo tem `aria-label` “Clear all active filters”.
- A alternância usa `aria-pressed`.
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
$endpoint = '/banks/transactions/widgets/entity-connections' /* rota do provider do módulo, a criar */;
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="entityTable"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="entityTable-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget entity-table-widget" data-widget="entityTable" aria-labelledby="entity-table-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-green" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line"><h2 id="entity-table-title">Entity connections</h2></div>
        <p>Received and sent amounts by entity</p>
      </div>
    </div>
    <div class="entity-table-actions">
      <button class="entity-filter-button" type="button" data-open-settings="entityTable" aria-label="Filter entity connections">
        <svg viewBox="0 0 20 20">…</svg>
        <span>Filter</span>
        <b data-filter-count="entityTable" hidden></b>
      </button>
    </div>
  </header>
  <div class="entity-table-switch">
    <div class="entity-view-toggle" role="group" aria-label="Connection scope">
      <button type="button" data-table-view="entityTable" data-view="all" aria-pressed="true">All</button>
      <button type="button" data-table-view="entityTable" data-view="direct" aria-pressed="false">Direct</button>
    </div>
    <div class="filter-chips" id="entity-table-chips"></div>
  </div>
  <div class="entity-table-scroll">
    <table class="entity-connection-table">
      <thead>
        <tr>
          <th scope="col">Entity</th>
          <th scope="col">Type</th>
          <th scope="col">Received, USD</th>
          <th scope="col">Sent, USD</th>
        </tr>
      </thead>
      <tbody id="entity-table-rows"></tbody>
    </table>
  </div>
  <footer class="entity-table-footer" id="entity-table-footer"></footer>
  <dialog class="widget-settings entity-filter-dialog" id="settings-entityTable" aria-label="Filter entity connections">
    <form method="dialog">
      <header>
        <div>
          <div>
            <h3>Filter connections</h3>
            <p>Combine date, type, entity and sent amount filters.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close filters">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">From date<input type="date" data-setting="entityTable" data-key="from"></label>
        <label class="settings-field">To date<input type="date" data-setting="entityTable" data-key="to"></label>
        <!-- … +3 elemento(s) iguais gerados pelo JS -->
      </div>
      <footer>
        <button class="button-secondary" type="button" data-clear-filters="entityTable">Clear all</button>
        <button class="button-primary" value="save">Apply filters</button>
      </footer>
    </form>
  </dialog>
</article>
```

```html
<article class="ttsc-analytics-card widget demo-widget entity-table-widget entity-table-filtered" data-widget="entityTableFiltered" aria-labelledby="entity-table-filtered-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-green" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line"><h2 id="entity-table-filtered-title">Entity connections</h2></div>
        <p>Filtered received and sent amounts</p>
      </div>
    </div>
    <div class="entity-table-actions">
      <button class="entity-filter-button is-active" type="button" data-open-settings="entityTableFiltered" aria-label="Edit active entity connection filters">
        <svg viewBox="0 0 20 20">…</svg>
        <span>Filter</span>
        <b data-filter-count="entityTableFiltered">4</b>
      </button>
    </div>
  </header>
  <div class="entity-table-switch">
    <div class="entity-view-toggle" role="group" aria-label="Connection scope">
      <button type="button" data-table-view="entityTableFiltered" data-view="all" aria-pressed="true">All</button>
      <button type="button" data-table-view="entityTableFiltered" data-view="direct" aria-pressed="false">
        Direct
      </button>
    </div>
    <div class="filter-chips" id="entity-table-filtered-chips"></div>
  </div>
  <div class="entity-table-scroll">
    <table class="entity-connection-table">
      <thead>
        <tr>
          <th scope="col">Entity</th>
          <th scope="col">Type</th>
          <th scope="col">Received, USD</th>
          <th scope="col">Sent, USD</th>
        </tr>
      </thead>
      <tbody id="entity-table-filtered-rows"></tbody>
    </table>
  </div>
  <footer class="entity-table-footer" id="entity-table-filtered-footer"></footer>
  <dialog class="widget-settings entity-filter-dialog" id="settings-entityTableFiltered" aria-label="Edit entity connection filters">
    <form method="dialog">
      <header>
        <div>
          <div>
            <h3>Filter connections</h3>
            <p>Combine date, type, entity and sent amount filters.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close filters">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          From date
          <input type="date" data-setting="entityTableFiltered" data-key="from">
        </label>
        <label class="settings-field">
          To date
          <input type="date" data-setting="entityTableFiltered" data-key="to">
        </label>
        <!-- … +3 elemento(s) iguais gerados pelo JS -->
      </div>
      <footer>
        <button class="button-secondary" type="button" data-clear-filters="entityTableFiltered">Clear all</button>
        <button class="button-primary" value="save">Apply filters</button>
      </footer>
    </form>
  </dialog>
</article>
```

### CSS

Arquivos: `ttsc.analytics-panels.css` (`.ttsc-analytics-card`, `-head`, `-plot`, `-foot`, `-empty`) + `docs/model/widgets/widgets.css` (layout e regras deste widget). O tema escuro de `widgets.css` é `html[data-theme="dark"]` (redefine `--w-surface`, `--w-text`, `--w-border`, `--w-grid`…); o de `ttsc.analytics-panels.css` é `html.dark` — `TTSCModelKit.syncTheme()` mantém os dois em sincronia.

Regras reais deste widget em `widgets.css`:

```css
.entity-map-widget, .entity-table-widget { min-width: 0; }
.entity-map-toolbar, .entity-table-switch { display: flex; min-width: 0; align-items: center; justify-content: space-between; gap: 12px; margin: 6px 0 12px; }
.entity-table-actions { display: flex; flex: 0 0 auto; }
.entity-table-switch { align-items: flex-start; margin: 0 0 12px; }
.filter-chip { display: inline-flex; min-height: 26px; align-items: center; gap: 6px; max-width: 100%; padding: 0 8px; border: 1px solid transparent; border-radius: 999px; background: var(--w-canvas); color: var(--w-muted); /* … */ }
.filter-chip > span:first-child { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.filter-chip > span:last-child { font-size: 13px; }
.filter-chip:hover { border-color: var(--w-border); color: var(--w-text); }
.entity-table-scroll { width: 100%; overflow-x: auto; }
.entity-connection-table { width: 100%; min-width: 510px; border-collapse: collapse; color: var(--w-text); font-size: 10px; font-variant-numeric: tabular-nums; }
.entity-connection-table th, .entity-connection-table td { padding: 9px 6px; border-bottom: 1px solid var(--w-grid); text-align: right; white-space: nowrap; }
.entity-connection-table thead th { color: var(--w-muted); font-size: 9px; font-weight: 500; }
.entity-connection-table th:first-child, .entity-connection-table td:first-child { text-align: left; }
.entity-connection-table tbody td { color: var(--w-text); font-size: 10px; }
.entity-connection-table tbody td:first-child strong { font-weight: 600; }
.entity-type-cell { display: inline-flex; align-items: center; gap: 6px; color: var(--w-muted); }
.entity-type-cell i { display: grid; width: 13px; height: 13px; place-items: center; border-radius: 50%; font-size: 9px; font-style: normal; font-weight: 700; }
.entity-type-cell i.is-good { background: #22c55e; color: #fff; }
.entity-type-cell i.is-warning { background: #facc15; color: #854d0e; }
.entity-type-cell i.is-danger { background: #ef4444; color: #fff; }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Densidade e cores de status com tokens semânticos */
.entity-connection-table td { padding-block: var(--ttsc-space-2); border-color: var(--ttsc-border-soft); }
.entity-type-cell i.is-danger  { background: var(--ttsc-danger); }
.entity-type-cell i.is-warning { background: var(--ttsc-warning); }
```

### JS

Render real em `widgets.js`:

```js
function activeEntityFilters(widget) {
  const filters = state[widget];
  return [
    ...(filters.from || filters.to ? [{ key: 'date', label: `${filters.from ? new Date(`${filters.from}T00:00:00`).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) : 'Any date'} – ${filters.to ? new Date(`${filters.to}T00:00:00`).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) : 'Any date'}` }] : []),
    ...(filters.sentMax !== '' && filters.sentMax !== null ? [{ key: 'sentMax', label: `Sent < ${entityMoney(Number(filters.sentMax))}` }] : []),
    ...(filters.type ? [{ key: 'type', label: filters.type }] : []),
    ...(filters.entity ? [{ key: 'entity', label: filters.entity }] : [])
  ];
}
```

```js
function renderEntityTable(widget) {
  const filtered = widget === 'entityTableFiltered';
  const prefix = filtered ? 'entity-table-filtered' : 'entity-table';
  const filters = state[widget];
  let rows = data.entityConnections.filter(row => {
    if (filters.view === 'direct' && !row.direct) return false;
    if (filters.from && row.date < filters.from) return false;
    if (filters.to && row.date > filters.to) return false;
    if (filters.sentMax !== '' && filters.sentMax !== null && row.sent >= Number(filters.sentMax)) return false;
    if (filters.type && row.type !== filters.type) return false;
    if (filters.entity && row.entity !== filters.entity) return false;
    return true;
  });
  const body = byId(`${prefix}-rows`);
  body.innerHTML = rows.length ? rows.map(row => {
    const status = row.type === 'Exchange' ? 'is-good' : row.type === 'Sanctions' ? 'is-danger' : row.type === 'Unnamed Service' || row.type === 'Infrastructure' ? 'is-warning' : 'is-good';
    const icon = status === 'is-good' ? '✓' : status === 'is-danger' ? '−' : '!';
    return `<tr><td><strong>${row.entity}</strong></td><td><span class="entity-type-cell"><i class="${status}" aria-hidden="true">${icon}</i><span>${row.type === 'Infrastructure' ? 'Infrastructure Asset' : row.type}</span></span></td><td>${entityMoney(row.received)}</td><td>${entityMoney(row.sent)}</td></tr>`;
  }).join('') : '<tr><td class="entity-empty-cell" colspan="4">No connections match these filters.</td></tr>';
  const chips = activeEntityFilters(widget);
  byId(`${prefix}-chips`).innerHTML = chips.map(chip => `<button type="button" class="filter-chip" data-remove-filter="${widget}" data-filter-key="${chip.key}"><span>${chip.label}</span><span aria-hidden="true">×</span></button>`).join('') + (chips.length ? `<button type="button" class="filter-chip-clear" data-clear-filters="${widget}" aria-label="Clear all active filters"><svg viewBox="0 0 20 20"><path d="M4 6h12m-10 0 1 11h6l1-11M8 6V4h4v2m-3 3v5m2-5v5"/></svg></button>` : '');
  const countButton = document.querySelector(`[data-filter-count="${widget}"]`);
  countButton.textContent = chips.length;
  countButton.hidden = chips.length === 0;
  countButton.parentElement.classList.toggle('is-active', chips.length > 0);
  document.querySelectorAll(`[data-table-view="${widget}"]`).forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === filters.view)));
  const start = rows.length ? 1 : 0;
  byId(`${prefix}-footer`).textContent = `Showing ${start}–${rows.length} of ${rows.length} connections · ${entityMoney(sum(rows.map(row => row.received)))} received · ${entityMoney(sum(rows.map(row => row.sent)))} sent`;
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

// Mesma carga do WidgetEntityMap (data.entityConnections). Para filtrar no servidor:
async function reloadEntityTable(widget) {
  const f = state[widget];
  const params = new URLSearchParams({ from: f.from || '', to: f.to || '', sent_max: f.sentMax ?? '', type: f.type || '', entity: f.entity || '', direct: f.view === 'direct' ? 1 : 0 });
  await loadWidget(widget, rows => {
    data.entityConnections = rows.map(row => ({ entity: row.entity, type: row.type, group: row.type, received: Number(row.received) || 0, sent: Number(row.sent) || 0, date: row.last_date, direct: true }));
  });
  // loadWidget lê card.dataset.endpoint: monte-o com `${base}?${params}` antes da chamada.
}
```

O menu “Download CSV” chama `downloadCsv('entityTable')`, que serializa a **série de amostra** (`entityTable-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Linhas da tabela já filtradas no servidor, com os mesmos filtros do diálogo; `HAVING` aplica o “enviado abaixo de”. Placeholders vazios (`''`) desligam cada filtro. Testado no MariaDB local com filtros vazios.

```sql
-- Exposição por contraparte bancária: volume recebido + enviado, agrupado por categoria (view "type") ou contraparte (view "entity")
SELECT COALESCE(t.category, 'Sem categoria')                         AS type,
       COALESCE(t.counterparty_name, 'Não identificado')             AS entity,
       SUM(CASE WHEN t.type = 'credit' THEN t.amount ELSE 0 END)     AS received,
       SUM(CASE WHEN t.type = 'debit'  THEN t.amount ELSE 0 END)     AS sent,
       COUNT(*)                                                      AS connections
  FROM banks_transactions t
 WHERE t.tenant_id = :tenant_id
   AND t.status NOT IN ('reversed', 'failed', 'cancelled')
   AND t.transaction_date >= CURDATE() - INTERVAL 90 DAY
 GROUP BY COALESCE(t.category, 'Sem categoria'), COALESCE(t.counterparty_name, 'Não identificado')
 ORDER BY SUM(t.amount) DESC;
```

```sql
-- Linhas da tabela com os filtros do diálogo (from, to, sentMax, type, entity) e a visão "direct"
SELECT t.counterparty_name AS entity,
       t.category          AS type,
       SUM(CASE WHEN t.type = 'credit' THEN t.amount ELSE 0 END) AS received,
       SUM(CASE WHEN t.type = 'debit'  THEN t.amount ELSE 0 END) AS sent,
       MAX(t.transaction_date) AS last_date
  FROM banks_transactions t
 WHERE t.tenant_id = :tenant_id
   AND t.status NOT IN ('reversed', 'failed', 'cancelled')
   AND (:from = '' OR t.transaction_date >= :from)
   AND (:to   = '' OR t.transaction_date <= :to)
   AND (:type = '' OR t.category = :type)
   AND (:entity = '' OR t.counterparty_name = :entity)
   AND (:direct = 0 OR t.counterparty_document IS NOT NULL)        -- visão "Direct": contraparte identificada
 GROUP BY t.counterparty_name, t.category
HAVING (:sent_max = '' OR sent < :sent_max)
 ORDER BY received DESC
 LIMIT 25 OFFSET 0;
```

O PHP passa os filtros como parâmetros nomeados (nunca concatenados); `LIMIT/OFFSET` fixos de 25 cobrem o card. Se a lista crescer, migre para a tabela paginada do chassi.

## Faça / Não faça

- **Faça:** refletir cada filtro ativo num chip removível;
- **Faça:** manter o rodapé com totais da seleção.
- **Não faça:** comparar datas como texto em formato diferente de `YYYY-MM-DD`;
- **Não faça:** usar este card como tabela principal de uma página.
