# jKanban Board

Quadro kanban com jKanban 1.3.1 (dragula embutido) para solicitações com status — colunas vindas de `kanban_boards.columns_cfg`, cartões arrastáveis entre colunas, botão “+” por coluna e tema ligado aos tokens.

## Quando usar

- Fluxos curtos de **status** com poucas dezenas de cartões por coluna: solicitações de SST (`smt_kanban_tasks`), tarefas de marketing (`mkt_kanban_tasks`), almoxarifado (`wms_kanban_tasks`).
- Quando as colunas são configuráveis por tenant (`kanban_boards`) e mover o cartão = trocar `kanban_status`.
- **Não use** para pipelines grandes com busca/paginação por coluna, recolher colunas e teclado completo: use o kanban nativo do chassi `SoftCloud.KanbanBoard` (`assets/js/ttsc.kanban-board.js` + `ttsc.kanban.css`, arquétipo [PagePipeline](../PagePipeline/README.md)).
- **Não use** para só reordenar itens de uma lista (sem colunas de status): [Draggable](../Draggable/README.md).
- Para histórico do que mudou num cartão use [Timeline](../Timeline/README.md).

## Anatomia

```
.ttsc-jkanban  (#kb-board, overflow-x auto)
└── .kanban-container
    └── .kanban-board[data-id="waiting"].kb-col-waiting
        ├── header  ● .kanban-title-board "Aguardando 2"     [+]  (itemAddOptions)
        └── main.kanban-drag
            └── .kanban-item[data-eid="<uuid>"][data-priority]  título · prazo · badge de prioridade
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Container | elemento de `element` dentro de `.ttsc-jkanban` | sim |
| Coluna | `.kanban-board[data-id=<kanban_status>]` + `class` do board (`kb-col-<status>`) | sim |
| Título | `.kanban-title-board` (nome + contador) | sim |
| Adicionar | botão em `header` (`itemAddOptions.enabled`) com `aria-label` | não |
| Cartão | `.kanban-item[data-eid]` (+ `data-*` de propriedades extras) | sim |
| Área de soltar | `.kanban-drag` | gerado |

## Variantes

| Coluna (`kanban_status`) | Rótulo | Ponto | Token |
|---|---|---|---|
| `waiting` | Aguardando | cinza | `ttsc-meta` |
| `in_progress` | Em andamento | azul | `ttsc-info` |
| `blocked` | Bloqueado | vermelho | `ttsc-danger` |
| `done` | Concluído | verde | `ttsc-success` |

| Prioridade (`priority`) | Badge |
|---|---|
| `normal` | `ttsc-badge-secondary` “Normal” |
| `urgent` | `ttsc-badge-warning` “Urgente” |
| `critical` | `ttsc-badge-destructive` “Crítica” |

Superfícies: coluna `ttsc-canvas-2` + borda `ttsc-border-soft`; cartão `ttsc-surface` + `ttsc-border` + `ttsc-shadow-xs`; espelho `ttsc-shadow-lg` + `ttsc-accent-border`.

## API

### Opções (`new jKanban({...})`)

| Opção | Padrão | Valor TTSC |
|---|---|---|
| `element` | `''` | `'#kb-board'` |
| `gutter` / `widthBoard` | `'15px'` / `'250px'` | `'6px'` / `'240px'` |
| `responsivePercentage` | `false` | `false` (rolagem horizontal) |
| `dragItems` / `dragBoards` | `true` / `true` | `true` / `false` (ordem vem do `columns_cfg`) |
| `boards` | `[]` | `[{ id, title, class, dragTo?, item: [{ id, title, ...props }] }]` |
| `itemAddOptions` | `{ enabled: false, content: '+', class, footer }` | `enabled: true`, `class: 'ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm'` |
| `itemHandleOptions` | `{ enabled: false, … }` | `false` (cartão inteiro arrasta) |
| `click(el)` | — | abre o drawer da solicitação |
| `dragEl(el, source)` / `dragendEl(el)` | — | — |
| `dropEl(el, target, source, sibling)` | — | **PATCH do status** |
| `buttonClick(el, boardId)` | — | criar solicitação na coluna |

`boards[].dragTo: ['in_progress']` restringe destinos (ex.: “Concluído” só a partir de “Em andamento”).

### Métodos

| Método | Uso |
|---|---|
| `addElement(boardId, item, position?)` | inserir cartão |
| `findElement(id)` / `replaceElement(id, item)` / `removeElement(id)` | atualizar após salvar |
| `getParentBoardID(id)` | coluna atual |
| `moveElement(targetBoardId, id, item)` | desfazer movimento que falhou |
| `getBoardElements(boardId)` | contagem por coluna |
| `addBoards([...])` / `findBoard(id)` / `removeBoard(id)` | colunas dinâmicas |
| `addForm(boardId, formEl)` | formulário inline |

## Acessibilidade

- O jKanban (dragula) não move por teclado. Cada cartão deve ser focável (`tabindex="0"`, `role="listitem"`) e o `click`/Enter abre o drawer, onde o status é um `<select>` — essa é a alternativa obrigatória.
- Anuncie movimentos em `aria-live="polite"` (“Cartão movido de Aguardando para Em andamento”).
- Botão “+” só-ícone com `aria-label="Adicionar solicitação"`.
- Coluna identificada por texto + cor; prioridade com texto no badge (nunca só a cor do ponto).

## Modelos

### HTML

```html
<div class="ttsc-card">
  <div class="ttsc-card-header">
    <h3 class="ttsc-card-title">Solicitações — Saúde e Segurança do Trabalho</h3>
    <span class="text-xs" id="kb-log" aria-live="polite"></span>
  </div>
  <div class="ttsc-card-content">
    <div class="ttsc-jkanban" id="kb-board"
         data-columns='<?= $this->e($board['columns_cfg']) ?>'
         data-list-url="/admin/smt/kanban/tasks" data-move-url="/admin/smt/kanban/tasks"></div>
  </div>
</div>
<link rel="stylesheet" href="/assets/vendors/jkanban/jkanban.min.css">
<script src="/assets/vendors/jkanban/jkanban.min.js"></script>
<script src="/assets/js/core/ttsc.jkanban.js"></script>
```

### CSS

```css
.ttsc-jkanban { overflow-x: auto; padding-bottom: var(--ttsc-space-1); }
.ttsc-jkanban .kanban-board { background: var(--ttsc-canvas-2); border: 1px solid var(--ttsc-border-soft); border-radius: var(--ttsc-radius-surface); }
.ttsc-jkanban .kanban-board header { display: flex; align-items: center; gap: 8px; padding: 10px 12px; font-size: 13px; }
.ttsc-jkanban .kanban-title-board { flex: 1; display: flex; align-items: center; gap: 6px; font-weight: 600; color: var(--ttsc-text); }
.ttsc-jkanban .kanban-title-board::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--col, var(--ttsc-meta)); }
.ttsc-jkanban .kanban-drag { min-height: 120px; padding: 8px; display: flex; flex-direction: column; gap: 8px; }
.ttsc-jkanban .kanban-item { background: var(--ttsc-surface); color: var(--ttsc-text); border: 1px solid var(--ttsc-border);
  border-radius: var(--ttsc-radius-control); padding: 10px; margin: 0; box-shadow: var(--ttsc-shadow-xs); font-size: 12px; cursor: grab; }
.ttsc-jkanban .kanban-item:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.ttsc-jkanban .kanban-item.is-moving.gu-mirror { box-shadow: var(--ttsc-shadow-lg); border-color: var(--ttsc-accent-border); }
.kb-col-waiting { --col: var(--ttsc-meta); }    .kb-col-in_progress { --col: var(--ttsc-info); }
.kb-col-blocked { --col: var(--ttsc-danger); }  .kb-col-done { --col: var(--ttsc-success); }
```

### JS

```js
// assets/js/core/ttsc.jkanban.js — requer jkanban.min.js (dragula embutido)
const PRIORITY = { normal: ['Normal', 'ttsc-badge-secondary'], urgent: ['Urgente', 'ttsc-badge-warning'], critical: ['Crítica', 'ttsc-badge-destructive'] };
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fmtDate = (d) => (d ? d.split('-').reverse().slice(0, 2).join('/') : '—');

const cardHtml = (t) => {
  const [label, cls] = PRIORITY[t.priority] || PRIORITY.normal;
  return `<div class="kb-title">${esc(t.title)}</div>
    <div class="kb-meta"><span><i class="fa-light fa-calendar"></i>${fmtDate(t.due_date)}</span>
    <span class="ttsc-badge ttsc-badge-sm ttsc-badge-outline ${cls}">${label}</span></div>`;
};

export async function initJKanban(el = document.getElementById('kb-board')) {
  const cfg = JSON.parse(el.dataset.columns);                    // kanban_boards.columns_cfg
  const token = document.querySelector('meta[name="csrf-token"]')?.content || '';
  const log = document.getElementById('kb-log');
  const res = await fetch(`${el.dataset.listUrl}?per_page=200`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
  const { data: tasks = [] } = await res.json();
  const title = (key) => cfg.columns.find((c) => c.key === key)?.title || key;

  const kanban = new jKanban({
    element: `#${el.id}`, gutter: '6px', widthBoard: '240px', responsivePercentage: false, dragBoards: false,
    itemAddOptions: { enabled: true, content: '<i class="fa-light fa-plus"></i>', class: 'ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm', footer: false },
    boards: cfg.columns.map((c) => ({
      id: c.key, title: c.title, class: `kb-col-${c.key}`,
      item: tasks.filter((t) => t[cfg.status_field] === c.key).map((t) => ({ id: t.uuid, title: cardHtml(t), priority: t.priority })),
    })),
    click: (item) => document.dispatchEvent(new CustomEvent('ttsc:smt-task-open', { detail: { uuid: item.dataset.eid } })),
    dropEl: async (item, target, source) => {
      const to = target.parentElement.dataset.id;
      const from = source.parentElement.dataset.id;
      if (to === from) return;
      const r = await fetch(`${el.dataset.moveUrl}/${encodeURIComponent(item.dataset.eid)}/move`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', 'X-CSRF-TOKEN': token },
        body: JSON.stringify({ kanban_status: to }),
      }).then((x) => x.json()).catch(() => ({ success: false }));
      if (!r.success) {
        kanban.moveElement(from, item.dataset.eid, { id: item.dataset.eid, title: item.innerHTML });   // desfaz
        TTSC.Toast?.show({ message: 'Não foi possível mover a solicitação.', variant: 'destructive' });
        return;
      }
      if (log) log.textContent = `Solicitação movida de "${title(from)}" para "${title(to)}".`;
    },
    buttonClick: (btn, boardId) => document.dispatchEvent(new CustomEvent('ttsc:smt-task-create', { detail: { status: boardId } })),
  });

  el.querySelectorAll('.kanban-item').forEach((i) => { i.tabIndex = 0; i.setAttribute('role', 'listitem'); });
  el.querySelectorAll('.kanban-board header button').forEach((b) => b.setAttribute('aria-label', 'Adicionar solicitação'));
  el.addEventListener('keydown', (e) => { if (e.key === 'Enter' && e.target.classList.contains('kanban-item')) e.target.click(); });
  return kanban;
}

document.addEventListener('DOMContentLoaded', () => { if (document.getElementById('kb-board')) initJKanban(); });
```

### SQL

`kanban_boards` guarda a configuração das colunas por entidade (JSON validado por `CHECK (json_valid)`); as tarefas vêm da tabela da entidade — aqui `smt_kanban_tasks` (`kanban_status`: `waiting`, `in_progress`, `blocked`, `done`; `priority`: `normal`, `urgent`, `critical`).

```sql
-- Configuração do quadro (padrão do tenant para a entidade)
SELECT kb.id, kb.name, kb.columns_cfg
  FROM kanban_boards kb
 WHERE kb.tenant_id = :tenant_id
   AND kb.entity = 'smt_kanban_tasks'
 ORDER BY kb.is_default DESC, kb.created_at
 LIMIT 1;

-- columns_cfg de exemplo (INSERT na criação do tenant)
INSERT INTO kanban_boards (id, tenant_id, entity, name, columns_cfg, is_default, created_by)
VALUES (:id, :tenant_id, 'smt_kanban_tasks', 'Solicitações SST',
        '{"status_field":"kanban_status","columns":[{"key":"waiting","title":"Aguardando"},{"key":"in_progress","title":"Em andamento"},{"key":"blocked","title":"Bloqueado"},{"key":"done","title":"Concluído","collapsed_after_days":30}]}',
        1, :user_uuid);

-- Cartões: abertos + concluídos nos últimos 30 dias, prioridade e prazo primeiro
SELECT t.uuid, t.title, t.kanban_status, t.priority, t.task_type, t.due_date, t.responsible_user_id
  FROM smt_kanban_tasks t
 WHERE t.tenant_id = :tenant_id
   AND t.is_deleted = 0
   AND t.deleted_at IS NULL
   AND (t.kanban_status <> 'done' OR t.completed_at >= CURRENT_DATE - INTERVAL 30 DAY)
 ORDER BY FIELD(t.priority, 'critical', 'urgent', 'normal'), t.due_date IS NULL, t.due_date, t.id;

-- Mover (dropEl → PATCH …/{uuid}/move)
UPDATE smt_kanban_tasks
   SET kanban_status = :status,
       completed_at  = CASE WHEN :status_chk = 'done' THEN NOW() ELSE NULL END,
       completed_by  = CASE WHEN :status_chk2 = 'done' THEN :user_id ELSE NULL END
 WHERE uuid = :uuid
   AND tenant_id = :tenant_id
   AND is_deleted = 0
   AND deleted_at IS NULL;
```

O PHP valida `:status` contra as `key` do `columns_cfg` antes do `UPDATE`, devolve `{"success": true}` e registra a mudança em `audit_logs`. O `columns_cfg` vai cru em `data-columns` (escapado) e as tarefas chegam por JSON (`{success, data:[…]}`, mesmo formato do `SmtKanban.reload()` atual).

## Faça / Não faça

- **Faça:** colunas e rótulos a partir de `kanban_boards.columns_cfg`, nunca fixos no JS.
- **Faça:** desfazer o movimento (`moveElement`) quando o PATCH falhar e avisar com [Toast](../Toast/README.md).
- **Faça:** escapar o título dos cartões (o `title` do jKanban é HTML).
- **Não faça:** usar `prompt()`/`alert()` para criar cartões (como o `ttsc.smt.kanban.js` atual) — abra o drawer.
- **Não faça:** carregar milhares de cartões no jKanban; acima de ~200 use `SoftCloud.KanbanBoard` com paginação por coluna.
- **Não faça:** permitir `dragBoards` quando a ordem das colunas é configuração do tenant.
