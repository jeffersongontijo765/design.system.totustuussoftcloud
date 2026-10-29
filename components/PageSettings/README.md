# PageSettings

Arquétipo de configurações de módulo: cabeçalho, banner com o escopo das regras, abas segmentadas por grupo de parâmetros e o par Descartar / Salvar alterações no lugar de Filtrar / Exportar / Novo.

## Quando usar

- Parâmetros que valem para o módulo inteiro: ano letivo, abertura da rematrícula, vencimento e multa, frequência mínima, alertas a responsáveis.
- Valores únicos (chave → valor). Listas configuráveis com várias linhas — calendários, períodos, regras de cobrança por curso — são páginas Records dentro da área de configurações (ex.: `/academic/settings/calendar`).
- Corpo da página: [SettingsPanel](../SettingsPanel/README.md).

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
PageHeader "Configurações Acadêmicas" (fa-gear)
ContextBanner "Regras do ano letivo — parâmetros aplicados a matrículas, frequência e avaliação de todas as unidades"
[[id] Matrícula] [[cal] Frequência]                              [↺ Descartar] [[salvar] Salvar alterações]
#view-enrollment   section Período de matrícula (academic_periods) · section Financeiro (academic_billing_rules)
#view-attendance   section Limites (module_settings academic.*)
```

| Parte | README |
|---|---|
| Cabeçalho / banner | [PageHeader](../PageHeader/README.md) · [ContextBanner](../ContextBanner/README.md) (sem pill) |
| Abas de grupo + ações | [SegmentedTabs](../SegmentedTabs/README.md) |
| Seções e campos | [SettingsPanel](../SettingsPanel/README.md) |

## Variantes

| Variante | Como | Exemplo real |
|---|---|---|
| Parâmetros do módulo | `module_settings` (`module = 'academic'`) | `/academic/settings` → view `inst_settings_academic` |
| Lista configurável | Records sob `…/settings/*`; `tabsFor()` desliga Kanban/linha do tempo | `/academic/settings/calendar` (`inst_academic_calendars`; `PATCH /api/v1/academic/settings/calendar/data-table/{calendar}`) |
| Chave bloqueada | `status = 'locked'` — campo desabilitado com `fa-lock` | qualquer chave travada pela rede |

## API

| Ficha | Valor em Settings |
|---|---|
| `layout` | `"settings"` |
| `groups[] {id, label, icon, sections[]}` | abas e cartões |
| `banner` | sem `pill` |

| JS | Efeito |
|---|---|
| `TTSCModelKit.render(t, page, {})` com `layout:"settings"` | cabeçalho, banner, abas de grupo, Descartar/Salvar, painéis |
| `TTSCModelKit.switchTab('<grupo>')` | troca de grupo |
| `[data-model-api="reset"]` / `[data-model-api="save"]` | descartar / salvar |

| Endpoint | Uso |
|---|---|
| `GET /api/v1/domain/records/academic/settings` | leitura (consulta; `writable => false`) |
| `GET\|PATCH /api/v1/academic/settings/calendar/data-table[/{calendar}]` | calendários |
| `GET\|PUT /api/v1/supplies/settings` · `GET\|POST /api/v1/meetings/settings` | padrão chave-valor existente em outros módulos |

## Acessibilidade

- Rótulos ligados aos campos (`for`/`id`); dicas lidas com o campo (`aria-describedby`).
- "Salvar alterações" com estado de carregamento (`aria-busy`) e toast de resultado.
- Trocar de aba com alterações pendentes pede confirmação — não perca dados em silêncio.

## Modelos

### HTML

1) PHP real — fonte da página `/academic/settings` e o shim:

```php
<?php
// app/Config/page-domain-sources.php
'/academic/settings' => [
    'source'     => 'inst_settings_academic',            // module_settings WHERE module = 'academic' (segredos mascarados)
    'permission' => 'admin.academic.settings',
    'scope'      => 'database',
    'writable'   => false,
    'statuses'   => ['default' => 'Default', 'customized' => 'Customized', 'locked' => 'Blocked'],
    'columns'    => ['label' => 'Setting', 'setting_key' => 'Key', 'value_type' => 'Type',
                     'display_value' => 'Value', 'default_value' => 'Default', 'status' => 'Status'],
    'search'     => ['label', 'setting_key'],
],

// resources/views/app/pages/client/academic/settings/overview.php
$pageRoute = '/academic/settings';
$title = 'Espaço de Trabalho — Configurações Acadêmicas';
$icon = 'fa-light fa-gear';
// … layout() …
include base_path('resources/views/app/partials/chassis/domain_page.php');
```

Hoje a página real lista as chaves numa tabela de consulta; o arquétipo Settings (grupos + formulário) está no modelo (`layout: "settings"`) e é o alvo de migração — montado com `chassis/chassis.php` (`$chassis['tabs']` = grupos, `$panes` = seções).

2) HTML gerado (preview `PageSettings`, rota da ficha `/academico/configuracoes`):

```html
<div id="model-tab-toolbar" class="commercial-tabs-layout flex flex-col lg:flex-row lg:items-center justify-between gap-3 select-none">
  <div id="chassis-segmented-tabs" role="tablist" class="ttsc-segmented-tabs …">
    <button id="tab-btn-enrollment" type="button" role="tab" aria-selected="true" aria-controls="view-enrollment" data-model-tab="enrollment" class="tab-btn … is-active"><i class="fa-light fa-id-card text-xs"></i><span>Matrícula</span></button>
    <button id="tab-btn-attendance" type="button" role="tab" aria-selected="false" aria-controls="view-attendance" data-model-tab="attendance" class="tab-btn …"><i class="fa-light fa-calendar-check text-xs"></i><span>Frequência</span></button>
  </div>
  <div class="commercial-tab-actions flex flex-wrap items-center gap-2.5">
    <button type="button" data-model-api="reset" class="inline-flex items-center space-x-1.5 px-3 py-2 bg-white border border-slate-200 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-50 transition shadow-sm cursor-pointer"><i class="fa-light fa-rotate-left text-emerald-600 text-xs"></i><span>Descartar</span></button>
    <button type="button" data-model-api="save" class="inline-flex items-center space-x-1.5 px-3.5 py-2 bg-emerald-500 hover:bg-emerald-600 active:bg-emerald-700 text-white rounded-xl text-xs font-semibold shadow-sm transition cursor-pointer"><i class="fa-light fa-floppy-disk text-xs"></i><span>Salvar alterações</span></button>
  </div>
</div>
<div id="view-enrollment" class="space-y-4" role="tabpanel" aria-labelledby="tab-btn-enrollment">
  <section class="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs space-y-4">…Período de matrícula…</section>
  <section class="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs space-y-4">…Financeiro…</section>
</div>
<div id="view-attendance" class="space-y-4" role="tabpanel" aria-labelledby="tab-btn-attendance" style="display:none">…Limites…</div>
```

### CSS

Blocos comuns; ver [SettingsPanel](../SettingsPanel/README.md). Barra de ações fixa no rodapé em telas pequenas:

```css
@media (max-width: 1023px) {
  .ttsc-settings .commercial-tab-actions {
    position: sticky; bottom: 0; z-index: var(--ttsc-z-floating);
    background: var(--ttsc-surface); border-top: 1px solid var(--ttsc-border); padding: var(--ttsc-space-2) 0;
  }
}
```

### JS

```js
// Página Settings: confirma troca de grupo com alterações pendentes
TTSCModelKit.syncTheme();
const ROUTE = '/academico/configuracoes';
let dirty = false;
fetch('../../models/academico.json').then((r) => r.json()).then((sheet) => {
  TTSCModelKit.render({ portal: { label: 'Administração' }, module: { label: 'Acadêmico' }, page: { label: 'Configurações', route: ROUTE } },
    sheet.pages[ROUTE], {});
  document.getElementById('model-page').addEventListener('input', () => { dirty = true; });
});
document.addEventListener('click', (ev) => {
  const tab = ev.target.closest('[data-model-tab]');
  if (tab && dirty && !confirm('Há alterações não salvas neste grupo. Trocar mesmo assim?')) ev.stopImmediatePropagation();
}, true);
window.addEventListener('beforeunload', (ev) => { if (dirty) { ev.preventDefault(); ev.returnValue = ''; } });
```

### SQL

```sql
-- Grupo "Frequência" e demais chaves do módulo (o que inst_settings_academic expõe)
SELECT setting_key, label, value_type,
       CASE WHEN is_sensitive = 1 THEN '********' ELSE display_value END AS display_value,
       default_value, status
  FROM module_settings
 WHERE module = 'academic' AND deleted_at IS NULL
 ORDER BY setting_key;

-- Grupo "Matrícula" › Período: ano letivo corrente e o próximo
SELECT uuid, name, year, start_date, end_date, status, is_current
  FROM academic_periods
 WHERE deleted_at IS NULL AND year >= :year
 ORDER BY year, start_date;

-- Grupo "Matrícula" › Financeiro: vencimento e multa configurados por curso
SELECT c.name AS curso, abr.due_day, abr.monthly_tuition, abr.payment_method, abr.auto_invoice
  FROM academic_billing_rules abr
  JOIN courses c ON c.uuid = abr.course_uuid AND c.deleted_at IS NULL
 WHERE abr.status = 'active'
 ORDER BY c.name;

-- Salvar uma chave (não toca em chaves travadas)
UPDATE module_settings
   SET display_value = :value, status = 'customized', updated_by = :actor_uuid, updated_at = NOW()
 WHERE module = 'academic' AND setting_key = :setting_key AND status <> 'locked' AND deleted_at IS NULL;
```

## Faça / Não faça

- **Faça:** agrupar por assunto do usuário (Matrícula, Frequência, Avaliação), não por tabela.
- **Faça:** escrever o escopo das regras no banner ("todas as unidades").
- **Não faça:** KPI, Kanban ou Exportar numa página de configurações.
- **Não faça:** gravar automaticamente a cada campo; um "Salvar alterações" com confirmação.
