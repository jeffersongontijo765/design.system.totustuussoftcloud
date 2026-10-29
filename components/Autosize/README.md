# Autosize

Plugin **autosize 6.0.1** aplicado a `textarea.ttsc-textarea[data-ttsc-autosize]`: a altura acompanha o conteúdo enquanto o usuário digita, com teto opcional por `max-height`.

## Quando usar

- Campos de texto livre de tamanho imprevisível: observações da matrícula, justificativa de falta, parecer do conselho de classe, descrição de ocorrência.
- Formulários em [Drawer](../Drawer/README.md) e modais, onde uma textarea alta fixa desperdiça espaço.
- **Não use** para texto formatado (negrito, listas, links) — use [TinyMCE](../TinyMCE/README.md), [Quill](../Quill/README.md) ou [CKEditor](../CKEditor/README.md).
- **Não use** para campo de uma linha — use `input.ttsc-input`.
- Em textos muito longos (contratos, planos de ensino), combine com `ttsc-autosize-max` para não empurrar o rodapé do formulário.

## Anatomia

```
Observações da matrícula               label.ttsc-form-label
┌──────────────────────────────────┐
│ linha 1                          │   textarea.ttsc-textarea[data-ttsc-autosize]
│ linha 2 … cresce a cada linha    │   (rows = altura mínima)
└──────────────────────────────────┘
Cresce com o conteúdo        0/2000    ajuda / contador (opcional)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Campo | `textarea.ttsc-textarea` | sim |
| Ativação | `data-ttsc-autosize` | sim |
| Altura mínima | atributo `rows` (1–3) + `min-height` do CSS | sim |
| Teto | `ttsc-autosize-max` (`max-height: 104px` ≈ 5 linhas; depois rola) | não |
| Rótulo | `label.ttsc-form-label[for]` | sim |
| Contador | elemento com `aria-live="polite"` (+ `maxlength` no campo) | não |

## Estados

| Estado | Como |
|---|---|
| Vazio | `rows` define a altura inicial; `placeholder` em `ttsc-text-muted` |
| Crescendo | automático em `input`; emite `autosize:resized` |
| No teto | `max-height` atingido → autosize liga `overflow-y: scroll` |
| Desabilitado | `disabled` (mantém altura do conteúdo) |
| Valor alterado por JS | chame `autosize.update(el)` ou dispare `autosize:update` |

## API

Global `autosize` (UMD), carregado de `../../vendor/autosize/autosize.min.js` (no app: `assets/vendors/autosize/autosize.min.js`).

| Função | Descrição |
|---|---|
| `autosize(elementos)` | ativa em um elemento, NodeList ou array; retorna os elementos |
| `autosize.update(elementos)` | recalcula (após mudar `value`, mostrar aba/drawer oculto) |
| `autosize.destroy(elementos)` | remove o comportamento e restaura estilos |

| Evento | Direção | Uso |
|---|---|---|
| `autosize:resized` | emitido pela textarea | depois de mudar a altura (ajustar layout, scroll do drawer) |
| `autosize:update` | disparado por você | equivalente a `autosize.update(el)` |
| `autosize:destroy` | disparado por você | equivalente a `autosize.destroy(el)` |

Não há opções: limites vêm do CSS (`min-height`, `max-height`) e de `rows`.

## Acessibilidade

- `<label for>` sempre; ajuda/limite em elemento referenciado por `aria-describedby`.
- `resize: none` só porque a altura é automática — com `ttsc-autosize-max` a rolagem interna continua acessível por teclado.
- O contador de caracteres usa `aria-live="polite"` e só anuncia perto do limite.
- Texto `ttsc-text` sobre `ttsc-surface` e borda/foco do runtime (`--input`, `--ring` = `ttsc-accent`).

## Modelos

### HTML

```html
<div class="flex flex-col gap-2">
  <label class="ttsc-form-label" for="enrollment-notes">Observações da matrícula</label>
  <textarea class="ttsc-textarea" id="enrollment-notes" name="notes" rows="2" maxlength="2000"
            data-ttsc-autosize aria-describedby="enrollment-notes-help"><?= $this->e($enrollment['notes'] ?? '') ?></textarea>
  <div class="flex justify-between text-xs text-muted-foreground" id="enrollment-notes-help">
    <span>Visível apenas para a secretaria.</span>
    <span data-counter-for="enrollment-notes" aria-live="polite"></span>
  </div>
</div>

<!-- Parecer com teto de 5 linhas -->
<label class="ttsc-form-label" for="council-feedback">Parecer do conselho</label>
<textarea class="ttsc-textarea ttsc-autosize-max" id="council-feedback" name="feedback" rows="1" data-ttsc-autosize></textarea>
```

### CSS

```css
/* assets/css/ttsc.css — integração autosize */
textarea[data-ttsc-autosize] { resize: none; min-height: 64px; line-height: 20px; overflow-y: hidden; }
textarea[data-ttsc-autosize].ttsc-autosize-max { max-height: 104px; }   /* ~5 linhas de 20px + padding */
textarea[data-ttsc-autosize][rows="1"] { min-height: 36px; }
[data-counter-for].is-near-limit { color: var(--ttsc-warning-text); }
```

### JS

```js
// assets/js/core/ttsc.autosize.js
function initAutosize(root = document) {
  const fields = root.querySelectorAll('textarea[data-ttsc-autosize]:not([data-autosize-ready])');
  fields.forEach((el) => el.setAttribute('data-autosize-ready', ''));
  autosize(fields);

  fields.forEach((el) => {
    const counter = document.querySelector(`[data-counter-for="${el.id}"]`);
    if (!counter || !el.maxLength || el.maxLength < 0) return;
    const update = () => {
      const left = el.maxLength - el.value.length;
      counter.textContent = `${el.value.length}/${el.maxLength}`;
      counter.classList.toggle('is-near-limit', left <= 100);
    };
    el.addEventListener('input', update);
    update();
  });
}

document.addEventListener('DOMContentLoaded', () => initAutosize());

// Drawer/aba que estava oculto: a textarea foi medida com 0px → recalcular ao abrir
document.addEventListener('shown', (event) => {
  const fields = event.target.querySelectorAll?.('textarea[data-ttsc-autosize]');
  if (fields?.length) autosize.update(fields);
});

// Conteúdo carregado por AJAX
export function setNotes(textarea, text) {
  textarea.value = text;
  autosize.update(textarea);
}

// Exemplo: manter o rodapé do drawer visível quando o campo cresce
document.getElementById('enrollment-notes')?.addEventListener('autosize:resized', (event) => {
  event.target.closest('.ttsc-drawer-content, [data-ttsc-drawer]')?.scrollTo({ top: 1e6, behavior: 'smooth' });
});
```

### SQL

```sql
-- Carregar as observações para o formulário de edição
SELECT en.uuid, en.code, en.notes
  FROM enrollments en
 WHERE en.uuid = :enrollment_uuid
   AND en.deleted_at IS NULL;

-- Salvar (DomainCrudController / endpoint da matrícula)
UPDATE enrollments
   SET notes = :notes, updated_at = NOW()
 WHERE uuid = :enrollment_uuid
   AND deleted_at IS NULL;
```

`enrollments.notes` é `text`: o PHP aplica `mb_substr($notes, 0, 2000)` para respeitar o mesmo `maxlength` do HTML e grava `NULL` quando o campo vem vazio. A view escapa o valor com `$this->e()` dentro da textarea.

## Faça / Não faça

- **Faça:** `rows` pequeno (1–2) e deixe crescer; `ttsc-autosize-max` em drawers.
- **Faça:** `autosize.update()` sempre que preencher o valor por JS ou mostrar o campo oculto.
- **Não faça:** combinar com `resize: vertical` (o usuário briga com o plugin).
- **Não faça:** usar textarea autosize para conteúdo que precisa de formatação.
