# GeoMap

Mapa do Brasil por unidade federativa para leitura de operação: volume de entregas ou SLA, hubs que concentram a rede, rotas ativas, filtros por região e ranking textual. O contorno é um SVG embutido — sem amCharts, sem tiles e sem requisição externa.

O componente ocupa 1280 px e 702 px de altura no preview. O mapa usa projeção equirretangular e `viewBox="-4 -4 668 664.5"`; o painel de 340 px vira uma faixa abaixo do mapa em telas menores que 900 px.

## Quando usar

Use o GeoMap quando a pergunta é “onde a operação acontece e como está a qualidade por estado?”. Ele funciona bem para uma visão nacional de cobertura, entregas, SLA, hubs e regiões — o tipo de leitura que antecede a abertura de uma tabela ou de um detalhe operacional.

É o componente certo para:

- acompanhar a cobertura nacional de entregas, instalações ou atendimentos por UF;
- comparar volume e SLA entre regiões sem trocar de tela;
- mostrar onde estão os hubs e quais estados cada um atende;
- abrir um painel executivo ou de logística com ranking e resumo;
- apresentar um recorte regional para diretoria, operação ou comercial.

Não use quando:

- a pergunta é sobre um endereço, uma rota ponto a ponto ou um CEP — use um mapa de rotas ou uma tabela de endereços;
- os dados estão no nível de município, bairro ou escola — agregue por UF antes de enviar, ou use [DataTable](../DataTable/README.md);
- há apenas dois ou três itens para comparar — use [RankedBars](../RankedBars/README.md), que deixa a comparação mais direta;
- a leitura principal é uma série temporal — use [AmCharts](../AmCharts/README.md) ou [ApexCharts](../ApexCharts/README.md);
- o objetivo é ocupar salas, mesas ou leitos — use [UnitGrid](../UnitGrid/README.md);
- a métrica é uma matriz de duas dimensões — use [HeatmapMatrix](../HeatmapMatrix/README.md);
- o número precisa ser auditado linha a linha — o mapa é uma visão agregada; a fonte de verdade fica na tabela.

Componentes próximos: [RankedBars](../RankedBars/README.md) para o ranking sozinho, [KpiView](../KpiView/README.md) para o resumo em cartões, [DataTable](../DataTable/README.md) para a lista de unidades e entregas, [WidgetEntityMap](../WidgetEntityMap/README.md) para uma visão proporcional por entidade e [AmCharts](../AmCharts/README.md) para os demais gráficos.

## Anatomia

```
┌ Mapa de operações ───────────────────────────────────────────────┐
│ ✦ Operações · Outubro de 2026                        (Volume)(SLA)│
│ Mapa de operações                                                │
│ Entregas por estado no mês corrente, com hubs, rotas e filtros.   │
│                                                                  │
│ (Todas 27) (Sudeste 4) (Sul 3) (Nordeste 9) (Centro-Oeste 4) …   │
│                                                                  │
│ ┌ Volume por estado          27 UFs · 94,1% SLA ──────────────┐  │
│ │                                                            │  │
│ │                    [ mapa do Brasil ]                      │  │
│ │             ● hub      - - - rota      ● hub               │  │
│ │                                                            │  │
│ │ 7 hubs · 3 rotas ativas · dados ilustrativos               │  │
│ │ Contorno: amCharts geodata (BrazilLow)                     │  │
│ └────────────────────────────────────────────────────────────┘  │
│ ┌ Resumo e ranking ───────────────────────────────────────────┐  │
│ │ Resumo e ranking                              Brasil         │  │
│ │ Em trânsito · rede nacional                                 │  │
│ │ 1.842 entregas                                              │  │
│ │ 27 UFs · 9.045 entregas no mês                              │  │
│ │ Intensidade de volume                        entregas/mês   │  │
│ │ ■ Até 99     ■ 100 a 299     ■ 300 a 599     ■ 600 ou mais  │  │
│ │ Maiores volumes                                  5 UFs      │  │
│ │ 1 São Paulo SP        2.140  █████████████████████████      │  │
│ │ 2 Rio de Janeiro RJ   1.180  ██████████████                 │  │
│ │ 3 Minas Gerais MG       860  ██████████                     │  │
│ │ …                                                           │  │
│ │ ● Atualizado há 2 min                         Ver Brasil     │  │
│ └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

| Parte | Classe ou atributo | Obrigatório | Função |
|---|---|---|---|
| Raiz | `section.card.gm-card[data-ttsc-geomap]` | Sim | Delimita o componente; `render(el, data)` adiciona o atributo e o namespace. |
| Cabeçalho | `.gm-head`, `.gm-title-wrap`, `.gm-icon` | Sim | Ícone, sobrancelha, título e subtítulo. |
| Título | `.gm-title` (`#gm-title`) | Sim | Nome acessível da seção. |
| Métrica | `.seg` > `button[data-metric]` | Sim | Alterna “Volume” e “SLA” com `aria-pressed`. |
| Filtros | `.chips` > `.chip[data-region]` | Sim | Recorte por região; inclui “Todas” e a contagem de UFs. |
| Dica | `.toolbar-hint` | Não | Instrução curta; some abaixo de 1100 px para não competir com os chips. |
| Corpo | `.gm-body` | Sim | Grid `minmax(0, 1fr) 340px`; empilha abaixo de 900 px. |
| Coluna do mapa | `.gm-mapcol` | Sim | Fundo com grade sutil, cabeçalho, SVG e rodapé. |
| Cabeçalho do mapa | `.map-head`, `.map-title`, `.map-hint`, `.map-stats` | Sim | Métrica ativa, instrução de uso e cobertura/SLA do recorte. |
| SVG | `.gm-map` | Sim | `viewBox="-4 -4 668 664.5"`, `role="group"`, `aria-labelledby` para título e descrição. |
| Estados | `path.uf[data-uf]` | Sim | 27 contornos; carrega nome, região, volume, SLA, unidades e nível. |
| Rótulos | `.uf-label` | Não | Siglas visuais; são `aria-hidden` porque cada path já tem `aria-label`. |
| Rotas | `.gm-routes` | Não | Três curvas tracejadas entre hubs; puramente ilustrativas. |
| Hubs | `g.hub[data-hub]` | Sim | Sete pontos clicáveis com `role="button"`, `aria-pressed` e anel de foco. |
| Tooltip | `.gm-tip` | Sim | Cartão flutuante no hover e no foco; `aria-hidden` e sem captura de ponteiro. |
| Painel | `.gm-panel` | Sim | Resumo, legenda e ranking ao lado do mapa. |
| Resumo | `.summary` | Sim | “Em trânsito”, total do recorte e meta com UFs e entregas do mês. |
| Legenda | `.legend[data-legend]` | Sim | Faixas de volume ou de SLA; uma lista por métrica. |
| Ranking | `.rank` (`ol`) | Sim | Top 5 em texto, com posição, UF, valor e barra proporcional. |
| Limpar | `#gm-clear` | Não | “Ver Brasil” quando há um hub selecionado. |
| Rodapé | `.map-foot` | Não | Contagem de hubs/rotas e atribuição do contorno. |
| Anúncio | `#gm-live` (`aria-live`) | Sim | Anuncia mudança de métrica, região e hub. |

O SVG é desenhado com coordenadas fixas a partir de `assets/vendors/amcharts5/geodata/brazilLow.js` e não carrega a biblioteca amCharts em tempo de execução. O grupo `.gm-states` contém os 27 paths; `.gm-uf-labels` repete as siglas em texto para leitura rápida; `.gm-hubs` fica por cima dos estados para receber o clique. A ordem de pintura é rotas → estados → rótulos → hubs.

## Variantes

| Variante | Como aplicar | Uso |
|---|---|---|
| Mapa de volume (padrão do preview) | `metric: 'volume'`; quatro faixas de verde do acento. | Magnitude de entregas, instalações ou atendimentos no período. |
| Mapa de SLA | `metric: 'sla'`; três faixas verde, âmbar e vermelho. | Qualidade da operação; o ranking passa a mostrar os menores SLA. |
| Recorte regional | `region: 'Sudeste'` (ou Sul, Nordeste, Centro-Oeste, Norte); estados de fora ficam esmaecidos. | Reunião de regional, meta por praça, comparação de cobertura. |
| Hub em foco | `select('SP')`; o hub fica selecionado, os estados atendidos ganham contorno e o painel abre o detalhe. | Entender a área de influência de um hub sem sair do mapa. |
| Compacto | Esconda `.map-foot` e `.toolbar-hint`, reduza o painel para 300 px e mantenha legenda e ranking. | Dashboard com vários cards; o mapa continua legível em 600 px. |
| Somente leitura | `pointer-events: none` em `.uf` e `.hub`, `aria-disabled="true"` nos controles; mantenha o painel. | Impressão, exportação em PDF ou conferência de um recorte já fechado. |

O hub selecionado não é uma variante de layout: ele é um estado de seleção. Ao selecionar um hub, o filtro de região volta para “Todas” para que os estados atendidos não fiquem esmaecidos; ao escolher uma região, o hub é limpo. As duas ações são exclusivas.

## Estados

| Estado | Como aparece | Regra |
|---|---|---|
| Padrão | Volume, filtro “Todas”, nenhum hub selecionado, resumo nacional. | Estado inicial do preview. |
| Volume | Quatro tons de verde do acento; legenda “Até 99”, “100 a 299”, “300 a 599”, “600 ou mais”. | `levelVolume`: 1 a 4. |
| SLA | Verde para 95% ou mais, âmbar para 91% a 94,9%, vermelho abaixo de 91%. | `levelSla`: 1 a 3; o texto “Bom/Atenção/Crítico” acompanha a cor. |
| Região | Estados de fora com `opacity: .2`, fora da ordem de Tab e com `aria-hidden`. | O ranking e o resumo passam a considerar só a região. |
| Hub | `aria-pressed="true"`, anel visível, estados atendidos com contorno; painel com “Em trânsito · hub …”. | `select(id)`; o filtro de região é zerado. |
| Tooltip | Abre no hover e no foco; mostra nome, UF, unidades, entregas e SLA. | Some com `mouseleave`, `blur`, `Esc` ou rolagem. |
| Foco | Contorno de 2 px no chip/botão; UF com traço de 2,2 px; hub com anel e ponto reforçados. | Nunca dependa só da cor para indicar o item ativo. |
| Sem dados | UF em `--ttsc-surface-2`, rótulo “Sem operação” e tooltip “Sem entregas no período”. | Não pinte zero como se fosse volume baixo; use `data-empty="true"`. |
| Carregando | Esqueleto na área do mapa, `aria-busy="true"` na raiz e painel com “Carregando…”. | Preserve a altura para evitar salto de layout. |
| Erro | Faixa `role="alert"` acima do mapa com “Não foi possível carregar o mapa” e “Tentar novamente”. | Mantenha o último recorte visível, se houver. |
| Atualização | “Atualizado há 2 min” no rodapé do painel; `title` com a data e hora absolutas. | Não use “agora” para dados com mais de cinco minutos. |
| Movimento reduzido | Pulsação dos hubs vira opacidade estática; transições caem para 0,001 ms. | Respeite `prefers-reduced-motion`. |
| Estreito | Abaixo de 900 px o painel desce; abaixo de 640 px a dica do mapa some. | Em 480 px os chips rolam na horizontal e o SVG mantém a proporção. |

O preview usa dados ilustrativos e todos os estados têm operação. Os estados “Sem dados”, “Carregando” e “Erro” são o contrato recomendado para a versão de produção; eles não substituem o painel textual.

## Acessibilidade

- **Estrutura:** o SVG é um `role="group"` com `<title>` e `<desc>`; cada UF é um `role="img"` com `aria-label` completo (“São Paulo (SP), Sudeste: 2.140 entregas, SLA de 96,4%, 9 unidades”). Os rótulos visuais são `aria-hidden` para não duplicar a leitura.
- **Hubs:** cada hub é um `role="button"` com `aria-pressed`; Enter e Espaço selecionam, Escape fecha o tooltip. O anel de foco é visível e o alvo transparente tem 28 px de diâmetro, maior que o ponto pintado.
- **Filtros:** os chips são botões com `aria-pressed`; a métrica usa o mesmo padrão. A troca é anunciada em `#gm-live` (`aria-live="polite"`), não apenas pela cor.
- **Painel textual:** o resumo, a legenda e o ranking em `<ol>` são a alternativa para quem não percorre o SVG. O ranking traz posição, nome, UF e valor; a barra é decorativa.
- **Tooltip:** aparece no hover e no foco, mas não recebe foco nem captura o ponteiro; a informação também está no `aria-label` e no painel. `Esc` e a saída do foco fecham o cartão.
- **Recorte:** ao filtrar uma região, os estados esmaecidos saem da ordem de Tab e recebem `aria-hidden`; os hubs de outras regiões fazem o mesmo. O foco não fica preso em um item invisível.
- **Contraste:** os preenchimentos usam `color-mix` sobre a superfície e os rótulos têm halo de 2,4 px; ainda assim, a cor nunca é o único canal — há legenda, texto de faixa e ranking.
- **Números:** `toLocaleString('pt-BR')` para milhares e uma casa decimal para SLA. O leitor de tela ouve “1.842 entregas”, não “1842”.
- **Toque:** chips têm 27 px de altura; hubs têm área de 28 px; o botão “Ver Brasil” fica no rodapé do painel, com rótulo explícito. Em telas pequenas, o painel abaixo do mapa evita alvos sobrepostos.
- **Movimento:** a pulsação é lenta e para com `prefers-reduced-motion`; nenhuma informação depende da animação.
- **Ordem de leitura:** título → métrica → filtros → mapa (UFs e hubs) → painel (resumo, legenda, ranking, atualização). No mobile, o painel vem depois do mapa, como na ordem visual.

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Use volume para magnitude e SLA para qualidade, com legendas distintas. | Misturar as duas escalas na mesma cor ou no mesmo gradiente. |
| Mantenha o ranking e o resumo como leitura textual do mapa. | Deixar a informação apenas no tooltip ou na cor do estado. |
| Calcule os agregados no servidor e envie um valor por UF. | Somar entregas ou calcular SLA no navegador a partir de linhas cruas. |
| Compare períodos completos e iguais. | Colocar um mês parcial ao lado de um mês fechado sem aviso. |
| Trate UF sem operação como “Sem dados”, com texto próprio. | Pintar zero com a cor mais clara e chamar de “volume baixo”. |
| Preserve o foco e anuncie a mudança de métrica, região ou hub. | Recriar o SVG inteiro a cada clique e perder o foco do teclado. |
| Use o filtro de região e o hub para recortes simples. | Transformar o mapa em uma tabela de 27 linhas com dezenas de ações. |
| Repita a atribuição “Contorno: amCharts geodata (BrazilLow)”. | Apresentar o contorno como mapa oficial do IBGE. |
| Formate números e percentuais em pt-BR. | Usar ponto decimal ou “1,842” em textos e tooltips. |
| Deixe claro que os dados são ilustrativos no preview. | Publicar o card de demonstração como se fosse dado de produção. |

## API

Namespace global: `window.TTSCGeoMap`. O preview roda uma instância embutida com dados ilustrativos; o contrato abaixo é o do módulo em `assets/js/core/ttsc.geomap.js`.

```js
const mapa = TTSCGeoMap.render(document.querySelector('[data-ttsc-geomap]'), {
  metric: 'volume',
  region: 'Todas',
  states: estados,
  hubs: hubs,
  transit: { Todas: 1842, Sudeste: 812, Sul: 396, Nordeste: 302, 'Centro-Oeste': 164, Norte: 168 },
  updatedAt: 'há 2 min',
  attribution: 'Contorno: amCharts geodata (BrazilLow)'
});

mapa.setMetric('sla');
mapa.setRegion('Sudeste');
mapa.select('SP'); // abre o hub e volta o recorte para “Todas”
```

| Opção | Tipo | Padrão | Função |
|---|---|---|---|
| `states` | array | obrigatório | Um item por UF: `{uf, name, region, units, deliveries, sla}`. |
| `hubs` | array | `[]` | `{id, name, region, x, y, deliveries, sla, transit, states}`; `x` e `y` no `viewBox`. |
| `metric` | string | `'volume'` | `volume` ou `sla`. |
| `region` | string | `'Todas'` | `Todas`, `Sudeste`, `Sul`, `Nordeste`, `Centro-Oeste` ou `Norte`. |
| `transit` | object | `{}` | Entregas em trânsito por recorte, incluindo `Todas`. |
| `updatedAt` | string | `'agora'` | Texto relativo exibido no rodapé do painel. |
| `attribution` | string | `'Contorno: amCharts geodata (BrazilLow)'` | Crédito do contorno no rodapé do mapa. |
| `animate` | boolean | `true` | Liga a pulsação dos hubs; sempre desligada em `prefers-reduced-motion`. |
| `onSelect` | function | `null` | Atalho para o evento `geomap:select`; recebe `{hub}`. |

Formato dos dados:

```js
{
  states: [
    { uf: 'SP', name: 'São Paulo', region: 'Sudeste', units: 9, deliveries: 2140, sla: 96.4 }
  ],
  hubs: [
    {
      id: 'SP', name: 'São Paulo', region: 'Sudeste',
      x: 446.7, y: 484.9,
      deliveries: 1284, sla: 96.8, transit: 214,
      states: ['SP', 'MG', 'MS', 'PR', 'SC']
    }
  ]
}
```

A geometria e as posições dos rótulos ficam no módulo (`assets/js/core/ttsc.geomap.paths.js`), geradas a partir de `brazilLow.js`: cada UF aponta para `{d, label:[x, y, fontSize]}`. O payload não carrega `d` nem coordenadas de UF; carrega apenas valores e os hubs.

Métodos da instância:

| Método | Retorno | Função |
|---|---|---|
| `setMetric(metric)` | instância | Troca `volume`/`sla`, atualiza legenda, ranking e painel. |
| `setRegion(region)` | instância | Filtra a região e limpa o hub selecionado. |
| `select(id)` | instância | Seleciona um hub (`'SP'`) ou limpa com `null`; zera o filtro de região. |
| `getState()` | objeto | `{metric, region, hub}` do recorte atual. |
| `setData(data)` | instância | Substitui os dados, remonta estados/hubs e preserva o recorte quando possível. |
| `on(event, handler)` | função | Assina um evento; devolve a função de cancelamento. |
| `destroy()` | void | Remove listeners e devolve o DOM ao estado inicial. |

Eventos: `geomap:ready`, `geomap:metric` (`{metric}`), `geomap:region` (`{region}`), `geomap:select` (`{hub}`), `geomap:hover` (`{uf, hub}`). Todos borbulham a partir da raiz e são disparados depois da atualização visual.

Atributos `data-*` no HTML: `data-ttsc-geomap`, `data-metric`, `data-region`, `data-updated-at`, `data-source` (JSON opcional) e `data-attribution`. Não edite os `data-*` dos paths à mão: eles são gerados no `render` e servem para o tooltip e o anúncio.

## Modelos

### HTML

```html
<section class="card gm-card" data-ttsc-geomap
         data-source="<?= $this->e($mapUrl) ?>"
         data-metric="volume" data-region="Todas"
         data-updated-at="<?= $this->e($updatedAt) ?>"
         aria-labelledby="mapa-titulo">
  <header class="gm-head">
    <div class="gm-title-wrap">
      <span class="gm-icon" aria-hidden="true"><i class="fa-light fa-map-location-dot"></i></span>
      <div>
        <p class="gm-eyebrow"><span class="live" aria-hidden="true"></span>Operações · <?= $this->e($periodLabel) ?></p>
        <h2 class="gm-title" id="mapa-titulo">Mapa de operações</h2>
        <p class="gm-sub">Entregas por estado no mês corrente, com hubs, rotas ativas e filtros por região.</p>
      </div>
    </div>
    <div class="seg" role="group" aria-label="Métrica do mapa">
      <button type="button" data-metric="volume" aria-pressed="true">Volume</button>
      <button type="button" data-metric="sla" aria-pressed="false">SLA</button>
    </div>
  </header>

  <div class="gm-toolbar">
    <div class="chips" role="group" aria-label="Filtrar por região">
      <button type="button" class="chip" data-region="Todas" aria-pressed="true">Todas <span class="n">27</span></button>
      <?php foreach ($regions as $region): ?>
        <button type="button" class="chip" data-region="<?= $this->e($region['name']) ?>" aria-pressed="false">
          <?= $this->e($region['name']) ?> <span class="n"><?= (int) $region['total'] ?></span>
        </button>
      <?php endforeach; ?>
    </div>
    <p class="toolbar-hint"><i class="fa-light fa-circle-info" aria-hidden="true"></i> Selecione um hub no mapa para abrir o detalhe.</p>
  </div>

  <div class="gm-body">
    <div class="gm-mapcol">
      <div class="map-head">
        <div class="map-head-l">
          <span class="map-title" id="mapa-metrica" data-geo-metric>Volume por estado</span>
          <span class="map-hint"><i class="fa-light fa-hand-pointer" aria-hidden="true"></i> Passe o cursor ou navegue com Tab</span>
        </div>
        <div class="map-stats">
          <span><strong data-geo-count>27</strong> UFs cobertas</span>
          <span class="sep" aria-hidden="true"></span>
          <span><strong data-geo-sla>94,1%</strong> SLA médio</span>
        </div>
      </div>

      <div class="map-wrap" data-geo-wrap>
        <svg class="gm-map" viewBox="-4 -4 668 664.5" role="group"
             aria-labelledby="mapa-svg-titulo mapa-svg-desc"
             data-metric="volume" preserveAspectRatio="xMidYMid meet">
          <title id="mapa-svg-titulo">Mapa de operações por estado</title>
          <desc id="mapa-svg-desc">Mapa do Brasil com os 27 estados, preenchidos por volume de entregas, sete hubs pulsantes e três rotas ativas. Use Tab para percorrer estados e hubs; o painel ao lado traz o ranking como alternativa em texto.</desc>
          <g class="gm-routes" aria-hidden="true"></g>
          <g class="gm-states" data-geo-states></g>
          <g class="gm-uf-labels" aria-hidden="true" data-geo-labels></g>
          <g class="gm-hubs" data-geo-hubs></g>
        </svg>
        <div class="gm-tip" data-geo-tip aria-hidden="true" hidden></div>
      </div>

      <div class="map-foot">
        <span><i class="fa-light fa-circle-nodes" aria-hidden="true"></i> 7 hubs · 3 rotas ativas · dados ilustrativos</span>
        <span data-geo-attribution>Contorno: amCharts geodata (BrazilLow)</span>
      </div>
    </div>

    <aside class="gm-panel" aria-label="Resumo e ranking de operações">
      <div class="panel-head">
        <h3>Resumo e ranking</h3>
        <span class="scope" id="mapa-scope"><i class="fa-light fa-earth-americas" aria-hidden="true"></i><span data-geo-scope>Brasil</span></span>
      </div>

      <div class="summary">
        <span class="sum-lbl" data-geo-sum-label>Em trânsito · rede nacional</span>
        <p class="sum-main"><strong data-geo-sum-value>1.842</strong><span>entregas</span></p>
        <p class="sum-meta" data-geo-sum-meta>27 UFs · 9.045 entregas no mês</p>
      </div>

      <div>
        <div class="block-h"><span data-geo-legend-title>Intensidade de volume</span><span class="note" data-geo-legend-note>entregas / mês</span></div>
        <ul class="legend" data-legend="volume">
          <li><i class="sw q1" aria-hidden="true"></i>Até 99</li>
          <li><i class="sw q2" aria-hidden="true"></i>100 a 299</li>
          <li><i class="sw q3" aria-hidden="true"></i>300 a 599</li>
          <li><i class="sw q4" aria-hidden="true"></i>600 ou mais</li>
        </ul>
        <ul class="legend" data-legend="sla" hidden>
          <li><i class="sw ok" aria-hidden="true"></i>Bom, 95% ou mais</li>
          <li><i class="sw warn" aria-hidden="true"></i>Atenção, 91% a 94,9%</li>
          <li><i class="sw crit" aria-hidden="true"></i>Crítico, abaixo de 91%</li>
        </ul>
      </div>

      <div class="rank-block">
        <div class="block-h"><span data-geo-rank-title>Maiores volumes</span><span class="note" data-geo-rank-note>5 UFs</span></div>
        <ol class="rank" data-geo-rank aria-label="Ranking de estados por volume de entregas"></ol>
      </div>

      <div class="panel-foot">
        <span class="live"><i aria-hidden="true"></i><span data-geo-updated>Atualizado há 2 min</span></span>
        <button type="button" class="link-btn" data-geo-clear hidden>Ver Brasil</button>
      </div>
    </aside>
  </div>

  <p class="sr-only" data-geo-live aria-live="polite"></p>
</section>
```

### CSS

```css
/* Contrato visual do GeoMap. Os tokens vêm de tokens.css. */
.gm-card{background:var(--ttsc-surface);border:1px solid var(--ttsc-border);border-radius:var(--ttsc-radius-surface);box-shadow:var(--ttsc-shadow-sm);padding:16px;min-width:0}
.gm-head{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:14px}
.gm-title-wrap{display:flex;align-items:center;gap:11px;min-width:0}
.gm-icon{width:36px;height:36px;flex-shrink:0;display:grid;place-items:center;border:1px solid var(--ttsc-accent-border);border-radius:11px;background:var(--ttsc-accent-soft);color:var(--ttsc-accent-text)}
.gm-eyebrow{display:flex;align-items:center;gap:6px;margin:0 0 3px;font-size:10px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--ttsc-text-muted)}
.gm-eyebrow .live{width:5px;height:5px;border-radius:50%;background:var(--ttsc-success)}
.gm-title{margin:0;font-size:17px;line-height:24px;font-weight:600;letter-spacing:-.01em;color:var(--ttsc-text)}
.gm-sub{margin:2px 0 0;font-size:12px;line-height:16px;color:var(--ttsc-text-muted)}

.seg{display:inline-flex;flex-shrink:0;padding:3px;gap:2px;border:1px solid var(--ttsc-border);border-radius:10px;background:var(--ttsc-canvas-2)}
.seg button{appearance:none;border:0;background:transparent;color:var(--ttsc-text-muted);font:inherit;font-size:11.5px;font-weight:600;padding:5px 14px;border-radius:7px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--ttsc-surface);color:var(--ttsc-text);box-shadow:0 1px 2px rgba(0,0,0,.10)}

.gm-toolbar{display:flex;align-items:center;gap:12px;min-width:0;margin-bottom:12px}
.chips{display:flex;align-items:center;gap:6px;min-width:0;overflow-x:auto;overflow-y:hidden;scrollbar-width:none;padding:1px}
.chips::-webkit-scrollbar{display:none}
.chip{display:inline-flex;align-items:center;gap:5px;flex-shrink:0;height:27px;padding:0 10px;border:1px solid var(--ttsc-border);border-radius:var(--ttsc-radius-pill);background:var(--ttsc-surface);color:var(--ttsc-text-2);font:inherit;font-size:11.5px;font-weight:500;cursor:pointer}
.chip[aria-pressed="true"]{background:var(--ttsc-accent-soft);border-color:var(--ttsc-accent-border);color:var(--ttsc-accent-text)}
.toolbar-hint{margin:0 0 0 auto;flex-shrink:0;font-size:10.5px;color:var(--ttsc-text-muted);white-space:nowrap}

.gm-body{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:14px;align-items:stretch}
.gm-mapcol{position:relative;display:flex;flex-direction:column;min-width:0;min-height:492px;padding:11px 12px 8px;border:1px solid var(--ttsc-border-soft);border-radius:14px;background-color:var(--ttsc-canvas-2);background-image:radial-gradient(ellipse 62% 58% at 50% 46%,color-mix(in srgb,var(--ttsc-accent) 9%,transparent),transparent 72%),radial-gradient(circle at 1px 1px,color-mix(in srgb,var(--ttsc-border-strong) 55%,transparent) 1px,transparent 0);background-size:auto,16px 16px}
.map-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;padding:0 2px;min-height:20px}
.map-title{font-size:11.5px;font-weight:600;line-height:16px;color:var(--ttsc-text-2)}
.map-hint{display:inline-flex;align-items:center;gap:5px;font-size:10px;color:var(--ttsc-text-muted)}
.map-stats{display:inline-flex;align-items:center;gap:8px;flex-shrink:0;font-size:10px;color:var(--ttsc-text-muted)}
.map-stats strong{font-weight:600;color:var(--ttsc-text);font-variant-numeric:tabular-nums}
.map-wrap{position:relative;flex:1;min-height:0;display:flex;align-items:center;justify-content:center;padding:2px 0}
.gm-map{display:block;width:100%;height:100%;max-height:440px;overflow:visible}
.map-foot{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:6px 2px 0;margin-top:2px;border-top:1px solid var(--ttsc-border-soft);font-size:10px;color:var(--ttsc-text-muted)}

.gm-card{--ttsc-geo-q1:color-mix(in srgb,var(--ttsc-accent) 12%,var(--ttsc-surface-2));--ttsc-geo-q2:color-mix(in srgb,var(--ttsc-accent) 30%,var(--ttsc-surface-2));--ttsc-geo-q3:color-mix(in srgb,var(--ttsc-accent) 52%,var(--ttsc-surface-2));--ttsc-geo-q4:color-mix(in srgb,var(--ttsc-accent) 78%,var(--ttsc-surface-2));--ttsc-geo-ok:color-mix(in srgb,var(--ttsc-success) 36%,var(--ttsc-surface-2));--ttsc-geo-warn:color-mix(in srgb,var(--ttsc-warning) 44%,var(--ttsc-surface-2));--ttsc-geo-crit:color-mix(in srgb,var(--ttsc-danger) 38%,var(--ttsc-surface-2))}
[data-theme="dark"] .gm-card,html.dark .gm-card{--ttsc-geo-q1:color-mix(in srgb,var(--ttsc-accent) 20%,var(--ttsc-surface-2));--ttsc-geo-q2:color-mix(in srgb,var(--ttsc-accent) 40%,var(--ttsc-surface-2));--ttsc-geo-q3:color-mix(in srgb,var(--ttsc-accent) 60%,var(--ttsc-surface-2));--ttsc-geo-q4:color-mix(in srgb,var(--ttsc-accent) 84%,var(--ttsc-surface-2));--ttsc-geo-ok:color-mix(in srgb,var(--ttsc-success) 48%,var(--ttsc-surface-2));--ttsc-geo-warn:color-mix(in srgb,var(--ttsc-warning) 55%,var(--ttsc-surface-2));--ttsc-geo-crit:color-mix(in srgb,var(--ttsc-danger) 48%,var(--ttsc-surface-2))}

.gm-states{filter:drop-shadow(0 5px 10px color-mix(in srgb,var(--ttsc-text) 9%,transparent))}
.uf{stroke:var(--ttsc-surface);stroke-width:1;stroke-linejoin:round;cursor:pointer;transition:opacity .18s ease,stroke .15s ease,filter .15s ease}
.gm-map[data-metric="volume"] .uf[data-level="1"]{fill:var(--ttsc-geo-q1)}
.gm-map[data-metric="volume"] .uf[data-level="2"]{fill:var(--ttsc-geo-q2)}
.gm-map[data-metric="volume"] .uf[data-level="3"]{fill:var(--ttsc-geo-q3)}
.gm-map[data-metric="volume"] .uf[data-level="4"]{fill:var(--ttsc-geo-q4)}
.gm-map[data-metric="sla"] .uf[data-level="1"]{fill:var(--ttsc-geo-ok)}
.gm-map[data-metric="sla"] .uf[data-level="2"]{fill:var(--ttsc-geo-warn)}
.gm-map[data-metric="sla"] .uf[data-level="3"]{fill:var(--ttsc-geo-crit)}
.uf:hover,.uf:focus-visible{stroke:var(--ttsc-accent-text);stroke-width:2.2;filter:brightness(1.05)}
.uf.is-dim{opacity:.2;pointer-events:none}
.uf.is-served{stroke:var(--ttsc-accent-text);stroke-width:2}
.uf-label{fill:var(--ttsc-text);font-weight:600;opacity:.78;pointer-events:none;paint-order:stroke;stroke:color-mix(in srgb,var(--ttsc-surface) 92%,transparent);stroke-width:2.4px;stroke-linejoin:round}

.hub{cursor:pointer;color:var(--ttsc-success)}
.hub.st-warn{color:var(--ttsc-warning)}.hub.st-crit{color:var(--ttsc-danger)}
.hub-hit{fill:transparent;pointer-events:all}
.hub-pulse{fill:currentColor;opacity:.2;transform-box:fill-box;transform-origin:center;animation:hubPulse 2.6s cubic-bezier(.4,0,.2,1) infinite}
.hub-dot{fill:currentColor;stroke:var(--ttsc-surface);stroke-width:1.6}
.hub-core{fill:var(--ttsc-surface);opacity:.9}
.hub-ring{fill:none;stroke:var(--ttsc-text);stroke-width:1.2;stroke-dasharray:2 3;opacity:0;transition:opacity .15s}
.hub.is-selected .hub-ring{opacity:.7}
.hub:hover .hub-dot,.hub:focus-visible .hub-dot{stroke:var(--ttsc-text);stroke-width:2.6}
.hub:focus-visible .hub-ring{opacity:.9;stroke:var(--ttsc-accent-text);stroke-width:2}
.hub.is-dim{opacity:.18;pointer-events:none}
.hub-label{pointer-events:none}
.hub-name{font-size:17px;font-weight:600;fill:var(--ttsc-text);paint-order:stroke;stroke:var(--ttsc-surface);stroke-width:3px;stroke-linejoin:round}
.hub-sub{display:none;font-size:13px;font-weight:500;fill:var(--ttsc-text-muted);paint-order:stroke;stroke:var(--ttsc-surface);stroke-width:2.6px;stroke-linejoin:round}
@keyframes hubPulse{0%{transform:scale(.55);opacity:.42}60%{transform:scale(1.55);opacity:0}100%{transform:scale(1.55);opacity:0}}
.gm-card.is-static .hub-pulse{animation:none;opacity:.16}

.gm-tip{position:absolute;z-index:5;min-width:196px;max-width:250px;padding:10px 12px;border:1px solid var(--ttsc-border);border-radius:10px;background:var(--ttsc-surface);box-shadow:var(--ttsc-shadow-md);pointer-events:none}
.gm-tip[hidden]{display:none}
.tip-top{display:flex;align-items:center;gap:6px;font-size:12.5px;font-weight:600;line-height:17px;color:var(--ttsc-text)}
.tip-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0;background:currentColor}
.tip-dot.ok{color:var(--ttsc-success)}.tip-dot.warn{color:var(--ttsc-warning)}.tip-dot.crit{color:var(--ttsc-danger)}
.tip-meta{margin:1px 0 7px;font-size:10px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--ttsc-text-muted)}
.tip-rows{display:grid;grid-template-columns:1fr auto;gap:3px 12px;padding-top:7px;border-top:1px solid var(--ttsc-border-soft);margin:0}
.tip-rows dt{font-size:11px;color:var(--ttsc-text-muted)}
.tip-rows dd{margin:0;font-size:11.5px;font-weight:600;text-align:right;font-variant-numeric:tabular-nums}

.gm-panel{display:flex;flex-direction:column;gap:11px;min-width:0;padding:13px 14px;border:1px solid var(--ttsc-border);border-radius:14px;background:var(--ttsc-surface)}
.panel-head{display:flex;align-items:center;justify-content:space-between;gap:8px}
.panel-head h3{margin:0;font-size:12.5px;font-weight:600;color:var(--ttsc-text)}
.scope{display:inline-flex;align-items:center;gap:5px;max-width:160px;padding:2px 8px;border:1px solid var(--ttsc-border);border-radius:var(--ttsc-radius-pill);background:var(--ttsc-canvas-2);font-size:10px;font-weight:600;color:var(--ttsc-text-2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.summary{position:relative;overflow:hidden;padding:10px 12px 10px 14px;border:1px solid var(--ttsc-border-soft);border-radius:11px;background:var(--ttsc-canvas-2)}
.summary::before{content:"";position:absolute;inset:0 auto 0 0;width:3px;background:var(--ttsc-accent)}
.sum-lbl{display:block;font-size:9.5px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--ttsc-text-muted)}
.sum-main{display:flex;align-items:baseline;gap:5px;margin:3px 0 0}
.sum-main strong{font-size:27px;line-height:30px;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.sum-meta{margin:2px 0 0;font-size:10.5px;color:var(--ttsc-text-muted)}
.block-h{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:6px}
.block-h span{font-size:10px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--ttsc-text-muted)}
.legend{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:5px 10px;margin:0;padding:0}
.legend[hidden]{display:none}
.legend li{display:flex;align-items:center;gap:6px;font-size:10.5px;color:var(--ttsc-text-2)}
.sw{width:10px;height:10px;border-radius:3px;flex-shrink:0;border:1px solid color-mix(in srgb,var(--ttsc-text) 10%,transparent)}
.sw.q1{background:var(--ttsc-geo-q1)}.sw.q2{background:var(--ttsc-geo-q2)}.sw.q3{background:var(--ttsc-geo-q3)}.sw.q4{background:var(--ttsc-geo-q4)}
.rank{list-style:none;margin:0;padding:0}
.rank-row{display:grid;grid-template-columns:15px minmax(0,1fr) auto;column-gap:7px;row-gap:4px;align-items:center;padding:5px 0 6px;border-bottom:1px solid var(--ttsc-border-soft)}
.rank-pos{font-size:10px;font-weight:600;color:var(--ttsc-text-muted);font-variant-numeric:tabular-nums}
.rank-name{display:flex;align-items:baseline;gap:5px;min-width:0;font-size:11.5px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rank-name small{font-size:9.5px;font-weight:600;color:var(--ttsc-text-muted)}
.rank-val{font-size:11.5px;font-weight:600;font-variant-numeric:tabular-nums}
.rank-bar{grid-column:1/-1;height:4px;border-radius:99px;background:var(--ttsc-surface-2);overflow:hidden}
.rank-bar i{display:block;height:100%;border-radius:99px;background:var(--ttsc-accent);min-width:4px}
.panel-foot{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:auto;padding-top:9px;border-top:1px solid var(--ttsc-border-soft);font-size:10px;color:var(--ttsc-text-muted)}
.link-btn{appearance:none;border:0;background:none;padding:0;font:inherit;font-size:10.5px;font-weight:600;color:var(--ttsc-accent-text);cursor:pointer;text-decoration:underline;text-underline-offset:2px}
.link-btn[hidden]{display:none}
@media (max-width:1100px){.gm-body{grid-template-columns:minmax(0,1fr) 320px}.toolbar-hint{display:none}}
@media (max-width:900px){.gm-body{grid-template-columns:minmax(0,1fr)}.gm-map{height:auto;max-height:none}.chips{-webkit-mask-image:linear-gradient(90deg,#000 calc(100% - 24px),transparent);mask-image:linear-gradient(90deg,#000 calc(100% - 24px),transparent);padding-right:24px}}
@media (max-width:640px){.gm-head{flex-wrap:wrap}.gm-sub{max-width:38ch}.map-hint{display:none}.map-foot{flex-wrap:wrap}}
@media (max-width:560px){.gm-title{font-size:16px}.legend{grid-template-columns:1fr}}
@media (prefers-reduced-motion:reduce){*{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important}.hub-pulse{opacity:.16}}
```

### JS

```js
// assets/js/core/ttsc.geomap.js — sem dependências.
(function (window, document) {
  'use strict';

  var GEO = window.TTSCGeoPaths || {};
  var instances = new WeakMap();

  function fmt(n) { return Number(n).toLocaleString('pt-BR'); }
  function pct(n) { return Number(n).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%'; }
  function level(metric, value) {
    if (metric === 'volume') return value >= 600 ? 4 : value >= 300 ? 3 : value >= 100 ? 2 : 1;
    return value >= 95 ? 1 : value >= 91 ? 2 : 3;
  }
  function tone(sla) { return sla >= 95 ? 'st-ok' : sla >= 91 ? 'st-warn' : 'st-crit'; }
  function word(sla) { return sla >= 95 ? 'Bom' : sla >= 91 ? 'Atenção' : 'Crítico'; }

  function GeoMap(el, data) {
    this.el = el;
    this.data = Object.assign({ states: [], hubs: [], transit: {}, updatedAt: 'agora', attribution: 'Contorno: amCharts geodata (BrazilLow)' }, data || {});
    this.state = { metric: this.data.metric || 'volume', region: this.data.region || 'Todas', hub: null };
    this.el.classList.toggle('is-static', this.data.animate === false);
    this.mount();
    this.bind();
    this.update();
  }

  GeoMap.prototype.q = function (selector) { return this.el.querySelector(selector); };
  GeoMap.prototype.qsa = function (selector) { return Array.prototype.slice.call(this.el.querySelectorAll(selector)); };

  GeoMap.prototype.mount = function () {
    this.q('[data-geo-states]').innerHTML = this.data.states.map(function (s) {
      return '<path class="uf" data-uf="' + s.uf + '" data-name="' + s.name + '" data-region="' + s.region +
        '" data-volume="' + s.deliveries + '" data-sla="' + s.sla + '" data-units="' + s.units +
        '" d="' + ((GEO[s.uf] && GEO[s.uf].d) || '') + '" tabindex="0" role="img" aria-label="' + s.name + ' (' + s.uf + '), ' +
        s.region + ': ' + fmt(s.deliveries) + ' entregas, SLA de ' + pct(s.sla) + ', ' + s.units + ' unidades."/>';
    }).join('');

    this.q('[data-geo-labels]').innerHTML = this.data.states.map(function (s) {
      var geometry = GEO[s.uf];
      if (!geometry || !geometry.label) return '';
      return '<text class="uf-label" data-uf="' + s.uf + '" x="' + geometry.label[0] + '" y="' + geometry.label[1] +
        '" style="font-size:' + geometry.label[2] + 'px">' + s.uf + '</text>';
    }).join('');

    this.q('[data-geo-hubs]').innerHTML = this.data.hubs.map(function (h) {
      return '<g class="hub ' + tone(h.sla) + '" data-hub="' + h.id + '" data-name="' + h.name + '" data-region="' + h.region +
        '" data-deliveries="' + h.deliveries + '" data-sla="' + h.sla + '" data-transit="' + h.transit +
        '" data-states="' + h.states.join(',') + '" role="button" tabindex="0" aria-pressed="false" aria-label="' + h.name +
        ', hub da região ' + h.region + ': ' + fmt(h.deliveries) + ' entregas, SLA de ' + pct(h.sla) + '. Selecione para detalhar.">' +
        '<circle class="hub-hit" cx="' + h.x + '" cy="' + h.y + '" r="14" aria-hidden="true"/>' +
        '<circle class="hub-pulse" cx="' + h.x + '" cy="' + h.y + '" r="11"/>' +
        '<circle class="hub-ring" cx="' + h.x + '" cy="' + h.y + '" r="10"/>' +
        '<circle class="hub-dot" cx="' + h.x + '" cy="' + h.y + '" r="6.5"/>' +
        '<circle class="hub-core" cx="' + h.x + '" cy="' + h.y + '" r="2.2"/>' +
        '<text class="hub-label" x="' + (h.x + 14) + '" y="' + (h.y - 8) + '"><tspan class="hub-name">' + h.name + '</tspan></text></g>';
    }).join('');
  };

  GeoMap.prototype.bind = function () {
    var self = this;
    this.onClick = function (event) {
      var chip = event.target.closest('[data-region]');
      if (chip) { self.setRegion(chip.dataset.region); return; }
      var metric = event.target.closest('[data-metric]');
      if (metric) { self.setMetric(metric.dataset.metric); return; }
      var hub = event.target.closest('.hub');
      if (hub) { self.select(hub.dataset.hub === self.state.hub ? null : hub.dataset.hub); return; }
      if (event.target.closest('[data-geo-clear]')) self.select(null);
    };
    this.onKeydown = function (event) {
      var hub = event.target.closest('.hub');
      if (hub && (event.key === 'Enter' || event.key === ' ' || event.key === 'Spacebar')) {
        event.preventDefault();
        self.select(hub.dataset.hub === self.state.hub ? null : hub.dataset.hub);
      }
      if (event.key === 'Escape') self.q('[data-geo-tip]').hidden = true;
    };
    this.el.addEventListener('click', this.onClick);
    this.el.addEventListener('keydown', this.onKeydown);
  };

  GeoMap.prototype.hub = function () {
    var id = this.state.hub;
    return id ? this.data.hubs.find(function (h) { return h.id === id; }) : null;
  };

  GeoMap.prototype.pool = function () {
    var list = this.data.states;
    var hub = this.hub();
    if (hub) {
      list = list.filter(function (s) { return hub.states.indexOf(s.uf) > -1; });
    } else if (this.state.hub) {
      list = [];
    } else if (this.state.region !== 'Todas') {
      list = list.filter(function (s) { return s.region === this.state.region; });
    }
    return list.slice().sort(function (a, b) {
      return this.state.metric === 'volume' ? b.deliveries - a.deliveries : a.sla - b.sla;
    }.bind(this));
  };

  GeoMap.prototype.text = function (selector, value) {
    var node = this.q(selector);
    if (node) node.textContent = value;
  };

  GeoMap.prototype.update = function () {
    var self = this, metric = this.state.metric, hub = this.hub();
    var list = this.pool();
    var max = list.length ? list[0].deliveries : 1;
    this.q('.gm-map').dataset.metric = metric;
    this.qsa('.uf').forEach(function (p) {
      var dim = !hub && self.state.region !== 'Todas' && p.dataset.region !== self.state.region;
      p.dataset.level = level(metric, Number(metric === 'volume' ? p.dataset.volume : p.dataset.sla));
      p.classList.toggle('is-dim', dim);
      p.classList.toggle('is-served', Boolean(hub && hub.states.indexOf(p.dataset.uf) > -1));
      p.tabIndex = dim ? -1 : 0;
      if (dim) p.setAttribute('aria-hidden', 'true'); else p.removeAttribute('aria-hidden');
    });
    this.qsa('.hub').forEach(function (g) {
      var dim = self.state.region !== 'Todas' && g.dataset.region !== self.state.region;
      g.classList.toggle('is-dim', dim);
      g.classList.toggle('is-selected', g.dataset.hub === self.state.hub);
      g.setAttribute('aria-pressed', String(g.dataset.hub === self.state.hub));
      g.tabIndex = dim ? -1 : 0;
      if (dim) g.setAttribute('aria-hidden', 'true'); else g.removeAttribute('aria-hidden');
    });
    this.qsa('[data-metric]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.metric === metric)); });
    this.qsa('[data-region]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.region === self.state.region)); });
    this.qsa('[data-legend]').forEach(function (el) { el.hidden = el.dataset.legend !== metric; });

    this.text('[data-geo-metric]', metric === 'volume' ? 'Volume por estado' : 'SLA por estado');
    this.text('[data-geo-legend-title]', metric === 'volume' ? 'Intensidade de volume' : 'Faixas de SLA');
    this.text('[data-geo-legend-note]', metric === 'volume' ? 'entregas / mês' : 'no mês');
    this.text('[data-geo-scope]', hub ? 'Hub ' + hub.name : (this.state.region === 'Todas' ? 'Brasil' : this.state.region));
    this.text('[data-geo-sum-label]', hub ? 'Em trânsito · hub ' + hub.name : 'Em trânsito · ' + (this.state.region === 'Todas' ? 'rede nacional' : this.state.region));
    this.text('[data-geo-sum-value]', fmt(hub ? hub.transit : (this.data.transit[this.state.region] || 0)));
    this.text('[data-geo-sum-meta]', hub
      ? hub.states.length + ' estados atendidos · SLA ' + pct(hub.sla)
      : list.length + ' UFs · ' + fmt(list.reduce(function (sum, s) { return sum + s.deliveries; }, 0)) + ' entregas no mês');
    this.text('[data-geo-rank-title]', metric === 'volume'
      ? (hub ? 'Maiores volumes do hub' : 'Maiores volumes')
      : (hub ? 'Menores SLA do hub' : 'Menores SLA'));
    this.text('[data-geo-rank-note]', Math.min(5, list.length) + ' UFs');
    this.text('[data-geo-updated]', 'Atualizado ' + this.data.updatedAt);
    this.text('[data-geo-attribution]', this.data.attribution);
    this.q('[data-geo-clear]').hidden = !hub;

    var visible = this.data.states.filter(function (s) { return self.state.region === 'Todas' || s.region === self.state.region; });
    var weight = visible.reduce(function (sum, s) { return sum + s.deliveries; }, 0);
    var sla = visible.reduce(function (sum, s) { return sum + s.sla * s.deliveries; }, 0);
    this.text('[data-geo-count]', visible.length);
    this.text('[data-geo-sla]', weight ? pct(sla / weight) : '—');

    this.q('[data-geo-rank]').innerHTML = list.slice(0, 5).map(function (s, i) {
      var value = metric === 'volume' ? fmt(s.deliveries) : pct(s.sla);
      var width = metric === 'volume'
        ? Math.max(4, s.deliveries / max * 100)
        : Math.max(4, Math.min(100, (s.sla - 80) / 20 * 100));
      return '<li class="rank-row"><span class="rank-pos">' + (i + 1) + '</span><span class="rank-name">' + s.name +
        '<small>' + s.uf + '</small></span><span class="rank-val">' + value + '</span><span class="rank-bar"><i style="width:' +
        width.toFixed(1) + '%"></i></span></li>';
    }).join('');
  };

  GeoMap.prototype.setMetric = function (metric) {
    if (metric !== 'volume' && metric !== 'sla') return this;
    this.state.metric = metric;
    this.update();
    this.emit('geomap:metric', { metric: metric });
    this.announce('Mapa por ' + (metric === 'volume' ? 'volume de entregas' : 'SLA') + '.');
    return this;
  };

  GeoMap.prototype.setRegion = function (region) {
    this.state.region = region;
    if (region !== 'Todas') this.state.hub = null;
    this.update();
    this.emit('geomap:region', { region: region });
    this.announce(region === 'Todas' ? 'Filtro removido. Todos os 27 estados visíveis.' : 'Região ' + region + ' selecionada.');
    return this;
  };

  GeoMap.prototype.select = function (id) {
    this.state.hub = id || null;
    if (id) this.state.region = 'Todas';
    this.update();
    var detail = { hub: this.state.hub };
    this.emit('geomap:select', detail);
    if (typeof this.data.onSelect === 'function') this.data.onSelect(detail);
    var hub = this.hub();
    this.announce(id ? 'Hub ' + (hub ? hub.name : id) + ' selecionado.' : 'Seleção de hub removida.');
    return this;
  };

  GeoMap.prototype.getState = function () {
    return { metric: this.state.metric, region: this.state.region, hub: this.state.hub };
  };

  GeoMap.prototype.setData = function (data) {
    this.data = Object.assign({ states: [], hubs: [], transit: {}, updatedAt: 'agora', attribution: 'Contorno: amCharts geodata (BrazilLow)' }, data || {});
    this.mount();
    this.update();
    return this;
  };

  GeoMap.prototype.announce = function (message) {
    var live = this.q('[data-geo-live]');
    if (!live) return;
    live.textContent = '';
    window.requestAnimationFrame(function () { live.textContent = message; });
  };

  GeoMap.prototype.emit = function (name, detail) {
    this.el.dispatchEvent(new CustomEvent(name, { bubbles: true, detail: detail }));
  };

  GeoMap.prototype.on = function (name, handler) {
    this.el.addEventListener(name, handler);
    return function () { this.el.removeEventListener(name, handler); }.bind(this);
  };

  GeoMap.prototype.destroy = function () {
    this.el.removeEventListener('click', this.onClick);
    this.el.removeEventListener('keydown', this.onKeydown);
    instances.delete(this.el);
  };

  window.TTSCGeoMap = {
    render: function (el, data) {
      if (!el) return null;
      if (instances.has(el)) {
        var current = instances.get(el);
        current.setData(data);
        return current;
      }
      var instance = new GeoMap(el, data);
      el.setAttribute('data-ttsc-geomap', '');
      instances.set(el, instance);
      return instance;
    }
  };
})(window, document);
```

O modelo acima é o esqueleto do módulo: o preview acrescenta o posicionamento do tooltip, a atribuição de cada rótulo de hub e o cálculo ponderado do SLA médio do recorte. Em produção, a geometria vem de `ttsc.geomap.paths.js`; o payload só traz valores agregados.

### SQL

A tabela `units` existe no repositório e é a base das unidades operacionais (`state` guarda a UF). A tabela `shipments` é **DDL nova** deste modelo e precisa de migration. O SLA é calculado no servidor, comparando `delivered_at` com `promised_at`.

```sql
-- DDL nova: remessas agregadas por UF.
CREATE TABLE shipments (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE,
  tenant_id VARCHAR(36) NOT NULL,
  unit_uuid VARCHAR(36) NOT NULL,
  destination_state CHAR(2) NOT NULL,
  status ENUM('in_transit', 'delivered', 'failed', 'returned') NOT NULL DEFAULT 'in_transit',
  promised_at DATETIME NULL,
  delivered_at DATETIME NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  deleted_at DATETIME NULL,
  KEY idx_shipments_tenant_state (tenant_id, destination_state, status),
  KEY idx_shipments_unit (unit_uuid),
  CONSTRAINT fk_shipments_tenant FOREIGN KEY (tenant_id) REFERENCES tenants (id),
  CONSTRAINT fk_shipments_unit FOREIGN KEY (unit_uuid) REFERENCES units (uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 1. Estados do mapa: unidades, entregas, trânsito e SLA por UF no período.
SELECT
  u.state AS uf,
  COUNT(DISTINCT u.uuid) AS units,
  COUNT(s.uuid) AS deliveries,
  COALESCE(SUM(s.status = 'in_transit'), 0) AS in_transit,
  ROUND(
    100 * SUM(s.status = 'delivered' AND s.delivered_at <= s.promised_at)
    / NULLIF(SUM(s.status = 'delivered'), 0),
    1
  ) AS sla
FROM units u
LEFT JOIN shipments s
  ON s.unit_uuid = u.uuid
 AND s.tenant_id = :tenant_uuid
 AND s.created_at >= :period_start
 AND s.created_at < :period_end
 AND s.deleted_at IS NULL
WHERE u.tenant_id = :tenant_uuid
  AND u.status = 'active'
  AND u.state IS NOT NULL
GROUP BY u.state
ORDER BY deliveries DESC;

-- 2. Hubs: as sete unidades com mais entregas no período.
SELECT
  u.uuid,
  u.name,
  u.city,
  u.state,
  COUNT(s.uuid) AS deliveries,
  COALESCE(SUM(s.status = 'in_transit'), 0) AS in_transit,
  ROUND(
    100 * SUM(s.status = 'delivered' AND s.delivered_at <= s.promised_at)
    / NULLIF(SUM(s.status = 'delivered'), 0),
    1
  ) AS sla,
  COUNT(DISTINCT s.destination_state) AS states_served
FROM units u
JOIN shipments s
  ON s.unit_uuid = u.uuid
 AND s.tenant_id = :tenant_uuid
 AND s.created_at >= :period_start
 AND s.created_at < :period_end
 AND s.deleted_at IS NULL
WHERE u.tenant_id = :tenant_uuid
  AND u.status = 'active'
GROUP BY u.uuid, u.name, u.city, u.state
HAVING deliveries > 0
ORDER BY deliveries DESC
LIMIT 7;

-- 3. Ranking textual: cinco UFs com maior volume.
WITH uf AS (
  SELECT u.state AS uf, COUNT(s.uuid) AS deliveries
  FROM units u
  LEFT JOIN shipments s
    ON s.unit_uuid = u.uuid
   AND s.tenant_id = :tenant_uuid
   AND s.created_at >= :period_start
   AND s.created_at < :period_end
   AND s.deleted_at IS NULL
  WHERE u.tenant_id = :tenant_uuid
    AND u.status = 'active'
    AND u.state IS NOT NULL
  GROUP BY u.state
)
SELECT
  ROW_NUMBER() OVER (ORDER BY deliveries DESC) AS position,
  uf,
  deliveries
FROM uf
WHERE deliveries > 0
ORDER BY position
LIMIT 5;
```

Todas as consultas recebem `:tenant_uuid` da sessão, nunca do formulário. O período é fechado (`>=` início e `<` fim) para não contar a virada do mês duas vezes. UF sem remessa aparece com `deliveries = 0` e `sla = NULL`; o componente deve tratar esse caso como “Sem operação”, não como volume zero. O contorno do mapa é ilustrativo e não substitui a malha oficial do IBGE.
