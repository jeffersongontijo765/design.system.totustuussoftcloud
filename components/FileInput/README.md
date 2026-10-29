# FileInput

Campo de arquivo do chassi: `input[type=file].ttsc-input` com o botão “Escolher arquivo” estilizado pelo runtime (`::file-selector-button`), lista dos arquivos selecionados com tamanho, validação de tipo/tamanho e remoção — implementação TTSC leve (`ttsc.file-input.js`).

## Quando usar

- Anexar 1–5 arquivos dentro de um formulário que é enviado de uma vez: documentos da solicitação de matrícula, comprovante de pagamento, plano de ensino em PDF.
- Lista de documentos exigidos, um campo por tipo, com status de conferência.
- Para fila de upload com progresso, várias requisições, prévia e retentativa use [Dropzone](../Dropzone/README.md); para soltar arquivos arrastando use a área de [DragAndDrop](../DragAndDrop/README.md).
- Foto/avatar com prévia circular: use [ImageInput](../ImageInput/README.md).
- **Não use** para importar planilhas grandes com mapeamento de colunas — isso é um assistente ([Stepper](../Stepper/README.md)).

## Anatomia

```
Histórico escolar *
[ Escolher arquivo | historico-ana.pdf               ]   input[type=file].ttsc-input
PDF ou imagem, até 5 MB                                   .ttsc-form-description
┌ ul.ttsc-file-list ─────────────────────────────────┐
│ 📄 historico-ana.pdf      182 KB          [×]       │   li.ttsc-file-item (+ .is-invalid)
└─────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Campo | `input[type=file].ttsc-input` + `accept` + `name` (`name="files[]"` com `multiple`) | sim |
| Implementação TTSC | `data-ttsc-file-input` no campo; `data-ttsc-file-max` (bytes); `data-ttsc-file-list="#id"` | não |
| Lista | `ul.ttsc-file-list` + `aria-live="polite"` | com `multiple` |
| Item | `li.ttsc-file-item` com ícone, nome, tamanho e botão remover (`aria-label`) | — |
| Dica / erro | `.ttsc-form-description` / `.ttsc-form-message` + `aria-invalid` | sim / quando validável |
| Status do documento | `.ttsc-doc-status[data-status]` (pending, submitted, approved, rejected, expired) | na lista de documentos |

## Variantes

| Variante | Como | Tokens |
|---|---|---|
| Simples | `input.ttsc-input[type=file]` | borda `--input`, botão com divisória `--input`, texto `--foreground` |
| Pequena | `+ ttsc-input-sm` | — |
| Múltipla com lista | `multiple` + `data-ttsc-file-list` | itens `ttsc-surface`, borda `ttsc-border` |
| Botão oculto | `input.sr-file` + `label.ttsc-btn.ttsc-btn-outline[for]` | para toolbars (“Anexar”) |

## Estados

| Estado | Como aplicar | Visual |
|---|---|---|
| Vazio | — | “Nenhum arquivo escolhido” (texto do navegador) |
| Selecionado | `change` | nome no campo + item na lista |
| Inválido | `aria-invalid="true"` + `.ttsc-form-message` | borda `ttsc-danger`; item `.is-invalid` em `ttsc-danger-text` |
| Desabilitado | `disabled` | 50% |
| Documento | `data-status` | pendente `ttsc-text-muted` · enviado `ttsc-info-text` · aprovado `ttsc-accent-text` · recusado/expirado `ttsc-danger-text` (todos sobre fundo `color-mix` 12% da cor) |

## API

Implementação TTSC (código no JS abaixo):

| Atributo | Descrição |
|---|---|
| `data-ttsc-file-input` | liga a instância ao `input[type=file]` |
| `data-ttsc-file-max` | tamanho máximo por arquivo em bytes (ex.: `5242880`) |
| `data-ttsc-file-max-files` | quantidade máxima com `multiple` |
| `data-ttsc-file-list` | seletor da `ul` que recebe os itens |

| Método (`TTSCFileInput`) | Descrição |
|---|---|
| `new TTSCFileInput(input)` / `TTSCFileInput.init(scope)` | instância |
| `files()` | `File[]` atuais |
| `remove(index)` | remove um arquivo (reconstrói `input.files` via `DataTransfer`) |
| `validate()` | aplica `aria-invalid` e retorna `true/false` |

| Evento | Alvo | `detail` |
|---|---|---|
| `ttsc.file.change` | input | `{ files, invalid: [{ file, reason }] }` |

## Acessibilidade

- O input nativo é focável e anunciado (“Escolher arquivo, Histórico escolar”); mantenha `<label for>`.
- Informe tipos e limite na dica **antes** do erro.
- Lista com `aria-live="polite"`; cada “remover” com `aria-label="Remover historico-ana.pdf"`.
- Status de documento com texto (“Recusado”), não só cor.
- O botão do seletor herda `--foreground` sobre `--background` (contraste de `ttsc-text`).

## Modelos

### HTML

```html
<!-- Documentos da solicitação de matrícula: um campo por tipo exigido -->
<form method="post" action="/academic/enrollment-requests/<?= $this->e($request['uuid']) ?>/documents" enctype="multipart/form-data">
  <input type="hidden" name="_token" value="<?= $this->e($csrf) ?>">
  <ul class="ttsc-doc-list">
    <?php foreach ($documents as $doc): ?>
      <li class="ttsc-doc-row">
        <div class="ttsc-doc-info">
          <label class="ttsc-form-label" for="doc-<?= $this->e($doc['uuid']) ?>"><?= $this->e($docTypes[$doc['document_type']]) ?></label>
          <span class="ttsc-doc-status" data-status="<?= $this->e($doc['status']) ?>"><?= $this->e($statusLabels[$doc['status']]) ?></span>
        </div>
        <?php if (in_array($doc['status'], ['pending', 'rejected', 'expired'], true)): ?>
          <input type="file" class="ttsc-input ttsc-input-sm" id="doc-<?= $this->e($doc['uuid']) ?>"
                 name="documents[<?= $this->e($doc['uuid']) ?>]" accept=".pdf,image/jpeg,image/png"
                 data-ttsc-file-input data-ttsc-file-max="5242880" aria-describedby="doc-hint">
        <?php else: ?>
          <a class="ttsc-link ttsc-link-sm" href="/files/<?= $this->e($doc['uuid']) ?>">Ver arquivo</a>
        <?php endif ?>
      </li>
    <?php endforeach ?>
  </ul>
  <p class="ttsc-form-description" id="doc-hint">PDF, JPG ou PNG, até 5 MB por arquivo.</p>
</form>

<!-- Vários anexos com lista -->
<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="attachments">Anexos do plano de ensino</label>
  <input type="file" class="ttsc-input" id="attachments" name="attachments[]" multiple accept=".pdf,.docx"
         data-ttsc-file-input data-ttsc-file-max="10485760" data-ttsc-file-max-files="5" data-ttsc-file-list="#attachments-list"
         aria-describedby="attachments-hint attachments-error">
  <div class="ttsc-form-description" id="attachments-hint">Até 5 arquivos PDF ou DOCX, 10 MB cada.</div>
  <div class="ttsc-form-message" id="attachments-error" role="alert"></div>
  <ul class="ttsc-file-list" id="attachments-list" aria-live="polite"></ul>
</div>
```

### CSS

```css
/* Ponte (bundle.css): .ttsc-input[type=file] zera o padding vertical; o botão usa borda --input e cor --foreground */
.ttsc-input[type="file"] { padding-inline-start: 0; cursor: pointer; color: var(--ttsc-text-2); }
.ttsc-input::file-selector-button {
  height: 100%; margin-inline-end: var(--ttsc-space-3); padding-inline: var(--ttsc-space-3);
  background: var(--ttsc-canvas-2); color: var(--ttsc-text); font-weight: 500; cursor: pointer;
}
.ttsc-input:hover::file-selector-button { background: var(--ttsc-surface-2); }
.ttsc-input[type="file"]:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }

.ttsc-file-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 6px; }
.ttsc-file-item {
  display: flex; align-items: center; gap: 8px; padding: 6px 6px 6px 10px; font-size: 12px;
  background: var(--ttsc-surface); border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-sm); color: var(--ttsc-text);
}
.ttsc-file-item i { color: var(--ttsc-text-muted); }
.ttsc-file-item .size { margin-inline-start: auto; color: var(--ttsc-text-muted); font-variant-numeric: tabular-nums; }
.ttsc-file-item.is-invalid { border-color: var(--ttsc-danger); color: var(--ttsc-danger-text); }
.ttsc-form-message { color: var(--ttsc-danger-text); }

.ttsc-doc-status { display: inline-flex; padding: 1px 8px; border-radius: var(--ttsc-radius-pill); font-size: 11px; font-weight: 500; }
.ttsc-doc-status[data-status="pending"]   { color: var(--ttsc-text-muted);  background: var(--ttsc-canvas-2); }
.ttsc-doc-status[data-status="submitted"] { color: var(--ttsc-info-text);   background: color-mix(in srgb, var(--ttsc-info) 12%, transparent); }
.ttsc-doc-status[data-status="approved"]  { color: var(--ttsc-accent-text); background: var(--ttsc-accent-soft); }
.ttsc-doc-status[data-status="rejected"],
.ttsc-doc-status[data-status="expired"]   { color: var(--ttsc-danger-text); background: color-mix(in srgb, var(--ttsc-danger) 12%, transparent); }
```

### JS

```js
// assets/js/core/ttsc.file-input.js — implementação TTSC
const ICONS = { pdf: 'fa-file-pdf', doc: 'fa-file-word', docx: 'fa-file-word', jpg: 'fa-file-image', jpeg: 'fa-file-image', png: 'fa-file-image' };
const kb = (n) => (n >= 1048576 ? `${(n / 1048576).toFixed(1).replace('.', ',')} MB` : `${Math.ceil(n / 1024)} KB`);

export class TTSCFileInput {
  static init(scope = document) { scope.querySelectorAll('[data-ttsc-file-input]').forEach((i) => i.ttscFile || new TTSCFileInput(i)); }
  constructor(input) {
    input.ttscFile = this;
    this.input = input;
    this.max = Number(input.dataset.ttscFileMax) || Infinity;
    this.maxFiles = Number(input.dataset.ttscFileMaxFiles) || Infinity;
    this.list = input.dataset.ttscFileList ? document.querySelector(input.dataset.ttscFileList) : null;
    this.message = input.closest('.ttsc-form-item')?.querySelector('.ttsc-form-message');
    input.addEventListener('change', () => this.render());
    this.list?.addEventListener('click', (e) => {
      const b = e.target.closest('[data-ttsc-file-remove]');
      if (b) this.remove(Number(b.dataset.ttscFileRemove));
    });
  }
  files() { return [...this.input.files]; }
  accepts(file) {
    const rules = (this.input.accept || '').split(',').map((s) => s.trim().toLowerCase()).filter(Boolean);
    const name = file.name.toLowerCase(), type = file.type.toLowerCase();
    return !rules.length || rules.some((r) => (r.startsWith('.') ? name.endsWith(r) : r.endsWith('/*') ? type.startsWith(r.slice(0, -1)) : type === r));
  }
  problems() {
    return this.files().map((file, i) => {
      if (!this.accepts(file)) return { file, reason: 'Tipo de arquivo não permitido.' };
      if (file.size > this.max) return { file, reason: `Maior que ${kb(this.max)}.` };
      if (i >= this.maxFiles) return { file, reason: `Limite de ${this.maxFiles} arquivos.` };
      return null;
    });
  }
  validate() {
    const invalid = this.problems().filter(Boolean);
    this.input.setAttribute('aria-invalid', invalid.length ? 'true' : 'false');
    if (this.message) this.message.textContent = invalid.length ? `${invalid[0].file.name}: ${invalid[0].reason}` : '';
    return invalid.length === 0;
  }
  remove(index) {
    const dt = new DataTransfer();
    this.files().forEach((f, i) => { if (i !== index) dt.items.add(f); });
    this.input.files = dt.files;
    this.render();
    this.input.focus();
  }
  render() {
    const problems = this.problems();
    this.validate();
    if (this.list) {
      this.list.innerHTML = this.files().map((f, i) => {
        const ext = f.name.split('.').pop().toLowerCase();
        const bad = problems[i];
        const item = document.createElement('li');
        item.className = `ttsc-file-item${bad ? ' is-invalid' : ''}`;
        item.innerHTML = `<i class="fa-light ${ICONS[ext] || 'fa-file'}" aria-hidden="true"></i><span class="name"></span>
          <span class="size">${bad ? bad.reason : kb(f.size)}</span>
          <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" data-ttsc-file-remove="${i}"><i class="fa-light fa-xmark"></i></button>`;
        item.querySelector('.name').textContent = f.name;
        item.querySelector('button').setAttribute('aria-label', `Remover ${f.name}`);
        return item.outerHTML;
      }).join('');
    }
    this.input.dispatchEvent(new CustomEvent('ttsc.file.change', {
      bubbles: true, detail: { files: this.files(), invalid: problems.filter(Boolean) },
    }));
  }
}

TTSCFileInput.init();

// Bloqueia o envio com arquivo inválido
document.addEventListener('submit', (e) => {
  const bad = [...e.target.querySelectorAll('[data-ttsc-file-input]')].filter((i) => !i.ttscFile.validate());
  if (bad.length) { e.preventDefault(); bad[0].focus(); }
});
```

### SQL

Documentos da solicitação vêm de `enrollment_request_documents` (status `enum('pending','submitted','approved','rejected','expired')`). Após salvar o arquivo no storage, grava o caminho e reabre a conferência:

```sql
-- Lista de documentos exigidos da solicitação
SELECT d.uuid, d.document_type, d.file_path, d.status, d.submitted_at
  FROM enrollment_request_documents d
 WHERE d.request_uuid = :request_uuid
   AND d.deleted_at IS NULL
 ORDER BY d.document_type;

-- Envio de um documento (só reenvia o que está pendente, recusado ou expirado)
UPDATE enrollment_request_documents
   SET file_path    = :file_path,
       submitted_at = NOW(),
       status       = 'submitted',
       validated_at = NULL,
       validated_by = NULL
 WHERE uuid = :document_uuid
   AND request_uuid = :request_uuid
   AND status IN ('pending', 'rejected', 'expired')
   AND deleted_at IS NULL;
```

O controller valida MIME real (`finfo`), tamanho e extensão no servidor — o `accept` do HTML é só conveniência —, grava em `tenant/<tenant>/enrollment-requests/<request>/<uuid>.<ext>` e usa o `rowCount()` do `UPDATE` para recusar reenvio de documento já aprovado (409).

## Faça / Não faça

- **Faça:** declarar tipos e limite na dica e revalidar no servidor.
- **Faça:** mostrar nome e tamanho do que foi escolhido, com como remover.
- **Não faça:** esconder o input sem um `label` focável no lugar.
- **Não faça:** confiar em `accept` ou na extensão para segurança.
