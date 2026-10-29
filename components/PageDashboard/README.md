# PageDashboard

Arquétipo de home de módulo ou de portal: cabeçalho, banner, KPI com distribuição e lista de atenção, e Analytics — sem "Novo", sem tabela como protagonista.

## Quando usar

- Página de entrada de um módulo (`/academic`, `/commercial`, `/marketing`) ou de um portal (`/student/dashboard`, `/teacher/dashboard`, `/parents/dashboard`).
- Quando o objetivo é orientar: quanto existe, o que exige atenção, como está evoluindo — e mandar o usuário para a página certa.
- Não use para trabalhar sobre registros (Records/Pipeline) nem para relatórios detalhados (Report). Uma home rica em widgets heterogêneos usa os widgets (`WidgetsSmallHorizontal`, `WidgetsLarge`…).

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
PageHeader "Painel Acadêmico" (fa-gauge) · ContextBanner "Matrículas 2026"
[KPI 4] [Analytics 3]                                                 [Filtrar] [Exportar ▾]
#view-kpi (abre aqui)
  [Matrículas ativas] [Receita mensal] [Frequência média] [Indeferidas]
  ┌ Matrículas por curso — distribuição ───────────┐ ┌ [!] Indeferidas — atenção ┐
#view-analytics  barras por curso · rosca por status · linha mensal (wide)
```

| Bloco | README |
|---|---|
| Números | [KpiView](../KpiView/README.md) |
| Gráficos | [AnalyticsPanels](../AnalyticsPanels/README.md) |
| Itens de atenção → detalhe | [RecordDrawers](../RecordDrawers/README.md) (View) |

## Variantes

| Variante | Como | Exemplo real |
|---|---|---|
| Home de módulo | `domain_page.php` sobre uma fonte-resumo | `/academic` → `inst_academic_overview` (cursos com turmas e matrículas ativas) |
| Home de portal | página própria com widgets | `/student/dashboard`, `/teacher/dashboard` |
| Developer | `developer/dashboard.php` (o modelo de todo o chassi) | `/developer/dashboard` |

## API

| Ficha | Valor em Dashboard |
|---|---|
| `views` | `["kpi","analytics"]` |
| `defaultView` | `"kpi"` (padrão: primeira de `views`) |
| `create` | `false` |
| `kpis[]`, `breakdown.attention` | 4 cards + lista "exige atenção" |
| `analytics[]` | 2–3 gráficos |

| JS | Efeito |
|---|---|
| `TTSCModelKit.render(t, page, {})` | página; KPI visível |
| clique em item de atenção (`data-model-view`) | drawer View |
| `GET /api/v1/kpi{rota}` | atualização ao vivo dos cards (`[data-kpi-id]`) |

| Endpoint | Uso |
|---|---|
| `GET /api/v1/kpi/academic` | cards e `statusCounts` |
| `GET /api/v1/domain/records/academic?status=…` | lista de atenção |
| `GET /api/v1/domain/records/academic/export?format=pdf` | exportar resumo |

## Acessibilidade

- O resumo precisa funcionar só com texto: cada card tem rótulo e unidade; a lista de atenção diz o motivo (badge de status em texto).
- Links/botões da lista de atenção levam ao registro (teclado: `Tab` + `Enter`).
- Evite animação contínua além do ponto do banner.

## Modelos

### HTML

1) PHP real — home do módulo acadêmico:

```php
<?php
// resources/views/app/pages/client/academic/overview.php
$pageRoute = '/academic';
$pageRail = 'client';
$pageModule = 'Academic Administration';
// … $title, $icon, $breadcrumb, $this->layout('app::layouts/main', […]) …
include base_path('resources/views/app/partials/chassis/domain_page.php');

// app/Config/page-domain-sources.php
'/academic' => [
    'source' => 'inst_academic_overview', 'permission' => 'admin.academic.view', 'scope' => 'database', 'writable' => false,
    'statuses' => ['active' => 'Active', 'inactive' => 'Inactive'],
    'columns' => ['code' => 'Code', 'name' => 'Course', 'type' => 'Level', 'modality' => 'Modality', 'unit_name' => 'Unit',
                  'classes' => 'Classes', 'active_enrollments' => 'Active enrollments', 'status' => 'Status'],
    'search' => ['code', 'name'],
],
```

`StandardPageRegistry::tabsFor('/academic')` não liga Kanban (folha sem palavra de ciclo), e `writable => false` remove "Novo".

2) HTML gerado (preview `PageDashboard`, rota da ficha `/academico`):

```html
<div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
  …<i class="fa-light fa-gauge text-emerald-600 text-lg"></i>…<h1 class="text-xl font-bold text-slate-900 tracking-tight">Painel Acadêmico</h1>…
</div>
<div id="model-tab-toolbar" class="commercial-tabs-layout …">
  <div id="chassis-segmented-tabs" role="tablist" class="ttsc-segmented-tabs …">
    <button id="tab-btn-kpi" role="tab" aria-selected="true" data-model-tab="kpi" class="tab-btn … is-active">KPI <span class="tab-badge">4</span></button>
    <button id="tab-btn-analytics" role="tab" aria-selected="false" data-model-tab="analytics" class="tab-btn …">Analytics <span class="tab-badge">3</span></button>
  </div>
  <div class="commercial-tab-actions …">Filtrar · Exportar <!-- sem Novo --></div>
</div>
<div id="view-kpi" class="space-y-5" role="tabpanel" aria-labelledby="tab-btn-kpi">
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">… 4 cards …</div>
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">… Matrículas por curso · Indeferidas …</div>
</div>
<div id="view-analytics" class="space-y-5" role="tabpanel" aria-labelledby="tab-btn-analytics" style="display: none;">…</div>
```

### CSS

Blocos comuns. A grade de dashboards de portal usa `.portal-dashboard` (em `assets/css/ttsc.css`), que compacta os estados vazios quando há vários painéis vazios na mesma tela:

```css
/* Já no runtime: .portal-dashboard .ttsc-empty-state { min-height: 8rem; padding: 1.25rem 1rem; } */
/* Extensão por tokens: destaque discreto do card de atenção */
#view-kpi .lg\:grid-cols-3 > div:last-child { border-color: color-mix(in srgb, var(--ttsc-warning) 35%, var(--ttsc-border)); }
```

### JS

```js
// Dashboard do módulo: KPI ao vivo a cada 60 s enquanto a aba estiver visível
TTSCModelKit.syncTheme();
fetch('../../models/academico.json').then((r) => r.json()).then((sheet) => {
  TTSCModelKit.render({ portal: { label: 'Administração' }, module: { label: 'Acadêmico' }, page: { label: 'Painel', route: '/academico' } },
    sheet.pages['/academico'], {});
});

async function refreshKpi() {
  if (document.hidden) return;
  const res = await fetch('/api/v1/kpi/academic', { credentials: 'same-origin' });
  const body = await res.json();
  if (!body.available) return;
  body.kpiCards.forEach((c) => {
    const el = document.querySelector(`[data-kpi-id="${c.id}"] .text-2xl`);
    if (el) el.textContent = new Intl.NumberFormat('pt-BR').format(c.value);
  });
}
setInterval(refreshKpi, 60000);
```

### SQL

```sql
-- Resumo por curso (o que a view inst_academic_overview entrega)
SELECT c.code, c.name, c.type, c.modality,
       (SELECT COUNT(*) FROM classes k WHERE k.course_uuid = c.uuid AND k.deleted_at IS NULL)        AS turmas,
       (SELECT COUNT(*) FROM enrollments e WHERE e.course_uuid = c.uuid AND e.status = 'active'
                                             AND e.deleted_at IS NULL)                               AS matriculas_ativas,
       CASE WHEN c.is_active = 1 THEN 'active' ELSE 'inactive' END                                  AS status
  FROM courses c
 WHERE c.deleted_at IS NULL
 ORDER BY matriculas_ativas DESC;

-- Cards: ativos, receita mensal, frequência 30 dias, indeferidas
SELECT
  (SELECT COUNT(*) FROM enrollments WHERE deleted_at IS NULL AND status = 'active') AS ativas,
  (SELECT COALESCE(SUM(abr.monthly_tuition), 0)
     FROM enrollments e JOIN academic_billing_rules abr ON abr.course_uuid = e.course_uuid AND abr.status = 'active'
    WHERE e.deleted_at IS NULL AND e.status = 'active')                               AS receita_mensal,
  (SELECT ROUND(100 * SUM(status IN ('present', 'late')) / NULLIF(COUNT(*), 0), 1)
     FROM attendance WHERE lesson_date >= CURRENT_DATE - INTERVAL 30 DAY)             AS frequencia_pct,
  (SELECT COUNT(*) FROM enrollment_requests WHERE deleted_at IS NULL AND status = 'rejected') AS indeferidas;
```

O controlador entrega a primeira consulta como `records` (tabela de apoio/exportação) e a segunda como `kpiCards`.

## Faça / Não faça

- **Faça:** no máximo 4 cards e 3 gráficos; links para as páginas de trabalho.
- **Faça:** lista de atenção com no máximo 5 itens e "ver todos" levando à página Records/Pipeline filtrada.
- **Não faça:** "Novo" no dashboard; criação acontece na página da entidade.
- **Não faça:** tabela longa como conteúdo principal.
