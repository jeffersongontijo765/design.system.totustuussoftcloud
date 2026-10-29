# KpiView

Aba KPI do chassi: faixa de 4 cards de indicador (rótulo, valor mono, unidade, chips ou barra, rodapé) seguida do painel de distribuição e da lista de atenção.

## Quando usar

- Como primeira aba das páginas Records, Pipeline e Dashboard — a visão-resumo do mesmo conjunto que a tabela lista.
- Indicadores que se calculam sobre os registros da página (contagem por status, soma de mensalidade, média de frequência).
- Quando a home precisa abrir com índice composto, deltas e limites (faixa executiva), use [ExecutiveStrip](../ExecutiveStrip/README.md) — o KpiView é a faixa simples de indicadores.
- Não use para séries temporais ou comparações entre categorias com eixo: isso é [AnalyticsPanels](../AnalyticsPanels/README.md).
- Não use cards de KPI soltos em telas sem registros (ex.: configurações) nem como widget de home rica: para isso há os widgets (`WidgetsSmallHorizontal` etc.).

## Anatomia

```
┌ card KPI ───────────────────┐ ×4 (grid 1 / sm:2 / lg:4)
│ MATRÍCULAS ATIVAS     [ico] │  1. cabeçalho: rótulo 11px caps + sublabel + tile 32px
│ Ano letivo 2026             │
│ 25 Alunos          (Mensal) │  2. valor 24px mono + unidade + pill
│ [5 Em análise][5 Documentação] 3. chips  —ou— barra de progresso
│ Ticket médio: R$ 1.540,00   │  4. rodapé border-t (opcional)
└─────────────────────────────┘
┌ Distribuição (lg:col-span-2) ──────────────┐ ┌ Atenção ───────────────┐
│ Matrículas por curso            Total: 48  │ │ [!] Indeferidas          │
│ ● Ensino Médio (21)   21 (43,8%) ▓▓▓▓░░░░  │ │ [Felipe Duarte  INDEF.]│
└────────────────────────────────────────────┘ └────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Painel | `#view-kpi.space-y-5[role=tabpanel]` | sim |
| Grade | `div.grid.grid-cols-1.sm:grid-cols-2.lg:grid-cols-4.gap-4` | sim |
| Card | `div.bg-white.border.rounded-xl.p-4.shadow-xs` (`kpi-card[data-kpi-id]` no chassi real), `title` = fórmula | sim |
| Valor | `span.text-2xl.font-bold.font-mono` | sim |
| Chips | `span.text-[10px].rounded.bg-<tom>-50.text-<tom>-700.border-<tom>-200` | não |
| Barra | `div.bg-slate-100.h-1.5` > `div.bg-<tom>-500` com `width:%` | não |
| Rodapé | `div.mt-3.pt-2.5.border-t.border-slate-100` | não |
| Distribuição | card `lg:col-span-2` com uma barra por valor de `breakdown.by` | não |
| Atenção | card com até 5 `button[data-model-view]` + badge de status; vazio = caixa verde com `fa-circle-check` | não |

## Variantes

| Variante | Campo da ficha | Visual |
|---|---|---|
| Contagem | `value:{agg:"count", where}` + `unitLabel` | "25 Alunos" |
| Dinheiro | `value:{agg:"sum", field}` + `unit:"money"` | "R$ 38.512,40" (Intl, `currency` da ficha) |
| Percentual | `value:{agg:"avg"\|"share"}` + `unit:"%"` | "81,3%" |
| Com chips | `chips:[{label, tone, value}]` | decomposição por status |
| Com barra | `bar:{label, num, den, unit}` | progresso `num/den` |
| Com pill | `pill` ou `pillShare` + `pillShareLabel` | pill neutra ou com % no tom |
| Tons | `tone`: `emerald`, `blue`, `amber`, `purple`, `rose`, `slate` | `TTSCModelKit.tones` |

## API

**Ficha — `kpis[]`**

| Campo | Tipo | Uso |
|---|---|---|
| `label`, `sub`, `icon`, `tone` | string | cabeçalho e tile |
| `value.agg` | `count\|sum\|avg\|min\|max\|share` | agregação sobre os registros |
| `value.field` | chave de `fields[]` | coluna somada/média |
| `value.where` | `{campo: valor \| [valores]}` | filtro (igualdade ou `IN`) |
| `value.of` | `{…}` | denominador de `share` |
| `unit` | `money\|%\|ms\|decimal` | formatação; sem `unit` = inteiro |
| `unitLabel` | string | palavra após o valor ("Alunos") |
| `chips[]`, `bar`, `footer[]`, `pill`, `pillShare` | ver Variantes | |
| `formula` | string | regra de negócio; vai para `title` do card e para o contrato do backend |

**Ficha — `breakdown`**: `by` (campo `enum`/`status`/`stage`), `title`, `desc`, `icon`, `attention:{where, badge, title, desc, empty}`.

**PHP — `chassis/kpi.php`** (`$kpiCards[]`): `label`, `sublabel`, `value`, `meta` (pill), `icon`, `tone` (`emerald|blue|purple|amber|rose|indigo`), `progress` (0–100), `progress_label`, `progress_value`, `chips[] = ['label','value','tone']`, `footer`, `footer_value`, `footer_note`. Em `domain_page.php` os cards nascem de `$kanbanColumns` (status "bons" × "de atenção") e da primeira coluna numérica; cada card tem `data-kpi-id` para o refresh ao vivo.

**JS**

| API | Efeito |
|---|---|
| `TTSCModelKit.blocks.kpi(page, rows)` | HTML de `#view-kpi` (cards + `breakdown`) |
| `TTSCModelKit.blocks.breakdown(page, rows, bd)` | só distribuição + atenção |
| `[data-model-view="<id>"]` | abre o drawer View do registro (`fillView`) |
| `assets/js/kpi-pages/<rail>/…` | refresh ao vivo: lê `GET /api/v1/kpi{rota}` e grava nos `[data-kpi-id]` |

**Endpoints**

| Rota | Resposta |
|---|---|
| `GET /api/v1/kpi{rota}` (`PerPageKpiController::show`) | `{success, available, route, table, totalRecords, statusCounts, kpiCards[]}` |
| `GET /api/v1/domain/records{rota}?status=<valor>` | lista filtrada por um status do vocabulário (`known_statuses`) |

## Acessibilidade

- O rótulo vem antes do valor no DOM; leitores leem "Matrículas ativas, Ano letivo 2026, 25 Alunos".
- A fórmula fica em `title` (só mouse). Se ela importa para a decisão, escreva-a no `sub`.
- Os chips usam texto + cor; nunca apenas a cor. `text-<tom>-700` sobre `<tom>-50` ≥ 4,6:1.
- Itens da lista de atenção são `<button>` (teclado abre o drawer).

## Modelos

### HTML

1) PHP real — página que monta seus cards e inclui o partial (`resources/views/app/partials/chassis/kpi.php`):

```php
<?php
$kpiCards = [
    ['label' => 'Matrículas ativas', 'sublabel' => 'Ano letivo 2026', 'value' => $kpi['active'],
     'icon' => 'fa-user-graduate', 'tone' => 'emerald',
     'chips' => [['label' => 'Em análise', 'value' => $kpi['pending_review'], 'tone' => 'amber'],
                 ['label' => 'Documentação', 'value' => $kpi['submitted'], 'tone' => 'blue']]],
    ['label' => 'Receita mensal', 'sublabel' => 'Mensalidades ativas', 'value' => 'R$ ' . number_format($kpi['revenue'], 2, ',', '.'),
     'meta' => 'Mensal', 'icon' => 'fa-sack-dollar', 'tone' => 'blue',
     'footer' => 'Ticket médio:', 'footer_value' => 'R$ ' . number_format($kpi['ticket'], 2, ',', '.')],
    ['label' => 'Frequência média', 'sublabel' => 'Últimos 30 dias', 'value' => $kpi['attendance_pct'] . '%',
     'icon' => 'fa-calendar-check', 'tone' => 'amber', 'progress' => $kpi['attendance_pct'],
     'progress_label' => 'Meta 75%', 'progress_value' => $kpi['attendance_pct'] . '%'],
    ['label' => 'Indeferidas', 'sublabel' => 'Exigem contato', 'value' => $kpi['rejected'],
     'icon' => 'fa-triangle-exclamation', 'tone' => 'rose'],
];
$panes['kpi'] = (function () use ($kpiCards) { ob_start(); require base_path('resources/views/app/partials/chassis/kpi.php'); return ob_get_clean(); })();
```

2) HTML gerado (preview; um card e uma linha da distribuição):

```html
<div id="view-kpi" class="space-y-5" role="tabpanel" aria-labelledby="tab-btn-kpi">
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
    <div class="bg-white dark:bg-[#1a1c23] border border-slate-200/80 dark:border-white/10 rounded-xl p-4 shadow-xs relative flex flex-col justify-between hover:border-emerald-300 dark:hover:border-emerald-500/50 transition duration-150"
         title="COUNT(enrollments WHERE status = 'active' AND deleted_at IS NULL)">
      <div>
        <div class="flex items-start justify-between gap-2">
          <div>
            <span class="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 block leading-none">Matrículas ativas</span>
            <span class="text-[10px] text-slate-400 dark:text-slate-500 font-normal mt-0.5 block">Ano letivo 2026</span>
          </div>
          <div class="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 border border-emerald-100 dark:border-emerald-800/40 flex items-center justify-center shrink-0">
            <i class="fa-light fa-user-graduate text-xs"></i>
          </div>
        </div>
        <div class="mt-3 flex items-baseline justify-between gap-2">
          <div class="flex items-baseline gap-1.5">
            <span class="text-2xl font-bold font-mono text-slate-900 dark:text-white tracking-tight">25</span>
            <span class="text-xs font-medium text-slate-500 dark:text-slate-400">Alunos</span>
          </div>
        </div>
        <div class="mt-3 pt-1 flex flex-wrap gap-1.5">
          <span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-50 text-amber-700 font-medium border border-amber-200">5 Em análise</span>
          <span class="text-[10px] px-1.5 py-0.5 rounded bg-blue-50 text-blue-700 font-medium border border-blue-200">5 Documentação</span>
        </div>
      </div>
    </div>
    <!-- … mais 3 cards -->
  </div>
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
    <div class="lg:col-span-2 bg-white border border-slate-200 rounded-2xl p-5 shadow-xs space-y-4">
      <div class="flex items-start justify-between gap-3 border-b border-slate-100 pb-3">
        <div>
          <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2"><i class="fa-light fa-layer-group text-emerald-600"></i>Matrículas por curso</h3>
          <p class="text-xs text-slate-500 mt-0.5">Distribuição atual</p>
        </div>
        <span class="px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-[10px] font-mono font-bold text-emerald-700">Total: 48</span>
      </div>
      <div class="space-y-1.5">
        <div class="flex items-center justify-between text-xs">
          <span class="flex items-center gap-2 font-semibold text-slate-700"><span class="w-2 h-2 rounded-full bg-blue-500"></span>Ensino Médio <span class="text-[10px] font-normal text-slate-400">(21 Matrículas)</span></span>
          <span class="font-mono font-bold text-slate-900">21 <span class="text-[10px] font-normal text-slate-400">(43,8%)</span></span>
        </div>
        <div class="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden"><div class="bg-blue-500 h-1.5 rounded-full" style="width: 43.8%"></div></div>
      </div>
    </div>
    <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs space-y-3">
      <!-- cabeçalho "Indeferidas" + até 5 itens -->
      <button type="button" data-model-view="m0" class="w-full text-left flex items-center justify-between gap-2 p-2.5 rounded-xl border border-slate-200 hover:border-amber-300 hover:bg-amber-50/40 transition cursor-pointer">
        <span class="min-w-0"><span class="block text-xs font-semibold text-slate-900 truncate">Felipe Duarte</span><span class="block text-[10px] font-mono text-slate-400">MAT-1001</span></span>
        <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-rose-50 text-rose-700 border border-rose-200 shrink-0"><span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span>Indeferido</span>
      </button>
    </div>
  </div>
</div>
```

### CSS

Cards e painéis são utilitários do runtime; o escuro vem das classes `dark:` embutidas no card (`dark:bg-[#1a1c23]`, `dark:border-white/10`, `dark:text-white`) e das regras `html.dark .bg-white`/`.border-slate-200` em `assets/css/ttsc.commercial.model.css`. `assets/css/ttsc.kpi-widgets.css` estiliza `.kpi-card` dos widgets de home.

```css
/* Extensão por tokens: valor negativo/alerta e foco do card clicável */
.kpi-card[data-trend="down"] .font-mono.text-2xl { color: var(--ttsc-danger-text); }
.kpi-card:focus-within { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.kpi-card .border-t { border-color: var(--ttsc-border-soft); }
```

### JS

```js
// Atualiza os cards a partir do endpoint real de KPI da página
async function refreshKpis(route) {
  const res = await fetch('/api/v1/kpi' + route, { credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' } });
  const body = await res.json();     // { success, available, totalRecords, statusCounts:{active: 25, …}, kpiCards:[{id, value, …}] }
  if (!body.available) return;
  body.kpiCards.forEach((card) => {
    const el = document.querySelector(`[data-kpi-id="${card.id}"] .text-2xl`);
    if (el) el.textContent = new Intl.NumberFormat('pt-BR').format(card.value);
  });
}
refreshKpis('/academic/enrollment/re-enrollment');

// Ou renderizar a aba inteira a partir da ficha (registros de amostra determinísticos)
fetch('../../models/academico.json').then((r) => r.json()).then((sheet) => {
  const t = { portal: { label: 'Administração' }, module: { label: 'Acadêmico' }, page: { label: 'Matrículas', route: '/academico/matriculas' } };
  TTSCModelKit.render(t, sheet.pages['/academico/matriculas'], { header: false, banner: false, tabs: false });
  TTSCModelKit.switchTab('kpi');
});
```

### SQL

As quatro fórmulas de `kpis[].formula` da ficha acadêmica, numa leitura cada (MariaDB 10.11 / MySQL 8):

```sql
-- 1. Matrículas ativas + chips (status do vocabulário real de enrollments)
SELECT SUM(e.status = 'active')              AS ativas,
       SUM(e.status = 'conditional_pending') AS pendentes,
       SUM(e.status = 'locked')              AS trancadas
  FROM enrollments e
 WHERE e.deleted_at IS NULL
   AND e.period_uuid = :period_uuid;

-- 2. Receita mensal e ticket médio: regra de cobrança ativa do curso de cada matrícula ativa
SELECT COALESCE(SUM(abr.monthly_tuition), 0) AS receita_mensal,
       AVG(abr.monthly_tuition)              AS ticket_medio
  FROM enrollments e
  JOIN academic_billing_rules abr
    ON abr.course_uuid = e.course_uuid AND abr.status = 'active'
 WHERE e.deleted_at IS NULL
   AND e.status = 'active';

-- 3. Frequência média e menor frequência por matrícula (últimos 30 dias)
SELECT ROUND(AVG(pct), 1) AS frequencia_media, ROUND(MIN(pct), 1) AS menor_frequencia
  FROM (SELECT a.enrollment_uuid,
               100 * SUM(a.status IN ('present', 'late')) / COUNT(*) AS pct
          FROM attendance a
         WHERE a.lesson_date >= CURRENT_DATE - INTERVAL 30 DAY
         GROUP BY a.enrollment_uuid) t;

-- 4. Solicitações indeferidas (funil real fica em enrollment_requests)
SELECT COUNT(*) AS indeferidas
  FROM enrollment_requests er
 WHERE er.deleted_at IS NULL AND er.status = 'rejected';

-- Distribuição por curso (breakdown.by = course)
SELECT c.uuid, c.name, COUNT(e.id) AS total,
       ROUND(100 * COUNT(e.id) / NULLIF(SUM(COUNT(e.id)) OVER (), 0), 1) AS pct
  FROM enrollments e
  JOIN courses c ON c.uuid = e.course_uuid AND c.deleted_at IS NULL
 WHERE e.deleted_at IS NULL
 GROUP BY c.uuid, c.name
 ORDER BY total DESC;

-- Lista de atenção (5 primeiras indeferidas)
SELECT er.uuid, er.student_name, er.course_name, er.rejection_reason
  FROM enrollment_requests er
 WHERE er.deleted_at IS NULL AND er.status = 'rejected'
 ORDER BY er.reviewed_at DESC
 LIMIT 5;
```

O controlador monta `$kpiCards` com esses números (o valor do card 2 formatado em `R$`) e passa a distribuição como `$distribution`; a lista de atenção vira os botões `data-model-view`/`data-action="domain-view-record"` com o `uuid`.

## Faça / Não faça

- **Faça:** escrever a fórmula de cada card na ficha (`formula`) — é o contrato do backend.
- **Faça:** quatro cards; o quinto número vai em chip, barra ou rodapé.
- **Não faça:** KPI que não reconcilia com a tabela (filtros diferentes) — o kit calcula tudo do mesmo conjunto por isso.
- **Não faça:** usar status inexistentes no vocabulário real (`ref_enum_*`); mapeie os rótulos da ficha para os valores do banco.
