# DateRangePicker

Seletor de período **daterangepicker 3.1.0** (jQuery 3.7.1 + moment 2.30.1) com presets em pt-BR (Hoje, Últimos 7 dias, Este mês…) e dois calendários, usado como filtro de relatórios e listas (`BETWEEN` no SQL).

## Quando usar

- Filtro de período em relatórios e listagens: matrículas por `enrollment_date`, eventos por `start_date`, frequência, financeiro.
- Quando presets economizam cliques (“Últimos 30 dias”, “Mês passado”, “Este ano letivo”).
- **Não use** para campo de formulário que grava um intervalo (início/fim da turma) — use [Flatpickr](../Flatpickr/README.md) `mode: 'range'`.
- **Não use** para data com hora — use [TempusDominus](../TempusDominus/README.md).
- Em telas sem jQuery, prefira flatpickr range com botões de preset próprios (evita +120 KB de jQuery + moment).

## Anatomia

```
Data da matrícula
[ (cal) 15/10/2026 a 21/10/2026 ]           input readonly (gatilho)
 ┌─────────────┬──────────────────┬──────────────────┐
 │ Hoje        │  ‹ outubro 2026  │  novembro 2026 › │   .daterangepicker
 │ Ontem       │  Do Se Te Qu …   │  Do Se Te Qu …   │   .ranges (presets) · .drp-calendar.left/right
 │ Últimos 7 ◀ │  [15]▒▒▒▒▒[21]   │                  │   start-date/end-date = ttsc-accent; in-range = accent-soft
 │ …           │                  │                  │
 ├─────────────┴──────────────────┴──────────────────┤
 │            15/10/2026 a 21/10/2026 [Cancelar][Aplicar] │  .drp-buttons
 └────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Gatilho | `input.ttsc-input[readonly]` (ou botão) | sim |
| Ícone | wrapper `.ttsc-date-field > i.fa-light.fa-calendar-range` | não |
| Campos enviados | `input[type=hidden][name=date_from]` / `[name=date_to]` em ISO | sim (filtro GET) |
| Popup | `.daterangepicker` (gerado; `parentEl` define onde é inserido) | — |
| Presets | `.ranges li` (`.active` no selecionado) | recomendado |

## Variantes

| Uso | Opções |
|---|---|
| Filtro com presets | `ranges`, `alwaysShowCalendars: true`, `autoApply: false` |
| Aplicar ao clicar | `autoApply: true` (sem botões; só sem presets) |
| Data única | `singleDatePicker: true`, `showDropdowns: true` (ex.: ano de nascimento) |
| Com hora | `timePicker: true`, `timePicker24Hour: true` (raro; prefira Tempus Dominus) |
| Vazio no início | `autoUpdateInput: false` + preencher em `apply.daterangepicker` |

Tokens: popup `ttsc-surface`, borda `ttsc-border`, sombra `ttsc-shadow-popover`; presets `ttsc-text-2` → ativo `ttsc-accent-soft`/`ttsc-accent-text`; início/fim `ttsc-accent`/`ttsc-accent-on`; intervalo `ttsc-accent-soft`; botão Aplicar `ttsc-accent`, Cancelar contorno `ttsc-border`.

## API

`$(el).daterangepicker(opções, callback(start, end, label))`; instância em `$(el).data('daterangepicker')`.

| Opção | Valor TTSC | Descrição |
|---|---|---|
| `startDate` / `endDate` | `moment()` | período inicial |
| `minDate` / `maxDate` | — | limites |
| `ranges` | objeto rótulo → `[início, fim]` | presets |
| `alwaysShowCalendars` | `true` | calendários visíveis com presets |
| `autoApply` / `autoUpdateInput` | `false` / `true` | aplicação |
| `opens` / `drops` / `parentEl` | `right` / `down` / `body` | posição e contêiner |
| `linkedCalendars` · `showDropdowns` · `maxSpan` | — | navegação, ex.: `maxSpan: { days: 366 }` |
| `locale` | ver JS | `format: 'DD/MM/YYYY'`, `separator: ' a '`, rótulos, `daysOfWeek`, `monthNames`, `firstDay: 0` |
| `buttonClasses` / `applyButtonClasses` / `cancelClass` | classes extras | estilo dos botões |

| Método | Descrição |
|---|---|
| `setStartDate(m)` · `setEndDate(m)` | define o período |
| `show()` · `hide()` · `toggle()` | popup |
| `remove()` | destrói |

| Evento jQuery (no input) | `picker` |
|---|---|
| `show.daterangepicker` · `hide.daterangepicker` | instância |
| `apply.daterangepicker` · `cancel.daterangepicker` | `picker.startDate`, `picker.endDate`, `picker.chosenLabel` |
| `showCalendar.daterangepicker` · `hideCalendar.daterangepicker` | instância |

## Acessibilidade

- O plugin tem suporte limitado a teclado: **sempre** ofereça os presets (clicáveis por Tab/Enter) e mantenha o input com rótulo (`<label for>`), além de permitir os parâmetros na URL (`?date_from=…&date_to=…`).
- O resumo do período aplicado aparece em texto (`role="status"`) fora do popup — ex.: “Últimos 7 dias · 15/10/2026 a 21/10/2026”.
- Botões “Aplicar/Cancelar” traduzidos; contraste `ttsc-accent-on` sobre `ttsc-accent` (9,6:1).
- Dias fora do mês em `ttsc-text-muted` com opacidade — não carregam informação.

## Modelos

### HTML

```html
<link rel="stylesheet" href="/assets/vendors/daterangepicker/daterangepicker.css">
<script src="/assets/vendors/jquery/jquery.min.js"></script>
<script src="/assets/vendors/moment/moment.min.js"></script>
<script src="/assets/vendors/daterangepicker/daterangepicker.js"></script>

<form method="get" action="/secretaria/relatorios/matriculas" class="flex items-end gap-3" id="filter-enrollments">
  <div class="flex flex-col gap-2">
    <label class="ttsc-form-label" for="enrollment-period">Data da matrícula</label>
    <div class="ttsc-date-field">
      <i class="fa-light fa-calendar-range" aria-hidden="true"></i>
      <input class="ttsc-input" id="enrollment-period" readonly data-ttsc-daterange
             data-from="<?= $this->e($dateFrom) ?>" data-to="<?= $this->e($dateTo) ?>">
    </div>
  </div>
  <input type="hidden" name="date_from" value="<?= $this->e($dateFrom) ?>">
  <input type="hidden" name="date_to" value="<?= $this->e($dateTo) ?>">
  <span class="text-xs text-muted-foreground" data-range-summary role="status" aria-live="polite"></span>
</form>
```

### CSS

```css
/* assets/css/ttsc.css — tema daterangepicker por tokens */
.daterangepicker { background: var(--ttsc-surface); border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control);
  box-shadow: var(--ttsc-shadow-popover); color: var(--ttsc-text); font-family: inherit; font-size: 13px; z-index: var(--ttsc-z-popover); }
.daterangepicker::before, .daterangepicker::after { display: none; }
.daterangepicker .calendar-table { background: var(--ttsc-surface); border-color: var(--ttsc-surface); }
.daterangepicker .calendar-table th, .daterangepicker .calendar-table td { min-width: 30px; width: 30px; height: 28px; line-height: 26px;
  font-size: 12px; border-radius: var(--ttsc-radius-xs); }
.daterangepicker .calendar-table th.month { color: var(--ttsc-text); font-weight: 600; font-size: 13px; text-transform: capitalize; }
.daterangepicker .calendar-table thead tr:nth-child(2) th { color: var(--ttsc-text-muted); font-weight: 500; font-size: 11px; }
.daterangepicker .calendar-table .next span, .daterangepicker .calendar-table .prev span { border-color: var(--ttsc-text-2); }
.daterangepicker td.available:hover, .daterangepicker th.available:hover { background: var(--ttsc-canvas-2); color: var(--ttsc-text); }
.daterangepicker td.off, .daterangepicker td.off.in-range, .daterangepicker td.off.start-date, .daterangepicker td.off.end-date {
  background: transparent; color: var(--ttsc-text-muted); opacity: .55; }
.daterangepicker td.in-range { background: var(--ttsc-accent-soft); color: var(--ttsc-text); border-radius: 0; }
.daterangepicker td.start-date { border-radius: var(--ttsc-radius-xs) 0 0 var(--ttsc-radius-xs); }
.daterangepicker td.end-date { border-radius: 0 var(--ttsc-radius-xs) var(--ttsc-radius-xs) 0; }
.daterangepicker td.start-date.end-date { border-radius: var(--ttsc-radius-xs); }
.daterangepicker td.active, .daterangepicker td.active:hover { background: var(--ttsc-accent); color: var(--ttsc-accent-on); font-weight: 600; }
.daterangepicker .ranges li { color: var(--ttsc-text-2); border-radius: var(--ttsc-radius-xs); margin: 2px 6px; padding: 7px 10px; }
.daterangepicker .ranges li:hover { background: var(--ttsc-canvas-2); color: var(--ttsc-text); }
.daterangepicker .ranges li.active { background: var(--ttsc-accent-soft); color: var(--ttsc-accent-text); font-weight: 600; }
.daterangepicker.show-ranges.ltr .drp-calendar.left { border-left-color: var(--ttsc-border); }
.daterangepicker .drp-buttons { border-top-color: var(--ttsc-border); }
.daterangepicker .drp-selected { color: var(--ttsc-text-2); font-size: 12px; }
.daterangepicker .drp-buttons .btn { font: inherit; font-weight: 500; font-size: 12px; padding: 5px 12px; border-radius: var(--ttsc-radius-sm); cursor: pointer; }
.daterangepicker .drp-buttons .cancelBtn { background: transparent; border: 1px solid var(--ttsc-border); color: var(--ttsc-text); }
.daterangepicker .drp-buttons .applyBtn { background: var(--ttsc-accent); border: 1px solid var(--ttsc-accent); color: var(--ttsc-accent-on); }
```

### JS

```js
// assets/js/core/ttsc.daterange.js
const DRP_LOCALE_PT_BR = {
  format: 'DD/MM/YYYY', separator: ' a ', applyLabel: 'Aplicar', cancelLabel: 'Cancelar',
  fromLabel: 'De', toLabel: 'Até', customRangeLabel: 'Personalizado', weekLabel: 'S', firstDay: 0,
  daysOfWeek: ['Do', 'Se', 'Te', 'Qu', 'Qu', 'Se', 'Sá'],
  monthNames: ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'],
};

function presets() {
  return {
    'Hoje': [moment(), moment()],
    'Ontem': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
    'Últimos 7 dias': [moment().subtract(6, 'days'), moment()],
    'Últimos 30 dias': [moment().subtract(29, 'days'), moment()],
    'Este mês': [moment().startOf('month'), moment().endOf('month')],
    'Mês passado': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
    'Este ano letivo': [moment().startOf('year'), moment().endOf('year')],
  };
}

$('input[data-ttsc-daterange]').each(function () {
  const $input = $(this);
  const form = this.closest('form');
  const from = $input.data('from') ? moment($input.data('from'), 'YYYY-MM-DD') : moment().subtract(6, 'days');
  const to = $input.data('to') ? moment($input.data('to'), 'YYYY-MM-DD') : moment();
  const summary = form.querySelector('[data-range-summary]');

  $input.daterangepicker({
    startDate: from, endDate: to, maxDate: moment().endOf('year'),
    ranges: presets(), alwaysShowCalendars: true, opens: 'right',
    maxSpan: { days: 366 }, locale: DRP_LOCALE_PT_BR,
  }, (start, end, label) => {
    form.querySelector('[name="date_from"]').value = start.format('YYYY-MM-DD');
    form.querySelector('[name="date_to"]').value = end.format('YYYY-MM-DD');
    if (summary) summary.textContent = `${label && label !== 'Personalizado' ? label + ' · ' : ''}${start.format('DD/MM/YYYY')} a ${end.format('DD/MM/YYYY')}`;
  });

  // Submete o filtro ao aplicar
  $input.on('apply.daterangepicker', () => form.requestSubmit());
});
```

### SQL

```sql
-- Matrículas por dia no período filtrado (BETWEEN em enrollments.enrollment_date — coluna DATE)
SELECT en.enrollment_date, COUNT(*) AS total, SUM(en.status = 'active') AS active
  FROM enrollments en
 WHERE en.deleted_at IS NULL
   AND en.unit_uuid = :unit_uuid
   AND en.enrollment_date BETWEEN :date_from AND :date_to
 GROUP BY en.enrollment_date
 ORDER BY en.enrollment_date;

-- Eventos que tocam o período (events.start_date/end_date — inclui eventos de vários dias)
SELECT e.uuid, e.title, e.type, e.start_date, e.end_date
  FROM events e
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid
   AND e.start_date <= :date_to
   AND COALESCE(e.end_date, e.start_date) >= :date_from
 ORDER BY e.start_date;
```

O controller lê `date_from`/`date_to` do GET (`Y-m-d`, validados com `DateTime::createFromFormat`, padrão últimos 7 dias, máximo 366 dias), executa a consulta e devolve os mesmos valores para a view (`data-from`/`data-to`) para o picker reabrir no período aplicado. Em colunas `DATETIME` (ex.: `created_at`), use `>= :date_from AND < :date_to + INTERVAL 1 DAY` em vez de `BETWEEN`.

## Faça / Não faça

- **Faça:** presets na ordem Hoje → Ontem → 7 → 30 dias → mês → ano letivo; “Personalizado” por último (automático).
- **Faça:** enviar ISO em campos ocultos e exibir `DD/MM/YYYY`.
- **Não faça:** `BETWEEN` direto em `DATETIME` (perde o último dia).
- **Não faça:** carregar jQuery + moment só para isso numa tela nova — avalie flatpickr range.
