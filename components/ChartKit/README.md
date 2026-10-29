# ChartKit

Galeria completa de gráficos de gestão — 41 modelos em 8 seções numeradas, com índice clicável e mapa de decisão no topo: famílias nativas do ApexCharts 8.5.0 e os modelos em SVG puro (funil, pirâmide, sunburst, waffle, marimekko, venn), tudo em tokens, aria e nos dois temas.

## Quando usar

- Painéis de gestão que precisam escolher o gráfico certo para cada pergunta: o topo do preview traz o **Índice do Catálogo** (âncoras `#ck-s1`–`#ck-s8` que rolam até cada família) e o **Mapa de Decisão** (“pergunta de gestão → modelo”).
- Dashboards escolares e administrativos (receita, matrículas, ocupação, inadimplência, unidades) com dados determinísticos e números em pt-BR (`R$ 1.512 mil`, `88,4%`).
- Funil, pirâmide, sunburst, waffle, marimekko e venn vêm como SVG puro com os mesmos tokens, `role="img"` e re-render no toggle de tema. Na versão instalada (8.5.0) funnel, pyramid, sunburst e waffle já têm tipo nativo (conforme scan do bundle) — os modelos em SVG permanecem por serem determinísticos, navegáveis por teclado (sunburst) e independentes da lib; migrar para o tipo nativo é opcional.
- Acelerar a implementação: cada card é uma função da fábrica `window.TTSCChartKit` que recebe `(el, data, opts)` e re-renderiza via `updateTheme()`.

Não use quando:

- O gráfico é um único modelo simples já coberto por [ApexCharts](../ApexCharts/README.md) — aqui a galeria é para escolher entre famílias.
- O tipo é radar ou waterfall com faixa de confiança: use [ApexChartsAdvanced](../ApexChartsAdvanced/README.md) (candlestick simples está no kit, modelo 36).
- O assunto é fluxo origem → desfecho: use [SankeyFlow](../SankeyFlow/README.md); o ApexCharts 8.5.0 não tem sankey nativo.
- O funil precisa de navegação por teclado em CSS puro: use [FunnelBars](../FunnelBars/README.md) — o modelo 33 daqui é visual, em SVG.
- A tela não pode carregar ApexCharts (~150 kB): use os componentes CSS/SVG ([Progress](../Progress/README.md), [Bullets](../Bullets/README.md), [KpiView](../KpiView/README.md)) ou os modelos em SVG puro da seção 7.

### Mapa completo do sistema

41 modelos numerados de forma estável (chip no canto de cada card); a coluna **Onde** aponta a seção do catálogo ou o componente especializado.

| # | Modelo | Use para | Não use para | Onde |
|---|---|---|---|---|
| 1 | Barra vertical básica | Comparar 3 a 8 períodos com valor exato em cima | Séries duplas (use 3) ou ranking (use 2) | 1. Comparação |
| 2 | Barra horizontal | Ranking de categorias com nome longo | Série temporal (use 10) | 1. Comparação |
| 3 | Barras agrupadas | Duas séries opostas no mesmo recorte | Mais de 3 séries (empilhe, 4) | 1. Comparação |
| 4 | Barra empilhada segmentada | Partes que somam um total por período | Totais muito distintos entre períodos (use 5) | 1. Comparação |
| 5 | Barra 100% empilhada | Composição percentual mês a mês | Mostrar volume absoluto (use 4) | 1. Comparação |
| 6 | Barra com meta | Valor por categoria contra um limite explícito | Vários limites por categoria ([BulletChart](../BulletChart/README.md)) | 1. Comparação |
| 7 | Range bar | Início e fim de períodos por projeto | Dependências entre tarefas ([Gantt](../Gantt/README.md)) | 1. Comparação |
| 8 | Dumbbell | De-para entre dois momentos por categoria | Mais de dois momentos (use 31) | 1. Comparação |
| 9 | Bullet vertical | Um valor contra faixas e meta em uma figura | Vários KPIs empilhados em lista ([BulletChart](../BulletChart/README.md)) | 1. Comparação |
| 10 | Linha suave com marcadores | Tendência contínua com leitura ponto a ponto | 3 a 5 valores soltos (use 1) | 2. Tendência |
| 11 | Área em gradiente | Volume de um único indicador | Comparar séries (use 12) | 2. Tendência |
| 12 | Área empilhada | Composição que evolui no tempo | Forma que flui sem leitura de eixo (use 35) | 2. Tendência |
| 13 | Multi-linha | Até 4 trajetórias no mesmo eixo | Muitas séries (vira espaguete) | 2. Tendência |
| 14 | Step line | Valor que só muda em evento (saldo, preço tabelado) | Tendência suave (use 10) | 2. Tendência |
| 15 | Realizada + prevista | Histórico com projeção contínua | Incerteza grande (faixa de confiança em [ApexChartsAdvanced](../ApexChartsAdvanced/README.md)) | 2. Tendência |
| 16 | Combo eixo duplo | Duas unidades relacionadas no tempo | Eixos sem relação entre si (engana a leitura) | 2. Tendência |
| 17 | Sparkline | Tendência dentro de um KPI de 48 px | Análise fora do KPI (use 10) | 2. Tendência |
| 18 | Donut | 3 a 5 fatias de um total, com total central | Precisão entre fatias próximas (use 2) | 3. Composição |
| 19 | Multi-donut (small multiples) | A mesma composição em vários grupos | Muitos grupos ou status ([HeatmapMatrix](../HeatmapMatrix/README.md)) | 3. Composição |
| 20 | Treemap | Muitas categorias proporcionais em uma figura | Hierarquia com dois níveis (use 37) | 3. Composição |
| 21 | Scatter | Correlação de duas medidas por indivíduo | Série no tempo (use 10) | 4. Distribuição |
| 22 | Bubble | Três medidas, uma por bolha | Mais de ~8 bolhas ou sem relação X/Y | 4. Distribuição |
| 23 | Gauge radial | Um percentual contra uma meta | Vários indicadores no mesmo card (use 25) | 5. Indicadores |
| 24 | Semi-gauge | Um valor contra um teto máximo | Valor sem máximo natural (use 23) | 5. Indicadores |
| 25 | Anéis múltiplos | 2 a 4 percentuais de naturezas diferentes | Evolução no tempo (use 13) | 5. Indicadores |
| 26 | Boxplot | Dispersão e outliers por categoria | Relação entre duas medidas (use 21) | 6. Estatística |
| 27 | Histograma | Frequência por faixa de um total | Categorias sem ordem (use 1) | 6. Estatística |
| 28 | Polar area | Ciclos (dia da semana, mês do ano) | Séries longas no tempo (use 10) | 6. Estatística |
| 29 | Pirâmide populacional | Duas populações por categoria em espelho | Mais de duas populações | 6. Estatística |
| 30 | Pareto | Poucas causas, maioria do efeito | Causas de peso similar | 6. Estatística |
| 31 | Slope | Dois momentos, uma linha por categoria | Mais de dois momentos (use 13) | 6. Estatística |
| 32 | Bump | Mudança de posição ao longo do tempo | Valores absolutos (use 10) | 6. Estatística |
| 33 | Funil (SVG puro) | Etapas que só diminuem, com % do topo | Navegação por teclado ([FunnelBars](../FunnelBars/README.md)) | 3. Composição |
| 34 | Pirâmide (SVG puro) | Base por segmento em largura proporcional | Comparação com o tempo (use 10) | 3. Composição |
| 35 | Streamgraph | Composição que flui ao longo do ano | Ler valores exatos por série (use 12) | 3. Composição |
| 36 | OHLC + volume | Preço com abertura/máxima/mínima/fechamento e volume | Série sem variação diária | 3. Composição |
| 37 | Sunburst | Hierarquia de 2 níveis com foco por ramo | Mais de 3 níveis de profundidade | 7. Hierarquia |
| 38 | Waffle | Partes do todo em pictograma de 100 | Precisão entre fatias (use 18) | 7. Hierarquia |
| 39 | Marimekko | Duas dimensões proporcionais sem eixos | Valores exatos por célula (use 4) | 7. Hierarquia |
| 40 | Venn | Interseções de até 3 conjuntos | Mais de 3 conjuntos | 7. Hierarquia |
| 41 | Calendar heatmap | Atividade por dia do ano em faixas | Padrão intra-diário (use 10) | 8. Calendário |

### Especializados de fora do kit

| Componente | Use para | Onde |
|---|---|---|
| [BulletChart](../BulletChart/README.md) | KPI composto de linha com faixas, em CSS puro e navegável por teclado | Componente próprio |
| [SankeyFlow](../SankeyFlow/README.md) | Fluxo origem → desfecho com volumes proporcionais | Componente próprio |
| [GeoMap](../GeoMap/README.md) | Distribuição geográfica por unidade da federação | Componente próprio |
| [FunnelBars](../FunnelBars/README.md) | Funil acessível em CSS, com valor e queda por etapa | Componente próprio |
| [HeatmapMatrix](../HeatmapMatrix/README.md) | Densidade em duas dimensões categóricas | Componente próprio |
| [RankedBars](../RankedBars/README.md) | Ranking com variação e destaque textual | Componente próprio |
| [QuadrantMatrix](../QuadrantMatrix/README.md) | Análise em quadrantes estratégicos | Componente próprio |
| [WidgetIncomeBreakdown](../WidgetIncomeBreakdown/README.md) | Quebra de receita pronta para painel | Widget de painel |
| [ApexChartsAdvanced](../ApexChartsAdvanced/README.md) | Radar, waterfall e linha com faixa de confiança | Componente próprio |



## Anatomia

```
┌ .ck (grade de 12 colunas, gap 14) ─────────────────────────────┐
│ ┌ figure.ck-card.s12 · Índice do Catálogo ──────────────────┐  │
│ │ nav.ck-toc → âncoras #ck-s1 … #ck-s8 (rolam suave)        │  │  topo: navegação
│ └────────────────────────────────────────────────────────────┘  │
│ ┌ figure.ck-card.s12 · Mapa de Decisão ─────────────────────┐  │
│ │ table.ck-map → pergunta de gestão ⇒ nº do chip do modelo  │  │  topo: decisão
│ └────────────────────────────────────────────────────────────┘  │
│ ┌ header.ck-sec#ck-s1 ──────────────────────────────────────┐  │
│ │ 1. Comparação           9 modelos · do básico ao dumbbell │  │  seção numerada + âncora
│ └────────────────────────────────────────────────────────────┘  │
│ ┌ figure.ck-card.s4 ───────────┐ ┌ figure.ck-card.s4 ────────┐ │
│ │ h3 + .sub + .ck-chip (1–41) │ │                           │ │  card com span 4/6/8/12
│ │ div[role=img][aria-label]   │ │  SVG do Apex ou SVG puro  │ │  180–240 px de gráfico
│ │ figcaption.ck-note (quando) │ │                           │ │  legenda Apex ou HTML
│ └──────────────────────────────┘ └───────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

| Parte | Classe / elemento | Obrigatório | Função |
|---|---|---|---|
| Grade | `.ck` | sim | 12 colunas `minmax(0,1fr)`, `max-width: 1280px`, `gap: 14px` |
| Índice | `figure.ck-card.s12` + `nav.ck-toc` | sim | Âncoras `#ck-s1`–`#ck-s8` com `scroll-behavior: smooth` e `scroll-margin-top` |
| Mapa de decisão | `table.ck-map` | recomendado | “Pergunta de gestão → modelo”, com os números dos chips |
| Seção | `header.ck-sec` + `h2` numerado + `id="ck-sN"` | sim | Oito famílias numeradas; alvo das âncoras do índice |
| Card | `figure.ck-card` + `.s4/.s6/.s8/.s12` | sim | Moldura com `ttsc-border`, `ttsc-radius-surface`, `ttsc-shadow-sm` e largura na grade |
| Chip | `.ck-chip` no canto do título | sim | Número estável do modelo (1–41), referenciado pelo mapa de decisão |
| Título | `.ck-hd h3` | sim | Title Case, uma linha, com o chip à direita |
| Contexto | `.ck-hd .sub` | sim | Período, unidade e recorte dos dados |
| Container | `div[role="img"][aria-label]` | sim | O SVG do Apex não tem semântica própria; no sunburst os setores ainda recebem `tabindex="0"` |
| Base options | `apexBase(C)` | sim | Fonte, `foreColor`, fundo transparente, toolbar/zoom off, animação curta, locale pt-BR inline |
| Nota | `figcaption.ck-note` | sim | Quando usar este modelo e qual escolha de grade/legenda foi feita |
| Legenda compartilhada | `.ck-legend` | quando 2+ séries sem legenda Apex | Dots e amostras de linha em HTML, sempre com texto |
| Overlay | `.ck-tm-labels`, `.ck-tick` | em treemap e semi-gauge | Rótulos sincronizados e marca do teto posicionados por medição |

### Escala e alturas

As alturas dos gráficos são fixas por card (180–240 px; sparklines de 48 px; roscas do multi-donut de 170 px; funil e pirâmide em viewBox 560 px que escala com a largura) e o card cresce com a legenda e a nota; a nota usa `margin-top: auto` para se alinhar à base do card. Em `> 1024 px` os spans variam entre 4, 6, 8 e 12 colunas; em `≤ 1024 px` os cards de 4 colunas passam a 6 e os demais a 12; em `≤ 640 px` tudo colapsa para 1 coluna, sem overflow, e o índice empacota como lista fluida. O preview completo mede 8.316 px em 1.280 px de largura (`@dsCard height=8330`).

## Variantes

| Variante | Classe / opção | Uso |
|---|---|---|
| Grade ligada | `gridOn(C)` — `borderColor` do token + `strokeDashArray: 3` | Leitura de valores nos eixos (2, 5, 8, 10, 14, 15, 16, 21, 22, 26, 30, 32, 36) |
| Grade desligada | `gridOff(C)` — `show: false` | O rótulo, a legenda ou a anotação já carregam o valor (1, 3, 4, 6, 7, 9, 11, 12, 13, 27, 29, 31, 35) |
| Legenda Apex | `legendBottom(C)` | 3, 4, 5, 12, 13, 16, 29, 35, 36 (a 25 usa `legend.formatter` com valores; a 28 também) |
| Legenda HTML compartilhada | `.ck-legend` | 8 (dois pontos + haste), 15 (amostra sólida/tracejada), 19 (status), 22 (unidades), 38 (status do waffle), 39 (categorias), 41 (faixas do heatmap) |
| Meta / limite | `annotations.yaxis` | 6 (“Meta 85” em `ttsc-warning`), 9 (faixas sombreadas + “Meta 80”), 15 (tracejado na projeção), 27 (“Média 7,5” no eixo X), 30 (“80%” no eixo acumulado), 23/24 (meta e teto em texto) |
| Séries simples | 1, 2, 6, 7, 9, 10, 11, 14, 18, 21, 23, 24, 27, 33, 34 | Um recorte, sem legenda |
| Séries duplas | 3 (agrupadas), 8 (dois pontos), 15 (dois trechos), 16 (dois eixos), 36 (velas + volume), 39 (largura × altura) | Comparação A vs. B |
| Séries empilhadas | 4 (`stacked: true`), 5 (`stackType: '100%'`), 12 (área), 35 (streamgraph `stackType: '100%'`), 39 (mix por coluna) | Parte/todo e composição |
| Eixo invertido | `yaxis.reversed: true` | 32 (bump com 1º no topo); 29 (pirâmide com valores negativos e `Math.abs`) |
| Tooltip custom | `tooltip.custom` + `.ck-tip` | 7 (datas + duração), 8 (de/para com Δ%), 15 (período + status), 16 (duas unidades), 21 (aluno), 22 (unidade), 26 (quartis), 30 (participação + acumulado), 31 (dois momentos), 32 (posição), 35 (total do mês), 36 (OHLC + volume), 41 (data + valor) |
| Tooltip nativo em SVG | `<title>` por forma | 33, 34 (etapas), 37 (setores), 38 (faixa de 10), 39 (coluna × categoria), 40 (conjunto) |
| Faixas de cor | `plotOptions.heatmap.colorScale` | 41 (cinco faixas da escala `ttsc-primary-50…700`) |
| SVG puro | `funnelSvg()`, `buildSunburst()`, `buildWaffle()`, `buildMarimekko()`, `buildVenn()` | 33, 34, 37–40: determinísticos, navegáveis (sunburst) e independentes da lib; funnel/pyramid/sunburst/waffle têm tipo nativo na 8.5.0 — migrar é opcional; re-renderizados no toggle de tema |
| Animação | `chart.animations.speed: 380`, `enabled: !RM` | Entrada curta em todos; desligada com `prefers-reduced-motion` |

## Estados

| Estado | Como aparece |
|---|---|
| Vazio | Mensagem central “Sem dados para o período” em `ttsc-text-muted` no lugar do SVG; mantenha o card e a nota. |
| Sem dados (série zerada) | Gráfico renderiza com zero em todas as categorias; esconda o eixo e mostre o valor “0” em texto na nota. |
| Carregando | [Skeleton](../Skeleton/README.md) com a altura do gráfico no lugar do container; título e contexto já visíveis. |
| Erro | Texto em `ttsc-danger-text` acima do container e ação “Tentar novamente”; não deixe o SVG antigo. |
| Hover | Tooltip do Apex com `ttsc-surface`, borda `ttsc-border` e sombra `ttsc-shadow-popover`; conteúdo por card (custom em 13 cards); nos SVG puros, `<title>` nativo por forma e destaque do ramo no sunburst. |
| Foco | Anel de 2 px em `ttsc-accent` via `:focus-visible` nos links do índice; no sunburst, cada setor tem `tabindex="0"` com stroke de foco; o SVG do Apex não recebe foco — a alternativa textual é o `aria-label`. |
| Desabilitado | `opacity: .55`, `pointer-events: none` e `aria-disabled="true"` no card; mantenha resumo em texto. |
| Movimento reduzido | `chart.animations.enabled = false` quando `prefers-reduced-motion: reduce`; overlays (treemap, teto) posicionam sem espera de animação. |
| Tema escuro | `updateTheme()` destrói e re-renderiza os 39 gráficos ApexCharts e os 6 SVGs customizados (funil, pirâmide, sunburst, waffle, marimekko, venn) relendo os tokens, sem recarregar a página. |

## Acessibilidade

- Cada um dos 45 containers tem `role="img"` e um `aria-label` que resume extremos, tendência e metas — o SVG do Apex não é lido pelo leitor de tela; no sunburst, cada setor ainda é focável (`tabindex="0"`) com `aria-label` e `title` próprios.
- Estado nunca só por cor: valores em rótulos (1, 2, 4, 5, 6, 9, 27, 29, 33, 34), legenda com nomes (3, 12, 13, 16, 18, 19, 22, 25, 28, 29, 32, 35, 36), deltas com seta Font Awesome + texto (“+8,1% vs. set.”) e metas sempre rotuladas (“Meta 85”, “Meta 80”, “Média 7,5”, “80%”, “teto 5%”).
- O teto do semi-gauge (24) tem marca visual (haste vermelha) e texto (“teto 5%”); o vermelho do arco é reforçado pela nota “acima do teto”.
- Venn (40) descreve as sete regiões no `aria-label`, com as contagens em texto dentro de cada região; os 888 alunos fora dos programas são declarados na nota para não parecer o total.
- Waffle (38) carrega tooltip textual por faixa de 10 (`title` em cada quadrado) e as três contagens no `aria-label`; calendar heatmap (41) traz a data completa e o valor no tooltip custom.
- Contraste: rótulos internos usam `ttsc-primary-950` sobre cores claras e `ttsc-primary-50` sobre escuras (função `onColor`); tooltips têm `ttsc-text` sobre `ttsc-surface` nos dois temas; eixos e grade são decorativos em `ttsc-text-muted`/`ttsc-border`.
- `prefers-reduced-motion: reduce` desliga animações do Apex, transições CSS e a rolagem suave das âncoras do índice; o gráfico continua legível sem movimento.
- Tooltips não são acessíveis por teclado: para dados críticos, repita os valores em texto na nota ou em uma tabela `details` (padrão do [ApexChartsAdvanced](../ApexChartsAdvanced/README.md)).
- Números sempre em pt-BR via `Intl.NumberFormat('pt-BR')` — o leitor anuncia “mil duzentos e trinta e quatro”, não “1234”.

## API

Namespace global `window.TTSCChartKit`. Cada família é uma função `(el, data, opts)` que monta o gráfico, registra a instância e devolve `{ charts, rebuild }`; `data` cai nos padrões determinísticos do preview quando omitido.

| Função | Modelo | `data` (quando omitida) |
|---|---|---|
| `barBasic(el, data, opts)` | 1 · barra vertical | `{ meses, valores }` |
| `barRanked(el, data, opts)` | 2 · barra horizontal | `{ itens: [[nome, valor]] }` |
| `barGrouped(el, data, opts)` | 3 · agrupadas | `{ meses, series }` |
| `barStacked(el, data, opts)` | 4 · empilhada segmentada | `{ meses, series }` |
| `bar100(el, data, opts)` | 5 · 100% empilhada | `{ meses, series }` (cada mês soma 100) |
| `barGoal(el, data, opts)` | 6 · barra com meta | `{ unidades, valores, meta }` |
| `rangeBar(el, data, opts)` | 7 · range bar | `{ itens: [[nome, início ISO, fim ISO]] }` |
| `dumbbell(el, data, opts)` | 8 · dumbbell | `{ unidades, pares: [[de, para]] }` |
| `bulletVertical(el, data, opts)` | 9 · bullet | `{ categoria, valor, meta }` |
| `lineSmooth(el, data, opts)` | 10 · linha suave | `{ meses, valores }` |
| `areaGradient(el, data, opts)` | 11 · área em gradiente | `{ semanas, valores }` |
| `areaStacked(el, data, opts)` | 12 · área empilhada | `{ meses, series }` |
| `multiLine(el, data, opts)` | 13 · multi-linha | `{ meses, series }` |
| `stepLine(el, data, opts)` | 14 · step line | `{ dias, valores }` |
| `forecastLine(el, data, opts)` | 15 · realizada + prevista | `{ meses12, real, prev }` (nulos costuram os trechos) |
| `comboDualAxis(el, data, opts)` | 16 · combo eixo duplo | `{ meses, barras, linha }` |
| `sparkline(el, data, opts)` | 17 · sparkline de KPI | `{ nome, valores, cor }` (cor = chave de token, ex.: `accent`) |
| `donut(el, data, opts)` | 18 · donut | `{ rotulos, valores }` |
| `multiDonut(el, data, opts)` | 19 · multi-donut | `{ turnos: [[nome, total, valores]], status }`; `el` é o wrapper com 3 `.ck-md-mount` |
| `treemap(el, data, opts)` | 20 · treemap | `{ itens: [[nome, valor]] }`; rótulos HTML via `relayout` |
| `scatter(el, data, opts)` | 21 · scatter | `{ alunos: [[nome, x, y]] }` |
| `bubble(el, data, opts)` | 22 · bubble | `{ itens: [[nome, x, y, z]] }` |
| `gauge(el, data, opts)` | 23 · gauge radial | `{ valor, rotulo, meta }` |
| `semiGauge(el, data, opts)` | 24 · semi-gauge | `{ valor, teto, escala, rotulo }` |
| `rings(el, data, opts)` | 25 · anéis múltiplos | `{ series: [[nome, valor]] }` |
| `boxplot(el, data, opts)` | 26 · boxplot | `{ turmas, dados: [[min, q1, mediana, q3, max]] }` |
| `histogram(el, data, opts)` | 27 · histograma | `{ faixas, valores, mediaFaixa, media }` |
| `polarArea(el, data, opts)` | 28 · polar area | `{ dias, valores }` |
| `pyramid(el, data, opts)` | 29 · pirâmide populacional | `{ series, masc, fem }` (fem entra negativo; rótulo usa `Math.abs`) |
| `pareto(el, data, opts)` | 30 · pareto | `{ motivos, valores, acumulado }` |
| `slope(el, data, opts)` | 31 · slope chart | `{ momentos, unidades: [[nome, de, para]] }` |
| `bump(el, data, opts)` | 32 · bump chart | `{ meses, series: [[nome, posições]] }` (`yaxis.reversed`) |
| `funnelNative(el, data, opts)` | 33 · funil | `{ etapas: [[nome, valor]] }` — **SVG puro**, independente da lib (tipo `funnel` nativo na 8.5.0; migração opcional) |
| `pyramidNative(el, data, opts)` | 34 · pirâmide de segmentos | `{ segmentos: [[nome, valor]] }` — **SVG puro**, funil invertido |
| `streamgraph(el, data, opts)` | 35 · streamgraph | `{ meses, series }` (`chart.stackType: '100%'`) |
| `ohlcVolume(el, data, opts)` | 36 · OHLC + volume | `{ ohlc: [[abertura, máxima, mínima, fechamento]], vol }` |
| `sunburst(el, data, opts)` | 37 · sunburst | `{ total, segmentos: [{label, value, children}] }` — **SVG puro**, setores focáveis |
| `waffle(el, data, opts)` | 38 · waffle | `{ total, grupos: [[nome, quadrados, contagem]] }` — **SVG/CSS puro** |
| `marimekko(el, data, opts)` | 39 · marimekko | `{ total, categorias, colunas: [[nome, valor, mix]] }` — **SVG puro** |
| `venn(el, data, opts)` | 40 · venn | `{ total, circulos, partes }` — **SVG puro** |
| `calendarHeatmap(el, data, opts)` | 41 · calendar heatmap | `{ semanas }` — dados gerados de forma determinística; `colorScale` em 5 faixas da escala `ttsc-primary` |

| Método | Efeito |
|---|---|
| `TTSCChartKit.init()` | Monta os 39 gráficos ApexCharts e os 6 SVGs customizados nos containers `#ck-*`; não duplica se já montado. |
| `TTSCChartKit.updateTheme()` | Destrói e re-renderiza tudo (Apex + SVG puro) relendo os tokens; ligado ao `MutationObserver` de `data-theme`/`class`. |
| `TTSCChartKit.destroy()` | Chama `chart.destroy()` em tudo, limpa os overlays e os containers de SVG puro, e desconecta os observers. |
| `TTSCChartKit.charts()` | Devolve a lista de instâncias ApexCharts montadas (os modelos em SVG puro não têm instância). |
| `TTSCChartKit.relayout()` | Reposiciona os rótulos do treemap e a marca do teto (ligado ao `ResizeObserver`). |

Atributos e opções relevantes: `role="img"` + `aria-label` em cada container; âncoras `href="#ck-sN"` com `scroll-behavior: smooth`; `chart.background: 'transparent'`, `toolbar: { show: false }`, `zoom: { enabled: false }`; `plotOptions.bar.borderRadiusApplication: 'end'` para cap arredondado; `annotations.yaxis` com `y`/`y2` para faixas e `label.text` para metas (a 30 usa `yAxisIndex: 1`); `stroke.dashArray` para projeção; `tooltip.custom` para HTML próprio; `plotOptions.heatmap.colorScale.ranges` para faixas. Formatadores: `NF0/NF1/NF2` (`Intl.NumberFormat` pt-BR), `pct1`, `brlMil`, `dataBR`.
## Modelos

### HTML

```php
<div class="ck">
  <header class="ck-sec"><h2>Comparação</h2><p>9 modelos · do básico ao dumbbell</p></header>

  <figure class="ck-card s4">
    <div class="ck-hd">
      <h3>Matrículas Novas por Mês</h3>
      <p class="sub"><?= (int) $periodo['meses'] ?> meses até <?= $this->e($periodo['fim']) ?></p>
    </div>
    <div id="ck-basic" class="ck-chart" role="img"
         aria-label="<?= $this->e($novasResumo) ?>"
         data-chart='<?= json_encode($novas, JSON_HEX_APOS | JSON_HEX_TAG) ?>'></div>
    <figcaption class="ck-note">Use para comparar poucos períodos com leitura exata; grade e eixo Y desligados.</figcaption>
  </figure>

  <figure class="ck-card s8">
    <div class="ck-hd">
      <h3>Receita <?= (int) $anoBase ?> → <?= (int) $anoAtual ?></h3>
      <p class="sub">Valores em R$ mil por unidade</p>
    </div>
    <div id="ck-dumbbell" class="ck-chart" role="img"
         aria-label="<?= $this->e($dumbbellResumo) ?>"
         data-chart='<?= json_encode($dumbbell, JSON_HEX_APOS | JSON_HEX_TAG) ?>'></div>
    <div class="ck-legend" aria-label="Séries do dumbbell">
      <span><i style="--c:var(--ttsc-text-muted)"></i><?= (int) $anoBase ?></span>
      <span><i style="--c:var(--ttsc-accent)"></i><?= (int) $anoAtual ?></span>
      <span><i style="--c:var(--ttsc-border-strong)"></i>Haste de variação</span>
    </div>
    <figcaption class="ck-note">De-para entre dois anos por unidade; tooltip custom com o Δ percentual.</figcaption>
  </figure>
</div>
```

O preview repete o padrão para os 41 modelos; `multiDonut` recebe um wrapper com três `.ck-md-mount` (um por turno), `treemap` fica dentro de `.ck-tm` com a camada `.ck-tm-labels`, o sunburst divide o card com `.ck-sb-legend`, e os modelos 33–34 e 37–40 desenham SVG puro direto no container.

### CSS

```css
.ck { max-width: 1280px; margin: 0 auto; padding: 16px; display: grid;
      grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 14px; align-items: stretch; }
.ck-card { display: flex; flex-direction: column; min-width: 0; margin: 0;
           padding: 14px 16px 12px; background: var(--ttsc-surface);
           border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-surface);
           box-shadow: var(--ttsc-shadow-sm); }
.s4 { grid-column: span 4; } .s6 { grid-column: span 6; }
.s8 { grid-column: span 8; } .s12 { grid-column: span 12; }
.ck-note { margin-top: auto; padding-top: 6px; font-size: 11px; line-height: 16px; color: var(--ttsc-text-muted); }
.ck-legend { display: flex; flex-wrap: wrap; gap: 6px 14px; margin: 6px 0 0;
             font-size: 11px; color: var(--ttsc-text-2); }
.ck-legend i { width: 8px; height: 8px; border-radius: var(--ttsc-radius-pill); background: var(--c); }

/* Apex nos tokens (os dois temas) */
.apexcharts-tooltip.apexcharts-theme-light,
.apexcharts-tooltip.apexcharts-theme-dark {
  background: var(--ttsc-surface) !important; color: var(--ttsc-text) !important;
  border: 1px solid var(--ttsc-border) !important; box-shadow: var(--ttsc-shadow-popover) !important;
  border-radius: var(--ttsc-radius-sm) !important; padding: 9px 11px !important;
}
.apexcharts-legend-text { color: var(--ttsc-text-2) !important; font-size: 11px !important; }
.apexcharts-xaxistooltip, .apexcharts-yaxistooltip {
  background: var(--ttsc-surface) !important; border-color: var(--ttsc-border) !important;
  color: var(--ttsc-text) !important;
}

@media (max-width: 1024px) { .s4 { grid-column: span 6; } .s6, .s8, .s12 { grid-column: span 12; } }
@media (max-width: 640px)  { .s4, .s6, .s8, .s12 { grid-column: span 12; } .ck { padding: 12px; gap: 10px; } }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .001ms !important; transition-duration: .001ms !important; }
}
```

### JS

```js
// assets/js/core/ttsc.chart-kit.js — requer ApexCharts 8.5.0 íntegro
(function () {
  'use strict';
  var RM = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function token(name) { /* lê --ttsc-* e converte oklch → hex, como no preview */ }
  function base() { /* fontFamily, foreColor, background transparent, toolbar/zoom off,
                       animations { enabled: !RM, speed: 380 }, locale pt-br inline */ }

  var BUILDERS = { barBasic: buildBarBasic, barRanked: buildBarRanked, /* … 25 famílias … */ };
  var REG = [];

  function mount(family, el, data, opts) {
    if (!el) return null;
    var entry = { charts: [] };
    entry.rebuild = function () { entry.charts = BUILDERS[family](el, data, opts); };
    entry.rebuild();
    REG.push(entry);
    return entry;
  }

  // Exemplo de família: dumbbell (rangeBar fino + pontos via linha com marcadores).
  // Nota (histórico da 4.7.0): scatter em combo com rangeBar não renderizava; os dois
  // pontos são séries de linha com stroke 0 e marcadores (mesmo desenho) — valide na 8.5.0 antes de trocar.
  function buildDumbbell(el, d) {
    var C = readTokens(), b = base();
    var chart = new ApexCharts(el, Object.assign({}, b, {
      chart: Object.assign({}, b.chart, { type: 'bar', height: 200 }),
      series: [
        { name: 'Variação', type: 'rangeBar',
          data: d.unidades.map(function (u, i) { return { x: u, y: d.pares[i] }; }) },
        { name: '2025', type: 'line', data: d.pares.map(function (p, i) { return { x: d.unidades[i], y: p[0] }; }) },
        { name: '2026', type: 'line', data: d.pares.map(function (p, i) { return { x: d.unidades[i], y: p[1] }; }) }
      ],
      colors: [C.borderStrong, C.muted, C.accent],
      plotOptions: { bar: { horizontal: false, columnWidth: '6%', borderRadius: 2 } },
      stroke: { width: [0, 0, 0] },
      markers: { size: [0, 7, 7], colors: [C.borderStrong, C.muted, C.accent],
                 strokeWidth: 2, strokeColors: C.surface, hover: { size: 9 } },
      tooltip: Object.assign({}, b.tooltip, { custom: function (ctx) {
        var i = ctx.dataPointIndex, p = d.pares[i], delta = (p[1] - p[0]) / p[0] * 100;
        return '<div class="ck-tip"><div class="ck-tip-t">' + d.unidades[i] + '</div>' +
          '<div class="ck-tip-r"><span>2025</span><b>' + p[0] + '</b></div>' +
          '<div class="ck-tip-r"><span>2026</span><b>' + p[1] + '</b></div>' +
          '<div class="ck-tip-r"><span>Δ</span><b>' + (delta >= 0 ? '+' : '−') +
          new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 1 }).format(Math.abs(delta)) + '%</b></div></div>';
      } })
    }));
    chart.render();
    return [chart];
  }

  var API = window.TTSCChartKit = {
    init: function (root) {
      root = root || document;
      mount('dumbbell', root.querySelector('#ck-dumbbell'), DUMBELL_DATA);
      /* … as demais 24 famílias … */
      return API;
    },
    updateTheme: function () {
      REG.forEach(function (e) { e.charts.forEach(function (c) { try { c.destroy(); } catch (x) {} }); });
      REG.forEach(function (e) { e.rebuild(); });
      return API;
    },
    destroy: function () {
      REG.forEach(function (e) { e.charts.forEach(function (c) { try { c.destroy(); } catch (x) {} }); });
      REG.length = 0;
      return API;
    }
  };

  new MutationObserver(function () { API.updateTheme(); })
    .observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme', 'class'] });
})();
```

No preview, `TTSCChartKit.init()` monta os 28 gráficos (25 cards + 3 roscas + 3 sparklines) e os dados vêm embutidos; em produção, prefira `data-chart` no container e `TTSC.init()` antes da fábrica.
### SQL

As três consultas alimentam os modelos 8, 14 e 19 a partir de tabelas reais do repo, no padrão MariaDB 10.11 / MySQL 8 (`uuid char(36)`, `deleted_at` quando a tabela tem, parâmetros nomeados `:param`, prepared statements). Todas são ilustrativas para efeito de layout: os números do preview são determinísticos, não vindos de banco.

Dumbbell (8): receita por unidade em dois anos, a partir de `organization_metrics` (snapshot diário) e `organization_units` — tabelas reais do módulo organizacional; o recorte de tenant é o banco/conexão do tenant (elas não têm `deleted_at`; a exclusão lógica não se aplica a snapshots):

```sql
-- Endpoints do dumbbell: total anual por unidade no ano base e no ano atual
SELECT u.name AS unidade,
       SUM(CASE WHEN YEAR(m.metric_date) = :ano_base  THEN m.revenue_total ELSE 0 END) AS receita_base,
       SUM(CASE WHEN YEAR(m.metric_date) = :ano_atual THEN m.revenue_total ELSE 0 END) AS receita_atual,
       ROUND(100 * (SUM(CASE WHEN YEAR(m.metric_date) = :ano_atual THEN m.revenue_total ELSE 0 END)
                  - SUM(CASE WHEN YEAR(m.metric_date) = :ano_base  THEN m.revenue_total ELSE 0 END))
             / NULLIF(SUM(CASE WHEN YEAR(m.metric_date) = :ano_base THEN m.revenue_total ELSE 0 END), 0), 1) AS delta_pct
  FROM organization_metrics m
  JOIN organization_units u ON u.uuid = m.unit_uuid
 WHERE m.metric_date >= MAKEDATE(:ano_base, 1)
   AND m.metric_date <  MAKEDATE(:ano_atual + 1, 1)
   AND u.status = 'active'
   AND m.unit_uuid IS NOT NULL
 GROUP BY u.name
 ORDER BY receita_atual DESC;
-- Para o pior e o melhor mês de cada unidade no lugar dos totais anuais, troque os
-- SUM(CASE …) por MIN(CASE …) e MAX(CASE …) sobre o mesmo recorte de datas.
```

Step line (14): saldo acumulado por dia com função de janela, a partir de `financial_transactions` — tabela real do módulo financeiro (não tem `deleted_at`; a integridade vem da conciliação, `reconciled = 1`):

```sql
-- Saldo acumulado por dia (window function, MariaDB 10.11 / MySQL 8)
WITH lancamentos AS (
  SELECT t.transaction_date AS dia,
         SUM(CASE WHEN t.type = 'credit' THEN t.amount
                  WHEN t.type = 'debit'  THEN -t.amount
                  ELSE 0 END)           AS movimento
    FROM financial_transactions t
   WHERE t.transaction_date >= :inicio
     AND t.transaction_date <  :fim
     AND t.reconciled = 1
     -- AND t.bank_account_id = :conta_id  -- opcional: uma conta por vez
   GROUP BY t.transaction_date
)
SELECT dia,
       movimento,
       SUM(movimento) OVER (ORDER BY dia
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS saldo_acumulado
  FROM lancamentos
 ORDER BY dia;
```

Multi-donut (19): contagem por turno e status, a partir de `enrollments` — tabela real com `deleted_at`, `period_uuid` e o enum `shift` (`morning`, `afternoon`, `evening`, `night`, `online`); o PHP mapeia os enums para os rótulos (Manhã/Tarde/Noite e Ativas/Trancadas/Transferidas):

```sql
-- Matrículas por turno e status para as três roscas
SELECT e.shift   AS turno,
       e.status  AS status,
       COUNT(*)  AS matriculas
  FROM enrollments e
 WHERE e.deleted_at IS NULL
   AND e.period_uuid = :periodo_uuid
   AND e.shift IN ('morning', 'afternoon', 'evening')
   AND e.status IN ('active', 'locked', 'transferred')
 GROUP BY e.shift, e.status
 ORDER BY FIELD(e.shift, 'morning', 'afternoon', 'evening'), matriculas DESC;
```

Para o scatter (21), a mesma lógica sai de `academic_assessment_scores` (nota por aluno) somada a `attendance` (frequência); `attendance` não tem `deleted_at` — o recorte é por `lesson_date`.

## Faça / Não faça

- **Faça:** escolher grade e legenda por card e explicar a escolha na nota — a galeria existe para tornar essa decisão explícita.
- **Faça:** reler os tokens em cada `updateTheme()` e re-renderizar; cores de gráfico não são literal em lugar nenhum.
- **Faça:** rótulo interno com contraste via `onColor` (`ttsc-primary-950` sobre claro, `ttsc-primary-50` sobre escuro) — nunca cinza sobre verde.
- **Faça:** costurar realizado e previsto com um ponto em comum e `stroke.dashArray` no trecho da projeção.
- **Faça:** meta sempre com rótulo textual (“Meta 85”), mesmo quando há linha de anotação.
- **Faça:** manter o `aria-label` em frases com extremos e tendência, não apenas “gráfico de barras”.
- **Faça:** numerar os cards (chip 1–41) e referenciar os números no mapa de decisão — os números são estáveis entre versões.
- **Não faça:** usar eixo duplo (16, 36) para variáveis sem relação — a sobreposição engana.
- **Não faça:** truncar o eixo sem declarar na nota (13 declara “inicia em 400”).
- **Não faça:** empilhar 100% (5) quando o volume absoluto importa — o leitor perde a escala.
- **Não faça:** confiar nos rótulos nativos do treemap em tiles estreitos — use a camada HTML sincronizada (20).
- **Não faça:** deixar a legenda Apex em coluna — o `bundle.css` força `column`; sobrescreva para `row`.
- **Não faça:** usar série `scatter` em combo com `rangeBar` (dumbbell) sem validar: na 4.7.0 os pontos silenciavam — o workaround com linha de `stroke.width: 0` e marcadores é histórico e segue funcionando; teste o scatter na 8.5.0 antes de trocar.
- **Não faça:** apressar a migração dos SVGs puros (33, 34, 37, 38) para os tipos nativos da 8.5.0 (`funnel`, `pyramid`, `sunburst`, `waffle`): os modelos do kit são determinísticos, navegáveis por teclado (sunburst) e independentes da lib — migre só quando fizer sentido.
- **Não faça:** animar com `speed` alto; 380 ms é o máximo daqui para cima o dashboard parece lento.
