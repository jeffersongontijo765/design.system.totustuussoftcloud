# ThirdPartyPlugin

Guia para integrar uma biblioteca de terceiros (flatpickr, Select2, FullCalendar, TinyMCE…) ao chassi TTSC: onde ficam os arquivos, ordem de carga, inicialização, tema por tokens, destruição e pt-BR.

## Quando usar

- Antes de trazer qualquer plugin novo para uma tela. Primeiro confira se o chassi já resolve: datas → `<input type="date">` (datepicker TTSC global, `assets/js/ttsc.datepicker.js`); select com busca → [AdvancedSelect](../AdvancedSelect/README.md); slider → [Slider](../Slider/README.md); repetidor → [Repeater](../Repeater/README.md).
- Só adote um plugin quando o recurso não existe no ttscui e a página realmente precisa dele (calendário completo, editor rico, gráficos).
- Páginas de cada plugin já documentado: [Flatpickr](../Flatpickr/README.md), [Select2](../Select2/README.md), [Tagify](../Tagify/README.md), [NoUiSlider](../NoUiSlider/README.md), [Inputmask](../Inputmask/README.md), [Autosize](../Autosize/README.md), [FullCalendar](../FullCalendar/README.md), [DataTables](../DataTables/README.md), [TinyMCE](../TinyMCE/README.md), [Quill](../Quill/README.md), [Dropzone](../Dropzone/README.md), [SweetAlert2](../SweetAlert2/README.md), [ApexCharts](../ApexCharts/README.md), [AmCharts](../AmCharts/README.md), [FormValidation](../FormValidation/README.md).

## Anatomia

```
assets/vendors/<plugin>/…             arquivos da lib (versão fixa, sem CDN)   ← DS: vendor/<plugin>/
assets/css/ttsc.<plugin>.css          tema por tokens (só var(--ttsc-*))
assets/js/core/ttsc.<plugin>.js       adaptador: init(root) / destroy(root) / i18n
view Plates  ── $this->start('scripts') → <script nonce src=vendors/…> → <script nonce src=core/ttsc.<plugin>.js>
                                                            ↑ depois da pilha base (ttsc.js → TTSC.init no DOMContentLoaded)
```

| Peça | Onde | Obrigatório |
|---|---|---|
| Arquivos da lib | app: `assets/vendors/<nome>/` (ex.: `chartjs/chart.umd.min.js`, `fullcalendar/`, `tinymce/`); DS: `vendor/<nome>/` | sim |
| Carga | `<script nonce="<?= \App\Security\CspNonce::get() ?>" src="<?= asset('vendors/…') ?>?v=<?= filemtime(…) ?>">` dentro de `$this->start('scripts')` | sim |
| Tema | CSS com tokens (`--ttsc-surface`, `--ttsc-text`, `--ttsc-border`, `--ttsc-accent`…), funcionando em `[data-theme=dark]` | sim |
| Adaptador | `init(root)` idempotente + `destroy(root)` | sim |
| Idioma | locale pt-BR do próprio plugin (`l10n/pt.js`, `language: 'pt-BR'`) | sim |
| Dados | endpoint JSON do controller — **nunca** acesso direto ao banco | quando há dados |

## Variantes

| Padrão de integração | Exemplo | Observação |
|---|---|---|
| Enriquecer campo nativo | flatpickr, Inputmask, autosize, Tagify | o `<input>` continua com `name` e valor; sem JS a tela funciona |
| Widget de página | FullCalendar, DataTables, ApexCharts | container vazio + `fetch` JSON |
| Editor | TinyMCE (`license_key: 'gpl'`, skin `oxide`/`oxide-dark` conforme tema), Quill | sincroniza um `<textarea name>` no submit |
| Depende de jQuery | Select2, daterangepicker, jsTree, toastr | carregue `jquery.min.js` antes; prefira alternativa sem jQuery |

## API

Contrato do adaptador (`assets/js/core/ttsc.<plugin>.js`) — o mesmo para todo plugin:

| Função | Faz |
|---|---|
| `init(root = document)` | encontra `[data-ttsc-<plugin>]` dentro de `root`, ignora os já marcados (`data-ttsc-<plugin>-initialized`), cria a instância e guarda em `ttscData.set(el, '<plugin>', inst)` |
| `destroy(root)` | para cada elemento inicializado: `inst.destroy()`, `ttscData.remove(el, '<plugin>')`, remove a marca |
| Opções por atributo | `data-ttsc-<plugin>-<opção>` (mesma convenção do ttscui: `ttsc.utils.parseDataAttribute` aceita `true`, números e JSON) |

Ganchos do chassi para chamar `init`/`destroy`:

| Momento | Evento |
|---|---|
| Página carregada | `DOMContentLoaded` (depois do `TTSC.init()` de `assets/js/ttsc.js`) |
| Drawer/modal do ttscui abriu / fechou | `shown` / `hidden` no elemento `[data-ttsc-drawer]` / `[data-ttsc-modal]` (bubbles) |
| Drawers do chassi (widget factory) | `ttsc:drawer:open` / `ttsc:drawer:close` no `document` |
| Conteúdo injetado via `fetch` | chame `init(container)` após inserir o HTML |

## Acessibilidade

- O plugin herda a obrigação do campo: `<label for>`, erro com `aria-invalid` + mensagem, foco visível com `ttsc-accent`.
- Verifique o teclado do plugin (flatpickr: setas no calendário, `Esc` fecha; Select2: digitação e setas). Se o plugin não for acessível, mantenha o campo nativo como alternativa (`allowInput: true`).
- O tema por tokens precisa manter ≥ 4,5:1 nos dois temas: texto `ttsc-text`/`ttsc-text-2`, dias fora do mês `ttsc-text-muted`, seleção `ttsc-accent` com texto `ttsc-accent-on`.

## Modelos

### HTML

```html
<!-- resources/views/app/pages/academic/events/form.php -->
<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="event-start">Início do evento</label>
  <input class="ttsc-input" id="event-start" name="start_date" data-ttsc-flatpickr
         data-ttsc-flatpickr-min-date="today" value="<?= $this->e($event['start_date'] ?? '') ?>">
</div>

<?php $this->start('scripts') ?>
<?php $nonce = \App\Security\CspNonce::get(); ?>
<link rel="stylesheet" href="<?= asset('vendors/flatpickr/flatpickr.min.css') ?>">
<link rel="stylesheet" href="<?= asset('css/ttsc.flatpickr.css') ?>?v=<?= filemtime(base_path('assets/css/ttsc.flatpickr.css')) ?>">
<script nonce="<?= $nonce ?>" src="<?= asset('vendors/flatpickr/flatpickr.min.js') ?>"></script>
<script nonce="<?= $nonce ?>" src="<?= asset('vendors/flatpickr/l10n/pt.js') ?>"></script>
<script nonce="<?= $nonce ?>" src="<?= asset('js/core/ttsc.flatpickr.js') ?>?v=<?= filemtime(base_path('assets/js/core/ttsc.flatpickr.js')) ?>"></script>
<?php $this->end() ?>
```

Ordem: CSS da lib → CSS de tema (sobrescreve) → JS da lib → locale → adaptador. Tudo com `nonce` (CSP sem `unsafe-inline`); nada de `onclick`/`<script>` inline sem nonce.

### CSS

```css
/* assets/css/ttsc.flatpickr.css — tema do flatpickr só com tokens (vale para claro e escuro) */
.flatpickr-calendar {
  background: var(--ttsc-surface);
  border: 1px solid var(--ttsc-border);
  border-radius: var(--ttsc-radius-surface);
  box-shadow: var(--ttsc-shadow-popover);
  color: var(--ttsc-text);
  font-family: inherit;
}
.flatpickr-calendar.arrowTop::before, .flatpickr-calendar.arrowTop::after { border-bottom-color: var(--ttsc-border); }
.flatpickr-months .flatpickr-month, .flatpickr-current-month .flatpickr-monthDropdown-months,
.flatpickr-current-month input.cur-year { color: var(--ttsc-text); fill: var(--ttsc-text); background: transparent; }
.flatpickr-months .flatpickr-prev-month, .flatpickr-months .flatpickr-next-month { color: var(--ttsc-text-2); fill: var(--ttsc-text-2); }
.flatpickr-months .flatpickr-prev-month:hover svg, .flatpickr-months .flatpickr-next-month:hover svg { fill: var(--ttsc-accent-text); }
span.flatpickr-weekday { color: var(--ttsc-text-muted); }
.flatpickr-day { color: var(--ttsc-text); border-radius: var(--ttsc-radius-sm); }
.flatpickr-day:hover, .flatpickr-day:focus { background: var(--ttsc-canvas-2); border-color: var(--ttsc-canvas-2); }
.flatpickr-day.today { border-color: var(--ttsc-accent-border); }
.flatpickr-day.selected, .flatpickr-day.startRange, .flatpickr-day.endRange,
.flatpickr-day.selected:hover { background: var(--ttsc-accent); border-color: var(--ttsc-accent); color: var(--ttsc-accent-on); }
.flatpickr-day.inRange { background: var(--ttsc-accent-soft); border-color: var(--ttsc-accent-soft); box-shadow: none; }
.flatpickr-day.prevMonthDay, .flatpickr-day.nextMonthDay { color: var(--ttsc-text-muted); }
.flatpickr-day.flatpickr-disabled, .flatpickr-day.flatpickr-disabled:hover { color: var(--ttsc-meta); }
```

### JS

```js
// assets/js/core/ttsc.flatpickr.js — adaptador padrão (init idempotente, destroy, pt-BR, opções por data-*)
(function (window, document) {
  'use strict';
  const KEY = 'flatpickr';
  const SELECTOR = '[data-ttsc-flatpickr]';

  function optionsFrom(el) {
    const opts = {};
    Object.keys(el.dataset).forEach((k) => {
      if (!k.startsWith('ttscFlatpickr') || k === 'ttscFlatpickr' || k === 'ttscFlatpickrInitialized') return;
      const name = k.replace('ttscFlatpickr', '');
      opts[name.charAt(0).toLowerCase() + name.slice(1)] = el.dataset[k];
    });
    return opts;
  }

  function init(root = document) {
    if (!window.flatpickr) return;
    root.querySelectorAll(SELECTOR).forEach((el) => {
      if (el.dataset.ttscFlatpickrInitialized === 'true') return;
      const inst = window.flatpickr(el, {
        locale: window.flatpickr.l10ns.pt,       // l10n/pt.js
        dateFormat: 'Y-m-d',                     // valor enviado ao servidor (DATE do MySQL)
        altInput: true, altFormat: 'd/m/Y',      // valor exibido em pt-BR
        allowInput: true,
        ...optionsFrom(el),
      });
      inst.altInput?.classList.add('ttsc-input');
      el.dataset.ttscFlatpickrInitialized = 'true';
      window.ttscData.set(el, KEY, inst);
    });
  }

  function destroy(root = document) {
    root.querySelectorAll(`${SELECTOR}[data-ttsc-flatpickr-initialized="true"]`).forEach((el) => {
      window.ttscData.get(el, KEY)?.destroy();
      window.ttscData.remove(el, KEY);
      delete el.dataset.ttscFlatpickrInitialized;
    });
  }

  document.addEventListener('DOMContentLoaded', () => init());            // depois do TTSC.init() do ttsc.js
  document.addEventListener('shown', (e) => init(e.target));               // drawer/modal ttscui abriu
  document.addEventListener('hidden', (e) => destroy(e.target));           // drawer/modal ttscui fechou
  document.addEventListener('ttsc:drawer:open', (e) => init(e.detail?.drawer || document));
  document.addEventListener('ttsc:drawer:close', (e) => destroy(e.detail?.drawer || document));

  window.TTSCFlatpickr = { init, destroy };
})(window, document);
```

### SQL

Plugin nenhum fala com o banco. O fluxo é sempre **plugin → `fetch` → controller (permissão + CSRF) → PDO com placeholders → JSON**. Exemplo: o FullCalendar pede `GET /api/v1/academic/events?start=2026-10-01&end=2026-11-01` e o controller executa:

```sql
SELECT e.uuid, e.title, e.type, e.start_date, e.end_date, e.start_time, e.end_time,
       e.location, e.color, e.status
  FROM events e
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid
   AND e.status <> 'cancelled'
   AND e.start_date < :range_end
   AND COALESCE(e.end_date, e.start_date) >= :range_start
 ORDER BY e.start_date, e.start_time;
```

O PHP converte cada linha no formato do plugin (`{id: uuid, title, start: "2026-10-12T08:00", end, color}`) e responde `application/json`. A cor vem do banco, mas o tema do calendário continua sendo tokens; o plugin nunca recebe credenciais, SQL ou nomes de tabela.

## Faça / Não faça

- **Faça:** versão fixa em `assets/vendors/`, `nonce` em todo `<script>`, adaptador com `init/destroy`, tema por tokens, locale pt-BR.
- **Faça:** destruir a instância ao fechar o drawer (popovers do plugin ficam presos no `body` e vazam memória).
- **Não faça:** CDN (CSP bloqueia e quebra offline); cores cruas no CSS de tema; inicializar antes do DOM do drawer existir; endpoint que devolve linhas cruas do banco sem passar pelo controller.
