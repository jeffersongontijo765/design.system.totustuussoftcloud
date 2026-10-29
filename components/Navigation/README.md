# Navigation

Shell de navegação real do app (`resources/views/app/layouts/main.php`): topbar de 56px, rail de portais e módulos `#primary-rail` (60px, expande para 288px) e sub-sidebar `#sub-sidebar` (320px) com as páginas do módulo agrupadas em accordion, filtrados por recurso e permissão e controlados por `assets/js/ttsc.shell.js` e `assets/js/ttsc.sidebar.js`.

## Quando usar

- Em toda página autenticada renderizada por `layouts/main.php` (`body.sb-app`). A navegação pertence ao **layout**: a view não monta rail nem sub-sidebar, só é roteada. `SidebarRouter::railFor()` escolhe o rail e `SidebarRouter::moduleFor()` escolhe o sub-sidebar a partir da URL; a view pode forçar com `$subSidebarModule` ou esconder com `$hideSubSidebar = true`.
- O **rail** lista o portal ativo (seletor no topo) e os **módulos** agrupados em `<details class="portal-rail-group">` (Ciclo Acadêmico, Gestão da Instituição…).
- O **sub-sidebar** lista as **páginas** do módulo ativo em grupos (`.subnav-group`), com filtro, CTA e indicador no rodapé.
- Abaixo de 1100px os dois viram gavetas, abertas pelos botões `#btn-mobile` e `#btn-sub-sidebar` do header.
- Troca de visão dentro de uma página (KPI / Tabela / Kanban) → [SegmentedTabs](../SegmentedTabs/README.md).
- Lista de links dentro de um drawer, dropdown ou card → [Menu](../Menu/README.md) (`.ttsc-menu`). O sub-sidebar do app **não** usa `.ttsc-menu`.
- Caminho da página → breadcrumb do [PageHeader](../PageHeader/README.md).

## Anatomia

```
┌ header[data-od-id="topnav"] (h-14 = --ttsc-header-h) ───────────────────────────────────────────────────┐
│ [☰][▯] [logo] [#btn-org-dropdown ▾] / [#btn-unit-dropdown ▾] / [período]     [busca] [agenda] [sino] [👤] │
│  └ .hdr-nav-toggles: só abaixo de 1100px                                                                │
├────────┬──────────────────────────────┬──────────────────────────────────────────────────────────────────┤
│ rail   │ aside#sub-sidebar            │ main#main-viewport (rola sozinho)                                │
│ 60px   │ .sb-head  [tile] Secretaria  │                                                                  │
│ [port.]│           ACA  [«]           │                                                                  │
│ ────── │ .sb-search-filter [Buscar…] /│                                                                  │
│ ▸ grupo│ .subnav-group (link direto)  │                                                                  │
│  [mód] │ .subnav-group                │                                                                  │
│  [mód]*│   ADMISSÕES E MATRÍCULAS 9 ▾ │                                                                  │
│ ────── │   .subnav-link               │                                                                  │
│ [?][⚙] │   .subnav-link.is-active*    │                                                                  │
│        │ .sb-foot [CTA] [indicador]   │                                                                  │
└────────┴──────────────────────────────┴──────────────────────────────────────────────────────────────────┘
  #navigation-backdrop (< 1100px, enquanto uma gaveta está aberta)
```

| Parte | Elemento / classe real | Fonte | Obrigatório |
|---|---|---|---|
| Topbar | `header[data-od-id="topnav"]` > `.hdr-left` + `.hdr-right` | `partials/header.php`, estilo `ttsc.header.css` | sim |
| Botões das gavetas | `.hdr-nav-toggles` > `button#btn-mobile.hdr-nav-toggle[aria-controls="primary-rail-wrapper"]` e `button#btn-sub-sidebar.hdr-nav-toggle[aria-controls="sub-sidebar"]`, com `aria-expanded` | `header.php` | sim (visíveis só < 1100px) |
| Contexto | `.hdr-entity` > `#btn-org-dropdown` (`#dropdown-org`), `.hdr-unit#crumb-unit` > `#btn-unit-dropdown` (`#dropdown-unit`), `#btn-period-dropdown` | `header.php` | sim (multiempresa) |
| Ações globais | `#btn-header-calendar`, `#btn-search` (Ctrl+K), `#btn-header-lgpd`, `#btn-header-notifications` + `#header-notif-badge`, `#btn-header-help`, `#btn-user-menu`; os secundários levam `.hdr-secondary` e somem progressivamente em telas estreitas | `header.php` | sim |
| Fundo das gavetas | `div#navigation-backdrop[hidden]` | `layouts/main.php`, estilo `ttsc.design-system.css` | sim |
| Rail (casca) | `#primary-rail-wrapper > aside#primary-rail[data-od-id="rail"][aria-label]` | `partials/rail.php` | sim |
| Seletor de portal | `#rail-portal-wrapper > button#btn-sidebar-portal.rail-portal-btn` + `#sidebar-portal-dropdown` (form `POST /portal/switch` por portal) | `rail.php` | sim |
| Grupo do rail | `details.portal-rail-group[data-portal-group="admin-academic_lifecycle"]` > `summary` (`.portal-group-icon`, `.portal-group-label`, `.portal-group-chevron`) + `.portal-group-items` | `rail.php` | quando o grupo tem 2+ módulos |
| Módulo | `a.rail-item[data-rail-slug][draggable="true"]` > ícone 40×40 + `.rail-label` + `.rail-tooltip`; ativo `.is-active` + `aria-current="page"` | `rail.php` | sim |
| Rodapé do rail | `button.rail-item[data-toggle-drawer="drawer-help"]`, `[data-toggle-drawer="drawer-profile"]` | `rail.php` | sim |
| Sub-sidebar | `aside#sub-sidebar[data-od-id="sidebar"][data-sidebar-id][aria-label="<módulo>"]` | `partials/sub_sidebar.php` | por módulo |
| Cabeçalho | `.sb-head` > `.sb-tile`, `.sb-title`, `.sb-sub`, `.sb-badge`, `button#subsidebar-collapse-btn.sb-collapse[data-sidebar-collapse]` | `sub_sidebar.php` | sim |
| Filtro | `.sb-search-filter` > `input#subsidebar-filter[data-sb-search="true"][data-sidebar-filter="sub-sidebar"][aria-keyshortcuts="/"].sb-search-input` + `.sb-kbd` (“/”) | `sub_sidebar.php` | sim |
| Link direto | `.subnav-group > a.subnav-link` (seção de 1 item ou “Visão geral”) | `sub_sidebar.php` | não |
| Grupo | `.subnav-group > button.sb-section-btn[data-accordion-toggle="acc-N"][data-accordion-chevron="chev-N"][aria-expanded][aria-controls]` + `.sb-count-pill` + `i.chev-icon` | `sub_sidebar.php` | sim |
| Painel do grupo | `div#acc-N.subnav-accordion-content.is-open|.is-closed > .subnav-tree` | `sub_sidebar.php` | sim |
| Página | `a.subnav-link` (+ `.is-active` e `aria-current="page"`) | `sub_sidebar.php` | sim |
| Rodapé | `.sb-foot` > CTA `.ttsc-btn.ttsc-btn-primary.ttsc-btn-sm` (`cta.url` ou `cta.drawer`, também filtrado por permissão) + `.sb-pipe` / `.sb-pipe-value` (só com métrica real) | `sub_sidebar.php` | não |
| Reabrir | `button#sub-sidebar-expand-btn.sub-sidebar-expand-btn` (visível só com o sub-sidebar recolhido, ≥ 1100px) | `layouts/main.php` | sim |
| Conteúdo | `main#main-viewport[data-od-id="content"]` | `layouts/main.php` | sim |

## Variantes / Estados

| Estado | Como | Visual |
|---|---|---|
| Rail compacto | padrão, 60px; rótulos escondidos por `@container portal-rail (max-width: 100px)` | ícones `text-slate-400` |
| Rail expandido | `:hover` / `:focus-within` em `#primary-rail`, ou `#primary-rail-wrapper.is-expanded` | largura `min(288px, 100vw - 16px)`, sombra lateral, `.rail-label` visível, `.rail-tooltip` oculto |
| Módulo ativo | `.is-active` + `aria-current="page"` (calculado no PHP: URL exata, `match`, prefixo e `SidebarRouter::moduleFor()`) | `bg-emerald-50 text-emerald-600 border-emerald-300` |
| Grupo do rail aberto | `<details open>`; o grupo do módulo ativo recebe `open data-active-group="true"` | estado salvo em `localStorage` |
| Grupo do sub aberto/fechado | `.subnav-accordion-content.is-open` / `.is-closed`, `i.chev-icon.rotate-180` | o grupo da página ativa abre no servidor; na home do módulo só o primeiro abre |
| Página ativa | `a.subnav-link.is-active` + `aria-current="page"` | `#ecfdf5` / `#047857` + borda verde (`ttsc.commercial.model.css`; escuro em `html.dark .subnav-link.is-active`) |
| Sub-sidebar recolhido (≥ 1100px) | `#sub-sidebar.collapsed` (`display: none`) + `#sub-sidebar-expand-btn` sem `hidden` | preferência em `localStorage` |
| Gaveta (< 1100px) | `@media (max-width: 1099px)`: `#primary-rail-wrapper` e `#sub-sidebar` viram `position: fixed` com `translateX(-100%)`; abrem com `.is-mobile-open`; a fechada recebe `inert` | `z-index: var(--ttsc-z-drawer)`, largura `min(320px, 100vw - 3rem)`, `#navigation-backdrop` visível |
| Botões do header | `#btn-mobile` / `#btn-sub-sidebar` com `aria-expanded` espelhando a gaveta; `#btn-sub-sidebar` fica `hidden` em página sem sub-sidebar | ocultos ≥ 1100px (`header .hdr-nav-toggles`) |
| Item sem permissão | omitido no servidor (`NavigationAccess::allows()`) | — |
| Busca sem resultado | `filterSubSidebar()` esconde links e grupos sem casamento e abre os que casam | — |

## API

A navegação é PHP + JS próprio do app; o ttscui não participa (o layout não carrega `assets/vendors/ttscui`).

**Dados, roteamento e visibilidade**

| Origem | Efeito |
|---|---|
| `app/Config/sidebar-nav.php` → `'rails'` (`aside.label`, `groups[]` com `items[]`: `module`, `url`, `label`, `key`, `icon`, `match`, `feature`) | estrutura do rail |
| `app/Config/sidebar-nav.php` → `'<modulo>'` (`sidebarId`, `title`, `icon`, `badge`, `subtitle`, `feature`, `cta`, `pipeline`, `sections[].label/icon/matchAny/isDirect/items[]` com `url`, `icon`, `matchExact`, `feature`, `permission`) | conteúdo do sub-sidebar |
| `App\Services\DynamicSidebarService::getNavigation()` | lê `storage/cache/dynamic_sidebar_nav.php` (projeção das tabelas `builder_*`, agora levando `required_permission_code` de cada item) quando existe; rails e módulos do `PagesManifest` vêm do arquivo de configuração; aplica `PortalNavigation::apply()` |
| `App\Support\PortalNavigation::apply()` | agrupa os módulos do rail por portal; o `id` de cada grupo é `<rail>-<id estável>` de `PortalNavigation::GROUP_IDS` (ex.: `admin-academic_lifecycle`), que não muda com a tradução do rótulo |
| `App\Support\FeatureFlags::enabled($flag)` | remove módulo, seção, item ou CTA com `feature` desligada no tenant |
| `App\Support\NavigationAccess::allows($node)` | remove o nó quando o usuário não tem a permissão exigida: `required_permission_code` ou `permission` declarado, senão a permissão da rota `GET` da `url` (`routePermission()`). Usa as regras do `AuthorizationGuard` (superadmin vê tudo); sem usuário ou com falha de consulta, mantém o link. Nunca grava auditoria: esconder link não é tentativa de acesso |
| Deduplicação em `sub_sidebar.php` | um destino que já está no rail nunca se repete no sub-sidebar (teste `PortalNavigationArchitectureTest::testRenderedSubmenusDoNotRepeatRailDestinations`) |
| `SidebarMetrics::value($metric)` | valor do `.sb-pipe`; sem métrica real o indicador não aparece |

**JS global** (todos em `window`)

| Função / atributo | Arquivo | Efeito |
|---|---|---|
| `toggleSubSidebar()` | `ttsc.shell.js` (dono único; `ttsc.drawer.js` só define um fallback se ele não existir) | ≥ 1100px: alterna `#sub-sidebar.collapsed`, mostra/esconde `#sub-sidebar-expand-btn` e grava `ttsc:sub-sidebar:collapsed`; < 1100px: alterna `.is-mobile-open`, fecha o rail, mostra o fundo e sincroniza `aria-expanded`/`inert`. Ignora chamadas a menos de 150 ms |
| `toggleMainSidebar()` | `ttsc.shell.js` | ≥ 1100px: alterna `#primary-rail-wrapper.is-expanded`; < 1100px: alterna a gaveta do rail |
| `closeAllSidebars()` | `ttsc.shell.js` | fecha as duas gavetas e o fundo; usado pelo `.rail-close-btn`, pelo gesto de arrastar e pelo `Esc` |
| `syncSubSidebarExpandButton()` | `ttsc.shell.js` | move `#sub-sidebar-expand-btn` para dentro de `#main-viewport`, antes do ícone 44×44 do cabeçalho da página |
| `#btn-mobile` · `#btn-sub-sidebar` · `#navigation-backdrop` | `ttsc.shell.js` | abrem as gavetas · o clique no fundo fecha |
| `Ctrl/Cmd + B` · `Esc` | `ttsc.shell.js` | alterna o sub-sidebar · fecha as gavetas e devolve o foco ao botão que as abriu |
| `/` (fora de campos de texto) | `ttsc.sidebar.js` (`focusSubSidebarFilter`) | foca `#subsidebar-filter`, abrindo a gaveta ou expandindo o sub-sidebar recolhido antes |
| `Ctrl/Cmd + K` | `ttsc.drawer.js` | busca global (`drawer-search`); o sub-sidebar não usa mais esse atalho |
| `[data-sidebar-collapse]` · `[data-accordion-toggle]` + `[data-accordion-chevron]` · `[data-sidebar-filter]` | delegação em `ttsc.drawer.js` | chama `toggleSubSidebar()` · `toggleAccordion()` e atualiza `aria-expanded` · `filterSubSidebar(valor)` |
| `toggleAccordion(accId, chevId, event)` | `sub_sidebar.php` (inline) e `ttsc.sidebar.js` | troca `is-open`/`is-closed` e gira o chevron |
| `filterSubSidebar(query)` | `ttsc.sidebar.js` (a versão inline de `sub_sidebar.php` é sobrescrita) | filtra `#sub-sidebar .subnav-group a`, abre grupos com resultado e restaura o estado anterior ao limpar (`data-before-search`) |
| `toggleSidebarPortalDropdown(e)` / `closeSidebarPortalDropdown()` | `rail.php` (inline) | abre/fecha `#sidebar-portal-dropdown`, `#primary-rail.portal-dropdown-open`, `aria-expanded`; fecha com clique fora, `Esc` ou ao sair com o mouse (120–220 ms) |
| `details[data-portal-group]` | `ttsc.sidebar.js` | grava aberto/fechado de cada grupo do rail; o grupo ativo sempre abre |
| Arrastar para reordenar | `ttsc.sidebar.js` (`initDragReorder`) | `a.rail-item` dentro de cada `.portal-group-items` do `#primary-rail` e `a.subnav-link` dentro de cada `.subnav-tree` (só ≥ 1100px); a ordem só muda entre irmãos do mesmo grupo |
| Gesto (< 1100px) | `ttsc.sidebar.js` | arrastar da borda esquerda para a direita abre a gaveta (sub-sidebar primeiro, senão o rail); para a esquerda fecha; clique fora fecha |

**Chaves de `localStorage`**: `ttsc:sub-sidebar:collapsed` (`'1'`/`'0'`), `ttsc:sidebar:portal-group:<id do grupo>`, `ttsc:sidebar:order:primary-rail:<id do grupo>` e `ttsc:sidebar:order:sub-sidebar:<data-sidebar-id>:<acc-N>`.

**Correções aplicadas** (branch `claude/design-system-extraction-srfpiz`): os botões `#btn-mobile` / `#btn-sub-sidebar` e o `#navigation-backdrop` agora são renderizados; `window.closeAllSidebars` existe; `Ctrl+K` ficou só com a busca global e o filtro usa `/`; gestos e reordenação apontam para `#primary-rail-wrapper` / `#sub-sidebar`; o menu esconde itens sem permissão (`NavigationAccess`); os ids dos grupos do rail são estáveis (`GROUP_IDS`). Continua fixa por utilitário (não por token) a cor verde do item ativo.

## Acessibilidade

- Landmarks: `header`, `aside#primary-rail` com `aria-label` do portal (“Portal da Instituição”), `aside#sub-sidebar` com `aria-label` do módulo, `main#main-viewport` com `role="main"`.
- Gavetas (< 1100px): botões com `aria-controls` + `aria-expanded` sincronizados; a gaveta fechada fica `inert` (seus links saem da ordem de Tab); `Esc` fecha e devolve o foco ao botão.
- Rail só-ícone: cada `a.rail-item` tem `aria-label` e `title`; `.rail-tooltip` é visual. O rail abre também por `:focus-within`, então a navegação por Tab mostra os rótulos.
- Página e módulo atuais marcados com `aria-current="page"`, não só por cor (o rail escreve `aria-current="false"` nos demais).
- Grupos: `button` com `aria-expanded` + `aria-controls`; grupos do rail usam `<details>/<summary>` nativos, que funcionam sem JS.
- Seletor de portal: `aria-haspopup="true"` + `aria-expanded`; fecha com `Esc`.
- Filtro: `role="searchbox"`, `aria-keyshortcuts="/"` e dica visual `.sb-kbd`; os links escondidos recebem `display: none`. Pendente: o filtro não tem `<label>` (só placeholder).
- Contraste: link ativo `#047857` sobre `#ecfdf5` (≥ 4,5:1); ícones inativos `text-slate-400` são decorativos.

## Modelos

### HTML

**1. Como o layout produz o shell** (`resources/views/app/layouts/main.php`, resumido):

```php
<body class="sb-app h-full bg-slate-50 text-slate-800 font-sans antialiased overflow-hidden flex flex-col">
    <div id="navigation-backdrop" aria-hidden="true" hidden></div>

    <?= $this->fetch('app::partials/header') ?>

    <div class="flex-1 min-h-0 flex overflow-hidden relative">
        <?= $this->fetch('app::partials/rail', ['railKey' => $railKey]) ?>

        <?php if (!($hideSubSidebar ?? false) && $sidebarModule !== null): ?>
            <?= $this->fetch('app::partials/sub_sidebar', ['module' => $sidebarModule ?? 'academic']) ?>
        <?php endif; ?>

        <button id="sub-sidebar-expand-btn" type="button" onclick="toggleSubSidebar()"
                class="sub-sidebar-expand-btn ... hidden" title="Expandir Barra Lateral">…<span>Menu</span></button>

        <main id="main-viewport" class="flex-1 overflow-y-auto ..." data-od-id="content" role="main">
            <?= $pageContent ?>
        </main>
    </div>
    <?= $this->fetch('app::partials/footer') ?>
    …
    <script src="<?= asset('js/ttsc.sidebar.js') ?>"></script>
    <script src="<?= asset('js/ttsc.drawer.js') ?>"></script>
    <script src="<?= asset('js/ttsc.select.js') ?>"></script>
    <script src="<?= asset('js/ttsc.pagination.js') ?>"></script>
    <script src="<?= asset('js/ttsc.overlays.js') ?>"></script>
    <script src="<?= asset('js/ttsc.shell.js') ?>"></script>
</body>
```

`$railKey` vem de `SidebarRouter::railFor($requestUri)` e `$sidebarModule` de `$subSidebarModule ?? SidebarRouter::moduleFor($requestUri)`. Uma página entra no sub-sidebar adicionando o item na seção do módulo em `app/Config/sidebar-nav.php` (uma `permission` explícita é opcional; sem ela vale a da rota):

```php
'academic_secretariat' => [
    'sidebarId' => 'academic-secretariat-sidebar',
    'title'     => 'Secretaria',
    'icon'      => 'fa-id-card',
    'sections'  => [
        [
            'label'    => 'Admissões e Matrículas',
            'icon'     => 'fa-id-card',
            'matchAny' => ['/academic/enrollment', '/academic/enrollment/re-enrollment'],
            'items'    => [
                ['label' => 'Matrícula',   'url' => '/academic/enrollment',               'icon' => 'fa-user-plus',    'matchExact' => ['/academic/enrollment']],
                ['label' => 'Rematrícula', 'url' => '/academic/enrollment/re-enrollment', 'icon' => 'fa-rotate-right', 'matchExact' => ['/academic/enrollment/re-enrollment']],
            ],
        ],
    ],
],
```

**2. HTML gerado** (render real de `/academic/enrollment/re-enrollment`, enxugado; classes e atributos exatos, URLs encurtadas):

```html
<!-- header.php: botões das gavetas (visíveis < 1100px) -->
<div class="hdr-nav-toggles flex items-center gap-1 shrink-0">
  <button type="button" id="btn-mobile" class="hdr-nav-toggle w-8 h-8 items-center justify-center rounded-xl text-slate-500 hover:text-emerald-600 hover:bg-slate-100 transition cursor-pointer" aria-controls="primary-rail-wrapper" aria-expanded="false" aria-label="Abrir menu principal" title="Menu principal">
    <i class="fa-light fa-bars text-sm" aria-hidden="true"></i>
  </button>
  <button type="button" id="btn-sub-sidebar" class="hdr-nav-toggle w-8 h-8 items-center justify-center rounded-xl text-slate-500 hover:text-emerald-600 hover:bg-slate-100 transition cursor-pointer" aria-controls="sub-sidebar" aria-expanded="false" aria-label="Abrir menu da seção" title="Menu da seção (Ctrl+B)">
    <i class="fa-light fa-sidebar text-sm" aria-hidden="true"></i>
  </button>
</div>

<!-- rail.php: um grupo, módulo ativo -->
<aside id="primary-rail" class="absolute inset-y-0 left-0 flex flex-col justify-between items-center py-2.5" data-od-id="rail" aria-label="Portal da Instituição">
  <details class="portal-rail-group" data-portal-group="admin-academic_lifecycle" open data-active-group="true">
    <summary title="Ciclo Acadêmico" aria-label="Ciclo Acadêmico">
      <i class="fa-light fa-graduation-cap portal-group-icon" aria-hidden="true"></i>
      <span class="portal-group-label">Ciclo Acadêmico</span>
      <i class="fa-light fa-chevron-down portal-group-chevron" aria-hidden="true"></i>
    </summary>
    <div class="portal-group-items">
      <a href="/academic/secretariat" draggable="true" data-rail-slug="academic_secretariat" aria-current="page"
         class="rail-item relative flex items-center justify-center h-10 rounded-xl transition duration-150 bg-emerald-50 text-emerald-600 border border-emerald-300 font-semibold shadow-xs is-active"
         title="Secretaria" aria-label="Secretaria">
        <div class="w-10 h-10 flex items-center justify-center shrink-0"><i class="fa-light fa-id-card text-base transition-transform duration-150"></i></div>
        <span class="rail-label text-xs font-semibold whitespace-nowrap text-emerald-700">Secretaria</span>
        <span class="rail-tooltip">Secretaria</span>
      </a>
    </div>
  </details>
</aside>

<!-- sub_sidebar.php: filtro e um grupo com a página ativa -->
<aside id="sub-sidebar" class="flex flex-col shrink-0 relative select-none" data-od-id="sidebar" data-sidebar-id="academic-secretariat-sidebar" aria-label="Secretaria">
  <div class="sb-search-filter p-3 shrink-0">
    <div class="relative flex items-center">
      <i class="fa-light fa-magnifying-glass sb-search-icon text-xs" aria-hidden="true"></i>
      <input type="search" id="subsidebar-filter" data-sb-search="true" data-sidebar-filter="sub-sidebar" placeholder="Buscar páginas..." autocomplete="off" role="searchbox" aria-keyshortcuts="/" class="sb-search-input" />
      <span class="sb-kbd" aria-hidden="true">/</span>
    </div>
  </div>
  <div class="flex-1 overflow-y-auto px-2.5 py-3 space-y-2 text-xs" style="scrollbar-width: thin;">
    <div class="subnav-group">
      <button type="button" data-accordion-toggle="acc-1" data-accordion-chevron="chev-1" aria-expanded="true" aria-controls="acc-1"
              class="sb-section-btn w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-[11px] uppercase">
        <span class="flex items-center gap-2 min-w-0 flex-1">
          <i class="fa-light fa-id-card text-xs shrink-0"></i><span class="truncate">Admissões e Matrículas</span>
        </span>
        <div class="flex items-center gap-1.5 shrink-0">
          <span class="sb-count-pill">9</span>
          <i id="chev-1" class="chev-icon fa-light fa-chevron-down text-[10px] shrink-0 rotate-180"></i>
        </div>
      </button>
      <div id="acc-1" class="subnav-accordion-content is-open mt-1">
        <div class="subnav-tree space-y-0.5">
          <a class="subnav-link" href="/academic/enrollment">
            <i class="fa-light fa-user-plus text-xs w-4 text-slate-400"></i><span class="truncate">Matrícula</span>
          </a>
          <a class="subnav-link is-active" href="/academic/enrollment/re-enrollment" aria-current="page">
            <i class="fa-light fa-rotate-right text-xs w-4"></i><span class="truncate">Rematrícula</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</aside>
```

### CSS

Arquivos e ordem (Layer 2–4 de `main.php`): `ttsc.design-system.css` (tokens de dimensão, `#sub-sidebar`, `.sb-*`, `#primary-rail .rail-item`, gavetas e `#navigation-backdrop` < 1100px), `ttsc.shell-layout.css` (regras `.sb-app #primary-rail…`, expansão por hover, `@container portal-rail`, gavetas), `ttsc.header.css` (topbar, `.hdr-nav-toggles`, condensação progressiva `.hdr-secondary`) e `ttsc.commercial.model.css` / `ttsc.luxury-commercial.css` (`.subnav-link`, `.subnav-accordion-content`, variações `html.dark`).

```css
/* Dimensões do chassi — fonte única (ttsc.design-system.css) */
:root { --ttsc-header-h: 3.5rem; --ttsc-rail-w: 60px; --ttsc-sub-sidebar-w: 320px; }

/* Largura do sub-sidebar: aside#sub-sidebar (1,0,1) vence os 264px fixos dos estilos de modelo */
aside#sub-sidebar { flex-basis: var(--ttsc-sub-sidebar-w); width: var(--ttsc-sub-sidebar-w); min-width: var(--ttsc-sub-sidebar-w); }

/* Rail: 60px, expande no hover/foco ou com .is-expanded (ttsc.shell-layout.css) */
.sb-app #primary-rail:hover,
.sb-app #primary-rail-wrapper.is-expanded #primary-rail { width: min(288px, calc(100vw - 16px)) !important; z-index: 50 !important; }

/* Botões das gavetas só abaixo de 1100px (ttsc.header.css) */
header .hdr-nav-toggles { display: none !important; }
@media (max-width: 1099px) { header .hdr-nav-toggles { display: flex !important; } }

/* Gavetas abaixo de 1100px (ttsc.design-system.css) */
@media (max-width: 1099px) {
  #primary-rail-wrapper { position: fixed !important; inset: 0 auto 0 0 !important; z-index: var(--ttsc-z-drawer) !important; transform: translateX(-100%); }
  #primary-rail-wrapper.is-mobile-open { transform: translateX(0); }
  #sub-sidebar { position: fixed !important; inset: 0 auto 0 0 !important; width: min(var(--ttsc-sub-sidebar-w), calc(100vw - 3rem)) !important; transform: translateX(-100%); }
  #sub-sidebar.is-mobile-open { transform: translateX(0); }
  #navigation-backdrop:not([hidden]) { position: fixed; inset: 0; z-index: var(--ttsc-z-backdrop); display: block; background: rgb(15 23 42 / .42); backdrop-filter: blur(2px); }
}

/* Extensão por token: estado ativo do sub-sidebar sem verde fixo (#ecfdf5/#047857) */
#sub-sidebar .subnav-link.is-active {
  background: var(--ttsc-accent-soft);
  color: var(--ttsc-accent-text);
  border-color: var(--ttsc-accent-border);
}
#sub-sidebar .subnav-link.is-active i { color: var(--ttsc-accent-text); }
#sub-sidebar .subnav-link:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: -2px; }
```

Tema escuro: o shell segue `html.dark` (classe aplicada pelo boot de tema de `main.php`); `#sub-sidebar` e `.sb-*` já leem tokens, enquanto `.subnav-link`, `.portal-rail-group` e `.hdr-nav-toggle` têm regras `html.dark` próprias com cores fixas.

### JS

Nada a inicializar: `ttsc.sidebar.js`, `ttsc.drawer.js` e `ttsc.shell.js` se ligam no `DOMContentLoaded` e já ligam `#btn-mobile`, `#btn-sub-sidebar` e `#navigation-backdrop`. Uso programático a partir de uma página:

```js
document.addEventListener('DOMContentLoaded', function () {
  // Recolher o sub-sidebar numa tela que precisa de largura (ex.: Kanban grande).
  // toggleSubSidebar() alterna; para forçar um estado, leia a classe antes.
  var sub = document.getElementById('sub-sidebar');
  var desktop = !window.matchMedia('(max-width: 1099px)').matches;
  if (sub && desktop && !sub.classList.contains('collapsed') && typeof window.toggleSubSidebar === 'function') {
    window.toggleSubSidebar();               // grava ttsc:sub-sidebar:collapsed = '1'
  }

  // Ao concluir uma ação dentro da gaveta (< 1100px), fechar a navegação
  document.getElementById('drawer-enrollment-save')?.addEventListener('click', function () {
    if (typeof window.closeAllSidebars === 'function') window.closeAllSidebars();
  });

  // Filtrar páginas a partir de outro campo (mesmo efeito do #subsidebar-filter)
  window.filterSubSidebar && window.filterSubSidebar('matrícula');

  // Abrir um grupo específico do sub-sidebar
  window.toggleAccordion && window.toggleAccordion('acc-1', 'chev-1');
});
```

### SQL

Por padrão o menu vem de `app/Config/sidebar-nav.php`. Quando o Construtor de Navegação é usado, `DynamicSidebarService::compileFromDatabase()` projeta as tabelas do banco **master** (`builder_sidebars` → `builder_navigation_groups` → `builder_navigation_items`) para `storage/cache/dynamic_sidebar_nav.php`, levando o `required_permission_code` de cada item. Consulta equivalente para um módulo, já com o mesmo filtro de permissão que `NavigationAccess` aplica no render:

```sql
SELECT g.title      AS group_title,
       g.icon_name  AS group_icon,
       i.uuid, i.title, i.icon_name, i.route_path,
       i.badge_type, i.badge_value, i.required_permission_code
  FROM builder_sidebars s
  JOIN builder_navigation_groups g
    ON g.sidebar_id = s.id AND g.is_active = 1 AND g.deleted_at IS NULL
  JOIN builder_navigation_items i
    ON i.navigation_group_id = g.id AND i.is_active = 1 AND i.is_visible = 1 AND i.deleted_at IS NULL
 WHERE s.code = :sidebar_code              -- ex.: 'academic_secretariat'
   AND s.is_active = 1
   AND s.deleted_at IS NULL
   AND (   i.required_permission_code IS NULL
        OR i.required_permission_code = ''
        OR EXISTS (SELECT 1
                     FROM permissions p
                     JOIN role_permission rp ON rp.permission_id = p.uuid
                     JOIN user_role ur       ON ur.role_id = rp.role_id
                    WHERE ur.user_id = :user_uuid
                      AND p.slug = i.required_permission_code))
 ORDER BY g.sort_order, g.id, i.sort_order, i.id;
```

No app o filtro não roda nessa consulta: `NavigationAccess` carrega uma vez por requisição os `slug` de permissão do usuário (`SELECT DISTINCT p.slug …` no tenant e no master) e decide item a item no PHP, incluindo a permissão herdada da rota quando o item não declara uma. Superadmin vê todos os itens. A rota continua conferindo o acesso pelo `AuthorizationGuard`.

## Faça / Não faça

- **Faça:** registre a página em `app/Config/sidebar-nav.php` (com `matchExact`/`matchAny`) em vez de escrever links na view.
- **Faça:** use `toggleSubSidebar()` / `toggleMainSidebar()` / `closeAllSidebars()` para mudar o estado; eles cuidam do breakpoint de 1100px, do fundo, de `aria-expanded`/`inert`, do botão de reabrir e do `localStorage`.
- **Faça:** use os tokens de dimensão (`--ttsc-header-h`, `--ttsc-rail-w`, `--ttsc-sub-sidebar-w`); nunca larguras fixas em CSS de módulo.
- **Faça:** declare a permissão da rota (ou `permission` no item) para o menu esconder o link de quem não pode abrir.
- **Não faça:** definir outra `window.toggleSubSidebar` ou outro atalho `Ctrl+K` numa view: cada atalho tem um dono (`Ctrl+B` → shell, `Ctrl+K` → busca global, `/` → filtro).
- **Não faça:** repetir no sub-sidebar um destino que já está no rail; o PHP descarta e o teste de arquitetura falha.
- **Não faça:** derivar ids de grupo do rótulo traduzido; use `PortalNavigation::GROUP_IDS`.
- **Não faça:** confiar no menu para proteger rota: esconder um link não bloqueia o acesso.
