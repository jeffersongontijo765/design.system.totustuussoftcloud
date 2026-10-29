# DataTables

Tabela de dados DataTables 2.3.7 (jQuery) com processamento server-side, idioma pt-BR e tema ligado aos tokens TTSC, para listagens grandes que o servidor pagina, busca e ordena.

## Quando usar

- Listagens com milhares de registros (matrículas, logs de privacidade, auditoria) em que **o servidor** faz `LIMIT/OFFSET`, `ORDER BY` e busca — o navegador recebe só a página atual.
- Telas que já falam o contrato `draw/start/length/search/order → {draw, recordsTotal, recordsFiltered, data}` (ex.: endpoints do `PrivacyController` e `PrivacyComplianceController`).
- Quando precisar de extensões do ecossistema DataTables (Responsive, Buttons, Select).
- **Não use** para tabelas novas e comuns do CRUD: use [DataTable](../DataTable/README.md) (`data-ttsc-datatable`, runtime ttscui, sem jQuery, com o mesmo visual do chassi). Para listas curtas (< 50 linhas, sem paginação) use uma `table.ttsc-table` simples.
- **Não use** modo client-side com `data:` de milhares de linhas renderizadas no PHP: a página pesa e a busca fica no cliente.

## Anatomia

```
.dt-container
├── .dt-layout-row  [ .dt-length (select) ]              [ .dt-search (input) ]
├── table.dataTable  thead th.dt-orderable-* > span.dt-column-order
│                    tbody tr > td
├── .dt-processing   (overlay "Carregando…")
└── .dt-layout-row  [ .dt-info "1 a 5 de 23" ]           [ .dt-paging > button.dt-paging-button ]
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Wrapper de tema | `.ttsc-dt` (no card que envolve a tabela) | sim |
| Tabela | `<table id="…" class="display">` com `<thead>` | sim |
| Container gerado | `.dt-container` (criado pelo plugin) | — |
| Busca / quantidade | `.dt-search input` · `.dt-length select` | não (`layout`) |
| Status de carga | `.dt-processing` (`processing: true`) | recomendado |
| Paginação | `.dt-paging .dt-paging-button.current/.disabled` | sim |

## Variantes

| Variante | Configuração | Uso | Tokens |
|---|---|---|---|
| Server-side | `serverSide: true, ajax: { url, type: 'POST' }` | padrão para > 500 linhas | — |
| Client-side | `data: [...]` sem `serverSide` | lista pequena já carregada | — |
| Compacta | `pageLength: 10` + `td { padding: 6px 10px }` | cards de dashboard | `ttsc-row-compact` |
| Paginação atual | `.dt-paging-button.current` | página ativa | fundo `ttsc-accent-soft`, borda `ttsc-accent-border`, texto `ttsc-accent-text` |
| Cabeçalho | `thead th` | rótulo caps 11px | fundo `ttsc-canvas`, texto `ttsc-text-muted`, borda `ttsc-border` |
| Linhas | `tbody td` | divisória e hover | borda `ttsc-border-soft`, hover `--dt-row-hover` (preto/branco por tema) |

## Estados

| Estado | Como aparece |
|---|---|
| Carregando | `.dt-processing` visível (barra em `ttsc-accent`) enquanto a requisição não volta |
| Vazio | `language.emptyTable` “Nenhuma matrícula cadastrada” (`recordsTotal = 0`) |
| Sem resultado | `language.zeroRecords` “Nenhuma matrícula encontrada” (`recordsFiltered = 0`) |
| Filtrado | `.dt-info` mostra “(filtradas de _MAX_)” quando `recordsFiltered < recordsTotal` |
| Erro | evento `dt-error` — mostre um [Toast](../Toast/README.md) em vez do `alert()` padrão (`DataTable.ext.errMode = 'none'`) |

## API

### Requisição server-side (enviada pelo DataTables)

| Parâmetro | Exemplo | Uso no servidor |
|---|---|---|
| `draw` | `3` | devolva o mesmo número (int) — descarta respostas fora de ordem |
| `start` | `20` | `OFFSET` (int ≥ 0) |
| `length` | `10` | `LIMIT` (int; `-1` = todos — limite a 100 no PHP) |
| `search[value]` | `ana` | termo global → `LIKE` escapado |
| `order[0][column]` / `order[0][dir]` | `1` / `asc` | índice da coluna → **whitelist** de colunas SQL; `dir` só `asc`/`desc` |
| `order[0][name]` | `student_name` | nome da coluna (DT 2), quando `columns[].name` está definido |
| `columns[i][data]` / `[searchable]` / `[orderable]` | `code` / `true` | metadados por coluna |

### Resposta JSON

```json
{ "draw": 3, "recordsTotal": 1240, "recordsFiltered": 37,
  "data": [ { "uuid": "…", "code": "MAT-2026-0101", "student_name": "Ana Beatriz Souza",
              "course_name": "Ensino Médio — 1º ano", "status": "active", "status_label": "Ativa",
              "enrollment_date": "2026-02-01" } ] }
```

### Opções usadas

| Opção | Valor | Efeito |
|---|---|---|
| `serverSide` | `true` | cada busca/ordem/página vira requisição |
| `processing` | `true` | mostra `.dt-processing` |
| `ajax` | `{ url, type: 'POST', data(d){ d._token = … } }` ou `function(data, callback)` | origem dos dados |
| `columns` | `[{ data: 'code', name: 'code', render }]` | mapeia chaves do JSON |
| `order` | `[[1, 'asc']]` | ordenação inicial |
| `pageLength` / `lengthMenu` | `10` / `[10, 25, 50]` | tamanho da página |
| `language` | objeto pt-BR inline (abaixo) | textos; não carregue JSON de CDN |
| `searchDelay` | `400` | debounce da busca (ms) |
| `layout` | `{ topStart: 'pageLength', topEnd: 'search', bottomStart: 'info', bottomEnd: 'paging' }` | posição dos controles |

### Métodos e eventos

| API | Uso |
|---|---|
| `table.ajax.reload(null, false)` | recarrega mantendo a página (após salvar no drawer) |
| `table.search('ana').draw()` | busca programática |
| `table.order([2, 'desc']).draw()` | ordenação programática |
| `table.page.info()` | `{ page, pages, start, end, recordsTotal, recordsDisplay }` |
| `table.destroy()` | antes de remover o HTML (navegação parcial) |
| `table.on('xhr', fn)` / `('draw', fn)` / `('dt-error', fn)` | resposta recebida / tabela redesenhada / falha |

## Acessibilidade

- Use `<th>` reais; o DataTables adiciona `aria-sort` e o `language.aria` lê “Ordenar por esta coluna”.
- A ordenação funciona por teclado (Tab até o `th`, Enter/Espaço). Não remova o foco do `th`.
- A busca tem `aria-controls` apontando para a tabela; mantenha `searchPlaceholder` descritivo (“Aluno, curso ou código”) porque o runtime oculta o rótulo visual (`font-size: 0` no `label`).
- Status em badge **com texto** (“Ativa”, “Trancada”), nunca só cor. Texto da paginação atual em `ttsc-accent-text` (≥ 4,5:1); nunca `ttsc-accent` como texto.

## Modelos

### HTML

```html
<!-- resources/views/app/pages/academic/enrollments/index.php -->
<link rel="stylesheet" href="/assets/vendors/datatables/dataTables.dataTables.css">

<div class="ttsc-card">
  <div class="ttsc-card-header">
    <h3 class="ttsc-card-title">Matrículas</h3>
  </div>
  <div class="ttsc-card-content ttsc-dt">
    <table id="dt-enrollments" class="display" style="width:100%"
           data-endpoint="<?= $this->e($endpoint) ?>">   <!-- /admin/academic/enrollments/datatable -->
      <thead>
        <tr><th>Código</th><th>Aluno</th><th>Curso</th><th>Status</th><th>Data</th></tr>
      </thead>
    </table>
  </div>
</div>

<script src="/assets/vendors/jquery/jquery.min.js"></script>
<script src="/assets/vendors/datatables/dataTables.min.js"></script>
<script src="/assets/js/core/ttsc.datatables-net.js"></script>
```

### CSS

O runtime (`tailwind-runtime.css`) já traz um tema `.dt-container` (labels ocultos, chevrons SVG, inputs `--input`). O CSS do vendor carregado depois troca os chevrons por “▲▼” — o bloco abaixo reconcilia os dois e liga as cores aos tokens:

```css
.ttsc-dt { --dt-row-hover: 0,0,0; --dt-row-stripe: 0,0,0; --dt-html-background: var(--ttsc-surface); color: var(--ttsc-text); }
[data-theme="dark"] .ttsc-dt { --dt-row-hover: 255,255,255; --dt-row-stripe: 255,255,255; }

.ttsc-dt table.dataTable > thead > tr > th {
  font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em;
  color: var(--ttsc-text-muted); background: var(--ttsc-canvas);
  border-bottom: 1px solid var(--ttsc-border) !important;
}
.ttsc-dt table.dataTable > tbody > tr > td { border-top: 1px solid var(--ttsc-border-soft) !important; color: var(--ttsc-text-2); }

/* mantém os chevrons SVG do runtime */
.ttsc-dt table.dataTable thead > tr > th span.dt-column-order:before,
.ttsc-dt table.dataTable thead > tr > th span.dt-column-order:after { content: "" !important; opacity: .45; }

.ttsc-dt div.dt-container .dt-paging .dt-paging-button.current {
  background: var(--ttsc-accent-soft) !important; border-color: var(--ttsc-accent-border) !important;
  color: var(--ttsc-accent-text) !important;
}
.ttsc-dt div.dt-processing { background: var(--ttsc-surface); color: var(--ttsc-text); border: 1px solid var(--ttsc-border); box-shadow: var(--ttsc-shadow-md); }
.ttsc-dt div.dt-processing > div:last-child > div { background: var(--ttsc-accent); }
```

### JS

```js
// assets/js/core/ttsc.datatables-net.js
window.TTSC = window.TTSC || {};

TTSC.DT_PT_BR = {
  processing: 'Carregando…', search: 'Buscar:', searchPlaceholder: 'Aluno, curso ou código',
  lengthMenu: '_MENU_ por página', info: '_START_ a _END_ de _TOTAL_ registros',
  infoEmpty: 'Nenhum registro', infoFiltered: '(filtrados de _MAX_)',
  zeroRecords: 'Nenhum registro encontrado', emptyTable: 'Nenhum registro cadastrado',
  paginate: { first: '«', previous: '‹', next: '›', last: '»' },
  aria: { orderable: 'Ordenar por esta coluna', orderableReverse: 'Inverter ordenação' },
};

DataTable.ext.errMode = 'none'; // sem alert(); tratamos no evento dt-error

const STATUS_BADGE = { active: 'ttsc-badge-success', locked: 'ttsc-badge-warning', transferred: 'ttsc-badge-info', cancelled: 'ttsc-badge-destructive' };
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

export function initEnrollmentsTable(selector = '#dt-enrollments') {
  const el = document.querySelector(selector);
  const token = document.querySelector('meta[name="csrf-token"]')?.content || '';

  const table = new DataTable(el, {
    serverSide: true,
    processing: true,
    searchDelay: 400,
    pageLength: 10,
    lengthMenu: [10, 25, 50],
    order: [[1, 'asc']],
    language: TTSC.DT_PT_BR,
    ajax: {
      url: el.dataset.endpoint,
      type: 'POST',
      headers: { 'X-CSRF-TOKEN': token },
    },
    columns: [
      { data: 'code', name: 'code' },
      { data: 'student_name', name: 'student_name' },
      { data: 'course_name', name: 'course_name' },
      { data: 'status_label', name: 'status', render: (d, type, row) =>
          type === 'display' ? `<span class="ttsc-badge ttsc-badge-sm ttsc-badge-outline ${STATUS_BADGE[row.status] || ''}">${esc(d)}</span>` : d },
      { data: 'enrollment_date', name: 'enrollment_date', render: (d, type) =>
          type === 'display' && d ? d.split('-').reverse().join('/') : d },
    ],
  });

  table.on('dt-error', () => TTSC.Toast?.show({ message: 'Não foi possível carregar as matrículas.', variant: 'destructive' }));

  // Após salvar no drawer de matrícula, recarrega mantendo a página atual
  document.addEventListener('ttsc:enrollment-saved', () => table.ajax.reload(null, false));
  return table;
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('#dt-enrollments')) initEnrollmentsTable();
});
```

### SQL

Três consultas por requisição: total sem filtro, total filtrado e a página. `ORDER BY` vem de uma **whitelist** (`[1 => 's.name', 2 => 'c.name', …]`) indexada por `order[0][column]`; o termo é escapado em PHP com `strtr($q, ['!' => '!!', '%' => '!%', '_' => '!_'])` e envolvido em `%…%`.

```sql
-- 1) recordsTotal: matrículas da unidade, sem busca
SELECT COUNT(*) AS records_total
  FROM enrollments e
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid;

-- 2) recordsFiltered: mesma base + termo de busca
SELECT COUNT(*) AS records_filtered
  FROM enrollments e
  JOIN courses c    ON c.uuid = e.course_uuid AND c.deleted_at IS NULL
  LEFT JOIN users s ON s.uuid = e.student_uuid AND s.deleted_at IS NULL
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid
   AND (:q = '' OR e.code LIKE :q_like ESCAPE '!' OR c.name LIKE :q_like ESCAPE '!' OR s.name LIKE :q_like ESCAPE '!');

-- 3) data: página atual (ORDER BY montado da whitelist; LIMIT/OFFSET como int)
SELECT e.uuid, e.code, s.name AS student_name, c.name AS course_name,
       e.status, e.enrollment_date
  FROM enrollments e
  JOIN courses c    ON c.uuid = e.course_uuid AND c.deleted_at IS NULL
  LEFT JOIN users s ON s.uuid = e.student_uuid AND s.deleted_at IS NULL
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid
   AND (:q = '' OR e.code LIKE :q_like ESCAPE '!' OR c.name LIKE :q_like ESCAPE '!' OR s.name LIKE :q_like ESCAPE '!')
 ORDER BY s.name ASC, e.code ASC
 LIMIT :length OFFSET :start;
```

Em MariaDB 10.11 / MySQL 8 as consultas 2 e 3 podem virar uma só com `COUNT(*) OVER () AS records_filtered` na lista do SELECT (página vazia ⇒ faça a consulta 2 de fallback). O controller devolve `Response::json(['draw' => (int) $draw, 'recordsTotal' => …, 'recordsFiltered' => …, 'data' => $rows])`, com `status_label` traduzido pelo catálogo `ref_enum_enrollments_status_*`.

## Faça / Não faça

- **Faça:** devolva `draw` como inteiro e use `type: 'POST'` + `X-CSRF-TOKEN` quando a URL passa pelo `CsrfMiddleware`.
- **Faça:** whitelist de colunas para `ORDER BY` e `LIMIT` máximo (100) no servidor; filtre `deleted_at IS NULL` e `unit_uuid`.
- **Faça:** escape o HTML no `render` (os dados vêm do banco).
- **Não faça:** concatenar `order[0][dir]` ou `search[value]` direto no SQL.
- **Não faça:** carregar `language.url` de CDN — use o objeto `TTSC.DT_PT_BR`.
- **Não faça:** usar DataTables em telas novas que o [DataTable](../DataTable/README.md) do ttscui atende — são dois visuais e duas APIs para manter.
