# Swapper

Move um bloco de marcação entre contêineres conforme o breakpoint usando `matchMedia` — mapa declarativo “media query → destino” em `data-ttsc-swapper`; implementação TTSC em JS puro (`TTSC.Swapper`).

## Quando usar

- O mesmo bloco precisa ficar em lugares diferentes por largura e **com mais de dois destinos** ou regras de media query arbitrárias: filtros na toolbar (≥ 1024px), no drawer de filtros (< 1024px) e no rodapé fixo (impressão / `orientation: portrait`).
- Quando o destino depende de query que não é largura (`(orientation: portrait)`, `(pointer: coarse)`, `print`).
- **Compare com [Reparent](../Reparent/README.md)** (`data-ttsc-reparent`, runtime ttscui): para o caso comum — um destino alternativo definido por `data-ttsc-reparent-target` / variável CSS `--ttsc-reparent-target` dentro de uma media query — **use o Reparent**, que já vem no chassi. O Swapper reage a `change` do `matchMedia` (sem ouvir `resize`), aceita N destinos num JSON e permite forçar um alvo por código.

| Critério | Swapper (TTSC vanilla) | Reparent (ttscui) |
|---|---|---|
| Configuração | `data-ttsc-swapper='{"(min-width: 1024px)": "#a", "default": "#b"}'` | `data-ttsc-reparent-target` + `-mode` (ou vars CSS por breakpoint) |
| Gatilho | `MediaQueryList` `change` | reavaliação no resize |
| Destinos | N, qualquer media query | 1 por regra CSS |
| Forçar por JS | `force(key)` | — |
| Evento | `ttsc:swapper:moved` | eventos do componente |

- **Não use** para mostrar/esconder: classes responsivas (`hidden lg:flex`). **Não** duplique o HTML em dois lugares — campos de formulário duplicados enviam valores duas vezes.

## Anatomia

```
desktop (≥1024px)                          mobile (default)
┌ #toolbar-slot ─────────────┐             ┌ #drawer-slot ─────┐
│ form[data-ttsc-swapper] ◄──┼── change ──►│ form (mesmo nó)   │
└────────────────────────────┘             └───────────────────┘
```

| Parte | Atributo | Obrigatório |
|---|---|---|
| Bloco móvel | `data-ttsc-swapper='{"<media query>": "<seletor>", …, "default": "<seletor>"}'` | sim |
| Modo | `data-ttsc-swapper-mode="append \| prepend"` | não (`append`) |
| Destinos | elementos existentes no DOM (slots) | sim |
| Ordem de precedência | ordem das chaves no JSON; a primeira query que casar vence | — |

## Estados

| Estado | Marca |
|---|---|
| No destino da regra que casou | `swapper.current = "<query>"` |
| Sem regra casando | destino `default` |
| Forçado | `force(key)` ignora o `matchMedia` até `force(null)` |

Slots de destino podem receber estilo de vazio/ativo (`.is-target` no preview: borda `ttsc-accent-border`, fundo `ttsc-accent-soft`).

## API

| Opção / atributo | Tipo | Descrição |
|---|---|---|
| `targets` / `data-ttsc-swapper` | objeto JSON | mapa query → seletor; `default` obrigatório |
| `mode` / `data-ttsc-swapper-mode` | `'append' \| 'prepend'` | posição no destino |

| Método | Descrição |
|---|---|
| `TTSC.Swapper.init(root?)` | inicializa todos os `[data-ttsc-swapper]` (idempotente; instância em `el._ttscSwapper`) |
| `new TTSC.Swapper(el, { targets, mode })` | instância manual |
| `update()` | reavalia e move se preciso |
| `resolve()` | chave da regra vigente |
| `force(key \| null)` | força uma regra (testes, preferência do usuário) |
| `destroy()` | remove os listeners |

| Evento (bubbles, no bloco) | `detail` |
|---|---|
| `ttsc:swapper:moved` | `{ key, from, to }` |

## Acessibilidade

- O nó é **movido**, não clonado: ids, `label for`, valores digitados e listeners continuam válidos.
- Se o foco estava dentro do bloco, ele é devolvido ao mesmo elemento após mover.
- A ordem do DOM muda com o destino: garanta que, em cada destino, a ordem de leitura faça sentido (filtros antes da tabela; no drawer, depois do título).
- Não anuncie cada movimento ao leitor de tela (acontece por redimensionamento); o `aria-live` do preview é só demonstração.

## Modelos

### HTML

```html
<!-- Página de listagem: slots nos dois lugares -->
<div class="flex items-center gap-2" id="toolbar-slot"></div>

<div class="ttsc-drawer ttsc-drawer-end hidden" data-ttsc-drawer="true" id="drawer-filters">
  <div class="ttsc-drawer-header"><h3 class="ttsc-drawer-title">Filtros</h3></div>
  <div class="ttsc-drawer-content" id="drawer-slot"></div>
</div>

<form class="flex flex-wrap items-center gap-2" id="enrollment-filters" method="get" aria-label="Filtros de matrícula"
      data-ttsc-swapper='{"(min-width: 1024px)": "#toolbar-slot", "default": "#drawer-slot"}' data-ttsc-swapper-mode="append">
  <select class="ttsc-select ttsc-select-sm" name="course_uuid" aria-label="Curso">
    <option value="">Todos os cursos</option>
    <?php foreach ($courses as $c): ?>
      <option value="<?= $this->e($c['uuid']) ?>" <?= $c['uuid'] === $filters['course_uuid'] ? 'selected' : '' ?>><?= $this->e($c['name']) ?></option>
    <?php endforeach; ?>
  </select>
  <select class="ttsc-select ttsc-select-sm" name="status" aria-label="Status">
    <option value="active">Ativas</option><option value="locked">Trancadas</option><option value="cancelled">Canceladas</option>
  </select>
  <button type="submit" class="ttsc-btn ttsc-btn-primary ttsc-btn-sm"><i class="fa-light fa-filter"></i> Filtrar</button>
</form>
```

### CSS

```css
/* o bloco se adapta ao destino atual */
#toolbar-slot #enrollment-filters { flex-wrap: nowrap; }
#drawer-slot #enrollment-filters { flex-direction: column; align-items: stretch; }
#drawer-slot #enrollment-filters .ttsc-btn { justify-content: center; }
/* slot vazio não ocupa espaço */
#toolbar-slot:empty { display: none; }
/* realce opcional do destino ativo */
.is-target { border-color: var(--ttsc-accent-border); background: var(--ttsc-accent-soft); }
```

### JS

```js
// assets/js/core/ttsc.swapper.js — implementação TTSC
(function (w) {
  function Swapper(el, options) {
    this.el = el;
    const raw = (options && options.targets) || el.getAttribute('data-ttsc-swapper') || '{}';
    this.targets = typeof raw === 'string' ? JSON.parse(raw) : raw;   // { "<media query>": "#sel", "default": "#sel" }
    this.mode = (options && options.mode) || el.getAttribute('data-ttsc-swapper-mode') || 'append';
    this.forced = null;
    this.current = null;
    this.queries = Object.keys(this.targets).filter((k) => k !== 'default').map((q) => w.matchMedia(q));
    this._onChange = () => this.update();
    this.queries.forEach((mq) => mq.addEventListener('change', this._onChange));
    this.update();
  }
  Swapper.prototype.resolve = function () {
    if (this.forced) return this.forced;
    const hit = this.queries.find((mq) => mq.matches);
    return hit ? hit.media : 'default';
  };
  Swapper.prototype.update = function () {
    const key = this.resolve();
    const sel = this.targets[key] || this.targets.default;
    const target = sel && document.querySelector(sel);
    if (!target || (key === this.current && this.el.parentElement === target)) return;
    const focused = this.el.contains(document.activeElement) ? document.activeElement : null;
    const from = this.el.parentElement;
    if (this.mode === 'prepend') target.prepend(this.el); else target.append(this.el);
    if (focused) focused.focus({ preventScroll: true });
    this.current = key;
    this.el.dispatchEvent(new CustomEvent('ttsc:swapper:moved', { bubbles: true, detail: { key, from, to: target } }));
  };
  Swapper.prototype.force = function (key) { this.forced = key || null; this.update(); };
  Swapper.prototype.destroy = function () { this.queries.forEach((mq) => mq.removeEventListener('change', this._onChange)); };
  Swapper.init = function (root) {
    (root || document).querySelectorAll('[data-ttsc-swapper]').forEach((el) => {
      if (!el._ttscSwapper) el._ttscSwapper = new Swapper(el);
    });
  };
  w.TTSC = w.TTSC || {};
  w.TTSC.Swapper = Swapper;
  document.addEventListener('DOMContentLoaded', () => Swapper.init());
})(window);
```

Atenção: `matchMedia().media` devolve a query **normalizada** pelo navegador; escreva as chaves no formato canônico (`(min-width: 1024px)`, com espaço após os dois-pontos) para que `targets[key]` encontre o destino.

### SQL

O Swapper não acessa dados; o bloco que ele move é que é alimentado pelo servidor — aqui, as opções do filtro de curso:

```sql
SELECT c.uuid, c.name
  FROM courses c
 WHERE c.deleted_at IS NULL
   AND c.is_active = 1
   AND c.unit_uuid = :unit_uuid
 ORDER BY c.name;
```

O controller passa `$courses` e os filtros atuais (`$filters` da query string) para a view; o formulário é renderizado **uma vez** e o Swapper o posiciona.

## Faça / Não faça

- **Faça:** sempre um destino `default` e slots que existam no DOM antes do `init`.
- **Faça:** preferir o [Reparent](../Reparent/README.md) do ttscui quando há um único destino alternativo.
- **Faça:** estilizar o bloco pelo destino (`#drawer-slot #filtros`), não por media query duplicada.
- **Não faça:** clonar o formulário para os dois lugares.
- **Não faça:** ouvir `resize` para isso — `matchMedia` só dispara quando cruza o breakpoint.
- **Não faça:** mover elementos com iframes/players (recarregam ao mudar de pai).
