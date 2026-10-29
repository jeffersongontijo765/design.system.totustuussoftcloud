# Cropper

Recorte de imagem com Cropper.js 1.6.2 para a foto de perfil (avatar 1:1), com prévia redonda, zoom/rotação e exportação em canvas 256×256 enviada ao perfil do usuário.

## Quando usar

- Foto de perfil do usuário, do aluno (ficha de matrícula) ou do colaborador, quando o arquivo enviado precisa virar um quadrado padronizado.
- Recorte de logotipo da unidade/escola com proporção fixa (`aspectRatio: 4 / 1` no cabeçalho de boletim).
- **Não use** só para escolher/remover a foto sem recorte: use [ImageInput](../ImageInput/README.md) (`data-ttsc-image-input`).
- **Não use** para upload de documentos (RG, histórico, comprovante): use [Dropzone](../Dropzone/README.md) — documentos não podem ser recortados.
- Para ampliar imagens apenas para visualização use [Lightbox](../Lightbox/README.md).

## Anatomia

```
┌──────────── .cropper-container ────────────┐   ┌ prévia ┐
│ .cropper-modal (véu)                        │   │  ( )   │  .cr-preview (border-radius 50%)
│      ┌ .cropper-crop-box ┐                  │   └────────┘
│      │ .cropper-view-box │  .cropper-point  │   [+][-][↻][⟲]   [Recortar e salvar]
│      └───────────────────┘                  │   (img) 256×256 JPEG
└─────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Palco | contêiner com altura fixa (`.cr-stage`) + `<img alt>` | sim |
| Imagem | `<img>` com `max-width: 100%` (Cropper envolve em `.cropper-container`) | sim |
| Caixa de recorte | `.cropper-crop-box` › `.cropper-view-box` / `.cropper-face` / `.cropper-point` | gerado |
| Prévia | elemento em `preview` (redondo para avatar) | recomendado |
| Ações | botões `ttsc-btn-icon` com `aria-label` | sim |
| Resultado | `<img>` ou envio direto do canvas | sim |

## Variantes

| Variante | Opções | Uso | Tokens |
|---|---|---|---|
| Avatar 1:1 redondo | `aspectRatio: 1`, `.cropper-view-box/face { border-radius: 50% }` | perfil, aluno | contorno `ttsc-accent`, véu `ttsc-scrim` |
| Logotipo | `aspectRatio: 4 / 1`, `viewMode: 1` | cabeçalho de documentos | idem |
| Livre | `aspectRatio: NaN` | anexos de comunicado | idem |
| Somente leitura | `cropper.disable()` | aguardando upload | `.cropper-disabled` |

## API

### Opções principais

| Opção | Padrão | Valor TTSC |
|---|---|---|
| `aspectRatio` | `NaN` | `1` |
| `viewMode` | `0` | `1` (caixa não sai da imagem) |
| `dragMode` | `'crop'` | `'move'` (arrasta a foto) |
| `autoCropArea` | `0.8` | `0.6` |
| `preview` | `''` | `'#avatar-preview'` |
| `background` / `guides` / `center` | `true` | `false` (visual limpo) |
| `toggleDragModeOnDblclick` | `true` | `false` |
| `minCropBoxWidth` | `0` | `96` |
| `checkOrientation` | `true` | `true` (EXIF de celular) |

### Métodos

| Método | Uso |
|---|---|
| `zoom(ratio)` / `zoomTo(ratio)` | `+0.1` / `-0.1` nos botões |
| `rotate(deg)` / `rotateTo(deg)` | `90` |
| `scaleX(-1)` / `scaleY(-1)` | espelhar |
| `reset()` / `clear()` | restaurar / remover caixa |
| `replace(url)` | trocar a imagem (novo arquivo) |
| `getData(rounded)` / `setData(data)` | `{x, y, width, height, rotate, scaleX, scaleY}` |
| `getCroppedCanvas({ width, height, fillColor, imageSmoothingQuality })` | canvas final (`toBlob` / `toDataURL`) |
| `setAspectRatio(r)` / `setDragMode(m)` | trocar em tempo real |
| `enable()` / `disable()` / `destroy()` | ciclo de vida (destrua ao fechar o modal) |

### Eventos (no `<img>` ou como opção)

| Evento | Quando |
|---|---|
| `ready` | imagem carregada e cropper montado |
| `cropstart` / `cropmove` / `cropend` | interação do usuário (`event.detail.action`) |
| `crop` | qualquer mudança (`event.detail` = dados) |
| `zoom` | antes do zoom (`event.detail.ratio`, cancelável) |

## Acessibilidade

- O recorte por mouse/toque não é acessível por teclado: **sempre** ofereça botões de zoom, girar e restaurar com `aria-label` (“Aproximar”, “Afastar”, “Girar 90 graus”) e um recorte automático centralizado (`autoCropArea`) que já é aceitável sem ajuste.
- `<img alt>` descrevendo a foto enviada; o resultado também com `alt`.
- Contorno da caixa em `ttsc-accent` (elemento gráfico, 3:1 sobre o véu `ttsc-scrim`); texto auxiliar em `ttsc-text-2`.
- Ao abrir em [Modal](../Modal/README.md), foco no primeiro botão; `Esc` cancela e chama `destroy()`.

## Modelos

### HTML

```html
<div class="ttsc-modal" data-ttsc-modal="true" id="modal-avatar">
  <div class="ttsc-modal-content" style="max-width: 640px">
    <div class="ttsc-modal-header"><h3 class="ttsc-modal-title">Foto de perfil</h3></div>
    <div class="ttsc-modal-body">
      <div class="grid gap-4" style="grid-template-columns: 1fr 180px">
        <div class="cr-stage"><img id="avatar-source" alt="Foto enviada"></div>
        <div class="flex flex-col gap-2">
          <div id="avatar-preview" class="cr-preview"></div>
          <div class="flex gap-1">
            <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-icon ttsc-btn-sm" aria-label="Aproximar" data-avatar="zoom-in"><i class="fa-light fa-magnifying-glass-plus"></i></button>
            <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-icon ttsc-btn-sm" aria-label="Afastar" data-avatar="zoom-out"><i class="fa-light fa-magnifying-glass-minus"></i></button>
            <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-icon ttsc-btn-sm" aria-label="Girar 90 graus" data-avatar="rotate"><i class="fa-light fa-rotate-right"></i></button>
          </div>
        </div>
      </div>
      <input type="file" id="avatar-file" accept="image/jpeg,image/png" class="ttsc-input mt-3">
    </div>
    <div class="ttsc-modal-footer">
      <button type="button" class="ttsc-btn ttsc-btn-ghost" data-ttsc-modal-dismiss="true">Cancelar</button>
      <button type="button" class="ttsc-btn ttsc-btn-primary" id="avatar-save"><i class="fa-light fa-crop-simple"></i> <span>Salvar foto</span></button>
    </div>
  </div>
</div>
```

### CSS

```css
/* assets/css/ttsc.cropper.css — tema do Cropper com tokens */
.cr-stage { height: 320px; background: var(--ttsc-canvas-2); border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-surface); overflow: hidden; }
.cr-stage img { display: block; max-width: 100%; }
.cr-stage .cropper-view-box { outline: 2px solid var(--ttsc-accent); border-radius: 50%; }
.cr-stage .cropper-face  { background-color: transparent; border-radius: 50%; }
.cr-stage .cropper-line, .cr-stage .cropper-point { background-color: var(--ttsc-accent); }
.cr-stage .cropper-point { width: 8px; height: 8px; opacity: 1; }
.cr-stage .cropper-modal { background-color: var(--ttsc-scrim); opacity: 1; }
.cr-preview { width: 96px; height: 96px; border-radius: 50%; overflow: hidden; border: 2px solid var(--ttsc-border); background: var(--ttsc-surface-2); }
```

### JS

```js
// assets/js/core/ttsc.avatar-cropper.js — requer /assets/vendors/cropper/cropper.min.{js,css}
const img = document.getElementById('avatar-source');
const fileInput = document.getElementById('avatar-file');
let cropper = null;

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (!file || !/^image\/(jpeg|png)$/.test(file.type)) return;
  if (file.size > 5 * 1024 * 1024) {
    TTSC.Toast?.show({ message: 'A foto deve ter até 5 MB.', variant: 'warning' });
    return;
  }
  const url = URL.createObjectURL(file);
  if (cropper) { cropper.replace(url); return; }
  img.src = url;
  cropper = new Cropper(img, {
    aspectRatio: 1, viewMode: 1, dragMode: 'move', autoCropArea: 0.6,
    background: false, guides: false, center: false, toggleDragModeOnDblclick: false,
    minCropBoxWidth: 96, preview: '#avatar-preview',
  });
});

document.querySelectorAll('[data-avatar]').forEach((btn) => btn.addEventListener('click', () => {
  if (!cropper) return;
  ({ 'zoom-in': () => cropper.zoom(0.1), 'zoom-out': () => cropper.zoom(-0.1), rotate: () => cropper.rotate(90) })[btn.dataset.avatar]();
}));

document.getElementById('avatar-save').addEventListener('click', async (event) => {
  if (!cropper) return;
  const button = event.currentTarget;
  button.disabled = true; button.setAttribute('aria-busy', 'true');
  try {
    const canvas = cropper.getCroppedCanvas({ width: 256, height: 256, fillColor: '#fff', imageSmoothingQuality: 'high' });
    // ProfileApiController::updateIdentity aceita photo_url em data:image (jpg/png) e grava em /uploads/avatars
    const res = await fetch('/api/v1/profile/me/identity', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ photo_url: canvas.toDataURL('image/jpeg', 0.9) }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const { data } = await res.json();
    document.querySelectorAll('[data-user-avatar]').forEach((el) => { el.src = data?.photo_url || el.src; });
    TTSC.Modal?.getInstance(document.getElementById('modal-avatar'))?.hide();
    TTSC.Toast?.show({ message: 'Foto de perfil atualizada.', variant: 'success' });
  } catch (e) {
    TTSC.Toast?.show({ message: 'Não foi possível salvar a foto.', variant: 'destructive' });
  } finally {
    button.disabled = false; button.removeAttribute('aria-busy');
  }
});
```

### SQL

O arquivo vai para `uploads/avatars/avatar_<uuid>_<timestamp>.jpg`; o banco guarda só o caminho em `users.avatar` (`varchar(255)`, banco master):

```sql
-- Gravar o novo avatar
UPDATE users
   SET avatar = :avatar_path,          -- ex.: '/uploads/avatars/avatar_<uuid>_1792500000.jpg'
       updated_at = CURRENT_TIMESTAMP
 WHERE uuid = :user_uuid
   AND deleted_at IS NULL;

-- Ler para o cabeçalho/perfil (fallback para iniciais quando NULL)
SELECT u.uuid, u.name, u.avatar
  FROM users u
 WHERE u.uuid = :user_uuid
   AND u.deleted_at IS NULL;
```

A view usa `<img data-user-avatar src="<?= $this->e($user['avatar']) ?>">` quando há caminho e o [Avatar](../Avatar/README.md) de iniciais quando `avatar IS NULL`. Apague o arquivo anterior após o `UPDATE` bem-sucedido.

## Faça / Não faça

- **Faça:** exportar em tamanho fixo (256×256) e JPEG 0,9 — avatares leves e iguais em toda a UI.
- **Faça:** validar tipo (jpg/png) e tamanho no cliente **e** no servidor; `destroy()` ao fechar o modal e `URL.revokeObjectURL`.
- **Faça:** `viewMode: 1` para a caixa nunca sair da foto.
- **Não faça:** gravar o base64 no banco — só o caminho do arquivo.
- **Não faça:** usar o cropper sem botões de teclado nem sem prévia.
- **Não faça:** enviar `image/webp`/`svg`: o endpoint atual só reconhece jpg, png e gif.
