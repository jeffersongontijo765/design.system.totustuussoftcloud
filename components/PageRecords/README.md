# PageRecords

Arquétipo padrão das páginas de módulo: lista de uma entidade com KPI, Tabela de Dados, Cards e Analytics, ações Filtrar · Exportar · Novo e os drawers de CRUD.

## Quando usar

- Toda página cujo assunto é "os registros de X": cursos, turmas, matrículas, solicitações, protocolos. É o arquétipo de cerca de 3 em cada 4 páginas da sidebar.
- Use outro arquétipo só quando a regra abaixo apontar para ele; sem etapas reais, **não** vire Pipeline.

### Regra de escolha do arquétipo

Escolha pela natureza da página, nesta ordem:

1. **Dashboard** ([PageDashboard](../PageDashboard/README.md)) — home de módulo ou de portal (`/academic`, `/student/dashboard`): resumo, sem "Novo".
2. **Settings** ([PageSettings](../PageSettings/README.md)) — configurações do módulo (`…/settings`, `…/config`).
3. **Report** ([PageReport](../PageReport/README.md)) — relatórios e indicadores (`…/reports/*`, `…/analytics`, `…/indicators`): gráficos primeiro, sem "Novo".
4. **History** ([PageHistory](../PageHistory/README.md)) — histórico ou auditoria somente leitura (`…/audit`, `…/logs`, `…/history`, `…/timeline`).
5. **Pipeline** ([PagePipeline](../PagePipeline/README.md)) — itens que andam por **etapas reais** e mudar de etapa grava o status (`StandardPageRegistry::tabsFor()['kanban'] === true`).
6. **Records** ([PageRecords](../PageRecords/README.md)) — lista de uma entidade. **É o padrão**: na dúvida, Records.

Fora do shell de módulos: agenda → [PageCalendar](../PageCalendar/README.md); telas de acesso → [PageAuth](../PageAuth/README.md).

### Mapa de abas e ações

| Arquétipo | Abas (`views`) | Abre em (`defaultView`) | Ações da barra | Novo / drawers de escrita |
|---|---|---|---|---|
| Dashboard | KPI · Analytics | KPI | Filtrar · Exportar | não (`create:false`) |
| Records | KPI · Tabela · Cards (+ Analytics) | KPI | Filtrar · Exportar · Novo | sim, se a fonte é gravável |
| Pipeline | KPI · Tabela · Cards · Kanban · Analytics | Kanban | Filtrar · Exportar · Novo | sim; mover cartão = `POST …/status` |
| History | KPI · Tabela · Analytics | Tabela | Filtrar · Exportar (CSV, PDF) | não; sem editar/excluir |
| Report | KPI · Tabela · Analytics | Analytics | Filtrar · Exportar | não |
| Settings | um grupo por aba | 1º grupo | Descartar · Salvar alterações | — |

`StandardPageRegistry::tabsFor($rota)` (em `app/Support/StandardPageRegistry.php`) decide Kanban e linha do tempo: primeiro a tabela curada `TAB_RULES` (ex.: `academic/academic-recovery` → Kanban + linha do tempo; `academic/settings/calendar` → nenhum); senão a folha da rota contra `LIFECYCLE_KEYWORDS` (`pipeline`, `workflow`, `requests`, `approvals`, `tickets`, `orders`, `applications`…) e `TIMELINE_KEYWORDS` (`audit`, `logs`, `history`, `timeline`, `ledger`, `journal`…); folhas `reports`, `analytics`, `settings`, `config`, `dashboard` nunca recebem Kanban. `chassis/domain_page.php` também liga o Kanban quando a fonte curada tem ≥ 2 status (`$curatedLifecycle`).

### Quantas páginas reais de cada arquétipo

Classificação das **2.566 URLs** de `app/Config/sidebar-nav.php` pela regra acima (folha da rota + `tabsFor()`; heurística, conferida por amostragem):

| Arquétipo | Páginas | Exemplos reais no Acadêmico |
|---|---|---|
| Records | ≈ 1.977 (77%) | `/academic/courses`, `/academic/units`, `/academic/enrollment/re-enrollment` |
| Pipeline | ≈ 186 (`tabsFor()` dá Kanban a 190 URLs) | `/academic/secretariat/diplomas`, `/academic/pastoral/requests`, `/academic/spaces/approvals` |
| Report | ≈ 125 | `/academic/reports`, `/academic/indicators`, `/academic/report-cards` |
| History | ≈ 105 (`tabsFor()` dá linha do tempo a 207) | `/academic/reports/audit`, `/developer/identity/audit`, `/student/diary/history` |
| Settings | ≈ 95 | `/academic/settings`, `/academic/settings/calendar` |
| Dashboard | ≈ 45 | `/academic`, `/student/dashboard`, `/teacher/dashboard` |
| Calendar | ≈ 33 | `/academic/calendar`, `/academic/events/calendar` |

## Anatomia

```
PageHeader · ContextBanner
[KPI 4] [Tabela de Dados 48] [Cards / Grade 48] [Analytics 3]      [Filtrar] [Exportar ▾] [+ Nova matrícula]
#view-kpi       KpiView: 4 cards + distribuição + atenção
#view-table     RecordsTable (busca, ordenação, expansão, lote, paginação)
#view-cards     RecordCards
#view-analytics AnalyticsPanels
drawers: View · Novo · Filtrar (+ Editar, Excluir, lote no chassi real)
```

| Bloco | README |
|---|---|
| Cabeçalho / banner | [PageHeader](../PageHeader/README.md) · [ContextBanner](../ContextBanner/README.md) |
| Abas e ações | [SegmentedTabs](../SegmentedTabs/README.md) |
| KPI | [KpiView](../KpiView/README.md) |
| Tabela / cards | [RecordsTable](../RecordsTable/README.md) · [RecordCards](../RecordCards/README.md) |
| Gráficos | [AnalyticsPanels](../AnalyticsPanels/README.md) |
| Drawers | [RecordDrawers](../RecordDrawers/README.md) |

## Variantes

| Variante | Como |
|---|---|
| Gravável | fonte em `page-domain-sources.php` sem `writable => false` e `DrawerRegistry::forRoute()` com `variants` → Novo, Editar, Excluir, Mudar status |
| Consulta | `writable => false` (ex.: `/academic/enrollment/re-enrollment`): banner "Consulta — gravado pelo fluxo do sistema", sem Novo/Editar/Excluir |
| Sem Analytics | ficha sem `analytics[]` ou `views: ["kpi","table","cards"]` |
| Abre na tabela | `defaultView: "table"` para listas longas de consulta |

## API

| Ficha | Valor típico em Records |
|---|---|
| `views` | `["kpi","table","cards","analytics"]` (padrão quando não há `stages`) |
| `defaultView` | `"kpi"` (ou `"table"`) |
| `create` | omitido (`true`) |
| `fields`, `kpis`, `breakdown`, `cardFields`, `drawer`, `form`, `analytics` | ver blocos |

| JS | Efeito |
|---|---|
| `TTSCModelKit.render(t, page, {})` + `TTSCModelKit.switchTab('table')` | página inteira, aberta na tabela (o preview) |
| `switchDomainTab(id)`, evento `ttsc:domain-tab` | página real |

| Endpoint | Uso |
|---|---|
| `GET /api/v1/kpi{rota}` | KPI ao vivo |
| `GET /api/v1/domain/records{rota}?search=&status=&page=&per_page=` | tabela/cards |
| `POST`, `GET/PUT/DELETE …/{id}` | drawers |
| `GET …/export?format=csv\|xlsx\|pdf\|json\|xml\|sql\|txt…[&ids=]` | Exportar |

## Acessibilidade

- Ordem de foco: cabeçalho → abas → ações → conteúdo da aba; atalhos `1`–`5` trocam de aba.
- Cada visão tem um `h3` próprio (cabeçalho da visão) abaixo do `h1`.
- Ações destrutivas sempre em drawer de confirmação; nada é excluído por um clique só.

## Modelos

### HTML

1) PHP real — a página Records é um shim gerado + `domain_page.php`; a fonte curada decide colunas, busca e status:

```php
<?php
// resources/views/app/pages/client/academic/enrollment/re-enrollment.php
$pageRoute = '/academic/enrollment/re-enrollment';
$pageRail = 'client';
$pageModule = 'Secretariat';
$title = 'Espaço de Trabalho — Rematrícula';
$icon = 'fa-light fa-user-plus';
$breadcrumb = [['label' => 'Portal da Instituição', 'url' => url('/dashboard')],
               ['label' => 'Rematrícula', 'url' => url('/academic/enrollment/re-enrollment')]];
$this->layout('app::layouts/main', ['title' => $title, 'icon' => $icon, 'breadcrumb' => $breadcrumb,
    'pageHasHeader' => true, 'railKey' => 'client', 'subSidebarModule' => 'academic_secretariat']);
include base_path('resources/views/app/partials/chassis/domain_page.php');

// app/Config/page-domain-sources.php
'/academic/enrollment/re-enrollment' => [
    'source' => 'inst_secretariat_reenrollment', 'permission' => 'admin.academic.enrollments',
    'scope' => 'database', 'writable' => false,
    'statuses' => ['draft' => 'Draft', 'submitted' => 'Sent', 'pending_review' => 'Under review', 'approved' => 'Approved',
                   'rejected' => 'Rejected', 'confirmed' => 'Confirmed', 'cancelled' => 'Cancelled', 'expired' => 'Expired'],
    'columns' => ['request_type' => 'Type', 'student_name' => 'Student', 'course_name' => 'Course', 'class_name' => 'Class',
                  'shift' => 'Shift', 'period_name' => 'Period', 'created_at' => 'Requested at', 'status' => 'Status'],
    'search' => ['student_name', 'course_name', 'class_name'],
],
```

2) HTML gerado (preview `PageRecords`, rota da ficha `/academico/matriculas/registros`):

```html
<main id="main-viewport" class="bg-slate-50">
  <div id="model-page" class="space-y-3.5" aria-live="polite">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">…<h1 class="text-xl font-bold text-slate-900 tracking-tight">Matrículas</h1>…</div>
    <div class="bg-emerald-50/70 border border-emerald-200/80 rounded-2xl p-4 …">…Matrículas 2026 … 48 matrículas</div>
    <div id="model-tab-toolbar" class="commercial-tabs-layout …">
      <div id="chassis-segmented-tabs" role="tablist" class="ttsc-segmented-tabs …">
        <button id="tab-btn-kpi" role="tab" aria-selected="false" data-model-tab="kpi" class="tab-btn …">KPI <span class="tab-badge">4</span></button>
        <button id="tab-btn-table" role="tab" aria-selected="true" data-model-tab="table" class="tab-btn … is-active">Tabela de Dados <span class="tab-badge">48</span></button>
        <button id="tab-btn-cards" role="tab" aria-selected="false" data-model-tab="cards" class="tab-btn …">Cards / Grade <span class="tab-badge">48</span></button>
        <button id="tab-btn-analytics" role="tab" aria-selected="false" data-model-tab="analytics" class="tab-btn …">Analytics <span class="tab-badge">3</span></button>
      </div>
      <div class="commercial-tab-actions …">Filtrar · Exportar · <button data-model-drawer="model-drawer-new">Nova matrícula</button></div>
    </div>
    <div id="view-kpi" role="tabpanel" style="display: none;">…</div>
    <div id="view-table" role="tabpanel" style="display: block;">… <table id="model-table">…</table> … <div id="model-table-footer" class="ttsc-pagination-standard">…</div></div>
    <div id="view-cards" role="tabpanel" style="display: none;">…</div>
    <div id="view-analytics" role="tabpanel" style="display: none;"><div id="model-analytics-panels"></div></div>
  </div>
</main>
```

### CSS

Sem CSS de página: blocos de `assets/css` (ver [PageModel](../PageModel/README.md) para a ordem). No escuro, `TTSCModelKit.syncTheme()` (preview) ou o `ttsc.js` (produto) põem `html.dark`.

```css
/* Extensão por tokens: largura máxima de leitura para páginas Records em monitores largos */
@media (min-width: 1600px) { #model-page { max-width: 1440px; margin-inline: auto; } }
```

### JS

```js
// Página Records: ficha + abertura na tabela + recarga dos dados reais ao trocar de aba
TTSCModelKit.syncTheme();
const ROUTE = '/academico/matriculas/registros';
fetch('../../models/academico.json').then((r) => r.json()).then((sheet) => {
  TTSCModelKit.render(
    { portal: { label: 'Administração' }, module: { label: 'Acadêmico' }, page: { label: 'Matrículas', route: ROUTE } },
    sheet.pages[ROUTE], {}
  );
  TTSCModelKit.switchTab('table');
});

// Produção: a aba Tabela recarrega pelo endpoint da página
document.addEventListener('ttsc:domain-tab', async (ev) => {
  if (ev.detail.tab !== 'table') return;
  const res = await fetch('/api/v1/domain/records/academic/enrollment/re-enrollment?per_page=25', { credentials: 'same-origin' });
  const { totalRecords } = await res.json();
  document.querySelector('#tab-btn-table .tab-badge').textContent = totalRecords;
});
```

### SQL

```sql
-- KPI da página Records (contagem por status do vocabulário)
SELECT status, COUNT(*) AS total
  FROM inst_secretariat_reenrollment
 GROUP BY status;

-- Tabela: total filtrado + página
SELECT COUNT(*) FROM inst_secretariat_reenrollment
 WHERE student_name LIKE :q ESCAPE '\\' OR course_name LIKE :q ESCAPE '\\';

SELECT uuid, request_type, student_name, course_name, class_name, shift, period_name, created_at, status
  FROM inst_secretariat_reenrollment
 WHERE student_name LIKE :q ESCAPE '\\' OR course_name LIKE :q ESCAPE '\\'
 ORDER BY created_at DESC
 LIMIT :limit OFFSET :offset;

-- Analytics: solicitações por curso
SELECT course_name, COUNT(*) AS total
  FROM inst_secretariat_reenrollment
 GROUP BY course_name
 ORDER BY total DESC
 LIMIT 8;
```

`PortalDomainDataService::getDataForRoute('/academic/enrollment/re-enrollment', $tenant)` executa esse conjunto e entrega `records`, `kpiCards`, `statusCounts` e `distribution` ao `domain_page.php`.

## Faça / Não faça

- **Faça:** Records quando em dúvida; troque para outro arquétipo só pela regra.
- **Faça:** declarar a fonte da página em `page-domain-sources.php` (colunas, busca, status) — é ela que impede a página de listar a tabela errada do módulo.
- **Não faça:** "Novo" em fonte de consulta (`writable => false`).
- **Não faça:** Kanban em Records sem etapas reais.
