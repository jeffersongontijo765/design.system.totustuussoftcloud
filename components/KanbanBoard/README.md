# KanbanBoard

Quadro Kanban v2.3 do chassi (`SoftCloud.KanbanBoard.mount`): colunas por etapa com contagem e soma, chips de etapa, busca e paginação por coluna, arrastar e soltar (mouse, toque e teclado), recolher/expandir e reordenar colunas com persistência.

## Quando usar

- Somente quando a entidade tem **etapas reais de ciclo de vida** e mover um item muda o `status` no banco: funil de rematrícula (`enrollment_requests`), diplomas, solicitações, recuperação.
- A aba só existe se `StandardPageRegistry::tabsFor($rota)['kanban']` for `true` (regra curada ou palavras como `requests`, `approvals`, `pipeline`, `workflow`) ou se a fonte curada tiver ≥ 2 status (`$curatedLifecycle`). Hoje são 190 rotas da sidebar com Kanban.
- Não use para listas sem fluxo (cursos, unidades, parâmetros), logs ou relatórios — o chassi mostra o painel "Kanban não se aplica" e a lista fica na [RecordsTable](../RecordsTable/README.md).
- Arquétipo de página que abre no quadro: [PagePipeline](../PagePipeline/README.md).

## Anatomia

```
┌ .skb ─────────────────────────────────────────────────────────────────────────┐
│ ▦ Funil de matrícula (48 Matrículas)                  Valor no quadro: R$ …   │ .skb-head
│ Etapas do ciclo [● Pré-matrícula 6][● Documentação 7]…[Todas as etapas] [+N] «» │ .skb-stages
│ ┌ .skb-col (--c: tom) ┐ ┌ .skb-col ┐ ┌ … ┐                    [+ Nova etapa]   │ .skb-board
│ │‹ ● Pré-matrícula 6  R$│ │          │                                          │ .skb-col-head
│ │[⌕ Buscar nesta etapa]│ │          │                                          │ .skb-tools
│ │┌ .skb-card ────────┐│ │          │                                          │
│ ││MAT-1003           ││ │          │                                          │
│ ││João Pereira       ││ │          │                                          │
│ ││▣ Téc. Enfermagem  ││ │          │                                          │
│ ││R$ 1.375,29  10 jun││ │          │                                          │
│ │└───────────────────┘│ │          │                                          │
│ │[+ Adicionar]         │ │          │                                          │
│ │« ‹ Página [1] de 1 › »  [10 por página ▾]                                    │ .skb-pager
└───────────────────────────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Host | qualquer `div` (`#domain-kanban-board.ttsc-chassis-kanban`, `#model-kanban`); recebe `.skb` (+ `.is-reorderable`) | sim |
| Cabeçalho | `.skb-head`, `.skb-pill[data-total]`, `.skb-value b[data-value]` | gerado |
| Chips | `.skb-chips[data-chips] > .skb-chip[data-goto-col]`, `.skb-chip.is-all`, `.skb-chip.is-more` + `.skb-chips-menu` | gerado |
| Coluna | `.skb-col[data-id][style="--c:<cor>"]`, `.is-collapsed` | gerado |
| Cabeçalho da coluna | `.skb-collapse[data-act=collapse][aria-expanded]`, `.skb-count[data-count]`, `.skb-sum[data-sum]` | gerado |
| Busca | `.skb-search input[data-q]` | gerado |
| Cartão | `article.skb-card[tabindex=0][data-id][data-col]` com `.skb-code`, `.skb-prob`, `.skb-title`, `.skb-org`, `.skb-val`, `.skb-date` | gerado |
| Adicionar | `[data-addbox] .skb-add[data-act=add]` (omitido com `readOnly`) | não |
| Paginação | `.skb-pager` com `first/prev/next/last`, `input[data-goto]`, `select[data-size]` | gerado |
| Nova etapa | `.skb-addcol[data-addcol]` (com `allowNewStage`) | não |

## Estados

| Estado | Como |
|---|---|
| Carregando coluna | `.skb-list.is-loading` (com `provider`) |
| Coluna vazia | `.skb-empty` "Nenhum item nesta etapa" / "Nenhum resultado para “…”" |
| Recolhida | `.skb-col.is-collapsed` (persistido em `localStorage['skb:<id>']`) |
| Arrastando | `.skb-card.is-dragging` + alvo de soltura; coluna reordenando: `.skb-coldrop` |
| Somente leitura | `readOnly:true` — sem "Adicionar", sem arrastar, sem Alt+setas |
| Não se aplica | painel `.ttsc-chassis-empty-card` "Kanban não se aplica" (sem etapas) |

## API

**`SoftCloud.KanbanBoard.mount(el, options)` → instância** (`assets/js/ttsc.kanban-board.js`)

| Opção | Padrão | Descrição |
|---|---|---|
| `id` | `'board'` | chave de persistência (`localStorage['skb:'+id]`: recolhidas + ordem) |
| `title`, `subtitle` | `'Kanban Board'`, `''` | cabeçalho |
| `unit` | `'Opportunities'` | palavra da pill total |
| `currency` | `'R$'` | prefixo literal dos valores (`''` esconde somas) |
| `columns` | `[]` | `[{id, title, tone, items:[{id, code, title, org, value, date, prob}], total?, sum?}]` |
| `pageSize`, `pageSizes` | `10`, `[5,10,25,50]` | paginação por coluna |
| `debounce` | `250` | ms da busca por coluna |
| `persist` | `true` | salvar recolhidas/ordem |
| `provider` | `null` | `(colId, {page, size, q}) => Promise<{items, total, all, sum}>` — carrega cada página do servidor |
| `allowNewStage` | `true` | botão "+ Nova etapa" |
| `allowColumnReorder` | `true` | arrastar cabeçalhos (v2.3) |
| `readOnly` | `false` | desliga edição |
| `addLabel` | `'Add item'` | rótulo do "+" |
| `strings` | inglês | `stages, all, boardValue, search, noItems, noResults, page, of, perPage, newStage, stageName, create, cancel, add, title, value, collapse, expand, showing, movedTo` |

`tone`: `slate`, `blue`, `amber`, `purple`, `emerald`, `rose`, `indigo` (ou uma cor CSS). `SoftCloud.KanbanBoard.TONES` expõe o mapa.

| Método da instância | Efeito |
|---|---|
| `el`, `columns` | host e estado das colunas |
| `addItem(colId, item)` | insere no topo e redesenha |
| `setItems(colId, items)` | troca os itens e volta à página 1 |
| `refresh(colId?)` | redesenha uma ou todas |
| `collapse(colId, bool)` | recolhe/expande |
| `addStage({id, title, tone, items})` | acrescenta coluna |

| Evento (no host, `bubbles`) | `detail` | Cancelável |
|---|---|---|
| `skb:move` | `{item, itemId, from, to}` | sim — `preventDefault()` devolve o cartão |
| `skb:add` | `{column, item:{title, value}}` | sim — o chassi cancela e abre o drawer de criação |
| `skb:addcol` | `{column:{title, tone}}` | sim — o chassi grava no vocabulário antes de criar |
| `skb:reorder` | `{columns:[{id, title}]}` | não |
| `skb:page` | `{column, page, size?}` | não |
| `skb:collapse` | `{column, collapsed}` | não |

**Ficha**: `stages[]` (`id`, `label`, `tone`), `stageField`, `kanbanTitle`, `kanbanDesc`, `kanbanValue` (campo `money` somado), `kanbanDate`, `codeField`, `subField` (linha `org`), `endpoints.move`.

**Endpoints (`DomainCrudController`)**

| Método | Rota | Corpo / resposta |
|---|---|---|
| POST | `/api/v1/domain/records{rota}/status` | `{id, status}` (uuid ou PK; status de `known_statuses`) → `{success, status}`; 404 se não existe; 422 se status inválido ou tabela sem `status` |
| POST | `/api/v1/domain/records{rota}/statuses` | `{label}` → `{success, value, label}` — nova etapa no `ref_enum_*` (só rail developer) |
| POST | `/api/v1/domain/records{rota}` | criação vinda do "+ Adicionar" via drawer |
| GET | `/api/v1/domain/records{rota}?status=<etapa>&page=&per_page=` | página de uma coluna (para `provider`) |

## Acessibilidade

- Cartões são focáveis (`tabindex="0"`, `role="article"`, `aria-label` = título). **Alt + ← / →** move o cartão para a coluna vizinha (dispara `skb:move`).
- Recolher tem `aria-expanded` e rótulo "Recolher etapa <nome>"; o quadro é `role="list"` e cada coluna `role="listitem"`.
- Busca da coluna: `Esc` limpa; `Enter` no campo de página navega.
- Cores de etapa vêm acompanhadas do nome em todos os pontos (chip, cabeçalho).
- Tokens próprios `--sc-*` em `:root` e `html.dark` (texto `--sc-text` sobre `--sc-surface` ≥ 12:1).

## Modelos

### HTML

1) PHP real (`chassis/domain_page.php`, VIEW 4) — dados em JSON e montagem no cliente:

```php
<div id="view-kanban" class="space-y-4" style="display: none;">
  <?php if ($kanbanEnabled): ?>
  <?php include base_path('resources/views/app/partials/kanban_engine.php'); ?>
  <div id="domain-kanban-board" class="ttsc-chassis-kanban"></div>
  <script type="application/json" id="domain-kanban-data"><?= json_encode([
      'columns' => $kanbanColumns,                       // [{id, title, tone, count}]
      'rows' => array_map(static fn (array $r) => [
          'id' => $recordId($r), 'title' => $recordLabel($r),
          'status' => strtolower(trim((string) ($r[$statusKey] ?? ''))),
      ] + $kanbanExtras($r), $records),                  // + code, org, value, date, prob
  ], JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_APOS | JSON_HEX_QUOT | JSON_HEX_AMP) ?></script>
  <?php else: ?>
  <div class="ttsc-chassis-empty-card">… Kanban não se aplica …</div>
  <?php endif; ?>
</div>
```

`$kanbanEnabled = ($tabsFlags['kanban'] || $curatedLifecycle) && $statusKey !== null && $kanbanColumns !== [] && $records !== []`.

2) HTML gerado (preview; 1 coluna e 1 cartão):

```html
<div id="model-kanban" class="skb is-reorderable">
  <div class="skb-head">
    <div class="skb-head-main"><span class="skb-tile">▦</span>
      <div><div class="skb-title-row"><b>Funil de matrícula</b><span class="skb-pill" data-total="">48 Matrículas</span></div>
        <div class="skb-sub">Pré-matrícula → documentação → análise → matriculado</div></div>
    </div>
    <div class="skb-head-actions"><span class="skb-value"><small>Valor no quadro:</small><b data-value="">BRL 67.740,46</b></span></div>
  </div>
  <div class="skb-stages">
    <span class="skb-stages-label">Etapas do ciclo</span>
    <div class="skb-chips" data-chips="">
      <button type="button" class="skb-chip" data-goto-col="pre_enrollment" style="--c: #64748b"><i></i>Pré-matrícula<em>6</em></button>
      <!-- … documents, review, active, rejected -->
      <button type="button" class="skb-chip is-all" data-act="expand-all">Todas as etapas</button>
    </div>
    <button class="skb-chip is-more" type="button" data-act="stages-more" hidden aria-expanded="false" aria-haspopup="true"></button>
    <div class="skb-chips-menu" data-chips-menu="" hidden></div>
  </div>
  <div class="skb-board" data-board="" role="list">
    <div class="skb-col" role="listitem" data-id="pre_enrollment" style="--c: #64748b" data-sum="BRL 10.013,83">
      <div class="skb-col-head">
        <button class="skb-collapse" type="button" data-act="collapse" aria-expanded="true" title="Recolher etapa" aria-label="Recolher etapa Pré-matrícula">‹</button>
        <span class="skb-dot"></span><span class="skb-col-title">Pré-matrícula</span>
        <span class="skb-count" data-count="">6</span><span class="skb-sum" data-sum="">BRL 10.013,83</span>
      </div>
      <div class="skb-tools">
        <div class="skb-search"><i>⌕</i><input type="search" data-q="" placeholder="Buscar nesta etapa..." aria-label="Buscar nesta etapa..." autocomplete="off"></div>
        <div class="skb-meta"><span data-showing="">Exibindo 1-6</span><span data-matches=""></span></div>
      </div>
      <div class="skb-list" data-list="">
        <article class="skb-card" tabindex="0" role="article" data-id="m2" data-col="pre_enrollment" aria-label="João Pereira">
          <div class="skb-card-top"><span class="skb-code">MAT-1003</span><b class="skb-prob"></b></div>
          <div class="skb-title">João Pereira</div>
          <div class="skb-org"><span>▣</span>Técnico em Enfermagem</div>
          <div class="skb-card-foot"><b class="skb-val">BRL 1.375,29</b><span class="skb-date">10 de jun. de 2026</span></div>
        </article>
      </div>
      <div data-addbox=""><button class="skb-add" type="button" data-act="add">+ Adicionar</button></div>
      <div class="skb-pager" data-pager="">
        <div class="grp">
          <button type="button" data-act="first" aria-label="Primeira página" disabled>«</button>
          <button type="button" data-act="prev" aria-label="Página anterior" disabled>‹</button>
          <span>Página</span><input type="number" data-goto="" min="1" max="1" value="1" aria-label="Número da página"><span>de 1</span>
          <button type="button" data-act="next" aria-label="Próxima página" disabled>›</button>
          <button type="button" data-act="last" aria-label="Última página" disabled>»</button>
        </div>
        <select data-size="" aria-label="Itens por página"><option value="10" selected>10 por página</option>…</select>
      </div>
    </div>
  </div>
</div>
```

O `select[data-size]` é trocado visualmente pelo `ttsc.select.js` (`.ttsc-select-wrapper` + `.ttsc-select-trigger`).

### CSS

`assets/css/ttsc.kanban.css` (classes `.skb-*`). Os tokens `--sc-surface`, `--sc-border`, `--sc-brand`, `--sc-text`, `--sc-r-xl`… ficam em `:root` e são redefinidos em `html.dark` (superfície `#0f172a`/`#1e293b`) — por isso o "fantasma" do arraste também fica escuro. A cor da etapa entra por `--c` em cada coluna e chip.

```css
/* Liga o quadro aos tokens do design system (light e dark seguem os tokens) */
.skb {
  --sc-surface: var(--ttsc-surface);
  --sc-surface-2: var(--ttsc-canvas);
  --sc-border: var(--ttsc-border);
  --sc-brand: var(--ttsc-accent);
  --sc-brand-text: var(--ttsc-accent-text);
  --sc-text: var(--ttsc-text);
  --sc-muted: var(--ttsc-text-muted);
}
.skb-card:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
```

### JS

```js
// Funil de rematrícula com dados do endpoint real e gravação do movimento
const ROUTE = '/academic/enrollment/re-enrollment';
const API = '/api/v1/domain/records' + ROUTE;
const csrf = () => document.querySelector('meta[name="csrf-token"]')?.content || '';
const STAGES = [
  { id: 'submitted', title: 'Enviada', tone: 'slate' },
  { id: 'pending_review', title: 'Em análise', tone: 'amber' },
  { id: 'approved', title: 'Aprovada', tone: 'blue' },
  { id: 'confirmed', title: 'Confirmada', tone: 'emerald' },
  { id: 'rejected', title: 'Indeferida', tone: 'rose' },
];

const host = document.getElementById('domain-kanban-board');
const board = SoftCloud.KanbanBoard.mount(host, {
  id: 'academic-reenrollment',
  title: 'Funil de rematrícula',
  subtitle: 'Enviada → em análise → aprovada → confirmada',
  unit: 'solicitações',
  currency: '',                        // sem coluna de valor
  allowNewStage: false,
  allowColumnReorder: false,
  addLabel: 'Adicionar',
  strings: { stages: 'Etapas do ciclo', all: 'Todas as etapas', search: 'Buscar nesta etapa...', noItems: 'Nenhuma solicitação nesta etapa',
             noResults: 'Nenhum resultado para', page: 'Página', of: 'de', perPage: 'por página', showing: 'Exibindo',
             collapse: 'Recolher etapa', expand: 'Expandir etapa', movedTo: 'movido para' },
  columns: STAGES.map((s) => ({ ...s, items: [] })),
  // cada coluna pagina no servidor
  provider: (colId, { page, size, q }) =>
    fetch(`${API}?status=${encodeURIComponent(colId)}&page=${page}&per_page=${Math.max(10, size)}&search=${encodeURIComponent(q)}`,
      { credentials: 'same-origin' })
      .then((r) => r.json())
      .then((b) => ({
        items: b.records.map((r) => ({ id: r.uuid, title: r.student_name, org: r.course_name, code: r.class_name, date: r.created_at?.slice(0, 10) })),
        total: b.totalRecords, all: b.totalRecords,
      })),
});

host.addEventListener('skb:move', (ev) => {
  const { itemId, from, to } = ev.detail;
  fetch(API + '/status', {
    method: 'POST', credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRF-TOKEN': csrf() },
    body: JSON.stringify({ id: String(itemId), status: to }),
  }).then((r) => { if (!r.ok) throw new Error('HTTP ' + r.status); })
    .catch(() => { board.refresh(from); board.refresh(to); window.showToast?.('Não foi possível salvar o novo status.', 'error'); });
});

host.addEventListener('skb:add', (ev) => {   // nunca cria cartão só na tela
  ev.preventDefault();
  window.openDrawer('drawer-create');
});

host.addEventListener('skb:reorder', (ev) => console.info('ordem', ev.detail.columns.map((c) => c.id)));
```

### SQL

Colunas (contagem e soma da mensalidade por etapa) e a gravação do movimento com auditoria:

```sql
-- Contagem por etapa + soma da mensalidade do curso (valor no quadro)
SELECT er.status,
       COUNT(*)                               AS itens,
       COALESCE(SUM(abr.monthly_tuition), 0)  AS valor
  FROM enrollment_requests er
  LEFT JOIN academic_billing_rules abr ON abr.course_uuid = er.course_uuid AND abr.status = 'active'
 WHERE er.deleted_at IS NULL
   AND er.status IN ('submitted', 'pending_review', 'approved', 'confirmed', 'rejected')
 GROUP BY er.status;

-- Página de uma coluna (provider)
SELECT er.uuid, er.student_name, er.course_name, er.class_name, er.created_at
  FROM enrollment_requests er
 WHERE er.deleted_at IS NULL AND er.status = :status
   AND er.student_name LIKE :q ESCAPE '\\'
 ORDER BY er.priority_order, er.created_at
 LIMIT :limit OFFSET :offset;

-- Mover (skb:move): mesmo UPDATE do DomainCrudController::status(), mais o histórico do funil
UPDATE enrollment_requests
   SET status = :to_status, reviewed_by = :actor_uuid, reviewed_at = NOW()
 WHERE uuid = :uuid AND deleted_at IS NULL;

INSERT INTO enrollment_request_history (uuid, request_uuid, action, old_status, new_status, actor_uuid, actor_name, created_at)
VALUES (UUID(), :uuid, 'status_change', :from_status, :to_status, :actor_uuid, :actor_name, NOW());

-- mesmas colunas do App\Models\Traits\Auditable (code = 'AUDL' + 11 dígitos)
INSERT INTO audit_logs (id, code, uuid, user_id, action, table_name, record_id, old_values, new_values, changed_fields, created_at)
VALUES (UUID(), :audit_code, UUID(), :actor_uuid, 'update', 'enrollment_requests', :uuid,
        JSON_OBJECT('status', :from_status), JSON_OBJECT('status', :to_status), JSON_ARRAY('status'), NOW());
```

Rode o `UPDATE` e os dois `INSERT` na mesma transação; o controlador responde `{success:true, status}` e o cliente só desfaz o cartão em erro. No SSR, o resultado do `GROUP BY` vira `$kanbanColumns` (`count`) e as linhas, `rows`.

## Faça / Não faça

- **Faça:** `readOnly: true` quando a fonte é `writable => false` (o chassi faz isso com `!canWrite`).
- **Faça:** `currency: 'R$'` (como o chassi). O kit do preview passa o código ISO e mostra "BRL 1.375,29" — não copie isso.
- **Faça:** `allowNewStage` só no rail developer: etapas são vocabulário compartilhado (`ref_enum_*`).
- **Não faça:** quadro para entidades sem fluxo; nem cartões criados só no cliente — "+ Adicionar" abre o drawer e grava pelo endpoint.
