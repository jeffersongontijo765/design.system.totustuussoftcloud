# PageHistory

Arquétipo de histórico e auditoria somente leitura: abre na Tabela de Dados, tem KPI e Analytics, exporta CSV/PDF e não oferece "Novo", editar nem excluir.

## Quando usar

- Registros que só se acumulam e não se editam pela página: diário de classe (chamadas), auditoria de notas, trilhas de login, histórico de notificações.
- Quando a pergunta do usuário é "o que aconteceu, quando e por quem".
- Se o usuário precisa corrigir ou criar registros, é Records; se precisa de gráficos antes da lista, é Report.

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
PageHeader "Histórico de Frequência" · ContextBanner "Diário de classe — somente leitura" (60 registros)
[KPI 2] [Tabela de Dados 60] [Analytics 2]                                 [Filtrar] [Exportar ▾ CSV · PDF]
#view-table  RecordsTable (abre aqui): Aluno · Turma · Registro · Status · Data/hora · Registrado por
             sem coluna de editar/excluir na produção; linha expansível com a seção "Registro"
#view-kpi    Presenças (% present+late) · Faltas sem justificativa
#view-analytics  Presença por turma (barras) · Registros por status (rosca)
```

| Bloco | README |
|---|---|
| Tabela | [RecordsTable](../RecordsTable/README.md) (`writable:false`) |
| KPI / gráficos | [KpiView](../KpiView/README.md) · [AnalyticsPanels](../AnalyticsPanels/README.md) |
| Detalhe | drawer View de [RecordDrawers](../RecordDrawers/README.md) + linha do tempo (`…/{id}/activity`) |

## Variantes

| Variante | Como | Exemplo real |
|---|---|---|
| Auditoria | ação no lugar do status (`statuses` = `created/updated/published/locked/voided…`) | `/academic/reports/audit` → `inst_reports_grade_audit` (`academic_grade_audit_logs` + `users`) |
| Diário / presença | status do vocabulário de `attendance` (`present`, `late`, `absent`, `justified`) | ficha `/academico/frequencia/historico` |
| Plataforma | `scope => 'platform'` (developer) | `/developer/identity/audit` → `developer_audit_users` |
| Com linha do tempo | `tabsFor()['timeline']` (207 URLs) — drawer com `activity` | `academic/secretariat/minutes`, `accounting/ledger` |

## API

| Ficha | Valor em History |
|---|---|
| `views` | `["kpi","table","analytics"]` |
| `defaultView` | `"table"` |
| `create` | `false` |
| `exports` | `["CSV","PDF"]` |
| `drawer.sections` | dados do evento (quem, quando, o quê) |

| Fonte (`page-domain-sources.php`) | Valor |
|---|---|
| `writable` | `false` — o `DomainCrudController` recusa `POST/PUT/DELETE` |
| `columns` | inclui `created_at`/data do evento e o autor |
| `search` | autor, entidade, motivo |

| Endpoint | Uso |
|---|---|
| `GET /api/v1/domain/records{rota}?search=&status=&page=&per_page=` | tabela (ordem `created_at DESC`) |
| `GET /api/v1/domain/records{rota}/{id}` · `…/{id}/activity` | detalhe e linha do tempo |
| `GET /api/v1/domain/records{rota}/export?format=csv\|pdf` | exportar |
| `GET /api/v1/kpi{rota}` | KPI |

## Acessibilidade

- Datas com hora em texto completo (`9 de abr. de 2026 14:05`); não só "há 2 horas".
- A ausência de ações de escrita é explícita: banner "Somente leitura" com ícone `fa-lock`.
- Tabela com ordenação por data acessível por teclado (`th[aria-sort]`).

## Modelos

### HTML

1) PHP real — fonte de auditoria acadêmica (somente leitura) e shim gerado:

```php
<?php
// app/Config/page-domain-sources.php
'/academic/reports/audit' => [
    'source'     => 'inst_reports_grade_audit',
    'permission' => 'admin.academic.view',
    'scope'      => 'database',
    'writable'   => false,
    'statuses'   => ['created' => 'Creation', 'updated' => 'Change', 'published' => 'Publication', 'locked' => 'Closing',
                     'voided' => 'Voiding', 'overridden' => 'Adjustment', 'exported' => 'Export'],
    'columns'    => ['created_at' => 'When', 'entity_type' => 'Record', 'actor_name' => 'User', 'reason' => 'Reason', 'status' => 'Action'],
    'search'     => ['entity_type', 'actor_name', 'reason'],
],

// resources/views/app/pages/client/academic/reports/audit.php
$pageRoute = '/academic/reports/audit';
// … $title, $icon, $breadcrumb, layout() …
include base_path('resources/views/app/partials/chassis/domain_page.php');
```

Com `writable => false`, o `domain_page.php` esconde "Novo registro", passa `'writable' => false` à tabela (sem editar/excluir/mudar status) e escreve "Somente leitura" no banner.

2) HTML gerado (preview `PageHistory`, aba Tabela):

```html
<div id="model-tab-toolbar" class="commercial-tabs-layout …">
  <div id="chassis-segmented-tabs" role="tablist" class="ttsc-segmented-tabs …">
    <button id="tab-btn-kpi" role="tab" aria-selected="false" data-model-tab="kpi" class="tab-btn …">KPI <span class="tab-badge">2</span></button>
    <button id="tab-btn-table" role="tab" aria-selected="true" data-model-tab="table" class="tab-btn … is-active">Tabela de Dados <span class="tab-badge">60</span></button>
    <button id="tab-btn-analytics" role="tab" aria-selected="false" data-model-tab="analytics" class="tab-btn …">Analytics <span class="tab-badge">2</span></button>
  </div>
  <div class="commercial-tab-actions flex flex-wrap items-center gap-2.5">
    <button type="button" data-model-drawer="model-drawer-filter" class="…">Filtrar</button>
    <div class="relative"><button type="button" data-model-toggle="model-dropdown-export" class="…">Exportar</button>
      <div id="model-dropdown-export" class="… hidden">… Exportar como CSV (.csv) · Documento PDF (.pdf)</div></div>
    <!-- sem "Novo registro" (create:false) -->
  </div>
</div>
<div id="view-table" class="space-y-4" role="tabpanel" aria-labelledby="tab-btn-table" style="display: block;">
  <header …><h3 class="text-sm font-bold text-slate-900">Registros</h3><span data-count-badge …>60 Registros</span></header>
  … <table id="model-table">… <th data-sort="lesson_date" aria-sort="none">…Data…</th> …</table>
</div>
```

### CSS

Blocos comuns; nenhuma regra própria. Para reforçar o caráter de leitura, a tabela pode dispensar a coluna de seleção:

```css
/* Extensão por tokens: histórico sem seleção em lote e com data em destaque */
.ttsc-history #model-table .sticky-col-left { display: none; }
.ttsc-history #model-table td.font-mono { color: var(--ttsc-text-2); }
```

### JS

```js
// Página History: abre na tabela; exportação só CSV/PDF
TTSCModelKit.syncTheme();
const ROUTE = '/academico/frequencia/historico';
fetch('../../models/academico.json').then((r) => r.json()).then((sheet) => {
  TTSCModelKit.render(
    { portal: { label: 'Administração' }, module: { label: 'Acadêmico' }, page: { label: 'Histórico de Frequência', route: ROUTE } },
    sheet.pages[ROUTE], {}
  );
  TTSCModelKit.switchTab('table');
});

// Produção: exportar o filtro atual da auditoria
function exportAudit(format) {
  const search = document.getElementById('domainSearchInput')?.value || '';
  const url = new URL('/api/v1/domain/records/academic/reports/audit/export', location.origin);
  url.searchParams.set('format', format);         // 'csv' ou 'pdf'
  if (search) url.searchParams.set('search', search);
  location.href = url.toString();
}
```

### SQL

```sql
-- Auditoria de notas (o que a view inst_reports_grade_audit expõe), página mais recente primeiro
SELECT a.uuid, a.created_at, a.entity_type, u.name AS actor_name, a.reason, a.action AS status
  FROM academic_grade_audit_logs a
  LEFT JOIN users u ON u.uuid = a.actor_uuid
 WHERE (u.name LIKE :q ESCAPE '\\' OR a.reason LIKE :q ESCAPE '\\' OR a.entity_type LIKE :q ESCAPE '\\')
 ORDER BY a.created_at DESC
 LIMIT :limit OFFSET :offset;

-- Diário de frequência (ficha /academico/frequencia/historico): chamadas com turma e responsável
SELECT a.uuid, a.lesson_date, a.status, cl.name AS turma, ru.name AS registrado_por, a.recorded_at
  FROM attendance a
  JOIN classes cl ON cl.uuid = a.class_uuid
  LEFT JOIN users ru ON ru.uuid = a.recorded_by
 WHERE a.lesson_date BETWEEN :from AND :to
 ORDER BY a.lesson_date DESC, a.recorded_at DESC
 LIMIT :limit OFFSET :offset;

-- KPI: presença (present + late) e faltas sem justificativa nos últimos 30 dias
SELECT ROUND(100 * SUM(status IN ('present', 'late')) / NULLIF(COUNT(*), 0), 1) AS presenca_pct,
       SUM(status = 'absent') AS faltas
  FROM attendance
 WHERE lesson_date >= CURRENT_DATE - INTERVAL 30 DAY;

-- Linha do tempo de um registro (audit_logs genérico)
SELECT action, user_id, changed_fields, created_at
  FROM audit_logs
 WHERE table_name = 'enrollments' AND record_id = :uuid
 ORDER BY created_at DESC
 LIMIT 50;
```

A primeira consulta é o que `DomainCrudController::index()` faz sobre a view; as demais alimentam KPI e drawer.

## Faça / Não faça

- **Faça:** `writable => false` na fonte e `create:false` na ficha — leitura garantida no servidor, não só escondida na tela.
- **Faça:** ordenar por data desc e mostrar o autor de cada evento.
- **Não faça:** Kanban em histórico (eventos não mudam de etapa).
- **Não faça:** apagar ou editar linhas de auditoria por nenhuma tela.
