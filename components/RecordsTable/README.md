# RecordsTable

Aba "Tabela de Dados" do chassi: cabeçalho da visão, busca com contador e "Limpar filtros", barra de lote, tabela com colunas fixas (seleção e ações), linha expansível e a paginação global `ttsc-pagination-standard`.

## Quando usar

- Listar os registros da entidade da página (matrículas, solicitações de rematrícula, diário de classe) com busca, ordenação, seleção em lote e ações por linha.
- É a aba padrão do arquétipo History ([PageHistory](../PageHistory/README.md)) e a mais usada em Records ([PageRecords](../PageRecords/README.md)).
- Para leitura visual de poucos atributos, prefira [RecordCards](../RecordCards/README.md); para itens que avançam por etapas, [KanbanBoard](../KanbanBoard/README.md).
- Tabela simples, sem estado de página (ex.: dentro de um drawer), use [Table](../Table/README.md).

## Anatomia

```
[tile] Matrículas (48)                                   [Pipeline: …]   ← viewHeader
[⌕ Buscar matrículas…                    ] 48 Matrículas  Limpar filtros ← toolbar role=search
[[v] 2 SELECIONADOS | Exportar selecionados | Excluir selecionados  ×]     ← barra de lote (só com seleção)
┌──┬──┬──────────────┬─────────┬────────────┬──────┬─────────┬──────┬────────┬────────┐
│[ ] │› │ ALUNO ⟳      │MATRÍCULA│ STATUS     │TURNO │MENSALID.│FREQ. │DATA    │ AÇÕES  │ ← thead th[data-sort]
│[ ] │⌄ │ Diego Almeida│MAT-1001 │●DOCUMENTAÇÃO│MANHÃ │R$ 2.078 │77,3% │9 abr.  │[ver] [editar] [excluir] │
│  └ Detalhamento • MAT-1001  [Ver detalhes][Editar]  3 grupos da ficha drawer.sections  │ ← tr#expand-<id>
Exibindo 1-10 de 48 Matrículas        [‹][1][2][3][4][5][›]        Por página: [10 ▾]  ← paginação global
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Painel | `#view-table.space-y-4[role=tabpanel]` | sim |
| Cabeçalho da visão | `header.rounded-2xl.border.bg-white` + `span[data-count-badge]` | sim |
| Toolbar | `div.table-toolbar.commercial-table-toolbar[role=search]`, `input[type=search]#<id>-search`, `#<id>-count[aria-live]`, `#<id>-reset` | sim |
| Barra de lote | `#model-batch-bar` (kit) / `.sel-bar#<prefix>SelBar` (chassi, `.is-visible`) | não |
| Rolagem | `#<id>-scroll.overflow-x-auto` > `table#<id>` com `min-width` e `white-space:nowrap` | sim |
| Coluna fixa | `th/td.sticky-col-left` (checkbox) e `.sticky-col-right` (ações) | sim |
| Ordenação | `th[data-sort=<campo>][aria-sort]` | não |
| Linha | `tr.model-row[data-row-id]` + `input.row-checkbox` | sim |
| Expansão | `tr#expand-<id>.hidden` > `.table-expanded-content`; chevron `#chevron-<id>` gira `rotate-90` | não |
| Vazio filtrado | `#<id>-empty` (sem resultado) — [EmptyState](../EmptyState/README.md) | sim |
| Paginação | `#<id>-footer.ttsc-pagination-standard` + `#<id>-pagination-buttons[role=group]` + `[data-ttsc-page-size-control] select` | sim |

## Estados

| Estado | Como |
|---|---|
| Carregado | `tbody` com até `per_page` linhas; range "1-10 de 48" |
| Buscando | contador `#<id>-count` atualizado (`aria-live`), "Limpar filtros" visível |
| Sem resultado | `#<id>-empty` visível, tabela vazia |
| Sem dados | `td.ttsc-empty-state-cell > .ttsc-empty-state.is-no-data` com ação "Novo" (`chassis/table.php`) |
| Seleção | barra de lote visível com "N SELECIONADOS" |
| Linha expandida | `tr#expand-<id>` sem `hidden`; chevron com `rotate-90` |
| Somente leitura | `table['writable'] = false`: sem editar/excluir/mudar status |

## API

**Ficha**

| Campo | Uso |
|---|---|
| `fields[]` (`key`, `label`, `type`, `table:false`) | colunas, na ordem; `type` decide a célula: `code` (pílula mono), `status/stage/enum` (badge com tom), `money` (mono negrito), `pct/int/number` (mono), `date/datetime/email/domain` (mono 11px) |
| `titleField` / `subField` | 1ª coluna com ícone `entity.icon` e linha secundária |
| `statusField`, `codeField` | badge e título do detalhamento |
| `drawer.sections` | até 3 grupos da linha expandida |
| `tableTitle`, `tableDesc`, `chip:{label,num,den,unit}` | cabeçalho da visão |
| `batch[]` | ações extras da barra de lote |
| `searchPlaceholder` | texto da busca |

**PHP — `chassis/table.php`** (`$table`): `prefix`, `columns[]`, `rows[] = ['uuid','data','cells']`, `search` (`false` desliga), `filters[] = ['name','label','options','selected']`, `batch[]`, `empty`, `emptyTitle`, `emptyDescription`, `viewIcon`, `viewTitle`, `viewDesc`, `viewChipLabel`, `viewChipValue`, `expandable`, `statusBatch`, `writable`, `total`, `page`, `perPage` (padrão 25).

**JS**

| API | Efeito |
|---|---|
| `TTSCModelKit.blocks.table(page, rows)` / `.search(id, page)` / `.pager(id, label, rounded)` | HTML das partes |
| `ttsc.pagination.js` (auto) | todo `select` de "Por página" dentro de `[data-ttsc-page-size-control]`/`.per-page` vira o menu visual `.ttsc-page-size-trigger`; o `select` nativo continua sendo a fonte do valor (`change`). Observa o DOM com `MutationObserver` — não há função global para chamar |
| `data-action="filter-table"` / `data-filter` | busca e filtros do chassi (`behaviors.php`) |
| `data-action="domain-view-record"` + `data-uuid` | abre o drawer View |
| `data-action="open-create-drawer"` | ação do estado vazio |

**Endpoints (`DomainCrudController`)**

| Método | Rota | Parâmetros / resposta |
|---|---|---|
| GET | `/api/v1/domain/records{rota}` | `search` (≤ 200, `LIKE` com `%`/`_` escapados nas colunas de texto), `status` (só valores de `known_statuses`), `page`, `per_page` (10–100, padrão 25) → `{success, route, table, totalRecords, page, per_page, records[]}`, ordem `created_at DESC` |
| GET | `/api/v1/domain/records{rota}/{id}` | registro do drawer |
| PUT / DELETE | `/api/v1/domain/records{rota}/{id}` | editar / excluir (CSRF, rate limit 30/15 min) |
| POST | `/api/v1/domain/records{rota}/status` | `{id, status}` — "Mudar status" em lote |
| GET | `/api/v1/domain/records{rota}/export?format=csv&ids=a,b` | "Exportar selecionados" |

## Acessibilidade

- `th[aria-sort]` alterna `ascending/descending/none`; o título da coluna é o rótulo do botão de ordenação.
- Checkboxes com `aria-label` ("Selecionar todos", "Selecionar linha"); a barra de lote anuncia a contagem.
- Contadores e range com `aria-live="polite"`; botões de página com `aria-label` e `aria-current="page"`.
- Ações só-ícone têm `title`; ao portar, acrescente `aria-label` ("Ver detalhes de Diego Almeida").
- Clique na linha expande; teclado: o título (`tabindex="0"`) e o botão "Ver detalhes" dão acesso equivalente.

## Modelos

### HTML

1) PHP real — `chassis/domain_page.php` monta `$table` e inclui o partial:

```php
<?php
$table = [
    'prefix'      => 'domain',
    'columns'     => array_map(fn ($c) => ['label' => $c['label']], $explorerColumns),
    'rows'        => array_map(fn ($r) => ['uuid' => $recordId($r), 'data' => $r], $records),
    'search'      => ['placeholder' => 'Buscar solicitações…'],
    'filters'     => [['name' => 'status', 'label' => 'Todos os status', 'options' => $drawerStatuses]],
    'viewIcon'    => 'fa-user-plus',
    'viewTitle'   => 'Solicitações de rematrícula',
    'expandable'  => true,
    'statusBatch' => true,
    'writable'    => $canWrite,          // false para fontes com 'writable' => false
    'total'       => $totalRecords, 'page' => 1, 'perPage' => 25,
    'emptyTitle'  => 'Nenhuma solicitação de rematrícula',
    'emptyDescription' => 'As solicitações aparecem aqui quando o período de rematrícula abrir.',
];
include base_path('resources/views/app/partials/chassis/table.php');
```

A fonte vem de `app/Config/page-domain-sources.php`:

```php
'/academic/enrollment/re-enrollment' => [
    'source'     => 'inst_secretariat_reenrollment',
    'permission' => 'admin.academic.enrollments',
    'writable'   => false,
    'statuses'   => ['draft' => 'Draft', 'submitted' => 'Sent', 'pending_review' => 'Under review', 'approved' => 'Approved',
                     'rejected' => 'Rejected', 'confirmed' => 'Confirmed', 'cancelled' => 'Cancelled', 'expired' => 'Expired'],
    'columns'    => ['request_type' => 'Type', 'student_name' => 'Student', 'course_name' => 'Course', 'class_name' => 'Class',
                     'shift' => 'Shift', 'period_name' => 'Period', 'created_at' => 'Requested at', 'status' => 'Status'],
    'search'     => ['student_name', 'course_name', 'class_name'],
],
```

2) HTML gerado (preview; 1 linha e paginação, colunas resumidas):

```html
<div class="table-toolbar commercial-table-toolbar flex flex-col lg:flex-row lg:items-center gap-2.5 rounded-2xl border border-slate-200 bg-white p-3 shadow-sm" role="search">
  <label class="relative min-w-0 flex-1">
    <i class="fa-light fa-magnifying-glass pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-xs text-slate-400" aria-hidden="true"></i>
    <input type="search" id="model-table-search" autocomplete="off" placeholder="Buscar matrículas…" class="w-full rounded-xl border border-slate-200 bg-white py-2.5 pl-9 pr-9 text-xs text-slate-800 shadow-sm placeholder:text-slate-400 focus:border-emerald-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/30" aria-label="Buscar matrículas…">
  </label>
  <div class="flex items-center justify-between gap-2 xl:justify-end">
    <span id="model-table-count" class="whitespace-nowrap px-1 text-xs tabular-nums text-slate-500" aria-live="polite" aria-atomic="true">48 Matrículas</span>
    <button type="button" id="model-table-reset" class="hidden whitespace-nowrap rounded-lg px-2.5 py-2 text-xs font-semibold text-emerald-700 hover:bg-emerald-50 focus:outline-none focus:ring-2 focus:ring-emerald-500/40">Limpar filtros</button>
  </div>
</div>
<div class="bg-white border border-slate-200 rounded-2xl shadow-sm">
  <div id="model-table-scroll" class="overflow-x-auto" style="max-width:100%">
    <table id="model-table" class="w-full text-left border-collapse text-xs" style="min-width:1120px;white-space:nowrap">
      <thead>
        <tr class="border-b border-slate-200 bg-slate-50 text-slate-500 font-semibold uppercase text-[11px] tracking-wider select-none">
          <th class="py-3.5 px-4 w-12 sticky-col-left bg-slate-50 border-r border-slate-100"><input type="checkbox" data-model-master class="rounded border-slate-300 text-emerald-600 focus:ring-emerald-500 cursor-pointer" aria-label="Selecionar todos"></th>
          <th class="py-3.5 px-2 w-8 bg-slate-50 text-center select-none text-slate-400"><i class="fa-light fa-chevron-down text-[10px]"></i></th>
          <th data-sort="student" aria-sort="none" class="py-3.5 px-4 cursor-pointer hover:text-emerald-700 select-none group"><div class="flex items-center space-x-1"><span>Aluno</span><i class="fa-light fa-arrows-rotate text-[9px] text-slate-300 group-hover:text-emerald-600 ml-1"></i></div></th>
          <!-- … Matrícula, Status, Turno, Mensalidade, Frequência, Data da matrícula -->
          <th class="py-3.5 px-4 text-center sticky-col-right bg-slate-50 border-l border-slate-100">Ações</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-100 text-slate-700">
        <tr class="hover:bg-slate-50/80 transition duration-150 group cursor-pointer model-row" data-row-id="m0">
          <td class="py-3.5 px-4 sticky-col-left bg-white group-hover:bg-slate-50 border-r border-slate-100"><input type="checkbox" class="row-checkbox rounded border-slate-300 text-emerald-600 focus:ring-emerald-500 cursor-pointer" aria-label="Selecionar linha"></td>
          <td class="py-3.5 px-2 text-center text-slate-400 group-hover:text-emerald-600"><i id="chevron-m0" class="fa-light fa-chevron-right text-[10px] transition-transform duration-200"></i></td>
          <td class="py-3.5 px-4 font-medium text-slate-900"><div class="flex items-start space-x-2"><i class="fa-light fa-id-card text-emerald-600 mt-1"></i><div><div class="font-semibold text-slate-900 hover:text-emerald-700 transition cursor-pointer" tabindex="0">Diego Almeida</div><div class="text-[11px] text-slate-400">Técnico em Enfermagem</div></div></div></td>
          <td class="py-3.5 px-4 font-mono text-[11px] text-slate-500 font-medium"><span class="px-2 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200">MAT-1001</span></td>
          <td class="py-3.5 px-4"><span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-blue-50 text-blue-700 border border-blue-200"><span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>Documentação</span></td>
          <td class="py-3.5 px-4 font-mono font-bold text-slate-900">R$&nbsp;2.078,66</td>
          <td class="py-3.5 px-4 sticky-col-right bg-white group-hover:bg-slate-50 border-l border-slate-100 text-center">
            <div class="inline-flex items-center space-x-1">
              <button type="button" data-model-view="m0" class="w-7 h-7 rounded-lg border border-emerald-300 text-emerald-600 hover:bg-emerald-50 flex items-center justify-center transition cursor-pointer" title="Ver detalhes"><i class="fa-light fa-eye text-xs"></i></button>
              <button type="button" data-model-api="edit" class="w-7 h-7 rounded-lg border border-emerald-300 text-emerald-600 hover:bg-emerald-50 flex items-center justify-center transition cursor-pointer" title="Editar"><i class="fa-light fa-pen text-xs"></i></button>
              <button type="button" data-model-api="delete" class="w-7 h-7 rounded-lg border border-rose-200 text-rose-600 hover:bg-rose-50 flex items-center justify-center transition cursor-pointer" title="Excluir"><i class="fa-light fa-trash-can text-xs"></i></button>
            </div>
          </td>
        </tr>
        <tr id="expand-m0" class="bg-slate-50 border-y border-slate-200 whitespace-normal hidden"><td colspan="10" class="p-2.5 sm:p-3.5 w-full max-w-full overflow-hidden"><div class="table-expanded-content bg-white rounded-xl border border-blue-200 p-3 sm:p-4 shadow-xs space-y-3 w-full max-w-full overflow-hidden">…</div></td></tr>
      </tbody>
    </table>
  </div>
  <div id="model-table-footer" class="ttsc-pagination-standard flex flex-wrap items-center justify-between gap-x-4 gap-y-2 px-4 py-2.5 bg-white border-t border-slate-200 text-xs select-none">
    <div aria-live="polite" class="flex items-center space-x-1 text-slate-500 shrink-0"><span>Exibindo</span> <span id="model-table-range" class="font-semibold text-slate-800">1-10</span> <span>de</span> <span id="model-table-total" class="font-semibold text-slate-800">48</span> <span>Matrículas</span></div>
    <div id="model-table-pagination-buttons" role="group" aria-label="Paginação" class="flex items-center space-x-1.5 shrink-0">
      <button type="button" data-nav="prev" aria-label="Página anterior" disabled class="w-7 h-7 rounded-lg border border-slate-200 text-slate-300 flex items-center justify-center cursor-not-allowed"><i class="fa-light fa-chevron-left text-[10px]" aria-hidden="true"></i></button>
      <button type="button" data-page="1" aria-label="Página 1" aria-current="page" class="model-table-page-btn w-7 h-7 rounded-lg font-bold flex items-center justify-center shadow-xs transition cursor-pointer focus:outline-none focus:ring-2 focus:ring-emerald-500/40 bg-emerald-500 text-white border border-emerald-500">1</button>
      <!-- … 2 3 4 5 › -->
    </div>
    <div class="per-page flex items-center gap-2 relative" data-ttsc-page-size-control>
      <span class="text-xs font-medium text-slate-500">Por página:</span>
      <select id="model-table-per-page" aria-label="Por página" class="… ttsc-page-size-native" data-ttsc-pagination-ready="true" data-pagination-select tabindex="-1" aria-hidden="true">
        <option value="5">5</option><option value="10" selected>10</option><option value="25">25</option><option value="50">50</option>
      </select>
      <button type="button" class="ttsc-page-size-trigger" id="ttsc-page-size-1-trigger" aria-haspopup="menu" aria-expanded="false" aria-label="Linhas por página" aria-controls="ttsc-page-size-1-menu"><span class="ttsc-page-size-value">10</span><i class="fa-light fa-chevron-down" aria-hidden="true"></i></button>
    </div>
  </div>
</div>
```

### CSS

- `assets/css/ttsc.commercial.css` / `ttsc.commercial.model.css` — `.commercial-table-toolbar`, `.sticky-col-left`, `.sticky-col-right`, `.table-expanded-content` e o escuro (`html.dark .bg-white`, `.bg-slate-50`, `.divide-slate-100`).
- `assets/css/ttsc.pagination.css` — `.ttsc-pagination-standard`, `.ttsc-page-size-trigger`, `.ttsc-page-size-menu`; `html.dark .ttsc-pagination-standard` troca fundo, borda e o `strong` do range.
- `chassis/table.php` injeta a densidade da tabela num `<style nonce>` por `#<prefix>DataTable` (th 11px caps, td 14×16px, ações sticky).

```css
/* Extensão por tokens: linha selecionada e foco de linha navegável */
#model-table tr.model-row:has(.row-checkbox:checked) td { background: var(--ttsc-accent-soft); }
#model-table tr.model-row:focus-within td { box-shadow: inset 0 0 0 1px var(--ttsc-accent-border); }
#model-table th[aria-sort="ascending"] .fa-arrows-rotate,
#model-table th[aria-sort="descending"] .fa-arrows-rotate { color: var(--ttsc-accent-text); }
```

### JS

```js
// Tabela alimentada pelo endpoint real (busca no servidor, paginação, total)
const ROUTE = '/academic/enrollment/re-enrollment';
const API = '/api/v1/domain/records' + ROUTE;
const state = { page: 1, per: 25, search: '', status: '' };
const tbody = document.querySelector('#domain-table tbody');

async function load() {
  const qs = new URLSearchParams({ page: state.page, per_page: state.per });
  if (state.search) qs.set('search', state.search);
  if (state.status) qs.set('status', state.status);
  const res = await fetch(`${API}?${qs}`, { credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' } });
  if (!res.ok) throw new Error('HTTP ' + res.status);
  const { records, totalRecords } = await res.json();
  tbody.innerHTML = records.map((r) => `
    <tr class="model-row" data-row-id="${r.uuid}">
      <td class="sticky-col-left"><input type="checkbox" class="row-checkbox" aria-label="Selecionar ${r.student_name}"></td>
      <td>${r.student_name}</td><td>${r.course_name ?? '—'}</td><td>${r.class_name ?? '—'}</td><td>${r.status}</td>
      <td class="sticky-col-right"><button type="button" data-action="domain-view-record" data-uuid="${r.uuid}" aria-label="Ver detalhes">
        <i class="fa-light fa-eye"></i></button></td>
    </tr>`).join('');
  const start = totalRecords ? (state.page - 1) * state.per + 1 : 0;
  document.getElementById('domain-table-range').textContent = `${start}-${Math.min(state.page * state.per, totalRecords)}`;
  document.getElementById('domain-table-total').textContent = totalRecords;
  document.getElementById('domain-table-empty').hidden = totalRecords > 0;
}

let timer;
document.getElementById('domain-table-search').addEventListener('input', (e) => {
  clearTimeout(timer);
  timer = setTimeout(() => { state.search = e.target.value.trim(); state.page = 1; load(); }, 250);
});
// o select nativo continua emitindo "change" depois que ttsc.pagination.js o substitui visualmente
document.getElementById('domain-table-per-page').addEventListener('change', (e) => { state.per = Number(e.target.value); state.page = 1; load(); });
load();
```

### SQL

O que `DomainCrudController::index()` executa sobre a fonte da página, escrito por extenso (ordenação por lista branca é acréscimo do front; o endpoint ordena por `created_at DESC`):

```sql
-- Total sem filtro (contador da aba)
SELECT COUNT(*) FROM inst_secretariat_reenrollment;

-- Total filtrado (contador da toolbar): busca nas colunas 'search' do contrato, LIKE com escape
SELECT COUNT(*)
  FROM inst_secretariat_reenrollment
 WHERE (student_name LIKE :q ESCAPE '\\' OR course_name LIKE :q ESCAPE '\\' OR class_name LIKE :q ESCAPE '\\')
   AND (:status = '' OR status = :status);

-- Página (colunas do contrato; ORDER BY só de uma lista branca: created_at, student_name, course_name, status)
SELECT uuid, request_type, student_name, course_name, class_name, shift, period_name, created_at, status
  FROM inst_secretariat_reenrollment
 WHERE (student_name LIKE :q ESCAPE '\\' OR course_name LIKE :q ESCAPE '\\' OR class_name LIKE :q ESCAPE '\\')
   AND (:status = '' OR status = :status)
 ORDER BY created_at DESC
 LIMIT :limit OFFSET :offset;

-- Mesma página direto na tabela de matrículas, com nome do aluno e curso
SELECT e.uuid, e.code, u.name AS aluno, c.name AS curso, e.status, e.shift, e.enrollment_date
  FROM enrollments e
  JOIN users u   ON u.uuid = e.student_uuid
  JOIN courses c ON c.uuid = e.course_uuid
 WHERE e.deleted_at IS NULL
   AND (u.name LIKE :q ESCAPE '\\' OR e.code LIKE :q ESCAPE '\\')
 ORDER BY e.enrollment_date DESC, e.id DESC
 LIMIT :limit OFFSET :offset;
```

`:q` é `'%' . strtr($busca, ['%' => '\%', '_' => '\_']) . '%'`; `:limit` = `per_page` (10–100) e `:offset` = `(page - 1) * per_page`, interpolados como inteiros. O PHP devolve `records` + `totalRecords`; no SSR, `$table['rows']` e `$table['total']`.

## Faça / Não faça

- **Faça:** colunas e busca vindas do contrato (`columns`/`search` de `page-domain-sources.php`) — nada além disso é selecionado ou exportado.
- **Faça:** `status` filtrado só por valores do vocabulário; o servidor recusa o resto (422).
- **Não faça:** ordenar por nome de coluna vindo do cliente sem lista branca.
- **Não faça:** paginação própria: use o rodapé `ttsc-pagination-standard` com o `select` nativo, que o `ttsc.pagination.js` estiliza.
