# ApexCharts

Gráficos ApexCharts 8.5.0 — área (frequência %), barras, donut e sparkline de KPI — com `theme.mode` conforme o `data-theme`, cores resolvidas dos tokens e locale pt-BR.

> **Nota de manutenção (resolvida em 27/10/2026):** a troca global `kt` → `ttsc` sem diferenciar maiúsculas corrompia a cópia de `assets/vendors/apexcharts` (ex.: `checkForDarkTheme` → `checkForDarttscheme`, `stackType` → `stacttscype`), gerando “Identifier 'ttsc' has already been declared” — o script não fazia parse. **Resolvido** com a instalação limpa da 8.5.0 em `assets/vendors/apexcharts/` e no vendor do DS (`vendor/apexcharts/apexcharts.min.js`). Mantenha `vendors/` fora do renomeador para não reintroduzir o bug.

## Quando usar

- Painéis acadêmicos com séries temporais e comparações: frequência média semanal, presença por turma, distribuição de registros de chamada.
- Sparklines dentro de cards de KPI (leve, sem eixos).
- Para candlestick, radar, treemap, waterfall (ponte), gauge radial, barras empilhadas/agrupadas e linha com faixa de previsão, use a galeria [ApexChartsAdvanced](../ApexChartsAdvanced/README.md).
- Para o catálogo completo de gráficos de gestão (com/sem grade e legenda, metas, eixo duplo, dumbbell, step line, multi-donut, semi-gauge e tooltip personalizado), use [ChartKit](../ChartKit/README.md).
- Catálogo oficial de demos com código ao vivo: [apexcharts.com/javascript-chart-demos](https://apexcharts.com/javascript-chart-demos/) — o mapeamento demo por demo está em `## Catálogo oficial de demos` abaixo.
- **Não use** quando a tela já usa amCharts (`assets/js/ttsc.charts.js`): fique com [AmCharts](../AmCharts/README.md) para não carregar duas bibliotecas.
- **Não use** gráfico para 1–2 números: use [KpiCard](../KpiCard/README.md) sem gráfico.
- Para fluxo entre etapas (Sankey), veja [SankeyFlow](../SankeyFlow/README.md); para mapa geográfico, [GeoMap](../GeoMap/README.md).

## Anatomia

```
┌ figure.ax-card ──────────────────────────────┐ ┌ .ax-card.ax-kpi ──────────┐
│ Frequência média por semana   (h3)           │ │ FREQUÊNCIA MÉDIA  (lbl)    │
│ 2º semestre · meta 75%        (p)            │ │ 88,4%             (val)    │
│ 100%┄┄┄┄┄┄┄╭──╮┄┄┄┄┄┄┄┄┄┄┄  área + gradiente  │ │ ↗ +2,1 p.p.       (delta)  │
│  ─ ─ ─ Meta 75% ─ ─ ─ ─ ─   annotations.yaxis │ │ ∿∿∿∿∿  sparkline           │
│ S1 S2 …                                       │ └───────────────────────────┘
└───────────────────────────────────────────────┘
```

| Parte | Classe / opção | Obrigatório |
|---|---|---|
| Card | `figure.ax-card` (título, subtítulo) | sim |
| Container | `div[role=img][aria-label]` | sim |
| Tema | `theme.mode`, `tooltip.theme`, `chart.background: 'transparent'`, `chart.foreColor` | sim |
| Grade | `grid.borderColor`, `strokeDashArray: 3` | sim |
| Meta | `annotations.yaxis[{ y: 75 }]` | quando houver meta |
| KPI | `.ax-kpi` + `chart.sparkline.enabled` | não |

## Variantes

| Tipo | Opções principais | Tokens |
|---|---|---|
| Área (frequência %) | `type: 'area'`, `stroke.curve: 'smooth'`, `fill.gradient` 0.35→0.02, `yaxis.min: 60`, anotação da meta | linha `ttsc-accent`, meta `ttsc-warning` |
| Barras horizontais | `plotOptions.bar.horizontal`, `distributed: true`, `borderRadius: 4`, rótulos de dados | ≥ 85% `ttsc-accent` (escuro `ttsc-primary-400`), 75–84% `ttsc-warning`, < 75% `ttsc-danger`; texto `ttsc-accent-on` |
| Donut | `donut.size: '66%'`, `labels.total` | presente `ttsc-accent`, ausente `ttsc-danger`, justificado `ttsc-warning`; borda `ttsc-surface` |
| Sparkline | `sparkline.enabled`, `height: 48`, `tooltip.enabled: false` | positivo `ttsc-accent`, negativo `ttsc-danger` |
| Textos | `chart.foreColor`, `labels.style.colors` | `ttsc-text-muted` (eixos), `ttsc-text-2` (categorias, legenda) |

## API

| Item | Uso |
|---|---|
| `new ApexCharts(el, options).render()` | Cria (retorna Promise) |
| `chart.updateOptions(opts, redraw?, animate?)` | Troca tema/cores sem recriar |
| `chart.updateSeries(series, animate?)` | Atualiza dados (filtros de unidade/período) |
| `chart.appendData(data)` | Acrescenta pontos |
| `chart.toggleSeries(name)`, `chart.dataURI()`, `chart.destroy()` | |
| `chart.defaultLocale` + `chart.locales` | Meses/dias em pt-BR (ver JS) |
| `theme.mode` | `'light'` / `'dark'` (escolhe paleta de eixos e tooltip padrão) |
| `chart.events` | `dataPointSelection(e, ctx, { dataPointIndex })`, `mounted`, `updated`, `legendClick` |
| Formatadores | `yaxis.labels.formatter`, `tooltip.y.formatter`, `dataLabels.formatter` com `toLocaleString('pt-BR')` |

## Acessibilidade

- SVG sem semântica útil: o container tem `role="img"` e `aria-label` com o resumo (“entre 81% e 93%, acima da meta de 75%”); a tabela de dados fica acessível na tela ou na exportação.
- Estados não dependem só da cor: barras têm rótulo de valor, KPI tem seta e texto (“+2,1 p.p.”), meta tem rótulo.
- Rótulo de dados em `ttsc-accent-on` (#0f0f0f) sobre as barras; tooltip com `ttsc-text` sobre `ttsc-surface` nos dois temas.
- `chart.animations.speed` curto; desligue (`enabled: false`) com `prefers-reduced-motion`.

## Modelos

### HTML

```html
<figure class="ax-card">
  <h3>Frequência média por semana</h3>
  <p><?= $this->e($periodLabel) ?> · meta <?= (int) $minAttendance ?>%</p>
  <div id="chart-attendance" role="img" aria-label="<?= $this->e($attendanceSummary) ?>"
       data-weeks='<?= json_encode($weeks, JSON_HEX_APOS | JSON_HEX_TAG) ?>'
       data-goal="<?= (int) $minAttendance ?>"></div>
</figure>

<figure class="ax-card ax-kpi">
  <span class="lbl">Frequência média</span>
  <span class="val"><?= number_format($avg, 1, ',', '.') ?>%</span>
  <span class="delta"><i class="fa-light fa-arrow-trend-up"></i> +<?= number_format($delta, 1, ',', '.') ?> p.p. vs. semestre anterior</span>
  <div data-ttsc-spark='<?= json_encode(array_column($weeks, 'attendance_pct')) ?>' role="img" aria-label="Tendência das últimas 12 semanas"></div>
</figure>
<link rel="stylesheet" href="<?= asset('vendors/apexcharts/apexcharts.css') ?>">
<script src="<?= asset('vendors/apexcharts/apexcharts.min.js') ?>"></script>
```

### CSS

```css
.ax-card { margin: 0; min-width: 0; padding: 14px 16px 6px; border: 1px solid var(--ttsc-border);
  border-radius: var(--ttsc-radius-surface); background: var(--ttsc-surface); box-shadow: var(--ttsc-shadow-sm); }
.ax-card h3 { margin: 0; font-size: 14px; font-weight: 600; color: var(--ttsc-text); }
.ax-card p { margin: 2px 0 0; font-size: 12px; color: var(--ttsc-text-muted); }
.ax-kpi .lbl { font-size: 11px; font-weight: 500; letter-spacing: .04em; text-transform: uppercase; color: var(--ttsc-text-muted); }
.ax-kpi .val { font-size: 24px; font-weight: 700; color: var(--ttsc-text); font-variant-numeric: tabular-nums; }
.ax-kpi .delta { font-size: 12px; color: var(--ttsc-accent-text); }
.ax-kpi .delta.down { color: var(--ttsc-danger-text); }
/* Tooltip do Apex (HTML) nos tokens, nos dois temas */
.apexcharts-tooltip.apexcharts-theme-light, .apexcharts-tooltip.apexcharts-theme-dark {
  background: var(--ttsc-surface) !important; color: var(--ttsc-text) !important;
  border: 1px solid var(--ttsc-border) !important; box-shadow: var(--ttsc-shadow-popover) !important; border-radius: var(--ttsc-radius-sm);
}
.apexcharts-tooltip .apexcharts-tooltip-title { background: var(--ttsc-canvas-2) !important; border-bottom: 1px solid var(--ttsc-border) !important; color: var(--ttsc-text-2); }
.apexcharts-xaxistooltip { background: var(--ttsc-surface); border-color: var(--ttsc-border); color: var(--ttsc-text); }
.apexcharts-legend-text { color: var(--ttsc-text-2) !important; }
```

### JS

```js
// assets/js/core/ttsc.apexcharts.js — requer apexcharts 8.5.0 íntegro
const tok = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const isDark = () => document.documentElement.dataset.theme === 'dark' || document.documentElement.classList.contains('dark');
const pct = (v) => `${Number(v).toLocaleString('pt-BR', { maximumFractionDigits: 1 })}%`;
const PT_BR = {
  name: 'pt-br',
  options: {
    months: ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'],
    shortMonths: ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'],
    days: ['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'],
    shortDays: ['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sáb'],
    toolbar: { download: 'Baixar SVG', selection: 'Selecionar', selectionZoom: 'Zoom', zoomIn: 'Ampliar', zoomOut: 'Reduzir', pan: 'Mover', reset: 'Restaurar' },
  },
};

function baseOptions() {
  const dark = isDark();
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  return {
    chart: { fontFamily: 'Inter, system-ui, sans-serif', foreColor: tok('--ttsc-text-muted'), background: 'transparent',
             toolbar: { show: false }, zoom: { enabled: false }, animations: { enabled: !reduce, speed: 400 },
             locales: [PT_BR], defaultLocale: 'pt-br' },
    theme: { mode: dark ? 'dark' : 'light' },
    tooltip: { theme: dark ? 'dark' : 'light' },
    grid: { borderColor: tok('--ttsc-border'), strokeDashArray: 3 },
    dataLabels: { enabled: false },
    legend: { labels: { colors: tok('--ttsc-text-2') } },
  };
}

export function attendanceArea(el) {
  const weeks = JSON.parse(el.dataset.weeks);           // [{iso_week, week_start, attendance_pct}]
  const goal = Number(el.dataset.goal || 75);
  const base = baseOptions();
  const chart = new ApexCharts(el, {
    ...base,
    chart: { ...base.chart, type: 'area', height: 220 },
    series: [{ name: 'Frequência', data: weeks.map((w) => Number(w.attendance_pct)) }],
    colors: [tok('--ttsc-accent')],
    stroke: { curve: 'smooth', width: 2 },
    fill: { type: 'gradient', gradient: { opacityFrom: 0.35, opacityTo: 0.02 } },
    xaxis: { categories: weeks.map((w) => new Date(`${w.week_start}T00:00`).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })) },
    yaxis: { min: 50, max: 100, tickAmount: 5, labels: { formatter: (v) => `${v}%` } },
    annotations: { yaxis: [{ y: goal, borderColor: tok('--ttsc-warning'), strokeDashArray: 4,
      label: { text: `Meta ${goal}%`, style: { background: tok('--ttsc-surface'), color: tok('--ttsc-text-2') }, borderColor: tok('--ttsc-warning') } }] },
    tooltip: { ...base.tooltip, y: { formatter: pct } },
  });
  chart.render();
  return chart;
}

export function sparkline(el) {
  const data = JSON.parse(el.dataset.ttscSpark);
  const color = el.closest('.ax-kpi').querySelector('.delta.down') ? tok('--ttsc-danger') : tok('--ttsc-accent');
  const chart = new ApexCharts(el, {
    chart: { type: 'area', height: 48, background: 'transparent', sparkline: { enabled: true } },
    theme: { mode: isDark() ? 'dark' : 'light' },
    series: [{ name: 'Valor', data }], colors: [color], stroke: { curve: 'smooth', width: 2 },
    fill: { type: 'gradient', gradient: { opacityFrom: 0.3, opacityTo: 0 } }, tooltip: { enabled: false },
  });
  chart.render();
  return chart;
}

// Troca de tema: cores e mode são valores resolvidos — atualize sem recriar
const charts = [];
document.querySelectorAll('#chart-attendance').forEach((el) => charts.push(attendanceArea(el)));
document.querySelectorAll('[data-ttsc-spark]').forEach((el) => charts.push(sparkline(el)));
new MutationObserver(() => {
  const b = baseOptions();
  charts.forEach((c) => c.updateOptions({ theme: b.theme, tooltip: b.tooltip, grid: b.grid,
    chart: { foreColor: b.chart.foreColor } }, false, false));
}).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
```

### SQL

```sql
-- Frequência média por semana ISO (attendance.status: present / absent / …). MariaDB 10.11 / MySQL 8
SELECT YEARWEEK(a.lesson_date, 3) AS iso_week,
       MIN(a.lesson_date)          AS week_start,
       ROUND(100 * SUM(a.status IN ('present', 'late', 'justified')) / COUNT(*), 1) AS attendance_pct,
       SUM(a.status = 'absent')    AS absences,
       COUNT(*)                    AS records
  FROM attendance a
  JOIN enrollments e ON e.uuid = a.enrollment_uuid AND e.deleted_at IS NULL
 WHERE a.lesson_date >= :period_start
   AND a.lesson_date <  :period_end
   AND (:unit_uuid = '' OR e.unit_uuid = :unit_uuid_again)
 GROUP BY YEARWEEK(a.lesson_date, 3)
 ORDER BY iso_week;

-- Barras: presença por turma na semana
SELECT c.uuid, c.code, COALESCE(c.name, c.code) AS class_name,
       ROUND(100 * SUM(a.status IN ('present', 'late', 'justified')) / COUNT(*), 1) AS attendance_pct
  FROM attendance a
  JOIN classes c ON c.uuid = a.class_uuid AND c.deleted_at IS NULL
 WHERE a.lesson_date >= :week_start AND a.lesson_date < :week_end
 GROUP BY c.uuid, c.code, c.name
 ORDER BY attendance_pct DESC;

-- Donut: registros de chamada dos últimos 30 dias por status
SELECT a.status, COUNT(*) AS total
  FROM attendance a
 WHERE a.lesson_date >= CURDATE() - INTERVAL 30 DAY
 GROUP BY a.status;
```

O PHP passa as semanas em `data-weeks` (e os últimos 12 `attendance_pct` em `data-ttsc-spark`), a meta (`75`, frequência mínima legal) em `data-goal`, traduz `status` pelo `lang/pt_BR` para os rótulos do donut e monta o `aria-label` com mínimo, máximo e meta. Quais status contam como presença (`late`, `justified`) é regra da instituição — mantenha a lista num só lugar no repositório do módulo.

## Faça / Não faça

- **Faça:** `theme.mode` + `chart.background: 'transparent'` e cores lidas dos tokens; `updateOptions` ao trocar o tema.
- **Faça:** formatadores pt-BR (`88,4%`, `2.098`) e locale `pt-br` para datas.
- **Faça:** reinstalar o ApexCharts original no repo (a cópia atual não faz parse).
- **Não faça:** deixar o fundo padrão do modo escuro do Apex (cinza) dentro de cards `ttsc-surface`.
- **Não faça:** usar verde/vermelho como único indicador nas barras; mantenha rótulos de valor.

## Catálogo oficial de demos

O site do ApexCharts mantém o [catálogo oficial de demos com código ao vivo](https://apexcharts.com/javascript-chart-demos/) — Line, Area, Column, Bar, Mixed, Range Area, Streamgraphs, Waterfall, Dumbbell, Timeline, Funnel, Candlestick, Boxplots, Violin, Raincloud, Histogram, Bubble, Scatter, Heatmap, Treemap, Sunburst, Icicle, Unit charts, Beeswarm, Waffle, Slope, Pie & Donut, RadialBar/Gauge, Radar, Polar area e Sparklines. Onde cada família vive no nosso Design System, e o que a versão que vendorizamos realmente suporta:

| Demo oficial | Onde no nosso DS | Na versão 8.5.0 vendorizada |
|---|---|---|
| Line | [ChartKit](../ChartKit/README.md) 10–16 | nativo |
| Area | [ApexCharts](../ApexCharts/README.md) clássico (área) · ChartKit 11–12 | nativo |
| Column | ChartKit 1–6 | nativo |
| Bar (horizontal) | ChartKit 2 · [RankedBars](../RankedBars/README.md) | nativo |
| Mixed / Combo | ChartKit 16 (coluna + linha), 30 (pareto), 36 (velas + volume) | nativo |
| Range Area | [ApexChartsAdvanced](../ApexChartsAdvanced/README.md) (linha com faixa de previsão) | nativo |
| Streamgraphs | ChartKit 35 | nativo — tipo `streamgraph` na 8.5.0; o kit usa área empilhada com `stackType: '100%'` |
| Waterfall | ApexChartsAdvanced (ponte em barras empilhadas) | **nativo na 8.5.0** (tipo `waterfall`); a ponte em barras empilhadas segue válida — migração opcional |
| Dumbbell | ChartKit 8 | **nativo na 8.5.0** (tipo `dumbbell`); o rangeBar + marcadores do kit segue válido |
| Timeline / Range Bar | ChartKit 7 · [Gantt](../Gantt/README.md) | nativo |
| Funnel | ChartKit 33 (SVG puro) · [FunnelBars](../FunnelBars/README.md) | **nativo na 8.5.0** (tipo `funnel`); o SVG do kit e o FunnelBars seguem válidos — migração opcional |
| Candlestick | ApexChartsAdvanced · ChartKit 36 (com volume) | nativo |
| Boxplots | ChartKit 26 | nativo |
| Histogram | ChartKit 27 | **nativo na 8.5.0** (tipo `histogram`); a barra em bins de 1 ponto do kit segue válida |
| Bubble | ChartKit 22 | nativo |
| Scatter | ChartKit 21 | nativo |
| Heatmap | ChartKit 41 (calendar heatmap) · [HeatmapMatrix](../HeatmapMatrix/README.md) | nativo |
| Treemap | ChartKit 20 · ApexChartsAdvanced | nativo |
| Sunburst | ChartKit 37 (SVG custom) | **nativo na 8.5.0**; o SVG do kit segue válido (navegável por teclado) |
| Icicle · Unit charts · Beeswarm · Violin · Raincloud | — | **icicle, unit, violin e raincloud nativos na 8.5.0** (scan do bundle); beeswarm não aparece no bundle instalado |
| Waffle | ChartKit 38 (SVG custom) | **nativo na 8.5.0** (tipo `waffle`, sobre `unit`); o SVG do kit segue válido |
| Slope | ChartKit 31 | implementado (2 categorias + rótulos nas pontas); a 8.5.0 também tem `plotOptions.line.isSlopeChart` |
| Pie & Donut | ApexCharts clássico (donut) · ChartKit 18–19 | nativo |
| RadialBar / Gauge | ApexChartsAdvanced (gauge radial) · ChartKit 23–25 | nativo |
| Radar | ApexChartsAdvanced | nativo |
| Polar area | ChartKit 28 | nativo |
| Sparklines | ApexCharts clássico (KPI) · ChartKit 17 | nativo |

Os recursos recentes do site estão no bundle instalado: **trellis** (scan: 161 ocorrências), **crossfilter** e **highlight-filter** presentes, carregados sob demanda; a “Marks API” (bullet/lollipop) não aparece pelo nome no bundle — para bullet/lollipop use `annotations` (presentes). Nota honesta: os demos oficiais mostram a versão atual do site; o bundle vendorizado agora é **8.5.0** (instalação limpa de 27/10/2026) e os status acima vêm do scan do arquivo instalado — os modelos em SVG puro do [ChartKit](../ChartKit/README.md) (33, 34, 37, 38) seguem válidos por serem determinísticos, navegáveis e independentes da lib; migrar para o tipo nativo é opcional.
