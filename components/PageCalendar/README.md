# PageCalendar

Arquétipo de página de agenda: cabeçalho e banner do chassi seguidos de um FullCalendar 6.1.20 (mês, semana, lista) com os eventos da tabela `events` coloridos por tipo e um drawer de detalhe ao clicar.

## Quando usar

- Páginas cujo assunto é **quando** as coisas acontecem: calendário escolar, eventos, agenda pastoral, reservas de espaço, reuniões. A sidebar tem ≈ 33 rotas assim (`/academic/calendar`, `/academic/events/calendar`, `/academic/spaces/calendar`, `/academic/pastoral/schedule`, `/student/events/calendar`, `/parents/events/calendar`, `/teacher/events/calendar`, `/meetings/calendar`…).
- Cadastrar e listar os calendários letivos em si (código, ano, dias letivos) é Records: `/academic/settings/calendar`.
- Escolher uma data num formulário: [DatePicker](../DatePicker/README.md). Histórico de ações: [Timeline](../Timeline/README.md).

### Regra de escolha (resumo)

Dashboard = home de módulo/portal · Records = lista de entidade (o padrão) · Pipeline = itens que andam por etapas reais · History = histórico/auditoria somente leitura · Report = relatórios, gráficos primeiro · Settings = configurações · **Calendar = datas e períodos no tempo**. Mapa completo de abas e ações em [PageRecords](../PageRecords/README.md).

### Situação no repositório

Nenhuma view em `resources/views` usa FullCalendar hoje. As rotas de calendário são páginas `domain_page.php` (tabela/cards/KPI) sobre fontes curadas: `/academic/calendar` → `inst_academic_calendars`, `/academic/events/calendar` → `inst_events_upcoming` (view sobre `events` + `units`, eventos com `start_date >= CURDATE()`). O bundle `assets/vendors/fullcalendar/index.global.min.js` (v6.1.20) está no repo, mas foi corrompido pelo replace `kt` → `ttsc` (há uma função renomeada para `ttsc(e, t)`) e não carrega; o preview usa a cópia original do npm em `vendor/fullcalendar/`. Esta página é o modelo para quando as rotas de calendário ganharem a visão de agenda.

## Anatomia

```
PageHeader "Calendário Escolar" (fa-calendar-days)        [Atualizar]
ContextBanner "Ano letivo 2026" ( ● 10 eventos em outubro )
┌ .ttsc-fc ────────────────────────────────────────────────────────────┐
│ ■ Acadêmico ■ Administrativo ■ Cultural ■ Cerimônia ■ Feriado        │ .fc-legend
│ [Anterior|Próximo] [Hoje]      Outubro de 2026      [Mês|Semana|Lista]│ .fc-header-toolbar
│ DOM. SEG. TER. QUA. QUI. SEX. SÁB.                                   │ .fc-col-header
│ … 21 (hoje) [19:00 Reunião de pais] …                                │ .fc-daygrid-event.ev-type.ev-<tipo>
└──────────────────────────────────────────────────────────────────────┘
drawer #drawer-event: título, data/hora, Tipo, Local, Público, Status
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Cabeçalho / banner | `TTSCModelKit.blocks.header` / `.banner` (ou `chassis.php`) | sim |
| Wrapper de tema | `div.ttsc-fc` com variáveis `--fc-*` ligadas aos tokens | sim |
| Legenda | `.fc-legend > span.ev-<tipo>` | sim |
| Alvo | `div#academic-calendar` | sim |
| Evento | `classNames: ['ev-type', 'ev-<type>']` (tipos de `ref_enum_events_type_*`) | sim |
| Drawer de detalhe | `.drawer-panel#drawer-event` aberto por `openDrawer` | recomendado |

## Variantes

| Visão | `initialView` / botão | Uso |
|---|---|---|
| Mês | `dayGridMonth` | padrão; `dayMaxEvents: 2` + "+ N eventos" |
| Semana | `timeGridWeek` | horários (`slotMinTime 07:00`, `slotMaxTime 23:00`) |
| Lista | `listMonth` | leitura linear, melhor em telas estreitas e leitores de tela |

| Tipo (`events.type`) | Classe | Cor (token) |
|---|---|---|
| `academic` | `ev-academic` | `--ttsc-info` |
| `administrative` | `ev-administrative` | `--ttsc-warning` |
| `cultural` | `ev-cultural` | `--ttsc-meta` |
| `ceremony` | `ev-ceremony` | `--ttsc-accent` |
| `holiday` | `ev-holiday` | `--ttsc-danger` |
| `sports`, `workshop`, `other` | `ev-<tipo>` | defina no mesmo padrão |

## API

**FullCalendar (`new FullCalendar.Calendar(el, options)`) — opções usadas**

| Opção | Valor |
|---|---|
| `locale` + `buttonText`, `allDayText`, `noEventsText`, `moreLinkText` | `'pt-br'` e rótulos em português (o bundle global não traz o locale) |
| `firstDay` | `0` (domingo) |
| `headerToolbar` | `{ left: 'prev,next today', center: 'title', right: 'dayGridMonth,timeGridWeek,listMonth' }` |
| `height`, `dayMaxEvents`, `nowIndicator`, `navLinks` | `'auto'`, `2`, `true`, `true` |
| `eventTimeFormat`, `slotLabelFormat` | 24 h (`hour12: false`) |
| `events` | array, ou função/URL que lê o endpoint (abaixo) |
| `eventDidMount` | `title` + `tabindex="0"` + `Enter` abre |
| `eventClick` | preenche e abre o drawer (`window.openDrawer('drawer-event')`) |

| Instância | Uso |
|---|---|
| `calendar.render()`, `.refetchEvents()`, `.changeView(v)`, `.gotoDate(d)`, `.getEventById(id)` | ciclo de vida |

**Mapeamento `events` → evento do FullCalendar**

| Coluna | Evento |
|---|---|
| `uuid` | `id` |
| `title` | `title` |
| `start_date` + `start_time` | `start` (sem hora → `allDay: true`) |
| `end_date` + `end_time` | `end` (dia inteiro: `end_date + 1 dia`, fim exclusivo) |
| `type` | `classNames` |
| `location`, `target_audience`, `status`, `unit_name` | `extendedProps` → drawer |

**Endpoints**

| Método | Rota | Uso |
|---|---|---|
| GET | `/api/v1/domain/records/academic/events/calendar?page=1&per_page=100` | eventos futuros (`inst_events_upcoming`) |
| GET | `/api/v1/domain/records/academic/events/calendar/{id}` | detalhe do drawer |
| GET | `/api/v1/domain/records/academic/events/calendar/export?format=csv\|pdf` | exportar agenda |
| GET | `/api/v1/kpi/academic/events/calendar` | contagens do banner |

A fonte é `writable => false`: criar/editar evento acontece em `/academic/events/list` (Records).

## Acessibilidade

- Eventos focáveis (`tabindex="0"`) e acionáveis com `Enter`; `title` com o nome completo (o mês trunca).
- A visão **Lista** é a alternativa linear; ofereça-a sempre no `headerToolbar`.
- Cor de tipo nunca sozinha: legenda com nome e título do evento em texto (`--ttsc-text` sobre fundo do tipo a 14–22%).
- O drawer de detalhe é `role="dialog"` com foco preso e `Esc` (via `openDrawer`).

## Modelos

### HTML

1) PHP real — hoje a rota é um shim do chassi sobre a fonte curada; a agenda entra como painel extra da página:

```php
<?php
// resources/views/app/pages/client/academic/events/calendar.php (gerado)
$pageRoute = '/academic/events/calendar';
$pageRail = 'client';
$title = 'Espaço de Trabalho — Calendário de Eventos';
$icon = 'fa-light fa-calendar-days';
// … $breadcrumb, $this->layout('app::layouts/main', […]) …
include base_path('resources/views/app/partials/chassis/domain_page.php');

// app/Config/page-domain-sources.php
'/academic/events/calendar' => [
    'source' => 'inst_events_upcoming', 'permission' => 'admin.academic.view', 'scope' => 'database', 'writable' => false,
    'statuses' => ['scheduled' => 'Scheduled', 'confirmed' => 'Confirmed', 'postponed' => 'Postponed', 'cancelled' => 'Cancelled', 'completed' => 'Done'],
    'columns' => ['title' => 'Event', 'type' => 'Type', 'start_date' => 'Start', 'end_date' => 'End', 'location' => 'Location',
                  'target_audience' => 'Public', 'unit_name' => 'Unit', 'status' => 'Status'],
    'search' => ['title', 'location'],
],
```

Painel de agenda (a incluir no lugar da aba KPI, com o bundle original — não o de `assets/vendors`, que está corrompido):

```php
<script nonce="<?= $nonce ?>" src="<?= asset('vendors/fullcalendar/index.global.min.js') ?>"></script>
<div class="ttsc-fc">
  <div class="fc-legend" aria-label="Tipos de evento">
    <span class="ev-academic">Acadêmico</span><span class="ev-administrative">Administrativo</span>
    <span class="ev-cultural">Cultural</span><span class="ev-ceremony">Cerimônia</span><span class="ev-holiday">Feriado / recesso</span>
  </div>
  <div id="academic-calendar" data-events-url="<?= url('/api/v1/domain/records/academic/events/calendar') ?>"></div>
</div>
```

2) HTML gerado (preview; FullCalendar renderiza o resto):

```html
<div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
  <div class="flex items-start space-x-3.5">
    <div class="w-11 h-11 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center shrink-0"><i class="fa-light fa-calendar-days text-emerald-600 text-lg"></i></div>
    <div><h1 class="text-xl font-bold text-slate-900 tracking-tight">Calendário Escolar</h1>
      <div class="flex items-center space-x-2 text-xs text-slate-400 mt-0.5"><i class="fa-light fa-house text-[10px]"></i><span>/</span><span>Portal da Instituição</span><span>/</span><span>Administração Acadêmica</span><span>/</span><span class="text-slate-600 font-medium">Calendário Escolar</span></div></div>
  </div>
  <button type="button" data-model-refresh class="… bg-emerald-500 …"><i class="fa-light fa-arrows-rotate text-xs"></i><span>Atualizar</span></button>
</div>
<div class="ttsc-fc">
  <div class="fc-legend" aria-label="Tipos de evento"><span class="ev-academic">Acadêmico</span>…</div>
  <div id="academic-calendar" class="fc fc-media-screen fc-direction-ltr fc-theme-standard">
    <div class="fc-header-toolbar fc-toolbar fc-toolbar-ltr">
      <div class="fc-toolbar-chunk"><div class="fc-button-group"><button type="button" title="Anterior" class="fc-prev-button fc-button fc-button-primary">Anterior</button>…</div></div>
      <div class="fc-toolbar-chunk"><h2 class="fc-toolbar-title" id="fc-dom-1">outubro de 2026</h2></div>
      <div class="fc-toolbar-chunk"><div class="fc-button-group"><button type="button" class="fc-dayGridMonth-button fc-button fc-button-primary fc-button-active" aria-pressed="true">Mês</button>…</div></div>
    </div>
    …
    <a class="fc-event fc-daygrid-event fc-daygrid-dot-event ev-type ev-administrative" tabindex="0" title="Reunião de pais — 9º ano">
      <div class="fc-daygrid-event-dot"></div><div class="fc-event-time">19:00</div><div class="fc-event-title">Reunião de pais — 9º ano</div>
    </a>
  </div>
</div>
```

### CSS

O tema é o do componente [FullCalendar](../FullCalendar/README.md) (`--fc-*` → `--ttsc-*`). Em página do chassi há três conflitos a neutralizar, todos resolvidos no preview:

- `ttsc.supabase.css`/`ttsc.commercial.model.css` aplicam no escuro `.dark table th`, `.dark table td` e `.dark a:not(…)` com `!important` (cabeçalho preto, números de dia verdes, "hoje" sem destaque);
- o runtime ttscui pinta `.fc-col-header-cell` e `.fc-button-active` em `@layer components` (com `!important` no botão);
- o runtime força `.fc-event { background-color: var(--primary) !important }`.

```css
.ttsc-fc .fc .fc-col-header-cell,
html.dark .ttsc-fc .fc table thead th.fc-col-header-cell { background-color: var(--ttsc-canvas) !important; }
html .ttsc-fc .fc a.fc-daygrid-day-number { color: var(--ttsc-text-2) !important; }
html .ttsc-fc .fc .fc-day-today a.fc-daygrid-day-number { color: var(--ttsc-accent-text) !important; }
html.dark .ttsc-fc .fc table td.fc-day-today { background-color: var(--fc-today-bg-color) !important; }
/* !important dentro de camada só vence o da camada "components" se estiver numa camada anterior */
@layer base {
  .ttsc-fc .fc .fc-button-primary:not(:disabled).fc-button-active { color: var(--ttsc-accent-text) !important; background-color: var(--ttsc-accent-soft) !important; }
  .ttsc-fc .fc-event.ev-type:not(.fc-list-event) { background-color: var(--ev-soft) !important; color: var(--ttsc-text) !important; }
}
.ev-academic { --ev: var(--ttsc-info); --ev-soft: color-mix(in srgb, var(--ttsc-info) 16%, transparent); }
.ev-holiday  { --ev: var(--ttsc-danger); --ev-soft: color-mix(in srgb, var(--ttsc-danger) 14%, transparent); }
```

### JS

```js
// Agenda alimentada pelo endpoint real; detalhe no drawer do chassi
const el = document.getElementById('academic-calendar');
const TYPES = { academic: 'Acadêmico', administrative: 'Administrativo', cultural: 'Cultural', ceremony: 'Cerimônia', holiday: 'Feriado / recesso' };
const nextDay = (d) => { const x = new Date(d + 'T00:00:00Z'); x.setUTCDate(x.getUTCDate() + 1); return x.toISOString().slice(0, 10); };
const toEvent = (r) => {
  const allDay = !r.start_time;
  return {
    id: r.uuid, title: r.title, allDay,
    start: allDay ? r.start_date : `${r.start_date}T${r.start_time}`,
    end: allDay ? (r.end_date ? nextDay(r.end_date) : undefined) : (r.end_time ? `${r.end_date || r.start_date}T${r.end_time}` : undefined),
    classNames: ['ev-type', 'ev-' + r.type], extendedProps: r,
  };
};

const calendar = new FullCalendar.Calendar(el, {
  locale: 'pt-br',
  buttonText: { today: 'Hoje', month: 'Mês', week: 'Semana', day: 'Dia', list: 'Lista', prev: 'Anterior', next: 'Próximo' },
  allDayText: 'Dia todo', noEventsText: 'Nenhum evento no período', moreLinkText: (n) => `+ ${n} eventos`,
  firstDay: 0, initialView: 'dayGridMonth', height: 'auto', dayMaxEvents: 2, nowIndicator: true, navLinks: true,
  headerToolbar: { left: 'prev,next today', center: 'title', right: 'dayGridMonth,timeGridWeek,listMonth' },
  eventTimeFormat: { hour: '2-digit', minute: '2-digit', hour12: false },
  // fonte de eventos assíncrona: FullCalendar chama a cada mudança de período
  events: (info, success, failure) => {
    fetch(`${el.dataset.eventsUrl}?per_page=100`, { credentials: 'same-origin' })
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error('HTTP ' + r.status))))
      .then((b) => success(b.records.map(toEvent)))
      .catch(failure);
  },
  eventDidMount: (info) => { info.el.title = info.event.title; info.el.tabIndex = 0; },
  eventClick: (info) => {
    info.jsEvent.preventDefault();
    const r = info.event.extendedProps;
    document.getElementById('ev-title').textContent = info.event.title;
    document.getElementById('ev-fields').textContent = `${TYPES[r.type] || r.type} · ${r.location || 'sem local'} · ${r.unit_name || ''}`;
    window.openDrawer('drawer-event');
  },
});
calendar.render();
document.querySelector('[data-model-refresh]')?.addEventListener('click', () => calendar.refetchEvents());
```

### SQL

```sql
-- Eventos do período visível (o FullCalendar pede start/end; dia inteiro quando start_time é nulo)
SELECT e.uuid, e.title, e.type, e.start_date, e.end_date, e.start_time, e.end_time,
       e.location, e.target_audience, e.status, un.name AS unit_name
  FROM events e
  LEFT JOIN units un ON un.uuid = e.unit_uuid
 WHERE e.deleted_at IS NULL
   AND e.status <> 'cancelled'
   AND e.start_date < :end
   AND COALESCE(e.end_date, e.start_date) >= :start
 ORDER BY e.start_date, e.start_time;

-- Pill do banner: eventos do mês por tipo
SELECT e.type, COUNT(*) AS total
  FROM events e
 WHERE e.deleted_at IS NULL
   AND e.start_date >= DATE_FORMAT(:start, '%Y-%m-01')
   AND e.start_date <  DATE_FORMAT(:start, '%Y-%m-01') + INTERVAL 1 MONTH
 GROUP BY e.type;

-- Legenda: tipos ativos do vocabulário real
SELECT value, label
  FROM ref_enum_events_type_6d42758ee279
 WHERE is_active = 1 AND deleted_at IS NULL
 ORDER BY sort_order;

-- Dias sem aula do calendário letivo (feriados vindos do cadastro de calendários)
SELECT code, name, year, start_date, end_date, total_days, days_off
  FROM inst_academic_calendars
 WHERE year = :year;
```

O controlador recebe `start`/`end` do FullCalendar (ISO) e devolve as linhas; o JS converte cada uma com `toEvent()`. A view `inst_events_upcoming` já aplica `deleted_at IS NULL` e `start_date >= CURDATE()` — para navegar a meses passados, leia `events` direto como acima.

## Faça / Não faça

- **Faça:** usar o bundle original do FullCalendar 6.1.20 (o de `assets/vendors` está corrompido) e o locale em português nas opções.
- **Faça:** fim exclusivo em eventos de dia inteiro (`end_date + 1 dia`).
- **Não faça:** cor de evento vinda da coluna `events.color` sem checar contraste; use a classe do tipo.
- **Não faça:** cadastrar eventos pelo calendário enquanto a fonte for `writable => false`; o "Novo" fica em `/academic/events/list`.
