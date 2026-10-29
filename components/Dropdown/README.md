# Dropdown

Menu flutuante do ttscui (`data-ttsc-dropdown`, posicionado com Popper) com itens `ttsc-dropdown-menu-link`, divisor, cabeçalho, item selecionado e submenu aninhado.

## Quando usar

- Ações de uma linha de tabela (“⋯”: Ver ficha, Editar, Emitir documento, Excluir).
- Ações secundárias de um cabeçalho de página ou card (Exportar CSV, Imprimir).
- Menu do usuário no cabeçalho (perfil, unidade, sair).
- Escolher **valor** de formulário → `select`/`ttsc-select`, não dropdown.
- 2–5 opções exclusivas sempre visíveis → [ButtonGroup](../ButtonGroup/README.md).
- Conteúdo rico ou formulário → [Drawer](../Drawer/README.md) ou [Modal](../Modal/README.md).

## Anatomia

```
[ Ações ˅ ]  ← button[data-ttsc-dropdown-toggle]      (raiz: [data-ttsc-dropdown])
┌ .ttsc-dropdown-menu [data-ttsc-dropdown-menu] ───┐
│ cabeçalho (texto discreto)                       │
│ 👁 Ver ficha                                     │  .ttsc-dropdown-menu-link
│ ✓ Turma 3º A                         (selected)  │
│ ⇪ Emitir documento                         ›  ──┼─► submenu (li.ttsc-menu-item[data-ttsc-dropdown-item])
│ ──────────────────────────────────────────────── │  .ttsc-dropdown-menu-separator
│ 🗑 Excluir matrícula                              │  destrutivo
└──────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Raiz | `div[data-ttsc-dropdown="true"]` | sim |
| Gatilho | `button[data-ttsc-dropdown-toggle="true"]` (primeiro da raiz) | sim |
| Menu | `div.ttsc-dropdown-menu[data-ttsc-dropdown-menu="true"]` (escondido por `:not(.open)`) | sim |
| Lista | `ul.ttsc-dropdown-menu-sub` > `li` | sim |
| Item | `a.ttsc-dropdown-menu-link` (ou `button`) com ícone `fa-light` | sim |
| Selecionado | `.selected` no link | não |
| Divisor | `li.ttsc-dropdown-menu-separator` | não |
| Cabeçalho | `li` com texto discreto (extensão `.dd-header`) ou `.ttsc-dropdown-header` em painéis | não |
| Submenu | `li.ttsc-menu-item[data-ttsc-dropdown-item="true"]` > `button.ttsc-dropdown-menu-toggle[data-ttsc-dropdown-toggle]` + `.ttsc-dropdown-menu-indicator` + `div.ttsc-dropdown-menu[data-ttsc-dropdown-menu]` | não |
| Fechar ao clicar | `data-ttsc-dropdown-dismiss="true"` no item | não |

O submenu só é criado se o `li` tiver **as duas** marcas: `data-ttsc-dropdown-item` e a classe `ttsc-menu-item` (é o seletor que `_setupNestedDropdowns` usa).

## Variantes

| Variante | Configuração | Uso | Tokens |
|---|---|---|---|
| Clique | `trigger: click` (padrão) | ações de linha, cabeçalho | menu `--popover` (= `ttsc-surface`), borda `ttsc-border`, sombra `ttsc-shadow-popover` |
| Hover | `data-ttsc-dropdown-trigger="hover"` (+ `hover-timeout`) | submenus em desktop | — |
| Alinhado à direita | `data-ttsc-dropdown-placement="bottom-end"` | botão “⋯” na última coluna | — |
| Permanente | `data-ttsc-dropdown-permanent="true"` | painel de filtros que não fecha com clique fora | — |
| Item selecionado | `.selected` | opção atual (turma, unidade) | `ttsc-accent-soft` + `ttsc-accent-text` (extensão; runtime usa `--accent` neutro) |
| Item destrutivo | `.dd-danger` (extensão) | Excluir | `ttsc-danger-text`; hover `ttsc-danger` 10% |

## API

Opções (`data-ttsc-dropdown-<opção>` na raiz ou no `li` do submenu):

| Opção | Padrão | Efeito |
|---|---|---|
| `trigger` | `click` | `click` ou `hover` |
| `placement` / `placementRtl` | `bottom-start` / `bottom-end` | posição Popper |
| `offset` / `offsetRtl` | `"0px, 5px"` | deslocamento `x, y` |
| `hoverTimeout` | `200` | ms para fechar no `mouseout` (hover) |
| `permanent` | `false` | ignora clique fora |
| `dismiss` | `false` | — (use `data-ttsc-dropdown-dismiss` nos itens) |
| `keyboard` | `true` | `Esc` fecha |
| `attach` | `""` | âncora do Popper: `"parent"` ou seletor (padrão: o gatilho) |
| `container` | `""` | `"body"` move o menu para o body (escapa de `overflow: hidden` em tabelas) |
| `zindex` | `105` | z-index mínimo (sobe acima do maior z-index ancestral) |

Métodos (`ttscDropdown.getInstance(raiz)` / `TTSC.Dropdown.getOrCreateInstance(raiz)`): `show()`, `hide()`, `toggle()`, `isOpen()`, `disable()`, `enable()`, `getToggleElement()`, `getContentElement()`, `isPermanent()`; estáticos `ttscDropdown.hide(excecao?)`, `update()` (reposiciona os abertos), `reinit()`.

Eventos (CustomEvent na raiz, `bubbles`): `show` (cancelável), `shown`, `hide` (cancelável), `hidden`. O JS adiciona `open` na raiz e no menu e `active` no gatilho.

## Acessibilidade

- Gatilho `<button>` com `aria-haspopup="menu"` e `aria-expanded` (sincronize em `shown`/`hidden` — o runtime não grava); botão “⋯” com `aria-label="Ações da matrícula MAT-2026-0381"`.
- Menu `role="menu"`, itens `role="menuitem"` (`menuitemradio` + `aria-checked` para o selecionado), `li` com `role="none"`, divisor `role="separator"`.
- `Esc` fecha (runtime); o modelo JS adiciona `↑`/`↓` entre itens e devolve o foco ao gatilho ao fechar.
- Item destrutivo com texto explícito (“Excluir matrícula”) e confirmação em [Modal](../Modal/README.md).
- Texto `ttsc-text` sobre `ttsc-surface`; ícones `ttsc-text-muted`.

## Modelos

### HTML

```html
<div data-ttsc-dropdown="true" data-ttsc-dropdown-placement="bottom-end" data-ttsc-dropdown-container="body">
  <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" data-ttsc-dropdown-toggle="true"
          aria-haspopup="menu" aria-expanded="false" aria-label="Ações da matrícula <?= $this->e($row['code']) ?>">
    <i class="fa-light fa-ellipsis-vertical"></i>
  </button>
  <div class="ttsc-dropdown-menu w-56" data-ttsc-dropdown-menu="true" role="menu">
    <ul class="ttsc-dropdown-menu-sub" role="none">
      <li role="none"><a class="ttsc-dropdown-menu-link" role="menuitem" href="/academic/students/<?= $this->e($row['student_uuid']) ?>"><i class="fa-light fa-eye"></i> Ver ficha</a></li>
      <?php if (in_array('academic.enrollments.edit', $perms, true)): ?>
      <li role="none"><button type="button" class="ttsc-dropdown-menu-link" role="menuitem" data-ttsc-dropdown-dismiss="true"
          data-ttsc-drawer-toggle="#drawer-matricula" data-edit-enrollment="<?= $this->e($row['uuid']) ?>"><i class="fa-light fa-pen"></i> Editar</button></li>
      <?php endif; ?>
      <li class="ttsc-menu-item" role="none" data-ttsc-dropdown-item="true" data-ttsc-dropdown-placement="right-start" data-ttsc-dropdown-offset="-4px, 4px">
        <button type="button" class="ttsc-dropdown-menu-toggle" data-ttsc-dropdown-toggle="true" role="menuitem" aria-haspopup="menu">
          <i class="fa-light fa-file-export"></i> Emitir documento
          <span class="ttsc-dropdown-menu-indicator"><i class="fa-light fa-chevron-right"></i></span>
        </button>
        <div class="ttsc-dropdown-menu w-56" data-ttsc-dropdown-menu="true" role="menu">
          <ul class="ttsc-dropdown-menu-sub" role="none">
            <li role="none"><a class="ttsc-dropdown-menu-link" role="menuitem" href="/academic/enrollments/<?= $this->e($row['uuid']) ?>/declaration"><i class="fa-light fa-file-certificate"></i> Declaração de matrícula</a></li>
            <li role="none"><a class="ttsc-dropdown-menu-link" role="menuitem" href="/academic/enrollments/<?= $this->e($row['uuid']) ?>/contract"><i class="fa-light fa-file-contract"></i> Contrato</a></li>
          </ul>
        </div>
      </li>
      <?php if (in_array('academic.enrollments.delete', $perms, true)): ?>
      <li class="ttsc-dropdown-menu-separator" role="separator"></li>
      <li role="none"><button type="button" class="ttsc-dropdown-menu-link dd-danger" role="menuitem" data-ttsc-dropdown-dismiss="true"
          data-ttsc-modal-toggle="#modal-excluir" data-uuid="<?= $this->e($row['uuid']) ?>"><i class="fa-light fa-trash"></i> Excluir matrícula</button></li>
      <?php endif; ?>
    </ul>
  </div>
</div>
```

### CSS

```css
/* Ponte (bundle.css): menu em --popover / --border; hover em --accent (neutro) */
:root { --popover: var(--ttsc-surface); --popover-foreground: var(--ttsc-text); --accent: var(--ttsc-canvas-2); }

/* Extensão TTSC */
.ttsc-dropdown-menu { box-shadow: var(--ttsc-shadow-popover); border-radius: var(--ttsc-radius-sm); z-index: var(--ttsc-z-dropdown); }
.ttsc-dropdown-menu-sub { list-style: none; margin: 0; padding: 0; }
.ttsc-dropdown-menu-link, .ttsc-dropdown-menu-toggle { font-size: 13px; color: var(--ttsc-text); background: none; border: 0; }
.ttsc-dropdown-menu-link.selected, .ttsc-dropdown-menu-link.selected i { background: var(--ttsc-accent-soft); color: var(--ttsc-accent-text); }
.ttsc-dropdown-menu-link.dd-danger, .ttsc-dropdown-menu-link.dd-danger i { color: var(--ttsc-danger-text); }
.ttsc-dropdown-menu-link.dd-danger:hover { background: color-mix(in oklab, var(--ttsc-danger) 10%, transparent); }
.dd-header { padding: 6px 10px 8px; font-size: 11px; font-weight: 500; color: var(--ttsc-text-muted); }
```

### JS

```js
// assets/js/core/ttsc.dropdown-a11y.js — aria-expanded, setas e retorno de foco
document.querySelectorAll('[data-ttsc-dropdown]').forEach((root) => {
  const toggle = root.querySelector(':scope > [data-ttsc-dropdown-toggle]');
  const items = () => [...root.querySelectorAll(':scope > [data-ttsc-dropdown-menu] > ul > li > .ttsc-dropdown-menu-link, :scope > [data-ttsc-dropdown-menu] > ul > li > .ttsc-dropdown-menu-toggle')];

  root.addEventListener('shown', (e) => {
    if (e.target !== root) return;
    toggle.setAttribute('aria-expanded', 'true');
    items()[0]?.focus();
  });
  root.addEventListener('hidden', (e) => {
    if (e.target !== root) return;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.focus();
  });
  root.addEventListener('keydown', (e) => {
    if (!['ArrowDown', 'ArrowUp'].includes(e.key)) return;
    const list = items();
    const i = list.indexOf(document.activeElement);
    e.preventDefault();
    list[(i + (e.key === 'ArrowDown' ? 1 : -1) + list.length) % list.length]?.focus();
  });
});

// Reposiciona menus abertos ao rolar a tabela
document.querySelector('.ttsc-scrollable-x-auto')?.addEventListener('scroll', () => ttscDropdown.update(), { passive: true });

// Fechar programaticamente (ex.: após abrir o drawer de edição)
document.addEventListener('shown', (e) => { if (e.target.id === 'drawer-matricula') ttscDropdown.hide(); });
```

### SQL

O menu é montado com as permissões do usuário (o servidor revalida cada ação):

```sql
-- Quais ações da matrícula o usuário pode ver (banco master)
SELECT DISTINCT p.slug
  FROM permissions p
  JOIN role_permission rp ON rp.permission_id = p.uuid
  JOIN user_role ur       ON ur.role_id = rp.role_id
 WHERE ur.user_id = :user_uuid
   AND p.slug IN ('academic.enrollments.edit', 'academic.enrollments.delete', 'academic.documents.issue');
```

O controller converte o resultado em `$perms` (lista de slugs) uma vez por request e passa à view; cada `<li>` é renderizado só se o slug estiver presente.

## Faça / Não faça

- **Faça:** até ~7 itens; agrupe com divisor e deixe o destrutivo por último.
- **Faça:** `container="body"` para menus dentro de tabelas com rolagem.
- **Faça:** `placement="bottom-end"` no “⋯” da última coluna.
- **Não faça:** mais de um nível de submenu; nem formulários dentro do menu.
- **Não faça:** executar exclusão direto do item — abra o [Modal](../Modal/README.md) de confirmação.
