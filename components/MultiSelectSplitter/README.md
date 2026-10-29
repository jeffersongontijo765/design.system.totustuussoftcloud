# MultiSelectSplitter

Implementação TTSC (JS puro) que transforma um `<select multiple>` com `<optgroup>` em duas colunas — grupo à esquerda, itens com checkbox à direita — mantendo o select original sincronizado para o envio do formulário.

## Quando usar

- Seleção múltipla em **dois níveis** com muitos itens: curso → disciplinas da matriz, unidade → turmas, módulo → permissões.
- Quando o usuário precisa ver quantos itens marcou em cada grupo sem abrir um dropdown.
- **Não use** para listas planas ou com menos de ~10 opções: use [Select2](../Select2/README.md) (`multiple`) ou o [Select](../Select/README.md) do ttscui.
- **Não use** para hierarquias com mais de dois níveis: use uma árvore (jsTree).
- Para rótulos livres (sem lista fechada) use [Tagify](../Tagify/README.md).

## Anatomia

```
┌ .ttsc-mss ───────────────────┬───────────────────────────────────────────┐
│ CURSO           (head)       │ DISCIPLINAS · ADMINISTRAÇÃO   Marcar todas │
│ ▌Administração           [2] │ [ Buscar disciplina...                  ]  │
│  Pedagogia               [1] │ [x] Teoria Geral da Administração    60 h │
│  Direito                 [0] │ [ ] Matemática Financeira            40 h │
└──────────────────────────────┴───────────────────────────────────────────┘
 select[multiple][hidden]  ← continua no form e é o que vai no POST
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Origem | `select[multiple][data-ttsc-mss]` com `name="…[]"` e `aria-label` | sim |
| Grupos | `<optgroup label="Curso">` | sim |
| Itens | `<option value="uuid" data-meta="60 h">` (`selected`, `disabled` respeitados) | sim |
| Container gerado | `.ttsc-mss` (2 colunas `.ttsc-mss-col`) | gerado |
| Lista de grupos | `ul.ttsc-mss-list[role=listbox] > button.ttsc-mss-group[role=option]` + `.ttsc-mss-count` | gerado |
| Itens | `label.ttsc-mss-item > input.ttsc-checkbox` | gerado |
| Busca | `.ttsc-mss-search .ttsc-input` (automática com mais de 8 opções) | não |

## Estados

| Estado | Visual | Tokens |
|---|---|---|
| Grupo ativo | `aria-selected="true"`, fundo tonal | `ttsc-accent-soft`, texto `ttsc-text` |
| Grupo com seleção | contador cheio | `ttsc-accent` + `ttsc-accent-on` |
| Grupo sem seleção | contador neutro | `ttsc-surface-2` + `ttsc-text-2` |
| Item marcado | checkbox do runtime | `--primary` |
| Busca sem resultado | “Nenhum item encontrado.” | `ttsc-text-muted` |

## API

Atributos:

| Atributo | Padrão | Descrição |
|---|---|---|
| `data-ttsc-mss` | — | Ativa no `select[multiple]` |
| `data-ttsc-mss-group-label` | `Grupo` | Título da coluna esquerda |
| `data-ttsc-mss-item-label` | `Itens` | Título da coluna direita (seguido do grupo ativo) |
| `data-meta` (na `option`) | — | Texto secundário à direita (carga horária) |

Opções JS (`new TTSCMultiSelectSplitter(select, opts)`): `groupLabel`, `itemLabel`, `search` (bool), `emptyText`.

| Método | Descrição |
|---|---|
| `TTSCMultiSelectSplitter.init(root?)` | Inicializa todos os `select[multiple][data-ttsc-mss]` (idempotente) |
| `getValues()` | Array de `value` selecionados |
| `setValues(array)` | Marca exatamente esses valores e re-renderiza |
| `activate(index, focus?)` | Troca o grupo ativo |
| `destroy()` | Remove a UI e mostra o select de volta |

Evento: o próprio `select` dispara `change` (bubbles) a cada alteração — use os mesmos listeners de um select comum.

## Acessibilidade

- Coluna de grupos é um `listbox` com *roving tabindex*: `Tab` entra no grupo ativo, `↑`/`↓` trocam de grupo.
- Itens são checkboxes nativos dentro de `label` (clique no texto marca; `Espaço` alterna).
- Contador tem `aria-label="2 selecionadas"`; título da coluna direita anuncia o grupo ativo.
- O select original fica `hidden` (fora da ordem de foco), mas continua no formulário — sem JS, ele aparece e funciona.
- Contraste: contador cheio usa `ttsc-accent-on` sobre `ttsc-accent` (9,6:1); link “Marcar todas” em `ttsc-accent-text`.

## Modelos

### HTML

```html
<div class="ttsc-form-item">
  <label class="ttsc-form-label" id="lbl-subjects">Disciplinas da turma</label>
  <select multiple name="subject_uuids[]" data-ttsc-mss aria-labelledby="lbl-subjects"
          data-ttsc-mss-group-label="Curso" data-ttsc-mss-item-label="Disciplinas">
    <?php foreach ($grouped as $courseName => $subjects): ?>
      <optgroup label="<?= $this->e($courseName) ?>">
        <?php foreach ($subjects as $s): ?>
          <option value="<?= $this->e($s['subject_uuid']) ?>" data-meta="<?= (int) $s['workload'] ?> h"
                  <?= $s['selected'] ? 'selected' : '' ?>><?= $this->e($s['subject_name']) ?></option>
        <?php endforeach; ?>
      </optgroup>
    <?php endforeach; ?>
  </select>
</div>
```

### CSS

```css
/* assets/css/ttsc.multiselect-splitter.css */
.ttsc-mss { display: grid; grid-template-columns: minmax(180px, 2fr) 3fr; overflow: hidden;
  border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control); background: var(--ttsc-surface); }
.ttsc-mss-col { display: flex; flex-direction: column; min-width: 0; }
.ttsc-mss-col + .ttsc-mss-col { border-inline-start: 1px solid var(--ttsc-border); }
.ttsc-mss-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; min-height: 40px; padding: 8px 12px;
  border-bottom: 1px solid var(--ttsc-border); background: var(--ttsc-canvas-2);
  font-size: 11px; font-weight: 500; letter-spacing: .04em; text-transform: uppercase; color: var(--ttsc-text-muted); }
.ttsc-mss-list { list-style: none; margin: 0; padding: 4px; overflow-y: auto; max-height: 232px; }
.ttsc-mss-group { display: flex; width: 100%; align-items: center; justify-content: space-between; gap: 8px; padding: 8px 10px;
  border: 0; border-radius: var(--ttsc-radius-sm); background: transparent; color: var(--ttsc-text-2); font: inherit; text-align: start; cursor: pointer; }
.ttsc-mss-group:hover { background: var(--ttsc-canvas-2); }
.ttsc-mss-group:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: -2px; }
.ttsc-mss-group[aria-selected="true"] { background: var(--ttsc-accent-soft); color: var(--ttsc-text); font-weight: 500; }
.ttsc-mss-count { font-size: 11px; min-width: 22px; text-align: center; padding: 1px 6px; border-radius: var(--ttsc-radius-pill);
  background: var(--ttsc-surface-2); color: var(--ttsc-text-2); }
.ttsc-mss-count.has { background: var(--ttsc-accent); color: var(--ttsc-accent-on); }
.ttsc-mss-item { display: flex; align-items: center; gap: 10px; padding: 7px 10px; border-radius: var(--ttsc-radius-sm); color: var(--ttsc-text); cursor: pointer; }
.ttsc-mss-item:hover { background: var(--ttsc-canvas-2); }
.ttsc-mss-item small { margin-inline-start: auto; color: var(--ttsc-text-muted); font-variant-numeric: tabular-nums; }
.ttsc-mss-search { padding: 8px; border-bottom: 1px solid var(--ttsc-border-soft); }
.ttsc-mss-empty { padding: 16px; color: var(--ttsc-text-muted); font-size: 12px; }
.ttsc-mss-link { border: 0; background: none; padding: 0; font: inherit; font-size: 12px; text-transform: none; letter-spacing: 0;
  color: var(--ttsc-accent-text); cursor: pointer; }
@media (max-width: 640px) {
  .ttsc-mss { grid-template-columns: 1fr; }
  .ttsc-mss-col + .ttsc-mss-col { border-inline-start: 0; border-top: 1px solid var(--ttsc-border); }
}
```

### JS

```js
// assets/js/core/ttsc.multiselect-splitter.js — implementação TTSC (sem dependências)
(function (w) {
  'use strict';
  var uid = 0;
  function TTSCMultiSelectSplitter(select, opts) {
    if (select.ttscMss) return select.ttscMss;
    this.select = select;
    this.o = Object.assign({
      groupLabel: select.dataset.ttscMssGroupLabel || 'Grupo',
      itemLabel: select.dataset.ttscMssItemLabel || 'Itens',
      search: select.options.length > 8,
      emptyText: 'Nenhum item encontrado.'
    }, opts || {});
    this.id = 'ttsc-mss-' + (++uid);
    this.groups = Array.prototype.slice.call(select.querySelectorAll('optgroup'));
    this.active = this.groups.findIndex(function (g) { return g.querySelector('option:checked'); });
    if (this.active < 0) this.active = 0;
    this.query = '';
    this.build();
    select.hidden = true;
    select.ttscMss = this;
  }
  TTSCMultiSelectSplitter.prototype.build = function () {
    var self = this, root = document.createElement('div');
    root.className = 'ttsc-mss';
    root.innerHTML =
      '<div class="ttsc-mss-col"><div class="ttsc-mss-head" id="' + this.id + '-g">' + this.o.groupLabel + '</div>' +
      '<ul class="ttsc-mss-list" role="listbox" aria-labelledby="' + this.id + '-g" data-groups></ul></div>' +
      '<div class="ttsc-mss-col"><div class="ttsc-mss-head"><span id="' + this.id + '-i"></span>' +
      '<button type="button" class="ttsc-mss-link" data-toggle-all></button></div>' +
      (this.o.search ? '<div class="ttsc-mss-search"><input type="search" class="ttsc-input" placeholder="Buscar disciplina..." aria-label="Buscar"></div>' : '') +
      '<ul class="ttsc-mss-list" role="group" aria-labelledby="' + this.id + '-i" data-items></ul></div>';
    this.select.after(root);
    this.root = root;
    this.gList = root.querySelector('[data-groups]');
    this.iList = root.querySelector('[data-items]');
    this.gList.addEventListener('click', function (e) { var b = e.target.closest('[data-index]'); if (b) self.activate(+b.dataset.index, true); });
    this.gList.addEventListener('keydown', function (e) {
      var d = { ArrowDown: 1, ArrowUp: -1 }[e.key];
      if (d) { e.preventDefault(); self.activate((self.active + d + self.groups.length) % self.groups.length, true); }
    });
    this.iList.addEventListener('change', function (e) {
      var opt = self.select.querySelector('option[value="' + CSS.escape(e.target.value) + '"]');
      opt.selected = e.target.checked; self.sync();
    });
    root.querySelector('[data-toggle-all]').addEventListener('click', function () {
      var opts = self.visibleOptions(), all = opts.every(function (o) { return o.selected; });
      opts.forEach(function (o) { o.selected = !all; }); self.render(); self.sync();
    });
    var s = root.querySelector('input[type=search]');
    if (s) s.addEventListener('input', function () { self.query = s.value.trim().toLowerCase(); self.renderItems(); });
    this.render();
  };
  TTSCMultiSelectSplitter.prototype.visibleOptions = function () {
    var q = this.query;
    return Array.prototype.filter.call(this.groups[this.active].children, function (o) { return !q || o.text.toLowerCase().indexOf(q) > -1; });
  };
  TTSCMultiSelectSplitter.prototype.render = function () {
    var self = this;
    this.gList.innerHTML = this.groups.map(function (g, i) {
      var n = g.querySelectorAll('option:checked').length;
      return '<li><button type="button" role="option" class="ttsc-mss-group" data-index="' + i + '" aria-selected="' + (i === self.active) + '" tabindex="' + (i === self.active ? 0 : -1) + '">' +
        '<span>' + g.label + '</span><span class="ttsc-mss-count' + (n ? ' has' : '') + '" aria-label="' + n + ' selecionadas">' + n + '</span></button></li>';
    }).join('');
    this.renderItems();
  };
  TTSCMultiSelectSplitter.prototype.renderItems = function () {
    var opts = this.visibleOptions(), g = this.groups[this.active];
    this.root.querySelector('#' + this.id + '-i').textContent = this.o.itemLabel + ' · ' + g.label;
    this.root.querySelector('[data-toggle-all]').textContent = opts.length && opts.every(function (o) { return o.selected; }) ? 'Desmarcar todas' : 'Marcar todas';
    this.iList.innerHTML = opts.length ? opts.map(function (o) {
      return '<li><label class="ttsc-mss-item"><input type="checkbox" class="ttsc-checkbox ttsc-checkbox-sm" value="' + o.value + '"' + (o.selected ? ' checked' : '') + (o.disabled ? ' disabled' : '') + '>' +
        '<span>' + o.text + '</span>' + (o.dataset.meta ? '<small>' + o.dataset.meta + '</small>' : '') + '</label></li>';
    }).join('') : '<li class="ttsc-mss-empty">' + this.o.emptyText + '</li>';
  };
  TTSCMultiSelectSplitter.prototype.activate = function (i, focus) {
    this.active = i; this.render();
    if (focus) this.gList.querySelector('[data-index="' + i + '"]').focus();
  };
  TTSCMultiSelectSplitter.prototype.sync = function () {
    var self = this;
    this.groups.forEach(function (g, i) {
      var n = g.querySelectorAll('option:checked').length, c = self.gList.querySelector('[data-index="' + i + '"] .ttsc-mss-count');
      c.textContent = n; c.classList.toggle('has', n > 0); c.setAttribute('aria-label', n + ' selecionadas');
    });
    this.renderItems();
    this.select.dispatchEvent(new Event('change', { bubbles: true }));
  };
  TTSCMultiSelectSplitter.prototype.getValues = function () {
    return Array.prototype.map.call(this.select.selectedOptions, function (o) { return o.value; });
  };
  TTSCMultiSelectSplitter.prototype.setValues = function (values) {
    Array.prototype.forEach.call(this.select.options, function (o) { o.selected = values.indexOf(o.value) > -1; });
    this.render(); this.select.dispatchEvent(new Event('change', { bubbles: true }));
  };
  TTSCMultiSelectSplitter.prototype.destroy = function () { this.root.remove(); this.select.hidden = false; delete this.select.ttscMss; };
  TTSCMultiSelectSplitter.init = function (root) {
    (root || document).querySelectorAll('select[multiple][data-ttsc-mss]').forEach(function (s) { new TTSCMultiSelectSplitter(s); });
  };
  w.TTSCMultiSelectSplitter = TTSCMultiSelectSplitter;
  document.addEventListener('DOMContentLoaded', function () { TTSCMultiSelectSplitter.init(); });
})(window);

// Uso: atualiza a carga horária total da turma
document.querySelector('[name="subject_uuids[]"]').addEventListener('change', (e) => {
  const total = [...e.target.selectedOptions].reduce((sum, o) => sum + parseInt(o.dataset.meta, 10), 0);
  document.querySelector('#class-workload').textContent = `${total} h`;
});
```

> Os textos de `optgroup`/`option` são inseridos como HTML: o PHP precisa escapá-los (`$this->e()`), como no modelo acima.

### SQL

```sql
-- Disciplinas por curso (matriz ativa) + as já vinculadas à turma. MariaDB 10.11 / MySQL 8
SELECT c.uuid  AS course_uuid,  c.name AS course_name,
       s.uuid  AS subject_uuid, s.name AS subject_name,
       COALESCE(cs.workload, s.workload) AS workload,
       cs.period_number,
       (cls.subject_uuid IS NOT NULL)    AS selected
  FROM courses c
  JOIN curriculums cu         ON cu.course_uuid = c.uuid AND cu.is_active = 1 AND cu.deleted_at IS NULL
  JOIN curriculum_subjects cs ON cs.curriculum_uuid = cu.uuid
  JOIN subjects s             ON s.uuid = cs.subject_uuid AND s.is_active = 1 AND s.deleted_at IS NULL
  LEFT JOIN class_subjects cls ON cls.subject_uuid = s.uuid AND cls.class_uuid = :class_uuid
 WHERE c.unit_uuid = :unit_uuid
   AND c.is_active = 1
   AND c.deleted_at IS NULL
 ORDER BY c.name, cs.period_number, s.name;

-- Gravação (numa transação): remove o que saiu e insere o que entrou
DELETE FROM class_subjects
 WHERE class_uuid = :class_uuid
   AND subject_uuid NOT IN (:s1, :s2, :s3);          -- lista expandida pelo PHP

INSERT IGNORE INTO class_subjects (uuid, class_uuid, subject_uuid, workload, created_at)
SELECT UUID(), :class_uuid, s.uuid, s.workload, NOW()
  FROM subjects s
 WHERE s.uuid IN (:s1, :s2, :s3) AND s.deleted_at IS NULL;   -- uk_class_subject evita duplicar
```

O PHP agrupa as linhas por `course_name` (`$grouped[$row['course_name']][] = $row`) e gera um `<optgroup>` por curso; `selected = 1` vira o atributo `selected`. `class_subjects` não tem `deleted_at`, por isso a desvinculação é `DELETE` físico.

## Faça / Não faça

- **Faça:** manter o `select` original com `name="…[]"` — ele é a fonte da verdade do POST e o fallback sem JS.
- **Faça:** escapar `label` e textos no servidor; mostrar o contador por grupo.
- **Faça:** busca quando um grupo tem muitos itens (automática acima de 8 opções).
- **Não faça:** usar para dois ou três itens por grupo (um select comum é mais rápido).
- **Não faça:** gravar a seleção só no `change` sem transação no servidor (DELETE + INSERT juntos).
