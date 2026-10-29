# Overlay

Camada sobre um card ou imagem (`.ttsc-overlay`) que revela ações no hover/foco, e camada de carregamento (`.ttsc-overlay-loading`) que bloqueia um bloco enquanto os dados recarregam.

## Quando usar

- Capa de curso, foto de documento ou miniatura de arquivo com ações rápidas (Ver, Editar, Baixar) que só aparecem ao passar o mouse ou focar.
- Bloquear um card/tabela durante recarga parcial (filtro, paginação, “Atualizar”) sem tirar o conteúdo antigo da tela.
- **Não use** para ações essenciais que precisam estar sempre visíveis — coloque botões fixos no card.
- **Não use** para bloquear a página inteira — use [Modal](../Modal/README.md) ou a barra do [Indicator](../Indicator/README.md).
- Efeitos de hover sem camada (sombra, borda) estão em [Hover](../Hover/README.md).

## Anatomia

```
.ttsc-overlay                    .ttsc-overlay-loading.is-loading
┌──────────────────────┐         ┌──────────────────────────┐
│ .ttsc-overlay-wrapper│         │ conteúdo (inerte)        │
│  (imagem/SVG)        │         │  ┌────────────────────┐  │
│ ┌──────────────────┐ │         │  │ ◠ Carregando…      │  │ .ttsc-overlay-block
│ │ [Ver] [✎]  layer │ │         │  └────────────────────┘  │
│ └──────────────────┘ │         └──────────────────────────┘
└──────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Container hover | `.ttsc-overlay` | sim |
| Conteúdo | `.ttsc-overlay-wrapper` (recebe zoom leve) | sim |
| Camada de ações | `.ttsc-overlay-layer` com botões `ttsc-btn-sm ttsc-btn-outline` | sim |
| Forçar visível | `.is-active` | não |
| Container de carregamento | `.ttsc-overlay-loading` | sim |
| Bloqueio | `.ttsc-overlay-block` + `role="status"` (spinner + texto) | sim |
| Estado | `.is-loading` + `aria-busy="true"` no container | — |

## Estados

| Estado | Gatilho | Tokens |
|---|---|---|
| Repouso | — | camada `opacity: 0` |
| Hover / foco | `:hover`, `:focus-within` ou `.is-active` | fundo `ttsc-scrim`; botões `ttsc-surface`/`ttsc-text` |
| Carregando | `.is-loading` | véu `ttsc-surface` 75% + blur 1px, texto `ttsc-text-2`, spinner `ttsc-accent` |

## API

Implementação TTSC (`assets/js/core/ttsc.overlay.js`).

| Método | Efeito |
|---|---|
| `TTSC.overlay.block(el, texto?)` | cria/mostra `.ttsc-overlay-block`, adiciona `.is-loading` e `aria-busy` |
| `TTSC.overlay.unblock(el)` | remove o bloqueio |
| `TTSC.overlay.wrap(el, promise, texto?)` | bloqueia até a promise resolver/rejeitar |

| Evento (no container) | Quando |
|---|---|
| `ttsc.overlay.block` | após bloquear |
| `ttsc.overlay.unblock` | após desbloquear |

## Acessibilidade

- Ações do overlay também aparecem com **teclado** (`:focus-within`): ao tabular até o botão, a camada fica visível.
- Em telas touch (sem hover), mostre a camada sempre ou repita as ações num menu do card.
- Botões só-ícone com `aria-label` (“Editar curso”). A imagem decorativa leva `aria-hidden="true"`; o nome do curso fica em texto fora da camada.
- Durante o bloqueio, `aria-busy="true"` no bloco e `role="status"` no texto — o conteúdo antigo fica inerte (`pointer-events: none`).
- Contraste: botões da camada usam `ttsc-surface` + `ttsc-text` sobre o scrim, ≥ 4,5:1 nos dois temas.

## Modelos

### HTML

```html
<!-- Card de curso com ações no hover -->
<article class="ttsc-card p-3">
  <div class="ttsc-overlay">
    <div class="ttsc-overlay-wrapper">
      <img src="<?= $this->e($course['cover_url']) ?>" alt="" aria-hidden="true" class="w-full">
    </div>
    <div class="ttsc-overlay-layer">
      <a href="/academico/cursos/<?= $this->e($course['uuid']) ?>" class="ttsc-btn ttsc-btn-sm ttsc-btn-outline"><i class="fa-light fa-eye"></i> Ver</a>
      <button type="button" class="ttsc-btn ttsc-btn-sm ttsc-btn-outline ttsc-btn-icon" aria-label="Editar curso"
              data-ttsc-drawer-toggle="#drawer-course"><i class="fa-light fa-pen"></i></button>
    </div>
  </div>
  <div class="font-semibold"><?= $this->e($course['name']) ?></div>
  <div class="text-xs text-muted-foreground"><?= (int) $course['classes_count'] ?> turmas · <?= (int) $course['students_count'] ?> alunos</div>
</article>

<!-- Bloco com carregamento -->
<section class="ttsc-card ttsc-overlay-loading" id="block-enrollments">
  <div class="ttsc-card-header">
    <h3 class="ttsc-card-title">Matrículas recentes</h3>
    <button type="button" class="ttsc-btn ttsc-btn-sm ttsc-btn-outline" data-reload="#block-enrollments"><i class="fa-light fa-arrows-rotate"></i> Atualizar</button>
  </div>
  <div class="ttsc-card-table"><table class="ttsc-table"><!-- linhas --></table></div>
</section>
```

### CSS

```css
.ttsc-overlay { position: relative; display: block; overflow: hidden; border-radius: var(--ttsc-radius-sm); }
.ttsc-overlay-layer { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; gap: var(--ttsc-space-2);
  background: var(--ttsc-scrim); opacity: 0; transition: opacity .2s ease; }
.ttsc-overlay:hover .ttsc-overlay-layer, .ttsc-overlay:focus-within .ttsc-overlay-layer, .ttsc-overlay.is-active .ttsc-overlay-layer { opacity: 1; }
.ttsc-overlay-wrapper { transition: transform .3s ease; }
.ttsc-overlay:hover .ttsc-overlay-wrapper, .ttsc-overlay.is-active .ttsc-overlay-wrapper { transform: scale(1.03); }
.ttsc-overlay-layer .ttsc-btn { background: var(--ttsc-surface); color: var(--ttsc-text); border-color: var(--ttsc-border); }
@media (hover: none) { .ttsc-overlay-layer { opacity: 1; background: transparent; align-items: flex-end; justify-content: flex-end; padding: var(--ttsc-space-2); } }

.ttsc-overlay-loading { position: relative; }
.ttsc-overlay-loading > .ttsc-overlay-block { position: absolute; inset: 0; z-index: 2; display: none; align-items: center; justify-content: center;
  gap: 10px; background: color-mix(in oklab, var(--ttsc-surface) 75%, transparent); backdrop-filter: blur(1px);
  border-radius: inherit; color: var(--ttsc-text-2); font-weight: 500; }
.ttsc-overlay-loading.is-loading > .ttsc-overlay-block { display: flex; }
.ttsc-overlay-loading.is-loading > :not(.ttsc-overlay-block) { pointer-events: none; user-select: none; }
```

### JS

```js
// assets/js/core/ttsc.overlay.js — implementação TTSC
(function (w) {
  const overlay = {
    block(el, text = 'Carregando…') {
      el.classList.add('ttsc-overlay-loading', 'is-loading');
      el.setAttribute('aria-busy', 'true');
      let layer = el.querySelector(':scope > .ttsc-overlay-block');
      if (!layer) {
        layer = document.createElement('div');
        layer.className = 'ttsc-overlay-block';
        layer.setAttribute('role', 'status');
        layer.innerHTML = '<span class="ttsc-spinner" aria-hidden="true"></span><span></span>';
        el.append(layer);
      }
      layer.lastElementChild.textContent = text;
      el.dispatchEvent(new CustomEvent('ttsc.overlay.block', { bubbles: true }));
    },
    unblock(el) {
      el.classList.remove('is-loading');
      el.removeAttribute('aria-busy');
      el.dispatchEvent(new CustomEvent('ttsc.overlay.unblock', { bubbles: true }));
    },
    async wrap(el, promise, text) {
      overlay.block(el, text);
      try { return await promise; } finally { overlay.unblock(el); }
    },
  };
  w.TTSC = w.TTSC || {};
  w.TTSC.overlay = overlay;
})(window);

// Botões "Atualizar" que recarregam o HTML parcial do bloco
document.addEventListener('click', async (event) => {
  const button = event.target.closest('[data-reload]');
  if (!button) return;
  const block = document.querySelector(button.dataset.reload);
  await TTSC.overlay.wrap(block, fetch('/secretaria/matriculas/recentes?partial=1')
    .then((r) => r.text())
    .then((html) => { block.querySelector('.ttsc-card-table').innerHTML = html; }), 'Carregando matrículas…');
});
```

### SQL

```sql
-- Cards de curso (overlay hover): turmas e alunos ativos por curso
SELECT co.uuid, co.code, co.name, co.type,
       COUNT(DISTINCT cl.uuid) AS classes_count,
       COUNT(DISTINCT en.uuid) AS students_count
  FROM courses co
  LEFT JOIN classes cl     ON cl.course_uuid = co.uuid AND cl.deleted_at IS NULL AND cl.is_active = 1
  LEFT JOIN enrollments en ON en.course_uuid = co.uuid AND en.deleted_at IS NULL AND en.status = 'active'
 WHERE co.deleted_at IS NULL AND co.is_active = 1 AND co.unit_uuid = :unit_uuid
 GROUP BY co.uuid, co.code, co.name, co.type
 ORDER BY co.name;

-- Bloco com overlay de carregamento: matrículas recentes (parcial recarregado)
SELECT en.uuid, en.code, u.name AS student_name, co.name AS course_name, en.enrollment_date
  FROM enrollments en
  JOIN users u    ON u.uuid = en.student_uuid
  JOIN courses co ON co.uuid = en.course_uuid
 WHERE en.deleted_at IS NULL AND en.unit_uuid = :unit_uuid
 ORDER BY en.created_at DESC
 LIMIT :limit OFFSET :offset;
```

`courses` não tem coluna de capa: a view usa a imagem do módulo de arquivos ou um SVG com o `code` do curso. O parcial de matrículas é a mesma view Plates renderizada com `?partial=1`.

## Faça / Não faça

- **Faça:** no máximo 2–3 ações na camada; a ação principal com rótulo.
- **Faça:** manter o conteúdo antigo visível sob o véu de carregamento (evita salto de layout).
- **Não faça:** esconder no hover a única forma de editar/excluir.
- **Não faça:** usar scrim preto fixo — use `ttsc-scrim` (ajusta no tema escuro).
