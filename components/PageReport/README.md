# PageReport

Arquétipo de relatório: abre direto em Analytics (gráficos primeiro), com KPI e Tabela de Dados como apoio, exportação e nenhuma ação de criação.

## Quando usar

- Relatórios, indicadores e painéis de análise de um módulo: matrículas por curso e mês, indicadores por período, boletins, relatórios de eventos.
- Quando a pergunta é "quanto / como evoluiu" e a lista é secundária.
- Se o usuário precisa agir sobre registros (criar, mudar status), use Records ou Pipeline; se é a home do módulo, Dashboard.

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
PageHeader "Relatório de Matrículas" · ContextBanner
[KPI 4] [Tabela de Dados 48] [Analytics 3]                                [Filtrar] [Exportar ▾]
#view-analytics (abre aqui)
  ┌ Matrículas por curso (barras) ┐ ┌ Matrículas por status (rosca) ┐
  ┌ Novas matrículas por mês (linha, wide) ────────────────────────────┐
#view-kpi   cards + distribuição
#view-table registros que compõem os gráficos (para conferência e exportação)
```

| Bloco | README |
|---|---|
| Gráficos | [AnalyticsPanels](../AnalyticsPanels/README.md) |
| Números | [KpiView](../KpiView/README.md) |
| Base | [RecordsTable](../RecordsTable/README.md) |

## Variantes

| Variante | Como | Exemplo real |
|---|---|---|
| Relatório de entidade | `analytics[]` sobre os registros da página | ficha `/academico/relatorios/matriculas` |
| Indicadores por período | fonte curada agregada (uma linha por período) | `/academic/reports` e `/academic/indicators` → `inst_academic_indicators` |
| Agendado | lista de relatórios programados (é Records) | `/academic/reports/scheduled` |
| Domínio sem `analytics[]` | o `domain_page.php` desenha "Registros criados por mês" + "Registros por status" | qualquer rota com contrato |

## API

| Ficha | Valor em Report |
|---|---|
| `views` | `["kpi","table","analytics"]` |
| `defaultView` | `"analytics"` |
| `create` | `false` |
| `analytics[]` | `by`, `measure`, `type`, `wide`, `months` |

| JS | Efeito |
|---|---|
| `TTSCModelKit.switchTab('analytics')` → `mountAnalytics(page, rows)` | cria um `TTSCAnalytics.create(host, spec)` por item de `analytics[]` |
| `panel.refresh()` | refaz um painel (após mudar o período) |

| Endpoint | Uso |
|---|---|
| `GET /api/v1/kpi{rota}` | `totalRecords`, `statusCounts`, `kpiCards` |
| `GET /api/v1/domain/records{rota}` | linhas de apoio da tabela |
| `GET /api/v1/domain/records{rota}/export?format=pdf\|xlsx\|csv` | exportação do relatório |

## Acessibilidade

- Todo gráfico tem total e legenda em texto, e a mesma informação está na tabela da página.
- Os filtros de cada gráfico ficam no drawer "Filtros" do painel (foco preso, `Esc`).
- Títulos de gráfico como `h3`, na ordem de leitura.

## Modelos

### HTML

1) PHP real — fonte de indicadores e shim:

```php
<?php
// app/Config/page-domain-sources.php
'/academic/reports' => [
    'source'     => 'inst_academic_indicators',
    'permission' => 'admin.academic.reports',
    'scope'      => 'database',
    'writable'   => false,
    'statuses'   => ['planned' => 'Planned', 'active' => 'In progress', 'closed' => 'Closed', 'cancelled' => 'Cancelled'],
    'columns'    => ['code' => 'Code', 'name' => 'Period', 'year' => 'Year', 'classes' => 'Classes',
                     'enrollments' => 'Enrollments', 'active' => 'Active', 'lost' => 'Cancelled/transferred', 'status' => 'Status'],
    'search'     => ['code', 'name'],
],

// resources/views/app/pages/client/academic/reports/overview.php → $pageRoute = '/academic/reports'; … domain_page.php
```

O `domain_page.php` não tem "abrir em Analytics" por rota; para o arquétipo Report a página chama `switchDomainTab('analytics')` no carregamento (ou usa a ficha com `defaultView: "analytics"`).

2) HTML gerado (preview `PageReport`, aba Analytics):

```html
<div id="chassis-segmented-tabs" role="tablist" class="ttsc-segmented-tabs …">
  <button id="tab-btn-kpi" role="tab" aria-selected="false" data-model-tab="kpi" class="tab-btn …">KPI <span class="tab-badge">4</span></button>
  <button id="tab-btn-table" role="tab" aria-selected="false" data-model-tab="table" class="tab-btn …">Tabela de Dados <span class="tab-badge">48</span></button>
  <button id="tab-btn-analytics" role="tab" aria-selected="true" data-model-tab="analytics" class="tab-btn … is-active">Analytics <span class="tab-badge">3</span></button>
</div>
<div id="view-analytics" class="space-y-5" role="tabpanel" aria-labelledby="tab-btn-analytics" style="display: block;">
  <div id="model-analytics-panels" class="ttsc-analytics-grid">
    <article class="ttsc-analytics-card" data-analytics-id="model-0">…Matrículas por curso…</article>
    <article class="ttsc-analytics-card" data-analytics-id="model-1">…Matrículas por status…</article>
    <article class="ttsc-analytics-card is-wide" data-analytics-id="model-2">…Novas matrículas por mês…</article>
  </div>
</div>
```

### CSS

`assets/css/ttsc.analytics-panels.css` + blocos comuns. Para impressão do relatório:

```css
/* Extensão por tokens: impressão do relatório (sem barra de ações, gráficos inteiros) */
@media print {
  #model-tab-toolbar, [data-model-refresh] { display: none !important; }
  .ttsc-analytics-card { break-inside: avoid; border-color: var(--ttsc-border); }
}
```

### JS

```js
// Página Report: abre em Analytics; na produção, troca a aba ao carregar
TTSCModelKit.syncTheme();
const ROUTE = '/academico/relatorios/matriculas';
fetch('../../models/academico.json').then((r) => r.json()).then((sheet) => {
  TTSCModelKit.render(
    { portal: { label: 'Administração' }, module: { label: 'Acadêmico' }, page: { label: 'Relatório de Matrículas', route: ROUTE } },
    sheet.pages[ROUTE], {}
  );
  TTSCModelKit.switchTab('analytics');
});

// Produção (domain_page.php): Report abre nos gráficos
document.addEventListener('DOMContentLoaded', () => window.switchDomainTab?.('analytics'));
```

### SQL

```sql
-- Indicadores por período (o que inst_academic_indicators entrega)
SELECT ap.code, ap.name, ap.year, ap.status,
       COUNT(DISTINCT cl.uuid)                                       AS turmas,
       COUNT(DISTINCT e.uuid)                                        AS matriculas,
       COUNT(DISTINCT CASE WHEN e.status = 'active' THEN e.uuid END) AS ativas,
       COUNT(DISTINCT CASE WHEN e.status IN ('cancelled', 'transferred') THEN e.uuid END) AS perdidas
  FROM academic_periods ap
  LEFT JOIN classes cl     ON cl.period_uuid = ap.uuid AND cl.deleted_at IS NULL
  LEFT JOIN enrollments e  ON e.period_uuid = ap.uuid AND e.deleted_at IS NULL
 WHERE ap.deleted_at IS NULL
 GROUP BY ap.uuid, ap.code, ap.name, ap.year, ap.status
 ORDER BY ap.year DESC, ap.start_date DESC;

-- Gráfico "Novas matrículas por mês" do ano selecionado
SELECT MONTH(enrollment_date) AS mes, COUNT(*) AS total
  FROM enrollments
 WHERE deleted_at IS NULL AND YEAR(enrollment_date) = :year
 GROUP BY MONTH(enrollment_date)
 ORDER BY mes;

-- Gráfico "Matrículas por curso" com taxa de evasão
SELECT c.name,
       COUNT(*) AS total,
       ROUND(100 * SUM(e.status IN ('cancelled', 'transferred')) / COUNT(*), 1) AS evasao_pct
  FROM enrollments e
  JOIN courses c ON c.uuid = e.course_uuid
 WHERE e.deleted_at IS NULL
 GROUP BY c.uuid, c.name
 ORDER BY total DESC;
```

O PHP completa os meses sem dado com 0 só depois de confirmar que a fonte tem data (sem data, o painel mostra "A origem não registra data de criação").

## Faça / Não faça

- **Faça:** gráficos primeiro (`defaultView: "analytics"`) e a tabela como base conferível.
- **Faça:** exportação em PDF/XLSX para relatórios.
- **Não faça:** "Novo" em relatório; nem Kanban (`tabsFor()` nunca liga Kanban em `reports`/`analytics`).
- **Não faça:** gráfico com dado inventado quando a fonte não tem a coluna — use o estado vazio.
