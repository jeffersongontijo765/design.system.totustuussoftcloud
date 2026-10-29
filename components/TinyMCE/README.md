# TinyMCE

Editor de documentos TinyMCE 8.3.2 (licença GPL) com skin `oxide`/`oxide-dark` e `content_css` `default`/`dark` escolhidos pelo `data-theme`, plugins `lists link table autolink code` e conteúdo do iframe estilizado com os valores dos tokens.

> **Nota de manutenção (bug no repo):** `assets/vendors/tinymce/tinymce.min.js` e `themes/silver/theme.min.js` foram corrompidos por uma substituição global `kt` → `ttsc` que ignorou maiúsculas (ex.: `isDesktop` → `isDesttscop`, e `kt`/`Kt` viraram o mesmo `ttsc`, gerando “Identifier 'ttsc' has already been declared”). Os dois arquivos **não fazem parse** e o editor não abre no app. Correção: reinstalar os arquivos do pacote `tinymce@8.3.2` sem rodar o renomeador nos vendors. O preview repara os arquivos em memória só para demonstração.

## Quando usar

- Documentos longos e estruturados: Projeto Pedagógico do Curso (`course_ppcs`), cláusulas de contrato (`ctr_contract_clauses`), políticas, páginas do CMS.
- Quando o usuário precisa de **tabelas** editáveis, colar do Word/Google Docs e eventualmente ver o HTML (`code`).
- **Não use** para descrições curtas ou comunicados: use [Quill](../Quill/README.md) (leve) ou [CKEditor](../CKEditor/README.md).
- Use um único editor por módulo; não misture TinyMCE e CKEditor na mesma tela.

## Anatomia

```
┌ .tox.tox-tinymce ──────────────────────────────────────────────────────┐
│ ↶ ↷ │ Heading 2 ▾ │ B I │ 🔗 │ • 1. ⇤ ⇥ │ ▦ ▾ │ <>                    │  .tox-toolbar__primary
├────────────────────────────────────────────────────────────────────────┤
│ iframe (content_css + content_style com tokens resolvidos)             │  .tox-edit-area
│ 3. Organização curricular …  ┌ tabela ┐                                │
├────────────────────────────────────────────────────────────────────────┤
│ h2                                                       palavras      │  .tox-statusbar
└────────────────────────────────────────────────────────────────────────┘
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Origem | `textarea[name]` com o HTML atual escapado + `<label for>` | sim |
| Wrapper | `.ttsc-tiny` (escopo das extensões) | sim |
| Editor | `.tox.tox-tinymce` (gerado) | gerado |
| Toolbar | `.tox-toolbar__primary` / `.tox-tbtn` | gerado |
| Área | iframe `.tox-edit-area__iframe` (body `#tinymce.mce-content-body`) | gerado |
| Barra de status | `.tox-statusbar` (caminho e contagem de palavras) | gerado |

## Variantes

| Variante | Config | Tokens |
|---|---|---|
| Claro | `skin: 'oxide'`, `content_css: 'default'` | toolbar `ttsc-canvas-2`, conteúdo `ttsc-surface`/`ttsc-text` via `content_style` |
| Escuro | `skin: 'oxide-dark'`, `content_css: 'dark'` | idem (tokens do tema escuro) |
| Botão ativo | automático (`.tox-tbtn--enabled`) | `ttsc-accent-soft` + ícone `ttsc-accent-text` |
| Foco | automático (`.tox-edit-focus`) | borda `ttsc-accent` + halo `ttsc-accent-soft` |
| Somente leitura | `editor.mode.set('readonly')` | — |

## API

Opções usadas:

| Opção | Valor | Observação |
|---|---|---|
| `selector` / `target` | `'#ppc-content'` | |
| `base_url` / `suffix` | `'../../vendor/tinymce'` / `'.min'` | no app: `asset('vendors/tinymce')` |
| `license_key` | `'gpl'` | obrigatório na 8.x (sem ele, aviso no console) |
| `plugins` | `'lists link table autolink code'` | únicos plugins vendorizados |
| `toolbar` | `'undo redo \| blocks \| bold italic \| link \| bullist numlist outdent indent \| table \| code'` | |
| `block_formats` | `'Parágrafo=p; Título=h2; Subtítulo=h3'` | |
| `skin` / `content_css` | `oxide`·`default` ou `oxide-dark`·`dark` | ler `data-theme` antes do init |
| `content_style` | CSS com valores de `getComputedStyle` | o iframe não herda variáveis CSS da página |
| `menubar` / `branding` / `promotion` | `false` | |
| `link_default_target` / `link_assume_external_targets` | `'_blank'` / `'https'` | |
| `invalid_elements` | `'script,style,iframe,object,embed'` | defesa no cliente; o servidor sanitiza |
| `language` | `'en'` (padrão) | **pt_BR não está no repo** — ver abaixo |

Idioma: o pacote do repo não tem a pasta `langs/`. Para pt-BR, baixe o pacote de idiomas oficial da versão 8, copie `langs/pt_BR.js` para `assets/vendors/tinymce/langs/` e use `language: 'pt_BR'` (ou `language_url` apontando para o arquivo). Sem o arquivo, `language: 'pt_BR'` gera 404 e a UI continua em inglês. Os rótulos de `block_formats` podem ser traduzidos direto na opção.

Métodos (`tinymce.get(id)` ou retorno de `init`): `getContent()`, `setContent(html)`, `save()` (copia para o textarea), `insertContent(html)`, `isDirty()` / `setDirty(false)`, `mode.set('readonly'|'design')`, `focus()`, `remove()` (antes de reabrir drawer), `plugins.wordcount`.

Eventos (`editor.on(...)`): `init`, `input`, `change`, `dirty`, `blur`, `SetContent`, `ExecCommand`; global `tinymce.init({ setup: (ed) => … })`.

## Acessibilidade

- Atalhos nativos: `Alt+F10` toolbar, `Alt+F9` menu, `Alt+F11` caminho de elementos, `Alt+0` ajuda (com o plugin `help`, não vendorizado).
- O iframe recebe o título do textarea: mantenha `<label for>` e `aria-label` descritivo.
- Contraste do conteúdo garantido por `content_style` com `--ttsc-text` sobre `--ttsc-surface`; links em `--ttsc-accent-text`.
- Tabelas: use cabeçalho (`th`) — a opção `table_header_type: 'sectionCells'` gera `<thead>`.

## Modelos

### HTML

```html
<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="ppc-curriculum">Organização curricular</label>
  <div class="ttsc-tiny">
    <textarea id="ppc-curriculum" name="sections[curriculum]" data-ttsc-tinymce><?= $this->e($section['html'] ?? '') ?></textarea>
  </div>
</div>
<script src="<?= asset('vendors/tinymce/tinymce.min.js') ?>"></script>
```

### CSS

```css
/* assets/css/ttsc.tinymce.css — entorno do editor (o conteúdo é estilizado por content_style) */
.ttsc-tiny .tox.tox-tinymce { border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control); box-shadow: var(--ttsc-shadow-xs); }
.ttsc-tiny .tox.tox-tinymce.tox-edit-focus { border-color: var(--ttsc-accent); box-shadow: 0 0 0 3px var(--ttsc-accent-soft); }
.ttsc-tiny .tox .tox-editor-header { border-bottom: 1px solid var(--ttsc-border); box-shadow: none; padding: 0; }
.ttsc-tiny .tox .tox-toolbar__primary, .ttsc-tiny .tox .tox-toolbar-overlord, .ttsc-tiny .tox .tox-editor-header { background: var(--ttsc-canvas-2); }
.ttsc-tiny .tox .tox-tbtn { color: var(--ttsc-text-2); background: transparent; border-radius: 6px; }
.ttsc-tiny .tox .tox-tbtn svg { fill: var(--ttsc-text-2); }
.ttsc-tiny .tox .tox-tbtn:hover { background: var(--ttsc-surface-2); color: var(--ttsc-text); }
.ttsc-tiny .tox .tox-tbtn--enabled, .ttsc-tiny .tox .tox-tbtn--enabled:hover { background: var(--ttsc-accent-soft); }
.ttsc-tiny .tox .tox-tbtn--enabled svg { fill: var(--ttsc-accent-text); }
.ttsc-tiny .tox .tox-tbtn--select { border: 1px solid var(--ttsc-border); background: var(--ttsc-surface); }
.ttsc-tiny .tox .tox-tbtn__select-label { color: var(--ttsc-text); }
.ttsc-tiny .tox .tox-statusbar { background: var(--ttsc-canvas-2); border-top: 1px solid var(--ttsc-border); color: var(--ttsc-text-muted); }
.ttsc-tiny .tox .tox-statusbar__path-item, .ttsc-tiny .tox .tox-statusbar__wordcount { color: var(--ttsc-text-muted); }
```

### JS

```js
// assets/js/core/ttsc.tinymce.js — requer assets/vendors/tinymce (pacote 8.3.2 íntegro)
function tokenContentStyle() {
  const css = getComputedStyle(document.documentElement);
  const t = (name) => css.getPropertyValue(name).trim();
  return `body{font-family:Inter,system-ui,sans-serif;font-size:13px;line-height:1.6;margin:12px 14px;
            background:${t('--ttsc-surface')};color:${t('--ttsc-text')}}
          a{color:${t('--ttsc-accent-text')}} h2{font-size:16px;font-weight:600}
          th,td{border:1px solid ${t('--ttsc-border-strong')};padding:6px 8px;text-align:left}
          th{background:${t('--ttsc-canvas-2')};font-weight:600}`;
}

export function initTinymce() {
  const dark = document.documentElement.dataset.theme === 'dark' || document.documentElement.classList.contains('dark');
  return tinymce.init({
    selector: 'textarea[data-ttsc-tinymce]',
    base_url: '/assets/vendors/tinymce',
    suffix: '.min',
    license_key: 'gpl',
    // language: 'pt_BR',             // habilite depois de copiar langs/pt_BR.js
    skin: dark ? 'oxide-dark' : 'oxide',
    content_css: dark ? 'dark' : 'default',
    content_style: tokenContentStyle(),
    plugins: 'lists link table autolink code',
    toolbar: 'undo redo | blocks | bold italic | link | bullist numlist outdent indent | table | code',
    block_formats: 'Parágrafo=p; Título=h2; Subtítulo=h3',
    menubar: false,
    branding: false,
    promotion: false,
    height: 420,
    link_default_target: '_blank',
    link_assume_external_targets: 'https',
    table_header_type: 'sectionCells',
    table_default_styles: { width: '100%', 'border-collapse': 'collapse' },
    invalid_elements: 'script,style,iframe,object,embed',
    setup(editor) {
      editor.on('change input', () => editor.save());               // textarea sempre atualizado para o FormData
    },
  });
}

// Troca de tema: o skin não muda em tempo real — recrie o editor preservando o conteúdo
new MutationObserver(async () => {
  const contents = tinymce.get().map((ed) => [ed.id, ed.getContent()]);
  tinymce.remove();
  await initTinymce();
  contents.forEach(([id, html]) => tinymce.get(id)?.setContent(html));
}).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme', 'class'] });

document.addEventListener('DOMContentLoaded', () => initTinymce());
```

### SQL

```sql
-- course_ppcs.content é LONGTEXT com CHECK json_valid: o PPC é guardado como JSON de seções.
-- Seções da versão mais recente do PPC do curso (JSON_TABLE: MariaDB 10.6+ e MySQL 8)
SELECT p.uuid, p.version, p.status, s.section_key, s.title, s.html
  FROM course_ppcs p
  JOIN JSON_TABLE(p.content, '$.sections[*]' COLUMNS (
         section_key VARCHAR(64)  PATH '$.key',
         title       VARCHAR(255) PATH '$.title',
         html        LONGTEXT     PATH '$.html')) AS s
 WHERE p.course_uuid = :course_uuid
   AND p.version = (SELECT MAX(p2.version) FROM course_ppcs p2 WHERE p2.course_uuid = p.course_uuid);

-- Edição de uma seção em rascunho (HTML já sanitizado no PHP)
UPDATE course_ppcs
   SET content = JSON_SET(content, CONCAT('$.sections[', :section_index, '].html'), :html_clean)
 WHERE uuid = :ppc_uuid AND status = 'draft';

-- Nova versão a partir de um PPC aprovado (o PHP gera :uuid e monta o JSON)
INSERT INTO course_ppcs (uuid, course_uuid, version, content, status, replaces_uuid, created_at)
SELECT :uuid, :course_uuid, COALESCE(MAX(p.version), 0) + 1, :content_json, 'draft', :replaces_uuid, NOW()
  FROM course_ppcs p
 WHERE p.course_uuid = :course_uuid_again;
```

O PHP agrupa as linhas por seção e imprime um `textarea` por seção (HTML escapado); no POST, cada `sections[key]` passa por `App\Support\RichTextSanitizer::clean()` (ver [CKEditor](../CKEditor/README.md)) e entra no JSON com `json_encode` — nunca concatene HTML em JSON no SQL. PPC aprovado (`status = 'approved'`) é imutável: editar cria nova versão.

## Faça / Não faça

- **Faça:** `license_key: 'gpl'`, `base_url` + `suffix` explícitos e skin conforme o tema.
- **Faça:** passar os tokens ao iframe via `content_style` (variáveis CSS não atravessam o iframe).
- **Faça:** restaurar os arquivos originais do pacote 8.3.2 no repo e excluir `vendors/` do renomeador `kt`→`ttsc`.
- **Não faça:** confiar em `invalid_elements` como sanitização; o servidor decide.
- **Não faça:** apontar `language: 'pt_BR'` sem o arquivo em `langs/` (404 e UI em inglês).
