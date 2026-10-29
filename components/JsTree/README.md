# jsTree

Árvore hierárquica com jsTree 3.3.17 (jQuery) para navegar e marcar **unidade › curso › turma** — plugins `checkbox`, `types`, `search` e `wholerow`, ícones Font Awesome light e tema ajustado por tokens nos dois temas.

## Quando usar

- Escolher destinatários por estrutura acadêmica: enviar comunicado, gerar boletos ou relatório de frequência para várias turmas de várias unidades.
- Navegar por hierarquias profundas e irregulares (plano de contas, pastas de documentos, organograma).
- **Não use** para 1 nível de opções: [Select2](../Select2/README.md) / [Checkbox](../Checkbox/README.md). Para 2 níveis fixos (curso → turma) com busca, um select com grupos (`optgroup`) é mais simples.
- **Não use** como menu de navegação do sistema — a sub-sidebar do chassi já é o [Menu](../Menu/README.md).
- **Não use** para reordenar itens arrastando (o plugin `dnd` existe, mas use [Draggable](../Draggable/README.md)).

## Anatomia

```
.ttsc-jstree
└── #tree.jstree.jstree-default[role=tree]
    └── ul.jstree-container-ul
        └── li.jstree-node[role=treeitem][aria-expanded]
            ├── i.jstree-ocl                (abre/fecha)
            └── a.jstree-anchor (.jstree-clicked = marcado)
                ├── i.jstree-checkbox (.jstree-undetermined = parcial)
                ├── i.jstree-themeicon.fa-light.fa-building | fa-graduation-cap | fa-users
                └── "1º ano B — Tarde"
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Wrapper de tema | `.ttsc-jstree` | sim |
| Alvo | `<div id="…" aria-label="Unidades, cursos e turmas">` | sim |
| Nó | objeto `{ id, parent, text, type, state, li_attr, a_attr }` (formato plano) | sim |
| Ícone por tipo | plugin `types` → `icon: 'fa-light fa-…'` | sim |
| Busca | `input[type=search]` + `tree.search(q)` | recomendado |
| Resumo da seleção | painel ao lado com contagem | recomendado |

## Variantes

| Tipo (`type`) | Ícone | Origem |
|---|---|---|
| `unit` | `fa-light fa-building` | `units` |
| `course` | `fa-light fa-graduation-cap` | `courses` (por `unit_uuid`) |
| `class` | `fa-light fa-users` (`max_children: 0`) | `classes` (por `course_uuid`) |

## Estados

| Estado | Marca | Tokens |
|---|---|---|
| Hover | `.jstree-hovered` | fundo `ttsc-canvas-2`, texto `ttsc-text` |
| Marcado | `.jstree-clicked` + checkbox preenchido | fundo `ttsc-accent-soft`, texto `ttsc-accent-text`, caixa `ttsc-accent` com check `ttsc-accent-on` |
| Parcial (três estados) | `.jstree-checkbox.jstree-undetermined` | borda + traço `ttsc-accent` |
| Desabilitado | `state.disabled` → `.jstree-disabled` | texto `ttsc-text-muted`, caixa `ttsc-canvas-2` |
| Resultado de busca | `.jstree-search` | `ttsc-accent-text` 600 |

## API

### Configuração

| Opção | Valor TTSC | Efeito |
|---|---|---|
| `core.data` | array plano ou `{ url, data(node) }` (lazy) | nós |
| `core.themes` | `{ name: 'default', dots: false, icons: true }` | tema base |
| `core.multiple` | `true` | várias marcações |
| `core.strings` | `{ 'Loading ...': 'Carregando…' }` | i18n |
| `plugins` | `['checkbox', 'types', 'search', 'wholerow']` | — |
| `checkbox.three_state` | `true` | pai marca/desmarca filhos; parcial |
| `checkbox.keep_selected_style` | `false` | estilo vem do CSS do tema |
| `checkbox.cascade` | `''` (padrão com three_state) / `'down'` | regra de cascata |
| `types.<tipo>` | `{ icon, max_children, valid_children }` | ícone e regras |
| `search.show_only_matches` / `show_only_matches_children` | `true` / `true` | filtra a árvore |

### Métodos (`$('#tree').jstree(true)`)

| Método | Uso |
|---|---|
| `get_selected(full?)` | ids (ou nós) marcados — filtre `type === 'class'` |
| `get_bottom_selected()` / `get_top_selected()` | só folhas / só raízes marcadas |
| `select_node(id)` / `deselect_all()` / `check_all()` | seleção programática |
| `open_node(id)` / `open_all()` / `close_all()` | expansão |
| `search(q)` / `clear_search()` | busca |
| `refresh()` / `settings.core.data = …` | recarregar |
| `disable_node(id)` / `enable_node(id)` | bloquear turma |
| `destroy()` | antes de remover o HTML |

### Eventos (jQuery, sufixo `.jstree`)

| Evento | Quando |
|---|---|
| `ready.jstree` / `loaded.jstree` | árvore pronta |
| `changed.jstree` | seleção mudou (`data.selected`, `data.action`) |
| `select_node.jstree` / `deselect_node.jstree` | nó marcado/desmarcado |
| `open_node.jstree` | expandiu (carregar filhos sob demanda) |
| `search.jstree` | busca concluída (`data.nodes`) |

## Acessibilidade

- jsTree aplica `role="tree"`/`treeitem`, `aria-expanded`, `aria-selected`, `aria-level`; dê `aria-label` ao container.
- Teclado nativo: ↑↓ move, → abre / ← fecha, Espaço/Enter marca, `*` expande irmãos, Home/End.
- Foco visível: contorno 2px `ttsc-accent` no `.jstree-anchor`.
- O total marcado aparece em texto no painel (“Turmas selecionadas (2)”), não só nos checkboxes.
- Tema escuro: as setas do sprite são invertidas e o checkbox é desenhado com tokens (o sprite padrão fica ilegível no escuro).

## Modelos

### HTML

```html
<div class="grid grid-cols-2 gap-4">
  <div class="ttsc-card"><div class="ttsc-card-content flex flex-col gap-3">
    <div class="ttsc-input-group">
      <span class="ttsc-input-addon"><i class="fa-light fa-magnifying-glass"></i></span>
      <input type="search" class="ttsc-input" id="tree-search" placeholder="Buscar unidade, curso ou turma" aria-label="Buscar na árvore">
    </div>
    <div class="ttsc-jstree">
      <div id="tree-classes" aria-label="Unidades, cursos e turmas" data-source="/admin/academic/structure/tree"></div>
    </div>
  </div></div>
  <form class="ttsc-card" method="post" action="/admin/communications/send">
    <input type="hidden" name="_token" value="<?= $this->e($csrf) ?>">
    <input type="hidden" name="class_uuids" id="tree-selected">
    <div class="ttsc-card-content">
      <div class="text-xs">Turmas selecionadas (<span id="tree-count">0</span>)</div>
      <button type="submit" class="ttsc-btn ttsc-btn-primary ttsc-btn-sm" id="tree-apply" disabled>
        <i class="fa-light fa-paper-plane"></i> Enviar comunicado
      </button>
    </div>
  </form>
</div>
<link rel="stylesheet" href="/assets/vendors/jstree/themes/default/style.min.css">
<script src="/assets/vendors/jquery/jquery.min.js"></script>
<script src="/assets/vendors/jstree/jstree.min.js"></script>
```

### CSS

```css
.ttsc-jstree .jstree-default .jstree-anchor { color: var(--ttsc-text-2); font-size: 13px; height: 26px; line-height: 26px; border-radius: var(--ttsc-radius-xs); }
.ttsc-jstree .jstree-default .jstree-hovered { background: var(--ttsc-canvas-2); box-shadow: none; color: var(--ttsc-text); }
.ttsc-jstree .jstree-default .jstree-clicked { background: var(--ttsc-accent-soft); box-shadow: none; color: var(--ttsc-accent-text); }
.ttsc-jstree .jstree-default .jstree-search { color: var(--ttsc-accent-text); font-style: normal; font-weight: 600; }
.ttsc-jstree .jstree-default .jstree-themeicon-custom { background: none; color: var(--ttsc-text-muted); }
.ttsc-jstree .jstree-default .jstree-anchor:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: -1px; }
.ttsc-jstree .jstree-default .jstree-disabled { color: var(--ttsc-text-muted); }
[data-theme="dark"] .ttsc-jstree .jstree-default .jstree-ocl { filter: invert(1) brightness(1.2); }

/* checkbox com tokens (substitui o sprite 32px.png) */
.ttsc-jstree .jstree-default .jstree-checkbox { background: none !important; position: relative; }
.ttsc-jstree .jstree-default .jstree-checkbox::before {
  content: ""; position: absolute; left: 5px; top: 5px; width: 14px; height: 14px; box-sizing: border-box;
  border: 1px solid var(--ttsc-border-strong); border-radius: 3px; background: var(--ttsc-surface);
}
.ttsc-jstree .jstree-default .jstree-clicked > .jstree-checkbox::before { background: var(--ttsc-accent); border-color: var(--ttsc-accent); }
.ttsc-jstree .jstree-default .jstree-clicked > .jstree-checkbox::after {
  content: ""; position: absolute; left: 10px; top: 7px; width: 4px; height: 8px;
  border: solid var(--ttsc-accent-on); border-width: 0 2px 2px 0; transform: rotate(45deg);
}
.ttsc-jstree .jstree-default .jstree-checkbox.jstree-undetermined::before { border-color: var(--ttsc-accent); }
.ttsc-jstree .jstree-default .jstree-checkbox.jstree-undetermined::after { content: ""; position: absolute; left: 8px; top: 11px; width: 8px; height: 2px; background: var(--ttsc-accent); }
```

### JS

```js
// assets/js/core/ttsc.class-tree.js
export async function initClassTree($el = $('#tree-classes')) {
  const rows = await fetch($el.data('source'), { headers: { Accept: 'application/json' } }).then((r) => r.json());
  const nodes = rows.map((r) => ({
    id: r.id, parent: r.parent, text: r.text, type: r.type,
    state: { opened: r.type === 'unit', disabled: !!Number(r.disabled) },
    li_attr: r.students !== null ? { 'data-students': r.students } : {},
  }));

  $el.jstree({
    core: { data: nodes, multiple: true, themes: { name: 'default', dots: false, icons: true }, strings: { 'Loading ...': 'Carregando…' } },
    plugins: ['checkbox', 'types', 'search', 'wholerow'],
    checkbox: { three_state: true, keep_selected_style: false },
    types: {
      unit: { icon: 'fa-light fa-building' },
      course: { icon: 'fa-light fa-graduation-cap' },
      class: { icon: 'fa-light fa-users', max_children: 0 },
    },
    search: { show_only_matches: true, show_only_matches_children: true },
  }).on('changed.jstree ready.jstree', () => {
    const tree = $el.jstree(true);
    const classes = tree.get_selected(true).filter((n) => n.type === 'class');
    $('#tree-count').text(classes.length);
    $('#tree-selected').val(classes.map((n) => n.id.replace(/^t-/, '')).join(','));
    $('#tree-apply').prop('disabled', classes.length === 0);
  });

  let timer;
  $('#tree-search').on('input', function () {
    clearTimeout(timer);
    const q = this.value.trim();
    timer = setTimeout(() => (q ? $el.jstree(true).search(q) : $el.jstree(true).clear_search()), 250);
  });
}

$(() => { if ($('#tree-classes').length) initClassTree(); });
```

### SQL

Uma consulta devolve todos os nós já no formato plano do jsTree (`id`/`parent` com prefixo de tipo para não colidir uuids), com a contagem de alunos ativos por turma:

```sql
SELECT CONCAT('u-', u.uuid) AS id, '#' AS parent, u.name AS text, 'unit' AS type,
       NULL AS students, 0 AS disabled, u.name AS sort1, '' AS sort2, '' AS sort3
  FROM units u
 WHERE u.tenant_id = :tenant_id AND u.status = 'active'
UNION ALL
SELECT CONCAT('c-', c.uuid), CONCAT('u-', c.unit_uuid), c.name, 'course',
       NULL, c.is_active = 0, u.name, c.name, ''
  FROM courses c
  JOIN units u ON u.uuid = c.unit_uuid
 WHERE c.deleted_at IS NULL AND u.tenant_id = :tenant_id2
UNION ALL
SELECT CONCAT('t-', cl.uuid), CONCAT('c-', cl.course_uuid), cl.name, 'class',
       (SELECT COUNT(*) FROM enrollments e
         WHERE e.class_uuid = cl.uuid AND e.status = 'active' AND e.deleted_at IS NULL),
       cl.is_active = 0, u.name, c.name, cl.name
  FROM classes cl
  JOIN courses c ON c.uuid = cl.course_uuid AND c.deleted_at IS NULL
  JOIN units u   ON u.uuid = cl.unit_uuid
 WHERE cl.deleted_at IS NULL AND u.tenant_id = :tenant_id3
 ORDER BY sort1, sort2, sort3;
```

Não é preciso CTE recursiva: a hierarquia tem 3 níveis fixos ligados por `unit_uuid` e `course_uuid`. O controller devolve as linhas em JSON (sem as colunas `sort*`); para árvores grandes, carregue só unidades e use `core.data` como função para buscar cursos/turmas no `open_node`. Filtre as unidades pelo escopo do usuário (unidades a que tem acesso).

## Faça / Não faça

- **Faça:** prefixar ids por tipo (`u-`, `c-`, `t-`) e enviar ao servidor só os uuids de turma (`get_selected` filtrado).
- **Faça:** revalidar no servidor que as turmas pertencem às unidades permitidas ao usuário.
- **Faça:** escapar `text` (jsTree insere como HTML).
- **Não faça:** usar o sprite de checkbox padrão no tema escuro.
- **Não faça:** carregar milhares de turmas de uma vez sem lazy load.
- **Não faça:** misturar plugin `dnd` com seleção por checkbox na mesma árvore.
