# StarterKitAppShell

Ponto de partida para qualquer tela autenticada: o render real de `resources/views/app/layouts/main.php` (header global, rail, sub-sidebar, rodapé, ações flutuantes) com o corpo padrão de página — cabeçalho, banner de contexto, abas segmentadas — e um slot vazio onde entra o conteúdo.

> Também listado em: **Navegação › Navigation** (o mesmo chassi, visto pela navegação) e **Páginas › PageModel**.

## Quando usar

- Toda página nova dentro do app (portais admin, developer, teacher, student, parents, thirdparty): a página só fornece `$this->section('content')`; o chassi vem do layout.
- Página de domínio com as 5 abas (KPI, Tabela, Cartões, Kanban, Analytics): gere a página fina e inclua `app/partials/chassis/domain_page.php` (é exatamente o corpo deste kit).
- Precisa do conteúdo em largura total sem o menu do módulo → [StarterKitAppShellCollapsed](../StarterKitAppShellCollapsed/README.md) (mesmo layout, sub-sidebar recolhido) ou `hideSubSidebar => true`.
- Portais de aluno/responsável/professor/terceiros → [StarterKitPortalStudent](../StarterKitPortalStudent/README.md) (mesmo layout, outro `railKey`).
- Tela sem sessão (login, MFA, seleção de portal) → [StarterKitAuth](../StarterKitAuth/README.md). Erro → [StarterKitError](../StarterKitError/README.md). Site institucional → [StarterKitPublicSite](../StarterKitPublicSite/README.md).

## Anatomia

```
body.sb-app (h-full, flex-col, overflow-hidden)
├─ header[data-od-id="topnav"]  app/partials/header.php ............ 56px  (--ttsc-header-h)
│   [logo] [Entidade v] / [Unidade v] / [Ano Letivo 2026] ......... [agenda][busca][LGPD][sino][ajuda][latência][avatar]
├─ div.flex-1.flex (corpo)
│  ├─ #primary-rail-wrapper > aside#primary-rail   app/partials/rail.php ............ 60px (--ttsc-rail-w)
│  ├─ aside#sub-sidebar                            app/partials/sub_sidebar.php ..... 320px (--ttsc-sub-sidebar-w)
│  ├─ button#sub-sidebar-expand-btn.hidden         (aparece com o sub-sidebar recolhido)
│  └─ main#main-viewport (overflow-y auto, px-4 sm:px-6 lg:px-8, space-y-4, pb-16)
│      ├─ cabeçalho: ícone 44px + h1 + breadcrumb ............ [Atualizar]
│      ├─ banner de contexto (bg-emerald-50/70, selo de permissão, "Banco ativo")
│      ├─ #domain-tab-toolbar > #chassis-segmented-tabs (.ttsc-segmented-tabs) + Filtrar/Exportar
│      └─ SLOT  <?= $pageContent ?>   (#view-kpi / #view-table / #view-cards / #view-kanban / #view-analytics)
├─ footer#appMainFooter   app/partials/footer.php ............ 40px
├─ #floating-actions-container (voltar ao topo com anel de progresso + chat)
├─ modal.php · drawer.php · cookie_consent_modal.php · confirm_dialog.php · section('drawers')
└─ #totus-toast-container + js_i18n_bridge.php + scripts (ordem abaixo) + section('scripts')
```

| Parte | Arquivo / seletor real | Obrigatório |
|---|---|---|
| Layout | `resources/views/app/layouts/main.php` (`$this->layout('app::layouts/main', [...])`) | sim |
| Header global | `app/partials/header.php` → `header[data-od-id="topnav"]`, `#btn-org-dropdown`, `#btn-unit-dropdown`, `#btn-period-dropdown`, `#header-notif-badge` | sim |
| Rail | `app/partials/rail.php` → `#primary-rail-wrapper > aside#primary-rail`, `a.rail-item.is-active` | sim |
| Sub-sidebar | `app/partials/sub_sidebar.php` → `aside#sub-sidebar`, `#subsidebar-filter`, `a.subnav-link.active` | por módulo |
| Cabeçalho automático | `app/components/templates/page-heading.php` (só se a página não tiver `<h1>` nem `pageHasHeader`) | sim |
| Corpo de domínio | `app/partials/chassis/domain_page.php` (cabeçalho, banner, abas, 5 visões) | páginas de domínio |
| Slot | `section('content')` → `$pageContent` dentro de `main#main-viewport` | sim |
| Rodapé | `app/partials/footer.php` → `footer#appMainFooter` | sim |
| Overlays globais | `app/partials/modal.php`, `drawer.php`, `cookie_consent_modal.php`, `confirm_dialog.php` | sim |
| Slots extras | `section('drawers')` (gavetas da página), `section('scripts')` (JS da página) | não |

### Variáveis do layout

| Variável (2º argumento de `layout()`) | Efeito |
|---|---|
| `title`, `description`, `icon`, `breadcrumb` | `<title>` e o `page-heading` automático |
| `pageHasHeader` | `true` quando a página desenha o próprio cabeçalho (o `domain_page` desenha) |
| `railKey` | `admin`, `developer`, `teacher`, `student`, `guardian`, `third-party` (aceita `client`, `parents`, `thirdparty`, `dev`) — padrão: `SidebarRouter::railFor(URI)` |
| `subSidebarModule` | módulo do sub-sidebar (ex.: `academic`, `dev_identity`) — padrão: `SidebarRouter::moduleFor(URI)` |
| `hideSubSidebar` | `true` remove o sub-sidebar desta página |

## Variantes / Estados

| Estado | Como | Onde ver |
|---|---|---|
| Desktop (≥ 1100px) | rail 60px + sub-sidebar 320px fixos | botão Desktop 1440 |
| Sub-sidebar recolhido | `#sub-sidebar.collapsed` + `#sub-sidebar-expand-btn` visível; `Ctrl+B`; `localStorage['ttsc:sub-sidebar:collapsed']='1'` | [StarterKitAppShellCollapsed](../StarterKitAppShellCollapsed/README.md) |
| ≤ 1099px | rail e sub-sidebar viram gavetas (`translateX(-100%)` → `.is-mobile-open`); `#btn-mobile` e `#btn-sub-sidebar` aparecem no início do header (`.hdr-nav-toggles`) e `#navigation-backdrop` cobre o conteúdo enquanto a gaveta está aberta | Tablet 1024 |
| < 1024px | gesto de arrastar abre/fecha a gaveta (`ttsc.sidebar.js`, limiar `SWIPE_THRESHOLD`) e dica `.sb-swipe-hint` | Tablet/Mobile |
| ≤ 767px | botões do header com 44×44 (alvo de toque) | Mobile 390 |
| ≤ 639px | `.ttsc-content` com padding 14px; rodapé compacto | Mobile 390 |
| Abas estreitas | `ttsc.tabs-overflow.js` agrupa as abas que não cabem em "Mais +N" | Mobile 390 |
| Tema escuro | `html.dark` + `data-theme="dark"`; preferência em `localStorage['ttsc-theme']` e cookie `ttsc-theme` (o PHP lê o cookie para evitar FOUC) | alternar o tema do preview |

Corrigido no repo (commit `fb7bd273c` fix(shell), branch `claude/design-system-extraction-srfpiz`): o header passou a imprimir `#btn-mobile`/`#btn-sub-sidebar`, o `main.php` imprime `#navigation-backdrop`, e a 390px o header e o rodapé não transbordam mais (o rodapé quebra em linhas). O kit foi regerado a partir desse código.

## API

| Ponto de integração | Efeito |
|---|---|
| `window.toggleSubSidebar()` / `Ctrl+B` | ≥ 1100px recolhe/expande e grava `ttsc:sub-sidebar:collapsed`; ≤ 1099px abre/fecha a gaveta |
| `window.toggleMainSidebar()` / `#btn-mobile` | abre/fecha o rail em gaveta (≤ 1099px) |
| `Esc` / clique em `#navigation-backdrop` | fecha as gavetas de navegação |
| `[data-sidebar-collapse]` (o `«` do sub-sidebar, `#subsidebar-collapse-btn`) | delegado por `ttsc.drawer.js` para `toggleSubSidebar()` |
| `window.scrollToTop()` | rola `#main-viewport` ao topo; o anel `#scroll-progress-ring` acompanha a rolagem |
| `window.toggleChatBot()` | abre `#support-chat-popover` |
| `window.switchDomainTab('kpi'|'table'|'cards'|'kanban'|'analytics')` | troca a visão (definido pelo `domain_page.php`) e dispara `ttsc:domain-tab` com `{detail:{tab}}` |
| `openDrawer('drawer-period')`, `openDrawer('drawer-profile')` … | gavetas globais do header (`ttsc.drawer.js`) |
| `#totus-toast-container` + `window.showToast(msg, tipo, título)` | toasts globais |
| `data-idle-timeout`, `data-ping-url` em `ttsc.session-timeout.js` | aviso de sessão ociosa |

## Acessibilidade

- Landmarks: `header` (topbar), `aside` com `aria-label` (nome do portal no rail, nome do módulo no sub-sidebar), `main role="main"`, `footer`.
- `h1` único por página (o `domain_page` ou o `page-heading` automático); breadcrumb com o item atual sem link.
- Itens ativos com `aria-current="page"` no rail e no sub-sidebar; rail só-ícone com `title`/`aria-label`.
- Abas: botões reais (`button type="button"`); a aba ativa tem peso 600 e fundo, não só cor.
- `#totus-toast-container` com `aria-live="polite"`; `Esc` fecha gavetas; foco visível com `--ttsc-accent`.
- Texto: corpo `--ttsc-text`, secundário `--ttsc-text-2` (≥ 7:1), metadados `--ttsc-text-muted` (≥ 4,5:1); verde de texto só com `--ttsc-accent-text`.

## Modelos

### HTML

Página nova (view Plates) — o layout faz o resto:

```php
<?php
// resources/views/app/pages/client/academic/rematriculas.php
$this->layout('app::layouts/main', [
    'title'            => 'Rematrículas 2027',
    'description'      => 'Acompanhe a renovação das matrículas da unidade.',
    'icon'             => 'fa-light fa-user-plus',
    'breadcrumb'       => [
        ['label' => 'Portal da Instituição', 'url' => url('/client/dashboard')],
        ['label' => 'Rematrículas', 'url' => url('/client/academic/re-enrollment')],
    ],
    'pageHasHeader'    => true,
    'railKey'          => 'admin',
    'subSidebarModule' => 'academic',
]);
?>
<?php $this->start('content') ?>
<!-- Cabeçalho (mesma marcação do domain_page.php) -->
<div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
  <div class="flex items-start space-x-3.5">
    <div class="w-11 h-11 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center shrink-0">
      <i class="fa-light fa-user-plus text-emerald-600 text-lg" aria-hidden="true"></i>
    </div>
    <div>
      <h1 class="text-xl font-semibold text-slate-900 tracking-tight">Rematrículas 2027</h1>
      <div class="flex items-center space-x-2 text-xs text-slate-400 mt-0.5">
        <i class="fa-light fa-house text-[10px]" aria-hidden="true"></i>
        <a href="<?= url('/client/dashboard') ?>" class="hover:text-slate-600 transition">Portal da Instituição</a>
        <span>/</span><span class="text-slate-600 font-medium">Rematrículas</span>
      </div>
    </div>
  </div>
  <button type="button" onclick="location.reload()" class="ttsc-btn ttsc-btn-primary ttsc-btn-sm">
    <i class="fa-light fa-arrows-rotate text-xs" aria-hidden="true"></i><span>Atualizar</span>
  </button>
</div>

<!-- Banner de contexto -->
<div class="bg-emerald-50/70 border border-emerald-200/80 rounded-2xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-3">
  <div class="flex items-center space-x-3.5 min-w-0">
    <div class="w-10 h-10 rounded-xl bg-white border border-emerald-200 flex items-center justify-center text-emerald-600 shrink-0">
      <i class="fa-light fa-user-plus text-base" aria-hidden="true"></i>
    </div>
    <div class="min-w-0">
      <h2 class="text-base font-semibold text-slate-800">Unidade Centro · Ano Letivo 2027</h2>
      <p class="text-xs text-slate-500 mt-0.5">1.284 alunos aptos, 96 com pendência financeira.</p>
    </div>
  </div>
</div>

<!-- Abas segmentadas -->
<div id="domain-tab-toolbar" class="flex flex-col lg:flex-row lg:items-center justify-between gap-3 select-none">
  <div id="chassis-segmented-tabs" class="ttsc-segmented-tabs inline-flex p-1 bg-slate-200/75 rounded-2xl border border-slate-200 text-xs font-medium text-slate-600 gap-1 relative" role="tablist">
    <button id="tab-btn-kpi" type="button" onclick="switchDomainTab('kpi')" role="tab" aria-selected="true"
      class="tab-btn is-active px-3.5 py-1.5 rounded-xl transition flex items-center space-x-1.5 bg-white text-slate-900 shadow-sm font-semibold">
      <i class="fa-light fa-chart-simple text-xs" aria-hidden="true"></i><span>KPI</span>
    </button>
    <button id="tab-btn-table" type="button" onclick="switchDomainTab('table')" role="tab" aria-selected="false"
      class="tab-btn px-3.5 py-1.5 rounded-xl transition flex items-center space-x-1.5 text-slate-600 hover:text-slate-900 bg-transparent">
      <i class="fa-light fa-table-list text-xs" aria-hidden="true"></i><span>Tabela de Dados</span>
    </button>
  </div>
</div>

<!-- SLOT: as visões da página -->
<div id="view-kpi" class="space-y-5">…</div>
<div id="view-table" class="space-y-5" style="display:none">…</div>
<?php $this->stop() ?>

<?php $this->start('scripts') ?>
<script nonce="<?= \App\Security\CspNonce::get() ?>" src="<?= asset('js/kpi-pages/client/secretaria/rematriculas.js') ?>"></script>
<?php $this->stop() ?>
```

Gatilhos de gaveta (≤ 1099px) — marcação real de `app/partials/header.php` (início do `header`) e de `main.php` (filho do `<body>`):

```html
<div class="hdr-nav-toggles flex items-center gap-1 shrink-0">
  <button type="button" id="btn-mobile" class="hdr-nav-toggle w-8 h-8 items-center justify-center rounded-xl text-slate-500 hover:text-emerald-600 hover:bg-slate-100 transition cursor-pointer"
          aria-controls="primary-rail-wrapper" aria-expanded="false" aria-label="Abrir menu principal" title="Menu principal">
    <i class="fa-light fa-bars text-sm" aria-hidden="true"></i>
  </button>
  <button type="button" id="btn-sub-sidebar" class="hdr-nav-toggle w-8 h-8 items-center justify-center rounded-xl text-slate-500 hover:text-emerald-600 hover:bg-slate-100 transition cursor-pointer"
          aria-controls="sub-sidebar" aria-expanded="false" aria-label="Abrir menu da seção" title="Menu da seção (Ctrl+B)">
    <i class="fa-light fa-sidebar text-sm" aria-hidden="true"></i>
  </button>
</div>
<!-- main.php: mostrado pelo ttsc.shell.js enquanto uma gaveta está aberta; clique fecha -->
<div id="navigation-backdrop" aria-hidden="true" hidden></div>
```

Página de domínio gerada (forma curta, usada pelas páginas do repo):

```php
<?php
$pageRoute = '/client/academic/re-enrollment';
$pageRail = 'admin';
$title = 'Espaço de Trabalho — Rematrícula';
$icon = 'fa-light fa-user-plus';
$this->layout('app::layouts/main', ['title' => $title, 'icon' => $icon, 'pageHasHeader' => true, 'railKey' => 'admin', 'subSidebarModule' => 'academic']);
include base_path('resources/views/app/partials/chassis/domain_page.php');
```

### CSS

Ordem real das folhas (`$coreStyleAssets` em `main.php`) — copie nesta ordem:

```css
/* 0 */ @import "inter.css";
/* 1 */ @import "tailwind-runtime.css";
/* 2 */ @import "ttsc.design-system.css"; @import "ttsc.supabase.css"; @import "ttsc.luxury-commercial.css";
/* 3 */ @import "ttsc.shell-layout.css"; @import "ttsc.header.css";
/* 4 */ @import "ttsc.commercial.css"; @import "ttsc.commercial.model.css";
/* 5 */ @import "ttsc.widgets.css"; @import "ttsc.kpi-widgets.css"; @import "ttsc.notifications.css"; @import "ttsc.drawer.css";
        @import "ttsc.chat-widget.css"; @import "ttsc.session-timeout.css"; @import "ttsc.pii-reveal.css"; @import "ttsc.rtl.css"; @import "ttsc.datepicker.css";
/* 6 */ @import "ttsc.css"; @import "ttsc.pagination.css";
/* +  */ /* fonts/fontawesome.v7.2.0/css/all.css, vendors/datatables-net/dataTables.dataTables.css e os CSS de domínio por rota (ttsc.financial-pages.css …) */
```

Extensão útil: um slot com estado vazio para páginas em construção, só com tokens.

```css
.kit-slot {
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: var(--ttsc-space-2);
  min-height: 340px; padding: var(--ttsc-space-6);
  border: 2px dashed var(--ttsc-border-strong); border-radius: var(--ttsc-radius-surface);
  background: var(--ttsc-surface); color: var(--ttsc-text-muted); text-align: center;
}
.kit-slot i { font-size: 28px; color: var(--ttsc-accent-text); }
.kit-slot strong { color: var(--ttsc-text); }
/* dimensões do chassi: nunca fixe larguras no CSS de módulo */
.minha-pagina-sticky { top: calc(var(--ttsc-header-h) + var(--ttsc-space-2)); }
```

### JS

Ordem real dos scripts no fim do `<body>` (depois de `js_i18n_bridge.php`): `ttsc.js`, `ttsc.events.js`, `ttsc.tabs-overflow.js`, `ttsc.sidebar.js`, `ttsc.drawer.js`, `ttsc.select.js`, `ttsc.pagination.js`, `ttsc.datepicker.js`, `ttsc.notifications.js`, `ttsc.notification-center.js`, `ttsc.overlays.js`, `ttsc.shell.js`, `ttsc.session-timeout.js`, depois `section('scripts')`. `chart.umd.min.js` + `ttsc.chart-defaults.js` entram no `<head>` só quando a página carrega Chart.js.

```js
// assets/js/kpi-pages/client/secretaria/rematriculas.js — script da página (vai em section('scripts'))
(function () {
  'use strict';
  // reage à troca de aba do chassi (switchDomainTab dispara ttsc:domain-tab)
  document.addEventListener('ttsc:domain-tab', function (e) {
    if (e.detail.tab === 'table' && !window.__rematriculasLoaded) {
      window.__rematriculasLoaded = true;
      fetch(document.querySelector('base').href + 'api/v1/academic/re-enrollments?status=pending', {
        headers: { 'Accept': 'application/json', 'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content },
        credentials: 'same-origin'
      })
        .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
        .then(function (res) {
          var badge = document.querySelector('#tab-btn-table .tab-badge');
          if (badge) badge.textContent = String(res.data.length);
        })
        .catch(function (err) { window.showToast && window.showToast('Não foi possível carregar as rematrículas: ' + err.message, 'error', 'Rematrículas'); });
    }
  });
  // atalho: Alt+1..5 troca de aba
  document.addEventListener('keydown', function (e) {
    var tabs = ['kpi', 'table', 'cards', 'kanban', 'analytics'], n = parseInt(e.key, 10);
    if (e.altKey && n >= 1 && n <= 5 && typeof window.switchDomainTab === 'function') { e.preventDefault(); window.switchDomainTab(tabs[n - 1]); }
  });
})();
```

No kit, o `../bundle.js` avalia os engines no `DOMContentLoaded`; por isso o `kit.html` traz um shim que executa listeners de `DOMContentLoaded` registrados tarde (sem ele, `ttsc.shell.js`, `ttsc.sidebar.js` e `ttsc.overlays.js` não iniciam). No app real não é preciso: os scripts estão no fim do `<body>`.

### SQL

O header e a navegação são montados a cada request com estas consultas (banco **master** salvo indicação):

```sql
-- 1) Entidades (tenants) do seletor #btn-org-dropdown — TenantManager::getAccessibleTenants()
SELECT DISTINCT t.uuid, t.code, t.company_name
  FROM tenants t
 WHERE t.status = 'active'
   AND (   t.uuid = :user_tenant_id
        OR EXISTS (SELECT 1 FROM user_memberships m
                    WHERE m.user_uuid = :user_uuid AND m.tenant_uuid = t.uuid AND m.status = 'active')
        OR t.uuid IN (SELECT u.tenant_id
                        FROM user_units uu
                        JOIN units u ON u.uuid = uu.unit_id
                       WHERE uu.user_id = :user_uuid AND uu.status = 'active' AND u.status = 'active'))
 ORDER BY t.company_name;

-- 2) Unidades do seletor #btn-unit-dropdown — TenantManager::getAccessibleUnits()
SELECT DISTINCT u.uuid, u.code, u.name, u.is_headquarters
  FROM units u
  LEFT JOIN user_units uu ON uu.unit_id = u.uuid AND uu.user_id = :user_uuid AND uu.status = 'active'
  JOIN users usr ON usr.uuid = :user_uuid
 WHERE (u.tenant_id = :tenant_uuid OR u.entity_id IN (SELECT e.id FROM entities e WHERE e.uuid = :tenant_uuid))
   AND u.status = 'active' AND u.deleted_at IS NULL
   AND (uu.id IS NOT NULL
        OR (usr.unit_id = u.uuid AND NOT EXISTS (SELECT 1 FROM user_units r WHERE r.user_id = usr.uuid AND r.unit_id = u.uuid)))
 ORDER BY u.is_headquarters DESC, u.name;

-- 3) Itens do sub-sidebar filtrados por permissão (DynamicSidebarService)
SELECT g.title AS group_title, g.icon_name AS group_icon,
       i.uuid, i.title, i.icon_name, i.route_path, i.badge_type, i.badge_value, i.required_permission_code
  FROM builder_sidebars s
  JOIN builder_navigation_groups g ON g.sidebar_id = s.id AND g.is_active = 1 AND g.deleted_at IS NULL
  JOIN builder_navigation_items i ON i.navigation_group_id = g.id AND i.is_active = 1 AND i.is_visible = 1 AND i.deleted_at IS NULL
 WHERE s.code = :sidebar_code AND s.is_active = 1 AND s.deleted_at IS NULL
   AND (   i.required_permission_code IS NULL OR i.required_permission_code = ''
        OR EXISTS (SELECT 1 FROM permissions p
                     JOIN role_permission rp ON rp.permission_id = p.uuid
                     JOIN user_role ur ON ur.role_id = rp.role_id
                    WHERE ur.user_id = :user_uuid AND p.slug = i.required_permission_code))
 ORDER BY g.sort_order, g.id, i.sort_order, i.id;

-- 4) Períodos da gaveta #drawer-period (banco do tenant): o atual primeiro
SELECT uuid, code, name, year, type, start_date, end_date, status
  FROM academic_periods
 WHERE deleted_at IS NULL
   AND (unit_uuid = :unit_uuid OR unit_uuid IS NULL)
 ORDER BY is_current DESC, start_date DESC
 LIMIT 12;

-- 5) Selo do sino #header-notif-badge (banco do tenant) — NotificationService::getUserFeedUnreadCount()
SELECT (SELECT COUNT(*) FROM sac_notifications
         WHERE tenant_id = :tenant_id AND user_id = :user_uuid AND is_read = 0)
     + (SELECT COUNT(*) FROM notification_instances
         WHERE tenant_id = :tenant_id AND channel = 'in_app' AND status IN ('sent', 'delivered') AND created_by = :user_id
           AND deleted_at IS NULL) AS unread_total;
```

`header.php` guarda o tenant e a unidade escolhidos na sessão (`tenant_id`, `current_unit_uuid`) e imprime os nomes já escapados; o sub-sidebar recebe o array agrupado por `group_title`; o selo é atualizado pelo `ttsc.notification-center.js` via `GET notifications/api/user-feed/unread`. A migração `2026_10_22_000001` acrescentou `units.deleted_at`, então a consulta 2 é a mesma do `TenantManager`; a `2026_10_22_000005` passou `sac_notifications.user_id` para UUID (por isso `:user_uuid` na consulta 5) — note que `getUserFeedUnreadCount()` ainda recebe `int $userId`.

## Como começar um projeto a partir do kit

1. **Arquivos do kit**: `kit.html` (render real, sem rede) e `preview.html` (barra de larguras). Gerados por `$SPD/dsh/gen_kits.py` a partir de `render_harness.php`.
2. **No repo**: crie a view em `resources/views/app/pages/<portal>/<módulo>/<página>.php` com `$this->layout('app::layouts/main', …)` e o conteúdo em `section('content')`; registre a rota e o item de sub-sidebar (`builder_navigation_items`).
3. **Em outro projeto** (PHP + Plates): copie `resources/views/app/layouts/main.php`, `app/partials/{header,rail,sub_sidebar,footer,modal,drawer,cookie_consent_modal,confirm_dialog,js_i18n_bridge,locale_init,ttsc_format}.php`, `app/components/xss-helper.php`, `app/components/templates/page-heading.php`, `app/partials/chassis/domain_page.php`; os 20 CSS da lista acima de `assets/css/`; `assets/fonts/fontawesome.v7.2.0/`; `assets/vendors/datatables-net/dataTables.dataTables.css`; os 13 JS da lista acima de `assets/js/`; e os helpers `asset()`, `url()`, `csrf_token()`, `CspNonce::get()`, `SidebarRouter`.
4. **Sem PHP**: use o `kit.html` como HTML estático — troque `../bundle.css`/`../bundle.js` pelas folhas e scripts na ordem acima e apague o shim de `DOMContentLoaded`.

## Faça / Não faça

- **Faça:** toda página autenticada herdando `app::layouts/main`; só o conteúdo muda.
- **Faça:** passe `pageHasHeader => true` quando a página desenhar o próprio `h1` (evita cabeçalho duplicado).
- **Faça:** scripts de página em `section('scripts')` e gavetas em `section('drawers')`, com `nonce`.
- **Faça:** respeite os pontos de quebra do chassi (1099px gaveta, 1024px gesto, 767px alvo de toque, 639px padding).
- **Não faça:** copiar header/rail/sub-sidebar para dentro da view, ou criar outro `<main>`.
- **Não faça:** larguras fixas (`w-[320px]`, `left: 60px`) — use `--ttsc-rail-w`, `--ttsc-sub-sidebar-w`, `--ttsc-header-h`.
- **Não faça:** ler o tema por outra chave — o app usa `localStorage['ttsc-theme']` + cookie `ttsc-theme` + `html.dark`.
