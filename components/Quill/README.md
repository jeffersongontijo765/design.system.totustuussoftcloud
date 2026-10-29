# Quill

Editor de texto leve Quill 2.0.3 com o tema snow ajustado aos tokens, toolbar declarada em HTML (com rótulos pt-BR) e saída em HTML semântico para comunicados e textos curtos formatados.

## Quando usar

- Textos curtos a médios com formatação básica: comunicados aos responsáveis, avisos de turma, respostas de chamado, observações pedagógicas.
- Quando o editor precisa ser leve e a toolbar enxuta (negrito, itálico, link, listas, citação).
- **Não use** para documentos com tabelas, títulos múltiplos e colagem do Word: use [CKEditor](../CKEditor/README.md) ou [TinyMCE](../TinyMCE/README.md).
- **Não use** para texto sem formatação: `textarea.ttsc-textarea`.

## Anatomia

```
Comunicado aos responsáveis                       34 palavras · 208 caracteres
┌ .ttsc-quill ──────────────────────────────────────────────────────────┐
│ Parágrafo ⇕ │ B I U 🔗 │ 1. • ❝ │ Tx                                  │  #q-toolbar.ql-toolbar.ql-snow
├───────────────────────────────────────────────────────────────────────┤
│ Reunião de pais e mestres                                             │  .ql-container > .ql-editor
│ • Entrega dos boletins                                                │
└───────────────────────────────────────────────────────────────────────┘
 input[type=hidden][name=body]  ← getSemanticHTML() no submit
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Wrapper | `.ttsc-quill` (borda, raio e foco do TTSC) | sim |
| Toolbar | `div#…-toolbar` com `.ql-formats` e botões `.ql-bold`, `.ql-link`, `.ql-list[value]`… com `aria-label` pt-BR | sim |
| Editor | `div#…-editor` → `.ql-container.ql-snow > .ql-editor[contenteditable]` | sim |
| Campo do formulário | `input[type=hidden]` sincronizado | sim |
| Tooltip de link | `.ql-tooltip` (textos trocados por CSS) | gerado |

## Variantes

| Variante | Configuração | Tokens |
|---|---|---|
| Snow TTSC | `theme: 'snow'` + CSS abaixo | toolbar `ttsc-canvas-2`, ícones `ttsc-text-2`, área `ttsc-surface` |
| Botão ativo | automático (`.ql-active`) | fundo `ttsc-accent-soft`, traço `ttsc-accent-text` |
| Foco | `:focus-within` no wrapper | borda `ttsc-accent` + halo `ttsc-accent-soft` |
| Somente leitura | `quill.disable()` / `readOnly: true` | toolbar oculta por CSS (`.ql-disabled`) |
| Compacto (resposta) | toolbar só `bold italic link` | — |

## API

Opções: `theme` (`'snow'`), `modules.toolbar` (seletor do container ou array), `modules.history` (`delay`, `maxStack`), `modules.keyboard` (atalhos), `modules.clipboard`, `placeholder`, `readOnly`, `formats` (lista de formatos permitidos — use para impedir colar cores/fontes: `['header','bold','italic','underline','link','list','blockquote']`).

Métodos: `getContents()` / `setContents(delta)` (formato Delta, JSON), `getSemanticHTML(index?, length?)` (HTML limpo), `getText()`, `getLength()`, `setText()`, `insertText(i, txt, formats)`, `formatText(i, len, formats)`, `getSelection()` / `setSelection(i, len)`, `enable()` / `disable()`, `focus()`, `blur()`, `clipboard.dangerouslyPasteHTML(html)` (só com HTML já sanitizado).

Eventos: `text-change (delta, oldDelta, source)`, `selection-change (range, oldRange, source)`, `editor-change`; `source` é `'user'` ou `'api'`.

> Quill 2.0.3: `getSemanticHTML()` devolve espaços como `&nbsp;`. Normalize com `.replace(/&nbsp;/g, ' ')` antes de gravar (senão a busca FULLTEXT e a quebra de linha sofrem).

## Acessibilidade

- O Quill não rotula a área editável: defina `role="textbox"`, `aria-multiline="true"` e `aria-labelledby` em `quill.root` (ver JS).
- Cada botão da toolbar precisa de `aria-label` em pt-BR (“Negrito”, “Lista numerada”); o Quill não gera.
- Atalhos: `Ctrl+B/I/U`, `Ctrl+K` (link), `Ctrl+Z`/`Ctrl+Shift+Z`. `Tab` dentro do editor indenta lista — informe `Esc` + `Tab` para sair (ou desative o binding Tab).
- Ícones são SVG com `stroke`: os tokens `ttsc-text-2`/`ttsc-accent-text` garantem contraste ≥ 4,5:1 nos dois temas.

## Modelos

### HTML

```html
<div class="ttsc-form-item">
  <label class="ttsc-form-label" id="lbl-notice">Comunicado aos responsáveis</label>
  <div class="ttsc-quill">
    <div id="notice-toolbar">
      <span class="ql-formats">
        <select class="ql-header" aria-label="Estilo do parágrafo"><option selected></option><option value="2"></option><option value="3"></option></select>
      </span>
      <span class="ql-formats">
        <button class="ql-bold" aria-label="Negrito"></button>
        <button class="ql-italic" aria-label="Itálico"></button>
        <button class="ql-underline" aria-label="Sublinhado"></button>
        <button class="ql-link" aria-label="Inserir link"></button>
      </span>
      <span class="ql-formats">
        <button class="ql-list" value="ordered" aria-label="Lista numerada"></button>
        <button class="ql-list" value="bullet" aria-label="Lista com marcadores"></button>
        <button class="ql-blockquote" aria-label="Citação"></button>
      </span>
      <span class="ql-formats"><button class="ql-clean" aria-label="Limpar formatação"></button></span>
    </div>
    <div id="notice-editor" data-ttsc-quill="#notice-toolbar" data-target="#notice-body" data-label="lbl-notice"></div>
  </div>
  <input type="hidden" name="body" id="notice-body" value="<?= $this->e($notice['body'] ?? '') ?>">
</div>
```

### CSS

```css
/* assets/css/ttsc.quill.css — carregar depois de vendor/quill/quill.snow.css */
.ttsc-quill { border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control); background: var(--ttsc-surface); }
.ttsc-quill:focus-within { border-color: var(--ttsc-accent); box-shadow: 0 0 0 3px var(--ttsc-accent-soft); }
.ttsc-quill .ql-toolbar.ql-snow { border: 0; border-bottom: 1px solid var(--ttsc-border); background: var(--ttsc-canvas-2);
  border-radius: var(--ttsc-radius-control) var(--ttsc-radius-control) 0 0; padding: 6px 8px; font-family: inherit; }
.ttsc-quill .ql-container.ql-snow { border: 0; font-family: inherit; font-size: 13px; }
.ttsc-quill .ql-editor { min-height: 150px; max-height: 360px; color: var(--ttsc-text); line-height: 1.6; padding: 12px 14px; }
.ttsc-quill .ql-editor.ql-blank::before { color: var(--ttsc-text-muted); font-style: normal; }
.ttsc-quill .ql-editor h2 { font-size: 16px; font-weight: 600; }
.ttsc-quill .ql-editor blockquote { border-inline-start: 3px solid var(--ttsc-accent); color: var(--ttsc-text-2); padding-inline-start: 12px; }
.ttsc-quill .ql-editor a { color: var(--ttsc-accent-text); }
.ttsc-quill .ql-snow .ql-stroke { stroke: var(--ttsc-text-2); }
.ttsc-quill .ql-snow .ql-fill { fill: var(--ttsc-text-2); }
.ttsc-quill .ql-snow .ql-picker { color: var(--ttsc-text-2); }
.ttsc-quill .ql-snow button { border-radius: 6px; }
.ttsc-quill .ql-snow button:hover, .ttsc-quill .ql-snow .ql-picker-label:hover { background: var(--ttsc-surface-2); }
.ttsc-quill .ql-snow button.ql-active { background: var(--ttsc-accent-soft); }
.ttsc-quill .ql-snow button.ql-active .ql-stroke { stroke: var(--ttsc-accent-text); }
.ttsc-quill .ql-snow button.ql-active .ql-fill { fill: var(--ttsc-accent-text); }
.ttsc-quill .ql-snow button:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 1px; }
.ttsc-quill .ql-snow .ql-picker-options { background: var(--ttsc-surface); border: 1px solid var(--ttsc-border) !important;
  border-radius: var(--ttsc-radius-sm); box-shadow: var(--ttsc-shadow-md); }
.ttsc-quill .ql-snow .ql-picker-item.ql-selected, .ttsc-quill .ql-snow .ql-picker-item:hover { color: var(--ttsc-accent-text); }
/* Textos pt-BR (o snow os define em CSS) */
.ttsc-quill .ql-snow .ql-picker.ql-header { width: 112px; }
.ttsc-quill .ql-snow .ql-picker.ql-header .ql-picker-label::before,
.ttsc-quill .ql-snow .ql-picker.ql-header .ql-picker-item::before { content: 'Parágrafo'; }
.ttsc-quill .ql-snow .ql-picker.ql-header [data-value="2"]::before { content: 'Título' !important; }
.ttsc-quill .ql-snow .ql-picker.ql-header [data-value="3"]::before { content: 'Subtítulo' !important; }
.ttsc-quill .ql-snow .ql-tooltip { background: var(--ttsc-surface); color: var(--ttsc-text); border: 1px solid var(--ttsc-border);
  border-radius: var(--ttsc-radius-sm); box-shadow: var(--ttsc-shadow-popover); }
.ttsc-quill .ql-snow .ql-tooltip::before { content: 'Abrir:'; color: var(--ttsc-text-muted); }
.ttsc-quill .ql-snow .ql-tooltip[data-mode=link]::before { content: 'Link:'; }
.ttsc-quill .ql-snow .ql-tooltip a.ql-action::after { content: 'Editar'; color: var(--ttsc-accent-text); }
.ttsc-quill .ql-snow .ql-tooltip.ql-editing a.ql-action::after { content: 'Salvar'; }
.ttsc-quill .ql-snow .ql-tooltip a.ql-remove::before { content: 'Remover'; color: var(--ttsc-danger-text); }
.ttsc-quill .ql-snow .ql-tooltip input[type=text] { background: var(--ttsc-canvas-2); color: var(--ttsc-text);
  border: 1px solid var(--ttsc-border-strong); border-radius: 6px; }
.ttsc-quill .ql-disabled + .ql-toolbar, .ttsc-quill:has(.ql-disabled) .ql-toolbar { display: none; }
```

### JS

```js
// assets/js/core/ttsc.quill.js — requer vendor/quill/quill.js
const FORMATS = ['header', 'bold', 'italic', 'underline', 'link', 'list', 'blockquote'];

export function initQuill(el) {
  const target = document.querySelector(el.dataset.target);
  const quill = new Quill(el, {
    theme: 'snow',
    modules: { toolbar: el.dataset.ttscQuill, history: { delay: 1000, maxStack: 100 } },
    formats: FORMATS,                                    // colar do Word não traz cor/fonte
    placeholder: 'Escreva o comunicado...',
  });
  quill.root.setAttribute('role', 'textbox');
  quill.root.setAttribute('aria-multiline', 'true');
  quill.root.setAttribute('aria-labelledby', el.dataset.label);

  if (target.value) quill.clipboard.dangerouslyPasteHTML(target.value);   // HTML já sanitizado pelo servidor

  const sync = () => {
    const html = quill.getSemanticHTML().replace(/&nbsp;/g, ' ');
    target.value = quill.getText().trim() ? html : '';
  };
  quill.on('text-change', sync);
  sync();
  return quill;
}

document.querySelectorAll('[data-ttsc-quill]').forEach((el) => initQuill(el));
```

### SQL

```sql
-- Envia o comunicado para os alunos ativos da turma (notification_items.body é TEXT). MariaDB 10.11 / MySQL 8
INSERT INTO notification_items (id, tenant_id, user_id, type, priority, title, body, resource, resource_id, created_at)
SELECT UUID(), :tenant_id, e.student_uuid, 'announcement', 'normal', :title, :body_clean, 'classes', e.class_uuid, NOW()
  FROM enrollments e
 WHERE e.class_uuid = :class_uuid
   AND e.status = 'active'
   AND e.deleted_at IS NULL;

-- Caixa do aluno/responsável
SELECT n.id, n.title, n.body, n.created_at, n.is_read
  FROM notification_items n
 WHERE n.user_id = :user_uuid AND n.type = 'announcement'
 ORDER BY n.created_at DESC
 LIMIT 20;
```

`:body_clean` é o HTML do campo `body` depois de `App\Support\RichTextSanitizer::clean()` (mesma lista de permissões do [CKEditor](../CKEditor/README.md)); o PHP rejeita acima de 65.535 bytes. Na leitura, o HTML sanitizado é impresso sem escape dentro de `.ttsc-rich`.

## Faça / Não faça

- **Faça:** restringir `formats` ao que a toolbar oferece e sanitizar no servidor.
- **Faça:** `aria-label` em cada botão e rótulo na área editável.
- **Faça:** normalizar `&nbsp;` do `getSemanticHTML()` antes de gravar.
- **Não faça:** gravar `quill.root.innerHTML` (traz classes `ql-*` e marcação interna) nem o Delta onde se espera HTML.
- **Não faça:** usar `dangerouslyPasteHTML` com HTML que não passou pelo sanitizador.
