# Pagination

Rodapé único de toda lista paginada do chassi (tabelas, grades de cards, colunas de kanban): faixa “Mostrando 1–10 de 52”, seletor “Por página” e botões de página `.ttsc-pagination`, seguindo o contrato de `assets/css/ttsc.pagination.css` + `assets/js/ttsc.pagination.js`.

> Também listado em: **Base › Pagination**.

## Quando usar

- Qualquer lista com mais de uma página de resultados vinda do servidor (matrículas, mensalidades, alunos de uma turma).
- Junto do [DataTable](../DataTable/README.md): o ttscui DataTable renderiza seu próprio paginador com as mesmas classes — não duplique.
- **Não use** para feeds que crescem para baixo (notificações, histórico): use “Carregar mais” com keyset (ver SQL).
- **Não use** para etapas de um processo: use [Stepper](../Stepper/README.md).

## Anatomia

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Mostrando 11–20 de 52 matrículas        Por página [10 ▾]   ‹ 1 2 [3] 4 … 6 › │
└──────────────────────────────────────────────────────────────────────────────┘
  .info (aria-live)                       .per-page             .ttsc-pagination
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Barra | `nav.ttsc-pagination-standard` + `aria-label="Paginação"` | sim |
| Faixa | `.info` com `aria-live="polite"`; números em `<b>` | sim |
| Por página | `.per-page` > `<select name="per_page">` (o `ttsc.pagination.js` troca pelo gatilho `.ttsc-page-size-trigger`) | não |
| Páginas | `.ttsc-pagination` (flex, gap 4px) | sim |
| Item | `.ttsc-pagination-item` > `button.ttsc-btn.ttsc-btn-icon.ttsc-btn-sm` | sim |
| Atual | botão com `aria-current="page"` (+ `active`) | sim |
| Reticências | `.ttsc-pagination-ellipsis` + `aria-hidden="true"` | quando > 7 páginas |
| Anterior / próxima | botões com `aria-label` e `disabled` nas pontas | sim |

## Variantes

| Variante | Uso | Tokens |
|---|---|---|
| Rodapé completo | Tabelas de página (PageRecords) | barra `ttsc-surface`, borda topo `ttsc-border`, texto `ttsc-text-muted`, números `ttsc-text` |
| Só páginas | Cards e drawers estreitos | `.ttsc-pagination` sem `.info`/`.per-page` |
| Compacta (mobile ≤ 640px) | `‹  3 / 6  ›` | mesmo contrato; `.info` ocupa 100% e centraliza |

## Estados

| Estado | Visual | Tokens |
|---|---|---|
| Normal | 28×28, borda 1px, `radius-sm`, 500 12px | borda `ttsc-border`, texto `ttsc-text-2` |
| Hover | realce verde suave | borda `ttsc-accent-border`, fundo `ttsc-accent-soft`, texto `ttsc-accent-text` |
| Atual | preenchido, 600 | fundo `ttsc-accent`, texto `ttsc-accent-on` (9,6:1) |
| Desabilitado | opacidade 45%, `cursor: not-allowed` | — |
| Vazio (0 registros) | “Mostrando 0–0 de 0”, sem botões de página, anterior/próxima desabilitados | — |

## API

O ttscui não tem módulo de paginação fora do DataTable; o contrato é do chassi:

| Fonte | O que faz |
|---|---|
| `ttsc.pagination.js` | Encontra `select[name*="per_page"]`, `select[id*="page-size"]`, `.per-page select`…, marca a barra com `.ttsc-pagination-standard` e cria o menu “Por página” portado para `<body>` (abre para cima sem espaço). O `<select>` nativo continua sendo a fonte do valor (`change` real). Opt-in automático via `MutationObserver`. |
| `TTSCPager` (JS abaixo) | Renderiza a janela de páginas e dispara `ttsc.pagination.change`. |

| Opção `TTSCPager` | Padrão | Descrição |
|---|---|---|
| `total` | `0` | total de registros (do `COUNT(*)`) |
| `page` | `1` | página atual (1-based) |
| `perPage` | `10` | tamanho da página |
| `noun` | `'registros'` | substantivo da faixa (“matrículas”) |
| `window` | `1` | vizinhos da página atual (`1 … p-1 p p+1 … N`) |

| Evento | Alvo | `detail` |
|---|---|---|
| `ttsc.pagination.change` | `nav.ttsc-pagination-standard` | `{ page, perPage, offset }` |

Regras: ≤ 7 páginas lista todas; trocar filtro ou tamanho de página volta à página 1; `page` fora do intervalo é ajustada para a última.

## Acessibilidade

- `<nav aria-label="Paginação de matrículas">`; a página atual tem `aria-current="page"`.
- Botões de ícone: `aria-label="Página anterior"` / `"Próxima página"` / `"Página 4"`.
- A faixa “Mostrando…” é `aria-live="polite"` — anuncia a troca sem roubar o foco.
- Após trocar de página, devolva o foco ao topo da tabela (`caption` ou cabeçalho) com `tabindex="-1"`.
- Não use texto verde `ttsc-accent` sobre branco (2:1): o hover usa `ttsc-accent-text`; a página atual usa `ttsc-accent-on` sobre `ttsc-accent`.

## Modelos

### HTML

```html
<!-- resources/views/academic/enrollments/index.php — $page, $perPage, $total vêm do controller -->
<nav class="ttsc-pagination-standard" aria-label="Paginação de matrículas" data-ttsc-pager
     data-total="<?= (int) $total ?>" data-page="<?= (int) $page ?>" data-per-page="<?= (int) $perPage ?>" data-noun="matrículas">
  <span class="info" aria-live="polite">
    Mostrando <b><?= $from ?>–<?= $to ?></b> de <b><?= $total ?></b> matrículas
  </span>
  <div class="flex items-center gap-4">
    <label class="per-page">
      <span>Por página</span>
      <select name="per_page" class="ttsc-select ttsc-select-sm">
        <?php foreach ([10, 25, 50, 100] as $n): ?>
          <option value="<?= $n ?>" <?= $n === $perPage ? 'selected' : '' ?>><?= $n ?></option>
        <?php endforeach ?>
      </select>
    </label>
    <div class="ttsc-pagination" data-ttsc-pager-pages>
      <!-- preenchido por TTSCPager; no servidor, renderize o mesmo HTML para funcionar sem JS -->
      <div class="ttsc-pagination-item">
        <button type="button" class="ttsc-btn ttsc-btn-icon ttsc-btn-sm" aria-label="Página anterior" disabled><i class="fa-light fa-chevron-left"></i></button>
      </div>
      <div class="ttsc-pagination-item">
        <button type="button" class="ttsc-btn ttsc-btn-icon ttsc-btn-sm active" aria-current="page">1</button>
      </div>
      <div class="ttsc-pagination-item"><button type="button" class="ttsc-btn ttsc-btn-icon ttsc-btn-sm" aria-label="Página 2">2</button></div>
      <div class="ttsc-pagination-ellipsis" aria-hidden="true">…</div>
      <div class="ttsc-pagination-item"><button type="button" class="ttsc-btn ttsc-btn-icon ttsc-btn-sm" aria-label="Página 6">6</button></div>
      <div class="ttsc-pagination-item">
        <button type="button" class="ttsc-btn ttsc-btn-icon ttsc-btn-sm" aria-label="Próxima página"><i class="fa-light fa-chevron-right"></i></button>
      </div>
    </div>
  </div>
</nav>
```

### CSS

`ttsc.pagination.css` no repositório ainda usa hex fixos (`#e2e8f0`, `#10b981` com texto branco = 2,5:1). Versão com tokens, mesma métrica:

```css
.ttsc-pagination-standard {
  display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;
  gap: 8px 16px; min-height: 54px; padding: 10px var(--ttsc-space-4);
  border-top: 1px solid var(--ttsc-border); background: var(--ttsc-surface);
  color: var(--ttsc-text-muted); font-size: 12px; line-height: 18px;
}
.ttsc-pagination-standard .info b { color: var(--ttsc-text); font-weight: 600; }
.ttsc-pagination-standard .per-page { display: inline-flex; align-items: center; gap: 8px; }
.ttsc-pagination-standard .ttsc-pagination-item .ttsc-btn {
  width: 28px; height: 28px; padding: 0; border: 1px solid var(--ttsc-border);
  border-radius: var(--ttsc-radius-sm); background: var(--ttsc-surface);
  color: var(--ttsc-text-2); font-size: 12px; font-weight: 500; box-shadow: var(--ttsc-shadow-xs);
}
.ttsc-pagination-standard .ttsc-pagination-item .ttsc-btn:hover:not(:disabled) {
  border-color: var(--ttsc-accent-border); background: var(--ttsc-accent-soft); color: var(--ttsc-accent-text);
}
.ttsc-pagination-standard .ttsc-pagination-item .ttsc-btn[aria-current="page"] {
  border-color: var(--ttsc-accent); background: var(--ttsc-accent); color: var(--ttsc-accent-on); font-weight: 600;
}
.ttsc-pagination-standard .ttsc-btn:disabled { opacity: .45; cursor: not-allowed; box-shadow: none; }
.ttsc-pagination-standard .ttsc-pagination-ellipsis { width: 20px; height: 28px; color: var(--ttsc-text-muted); }
@media (max-width: 640px) {
  .ttsc-pagination-standard { justify-content: center; }
  .ttsc-pagination-standard .info { flex: 1 1 100%; justify-content: center; }
}
```

### JS

```js
// assets/js/core/ttsc.pager.js — implementação TTSC: janela de páginas + evento
export class TTSCPager {
  constructor(nav, options = {}) {
    this.nav = nav;
    this.pages = nav.querySelector('[data-ttsc-pager-pages]');
    this.info = nav.querySelector('.info');
    this.select = nav.querySelector('select[name="per_page"]');
    const d = nav.dataset;
    this.o = { total: +d.total || 0, page: +d.page || 1, perPage: +d.perPage || 10, noun: d.noun || 'registros', window: 1, ...options };
    this.pages.addEventListener('click', (e) => {
      const b = e.target.closest('button[data-page]');
      if (b && !b.disabled) this.go(+b.dataset.page);
    });
    this.select?.addEventListener('change', () => { this.o.perPage = +this.select.value; this.go(1, true); });
    this.render();
  }
  get last() { return Math.max(1, Math.ceil(this.o.total / this.o.perPage)); }
  windowPages() {
    const { page } = this.o, last = this.last, w = this.o.window;
    if (last <= 7) return Array.from({ length: last }, (_, i) => i + 1);
    const out = [1];
    const from = Math.max(2, page - w), to = Math.min(last - 1, page + w);
    if (from > 2) out.push('…');
    for (let p = from; p <= to; p++) out.push(p);
    if (to < last - 1) out.push('…');
    out.push(last);
    return out;
  }
  btn(label, page, { current = false, disabled = false, aria } = {}) {
    return `<div class="ttsc-pagination-item"><button type="button" class="ttsc-btn ttsc-btn-icon ttsc-btn-sm${current ? ' active' : ''}"
      data-page="${page}" ${current ? 'aria-current="page"' : ''} ${disabled ? 'disabled' : ''} aria-label="${aria || 'Página ' + page}">${label}</button></div>`;
  }
  render() {
    const { total, page, perPage, noun } = this.o;
    const from = total ? (page - 1) * perPage + 1 : 0, to = Math.min(total, page * perPage);
    this.info.innerHTML = `Mostrando <b>${from}–${to}</b> de <b>${total}</b> ${noun}`;
    let html = this.btn('<i class="fa-light fa-chevron-left"></i>', page - 1, { disabled: page <= 1 || !total, aria: 'Página anterior' });
    if (total) this.windowPages().forEach((p) => {
      html += p === '…' ? '<div class="ttsc-pagination-ellipsis" aria-hidden="true">…</div>' : this.btn(p, p, { current: p === page });
    });
    html += this.btn('<i class="fa-light fa-chevron-right"></i>', page + 1, { disabled: page >= this.last || !total, aria: 'Próxima página' });
    this.pages.innerHTML = html;
  }
  go(page, force = false) {
    page = Math.min(Math.max(1, page), this.last);
    if (page === this.o.page && !force) return;
    this.o.page = page;
    this.render();
    const detail = { page, perPage: this.o.perPage, offset: (page - 1) * this.o.perPage };
    this.nav.dispatchEvent(new CustomEvent('ttsc.pagination.change', { bubbles: true, detail }));
  }
  setTotal(total) { this.o.total = total; this.go(Math.min(this.o.page, this.last), true); }
}

// Lista de matrículas: recarrega via fetch a cada troca
document.querySelectorAll('[data-ttsc-pager]').forEach((nav) => {
  const pager = new TTSCPager(nav);
  nav.addEventListener('ttsc.pagination.change', async ({ detail }) => {
    const url = new URL(location.href);
    url.searchParams.set('page', detail.page);
    url.searchParams.set('per_page', detail.perPage);
    history.replaceState(null, '', url);
    const res = await fetch(`/academic/enrollments/list${url.search}`, { headers: { Accept: 'application/json' } });
    const { rows, total } = await res.json();
    document.querySelector('#enrollments-tbody').innerHTML = rows.map((r) => `<tr><td>${r.code}</td><td>${r.course_name}</td></tr>`).join('');
    if (total !== pager.o.total) pager.setTotal(total);
  });
});
```

### SQL

Paginação por `LIMIT/OFFSET` com total separado (o mesmo `WHERE` nas duas):

```sql
-- 1) Total para a faixa "Mostrando x–y de N"
SELECT COUNT(*) AS total
  FROM enrollments e
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid
   AND (:status = '' OR e.status = :status);

-- 2) Página (PDO: bindValue(':limit', $perPage, PDO::PARAM_INT) e ':offset' = ($page - 1) * $perPage)
SELECT e.id, e.uuid, e.code, e.status, e.enrollment_date, c.name AS course_name
  FROM enrollments e
  JOIN courses c ON c.uuid = e.course_uuid AND c.deleted_at IS NULL
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid
   AND (:status = '' OR e.status = :status)
 ORDER BY e.enrollment_date DESC, e.id DESC
 LIMIT :limit OFFSET :offset;

-- Alternativa em uma ida ao banco (MariaDB 10.2+ / MySQL 8): total por janela
SELECT e.id, e.uuid, e.code, e.status, e.enrollment_date, COUNT(*) OVER () AS total
  FROM enrollments e
 WHERE e.deleted_at IS NULL AND e.unit_uuid = :unit_uuid
 ORDER BY e.enrollment_date DESC, e.id DESC
 LIMIT :limit OFFSET :offset;

-- Keyset ("Carregar mais", listas longas): sem OFFSET, usa o último par (data, id) recebido
SELECT e.id, e.uuid, e.code, e.status, e.enrollment_date
  FROM enrollments e
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid
   AND (e.enrollment_date, e.id) < (:last_date, :last_id)
 ORDER BY e.enrollment_date DESC, e.id DESC
 LIMIT :limit;
```

O controller devolve `total`, `page`, `per_page` e as linhas; a view grava os três em `data-*` do `<nav>` e renderiza a primeira janela no servidor. O desempate por `e.id` mantém a ordem estável entre páginas; com PDO em modo emulado desligado, `LIMIT/OFFSET` precisa de `PDO::PARAM_INT`.

## Faça / Não faça

- **Faça:** um único rodapé por lista, sempre com total; voltar à página 1 ao filtrar.
- **Faça:** keyset quando o `OFFSET` passar de alguns milhares de linhas.
- **Não faça:** página atual verde com texto branco (2,5:1) — use `ttsc-accent-on`.
- **Não faça:** paginação sem `aria-current` nem rótulos nos botões de seta.
