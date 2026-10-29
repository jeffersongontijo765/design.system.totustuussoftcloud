# Hover

Efeitos de hover padronizados (`.ttsc-hover-*`) — elevar sombra, borda de destaque, cor do ícone, fundo e mostrar ações — que também respondem a foco de teclado.

## Quando usar

- Cards clicáveis (atalhos do dashboard, cursos, planos): `ttsc-hover-elevate` ou `ttsc-hover-border`.
- Atalhos com ícone (Declarações, Boletos): `ttsc-hover-icon` destaca o ícone em `ttsc-accent-text`.
- Linhas/itens com ações secundárias (editar, excluir) que só aparecem ao apontar: `ttsc-hover-actions` + `ttsc-hover-bg`.
- **Não use** em elementos que não são interativos (hover sugere clique).
- Camada escura sobre imagem com botões: use [Overlay](../Overlay/README.md).
- Linhas de tabela já têm hover próprio no [DataTable](../DataTable/README.md).

## Anatomia

```
.ttsc-hover-elevate   ┌────────┐ → sombra lg + translateY(-2px)
.ttsc-hover-border    ┌────────┐ → borda ttsc-accent-border + anel ttsc-accent-soft
.ttsc-hover-icon      [ícone .ttsc-hover-icon-target] → ttsc-accent-text
.ttsc-hover-actions   texto ……… [.ttsc-hover-actions-target editar excluir] → opacity 0 → 1
```

| Parte | Classe | Obrigatório |
|---|---|---|
| Elemento interativo | `a`, `button` ou `label` com uma ou mais classes `ttsc-hover-*` | sim |
| Alvo do ícone | `.ttsc-hover-icon-target` (dentro de `.ttsc-hover-icon`) | com `-icon` |
| Alvo das ações | `.ttsc-hover-actions-target` (dentro de `.ttsc-hover-actions`) | com `-actions` |
| Forçar estado | `.is-hover` (documentação, item selecionado) | não |

## Variantes

| Classe | Efeito | Tokens |
|---|---|---|
| `ttsc-hover-elevate` | sombra + sobe 2px | `ttsc-shadow-lg` |
| `ttsc-hover-border` | borda e anel de 3px | `ttsc-accent-border`, `ttsc-accent-soft` |
| `ttsc-hover-icon` | ícone muda de cor e escala 1.08 | `ttsc-text-muted` → `ttsc-accent-text` |
| `ttsc-hover-bg` | fundo neutro | `ttsc-canvas-2` |
| `ttsc-hover-actions` | ações aparecem | opacidade |

As classes podem ser combinadas (`ttsc-hover-actions ttsc-hover-bg`). Todas respondem a `:hover`, `:focus-within` e `.is-hover`.

## API

Somente CSS (implementação TTSC em `assets/css/ttsc.css`). Sem atributos nem JS.

| Media query | Comportamento |
|---|---|
| `(hover: none)` | `.ttsc-hover-actions-target` sempre visível (touch) |
| `(prefers-reduced-motion: reduce)` | sem `translateY` no elevate |

## Acessibilidade

- `:focus-within` garante o mesmo destaque ao navegar por Tab — as ações escondidas aparecem quando um botão delas recebe foco.
- Ações ocultas continuam no DOM e na ordem de tabulação (opacidade, não `display:none`), com `aria-label`.
- Hover nunca é o único caminho: em touch as ações ficam visíveis; o card inteiro é um `<a>` com texto.
- Mudança de cor do ícone usa `ttsc-accent-text` (≥ 4,5:1); nunca `ttsc-accent` como cor de ícone/texto sobre superfície clara.

## Modelos

### HTML

```html
<!-- Atalhos do dashboard -->
<div class="grid grid-cols-3 gap-3">
  <a href="/secretaria/declaracoes" class="ttsc-card p-4 flex items-center gap-3 ttsc-hover-icon ttsc-hover-elevate">
    <i class="fa-light fa-file-certificate ttsc-hover-icon-target text-xl"></i>
    <span><span class="font-semibold">Declarações</span><br><span class="text-xs text-muted-foreground">Secretaria</span></span>
  </a>
</div>

<!-- Lista de alunos da turma com ações no hover -->
<ul>
  <?php foreach ($students as $s): ?>
    <li class="flex items-center justify-between p-3 ttsc-hover-bg ttsc-hover-actions">
      <span><?= $this->e($s['student_name']) ?> <span class="text-xs text-muted-foreground"><?= $this->e($s['code']) ?></span></span>
      <span class="ttsc-hover-actions-target flex gap-1">
        <a href="/secretaria/matriculas/<?= $this->e($s['uuid']) ?>/editar" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" aria-label="Editar matrícula de <?= $this->e($s['student_name']) ?>"><i class="fa-light fa-pen"></i></a>
        <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" aria-label="Excluir matrícula de <?= $this->e($s['student_name']) ?>"><i class="fa-light fa-trash"></i></button>
      </span>
    </li>
  <?php endforeach ?>
</ul>
```

### CSS

```css
.ttsc-hover-elevate, .ttsc-hover-border, .ttsc-hover-icon, .ttsc-hover-bg, .ttsc-hover-actions {
  transition: box-shadow .2s ease, transform .2s ease, border-color .2s ease, background-color .2s ease, color .2s ease; }
.ttsc-hover-elevate:hover, .ttsc-hover-elevate:focus-within, .ttsc-hover-elevate.is-hover { box-shadow: var(--ttsc-shadow-lg); transform: translateY(-2px); }
.ttsc-hover-border:hover, .ttsc-hover-border:focus-within, .ttsc-hover-border.is-hover { border-color: var(--ttsc-accent-border); box-shadow: 0 0 0 3px var(--ttsc-accent-soft); }
.ttsc-hover-icon .ttsc-hover-icon-target { color: var(--ttsc-text-muted); transition: color .2s ease, transform .2s ease; }
.ttsc-hover-icon:hover .ttsc-hover-icon-target, .ttsc-hover-icon:focus-within .ttsc-hover-icon-target,
.ttsc-hover-icon.is-hover .ttsc-hover-icon-target { color: var(--ttsc-accent-text); transform: scale(1.08); }
.ttsc-hover-bg:hover, .ttsc-hover-bg:focus-within, .ttsc-hover-bg.is-hover { background-color: var(--ttsc-canvas-2); }
.ttsc-hover-actions .ttsc-hover-actions-target { opacity: 0; transition: opacity .15s ease; }
.ttsc-hover-actions:hover .ttsc-hover-actions-target, .ttsc-hover-actions:focus-within .ttsc-hover-actions-target,
.ttsc-hover-actions.is-hover .ttsc-hover-actions-target { opacity: 1; }
@media (hover: none) { .ttsc-hover-actions .ttsc-hover-actions-target { opacity: 1; } }
@media (prefers-reduced-motion: reduce) { .ttsc-hover-elevate:hover, .ttsc-hover-elevate.is-hover { transform: none; } }
```

### JS

```js
// Sem JS obrigatório. Opcional: item selecionado mantém o estado de hover (lista mestre-detalhe)
document.querySelectorAll('[data-ttsc-select-list]').forEach((list) => {
  list.addEventListener('click', (event) => {
    const item = event.target.closest('.ttsc-hover-bg');
    if (!item || event.target.closest('.ttsc-hover-actions-target')) return;
    list.querySelectorAll('.is-hover').forEach((el) => { el.classList.remove('is-hover'); el.removeAttribute('aria-current'); });
    item.classList.add('is-hover');
    item.setAttribute('aria-current', 'true');
  });
});
```

### SQL

```sql
-- Lista de alunos da turma (itens com ações no hover)
SELECT en.uuid, en.code, u.name AS student_name, en.status
  FROM enrollments en
  JOIN users u ON u.uuid = en.student_uuid
 WHERE en.class_uuid = :class_uuid
   AND en.deleted_at IS NULL
 ORDER BY u.name;
```

O controller entrega `$students`; os botões de editar/excluir só são renderizados quando o usuário tem a permissão de escrita (mesma checagem do [Button](../Button/README.md)).

## Faça / Não faça

- **Faça:** um efeito principal por card (elevate **ou** border), mais `-icon` se houver ícone.
- **Faça:** garantir que o card inteiro seja um link/botão quando tem hover.
- **Não faça:** esconder no hover ações que o usuário precisa descobrir (ex.: único “Editar”).
- **Não faça:** animar `width/height` ou trocar layout no hover.
