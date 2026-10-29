# Tiny Slider

Carrossel tiny-slider 2.9.4 (`tns()`) para avisos e destaques — 1/2/3 cartões por vista conforme a largura, controles e paginação com botões do chassi, autoplay com pausa e anúncio acessível da posição.

## Quando usar

- Faixa de **avisos** no painel do aluno/responsável ou na home do portal, quando há mais cartões do que cabem na largura e todos têm o mesmo peso.
- Quando precisar de recursos que o carrossel nativo não tem: `responsive` por breakpoint com `gutter`, `edgePadding` (espiar o próximo), `axis: 'vertical'`, `lazyload`, `rewind`.
- **Prefira o [Carousel](../Carousel/README.md) do ttscui** (`data-ttsc-carousel`) para carrosséis comuns: é declarativo, já segue o tema e não adiciona dependência. Use tiny-slider só quando uma das opções acima for necessária.
- **Não use** para informação obrigatória (bloqueio de matrícula, boleto vencido): isso é alerta fixo. Para listas comparáveis (turmas, cursos) use grade de cards.

## Anatomia

```
section[aria-roledescription="carrossel"][aria-label="Avisos da escola"]
├── cabeçalho: "Avisos"   [⏸ pausar]  #ts-controls [‹][›]   (controlsContainer)
├── .tns-outer > .tns-ovh > .tns-inner > #ts-slider.tns-slider
│     └── .tns-item > article.ts-card   badge · título · resumo · data · "Ver detalhes"
├── #ts-nav  (navContainer)  ● ○ ○ ○ ○   .tns-nav-active
└── .ts-live [aria-live=polite]  "Avisos 1 a 3 de 5"
```

| Parte | Classe / opção | Obrigatório |
|---|---|---|
| Região | `section[aria-roledescription="carrossel"][aria-label]` | sim |
| Contêiner | `container: '#id'` — cada filho direto vira um slide | sim |
| Slide | wrapper `<div>` + `article.ts-card` (o `gutter` vira padding do wrapper) | sim |
| Controles | `controlsContainer` com dois `ttsc-btn-icon` + `aria-label` | sim |
| Paginação | `navContainer` com um `button[aria-label="Aviso n"]` por slide | recomendado |
| Pausa | botão próprio + `autoplayButtonOutput: false` | sim com autoplay |
| Anúncio | `aria-live="polite"` atualizado em `indexChanged` | sim |

## Variantes

| Variante | Opções | Uso | Tokens |
|---|---|---|---|
| Responsivo | `items: 1`, `responsive: { 560: { items: 2 }, 900: { items: 3 } }`, `gutter: 12` | avisos no painel | cartão `ttsc-surface` + `ttsc-border` + `ttsc-radius-surface` |
| Destaque único | `items: 1`, `edgePadding: 40` | banner de evento | — |
| Autoplay | `autoplay: true`, `autoplayTimeout: 6000`, `autoplayHoverPause: true` | home do portal | — |
| Paginação | `.tns-nav-active` | — | ativo `ttsc-accent` (24px), inativo `ttsc-border-strong` |
| Categoria | badge no cartão | prazo/evento/notícia/recesso | `ttsc-badge-warning/-info/-success/-destructive` |

## API

### Opções

| Opção | Padrão | Valor TTSC |
|---|---|---|
| `container` | `'.slider'` | `'#ts-slider'` |
| `items` / `slideBy` | `1` / `1` | `1` / `1` (+ `responsive`) |
| `gutter` / `edgePadding` | `0` / `0` | `12` / `0` |
| `loop` / `rewind` | `true` / `false` | `false` / `true` (sem clones no DOM, melhor para leitores) |
| `controlsContainer` / `navContainer` | `false` | contêineres próprios com botões `ttsc-btn` |
| `controls` / `nav` / `controlsText` | `true` / `true` / `['prev','next']` | via contêineres próprios |
| `autoplay`, `autoplayTimeout`, `autoplayHoverPause`, `autoplayButtonOutput` | `false`, `5000`, `false`, `true` | `!reduceMotion`, `6000`, `true`, `false` |
| `speed` | `300` | `350`; `0` com reduced motion |
| `mouseDrag` / `touch` / `preventScrollOnTouch` | `false` / `true` / `false` | `true` / `true` / `'auto'` |
| `lazyload` / `lazyloadSelector` | `false` / `'.tns-lazy-img'` | imagens dos avisos |
| `responsive` | `false` | `{ 560: { items: 2 }, 900: { items: 3 } }` |

### Métodos e eventos

| API | Uso |
|---|---|
| `slider.getInfo()` | `{ index, displayIndex, items, slideCount, … }` |
| `slider.goTo(n \| 'next' \| 'prev' \| 'first' \| 'last')` | navegar |
| `slider.play()` / `slider.pause()` | autoplay |
| `slider.destroy()` / `slider.rebuild()` | ciclo de vida (após trocar os avisos) |
| `slider.events.on('indexChanged', fn)` | atualizar o `aria-live` |
| `events.on('transitionEnd' \| 'dragStart' \| 'newBreakpointEnd', fn)` | outros ganchos |

## Acessibilidade

- Região nomeada (`aria-label="Avisos da escola"`) com `aria-roledescription="carrossel"`; slides fora da vista recebem `aria-hidden` e `tabindex="-1"` nos links (tiny-slider faz isso).
- Botão de **pausar** visível sempre que houver autoplay (WCAG 2.2.2); `autoplayHoverPause` também pausa no foco/hover.
- Controles e bolinhas com `aria-label` em pt-BR; foco 2px `ttsc-accent`.
- `prefers-reduced-motion`: sem autoplay e `speed: 0`.
- Posição anunciada (“Avisos 1 a 3 de 5”) em `aria-live="polite"`, não a cada tick do autoplay além do necessário.

## Modelos

### HTML

```html
<section aria-roledescription="carrossel" aria-label="Avisos da escola">
  <div class="ts-head">
    <h3>Avisos</h3>
    <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" id="ts-play" aria-label="Pausar rotação automática"><i class="fa-light fa-pause"></i></button>
    <div id="ts-controls" class="flex gap-1">
      <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-icon ttsc-btn-sm" aria-label="Aviso anterior"><i class="fa-light fa-chevron-left"></i></button>
      <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-icon ttsc-btn-sm" aria-label="Próximo aviso"><i class="fa-light fa-chevron-right"></i></button>
    </div>
  </div>
  <div id="ts-slider">
    <?php foreach ($notices as $n): ?>
      <div>
        <article class="ts-card">
          <span class="ttsc-badge ttsc-badge-sm ttsc-badge-outline <?= $this->e($badgeClass[$n['item_type']] ?? '') ?>"><?= $this->e($n['type_label']) ?></span>
          <h4><?= $this->e($n['title']) ?></h4>
          <p><?= $this->e($n['summary']) ?></p>
          <div class="ts-meta">
            <span><?= $this->e(date('d/m/Y', strtotime($n['published_at']))) ?></span>
            <a href="<?= $this->e($n['url']) ?>">Ver detalhes</a>
          </div>
        </article>
      </div>
    <?php endforeach; ?>
  </div>
  <div class="ts-nav" id="ts-nav">
    <?php foreach ($notices as $i => $n): ?><button type="button" aria-label="Aviso <?= $i + 1 ?>"></button><?php endforeach; ?>
  </div>
  <div class="ts-live" aria-live="polite"></div>
</section>
<link rel="stylesheet" href="/assets/vendors/tiny-slider/tiny-slider.css">
<script src="/assets/vendors/tiny-slider/tiny-slider.js"></script>
```

### CSS

```css
.ts-head { display: flex; align-items: center; gap: var(--ttsc-space-2); }
.ts-head h3 { margin: 0 auto 0 0; font-size: 14px; font-weight: 600; color: var(--ttsc-text); }
.ts-card { display: flex; flex-direction: column; gap: var(--ttsc-space-2); height: 168px; padding: 14px;
  background: var(--ttsc-surface); border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-surface); }
.ts-card h4 { margin: 0; font-size: 14px; font-weight: 600; color: var(--ttsc-text); }
.ts-card p { flex: 1; margin: 0; font-size: 12px; line-height: 1.5; color: var(--ttsc-text-2); overflow: hidden; }
.ts-card .ts-meta { display: flex; justify-content: space-between; font-size: 11px; color: var(--ttsc-text-muted); }
.ts-card a { color: var(--ttsc-accent-text); font-weight: 500; }
.ts-nav { display: flex; justify-content: center; gap: 6px; margin-top: 10px; }
.ts-nav button { width: 8px; height: 8px; padding: 0; border: 0; border-radius: var(--ttsc-radius-pill); background: var(--ttsc-border-strong); transition: width .2s ease; }
.ts-nav button.tns-nav-active { width: 20px; background: var(--ttsc-accent); }
.ts-nav button:focus-visible, .ts-card a:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.ts-live { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
```

### JS

```js
// assets/js/core/ttsc.notices-slider.js — requer tiny-slider.js (global tns)
export function initNoticesSlider(root = document) {
  const container = root.querySelector('#ts-slider');
  if (!container || !container.children.length) return null;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const slider = tns({
    container,
    items: 1, slideBy: 1, gutter: 12,
    loop: false, rewind: true,
    controlsContainer: root.querySelector('#ts-controls'),
    navContainer: root.querySelector('#ts-nav'),
    autoplay: !reduceMotion, autoplayTimeout: 6000, autoplayHoverPause: true, autoplayButtonOutput: false,
    speed: reduceMotion ? 0 : 350,
    mouseDrag: true, preventScrollOnTouch: 'auto',
    responsive: { 560: { items: 2 }, 900: { items: 3 } },
  });

  const live = root.querySelector('.ts-live');
  slider.events.on('indexChanged', (info) => {
    const first = info.displayIndex;
    const last = Math.min(first + info.items - 1, info.slideCount);
    live.textContent = `Avisos ${first}${last > first ? ` a ${last}` : ''} de ${info.slideCount}`;
  });

  const playBtn = root.querySelector('#ts-play');
  let playing = !reduceMotion;
  const sync = () => {
    playBtn.setAttribute('aria-label', playing ? 'Pausar rotação automática' : 'Retomar rotação automática');
    playBtn.innerHTML = `<i class="fa-light fa-${playing ? 'pause' : 'play'}"></i>`;
  };
  playBtn.addEventListener('click', () => { playing ? slider.pause() : slider.play(); playing = !playing; sync(); });
  if (reduceMotion) playBtn.hidden = true;
  sync();
  return slider;
}

document.addEventListener('DOMContentLoaded', () => initNoticesSlider());
```

### SQL

Os avisos vêm das publicações institucionais (`institution_articles`, `item_type` `news`/`event`, `status` `published`):

```sql
SELECT a.uuid, a.item_type, a.title, a.summary, a.url, a.published_at
  FROM institution_articles a
 WHERE a.tenant_id = :tenant_id
   AND a.deleted_at IS NULL
   AND a.status = 'published'
   AND a.item_type IN ('news', 'event')
   AND a.published_at <= CURDATE()
 ORDER BY a.published_at DESC, a.id DESC
 LIMIT 6;
```

O controller traduz `item_type` para o rótulo/badge (catálogo `ref_enum_institution_articles_item_type_*`) e passa `$notices` para a view; com 0 avisos, não renderize a seção; com 1–3, mostre uma grade simples sem slider.

## Faça / Não faça

- **Faça:** botão de pausa sempre que houver autoplay e `rewind` em vez de `loop` (sem clones).
- **Faça:** envolver cada cartão num `<div>` para o `gutter` funcionar e o cartão manter `display: flex`.
- **Faça:** limitar a 6 avisos e linkar para a lista completa.
- **Não faça:** usar `controlsText` com texto em inglês ou setas sem `aria-label`.
- **Não faça:** colocar avisos críticos só no carrossel.
- **Não faça:** adotar tiny-slider onde o [Carousel](../Carousel/README.md) do ttscui resolve.
