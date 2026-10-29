# WidgetConversionRate

Card “Conversion rate”: rosca SVG com a distribuição de itens por etapa (concluído, em andamento, a fazer), legenda e três chamadas de percentual.

> **Sobre o preview.** O card carrega o catálogo inteiro de `docs/model/widgets` (`vendor/app/widgets/widgets.{css,js}`, cópia idêntica do repositório) porque o `widgets.js` monta e atualiza todos os widgets de uma vez; um script no fim do preview marca os demais elementos com `data-ds-hidden` e deixa visível só o card `conversion`. Os números são **ilustrativos** (objeto `data` de `widgets.js`) e os rótulos ficam em inglês, como na referência aprovada.

## Quando usar

- Mostrar a distribuição atual de um funil curto: solicitações de matrícula (`enrollment_requests`) concluídas × em análise × pendentes, em 30 ou 90 dias.
- Exatamente três etapas que somam 100%.
- Para evolução mensal de conversões use [WidgetMonthlyConversions](../WidgetMonthlyConversions/README.md); para o funil completo com cartões, o Kanban ([KanbanBoard](../KanbanBoard/README.md)).

## Anatomia

```
┌        ícone · Conversion rate (i)    [ajustes] [⋯] ┐   (cabeçalho centralizado)
│   ● Delivered  ● In progress  ● To-do                │  #conversion-legend
│  35% ◜‾‾‾◝ 48%                                       │  svg#conversion-chart (240×240)
│      ◟___◞   17%                                     │  .conversion-callout × 3
│ Distribution of tracked work items   100% · sample   │
└──────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Cabeçalho | `header.ttsc-analytics-head.widget-head.centered-widget-head` | sim |
| Legenda | `div.conversion-legend#conversion-legend` | não (configurável) |
| Rosca | `.conversion-chart-wrap` > `svg#conversion-chart.conversion-chart[role="img"]` (uma `<path>` por etapa) | sim |
| Chamadas | `.conversion-callout.callout-delivered\|-progress\|-todo` com `#conversion-delivered`, `#conversion-in-progress`, `#conversion-to-do` | sim |
| Rodapé | `#conversion-total`, `#conversion-period-label` | sim |
| Configurações | `dialog#settings-conversion` | sim |

## Estados

| Estado | Como aparece / como aplicar |
|---|---|
| Padrão | Renderizado por `renderWidget('conversion')` quando o card entra na viewport (`IntersectionObserver`, margem 420px). |
| Carregando | Provider: `aria-busy="true"` no `<article>` + bloco `.ttsc-analytics-empty[data-widget-state="loading"]` (ver JS). |
| Vazio | `.ttsc-analytics-empty[data-widget-state="empty"]` com título e explicação; o plot fica `hidden`. |
| Erro | `.ttsc-analytics-empty[data-widget-state="error"]` com `role="alert"` e texto `.ttsc-analytics-error`. Se o Chart.js não carregar, o próprio `widgets.js` troca o canvas por “Charts could not load”. |
| Configurado | Após “Apply settings” o diálogo grava em `state.conversion` e re-renderiza só este widget; o toast `#widget-toast` confirma. |
| Filtrado | Gaveta “Filter”: marcas fora da busca/faixa recebem `.widget-filtered-out`; o botão mostra um contador `<b>`. |
| Sem legenda | `state.conversion.showLegend = false` → `#conversion-legend[hidden]`. |

## API

### Dados esperados

Duas listas (`month`, `quarter`) com três etapas cada; os ids das chamadas são derivados do `label` (`conversion-${label.toLowerCase().replaceAll(" ", "-")}`), então **mantenha os três rótulos ou renomeie os ids juntos**.

| Campo | Tipo | Unidade / formato | Significado |
|---|---|---|---|
| `label` | `string` | texto | `Delivered`, `In progress`, `To-do` (definem os ids das chamadas). |
| `value` | `number` | % inteiro | Fatia da rosca; as três somam 100. |
| `color` | `string` | hex | Cor da fatia e da legenda. |

Trecho real do objeto de amostra em `widgets.js` (é ele que o provider substitui):

```js
conversion: {
  month: [{ label: 'Delivered', value: 35, color: '#7653f9' }, { label: 'In progress', value: 48, color: '#ff8a70' }, { label: 'To-do', value: 17, color: '#267eea' }],
  quarter: [{ label: 'Delivered', value: 42, color: '#7653f9' }, { label: 'In progress', value: 39, color: '#ff8a70' }, { label: 'To-do', value: 19, color: '#267eea' }]
}
```

### Configurações do widget

Padrão em `state.conversion`: `{ period: 'month', showLegend: true }`.

| Chave (`data-key`) | Controle | Valores | Rótulo no diálogo | Efeito |
|---|---|---|---|---|
| `period` | select | `month` (Last 30 days) · `quarter` (Last 90 days) | Reporting period | `month` = 30 dias, `quarter` = 90 dias. |
| `showLegend` | input checkbox | booleano | Show stage legend | Mostra/esconde a legenda superior. |

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
| `renderConversion()` | Monta as fatias, legenda, textos das chamadas e `aria-label`. |
| `donutSlicePath(start, end)` | Caminho SVG de um setor (raio externo 82, interno 48, centro 120,120). |
| `renderWidget(widget)` | Despacha para o render certo (tabela `renderers`) e reaplica um filtro ativo. |
| `downloadCsv(widget)` | Gera o CSV da série atual do widget e mostra o toast. |
| `toast(message)` | Mensagem curta em `#widget-toast` por 2,8 s. |
| `submit` do `<form method="dialog">` | `submitter.value === "save"` grava os campos `[data-setting]` em `state` e re-renderiza; `cancel` só fecha. |
| `click #theme-toggle` | Alterna `html[data-theme]`; atualiza cores de eixo/grade das instâncias Chart.js (`tone()`). No app, `TTSCModelKit.syncTheme()` mantém `html.dark` e `data-theme` iguais. |

### Endpoints

- **Pronto:** `GET /api/v1/domain/records/commercial/enrollment?per_page=100` (view `inst_enr_requests`: `status`, `submitted_at`, `confirmed_at`…). Bom para listar; o percentual deve vir agregado.
- **Recomendado:** provider do módulo comercial/secretaria com a consulta abaixo (`?days=30|90`), com a permissão da página `/commercial/enrollment`.

## Acessibilidade

- A rosca tem `aria-label` “Conversion stages: Delivered 35%, …”; os percentuais também estão em texto nas chamadas.
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
$endpoint = '/api/v1/domain/records/commercial/enrollment?per_page=100';
?>
<!-- O <article> abaixo é copiado de docs/model/widgets/index.html; só data-endpoint é acrescentado -->
<article class="ttsc-analytics-card widget demo-widget" data-widget="conversion"
         data-endpoint="<?= $e($endpoint) ?>" aria-labelledby="conversion-title">
  …
</article>
```

**2. Marcação real** (`docs/model/widgets/index.html`, com o diálogo de configurações dentro do card; SVG de ícones abreviados com `…`):

```html
<article class="ttsc-analytics-card widget demo-widget activity-widget" data-widget="conversion" aria-labelledby="conversion-title">
  <header class="ttsc-analytics-head widget-head centered-widget-head">
    <div class="widget-heading">
      <span class="widget-icon tone-purple" aria-hidden="true"><svg viewBox="0 0 20 20">…</svg></span>
      <div>
        <div class="title-line">
          <h2 id="conversion-title">Conversion rate</h2>
          <button class="info-button" type="button" data-tip="Share of tracked work items in each delivery stage for the selected reporting period." aria-label="About conversion rate">
            i
          </button>
        </div>
        <p id="conversion-period-label">Delivered, in progress and to-do</p>
      </div>
    </div>
    <div class="widget-actions">
      <button class="widget-config" type="button" data-open-settings="conversion" aria-label="Adjust conversion rate chart">
        <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
      </button>
      <div class="widget-menu-wrap">
        <button class="widget-more" type="button" aria-label="More conversion rate actions" aria-expanded="false" data-menu="conversion">
          <svg viewBox="0 0 20 20" aria-hidden="true">…</svg>
        </button>
        <div class="widget-menu" hidden>
          <button type="button" data-download="conversion">Download CSV</button>
          <button type="button" data-reset="conversion">Reset widget</button>
        </div>
      </div>
    </div>
  </header>
  <div class="conversion-legend" id="conversion-legend"></div>
  <div class="conversion-chart-wrap">
    <svg id="conversion-chart" class="conversion-chart" viewBox="0 0 240 240" role="img" aria-label="Delivery stage distribution"></svg>
    <div class="conversion-callout callout-delivered" id="conversion-delivered"></div>
    <!-- … +2 elemento(s) iguais gerados pelo JS -->
  </div>
  <footer class="ttsc-analytics-foot widget-foot">
    <span>Distribution of tracked work items</span>
    <span id="conversion-total">100% · sample</span>
  </footer>
  <dialog class="widget-settings" id="settings-conversion" aria-labelledby="settings-conversion-title">
    <form method="dialog">
      <header>
        <div>
          <span class="settings-icon"><svg viewBox="0 0 20 20" aria-hidden="true">…</svg></span>
          <div>
            <h3 id="settings-conversion-title">Conversion rate settings</h3>
            <p>Settings apply to this widget only.</p>
          </div>
          <button class="dialog-close" value="cancel" aria-label="Close settings">×</button>
        </div>
      </header>
      <div class="settings-body">
        <label class="settings-field">
          Reporting period
          <select data-setting="conversion" data-key="period">
            <option value="month" selected>Last 30 days</option>
            <option value="quarter">Last 90 days</option>
          </select>
        </label>
        <label class="settings-check">
          <input type="checkbox" data-setting="conversion" data-key="showLegend" checked>
          Show stage legend
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
.centered-widget-head { position: relative; justify-content: center; }
.centered-widget-head .widget-heading { justify-content: center; }
.centered-widget-head .widget-actions { position: absolute; top: 0; right: 0; }
.conversion-legend { display: flex; justify-content: center; flex-wrap: wrap; gap: 16px; margin: 2px 0 3px; color: var(--w-secondary); font-size: 11px; }
.conversion-legend[hidden] { display: none; }
.conversion-legend span { display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; }
.conversion-legend i { width: 8px; height: 8px; border-radius: 50%; background: var(--series-color); }
.conversion-chart { display: block; width: 100%; height: 100%; overflow: visible; }
.conversion-callout { position: absolute; display: inline-flex; min-width: 55px; min-height: 32px; align-items: center; justify-content: center; gap: 5px; padding: 0 9px; border: 1px solid #f1f5f9; border-radius: 9px; background: var(--w-surface); /* … */ }
.conversion-callout::before { width: 7px; height: 7px; border-radius: 50%; background: var(--callout-color); content: ""; }
.callout-delivered { top: 18%; right: 9%; --callout-color: #7653f9; }
.callout-progress { bottom: 18%; left: 8%; --callout-color: #ff8a70; }
.callout-todo { right: 6%; bottom: 20%; --callout-color: #267eea; }
```

Customização legítima (por variável, sem tocar nas classes):

```css
/* Etapas com a semântica do produto (as cores das fatias vêm de `color` no dado) */
[data-widget="conversion"] .conversion-callout { font-variant-numeric: tabular-nums; }
[data-widget="conversion"] .conversion-legend i { border-radius: var(--ttsc-radius-xs); }
```

### JS

Render real em `widgets.js` (`tipAttrs()` devolve `tabindex="0" data-tip="…" aria-label="…"` para a marca abrir o tooltip comum em hover e foco):

```js
function donutSlicePath(startAngle, endAngle) {
  const cx = 120, cy = 120, outer = 82, inner = 48;
  const point = (radius, angle) => {
    const radians = (angle - 90) * Math.PI / 180;
    return [cx + radius * Math.cos(radians), cy + radius * Math.sin(radians)];
  };
  const [x1, y1] = point(outer, startAngle);
  const [x2, y2] = point(outer, endAngle);
  const [x3, y3] = point(inner, endAngle);
  const [x4, y4] = point(inner, startAngle);
  const large = endAngle - startAngle > 180 ? 1 : 0;
  return `M ${x1.toFixed(2)} ${y1.toFixed(2)} A ${outer} ${outer} 0 ${large} 1 ${x2.toFixed(2)} ${y2.toFixed(2)} L ${x3.toFixed(2)} ${y3.toFixed(2)} A ${inner} ${inner} 0 ${large} 0 ${x4.toFixed(2)} ${y4.toFixed(2)} Z`;
}
```

```js
function renderConversion() {
  const rows = data.conversion[state.conversion.period];
  const total = sum(rows.map(row => row.value));
  let angle = 0;
  const slices = rows.map(row => {
    const sweep = row.value / total * 360;
    const path = donutSlicePath(angle + 1, angle + sweep - 1);
    angle += sweep;
    return `<path class="conversion-slice" role="img" ${tipAttrs(`${row.label}: ${row.value}% of tracked work items`)} d="${path}" fill="${row.color}"/>`;
  }).join('');
  byId('conversion-chart').innerHTML = slices;
  byId('conversion-chart').setAttribute('aria-label', `Conversion stages: ${rows.map(row => `${row.label} ${row.value}%`).join(', ')}.`);
  byId('conversion-legend').hidden = !state.conversion.showLegend;
  byId('conversion-legend').innerHTML = rows.map(row => `<span class="conversion-legend-item" ${tipAttrs(`${row.label}: ${row.value}% of tracked work items`)}><i style="--series-color:${row.color}"></i>${row.label}</span>`).join('');
  rows.forEach(row => { byId(`conversion-${row.label.toLowerCase().replaceAll(' ', '-')}`).textContent = `${row.value}%`; });
  byId('conversion-period-label').textContent = state.conversion.period === 'quarter' ? 'Last 90 days' : 'Last 30 days';
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

// rows = [{ stage: 'Concluídas', total: 35, percent: 35 }, { stage: 'Em andamento', … }, { stage: 'A fazer', … }]
const STAGES = [['Concluídas', 'Delivered', '#7653f9'], ['Em andamento', 'In progress', '#ff8a70'], ['A fazer', 'To-do', '#267eea']];
async function loadConversion() {
  const base = widgetCard('conversion').dataset.endpoint;
  const lists = await Promise.all([30, 90].map(days => fetch(`${base}?days=${days}`, { credentials: 'same-origin' }).then(r => r.json())));
  const map = payload => STAGES.map(([stage, label, color]) => ({ label, color, value: Number((payload.rows ?? []).find(r => r.stage === stage)?.percent) || 0 }));
  data.conversion = { month: map(lists[0]), quarter: map(lists[1]) };   // label mantém os ids #conversion-delivered…
  renderWidget('conversion');
}
```

O menu “Download CSV” chama `downloadCsv('conversion')`, que serializa a **série de amostra** (`conversion-widget-sample.csv`). Em produção, troque o item por um link para a exportação real da mesma consulta, com os mesmos filtros/configurações do card (no CRUD genérico: `GET /api/v1/domain/records{rota}/export?format=csv`, `DomainCrudController::export`, formatos de `TableExporter::FORMATS`: `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`).

### SQL

Distribuição das solicitações de matrícula não canceladas/rejeitadas/expiradas criadas nos últimos `:days` dias, agrupadas em três etapas a partir dos status reais (`Approved`, `Confirmed`, `Submitted`, `Pending Review`, `Draft` — ver `ref_enum_enrollment_requests_status_*`). Testado no MariaDB local.

```sql
-- Funil de solicitações de matrícula: concluídas / em andamento / a fazer (percentual)
SELECT stage, total, ROUND(total / SUM(total) OVER () * 100, 0) AS percent
  FROM (
        SELECT CASE
                 WHEN r.status IN ('approved', 'confirmed')        THEN 'Concluídas'
                 WHEN r.status IN ('submitted', 'pending review')  THEN 'Em andamento'
                 ELSE 'A fazer'
               END AS stage,
               COUNT(*) AS total
          FROM enrollment_requests r
         WHERE r.deleted_at IS NULL
           AND r.status NOT IN ('cancelled', 'rejected', 'expired')
           AND r.created_at >= CURDATE() - INTERVAL :days DAY        -- :days = 30 | 90
         GROUP BY 1
       ) s
 ORDER BY FIELD(stage, 'Concluídas', 'Em andamento', 'A fazer');
```

`SUM(total) OVER ()` calcula o total sem segunda consulta. Arredondamentos podem somar 99 ou 101: ajuste a maior fatia no provider para fechar 100.

## Faça / Não faça

- **Faça:** manter três etapas e percentuais que somam 100;
- **Faça:** traduzir os rótulos exibidos sem quebrar os ids das chamadas.
- **Não faça:** usar a rosca para mais de três etapas;
- **Não faça:** mostrar contagens absolutas como se fossem percentuais.
