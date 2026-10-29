# ColorPicker

Campo de cor do chassi para dados que guardam uma cor hexadecimal (ex.: `events.color varchar(7)` da agenda): `<input type="color">` estilizado + campo hex + paleta de amostras institucionais, com pré-visualização e texto de contraste automático — implementação TTSC (`ttsc.color-picker.js`).

## Quando usar

- Cor de categoria/etiqueta que aparece em calendário, kanban ou badge: evento acadêmico, tag de CRM, prioridade de chamado (`admin-tag.php` do SAC já usa `<input type="color" class="ttsc-input">`).
- **Prefira a paleta** (6–10 amostras) e deixe a cor livre como “Personalizada” — mantém a agenda legível.
- **Não use** para temas da interface (cores do produto vêm de tokens, nunca do usuário).
- **Não use** para escolher entre poucos estados com significado (ativo/inativo): use [Badge](../Badge/README.md) com variante fixa.

## O que existe no chassi (verificado)

| Peça | Situação |
|---|---|
| `bundle.css` | traz o tema do **Pickr** (`.pcr-app`, `.pcr-swatches`, variáveis `--pcr-bg`, `--pcr-border`, `--pcr-btn-bg`…, ligadas a `--popover`/`--border`/`--primary`) |
| JS do Pickr | **não** está no repositório nem em `vendor/` — sem a lib, o CSS `.pcr-*` não tem uso |
| ttscui | sem módulo de cor |
| Decisão | `<input type="color">` nativo (seletor do SO, acessível, zero dependência) + paleta TTSC |

## Anatomia

```
Cor do evento
[■][ #3ECF8E      ]   ● ● ● ● ● ● ● ●  (radiogroup de amostras)
 │       └ input.ttsc-input[data-ttsc-color-hex]  (texto, pattern ^#[0-9A-Fa-f]{6}$)
 └ input[type=color].ttsc-color-swatch-input[data-ttsc-color-input]   ← name="color" (valor enviado)
┌ prévia: [ Semana de Integração ]  texto preto/branco escolhido por contraste ┐
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Raiz | `[data-ttsc-color-picker]` | sim |
| Cor nativa | `input[type=color].ttsc-color-input[data-ttsc-color-input][name]` | sim |
| Hex | `input.ttsc-input[data-ttsc-color-hex]` (`maxlength=7`, `pattern`) | sim |
| Paleta | `[role=radiogroup]` com `button.ttsc-color-swatch[data-ttsc-color-swatch="#hex"][role=radio]` | recomendado |
| Prévia | `[data-ttsc-color-preview]` | não |
| Limpar | `[data-ttsc-color-clear]` → valor vazio (`NULL` no banco = cor padrão do tipo) | não |

## Estados

| Estado | Visual | Tokens |
|---|---|---|
| Amostra normal | círculo 22px com anel interno | anel `ttsc-border-strong` |
| Amostra selecionada | `aria-checked="true"`, anel duplo | anel externo `ttsc-text` sobre `ttsc-surface` |
| Foco | contorno 2px | `ttsc-accent` |
| Hex inválido | `aria-invalid="true"` + mensagem | `ttsc-danger-text` |
| Sem cor | prévia tracejada “Padrão do tipo” | borda `ttsc-border-strong`, texto `ttsc-text-muted` |

## API

Implementação TTSC (código completo no JS abaixo).

| Atributo | Elemento | Descrição |
|---|---|---|
| `data-ttsc-color-picker` | raiz | liga a instância |
| `data-ttsc-color-input` | `input[type=color]` | fonte do valor (`name` enviado) |
| `data-ttsc-color-hex` | `input` texto | edição manual; aceita `#abc`, `abc123`, normaliza para `#AABBCC` |
| `data-ttsc-color-swatch="#hex"` | botão | aplica a cor; `title` = nome (“Verde institucional”) |
| `data-ttsc-color-preview` | qualquer | recebe `background` e `color` de contraste |
| `data-ttsc-color-clear` | botão | zera o valor |

| Método (`TTSCColorPicker`) | Descrição |
|---|---|
| `new TTSCColorPicker(root)` / `TTSCColorPicker.init(scope)` | cria instâncias |
| `getValue()` | `'#RRGGBB'` ou `''` |
| `setValue(hex, { silent })` | aplica, sincroniza campos e paleta |
| `TTSCColorPicker.contrastText(hex)` | `'#000'` ou `'#fff'` (maior razão WCAG) — usado pela agenda |

| Evento | Alvo | `detail` |
|---|---|---|
| `ttsc.color.change` | raiz | `{ value }` — além do `input`/`change` nativos do campo |

## Acessibilidade

- O seletor nativo é operável por teclado e leitor de tela; tem `<label for>` próprio.
- Paleta como `role="radiogroup"` com `aria-label`; cada amostra `role="radio"`, `aria-checked` e `aria-label` com o **nome** da cor (“Azul informação”), nunca só o hex.
- Setas ← → movem entre amostras (roving tabindex).
- Cor nunca é a única informação: o evento continua com título e tipo.
- Texto sobre a cor escolhida é calculado (preto/branco com maior contraste) — garante ≥ 4,5:1 nas cores da paleta.

## Modelos

### HTML

```html
<div class="ttsc-form-item" data-ttsc-color-picker>
  <label class="ttsc-form-label" for="event-color">Cor no calendário</label>
  <div class="flex items-center gap-2">
    <input type="color" class="ttsc-color-input" id="event-color" name="color" data-ttsc-color-input
           value="<?= $this->e($event['color'] ?? '#3ECF8E') ?>">
    <input type="text" class="ttsc-input ttsc-input-sm ttsc-color-hex" data-ttsc-color-hex maxlength="7"
           pattern="^#[0-9A-Fa-f]{6}$" aria-label="Código hexadecimal" aria-describedby="event-color-error">
    <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-sm" data-ttsc-color-clear>Padrão</button>
  </div>
  <div class="ttsc-color-palette" role="radiogroup" aria-label="Cores sugeridas">
    <?php foreach ($palette as $hex => $label): ?>
      <button type="button" class="ttsc-color-swatch" role="radio" aria-checked="false"
              data-ttsc-color-swatch="<?= $this->e($hex) ?>" aria-label="<?= $this->e($label) ?>" title="<?= $this->e($label) ?>"
              style="--swatch: <?= $this->e($hex) ?>"></button>
    <?php endforeach ?>
  </div>
  <span class="ttsc-color-preview" data-ttsc-color-preview><?= $this->e($event['title']) ?></span>
  <div class="ttsc-form-message" id="event-color-error" role="alert">Use o formato #RRGGBB.</div>
</div>
```

### CSS

```css
/* Seletor nativo com cara de controle do chassi */
.ttsc-color-input {
  inline-size: 34px; block-size: 34px; padding: 3px; flex: none; cursor: pointer;
  border: 1px solid var(--input); border-radius: var(--ttsc-radius-sm); background: var(--ttsc-surface);
}
.ttsc-color-input::-webkit-color-swatch-wrapper { padding: 0; }
.ttsc-color-input::-webkit-color-swatch { border: 0; border-radius: var(--ttsc-radius-xs); }
.ttsc-color-input::-moz-color-swatch { border: 0; border-radius: var(--ttsc-radius-xs); }
.ttsc-color-input:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.ttsc-color-hex { inline-size: 110px; font-family: var(--font-mono, ui-monospace, monospace); text-transform: uppercase; }

.ttsc-color-palette { display: flex; flex-wrap: wrap; gap: 8px; }
.ttsc-color-swatch {
  inline-size: 22px; block-size: 22px; border-radius: var(--ttsc-radius-pill); cursor: pointer;
  background: var(--swatch); border: 0; box-shadow: inset 0 0 0 1px var(--ttsc-border-strong);
}
.ttsc-color-swatch[aria-checked="true"] { box-shadow: 0 0 0 2px var(--ttsc-surface), 0 0 0 4px var(--ttsc-text); }
.ttsc-color-swatch:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 4px; }

.ttsc-color-preview {
  display: inline-flex; align-items: center; gap: 6px; padding: 3px 10px; font-size: 12px; font-weight: 500;
  border-radius: var(--ttsc-radius-sm); border: 1px dashed transparent;
}
.ttsc-color-preview[data-empty] { border-color: var(--ttsc-border-strong); color: var(--ttsc-text-muted); background: transparent; }

/* Ponte do tema Pickr (bundle.css), caso a lib seja adotada no futuro */
:root { --pcr-bg: var(--ttsc-surface); --pcr-border: var(--ttsc-border); --pcr-btn-bg: var(--ttsc-accent); --pcr-btn-text: var(--ttsc-accent-on); }
```

### JS

```js
// assets/js/core/ttsc.color-picker.js — implementação TTSC
const HEX = /^#?([0-9a-f]{3}|[0-9a-f]{6})$/i;

function normalize(value) {
  const m = HEX.exec(String(value || '').trim());
  if (!m) return null;
  let h = m[1];
  if (h.length === 3) h = h.split('').map((c) => c + c).join('');
  return `#${h.toUpperCase()}`;
}
function luminance(hex) {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
    .map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

export class TTSCColorPicker {
  static contrastText(hex) {
    const L = luminance(hex);
    return (L + 0.05) / 0.05 >= 1.05 / (L + 0.05) ? '#000' : '#fff';
  }
  static init(scope = document) {
    scope.querySelectorAll('[data-ttsc-color-picker]').forEach((root) => root.ttscColor || new TTSCColorPicker(root));
  }
  constructor(root) {
    this.root = root;
    root.ttscColor = this;
    this.native = root.querySelector('[data-ttsc-color-input]');
    this.hex = root.querySelector('[data-ttsc-color-hex]');
    this.preview = root.querySelector('[data-ttsc-color-preview]');
    this.swatches = [...root.querySelectorAll('[data-ttsc-color-swatch]')];
    this.value = normalize(this.native.value) || '';

    this.native.addEventListener('input', () => this.setValue(this.native.value));
    this.hex.addEventListener('input', () => {
      const v = normalize(this.hex.value);
      this.hex.setAttribute('aria-invalid', v || this.hex.value === '' ? 'false' : 'true');
      if (v) this.setValue(v, { keepHex: true });
    });
    this.hex.addEventListener('blur', () => { if (this.hex.getAttribute('aria-invalid') !== 'true') this.hex.value = this.value; });
    this.swatches.forEach((s, i) => {
      s.addEventListener('click', () => this.setValue(s.dataset.ttscColorSwatch));
      s.addEventListener('keydown', (e) => {
        const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
        if (!step) return;
        e.preventDefault();
        const next = this.swatches[(i + step + this.swatches.length) % this.swatches.length];
        next.focus();
        next.click();
      });
    });
    root.querySelector('[data-ttsc-color-clear]')?.addEventListener('click', () => this.setValue(''));
    this.setValue(this.value, { silent: true });
  }
  getValue() { return this.value; }
  setValue(input, { silent = false, keepHex = false } = {}) {
    const v = input === '' ? '' : normalize(input);
    if (v === null) return;
    const changed = v !== this.value;
    this.value = v;
    if (v) this.native.value = v.toLowerCase();
    if (!keepHex) this.hex.value = v;
    let found = false;
    this.swatches.forEach((s) => {
      const on = normalize(s.dataset.ttscColorSwatch) === v;
      found ||= on;
      s.setAttribute('aria-checked', String(on));
      s.tabIndex = on ? 0 : -1;
    });
    if (!found && this.swatches[0]) this.swatches[0].tabIndex = 0;
    if (this.preview) {
      this.preview.toggleAttribute('data-empty', !v);
      this.preview.style.background = v || '';
      this.preview.style.color = v ? TTSCColorPicker.contrastText(v) : '';
    }
    if (changed && !silent) {
      this.root.dispatchEvent(new CustomEvent('ttsc.color.change', { bubbles: true, detail: { value: v } }));
    }
  }
}

TTSCColorPicker.init();

// Envio: input[type=color] não aceita vazio — mande o valor real num hidden quando "Padrão"
document.addEventListener('submit', (e) => {
  e.target.querySelectorAll('[data-ttsc-color-picker]').forEach((root) => {
    const hidden = root.querySelector('input[type=hidden][name=color]') || root.appendChild(Object.assign(document.createElement('input'), { type: 'hidden', name: 'color' }));
    root.querySelector('[data-ttsc-color-input]').removeAttribute('name');
    hidden.value = root.ttscColor.getValue();
  });
}, true);
```

### SQL

`events.color` é `varchar(7)` com comentário “Cor hex para calendário visual”; `NULL` = cor padrão do tipo. As “cores recentes” da unidade complementam a paleta:

```sql
-- Cores já usadas na unidade (para sugestões abaixo da paleta)
SELECT color, COUNT(*) AS uses
  FROM events
 WHERE deleted_at IS NULL
   AND unit_uuid = :unit_uuid
   AND color REGEXP '^#[0-9A-Fa-f]{6}$'
 GROUP BY color
 ORDER BY uses DESC
 LIMIT 8;

-- Gravação (prepared statement; :color = '#RRGGBB' ou NULL)
UPDATE events
   SET color = :color
 WHERE uuid = :event_uuid
   AND unit_uuid = :unit_uuid
   AND deleted_at IS NULL;
```

O controller valida com `preg_match('/^#[0-9A-F]{6}$/i', $color)`, grava em maiúsculas e converte `''` em `NULL`. A view do calendário usa `color` como fundo e `TTSCColorPicker.contrastText()` (ou o equivalente PHP) para o texto.

## Faça / Não faça

- **Faça:** paleta curta com nomes; “Personalizada” no seletor nativo.
- **Faça:** calcular a cor do texto sobre a cor escolhida.
- **Não faça:** usar a cor do usuário em bordas/fundos da interface fora do item que ela identifica.
- **Não faça:** carregar o CSS do Pickr esperando um seletor — não há JS dele no chassi.
