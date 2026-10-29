# DataTable

Visão “Tabela” do modelo aprovado de página (`/developer/dashboard`): cabeçalho da visão, barra de busca, barra de lote, tabela com seleção, linha expansível, ordenação por coluna, ações por linha e paginação com seletor de linhas por página; no app vem de `partials/chassis/table.php` incluído por `partials/chassis/domain_page.php`.

> Também listado em: **Base › Datatable**.

## Quando usar

- Listagens de registros de uma página de domínio: turmas, matrículas, rematrículas, mensalidades. É a aba **Tabela** das páginas geradas (`domain_page.php`) e do modelo (`TTSCModelKit`, ficha `/academico/turmas` em `models/academico.json`).
- Quando o usuário precisa buscar, ordenar, selecionar em lote e abrir o registro num drawer (ver/editar/excluir).
- Lista curta e fixa (≤ 10 linhas, sem busca) dentro de um card → [Table](../Table/README.md).
- Registros por etapa → [KanbanBoard](../KanbanBoard/README.md); números agregados → [KpiView](../KpiView/README.md); um registro → [RecordDrawers](../RecordDrawers/README.md).
- Página inteira de registros (abas + tabela + cards) → [PageRecords](../PageRecords/README.md).
- Telas legadas com jQuery DataTables → [DataTablesNet](../DataTablesNet/README.md). O ttscui `data-ttsc-datatable` não é carregado pelo layout do app.

## Anatomia

```
┌ header (view header) ─────────────────────────────────────────────────────────────┐
│ [tile 40×40] Turmas  (36 Turmas)                        [chip opcional: Total: N] │
└───────────────────────────────────────────────────────────────────────────────────┘
┌ .commercial-table-toolbar[role=search] ───────────────────────────────────────────┐
│ [🔍 input type=search]                         36 Turmas   [Limpar filtros] [status▾] │
└───────────────────────────────────────────────────────────────────────────────────┘
┌ barra de lote (só com seleção) ───────────────────────────────────────────────────┐
│ ✓ 1 SELECIONADOS                 [Exportar selecionados] [Excluir selecionados] [×] │
└───────────────────────────────────────────────────────────────────────────────────┘
┌ bg-white rounded-2xl ─────────────────────────────────────────────────────────────┐
│ ☐ │ ⌄ │ TURMA ⇅ │ CÓDIGO ⇅ │ STATUS ⇅ │ TURNO ⇅ │ ALUNOS ⇅ │ … │ AÇÕES (sticky) │
│ ☐ │ › │ 1ª série A / Ensino Médio │ TUR-1001 │ ● Matrículas abertas │ … │ 👁 ✎ 🗑 │
│   └ linha expandida (detalhe do registro)                                          │
│ .ttsc-pagination-standard: Exibindo 1-10 de 36 Turmas │ ‹ 1 2 3 4 › │ Por página [10▾] │
└───────────────────────────────────────────────────────────────────────────────────┘
```

| Parte | Modelo (`TTSCModelKit`) | App (`table.php`, prefixo `page-data`) | Obrigatório |
|---|---|---|---|
| Cabeçalho da visão | `header` com tile + `h3` + `[data-count-badge]` | `header` com tile + `h3` + contador | sim |
| Busca | `input#model-table-search` + `#model-table-count` + `#model-table-reset` | `input#page-dataSearchInput[data-action="filter-table"]` + `#page-dataFilterCount` + `#page-dataFilterReset` | sim |
| Filtro de status | drawer de filtros (`[data-filter-key]`) | `select.sb-select[data-action="filter-table"][data-filter="status"]` (realçado pelo TTSCSelect) | quando há status |
| Barra de lote | `#model-batch-bar` (`display:flex` com seleção) + `#model-selected-label` | `.sel-bar#page-dataSelBar` (`.is-visible`) + `#page-dataSelCount` | sim |
| Tabela | `table#model-table` dentro de `#model-table-scroll` | `table#page-dataDataTable[data-page-table]` dentro de `#page-dataTableScroll` | sim |
| Selecionar tudo | `input[data-model-master]` | `input#page-dataSelectAll` | sim |
| Coluna ordenável | `th[data-sort="campo"][aria-sort]` | `th[data-action="sort-column"][data-key="campo"]` | sim |
| Linha | `tr.model-row[data-row-id]` + `input.row-checkbox` | `tr[data-uuid][data-*]` + `input.row-checkbox[data-uuid]` | sim |
| Expandir | `i#chevron-<id>` + `tr#expand-<id>` | `td[data-expand-toggle]` + `<template data-row-detail>` | `expandable` |
| Ações | `[data-model-view]`, `[data-model-api="edit|delete"]` | `[data-action="view-record|edit-record|delete-record"][data-uuid]` | `actions` |
| Vazio | `#model-table-empty` | `.ttsc-empty-state.is-no-data` na `tbody` | sim |
| Paginação | `#model-table-footer.ttsc-pagination-standard` + `#model-table-pagination-buttons` | `.pagination.ttsc-pagination-standard` + `#page-dataPaginationPages` | sim |
| Linhas por página | `select#model-table-per-page` dentro de `.per-page[data-ttsc-page-size-control]` | `select#page-dataPerPage` dentro de `.per-page` | sim |

## Variantes

| Variante | Como | Uso |
|---|---|---|
| Somente leitura | `$table['writable'] = false` (fonte com `'writable' => false` em `page-domain-sources.php`) | ações só “Ver”; lote sem “Excluir”/“Mudar status” |
| Sem ações | `$table['actions'] = false` | relatórios |
| Linha expansível | `$table['expandable'] = true` (o `domain_page` liga quando há linhas) | detalhe sem abrir drawer |
| Lote de status | `$table['statusBatch'] = true` (2+ status conhecidos) | botão “Mudar status” |
| Filtro de status | `$table['filters'] = [['name' => 'status', 'label' => 'Todos os status', 'options' => […]]]` | páginas com vocabulário de status |

Visual: tudo em utilitários fixos do modelo (`bg-slate-50`, `text-slate-500`, `emerald-*`); `table.php` injeta um `<style>` por prefixo com a densidade (cabeçalho 11px maiúsculo, células `14px 16px`, coluna de ações `sticky`). O tema escuro vem das regras `html.dark` de `ttsc.commercial.model.css` / `ttsc.luxury-commercial.css`.

## Estados

| Estado | Como aparece |
|---|---|
| Sem registros | `ttsc-empty-state is-no-data` com botão “Nova …” (`data-action="open-create-drawer"`) quando a página permite criar |
| Busca sem resultado | modelo: `#model-table-empty` (“Nenhum registro em turmas para estes filtros”); “Limpar filtros” aparece |
| Ordenado | modelo: `aria-sort="ascending|descending"` no `th`; app: só a ordem muda (sem `aria-sort`) |
| Selecionado | barra de lote visível com a contagem; o “selecionar tudo” fica `indeterminate` no app |
| Linha aberta | modelo: `tr#expand-<id>` sem `hidden` e chevron `rotate-90`; app: `tr.is-expanded` |
| Linhas por página | o `<select>` vira o botão `.ttsc-page-size-trigger` + menu `.ttsc-page-size-menu[role=menu]` do `ttsc.pagination.js` |

## API

**Parâmetros de `table.php`** (`$table`):

| Chave | Padrão | Efeito |
|---|---|---|
| `prefix` | `'chassis'` (`domain_page` usa `'page-data'`) | prefixo de todos os ids |
| `columns` | `[]` | `[['label' => 'Turma', 'key' => 'name', 'class' => '']]` |
| `rows` | `[]` | `[['uuid' => …, 'cells' => ['<td…>', …], 'data' => ['status' => 'open', …]]]` (as `cells` já são HTML) |
| `search` | `null` (mostra) | `false` esconde; `['placeholder' => …, 'value' => …]` |
| `filters` | `[]` | selects de filtro (`name`, `label`, `options`, `selected`) |
| `actions` / `writable` | `true` / `true` | coluna de ações / editar-excluir e lote destrutivo |
| `expandable` / `statusBatch` | `false` / `false` | chevron por linha / “Mudar status” |
| `total`, `page`, `perPage` | `count(rows)`, `1`, `25` | números iniciais da paginação (opções 10, 25, 50, 100) |
| `viewIcon`, `viewTitle`, `viewDesc`, `recordsLabel`, `viewChipLabel`, `viewChipValue` | — | cabeçalho da visão |
| `empty`, `emptyTitle`, `emptyDescription` | “Nenhum registro encontrado.” | estado vazio |

**Ficha do modelo** (`models/academico.json` → `pages['/academico/turmas']`):

| Campo | Uso na tabela |
|---|---|
| `fields[]` (`key`, `label`, `type`, `table: false`) | colunas, na ordem; `title` vira a célula principal com `subField` embaixo; `code` vira chip mono; `status`/`enum` viram pílula com o `label` de `values`/`statuses`; `int`/`pct`/`money` em mono; `date` em pt-BR |
| `titleField`, `codeField`, `subField`, `statusField` | célula principal, chip, subtítulo, pílula |
| `entity.singular/plural/icon` | contador, rótulo da paginação, ícone |
| `statuses[]` (`id`, `label`, `tone`) | pílula e filtro |
| `endpoints.create/edit/delete/export` | rotas reais do CRUD (abaixo) |

**JS do modelo** (`window.TTSCModelKit`): `render(crumbs, ficha, {header, banner, tabs})`, `switchTab('table')`, `blocks.table(ficha, linhas)` (só a casca; a `tbody` é preenchida pelo motor interno de lista), `blocks.search`, `blocks.pager`, `fillView(ficha, linha)`, `generate(ficha, rota)`, `syncTheme()`. O `render` sempre gera linhas sintéticas com `generate()` a partir de `fields` e `count` (36 turmas no preview); ele não recebe linhas reais. A busca do modelo olha só campos de texto (`title`, `text`, `code`, `person`…), não enums, e a ordenação compara o valor bruto (enum ordena pelo `id`, não pelo rótulo).

**JS do app** (inline em `domain_page.php`, delegação no `document`): `data-action="filter-table"` (busca com debounce de 250 ms e filtro de status), `sort-column`, `select-all`, `clear-selection`, `batch-view`, `batch-action` (`data-op="export|status|delete"`), `view-record` / `edit-record` / `delete-record` (abrem os drawers via `window.openDrawer()`), `domain-export` (`data-format`), `domain-goto-page`, `change` em `#page-dataPerPage`. A ordenação compara `td[data-field][data-raw]` como número quando ambos são numéricos e senão com `localeCompare('pt-BR')`. Busca, ordenação e paginação são **no cliente**, sobre as linhas renderizadas.

**`ttsc.pagination.js`** (sem objeto global): realça `select` de linhas por página encontrado por `.pagination select`, `.per-page select`, `[data-ttsc-page-size-control] select` ou `id`/`name` com `perpage`, `per-page`, `pagesize`, `page-size`, `per_page`. Esconde o nativo (`.ttsc-page-size-native`, `aria-hidden`, `tabindex=-1`), cria `button.ttsc-page-size-trigger[aria-haspopup="menu"]` e `div.ttsc-page-size-menu[role="menu"]` no `<body>` com `button.ttsc-page-size-option[role="menuitemradio"][aria-checked]`; ao escolher, escreve `select.value` e dispara `change`. Teclado: ↓/Enter/Espaço abre, ↑/↓/Home/End navegam, `Esc` fecha e devolve o foco. O `TTSCSelect` ignora esses selects.

**Endpoints reais** (`routes/kpi-pages.generated.php` → `App\Http\Controllers\Api\V1\DomainCrudController`, um conjunto por rota de página):

| Verbo e rota | Ação |
|---|---|
| `GET /api/v1/domain/records{rota}?search=&status=&page=&per_page=` | lista: `{success, route, table, totalRecords, page, per_page, records}`; `per_page` entre 10 e 100 (padrão 25); ordena por `created_at DESC`; busca `LIKE` nas colunas de texto |
| `GET /api/v1/domain/records{rota}/{id}` | um registro (drawer Ver/Editar) |
| `POST /api/v1/domain/records{rota}` · `PUT …/{id}` · `DELETE …/{id}` | criar · editar · excluir |
| `POST /api/v1/domain/records{rota}/status` · `POST …/statuses` | mudar status (lote) · criar status |
| `GET /api/v1/domain/records{rota}/export?format=csv&ids=a,b` | exportação (formatos de `TableExporter::FORMATS`) |
| `GET /api/v1/domain/records{rota}/{id}/activity` · `…/chat` | linha do tempo e conversa do registro |

## Divergências conhecidas no render real (domain_page)

Encontradas ao renderizar `domain_page.php` para a fonte `inst_secretariat_reenrollment` (`/academic/enrollment/re-enrollment`) e **corrigidas** no commit `fix(views): domain page labels and formatting…` (branch `claude/design-system-extraction-srfpiz`). O render atual mostra o comportamento da coluna “Agora”.

| Defeito (antes) | Agora | Onde |
|---|---|---|
| Título da visão “Registros de inst_secretariat_reenrollment” vazava o nome da tabela | “Registros de Rematrícula”: `$recordsLabel` usa o título da página (sem “Workspace” e sem o prefixo “… — ”); o nome da tabela só aparece como `title` dos selos no portal do desenvolvedor | `domain_page.php` |
| Ícone de busca escondido atrás do fundo do campo | visível: `.tbl-search > input` com `z-index: 0` e o ícone/botão limpar com `z-index: 1` no `<style>` do prefixo (o mesmo vale para `.domain-cards-search-box` na visão de cards) | `table.php`, `domain_page.php` |
| Códigos de enum crus (“renewal”, “morning”) | “Renovação”, “Manhã”: `PortalDomainDataService::columnMeta($tabela)` devolve os tipos vivos e o vocabulário de cada coluna codificada (ENUM, FK para `ref_enum_*` ou o catálogo `enum-reference-catalog.php`, seguindo a coluna de origem quando a fonte é uma view); o rótulo passa por `PageDomainSources::label()`. O valor gravado continua em `td[data-raw]` | `PortalDomainDataService.php`, `domain_page.php` |
| Texto numérico formatado como decimal (“2026.2” → “2.026,20”) | `$fmt($valor, $coluna)` só formata número quando a coluna é numérica no esquema (`int`, `decimal`, `float`…) ou o valor já é `int`/`float`; texto fica como digitado | `domain_page.php` |

Ainda presente: o `select` de filtro de status (`.sb-select`) é realçado pelo `TTSCSelect` sem `data-category` nem `<label>` no seu `div`; o cabeçalho do painel sai da palavra `status` do id (“Status da Oportunidade”). Acrescente `data-category="Status"` ao portar.

## Acessibilidade

- Busca dentro de `role="search"`, com `aria-label` (app) ou `aria-controls` + `aria-describedby` apontando para o contador (modelo); o contador é `aria-live="polite"`.
- Checkboxes com `aria-label` (“Selecionar todos”, “Selecionar linha”); no app o mestre fica `indeterminate` em seleção parcial.
- Ordenação: o modelo escreve `aria-sort` no `th`; no app os `th` clicáveis não são focáveis nem anunciam a ordem. Ao portar, troque o conteúdo do `th` por um `<button>` e atualize `aria-sort`.
- Ações por linha só com ícone: os botões têm `title`; acrescente `aria-label` com o nome do registro (“Editar 1ª série A”).
- Paginação: `role="group" aria-label="Paginação"`, página atual com `aria-current="page"`; linhas por página com `aria-label="Linhas por página"` e menu navegável por setas.
- Contraste: cabeçalho `text-slate-500` sobre `bg-slate-50` (≥ 4,5:1), células `text-slate-700`; pílulas de status com texto da paleta 700 sobre fundo 50.

## Modelos

### HTML

**1. Como o app produz a tabela.** A view gerada só define a rota e inclui o chassi; `domain_page.php` monta `$table` e inclui `table.php` na aba Tabela:

```php
<?php
// resources/views/app/pages/<portal>/<modulo>/<pagina>.php (gerado por scripts/generate-domain-pages.php)
$pageRoute = '/academic/enrollment/re-enrollment';
$title = 'Rematrícula';
$icon  = 'fa-light fa-rotate-right';
$this->layout('app::layouts/main', ['title' => $title, 'icon' => $icon, 'pageHasHeader' => true]);
include base_path('resources/views/app/partials/chassis/domain_page.php');
```

```php
// trecho de domain_page.php
$table = [
    'prefix'       => 'page-data',
    'columns'      => $tblColumns,            // de $explorerColumns (columns da fonte)
    'rows'         => $tblRows,               // cells já formatadas ($statusPill, $fmt…)
    'total'        => count($tblRows),
    'perPage'      => 25,
    'actions'      => $canCrud,
    'writable'     => $canWrite,
    'viewIcon'     => $icon,
    'expandable'   => $tblRows !== [],
    'statusBatch'  => $statusKey !== null && count((array) ($domainContract['known_statuses'] ?? [])) >= 2,
    'recordsLabel' => $recordsLabel,
    'filters'      => [['name' => 'status', 'label' => 'Todos os status', 'options' => $statusFilterOptions]],
];
?>
<div id="view-table" class="space-y-5" style="display: none;">
  <?php include base_path('resources/views/app/partials/chassis/table.php'); ?>
</div>
```

A fonte de dados de cada rota fica em `app/Config/page-domain-sources.php`:

```php
'/academic/enrollment/re-enrollment' => [
    'source'     => 'inst_secretariat_reenrollment',
    'permission' => 'admin.academic.enrollments',
    'writable'   => false,
    'statuses'   => ['draft' => 'Draft', 'submitted' => 'Sent', 'approved' => 'Approved', /* … */],
    'columns'    => ['request_type' => 'Type', 'student_name' => 'Student', 'course_name' => 'Course',
                     'class_name' => 'Class', 'shift' => 'Shift', 'period_name' => 'Period',
                     'created_at' => 'Requested at', 'status' => 'Status'],
    'search'     => ['student_name', 'course_name', 'class_name'],
],
```

**2. HTML gerado** (capturado do preview, ficha `/academico/turmas`; uma linha, enxugado):

```html
<table id="model-table" class="w-full text-left border-collapse text-xs" style="min-width:980px;white-space:nowrap">
  <thead>
    <tr class="border-b border-slate-200 bg-slate-50 text-slate-500 font-semibold uppercase text-[11px] tracking-wider select-none">
      <th class="py-3.5 px-4 w-12 sticky-col-left bg-slate-50 border-r border-slate-100"><input type="checkbox" data-model-master class="rounded border-slate-300 text-emerald-600 focus:ring-emerald-500 cursor-pointer" aria-label="Selecionar todos"></th>
      <th class="py-3.5 px-2 w-8 bg-slate-50 text-center select-none text-slate-400"><i class="fa-light fa-chevron-down text-[10px]"></i></th>
      <th data-sort="name" aria-sort="none" class="py-3.5 px-4 cursor-pointer hover:text-emerald-700 select-none group"><div class="flex items-center space-x-1"><span>Turma</span><i class="fa-light fa-arrows-rotate text-[9px] text-slate-300 group-hover:text-emerald-600 ml-1"></i></div></th>
      <th data-sort="status" aria-sort="none" class="py-3.5 px-4 cursor-pointer hover:text-emerald-700 select-none group"><div class="flex items-center space-x-1"><span>Status</span><i class="fa-light fa-arrows-rotate text-[9px] text-slate-300 group-hover:text-emerald-600 ml-1"></i></div></th>
      <th class="py-3.5 px-4 text-center sticky-col-right bg-slate-50 border-l border-slate-100">Ações</th>
    </tr>
  </thead>
  <tbody class="divide-y divide-slate-100 text-slate-700">
    <tr class="hover:bg-slate-50/80 transition duration-150 group cursor-pointer model-row" data-row-id="m0">
      <td class="py-3.5 px-4 sticky-col-left bg-white group-hover:bg-slate-50 border-r border-slate-100"><input type="checkbox" class="row-checkbox rounded border-slate-300 text-emerald-600 focus:ring-emerald-500 cursor-pointer" aria-label="Selecionar linha"></td>
      <td class="py-3.5 px-2 text-center text-slate-400 group-hover:text-emerald-600"><i id="chevron-m0" class="fa-light fa-chevron-right text-[10px] transition-transform duration-200"></i></td>
      <td class="py-3.5 px-4 font-medium text-slate-900"><div class="flex items-start space-x-2"><i class="fa-light fa-chalkboard-user text-emerald-600 mt-1"></i><div><div class="font-semibold text-slate-900 hover:text-emerald-700 transition cursor-pointer" tabindex="0">1ª série A</div><div class="text-[11px] text-slate-400">Ensino Médio</div></div></div></td>
      <td class="py-3.5 px-4"><span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-blue-50 text-blue-700 border border-blue-200 "><span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>Matrículas abertas</span></td>
      <td class="py-3.5 px-4 sticky-col-right bg-white group-hover:bg-slate-50 border-l border-slate-100 text-center"><div class="inline-flex items-center space-x-1">
        <button type="button" data-model-view="m0" class="w-7 h-7 rounded-lg border border-emerald-300 text-emerald-600 hover:bg-emerald-50 flex items-center justify-center transition cursor-pointer" title="Ver detalhes"><i class="fa-light fa-eye text-xs"></i></button>
        <button type="button" data-model-api="edit" class="w-7 h-7 rounded-lg border border-emerald-300 text-emerald-600 hover:bg-emerald-50 flex items-center justify-center transition cursor-pointer" title="Editar"><i class="fa-light fa-pen text-xs"></i></button>
        <button type="button" data-model-api="delete" class="w-7 h-7 rounded-lg border border-rose-200 text-rose-600 hover:bg-rose-50 flex items-center justify-center transition cursor-pointer" title="Excluir"><i class="fa-light fa-trash-can text-xs"></i></button>
      </div></td>
    </tr>
  </tbody>
</table>

<div id="model-table-footer" class="ttsc-pagination-standard flex flex-wrap items-center justify-between gap-x-4 gap-y-2 px-4 py-2.5 bg-white border-t border-slate-200 text-xs select-none">
  <div aria-live="polite" class="flex items-center space-x-1 text-slate-500 shrink-0"><span>Exibindo</span> <span id="model-table-range" class="font-semibold text-slate-800">1-10</span> <span>de</span> <span id="model-table-total" class="font-semibold text-slate-800">36</span> <span>Turmas</span></div>
  <div id="model-table-pagination-buttons" role="group" aria-label="Paginação" class="flex items-center space-x-1.5 shrink-0">…</div>
  <div class="per-page flex items-center gap-2 relative" data-ttsc-page-size-control>
    <span class="text-xs font-medium text-slate-500">Por página:</span>
    <select id="model-table-per-page" aria-label="Por página" class="… ttsc-page-size-native" data-ttsc-pagination-ready="true" data-pagination-select tabindex="-1" aria-hidden="true">
      <option value="5">5</option><option value="10" selected>10</option><option value="25">25</option><option value="50">50</option>
    </select>
    <button type="button" class="ttsc-page-size-trigger" id="ttsc-page-size-1-trigger" aria-haspopup="menu" aria-expanded="false" aria-label="Linhas por página" aria-controls="ttsc-page-size-1-menu"><span class="ttsc-page-size-value">10</span><i class="fa-light fa-chevron-down" aria-hidden="true"></i></button>
  </div>
</div>
```

### CSS

Arquivos: `ttsc.commercial.css` / `ttsc.commercial.model.css` (`.commercial-table-toolbar`, `.sticky-col-left`, `.sticky-col-right`, `html.dark`), `ttsc.pagination.css` (`.ttsc-pagination-standard`, `[data-ttsc-page-size-control]`, `.ttsc-page-size-*`), `ttsc.design-system.css` (`.ttsc-input.has-leading-icon`) e o `<style>` por prefixo que `table.php` imprime. Extensões úteis por token:

```css
/* Ícone de busca acima do fundo do campo (regra que table.php já imprime por prefixo) */
#page-dataToolbar .tbl-search > input { position: relative; z-index: 0; }
#page-dataToolbar .tbl-search > i { z-index: 1; }

/* Densidade e cores por token sobre o <style> do prefixo */
#page-dataDataTable thead th { color: var(--ttsc-text-muted) !important; background: var(--ttsc-canvas-2); }
#page-dataDataTable tbody td { color: var(--ttsc-text-2); }
#page-dataDataTable tbody tr:hover,
#page-dataDataTable tbody tr:hover td.col-actions { background: var(--ttsc-canvas-2); }
#page-dataDataTable td.col-actions,
#page-dataDataTable th.col-actions { background: var(--ttsc-surface); border-left-color: var(--ttsc-border-soft); }
#page-dataDataTable tr:has(.row-checkbox:checked) td { background: var(--ttsc-accent-soft); }

/* Linhas por página no tema escuro */
html.dark .ttsc-page-size-trigger,
html.dark .ttsc-page-size-menu { background: var(--ttsc-surface); border-color: var(--ttsc-border); color: var(--ttsc-text); }
```

### JS

**Preview / documentação** (ficha estática, linhas geradas pelo kit):

```js
TTSCModelKit.syncTheme();
fetch('../../models/academico.json').then(function (r) { return r.json(); }).then(function (sheet) {
  TTSCModelKit.render(
    { portal: { label: 'Administração' }, module: { label: 'Acadêmico' }, page: { label: 'Turmas', route: '/academico/turmas' } },
    sheet.pages['/academico/turmas'], { header: false, banner: false, tabs: false }
  );
  TTSCModelKit.switchTab('table');
});
```

**App, com dados do endpoint**: recarrega a `tbody` da tabela do chassi (`prefix = 'page-data'`) a partir do `DomainCrudController`. O script inline do `domain_page.php` continua ordenando, filtrando e paginando o que estiver na `tbody`, e o `ttsc.pagination.js` cuida do “Por página”.

```js
(function () {
  var ROUTE = '/academic/enrollment/re-enrollment';            // rota de página registrada em kpi-pages
  var LABELS = { shift: { morning: 'Manhã', afternoon: 'Tarde', night: 'Noite' },
                 request_type: { renewal: 'Renovação' },
                 status: { draft: 'Rascunho', submitted: 'Enviado', pending_review: 'Em análise', approved: 'Aprovado',
                           rejected: 'Recusado', confirmed: 'Confirmado', cancelled: 'Cancelado', expired: 'Expirado' } };
  // O endpoint devolve os valores gravados; o render do servidor já traduz via columnMeta,
  // então ao montar pelo JSON a tradução é do cliente.
  var COLS = ['request_type', 'student_name', 'course_name', 'class_name', 'shift', 'period_name', 'created_at', 'status'];
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var text = function (key, v) {
    if (v == null || v === '') return '—';
    if (LABELS[key] && LABELS[key][v]) return LABELS[key][v];
    if (/_at$/.test(key)) return new Date(String(v).replace(' ', 'T')).toLocaleDateString('pt-BR');
    return String(v);                                             // nunca number_format em texto
  };

  async function load(search, status) {
    var qs = new URLSearchParams({ per_page: '100', page: '1', search: search || '', status: status || '' });
    var res = await fetch('/api/v1/domain/records' + ROUTE + '?' + qs, { credentials: 'same-origin', headers: { Accept: 'application/json' } });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    var json = await res.json();                                  // {records, totalRecords, page, per_page}
    var body = document.getElementById('page-dataTableBody');
    body.innerHTML = json.records.map(function (r) {
      return '<tr class="hover:bg-slate-50/80 transition duration-150 group cursor-pointer" data-uuid="' + esc(r.uuid) + '" data-status="' + esc(r.status) + '">' +
        '<td class="col-check"><input type="checkbox" class="row-checkbox rounded border-slate-300 text-emerald-600 focus:ring-emerald-500 cursor-pointer" data-uuid="' + esc(r.uuid) + '" aria-label="Selecionar ' + esc(r.student_name) + '"></td>' +
        '<td class="py-3.5 px-2 text-center text-slate-400 group-hover:text-emerald-600" data-expand-toggle><i class="fa-light fa-chevron-right text-[10px]"></i></td>' +
        COLS.map(function (k) {
          return '<td class="py-3.5 px-4 text-xs text-slate-700 align-middle" data-field="' + k + '" data-raw="' + esc(r[k]) + '">' + esc(text(k, r[k])) + '</td>';
        }).join('') +
        '<td class="col-actions py-3.5 px-4"><button type="button" class="w-7 h-7 rounded-lg border border-emerald-200 text-emerald-600 hover:bg-emerald-50 inline-flex items-center justify-center" data-action="view-record" data-uuid="' + esc(r.uuid) + '" title="Ver" aria-label="Ver ' + esc(r.student_name) + '"><i class="fa-light fa-eye text-xs"></i></button></td>' +
        '</tr>';
    }).join('');
    document.getElementById('page-dataFilterCount').textContent = json.totalRecords + ' registros';
    // o apply() do domain_page roda em eventos: o 'change' do "Por página" repagina as linhas novas
    document.getElementById('page-dataPerPage').dispatchEvent(new Event('change', { bubbles: true }));
  }

  document.addEventListener('DOMContentLoaded', function () {
    load().catch(function (e) { window.showToast && window.showToast('Não foi possível carregar as rematrículas. ' + e.message, 'error'); });
  });
})();
```

### SQL

Página de turmas para a ficha `/academico/turmas`: rótulo do turno pela tabela de enum (evita o código cru), status derivado (a tabela `classes` não tem coluna `status`), ocupação e alunos ativos; ordenação por lista branca e busca com `ESCAPE`.

```sql
-- Página (o PHP troca ORDER BY a partir de uma lista branca: name, code, course_name, start_date, students)
SELECT cl.uuid, cl.code, cl.name, co.name AS course_name,
       cl.shift, COALESCE(rs.label, cl.shift) AS shift_label,
       CASE
         WHEN cl.is_active = 0 OR cl.end_date < CURDATE() THEN 'closed'
         WHEN cl.start_date IS NULL                         THEN 'planned'
         WHEN cl.start_date > CURDATE()                     THEN 'open'
         ELSE 'active'
       END AS status,
       COALESCE(en.students, 0) AS students,
       ROUND(100 * COALESCE(en.students, 0) / NULLIF(cl.max_students, 0), 1) AS occupancy,
       cl.start_date
  FROM classes cl
  JOIN courses co ON co.uuid = cl.course_uuid AND co.deleted_at IS NULL
  LEFT JOIN ref_enum_classes_shift_0111b37ec3c0 rs ON rs.value = cl.shift AND rs.deleted_at IS NULL
  LEFT JOIN (SELECT class_uuid, COUNT(*) AS students
               FROM enrollments
              WHERE deleted_at IS NULL AND status = 'active'
              GROUP BY class_uuid) en ON en.class_uuid = cl.uuid
 WHERE cl.unit_uuid = :unit_uuid
   AND cl.deleted_at IS NULL
   AND (:q = '' OR cl.name LIKE :like1 ESCAPE '!' OR cl.code LIKE :like2 ESCAPE '!' OR co.name LIKE :like3 ESCAPE '!')
 ORDER BY cl.name ASC, cl.id ASC
 LIMIT :per_page OFFSET :offset;

-- Total e filtrado ("Exibindo 1-10 de 36")
SELECT COUNT(*) AS total,
       SUM(:q = '' OR cl.name LIKE :like1 ESCAPE '!' OR cl.code LIKE :like2 ESCAPE '!' OR co.name LIKE :like3 ESCAPE '!') AS filtered
  FROM classes cl
  JOIN courses co ON co.uuid = cl.course_uuid AND co.deleted_at IS NULL
 WHERE cl.unit_uuid = :unit_uuid
   AND cl.deleted_at IS NULL;
```

O PHP monta `:like = '%' . strtr($q, ['!' => '!!', '%' => '!%', '_' => '!_']) . '%'` (um nome por ocorrência), faz `bindValue(':per_page', $perPage, PDO::PARAM_INT)` com `$perPage` entre 10 e 100 e `:offset = ($page - 1) * $perPage`, e devolve `{records, totalRecords, page, per_page}` no mesmo formato do `DomainCrudController::index()`; a view converte cada linha em `cells` (usando `shift_label`, não `shift`).

## Faça / Não faça

- **Faça:** declarar `columns`, `statuses` e `search` da rota em `page-domain-sources.php`; a tabela, o filtro e a busca do endpoint saem dali.
- **Faça:** mostrar rótulos, não códigos: no servidor isso já vem de `status_labels` + `PortalDomainDataService::columnMeta()`; numa montagem pelo JSON, traduza no cliente e guarde o valor em `data-raw`.
- **Faça:** escapar todo valor das `cells` (`$e()`); elas entram cruas na `tbody`.
- **Não faça:** formatar texto como número por regex (`2026.2` não é decimal); use o tipo da coluna, como `$fmt($valor, $coluna)`.
- **Não faça:** expor o nome da tabela no título da visão.
- **Não faça:** `ORDER BY` com texto vindo do request; sempre lista branca.
- **Não faça:** `data-ttsc-datatable` / `ttscDataTable`: são do ttscui, que o layout do app não carrega.
