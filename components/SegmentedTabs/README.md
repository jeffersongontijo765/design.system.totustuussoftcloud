# SegmentedTabs

Barra de abas segmentadas do chassi (`#chassis-segmented-tabs.ttsc-segmented-tabs`) com contador por aba, à esquerda, e as ações da página — Filtrar, Exportar (menu de formatos) e Novo — à direita.

## Quando usar

- Em páginas de módulo que mostram o mesmo conjunto de registros em visões diferentes: KPI, Tabela de Dados, Cards / Grade, Quadro Kanban, Analytics.
- Em páginas de configuração, as abas são os **grupos** de parâmetros ([SettingsPanel](../SettingsPanel/README.md)), e as ações viram Descartar / Salvar alterações.
- Não use para navegar entre páginas diferentes (isso é a sub-sidebar) nem para passos de formulário (use [Stepper](../Stepper/README.md)). Abas dentro de um card ou drawer: [Tabs](../Tabs/README.md).

## Anatomia

```
┌ #chassis-segmented-tabs ─────────────────────────────────────┐    [Filtrar] [Exportar ▾] [+ Nova matrícula]
│ [▣ KPI 4] [≣ Tabela de Dados 48] [▦ Cards / Grade 48] [Mais ▾]│              └ menu .w-72: CSV / XLSX / PDF …
└──────────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Linha | `div.commercial-tabs-layout` (`#domain-tab-toolbar` / `#model-tab-toolbar`) | sim |
| Grupo | `div#chassis-segmented-tabs.ttsc-segmented-tabs[role=tablist]` | sim |
| Aba | `button.tab-btn#tab-btn-<id>[role=tab][aria-controls=view-<id>]`; ativa = `.is-active.bg-white.shadow-sm.font-semibold` | sim |
| Contador | `span.tab-badge` (na aba Tabela: `bg-emerald-100 text-emerald-800`) | não |
| Painel | `div#view-<id>[role=tabpanel]` alternado por `style.display` | sim |
| Overflow | `button.tab-overflow-btn` "Mais" + menu, criado por `ttsc.tabs-overflow.js` | automático |
| Ações | `div.commercial-tab-actions` | sim |
| Exportar | botão + `div#domain-export-menu` / `#dropdown-export` (`absolute right-0 w-72 hidden`) | se houver endpoint |
| Novo | botão primário que abre o drawer de criação | se gravável |

## Variantes

| Variante | Quando | Ações |
|---|---|---|
| Records (padrão) | lista de entidade | Filtrar · Exportar · Novo |
| Somente leitura | `writable => false` em `page-domain-sources.php` ou ficha `create:false` | Filtrar · Exportar |
| Settings | ficha `layout:"settings"` | Descartar · Salvar alterações |
| Kanban condicional | `StandardPageRegistry::tabsFor($route)['kanban']` ou fonte curada com ≥ 2 status | aba "Quadro Kanban" com contador = nº de etapas |

## API

**Abas e contadores (PHP, `chassis/domain_page.php`)**

| Aba | `id` | Ícone | Contador |
|---|---|---|---|
| KPI | `kpi` | `fa-chart-simple` | 4 |
| Tabela de Dados | `table` | `fa-table-list` (verde) | `$totalRecords` |
| Cartões / Grade | `cards` | `fa-border-all` | `$totalRecords` |
| Quadro Kanban | `kanban` | `fa-bars-progress` | `count($kanbanColumns)` ou nenhum |
| Analytics | `analytics` | `fa-chart-line` | ano corrente |

`chassis/chassis.php` aceita `$chassis['tabs'] = [['id','label','icon','badge'], …]`, `$chassis['active']`, `$chassis['filter']`, `$chassis['create'] = ['label'=>…]`, `$chassis['export'] = ['filename'=>…]`.

**Ficha**: `views` (lista e ordem das abas), `defaultView` (aba inicial), `tabLabels` (rótulos), `create:false` (sem Novo), `exports` (subconjunto de `CSV`, `XLSX`, `PDF`, `JSON` no kit), `entity.newLabel`.

**JS**

| API | Origem | Efeito |
|---|---|---|
| `switchDomainTab(id)` | `domain_page.php` | mostra `#view-<id>`, troca classes, chama `recalculateTabs()` e dispara `ttsc:domain-tab` `{detail:{tab}}` |
| `switchCommercialTab(id)` / `switchChassisTab(id)` | `chassis.php` | mesmo comportamento, sem evento |
| `TTSCModelKit.switchTab(id)` | kit | idem + monta Kanban/Analytics na primeira abertura |
| `group.recalculateTabs()` | `ttsc.tabs-overflow.js` | recalcula o botão "Mais" (chamar após mudar abas ou largura) |
| `window.setupAllResponsiveTabs()` | `ttsc.tabs-overflow.js` | inicializa todo `.ttsc-segmented-tabs` / `.segmented-tab-group` (também via `MutationObserver`) |
| teclas `1`…`5` | `domain_page.php` | trocam de aba fora de campos de texto |

| Atributo `data-*` | Efeito |
|---|---|
| `data-action="domain-toggle-export"` / `domain-export` + `data-format` | abre o menu / baixa `…/export?format=` |
| `data-action="domain-open-filter"` / `domain-open-create` | `openDrawer(CFG.drawers.filter / create)` |
| `data-model-tab`, `data-model-toggle`, `data-model-drawer`, `data-model-api` | equivalentes no kit |

**Endpoints usados pelas ações** (`routes/kpi-pages.generated.php` → `DomainCrudController`):

| Ação | Método e rota |
|---|---|
| Exportar | `GET /api/v1/domain/records{rota}/export?format=csv\|xlsx\|xls\|pdf\|docx\|html\|md\|tsv\|json\|xml\|sql\|txt…[&ids=uuid,uuid]` |
| Novo (salvar) | `POST /api/v1/domain/records{rota}` |
| Contadores | `GET /api/v1/domain/records{rota}?per_page=10` → `totalRecords`; `GET /api/v1/kpi{rota}` |

## Acessibilidade

- `role="tablist"`, `role="tab"` com `aria-selected` e `aria-controls`; painéis `role="tabpanel"` com `aria-labelledby` (kit). O chassi real ainda não emite `role`/`aria-selected` — ao portar, adicione.
- Atalhos `1`–`5` são ignorados dentro de `input/select/textarea`.
- O menu Exportar fecha no clique fora; adicione `aria-expanded` no gatilho quando portar para `ttscDropdown`.
- Contador da aba ativa em `emerald-800` sobre `emerald-100` = 7,9:1.

## Modelos

### HTML

1) PHP real (`chassis/domain_page.php`):

```php
<?php
$tabBadges = ['kpi' => 4, 'table' => $totalRecords, 'cards' => $totalRecords,
    'kanban' => $kanbanEnabled ? count($kanbanColumns) : null, 'analytics' => date('Y')];
?>
<div id="domain-tab-toolbar" class="commercial-tabs-layout flex flex-col lg:flex-row lg:items-center justify-between gap-3 select-none">
  <div id="chassis-segmented-tabs" class="ttsc-segmented-tabs inline-flex p-1 bg-slate-200/75 rounded-2xl border border-slate-200 text-xs font-medium text-slate-600 gap-1 overflow-x-visible relative">
    <?php foreach ($tabs as $tab): ?>
    <button id="tab-btn-<?= $e($tab['id']) ?>" type="button" onclick="switchDomainTab('<?= $e($tab['id']) ?>')" class="tab-btn …">
      <i class="fa-light <?= $e($tab['icon']) ?> text-xs"></i><span><?= $e($tab['label']) ?></span>
      <span class="tab-badge px-1.5 py-0.5 bg-slate-300 text-slate-700 rounded-full text-[10px]"><?= $e((string) $tabBadges[$tab['id']]) ?></span>
    </button>
    <?php endforeach; ?>
  </div>
  <div class="commercial-tab-actions flex flex-wrap items-center gap-2.5">
    <?php if ($canCrud): ?><button type="button" data-action="domain-open-filter" class="ttsc-btn ttsc-btn-outline ttsc-btn-sm">…Filtrar</button><?php endif; ?>
    <?php if ($hasDomainEndpoint): ?>… data-action="domain-toggle-export" … #domain-export-menu …<?php endif; ?>
    <?php if ($canWrite): ?><button type="button" data-action="domain-open-create" class="ttsc-btn ttsc-btn-primary ttsc-btn-sm">…Novo registro</button><?php endif; ?>
  </div>
</div>
```

2) HTML gerado (preview; 3 abas e 2 formatos mostrados):

```html
<div id="model-tab-toolbar" class="commercial-tabs-layout flex flex-col lg:flex-row lg:items-center justify-between gap-3 select-none">
  <div id="chassis-segmented-tabs" role="tablist" class="ttsc-segmented-tabs inline-flex p-1 bg-slate-200/75 rounded-2xl border border-slate-200 text-xs font-medium text-slate-600 gap-1 overflow-x-visible relative">
    <button id="tab-btn-kpi" type="button" role="tab" aria-selected="true" aria-controls="view-kpi" data-model-tab="kpi"
      class="tab-btn px-3.5 py-1.5 rounded-xl transition flex items-center space-x-1.5 bg-white text-slate-900 shadow-sm font-semibold is-active cursor-pointer">
      <i class="fa-light fa-chart-simple text-xs"></i><span>KPI</span>
      <span class="tab-badge px-1.5 py-0.5 bg-slate-300 text-slate-700 rounded-full text-[10px]">4</span>
    </button>
    <button id="tab-btn-table" type="button" role="tab" aria-selected="false" aria-controls="view-table" data-model-tab="table"
      class="tab-btn px-3.5 py-1.5 rounded-xl transition flex items-center space-x-1.5 text-slate-600 hover:text-slate-900 bg-transparent font-normal cursor-pointer">
      <i class="fa-light fa-table-list text-emerald-600 text-xs"></i><span>Tabela de Dados</span>
      <span class="tab-badge px-1.5 py-0.5 bg-emerald-100 text-emerald-800 font-bold rounded-full text-[10px]">48</span>
    </button>
  </div>
  <div class="commercial-tab-actions flex flex-wrap items-center gap-2.5">
    <button type="button" data-model-drawer="model-drawer-filter" class="inline-flex items-center space-x-1.5 px-3 py-2 bg-white border border-slate-200 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-50 transition shadow-sm cursor-pointer">
      <i class="fa-light fa-filter text-emerald-600 text-xs"></i><span>Filtrar</span>
    </button>
    <div class="relative">
      <button type="button" data-model-toggle="model-dropdown-export" class="inline-flex items-center space-x-1.5 px-3 py-2 bg-white border border-emerald-400/80 rounded-xl text-xs font-semibold text-emerald-700 hover:bg-emerald-50 transition shadow-sm cursor-pointer">
        <i class="fa-light fa-arrow-up-from-bracket text-emerald-600 text-xs"></i><span>Exportar</span><i class="fa-light fa-chevron-down text-[10px] text-emerald-600"></i>
      </button>
      <div id="model-dropdown-export" class="absolute right-0 mt-2 bg-white rounded-2xl shadow-2xl border border-slate-200 py-2 z-50 text-xs w-72">
        <div class="px-3.5 py-1.5 border-b border-slate-100 text-[10px] uppercase font-bold tracking-wider text-slate-400 flex items-center justify-between">
          <span>Exportar Matrículas</span><i class="fa-light fa-arrow-up-from-bracket text-emerald-600 text-[11px]"></i>
        </div>
        <div class="max-h-80 overflow-y-auto space-y-0.5 py-1">
          <button type="button" data-model-api="export CSV" class="w-full text-left px-3.5 py-2 hover:bg-emerald-50 text-slate-700 hover:text-emerald-800 flex items-center justify-between transition cursor-pointer">
            <span class="flex items-center space-x-2.5"><i class="fa-light fa-file-csv text-emerald-600 text-sm"></i><span class="font-medium">Exportar como CSV</span></span>
            <span class="text-[10px] text-slate-400 font-mono bg-slate-100 px-1.5 py-0.5 rounded">.csv</span>
          </button>
        </div>
      </div>
    </div>
    <button type="button" data-model-drawer="model-drawer-new" class="inline-flex items-center space-x-1.5 px-3.5 py-2 bg-emerald-500 hover:bg-emerald-600 active:bg-emerald-700 text-white rounded-xl text-xs font-semibold shadow-sm transition cursor-pointer">
      <i class="fa-light fa-plus text-xs"></i><span>Nova matrícula</span>
    </button>
  </div>
</div>
```

### CSS

- `assets/css/ttsc.commercial.model.css` — `.ttsc-segmented-tabs`, `.ttsc-segmented-tabs .tab-btn`, `.tab-btn.is-active`, contadores e as regras `html.dark` (grupo em `slate-800`, aba ativa em superfície escura, contador ativo verde translúcido).
- `assets/css/ttsc.commercial.css` — `.commercial-tabs-layout` e `.commercial-tab-actions` (quebra de linha < `lg`).
- `.tab-overflow-btn` e o menu "Mais" são estilizados inline pelo `ttsc.tabs-overflow.js`.

```css
/* Extensão por tokens: aba ativa e contador seguindo o acento do design system */
.ttsc-segmented-tabs .tab-btn.is-active { background: var(--ttsc-surface); color: var(--ttsc-text); box-shadow: var(--ttsc-shadow-xs); }
.ttsc-segmented-tabs .tab-btn:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.ttsc-segmented-tabs .tab-btn.is-active .tab-badge { background: var(--ttsc-accent-soft); color: var(--ttsc-accent-text); }
```

### JS

```js
// Troca de aba com carga preguiçosa da visão (padrão do domain_page.php)
document.addEventListener('ttsc:domain-tab', (ev) => {
  if (ev.detail.tab === 'table') loadPage(1);
});

const ROUTE = '/academic/enrollment/re-enrollment';
const API = '/api/v1/domain/records' + ROUTE;

async function loadPage(page) {
  const res = await fetch(`${API}?page=${page}&per_page=25`, { credentials: 'same-origin' });
  const body = await res.json();
  // contador da aba = total do servidor
  const badge = document.querySelector('#tab-btn-table .tab-badge');
  if (badge) badge.textContent = body.totalRecords;
  document.getElementById('chassis-segmented-tabs').recalculateTabs?.();
}

// Exportar com os selecionados (mesmo contrato do runExport() real)
function exportRecords(format, ids = []) {
  const url = new URL(API + '/export', location.origin);
  url.searchParams.set('format', format);           // csv, xlsx, pdf, json, xml, sql, txt…
  if (ids.length) url.searchParams.set('ids', ids.join(','));
  location.href = url.toString();
}
```

### SQL

Os contadores das abas vêm de duas leituras: o total (Tabela/Cards) e as etapas (Kanban).

```sql
-- Tabela / Cards: total de solicitações de rematrícula do período
-- (mesmo recorte da view inst_secretariat_reenrollment, fonte de /academic/enrollment/re-enrollment)
SELECT COUNT(*) AS total
  FROM enrollment_requests
 WHERE deleted_at IS NULL
   AND request_type IN ('rematricula_online', 'rematricula_manual', 'rematricula_auto')
   AND period_uuid  = :period_uuid;

-- Kanban: número de etapas com vocabulário ativo (ref_enum_* do status)
SELECT COUNT(*) AS etapas
  FROM ref_enum_enrollment_requests_status_21ca774d7caf
 WHERE is_active = 1 AND deleted_at IS NULL;
```

O PHP passa os dois números para `$tabBadges['table']`, `['cards']` e `['kanban']`.

## Faça / Não faça

- **Faça:** só as abas que a entidade justifica — Kanban apenas com etapas reais (`tabsFor()`), Analytics quando houver agregação.
- **Faça:** `recalculateTabs()` depois de mudar rótulos ou contadores.
- **Não faça:** duas ações primárias; "Novo" some quando a fonte é somente leitura.
- **Não faça:** esconder painéis com `hidden` — o chassi alterna `style.display`, e o overflow conta com isso.
