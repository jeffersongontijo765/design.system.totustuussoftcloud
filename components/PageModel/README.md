# PageModel

A página padrão do chassi montada inteira a partir de uma ficha: cabeçalho, banner, abas segmentadas com ações, KPI + distribuição, tabela, cards, Kanban, Analytics e os drawers View / Novo / Filtrar — o mesmo esqueleto de `developer/dashboard.php` e `chassis/domain_page.php`.

## Quando usar

- Como ponto de partida de **qualquer** página de módulo dos portais autenticados; os arquétipos ([PageRecords](../PageRecords/README.md), [PagePipeline](../PagePipeline/README.md), [PageDashboard](../PageDashboard/README.md), [PageHistory](../PageHistory/README.md), [PageReport](../PageReport/README.md), [PageSettings](../PageSettings/README.md)) são esta página com `views`/`defaultView`/`create` diferentes.
- Para conferir como os blocos conversam: filtros valem para tabela, cards e Kanban; KPI, tabela e gráficos saem do mesmo conjunto.
- Não use para telas fora do shell (login: [PageAuth](../PageAuth/README.md)) nem para agenda ([PageCalendar](../PageCalendar/README.md)).

## Anatomia

```
#main-viewport
└ #model-page.space-y-3.5
  ├ PageHeader        h1 + breadcrumb + Atualizar                  → ../PageHeader
  ├ ContextBanner     título, descrição, pill de contagem          → ../ContextBanner
  ├ SegmentedTabs     KPI · Tabela · Cards · Kanban · Analytics | Filtrar · Exportar · Novo → ../SegmentedTabs
  ├ #view-kpi         KpiView (cards + distribuição + atenção)     → ../KpiView
  ├ #view-table       RecordsTable                                 → ../RecordsTable
  ├ #view-cards       RecordCards                                  → ../RecordCards
  ├ #view-kanban      KanbanBoard (SoftCloud.KanbanBoard)          → ../KanbanBoard
  └ #view-analytics   AnalyticsPanels (TTSCAnalytics)              → ../AnalyticsPanels
body
├ #backdrop-overlay
└ #model-drawers      View · Novo · Filtrar                        → ../RecordDrawers
```

| Parte | Elemento | Obrigatório |
|---|---|---|
| Viewport | `main#main-viewport` (rolagem da página; `switch*Tab` rola ao topo) | sim |
| Raiz | `div#model-page[aria-live=polite]` (no produto: conteúdo do `layouts/main.php`) | sim |
| Painéis | `#view-<aba>[role=tabpanel]`, um visível por vez (`style.display`) | sim |
| Backdrop | `#backdrop-overlay` | sim |
| Drawers | `.drawer-panel` anexados ao `body` | sim |

## Variantes

| Ficha | Resultado |
|---|---|
| `views` ausente | KPI · Tabela · Cards + Kanban (se `stages`) + Analytics (se `analytics`) |
| `views: [...]`, `defaultView` | abas e aba inicial (Report abre em `analytics`, History em `table`, Pipeline em `kanban`) |
| `create: false` | sem "Novo" e sem drawer de criação |
| `layout: "settings"` | abas = grupos, Descartar/Salvar ([SettingsPanel](../SettingsPanel/README.md)) |
| ficha ausente | cabeçalho + estado vazio "Page sheet pending" ([EmptyState](../EmptyState/README.md)) |

## API

**`TTSCModelKit.render(t, page, opts)`** (fim de `vendor/app/app.js`, renderizadores de `docs/model/app/_assets/model-page.js`)

| Argumento | Formato |
|---|---|
| `t` | `{portal:{label}, module:{label}, page:{label, route}}` — breadcrumb e semente dos registros |
| `page` | ficha da rota (`specs/<portal>/<módulo>.json` → `pages[rota]`) |
| `opts.header` / `opts.banner` / `opts.tabs` | `false` omite o bloco |

| Outras funções | Efeito |
|---|---|
| `TTSCModelKit.switchTab(id)` | troca a aba; monta Kanban/Analytics na 1ª vez |
| `TTSCModelKit.generate(page, route)` | registros de amostra determinísticos (mesma rota → mesmos dados) |
| `TTSCModelKit.blocks.*` | `header, banner, tabs, actions, viewHeader, search, pager, empty, kpi, breakdown, table, cards, card, drawers, settings` |
| `TTSCModelKit.mountKanban(page, rows)`, `.mountAnalytics(page, rows)`, `.fillView(page, row)` | montagem avulsa |
| `TTSCModelKit.tones` | tons `slate/blue/amber/purple/emerald/rose` (classes Tailwind + hex) |
| `TTSCModelKit.syncTheme()` | espelha `<html data-theme>` em `html.dark`/`html.light` (o CSS do app usa `html.dark`) |

**Ficha (resumo; detalhes em cada bloco)**

| Campo | Bloco |
|---|---|
| `title`, `icon` | cabeçalho |
| `banner {icon,title,desc,pill,attention}` | banner |
| `entity {singular, plural, icon, newLabel}` | contagens, botões, drawers |
| `fields[] {key,label,type,…}` · `titleField/codeField/subField/statusField/stageField` | tabela, cards, drawers |
| `statuses[]`, `stages[]` | badges e colunas do Kanban |
| `kpis[]`, `breakdown` | KPI |
| `cardFields`, `cardLine`, `cardBar` | cards |
| `kanbanTitle/Desc/Value/Date` | Kanban |
| `analytics[]` | Analytics |
| `drawer {metrics, sections}`, `form[]` | drawers |
| `views`, `defaultView`, `create`, `exports`, `batch` | abas e ações |
| `endpoints {create, edit, delete, export, move}` | aviso do kit (rotas da produção) |

**Endpoints da página real** (`routes/kpi-pages.generated.php`, 1.643 rotas de página):

| Método | Rota | Controller |
|---|---|---|
| GET | `/api/v1/kpi{rota}` | `PerPageKpiController::show` |
| GET | `/api/v1/domain/records{rota}?search=&status=&page=&per_page=` | `DomainCrudController::index` |
| POST | `/api/v1/domain/records{rota}` | `::store` |
| GET / PUT / DELETE | `/api/v1/domain/records{rota}/{id}` | `::show` / `::update` / `::delete` |
| POST | `/api/v1/domain/records{rota}/status` · `/statuses` | `::status` · `::addStatus` |
| GET | `/api/v1/domain/records{rota}/export?format=` | `::export` (`TableExporter::FORMATS`) |
| GET / POST | `/api/v1/domain/records{rota}/{id}/activity` · `/chat` | `::activity` · `::chat` |

Os `endpoints` da ficha de exemplo usam essas rotas reais, com a rota da página `/academic/enrollment/re-enrollment` (`inst_secretariat_reenrollment`): `POST /api/v1/domain/records/academic/enrollment/re-enrollment`, `…/{id}`, `…/status` e `…/export?format=csv`.

## Acessibilidade

- Um `h1` (cabeçalho), `h2` no banner, `h3` em visões/drawers.
- Abas com `role=tablist/tab/tabpanel` e atalhos `1`–`5`; drawers `role=dialog` com foco preso e `Esc`.
- `#model-page` é `aria-live=polite`: re-render (Atualizar) é anunciado; evite re-renderizar a cada tecla.
- Contraste herdado do runtime Tailwind + remapeamento `html.dark`; detalhes nos blocos.

## Modelos

### HTML

1) PHP real — o shim gerado por `scripts/generate-domain-pages.php` e o template canônico:

```php
<?php
// resources/views/app/pages/client/academic/enrollment/re-enrollment.php
$pageRoute  = '/academic/enrollment/re-enrollment';
$pageRail   = 'client';
$pageModule = 'Secretariat';
$title      = 'Espaço de Trabalho — Rematrícula';
$icon       = 'fa-light fa-user-plus';
$breadcrumb = [['label' => 'Portal da Instituição', 'url' => url('/dashboard')],
               ['label' => 'Rematrícula', 'url' => url('/academic/enrollment/re-enrollment')]];
$this->layout('app::layouts/main', ['title' => $title, 'icon' => $icon, 'breadcrumb' => $breadcrumb,
    'pageHasHeader' => true, 'railKey' => 'client', 'subSidebarModule' => 'academic_secretariat']);
include base_path('resources/views/app/partials/chassis/domain_page.php');
```

`domain_page.php` resolve tudo a partir de `$pageRoute`: `PortalDomainDataService::getDataForRoute()` (registros, KPI, colunas, distribuição), `DrawerRegistry::forRoute()` (CRUD), `ScaffoldKpiService::contractFor()` (contrato de `page-domain-sources.php`) e `StandardPageRegistry::tabsFor()` (Kanban/linha do tempo).

2) HTML gerado (esqueleto do preview; o conteúdo de cada painel está no README do bloco):

```html
<main id="main-viewport" class="bg-slate-50">
  <div id="model-page" class="space-y-3.5" aria-live="polite">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4"><!-- PageHeader --></div>
    <div class="bg-emerald-50/70 border border-emerald-200/80 rounded-2xl p-4 …"><!-- ContextBanner --></div>
    <div id="model-tab-toolbar" class="commercial-tabs-layout …">
      <div id="chassis-segmented-tabs" role="tablist" class="ttsc-segmented-tabs …">
        <button id="tab-btn-kpi" role="tab" aria-selected="true" aria-controls="view-kpi" data-model-tab="kpi" class="tab-btn … is-active">…KPI <span class="tab-badge">4</span></button>
        <button id="tab-btn-kanban" role="tab" aria-selected="false" aria-controls="view-kanban" data-model-tab="kanban" class="tab-btn …">…Quadro Kanban <span class="tab-badge">5</span></button>
      </div>
      <div class="commercial-tab-actions …"><!-- Filtrar · Exportar · Nova matrícula --></div>
    </div>
    <div id="view-kpi" class="space-y-5" role="tabpanel" aria-labelledby="tab-btn-kpi" style="display: block;">…</div>
    <div id="view-table" class="space-y-4" role="tabpanel" aria-labelledby="tab-btn-table" style="display: none;">…</div>
    <div id="view-cards" class="space-y-4" role="tabpanel" aria-labelledby="tab-btn-cards" style="display: none;">…</div>
    <div id="view-kanban" class="space-y-4" role="tabpanel" aria-labelledby="tab-btn-kanban" style="display: none;"><div id="model-kanban"></div></div>
    <div id="view-analytics" class="space-y-5" role="tabpanel" aria-labelledby="tab-btn-analytics" style="display: none;"><div id="model-analytics-panels" class="space-y-5"></div></div>
  </div>
</main>
<div id="backdrop-overlay" class="fixed inset-0 bg-slate-900/40 backdrop-blur-[2px] z-40 transition-opacity hidden" onclick="window.closeAllDrawers && window.closeAllDrawers()"></div>
<div id="model-drawers">
  <div id="model-drawer-view" class="drawer-panel fixed top-0 right-0 h-full w-[480px] max-w-full bg-white z-50 flex flex-col overflow-hidden">…</div>
  <div id="model-drawer-new" class="drawer-panel …">…</div>
  <div id="model-drawer-filter" class="drawer-panel …">…</div>
</div>
```

### CSS

Ordem real (de `docs/model/app/developer.html`, copiada em `vendor/app/app-1.css` e `app-2.css`): `ttsc.design-system`, `ttsc.supabase`, `ttsc.luxury-commercial`, `ttsc.shell-layout`, `ttsc.header`, `ttsc.commercial` | `ttsc.commercial.model`, `ttsc.widgets`, `ttsc.kpi-widgets`, `ttsc.notifications`, `ttsc.drawer`, `ttsc.chat-widget`, `ttsc.session-timeout`, `ttsc.pii-reveal`, `ttsc.rtl`, `ttsc.datepicker`, `ttsc`, `ttsc.pagination`, `ttsc.developer-dashboard`, `ttsc.kanban`, `ttsc.analytics-panels`. O escuro é por `html.dark` (classe), não por `data-theme`: `TTSCModelKit.syncTheme()` faz a ponte.

```css
/* Ponte do design system para a página: fundo e gutter do viewport por tokens */
#main-viewport { background: var(--ttsc-canvas); padding: var(--ttsc-space-4) var(--ttsc-space-4) var(--ttsc-space-6); }
#model-page > * + * { margin-top: var(--ttsc-space-3); }
```

### JS

```js
// Página completa a partir da ficha, abrindo na aba pedida pela URL (#kanban)
TTSCModelKit.syncTheme();
const ROUTE = '/academico/matriculas/funil';
fetch('../../models/academico.json')
  .then((r) => r.json())
  .then((sheet) => {
    TTSCModelKit.render(
      { portal: { label: 'Administração' }, module: { label: 'Acadêmico' }, page: { label: 'Funil de Matrícula', route: ROUTE } },
      sheet.pages[ROUTE], {}
    );
    const tab = location.hash.slice(1);
    if (['kpi', 'table', 'cards', 'kanban', 'analytics'].includes(tab)) TTSCModelKit.switchTab(tab);
  });

// Na página real, a troca de aba é switchDomainTab(id) e emite 'ttsc:domain-tab'
document.addEventListener('ttsc:domain-tab', (ev) => history.replaceState(null, '', '#' + ev.detail.tab));
```

### SQL

Uma consulta por bloco, todas sobre o funil real de rematrícula (`enrollment_requests`, fonte da view `inst_secretariat_reenrollment`):

```sql
-- Banner + contadores das abas
SELECT COUNT(*) AS total, SUM(status IN ('pending_review', 'rejected')) AS atencao
  FROM enrollment_requests WHERE deleted_at IS NULL;

-- KPI / Kanban / Analytics (rosca): contagem por status
SELECT status, COUNT(*) AS total
  FROM enrollment_requests WHERE deleted_at IS NULL
 GROUP BY status;

-- Distribuição por curso
SELECT course_name, COUNT(*) AS total
  FROM enrollment_requests WHERE deleted_at IS NULL
 GROUP BY course_name ORDER BY total DESC;

-- Tabela e cards (página)
SELECT uuid, student_name, course_name, class_name, shift, status, created_at
  FROM enrollment_requests
 WHERE deleted_at IS NULL AND student_name LIKE :q ESCAPE '\\'
 ORDER BY created_at DESC
 LIMIT :limit OFFSET :offset;

-- Analytics (linha): solicitações por mês
SELECT DATE_FORMAT(created_at, '%Y-%m') AS mes, COUNT(*) AS total
  FROM enrollment_requests
 WHERE deleted_at IS NULL AND created_at >= CURRENT_DATE - INTERVAL 12 MONTH
 GROUP BY mes ORDER BY mes;

-- Drawer View
SELECT * FROM inst_secretariat_reenrollment WHERE uuid = :uuid;
```

`PortalDomainDataService::getDataForRoute()` devolve `records`, `kpiCards`, `explorerColumns`, `totalRecords`, `statusCounts` e `distribution`, e o `domain_page.php` distribui isso pelos blocos.

## Faça / Não faça

- **Faça:** uma ficha por página; KPI, tabela e gráficos do mesmo conjunto de registros.
- **Faça:** dados reais na página de produção — a ficha é só o contrato e o modelo, nunca fallback inventado.
- **Não faça:** CSS próprio por página; tudo vem dos blocos e dos arquivos de `assets/css`.
- **Não faça:** abas que a entidade não justifica (Kanban sem etapas, Analytics sem agregação).
