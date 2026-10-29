# Menu

Menu vertical do runtime (`.ttsc-menu.ttsc-menu-default`) com itens, ícones, títulos, badges, bullets, títulos de seção, separadores e submenus em accordion, mais uma implementação TTSC de abrir/fechar e item ativo.

> Também listado em: **Geral › Menu**.

> **Não é o sub-sidebar do app.** O exemplo abaixo usa rótulos da Secretaria (Matrículas, Rematrícula) só como conteúdo; a navegação real do módulo é o `aside#sub-sidebar` de `partials/sub_sidebar.php` (`.subnav-group`, `button.sb-section-btn[data-accordion-toggle]`, `a.subnav-link.is-active`), gerado a partir de `app/Config/sidebar-nav.php` e controlado por `ttsc.shell.js` / `ttsc.sidebar.js`. A fonte de verdade para rail e sub-sidebar é [Navigation](../Navigation/README.md); não reproduza o sub-sidebar com `.ttsc-menu`. As classes `.ttsc-menu-*` vêm do CSS do runtime (`tailwind-runtime.css`), e o `TTSCMenu` desta página (`init` / `setActive`) é uma implementação proposta: o layout `main.php` não carrega módulo de menu (o `TTSCMenu` embutido em `assets/js/ttsc.builder.js` é outro, do bundle do Construtor).

## Quando usar

- Lista de navegação dentro de um painel: menu de um drawer de configurações, menu lateral de uma página de perfil, navegação de um portal do aluno/responsável.
- Listas de ações dentro de um [Dropdown](../Dropdown/README.md) (`.ttsc-menu-dropdown`).
- Hierarquia de até 2 níveis (grupo → páginas) com accordion.
- Navegação principal entre módulos e páginas do app → [Navigation](../Navigation/README.md) (rail + sub-sidebar do chassi).
- Troca de visão dentro da mesma página → [SegmentedTabs](../SegmentedTabs/README.md).

## Anatomia

```
.ttsc-menu.ttsc-menu-default.flex-col
  ├ .ttsc-menu-heading                              SECRETARIA
  ├ .ttsc-menu-item[.active|.here|.show|.disabled]
  │    └ a|button.ttsc-menu-link
  │         ├ .ttsc-menu-icon > i.fa-light          (ou .ttsc-menu-bullet nos subitens)
  │         ├ .ttsc-menu-title
  │         ├ .ttsc-menu-badge > .ttsc-badge
  │         └ .ttsc-menu-arrow > i.fa-chevron-down
  │    └ .ttsc-menu-accordion  (display:none até o item ter .show)
  │         └ .ttsc-menu-item > .ttsc-menu-link …
  └ .ttsc-menu-separator
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Container | `div.ttsc-menu.ttsc-menu-default.flex-col` dentro de `<nav aria-label>` | sim |
| Item | `.ttsc-menu-item` | sim |
| Link | `a.ttsc-menu-link` (ou `button` para toggles) | sim |
| Ícone / bullet | `.ttsc-menu-icon` · `.ttsc-menu-bullet` | não |
| Título | `.ttsc-menu-title` | sim |
| Badge / seta | `.ttsc-menu-badge` · `.ttsc-menu-arrow` | não |
| Submenu | `.ttsc-menu-accordion` (filho do item) + `data-ttsc-menu-item-toggle="accordion"` no item | não |
| Seção / divisória | `.ttsc-menu-heading` · `.ttsc-menu-separator` | não |
| Espaçamento | `ttsc-menu-fit` (sem margem lateral) · `ttsc-menu-space` · `ttsc-menu-no-indent` (accordion sem recuo) | não |

## Estados

| Estado | Classe | Tokens |
|---|---|---|
| Normal | — | título `--foreground`=`ttsc-text`, ícone `--muted-foreground`=`ttsc-text-muted` |
| Hover | automático | fundo `--accent`=`ttsc-canvas-2`, título `--mono`, ícone `--primary` |
| Ativo (página atual) | `.active` + `aria-current="page"` | fundo `ttsc-canvas-2`, barra 2px `ttsc-accent` (TTSC), ícone `ttsc-accent-text` |
| Pai do ativo | `.here` | fundo `ttsc-canvas-2` |
| Aberto (accordion) | `.show` | seta gira 180° |
| Desabilitado | `.disabled` + `aria-disabled="true"` | opacidade .5 |

Variantes utilitárias do runtime também existem para composições (`ttsc-menu-item-active:text-primary`, `ttsc-menu-link-hover:bg-accent/60`, `ttsc-menu-item-here:font-semibold`…); prefira os tokens acima para manter contraste.

## API

O CSS vem do runtime; **o ttscui não traz módulo JS de menu** (não há `TTSC.Menu`). A implementação TTSC (`assets/js/core/ttsc.menu.js`, abaixo) cobre:

| Atributo / classe | Efeito |
|---|---|
| `[data-ttsc-menu]` | ativa o comportamento no container |
| `data-ttsc-menu-item-toggle="accordion"` (no `.ttsc-menu-item`) | o link filho direto alterna `.show` e `aria-expanded` |
| `data-ttsc-menu-accordion-single="true"` (no container) | só um accordion aberto por vez |
| `.ttsc-menu-link[href]` | marca `.active` + `aria-current`, pai recebe `.here` |
| Evento `ttsc.menu.select` | no container, `detail: { href, title }` |
| `TTSCMenu.setActive(menu, href)` | ativa pelo `href` (ex.: rota atual) e abre o accordion pai |

## Acessibilidade

- Envolva em `<nav aria-label="…">`; não use `role="menu"` para navegação (esse papel é para menus de ação com teclas de seta).
- Toggle de accordion é `<button type="button">` com `aria-expanded` e `aria-controls`.
- Página atual: `aria-current="page"`; desabilitado: `aria-disabled="true"` + `tabindex="-1"` e texto explicando (“Em breve”).
- Ícones decorativos `aria-hidden="true"`; contraste do título `ttsc-text` (≥ 15:1), headings `ttsc-text-muted` (≥ 4,5:1).
- Foco visível `ttsc-accent` interno (outline-offset negativo para não cortar).

## Modelos

### HTML

```html
<nav aria-label="Secretaria acadêmica" class="ttsc-card">
  <div class="ttsc-menu ttsc-menu-default flex-col" data-ttsc-menu="true" data-ttsc-menu-accordion-single="true">
    <div class="ttsc-menu-heading">Secretaria</div>
    <?php foreach ($menu as $node): ?>
      <?php if (empty($node['children'])): ?>
      <div class="ttsc-menu-item<?= $node['active'] ? ' active' : '' ?>">
        <a class="ttsc-menu-link" href="<?= url($node['route_path']) ?>"<?= $node['active'] ? ' aria-current="page"' : '' ?>>
          <span class="ttsc-menu-icon"><i class="fa-light <?= $e($node['icon_name']) ?>" aria-hidden="true"></i></span>
          <span class="ttsc-menu-title"><?= $e($node['title']) ?></span>
        </a>
      </div>
      <?php else: $open = $node['has_active_child']; ?>
      <div class="ttsc-menu-item<?= $open ? ' show here' : '' ?>" data-ttsc-menu-item-toggle="accordion">
        <button type="button" class="ttsc-menu-link" aria-expanded="<?= $open ? 'true' : 'false' ?>" aria-controls="menu-acc-<?= (int) $node['id'] ?>">
          <span class="ttsc-menu-icon"><i class="fa-light <?= $e($node['icon_name']) ?>" aria-hidden="true"></i></span>
          <span class="ttsc-menu-title"><?= $e($node['title']) ?></span>
          <span class="ttsc-menu-arrow"><i class="fa-light fa-chevron-down" aria-hidden="true"></i></span>
        </button>
        <div class="ttsc-menu-accordion" id="menu-acc-<?= (int) $node['id'] ?>">
          <?php foreach ($node['children'] as $child): ?>
          <div class="ttsc-menu-item<?= $child['active'] ? ' active' : '' ?>">
            <a class="ttsc-menu-link" href="<?= url($child['route_path']) ?>"<?= $child['active'] ? ' aria-current="page"' : '' ?>>
              <span class="ttsc-menu-bullet"><span></span></span>
              <span class="ttsc-menu-title"><?= $e($child['title']) ?></span>
            </a>
          </div>
          <?php endforeach; ?>
        </div>
      </div>
      <?php endif; ?>
    <?php endforeach; ?>
    <div class="ttsc-menu-separator" role="separator"></div>
  </div>
</nav>
```

### CSS

```css
/* Ponte (bundle.css): o menu lê --foreground, --muted-foreground, --accent (hover neutro), --mono, --primary */
:root { --accent: var(--ttsc-canvas-2); --mono: var(--ttsc-text); --muted-foreground: var(--ttsc-text-muted); }

/* Extensões TTSC */
.ttsc-menu-heading { padding: 10px 16px 4px; font-size: 11px; font-weight: 600; letter-spacing: .05em; text-transform: uppercase; color: var(--ttsc-text-muted); }
.ttsc-menu-default .ttsc-menu-item.active > .ttsc-menu-link { box-shadow: inset 2px 0 0 var(--ttsc-accent); }
.ttsc-menu-default .ttsc-menu-item.active > .ttsc-menu-link .ttsc-menu-icon i { color: var(--ttsc-accent-text); }
.ttsc-menu-bullet span { width: 5px; height: 5px; border-radius: var(--ttsc-radius-pill); background: var(--ttsc-border-prominent); display: inline-block; }
.ttsc-menu-item.active > .ttsc-menu-link .ttsc-menu-bullet span { background: var(--ttsc-accent); }
.ttsc-menu-arrow i { transition: rotate var(--ttsc-motion-base, .2s) ease; }
.ttsc-menu-item.show > .ttsc-menu-link .ttsc-menu-arrow i { rotate: 180deg; }
button.ttsc-menu-link { border: 0; background: none; font: inherit; text-align: start; }
.ttsc-menu-link:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: -2px; }
```

### JS

```js
// assets/js/core/ttsc.menu.js — implementação TTSC (o ttscui não tem módulo menu)
(function (w) {
  function setActive(menu, href) {
    menu.querySelectorAll('.ttsc-menu-item.active, .ttsc-menu-item.here').forEach(function (i) { i.classList.remove('active', 'here'); });
    menu.querySelectorAll('[aria-current]').forEach(function (a) { a.removeAttribute('aria-current'); });
    var link = menu.querySelector('.ttsc-menu-link[href="' + CSS.escape(href) + '"]');
    if (!link) return null;
    link.parentElement.classList.add('active');
    link.setAttribute('aria-current', 'page');
    var parent = link.parentElement.parentElement.closest('.ttsc-menu-item');
    if (parent) { parent.classList.add('here', 'show'); var t = parent.querySelector(':scope > .ttsc-menu-link'); if (t) t.setAttribute('aria-expanded', 'true'); }
    return link;
  }

  function init(menu) {
    if (menu.dataset.ttscMenuInitialized) return;
    menu.dataset.ttscMenuInitialized = 'true';
    var single = menu.getAttribute('data-ttsc-menu-accordion-single') === 'true';
    menu.addEventListener('click', function (e) {
      var toggle = e.target.closest('[data-ttsc-menu-item-toggle="accordion"] > .ttsc-menu-link');
      if (toggle && menu.contains(toggle)) {
        var item = toggle.parentElement, open = !item.classList.contains('show');
        if (single && open) {
          item.parentElement.querySelectorAll(':scope > .ttsc-menu-item.show').forEach(function (o) {
            o.classList.remove('show');
            o.querySelector(':scope > .ttsc-menu-link').setAttribute('aria-expanded', 'false');
          });
        }
        item.classList.toggle('show', open);
        toggle.setAttribute('aria-expanded', String(open));
        return;
      }
      var link = e.target.closest('.ttsc-menu-link[href]');
      if (link && !link.closest('.disabled')) {
        setActive(menu, link.getAttribute('href'));
        menu.dispatchEvent(new CustomEvent('ttsc.menu.select', { bubbles: true, detail: { href: link.getAttribute('href'), title: link.textContent.trim() } }));
      }
    });
  }

  w.TTSCMenu = { init: init, setActive: setActive };
  document.querySelectorAll('[data-ttsc-menu]').forEach(init);
})(window);

// Marca a rota atual ao carregar
document.querySelectorAll('[data-ttsc-menu]').forEach(function (m) { TTSCMenu.setActive(m, location.pathname); });
```

### SQL

Árvore de itens do menu (pai → filhos) a partir do construtor de navegação no banco **master**, filtrada por permissão:

```sql
WITH RECURSIVE tree AS (
  SELECT i.id, i.parent_item_id, i.title, i.icon_name, i.route_path, i.required_permission_code,
         0 AS depth, CAST(LPAD(i.sort_order, 5, '0') AS CHAR(200)) AS sort_path
    FROM builder_navigation_items i
   WHERE i.sidebar_id = :sidebar_id
     AND i.parent_item_id IS NULL
     AND i.is_active = 1 AND i.is_visible = 1 AND i.deleted_at IS NULL
  UNION ALL
  SELECT c.id, c.parent_item_id, c.title, c.icon_name, c.route_path, c.required_permission_code,
         t.depth + 1, CONCAT(t.sort_path, '.', LPAD(c.sort_order, 5, '0'))
    FROM builder_navigation_items c
    JOIN tree t ON c.parent_item_id = t.id
   WHERE c.is_active = 1 AND c.is_visible = 1 AND c.deleted_at IS NULL
     AND t.depth < 2
)
SELECT t.id, t.parent_item_id, t.title, t.icon_name, t.route_path, t.depth
  FROM tree t
 WHERE t.required_permission_code IS NULL
    OR t.required_permission_code = ''
    OR EXISTS (SELECT 1
                 FROM permissions p
                 JOIN role_permission rp ON rp.permission_id = p.uuid
                 JOIN user_role ur       ON ur.role_id = rp.role_id
                WHERE ur.user_id = :user_uuid
                  AND p.slug = t.required_permission_code)
 ORDER BY t.sort_path;
```

O PHP monta a árvore pelo `parent_item_id` (descartando grupos que ficaram sem filhos visíveis), marca `active` comparando `route_path` com a rota atual e `has_active_child` no pai, e passa `$menu` para a view.

## Faça / Não faça

- **Faça:** no máximo 2 níveis; título curto; ícone só no primeiro nível.
- **Faça:** renderize `show`/`here`/`active` no servidor para a página atual (sem “piscar”).
- **Não faça:** `role="menu"` em navegação; nem links desabilitados sem explicação.
- **Não faça:** usar o menu como navegação principal entre módulos — isso é do chassi.
