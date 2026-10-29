# RecordCards

Aba "Cards / Grade" do chassi: os mesmos registros da tabela em cartões de 3 colunas, cada um com título, linha secundária, badge de etapa/status, caixa de linha + código, métricas da ficha, barra opcional e ações; busca e paginação próprias.

## Quando usar

- Quando poucos atributos bastam para reconhecer o registro e a leitura visual ajuda (matrícula com curso, turno, mensalidade e frequência).
- Sempre como visão alternativa da [RecordsTable](../RecordsTable/README.md) — mesmo conjunto, mesmos filtros, mesmos drawers.
- Não use para comparar muitas colunas ou ordenar (use a tabela) nem para fluxo de etapas (use [KanbanBoard](../KanbanBoard/README.md)).
- Um cartão isolado de conteúdo, fora do chassi, é [Card](../Card/README.md).

## Anatomia

```
┌ article ─────────────────────────────────────┐
│ [ico] Diego Almeida              [DOCUMENTAÇÃO]│ 1. título (abre View) + sub + badge da etapa
│       Técnico em Enfermagem                    │
│ ┌ bg-slate-50 ─────────────────────────────┐  │ 2. cardLine (ou badge de status) + código
│ │ Manhã                          MAT-1001  │  │
│ └──────────────────────────────────────────┘  │
│ Mensalidade                     R$ 2.078,66    │ 3. cardBar (barra) + cardFields (métricas)
│ Frequência                           77,3%    │
│───────────────────────────────────────────────│
│ [[ver] Ver registro]                    [[editar]] [[excluir]] │ 4. ações
└───────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Painel | `#view-cards.space-y-4[role=tabpanel]` | sim |
| Cabeçalho da visão | `header` com `fa-table-cells-large` e contador | sim |
| Busca | `#<id>-search` em `div[role=search]` | sim |
| Grade | `#model-cards-grid` / `#domain-cards-grid.grid.grid-cols-1.md:grid-cols-2.lg:grid-cols-3.gap-4` | sim |
| Cartão | `article.bg-white.border.rounded-2xl.p-4.hover:border-emerald-300.hover:shadow-md` | sim |
| Título | `h4.line-clamp-1[data-model-view]` | sim |
| Badge da etapa | `span.font-mono.bg-<tom>-50.text-<tom>-700.border-<tom>-200` | não |
| Caixa de linha | `div.mt-3.p-2.5.rounded-xl.bg-slate-50` | não |
| Métricas | `div.text-[10px]` rótulo + `span.font-mono.font-semibold` | não |
| Ações | "Ver registro" (gradiente verde) + editar/excluir 32px | sim |
| Vazio filtrado | `#<id>-empty` | sim |
| Paginação | `.ttsc-pagination-standard` (no chassi real `.ttsc-pagination-card`, 12/24/48/96 por página) | sim |

## Estados

| Estado | Como |
|---|---|
| Normal / hover | borda `emerald-300` + `shadow-md` |
| Sem resultado | `#<id>-empty` "Nenhuma matrícula corresponde aos filtros" |
| Sem registros | `.ttsc-chassis-empty-card` "Nenhum cartão para exibir" + "Novo registro" se gravável |
| Somente leitura | sem editar/excluir |

## API

**Ficha**

| Campo | Uso |
|---|---|
| `titleField`, `subField` | título e linha secundária |
| `stageField` (ou `statusField`) | badge do canto (tom da etapa) |
| `statusField` ≠ `stageField` | badge de status vai para a caixa de linha |
| `cardLine` | texto da caixa (ex.: turno) |
| `codeField` | código à direita da caixa |
| `cardFields[]` | métricas (rótulo/valor formatado por `type`) |
| `cardBar` | campo `pct`/numérico desenhado como barra no tom da etapa |
| `cardsTitle`, `cardsDesc`, `chip` | cabeçalho da visão |

**JS**

| API | Efeito |
|---|---|
| `TTSCModelKit.blocks.cards(page, rows)` | HTML da aba (cabeçalho, busca, vazio, grade, paginação) |
| `TTSCModelKit.blocks.card(page, row)` | HTML de um `article` |
| `[data-model-view]` / `data-action="domain-view-record"` | abre o drawer View |
| `data-action="domain-open-create"` | ação do estado vazio |

Os cartões compartilham o predicado de filtro da tabela (`window.__modelFilters` no kit; `apply()` no `domain_page.php`) — o drawer Filtrar vale para as duas visões.

**Endpoints**: mesmos da tabela — `GET /api/v1/domain/records{rota}?search=&status=&page=&per_page=` para a grade; `GET …/{id}` para o drawer; `PUT`/`DELETE …/{id}` nas ações.

## Acessibilidade

- O título é o alvo principal; "Ver registro" repete a ação como `<button>` para teclado.
- Editar/Excluir são só-ícone: use `aria-label` com o nome do registro ao portar ("Excluir matrícula de Diego Almeida").
- Use `article` por cartão e mantenha a ordem de leitura igual à da tabela.
- Badge da etapa: texto + cor, `text-<tom>-700` sobre `<tom>-50` ≥ 4,6:1.

## Modelos

### HTML

1) PHP real (`chassis/domain_page.php`, VIEW 3) — um `article` por registro da página atual, com paginação de 12:

```php
<div id="view-cards" class="space-y-4" style="display: none;">
  <header class="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm md:flex-row md:items-center md:justify-between">
    … <h3 class="text-sm font-semibold text-slate-900"><?= $e('Cartões') ?> — <?= $e($bannerTitle) ?></h3> …
  </header>
  <?php if ($records === []): ?>
  <div class="ttsc-chassis-empty-card">… Nenhum cartão para exibir …</div>
  <?php else: ?>
  <input type="search" id="domain-cards-search" class="ttsc-input ttsc-input-sm w-full has-leading-icon" aria-controls="domain-cards-grid">
  <div id="domain-cards-grid" class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
    <?php foreach ($records as $r): ?>
    <article …><?= $e($recordLabel($r)) ?> … <?= $statusText((string) ($r[$statusKey] ?? '')) ?></article>
    <?php endforeach; ?>
  </div>
  <div id="domain-cards-pagination" class="ttsc-pagination-standard ttsc-pagination-card rounded-2xl">
    … <div class="per-page" data-ttsc-page-size-control><select id="domain-cards-per-page">12 / 24 / 48 / 96</select></div>
  </div>
  <?php endif; ?>
</div>
```

2) HTML gerado (preview, 1 cartão):

```html
<div id="model-cards-grid" class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
  <article class="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs hover:border-emerald-300 hover:shadow-md transition flex flex-col justify-between space-y-3">
    <div>
      <div class="flex items-start justify-between gap-2">
        <div class="flex items-center space-x-2 min-w-0">
          <span class="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0"><i class="fa-light fa-id-card"></i></span>
          <div class="min-w-0">
            <h4 class="font-bold text-xs text-slate-900 leading-tight line-clamp-1 hover:text-emerald-700 transition cursor-pointer" data-model-view="m0">Diego Almeida</h4>
            <span class="text-[10px] text-slate-400 truncate block">Técnico em Enfermagem</span>
          </div>
        </div>
        <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-blue-50 text-blue-700 font-bold border border-blue-200 shrink-0">Documentação</span>
      </div>
      <div class="mt-3 p-2.5 rounded-xl bg-slate-50 border border-slate-100 space-y-1 text-xs">
        <div class="flex items-center justify-between text-[11px]">
          <span class="text-slate-500 font-medium truncate flex items-center gap-1">Manhã</span>
          <span class="font-mono text-slate-400 text-[10px]">MAT-1001</span>
        </div>
      </div>
      <div class="mt-3 space-y-1.5">
        <div class="flex items-center justify-between text-[10px] text-slate-400 pt-0.5"><span>Mensalidade</span><span class="font-mono font-semibold text-slate-600">R$&nbsp;2.078,66</span></div>
        <div class="flex items-center justify-between text-[10px] text-slate-400 pt-0.5"><span>Frequência</span><span class="font-mono font-semibold text-slate-600">77,3%</span></div>
      </div>
    </div>
    <div class="pt-2.5 border-t border-slate-100 flex items-center justify-between gap-2">
      <button type="button" data-model-view="m0" class="group inline-flex items-center gap-1.5 px-3 py-1.5 h-8 rounded-xl text-xs font-semibold text-emerald-700 hover:text-emerald-800 bg-gradient-to-r from-emerald-50 to-teal-50/70 hover:from-emerald-100 hover:to-teal-100 border border-emerald-200/90 hover:border-emerald-300 shadow-2xs transition-all duration-150 active:scale-[0.97] whitespace-nowrap cursor-pointer">
        <i class="fa-light fa-eye text-xs text-emerald-600 transition-transform duration-150 group-hover:scale-110 shrink-0"></i><span>Ver registro</span>
      </button>
      <div class="inline-flex items-center gap-1 shrink-0">
        <button type="button" data-model-api="edit" class="w-8 h-8 rounded-xl border border-slate-200 text-slate-600 hover:text-slate-800 hover:bg-slate-50 hover:border-slate-300 flex items-center justify-center transition-all duration-150 active:scale-[0.95] cursor-pointer shadow-2xs" title="Editar"><i class="fa-light fa-pen text-xs"></i></button>
        <button type="button" data-model-api="delete" class="w-8 h-8 rounded-xl border border-rose-200 text-rose-600 hover:text-rose-700 hover:bg-rose-50 hover:border-rose-300 flex items-center justify-center transition-all duration-150 active:scale-[0.95] cursor-pointer shadow-2xs" title="Excluir"><i class="fa-light fa-trash-can text-xs"></i></button>
      </div>
    </div>
  </article>
</div>
```

### CSS

Utilitários do runtime; escuro por `assets/css/ttsc.commercial.model.css` (`html.dark .bg-white`, `.bg-slate-50`, `.border-slate-100`, gradiente `from-emerald-50`). `ttsc.commercial.css` define `.ttsc-chassis-empty-card` e `ttsc.pagination.css` a variante `.ttsc-pagination-card` (rodapé com borda e raio próprios).

```css
/* Extensão por tokens: cartão selecionável por teclado e destaque do cartão aberto no drawer */
#model-cards-grid article:focus-within { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
#model-cards-grid article[aria-current="true"] {
  border-color: var(--ttsc-accent-border);
  box-shadow: 0 0 0 3px var(--ttsc-accent-soft);
}
```

### JS

```js
// Grade de cartões alimentada pelo endpoint real, 12 por página como no chassi
const API = '/api/v1/domain/records/academic/enrollment/re-enrollment';
const grid = document.getElementById('domain-cards-grid');
const fmt = new Intl.DateTimeFormat('pt-BR', { dateStyle: 'medium' });

async function loadCards(page = 1, per = 12, search = '') {
  const qs = new URLSearchParams({ page, per_page: Math.max(10, per), search });
  const res = await fetch(`${API}?${qs}`, { credentials: 'same-origin' });
  const { records, totalRecords } = await res.json();
  grid.innerHTML = records.map((r) => `
    <article class="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs hover:border-emerald-300 hover:shadow-md transition flex flex-col justify-between space-y-3">
      <h4 class="font-bold text-xs text-slate-900 line-clamp-1" data-action="domain-view-record" data-uuid="${r.uuid}">${r.student_name}</h4>
      <span class="text-[10px] text-slate-400">${r.course_name ?? ''} · ${r.class_name ?? ''}</span>
      <div class="flex justify-between text-[10px] text-slate-400"><span>Solicitado em</span>
        <span class="font-mono font-semibold text-slate-600">${fmt.format(new Date(r.created_at))}</span></div>
    </article>`).join('');
  document.getElementById('domain-cards-total').textContent = totalRecords;
}
loadCards();
```

### SQL

Cartões de matrícula com as métricas da ficha (`cardFields: tuition, attendance, enrollment_date`, `cardLine: shift`):

```sql
SELECT e.uuid, e.code, u.name AS aluno, c.name AS curso, e.status, e.shift, e.enrollment_date,
       abr.monthly_tuition                                          AS mensalidade,
       ROUND(100 * SUM(a.status IN ('present', 'late')) / NULLIF(COUNT(a.id), 0), 1) AS frequencia
  FROM enrollments e
  JOIN users u   ON u.uuid = e.student_uuid
  JOIN courses c ON c.uuid = e.course_uuid
  LEFT JOIN academic_billing_rules abr ON abr.course_uuid = e.course_uuid AND abr.status = 'active'
  LEFT JOIN attendance a ON a.enrollment_uuid = e.uuid
 WHERE e.deleted_at IS NULL
 GROUP BY e.uuid, e.code, u.name, c.name, e.status, e.shift, e.enrollment_date, abr.monthly_tuition
 ORDER BY e.enrollment_date DESC
 LIMIT :limit OFFSET :offset;
```

O PHP passa cada linha como `$records[]`; o cartão formata `mensalidade` em `R$` e `frequencia` em `%`.

## Faça / Não faça

- **Faça:** 2–4 métricas por cartão; o resto fica no drawer.
- **Faça:** manter busca e filtros iguais aos da tabela.
- **Não faça:** cartões com alturas muito diferentes (textos longos sem `line-clamp`).
- **Não faça:** ação primária verde sólida em cada cartão — o "Ver registro" é secundário de propósito.
