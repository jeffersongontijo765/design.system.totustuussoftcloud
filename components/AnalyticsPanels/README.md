# AnalyticsPanels

Aba Analytics do chassi: grade de painéis `TTSCAnalytics` (Chart.js 4) — barras, rosca ou linha — cada um com badges, legenda, total e um drawer de filtros próprio por gráfico.

## Quando usar

- Agregações dos registros da página: por curso, por status, novas matrículas por mês.
- É a aba de abertura do arquétipo Report ([PageReport](../PageReport/README.md)) e aparece em Dashboard e Records quando a ficha tem `analytics[]`.
- Não use para um número isolado (use [KpiView](../KpiView/README.md)) nem para listas (use [RecordsTable](../RecordsTable/README.md)).
- Gráfico avulso fora do chassi (widgets de home): veja os widgets `Widget*`; gráficos genéricos: [ApexCharts](../ApexCharts/README.md) ou [AmCharts](../AmCharts/README.md).

## Anatomia

```
.ttsc-analytics-grid (2 colunas; .is-wide ocupa a linha)
┌ article.ttsc-analytics-card ─────────────────────────────┐
│ ▥ Matrículas por curso                   [[filtros] Filtros]      │ .ttsc-analytics-head  (abre drawer-analytics-<id>)
│ Situação atual                                            │
│ [Situação atual] [48 Matrículas]                          │ .ttsc-analytics-badges
│ ┌ .ttsc-analytics-plot ────────────────────────────────┐  │ canvas[role=img][tabindex=0]
│ │  ▇▇  ▇  ▅  ▅                                         │  │
│ └──────────────────────────────────────────────────────┘  │
│ ■ Ensino Médio ■ Fundamental II …            Total 48     │ .ttsc-analytics-foot
└───────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Host | `div` (`#model-analytics-panels`, `#dashboard-analytics-panels`) — recebe `.ttsc-analytics-grid` (`.has-three-columns` opcional) | sim |
| Painel | `article.ttsc-analytics-card[data-analytics-id]` (`.is-wide`) | gerado |
| Cabeçalho | `header.ttsc-analytics-head` + `button.ttsc-analytics-action[aria-controls=drawer-analytics-<id>]` | gerado |
| Badges | `.ttsc-analytics-badges > .ttsc-analytics-badge` | gerado |
| Gráfico | `.ttsc-analytics-content > .ttsc-analytics-plot > canvas[role=img][data-chart-unit]` | gerado |
| Rosca | lista `.ttsc-analytics-category` ao lado do gráfico | gerado |
| Rodapé | `footer.ttsc-analytics-foot` com `.ttsc-analytics-key` (legenda) e `note` | gerado |
| Vazio | `.ttsc-analytics-empty` (`empty` / `emptyDetail`) | gerado |
| Drawer de filtros | `.ttsc-analytics-drawer.drawer-panel#drawer-analytics-<id>` anexado ao `body` | gerado |

## Variantes

| `type` | Quando | Notas |
|---|---|---|
| `bar` | categorias (curso, turma) | `horizontal: true` para rótulos longos; cores por categoria com `backgroundColor` + `40` de alfa |
| `doughnut` | parte do todo (status) | lista de categorias ao lado; cores de `TTSCAnalytics.palette` ou dos tons da ficha |
| `line` | série mensal | `wide: true`; pontos e área do Chart.js |
| forecast | meta × realizado mensal | modelo `{months, target, annualTarget, series}` (comercial) |

## API

**`TTSCAnalytics.create(host, spec)` → `{refresh(), card, drawer, getState()}`** (`assets/js/ttsc.analytics-panels.js`)

| `spec` | Tipo | Descrição |
|---|---|---|
| `id` | string | id do painel; drawer = `drawer-analytics-<id>` |
| `title`, `description`, `icon` | string | cabeçalho (`fa-chart-column` padrão) |
| `wide` | bool | ocupa a largura da grade |
| `fields` | array ou `() => array` | campos do drawer: `{key, label, options:[[valor, rótulo]…]}` (select) ou `{key, label, type:'number', min, max, help}` |
| `defaults` | objeto | estado inicial; "Redefinir" volta a ele |
| `build(state)` | `(state) => Promise<model>` | devolve o modelo do gráfico; rejeição mostra erro e mantém o anterior |

| `model` (retorno de `build`) | Descrição |
|---|---|
| `type` | `bar`, `line`, `doughnut` |
| `labels`, `datasets[]` | dados do Chart.js (`label`, `data`, `backgroundColor`, `borderColor`) |
| `horizontal`, `integer`, `max` | eixo |
| `currency`, `unit` | formatação de tooltip/eixo (`Intl`) |
| `badges[]`, `note`, `legend[{label,color}]`, `summary` | textos e legenda (`summary` vira `data-chart-summary`) |
| `empty`, `emptyDetail` | estado vazio |
| `target` | linha de meta |

Também expostos: `TTSCAnalytics.palette` (`#10b981 #3b82f6 #a855f7 #f59e0b #ef4444 #64748b #06b6d4`), `.money()`, `.number()`, `.escape()`. `ttsc.chart-defaults.js` aplica fonte, cores de grade e tooltip escuro do modelo a todo `Chart`.

**Ficha — `analytics[]`**: `title`, `desc`, `icon`, `by` (campo ou `month` + `date`), `months` (padrão 12), `measure:{agg: count|sum|avg, field, unit: count|money|%}`, `type`, `wide`, `horizontal`, `top` (máx. categorias, padrão 8), `seriesLabel`, `note`.

**PHP** — `chassis/domain_page.php` (VIEW 5) desenha 4 mini-cards (total, criados no ano, no mês, status predominante) e dois `canvas` com Chart.js direto: "Registros criados por mês" (`ScaffoldKpiService::monthlySeries($contract, $tenant, $ano)`) e "Registros por status" (`$kanbanColumns`). As páginas do developer usam `TTSCAnalytics` via `partials/analytics/developer/dashboard-analytics.php` + `assets/js/ttsc.developer-analytics.js`.

**Endpoints**: `GET /api/v1/kpi{rota}` (`statusCounts`, `totalRecords`) e `GET /api/v1/domain/records{rota}?status=` para séries por status; a série mensal é calculada no servidor (SSR) a partir de `created_at`.

## Acessibilidade

- `canvas[role=img]` com `aria-label` = título + instrução; `tabindex="0"` e setas do teclado percorrem os pontos (tooltip por teclado do `ttsc.chart-defaults.js`).
- O total e a legenda estão em texto no rodapé — o gráfico não é a única fonte do número.
- O drawer de filtros é `role=dialog` (via `openDrawer`), com "Aplicar" e "Redefinir"; o botão "Filtros" tem `aria-label` com o título do gráfico.
- Não dependa só da cor entre séries: a legenda nomeia cada uma.

## Modelos

### HTML

1) PHP real — host + script, como em `resources/views/app/partials/analytics/developer/dashboard-analytics.php`:

```php
<link rel="stylesheet" href="<?= asset('css/ttsc.analytics-panels.css') ?>?v=<?= filemtime(base_path('assets/css/ttsc.analytics-panels.css')) ?>">
<script nonce="<?= $nonce ?>" src="<?= asset('js/ttsc.analytics-panels.js') ?>?v=<?= filemtime(base_path('assets/js/ttsc.analytics-panels.js')) ?>"></script>
<div id="view-analytics" class="space-y-5" style="display: none;" role="tabpanel" aria-labelledby="tab-btn-analytics">
  <div id="academic-analytics-panels" class="space-y-5"></div>
</div>
<script type="application/json" id="academic-analytics-data"><?= json_encode([
    'byCourse' => $byCourse, 'byStatus' => $statusCounts, 'monthly' => $monthly, 'labels' => $monthNames,
], JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?></script>
```

2) HTML gerado (preview, 1 painel):

```html
<div id="model-analytics-panels" class="ttsc-analytics-grid">
  <article class="ttsc-analytics-card" data-analytics-id="model-0" data-chart-summary="{}">
    <header class="ttsc-analytics-head">
      <div>
        <h3><i class="fa-light fa-chart-column" aria-hidden="true"></i>Matrículas por curso</h3>
        <p>Situação atual</p>
      </div>
      <button type="button" class="ttsc-analytics-action" aria-label="Filtrar Matrículas por curso" aria-controls="drawer-analytics-model-0">
        <i class="fa-light fa-sliders" aria-hidden="true"></i>Filtros
      </button>
    </header>
    <div class="ttsc-analytics-badges">
      <span class="ttsc-analytics-badge">Situação atual</span>
      <span class="ttsc-analytics-badge">48 Matrículas</span>
    </div>
    <div class="ttsc-analytics-content">
      <div class="ttsc-analytics-plot">
        <canvas role="img" aria-label="Matrículas por curso. Use arrow keys to inspect values." data-chart-unit="matrículas" tabindex="0" data-ttsc-tooltip-keys="ready"></canvas>
      </div>
    </div>
    <footer class="ttsc-analytics-foot">
      <div>
        <span class="ttsc-analytics-key"><i style="background: #3b82f6"></i>Ensino Médio</span>
        <span class="ttsc-analytics-key"><i style="background: #10b981"></i>Fundamental II</span>
        <span class="ttsc-analytics-key"><i style="background: #a855f7"></i>Técnico em Informática</span>
        <span class="ttsc-analytics-key"><i style="background: #f59e0b"></i>Técnico em Enfermagem</span>
      </div>
      <span>Total 48</span>
    </footer>
  </article>
</div>
```

### CSS

`assets/css/ttsc.analytics-panels.css`: `.ttsc-analytics-grid` (2 colunas, `.has-three-columns`), `.ttsc-analytics-card`, `.is-wide`, `-head`, `-badges`, `-plot`, `-foot`, `-key`, `-category`, `-empty`, o drawer e o tooltip escuro compartilhado. Escuro: `html.dark .ttsc-analytics-head, .ttsc-analytics-foot {border-color:#334155}`, badges/vazio/categorias em `#1e293b`, textos `#cbd5e1`/`#f1f5f9`; a superfície do card segue `html.dark .bg-white`/tokens do shell.

```css
/* Extensão por tokens: cartão e badges seguindo o design system */
.ttsc-analytics-card { background: var(--ttsc-surface); border-color: var(--ttsc-border); border-radius: var(--ttsc-radius-surface); }
.ttsc-analytics-badge { background: var(--ttsc-canvas); color: var(--ttsc-text-2); border-color: var(--ttsc-border-soft); }
.ttsc-analytics-action:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
```

### JS

```js
// Três painéis da ficha acadêmica com dados do servidor e filtro por visualização
const data = JSON.parse(document.getElementById('academic-analytics-data').textContent);
const host = document.getElementById('academic-analytics-panels');
host.className = 'ttsc-analytics-grid';

TTSCAnalytics.create(host, {
  id: 'by-course', title: 'Matrículas por curso', description: 'Situação atual', icon: 'fa-chart-column',
  fields: [{ key: 'view', label: 'Visualização', options: [['bar', 'Barras'], ['doughnut', 'Rosca']] }],
  defaults: { view: 'bar' },
  build: async (st) => ({
    type: st.view,
    labels: data.byCourse.map((r) => r.name),
    datasets: [{ label: 'Matrículas', data: data.byCourse.map((r) => r.total) }],
    unit: 'matrículas', integer: true,
    badges: ['Situação atual', data.byCourse.reduce((s, r) => s + r.total, 0) + ' matrículas'],
    empty: data.byCourse.length ? undefined : 'Sem dados para este gráfico',
  }),
});

TTSCAnalytics.create(host, {
  id: 'by-status', title: 'Solicitações por status', description: 'Funil de rematrícula',
  fields: [], defaults: {},
  build: async () => {
    const res = await fetch('/api/v1/kpi/academic/enrollment/re-enrollment', { credentials: 'same-origin' });
    const { statusCounts = {} } = await res.json();
    const labels = Object.keys(statusCounts);
    return { type: 'doughnut', labels, datasets: [{ data: labels.map((k) => statusCounts[k]), backgroundColor: TTSCAnalytics.palette }],
             integer: true, unit: 'solicitações' };
  },
});

TTSCAnalytics.create(host, {
  id: 'monthly', title: 'Novas matrículas por mês', description: 'Pela data da matrícula', wide: true, icon: 'fa-chart-line',
  fields: [{ key: 'view', label: 'Visualização', options: [['line', 'Linha'], ['bar', 'Barras']] }],
  defaults: { view: 'line' },
  build: async (st) => ({ type: st.view, labels: data.labels, datasets: [{ label: 'Matrículas', data: data.monthly, borderColor: '#10b981' }],
                          integer: true, badges: ['Últimos 12 meses'], note: 'Total ' + data.monthly.reduce((a, b) => a + b, 0) }),
});
```

### SQL

```sql
-- Barras: matrículas por curso
SELECT c.name, COUNT(e.id) AS total
  FROM enrollments e
  JOIN courses c ON c.uuid = e.course_uuid
 WHERE e.deleted_at IS NULL
 GROUP BY c.uuid, c.name
 ORDER BY total DESC
 LIMIT 8;

-- Rosca: solicitações por status (statusCounts)
SELECT status, COUNT(*) AS total
  FROM enrollment_requests
 WHERE deleted_at IS NULL
 GROUP BY status;

-- Linha: novas matrículas por mês nos últimos 12 meses (meses sem matrícula = 0 no PHP)
SELECT DATE_FORMAT(e.enrollment_date, '%Y-%m') AS mes, COUNT(*) AS total
  FROM enrollments e
 WHERE e.deleted_at IS NULL
   AND e.enrollment_date >= DATE_FORMAT(CURRENT_DATE - INTERVAL 11 MONTH, '%Y-%m-01')
 GROUP BY mes
 ORDER BY mes;

-- Mensalidade somada por mês de matrícula (measure: sum + unit money)
SELECT DATE_FORMAT(e.enrollment_date, '%Y-%m') AS mes, SUM(abr.monthly_tuition) AS receita
  FROM enrollments e
  JOIN academic_billing_rules abr ON abr.course_uuid = e.course_uuid AND abr.status = 'active'
 WHERE e.deleted_at IS NULL AND YEAR(e.enrollment_date) = :year
 GROUP BY mes
 ORDER BY mes;
```

O PHP completa os 12 meses (`array_fill(0, 12, 0)` + índice do mês) e serializa em `#academic-analytics-data`; cada `build()` só lê esse JSON ou o endpoint de KPI.

## Faça / Não faça

- **Faça:** `build()` assíncrono e idempotente; o painel descarta respostas antigas (sequência interna).
- **Faça:** `empty` quando não há dado — nunca zero inventado ("Medições indisponíveis não são tratadas como zero").
- **Não faça:** carregar Chart.js de CDN em página nova: use o `assets` local (o `domain_page.php` ainda aponta para jsDelivr).
- **Não faça:** mais de 8 categorias numa barra; agrupe em "Outros" (`top`).
