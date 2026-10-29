# Radio

Botão de opção nativo estilizado (`input[type=radio].ttsc-radio`) para escolher **uma** opção entre poucas, em lista, linha ou cartões selecionáveis.

## Quando usar

- 2 a 5 opções mutuamente exclusivas que o usuário precisa **ver** de uma vez: turno (manhã/tarde/noite), modalidade (presencial/híbrido/EaD), tipo de matrícula.
- Opções com descrição ou preço → cartões selecionáveis (variante "card").
- Mais de 6 opções ou lista vinda do banco → [Select](../Select/README.md). Escolha visual compacta em toolbar → [ToggleGroup](../ToggleGroup/README.md).
- Ligar/desligar uma configuração → [Switch](../Switch/README.md); várias escolhas independentes → Checkbox.

## Anatomia

```
Turno *                                  fieldset > legend.ttsc-form-label
( ) Manhã   (•) Tarde   ( ) Noite        label.ttsc-form-control-inline > input.ttsc-radio + texto
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Grupo | `<fieldset>` + `<legend class="ttsc-form-label">` (ou `role="radiogroup"` + `aria-labelledby`) | sim |
| Opção | `input[type=radio].ttsc-radio` com o **mesmo `name`** | sim |
| Linha da opção | `label.ttsc-form-control-inline` (flex, gap 10px) envolvendo input + texto | recomendado |
| Rótulo | texto dentro do `<label>`, ou `label.ttsc-label[for]` logo após o input | sim |
| Tamanho | `ttsc-radio-sm` (18px) · padrão (20px) · `ttsc-radio-lg` (22px) | não |
| Cor | `ttsc-radio-mono` (marcado em `ttsc-text`) | não |
| Cartão | `label.pv-radio-card` (extensão CSS, abaixo) | não |

## Variantes

| Variante | Classe | Uso | Tokens |
|---|---|---|---|
| Padrão | `ttsc-radio` | formulários | borda `--input` → `ttsc-border-strong`; marcado: fundo `--primary` → `ttsc-accent`, ponto branco |
| Mono | `ttsc-radio ttsc-radio-mono` | telas neutras, **só tema claro** | marcado `--mono` → `ttsc-text`; no escuro o ponto (SVG branco fixo) some sobre o fundo claro |
| Tamanhos | `-sm` / `-lg` | tabelas densas / auth | 18 / 20 / 22px |
| Cartão selecionável | `.ttsc-radio-card` (extensão) | plano, modalidade com descrição | borda `ttsc-accent-border`, fundo `ttsc-accent-soft` quando `:has(:checked)` |

## Estados

| Estado | Como aplicar |
|---|---|
| Marcado | `checked` (servidor) |
| Foco | automático — anel 2px `--ring` (`:focus-visible`) |
| Desabilitado | `disabled`; o rótulo `.ttsc-label`/`.ttsc-form-label` irmão fica com opacidade 0,5 |
| Inválido | `aria-invalid="true"` em cada radio do grupo (borda `ttsc-danger`) + mensagem no `.ttsc-form-message` |
| Nenhum marcado | grupo sem `checked` casa `:indeterminate`, e o runtime pinta `.ttsc-radio:indeterminate` como marcado (verde cheio). Use a correção do CSS abaixo ou sempre pré-marque uma opção |

## API

Sem JavaScript: comportamento nativo do navegador. Atributos úteis: `name` (agrupa), `value`, `checked`, `required` (em **um** radio do grupo basta), `disabled`. Leitura em JS: `form.elements.shift.value` (RadioNodeList).

## Acessibilidade

- Agrupe com `<fieldset>`/`<legend>`; o leitor de tela anuncia "Turno, grupo, Tarde, 2 de 3".
- Teclado nativo: `Tab` entra no grupo (na opção marcada), setas mudam a seleção, `Espaço` marca.
- Não use `display:none` no input dos cartões — esconda visualmente (extensão CSS) para manter foco e setas.
- O ponto marcado é branco sobre `ttsc-accent`: é indicador não textual (≥ 3:1 contra a borda), o rótulo continua em `ttsc-text`.

## Modelos

### HTML

```html
<!-- Drawer de matrícula: turno (lista inline) -->
<fieldset class="ttsc-form-item">
  <legend class="ttsc-form-label">Turno *</legend>
  <div class="flex flex-wrap gap-4">
    <?php foreach ($shiftOptions as $opt): ?>
      <label class="ttsc-form-control-inline">
        <input type="radio" class="ttsc-radio" name="shift" value="<?= $this->e($opt['value']) ?>"
               <?= $opt['value'] === ($enrollment['shift'] ?? 'morning') ? 'checked' : '' ?> required>
        <span class="text-sm"><?= $this->e($opt['label']) ?></span>
      </label>
    <?php endforeach; ?>
  </div>
</fieldset>

<!-- Modalidade em cartões selecionáveis -->
<fieldset class="ttsc-form-item">
  <legend class="ttsc-form-label">Modalidade *</legend>
  <div class="grid grid-cols-3 gap-3">
    <label class="ttsc-radio-card">
      <input type="radio" class="ttsc-radio" name="modality" value="in_person" checked>
      <span><strong>Presencial</strong><small>Aulas na unidade</small></span>
    </label>
    <label class="ttsc-radio-card">
      <input type="radio" class="ttsc-radio" name="modality" value="hybrid">
      <span><strong>Híbrido</strong><small>Presencial + online</small></span>
    </label>
    <label class="ttsc-radio-card">
      <input type="radio" class="ttsc-radio" name="modality" value="distance">
      <span><strong>EaD</strong><small>100% online</small></span>
    </label>
  </div>
</fieldset>
```

### CSS

```css
/* Ponte (bundle.css) */
:root { --primary: var(--ttsc-accent); --input: var(--ttsc-border-strong); --mono: var(--ttsc-text); }

/* Correção obrigatória: radio de grupo sem seleção é :indeterminate e o runtime o pinta de --primary */
.ttsc-radio:indeterminate:not(:checked) { background-color: var(--ttsc-surface); border-color: var(--ttsc-border-strong); }
.ttsc-radio[aria-invalid=true]:indeterminate:not(:checked) { border-color: var(--ttsc-danger); }

/* Extensão do chassi: cartão selecionável */
.ttsc-radio-card {
  display: flex; align-items: flex-start; gap: var(--ttsc-space-3);
  padding: var(--ttsc-space-3) var(--ttsc-space-4);
  border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control);
  background: var(--ttsc-surface); cursor: pointer;
  transition: border-color .15s, background-color .15s;
}
.ttsc-radio-card:hover { border-color: var(--ttsc-border-strong); }
.ttsc-radio-card:has(:checked) { border-color: var(--ttsc-accent-border); background: var(--ttsc-accent-soft); }
.ttsc-radio-card:has(:focus-visible) { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.ttsc-radio-card:has(:disabled) { opacity: .5; cursor: not-allowed; }
.ttsc-radio-card strong { display: block; font-weight: 500; color: var(--ttsc-text); }
.ttsc-radio-card small { display: block; font-size: 12px; color: var(--ttsc-text-muted); }
```

### JS

```js
// Mostra campos dependentes conforme a modalidade (ex.: polo EaD só quando "distance")
const form = document.querySelector('#form-enrollment');
const poloField = form.querySelector('[data-show-when-modality="distance"]');

function syncModality() {
  const modality = form.elements.modality.value;          // RadioNodeList.value
  poloField.classList.toggle('hidden', modality !== 'distance');
  poloField.querySelectorAll('input, select').forEach((el) => { el.disabled = modality !== 'distance'; });
}

form.addEventListener('change', (event) => {
  if (event.target.name === 'modality') syncModality();
  if (event.target.type === 'radio') {
    form.querySelectorAll(`[name="${event.target.name}"]`).forEach((r) => r.removeAttribute('aria-invalid'));
  }
});
syncModality();
```

### SQL

```sql
-- Opções do grupo vêm do catálogo de enum da coluna (rótulos traduzidos no PHP via __())
SELECT r.value, r.label
  FROM ref_enum_enrollments_shift_3dacc9afe6c9 r
 WHERE r.is_active = 1
   AND r.deleted_at IS NULL
 ORDER BY r.sort_order, r.label;

-- Valores realmente usados (com contagem) — útil para filtros por turno/modalidade
SELECT e.shift, e.modality, COUNT(*) AS total
  FROM enrollments e
 WHERE e.deleted_at IS NULL
 GROUP BY e.shift, e.modality
 ORDER BY total DESC;
```

O catálogo pode estar vazio num tenant novo; nesse caso o PHP usa a constante `OPTIONS['shift']` do serviço (`morning`, `afternoon`, `evening`, `night`, `online`) e `OPTIONS['modality']` (`in_person`, `hybrid`, `distance`). A view recebe `$shiftOptions` (`value`, `label`) e marca `checked` comparando com `$enrollment['shift']`.

## Faça / Não faça

- **Faça:** sempre uma opção pré-marcada quando houver padrão do banco (`DEFAULT 'morning'`).
- **Faça:** cartões para opções com descrição; lista inline para rótulos curtos.
- **Não faça:** radio para ligar/desligar (use Switch); mais de 6 opções; esconder o input com `display:none`.
