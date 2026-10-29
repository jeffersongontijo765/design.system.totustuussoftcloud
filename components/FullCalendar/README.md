# FullCalendar

Calendário FullCalendar 6.1.20 (bundle global do repo) para a agenda acadêmica — visões mês/semana/lista, locale `pt-br` inline, eventos coloridos por tipo e tema ligado aos tokens via variáveis `--fc-*`.

## Quando usar

- Agenda institucional (`events`): provas, conselhos de classe, reuniões de pais, feriados/recessos, formaturas.
- Telas do arquétipo Calendar ([PageCalendar](../PageCalendar/README.md)) e widgets “Próximos eventos” na visão lista.
- **Não use** para escolher uma data num formulário: use [DatePicker](../DatePicker/README.md) / [Flatpickr](../Flatpickr/README.md); intervalo de datas → [DateRangePicker](../DateRangePicker/README.md).
- **Não use** para histórico de ações: [Timeline](../Timeline/README.md). Para grade horária fixa de aulas sem datas, uma tabela é mais legível.

## Anatomia

```
.ttsc-fc (card + variáveis --fc-*)
└── .fc
    ├── .fc-header-toolbar  [Anterior|Próximo] [Hoje]   "Outubro de 2026"   [Mês|Semana|Lista]
    └── .fc-view-harness
        ├── .fc-col-header (DOM. SEG. …)
        └── .fc-daygrid-day (.fc-day-today) › .fc-daygrid-event.ev-type.ev-<tipo>
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Wrapper de tema | `.ttsc-fc` com as variáveis `--fc-*` | sim |
| Alvo | `<div id="calendar">` | sim |
| Evento | `classNames: ['ev-type', 'ev-<type>']` (`academic`, `administrative`, `cultural`, `ceremony`, `holiday`…) | sim |
| Legenda | `.fc-legend` com os tipos (cor + texto) | recomendado |
| Hoje | `.fc-day-today` | gerado |

## Variantes

| Tipo (`events.type`) | Classe | Barra / fundo | Uso |
|---|---|---|---|
| `academic` | `ev-academic` | `ttsc-info` / 16% | provas, prazos, entrega de notas |
| `administrative` | `ev-administrative` | `ttsc-warning` / 16% | conselhos, reuniões |
| `cultural`, `sports`, `workshop` | `ev-cultural` | `ttsc-meta` / 22% | mostras, jogos, oficinas |
| `ceremony` | `ev-ceremony` | `ttsc-accent` / `ttsc-accent-soft` | formaturas |
| `holiday` | `ev-holiday` | `ttsc-danger` / 14% | feriados e recessos |

Visões: `dayGridMonth` (padrão), `timeGridWeek` (07:00–23:00), `listMonth` (mobile e widgets). Texto do evento sempre `ttsc-text`; dia atual `ttsc-accent-soft` com número em `ttsc-accent-text`.

## API

### Opções usadas

| Opção | Valor | Nota |
|---|---|---|
| `locale` | `'pt-br'` | o bundle não traz `locales-all`; textos vão inline (abaixo) e datas usam `Intl` |
| `buttonText` | `{ today: 'Hoje', month: 'Mês', week: 'Semana', day: 'Dia', list: 'Lista', prev: 'Anterior', next: 'Próximo' }` | |
| `allDayText` / `noEventsText` / `moreLinkText` | `'Dia todo'` / `'Nenhum evento no período'` / `n => '+ ' + n + ' eventos'` | ver “bug do vendor” |
| `firstDay` | `0` (domingo) | |
| `headerToolbar` | `{ left: 'prev,next today', center: 'title', right: 'dayGridMonth,timeGridWeek,listMonth' }` | |
| `events` | URL (`/admin/academic/events/feed`) ou função | recebe `start`/`end` ISO do intervalo visível |
| `dayMaxEvents` | `2` | “+ n eventos” abre popover |
| `eventTimeFormat` / `slotLabelFormat` | `{ hour: '2-digit', minute: '2-digit', hour12: false }` | 24h |
| `slotMinTime` / `slotMaxTime` | `'07:00:00'` / `'23:00:00'` | turnos da escola |
| `nowIndicator` / `navLinks` | `true` | |
| `height` | `'auto'` | sem rolagem interna |

### Métodos e callbacks

| API | Uso |
|---|---|
| `calendar.render()` / `destroy()` | ciclo de vida |
| `calendar.refetchEvents()` | após salvar no drawer de evento |
| `calendar.changeView('listMonth')` / `gotoDate(d)` / `today()` | navegação |
| `calendar.addEvent(obj)` / `getEventById(id)?.remove()` | edição otimista |
| `eventClick(info)` | abre o [Drawer](../Drawer/README.md) do evento (`info.event.id` = `uuid`) |
| `dateClick(info)` / `select(info)` | criar evento no dia/intervalo (`selectable: true`) |
| `eventDidMount(info)` | `title`/`aria-label` no elemento |
| `datesSet(info)` | sincronizar filtros/URL com o intervalo |

### Bug do vendor (repo)

`assets/vendors/fullcalendar/index.global.min.js` foi atingido pelo rename global `kt → ttsc`: o arquivo declara `function ttsc` e `ttsc = /UTC|GMT/` no mesmo escopo e lança **“Identifier 'ttsc' has already been declared”** (o calendário não carrega). As opções `weekText` e `moreLinkText` também viraram `weettscext`/`moreLinttscext`. Correção: restaurar o arquivo original do pacote `fullcalendar@6.1.20` (`dist/index.global.min.js`) e excluir `assets/vendors/` de substituições de prefixo. O preview desfaz a colisão em tempo de carga apenas para demonstrar.

## Acessibilidade

- Botões da toolbar são `<button>` com texto em pt-BR; `navLinks` torna os números de dia links focáveis.
- O tipo do evento nunca é só cor: inclua o tipo no título ou no `aria-label` (`eventDidMount`) e mostre a legenda com texto.
- Ofereça a visão **Lista** (`listMonth`) — é a mais acessível para leitor de tela e celular.
- Contraste: texto `ttsc-text` sobre fundo do tipo a 14–22% (≥ 7:1 nos dois temas); barra lateral sólida como pista extra.

## Modelos

### HTML

```html
<div class="ttsc-card">
  <div class="ttsc-card-content">
    <div class="fc-legend">
      <span class="ev-academic">Acadêmico</span><span class="ev-administrative">Administrativo</span>
      <span class="ev-cultural">Cultural</span><span class="ev-ceremony">Cerimônia</span><span class="ev-holiday">Feriado / recesso</span>
    </div>
    <div class="ttsc-fc">
      <div id="calendar" data-feed="/admin/academic/events/feed" data-unit="<?= $this->e($unitUuid) ?>"></div>
    </div>
  </div>
</div>
<script src="/assets/vendors/fullcalendar/index.global.min.js"></script>
<script src="/assets/js/core/ttsc.calendar.js"></script>
```

### CSS

```css
.ttsc-fc {
  --fc-border-color: var(--ttsc-border-soft);
  --fc-page-bg-color: var(--ttsc-surface);
  --fc-neutral-bg-color: var(--ttsc-canvas);
  --fc-neutral-text-color: var(--ttsc-text-muted);
  --fc-today-bg-color: var(--ttsc-accent-soft);
  --fc-now-indicator-color: var(--ttsc-danger);
  --fc-highlight-color: var(--ttsc-accent-soft);
  --fc-list-event-hover-bg-color: var(--ttsc-canvas-2);
  --fc-button-text-color: var(--ttsc-text);
  --fc-button-bg-color: var(--ttsc-surface);
  --fc-button-border-color: var(--ttsc-border);
  --fc-button-hover-bg-color: var(--ttsc-canvas-2);
  --fc-button-active-bg-color: var(--ttsc-accent-soft);
  --fc-button-active-border-color: var(--ttsc-accent-border);
}
.ttsc-fc .fc .fc-toolbar-title { font-size: 15px; font-weight: 600; color: var(--ttsc-text); }
.ttsc-fc .fc .fc-toolbar-title::first-letter { text-transform: uppercase; }
.ttsc-fc .fc .fc-day-today .fc-daygrid-day-number { color: var(--ttsc-accent-text); font-weight: 700; }

/* O runtime (tailwind-runtime.css, @layer components) força
   .fc-event { background-color: var(--primary) !important }.
   !important fora de camada PERDE para !important em camada — por isso a regra vai em @layer base. */
@layer base {
  .ttsc-fc .fc-event.ev-type:not(.fc-list-event) {
    background-color: var(--ev-soft) !important; color: var(--ttsc-text) !important; padding: 1px 4px !important;
  }
}
.ttsc-fc .fc-event.ev-type:not(.fc-list-event) { border: 0; border-left: 3px solid var(--ev); border-radius: var(--ttsc-radius-xs); }
.ev-academic       { --ev: var(--ttsc-info);    --ev-soft: color-mix(in srgb, var(--ttsc-info) 16%, transparent); }
.ev-administrative { --ev: var(--ttsc-warning); --ev-soft: color-mix(in srgb, var(--ttsc-warning) 16%, transparent); }
.ev-cultural       { --ev: var(--ttsc-meta);    --ev-soft: color-mix(in srgb, var(--ttsc-meta) 22%, transparent); }
.ev-ceremony       { --ev: var(--ttsc-accent);  --ev-soft: var(--ttsc-accent-soft); }
.ev-holiday        { --ev: var(--ttsc-danger);  --ev-soft: color-mix(in srgb, var(--ttsc-danger) 14%, transparent); }
```

### JS

```js
// assets/js/core/ttsc.calendar.js
const TYPE_CLASS = { academic: 'ev-academic', administrative: 'ev-administrative', cultural: 'ev-cultural',
  sports: 'ev-cultural', workshop: 'ev-cultural', ceremony: 'ev-ceremony', holiday: 'ev-holiday', other: 'ev-cultural' };

export function initAcademicCalendar(el = document.getElementById('calendar')) {
  const calendar = new FullCalendar.Calendar(el, {
    locale: 'pt-br',
    buttonText: { today: 'Hoje', month: 'Mês', week: 'Semana', day: 'Dia', list: 'Lista', prev: 'Anterior', next: 'Próximo' },
    allDayText: 'Dia todo',
    noEventsText: 'Nenhum evento no período',
    moreLinkText: (n) => `+ ${n} eventos`,
    firstDay: 0,
    initialView: window.matchMedia('(max-width: 768px)').matches ? 'listMonth' : 'dayGridMonth',
    headerToolbar: { left: 'prev,next today', center: 'title', right: 'dayGridMonth,timeGridWeek,listMonth' },
    height: 'auto',
    dayMaxEvents: 2,
    nowIndicator: true,
    navLinks: true,
    eventTimeFormat: { hour: '2-digit', minute: '2-digit', hour12: false },
    slotLabelFormat: { hour: '2-digit', minute: '2-digit', hour12: false },
    slotMinTime: '07:00:00',
    slotMaxTime: '23:00:00',
    events: {
      url: el.dataset.feed,                 // GET ?start=2026-09-27T00:00:00&end=2026-11-08T00:00:00&unit=…
      extraParams: { unit: el.dataset.unit },
      failure: () => TTSC.Toast?.show({ message: 'Não foi possível carregar a agenda.', variant: 'destructive' }),
    },
    eventDataTransform: (row) => ({
      id: row.id, title: row.title, start: row.start_at, end: row.end_at, allDay: !!Number(row.all_day),
      classNames: ['ev-type', TYPE_CLASS[row.type] || 'ev-cultural'],
      extendedProps: { type: row.type, location: row.location },
    }),
    eventDidMount: (info) => {
      const where = info.event.extendedProps.location ? ` — ${info.event.extendedProps.location}` : '';
      info.el.setAttribute('aria-label', `${info.event.title}${where}`);
      info.el.title = info.event.title + where;
    },
    eventClick: (info) => {
      info.jsEvent.preventDefault();
      document.dispatchEvent(new CustomEvent('ttsc:event-open', { detail: { uuid: info.event.id } }));
    },
  });
  calendar.render();
  document.addEventListener('ttsc:event-saved', () => calendar.refetchEvents());
  return calendar;
}

document.addEventListener('DOMContentLoaded', () => { if (document.getElementById('calendar')) initAcademicCalendar(); });
```

### SQL

O feed recebe o intervalo visível (`start` inclusivo, `end` exclusivo) e devolve os eventos que se **sobrepõem** a ele. Eventos sem hora são de dia inteiro e o `end` exclusivo soma 1 dia:

```sql
SELECT ev.uuid AS id, ev.title, ev.type, ev.location, ev.color,
       CASE WHEN ev.start_time IS NULL
            THEN DATE_FORMAT(ev.start_date, '%Y-%m-%d')
            ELSE CONCAT(DATE_FORMAT(ev.start_date, '%Y-%m-%d'), 'T', TIME_FORMAT(ev.start_time, '%H:%i:%s'))
       END AS start_at,
       CASE WHEN ev.start_time IS NULL
            THEN DATE_FORMAT(COALESCE(ev.end_date, ev.start_date) + INTERVAL 1 DAY, '%Y-%m-%d')
            ELSE CONCAT(DATE_FORMAT(COALESCE(ev.end_date, ev.start_date), '%Y-%m-%d'), 'T',
                        TIME_FORMAT(COALESCE(ev.end_time, ev.start_time), '%H:%i:%s'))
       END AS end_at,
       ev.start_time IS NULL AS all_day
  FROM events ev
 WHERE ev.deleted_at IS NULL
   AND ev.unit_uuid = :unit_uuid
   AND ev.status <> 'cancelled'
   AND ev.start_date < :range_end                          -- '2026-11-08'
   AND COALESCE(ev.end_date, ev.start_date) >= :range_start -- '2026-09-27'
 ORDER BY ev.start_date, ev.start_time;
```

O controller valida `start`/`end` (datas ISO, intervalo ≤ 62 dias), executa e devolve o array JSON direto (`Response::json($rows)`); `eventDataTransform` mapeia as colunas. A coluna `color` é ignorada na UI: a cor vem do `type` → token (cores livres quebram contraste no escuro).

## Faça / Não faça

- **Faça:** feed por intervalo (nunca todos os eventos do ano) e filtro por `unit_uuid` + `deleted_at IS NULL`.
- **Faça:** cores por tipo via classes/tokens e legenda com texto; visão lista no mobile.
- **Faça:** restaurar o vendor original do FullCalendar antes de usar em produção (ver “Bug do vendor”).
- **Não faça:** carregar `locales-all` de CDN — os textos pt-BR vão inline.
- **Não faça:** usar `events.color` (hex do banco) como `backgroundColor` do evento.
- **Não faça:** sobrescrever o runtime com `!important` fora de camada — use `@layer base` como no CSS acima.
