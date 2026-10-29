# ApexChartsAdvanced

Galeria de sete gráficos ApexCharts 8.5.0 — candlestick, radar, treemap, waterfall, gauge radial, barras empilhadas/agrupadas e linha com faixa de previsão — com cores dos tokens, locale pt-BR e troca de tema sem recarregar.

## Quando usar

- Painéis que precisam de tipos que o [ApexCharts](../ApexCharts/README.md) básico não cobre: candlestick OHLC, radar de maturidade, treemap de composição, waterfall de saldo, gauge radial e previsão com intervalo.
- Uma grade de 12 colunas com cards de larguras diferentes (7/5, 5/7, 4/8, 12), mantendo todos os gráficos no mesmo tema.
- Comparações em que o valor também precisa aparecer em texto: rótulos de dados, legenda e tabela alternativa.
- Para o catálogo completo de gráficos de gestão (grade/legenda opcionais, metas, eixo duplo, dumbbell, step line, multi-donut, semi-gauge, tooltip personalizado), veja [ChartKit](../ChartKit/README.md).

Não use quando:

- O painel só tem linha, área, barra simples ou donut: use [ApexCharts](../ApexCharts/README.md), menor e sem os casos especiais desta galeria.
- O assunto é fluxo entre etapas (origem → desfecho): use [SankeyFlow](../SankeyFlow/README.md); o ApexCharts 8.5.0 não tem sankey nativo.
- O dado é uma sequência de etapas que só diminui: [FunnelBars](../FunnelBars/README.md) comunica melhor que um gráfico de barras.
- O usuário precisa de datas por tarefa ou dependências: use [Gantt](../Gantt/README.md).
- A tela não carrega ApexCharts: prefira [HeatmapMatrix](../HeatmapMatrix/README.md), [Bullets](../Bullets/README.md) ou [Progress](../Progress/README.md) em CSS/SVG.

## Anatomia

```
┌ figure.ax-card.s7 ───────────────────────────────┐
│ Candlestick · BTC/USDT                  [pill]   │  h2 + pill de resumo
│ 30 dias até 23/10/2026 · preços em US$            │  p de contexto
│ ┌ div[role=img][aria-label] ───────────────────┐ │
│ │  eixos · grade · série · legenda            │ │  SVG do Apex
│ └──────────────────────────────────────────────┘ │
│ nota ou <details> com tabela de dados            │
└──────────────────────────────────────────────────┘
```

| Parte | Classe / opção | Obrigatório | Função |
|---|---|---|---|
| Grade | `.axg` | sim | 12 colunas, `max-width: 1280px`, `minmax(0, 1fr)` |
| Card | `figure.ax-card` + `.s7/.s5/.s4/.s8/.s12` | sim | Moldura, título, subtítulo e largura na grade |
| Título | `.ax-hd h2` | sim | Title Case, uma linha |
| Contexto | `.ax-hd p` | sim | Período, unidade e recorte |
| Resumo | `.ax-pill` | recomendado | Número-âncora em texto, não só cor |
| Container | `div[role="img"][aria-label]` | sim | O SVG do Apex não tem semântica própria |
| Gráfico | `new ApexCharts(el, options)` | sim | Tipo, séries, eixos, tooltip e tema |
| Alternativa | `<details class="ax-details">` + `.ax-table` | recomendado | Tabela com os mesmos dados para teclado/leitor |
| Nota | `.ax-note` | não | Origem, Ressalva ou dado ilustrativo |

### Escala e alturas

As alturas dos containers são fixas por gráfico (196–268 px) e o card cresce com o conteúdo; a grade não usa `height: 100%` para não achatar o SVG. Em `< 1024px`, todos os cards passam a `span 12`; em `< 560px`, o padding cai para 12 px e os títulos para 13 px. O preview completo mede 1.525 px em 1.280 px de largura.

## Variantes

| Variante | Classe / opção | Uso |
|---|---|---|
| Candlestick | `chart.type: 'candlestick'`, dados `{ x, y: [abertura, máxima, mínima, fechamento] }`, `plotOptions.candlestick.colors` | Preço de mercado em 30 dias |
| Radar | `chart.type: 'radar'`, `plotOptions.radar.polygons`, `fill.opacity` | Comparar duas rodadas nas mesmas dimensões |
| Treemap | `chart.type: 'treemap'`, `distributed: true`, rótulos HTML sobrepostos | Composição de receita; área proporcional ao valor |
| Waterfall | `chart.type: 'bar'` + `stacked: true`, base transparente | Saldo inicial → receitas → custos → saldo final |
| Gauge radial | `chart.type: 'radialBar'`, `plotOptions.radialBar.track` | Percentual único contra uma meta |
| Empilhado / agrupado | `chart.type: 'bar'`, `chart.stacked` alternado por `updateOptions` | Mesma série em duas leituras, sem recriar o gráfico |
| Previsão | `chart.type: 'line'` com uma série `type: 'rangeArea'` | Realizado sólido + previsto tracejado + faixa de confiança |

O waterfall não é um tipo nativo do ApexCharts: é uma barra empilhada com uma série transparente de base, uma de aumento (`ttsc-success`), uma de redução (`ttsc-danger`) e uma de total (`ttsc-accent`; `ttsc-primary-400` no escuro). A anotação `−78` marca a barra pequena de impostos. Rótulos: branco sobre aumento/redução, `ttsc-accent-on` sobre o total.

O treemap também não usa os rótulos nativos: o Apex gira e trunca o texto em tiles estreitos. O preview desenha `.tm-lab` em HTML, sincronizado com `rect.apexcharts-treemap-rect` por `getBoundingClientRect()` e `ResizeObserver`.

## Estados

| Estado | Como aparece |
|---|---|
| Carregando | Card com [Skeleton](../Skeleton/README.md) de 220 px no lugar do gráfico; título e pill já visíveis. |
| Vazio | Mensagem central “Sem dados para o período” em `ttsc-text-muted`, sem eixos; mantenha o card. |
| Erro | Texto em `ttsc-danger-text` acima do container e ação “Tentar novamente”; não deixe o SVG antigo. |
| Hover | Tooltip do Apex com `ttsc-surface`, borda `ttsc-border` e sombra `ttsc-shadow-popover`; conteúdo específico por gráfico. |
| Foco | Anel de 2 px em `ttsc-accent` nos botões do seletor; o SVG do Apex não recebe foco. |
| Selecionado | `aria-pressed="true"` no botão Empilhado/Agrupado, fundo `ttsc-surface` e status `aria-live`. |
| Destaque | Série/ponto ativo com cores de `success`, `danger` ou `warning`; sempre acompanhado de rótulo. |
| Desabilitado | `opacity: .55`, `pointer-events: none` e `aria-disabled="true"` no card; não remova o resumo em texto. |
| Movimento reduzido | `chart.animations.enabled = false` quando `prefers-reduced-motion: reduce`. |
| Tema escuro | `theme.mode`, `tooltip.theme`, `foreColor` e grade relidos por `MutationObserver` em `data-theme`/`class`. |

## Acessibilidade

- Cada container tem `role="img"` e um `aria-label` que resume tendência, extremos e metas — o SVG do Apex não é lido.
- O `<details>` “Ver tabela de dados” repete mês, previsto, intervalo e realizado; é o caminho de teclado e de leitor de tela para os números.
- Valores aparecem em texto: rótulos de dados no waterfall, legenda com nomes, pill de saldo e anotação `−78`. Cor não é o único indicador.
- Rótulos do waterfall usam branco sobre `ttsc-success`/`ttsc-danger` e `ttsc-accent-on` (#0f0f0f) sobre o total. No escuro, o total usa `ttsc-primary-400` com o mesmo texto escuro.
- Tooltips têm `ttsc-text` sobre `ttsc-surface` nos dois temas; a legenda usa `ttsc-text-2`, não o verde da série.
- O seletor Empilhado/Agrupado é um `role="group"` com dois `<button type="button">` e `aria-pressed`; o resultado é anunciado em `role="status" aria-live="polite"`.
- `prefers-reduced-motion: reduce` desliga animações do Apex e transições CSS; o gráfico continua legível sem movimento.
- Contraste mínimo de 4,5:1 para texto pequeno; eixos e grade são decorativos e ficam em `ttsc-text-muted`/`ttsc-border`.

## API

Namespace global `window.TTSCChartsAdvanced` (preview). Em produção, os mesmos blocos de opções podem ser extraídos para `assets/js/core/ttsc.apex-advanced.js`.

| Método | Efeito |
|---|---|
| `TTSCChartsAdvanced.init()` | Monta os sete gráficos nos containers `#ax-*`; não duplica se já houver gráficos. |
| `TTSCChartsAdvanced.destroy()` | Chama `chart.destroy()` em todos, limpa rótulos do treemap e desconecta o observer de tema. |
| `TTSCChartsAdvanced.charts()` | Devolve a lista de instâncias ApexCharts montadas. |
| `TTSCChartsAdvanced.relayout()` | Reposiciona os rótulos HTML do treemap após mudança de largura. |

Opções relevantes do ApexCharts:

| Opção | Efeito |
|---|---|
| `chart.type` | `candlestick`, `radar`, `treemap`, `bar`, `radialBar` ou `line`. |
| `chart.stacked` | Alterna empilhado/agrupado via `updateOptions({ chart: { stacked } }, true, false)`. |
| `theme.mode`, `tooltip.theme`, `chart.foreColor` | Paleta do Apex conforme `data-theme`. |
| `chart.background: 'transparent'` | Deixa o `ttsc-surface` do card aparecer. |
| `dataLabels.style.colors` | Aceita um array por série; no waterfall, `['transparent', '#fff', '#fff', accentOn]`. |
| `plotOptions.bar.dataLabels.position` | `'top'` para valores fora da barra no waterfall. |
| `xaxis.type: 'datetime'` + `labels.format` | Datas em `dd/MM` no candlestick. |
| `tooltip.custom` | HTML próprio com os tokens, em vez do tooltip padrão do Apex. |
| `annotations.points` | Marca a barra de impostos com `−78`. |

Formatadores: `Intl.NumberFormat('pt-BR')` para inteiros, uma e duas casas; `toLocaleDateString('pt-BR')` para datas. O locale `pt-br` é inline (`months`, `shortMonths`, `days`, `shortDays`, `toolbar`).

## Modelos

### HTML

```php
<div class="axg">
  <figure class="ax-card s7">
    <div class="ax-hd">
      <div>
        <h2>Candlestick · <?= $this->e($symbol) ?></h2>
        <p><?= (int) $days ?> dias até <?= $this->e($asOf) ?> · preços em US$</p>
      </div>
      <span class="ax-pill ax-pill--ok"><span class="dot"></span><?= $this->e($changeLabel) ?></span>
    </div>
    <div id="ax-candle" class="ax-chart" role="img"
         aria-label="<?= $this->e($candleSummary) ?>"
         data-chart='<?= json_encode($candles, JSON_HEX_APOS | JSON_HEX_TAG) ?>'></div>
  </figure>

  <figure class="ax-card s5">
    <div class="ax-hd">
      <div><h2>Radar · Maturidade operacional</h2><p>Comparação <?= (int) $yearA ?> e <?= (int) $yearB ?> · escala de 0 a 100</p></div>
    </div>
    <div id="ax-radar" class="ax-chart" role="img"
         aria-label="<?= $this->e($radarSummary) ?>"
         data-chart='<?= json_encode($radar, JSON_HEX_APOS | JSON_HEX_TAG) ?>'></div>
    <ul class="ax-radar-legend" aria-label="Séries">
      <li class="lg" style="--c:var(--ttsc-info)"><i></i><?= (int) $yearA ?></li>
      <li class="lg" style="--c:var(--ttsc-accent)"><i></i><?= (int) $yearB ?></li>
    </ul>
  </figure>

  <figure class="ax-card s12">
    <div class="ax-hd">
      <div>
        <h2>Receita realizada vs. prevista</h2>
        <p>Valores em R$ mil · faixa de 90% de confiança</p>
      </div>
      <span class="ax-pill ax-pill--warn"><span class="dot"></span>Outubro previsto: <?= $this->e($forecastPill) ?></span>
    </div>
    <div id="ax-forecast" class="ax-chart" role="img"
         aria-label="<?= $this->e($forecastSummary) ?>"
         data-chart='<?= json_encode($forecast, JSON_HEX_APOS | JSON_HEX_TAG) ?>'></div>
    <details class="ax-details">
      <summary>Ver tabela de dados</summary>
      <div class="ax-table-wrap">
        <table class="ax-table">
          <caption class="sr-only">Receita realizada e prevista, em reais mil.</caption>
          <thead><tr><th scope="col">Mês</th><th scope="col">Previsto</th><th scope="col">Intervalo</th><th scope="col">Realizado</th></tr></thead>
          <tbody>
            <?php foreach ($forecast['rows'] as $row): ?>
            <tr>
              <td><?= $this->e($row['month']) ?></td>
              <td><?= number_format($row['prev'], 0, ',', '.') ?></td>
              <td><?= number_format($row['low'], 0, ',', '.') ?>–<?= number_format($row['high'], 0, ',', '.') ?></td>
              <td><b><?= $row['real'] === null ? '—' : number_format($row['real'], 0, ',', '.') ?></b></td>
            </tr>
            <?php endforeach; ?>
          </tbody>
        </table>
      </div>
    </details>
  </figure>
</div>
```

O preview também tem waterfall, gauge, treemap e barras por canal; os containers e `aria-label` seguem o mesmo padrão.

### CSS

```css
.axg { max-width: 1280px; margin: 0 auto; padding: 16px; display: grid;
       grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 14px; }
.ax-card { margin: 0; min-width: 0; padding: 14px 16px 12px; background: var(--ttsc-surface);
           border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-surface);
           box-shadow: var(--ttsc-shadow-sm); }
.s7 { grid-column: span 7; } .s5 { grid-column: span 5; }
.s4 { grid-column: span 4; } .s8 { grid-column: span 8; } .s12 { grid-column: span 12; }
.ax-hd { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: 8px; }
.ax-hd h2 { margin: 0; font-size: 14px; line-height: 20px; font-weight: 600; color: var(--ttsc-text); }
.ax-hd p { margin: 2px 0 0; font-size: 12px; line-height: 16px; color: var(--ttsc-text-muted); }
.ax-chart { min-width: 0; }
.ax-note { margin: 4px 0 0; font-size: 11px; line-height: 16px; color: var(--ttsc-text-muted); }

/* Apex usa SVG; a legenda fica horizontal no topo/rodapé */
.ax-card .apexcharts-legend { flex-direction: row; flex-wrap: wrap; justify-content: flex-start; }
.apexcharts-tooltip, .apexcharts-tooltip.apexcharts-theme-light,
.apexcharts-tooltip.apexcharts-theme-dark {
  background: var(--ttsc-surface) !important; color: var(--ttsc-text) !important;
  border: 1px solid var(--ttsc-border) !important; box-shadow: var(--ttsc-shadow-popover) !important;
  border-radius: var(--ttsc-radius-sm);
}
.apexcharts-xaxistooltip { background: var(--ttsc-surface); border-color: var(--ttsc-border); color: var(--ttsc-text); }
.apexcharts-legend-text { color: var(--ttsc-text-2) !important; }

/* Treemap: rótulos HTML sobre o SVG */
.tm-wrap { position: relative; width: 100%; }
.tm-labels { position: absolute; inset: 0; pointer-events: none; }
.tm-lab { position: absolute; display: flex; flex-direction: column; align-items: center;
          justify-content: center; overflow: hidden; padding: 2px 4px; text-align: center;
          color: var(--ttsc-text); line-height: 1.15; }
.tm-lab span { font-size: 10px; color: var(--ttsc-text-2); font-variant-numeric: tabular-nums; }

@media (max-width: 1024px) { .ax-card { grid-column: span 12; } }
@media (max-width: 560px)  { .axg { padding: 12px; gap: 10px; } .ax-card { padding: 12px; } }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .001ms !important; transition-duration: .001ms !important; }
}
```

### JS

```js
// assets/js/core/ttsc.apex-advanced.js — requer ApexCharts 8.5.0 íntegro
(function () {
  'use strict';

  var NF0 = new Intl.NumberFormat('pt-BR');
  var NF2 = new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  var isDark = function () {
    var el = document.documentElement;
    return el.dataset.theme === 'dark' || el.classList.contains('dark');
  };

  // Tokens com @property chegam em oklch; o Apex calcula sombras melhor com hex.
  function token(name) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return v.indexOf('oklch(') === 0 ? oklchToHex(v) : v;
  }
  function oklchToHex(str) {
    var m = str.match(/oklch\(\s*([\d.]+%?)\s+([\d.]+)\s+([\d.]+)(?:deg)?\s*\)/);
    if (!m) return str;
    var L = m[1].slice(-1) === '%' ? parseFloat(m[1]) / 100 : parseFloat(m[1]);
    var C = parseFloat(m[2]), h = parseFloat(m[3]) * Math.PI / 180;
    var A = C * Math.cos(h), B = C * Math.sin(h);
    var l = Math.pow(L + 0.3963377774 * A + 0.2158037573 * B, 3);
    var mm = Math.pow(L - 0.1055613458 * A - 0.0638541728 * B, 3);
    var s = Math.pow(L - 0.0894841775 * A - 1.2914855480 * B, 3);
    var enc = function (x) {
      x = x <= 0.0031308 ? 12.92 * x : 1.055 * Math.pow(x, 1 / 2.4) - 0.055;
      return Math.max(0, Math.min(255, Math.round(x * 255))).toString(16).padStart(2, '0');
    };
    return '#' + enc(4.0767416621 * l - 3.3077115913 * mm + 0.2309699292 * s) +
                 enc(-1.2684380046 * l + 2.6097574011 * mm - 0.3413193965 * s) +
                 enc(-0.0041960863 * l - 0.7034186147 * mm + 1.7076147010 * s);
  }

  var PT_BR = { name: 'pt-br', options: {
    months: ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'],
    shortMonths: ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'],
    days: ['domingo','segunda','terça','quarta','quinta','sexta','sábado'],
    shortDays: ['dom','seg','ter','qua','qui','sex','sáb'],
    toolbar: { download: 'Baixar SVG', selection: 'Selecionar', selectionZoom: 'Zoom',
               zoomIn: 'Ampliar', zoomOut: 'Reduzir', pan: 'Mover', reset: 'Restaurar' }
  } };

  function base() {
    var dark = isDark();
    return {
      chart: { fontFamily: 'Inter, system-ui, sans-serif', foreColor: token('--ttsc-text-muted'),
               background: 'transparent', toolbar: { show: false }, zoom: { enabled: false },
               animations: { enabled: !matchMedia('(prefers-reduced-motion: reduce)').matches, speed: 420 },
               defaultLocale: 'pt-br', locales: [PT_BR] },
      theme: { mode: dark ? 'dark' : 'light' },
      tooltip: { theme: dark ? 'dark' : 'light' },
      grid: { borderColor: token('--ttsc-border'), strokeDashArray: 3 },
      dataLabels: { enabled: false },
      legend: { labels: { colors: token('--ttsc-text-2') } }
    };
  }

  var registry = [];

  function mount(el, options, theme) {
    if (!el) return null;
    var chart = new ApexCharts(el, options);
    chart.render();
    registry.push({ chart: chart, theme: theme });
    return chart;
  }

  function mountWaterfall(el) {
    var C = {
      success: token('--ttsc-success'), danger: token('--ttsc-danger'),
      accent: token('--ttsc-accent'), accentOn: token('--ttsc-accent-on'),
      p400: token('--ttsc-primary-400'), text: token('--ttsc-text')
    };
    var theme = function () {
      var dark = isDark();
      return {
        chart: { foreColor: token('--ttsc-text-muted') },
        theme: { mode: dark ? 'dark' : 'light' },
        colors: ['transparent', C.success, C.danger, dark ? C.p400 : C.accent]
      };
    };
    var b = base();
    var chart = new ApexCharts(el, {
      ...b,
      chart: { ...b.chart, type: 'bar', height: 250, stacked: true },
      series: [
        { name: 'Base', data: [0, 1240, 1412, 1334, 0] },
        { name: 'Aumento', data: [0, 386, 0, 0, 0] },
        { name: 'Redução', data: [0, 0, 214, 78, 0] },
        { name: 'Total', data: [1240, 0, 0, 0, 1334] }
      ],
      colors: ['transparent', C.success, C.danger, isDark() ? C.p400 : C.accent],
      plotOptions: { bar: { columnWidth: '56%', borderRadius: 3, borderRadiusWhenStacked: 'last' } },
      dataLabels: { enabled: true, offsetY: -2,
        style: { fontSize: '11px', fontWeight: 600, colors: ['transparent', '#ffffff', '#ffffff', C.accentOn] },
        formatter: function (v, opt) {
          if (!v || opt.seriesIndex === 0) return '';
          return opt.seriesIndex === 1 ? '+' + NF0.format(v)
               : opt.seriesIndex === 2 ? '−' + NF0.format(v) : NF0.format(v);
        } },
      xaxis: { categories: ['Saldo inicial', 'Receitas', 'Custos', 'Impostos', 'Saldo final'] },
      yaxis: { min: 0, max: 2000, tickAmount: 4 }
    });
    chart.render();
    registry.push({ chart: chart, theme: theme });
    return chart;
  }

  function mountForecast(el) {
    var C = { accent: token('--ttsc-accent'), info: token('--ttsc-info') };
    var months = ['nov','dez','jan','fev','mar','abr','mai','jun','jul','ago','set','out'];
    var low = [398,414,427,442,457,470,484,498,512,526,540,556];
    var high = [422,438,453,470,487,502,518,534,551,568,588,610];
    var prev = [410,426,440,456,472,486,501,517,532,548,566,584];
    var real = [412,428,441,458,474,487,503,518,534,549,null,null];
    var band = isDark() ? token('--ttsc-primary-800') : token('--ttsc-primary-200');
    var b = base();
    var chart = new ApexCharts(el, {
      ...b,
      chart: { ...b.chart, type: 'line', height: 252 },
      series: [
        { name: 'Intervalo de confiança', type: 'rangeArea',
          data: months.map(function (m, i) { return { x: m, y: [low[i], high[i]] }; }) },
        { name: 'Realizado', type: 'line',
          data: real.map(function (v, i) { return v == null ? null : { x: months[i], y: v }; }).filter(Boolean) },
        { name: 'Previsto', type: 'line',
          data: months.map(function (m, i) { return { x: m, y: prev[i] }; }) }
      ],
      colors: [band, C.accent, C.info],
      stroke: { curve: 'straight', width: [0, 3, 2], dashArray: [0, 0, 6] },
      fill: { type: ['solid', 'solid', 'solid'], opacity: [isDark() ? 0.5 : 0.7, 1, 1] },
      markers: { size: [0, 3, 0], strokeWidth: 0 },
      yaxis: { min: 380, max: 620, tickAmount: 3 },
      tooltip: { custom: function (ctx) {
        var i = ctx.dataPointIndex;
        return '<b>' + months[i] + ' · R$ mil</b><br>Previsto: ' + NF0.format(prev[i]) +
          '<br>Intervalo: ' + NF0.format(low[i]) + '–' + NF0.format(high[i]) +
          (real[i] == null ? '<br>Sem realizado consolidado.'
            : '<br>Realizado: ' + NF0.format(real[i]) + ' (' + NF2.format(real[i] / prev[i] * 100 - 100) + '%)');
      } }
    });
    chart.render();
    registry.push({ chart: chart, theme: function () {
      return { theme: { mode: isDark() ? 'dark' : 'light' }, tooltip: { theme: isDark() ? 'dark' : 'light' } };
    } });
    return chart;
  }

  var observer = new MutationObserver(function () {
    registry.forEach(function (item) {
      try { item.chart.updateOptions(item.theme(), true, false); } catch (e) { /* desmontado */ }
    });
  });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme', 'class'] });

  window.TTSCChartsAdvanced = {
    init: function (root) {
      root = root || document;
      mountWaterfall(root.querySelector('#ax-waterfall'));
      mountForecast(root.querySelector('#ax-forecast'));
      return this;
    },
    destroy: function () {
      registry.forEach(function (item) { try { item.chart.destroy(); } catch (e) {} });
      registry.length = 0;
      observer.disconnect();
      return this;
    },
    charts: function () { return registry.map(function (item) { return item.chart; }); }
  };
})();
```

Os outros cinco gráficos usam o mesmo `base()` e a mesma rotina de `registry`; no preview, `candleSeries()`, `buildTreemap()`, `buildGauge()` e `buildStacked()` completam a galeria. O treemap precisa de `layoutTreemapLabels()` depois de `render()` e no `ResizeObserver`.

### SQL

Receita por categoria para o treemap, a partir de `financial_receivables` e `financial_categories` (MariaDB 10.11 / MySQL 8):

```sql
SELECT COALESCE(c.name, 'Sem categoria') AS label,
       SUM(COALESCE(r.amount_paid, 0))   AS total
  FROM financial_receivables r
  LEFT JOIN financial_categories c
         ON c.id = r.category_id AND c.deleted_at IS NULL
 WHERE r.deleted_at IS NULL
   AND r.status IN ('paid', 'partial')
   AND r.payment_date >= :period_start
   AND r.payment_date <  :period_end
 GROUP BY COALESCE(c.name, 'Sem categoria')
HAVING total > 0
 ORDER BY total DESC;
```

Waterfall de receita reconhecida, a partir da tabela real `billing_revenue_waterfall`:

```sql
SELECT beginning_balance, new_deferred, recognized, adjustments, ending_balance
  FROM billing_revenue_waterfall
 WHERE period_label = :period_label
 ORDER BY snapshot_date DESC
 LIMIT 1;
```

O PHP converte o resultado em quatro séries (`base`, `aumento`, `redução`, `total`): `new_deferred` entra como aumento, `recognized` e `adjustments` negativos entram como redução, e `ending_balance` fecha o total. `billing_revenue_waterfall` não tem `tenant_id` nem `deleted_at`; o recorte de tenant é o banco/conexão do tenant. Para previsão, a série mensal sai de `financial_budgets` (`jan`…`dec_month`) e o realizado de `billing_payments`; o candlestick de BTC é dado externo e não tem tabela no repo.

## Faça / Não faça

- **Faça:** ler as cores dos tokens em cada troca de tema e atualizar com `updateOptions`, sem recriar o gráfico.
- **Faça:** usar `chart.background: 'transparent'` e `foreColor`; o card já tem `ttsc-surface`.
- **Faça:** manter rótulos de valor no waterfall e uma tabela alternativa para leitores de tela.
- **Faça:** testar o waterfall com valores negativos e com barras muito pequenas; a anotação resolve o caso de 78 mil.
- **Não faça:** usar `chart.type: 'rangeArea'` com séries mistas e pontos nulos — use `type: 'line'` com uma série `rangeArea`, como no preview.
- **Não faça:** confiar nos rótulos nativos do treemap em tiles estreitos; eles giram e truncam.
- **Não faça:** deixar a legenda vertical (o `bundle.css` força `flex-direction: column`; sobrescreva para `row`).
- **Não faça:** usar este componente como sankey nativo — a lib não tem (use [SankeyFlow](../SankeyFlow/README.md)); o waterfall ganhou tipo nativo na 8.5.0, mas a ponte em barras empilhadas daqui segue válida — migre só se fizer sentido.
