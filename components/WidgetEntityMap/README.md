# WidgetEntityMap

Card “Entity exposure”: treemap de botões proporcional ao volume (recebido + enviado) por tipo de contraparte ou por contraparte, com painel de detalhe do segmento selecionado e atalho para a tabela de conexões.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só os cards `entityMap` e `entityMapFocus` (este já com “Dark Market” selecionado). Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Mostrar concentração de movimentação bancária por contraparte ou por categoria (`banks_transactions.counterparty_name` / `category`), para auditoria e conciliação.
- Quando a pergunta é “quem concentra o volume” e o próximo passo é abrir a lista filtrada ([WidgetEntityTable](../WidgetEntityTable/README.md)).
- Não use para séries no tempo; para participação com total fixo e até 3 itens use [WidgetSubscriptions](../WidgetSubscriptions/README.md).

## Anatomia

```
┌ ícone · Entity exposure (i)              Balance $34,328.83 ┐
│ [Entity types] [Entities]           9 monitored connections │  .entity-view-toggle
│ ┌──────────── Exchange ───────────┬─ Market ─┬ Dark ┐       │  #entity-map-chart > button.entity-treemap-segment
│ └─────────────────────────────────┴──────────┴──────┘       │
│ 36.4%  Dark Market  $20,100 · 1 connections  [View conn. ›] │  #entity-map-detail
└─────────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Saldo | `.entity-balance` (no cabeçalho, sem menu) | não |
| Alternância | `.entity-map-toolbar > .entity-view-toggle[role="group"] > button[data-map-view][data-view][aria-pressed]` | sim |
| Treemap | `div.entity-treemap#entity-map-chart[role="group"]` > `button.entity-treemap-segment[data-map-segment][data-map-label][aria-pressed]` (`--segment-color`, `--segment-value`) | sim |
| Detalhe | `div.entity-map-detail#entity-map-detail[hidden]` + `button[data-view-connections]` | sim |
| Configurações | `dialog#settings-entityMap` (`showValues`) | ver nota |

## Variantes

| Variação | Estado inicial |
|---|---|
| `entityMap` | `{ view: 'type', selected: null, showValues: true }` — nada selecionado, detalhe oculto |
| `entityMapFocus` | `selected: 'Dark Market'` — mostra o detalhe e liga ao card `entityTableFiltered` |

Nota: o modelo tem `dialog#settings-entityMap`/`#settings-entityMapFocus`, mas nenhum botão `data-open-settings` aponta para eles. Em produção, acrescente o botão `.widget-config` no cabeçalho (como nos demais cards) ou remova o diálogo.

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('entityMap')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Após “Apply settings” o diálogo grava em `state.entityMap` e re-renderiza só este widget; o toast `#widget-toast` confirma. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Selecionado | Segmento com `.is-selected` e `aria-pressed="true"`; `#…-detail` visível com percentual, nome e (se `showValues`) valor e nº de conexões. |
| Visão por entidade | `state.view = "entity"`: um segmento por contraparte, rótulo “Nome · Tipo”; seleção inválida é limpa. |

## API

### Dados esperados

Lista de conexões (uma linha por contraparte × tipo) com valores recebidos e enviados; o mapa agrega por `group` (tipos) ou `entity`.

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `entity` | `string` | texto | Contraparte. |
| `type` | `string` | texto | Tipo usado pelo filtro da tabela. |
| `group` | `string` | texto | Agrupamento da visão “Entity types” (cor em `entityGroupColors`). |
| `received` / `sent` | `number` | moeda, 2 casas | Volume = received + sent. |
| `date` | `string` | `YYYY-MM-DD` | Usado pela tabela. |
| `direct` | `boolean` | — | Visão “Direct” da tabela. |

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

**`entityMap`**

Padrão em `state.entityMap`: `{ view: 'type', selected: null, showValues: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `showValues` | input checkbox | booleano | Show connection values in segment details | Valor e nº de conexões no detalhe. |

**`entityMapFocus`**

Padrão em `state.entityMapFocus`: `{ view: 'type', selected: 'Dark Market', showValues: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `showValues` | input checkbox | booleano | Show connection values in segment details | Valor e nº de conexões no detalhe. |

### Atributos `data-*`

| Atributo | Onde / efeito |
|---|---|
| `data-widget` | No `<article>`: chave do widget em `state`/`renderWidget()`; também é o alvo do filtro e do observador de renderização preguiçosa. |
| `data-setting` | Campo do diálogo: widget dono da configuração (isolamento: cada widget só lê os seus campos). |
| `data-key` | Campo do diálogo: chave dentro de `state[widget]` (checkbox vira booleano, `number` vira número). |
| `data-tip` | Texto do tooltip comum (`#widget-tooltip`) em hover/foco. |
| `data-map-view` | Botão da alternância: widget alvo; com `data-view="type|entity"` muda `state[widget].view`. |
| `data-view` | Valor da visão do botão (`type`, `entity`; na tabela `all`, `direct`). |
| `data-map-segment` | Gerado: segmento do treemap; clique grava `state[widget].selected = data-map-label`. |
| `data-map-label` | Gerado: nome do grupo/entidade do segmento. |
| `data-view-connections` | Gerado no detalhe: aplica o filtro na tabela ligada (`entityMap`→`entityTable`, `entityMapFocus`→`entityTableFiltered`) e rola até ela. |
| `data-widget-filter` | Criado pelo JS (`addFilterAction`): botão “Filter” no canto do card, abre a gaveta `#widget-filter-drawer` com busca e faixa mín./máx. |

### Funções e eventos

| Função / evento | O que faz |
|---|---|
| `entityMapItems(widget)` | Agrega `data.entityConnections` por `group` ou `entity`, ordena por volume. |
| `renderEntityMap(widget)` | Gera os botões do treemap, `aria-label` do grupo e o detalhe. |
| clique `[data-view-connections]` | Zera datas/valor da tabela alvo, define `type` ou `entity` e chama `renderWidget(tabela)`. |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- Não há rota de domínio que agregue `banks_transactions` por contraparte; a view `inst_banks_transactions` (com `counterparty_name`, `category`, `type`, `amount`) é a fonte de leitura do módulo Bancos. Exponha as consultas abaixo num provider desse módulo, com a permissão da página de transações bancárias e o filtro de `tenant_id` que o `BanksController` já aplica.

## Acessibilidade

- Cada segmento é um `<button>` com `aria-pressed` e `aria-label` “Nome: X percent, $valor, N connections” — o treemap é navegável por Tab.
- Cores de grupo são pastel com texto escuro; mantenha o nome dentro do segmento (não só a cor).
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
$endpoint = '/banks/transactions/widgets/entity-exposure' /* rota do provider do módulo, a criar */;
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="entityMap"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="entityMap-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget entity-map-widget" data-widget="entityMap" aria-labelledby="entity-map-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-blue" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="entity-map-title">Entity exposure</h2>
          <button class="info-button" type="button" data-tip="Connection volume is grouped by entity type or entity name. It is calculated from received and sent USD values below." aria-label="About entity exposure">
            i
          </button>
        </div>
        <p>Connection volume by classification</p>
      </div>
    </div>
    <div class="entity-balance"><span>Balance</span><strong>$34,328.83</strong><small>15.83 ETH</small></div>
  </header>
  <div class="entity-map-toolbar">
    <div class="entity-view-toggle" role="group" aria-label="Group exposure by">
      <button type="button" data-map-view="entityMap" data-view="type" aria-pressed="true">Entity types</button>
      <button type="button" data-map-view="entityMap" data-view="entity" aria-pressed="false">Entities</button>
    </div>
    <span>9 monitored connections</span>
  </div>
  <div class="entity-treemap" id="entity-map-chart" role="group" aria-label="Exposure by entity type"></div>
  <div class="entity-map-detail" id="entity-map-detail" hidden></div>
  <dialog class="widget-settings" id="settings-entityMap" aria-label="Entity exposure settings">
    <form method="dialog">
      <header>
        <div>
          <div><h3>Entity exposure settings</h3><p>Settings apply to this widget only.</p></div>
          <button class="dialog-close" value="cancel" aria-label="Close">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-check">
          <input type="checkbox" data-setting="entityMap" data-key="showValues" checked>
          Show connection values in segment details
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

```html
<article class="ttsc-analytics-card widget demo-widget entity-map-widget" data-widget="entityMapFocus" aria-labelledby="entity-map-focus-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-blue" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="entity-map-focus-title">Entity exposure</h2>
          <button class="info-button" type="button" data-tip="Select a segment to inspect its share and open the matching connections." aria-label="About selected entity exposure">
            i
          </button>
        </div>
        <p>Selected classification and connections</p>
      </div>
    </div>
    <div class="entity-balance"><span>Balance</span><strong>$34,328.83</strong><small>15.83 ETH</small></div>
  </header>
  <div class="entity-map-toolbar">
    <div class="entity-view-toggle" role="group" aria-label="Group exposure by">
      <button type="button" data-map-view="entityMapFocus" data-view="type" aria-pressed="true">Entity types</button>
      <button type="button" data-map-view="entityMapFocus" data-view="entity" aria-pressed="false">Entities</button>
    </div>
    <span>9 monitored connections</span>
  </div>
  <div class="entity-treemap" id="entity-map-focus-chart" role="group" aria-label="Selected exposure by entity type"></div>
  <div class="entity-map-detail" id="entity-map-focus-detail"></div>
  <dialog class="widget-settings" id="settings-entityMapFocus" aria-label="Selected entity exposure settings">
    <form method="dialog">
      <header>
        <div>
          <div><h3>Entity exposure settings</h3><p>Settings apply to this widget only.</p></div>
          <button class="dialog-close" value="cancel" aria-label="Close">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-check">
          <input type="checkbox" data-setting="entityMapFocus" data-key="showValues" checked>
          Show connection values in segment details
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
.entity-map-widget, .entity-table-widget { min-width: 0; }
.entity-balance { display: grid; justify-items: end; gap: 2px; margin-left: auto; white-space: nowrap; }
.entity-balance span { color: var(--w-muted); font-size: 9px; }
.entity-balance strong { color: var(--w-text); font: 600 12px var(--ttsc-font-mono, ui-monospace, monospace); }
.entity-balance small { color: var(--w-muted); font-size: 10px; }
.entity-map-toolbar, .entity-table-switch { display: flex; min-width: 0; align-items: center; justify-content: space-between; gap: 12px; margin: 6px 0 12px; }
.entity-map-toolbar > span { color: var(--w-muted); font-size: 10px; white-space: nowrap; }
.entity-view-toggle { display: inline-flex; flex: 0 0 auto; align-items: center; padding: 3px; border-radius: 999px; background: var(--w-canvas); }
.entity-view-toggle button { min-height: 29px; padding: 0 15px; border: 0; border-radius: 999px; background: transparent; color: var(--w-muted); font: 500 11px/1 var(--ttsc-font-sans, Inter, sans-serif); cursor: pointer; /* … */ }
.entity-view-toggle button[aria-pressed="true"] { background: var(--w-surface); box-shadow: 0 1px 4px rgb(15 23 42 / .08); color: var(--w-text); font-weight: 600; }
.entity-treemap { display: flex; width: 100%; height: 42px; overflow: hidden; gap: 3px; border-radius: 6px; background: var(--w-canvas); }
.entity-map-detail { display: flex; min-height: 39px; align-items: center; justify-content: space-between; gap: 12px; margin: 10px 0 0 auto; padding: 6px 10px; border: 1px solid var(--w-border); border-radius: 9px; background: var(--w-surface); /* … */ }
.entity-map-detail[hidden] { display: none; }
.entity-map-detail > div { display: grid; grid-template-columns: auto auto; align-items: baseline; column-gap: 5px; }
.entity-map-detail strong { color: #059669; font-size: 11px; }
.entity-map-detail span { color: var(--w-text); font-size: 11px; font-weight: 600; }
.entity-map-detail small { grid-column: 1 / -1; color: var(--w-muted); font-size: 9px; }
.entity-map-detail button { padding: 4px 7px; border: 0; border-radius: 6px; background: transparent; color: var(--w-secondary); font: 500 10px/1.4 var(--ttsc-font-sans, Inter, sans-serif); cursor: pointer; white-space: nowrap; }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Seleção e foco com o anel do produto */
.entity-treemap-segment.is-selected { outline: 2px solid var(--ttsc-text); outline-offset: -2px; }
.entity-treemap-segment:focus-visible { outline: 2px solid var(--ttsc-accent); }
```

### JS

Render real em `widgets.js`:

```js
function entityMapItems(widget) {
  const stateItem = state[widget];
  const aggregateKey = stateItem.view === 'entity' ? 'entity' : 'group';
  const aggregated = new Map();
  data.entityConnections.forEach(row => {
    const name = row[aggregateKey];
    const current = aggregated.get(name) || { name, value: 0, count: 0, entity: row.entity, type: row.type };
    current.value += row.received + row.sent;
    current.count += 1;
    if (aggregateKey === 'entity') current.type = row.group;
    aggregated.set(name, current);
  });
  return [...aggregated.values()].sort((a, b) => b.value - a.value);
}
```

```js
function renderEntityMap(widget) {
  const focused = widget === 'entityMapFocus';
  const chart = byId(focused ? 'entity-map-focus-chart' : 'entity-map-chart');
  const detail = byId(focused ? 'entity-map-focus-detail' : 'entity-map-detail');
  const groups = entityMapItems(widget);
  const total = sum(groups.map(item => item.value));
  const selected = state[widget].selected;
  chart.innerHTML = groups.map(item => {
    const color = entityGroupColors[item.name] || (item.name === 'ByBit' ? '#a5d5a9' : item.name === 'Private' ? '#f4d9ad' : '#d5e5d6');
    const share = total ? item.value / total * 100 : 0;
    const label = state[widget].view === 'type' ? item.name : `${item.name} · ${item.type}`;
    return `<button type="button" class="entity-treemap-segment${selected === item.name ? ' is-selected' : ''}" style="--segment-color:${color};--segment-value:${item.value}" data-map-segment="${widget}" data-map-label="${item.name}" aria-pressed="${selected === item.name}" aria-label="${label}: ${share.toFixed(1)} percent, ${entityMoney(item.value)}, ${item.count} connections" title="${label} · ${share.toFixed(1)}% · ${entityMoney(item.value)}"><span>${item.name}</span></button>`;
  }).join('');
  chart.setAttribute('aria-label', `Connection volume by ${state[widget].view === 'type' ? 'entity type' : 'entity'}: ${groups.map(item => `${item.name} ${entityMoney(item.value)}`).join('; ')}.`);
  const item = groups.find(entry => entry.name === selected);
  detail.hidden = !item;
  if (item) {
    const share = item.value / total * 100;
    detail.innerHTML = `<div><strong>${share.toFixed(1)}%</strong><span>${item.name}</span>${state[widget].showValues ? `<small>${entityMoney(item.value)} · ${item.count} connections</small>` : ''}</div><button type="button" data-view-connections="${widget}" data-map-label="${item.name}">View connections <span aria-hidden="true">›</span></button>`;
  }
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

// rows = [{ type: 'Fornecedores', entity: 'Papelaria Central Ltda', received: '0.00', sent: '12500.00', connections: 7 }, …]
loadWidget('entityMap', rows => {
  data.entityConnections = rows.map(row => ({
    entity: row.entity, type: row.type, group: row.type,
    received: Number(row.received) || 0, sent: Number(row.sent) || 0,
    date: row.last_date ?? '', direct: Boolean(row.direct ?? true),
  }));
  // entityGroupColors é um mapa fixo por nome: na cópia de produção gere as cores a partir dos tipos recebidos.
  ['entityMapFocus', 'entityTable', 'entityTableFiltered'].forEach(renderWidget);   // os quatro cards compartilham a lista
});
```

O menu “Download CSV” chama `downloadCsv('entityMap')`, que serializa a **série de amostra** (`entityMap-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Volume por contraparte e categoria nos últimos 90 dias: créditos (`type = 'credit'`) como recebido e débitos como enviado, ignorando estornos/falhas. Testado no MariaDB local.

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

A mesma resposta alimenta o mapa e a tabela. Agrupe por `category` para a visão “Entity types” e por `counterparty_name` para “Entities”; o JS já faz as duas agregações a partir das linhas.

## Faça / Não faça

- **Faça:** manter mapa e tabela com a mesma fonte (o atalho “View connections” depende disso);
- **Faça:** mostrar o nome no segmento.
- **Não faça:** deixar o diálogo de configurações sem botão de abertura;
- **Não faça:** usar cores como única identificação do grupo.
