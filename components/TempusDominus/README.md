# TempusDominus

Seletor de data e hora **Tempus Dominus 6.9.4** (com **Popper 2.11.8**), localizado em pt-BR, com ícones Font Awesome Light e tema ligado aos tokens TTSC — para datas com hora (provas, eventos, aulas).

## Quando usar

- Data **e** hora no mesmo campo: agendamento de prova, evento institucional, reunião de conselho.
- Só hora com passos (início da aula a cada 5 min), via `viewMode: 'clock'`.
- Calendário inline em painéis de agendamento.
- **Prefira [Flatpickr](../Flatpickr/README.md)** para data simples, intervalo ou formulários comuns — é mais leve e é o formato que o `DomainCrudController` já normaliza.
- Para filtro de período com presets (“Últimos 7 dias”), use [DateRangePicker](../DateRangePicker/README.md).
- Não carregue Tempus Dominus e flatpickr na mesma tela.

## Anatomia

```
Data da avaliação
[ 03/11/2026 19:00            ][cal]   .ttsc-input-group  (data-td-target-input/toggle="nearest")
 ┌──────────────────────────────┐
 │ ‹   novembro de 2026      ›  │      .tempus-dominus-widget (popup Popper ou inline)
 │ dom seg ter qua qui sex sáb  │
 │  …   [3]  …                  │      dia ativo = ttsc-accent / ttsc-accent-on
 │ [hoje] [limpar] [hora] [fechar] │      toolbar com ícones fa-light
 └──────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Grupo | `.ttsc-input-group#id` + `data-td-target-input="nearest"` + `data-td-target-toggle="nearest"` | com botão |
| Campo | `input.ttsc-input[data-td-target="#id"]` (`autocomplete="off"`) | sim |
| Botão | `button[data-td-target="#id"][data-td-toggle="datetimepicker"]` + `aria-label` | não |
| Inline | `div` alvo com `display.inline: true` | não |
| Widget | `.tempus-dominus-widget` (gerado; `.light` forçado, tokens fazem o tema) | — |

## Variantes

| Modo | Opções principais |
|---|---|
| Data + hora (popup) | padrão, `localization.format: 'dd/MM/yyyy HH:mm'` |
| Inline | `display.inline: true` |
| Só data | `display.components: { clock: false }` + `format: 'dd/MM/yyyy'` |
| Só hora | `display.viewMode: 'clock'`, `components: { calendar: false, date: false, month: false, year: false, decades: false }`, `stepping: 5` |
| Intervalo | `dateRange: true` (prefira DateRangePicker para filtros) |

Tema: as variáveis `--td-*` “light” do plugin apontam para tokens (`--td-widget-background: ttsc-surface`, `--td-active-bg: ttsc-accent`, `--td-active-color: ttsc-accent-on`, `--td-btn-hover-bg: ttsc-canvas-2`…). Como os tokens trocam por `data-theme`, use **sempre** `display.theme: 'light'` — o tema escuro do plugin (`--td-dark-*`, azul) fica desligado.

## API

Global `tempusDominus` (UMD). Requer `window.Popper` carregado antes.

| Opção | Valor TTSC | Descrição |
|---|---|---|
| `localization` | objeto `ptBR` (ver JS) | `locale: 'pt-BR'`, `format`, `hourCycle: 'h23'`, `startOfTheWeek: 0`, rótulos traduzidos |
| `display.icons` | `fa-light …` | `type: 'icons'`, `time`, `date`, `up`, `down`, `previous`, `next`, `today`, `clear`, `close` |
| `display.theme` | `'light'` | ver tema acima |
| `display.buttons` | `{ today, clear, close }` | botões da toolbar |
| `display.inline` / `sideBySide` / `viewMode` / `components` | — | layout |
| `restrictions` | `minDate`, `maxDate`, `disabledDates`, `enabledDates`, `daysOfWeekDisabled`, `disabledHours` | bloqueios |
| `stepping` | `5` | minutos |
| `defaultDate`, `useCurrent`, `keepInvalid`, `allowInputToggle`, `container` | — | comportamento |

| Método (instância) | Descrição |
|---|---|
| `show()` · `hide()` · `toggle()` | popup |
| `dates.setValue(new tempusDominus.DateTime(...))` · `dates.clear()` · `dates.picked` · `dates.lastPicked` | valor |
| `updateOptions(obj, reset?)` | muda opções (ex.: `restrictions`) |
| `subscribe(evento, fn)` → `{ unsubscribe() }` | eventos |
| `dispose()` | destrói |

| Evento (`tempusDominus.Namespace.events.*`) | Nome DOM | `e` |
|---|---|---|
| `change` | `change.td` | `{ date, oldDate, isClear, isValid }` |
| `update` | `update.td` | mudança de visão |
| `error` | `error.td` | `{ reason, date, oldDate }` |
| `show` / `hide` | `show.td` / `hide.td` | — |

## Acessibilidade

- `<label for>` no input; botão do calendário com `aria-label="Abrir calendário"`.
- O campo aceita digitação no formato `dd/mm/aaaa hh:mm` (mostre o formato no `placeholder`); o calendário é auxiliar.
- Os botões do widget recebem `title` traduzido (via `localization`) — anunciados por leitores.
- Dia selecionado: `ttsc-accent` com `ttsc-accent-on` (9,6:1); hoje marcado com triângulo `ttsc-accent` além da cor.
- Datas bloqueadas usam `ttsc-meta` **e** cursor `not-allowed`; explique a regra no texto de ajuda (“Datas anteriores a hoje e feriados indisponíveis”).

## Modelos

### HTML

```html
<link rel="stylesheet" href="/assets/vendors/tempus-dominus/tempus-dominus.min.css">
<script src="/assets/vendors/popper/popper.min.js"></script>
<script src="/assets/vendors/tempus-dominus/tempus-dominus.min.js"></script>

<div class="flex flex-col gap-2">
  <label class="ttsc-form-label" for="exam-at">Data da avaliação</label>
  <div class="ttsc-input-group" id="exam-at-group" data-td-target-input="nearest" data-td-target-toggle="nearest">
    <input class="ttsc-input" id="exam-at" name="exam_at" type="text" autocomplete="off" placeholder="dd/mm/aaaa hh:mm"
           data-td-target="#exam-at-group" value="<?= $this->e($exam ? date('d/m/Y H:i', strtotime($exam['start_date'] . ' ' . $exam['start_time'])) : '') ?>">
    <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-icon" aria-label="Abrir calendário"
            data-td-target="#exam-at-group" data-td-toggle="datetimepicker"><i class="fa-light fa-calendar"></i></button>
  </div>
  <p class="text-xs text-muted-foreground">Datas anteriores a hoje, feriados e dias com outra prova ficam indisponíveis.</p>
  <script type="application/json" id="exam-blocked-dates"><?= json_encode(array_column($blockedDates, 'start_date')) ?></script>
</div>
```

### CSS

```css
/* assets/css/ttsc.css — tema Tempus Dominus por tokens (use display.theme: 'light') */
:root {
  --td-widget-background: var(--ttsc-surface);
  --td-font-color: var(--ttsc-text);
  --td-active-bg: var(--ttsc-accent);
  --td-active-color: var(--ttsc-accent-on);
  --td-active-border-color: var(--ttsc-surface);
  --td-range-bg: var(--ttsc-accent-soft);
  --td-btn-hover-bg: var(--ttsc-canvas-2);
  --td-disabled-color: var(--ttsc-meta);
  --td-alternate-color: var(--ttsc-text-muted);
  --td-secondary-border-color: var(--ttsc-border);
  --td-secondary-border-color-rgba: var(--ttsc-border);
  --td-primary-border-color: var(--ttsc-surface);
  --td-dow-color: var(--ttsc-text-muted);
  --td-text-shadow: none;
  --td-border-radius: var(--ttsc-radius-xs);
}
.tempus-dominus-widget { font-family: inherit; font-size: 13px; border: 1px solid var(--ttsc-border);
  border-radius: var(--ttsc-radius-control); box-shadow: var(--ttsc-shadow-popover); z-index: var(--ttsc-z-popover); }
.tempus-dominus-widget.inline { box-shadow: none; }
.tempus-dominus-widget .date-container-days .dow { font-size: 11px; text-transform: uppercase; }
.tempus-dominus-widget .date-container-days div.today::before { border-bottom-color: var(--ttsc-accent); }
.tempus-dominus-widget i { font-size: 14px; }
.tempus-dominus-widget .toolbar div i { color: var(--ttsc-text-2); }
```

### JS

```js
// assets/js/core/ttsc.tempus.js
const td = window.tempusDominus;

export const TD_PT_BR = {
  locale: 'pt-BR', format: 'dd/MM/yyyy HH:mm', hourCycle: 'h23', startOfTheWeek: 0,
  dayViewHeaderFormat: { month: 'long', year: 'numeric' },
  today: 'Ir para hoje', clear: 'Limpar seleção', close: 'Fechar',
  selectMonth: 'Selecionar mês', previousMonth: 'Mês anterior', nextMonth: 'Próximo mês',
  selectYear: 'Selecionar ano', previousYear: 'Ano anterior', nextYear: 'Próximo ano',
  selectDecade: 'Selecionar década', previousDecade: 'Década anterior', nextDecade: 'Próxima década',
  previousCentury: 'Século anterior', nextCentury: 'Próximo século',
  pickHour: 'Escolher hora', incrementHour: 'Mais uma hora', decrementHour: 'Menos uma hora',
  pickMinute: 'Escolher minuto', incrementMinute: 'Mais um minuto', decrementMinute: 'Menos um minuto',
  pickSecond: 'Escolher segundo', incrementSecond: 'Mais um segundo', decrementSecond: 'Menos um segundo',
  toggleMeridiem: 'AM/PM', selectTime: 'Selecionar hora', selectDate: 'Selecionar data',
};

export const TD_ICONS = {
  type: 'icons', time: 'fa-light fa-clock', date: 'fa-light fa-calendar', up: 'fa-light fa-chevron-up',
  down: 'fa-light fa-chevron-down', previous: 'fa-light fa-chevron-left', next: 'fa-light fa-chevron-right',
  today: 'fa-light fa-calendar-check', clear: 'fa-light fa-trash', close: 'fa-light fa-xmark',
};

export function ttscDateTime(el, options = {}) {
  return new td.TempusDominus(el, {
    ...options,
    localization: { ...TD_PT_BR, ...(options.localization || {}) },
    display: { icons: TD_ICONS, theme: 'light', buttons: { today: true, clear: true, close: true }, ...(options.display || {}) },
  });
}

// Data da avaliação: bloqueia passado + feriados/provas já marcadas
const group = document.getElementById('exam-at-group');
if (group) {
  const blocked = JSON.parse(document.getElementById('exam-blocked-dates').textContent || '[]')
    .map((iso) => new td.DateTime(`${iso}T00:00:00`));
  const picker = ttscDateTime(group, {
    stepping: 5,
    restrictions: { minDate: new td.DateTime(new Date().setHours(0, 0, 0, 0)), disabledDates: blocked, disabledHours: [0, 1, 2, 3, 4, 5, 6, 23] },
  });
  picker.subscribe(td.Namespace.events.change, (e) => {
    // envia ISO para o backend em um hidden: 2026-11-03 19:00
    const hidden = document.querySelector('input[name="exam_at_iso"]') || Object.assign(document.createElement('input'), { type: 'hidden', name: 'exam_at_iso' });
    group.closest('form')?.append(hidden);
    hidden.value = e.date ? e.date.format('yyyy-MM-dd HH:mm') : '';
  });
  picker.subscribe(td.Namespace.events.error, (e) => console.warn('Data inválida:', e.reason));
}
```

### SQL

```sql
-- Dias indisponíveis nos próximos 90 dias (feriados e provas já marcadas) → restrictions.disabledDates
SELECT DISTINCT e.start_date
  FROM events e
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid
   AND e.status <> 'cancelled'
   AND e.type IN ('holiday', 'exam')          -- tipos conforme ref_enum_events_type_*
   AND e.start_date BETWEEN CURDATE() AND CURDATE() + INTERVAL 90 DAY
 ORDER BY e.start_date;

-- Gravar a prova escolhida
INSERT INTO events (uuid, title, type, start_date, start_time, end_time, target_audience, status, unit_uuid, created_by)
VALUES (UUID(), :title, 'exam', :start_date, :start_time, :end_time, 'all', 'scheduled', :unit_uuid, :user_uuid);
```

O PHP passa `$blockedDates` para a view (JSON no `<script type="application/json">`) e, no POST, separa `exam_at_iso` (`Y-m-d H:i`) em `start_date`/`start_time`, calculando `end_time` pela duração da avaliação.

## Faça / Não faça

- **Faça:** `display.theme: 'light'` + variáveis `--td-*` em tokens (funciona nos dois temas).
- **Faça:** enviar ao servidor em ISO (`yyyy-MM-dd HH:mm`), exibir em `dd/MM/yyyy HH:mm`.
- **Não faça:** usar os ícones padrão `fa-solid` (o peso solid não é carregado — ficariam quadrados vazios).
- **Não faça:** esquecer o Popper antes do script (o popup não posiciona).
