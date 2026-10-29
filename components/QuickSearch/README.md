# Quick Search

Busca rápida global (command palette) aberta com Ctrl/⌘ K — resultados agrupados por tipo (páginas, cursos, turmas, pessoas), navegação por ↑ ↓ Enter Esc e comparação sem acento; implementação TTSC em JS puro (`TTSC.QuickSearch`).

## Quando usar

- Ir direto a um registro ou tela de qualquer lugar do sistema: “inf” → curso Técnico em Informática, turma, professora.
- Usuários frequentes (secretaria, coordenação) que preferem teclado a navegar pelo menu.
- **Não use** para filtrar a tabela da página atual: o campo de busca da própria tabela usa `IntelligentSearch.autoInitInPageSearch` (`assets/js/intelligent-search.js`) ou o filtro do [DataTable](../DataTable/README.md).
- **Não use** como campo de formulário para escolher um valor: use [Select2](../Select2/README.md) / [Select](../Select/README.md) com busca remota.
- Uma única paleta por layout.

## Anatomia

```
[ Buscar  Ctrl K ]  ← gatilho no cabeçalho (data-ttsc-quicksearch-toggle)

.ttsc-qs-backdrop (fixed, --ttsc-scrim, z --ttsc-z-modal)
└── .ttsc-qs [role=dialog]
    ├── .ttsc-qs-head   (lupa) input[role=combobox][aria-activedescendant]   [Esc]
    ├── ul.ttsc-qs-list [role=listbox]
    │   ├── li.ttsc-qs-group  "CURSOS"
    │   └── li.ttsc-qs-item[role=option][aria-selected]  ícone · título com <mark> · subtítulo
    └── .ttsc-qs-foot   ↑ ↓ navegar · Enter abrir · Esc fechar
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Gatilho | botão com `data-ttsc-quicksearch-toggle`, `aria-haspopup="dialog"`, `aria-keyshortcuts="Control+K Meta+K"` | sim |
| Raiz | `.ttsc-qs-backdrop[hidden]` | sim |
| Diálogo | `.ttsc-qs[role=dialog][aria-modal=true][aria-label]` | sim |
| Campo | `input[role=combobox][aria-controls][aria-autocomplete=list]` | sim |
| Lista | `ul[role=listbox]` | sim |
| Grupo | `li.ttsc-qs-group[role=presentation]` | gerado |
| Item | `li.ttsc-qs-item[role=option]` | gerado |
| Atalhos | `.ttsc-kbd` | recomendado |

## Variantes

| Grupo (`kind`) | Rótulo | Ícone | Fonte |
|---|---|---|---|
| `page` | Páginas | `fa-file-lines` | catálogo de rotas/menu filtrado por permissão |
| `course` | Cursos | `fa-graduation-cap` | `courses` |
| `class` | Turmas | `fa-users` | `classes` |
| `person` | Pessoas | `fa-user` | `users` (alunos, professores, responsáveis) |

## Estados

| Estado | Marca | Tokens |
|---|---|---|
| Fechado | `[hidden]` na raiz | — |
| Menos de `minChars` | mensagem “Digite ao menos 2 caracteres” | `ttsc-text-muted` |
| Resultados | grupos + itens; primeiro item ativo | — |
| Item ativo | `aria-selected="true"` | fundo `ttsc-accent-soft`, ícone `ttsc-accent-text` |
| Trecho encontrado | `<mark>` | `ttsc-accent-text` 700, sem fundo |
| Sem resultados | “Nenhum resultado para “…”” | `ttsc-text-muted` |

## API

| Opção | Padrão | Descrição |
|---|---|---|
| `source(q)` | — | função que devolve (ou Promise de) `[{ kind, title, subtitle, url }]` |
| `groups` | `{}` | `{ kind: { label, icon } }` — também define a **ordem** dos grupos |
| `minChars` | `2` | caracteres mínimos |
| `debounce` | `200` | ms entre digitação e busca |
| `onSelect(item)` | — | ação ao escolher (padrão do app: `location.href = item.url`) |

| Método | Descrição |
|---|---|
| `new TTSC.QuickSearch(root, options)` | cria (registra Ctrl/⌘ K no `document`) |
| `open(q?)` / `close()` / `isOpen()` | abre com termo opcional; fechar devolve o foco ao gatilho |
| `search(q)` | executa a busca (descarta respostas fora de ordem) |
| `move(±1)` / `setActive(i)` / `choose(i)` | navegação programática |
| `TTSC.QuickSearch.normalize(s)` | minúsculas sem acento (mesma regra do `IntelligentSearch.normalize`) |

| Evento | Detalhe |
|---|---|
| `ttsc:quicksearch:select` (bubbles, na raiz) | o item escolhido |

| Tecla | Ação |
|---|---|
| Ctrl K / ⌘ K | abre/fecha |
| ↑ / ↓ | item anterior/próximo (circular) |
| Enter | abre o item ativo |
| Esc / clique fora | fecha |

## Acessibilidade

- Padrão **combobox + listbox** (ARIA 1.2): o foco fica no campo; `aria-activedescendant` aponta o item ativo; cada opção tem `aria-describedby` com o nome do grupo.
- `role="dialog"` + `aria-modal`; ao fechar o foco volta ao elemento anterior.
- O atalho é anunciado por `aria-keyshortcuts` e visível no gatilho (`.ttsc-kbd`).
- Não dependa só do realce: o item ativo tem fundo `ttsc-accent-soft` e o trecho encontrado é negrito em `ttsc-accent-text` (≥ 4,5:1).
- Resultados de pessoas mostram só dados que o usuário pode ver (nunca CPF completo).

## Modelos

### HTML

```html
<!-- Cabeçalho do layout -->
<button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-sm" data-ttsc-quicksearch-toggle
        aria-haspopup="dialog" aria-keyshortcuts="Control+K Meta+K">
  <i class="fa-light fa-magnifying-glass"></i> Buscar <span class="ttsc-kbd">Ctrl K</span>
</button>

<!-- Fim do <body> -->
<div class="ttsc-qs-backdrop" id="quick-search" hidden data-endpoint="/search/quick">
  <div class="ttsc-qs" role="dialog" aria-modal="true" aria-label="Busca rápida">
    <div class="ttsc-qs-head">
      <i class="fa-light fa-magnifying-glass"></i>
      <input type="text" role="combobox" aria-expanded="true" aria-controls="quick-search-list" aria-autocomplete="list"
             placeholder="Buscar cursos, turmas, pessoas ou páginas…" autocomplete="off" spellcheck="false">
      <span class="ttsc-kbd">Esc</span>
    </div>
    <ul class="ttsc-qs-list" id="quick-search-list" role="listbox" aria-label="Resultados"></ul>
    <div class="ttsc-qs-foot" aria-hidden="true">
      <span><span class="ttsc-kbd">↑</span> <span class="ttsc-kbd">↓</span> navegar</span>
      <span><span class="ttsc-kbd">Enter</span> abrir</span>
      <span><span class="ttsc-kbd">Esc</span> fechar</span>
    </div>
  </div>
</div>
```

### CSS

```css
.ttsc-qs-backdrop { position: fixed; inset: 0; z-index: var(--ttsc-z-modal); background: var(--ttsc-scrim);
  display: flex; align-items: flex-start; justify-content: center; padding-top: 12vh; }
.ttsc-qs-backdrop[hidden] { display: none; }
.ttsc-qs { width: min(640px, calc(100vw - 32px)); background: var(--ttsc-surface); border: 1px solid var(--ttsc-border);
  border-radius: var(--ttsc-radius-surface); box-shadow: var(--ttsc-shadow-xl); overflow: hidden; }
.ttsc-qs-head { display: flex; align-items: center; gap: 10px; padding: 12px 14px; border-bottom: 1px solid var(--ttsc-border-soft); color: var(--ttsc-text-muted); }
.ttsc-qs-head input { flex: 1; border: 0; background: transparent; color: var(--ttsc-text); font: inherit; font-size: 14px; }
.ttsc-qs-list { max-height: 360px; overflow-y: auto; padding: 6px; margin: 0; list-style: none; }
.ttsc-qs-group { padding: 8px 8px 4px; font-size: 11px; font-weight: 600; letter-spacing: .04em; text-transform: uppercase; color: var(--ttsc-text-muted); }
.ttsc-qs-item { display: flex; align-items: center; gap: 10px; padding: 7px 8px; border-radius: var(--ttsc-radius-control); cursor: pointer; color: var(--ttsc-text-2); }
.ttsc-qs-item .t { color: var(--ttsc-text); font-weight: 500; }
.ttsc-qs-item .s { margin-left: auto; font-size: 12px; color: var(--ttsc-text-muted); }
.ttsc-qs-item mark { background: transparent; color: var(--ttsc-accent-text); font-weight: 700; }
.ttsc-qs-item[aria-selected="true"] { background: var(--ttsc-accent-soft); }
.ttsc-qs-item[aria-selected="true"] i { color: var(--ttsc-accent-text); }
.ttsc-qs-foot { display: flex; gap: 14px; padding: 8px 14px; border-top: 1px solid var(--ttsc-border-soft); font-size: 11px; color: var(--ttsc-text-muted); }
```

### JS

```js
/* assets/js/core/ttsc.quicksearch.js — implementação TTSC */
(function (w) {
  var norm = function (s) { return String(s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase(); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  function highlight(text, q) {
    var n = norm(text), i = q ? n.indexOf(norm(q)) : -1;
    if (i < 0) return esc(text);
    return esc(text.slice(0, i)) + '<mark>' + esc(text.slice(i, i + q.length)) + '</mark>' + esc(text.slice(i + q.length));
  }
  function QuickSearch(root, options) {
    this.root = root; this.input = root.querySelector('input'); this.list = root.querySelector('[role="listbox"]');
    this.options = Object.assign({ minChars: 2, debounce: 200, source: null, groups: {} }, options || {});
    this.items = []; this.active = -1; this.lastFocus = null; this.seq = 0;
    var self = this, timer;
    this.input.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(function () { self.search(self.input.value.trim()); }, self.options.debounce); });
    this.input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); self.move(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); self.move(-1); }
      else if (e.key === 'Enter') { e.preventDefault(); self.choose(self.active); }
      else if (e.key === 'Escape') { e.preventDefault(); self.close(); }
    });
    this.list.addEventListener('mousemove', function (e) { var li = e.target.closest('[role="option"]'); if (li) self.setActive(+li.dataset.index); });
    this.list.addEventListener('click', function (e) { var li = e.target.closest('[role="option"]'); if (li) self.choose(+li.dataset.index); });
    root.addEventListener('mousedown', function (e) { if (e.target === root) self.close(); });
    document.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); self.isOpen() ? self.close() : self.open(); }
    });
  }
  QuickSearch.prototype.isOpen = function () { return !this.root.hidden; };
  QuickSearch.prototype.open = function (q) {
    this.lastFocus = document.activeElement; this.root.hidden = false;
    if (q !== undefined) this.input.value = q;
    this.input.focus(); this.input.select(); this.search(this.input.value.trim());
  };
  QuickSearch.prototype.close = function () { this.root.hidden = true; if (this.lastFocus && this.lastFocus.focus) this.lastFocus.focus(); };
  QuickSearch.prototype.search = function (q) {
    var self = this, seq = ++this.seq;
    if (q.length < this.options.minChars) { this.render([], q, 'Digite ao menos ' + this.options.minChars + ' caracteres'); return; }
    Promise.resolve(this.options.source(q)).then(function (rows) { if (seq === self.seq) self.render(rows, q); });
  };
  QuickSearch.prototype.render = function (rows, q, emptyMsg) {
    var self = this, html = '', idx = 0, groups = {};
    this.items = rows;
    rows.forEach(function (r) { (groups[r.kind] = groups[r.kind] || []).push(r); });
    this.items = [];
    Object.keys(this.options.groups).forEach(function (kind) {
      if (!groups[kind]) return; var g = self.options.groups[kind];
      html += '<li role="presentation" class="ttsc-qs-group" id="qs-g-' + kind + '">' + g.label + '</li>';
      groups[kind].forEach(function (r) {
        self.items.push(r);
        html += '<li role="option" id="qs-opt-' + idx + '" data-index="' + idx + '" class="ttsc-qs-item" aria-selected="false" aria-describedby="qs-g-' + kind + '">' +
          '<i class="fa-light ' + g.icon + '" aria-hidden="true"></i><span class="t">' + highlight(r.title, q) + '</span><span class="s">' + esc(r.subtitle || '') + '</span></li>';
        idx++;
      });
    });
    this.list.innerHTML = html || '<li role="presentation" class="ttsc-qs-empty">' + esc(emptyMsg || 'Nenhum resultado para “' + q + '”') + '</li>';
    this.setActive(this.items.length ? 0 : -1);
  };
  QuickSearch.prototype.setActive = function (i) {
    var prev = this.list.querySelector('[aria-selected="true"]'); if (prev) prev.setAttribute('aria-selected', 'false');
    this.active = i;
    if (i < 0) { this.input.removeAttribute('aria-activedescendant'); return; }
    var li = document.getElementById('qs-opt-' + i); li.setAttribute('aria-selected', 'true');
    this.input.setAttribute('aria-activedescendant', li.id); li.scrollIntoView({ block: 'nearest' });
  };
  QuickSearch.prototype.move = function (d) { if (!this.items.length) return; this.setActive((this.active + d + this.items.length) % this.items.length); };
  QuickSearch.prototype.choose = function (i) {
    var item = this.items[i]; if (!item) return;
    this.root.dispatchEvent(new CustomEvent('ttsc:quicksearch:select', { detail: item, bubbles: true }));
    if (this.options.onSelect) this.options.onSelect(item);
  };
  QuickSearch.normalize = norm;
  w.TTSC = w.TTSC || {}; w.TTSC.QuickSearch = QuickSearch;
})(window);
```

Ligação no app (endpoint real, abort de requisições antigas):

```js
// assets/js/core/ttsc.quicksearch.boot.js
document.addEventListener('DOMContentLoaded', () => {
  const root = document.getElementById('quick-search');
  if (!root) return;
  let controller;

  const qs = new TTSC.QuickSearch(root, {
    minChars: 2,
    debounce: 200,
    groups: {
      page:   { label: 'Páginas', icon: 'fa-file-lines' },
      course: { label: 'Cursos',  icon: 'fa-graduation-cap' },
      class:  { label: 'Turmas',  icon: 'fa-users' },
      person: { label: 'Pessoas', icon: 'fa-user' },
    },
    source: async (q) => {
      controller?.abort();                       // cancela a busca anterior
      controller = new AbortController();
      try {
        const res = await fetch(`${root.dataset.endpoint}?q=${encodeURIComponent(q)}`, {
          headers: { Accept: 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
          signal: controller.signal,
        });
        return res.ok ? (await res.json()).data : [];
      } catch (e) {
        return [];
      }
    },
    onSelect: (item) => { window.location.href = item.url; },
  });

  document.querySelectorAll('[data-ttsc-quicksearch-toggle]').forEach((btn) => btn.addEventListener('click', () => qs.open()));
});
```

### SQL

Uma consulta `UNION ALL` com `LIMIT` por grupo (cada parte entre parênteses), filtrando soft delete e o escopo do tenant/unidade. O termo é escapado em PHP para `LIKE` com `ESCAPE '!'`:
`$like = '%' . strtr($q, ['!' => '!!', '%' => '!%', '_' => '!_']) . '%';`

```sql
(SELECT 'course' AS kind, c.uuid, c.name AS title, c.code AS subtitle
   FROM courses c
  WHERE c.deleted_at IS NULL
    AND c.unit_uuid = :unit_uuid
    AND (c.name LIKE :like ESCAPE '!' OR c.code LIKE :like2 ESCAPE '!')
  ORDER BY c.name
  LIMIT 5)
UNION ALL
(SELECT 'class', cl.uuid, cl.name, c.name
   FROM classes cl
   JOIN courses c ON c.uuid = cl.course_uuid AND c.deleted_at IS NULL
  WHERE cl.deleted_at IS NULL
    AND cl.unit_uuid = :unit_uuid2
    AND (cl.name LIKE :like3 ESCAPE '!' OR cl.code LIKE :like4 ESCAPE '!')
  ORDER BY cl.name
  LIMIT 5)
UNION ALL
(SELECT 'person', u.uuid, u.name, u.email
   FROM users u
  WHERE u.deleted_at IS NULL
    AND u.tenant_id = :tenant_id
    AND u.status = 'active'
    AND (u.name LIKE :like5 ESCAPE '!' OR u.email LIKE :like6 ESCAPE '!' OR u.cpf LIKE :digits_like ESCAPE '!')
  ORDER BY u.name
  LIMIT 5);
```

O controller monta `url` por tipo (`/admin/academic/courses/{uuid}`…), acrescenta as páginas do menu que o usuário pode acessar (permissões RBAC) e devolve `{"data": [...]}`. Para ordenar por relevância, aplique `IntelligentSearch.score()` no cliente ou um `CASE WHEN title LIKE 'q%' THEN 0 ELSE 1 END` no `ORDER BY` de cada parte. `:digits_like` só é usado com ≥ 3 dígitos (mesma regra do `sanitizeDigits`).

## Faça / Não faça

- **Faça:** `LIMIT` por grupo, debounce e `AbortController` (respostas fora de ordem são descartadas).
- **Faça:** escapar `%`, `_` e o caractere de escape antes do `LIKE`; escapar o HTML ao renderizar.
- **Faça:** filtrar por unidade/tenant e permissões — a busca não pode revelar registros que a tela não mostraria.
- **Não faça:** `LIKE '%termo%'` sem índice em tabelas enormes sem limite de caracteres mínimos.
- **Não faça:** capturar Ctrl K quando o foco está num editor rico que usa o atalho (TinyMCE/CKEditor “link”): ignore se `event.target.closest('.tox, .ck')`.
- **Não faça:** mostrar CPF/e-mail completos de alunos para perfis sem permissão.
