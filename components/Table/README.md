# Table

Tabela estática do runtime (`.ttsc-table` dentro de `.ttsc-table-wrapper`) com realce de linha, bordas, e extensões TTSC para zebra, compacta, cabeçalho fixo, linha selecionada e coluna de ações.

> Também listado em: **Base › Tables**.

## Quando usar

- Dados tabulares renderizados no servidor que cabem numa tela (até ~50 linhas): turmas de um curso, parcelas de uma matrícula, notas de uma avaliação.
- Tabelas de resumo dentro de cards, drawers e relatórios impressos.
- Busca, ordenação no cliente e paginação → [DataTable](../DataTable/README.md) (`data-ttsc-datatable`), que usa as mesmas classes.
- Muitas linhas com navegação por página → DataTable + [Pagination](../Pagination/README.md).
- Registros com muitos campos heterogêneos (ficha do aluno) → [RecordCard](../RecordCard/README.md), não uma tabela de 2 colunas.

## Anatomia

```
.ttsc-table-wrapper (overflow:auto, role=region, tabindex=0)
  table.ttsc-table [.ttsc-table-highlight .ttsc-table-zebra .ttsc-table-sticky .ttsc-table-border .ttsc-table-compact]
    thead > tr > th (altura 40px, fundo --muted 40%)
    tbody > tr[.checked] > td (padding 12px 16px; última coluna = ações)
    tfoot (totais, fundo --muted 50%)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Wrapper | `div.ttsc-table-wrapper` (rolagem horizontal no mobile) | sim |
| Tabela | `table.ttsc-table` | sim |
| Realce no hover / selecionada | `ttsc-table-highlight` + `tr.checked` | não |
| Bordas | `ttsc-table-border` (todas) · `ttsc-table-border-s/-e/-t/-b` (lados) | não |
| Ordenação visual | `th[aria-sort] > .ttsc-table-col > .ttsc-table-col-label + .ttsc-table-col-sort` | não |
| Centralizar | `ttsc-table-cell-center` | não |
| Extensões TTSC | `ttsc-table-zebra` · `ttsc-table-compact` · `ttsc-table-sticky` | não |

## Variantes

| Variante | Classe | Uso | Tokens |
|---|---|---|---|
| Padrão | `ttsc-table` | listas simples | linhas `--border`=`ttsc-border`; cabeçalho `--muted`=`ttsc-canvas-2` 40%; texto `ttsc-text`, cabeçalho `--secondary-foreground` |
| Highlight | `ttsc-table-highlight` | linhas clicáveis | hover `ttsc-canvas-2` 50% |
| Zebra | `ttsc-table-zebra` (TTSC) | tabelas largas de leitura | pares `ttsc-canvas` |
| Bordas | `ttsc-table-border` | relatórios, impressão | `ttsc-border` |
| Compacta | `ttsc-table-compact` (TTSC) | cards densos | linha `--ttsc-row-compact` (36px) |
| Sticky header | `ttsc-table-sticky` (TTSC) + wrapper com `max-height` | listas com rolagem interna | `ttsc-canvas-2` opaco |
| Selecionada | `tr.checked` + `aria-selected="true"` | seleção em lote | `ttsc-accent-soft` + barra 3px `ttsc-accent` |

## API

Tabela estática não tem JS no ttscui. Ao ganhar `data-ttsc-datatable` vira [DataTable](../DataTable/README.md) (a mesma marcação). O controle de seleção é implementação TTSC (`assets/js/core/ttsc.table-select.js`, abaixo): marca `tr.checked`, sincroniza o checkbox do cabeçalho (inclusive `indeterminate`) e dispara `ttsc.table.selection` com `detail: { values }`.

| Atributo | Efeito |
|---|---|
| `data-ttsc-table-select` (na `<table>`) | ativa a seleção em lote |
| `data-ttsc-table-check="all"` | checkbox do cabeçalho |
| `data-ttsc-table-check` + `value` | checkbox da linha |
| `[data-ttsc-table-count]` | elemento que recebe “N selecionadas” |

## Acessibilidade

- Use `<table>` semântica com `<th scope="col">`; nunca grids de `div` para dados tabulares.
- Wrapper rolável: `role="region"`, `aria-label` e `tabindex="0"` (teclado consegue rolar).
- Coluna de ações: cabeçalho com texto oculto (“Ações”); botões só-ícone com `aria-label` que cite a linha (“Editar turma 2º A”).
- Linha selecionada: `aria-selected="true"` + checkbox marcado (não só cor).
- Números alinhados à direita com `tabular-nums`; status com [Badge](../Badge/README.md) contendo texto.
- Contraste: corpo `ttsc-text` (16:1), subtexto `ttsc-text-muted` (4,9:1); o fundo selecionado `ttsc-accent-soft` mantém o texto ≥ 12:1.

## Modelos

### HTML

```html
<div class="ttsc-table-wrapper" role="region" aria-label="Turmas do curso" tabindex="0" style="max-height: 420px">
  <table class="ttsc-table ttsc-table-highlight ttsc-table-sticky" data-ttsc-table-select>
    <thead>
      <tr>
        <th scope="col" style="width: 36px">
          <input type="checkbox" class="ttsc-checkbox ttsc-checkbox-sm" data-ttsc-table-check="all" aria-label="Selecionar todas">
        </th>
        <th scope="col">Turma</th>
        <th scope="col">Turno</th>
        <th scope="col" class="text-end">Matrículas</th>
        <th scope="col" class="text-end">Ocupação</th>
        <th scope="col"><span class="sr-only">Ações</span></th>
      </tr>
    </thead>
    <tbody>
      <?php foreach ($classes as $c): ?>
      <tr>
        <td><input type="checkbox" class="ttsc-checkbox ttsc-checkbox-sm" data-ttsc-table-check value="<?= $e($c['uuid']) ?>" aria-label="Selecionar <?= $e($c['name']) ?>"></td>
        <td><strong><?= $e($c['name']) ?></strong><span class="block text-xs"><?= $e($c['course_name']) ?></span></td>
        <td><?= $e(__('shift_' . $c['shift'], 'academic', $c['shift'])) ?></td>
        <td class="text-end"><?= (int) $c['enrolled'] ?>/<?= (int) $c['max_students'] ?></td>
        <td class="text-end"><?= $c['occupancy_pct'] === null ? '—' : (int) $c['occupancy_pct'] . '%' ?></td>
        <td class="text-end">
          <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" aria-label="Editar turma <?= $e($c['name']) ?>"><i class="fa-light fa-pen"></i></button>
        </td>
      </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>
```

### CSS

```css
/* Ponte (bundle.css): a tabela lê --border, --muted, --foreground, --secondary-foreground */
:root { --border: var(--ttsc-border); --muted: var(--ttsc-canvas-2); --foreground: var(--ttsc-text); }

/* Extensões TTSC */
.ttsc-table-zebra tbody tr:nth-child(even) { background-color: var(--ttsc-canvas); }
.ttsc-table-compact thead th { height: var(--ttsc-row-compact); }
.ttsc-table-compact tbody td { padding-block: 6px; }
.ttsc-table-sticky thead th { position: sticky; top: 0; z-index: 1; background-color: var(--ttsc-canvas-2); }
.ttsc-table tbody tr.checked { background-color: var(--ttsc-accent-soft) !important; box-shadow: inset 3px 0 0 var(--ttsc-accent); }
.ttsc-table td.num, .ttsc-table th.num { text-align: right; font-variant-numeric: tabular-nums; }

@media print { .ttsc-table { font-size: 10pt; } .ttsc-table-sticky thead th { position: static; } }
```

### JS

```js
// assets/js/core/ttsc.table-select.js — implementação TTSC de seleção em lote
document.querySelectorAll('table[data-ttsc-table-select]').forEach(function (table) {
  var all = table.querySelector('[data-ttsc-table-check="all"]');
  var counter = document.querySelector('[data-ttsc-table-count]');

  function rows() { return table.querySelectorAll('tbody [data-ttsc-table-check]'); }

  function sync() {
    var values = [];
    rows().forEach(function (chk) {
      var tr = chk.closest('tr');
      tr.classList.toggle('checked', chk.checked);
      tr.setAttribute('aria-selected', String(chk.checked));
      if (chk.checked) values.push(chk.value);
    });
    all.checked = values.length > 0 && values.length === rows().length;
    all.indeterminate = values.length > 0 && values.length < rows().length;
    if (counter) counter.textContent = values.length === 1 ? '1 selecionada' : values.length + ' selecionadas';
    table.dispatchEvent(new CustomEvent('ttsc.table.selection', { bubbles: true, detail: { values: values } }));
  }

  all.addEventListener('change', function () {
    rows().forEach(function (chk) { chk.checked = all.checked; });
    sync();
  });
  table.querySelector('tbody').addEventListener('change', sync);
  sync();
});

// Ação em lote: exportar lista de alunos das turmas selecionadas
document.addEventListener('ttsc.table.selection', function (e) {
  document.getElementById('btn-export-selected').disabled = e.detail.values.length === 0;
});
```

### SQL

Turmas com contagem de matrículas ativas e ocupação:

```sql
SELECT cl.uuid,
       cl.code,
       COALESCE(cl.name, cl.code) AS name,
       co.name AS course_name,
       cl.shift,
       cl.max_students,
       COUNT(e.uuid) AS enrolled,
       ROUND(100 * COUNT(e.uuid) / NULLIF(cl.max_students, 0)) AS occupancy_pct
  FROM classes cl
  JOIN courses co
    ON co.uuid = cl.course_uuid AND co.deleted_at IS NULL
  LEFT JOIN enrollments e
    ON e.class_uuid = cl.uuid AND e.status = 'active' AND e.deleted_at IS NULL
 WHERE cl.unit_uuid = :unit_uuid
   AND cl.deleted_at IS NULL
 GROUP BY cl.uuid, cl.code, cl.name, co.name, cl.shift, cl.max_students
 ORDER BY co.name, name;
```

O controller passa `$classes` para a view, que itera as linhas como no HTML acima; `occupancy_pct` nulo (turma sem limite) aparece como “—”, e `shift` é traduzido pelo catálogo `ref_enum_classes_shift_*`.

## Faça / Não faça

- **Faça:** sempre o wrapper (rolagem no mobile) e números à direita.
- **Faça:** ações por linha com botões ghost só-ícone e `aria-label` contextual.
- **Não faça:** zebra + highlight + bordas ao mesmo tempo (ruído visual).
- **Não faça:** tabela estática com centenas de linhas — use DataTable com paginação no servidor.
