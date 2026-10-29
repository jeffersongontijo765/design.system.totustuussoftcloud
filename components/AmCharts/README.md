# AmCharts

Gráficos amCharts 5.17.2 (colunas e rosca) com cores da escala `ttsc-primary`, rótulos em `ttsc-text-muted`, grade em `ttsc-border` e tooltip invertido, lidos dos tokens em tempo de execução para funcionar nos dois temas.

## Quando usar

- Gráficos de painel com categorias e partes de um todo: matrículas por mês, matrículas por modalidade, inadimplência por unidade.
- Telas que já usam o helper do repo `assets/js/ttsc.charts.js` (`TTSCChart.bar`, `.donut`, `.line`, `.sparkline`), que é uma fábrica sobre amCharts 5.
- Catálogo oficial com 303 demos ao vivo: [amcharts.com/demos](https://www.amcharts.com/demos/) — o mapeamento por categoria está em `## Catálogo oficial de demos` abaixo.
- **Não use** para sparklines dentro de KPIs ou gráficos muito simples em telas leves: use [ApexCharts](../ApexCharts/README.md) (menor e com `theme.mode`).
- **Não use** para tabelas de números exatos: mostre a tabela (e o gráfico como apoio).
- Rosca com no máximo 5 fatias; acima disso, use colunas ordenadas.

## Anatomia

```
┌ figure.ac-card ─────────────────────────┐  ┌ figure.ac-card ──────────────┐
│ Matrículas por mês          (h3)        │  │ Por modalidade                │
│ 2026 · todas as unidades    (p, muted)  │  │      ╭───╮                    │
│ 400┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄  grid        │  │     │1.284│  ← Label central │
│     ▇  █  ▆        ▅ ▆      ColumnSeries│  │      ╰───╯   PieSeries        │
│ jan fev mar …               CategoryAxis│  │ ■ Presencial 62%  ← Legend    │
└─────────────────────────────────────────┘  └───────────────────────────────┘
```

| Parte | Classe / API | Obrigatório |
|---|---|---|
| Card | `figure.ac-card` com título e subtítulo | sim |
| Container | `div[role=img][aria-label="resumo do gráfico"]` com altura fixa | sim |
| Root | `am5.Root.new(id)` + `am5themes_Animated` | sim |
| Cores | `root.interfaceColors` (`text`, `grid`, `background`, `alternativeBackground`) | sim |
| Série | `am5xy.ColumnSeries` / `am5percent.PieSeries` | sim |
| Legenda | `am5.Legend` (rosca) | recomendado |

## Variantes

| Variante | Configuração | Tokens |
|---|---|---|
| Colunas | `XYChart` + `CategoryAxis` + `ValueAxis` + `ColumnSeries`, cantos 4px | claro `ttsc-primary-500`; escuro `ttsc-primary-400` |
| Destaque | adapter `fill` na coluna de pico | claro `ttsc-primary-700`; escuro `ttsc-primary-200` |
| Rosca | `PieChart` `innerRadius: 62%`, rótulos ocultos, legenda | claro `500/800/200`; escuro `400/200/700` |
| Rótulos | eixos e valores | `ttsc-text-muted` |
| Grade | tracejada `[3,3]` | `ttsc-border` |
| Tooltip | fundo `ttsc-text`, texto `ttsc-surface` | inverso, contraste alto nos dois temas |

## API

| Item | Uso |
|---|---|
| `am5.Root.new(el)` | Um root por gráfico; `root.dispose()` antes de recriar |
| `root.setThemes([am5themes_Animated.new(root)])` | Animação de entrada (respeite `prefers-reduced-motion`: omita o tema) |
| `root.locale` / `root.numberFormatter.set('numberFormat', '#,###')` | Separadores pt-BR (`.` milhar, `,` decimal) |
| `root.interfaceColors.set(nome, am5.color(hex))` | Ponte de tokens (amCharts não lê variáveis CSS: resolva com `getComputedStyle`) |
| `am5xy.XYChart.new(root, { panX:false, panY:false, wheelX:'none', wheelY:'none' })` | Painel estático |
| `am5xy.CategoryAxis` / `ValueAxis` / `AxisRendererX/Y` | `renderer.labels.template.setAll({ fill, fontSize })` |
| `am5xy.ColumnSeries.new(root, { valueYField, categoryXField, tooltip })` | `series.columns.template.setAll({...})`, `adapters.add('fill', fn)` |
| `am5percent.PieChart` / `PieSeries` | `series.get('colors').set('colors', [...])`, `slices.template` |
| `am5.Legend.new(root, {...})` | `legend.data.setAll(series.dataItems)` |
| `series.data.setAll(rows)` | Atualiza os dados (sem recriar) |
| `series.appear(ms)` / `chart.appear(ms, delay)` | Entrada |
| Eventos | `series.columns.template.events.on('click', e => e.target.dataItem.dataContext)` |

## Acessibilidade

- O canvas não é lido por leitores de tela: o container tem `role="img"` e `aria-label` com o resumo (“pico de 312 em fevereiro”), e o dado detalhado fica disponível em tabela/exportação.
- Nunca dependa só da cor: valores sobre as colunas e legenda com percentuais.
- Tons da escala escolhidos para separar fatias vizinhas (500/800/200); no escuro a ordem muda para manter contraste com `ttsc-surface`.
- Animação curta (600 ms); com `prefers-reduced-motion: reduce`, não aplique o tema Animated.

## Modelos

### HTML

```html
<figure class="ac-card">
  <h3>Matrículas por mês</h3>
  <p><?= (int) $year ?> · <?= $this->e($unitName ?? 'todas as unidades') ?></p>
  <div class="ac-chart" id="chart-enrollments" role="img"
       aria-label="<?= $this->e($chartSummary) ?>"
       data-rows='<?= json_encode($byMonth, JSON_HEX_APOS | JSON_HEX_TAG) ?>'></div>
</figure>
<script src="<?= asset('vendors/amcharts5/index.js') ?>"></script>
<script src="<?= asset('vendors/amcharts5/xy.js') ?>"></script>
<script src="<?= asset('vendors/amcharts5/percent.js') ?>"></script>
<script src="<?= asset('vendors/amcharts5/themes/Animated.js') ?>"></script>
```

### CSS

```css
.ac-card { margin: 0; min-width: 0; padding: 14px 16px 8px; border: 1px solid var(--ttsc-border);
  border-radius: var(--ttsc-radius-surface); background: var(--ttsc-surface); box-shadow: var(--ttsc-shadow-sm); }
.ac-card h3 { margin: 0; font-size: 14px; font-weight: 600; color: var(--ttsc-text); }
.ac-card p { margin: 2px 0 0; font-size: 12px; color: var(--ttsc-text-muted); }
.ac-chart { height: 260px; }
.ac-card:hover { border-color: var(--ttsc-border-strong); }
```

### JS

```js
// assets/js/core/ttsc.amcharts-theme.js — ponte de tokens para amCharts 5
const tok = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const col = (n) => am5.color(tok(n));
const isDark = () => document.documentElement.dataset.theme === 'dark' || document.documentElement.classList.contains('dark');
const MONTHS = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];

export function ttscRoot(id) {
  const root = am5.Root.new(id);
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) root.setThemes([am5themes_Animated.new(root)]);
  root.locale = { _decimalSeparator: ',', _thousandSeparator: '.' };
  root.numberFormatter.set('numberFormat', '#,###');
  root.interfaceColors.set('text', col('--ttsc-text-muted'));
  root.interfaceColors.set('grid', col('--ttsc-border'));
  root.interfaceColors.set('background', col('--ttsc-surface'));
  root.interfaceColors.set('alternativeBackground', col('--ttsc-text'));
  root.interfaceColors.set('alternativeText', col('--ttsc-surface'));
  return root;
}

export function enrollmentsByMonth(el) {
  const rows = JSON.parse(el.dataset.rows).map((r) => ({ month: MONTHS[r.month_num - 1], total: +r.total }));
  const root = ttscRoot(el.id);
  const chart = root.container.children.push(am5xy.XYChart.new(root, { panX: false, panY: false, wheelX: 'none', wheelY: 'none', paddingLeft: 0 }));
  const xr = am5xy.AxisRendererX.new(root, { minGridDistance: 20, cellStartLocation: 0.15, cellEndLocation: 0.85 });
  xr.labels.template.setAll({ fill: col('--ttsc-text-muted'), fontSize: 11 });
  xr.grid.template.set('visible', false);
  const x = chart.xAxes.push(am5xy.CategoryAxis.new(root, { categoryField: 'month', renderer: xr }));
  const yr = am5xy.AxisRendererY.new(root, {});
  yr.labels.template.setAll({ fill: col('--ttsc-text-muted'), fontSize: 11 });
  yr.grid.template.setAll({ stroke: col('--ttsc-border'), strokeOpacity: 1, strokeDasharray: [3, 3] });
  const y = chart.yAxes.push(am5xy.ValueAxis.new(root, { min: 0, maxPrecision: 0, renderer: yr }));
  const s = chart.series.push(am5xy.ColumnSeries.new(root, {
    xAxis: x, yAxis: y, valueYField: 'total', categoryXField: 'month',
    tooltip: am5.Tooltip.new(root, { labelText: '{categoryX}: {valueY} matrículas' }),
  }));
  s.columns.template.setAll({ cornerRadiusTL: 4, cornerRadiusTR: 4, strokeOpacity: 0,
    fill: col(isDark() ? '--ttsc-primary-400' : '--ttsc-primary-500') });
  const peak = Math.max(...rows.map((r) => r.total));
  s.columns.template.adapters.add('fill', (fill, t) =>
    t.dataItem?.dataContext.total === peak ? col(isDark() ? '--ttsc-primary-200' : '--ttsc-primary-700') : fill);
  x.data.setAll(rows);
  s.data.setAll(rows);
  s.appear(600);
  return root;
}

export function enrollmentsByModality(el, labels) {   // labels: { in_person: 'Presencial', … } do lang/
  const rows = JSON.parse(el.dataset.rows).map((r) => ({ modality: labels[r.modality] || r.modality, total: +r.total }));
  const root = ttscRoot(el.id);
  const chart = root.container.children.push(am5percent.PieChart.new(root, { innerRadius: am5.percent(62), layout: root.verticalLayout }));
  const s = chart.series.push(am5percent.PieSeries.new(root, { valueField: 'total', categoryField: 'modality' }));
  s.get('colors').set('colors', (isDark()
    ? ['--ttsc-primary-400', '--ttsc-primary-200', '--ttsc-primary-700']
    : ['--ttsc-primary-500', '--ttsc-primary-800', '--ttsc-primary-200']).map(col));
  s.slices.template.setAll({ stroke: col('--ttsc-surface'), strokeWidth: 2, cornerRadius: 4 });
  s.labels.template.set('forceHidden', true);
  s.ticks.template.set('forceHidden', true);
  const legend = chart.children.push(am5.Legend.new(root, { centerX: am5.p50, x: am5.p50 }));
  legend.labels.template.setAll({ fill: col('--ttsc-text-2'), fontSize: 12 });
  s.data.setAll(rows);
  legend.data.setAll(s.dataItems);
  return root;
}

// Troca de tema: as cores foram resolvidas na criação — descarte e recrie
const roots = [];
document.querySelectorAll('[data-chart="enrollments-month"]').forEach((el) => roots.push([el, enrollmentsByMonth]));
new MutationObserver(() => {
  am5.registry.rootElements.forEach((r) => r.dispose());
  roots.forEach(([el, fn]) => fn(el));
}).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
```

### SQL

```sql
-- Matrículas por mês do ano (índice em enrollment_date ajuda; use faixa, não YEAR()). MariaDB 10.11 / MySQL 8
SELECT DATE_FORMAT(e.enrollment_date, '%Y-%m') AS month_key,
       MONTH(e.enrollment_date)               AS month_num,
       COUNT(*)                                AS total
  FROM enrollments e
 WHERE e.deleted_at IS NULL
   AND e.enrollment_date >= :year_start          -- '2026-01-01'
   AND e.enrollment_date <  :year_end            -- '2027-01-01'
   AND (:unit_uuid = '' OR e.unit_uuid = :unit_uuid_again)
 GROUP BY DATE_FORMAT(e.enrollment_date, '%Y-%m'), MONTH(e.enrollment_date)
 ORDER BY month_key;

-- Matrículas ativas por modalidade, com percentual (função de janela: MariaDB 10.2+ / MySQL 8)
SELECT e.modality,
       COUNT(*)                                            AS total,
       ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)    AS pct
  FROM enrollments e
 WHERE e.deleted_at IS NULL
   AND e.status = 'active'
 GROUP BY e.modality
 ORDER BY total DESC;
```

O PHP completa os meses sem matrícula com `total = 0` (12 linhas), traduz `modality` (`in_person` → “Presencial”) pelo `lang/pt_BR`, gera o `aria-label` com total e pico e imprime as linhas em `data-rows`.

## Faça / Não faça

- **Faça:** resolver tokens com `getComputedStyle` e recriar o gráfico ao trocar o tema.
- **Faça:** usar a escala `ttsc-primary` (fundos tonais e gráficos) e `ttsc-text-muted` nos rótulos.
- **Faça:** `role="img"` + resumo textual; tabela ao lado quando o número exato importa.
- **Não faça:** cores hexadecimais fixas (como o `PALETTE` atual de `ttsc.charts.js`, com `text: 0x111827` invisível no escuro) — migre para a ponte de tokens.
- **Não faça:** remover o logotipo do amCharts sem licença comercial; nem rosca com mais de 5 fatias.

## Catálogo oficial de demos

O site da amCharts mantém o [catálogo oficial de demos](https://www.amcharts.com/demos/) — **303 demos ao vivo** de amCharts 5, distribuídos em 11 categorias. Onde cada categoria vive no nosso Design System:

| Categoria oficial (nº de demos) | Onde no nosso DS |
|---|---|
| Column & Bar (45) | [AmCharts](../AmCharts/README.md) clássico (colunas) · [ChartKit](../ChartKit/README.md) 1–6 |
| Line & Area (51) | helper `assets/js/ttsc.charts.js` (`TTSCChart.line`) · ChartKit 10–16 |
| Pie & Donut (17) | AmCharts clássico (rosca) · ChartKit 18–19 |
| XY & Bubble (14) | ChartKit 21 (scatter) · ChartKit 22 (bubble) |
| Maps (48) | [GeoMap](../GeoMap/README.md) — SVG próprio, não usa a lib |
| Candlestick & OHLC (6) | [ApexChartsAdvanced](../ApexChartsAdvanced/README.md) (candlestick) · ChartKit 36 (OHLC + volume) |
| Stock (10) | módulo não vendorizado — para painéis use o OHLC do ChartKit 36 e widgets de séries |
| Gantt (6) | componente [Gantt](../Gantt/README.md) do DS — o módulo `gantt.js` não está no bundle |
| Gauges (11) | ChartKit 23 (gauge radial), 24 (semi-gauge), 25 (anéis) |
| Radar & Polar (18) | ApexChartsAdvanced (radar) · ChartKit 28 (polar area) |
| Hierarchy (20) | ChartKit 20 (treemap) · ChartKit 37 (sunburst em SVG puro) |

Nota de vendor: o bundle traz apenas `index.js` (core), `percent.js` e `xy.js` — `gantt`, `map`, `hierarchy`, `stock` e `flow` **não estão incluídos**. Para esses casos use os componentes do DS indicados na tabela, que não carregam módulos extras; incluir módulos novos no `vendors/amcharts5/` é decisão de build, igual à reinstalação do ApexCharts íntegro (ver nota no [ApexCharts](../ApexCharts/README.md)).
