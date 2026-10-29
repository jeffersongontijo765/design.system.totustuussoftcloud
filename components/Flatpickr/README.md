# Flatpickr

Seletor de data **flatpickr 4.6.13** com **l10n pt** — data única, intervalo e hora (24 h) — e tema TTSC por tokens válido nos dois temas; é o seletor de data padrão dos formulários.

## Quando usar

- Qualquer campo de data em formulário CRUD: nascimento, data da matrícula, início/fim da turma, vencimento.
- Intervalo simples (início — fim de turma, período de rematrícula) com `mode: 'range'`.
- Hora isolada (horário da aula) com `noCalendar`.
- Calendário inline em telas de configuração de período.
- Data + hora com regras ricas e toolbar: [TempusDominus](../TempusDominus/README.md).
- Filtro de relatório com presets (“Últimos 30 dias”): [DateRangePicker](../DateRangePicker/README.md).
- Não use `<input type="date">` nativo em telas do chassi (formato e estilo variam por navegador).

## Anatomia

```
Data de nascimento
[ (cal) 14/03/2009            ]   altInput visível (d/m/Y) — input original oculto envia Y-m-d
 ┌───────────────────────────┐
 │  outubro ▾ 2026        ›  │    .flatpickr-calendar (.inline quando embutido)
 │ DOM SEG TER QUA QUI SEX SÁB│
 │ … [24]▒▒▒▒▒▒▒▒▒▒[30] …     │    startRange/endRange = ttsc-accent; inRange = accent 16%
 └───────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Campo | `input.ttsc-input` com `name` (valor enviado em `Y-m-d`) | sim |
| Ícone | wrapper `.ttsc-date-field > i.fa-light` (posicionado, `z-index: 1`) | não |
| Campo visível | `altInput: true`, `altInputClass: 'ttsc-input'`, `altFormat: 'd/m/Y'` | recomendado |
| Calendário | `.flatpickr-calendar` (gerado; `.inline` / `.open`) | — |
| Hora | `.flatpickr-time` (com `enableTime`) | não |

## Variantes

| Modo | Opções |
|---|---|
| Single | `dateFormat: 'Y-m-d'`, `altInput`, `altFormat: 'd/m/Y'`, `allowInput: true` |
| Range | `mode: 'range'`, `locale: { rangeSeparator: ' a ' }` (valor `2027-02-01 a 2027-06-30`) |
| Time | `enableTime: true`, `noCalendar: true`, `dateFormat: 'H:i'`, `time_24hr: true`, `minuteIncrement: 5` |
| Data + hora | `enableTime: true`, `dateFormat: 'Y-m-d H:i'`, `altFormat: 'd/m/Y H:i'` |
| Inline | `inline: true` (input oculto com `display:none`) |
| Múltiplas | `mode: 'multiple'` (dias de aula avulsos) |

Tokens do tema: calendário `ttsc-surface` + borda `ttsc-border` + `ttsc-shadow-popover`; dias `ttsc-text`; fora do mês `ttsc-text-muted`; hoje borda `ttsc-accent`; selecionado `ttsc-accent`/`ttsc-accent-on`; intervalo `color-mix(ttsc-accent 16%, ttsc-surface)`; hover `ttsc-canvas-2`.

## API

Global `flatpickr`; locale via `flatpickr.localize(flatpickr.l10ns.pt)` (arquivo `l10n/pt.js`).

| Opção | Descrição |
|---|---|
| `dateFormat` / `altInput` / `altFormat` / `altInputClass` | formato enviado × exibido |
| `mode` | `single` · `multiple` · `range` |
| `minDate` / `maxDate` / `disable` / `enable` | restrições (`'today'`, datas, funções) |
| `defaultDate` | valor inicial |
| `enableTime` / `noCalendar` / `time_24hr` / `minuteIncrement` | hora |
| `inline` / `static` / `appendTo` / `position` | posicionamento |
| `allowInput` / `clickOpens` / `locale` | comportamento |

| Método (instância `fp`) | Descrição |
|---|---|
| `setDate(datas, disparaChange?)` · `clear()` | valor |
| `open()` · `close()` · `toggle()` | popup |
| `set(opção, valor)` | muda opção (ex.: `minDate` do fim = início) |
| `formatDate(date, formato)` · `parseDate(str, formato)` | utilitários |
| `selectedDates` · `destroy()` | estado / destruir |

| Hook | Assinatura |
|---|---|
| `onChange` · `onOpen` · `onClose` · `onReady` · `onValueUpdate` · `onMonthChange` · `onDayCreate` | `(selectedDates, dateStr, instance)` |

## Acessibilidade

- Com `altInput`, o campo visível é um novo `<input>` sem `id`: no `onReady`, dê um `id` a `fp.altInput`, aponte o `<label for>` para ele e copie o `aria-describedby` (ver JS). Os dias do calendário recebem `aria-label` por `ariaDateFormat` (padrão `F j, Y`; use `'j \\de F \\de Y'`).
- `allowInput: true` permite digitar `dd/mm/aaaa`; teclado no calendário: setas navegam, Enter seleciona, Esc fecha.
- Datas desabilitadas com opacidade + `ttsc-text-muted`; explique a regra no texto de ajuda.
- Contraste: selecionado `ttsc-accent-on` sobre `ttsc-accent` (9,6:1); dias `ttsc-text` sobre `ttsc-surface` nos dois temas; intervalo mistura opaca (sem listras escuras no tema escuro).

## Modelos

### HTML

```html
<link rel="stylesheet" href="/assets/vendors/flatpickr/flatpickr.min.css">
<script src="/assets/vendors/flatpickr/flatpickr.min.js"></script>
<script src="/assets/vendors/flatpickr/l10n/pt.js"></script>

<div class="flex flex-col gap-2">
  <label class="ttsc-form-label" for="class-period">Período da turma</label>
  <div class="ttsc-date-field">
    <i class="fa-light fa-calendar-range" aria-hidden="true"></i>
    <input class="ttsc-input" id="class-period" name="period" data-ttsc-date="range" placeholder="Selecione o intervalo"
           value="<?= $this->e($class['start_date'] && $class['end_date'] ? $class['start_date'] . ' a ' . $class['end_date'] : '') ?>"
           aria-describedby="class-period-help">
  </div>
  <p class="text-xs text-muted-foreground" id="class-period-help">Data de início e de término das aulas.</p>
</div>

<div class="flex flex-col gap-2">
  <label class="ttsc-form-label" for="lesson-time">Horário da aula</label>
  <div class="ttsc-date-field">
    <i class="fa-light fa-clock" aria-hidden="true"></i>
    <input class="ttsc-input" id="lesson-time" name="start_time" data-ttsc-date="time" value="19:00">
  </div>
</div>
```

### CSS

```css
/* assets/css/ttsc.css — tema flatpickr por tokens */
.flatpickr-calendar { background: var(--ttsc-surface); border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control);
  box-shadow: var(--ttsc-shadow-popover); font-family: inherit; font-size: 13px; }
.flatpickr-calendar.inline { box-shadow: none; }
.flatpickr-calendar.arrowTop::before, .flatpickr-calendar.arrowTop::after,
.flatpickr-calendar.arrowBottom::before, .flatpickr-calendar.arrowBottom::after { display: none; }
.flatpickr-months .flatpickr-month, .flatpickr-current-month input.cur-year,
.flatpickr-current-month .flatpickr-monthDropdown-months { color: var(--ttsc-text); fill: var(--ttsc-text); background: transparent; }
.flatpickr-current-month { font-size: 14px; font-weight: 600; }
.flatpickr-current-month .flatpickr-monthDropdown-months .flatpickr-monthDropdown-month { background: var(--ttsc-surface); color: var(--ttsc-text); }
.flatpickr-months .flatpickr-prev-month, .flatpickr-months .flatpickr-next-month { color: var(--ttsc-text-2); fill: var(--ttsc-text-2); }
.flatpickr-months .flatpickr-prev-month:hover svg, .flatpickr-months .flatpickr-next-month:hover svg { fill: var(--ttsc-accent-text); }
.numInputWrapper span.arrowUp::after { border-bottom-color: var(--ttsc-text-2); }
.numInputWrapper span.arrowDown::after { border-top-color: var(--ttsc-text-2); }
span.flatpickr-weekday { color: var(--ttsc-text-muted); font-weight: 500; font-size: 11px; text-transform: uppercase; background: transparent; }
.flatpickr-day { color: var(--ttsc-text); border-radius: var(--ttsc-radius-xs); }
.flatpickr-day:hover, .flatpickr-day:focus { background: var(--ttsc-canvas-2); border-color: var(--ttsc-canvas-2); color: var(--ttsc-text); }
.flatpickr-day.today { border-color: var(--ttsc-accent); }
.flatpickr-day.prevMonthDay, .flatpickr-day.nextMonthDay, .flatpickr-day.flatpickr-disabled { color: var(--ttsc-text-muted); opacity: .55; }
.flatpickr-day.selected, .flatpickr-day.startRange, .flatpickr-day.endRange,
.flatpickr-day.selected:hover, .flatpickr-day.startRange:hover, .flatpickr-day.endRange:hover {
  background: var(--ttsc-accent); border-color: var(--ttsc-accent); color: var(--ttsc-accent-on); font-weight: 600; }
.flatpickr-day.inRange, .flatpickr-day.inRange:hover { --fp-range: color-mix(in oklab, var(--ttsc-accent) 16%, var(--ttsc-surface));
  background: var(--fp-range); border-color: transparent; box-shadow: -5px 0 0 var(--fp-range), 5px 0 0 var(--fp-range); color: var(--ttsc-text); }
.flatpickr-day.selected.startRange, .flatpickr-day.startRange.startRange { border-radius: var(--ttsc-radius-xs) 0 0 var(--ttsc-radius-xs); }
.flatpickr-day.selected.endRange, .flatpickr-day.endRange.endRange { border-radius: 0 var(--ttsc-radius-xs) var(--ttsc-radius-xs) 0; }
.flatpickr-day.startRange.endRange { border-radius: var(--ttsc-radius-xs); }
.flatpickr-time { border-top: 1px solid var(--ttsc-border) !important; }
.flatpickr-time input, .flatpickr-time .flatpickr-time-separator, .flatpickr-time .flatpickr-am-pm { color: var(--ttsc-text); background: transparent; }
.flatpickr-time input:hover, .flatpickr-time input:focus { background: var(--ttsc-canvas-2); }

/* Campo com ícone */
.ttsc-date-field { position: relative; }
.ttsc-date-field > i { position: absolute; left: 10px; top: 50%; transform: translateY(-50%); z-index: 1; color: var(--ttsc-text-muted); pointer-events: none; }
.ttsc-date-field > .ttsc-input { padding-left: 32px; width: 100%; }
```

### JS

```js
// assets/js/core/ttsc.date.js — inicializa todos os input[data-ttsc-date]
flatpickr.localize(flatpickr.l10ns.pt);

const PRESETS = {
  single: { dateFormat: 'Y-m-d', altInput: true, altFormat: 'd/m/Y', allowInput: true },
  range:  { mode: 'range', dateFormat: 'Y-m-d', altInput: true, altFormat: 'd/m/Y', locale: { rangeSeparator: ' a ' } },
  time:   { enableTime: true, noCalendar: true, dateFormat: 'H:i', time_24hr: true, minuteIncrement: 5 },
  datetime: { enableTime: true, time_24hr: true, dateFormat: 'Y-m-d H:i', altInput: true, altFormat: 'd/m/Y H:i' },
};

export function initDates(root = document) {
  root.querySelectorAll('input[data-ttsc-date]:not(.flatpickr-input)').forEach((input) => {
    const preset = PRESETS[input.dataset.ttscDate] || PRESETS.single;
    flatpickr(input, {
      ...preset,
      altInputClass: 'ttsc-input',
      minDate: input.dataset.minDate || null,
      maxDate: input.dataset.maxDate || null,
      onReady(_, __, fp) {
        // acessibilidade: o campo visível herda rótulo/ajuda do original
        if (fp.altInput) {
          fp.altInput.id = `${input.id}-display`;
          document.querySelector(`label[for="${input.id}"]`)?.setAttribute('for', fp.altInput.id);
          if (input.getAttribute('aria-describedby')) fp.altInput.setAttribute('aria-describedby', input.getAttribute('aria-describedby'));
        }
      },
    });
  });
}
initDates();

// Fim do período nunca antes do início (dois campos separados)
const start = document.querySelector('#class-start')?._flatpickr;
const end = document.querySelector('#class-end')?._flatpickr;
start?.config.onChange.push(([date]) => end?.set('minDate', date || null));
```

### SQL

```sql
-- Período atual da turma para preencher o range
SELECT cl.uuid, cl.code, cl.start_date, cl.end_date
  FROM classes cl
 WHERE cl.uuid = :class_uuid AND cl.deleted_at IS NULL;

-- Salvar o período (o PHP separa "2027-02-01 a 2027-06-30" em :start_date / :end_date)
UPDATE classes
   SET start_date = :start_date, end_date = :end_date, updated_at = NOW()
 WHERE uuid = :class_uuid
   AND deleted_at IS NULL;
```

O input envia `Y-m-d` (ou `Y-m-d H:i`), formato que o `DomainCrudController` já aceita (“accept the HTML form's flatpickr output”) e normaliza; para range, o controller faz `explode(' a ', $period)` e rejeita (422) quando o início é maior que o fim.

## Faça / Não faça

- **Faça:** `altInput` com `d/m/Y` para o usuário e `Y-m-d` para o servidor.
- **Faça:** aplicar o tema por tokens — o CSS padrão do flatpickr é claro e fica ilegível no tema escuro.
- **Não faça:** mostrar formato americano ou depender do `type="date"` nativo.
- **Não faça:** usar flatpickr e Tempus Dominus na mesma tela.
