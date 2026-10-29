# Dialer

Campo numérico com botões − / + (implementação TTSC, JS puro), com mínimo, máximo, passo, casas decimais e prefixo como `R$ `, formatado em pt-BR.

## Quando usar

- Ajustar números pequenos e limitados por passos conhecidos: vagas por turma (`courses.max_students`), duração em períodos, quantidade de parcelas, mensalidade em degraus de R$ 50,00.
- Quando o usuário costuma mudar o valor em poucas unidades a partir de um padrão.
- **Não use** para valores livres e longos (CPF, valor exato de boleto): use [Inputmask](../Inputmask/README.md).
- **Não use** para escolher uma faixa (mín.–máx.) ou um valor numa escala visual: use [NoUiSlider](../NoUiSlider/README.md).

## Anatomia

```
[ − ][   R$ 1.250,00   ][ + ]      .ttsc-dialer[data-ttsc-dialer]
 dec        input           inc
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Container | `.ttsc-dialer[data-ttsc-dialer]` | sim |
| Botão diminuir | `button.ttsc-btn.ttsc-btn-outline.ttsc-btn-icon[data-ttsc-dialer-control="decrease"]` + `aria-label` | sim |
| Campo | `input.ttsc-input[data-ttsc-dialer-input]` com `name` e rótulo (`aria-labelledby`) | sim |
| Botão aumentar | `button…[data-ttsc-dialer-control="increase"]` + `aria-label` | sim |
| Ícones | `fa-light fa-minus` / `fa-light fa-plus` | sim |

## Variantes

| Variante | Configuração | Exemplo | Tokens |
|---|---|---|---|
| Inteiro | `data-ttsc-dialer-step="5"` | Vagas: 40 | borda `ttsc-border` (via `--input`), texto `ttsc-text` |
| Monetário | `data-ttsc-dialer-decimals="2"` + `data-ttsc-dialer-prefix="R$ "` | R$ 1.250,00 | idem; `font-variant-numeric: tabular-nums` |
| Com sufixo | `data-ttsc-dialer-suffix=" h"` | 360 h | idem |

## Estados

| Estado | Como aparece |
|---|---|
| No mínimo / no máximo | o botão correspondente recebe `disabled` (50% de opacidade) |
| Desabilitado | `disabled` no input e nos dois botões |
| Foco | anel do `.ttsc-input` (`--ring` = `ttsc-accent`) |
| Valor fora da faixa digitado | corrigido para o limite no `blur` e reformatado |

## API

Atributos (lidos na inicialização):

| Atributo | Padrão | Descrição |
|---|---|---|
| `data-ttsc-dialer-min` | `-Infinity` | Valor mínimo |
| `data-ttsc-dialer-max` | `Infinity` | Valor máximo |
| `data-ttsc-dialer-step` | `1` | Incremento dos botões e das setas |
| `data-ttsc-dialer-decimals` | `0` | Casas decimais exibidas e arredondadas |
| `data-ttsc-dialer-prefix` / `-suffix` | `''` | Texto antes/depois do número (ex.: `R$ `) |

Métodos (instância em `el.ttscDialer` ou `TTSCDialer.getInstance(el)`):

| Método | Descrição |
|---|---|
| `TTSCDialer.init(root?)` | Inicializa todos os `[data-ttsc-dialer]` de `root` (idempotente) |
| `new TTSCDialer(el, opts?)` | Cria com opções `{min, max, step, decimals, prefix, suffix}` que sobrepõem os atributos |
| `getValue()` | Número cru (ex.: `1250`) |
| `setValue(n, silent?)` | Aplica limites, arredonda e formata; `silent` não dispara evento |
| `increase()` / `decrease()` | Soma / subtrai `step` |

Evento:

| Evento | `detail` | Quando |
|---|---|---|
| `ttsc.dialer.change` (bubbles) | `{ value, formatted }` | Valor mudou por botão, teclado ou digitação |

## Acessibilidade

- O input recebe `role="spinbutton"`, `aria-valuemin`, `aria-valuemax`, `aria-valuenow` e `aria-valuetext` (“R$ 1.250,00”).
- Teclado: `↑`/`↓` somam/subtraem o passo, `PageUp`/`PageDown` 10 passos, `Home`/`End` vão aos limites.
- Botões só-ícone sempre com `aria-label` específico (“Aumentar vagas”), não apenas “+”.
- O input é `type="text"` com `inputmode="numeric|decimal"` para aceitar a vírgula pt-BR e o prefixo; o servidor recebe o valor formatado e normaliza.

## Modelos

### HTML

```html
<div class="flex flex-col gap-2">
  <label id="lbl-max-students" class="ttsc-form-label">Vagas por turma</label>
  <div class="ttsc-dialer" data-ttsc-dialer
       data-ttsc-dialer-min="<?= (int) $minAllowed ?>" data-ttsc-dialer-max="200" data-ttsc-dialer-step="5">
    <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-icon" data-ttsc-dialer-control="decrease" aria-label="Diminuir vagas">
      <i class="fa-light fa-minus"></i>
    </button>
    <input type="text" class="ttsc-input" name="max_students" inputmode="numeric"
           value="<?= $this->e($course['max_students'] ?? 40) ?>" aria-labelledby="lbl-max-students" data-ttsc-dialer-input>
    <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-icon" data-ttsc-dialer-control="increase" aria-label="Aumentar vagas">
      <i class="fa-light fa-plus"></i>
    </button>
  </div>
  <p class="ds-note">Não pode ser menor que o total de alunos já matriculados na maior turma.</p>
</div>

<!-- Monetário -->
<div class="ttsc-dialer" data-ttsc-dialer data-ttsc-dialer-min="0" data-ttsc-dialer-step="50"
     data-ttsc-dialer-decimals="2" data-ttsc-dialer-prefix="R$ ">
  <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-icon" data-ttsc-dialer-control="decrease" aria-label="Diminuir mensalidade"><i class="fa-light fa-minus"></i></button>
  <input type="text" class="ttsc-input" name="tuition_amount" inputmode="decimal" value="1250.00" aria-label="Mensalidade" data-ttsc-dialer-input>
  <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-icon" data-ttsc-dialer-control="increase" aria-label="Aumentar mensalidade"><i class="fa-light fa-plus"></i></button>
</div>
```

### CSS

```css
/* assets/css/ttsc.dialer.css — junta botão + input + botão num único controle */
.ttsc-dialer { display: inline-flex; align-items: stretch; }
.ttsc-dialer .ttsc-input {
  width: 128px; text-align: center; border-radius: 0;
  font-variant-numeric: tabular-nums;
}
.ttsc-dialer > .ttsc-btn:first-child { border-start-end-radius: 0; border-end-end-radius: 0; border-inline-end-width: 0; }
.ttsc-dialer > .ttsc-btn:last-child  { border-start-start-radius: 0; border-end-start-radius: 0; border-inline-start-width: 0; }
.ttsc-dialer [data-ttsc-dialer-control]:disabled { opacity: .5; cursor: not-allowed; }

/* Extensão: versão compacta para linhas de tabela */
.ttsc-dialer.ttsc-dialer-sm .ttsc-input { width: 72px; height: var(--ttsc-row-compact); }
.ttsc-dialer.ttsc-dialer-sm .ttsc-btn { height: var(--ttsc-row-compact); width: var(--ttsc-row-compact); }
```

### JS

```js
// assets/js/core/ttsc.dialer.js — implementação TTSC (sem dependências)
(function (w) {
  'use strict';
  function TTSCDialer(el, opts) {
    if (el.ttscDialer) return el.ttscDialer;
    var d = el.dataset;
    this.el = el;
    this.input = el.querySelector('[data-ttsc-dialer-input]');
    this.dec = el.querySelector('[data-ttsc-dialer-control="decrease"]');
    this.inc = el.querySelector('[data-ttsc-dialer-control="increase"]');
    this.o = Object.assign({
      min: d.ttscDialerMin !== undefined ? +d.ttscDialerMin : -Infinity,
      max: d.ttscDialerMax !== undefined ? +d.ttscDialerMax : Infinity,
      step: +(d.ttscDialerStep || 1),
      decimals: +(d.ttscDialerDecimals || 0),
      prefix: d.ttscDialerPrefix || '',
      suffix: d.ttscDialerSuffix || ''
    }, opts || {});
    this.fmt = new Intl.NumberFormat('pt-BR', { minimumFractionDigits: this.o.decimals, maximumFractionDigits: this.o.decimals });
    this.input.setAttribute('role', 'spinbutton');
    if (isFinite(this.o.min)) this.input.setAttribute('aria-valuemin', this.o.min);
    if (isFinite(this.o.max)) this.input.setAttribute('aria-valuemax', this.o.max);
    var self = this;
    this.dec.addEventListener('click', function () { self.decrease(); });
    this.inc.addEventListener('click', function () { self.increase(); });
    this.input.addEventListener('keydown', function (e) {
      var k = { ArrowUp: 1, ArrowDown: -1, PageUp: 10, PageDown: -10 }[e.key];
      if (k) { e.preventDefault(); self.setValue(self.getValue() + k * self.o.step); }
      if (e.key === 'Home' && isFinite(self.o.min)) { e.preventDefault(); self.setValue(self.o.min); }
      if (e.key === 'End' && isFinite(self.o.max)) { e.preventDefault(); self.setValue(self.o.max); }
    });
    this.input.addEventListener('blur', function () { self.setValue(self.parse(self.input.value)); });
    this.setValue(this.parse(this.input.value), true);
    el.ttscDialer = this;
  }
  TTSCDialer.prototype.parse = function (text) {
    var s = String(text).replace(this.o.prefix, '').replace(this.o.suffix, '').replace(/\s/g, '');
    if (s.indexOf(',') > -1) s = s.replace(/\./g, '').replace(',', '.');   // 1.250,00 → 1250.00
    var n = parseFloat(s);
    return isNaN(n) ? (isFinite(this.o.min) ? this.o.min : 0) : n;
  };
  TTSCDialer.prototype.getValue = function () { return this.value; };
  TTSCDialer.prototype.setValue = function (v, silent) {
    var f = Math.pow(10, this.o.decimals);
    v = Math.round(Math.min(this.o.max, Math.max(this.o.min, v)) * f) / f;
    var changed = v !== this.value;
    this.value = v;
    this.input.value = this.o.prefix + this.fmt.format(v) + this.o.suffix;
    this.input.setAttribute('aria-valuenow', v);
    this.input.setAttribute('aria-valuetext', this.input.value);
    if (!this.input.disabled) {
      this.dec.disabled = v <= this.o.min;
      this.inc.disabled = v >= this.o.max;
    }
    if (changed && !silent) {
      this.el.dispatchEvent(new CustomEvent('ttsc.dialer.change', { bubbles: true, detail: { value: v, formatted: this.input.value } }));
    }
  };
  TTSCDialer.prototype.increase = function () { this.setValue(this.value + this.o.step); };
  TTSCDialer.prototype.decrease = function () { this.setValue(this.value - this.o.step); };
  TTSCDialer.getInstance = function (el) { return el.ttscDialer || null; };
  TTSCDialer.init = function (root) {
    (root || document).querySelectorAll('[data-ttsc-dialer]').forEach(function (el) { new TTSCDialer(el); });
  };
  w.TTSCDialer = TTSCDialer;
  document.addEventListener('DOMContentLoaded', function () { TTSCDialer.init(); });
})(window);

// Uso: recalcula o resumo da turma quando as vagas mudam
document.addEventListener('ttsc.dialer.change', function (e) {
  if (e.target.querySelector('[name="max_students"]')) {
    document.querySelector('#vacancy-summary').textContent = e.detail.value + ' vagas';
  }
});
// Depois de inserir HTML dinâmico (drawer do CRUD): TTSCDialer.init(drawerEl);
```

### SQL

```sql
-- Carrega o valor atual e o mínimo permitido (maior turma ativa do curso). MariaDB 10.11 / MySQL 8
SELECT c.uuid, c.code, c.name,
       COALESCE(c.max_students, 40)   AS max_students,
       COALESCE(MAX(occ.enrolled), 0) AS min_allowed
  FROM courses c
  LEFT JOIN (SELECT e.course_uuid, e.class_uuid, COUNT(*) AS enrolled
               FROM enrollments e
              WHERE e.status = 'active' AND e.deleted_at IS NULL AND e.class_uuid IS NOT NULL
              GROUP BY e.course_uuid, e.class_uuid) occ ON occ.course_uuid = c.uuid
 WHERE c.uuid = :course_uuid
   AND c.deleted_at IS NULL
 GROUP BY c.uuid, c.code, c.name, c.max_students;

-- Gravação (o servidor normaliza "R$ 1.250,00" → 1250.00 e revalida min/max)
UPDATE courses
   SET max_students = :max_students, updated_at = NOW()
 WHERE uuid = :course_uuid AND deleted_at IS NULL;
```

O PHP passa `max_students` para `value` e `min_allowed` para `data-ttsc-dialer-min`; `max_students` é `smallint unsigned`, então o servidor rejeita valores fora de 0–65535 e menores que `min_allowed` antes do `UPDATE`.

## Faça / Não faça

- **Faça:** sempre defina `min`/`max` reais (do banco ou da regra de negócio) e revalide no servidor.
- **Faça:** `aria-label` específico em cada botão e rótulo visível no campo.
- **Faça:** passo coerente com o domínio (5 vagas, R$ 50,00), não 1 para valores grandes.
- **Não faça:** usar `type="number"` com prefixo `R$` (o navegador descarta o valor) nem confiar no valor formatado sem normalizar no servidor.
- **Não faça:** usar o Dialer para valores sem limite superior ou que mudam em milhares.
