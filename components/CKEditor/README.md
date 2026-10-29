# CKEditor

Editor de texto formatado CKEditor 5 (build classic 41.4.2) com toolbar em pt-BR, cores ligadas aos tokens por variáveis `--ck-color-*` e HTML sanitizado no servidor antes de gravar em colunas `text`/`longtext`.

## Quando usar

- Textos institucionais longos com formatação: descrição de curso (`courses.description`), ementas, comunicados, termos de matrícula.
- Quando o conteúdo precisa de títulos, listas, links, citações e tabelas simples, e o usuário não escreve HTML.
- **Não use** para campos de uma linha ou observações curtas: use `textarea.ttsc-textarea` (com autosize).
- Para um editor mais leve (sem tabela, ~40 kB) use [Quill](../Quill/README.md); para recursos de documento (tabelas avançadas, código-fonte HTML) use [TinyMCE](../TinyMCE/README.md). Use **um** editor por produto/módulo.

## Anatomia

```
Descrição do curso                               48 palavras · 427 caracteres   ← rótulo + contador
┌ .ck-editor ────────────────────────────────────────────────────────────┐
│ ↶ ↷ │ Título ▾ │ B I 🔗 │ • 1. ⇤ ⇥ │ ❝ ▦                               │  .ck-toolbar
├────────────────────────────────────────────────────────────────────────┤
│ Administração — Bacharelado                                            │  .ck-editor__editable.ck-content
│ O curso forma gestores…                                                │
└────────────────────────────────────────────────────────────────────────┘
textarea[name=description] (oculta; recebe getData() no submit)
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Origem | `textarea[name]` com o HTML atual (escapado) e `aria-labelledby` | sim |
| Wrapper | `.ttsc-ck` (escopo das extensões de CSS) | sim |
| Toolbar | `.ck-toolbar` (itens em `config.toolbar.items`) | gerado |
| Área editável | `.ck-editor__editable.ck-content` (`role=textbox`, `aria-label` traduzido) | gerado |
| Painéis | `.ck-body-wrapper` no `body` (dropdowns, balão de link) | gerado |

## Variantes

| Variante | Como | Tokens |
|---|---|---|
| Padrão | `ClassicEditor.create(textarea, config)` | toolbar `ttsc-canvas-2`, área `ttsc-surface`, borda `ttsc-border` |
| Foco | automático | borda `ttsc-accent`, halo `ttsc-accent-soft` |
| Botão ativo (negrito ligado) | automático | fundo `ttsc-accent-soft`, ícone `ttsc-accent-text` |
| Somente leitura | `editor.enableReadOnlyMode('motivo')` | toolbar desabilitada |
| Compacto | toolbar sem `insertTable`/`blockQuote` | — |

## API

Itens de toolbar disponíveis neste build: `undo`, `redo`, `heading`, `bold`, `italic`, `link`, `bulletedList`, `numberedList`, `outdent`, `indent`, `blockQuote`, `insertTable`, `uploadImage`, `mediaEmbed`, `selectAll`, `accessibilityHelp` (+ `tableColumn`, `tableRow`, `mergeTableCells`, `imageStyle:*` nas toolbars contextuais).

| Opção | Exemplo |
|---|---|
| `language` | `'pt-br'` (exige `window.CKEDITOR_TRANSLATIONS['pt-br']`, ver JS) |
| `toolbar.items` | `['undo','redo','|','heading','|','bold','italic','link','|','bulletedList','numberedList','outdent','indent','|','blockQuote','insertTable']` |
| `heading.options` | `[{ model: 'paragraph', title: 'Parágrafo' }, { model: 'heading2', view: 'h2', title: 'Título' }, …]` |
| `link.defaultProtocol` / `link.decorators` | `'https://'` / `openInNewTab` com `rel="noopener noreferrer"` |
| `placeholder` | `'Descreva o curso…'` |
| `simpleUpload` | `{ uploadUrl, headers: { 'X-CSRF-Token' } }` (só com endpoint de upload; senão remova `uploadImage`) |

Métodos: `editor.getData()`, `editor.setData(html)`, `editor.updateSourceElement()`, `editor.enableReadOnlyMode(id)` / `disableReadOnlyMode(id)`, `editor.focus()`, `editor.destroy()`, `editor.execute('bold')`, `editor.plugins.get(...)`.

Eventos: `editor.model.document.on('change:data', fn)`, `editor.editing.view.document.on('focus'|'blur', fn)`, `editor.on('ready')`.

## Acessibilidade

- A área editável é `role="textbox"` `aria-multiline` com rótulo “Editor de texto formatado. Área de edição: …”; ligue o rótulo visível ao `textarea` (`aria-labelledby`).
- Teclado: `Alt+F10` vai para a toolbar, setas navegam, `Esc` volta ao texto; `Alt+0` abre a ajuda de acessibilidade (`accessibilityHelp`).
- Tooltips usam `ttsc-text` sobre `ttsc-surface` (inverso, alto contraste nos dois temas); links em `ttsc-accent-text`.
- Use títulos na ordem (Título = h2, Subtítulo = h3): o h1 é o título da página.

## Modelos

### HTML

```html
<div class="ttsc-form-item">
  <div class="flex items-center justify-between">
    <label class="ttsc-form-label" id="lbl-desc">Descrição do curso</label>
    <span class="ds-note" id="ck-count" aria-live="polite"></span>
  </div>
  <div class="ttsc-ck">
    <textarea id="course-description" name="description" aria-labelledby="lbl-desc"
              data-ttsc-ckeditor><?= $this->e($course['description'] ?? '') ?></textarea>
  </div>
</div>
<script src="<?= asset('vendors/ckeditor5/ckeditor.js') ?>"></script>
<script src="<?= asset('vendors/ckeditor5/translations/pt-br.js') ?>"></script>
```

### CSS

```css
/* assets/css/ttsc.ckeditor.css — :root:root vence o :root injetado pelo CKEditor depois do nosso CSS */
:root:root {
  --ck-border-radius: var(--ttsc-radius-sm);
  --ck-font-size-base: 13px;
  --ck-color-base-foreground: var(--ttsc-canvas-2);
  --ck-color-base-background: var(--ttsc-surface);
  --ck-color-base-border: var(--ttsc-border);
  --ck-color-base-text: var(--ttsc-text);
  --ck-color-text: var(--ttsc-text);
  --ck-color-shadow-inner: transparent;
  --ck-color-focus-border: var(--ttsc-accent);
  --ck-color-focus-outer-shadow: var(--ttsc-accent-soft);
  --ck-focus-ring: 1px solid var(--ttsc-accent);
  --ck-color-toolbar-background: var(--ttsc-canvas-2);
  --ck-color-toolbar-border: var(--ttsc-border);
  --ck-color-button-default-hover-background: var(--ttsc-surface-2);
  --ck-color-button-default-active-background: var(--ttsc-border);
  --ck-color-button-on-background: var(--ttsc-accent-soft);
  --ck-color-button-on-hover-background: var(--ttsc-accent-soft);
  --ck-color-button-on-color: var(--ttsc-accent-text);
  --ck-color-button-action-background: var(--ttsc-accent);
  --ck-color-button-action-text: var(--ttsc-accent-on);
  --ck-color-button-save: var(--ttsc-accent-text);
  --ck-color-button-cancel: var(--ttsc-danger-text);
  --ck-color-dropdown-panel-background: var(--ttsc-surface);
  --ck-color-dropdown-panel-border: var(--ttsc-border);
  --ck-color-panel-background: var(--ttsc-surface);
  --ck-color-panel-border: var(--ttsc-border);
  --ck-color-list-background: var(--ttsc-surface);
  --ck-color-list-button-hover-background: var(--ttsc-canvas-2);
  --ck-color-list-button-on-background: var(--ttsc-accent-soft);
  --ck-color-list-button-on-background-focus: var(--ttsc-accent-soft);
  --ck-color-list-button-on-text: var(--ttsc-text);
  --ck-color-input-background: var(--ttsc-surface);
  --ck-color-input-border: var(--ttsc-border-strong);
  --ck-color-input-text: var(--ttsc-text);
  --ck-color-labeled-field-label-background: var(--ttsc-surface);
  --ck-color-tooltip-background: var(--ttsc-text);
  --ck-color-tooltip-text: var(--ttsc-surface);
  --ck-color-link-default: var(--ttsc-accent-text);
  --ck-color-engine-placeholder-text: var(--ttsc-text-muted);
  --ck-color-switch-button-on-background: var(--ttsc-accent);
  --ck-color-widget-hover-border: var(--ttsc-accent-border);
}
.ttsc-ck .ck.ck-editor__top .ck-sticky-panel .ck-toolbar { border-radius: var(--ttsc-radius-control) var(--ttsc-radius-control) 0 0; }
.ttsc-ck .ck.ck-editor__main > .ck-editor__editable { min-height: 160px; max-height: 420px;
  border-radius: 0 0 var(--ttsc-radius-control) var(--ttsc-radius-control); }
/* O preflight do Tailwind zera listas e títulos: restaure dentro do conteúdo */
.ttsc-ck .ck-content, .ttsc-rich { color: var(--ttsc-text); line-height: 1.6; }
.ttsc-ck .ck-content ul, .ttsc-rich ul { list-style: disc; padding-inline-start: 22px; }
.ttsc-ck .ck-content ol, .ttsc-rich ol { list-style: decimal; padding-inline-start: 22px; }
.ttsc-ck .ck-content h2, .ttsc-rich h2 { font-size: 16px; font-weight: 600; margin: 0 0 6px; }
.ttsc-ck .ck-content blockquote, .ttsc-rich blockquote { border-inline-start: 3px solid var(--ttsc-accent); color: var(--ttsc-text-2);
  font-style: normal; margin-inline: 0; padding-inline-start: 12px; }
.ttsc-ck .ck-content a, .ttsc-rich a { color: var(--ttsc-accent-text); }
```

`.ttsc-rich` é a mesma tipografia para **exibir** o HTML gravado fora do editor (página do curso).

### JS

```js
// assets/js/core/ttsc.ckeditor.js — requer o build classic 41.4.2 (global ClassicEditor)
// translations/pt-br.js preenche window.CKEDITOR_TRANSLATIONS['pt-br']; sem ele, a UI fica em inglês.
export async function initCkeditor(textarea) {
  const editor = await ClassicEditor.create(textarea, {
    language: 'pt-br',
    toolbar: {
      items: ['undo', 'redo', '|', 'heading', '|', 'bold', 'italic', 'link', '|',
              'bulletedList', 'numberedList', 'outdent', 'indent', '|', 'blockQuote', 'insertTable'],
    },
    heading: {
      options: [
        { model: 'paragraph', title: 'Parágrafo', class: 'ck-heading_paragraph' },
        { model: 'heading2', view: 'h2', title: 'Título', class: 'ck-heading_heading2' },
        { model: 'heading3', view: 'h3', title: 'Subtítulo', class: 'ck-heading_heading3' },
      ],
    },
    link: {
      defaultProtocol: 'https://',
      decorators: { openInNewTab: { mode: 'manual', label: 'Abrir em nova aba', attributes: { target: '_blank', rel: 'noopener noreferrer' } } },
    },
    placeholder: 'Descreva o curso, público-alvo e diferenciais...',
  });

  const counter = document.getElementById('ck-count');
  const count = () => {
    const text = editor.getData().replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').trim();
    counter.textContent = `${text ? text.split(/\s+/).length : 0} palavras`;
  };
  editor.model.document.on('change:data', count);
  count();

  // O CRUD envia FormData: sincronize o textarea antes do submit
  textarea.form?.addEventListener('submit', () => editor.updateSourceElement(), { capture: true });
  return editor;
}

document.querySelectorAll('textarea[data-ttsc-ckeditor]').forEach((t) => initCkeditor(t));
```

Servidor — sanitização por lista de permissões (o repo não tem HTMLPurifier; `DOMDocument` nativo basta):

```php
// App\Support\RichTextSanitizer::clean(string $html): string — usar também para Quill e TinyMCE
$allowed = ['p' => [], 'br' => [], 'strong' => [], 'em' => [], 'u' => [], 's' => [], 'h2' => [], 'h3' => [],
            'ul' => [], 'ol' => [], 'li' => [], 'blockquote' => [], 'a' => ['href', 'target', 'rel'],
            'table' => [], 'thead' => [], 'tbody' => [], 'tr' => [], 'th' => ['colspan', 'rowspan'], 'td' => ['colspan', 'rowspan'],
            'figure' => ['class']];
$doc = new \DOMDocument();
@$doc->loadHTML('<?xml encoding="utf-8"?><div>' . $html . '</div>', LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD);
$walk = function (\DOMNode $node) use (&$walk, $allowed) {
    foreach (iterator_to_array($node->childNodes) as $child) {
        if ($child instanceof \DOMElement) {
            $tag = strtolower($child->tagName);
            if (!isset($allowed[$tag])) {                      // script, style, iframe, img externo…
                in_array($tag, ['script', 'style', 'iframe', 'object'], true)
                    ? $node->removeChild($child)
                    : $child->replaceWith(...iterator_to_array($child->childNodes));
                continue;
            }
            foreach (iterator_to_array($child->attributes) as $attr) {
                if (!in_array($attr->name, $allowed[$tag], true)) $child->removeAttribute($attr->name);
            }
            if ($tag === 'a' && !preg_match('#^(https?:|mailto:|/)#i', $child->getAttribute('href'))) $child->removeAttribute('href');
            if ($child->getAttribute('target') === '_blank') $child->setAttribute('rel', 'noopener noreferrer');
            $walk($child);
        }
    }
};
$walk($doc->documentElement);
$clean = substr($doc->saveHTML($doc->documentElement), 5, -6);   // remove o <div> externo
```

### SQL

```sql
-- Carrega (courses.description é TEXT, até 65.535 bytes). MariaDB 10.11 / MySQL 8
SELECT c.uuid, c.code, c.name, c.description, CHAR_LENGTH(c.description) AS html_length
  FROM courses c
 WHERE c.uuid = :course_uuid AND c.deleted_at IS NULL;

-- Grava SOMENTE o HTML já sanitizado (RichTextSanitizer::clean) e com strlen() <= 65535
UPDATE courses
   SET description = :description_clean, updated_at = NOW()
 WHERE uuid = :course_uuid AND deleted_at IS NULL;

-- A busca usa o índice FULLTEXT ft_courses_search (code, name, description)
SELECT c.uuid, c.name
  FROM courses c
 WHERE c.deleted_at IS NULL
   AND MATCH(c.code, c.name, c.description) AGAINST (:term IN NATURAL LANGUAGE MODE)
 LIMIT 20;
```

O PHP imprime `description` escapado dentro do `<textarea>` (`$this->e()`), o CKEditor reconstrói o HTML; na exibição pública o HTML **sanitizado** vai sem escape dentro de `.ttsc-rich`. Conteúdo maior que 64 KB pede `MEDIUMTEXT`/`LONGTEXT` (ex.: termos de contrato).

## Faça / Não faça

- **Faça:** sanitizar no servidor por lista de permissões; o filtro do CKEditor no cliente não é segurança.
- **Faça:** limitar a toolbar ao que o campo precisa e carregar `translations/pt-br.js`.
- **Faça:** `updateSourceElement()` antes de enviar formulários por `fetch`.
- **Não faça:** manter `uploadImage`/`mediaEmbed` sem endpoint de upload e sem política para iframes.
- **Não faça:** misturar CKEditor, Quill e TinyMCE na mesma tela.
