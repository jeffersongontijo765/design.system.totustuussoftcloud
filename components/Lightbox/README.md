# Fullscreen Lightbox

Visualizador de imagens em tela cheia com fslightbox 3.4.1 — galerias por `data-fslightbox`, navegação por setas/teclado/gesto, tela cheia e reinicialização com `refreshFsLightbox()` para itens inseridos dinamicamente.

## Quando usar

- Galerias de fotos de eventos (Feira de Ciências, formatura), portfólio do aluno, fotos de ocorrências e vistorias de patrimônio.
- Ampliar uma imagem que aparece reduzida num card ou tabela (miniatura de comprovante em imagem).
- **Não use** para PDFs ou documentos: abra em nova aba ou no visualizador de documentos. **Não use** para vídeos de terceiros com iframe (proibido no preview; em produção, só com consentimento de cookies de terceiros).
- **Não use** para conteúdo com formulário/ações: isso é [Modal](../Modal/README.md) ou [Drawer](../Drawer/README.md).
- Para recortar a imagem antes de salvar, use [Cropper](../Cropper/README.md).

## Anatomia

```
a.lb-thumb[href=<imagem grande>][data-fslightbox="<galeria>"][data-type="image"]
└── img (miniatura, alt) + selo .lb-zoom (fa-magnifying-glass-plus)

.fslightbox-container (criado no body, fixed)
├── .fslightbox-toolbar          [ tela cheia ] [ fechar ]
├── .fslightbox-slide-number-container   "2 / 4"
├── .fslightbox-slide-btn-container-previous / -next
└── .fslightbox-source (img)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Gatilho | `<a href="…">` com `data-fslightbox="<nome-da-galeria>"` | sim |
| Tipo | `data-type="image"` (obrigatório para URLs sem extensão, `data:` ou rotas PHP) | recomendado |
| Miniatura | `<img alt>` dentro do link | sim |
| Rótulo do link | `aria-label="Ampliar foto 2 de 4: …"` | sim |
| Classe extra no slide | `data-class` / `data-custom-class` | não |
| Pôster de vídeo | `data-video-poster` | não |

## Variantes

| Variante | Como | Uso | Tokens |
|---|---|---|---|
| Galeria | vários links com o mesmo `data-fslightbox` | álbum de evento | miniaturas `ttsc-border`, `ttsc-radius-control` |
| Imagem única | `data-fslightbox` com nome exclusivo | comprovante, foto de ocorrência | idem |
| Programático | `fsLightboxInstances['nome'].open(i)` ou `new FsLightbox()` com `props.sources` | abrir a partir de botão/tabela | — |
| Grade de miniaturas | `.lb-grid` 4 colunas / 2 no mobile | — | foco `ttsc-accent` |

O overlay do fslightbox é sempre escuro (independe do tema), com ícones claros — contraste garantido nos dois temas.

## API

| Item | Descrição |
|---|---|
| `refreshFsLightbox()` | global; varre de novo os `[data-fslightbox]` (após AJAX/render dinâmico) |
| `fsLightboxInstances['<nome>']` | instância por galeria |
| `.open(index?)` / `.close()` | abrir no slide `index` (0-based) / fechar |
| `.props.sources` | array de URLs (ou seletor `#id` de elemento a clonar) |
| `.props.types` | `['image', …]` por índice |
| `.props.customAttributes` / `.props.customClasses` | atributos/classes por slide (`alt`, `class`) |
| `.props.slideDistance` | distância entre slides (padrão `0.3`) |
| `.props.exitFullscreenOnClose` | sai da tela cheia ao fechar |
| `.props.loadOnlyCurrentSource` | carrega só o slide atual (galerias grandes) |
| `.props.disableLocalStorage` | não guarda o tipo detectado por URL |
| `.props.onInit` / `onOpen` / `onShow` / `onClose` | callbacks do ciclo de vida |
| Teclado | `←`/`→` navegam, `Esc` fecha, `F11`/botão tela cheia |

## Acessibilidade

- Cada miniatura é um `<a href>` focável com `aria-label` descritivo e `<img alt>` com o conteúdo da foto (não “imagem 1”).
- O link funciona sem JS (abre a imagem) — progressive enhancement.
- Teclado: `Enter` abre, setas navegam, `Esc` fecha; ao fechar o foco volta ao link (`onClose` + `focus()` se necessário).
- Use `figcaption` visível com a legenda; o lightbox não lê legendas — mantenha `alt` útil.
- Foco da miniatura com contorno 2px `ttsc-accent`; selo de zoom em `ttsc-surface` + `ttsc-text`.

## Modelos

### HTML

```html
<div class="lb-grid">
  <?php foreach ($photos as $i => $photo): ?>
    <figure style="margin:0">
      <a class="lb-thumb" href="<?= $this->e($photo['url']) ?>" data-fslightbox="evento-<?= $this->e($eventUuid) ?>"
         data-type="image"
         aria-label="Ampliar foto <?= $i + 1 ?> de <?= count($photos) ?>: <?= $this->e($photo['alt_text']) ?>">
        <img src="<?= $this->e($photo['thumb_url'] ?? $photo['url']) ?>" alt="<?= $this->e($photo['alt_text']) ?>" loading="lazy">
        <span class="lb-zoom" aria-hidden="true"><i class="fa-light fa-magnifying-glass-plus"></i></span>
      </a>
      <figcaption class="lb-caption"><?= $this->e($photo['description']) ?></figcaption>
    </figure>
  <?php endforeach; ?>
</div>
<script src="/assets/vendors/fslightbox/fslightbox.js"></script>
```

### CSS

```css
.lb-grid  { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--ttsc-space-3); }
@media (max-width: 640px) { .lb-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.lb-thumb { position: relative; display: block; aspect-ratio: 4 / 3; overflow: hidden;
  border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control); background: var(--ttsc-surface-2); }
.lb-thumb img { width: 100%; height: 100%; object-fit: cover; transition: transform .2s ease; }
.lb-thumb:hover img { transform: scale(1.03); }
.lb-thumb:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.lb-thumb .lb-zoom { position: absolute; right: 6px; bottom: 6px; width: 26px; height: 26px; display: flex; align-items: center; justify-content: center;
  background: var(--ttsc-surface); color: var(--ttsc-text); border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-sm); }
.lb-caption { font-size: 12px; color: var(--ttsc-text-2); margin-top: var(--ttsc-space-1); }
/* fslightbox acima de drawers/modais do chassi */
.fslightbox-container { font-family: inherit; z-index: var(--ttsc-z-modal) !important; }
```

### JS

```js
// assets/js/core/ttsc.lightbox.js — requer /assets/vendors/fslightbox/fslightbox.js
export async function loadEventGallery(container, eventUuid) {
  const res = await fetch(`/admin/academic/events/${encodeURIComponent(eventUuid)}/photos`, { headers: { Accept: 'application/json' } });
  const photos = await res.json();
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  container.innerHTML = photos.map((p, i) => `
    <figure style="margin:0">
      <a class="lb-thumb" href="${esc(p.url)}" data-fslightbox="evento-${esc(eventUuid)}" data-type="image"
         aria-label="Ampliar foto ${i + 1} de ${photos.length}: ${esc(p.alt_text)}">
        <img src="${esc(p.url)}" alt="${esc(p.alt_text)}" loading="lazy">
      </a>
      <figcaption class="lb-caption">${esc(p.description)}</figcaption>
    </figure>`).join('');

  refreshFsLightbox();                                   // itens novos no DOM
  const lightbox = fsLightboxInstances[`evento-${eventUuid}`];
  if (!lightbox) return;
  lightbox.props.exitFullscreenOnClose = true;
  lightbox.props.loadOnlyCurrentSource = photos.length > 30;
  let opener = null;
  lightbox.props.onOpen = () => { opener = document.activeElement; };
  lightbox.props.onClose = () => opener?.focus();        // devolve o foco à miniatura
}

// Abrir a partir de um botão "Ver fotos" (slide 0)
document.addEventListener('click', (event) => {
  const btn = event.target.closest('[data-open-gallery]');
  if (btn) fsLightboxInstances[btn.dataset.openGallery]?.open(0);
});
```

### SQL

As imagens ficam na biblioteca de mídia (`cms_media`), agrupadas por `folder`; o banco guarda URL, dimensões e texto alternativo:

```sql
SELECT m.uuid, m.url, m.alt_text, m.description, m.width, m.height
  FROM cms_media m
 WHERE m.tenant_id = :tenant_id
   AND m.deleted_at IS NULL
   AND m.mime_type LIKE 'image/%'
   AND m.folder = :folder              -- ex.: 'eventos/feira-de-ciencias-2026'
 ORDER BY m.created_at
 LIMIT 48;
```

O controller passa o array para a view (ou devolve JSON para `loadEventGallery`). Para portfólio do aluno, a fonte é `student_portfolios.file_path` filtrando `enrollment_uuid`, `is_public = 1` e `deleted_at IS NULL`.

## Faça / Não faça

- **Faça:** `data-type="image"` quando a URL não termina em extensão (rotas PHP, `data:`), evitando a detecção por XHR.
- **Faça:** miniaturas leves (`loading="lazy"` ou [Lozad](../Lozad/README.md)) e imagem grande só no `href`.
- **Faça:** chamar `refreshFsLightbox()` após inserir itens por AJAX.
- **Não faça:** misturar fotos de alunos em galeria pública sem `is_public` / autorização de uso de imagem.
- **Não faça:** colocar ações (excluir, aprovar) dentro do lightbox — use o card ou um drawer.
- **Não faça:** reutilizar o mesmo nome de galeria em listas diferentes da página.
