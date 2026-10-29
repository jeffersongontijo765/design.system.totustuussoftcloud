# SmoothScroll

Rolagem suave para âncoras internas com smooth-scroll 16.1.3 (global `SmoothScroll`), descontando o header fixo de 56px (`data-scroll-header`), atualizando a URL e movendo o foco para a seção de destino.

## Quando usar

- Páginas longas com índice de seções: regimento escolar, termos/contrato, política de privacidade, base de conhecimento, relatório com sumário.
- Links “Ir para…” dentro da mesma página quando o header fixo cobriria o título da seção.
- **Não use** para voltar ao topo: [Scrolltop](../Scrolltop/README.md).
- **Não use** dentro de contêineres roláveis (card, drawer, modal): o smooth-scroll só rola a **janela**. Use o [Scrollto](../Scrollto/README.md) do ttscui (`data-ttsc-scrollto`) ou `element.scrollIntoView({ behavior: 'smooth' })` com `scroll-margin-top`.
- **Não use** para destacar a seção visível durante a rolagem: isso é [Scrollspy](../Scrollspy/README.md) (combine os dois).
- Se só precisa do comportamento nativo, `html { scroll-behavior: smooth }` + `scroll-margin-top` basta — use a biblioteca quando precisar de eventos, duração controlada, `history`/popstate e offset dinâmico.

## Anatomia

```
header[data-scroll-header] (sticky/fixed, 56px)   [Matrícula] [Frequência] [Avaliação] [Mensalidades]
                                                      a[href="#avaliacao"][data-ss-link]
main
└── section#avaliacao
    └── h2[tabindex=-1]  ← recebe o foco ao parar (scrollStop); topo = 56px + offset
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Links | `a[href="#id"]` que casam com o seletor passado ao construtor (`[data-ss-link]`) | sim |
| Header | elemento fixo com `data-scroll-header` (altura somada ao offset) | sim no chassi |
| Destino | elemento com `id`; título interno com `tabindex="-1"` | sim |
| Ignorar | `data-scroll-ignore` no link | não |
| Status | `aria-live="polite"` (opcional) | não |

## Variantes

| Variante | Opções | Uso | Tokens |
|---|---|---|---|
| Índice no header | `header: '[data-scroll-header]'`, `offset: 8` | documentos longos | link ativo `ttsc-accent-soft` + `ttsc-accent-text` |
| Sumário lateral | mesmo, sem header próprio (o do chassi já tem `data-scroll-header`) | relatórios | — |
| Duração fixa | `speed: 450, speedAsDuration: true` | padrão TTSC | — |
| Sem animação | `speed: 0` com `prefers-reduced-motion` | acessibilidade | — |

## API

### Opções (`new SmoothScroll(selector, options)`)

| Opção | Padrão | Valor TTSC |
|---|---|---|
| `ignore` | `'[data-scroll-ignore]'` | padrão |
| `header` | `null` | `'[data-scroll-header]'` (header de 56px = `--ttsc-header-h`) |
| `offset` | `0` | `8` (número ou função `(anchor, toggle) => px`) |
| `speed` / `speedAsDuration` | `500` / `false` | `450` / `true` (ms totais) |
| `durationMin` / `durationMax` | `null` | — |
| `easing` / `customEasing` | `'easeInOutCubic'` | padrão |
| `clip` | `true` | não passa do fim da página |
| `topOnEmptyHash` | `true` | `href="#"` sobe ao topo |
| `updateURL` / `popstate` | `true` / `true` | atualiza o hash e respeita voltar/avançar |
| `emitEvents` | `true` | eventos abaixo |

### Métodos

| Método | Uso |
|---|---|
| `scroll.animateScroll(anchor, toggle?, options?)` | rolar por código (anchor = elemento, seletor ou número de px) |
| `scroll.cancelScroll(noEvent?)` | interromper |
| `scroll.destroy()` | remover listeners (navegação parcial) |

### Eventos (no `document`, `event.detail = { anchor, toggle }`)

| Evento | Quando |
|---|---|
| `scrollStart` | início da animação |
| `scrollStop` | chegou ao destino → mova o foco e marque o link ativo |
| `scrollCancel` | interrompida (novo clique, roda do mouse) |

## Acessibilidade

- Os links são `<a href="#id">` reais: sem JS a âncora nativa funciona; com `scroll-margin-top` o título não fica sob o header.
- No `scrollStop`, foque o título da seção (`tabindex="-1"`, `focus({ preventScroll: true })`) — leitores de tela e teclado continuam dali.
- Marque o link atual com `aria-current="location"` e fundo `ttsc-accent-soft` + texto `ttsc-accent-text` (≥ 4,5:1).
- `prefers-reduced-motion: reduce` → `speed: 0`. (A biblioteca também detecta `(prefers-reduced-motion)` e salta direto.)

## Modelos

### HTML

```html
<!-- O header do chassi já é fixo: só acrescente data-scroll-header -->
<header class="ttsc-header" data-scroll-header>…</header>

<nav class="flex gap-2" aria-label="Seções do regimento">
  <a class="ttsc-btn ttsc-btn-ghost ttsc-btn-sm" href="#matricula" data-ss-link>Matrícula</a>
  <a class="ttsc-btn ttsc-btn-ghost ttsc-btn-sm" href="#frequencia" data-ss-link>Frequência</a>
  <a class="ttsc-btn ttsc-btn-ghost ttsc-btn-sm" href="#avaliacao" data-ss-link>Avaliação</a>
  <a class="ttsc-btn ttsc-btn-ghost ttsc-btn-sm" href="#mensalidades" data-ss-link>Mensalidades</a>
</nav>

<?php foreach ($sections as $s): ?>
  <section class="ss-section" id="<?= $this->e($s['slug']) ?>">
    <h2 tabindex="-1"><?= $this->e($s['title']) ?></h2>
    <?= $s['html'] /* conteúdo já sanitizado no salvamento */ ?>
  </section>
<?php endforeach; ?>
<script src="/assets/vendors/smooth-scroll/smooth-scroll.polyfills.min.js"></script>
```

### CSS

```css
/* fallback nativo e destino sob o header de 56px */
.ss-section { scroll-margin-top: calc(var(--ttsc-header-h) + var(--ttsc-space-2)); }
.ss-section h2:focus { outline: none; }
.ss-section h2:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
[data-ss-link].is-active,
[data-ss-link][aria-current="location"] { background: var(--ttsc-accent-soft); color: var(--ttsc-accent-text); }
```

### JS

```js
// assets/js/core/ttsc.smooth-scroll.js — requer smooth-scroll.polyfills.min.js
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

export const smoothScroll = new SmoothScroll('a[data-ss-link]', {
  header: '[data-scroll-header]',
  offset: 8,
  speed: reduceMotion ? 0 : 450,
  speedAsDuration: true,
  easing: 'easeInOutCubic',
  updateURL: true,
  popstate: true,
});

function markActive(id) {
  document.querySelectorAll('a[data-ss-link]').forEach((link) => {
    const on = link.getAttribute('href') === `#${id}`;
    link.classList.toggle('is-active', on);
    if (on) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
  });
}

document.addEventListener('scrollStop', (event) => {
  const anchor = event.detail.anchor;
  if (!(anchor instanceof Element)) return;
  (anchor.querySelector('h2, h3') || anchor).focus({ preventScroll: true });
  markActive(anchor.id);
});

// Abrindo a página já com #hash: rola descontando o header
window.addEventListener('load', () => {
  const target = location.hash && document.querySelector(location.hash);
  if (target) smoothScroll.animateScroll(target, null, { speed: 0, updateURL: false });
});
```

### SQL

Componente de navegação, sem dados próprios. As seções vêm do documento institucional publicado, por exemplo os blocos de uma página do CMS (`cms_page_blocks`, ordenados por `sort_order`):

```sql
SELECT b.uuid, b.sort_order, b.block_type, b.content_json
  FROM cms_page_blocks b
 WHERE b.page_uuid = :page_uuid
   AND b.tenant_id = :tenant_id
 ORDER BY b.sort_order;
```

O PHP gera o `slug` de cada seção a partir do título (sem acento, minúsculas, hífens) e usa o mesmo valor no `id` da `<section>` e no `href` do índice.

## Faça / Não faça

- **Faça:** `data-scroll-header` no header fixo e `scroll-margin-top` como fallback.
- **Faça:** foco no título ao terminar e `aria-current` no link.
- **Faça:** ids estáveis e legíveis (`#avaliacao`), que podem ser compartilhados por link.
- **Não faça:** usar em contêiner com rolagem própria — a biblioteca só rola a janela.
- **Não faça:** durações longas (> 600 ms) nem desligar `popstate` (quebra o botão voltar).
- **Não faça:** nomear variável global `status` no script da página (colide com `window.status` e vira string).
