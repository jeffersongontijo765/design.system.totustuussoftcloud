# DragAndDrop

Arrastar e soltar nativo do HTML5 no chassi — reordenar itens de uma lista (ex.: fila de espera de vagas) e soltar arquivos numa área de envio — como implementação TTSC em JS puro (`ttsc.dnd.js`), com alternativa completa por teclado.

## Quando usar

- Reordenar listas curtas e médias (até ~100 itens) cuja ordem é dado de negócio: fila de espera (`enrollment_waitlist.position`), ordem de disciplinas, cláusulas de contrato, blocos de layout de documento (`sort_order`).
- Soltar 1–5 arquivos num formulário simples (comprovante, foto), quando não precisa de fila de upload com progresso.
- Para quadros com colunas e muitos cartões use [Kanban](../Kanban/README.md); para ordenar grades e listas aninhadas com animação, o plugin [Draggable](../Draggable/README.md) (`@shopify/draggable`, `Draggable.Sortable`).
- Para upload com fila, progresso, várias requisições e retentativa use [Dropzone](../Dropzone/README.md); campo de arquivo simples sem arrastar: [FileInput](../FileInput/README.md).
- **Não use** arrastar como a única forma de executar a ação — sempre ofereça botões/teclado.

## Anatomia

```
Fila de espera — ADM-2026-1N                      [data-ttsc-sortable]
┌──────────────────────────────────────────────┐
│ ⠿  1  Larissa Gomes         [↑][↓]          │  li[draggable=true][data-ttsc-sortable-item][data-id]
│ ⠿  2  João Pedro Cardoso    [↑][↓]  ← .is-dragging (origem) │
│ ─────────── indicador de soltura ───────────│  .is-drop-before / .is-drop-after
│ ⠿  3  Marcelo Dias          [↑][↓]          │
└──────────────────────────────────────────────┘
┌ [data-ttsc-dropzone] ── Arraste o PDF aqui ou [escolha] ┐   .is-over durante dragover
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Lista | `ol/ul[data-ttsc-sortable]` + `aria-label` | sim |
| Item | `li[data-ttsc-sortable-item][data-id][draggable="true"]` | sim |
| Alça | `[data-ttsc-sortable-handle]` (`fa-grip-dots-vertical`); se existir, só ela inicia o arraste | recomendado |
| Mover (teclado) | botões `[data-ttsc-sortable-up]` / `[data-ttsc-sortable-down]` com `aria-label` | sim |
| Anúncio | `[data-ttsc-sortable-status][aria-live=polite]` | sim |
| Área de soltar | `[data-ttsc-dropzone]` contendo `input[type=file]` | para arquivos |

## Estados

| Estado | Classe | Tokens |
|---|---|---|
| Normal | — | fundo `ttsc-surface`, borda `ttsc-border` |
| Hover da alça | `cursor: grab` | ícone `ttsc-text-muted` → `ttsc-text` |
| Arrastando (origem) | `.is-dragging` | opacidade 40%, borda tracejada `ttsc-border-strong` |
| Destino | `.is-drop-before` / `.is-drop-after` | linha 2px `ttsc-accent` |
| Área de soltar ativa | `.is-over` | borda `ttsc-accent`, fundo `ttsc-accent-soft`, texto `ttsc-accent-text` |
| Arquivo recusado | `.is-rejected` + mensagem | borda `ttsc-danger`, texto `ttsc-danger-text` |
| Salvando | `aria-busy="true"` na lista | itens bloqueados |

## API

Implementação TTSC (`assets/js/core/ttsc.dnd.js`, código no JS abaixo).

| Opção `TTSCSortable` | Atributo | Padrão | Descrição |
|---|---|---|---|
| `handle` | — | `[data-ttsc-sortable-handle]` | seletor da alça |
| `url` | `data-ttsc-sortable-url` | — | endpoint que recebe `{ ids: [...] }` (POST JSON) |

| Método | Descrição |
|---|---|
| `new TTSCSortable(list, opts)` / `TTSCSortable.init(scope)` | instância |
| `order()` | `string[]` com os `data-id` na ordem atual |
| `move(item, delta)` | move por teclado/botão (−1 / +1) |

| Evento | Alvo | `detail` |
|---|---|---|
| `ttsc.sortable.change` | lista | `{ ids, item, from, to }` (índices 0-based) — antes de salvar |
| `ttsc.sortable.saved` / `ttsc.sortable.error` | lista | `{ ids }` / `{ error }` (em erro a ordem anterior é restaurada) |

| Opção `TTSCDropzone` | Atributo | Descrição |
|---|---|---|
| `accept` | `accept` do `input[type=file]` | tipos aceitos (`.pdf,image/*`) |
| `maxSize` | `data-ttsc-dropzone-max` (bytes) | tamanho máximo por arquivo |

| Evento | Alvo | `detail` |
|---|---|---|
| `ttsc.dropzone.files` | área | `{ accepted: File[], rejected: { file, reason }[] }` — os aceitos também vão para `input.files` |

## Acessibilidade

- Arrastar é só atalho: cada item tem botões “Mover para cima/baixo” e aceita `Alt+↑` / `Alt+↓` com foco no item (`tabindex="0"`).
- Toda mudança de posição é anunciada em `aria-live`: “Larissa Gomes movida para a posição 1 de 4”.
- Lista é `ol` (a ordem é o conteúdo); itens com o número da posição visível.
- A área de soltar é um `<label>` do `input[type=file]`: clique, Enter e Espaço abrem o seletor do sistema.
- Indicadores usam forma (linha/borda tracejada), não só cor; `ttsc-accent` aqui é decorativo, o texto usa `ttsc-accent-text`.

## Modelos

### HTML

```html
<ol class="ttsc-sortable" data-ttsc-sortable aria-label="Fila de espera da turma ADM-2026-1N"
    data-ttsc-sortable-url="/academic/waitlist/<?= $this->e($class['uuid']) ?>/reorder">
  <?php foreach ($waitlist as $i => $w): ?>
    <li class="ttsc-sortable-item" data-ttsc-sortable-item data-id="<?= $this->e($w['uuid']) ?>" draggable="true" tabindex="0">
      <span class="ttsc-sortable-handle" data-ttsc-sortable-handle aria-hidden="true"><i class="fa-light fa-grip-dots-vertical"></i></span>
      <span class="ttsc-sortable-pos"><?= $i + 1 ?></span>
      <span class="ttsc-sortable-label"><?= $this->e($w['student_name']) ?></span>
      <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" data-ttsc-sortable-up aria-label="Mover <?= $this->e($w['student_name']) ?> para cima"><i class="fa-light fa-arrow-up"></i></button>
      <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" data-ttsc-sortable-down aria-label="Mover <?= $this->e($w['student_name']) ?> para baixo"><i class="fa-light fa-arrow-down"></i></button>
    </li>
  <?php endforeach ?>
</ol>
<p class="sr-status" data-ttsc-sortable-status aria-live="polite"></p>

<label class="ttsc-dropzone-native" data-ttsc-dropzone data-ttsc-dropzone-max="5242880">
  <input type="file" name="proof" accept=".pdf,image/*" class="sr-input">
  <i class="fa-light fa-cloud-arrow-up" aria-hidden="true"></i>
  <span>Arraste o comprovante aqui ou <u>escolha um arquivo</u></span>
  <small>PDF ou imagem, até 5 MB</small>
</label>
```

### CSS

```css
.ttsc-sortable { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 6px; }
.ttsc-sortable-item {
  position: relative; display: flex; align-items: center; gap: 10px; padding: 6px 8px 6px 10px;
  background: var(--ttsc-surface); border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control);
  color: var(--ttsc-text); font-size: 13px;
}
.ttsc-sortable-item:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.ttsc-sortable-handle { cursor: grab; color: var(--ttsc-text-muted); }
.ttsc-sortable-item:hover .ttsc-sortable-handle { color: var(--ttsc-text); }
.ttsc-sortable-pos { min-width: 22px; text-align: center; font-weight: 600; color: var(--ttsc-text-2); font-variant-numeric: tabular-nums; }
.ttsc-sortable-label { flex: 1; min-width: 0; }
.ttsc-sortable-item.is-dragging { opacity: .4; border-style: dashed; border-color: var(--ttsc-border-strong); }
.ttsc-sortable-item.is-drop-before::before,
.ttsc-sortable-item.is-drop-after::after {
  content: ""; position: absolute; inset-inline: 0; height: 2px; background: var(--ttsc-accent); border-radius: var(--ttsc-radius-pill);
}
.ttsc-sortable-item.is-drop-before::before { top: -5px; }
.ttsc-sortable-item.is-drop-after::after { bottom: -5px; }
.ttsc-sortable[aria-busy="true"] { pointer-events: none; opacity: .7; }
.sr-status { min-height: 16px; font-size: 12px; color: var(--ttsc-text-muted); }

.ttsc-dropzone-native {
  display: flex; flex-direction: column; align-items: center; gap: 4px; padding: var(--ttsc-space-5);
  border: 1.5px dashed var(--ttsc-border-strong); border-radius: var(--ttsc-radius-surface);
  background: var(--ttsc-canvas-2); color: var(--ttsc-text-2); font-size: 13px; text-align: center; cursor: pointer;
}
.ttsc-dropzone-native i { font-size: 20px; color: var(--ttsc-text-muted); }
.ttsc-dropzone-native small { color: var(--ttsc-text-muted); font-size: 12px; }
.ttsc-dropzone-native.is-over { border-color: var(--ttsc-accent); background: var(--ttsc-accent-soft); color: var(--ttsc-accent-text); }
.ttsc-dropzone-native.is-rejected { border-color: var(--ttsc-danger); color: var(--ttsc-danger-text); }
.ttsc-dropzone-native:focus-within { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.ttsc-dropzone-native .sr-input { position: absolute; width: 1px; height: 1px; opacity: 0; }
```

### JS

```js
// assets/js/core/ttsc.dnd.js — implementação TTSC (HTML5 Drag and Drop nativo)
export class TTSCSortable {
  static init(scope = document) {
    scope.querySelectorAll('[data-ttsc-sortable]').forEach((l) => l.ttscSortable || new TTSCSortable(l));
  }
  constructor(list, { handle = '[data-ttsc-sortable-handle]', url = list.dataset.ttscSortableUrl } = {}) {
    Object.assign(this, { list, handle, url, dragged: null, armed: false });
    list.ttscSortable = this;
    this.status = list.parentElement.querySelector('[data-ttsc-sortable-status]');

    list.addEventListener('pointerdown', (e) => { this.armed = !list.querySelector(handle) || !!e.target.closest(handle); });
    list.addEventListener('dragstart', (e) => {
      const item = e.target.closest('[data-ttsc-sortable-item]');
      if (!item || !this.armed) { e.preventDefault(); return; }
      this.dragged = item;
      this.before = this.order();
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', item.dataset.id);
      requestAnimationFrame(() => item.classList.add('is-dragging'));
    });
    list.addEventListener('dragover', (e) => {
      if (!this.dragged) return;
      e.preventDefault();
      const over = e.target.closest('[data-ttsc-sortable-item]');
      this.clearMarks();
      if (!over || over === this.dragged) return;
      const r = over.getBoundingClientRect();
      over.classList.add(e.clientY < r.top + r.height / 2 ? 'is-drop-before' : 'is-drop-after');
    });
    list.addEventListener('drop', (e) => {
      if (!this.dragged) return;
      e.preventDefault();
      const target = list.querySelector('.is-drop-before, .is-drop-after');
      if (target) {
        const from = this.items().indexOf(this.dragged);
        target.classList.contains('is-drop-before') ? target.before(this.dragged) : target.after(this.dragged);
        this.commit(this.dragged, from);
      }
    });
    list.addEventListener('dragend', () => { this.dragged?.classList.remove('is-dragging'); this.dragged = null; this.clearMarks(); });

    list.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-ttsc-sortable-up], [data-ttsc-sortable-down]');
      if (btn) this.move(btn.closest('[data-ttsc-sortable-item]'), btn.hasAttribute('data-ttsc-sortable-up') ? -1 : 1);
    });
    list.addEventListener('keydown', (e) => {
      const item = e.target.closest('[data-ttsc-sortable-item]');
      if (item && e.altKey && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) {
        e.preventDefault();
        this.move(item, e.key === 'ArrowUp' ? -1 : 1);
        item.focus();
      }
    });
  }
  items() { return [...this.list.querySelectorAll('[data-ttsc-sortable-item]')]; }
  order() { return this.items().map((i) => i.dataset.id); }
  clearMarks() { this.list.querySelectorAll('.is-drop-before, .is-drop-after').forEach((i) => i.classList.remove('is-drop-before', 'is-drop-after')); }
  move(item, delta) {
    const all = this.items(), from = all.indexOf(item), to = from + delta;
    if (to < 0 || to >= all.length) return;
    this.before = this.order();
    delta < 0 ? all[to].before(item) : all[to].after(item);
    this.commit(item, from);
  }
  async commit(item, from) {
    const ids = this.order(), to = ids.indexOf(item.dataset.id);
    if (from === to) return;
    this.items().forEach((it, i) => { const p = it.querySelector('.ttsc-sortable-pos'); if (p) p.textContent = i + 1; });
    const name = item.querySelector('.ttsc-sortable-label')?.textContent.trim();
    if (this.status) this.status.textContent = `${name} movido para a posição ${to + 1} de ${ids.length}.`;
    this.list.dispatchEvent(new CustomEvent('ttsc.sortable.change', { bubbles: true, detail: { ids, item, from, to } }));
    if (!this.url) return;
    this.list.setAttribute('aria-busy', 'true');
    try {
      const res = await fetch(this.url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content },
        body: JSON.stringify({ ids }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      this.list.dispatchEvent(new CustomEvent('ttsc.sortable.saved', { bubbles: true, detail: { ids } }));
    } catch (error) {
      this.before.forEach((id) => this.list.append(this.list.querySelector(`[data-id="${CSS.escape(id)}"]`)));
      this.items().forEach((it, i) => { const p = it.querySelector('.ttsc-sortable-pos'); if (p) p.textContent = i + 1; });
      this.list.dispatchEvent(new CustomEvent('ttsc.sortable.error', { bubbles: true, detail: { error } }));
    } finally {
      this.list.removeAttribute('aria-busy');
    }
  }
}

export class TTSCDropzone {
  static init(scope = document) { scope.querySelectorAll('[data-ttsc-dropzone]').forEach((z) => z.ttscDropzone || new TTSCDropzone(z)); }
  constructor(zone) {
    zone.ttscDropzone = this;
    this.zone = zone;
    this.input = zone.querySelector('input[type=file]');
    this.max = Number(zone.dataset.ttscDropzoneMax) || Infinity;
    let depth = 0;
    zone.addEventListener('dragenter', (e) => { if (e.dataTransfer.types.includes('Files')) { depth++; zone.classList.add('is-over'); } });
    zone.addEventListener('dragleave', () => { if (--depth <= 0) { depth = 0; zone.classList.remove('is-over'); } });
    zone.addEventListener('dragover', (e) => { if (e.dataTransfer.types.includes('Files')) { e.preventDefault(); e.dataTransfer.dropEffect = 'copy'; } });
    zone.addEventListener('drop', (e) => { e.preventDefault(); depth = 0; zone.classList.remove('is-over'); this.take([...e.dataTransfer.files]); });
    this.input.addEventListener('change', () => this.take([...this.input.files], false));
  }
  accepts(file) {
    const rules = (this.input.accept || '').split(',').map((s) => s.trim().toLowerCase()).filter(Boolean);
    if (!rules.length) return true;
    const name = file.name.toLowerCase(), type = file.type.toLowerCase();
    return rules.some((r) => (r.startsWith('.') ? name.endsWith(r) : r.endsWith('/*') ? type.startsWith(r.slice(0, -1)) : type === r));
  }
  take(files, assign = true) {
    const accepted = [], rejected = [];
    files.slice(0, this.input.multiple ? files.length : 1).forEach((file) => {
      if (!this.accepts(file)) rejected.push({ file, reason: 'Tipo de arquivo não permitido.' });
      else if (file.size > this.max) rejected.push({ file, reason: 'Arquivo acima do limite.' });
      else accepted.push(file);
    });
    if (assign && accepted.length) {
      const dt = new DataTransfer();
      accepted.forEach((f) => dt.items.add(f));
      this.input.files = dt.files;
    }
    this.zone.classList.toggle('is-rejected', rejected.length > 0);
    this.zone.dispatchEvent(new CustomEvent('ttsc.dropzone.files', { bubbles: true, detail: { accepted, rejected } }));
  }
}

TTSCSortable.init();
TTSCDropzone.init();
// Fora das áreas, impede o navegador de abrir o arquivo solto por engano
['dragover', 'drop'].forEach((t) => window.addEventListener(t, (e) => { if (!e.target.closest?.('[data-ttsc-dropzone]')) e.preventDefault(); }));
```

### SQL

A fila de espera tem ordem real em `enrollment_waitlist.position` (`int`, indexado em `idx_position`). Leitura e regravação da ordem inteira numa instrução:

```sql
-- Itens da fila (curso + período; só quem ainda espera)
SELECT w.uuid, w.position, w.status, r.student_name, r.course_name
  FROM enrollment_waitlist w
  JOIN enrollment_requests r ON r.uuid = w.request_uuid AND r.deleted_at IS NULL
 WHERE w.course_uuid = :course_uuid
   AND w.period_uuid = :period_uuid
   AND w.status = 'waiting'
 ORDER BY w.position;

-- Nova ordem (o PHP gera um WHEN por id recebido, na ordem do array, e o IN correspondente)
START TRANSACTION;
UPDATE enrollment_waitlist
   SET position = CASE uuid
                    WHEN :id_0 THEN 1
                    WHEN :id_1 THEN 2
                    WHEN :id_2 THEN 3
                  END
 WHERE course_uuid = :course_uuid
   AND period_uuid = :period_uuid
   AND uuid IN (:id_0, :id_1, :id_2);
COMMIT;
```

O controller confere que o conjunto de `ids` recebido é exatamente o conjunto atual da fila (mesmo `COUNT` e mesmos uuids); se alguém foi chamado ou incluído nesse meio-tempo responde 409 e o JS restaura a ordem. A mesma estrutura serve às tabelas com `sort_order` (`exam_question_set_items`, `ctr_contract_clauses`, `document_layout_blocks`).

## Faça / Não faça

- **Faça:** alça visível, botões de mover e `Alt+↑/↓`; anúncio em `aria-live`.
- **Faça:** salvar a ordem completa numa transação e restaurar a lista em erro.
- **Não faça:** arrastar em listas paginadas — a posição só faz sentido na lista inteira.
- **Não faça:** área de soltar sem `input[type=file]` clicável.
