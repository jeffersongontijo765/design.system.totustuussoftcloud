# ImageInput

Seletor de imagem com prévia circular (`data-ttsc-image-input`, ttscui) para avatar de usuário, foto do aluno e logotipo da unidade: troca, remove e restaura a imagem salva, sinalizando a remoção num `input[type=hidden]`.

> Também listado em: **Formulários › Image Input (plugins)**.

## Quando usar

- Uma única imagem que representa o registro: avatar (`users.avatar`), foto 3×4 do aluno, logo da unidade.
- Quando a prévia imediata importa mais que a fila de upload.
- Precisa recortar/girar antes de enviar? Combine com [Cropper](../Cropper/README.md) no evento `change`.
- Vários arquivos ou documentos: use [FileInput](../FileInput/README.md); upload em lote com progresso: [Dropzone](../Dropzone/README.md).

## Anatomia

```
   ┌──────────┐ (×)  ← [data-ttsc-image-input-remove] .ttsc-image-input-remove (hidden quando não há o que remover)
   │  prévia  │      ← [data-ttsc-image-input-placeholder] .ttsc-image-input-placeholder (clique abre o seletor)
   │  ( AB )  │         └ [data-ttsc-image-input-preview] .ttsc-image-input-preview (background-image)
   │ [câmera] │         └ faixa "Alterar" (dentro do placeholder)
   └──────────┘
 input[type=file] (oculto)   input[type=hidden] (= "1" quando a imagem salva foi removida)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Raiz | `.ttsc-image-input` + `data-ttsc-image-input="true"`; recebe `empty` / `changed` | sim |
| Arquivo | `input[type=file]` com `name` e `accept` (oculto pelo runtime) | sim |
| Remoção | `input[type=hidden]` com `name` (ex.: `avatar_remove`) | sim |
| Área clicável | `.ttsc-image-input-placeholder` + `data-ttsc-image-input-placeholder` | sim |
| Prévia | `.ttsc-image-input-preview` + `data-ttsc-image-input-preview`; imagem salva em `style="background-image: url(…)"` | sim |
| Remover | `.ttsc-image-input-remove` + `data-ttsc-image-input-remove` (botão) | sim (o JS assume que existe) |
| Alterar | faixa/ícone **dentro** do placeholder. `data-ttsc-image-input-change` é só marcador: o build atual não lê esse atributo — o clique funciona por estar no placeholder | não |

## Estados

| Estado | Classe na raiz | Remover | Hidden | Tokens |
|---|---|---|---|---|
| Vazio (sem imagem salva) | `empty` | escondido | `""` | placeholder `ttsc-canvas-2`, ícone `ttsc-text-muted`, borda `--input` |
| Imagem salva | — | visível | `""` | borda `ttsc-border` |
| Nova imagem escolhida | `changed` | visível (“desfazer”) | `""` | anel `ttsc-accent` (extensão) |
| Salva removida | `empty` | escondido se não há salva para restaurar | `"1"` | — |
| Foco | — | — | — | contorno 2px `ttsc-accent` no placeholder |

Ciclo do botão remover (fonte): **nova** → volta à salva (ou vazio) · **salva** → vazio + hidden `1` · **vazio após remover** → restaura a salva.

## API

Conferida em `src/components/image-input/image-input.ts`.

| Opção | Atributo | Padrão | Descrição |
|---|---|---|---|
| `hiddenClass` | `data-ttsc-image-input-hidden-class` | `"hidden"` | classe para esconder o botão remover |

| Método | Descrição |
|---|---|
| `ttscImageInput.getInstance(el)` / `getOrCreateInstance(el, cfg)` | instância |
| `getSelectedFile()` | `File` escolhido ou `null` |
| `isChanged()` / `isEmpty()` | há / não há arquivo novo selecionado |
| `remove()` | mesmo efeito do botão remover |
| `getPreviewUrl()` / `setPreviewUrl(url)` | URL da imagem salva (usada para restaurar) |
| `update()` | relê o `background-image` da prévia (após trocá-lo por JS) |

| Evento (DOM, na raiz) | `detail.payload` | Cancelável |
|---|---|---|
| `change` | `{ cancel }` — antes de ler o arquivo | sim (`payload.cancel = true`, ex.: arquivo grande) |
| `changed` | `null` — prévia aplicada | não |
| `remove` | `{ cancel }` antes; dispara de novo com `null` depois | sim (no primeiro) |

O `change` do `input[type=file]` também borbulha até a raiz: filtre por `event.detail?.payload`.

## Acessibilidade

- O placeholder é uma `div`: dê `role="button"`, `tabindex="0"` e `aria-label="Alterar foto"`, e trate Enter/Espaço (ver JS) — o ttscui só escuta clique.
- O remover é `<button type="button" aria-label="Remover foto">`.
- Anuncie o resultado em `aria-live` (“Nova foto selecionada”, “Foto removida”).
- A prévia é decorativa; o nome da pessoa está no formulário. Iniciais (sem foto) com `ttsc-text-2` sobre `ttsc-canvas-2`.

## Modelos

### HTML

```html
<div class="ttsc-form-item">
  <span class="ttsc-form-label" id="avatar-label">Foto do perfil</span>
  <div class="ttsc-image-input" data-ttsc-image-input="true" aria-labelledby="avatar-label">
    <input type="file" name="avatar" accept=".png,.jpg,.jpeg,.webp">
    <input type="hidden" name="avatar_remove">
    <button type="button" class="ttsc-image-input-remove" data-ttsc-image-input-remove aria-label="Remover foto">
      <i class="fa-light fa-xmark"></i>
    </button>
    <div class="ttsc-image-input-placeholder" data-ttsc-image-input-placeholder role="button" tabindex="0" aria-label="Alterar foto">
      <span class="ttsc-image-input-initials" aria-hidden="true"><?= $this->e($initials) ?></span>
      <div class="ttsc-image-input-preview" data-ttsc-image-input-preview
           <?php if ($user['avatar']): ?>style="background-image: url('<?= $this->e($avatarUrl) ?>')"<?php endif ?>></div>
      <span class="ttsc-image-input-change" data-ttsc-image-input-change aria-hidden="true"><i class="fa-light fa-camera"></i></span>
    </div>
  </div>
  <div class="ttsc-form-description">PNG, JPG ou WEBP, até 2 MB. Recomendado 400×400.</div>
</div>
```

### CSS

```css
/* Ponte (bundle.css): placeholder/remover usam --border, --background e --muted-foreground */
.ttsc-image-input-placeholder { background-color: var(--ttsc-canvas-2); display: flex; align-items: center; justify-content: center; }
.ttsc-image-input-placeholder:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.ttsc-image-input-preview { position: absolute; inset: 0; }
.ttsc-image-input-initials { font-weight: 600; font-size: 20px; color: var(--ttsc-text-2); }
.ttsc-image-input:not(.empty) .ttsc-image-input-initials { visibility: hidden; }
.ttsc-image-input-change {
  position: absolute; inset-inline: 0; bottom: 0; height: 22px; display: flex; align-items: center; justify-content: center;
  background: var(--ttsc-scrim); color: var(--ttsc-surface); font-size: 11px; opacity: 0; transition: opacity .15s;
}
.ttsc-image-input:hover .ttsc-image-input-change,
.ttsc-image-input-placeholder:focus-visible .ttsc-image-input-change { opacity: 1; }
.ttsc-image-input.changed .ttsc-image-input-placeholder { box-shadow: 0 0 0 2px var(--ttsc-surface), 0 0 0 4px var(--ttsc-accent); }
.ttsc-image-input-remove.hidden { display: none; }
.ttsc-image-input-remove:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 1px; }
/* Logo de unidade: quadrado */
.ttsc-image-input.is-square .ttsc-image-input-placeholder,
.ttsc-image-input.is-square .ttsc-image-input-preview { border-radius: var(--ttsc-radius-control); background-size: contain; background-position: center; }
```

### JS

```js
TTSC.init();

const MAX = 2 * 1024 * 1024;

document.querySelectorAll('[data-ttsc-image-input]').forEach((root) => {
  const instance = ttscImageInput.getOrCreateInstance(root);
  const file = root.querySelector('input[type=file]');
  const status = root.closest('.ttsc-form-item').querySelector('[aria-live]');

  // Valida antes da prévia: o change do ttscui é cancelável
  root.addEventListener('change', (event) => {
    const payload = event.detail?.payload;
    if (!payload) return; // change nativo do input borbulhando
    const f = file.files[0];
    if (!f || !/^image\/(png|jpe?g|webp)$/.test(f.type) || f.size > MAX) {
      payload.cancel = true;
      file.value = '';
      if (status) status.textContent = 'Use PNG, JPG ou WEBP de até 2 MB.';
    }
  });
  root.addEventListener('changed', () => { if (status) status.textContent = 'Nova foto selecionada. Salve para aplicar.'; });
  root.addEventListener('remove', (event) => {
    if (event.detail?.payload) return; // primeiro disparo (cancelável)
    if (status) status.textContent = root.classList.contains('empty') ? 'Foto removida.' : 'Foto restaurada.';
  });

  // Teclado no placeholder (o ttscui só trata clique)
  root.querySelector('[data-ttsc-image-input-placeholder]').addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); file.click(); }
  });
});

// Envio via fetch (perfil): multipart com o arquivo e a flag de remoção
document.querySelector('#profile-form')?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const res = await fetch(form.action, { method: 'POST', body: new FormData(form) });
  if (res.ok) {
    const { avatar_url: url } = await res.json();
    const root = form.querySelector('[data-ttsc-image-input]');
    root.querySelector('[data-ttsc-image-input-preview]').style.backgroundImage = url ? `url("${url}")` : 'none';
    ttscImageInput.getInstance(root).update();
  }
});
```

### SQL

O avatar é `users.avatar varchar(255)` (caminho no storage) no banco master `totustuus_master` (o tenant tem a mesma coluna espelhada):

```sql
-- Carregar a prévia
SELECT uuid, name, avatar
  FROM users
 WHERE uuid = :user_uuid
   AND deleted_at IS NULL;

-- Nova imagem enviada (após gravar o arquivo e obter o caminho)
UPDATE users
   SET avatar = :avatar_path, updated_at = NOW()
 WHERE uuid = :user_uuid
   AND deleted_at IS NULL;

-- avatar_remove = "1" e nenhum arquivo novo: volta às iniciais
UPDATE users
   SET avatar = NULL, updated_at = NOW()
 WHERE uuid = :user_uuid
   AND deleted_at IS NULL;
```

O controller decide pela ordem: arquivo novo válido (MIME real via `finfo`, ≤ 2 MB, redimensionado para 400×400) → `UPDATE … avatar = :avatar_path`; senão `avatar_remove === '1'` → `NULL` e apaga o arquivo antigo; senão não toca na coluna. A view monta a URL pública a partir de `avatar` e, quando nulo, mostra as iniciais de `name`.

## Faça / Não faça

- **Faça:** sempre incluir o `input[type=hidden]` e o botão remover — o JS do ttscui espera os dois.
- **Faça:** validar tipo/tamanho no evento `change` (cancelável) e de novo no servidor.
- **Não faça:** colocar o “Alterar” fora do placeholder esperando que `data-ttsc-image-input-change` funcione.
- **Não faça:** gravar a imagem em base64 no banco; guarde só o caminho em `users.avatar`.
