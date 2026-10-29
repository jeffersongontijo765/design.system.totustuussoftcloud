# Lozad

Carregamento preguiçoso (lazy load) de imagens e fundos com lozad 1.16.0 — `data-src`, `data-srcset` e `data-background-image` só viram requisição quando o elemento entra na área visível (IntersectionObserver).

## Quando usar

- Listas e grades com muitas fotos: alunos da turma com avatar, galeria de eventos, catálogo de patrimônio, banners de comunicados abaixo da dobra.
- Imagens de **fundo** (CSS `background-image`) — o `loading="lazy"` nativo não cobre esse caso.
- Quando é preciso saber que a imagem carregou (`loaded`) para animar, contar ou trocar placeholder.
- **Não use** para a imagem principal acima da dobra (logo, avatar do header, banner do topo): carregue normal, com `fetchpriority="high"`.
- Para `<img>` simples sem callback, prefira o nativo `loading="lazy"` + `width`/`height` — zero JS.
- **Não use** com `iframe` (vídeos, mapas, embeds de terceiros): proibido no design system e, em produção, dependente de consentimento ([CookieAlert](../CookieAlert/README.md)).

## Anatomia

```
img.lozad[data-src="…"][width][height][alt][data-toggle-class="is-loaded"]   → src preenchido ao entrar na tela
div.lozad[data-background-image="url1|url2"][data-background-delimiter="|"]  → style.backgroundImage
        └─ data-loaded="true" após carregar
```

| Parte | Atributo | Obrigatório |
|---|---|---|
| Seletor | classe `.lozad` (ou o seletor passado a `lozad()`) | sim |
| Fonte | `data-src` (img) / `data-srcset` / `data-background-image` | sim |
| Dimensões | `width` + `height` (evita salto de layout) | sim em img |
| Texto alternativo | `alt` (img) ou `role="img"` + `aria-label` (fundo) | sim |
| Classe ao carregar | `data-toggle-class="is-loaded"` | recomendado |
| Delimitador | `data-background-delimiter="\|"` — **obrigatório** com `data:` URI (o padrão `,` quebra a URL) | com data: |
| Placeholder | `data-placeholder-background="var(--ttsc-surface-2)"` ou cor de fundo no CSS | não |
| Estado | `data-loaded="true"` (posto pela lib) | — |

## Estados

| Estado | Marca | Tokens |
|---|---|---|
| Aguardando | sem `src` / sem fundo; opacidade .35 | fundo `ttsc-surface-2`, borda `ttsc-border-soft` |
| Carregada | `.is-loaded` + `data-loaded="true"` | opacidade 1 (transição .3s) |
| Falha | evento `error` na img → iniciais/ícone | [Avatar](../Avatar/README.md) de iniciais |

## API

| Opção (`lozad(selector, options)`) | Padrão | Uso TTSC |
|---|---|---|
| `rootMargin` | `'0px'` | `'0px 0px 200px 0px'` (pré-carrega 200px antes) |
| `threshold` | `0` | `0.1` |
| `enableAutoReload` | `false` | recarrega se `data-src` mudar |
| `load(el)` | aplica `data-*` | personalizar (ex.: `<picture>`) |
| `loaded(el)` | — | contador, remover skeleton |

| Método | Uso |
|---|---|
| `observer.observe()` | começa a observar (chame de novo após inserir itens) |
| `observer.triggerLoad(el)` | força o carregamento (impressão, abrir no [Lightbox](../Lightbox/README.md)) |
| `observer.observer` | o `IntersectionObserver` interno (`disconnect()` ao sair da página) |

Sem `root` configurável: o observador usa a viewport, mas respeita o recorte de contêineres com `overflow` — itens fora da área visível de uma lista rolável só carregam ao rolar.

## Acessibilidade

- `alt` descritivo em toda `img` (“Foto de Ana Beatriz Souza”); fundos com significado precisam de `role="img"` + `aria-label`, fundos decorativos não.
- `width`/`height` fixos evitam deslocamento de layout (quem usa zoom/leitor não perde a posição).
- Não esconda o texto até a imagem carregar; nome e matrícula aparecem desde o início.
- Texto sobre fundo carregado (banner) precisa de contraste também **antes** de carregar: use `ttsc-surface-2` como placeholder com texto `ttsc-text`, ou sombra no texto sobre a foto.

## Modelos

### HTML

```html
<div class="lz-list" tabindex="0" aria-label="Alunos da turma">
  <?php foreach ($students as $s): ?>
    <div class="lz-row">
      <?php if (!empty($s['avatar'])): ?>
        <img class="lz-avatar lozad" width="36" height="36" alt="Foto de <?= $this->e($s['name']) ?>"
             data-src="<?= $this->e($s['avatar']) ?>" data-toggle-class="is-loaded">
      <?php else: ?>
        <span class="ttsc-avatar"><?= $this->e(mb_substr($s['name'], 0, 1)) ?></span>
      <?php endif; ?>
      <div>
        <div class="lz-name"><?= $this->e($s['name']) ?></div>
        <div class="lz-sub"><?= $this->e($s['code']) ?></div>
      </div>
    </div>
  <?php endforeach; ?>
</div>

<div class="lz-banner lozad" role="img" aria-label="Banner da Feira de Ciências 2026"
     data-background-image="/uploads/banners/feira-2026.webp" data-toggle-class="is-loaded"></div>
<script src="/assets/vendors/lozad/lozad.min.js"></script>
```

### CSS

```css
.lz-avatar { width: 36px; height: 36px; border-radius: 50%; background: var(--ttsc-surface-2);
  border: 1px solid var(--ttsc-border-soft); opacity: .35; transition: opacity .3s ease; }
.lz-avatar.is-loaded { opacity: 1; }
.lz-banner { min-height: 92px; border-radius: var(--ttsc-radius-surface); background-color: var(--ttsc-surface-2);
  background-size: cover; background-position: center; border: 1px solid var(--ttsc-border); }
@media (prefers-reduced-motion: reduce) { .lz-avatar, .lz-banner { transition: none; } }
```

### JS

```js
// assets/js/core/ttsc.lazy.js — requer lozad.min.js
export const lazyObserver = lozad('.lozad', {
  rootMargin: '0px 0px 200px 0px',
  threshold: 0.1,
  loaded: (el) => {
    if (el.tagName === 'IMG') {
      el.addEventListener('error', () => {
        const fallback = document.createElement('span');
        fallback.className = 'ttsc-avatar';
        fallback.textContent = (el.alt.replace(/^Foto de /, '')[0] || '?').toUpperCase();
        el.replaceWith(fallback);
      }, { once: true });
    }
  },
});
lazyObserver.observe();

// Conteúdo inserido depois (paginação "carregar mais", AJAX)
document.addEventListener('ttsc:content-loaded', () => lazyObserver.observe());

// Antes de imprimir, força tudo a carregar
window.addEventListener('beforeprint', () => {
  document.querySelectorAll('.lozad:not([data-loaded])').forEach((el) => lazyObserver.triggerLoad(el));
});
```

### SQL

As fotos são o caminho em `users.avatar` (gravado pelo [Cropper](../Cropper/README.md)); a lista de alunos da turma traz o caminho e o PHP decide entre `img.lozad` e as iniciais:

```sql
SELECT e.code, s.uuid AS student_uuid, s.name, s.avatar
  FROM enrollments e
  JOIN users s ON s.uuid = e.student_uuid AND s.deleted_at IS NULL
 WHERE e.class_uuid = :class_uuid
   AND e.status = 'active'
   AND e.deleted_at IS NULL
 ORDER BY s.name
 LIMIT 60;
```

Para galerias, a fonte é `cms_media` (`url`, `width`, `height`, `alt_text`) — use `width`/`height` do banco nos atributos da `img`.

## Faça / Não faça

- **Faça:** `width`/`height`, `alt` e placeholder com token em todas as imagens preguiçosas.
- **Faça:** `data-background-delimiter="|"` quando a URL pode conter vírgula (`data:` URI, URLs assinadas).
- **Faça:** chamar `observe()` após inserir itens dinamicamente.
- **Não faça:** lazy load na imagem principal acima da dobra (piora o LCP).
- **Não faça:** usar lozad com `iframe`/vídeo de terceiros.
- **Não faça:** esconder conteúdo textual até a imagem carregar.
