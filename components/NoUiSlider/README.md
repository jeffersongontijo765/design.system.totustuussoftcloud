# NoUiSlider

Controle deslizante de valor único ou faixa com noUiSlider 15.8.1, com tooltips, marcas (pips) e formatação pt-BR (R$, anos, %), tematizado por tokens.

## Quando usar

- Filtros por **faixa**: mensalidade (R$ 800 a R$ 2.200), idade do aluno, carga horária.
- Parâmetros com escala visual e limites claros: frequência mínima para aprovação (75%).
- **Não use** quando o valor exato importa mais que a posição (valor de boleto, CPF): use [Inputmask](../Inputmask/README.md) ou [Dialer](../Dialer/README.md).
- O [Range Slider](../RangeSlider/README.md) do ttscui (`input[type=range]`) basta para um valor único simples sem tooltip; use noUiSlider para **dois puxadores**, pips ou formato monetário.

## Anatomia

```
Faixa de mensalidade                         R$ 800 a R$ 2.200   ← rótulo + resumo (aria-live)
          [R$ 800]               [R$ 2.200]                      ← .noUi-tooltip
  ────────●━━━━━━━━━━━━━━━━━━━━━━●──────────                     ← .noUi-target / .noUi-connect / .noUi-handle
  |    '    |    '    |    '    |    '    |                       ← .noUi-pips (.noUi-marker / .noUi-value)
 R$ 0     R$ 1.000  R$ 2.000  R$ 3.000  R$ 4.000
```

| Parte | Classe | Obrigatório |
|---|---|---|
| Wrapper TTSC | `.ttsc-range` (+ `.has-pips`, `.no-tip`) — reserva espaço para tooltip e pips | sim |
| Alvo | `div` passado a `noUiSlider.create` → `.noUi-target` | sim |
| Trilho preenchido | `.noUi-connect` (opção `connect`) | não |
| Puxador | `.noUi-handle` com `aria-label` (`handleAttributes`) | sim |
| Tooltip | `.noUi-tooltip` (opção `tooltips`) | não |
| Marcas | `.noUi-pips` (opção `pips`) | não |
| Campos ocultos | `input[type=hidden]` sincronizados no `change` | sim em formulários |

## Variantes

| Variante | Opções | Tokens |
|---|---|---|
| Faixa | `start: [a, b], connect: true` | trilho `ttsc-surface-2`, faixa `ttsc-accent` |
| Valor único | `start: v, connect: 'lower'` | idem |
| Com tooltip | `tooltips: true` ou `[fmt, fmt]` | fundo `ttsc-text`, texto `ttsc-surface` (inverso, ≥ 15:1) |
| Com pips | `pips: { mode: 'values', values: [...] }` | marcas `ttsc-border-strong`/`ttsc-meta`, texto `ttsc-text-muted` |
| Desabilitado | `slider.disable()` → atributo `disabled` | opacidade 50% |

## API

Opções (noUiSlider 15.8.1):

| Opção | Exemplo | Descrição |
|---|---|---|
| `start` | `[800, 2200]` | Valores iniciais (um por puxador) |
| `range` | `{ min: 0, max: 4000 }` | Limites; aceita pontos intermediários (`'50%': 1000`) para escala não linear |
| `step` | `50` | Passo |
| `margin` / `limit` | `100` / `2000` | Distância mínima / máxima entre puxadores |
| `connect` | `true`, `'lower'`, `[false, true, false]` | Trilho preenchido |
| `format` | `{ to(v), from(s) }` | Formata `get()` e eventos (use `Intl.NumberFormat('pt-BR')`) |
| `tooltips` | `true` ou formatador por puxador | Balões com o valor |
| `pips` | `{ mode: 'values', values, density, format }` | Marcas da escala |
| `handleAttributes` | `[{ 'aria-label': 'Mensalidade mínima' }, …]` | Atributos ARIA por puxador |
| `keyboardSupport` / `keyboardPageMultiplier` | `true` / `5` | Teclado |
| `behaviour` | `'tap-drag'` | Interação com o trilho |

Métodos (`el.noUiSlider.*`): `get(unencoded?)`, `set(values)`, `setHandle(i, v)`, `reset()`, `disable(i?)`, `enable(i?)`, `updateOptions(opts, fireSet?)`, `on(evento, fn)`, `off(evento)`, `destroy()`.

Eventos: `update` (contínuo, inclusive na criação), `slide` (arrastando), `change` (soltou — use para filtrar/consultar), `set`, `start`, `end`. Assinatura `(values, handle, unencoded, tap, positions)`.

## Acessibilidade

- Puxadores recebem `role="slider"`, `aria-valuemin/max/now` e `aria-valuetext` (valor formatado) automaticamente; dê `aria-label` distinto a cada um via `handleAttributes`.
- Teclado: setas mudam um passo, `PageUp`/`PageDown` vários passos, `Home`/`End` vão aos limites.
- Resumo textual ao lado do rótulo (“R$ 800 a R$ 2.200”) com `aria-live="polite"` para quem não vê os tooltips.
- Foco visível: contorno 2px `ttsc-accent` com offset; puxador ativo ganha halo `ttsc-accent-soft`.

## Modelos

### HTML

```html
<form method="get" action="/academic/courses" class="flex flex-col gap-2">
  <div class="flex items-center justify-between">
    <label class="ttsc-form-label" id="lbl-fee">Faixa de mensalidade</label>
    <span class="text-sm" id="val-fee" aria-live="polite"></span>
  </div>
  <div class="ttsc-range has-pips">
    <div id="sl-fee" data-min="<?= (int) $range['range_min'] ?>" data-max="<?= (int) $range['range_max'] ?>"></div>
  </div>
  <input type="hidden" name="fee_min" value="<?= (int) ($filters['fee_min'] ?? $range['range_min']) ?>">
  <input type="hidden" name="fee_max" value="<?= (int) ($filters['fee_max'] ?? $range['range_max']) ?>">
</form>
```

### CSS

```css
/* assets/css/ttsc.nouislider.css — carregar depois de vendor/nouislider/nouislider.min.css */
.ttsc-range { padding: 36px 28px 6px; }
.ttsc-range.no-tip { padding-top: 16px; }
.ttsc-range.has-pips { padding-bottom: 40px; }
.ttsc-range .noUi-target { background: var(--ttsc-surface-2); border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-pill); box-shadow: none; }
.ttsc-range .noUi-horizontal { height: 6px; }
.ttsc-range .noUi-connects { border-radius: var(--ttsc-radius-pill); }
.ttsc-range .noUi-connect { background: var(--ttsc-accent); }
.ttsc-range .noUi-horizontal .noUi-handle {
  width: 18px; height: 18px; right: -9px; top: -7px; border-radius: 50%; cursor: grab;
  border: 2px solid var(--ttsc-accent); background: var(--ttsc-surface); box-shadow: var(--ttsc-shadow-sm);
}
.ttsc-range .noUi-handle::before, .ttsc-range .noUi-handle::after { display: none; }
.ttsc-range .noUi-handle:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.ttsc-range .noUi-active { box-shadow: 0 0 0 4px var(--ttsc-accent-soft); cursor: grabbing; }
.ttsc-range .noUi-tooltip {
  bottom: 140%; padding: 2px 8px; border: 0; border-radius: var(--ttsc-radius-sm);
  font-size: 12px; font-weight: 500; font-variant-numeric: tabular-nums;
  color: var(--ttsc-surface); background: var(--ttsc-text);
}
.ttsc-range .noUi-pips { color: var(--ttsc-text-muted); font-size: 11px; }
.ttsc-range .noUi-value-horizontal { transform: translate(-50%, 12px); }
.ttsc-range .noUi-marker { background: var(--ttsc-border-strong); }
.ttsc-range .noUi-marker-large { background: var(--ttsc-meta); }
.ttsc-range [disabled].noUi-target { opacity: .5; }
.ttsc-range [disabled] .noUi-handle { cursor: not-allowed; }
```

### JS

```js
// assets/js/core/ttsc.range-filter.js — requer vendor/nouislider/nouislider.min.js
const brl = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 });
const fmtBRL = {
  to: (v) => brl.format(v),
  from: (s) => Number(String(s).replace(/[^\d,]/g, '').replace(',', '.')),
};

const el = document.getElementById('sl-fee');
const form = el.closest('form');
const [inMin, inMax] = [form.elements.fee_min, form.elements.fee_max];
const min = +el.dataset.min || 0;
const max = Math.max(+el.dataset.max || 4000, min + 100);

noUiSlider.create(el, {
  start: [+inMin.value, +inMax.value],
  connect: true,
  step: 50,
  margin: 100,
  range: { min, max },
  format: fmtBRL,
  tooltips: [fmtBRL, fmtBRL],
  pips: { mode: 'count', values: 5, density: 5, format: fmtBRL },
  handleAttributes: [{ 'aria-label': 'Mensalidade mínima' }, { 'aria-label': 'Mensalidade máxima' }],
});

el.noUiSlider.on('update', (values) => {
  document.getElementById('val-fee').textContent = `${values[0]} a ${values[1]}`;
});
// "change" só quando o usuário solta: evita uma consulta por pixel
el.noUiSlider.on('change', (_values, _handle, unencoded) => {
  inMin.value = Math.round(unencoded[0]);
  inMax.value = Math.round(unencoded[1]);
  form.requestSubmit();
});
```

### SQL

```sql
-- Limites do slider (preço vem de academic_billing_rules.monthly_tuition, por curso). MariaDB 10.11 / MySQL 8
SELECT FLOOR(MIN(r.monthly_tuition)) AS range_min,
       CEIL(MAX(r.monthly_tuition))  AS range_max
  FROM academic_billing_rules r
  JOIN courses c ON c.uuid = r.course_uuid AND c.deleted_at IS NULL
 WHERE r.status = 'active'
   AND c.unit_uuid = :unit_uuid;

-- Cursos dentro da faixa escolhida
SELECT c.uuid, c.code, c.name, r.monthly_tuition
  FROM courses c
  JOIN academic_billing_rules r ON r.course_uuid = c.uuid AND r.status = 'active'
 WHERE c.unit_uuid = :unit_uuid
   AND c.is_active = 1
   AND c.deleted_at IS NULL
   AND r.monthly_tuition BETWEEN :fee_min AND :fee_max
 ORDER BY r.monthly_tuition;

-- Faixa de idade (6 a 14 anos) sem calcular idade linha a linha: compara datas e usa índice
SELECT e.uuid, e.code, TIMESTAMPDIFF(YEAR, ui.birth_date, CURDATE()) AS age
  FROM enrollments e
  JOIN user_identity ui ON ui.user_uuid = e.student_uuid
 WHERE e.status = 'active'
   AND e.deleted_at IS NULL
   AND ui.birth_date BETWEEN DATE_SUB(CURDATE(), INTERVAL :age_max + 1 YEAR) + INTERVAL 1 DAY
                         AND DATE_SUB(CURDATE(), INTERVAL :age_min YEAR);
```

O PHP passa `range_min`/`range_max` em `data-min`/`data-max` e os filtros atuais nos `input[type=hidden]`; sem regras de cobrança (`NULL`), usa 0–4000. O servidor faz `(int)` e `min()`/`max()` nos parâmetros antes do `BETWEEN`.

## Faça / Não faça

- **Faça:** consultar no evento `change` (soltou), não no `update`.
- **Faça:** `aria-label` por puxador e resumo textual visível.
- **Faça:** limites vindos do banco e `margin` para os puxadores não se cruzarem.
- **Não faça:** usar o slider para valores exatos com muitas casas; ofereça também campos numéricos se a precisão importa.
- **Não faça:** manter o puxador padrão do noUiSlider (claro com sombra) — no tema escuro ele some no fundo; use os tokens acima.
