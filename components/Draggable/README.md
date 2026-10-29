# Draggable

Reordenação por arrastar com @shopify/draggable 1.0.0-beta.12 (`Draggable.Sortable`) — cards de painel, séries, etapas — com alça, espelho (mirror), alternativa de teclado e gravação da nova ordem.

## Quando usar

- Reordenar itens **dentro de uma lista**: cards do painel do usuário, ordem das séries (`series.sequence_order`), etapas de aprovação, perguntas de prova.
- Quando a ordem é uma preferência ou um dado de configuração que precisa ser persistido logo após soltar.
- **Não use** para mover cartões entre colunas com status (pipeline, solicitações): use [Kanban](../Kanban/README.md) (jKanban), que já trata colunas e eventos de drop.
- **Não use** para soltar arquivos: [Dropzone](../Dropzone/README.md). Para arrastar livre entre áreas sem ordenação, veja [DragAndDrop](../DragAndDrop/README.md).
- **Não use** quando há só 2–3 itens: botões “subir/descer” são mais claros.

## Anatomia

```
.dg-grid  (container passado ao Sortable)
├── .dg-card [data-card-id] tabindex=0      ← draggable
│   └── .dg-head  "Matrículas ativas"  .dg-handle (fa-grip-dots-vertical)  ← handle
├── .dg-card.draggable-source--is-dragging  ← placeholder (vazio, borda tracejada)
└── .dg-card.draggable-mirror              ← cópia que segue o ponteiro (fixed, sombra)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Container | elemento passado a `new Draggable.Sortable(container, …)` | sim |
| Item | seletor de `draggable` (`.dg-card`) + `data-card-id` | sim |
| Alça | seletor de `handle` (`.dg-handle`, ícone `fa-grip-dots-vertical`) | recomendado |
| Foco | `tabindex="0"` + `aria-roledescription="card reordenável"` | sim |
| Região de anúncio | `aria-live="polite"` com a nova posição | sim |

## Estados

| Estado | Classe (aplicada pelo plugin) | Tokens |
|---|---|---|
| Arrastando (origem) | `.draggable-source--is-dragging` | fundo `ttsc-accent-soft`, borda tracejada `ttsc-accent-border` |
| Espelho | `.draggable-mirror` | `ttsc-shadow-lg`, borda `ttsc-accent-border`, z `ttsc-z-popover` |
| Container ativo | `.draggable-container--is-dragging` | — |
| Solto | `.draggable-source--placed` (temporário) | flash `ttsc-accent-soft` |
| Foco teclado | `:focus-visible` | contorno 2px `ttsc-accent` |

## API

### Opções

| Opção | Valor TTSC | Descrição |
|---|---|---|
| `draggable` | `'.dg-card'` | itens arrastáveis (padrão `.draggable-source`) |
| `handle` | `'.dg-handle'` | só a alça inicia o arraste (texto continua selecionável) |
| `mirror` | `{ constrainDimensions: true }` | espelho com o tamanho do item; `appendTo`, `xAxis`, `yAxis` |
| `delay` | `{ mouse: 0, drag: 0, touch: 150 }` | evita arrastar ao rolar no celular |
| `distance` | `4` | px antes de iniciar |
| `classes` | `{ 'source:dragging': '…' }` | renomear classes de estado |
| `plugins` / `swapAnimation` | `[Draggable.Plugins.SwapAnimation]` | animação de troca |

### Eventos (`sortable.on(nome, fn)`)

| Evento | Dados | Uso |
|---|---|---|
| `sortable:start` | `startIndex`, `startContainer`, `cancel()` | bloquear itens fixos |
| `sortable:sort` | `currentIndex`, `over`, `cancel()` | validar destino |
| `sortable:sorted` | `oldIndex`, `newIndex`, `dragEvent` | feedback durante o arraste |
| `sortable:stop` | `oldIndex`, `newIndex`, `oldContainer`, `newContainer` | **gravar a ordem** (após `setTimeout(0)` o DOM já está final) |
| `drag:start` / `drag:stop` / `mirror:created` | — | eventos do Draggable base |

### Métodos

| Método | Uso |
|---|---|
| `sortable.destroy()` | ao remover o painel (navegação parcial) |
| `sortable.addContainer(el)` / `removeContainer(el)` | listas dinâmicas |
| `sortable.on/off(evento, fn)` | assinaturas |
| `sortable.index(el)` / `getDraggableElementsForContainer(c)` | posição atual |

## Acessibilidade

- O Draggable **não** reordena por teclado: implemente Alt+↑/↓ (ou botões “Mover para cima/baixo” num menu) no item focado, como no modelo JS.
- Anuncie a mudança em `aria-live="polite"`: “Receita do mês movido para a posição 3”.
- Alça com `aria-hidden` (o item inteiro é focável) e ícone visível em `ttsc-text-muted` (hover `ttsc-text`).
- Não dependa só da cor do placeholder: ele também tem borda tracejada.

## Modelos

### HTML

```html
<div class="dg-grid" id="dashboard-cards" data-save-url="/admin/dashboard/card-order"
     aria-label="Cards do painel, reordenáveis">
  <?php foreach ($cards as $card): ?>
    <article class="ttsc-card dg-card" tabindex="0" data-card-id="<?= $this->e($card['id']) ?>"
             aria-roledescription="card reordenável">
      <div class="dg-head">
        <?= $this->e($card['title']) ?>
        <span class="dg-handle" aria-hidden="true"><i class="fa-light fa-grip-dots-vertical"></i></span>
      </div>
      <?= $this->insert('app::partials.kpi_value', ['card' => $card]) ?>
    </article>
  <?php endforeach; ?>
</div>
<div class="ttsc-sr-only" aria-live="polite" id="dashboard-cards-status"></div>
```

### CSS

```css
.dg-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--ttsc-space-3); }
/* região de anúncio invisível (o runtime não tem sr-only) */
.ttsc-sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.dg-handle { cursor: grab; color: var(--ttsc-text-muted); padding: 2px 4px; border-radius: var(--ttsc-radius-xs); }
.dg-handle:hover { background: var(--ttsc-canvas-2); color: var(--ttsc-text); }
.dg-card:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.dg-card.draggable-source--is-dragging { background: var(--ttsc-accent-soft); border: 1px dashed var(--ttsc-accent-border); }
.dg-card.draggable-source--is-dragging > * { visibility: hidden; }
.dg-card.draggable-mirror { box-shadow: var(--ttsc-shadow-lg); border-color: var(--ttsc-accent-border); z-index: var(--ttsc-z-popover); cursor: grabbing; }
.dg-card.draggable-source--placed { animation: dg-placed .4s ease; }
@keyframes dg-placed { from { background: var(--ttsc-accent-soft); } to { background: var(--ttsc-surface); } }
```

### JS

```js
// assets/js/core/ttsc.sortable-cards.js — requer /assets/vendors/draggable/draggable.bundle.js (global Draggable)
export function initSortableCards(board) {
  const status = document.getElementById(`${board.id}-status`);
  const token = document.querySelector('meta[name="csrf-token"]')?.content || '';
  const order = () => [...board.querySelectorAll('.dg-card:not(.draggable-mirror):not(.draggable--original)')]
    .map((card) => card.dataset.cardId);

  let saveTimer;
  const save = (message) => {
    if (status) status.textContent = message;
    clearTimeout(saveTimer);
    saveTimer = setTimeout(async () => {
      const res = await fetch(board.dataset.saveUrl, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', 'X-CSRF-TOKEN': token },
        body: JSON.stringify({ card_order: order() }),
      });
      if (!res.ok) TTSC.Toast?.show({ message: 'Não foi possível salvar a ordem.', variant: 'destructive' });
    }, 300);
  };

  const sortable = new Draggable.Sortable(board, {
    draggable: '.dg-card',
    handle: '.dg-handle',
    mirror: { constrainDimensions: true },
    delay: { mouse: 0, drag: 0, touch: 150 },
  });
  sortable.on('sortable:stop', (event) => {
    if (event.oldIndex === event.newIndex) return;
    setTimeout(() => save(`Card movido para a posição ${event.newIndex + 1}`), 0);
  });

  // Teclado: Alt + setas no card focado
  board.addEventListener('keydown', (event) => {
    const card = event.target.closest('.dg-card');
    if (!card || !event.altKey) return;
    const back = event.key === 'ArrowUp' || event.key === 'ArrowLeft';
    const fwd = event.key === 'ArrowDown' || event.key === 'ArrowRight';
    if (back && card.previousElementSibling) board.insertBefore(card, card.previousElementSibling);
    else if (fwd && card.nextElementSibling) board.insertBefore(card.nextElementSibling, card);
    else return;
    event.preventDefault();
    card.focus();
    save(`Card movido para a posição ${order().indexOf(card.dataset.cardId) + 1}`);
  });
  return sortable;
}

document.querySelectorAll('[data-save-url]#dashboard-cards').forEach(initSortableCards);
```

### SQL

A ordem dos cards é preferência do usuário (JSON em `user_preferences.dashboard_settings`); a ordem de cadastros (ex.: séries) é coluna da própria tabela:

```sql
-- Cards do painel: grava o array recebido (JSON validado no PHP: só ids conhecidos)
UPDATE user_preferences
   SET dashboard_settings = JSON_SET(COALESCE(dashboard_settings, '{}'),
                                     '$.card_order', JSON_EXTRACT(:card_order_json, '$'))  -- '["kpi-revenue","kpi-enrollments",…]'
 WHERE user_uuid = :user_uuid;

-- Leitura ao montar o painel
SELECT JSON_EXTRACT(dashboard_settings, '$.card_order') AS card_order
  FROM user_preferences
 WHERE user_uuid = :user_uuid;

-- Ordem das séries: um UPDATE com CASE, numa transação (uuids vindos do array, na ordem nova)
UPDATE series
   SET sequence_order = CASE uuid
                          WHEN :uuid_1 THEN 1
                          WHEN :uuid_2 THEN 2
                          WHEN :uuid_3 THEN 3
                          ELSE sequence_order
                        END
 WHERE uuid IN (:uuid_1, :uuid_2, :uuid_3)
   AND deleted_at IS NULL;
```

O PHP monta o `CASE` com um placeholder por item (nunca concatenando o uuid), roda dentro de `beginTransaction()` e responde `204`. Ao renderizar, o controller ordena `$cards` pela `card_order` salva e anexa ao fim os cards novos que ainda não estão no array.

## Faça / Não faça

- **Faça:** use alça (`handle`) em cards com links ou texto selecionável.
- **Faça:** grave a ordem no `sortable:stop` com debounce e devolva erro com [Toast](../Toast/README.md).
- **Faça:** ofereça a alternativa de teclado e anuncie a nova posição.
- **Não faça:** gravar a cada `sortable:sorted` (dispara várias vezes por arraste).
- **Não faça:** confiar nos ids enviados — valide contra a lista de cards/séries do tenant.
- **Não faça:** usar `Sortable` para trocar status entre colunas — isso é [Kanban](../Kanban/README.md).
