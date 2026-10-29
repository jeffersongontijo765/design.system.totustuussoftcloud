# RecordDrawers

Os três drawers laterais (480 px) das páginas do chassi no padrão `view_item`: **View** (detalhes do registro com métricas e seções), **Novo** (formulário dos campos da ficha) e **Filtrar** (selects de status/enum), abertos por `window.openDrawer(id)` sobre o `#backdrop-overlay`.

## Quando usar

- Ver, criar, editar e filtrar registros de uma página do chassi sem sair da lista (tabela, cards, Kanban, lista de atenção).
- Formulários curtos (até ~10 campos). Cadastros longos usam o drawer de 5 passos de `chassis/drawers.php` (`steps`), ou uma página própria.
- Confirmação destrutiva: drawer `drawer-delete-confirm` (palavra-chave EXCLUIR) — não o View.
- Avisos curtos ou confirmação simples fora do chassi: [Modal](../Modal/README.md). Painel lateral genérico do ttscui: [Drawer](../Drawer/README.md).

## Anatomia

```
┌ .drawer-panel (fixed right, w-[480px]) ────────────────┐
│ [ico] Matrícula · detalhes                         [×] │ cabeçalho: tile + h3 + código + badge de status
│       [MAT-1001] [● DOCUMENTAÇÃO]                      │
├────────────────────────────────────────────────────────┤
│ ┌ MATRÍCULA ─────────────────────────────────────────┐ │ corpo (overflow-y-auto, bg-slate-50/40)
│ │ Diego Almeida  · Técnico em Enfermagem             │ │   título + sub
│ │ [Mensalidade R$ 2.078,66] [Frequência 77,3% ▓▓▓░]  │ │   drawer.metrics (grid 2)
│ └────────────────────────────────────────────────────┘ │
│ ┌ [pessoa] ALUNO E RESPONSÁVEL ──────────────────────────────┐ │   drawer.sections
│ │ Aluno: ………………………………… Diego Almeida                 │ │
├────────────────────────────────────────────────────────┤
│ [Fechar]                       [[excluir] Excluir] [[editar] Editar] │ rodapé
└────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Painel | `div.drawer-panel.fixed.top-0.right-0.h-full.w-[480px].max-w-full.z-50.flex.flex-col` | sim |
| Aberto | `.open.is-open.active` + `role=dialog`, `aria-modal=true`, `aria-hidden=false`, `aria-labelledby` (postos por `openDrawer`) | automático |
| Fechado | `.hidden` + `aria-hidden=true` + `inert` | automático |
| Backdrop | `#backdrop-overlay` (`fixed inset-0 bg-slate-900/40 backdrop-blur-[2px] z-40`) | sim |
| Cabeçalho | `div.p-4.border-b` com tile 36px, `h3`, botão fechar `onclick="closeAllDrawers()"` | sim |
| Campos preenchidos | `[data-v="code\|status\|title\|sub\|metrics\|section-N"]` (kit) | View |
| Corpo | `div.flex-1.overflow-y-auto.p-5.space-y-4.bg-slate-50/40` | sim |
| Rodapé | `div.p-4.border-t.shadow-lg` | sim |
| Filtro | `select[data-filter-key]` + `[data-model-filter-apply]` / `[data-model-filter-clear]` | Filtrar |

## Variantes

| Drawer | id no chassi (`domain_page.php`) | id no kit | Abre com |
|---|---|---|---|
| View | `drawer-view-item` | `model-drawer-view` | `data-action="domain-view-record"` / `data-model-view` |
| Novo | `new-opportunity-drawer` | `model-drawer-new` | `data-action="domain-open-create"`, "+ Adicionar" do Kanban |
| Editar | `edit-opportunity-drawer` | — | `data-action="domain-edit-record"` |
| Excluir | `drawer-delete-confirm` | — | `data-action="domain-delete-record"` |
| Filtrar | `drawer-filter` | `model-drawer-filter` | `data-action="domain-open-filter"` |
| Selecionados | `view-selected-drawer`, `drawer-delete-selected`, `drawer-export-batch` | — | barra de lote |

## API

**JS global (`assets/js/ttsc.overlays.js` + `ttsc.drawer.js`)**

| Função | Efeito |
|---|---|
| `window.openDrawer(id)` (= `sbDrawerOpen`) | resolve `#id` (aceita `#`, aliases legados e `<id>Drawer`), move o painel para o `body`, tira `hidden`/`inert`, põe `open is-open active`, `role=dialog`, mostra o backdrop, foca o 1º campo e dispara `ttsc:drawer-open` `{detail:{id, panel}}` |
| `window.closeAllDrawers(restoreFocus?)` | fecha todos (`.drawer-panel, .sb-drawer, .drawer`), esconde backdrops, devolve o foco ao gatilho |
| `window.closeDrawer(id)` (= `sbDrawerClose`) | fecha um |
| `window.TTSCOverlays.{open, closeAll, resolve}` | mesmas funções |
| `Esc` | fecha o drawer ativo; `Tab` fica preso dentro dele |
| `TTSCModelKit.blocks.drawers(page)` / `TTSCModelKit.fillView(page, row)` | HTML dos 3 drawers / preenche `data-v` e abre o View |

**Ficha**: `drawer.title`, `drawer.metrics[]` (campos; `pct` ganha barra), `drawer.sections[] = {title, icon, fields[]}`, `form[]` (campos do Novo; padrão: todos menos `code`), `fields[].required`, `fields[].placeholder`, `createDesc`, `entity.newLabel`. O Filtrar lista todo campo `status`/`stage`/`enum`.

**PHP**: `DrawerRegistry::forRoute($rota)` → `{route, title, module, portal, source, permission, statuses, writable, fields, variants, endpoints}`; `chassis/drawers.php` (`$chassis['drawers'] = ['view'=>['title','sub','fields'], 'create'=>['title','sub','steps','bodies','submit'], 'delete'=>['title','sub','subject']]`).

**Endpoints (`DrawerRegistry::forRoute()['endpoints']`)**

| Ação | Método e rota |
|---|---|
| Abrir View / Editar | `GET /api/v1/domain/records{rota}/{id}` |
| Salvar Novo | `POST /api/v1/domain/records{rota}` (campos validados por `DomainFields`; `references` só aceita linhas da tabela citada) |
| Salvar edição | `PUT /api/v1/domain/records{rota}/{id}` |
| Excluir | `DELETE /api/v1/domain/records{rota}/{id}` |
| Linha do tempo / chat | `GET\|POST /api/v1/domain/records{rota}/{id}/activity` e `/chat` (notas em `entity_comments`, 1–4000 caracteres) |

Escritas exigem `X-CSRF-TOKEN` (meta `csrf-token`), respeitam rate limit (30 em 15 min) e voltam 403/409/422 em falha de permissão, tenant ou validação.

## Acessibilidade

- `openDrawer` aplica `role="dialog"`, `aria-modal="true"` e `aria-labelledby` → `h3` do cabeçalho; o foco vai ao primeiro campo e volta ao gatilho no fechamento.
- `Esc` fecha; foco preso no painel; painéis fechados ficam `inert`.
- O botão "×" só-ícone tem `title`; adicione `aria-label="Fechar"` ao portar.
- Rótulos de formulário com `for`/`id` (`model-new-<campo>`, `model-filter-<campo>`); obrigatórios com `*` em `text-rose-600` e `required`.

## Modelos

### HTML

1) PHP real — `chassis/drawers.php` com o View e o Novo de 5 passos:

```php
<?php
$chassis['drawers'] = [
    'view' => ['title' => 'Solicitação de rematrícula', 'sub' => 'Detalhes da solicitação', 'fields' => [
        ['label' => 'Aluno',   'id' => 'student_name'],
        ['label' => 'Curso',   'id' => 'course_name'],
        ['label' => 'Turma',   'id' => 'class_name'],
        ['label' => 'Período', 'id' => 'period_name', 'mono' => true],
        ['label' => 'Status',  'id' => 'status', 'tone' => 'emerald'],
    ]],
    'create' => ['title' => 'Nova solicitação', 'sub' => 'Rematrícula 2027',
        'steps'  => ['Aluno', 'Curso e turma', 'Financeiro', 'Documentos', 'Revisão'],
        'bodies' => [$stepAluno, $stepCurso, $stepFinanceiro, $stepDocumentos, $stepRevisao],
        'submit' => 'Enviar solicitação'],
    'delete' => ['title' => 'Cancelar solicitação', 'sub' => 'Digite EXCLUIR para confirmar', 'subject' => $record['uuid'] ?? ''],
];
require base_path('resources/views/app/partials/chassis/drawers.php');
```

2) HTML gerado (preview, View aberto; uma seção):

```html
<div id="model-drawer-view" class="drawer-panel fixed top-0 right-0 h-full w-[480px] max-w-full bg-white z-50 flex flex-col overflow-hidden open is-open active"
     aria-hidden="false" role="dialog" aria-modal="true" tabindex="-1" aria-labelledby="model-drawer-view-title">
  <div class="p-4 border-b border-slate-100 flex items-center justify-between bg-white shrink-0">
    <div class="flex items-center space-x-3 min-w-0 flex-1 mr-2">
      <div class="w-9 h-9 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-600 flex items-center justify-center text-sm font-bold shadow-xs shrink-0"><i class="fa-light fa-id-card text-sm"></i></div>
      <div class="min-w-0 flex-1">
        <h3 class="font-bold text-sm text-slate-900 truncate" id="model-drawer-view-title">Matrícula · detalhes</h3>
        <div class="flex items-center gap-1.5 mt-1 flex-wrap">
          <span data-v="code" class="px-2 py-0.5 rounded font-mono text-[10px] font-bold uppercase bg-emerald-50 text-emerald-700 border border-emerald-200 whitespace-nowrap shrink-0">MAT-1001</span>
          <span data-v="status"><span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-blue-50 text-blue-700 border border-blue-200"><span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>Documentação</span></span>
        </div>
      </div>
    </div>
    <button type="button" onclick="closeAllDrawers()" class="w-8 h-8 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 flex items-center justify-center transition shrink-0 cursor-pointer" title="Fechar"><i class="fa-light fa-xmark text-sm"></i></button>
  </div>
  <div class="flex-1 overflow-y-auto p-5 space-y-4 text-xs bg-slate-50/40">
    <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs space-y-3">
      <div class="space-y-1 min-w-0">
        <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">Matrícula</span>
        <h4 data-v="title" class="font-bold text-slate-900 text-sm leading-snug break-words">Diego Almeida</h4>
        <div data-v="sub" class="text-slate-500 text-[11px]">Técnico em Enfermagem</div>
      </div>
      <div data-v="metrics" class="grid grid-cols-2 gap-3 pt-2">
        <div class="p-3 bg-slate-50 rounded-xl border border-slate-100 space-y-1">
          <span class="text-[10px] uppercase font-semibold text-slate-400 block">Frequência</span>
          <span class="font-mono font-bold text-base text-emerald-700 break-words">77,3%</span>
          <div class="w-full bg-slate-200 rounded-full h-1.5 mt-1 overflow-hidden"><div class="bg-emerald-500 h-1.5 rounded-full" style="width: 77.3%"></div></div>
        </div>
      </div>
    </div>
    <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs space-y-2.5">
      <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 block flex items-center gap-1.5"><i class="fa-light fa-user text-slate-400 text-xs"></i>Aluno e responsável</span>
      <div data-v="section-0">
        <div class="flex justify-between items-center gap-2 py-1.5 border-b border-slate-100"><span class="text-slate-500 shrink-0">Aluno:</span><strong class="font-mono text-slate-800 text-right break-all">Diego Almeida</strong></div>
        <div class="flex justify-between items-center gap-2 py-1.5"><span class="text-slate-500 shrink-0">Bolsista:</span><strong class="font-mono text-slate-800 text-right break-all">Sim</strong></div>
      </div>
    </div>
  </div>
  <div class="p-4 border-t border-slate-200 bg-white flex items-center justify-between gap-2.5 shadow-lg shrink-0">
    <button type="button" onclick="closeAllDrawers()" class="px-3.5 py-2 border border-slate-200 hover:bg-slate-50 rounded-xl text-xs font-semibold text-slate-600 transition cursor-pointer">Fechar</button>
    <div class="flex items-center gap-2">
      <button type="button" data-model-api="delete" class="px-3.5 py-2 border border-rose-200 text-rose-600 hover:bg-rose-50 rounded-xl text-xs font-semibold transition cursor-pointer"><i class="fa-light fa-trash-can text-xs mr-1"></i>Excluir</button>
      <button type="button" data-model-api="edit" class="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 active:bg-emerald-700 text-white rounded-xl font-semibold text-xs shadow-sm transition active:scale-95 cursor-pointer"><i class="fa-light fa-pen text-xs mr-1"></i>Editar Matrícula</button>
    </div>
  </div>
</div>
```

O Filtrar segue a mesma casca, com um `select[data-filter-key="status"]` por campo e "Limpar" / "Aplicar filtros" no rodapé.

### CSS

- `assets/css/ttsc.drawer.css` — "Universal .drawer-panel Sliding Transforms": painel fora da tela (`translateX(100%)`) e entrada com `.open`; dropdowns internos acima do painel.
- `assets/css/ttsc.commercial.css` — `.drawer-panel` / `.drawer-panel.open` do modelo comercial.
- `assets/css/ttsc.commercial.model.css` — escuro: `html.dark .drawer-panel` (fundo `#0f172a`/borda), `html.dark .drawer-panel .bg-white` e `.bg-slate-50` remapeados.

```css
/* Extensão por tokens: largura por tamanho do design system e foco do fechar */
.drawer-panel.is-lg { width: var(--ttsc-drawer-lg); }
.drawer-panel.is-sm { width: var(--ttsc-drawer-sm); }
.drawer-panel [onclick*="closeAllDrawers"]:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
#backdrop-overlay { background: var(--ttsc-scrim); }
```

### JS

```js
// View preenchido pelo endpoint real; Novo salvo com CSRF
const ROUTE = '/academic/enrollment/re-enrollment';
const API = '/api/v1/domain/records' + ROUTE;
const csrf = () => document.querySelector('meta[name="csrf-token"]')?.content || '';

document.addEventListener('click', async (ev) => {
  const btn = ev.target.closest('[data-action="domain-view-record"]');
  if (!btn) return;
  const res = await fetch(`${API}/${encodeURIComponent(btn.dataset.uuid)}`, { credentials: 'same-origin' });
  if (!res.ok) return window.showToast?.('Registro não encontrado.', 'error');
  const { record } = await res.json();
  const panel = document.getElementById('drawer-view-item');
  panel.querySelector('[data-v="title"]').textContent = record.student_name;
  panel.querySelector('[data-v="sub"]').textContent = `${record.course_name ?? ''} · ${record.class_name ?? ''}`;
  panel.querySelector('[data-v="code"]').textContent = record.period_name ?? '';
  window.openDrawer('drawer-view-item');
});

document.getElementById('drawer-create-form')?.addEventListener('submit', async (ev) => {
  ev.preventDefault();
  const res = await fetch(API, {
    method: 'POST', credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRF-TOKEN': csrf() },
    body: JSON.stringify(Object.fromEntries(new FormData(ev.target))),
  });
  const body = await res.json();
  if (!res.ok || !body.success) return window.showToast?.(body.error || 'Não foi possível salvar.', 'error');
  window.closeAllDrawers();
  window.showToast?.('Solicitação criada.', 'success');
});

document.addEventListener('ttsc:drawer-open', (ev) => console.debug('drawer aberto', ev.detail.id));
```

### SQL

```sql
-- View: registro por uuid (colunas do contrato da página)
SELECT uuid, request_type, student_name, course_name, class_name, shift, modality, period_name, status, created_at, updated_at
  FROM inst_secretariat_reenrollment
 WHERE uuid = :uuid
 LIMIT 1;

-- View de matrícula com aluno, curso, turma e mensalidade
SELECT e.uuid, e.code, u.name AS aluno, u.email, c.name AS curso, cl.name AS turma,
       e.shift, e.status, e.enrollment_date, abr.monthly_tuition
  FROM enrollments e
  JOIN users u        ON u.uuid = e.student_uuid
  JOIN courses c      ON c.uuid = e.course_uuid
  LEFT JOIN classes cl ON cl.uuid = e.class_uuid
  LEFT JOIN academic_billing_rules abr ON abr.course_uuid = e.course_uuid AND abr.status = 'active'
 WHERE e.uuid = :uuid AND e.deleted_at IS NULL;

-- Opções do Filtrar: vocabulário real do status
SELECT value, label
  FROM ref_enum_enrollment_requests_status_21ca774d7caf
 WHERE is_active = 1 AND deleted_at IS NULL
 ORDER BY sort_order;

-- Linha do tempo do drawer (notas da conversa)
SELECT ec.uuid, ec.user_uuid, ec.content, ec.created_at
  FROM entity_comments ec
 WHERE ec.entity_type = 'enrollment_requests' AND ec.entity_uuid = :uuid
 ORDER BY ec.created_at DESC
 LIMIT 50;
```

O `GET …/{id}` devolve a linha (só colunas do contrato, nunca segredos) e o JS preenche os `data-v`; no SSR, `$chassis['drawers']['view']['fields']` usa as mesmas chaves.

## Faça / Não faça

- **Faça:** um drawer aberto por vez — `openDrawer` fecha os demais.
- **Faça:** salvar pelo endpoint e só então fechar; erro mantém o drawer aberto com a mensagem.
- **Não faça:** escrever `display:block` à mão; use `openDrawer`/`closeAllDrawers` (classes, `inert`, foco e backdrop).
- **Não faça:** mostrar no View colunas fora do contrato (`columns` de `page-domain-sources.php`).
