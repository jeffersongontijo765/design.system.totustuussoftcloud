# Dropzone

Área de arrastar e soltar arquivos (Dropzone 5.9.3 do repo) com fila, barra de progresso, validação de tipo/tamanho e mensagens pt-BR, em lista tematizada por tokens.

## Quando usar

- Envio de **vários** documentos de uma vez: documentos da solicitação de matrícula (`enrollment_request_documents`), anexos de fatura, arquivos de importação.
- Quando o usuário precisa revisar a fila (remover, ver erro) antes de enviar — use `autoProcessQueue: false` + botão “Enviar documentos”.
- **Não use** para um único avatar/foto com recorte: use [Image Input](../ImageInput/README.md) do ttscui.
- **Não use** para um campo de arquivo simples dentro de formulário curto: `<input type="file" class="ttsc-input">` basta.

## Anatomia

```
┌ .ttsc-dropzone ───────────────────────────────────────────┐
│ [ícone]  Arraste os arquivos aqui ou clique para selecionar │   área clicável (dz-message)
│          PDF, JPG ou PNG · até 5 MB                        │
└────────────────────────────────────────────────────────────┘
 ul.ttsc-dz-list   (previewsContainer)
 ├ li.ttsc-dz-item [thumb] nome · tamanho · badge   [×]
 │                 ▬▬▬▬▬▬▬ progresso / mensagem de erro
 rodapé: status da fila · [Limpar fila] [Enviar documentos]
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Área de soltar | `div.ttsc-dropzone` + `tabindex="0"` `role="button"` | sim |
| Mensagem | `.dz-message[data-dz-message]` | sim |
| Lista de arquivos | `ul.ttsc-dz-list` (opção `previewsContainer`) | sim |
| Modelo do item | `<template>` com `data-dz-name`, `data-dz-size`, `data-dz-thumbnail`, `data-dz-uploadprogress`, `data-dz-errormessage`, `data-dz-remove` | sim |
| Ações | `ttsc-btn-primary` (Enviar), `ttsc-btn-ghost` (Limpar fila) | quando `autoProcessQueue: false` |

> Não use a classe `dropzone` no container: ela ativa o *autoDiscover* e o CSS padrão (fundo branco). Defina `Dropzone.autoDiscover = false` logo após carregar o script.

## Estados

| Estado | Classe aplicada pelo Dropzone | Visual | Tokens |
|---|---|---|---|
| Ocioso | — | borda tracejada | `ttsc-border-strong`, fundo `ttsc-canvas-2` |
| Arrastando sobre | `.dz-drag-hover` | borda verde, fundo tonal | `ttsc-accent`, `ttsc-accent-soft` |
| Na fila | (sem `dz-success`/`dz-error`) | badge “Na fila”, barra vazia | `ttsc-surface-2` |
| Enviando | `.dz-processing` | barra cresce | `ttsc-accent` |
| Enviado | `.dz-success .dz-complete` | badge “Enviado” | `ttsc-badge-success` |
| Recusado | `.dz-error` | borda e mensagem vermelhas | `ttsc-danger`, texto `ttsc-danger-text` |

## API

Opções usadas (Dropzone 5.9.3):

| Opção | Valor | Descrição |
|---|---|---|
| `url` | `/commercial/enrollment/documents/upload` | Endpoint POST (multipart) |
| `autoProcessQueue` | `false` | Só envia em `dz.processQueue()` |
| `paramName` | `'file'` | Nome do campo do arquivo |
| `params` | `{ request_uuid, document_type }` | Campos extras do POST |
| `headers` | `{ 'X-CSRF-Token': … }` | CSRF do chassi |
| `maxFilesize` | `5` | Em MB (base 1000) |
| `maxFiles` | `6` | Excedentes disparam `maxfilesexceeded` |
| `acceptedFiles` | `'.pdf,.jpg,.jpeg,.png'` | Filtro no cliente (o servidor revalida MIME) |
| `previewsContainer` / `previewTemplate` | `'#dz-previews'` / HTML do `<template>` | Lista no padrão TTSC |
| `parallelUploads` / `uploadMultiple` | `2` / `false` | Um request por arquivo |
| `dict*` | ver JS | Mensagens pt-BR |

Métodos: `processQueue()`, `addFile(file)`, `removeFile(file)`, `removeAllFiles(cancelInProgress)`, `getQueuedFiles()`, `getRejectedFiles()`, `getAcceptedFiles()`, `getFilesWithStatus(Dropzone.SUCCESS)`, `displayExistingFile(mock, thumbUrl)`, `disable()` / `enable()`, `destroy()`.

Eventos (`dz.on(nome, fn)`): `addedfile`, `removedfile`, `thumbnail`, `error (file, msg, xhr)`, `sending (file, xhr, formData)`, `uploadprogress (file, %, bytes)`, `success (file, response)`, `complete`, `queuecomplete`, `maxfilesexceeded`, `reset`.

> Nota de manutenção: no `dropzone.js` do repo a opção `dictFallbackText` foi renomeada por engano para `dictFallbacttscext` (substituição global `kt` → `ttsc`). Ela só afeta o formulário de fallback de navegadores antigos; ao atualizar o vendor, restaure o nome original.

## Acessibilidade

- A área é focável (`tabindex="0"`, `role="button"`) e abre o seletor com `Enter`/`Espaço` (`dz.hiddenFileInput.click()`).
- Tipos e limites ficam **visíveis** no texto de ajuda e ligados por `aria-describedby`.
- A lista tem `aria-live="polite"` para anunciar arquivos adicionados, enviados e recusados.
- Erro nunca só por cor: badge “Recusado” + mensagem em `ttsc-danger-text` (4,5:1 nos dois temas).
- Botão remover é só-ícone, com `aria-label="Remover arquivo"`.

## Modelos

### HTML

```html
<div class="ttsc-dropzone" id="dz-docs" tabindex="0" role="button" aria-describedby="dz-help">
  <span class="dz-icon"><i class="fa-light fa-cloud-arrow-up"></i></span>
  <div class="dz-message" data-dz-message>
    <div class="dz-title">Arraste os arquivos aqui ou clique para selecionar</div>
    <div class="dz-sub" id="dz-help">PDF, JPG ou PNG · até 5 MB por arquivo · máximo de 6 arquivos</div>
  </div>
</div>
<ul class="ttsc-dz-list" id="dz-previews" aria-live="polite"></ul>
<div class="flex items-center justify-between gap-2">
  <span class="ds-note" id="dz-status"></span>
  <div class="flex gap-2">
    <button type="button" class="ttsc-btn ttsc-btn-ghost" id="dz-clear">Limpar fila</button>
    <button type="button" class="ttsc-btn ttsc-btn-primary" id="dz-send"><i class="fa-light fa-paper-plane"></i> Enviar documentos</button>
  </div>
</div>

<template id="dz-tpl">
  <li class="ttsc-dz-item dz-preview">
    <div class="dz-thumb"><img data-dz-thumbnail alt=""><i class="fa-light fa-file-pdf"></i></div>
    <div style="min-width:0">
      <div class="dz-name" data-dz-name></div>
      <div class="dz-meta">
        <span class="dz-size" data-dz-size></span>
        <span class="ttsc-badge ttsc-badge-sm ttsc-badge-outline dz-state dz-state-queue">Na fila</span>
        <span class="ttsc-badge ttsc-badge-sm ttsc-badge-success ttsc-badge-outline dz-state dz-state-ok"><i class="fa-light fa-check"></i> Enviado</span>
        <span class="ttsc-badge ttsc-badge-sm ttsc-badge-destructive ttsc-badge-outline dz-state dz-state-err">Recusado</span>
      </div>
      <div class="dz-bar"><span data-dz-uploadprogress></span></div>
      <div class="dz-error-message" data-dz-errormessage></div>
    </div>
    <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" data-dz-remove aria-label="Remover arquivo"><i class="fa-light fa-xmark"></i></button>
  </li>
</template>

<!-- Arquivos já enviados (do SQL abaixo) -->
<script type="application/json" id="dz-existing"><?= json_encode($documents, JSON_HEX_TAG | JSON_HEX_AMP) ?></script>
```

### CSS

```css
/* assets/css/ttsc.dropzone.css — carregar depois de vendor/dropzone/dropzone.css */
.ttsc-dropzone {
  display: flex; align-items: center; gap: 14px; padding: 18px 20px; cursor: pointer;
  border: 1px dashed var(--ttsc-border-strong); border-radius: var(--ttsc-radius-surface);
  background: var(--ttsc-canvas-2); color: var(--ttsc-text-2);
  transition: border-color .15s, background-color .15s;
}
.ttsc-dropzone:hover, .ttsc-dropzone:focus-visible { border-color: var(--ttsc-accent); outline: none; }
.ttsc-dropzone.dz-drag-hover { border-color: var(--ttsc-accent); background: var(--ttsc-accent-soft); }
.ttsc-dropzone .dz-icon { width: 40px; height: 40px; display: grid; place-items: center; border-radius: var(--ttsc-radius-control);
  background: var(--ttsc-surface); border: 1px solid var(--ttsc-border); color: var(--ttsc-accent-text); font-size: 18px; }
.ttsc-dropzone .dz-title { color: var(--ttsc-text); font-weight: 600; font-size: 14px; }
.ttsc-dropzone .dz-sub { color: var(--ttsc-text-muted); font-size: 12px; }

.ttsc-dz-list { display: flex; flex-direction: column; gap: 8px; margin: 0; padding: 0; list-style: none; }
.ttsc-dz-item { display: grid; grid-template-columns: 36px 1fr auto; gap: 12px; align-items: center; padding: 10px 12px;
  border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control); background: var(--ttsc-surface); }
.ttsc-dz-item .dz-thumb { width: 36px; height: 36px; border-radius: var(--ttsc-radius-sm); background: var(--ttsc-surface-2);
  display: grid; place-items: center; overflow: hidden; color: var(--ttsc-text-2); }
.ttsc-dz-item .dz-thumb img { width: 100%; height: 100%; object-fit: cover; }
.ttsc-dz-item .dz-thumb img:not([src]) { display: none; }
.ttsc-dz-item .dz-thumb img[src] + i { display: none; }
.ttsc-dz-item .dz-name { color: var(--ttsc-text); font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ttsc-dz-item .dz-meta { display: flex; gap: 8px; align-items: center; font-size: 12px; color: var(--ttsc-text-muted); }
.ttsc-dz-item .dz-size strong { font-weight: 400; }
.ttsc-dz-item .dz-bar { height: 4px; margin-top: 6px; border-radius: var(--ttsc-radius-pill); background: var(--ttsc-surface-2); overflow: hidden; }
.ttsc-dz-item .dz-bar > span { display: block; height: 100%; width: 0; background: var(--ttsc-accent); transition: width .2s; }
.ttsc-dz-item .dz-error-message { display: none; margin-top: 4px; font-size: 12px; color: var(--ttsc-danger-text); }
.ttsc-dz-item.dz-error { border-color: var(--ttsc-danger); }
.ttsc-dz-item.dz-error .dz-error-message { display: block; }
.ttsc-dz-item.dz-error .dz-bar, .ttsc-dz-item.dz-success .dz-bar { display: none; }
.ttsc-dz-item .dz-state { display: none; }
.ttsc-dz-item.dz-success .dz-state-ok,
.ttsc-dz-item.dz-error .dz-state-err,
.ttsc-dz-item:not(.dz-success):not(.dz-error) .dz-state-queue { display: inline-flex; }
```

### JS

```js
// assets/js/core/ttsc.dropzone.js — requer vendor/dropzone/dropzone.js
Dropzone.autoDiscover = false;

const DZ_PT_BR = {
  dictDefaultMessage: 'Arraste os arquivos aqui ou clique para selecionar',
  dictFallbackMessage: 'Seu navegador não suporta envio por arrastar e soltar.',
  dictFileTooBig: 'Arquivo muito grande ({{filesize}} MB). Máximo: {{maxFilesize}} MB.',
  dictInvalidFileType: 'Tipo de arquivo não permitido. Envie PDF, JPG ou PNG.',
  dictResponseError: 'O servidor respondeu com o código {{statusCode}}.',
  dictCancelUpload: 'Cancelar envio',
  dictUploadCanceled: 'Envio cancelado.',
  dictCancelUploadConfirmation: 'Deseja cancelar este envio?',
  dictRemoveFile: 'Remover arquivo',
  dictRemoveFileConfirmation: null,
  dictMaxFilesExceeded: 'Limite de {{maxFiles}} arquivos atingido.',
  dictFileSizeUnits: { tb: 'TB', gb: 'GB', mb: 'MB', kb: 'KB', b: 'bytes' },
};

export function initDocumentsDropzone(el, { requestUuid, documentType }) {
  const dz = new Dropzone(el, {
    ...DZ_PT_BR,
    url: '/commercial/enrollment/documents/upload',
    autoProcessQueue: false,
    parallelUploads: 2,
    paramName: 'file',
    maxFilesize: 5,
    maxFiles: 6,
    acceptedFiles: '.pdf,.jpg,.jpeg,.png',
    thumbnailWidth: 72,
    thumbnailHeight: 72,
    previewsContainer: '#dz-previews',
    previewTemplate: document.getElementById('dz-tpl').innerHTML,
    headers: { 'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content },
    params: { request_uuid: requestUuid, document_type: documentType },
  });
  const baseSize = dz.filesize.bind(dz);
  dz.filesize = (size) => baseSize(size).replace('.', ',');           // "0,3 MB"

  // Documentos já existentes no servidor
  JSON.parse(document.getElementById('dz-existing').textContent).forEach((doc) => {
    const mock = { name: doc.file_name, size: +doc.file_size || 0, accepted: true, status: Dropzone.SUCCESS, uuid: doc.uuid };
    dz.files.push(mock);
    dz.displayExistingFile(mock, doc.thumb_url || '');
    mock.previewElement.classList.add('dz-success', 'dz-complete');
  });

  dz.on('success', (file, response) => { file.uuid = response.uuid; });
  dz.on('error', (file, message, xhr) => {
    if (xhr && message && message.error) {              // JSON do servidor {error: "..."}
      file.previewElement.querySelector('[data-dz-errormessage]').textContent = message.error;
    }
  });
  dz.on('removedfile', (file) => {
    if (file.uuid) {                                     // remove no servidor (soft delete)
      fetch(`/commercial/enrollment/documents/${file.uuid}`, {
        method: 'DELETE',
        headers: { 'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content },
      });
    }
  });
  dz.on('queuecomplete', () => TTSC.Toast && TTSC.Toast.show({ message: 'Documentos enviados para análise.', variant: 'success' }));

  el.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); dz.hiddenFileInput.click(); }
  });
  document.getElementById('dz-send').addEventListener('click', () => dz.processQueue());
  document.getElementById('dz-clear').addEventListener('click', () => {
    [...dz.getQueuedFiles(), ...dz.getRejectedFiles()].forEach((f) => dz.removeFile(f));
  });
  return dz;
}
```

### SQL

```sql
-- Documentos já enviados da solicitação (alimenta #dz-existing). MariaDB 10.11 / MySQL 8
SELECT d.uuid, d.document_type, d.status, d.file_path, d.submitted_at, d.validated_at
  FROM enrollment_request_documents d
  JOIN enrollment_requests r ON r.uuid = d.request_uuid AND r.deleted_at IS NULL
 WHERE d.request_uuid = :request_uuid
   AND d.deleted_at IS NULL
 ORDER BY d.created_at;

-- Cada upload aceito pelo servidor (após checar MIME real com finfo e mover para o storage)
INSERT INTO enrollment_request_documents
       (uuid, tenant_id, request_uuid, document_type, file_path, submitted_at, status, created_at, updated_at)
VALUES (:uuid, :tenant_id, :request_uuid, :document_type, :file_path, NOW(), 'submitted', NOW(), NOW());

-- Remoção pelo botão × (soft delete; só enquanto não validado)
UPDATE enrollment_request_documents
   SET deleted_at = NOW(), updated_at = NOW()
 WHERE uuid = :uuid AND status IN ('pending', 'submitted') AND deleted_at IS NULL;
```

O PHP converte cada linha em `{uuid, file_name: basename(file_path), file_size: filesize(), thumb_url}` e imprime no `<script type="application/json" id="dz-existing">`. O endpoint de upload usa o pipeline do repo (`App\Uploads\UploadPipeline` / `App\Services\Security\FileUploadService`: MIME real via `finfo_file`, limite de tamanho) e exige a `write_permission` da rota `/commercial/enrollment/documents` (`admin.crm.manage`) e `_token`.

## Faça / Não faça

- **Faça:** `autoProcessQueue: false` quando o usuário precisa revisar a fila; mostre o total na fila.
- **Faça:** revalidar tipo (MIME real), tamanho e permissão no servidor; `acceptedFiles` é só conveniência.
- **Faça:** mensagens pt-BR completas em todas as opções `dict*`.
- **Não faça:** usar a classe `dropzone` (CSS branco, sem tema escuro) nem deixar o *autoDiscover* ligado.
- **Não faça:** gravar o arquivo no banco (BLOB); grave só `file_path` e mantenha o arquivo no storage.
