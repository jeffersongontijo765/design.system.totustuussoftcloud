# DatePicker

Seletor de data padrão do chassi: `<input type="date" class="ttsc-input">` aprimorado automaticamente pelo **TTSCDatepicker** (implementação TTSC, `assets/js/ttsc.datepicker.js` + `assets/css/ttsc.datepicker.css`), com calendário em pt-BR, teclado completo e valor `YYYY-MM-DD` no próprio input.

## Quando usar

- Qualquer campo de data simples: data da matrícula, vencimento, nascimento, início/fim de período letivo.
- Intervalo com dois campos (“de/até”) usando `min`/`max` ligados entre si (ver JS).
- Precisa de hora, intervalos num único campo, datas desabilitadas por regra ou múltiplas datas? Use os plugins: [Flatpickr](../Flatpickr/README.md) (data/hora, `disable`, `mode: "range"`), [TempusDominus](../TempusDominus/README.md) (data + hora com relógio) ou [DateRangePicker](../DateRangePicker/README.md) (intervalos com atalhos “Últimos 30 dias” em relatórios).
- **Não use** para ano/mês isolados (competência): use `<select>` de mês + ano ou `type="month"` com `data-no-datepicker`.

## O que existe no chassi (verificado)

| Peça | Situação |
|---|---|
| ttscui (`ttscui.js`) | **sem** módulo de datepicker (componentes: accordion … tooltip; nenhum `datepicker`) |
| `bundle.css` / runtime | traz CSS `.vc-*` do vanilla-calendar (`[data-vc-theme]`), mas **sem JS** correspondente; não há `.ttsc-datepicker` |
| Repositório | `ttsc.datepicker.js` (TTSCDatepicker 1.0.0) + `ttsc.datepicker.css` (`.ttsc-dp*`), carregados em `layouts/main.php` para todas as páginas |

## Anatomia

```
┌ input[type=date].ttsc-input.ttsc-dp-input  [ 15/03/2026     📅 ] ┐   ← valor real "2026-03-15"
└───────────────────────────────────────────────────────────────────┘
┌ .ttsc-dp (popup fixo no <body>, role="dialog") ──┐
│ «  ‹      março 2026      ›  »                  │  .ttsc-dp__head / __nav / __title (__month __year)
│ D  S  T  Q  Q  S  S                             │  .ttsc-dp__weekdays
│ 1  2  3 … [15] …                                 │  .ttsc-dp__grid > button.ttsc-dp__day (.is-today .is-selected .is-outside .is-focus)
│ Limpar                                  Hoje     │  .ttsc-dp__foot (.ttsc-dp__clear / .ttsc-dp__today)
└──────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Campo | `input[type="date"].ttsc-input` | sim |
| Marcação do motor | `.ttsc-dp-input`, `data-ttsc-dp-enhanced="true"`, `aria-haspopup="dialog"`, `aria-expanded` | automático |
| Limites | `min` / `max` nativos (`YYYY-MM-DD`) | não |
| Opt-out | `data-no-datepicker` | não |
| Popup | `.ttsc-dp` único, `position: fixed`, `z-index` ≥ 1100 (acima do drawer mais próximo) | automático |

## Estados

| Estado | Classe | Tokens |
|---|---|---|
| Hoje | `.is-today` | fundo `ttsc-accent-soft`, texto `ttsc-accent-text`, anel `ttsc-accent-border` |
| Selecionado | `.is-selected` | fundo `ttsc-accent`, texto `ttsc-accent-on` (o CSS do repo usa branco = 2,1:1; corrigido abaixo) |
| Cursor de teclado | `.is-focus` | contorno 2px `ttsc-accent` |
| Fora do mês | `.is-outside` | opacidade 38% |
| Fora de min/max | `[disabled]` (extensão) | opacidade 30%, sem clique |
| Campo inválido | `aria-invalid="true"` | borda `ttsc-danger` ([Forms](../Forms/README.md)) |

## API

| `window.TTSCDatepicker` | Descrição |
|---|---|
| `initAll(root?)` | aprimora todos os `input[type=date]` dentro de `root` (já roda no `DOMContentLoaded` e via `MutationObserver` para drawers/tabelas renderizados depois) |
| `enhance(input)` | aprimora um input |
| `open(input)` | abre o popup ancorado ao input |
| `closeAll()` | fecha o popup |
| `isOpen()` | `true` se aberto |
| `version` | `"1.0.0"` |

| Evento | Alvo | Quando |
|---|---|---|
| `input` e `change` (nativos, borbulham) | o próprio input | ao escolher dia, “Hoje” ou “Limpar” — listeners existentes continuam funcionando |

| Teclado (foco fica no input) | Ação |
|---|---|
| ← → / ↑ ↓ | dia / semana |
| PageUp / PageDown (+Shift) | mês (ano) |
| Home / End | início / fim do mês |
| Enter | confirma o dia do cursor |
| Esc / Tab | fecha |

| i18n | Descrição |
|---|---|
| `window.__ttscDatepickerI18N = { months, weekdays, today, clear, prevMonth, nextMonth, prevYear, nextYear, dialogLabel }` | substitui rótulos (padrão pt-BR) |
| `window.__('ttsc_dp_<chave>')` | ponte de i18n do app, usada se existir |

## Acessibilidade

- O input nativo continua sendo o campo: `<label for>`, `required`, `min`/`max` e validação nativa valem normalmente.
- Popup `role="dialog"` com `aria-label="Selecionar data"`; o input ganha `aria-expanded`. O foco **não** sai do input — o cursor de dia é visual (`.is-focus`) e operado pelas setas.
- Botões de navegação têm `aria-label` (“Mês anterior”, “Próximo ano”); dias têm `aria-label` com a data por extenso (extensão abaixo).
- Formato exibido segue o locale do navegador; documente o formato na dica (“dd/mm/aaaa”).

## Modelos

### HTML

```html
<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="enrollment-date">Data da matrícula</label>
  <input type="date" class="ttsc-input" id="enrollment-date" name="enrollment_date" required
         value="<?= $this->e($enrollment['enrollment_date'] ?? date('Y-m-d')) ?>"
         min="<?= $this->e($period['start_date']) ?>" max="<?= $this->e($period['end_date']) ?>"
         aria-describedby="enrollment-date-hint">
  <div class="ttsc-form-description" id="enrollment-date-hint">Dentro do período letivo vigente.</div>
</div>

<!-- Intervalo de/até (filtro da agenda de eventos) -->
<div class="grid grid-cols-2 gap-3" data-ttsc-date-range>
  <input type="date" class="ttsc-input" name="from" aria-label="Data inicial" data-range-start>
  <input type="date" class="ttsc-input" name="to" aria-label="Data final" data-range-end>
</div>

<!-- Competência: sem o calendário de dia -->
<input type="month" class="ttsc-input" name="competence" data-no-datepicker aria-label="Competência">
```

### CSS

`ttsc.datepicker.css` já lê `--ttsc-surface`, `--ttsc-border`, `--ttsc-text`, `--ttsc-accent`, `--ttsc-radius-*` e `--ttsc-shadow-popover`. Ajustes de contraste e de limites:

```css
.ttsc-dp { --dp-muted: var(--ttsc-text-muted); --dp-accent-strong: var(--ttsc-accent-text); }
.ttsc-dp__day.is-selected,
.ttsc-dp__day.is-selected:hover { background: var(--ttsc-accent); color: var(--ttsc-accent-on); }
.ttsc-dp__day.is-today { color: var(--ttsc-accent-text); background: var(--ttsc-accent-soft); box-shadow: inset 0 0 0 1px var(--ttsc-accent-border); }
.ttsc-dp__day[disabled] { opacity: .3; cursor: not-allowed; background: transparent; }
.ttsc-dp__today { color: var(--ttsc-accent-text); }
.ttsc-dp__clear { color: var(--ttsc-text-muted); }
/* Ícone do campo: currentColor em vez do SVG cinza fixo */
input[type="date"].ttsc-dp-input { color-scheme: light dark; }
```

### JS

O motor já se inicializa sozinho. O que a página acrescenta — limites a partir do servidor, intervalo encadeado, dias fora do intervalo desabilitados e rótulos acessíveis:

```js
// assets/js/core/ttsc.date-range.js — encadeia "de/até" e respeita min/max no calendário
export function bindDateRange(root) {
  const start = root.querySelector('[data-range-start]');
  const end = root.querySelector('[data-range-end]');
  start.addEventListener('change', () => {
    end.min = start.value || '';
    if (end.value && start.value && end.value < start.value) {
      end.value = start.value;
      end.dispatchEvent(new Event('change', { bubbles: true }));
    }
  });
  end.addEventListener('change', () => { start.max = end.value || ''; });
}
document.querySelectorAll('[data-ttsc-date-range]').forEach(bindDateRange);

// Pós-processa cada render do popup: desabilita dias fora de min/max e dá nome por extenso
const fmt = new Intl.DateTimeFormat('pt-BR', { dateStyle: 'full' });
new MutationObserver(() => {
  const panel = document.querySelector('.ttsc-dp:not([hidden])');
  const input = document.querySelector('input.ttsc-dp-input[aria-expanded="true"]');
  if (!panel || !input) return;
  panel.querySelectorAll('.ttsc-dp__day[data-date]').forEach((b) => {
    const d = b.dataset.date;
    b.disabled = (input.min && d < input.min) || (input.max && d > input.max);
    b.setAttribute('aria-label', fmt.format(new Date(`${d}T12:00:00`)));
  });
}).observe(document.body, { subtree: true, childList: true });

// Abrir programaticamente (ex.: atalho "Alterar vencimento" na linha da tabela)
document.querySelector('#btn-change-due')?.addEventListener('click', () => {
  window.TTSCDatepicker.open(document.querySelector('#due-date'));
});
```

### SQL

`min`/`max` vêm do período letivo vigente da unidade; a agenda filtra eventos que **intersectam** o intervalo escolhido:

```sql
-- Limites do campo "Data da matrícula"
SELECT start_date, end_date
  FROM academic_periods
 WHERE is_current = 1
   AND deleted_at IS NULL
   AND (unit_uuid = :unit_uuid OR unit_uuid IS NULL)
 ORDER BY start_date DESC
 LIMIT 1;

-- Eventos no intervalo de/até (end_date nulo = evento de um dia)
SELECT uuid, title, start_date, COALESCE(end_date, start_date) AS end_date, color
  FROM events
 WHERE deleted_at IS NULL
   AND unit_uuid = :unit_uuid
   AND start_date <= :to
   AND COALESCE(end_date, start_date) >= :from
 ORDER BY start_date;
```

O PHP recebe `from`/`to` já em `YYYY-MM-DD` (valor nativo do input), valida com `DateTimeImmutable::createFromFormat('!Y-m-d', …)` e grava em colunas `date` sem conversão de fuso.

## Faça / Não faça

- **Faça:** manter o input nativo como fonte do valor e ouvir `change`.
- **Faça:** usar `min`/`max` do servidor e revalidar no backend.
- **Não faça:** carregar flatpickr só para escolher um dia — o motor do chassi já está em todas as páginas.
- **Não faça:** máscara de texto `dd/mm/aaaa` em campo de data; use `type="date"`.
