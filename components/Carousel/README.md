# Carousel

Faixa rolável horizontal do ttscui (`data-ttsc-carousel`) com anterior/próximo, paginação, contador “2 / 5”, autoplay, arraste e vários itens por vista (`perView`).

> Também listado em: **Base › Carousel**.

## Quando usar

- Destaques e comunicados no portal do aluno/responsável (notícias de `institution_articles`, eventos da semana).
- Galeria de fotos de um evento, anexos de imagem de uma ocorrência, cartões de cursos em oferta (`perView` 3).
- Não use para conteúdo que o usuário **precisa** ver (avisos de bloqueio, pendências financeiras): metade do público nunca passa do 1º slide. Use um alerta ou um [Card](../Card/README.md).
- Para listas comparáveis (turmas, matrículas) use uma grade de cards ou [DataTable](../DataTable/README.md), não carrossel.

## Anatomia

```
┌ [data-ttsc-carousel] .ttsc-carousel ─────────────────────────────────┐
│ ┌ [data-ttsc-carousel-viewport] (overflow-x: auto, scroll-snap) ────┐ │
│ │ [item] [item] [item] …   ← [data-ttsc-carousel-item]              │ │
│ └───────────────────────────────────────────────────────────────────┘ │
│ (‹) [data-ttsc-carousel-prev]   ● ○ ○ ○  [-pagination]   2 / 5   (›) │
└───────────────────────────────────────────────────────────────────────┘
```

| Parte | Atributo / classe | Obrigatório |
|---|---|---|
| Raiz | `data-ttsc-carousel="true"` + `.ttsc-carousel` (extensão CSS) | sim |
| Viewport | `data-ttsc-carousel-viewport="true"` + `.ttsc-carousel-viewport` (se ausente, a raiz rola) | recomendado |
| Slide | `data-ttsc-carousel-item="true"` + `.ttsc-carousel-item` | sim (≥1, senão não inicializa) |
| Anterior / próximo | `button[data-ttsc-carousel-prev]` · `button[data-ttsc-carousel-next]` (vários permitidos) | não |
| Contador | `[data-ttsc-carousel-current]` · `[data-ttsc-carousel-total]` (texto preenchido pelo JS) | não |
| Paginação | `[data-ttsc-carousel-pagination]` > `button[data-ttsc-carousel-pagination-item]` (um por slide) | não |
| Miniaturas | `[data-ttsc-carousel-thumbnails]` > `[data-ttsc-carousel-thumbnail]` | não |

O módulo **não injeta CSS**: ele rola o viewport (`scrollTo`) e sincroniza o índice pelo `scroll`. Layout (flex, largura dos slides, snap, scrollbar) vem da extensão CSS abaixo — já pronta para ir ao chassi.

## Variantes

| Variante | Configuração | Uso | Tokens |
|---|---|---|---|
| Um por vista | `--ttsc-carousel-per-view: 1` | destaque/banner | slide `ttsc-surface`, borda `ttsc-border`, raio `ttsc-radius-surface` |
| Vários por vista | `--ttsc-carousel-per-view: 3` + `data-ttsc-carousel-per-view="3"` | cursos em oferta, fotos | gap `ttsc-space-3` |
| Centralizado | `data-ttsc-carousel-centered="true"` | galerias com slide parcial nas bordas | — |
| Autoplay | `data-ttsc-carousel-autoplay="true"` + `-autoplay-interval="6000"` | mural de comunicados | — |
| Snap / arraste | `data-ttsc-carousel-snap="true"` (CSS `scroll-snap`) ou `-draggable="true"` (mouse) | — | `snap` desativa `draggable` |

Paginação: ponto `ttsc-meta` (decorativo), ativo `ttsc-accent` alongado; controles são `ttsc-btn ttsc-btn-outline ttsc-btn-icon ttsc-btn-sm`.

## API

Opções (`data-ttsc-carousel-<opção>` na raiz, objeto em `getOrCreateInstance(el, {...})` ou propriedade CSS `--ttsc-carousel-<opção>`, que tem prioridade):

| Opção | Padrão | Efeito |
|---|---|---|
| `autoplay` | `false` | avança sozinho; desligado com `prefers-reduced-motion` ou 1 slide |
| `autoplayInterval` | `4000` | ms entre slides (mín. 200) |
| `pauseOnHover` | `true` | pausa em `mouseenter`/`focusin`, retoma em `mouseleave`/`focusout` |
| `infiniteLoop` | `false` | do último volta ao primeiro (e vice-versa) |
| `perView` | `1` | itens por vista (lido pela extensão CSS via `--ttsc-carousel-per-view`) |
| `centered` | `false` | centraliza o slide ativo ao rolar |
| `draggable` | `false` | arrastar com mouse (pointer events); ignorado se `snap: true` |
| `snap` | `false` | indica uso de `scroll-snap` (a extensão CSS aplica `scroll-snap-type`) |
| `autoHeight` | `false` | ajusta a altura do viewport ao slide ativo (ResizeObserver) |
| `showScrollbar` | `false` | grava `data-ttsc-carousel-show-scrollbar` na raiz (a extensão esconde a barra caso contrário) |
| `rtl` | `false` | inverte setas (também detecta `dir="rtl"`) |
| `lazy` | `false` | com `data-ttsc-carousel-lazy="true"` o `init()` **pula** o elemento; crie com `getOrCreateInstance` quando visível |
| `changeEvent` | `ttsc.carousel.change` | nome do evento de troca |

Métodos (`const c = ttscCarousel.getInstance(el)` / `TTSC.Carousel.getOrCreateInstance(el, opts)`):

| Método | Descrição |
|---|---|
| `next(userInitiated?)` · `prev(userInitiated?)` | avança/volta (respeita `infiniteLoop`) |
| `goTo(index, userInitiated?)` | vai ao slide (índice 0-based, limitado ao intervalo) |
| `getIndex()` · `getSlideCount()` | estado atual |
| `dispose()` | remove ouvintes, timers e observer |

Eventos (CustomEvent na raiz, `bubbles`): `ttsc.carousel.change` com `detail.payload = { index, prevIndex, userInitiated }`.

Teclado: `←`/`→` com foco dentro do carrossel (ignorado em inputs).

## Acessibilidade

- Raiz com `role="region"`, `aria-roledescription="carrossel"` e `aria-label` (“Comunicados da secretaria”); cada slide `role="group"`, `aria-roledescription="slide"`, `aria-label="2 de 5"`.
- Botões só-ícone com `aria-label` (“Comunicado anterior”/“Próximo comunicado”); pontos da paginação com `aria-label="Ir para o comunicado 3"` — o JS marca o ativo com `aria-current="true"`.
- Autoplay: pausa em foco/hover (padrão) e **sempre** ofereça um botão pausar; o módulo já respeita `prefers-reduced-motion`.
- Torne o viewport focável (`tabindex="0"`) para que `←`/`→` funcionem sem mouse.
- Texto dos slides em `ttsc-text`/`ttsc-text-2` sobre `ttsc-surface`; nunca texto sobre foto sem scrim (`ttsc-scrim`).

## Modelos

### HTML

```html
<div class="ttsc-carousel" data-ttsc-carousel="true" data-ttsc-carousel-autoplay="true" data-ttsc-carousel-autoplay-interval="6000"
     data-ttsc-carousel-infinite-loop="true" data-ttsc-carousel-snap="true"
     role="region" aria-roledescription="carrossel" aria-label="Comunicados da secretaria">
  <div class="ttsc-carousel-viewport" data-ttsc-carousel-viewport="true" tabindex="0">
    <?php foreach ($news as $i => $n): ?>
    <article class="ttsc-carousel-item" data-ttsc-carousel-item="true" role="group" aria-roledescription="slide"
             aria-label="<?= $i + 1 ?> de <?= count($news) ?>">
      <span class="ttsc-badge ttsc-badge-sm ttsc-badge-stroke"><?= $this->e($n['type_label']) ?></span>
      <h3><?= $this->e($n['title']) ?></h3>
      <p><?= $this->e($n['summary']) ?></p>
      <a class="ttsc-link ttsc-link-sm" href="<?= $this->e($n['url']) ?>">Ler comunicado</a>
    </article>
    <?php endforeach; ?>
  </div>
  <div class="ttsc-carousel-controls">
    <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-icon ttsc-btn-sm" data-ttsc-carousel-prev="true" aria-label="Comunicado anterior"><i class="fa-light fa-chevron-left"></i></button>
    <div class="ttsc-carousel-pagination" data-ttsc-carousel-pagination="true">
      <?php foreach ($news as $i => $n): ?>
      <button type="button" data-ttsc-carousel-pagination-item="true" aria-label="Ir para o comunicado <?= $i + 1 ?>"></button>
      <?php endforeach; ?>
    </div>
    <span class="ttsc-carousel-count"><span data-ttsc-carousel-current="true">1</span> / <span data-ttsc-carousel-total="true"><?= count($news) ?></span></span>
    <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-icon ttsc-btn-sm" data-ttsc-carousel-next="true" aria-label="Próximo comunicado"><i class="fa-light fa-chevron-right"></i></button>
  </div>
</div>
```

### CSS

```css
/* Extensão TTSC (o módulo ttscui não traz CSS de carrossel) */
.ttsc-carousel { --ttsc-carousel-per-view: 1; --ttsc-carousel-gap: var(--ttsc-space-3); display: flex; flex-direction: column; gap: var(--ttsc-space-3); }
.ttsc-carousel-viewport { display: flex; gap: var(--ttsc-carousel-gap); overflow-x: auto; overscroll-behavior-x: contain; scroll-behavior: smooth; }
.ttsc-carousel[data-ttsc-carousel-snap="true"] .ttsc-carousel-viewport { scroll-snap-type: x mandatory; }
.ttsc-carousel[data-ttsc-carousel-centered="true"] .ttsc-carousel-item { scroll-snap-align: center; }
.ttsc-carousel:not([data-ttsc-carousel-show-scrollbar]) .ttsc-carousel-viewport { scrollbar-width: none; }
.ttsc-carousel:not([data-ttsc-carousel-show-scrollbar]) .ttsc-carousel-viewport::-webkit-scrollbar { display: none; }
.ttsc-carousel[data-ttsc-carousel-draggable="true"] .ttsc-carousel-viewport { cursor: grab; user-select: none; }

.ttsc-carousel-item {
  flex: 0 0 calc((100% - (var(--ttsc-carousel-per-view) - 1) * var(--ttsc-carousel-gap)) / var(--ttsc-carousel-per-view));
  scroll-snap-align: start;
  background: var(--ttsc-surface); border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-surface);
  padding: var(--ttsc-space-5); color: var(--ttsc-text-2);
}
.ttsc-carousel-item h3 { font-size: 15px; font-weight: 600; color: var(--ttsc-text); margin: var(--ttsc-space-2) 0 var(--ttsc-space-1); }

.ttsc-carousel-controls { display: flex; align-items: center; gap: var(--ttsc-space-2); }
.ttsc-carousel-pagination { display: flex; gap: 6px; margin-inline: auto; }
.ttsc-carousel-pagination button { width: 8px; height: 8px; border-radius: var(--ttsc-radius-pill); background: var(--ttsc-meta); border: 0; padding: 0; cursor: pointer; transition: width .2s; }
.ttsc-carousel-pagination button[data-ttsc-carousel-pagination-active] { width: 20px; background: var(--ttsc-accent); }
.ttsc-carousel-count { font-size: 12px; color: var(--ttsc-text-muted); font-variant-numeric: tabular-nums; }

@media (max-width: 767px) { .ttsc-carousel { --ttsc-carousel-per-view: 1 !important; } }
```

### JS

```js
// Inicialização automática: TTSC.init() cria todos [data-ttsc-carousel] (exceto data-ttsc-carousel-lazy="true")
TTSC.init();

const root = document.querySelector('#mural-comunicados');
TTSC.Carousel.getOrCreateInstance(root);

// Registra a visualização do comunicado ativo (uma vez por slide)
const seen = new Set();
root.addEventListener('ttsc.carousel.change', (event) => {
  const { index, userInitiated } = event.detail.payload;
  const slide = root.querySelectorAll('[data-ttsc-carousel-item]')[index];
  if (!slide || seen.has(slide.dataset.uuid)) return;
  seen.add(slide.dataset.uuid);
  navigator.sendBeacon('/api/v1/institution/articles/view', new URLSearchParams({ uuid: slide.dataset.uuid, manual: userInitiated ? 1 : 0 }));
});

// Botão pausar/retomar do autoplay (WCAG 2.2.2)
document.querySelector('#mural-pausa').addEventListener('click', (event) => {
  const btn = event.currentTarget;
  const paused = btn.getAttribute('aria-pressed') === 'true';
  TTSC.Carousel.getInstance(root).dispose();           // dispose() limpa timers e a instância
  TTSC.Carousel.getOrCreateInstance(root, { autoplay: paused });
  btn.setAttribute('aria-pressed', paused ? 'false' : 'true');
  btn.querySelector('i').className = paused ? 'fa-light fa-pause' : 'fa-light fa-play';
});

// Carrossel em aba escondida: crie só quando visível
document.querySelectorAll('[data-ttsc-carousel-lazy="true"]').forEach((el) => {
  new IntersectionObserver(([entry], obs) => {
    if (entry.isIntersecting) { TTSC.Carousel.getOrCreateInstance(el); obs.disconnect(); }
  }).observe(el);
});
```

### SQL

```sql
-- Comunicados/eventos publicados para o mural do portal (MariaDB 10.11 / MySQL 8)
SELECT a.uuid, a.item_type, a.title, a.summary, a.url, a.published_at
  FROM institution_articles a
 WHERE a.tenant_id = :tenant_id
   AND a.status = 'published'
   AND a.item_type IN ('news', 'event')
   AND a.published_at <= CURDATE()
   AND a.deleted_at IS NULL
 ORDER BY a.published_at DESC, a.id DESC
 LIMIT 8;
```

O controller passa `$news` (até 8 linhas) para a view, com `type_label` traduzido de `item_type` (“Notícia”, “Evento”); com 1 linha só, renderize um card simples em vez do carrossel.

## Faça / Não faça

- **Faça:** 3–8 slides; mesmo formato e altura em todos (ou `autoHeight`).
- **Faça:** contador “2 / 5” ou paginação sempre visível; setas fora da área de texto.
- **Faça:** autoplay ≥ 6 s com pausa no hover/foco e botão pausar.
- **Não faça:** carrossel para avisos obrigatórios ou para a única ação da página.
- **Não faça:** texto branco sobre foto sem `ttsc-scrim`; pontos da paginação como único controle.
