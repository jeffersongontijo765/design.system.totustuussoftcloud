# Textarea

Campo de texto multilinha do chassi (`textarea.ttsc-textarea`), com tamanhos, contador de caracteres, controle de redimensionamento e estado inválido.

## Quando usar

- Texto livre de várias linhas: observações da matrícula (`enrollments.notes`), justificativa de falta, parecer descritivo, motivo de cancelamento.
- Uma linha só (nome, e-mail) → [Input](../Input/README.md).
- Altura que cresce com o conteúdo → combine com [Autosize](../Autosize/README.md) (`autosize(el)`).
- Formatação (negrito, listas, links) → editor rico ([TinyMCE](../TinyMCE/README.md) / [Quill](../Quill/README.md)).

## Anatomia

```
Observações                                   label.ttsc-form-label
┌──────────────────────────────────────────┐
│ Aluno transferido da E.E. Prof. Lima…    │  textarea.ttsc-textarea
│                                          │
└──────────────────────────────────────── ◢┘  (alça de resize)
Visível apenas para a secretaria.   182/500   .ttsc-form-description + .ttsc-textarea-counter
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Campo | `textarea.ttsc-textarea` (largura 100%, padding 12px) | sim |
| Tamanho | `ttsc-textarea-sm` (padding 10px, 12px) · padrão · `ttsc-textarea-lg` (padding 16px, 14px) | não |
| Linhas | `rows="4"` (altura inicial) | recomendado |
| Limite | `maxlength="500"` (o navegador bloqueia acima) | recomendado |
| Contador | `.ttsc-textarea-counter[data-for]` (extensão, JS abaixo) | não |
| Resize | `.resize-none` / `.resize-y` (extensões; o runtime não define) | não |

## Variantes

| Variante | Classe | Uso | Tokens |
|---|---|---|---|
| Pequeno | `ttsc-textarea-sm` | justificativa em linha de tabela | borda `--input` → `ttsc-border-strong` |
| Padrão | — | drawers | fundo `--background` → `ttsc-surface`, texto `--foreground` → `ttsc-text` |
| Grande | `ttsc-textarea-lg` | parecer descritivo | placeholder `--muted-foreground` a 80% |

## Estados

| Estado | Como aplicar |
|---|---|
| Foco | automático — borda `--ring` + anel 3px |
| Desabilitado | `disabled` (opacidade 0,6) |
| Somente leitura | `readonly` (extensão: fundo `ttsc-canvas-2`) |
| Inválido | `aria-invalid="true"` + `.ttsc-form-message` |
| Perto do limite | contador muda para `ttsc-warning-text` a 90% e `ttsc-danger-text` em 100% |

## API

Sem JavaScript no runtime. Atributos nativos: `rows`, `maxlength`, `minlength`, `required`, `placeholder`, `spellcheck="true"`, `lang="pt-BR"`. O contador abaixo é uma implementação TTSC (`assets/js/core/ttsc.textarea-counter.js`).

| Atributo do contador | Efeito |
|---|---|
| `data-ttsc-counter` no textarea | liga o contador |
| `.ttsc-textarea-counter[data-for="id"]` | elemento que recebe "n/máx" |

## Acessibilidade

- `<label for>` sempre. O contador é ligado por `aria-describedby` e atualizado com `aria-live="polite"` **somente** a partir de 90% (evita anunciar a cada tecla).
- Não use `resize: none` em textos longos sem Autosize: o usuário precisa ver o que escreveu.
- `spellcheck` ativo e `lang="pt-BR"` para correção ortográfica do navegador.

## Modelos

### HTML

```html
<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="enr-notes">Observações</label>
  <textarea class="ttsc-textarea resize-y" id="enr-notes" name="notes" rows="4" maxlength="500"
            lang="pt-BR" spellcheck="true" data-ttsc-counter
            aria-describedby="enr-notes-help enr-notes-count"
            placeholder="Ex.: aluno transferido, laudo entregue, combinação com a família…"><?= $this->e($enrollment['notes'] ?? '') ?></textarea>
  <div class="flex justify-between gap-2">
    <span class="ttsc-form-description" id="enr-notes-help">Visível apenas para a secretaria.</span>
    <span class="ttsc-textarea-counter" id="enr-notes-count" data-for="enr-notes"></span>
  </div>
</div>

<!-- Justificativa obrigatória (inválida) -->
<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="att-just">Justificativa da falta *</label>
  <textarea class="ttsc-textarea ttsc-textarea-sm" id="att-just" name="justification" rows="2" required
            minlength="10" aria-invalid="true" aria-describedby="att-just-msg"></textarea>
  <div class="ttsc-form-message" id="att-just-msg">Descreva o motivo (mínimo 10 caracteres).</div>
</div>
```

### CSS

```css
/* Ponte (bundle.css) */
:root { --input: var(--ttsc-border-strong); --background: var(--ttsc-surface); --foreground: var(--ttsc-text); }

/* Extensões do chassi */
.ttsc-textarea.resize-y { resize: vertical; }
.ttsc-textarea.resize-none { resize: none; }
.ttsc-textarea[readonly] { background-color: var(--ttsc-canvas-2); color: var(--ttsc-text-2); }
.ttsc-textarea { min-height: calc(var(--ttsc-space-8) * 2); }

.ttsc-textarea-counter { font-size: 12px; color: var(--ttsc-text-muted); font-variant-numeric: tabular-nums; white-space: nowrap; }
.ttsc-textarea-counter.is-near { color: var(--ttsc-warning-text); }
.ttsc-textarea-counter.is-full { color: var(--ttsc-danger-text); font-weight: 600; }
```

### JS

```js
// assets/js/core/ttsc.textarea-counter.js — contador n/máx (+ autosize quando disponível)
export function bindCounter(textarea) {
  const counter = document.querySelector(`.ttsc-textarea-counter[data-for="${textarea.id}"]`);
  const max = Number(textarea.maxLength) > 0 ? textarea.maxLength : null;
  const update = () => {
    const n = textarea.value.length;
    counter.textContent = max ? `${n}/${max}` : `${n}`;
    const ratio = max ? n / max : 0;
    counter.classList.toggle('is-near', ratio >= 0.9 && ratio < 1);
    counter.classList.toggle('is-full', ratio >= 1);
    counter.setAttribute('aria-live', ratio >= 0.9 ? 'polite' : 'off');
  };
  textarea.addEventListener('input', update);
  update();
  if (window.autosize) window.autosize(textarea); // ver ../Autosize/README.md
}

document.querySelectorAll('textarea.ttsc-textarea[data-ttsc-counter]').forEach(bindCounter);

// Inválido some ao corrigir
document.addEventListener('input', (event) => {
  const ta = event.target.closest('textarea.ttsc-textarea[aria-invalid="true"]');
  if (ta && ta.checkValidity()) ta.setAttribute('aria-invalid', 'false');
});
```

### SQL

```sql
-- Carrega a observação da matrícula (tenant)
SELECT e.uuid, e.code, e.notes
  FROM enrollments e
 WHERE e.uuid = :enrollment_uuid
   AND e.deleted_at IS NULL;

-- Salva (texto já validado: trim, ≤ 500 chars; string vazia vira NULL)
UPDATE enrollments
   SET notes = NULLIF(TRIM(:notes), ''),
       updated_at = NOW()
 WHERE uuid = :enrollment_uuid
   AND deleted_at IS NULL;
```

`notes` é `text`: o limite de 500 é regra de UI repetida no controller (`mb_strlen`). A view escreve o conteúdo **entre** as tags com `$this->e()` (sem espaços/quebras extras, senão o valor ganha whitespace).

## Faça / Não faça

- **Faça:** `maxlength` + contador; `rows` adequado ao uso (2 para justificativa, 4–6 para observações).
- **Faça:** `NULLIF(TRIM(...), '')` para não gravar observação vazia.
- **Não faça:** `resize: none` sem autosize; placeholder com instruções importantes (some ao digitar); editor rico para texto simples.
