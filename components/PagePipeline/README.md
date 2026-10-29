# PagePipeline

Arquétipo de página para itens que andam por etapas reais: abre no Quadro Kanban, com KPI, Tabela, Cards e Analytics nas outras abas; mover um cartão grava o novo status.

## Quando usar

- Solicitações, processos e funis com etapas que existem no banco (vocabulário `ref_enum_*` do `status`): rematrícula, diplomas, recuperação, aprovações de espaço.
- Só quando `StandardPageRegistry::tabsFor($rota)['kanban']` é `true` ou a fonte curada tem ≥ 2 status. Etapas "decorativas" ou listas estáticas são Records.

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
PageHeader · ContextBanner (ponto âmbar = itens em análise/indeferidos)
[KPI] [Tabela] [Cards] [Quadro Kanban 5] [Analytics]            [Filtrar] [Exportar ▾] [+ Nova matrícula]
#view-kanban  ▦ Funil de matrícula (48)                       Valor no quadro
              Etapas: [Pré-matrícula 6][Documentação 7][Em análise 8][Matriculado 26][Indeferido 1]
              ┌Pré-matrícula┐┌Documentação┐┌Em análise┐┌Matriculado┐┌Indeferido┐
```

| Bloco | README |
|---|---|
| Quadro | [KanbanBoard](../KanbanBoard/README.md) |
| Demais abas | [KpiView](../KpiView/README.md) · [RecordsTable](../RecordsTable/README.md) · [RecordCards](../RecordCards/README.md) · [AnalyticsPanels](../AnalyticsPanels/README.md) |
| Criação a partir do "+ Adicionar" | [RecordDrawers](../RecordDrawers/README.md) |

## Variantes

| Variante | Como | Exemplo real |
|---|---|---|
| Gravável | fonte gravável → `readOnly:false`, `skb:move` → `POST …/status` | `/developer/commercial/pipeline` (`crm_deals`, `stage_uuid` → `crm_pipeline_stages`) |
| Consulta | `writable => false` → `readOnly:true` (quadro só leitura; status muda pelo fluxo do sistema) | `/academic/secretariat/diplomas` (`inst_secretariat_diplomas`), `/academic/enrollment/re-enrollment` |
| Nova etapa | `allowNewStage` só no rail developer (`POST …/statuses`) | vocabulário compartilhado |

## API

| Ficha | Valor em Pipeline |
|---|---|
| `views` | `["kpi","table","cards","kanban","analytics"]` |
| `defaultView` | `"kanban"` |
| `stages[]` + `stageField` | colunas (sem `stages`, a aba some) |
| `kanbanTitle`, `kanbanDesc`, `kanbanValue`, `kanbanDate` | cabeçalho e cartões |
| `endpoints.move` | gravação do movimento |

| JS | Efeito |
|---|---|
| `TTSCModelKit.switchTab('kanban')` | monta `SoftCloud.KanbanBoard` na 1ª abertura |
| `SoftCloud.KanbanBoard.mount(el, {readOnly, allowNewStage, allowColumnReorder, provider, …})` | quadro |
| eventos `skb:move`, `skb:add`, `skb:addcol`, `skb:reorder` | gravação, criação via drawer, nova etapa, ordem |

| Endpoint | Uso |
|---|---|
| `POST /api/v1/domain/records{rota}/status` `{id, status}` | mover cartão (422 se status fora de `known_statuses`) |
| `POST /api/v1/domain/records{rota}/statuses` `{label}` | nova etapa (developer) |
| `GET /api/v1/domain/records{rota}?status=<etapa>&page=&per_page=` | página de uma coluna |
| `POST /api/v1/domain/records{rota}` | "+ Adicionar" (pelo drawer) |

## Acessibilidade

- Mover sem mouse: foco no cartão + **Alt + ← / →**.
- O quadro não é o único caminho: a mesma mudança de status existe na barra de lote da tabela ("Mudar status").
- Etapas sempre com nome visível; cor é complemento.

## Modelos

### HTML

1) PHP real — shim + `domain_page.php`; a aba Kanban nasce de `tabsFor()` e da fonte:

```php
<?php
// app/Support/StandardPageRegistry.php — regra curada que liga o Kanban
'academic/secretariat/diplomas' => ['kanban' => true, 'timeline' => true],

// resources/views/app/partials/chassis/domain_page.php
$curatedLifecycle = ($domainContract['curated'] ?? false) === true
    && count((array) ($domainContract['known_statuses'] ?? [])) >= 2;
$kanbanEnabled = (($tabsFlags['kanban'] ?? false) || $curatedLifecycle)
    && $statusKey !== null && $kanbanColumns !== [] && $records !== [];
// …
var board = window.SoftCloud.KanbanBoard.mount(host, {
  id: 'domain-kanban', title: <?= json_encode($title) ?>, columns: columns,
  allowNewStage: <?= $kbNewStage ? 'true' : 'false' ?>, currency: <?= json_encode($kbHasMoney ? 'R$' : '') ?>,
  strings: <?= json_encode($kbStrings) ?>, unit: 'registros', addLabel: 'Adicionar',
  allowColumnReorder: false, readOnly: !canWrite
});
```

2) HTML gerado (preview `PagePipeline`, rota da ficha `/academico/matriculas/funil`, aba Kanban ativa):

```html
<div id="model-tab-toolbar" class="commercial-tabs-layout …">
  <div id="chassis-segmented-tabs" role="tablist" class="ttsc-segmented-tabs …">
    <button id="tab-btn-kpi" role="tab" aria-selected="false" data-model-tab="kpi" class="tab-btn …">KPI <span class="tab-badge">4</span></button>
    <button id="tab-btn-kanban" role="tab" aria-selected="true" data-model-tab="kanban" class="tab-btn … is-active">Quadro Kanban <span class="tab-badge">5</span></button>
  </div>
  …
</div>
<div id="view-kanban" class="space-y-4" role="tabpanel" aria-labelledby="tab-btn-kanban" style="display: block;">
  <div id="model-kanban" class="skb is-reorderable">
    <div class="skb-head">…<b>Funil de matrícula</b><span class="skb-pill" data-total="">48 Matrículas</span>…</div>
    <div class="skb-stages">…<button type="button" class="skb-chip" data-goto-col="review" style="--c: #f59e0b"><i></i>Em análise<em>8</em></button>…</div>
    <div class="skb-board" data-board="" role="list">
      <div class="skb-col" role="listitem" data-id="pre_enrollment" style="--c: #64748b">…</div>
    </div>
  </div>
</div>
```

### CSS

`assets/css/ttsc.kanban.css` (tokens `--sc-*` em `:root` e `html.dark`) + blocos comuns. O quadro rola na horizontal dentro da página (`.skb-board`, `scroll-snap`), sem barra horizontal no `body`.

```css
/* Extensão por tokens: altura útil do quadro numa página Pipeline */
#view-kanban .skb-board { max-height: calc(100vh - 260px); }
#view-kanban .skb-col { background: color-mix(in srgb, var(--ttsc-canvas) 70%, transparent); }
```

### JS

```js
// Página Pipeline: abre no Kanban e grava o movimento
TTSCModelKit.syncTheme();
const ROUTE = '/academico/matriculas/funil';
fetch('../../models/academico.json').then((r) => r.json()).then((sheet) => {
  TTSCModelKit.render(
    { portal: { label: 'Administração' }, module: { label: 'Acadêmico' }, page: { label: 'Funil de Matrícula', route: ROUTE } },
    sheet.pages[ROUTE], {}
  );
  TTSCModelKit.switchTab('kanban');
});

// Produção (rota gravável): o quadro do domain_page.php já faz isto; com fonte própria:
document.getElementById('domain-kanban-board')?.addEventListener('skb:move', (ev) => {
  const { itemId, to } = ev.detail;
  fetch('/api/v1/domain/records/developer/commercial/pipeline/status', {
    method: 'POST', credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json', 'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content },
    body: JSON.stringify({ id: String(itemId), status: to }),
  }).then((r) => { if (!r.ok) throw new Error(r.status); })
    .catch(() => window.showToast?.('Não foi possível salvar o novo status.', 'error'));
});
```

### SQL

```sql
-- Colunas do funil de diplomas (fonte de /academic/secretariat/diplomas)
SELECT status, COUNT(*) AS total
  FROM inst_secretariat_diplomas
 GROUP BY status;

-- Cartões de uma coluna
SELECT uuid, code, student_name, subject, priority, unit_name, created_at
  FROM inst_secretariat_diplomas
 WHERE status = :status
 ORDER BY created_at
 LIMIT :limit OFFSET :offset;

-- Funil de rematrícula com soma da mensalidade por etapa (valor no quadro)
SELECT er.status, COUNT(*) AS itens, COALESCE(SUM(abr.monthly_tuition), 0) AS valor
  FROM enrollment_requests er
  LEFT JOIN academic_billing_rules abr ON abr.course_uuid = er.course_uuid AND abr.status = 'active'
 WHERE er.deleted_at IS NULL
 GROUP BY er.status;

-- Movimento (mesmo UPDATE do DomainCrudController::status) + histórico do funil
UPDATE enrollment_requests SET status = :to_status, reviewed_at = NOW()
 WHERE uuid = :uuid AND deleted_at IS NULL;

INSERT INTO enrollment_request_history (uuid, request_uuid, action, old_status, new_status, actor_uuid, created_at)
VALUES (UUID(), :uuid, 'status_change', :from_status, :to_status, :actor_uuid, NOW());
```

O `GROUP BY` vira `$kanbanColumns` (`count`) e as linhas, os cartões; o movimento roda numa transação e responde `{success, status}`.

## Faça / Não faça

- **Faça:** abrir em Kanban (`defaultView`) e manter a tabela como alternativa acessível.
- **Faça:** `readOnly` quando o status é escrito por outro fluxo (consulta).
- **Não faça:** Pipeline para entidades sem ciclo de vida — cursos, unidades, parâmetros e logs ficam em Records/History.
- **Não faça:** criar etapas no quadro fora do rail developer.
