# WidgetTimeByCategory

Card “Time by category”: média diária de horas por categoria em barras horizontais proporcionais (roxas), com a duração em “Xh YYm”.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só o card `activity`. Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Mostrar uso de tempo por categoria: horas reservadas por tipo de sala da biblioteca (`lib_room_bookings`), carga de atendimento, horas por atividade.
- Comparar categorias entre si (barras horizontais, rótulo à esquerda), em 7 ou 30 dias.
- Para dinheiro por categoria contra limite use [WidgetCategoryLimit](../WidgetCategoryLimit/README.md); para evolução no tempo, [WidgetMonthlyConversions](../WidgetMonthlyConversions/README.md).

## Anatomia

```
┌ ícone · Time by category (i) ───────── [ajustes] [⋯] ┐
│ Daily average across the selected period             │
│ Entertainment 6h 37m  ████████████████████           │  #activity-bars > .activity-bar-row
│ CPU           3h 46m  ███████████                    │
│ Productivity  1h 45m  █████                          │
│ Tracked categories               Last 7 days · sample│
└──────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Card | `article…activity-widget[data-widget="activity"]` | sim |
| Descrição | `p.activity-description` | não |
| Barras | `div.activity-bars#activity-bars` > `.activity-bar-row[role="img"]` (`.activity-bar-label` + `.activity-track > span`) | sim |
| Rodapé | `#activity-period-label` | sim |
| Configurações | `dialog#settings-activity` | sim |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('activity')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Após “Apply settings” o diálogo grava em `state.activity` e re-renderiza só este widget; o toast `#widget-toast` confirma. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Sem duração | `state.activity.showTime = false` esconde o “Xh YYm” (a barra continua com `aria-label` completo). |

## API

### Dados esperados

Um objeto com duas listas (`week`, `month`) de categorias com horas médias por dia; a maior vira 100% da largura.

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `name` | `string` | texto | Categoria. |
| `hours` | `number` | horas decimais/dia | Formatada por `durationLabel()` como `6h 37m`. |
| chave do período | `week` \| `month` | — | Seleciona a lista pelo `state.activity.period`. |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js
activity: {
  week: [
    { name: 'CPU', hours: 3 + 46 / 60 },
    { name: 'Entertainment', hours: 6 + 37 / 60 },
    { name: 'Productivity', hours: 1 + 45 / 60 },
    { name: 'Games', hours: 3 + 24 / 60 },
    { name: 'Social Media', hours: 2 + 10 / 60 }
  ],
  month: [
    { name: 'CPU', hours: 3 + 32 / 60 },
    { name: 'Entertainment', hours: 6 + 18 / 60 },
    { name: 'Productivity', hours: 1 + 54 / 60 },
    { name: 'Games', hours: 3 + 8 / 60 },
    { name: 'Social Media', hours: 2 + 24 / 60 }
  ]
}
```

### Configurações do widget

Padrão em `state.activity`: `{ period: 'week', showTime: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `period` | select | `week` (Last 7 days) · `month` (Last 30 days) | Reporting period | `week` = 7 dias, `month` = 30 dias. |
| `showTime` | input checkbox | booleano | Show time totals | Mostra a duração ao lado do nome. |

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
| `renderActivity()` | Gera as linhas proporcionais ao máximo e o rótulo do período. |
| `durationLabel(hours)` | Converte horas decimais em `Xh YYm`. |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- Não há rota de domínio que agregue horas por categoria. Exponha a consulta abaixo num provider do módulo da biblioteca, com a permissão da página de reservas de sala, e devolva `{ "week": [...], "month": [...] }` ou uma lista por chamada (`?days=7|30`).

## Acessibilidade

- Cada linha é `role="img"` com `aria-label` “Categoria: Xh YYm”, mesmo quando a duração está escondida.
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
$endpoint = '/library/rooms/bookings/widgets/time-by-category' /* rota do provider do módulo, a criar */;
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="activity"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="activity-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget activity-widget" data-widget="activity" aria-labelledby="activity-title">
  <header class="ttsc-analytics-head widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-purple" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="activity-title">Time by category</h2>
          <button class="info-button" type="button" data-tip="Tracked device time grouped by activity category for the selected period." aria-label="About time by category">
            i
          </button>
        </div>
        <p>Tracked screen time by category</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="activity" aria-label="Adjust time by category">
        <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" aria-label="More time by category actions" aria-expanded="false" data-menu="activity">
          <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="activity">Download CSV</button>
          <button type="button" data-reset="activity">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <p class="activity-description">Daily average across the selected period</p>
  <div class="activity-bars" id="activity-bars" aria-label="Tracked time by category"></div>
  <footer class="ttsc-analytics-foot widget-foot">
    <span>Tracked categories</span>
    <span id="activity-period-label">Last 7 days · sample</span>
  </footer>
  <dialog class="widget-settings" id="settings-activity" aria-labelledby="settings-activity-title">
    <form method="dialog">
      <header>
        <div>
          <span class="settings-icon"><svg viewBox="0 0 20 20" aria-hidden="true">…</svg></span>
          <div>
            <h3 id="settings-activity-title">Time by category settings</h3>
            <p>Settings apply to this widget only.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close settings">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Reporting period
          <select data-setting="activity" data-key="period">
            <option value="week" selected>Last 7 days</option>
            <option value="month">Last 30 days</option>
          </select>
        </label>
        <label class="settings-check">
          <input type="checkbox" data-setting="activity" data-key="showTime" checked>
          Show time totals
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
.activity-widgets-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); margin-top: 16px; }
.activity-widget { min-width: 0; }
.activity-description { margin: -5px 0 18px; color: var(--w-muted); font-size: 11px; }
.activity-bars { display: grid; gap: 15px; padding: 10px 0 6px; }
.activity-bar-row { min-width: 0; }
.activity-bar-label { display: flex; min-width: 0; align-items: center; gap: 8px; margin-bottom: 5px; color: var(--w-text); font-size: 12px; }
.activity-bar-label strong { overflow: hidden; font-weight: 600; text-overflow: ellipsis; white-space: nowrap; }
.activity-bar-label span { color: #7653f9; font-weight: 650; font-variant-numeric: tabular-nums; white-space: nowrap; }
.activity-track { height: 8px; overflow: hidden; border-radius: 999px; background: #eeeaff; }
.activity-track span { display: block; height: 100%; border-radius: inherit; background: #7653f9; transition: width .3s ease; }
.activity-widget .widget-foot { margin-top: 14px; }
.activity-bar-plot.ttsc-analytics-plot { height: 245px; margin-top: 9px; }
.activity-widgets-grid { grid-template-columns: minmax(0, 1fr); }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Barras na cor da marca em vez do roxo do modelo */
[data-widget="activity"] .activity-track span { background: var(--ttsc-accent); }
```

### JS

Render real em `widgets.js`:

```js
function durationLabel(hours) {
  const minutes = Math.round(hours * 60);
  return `${Math.floor(minutes / 60)}h ${String(minutes % 60).padStart(2, '0')}m`;
}
```

```js
function renderActivity() {
  const values = data.activity[state.activity.period].map(item => ({ ...item, total: item.hours }));
  const max = Math.max(...values.map(item => item.total), 1);
  byId('activity-bars').innerHTML = values.map(item => `<div class="activity-bar-row" role="img" aria-label="${item.name}: ${durationLabel(item.total)}"><div class="activity-bar-label"><strong>${item.name}</strong>${state.activity.showTime ? `<span>${durationLabel(item.total)}</span>` : ''}</div><div class="activity-track"><span style="width:${(item.total / max * 100).toFixed(1)}%"></span></div></div>`).join('');
  byId('activity-period-label').textContent = `${state.activity.period === 'month' ? 'Last 30 days' : 'Last 7 days'} · sample`;
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

// rows = [{ category: 'Estudo em grupo', hours_per_day: '3.77', bookings: 41 }, …]  (consulta com :days = 7 e 30)
const card = widgetCard('activity');
const base = card.dataset.endpoint;
Promise.all([7, 30].map(days => fetch(`${base}?days=${days}`, { credentials: 'same-origin', headers: { Accept: 'application/json' } }).then(r => r.ok ? r.json() : Promise.reject(r.status))))
  .then(([week, month]) => {
    const map = rows => (rows.rows ?? rows.records ?? []).map(row => ({ name: row.category, hours: Number(row.hours_per_day) || 0 }));
    data.activity = { week: map(week), month: map(month) };
    if (!data.activity.week.length && !data.activity.month.length) return widgetState(card, 'empty', 'Sem reservas', 'Nenhuma reserva de sala no período.');
    widgetState(card, 'ready');
    renderWidget('activity');
  })
  .catch(() => widgetState(card, 'error', 'Não foi possível carregar', 'Tente novamente em instantes.'));
```

O menu “Download CSV” chama `downloadCsv('activity')`, que serializa a **série de amostra** (`activity-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Média diária de horas reservadas por tipo de sala (`lib_room_bookings.duration_minutes` + `lib_rooms.room_type`), excluindo canceladas e registros apagados. Testado no MariaDB local com `:days` = 30.

```sql
-- Média diária de horas reservadas por tipo de sala (biblioteca), últimos :days dias
SELECT r.room_type                                   AS category,
       ROUND(SUM(b.duration_minutes) / 60 / :days, 2) AS hours_per_day,
       COUNT(*)                                      AS bookings
  FROM lib_room_bookings b
  JOIN lib_rooms r ON r.id = b.room_id AND r.deleted_at IS NULL
 WHERE b.deleted_at IS NULL
   AND b.status <> 'cancelled'
   AND b.booking_date >= CURDATE() - INTERVAL :days DAY          -- :days = 7 | 30
 GROUP BY r.room_type
 ORDER BY hours_per_day DESC;
```

Rode duas vezes (7 e 30) ou devolva as duas listas numa resposta. O `room_type` é chave técnica: traduza para o rótulo antes de enviar (o card mostra o texto como está).

## Faça / Não faça

- **Faça:** ordenar da maior para a menor;
- **Faça:** manter a unidade “por dia” explícita no texto do card.
- **Não faça:** misturar horas totais e médias diárias entre as duas listas;
- **Não faça:** usar mais de 6 categorias (o card não rola).
