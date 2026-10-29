# SankeyFlow

Fluxo Sankey em SVG puro, em quatro colunas, com volumes conservados, links Bézier proporcionais, destaque por foco e uma lista vertical equivalente no mobile.

## Quando usar

- Mostrar como uma coorte se distribui da origem ao desfecho: site, indicação, campanha → qualificação → proposta → ganho/perda.
- Processos em que o total é o mesmo em todas as etapas: onboarding, roteamento de chamados, distribuição de receita.
- Quando o usuário precisa comparar a espessura de um caminho com o volume da etapa, não apenas ver um total.

Não use quando:

- As etapas podem crescer e diminuir sem conservar o total: use [ApexCharts](../ApexCharts/README.md) ou [FunnelBars](../FunnelBars/README.md).
- O dado é uma série temporal ou uma comparação simples: [ApexCharts](../ApexCharts/README.md).
- O assunto é hierarquia, não fluxo: use [OrgChart](../OrgChart/README.md).
- O usuário precisa editar etapas, prazos ou responsáveis: [KanbanBoard](../KanbanBoard/README.md) ou [Gantt](../Gantt/README.md).
- Há dezenas de origens e destinos: agregue em grupos antes de renderizar; 36 paradas de teclado já é o limite prático deste componente.

## Anatomia

```
ORIGEM            QUALIFICAÇÃO        OPORTUNIDADE        DESFECHO
[Orgânico]════════[MQL]═══════════════[Proposta]══════════[Ganho]
     ╲════════════[SQL]══════╲════════[Follow-up]════════[Em negociação]
      ╲═══════════[Nutrição]══╲═══════════════════════════[Perdido]
```

| Parte | Classe / elemento | Obrigatório | Função |
|---|---|---|---|
| Card | `.sk-card` | sim | Superfície, borda, raio e sombra |
| Cabeçalho | `.sk-hd`, `.sk-kpis`, `.sk-pill` | sim | Título, contexto e totais em texto |
| Palco | `.sk-stage` | sim | `position: relative` para o tooltip |
| SVG | `svg.sk-svg` | sim | `viewBox="0 0 1200 330"`, `role="group"` |
| Colunas | `.sk-col` | sim | Rótulo de cada etapa |
| Links | `.sk-links` > `path.sk-link` | sim | Área Bézier proporcional ao volume |
| Nós | `.sk-nodes` > `g.sk-node` > `rect` | sim | Barra de 10 px com rótulo e valor |
| Tooltip | `.sk-tip` | sim | Valor e participação no hover/foco |
| Legenda | `.sk-legend` | recomendado | Traduz as cores das etapas |
| Resumo | `.sk-sr#sk-summary` | sim | Alternativa textual para leitor de tela |
| Lista mobile | `.sk-mobile` | sim | Substitui o SVG abaixo de 640 px |

### Estrutura de dados

```js
{
  total: 5800,
  stages: ['Origem', 'Qualificação', 'Oportunidade', 'Desfecho'],
  nodes: [
    { id: 'organico', label: 'Orgânico', stage: 0, value: 2300, tone: 'accent' },
    { id: 'mql', label: 'MQL', stage: 1, value: 2050, tone: 'info' },
    // ...
  ],
  links: [
    { source: 'organico', target: 'mql', value: 900 },
    // ...
  ]
}
```

Regras de integridade:

- `id` é único; `stage` vai de `0` a `3`; `links` só ligam `stage` a `stage + 1`.
- Nó de origem: `value = soma dos links de saída`. Nó de destino: `value = soma dos links de entrada`. Nó intermediário: as duas somas são iguais.
- `total = soma dos nós da coluna 0 = soma dos nós da coluna 3`.
- Todos os valores são inteiros positivos; links com `value: 0` não são desenhados.
- `tone` é `accent`, `info`, `warning`, `success`, `danger` ou `primary`; o renderer traduz para `var(--ttsc-*)`.

O preview usa 5.800 leads: 2.300 + 1.750 + 960 + 790 na origem, 2.050 + 1.480 + 2.270 na qualificação, 3.020 + 2.780 na oportunidade e 1.624 + 1.392 + 2.784 no desfecho. Todas as colunas somam 5.800.

### Layout

- `viewBox` 1200 × 330; colunas em `x = 4, 300, 600, 900`; topo em `y = 34`; área útil de 286 px; gap de 11 px; nó de 10 px.
- Uma única escala para as quatro colunas: `k = (286 − 11 × (maxNós − 1)) / total`. A altura de um nó é `value × k`, então 2.300 leads ocupam mais altura que 1.750 em qualquer coluna.
- Os links saem da borda direita do nó de origem e entram na borda esquerda do destino. A espessura na origem é `alturaDoNó × valorDoLink / valorDoNó`; no destino, o mesmo cálculo com o nó de destino. O caminho é uma curva Bézier cúbica com controles no `x` médio.
- Links de saída são ordenados pela posição `y` do destino; links de entrada, pela posição `y` da origem. Isso reduz cruzamentos sem mudar os volumes.
- O SVG escala com `width: 100%` e `height: auto`; a altura do card acompanha o conteúdo. Abaixo de 640 px, o SVG e a legenda somem e uma lista ordenada por par de etapas ocupa o lugar.

## Variantes

| Variante | Classe / opção | Uso |
|---|---|---|
| Quatro colunas | padrão | Origem → qualificação → oportunidade → desfecho |
| Volume absoluto | `total` + `value` em leads/reais | Compara espessura e mostra o número no rótulo |
| Contagem | mesmos campos com contagem de registros | Funil de chamados, matrículas, tickets |
| Densidade | até 4–5 nós por coluna, 24–30 links | Mantém rótulos legíveis e o tabuleiro navegável |
| Lista mobile | `< 640px`, `.sk-mobile` | Mesmos dados em texto, sem rolagem horizontal |
| Destaque de nó | `tone` + hover/foco | Realça o nó e todos os links vizinhos |
| Destaque de link | hover/foco no `path` | Realça o caminho e os dois nós das pontas |

O componente é intencionalmente fixo em quatro colunas. Para três ou cinco etapas, altere `stages`, `cols` e o laço de links no renderer; o layout e a validação precisam acompanhar.

## Estados

| Estado | Como aparece |
|---|---|
| Padrão | Links com `fill-opacity: .32`; nós e rótulos em `ttsc-text`/`ttsc-text-2`. |
| Hover no link | Link em `.is-active` com `fill-opacity: .72`; demais links em `.07`; nós das pontas em `.is-active`. |
| Hover no nó | Nó e links vizinhos em `.is-active`; demais em `.07`/`opacity: .35`. |
| Foco por teclado | Mesmo destaque do hover; o `rect` do nó recebe contorno de 2,5 px em `ttsc-text`. |
| Tooltip | `.sk-tip.on`, com origem → destino, volume, percentual da origem e percentual do total. |
| Escape | Remove `.is-dim`, `.is-active` e fecha o tooltip. |
| Mobile | SVG oculto; lista com pares “origem → destinos” e valores. |
| Vazio | Card mantém cabeçalho e mostra “Sem fluxo no período”; não renderize SVG vazio. |
| Carregando | [Skeleton](../Skeleton/README.md) de 330 px no lugar do palco. |
| Erro | Texto em `ttsc-danger-text`, ação “Tentar novamente” e o resumo textual anterior. |
| Movimento reduzido | Sem transição de `fill-opacity`; o destaque continua por opacidade. |
| Tema escuro | Cores vêm de `var(--ttsc-*)`; não há recriação do SVG na troca de tema. |

## Acessibilidade

- O SVG tem `role="group"`, `aria-labelledby` com o título e `aria-describedby` com o resumo. Cada link e cada nó é `role="img"` com `aria-label` completo: origem, destino, volume e participação.
- `Tab` percorre os 24 links e os 12 nós na ordem do DOM; `Enter`/`Espaço` não são necessários porque o foco já revela o tooltip. `Escape` limpa o destaque.
- O tooltip tem `role="status"` e `aria-live="polite"`; ele repete o mesmo conteúdo do `aria-label`, nunca informação exclusiva.
- O resumo `.sk-sr` descreve o total e os desfechos em texto. No mobile, a lista `ol` tem `aria-label` e cada item descreve origem, destinos e valores.
- Cor não é o único canal: cada nó tem nome e valor; a legenda traduz as cores; os percentuais aparecem no tooltip e nos KPIs.
- O foco visível usa `filter: drop-shadow` no link e `stroke` no nó, porque `outline` não funciona bem em SVG.
- Evite mais de 36 paradas de teclado. Se o fluxo crescer, agregue origens/destinos ou ofereça uma tabela antes do SVG.
- `prefers-reduced-motion: reduce` remove as transições; o SVG é estático por padrão.

## API

Namespace global `window.TTSCSankey`.

| Método | Efeito |
|---|---|
| `TTSCSankey.render(container, data)` | Limpa o container, monta `.sk-stage` com SVG e tooltip e devolve `{ stage, svg }`. |
| `TTSCSankey.destroy(container)` | Limpa o conteúdo montado pelo componente e zera a referência no container. |

O container deve ser um elemento vazio (por exemplo `<div id="sk-chart"></div>`); o renderer cria o palco internamente. `render` não valida a conservação dos volumes: valide antes, no PHP ou no módulo de dados, e mostre erro em vez de desenhar um fluxo inconsistente.

```js
// Validação mínima antes de renderizar
function validarSankey(data) {
  var byId = {};
  data.nodes.forEach(function (n) {
    if (!n.id || byId[n.id] || n.stage < 0 || n.stage > 3 || !(n.value > 0)) {
      throw new Error('SankeyFlow: nó inválido em ' + n.id);
    }
    byId[n.id] = n;
  });
  var soma = [0, 0, 0, 0], entra = [0, 0, 0, 0], sai = [0, 0, 0, 0];
  data.nodes.forEach(function (n) { soma[n.stage] += n.value; });
  data.links.forEach(function (l) {
    var s = byId[l.source], t = byId[l.target];
    if (!s || !t || t.stage !== s.stage + 1 || !(l.value > 0)) {
      throw new Error('SankeyFlow: link inválido ' + l.source + ' → ' + l.target);
    }
    sai[s.stage] += l.value; entra[t.stage] += l.value;
  });
  for (var i = 0; i < 4; i += 1) {
    if (i > 0 && entra[i] !== soma[i]) throw new Error('SankeyFlow: entrada não fecha na coluna ' + i);
    if (i < 3 && sai[i] !== soma[i]) throw new Error('SankeyFlow: saída não fecha na coluna ' + i);
  }
  if (soma[0] !== data.total || soma[3] !== data.total) throw new Error('SankeyFlow: total não fecha');
}
```

Classes e atributos:

| Seletor | Efeito |
|---|---|
| `.sk-stage.is-dim` | Esmaece tudo que não está ativo |
| `.sk-link.is-active` | Link em destaque |
| `.sk-node.is-active` | Nó em destaque |
| `.sk-tip.on` | Tooltip visível |
| `--c` no link/nó | Cor do token da etapa |
| `tabindex="0"` + `role="img"` | Foco e leitura por leitor de tela |

## Modelos

### HTML

```php
<section class="sk-card" aria-labelledby="sk-title">
  <div class="sk-hd">
    <div>
      <h2 id="sk-title">Fluxo de aquisição</h2>
      <p>Coorte de <?= $this->e($periodLabel) ?> · origem, qualificação, oportunidade e desfecho.</p>
    </div>
    <span class="sk-pill"><i></i><span id="sk-total"><?= number_format($total, 0, ',', '.') ?> leads</span></span>
  </div>

  <ul class="sk-kpis" aria-label="Resumo por desfecho">
    <li style="--c:var(--ttsc-success)"><i></i>Ganho <b><?= number_format($won, 0, ',', '.') ?></b> <small><?= $this->e($wonPct) ?></small></li>
    <li style="--c:var(--ttsc-warning)"><i></i>Em negociação <b><?= number_format($open, 0, ',', '.') ?></b> <small><?= $this->e($openPct) ?></small></li>
    <li style="--c:var(--ttsc-danger)"><i></i>Perdido <b><?= number_format($lost, 0, ',', '.') ?></b> <small><?= $this->e($lostPct) ?></small></li>
  </ul>

  <div id="sk-chart"></div>
  <ol class="sk-mobile" id="sk-mobile" aria-label="Fluxo de aquisição em lista"></ol>

  <p class="sk-legend" aria-hidden="true">
    <span style="--c:var(--ttsc-accent)"><i></i>Origem</span>
    <span style="--c:var(--ttsc-info)"><i></i>Qualificação</span>
    <span style="--c:var(--ttsc-warning)"><i></i>Oportunidade</span>
    <span style="--c:var(--ttsc-primary-700)"><i></i>Desfecho</span>
  </p>

  <p class="sk-sr" id="sk-summary"><?= $this->e($summary) ?></p>
</section>

<script type="application/json" id="sk-data">
  <?= json_encode($sankey, JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?>
</script>
```

`$summary` deve trazer o total, os totais por etapa e os desfechos com percentual. O texto do PHP não deve depender de cor.

### CSS

```css
.sk-card { background: var(--ttsc-surface); border: 1px solid var(--ttsc-border);
           border-radius: var(--ttsc-radius-surface); box-shadow: var(--ttsc-shadow-sm);
           padding: 16px 20px 14px; min-width: 0; }
.sk-stage { position: relative; min-width: 0; }
.sk-svg { display: block; width: 100%; height: auto; overflow: visible; }
.sk-col { font-size: 10px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase;
          fill: var(--ttsc-text-muted); }
.sk-link { fill: var(--c); fill-opacity: .32; cursor: pointer; transition: fill-opacity .15s ease; }
.sk-node { cursor: pointer; }
.sk-node rect { fill: var(--c); stroke: var(--ttsc-surface); stroke-width: 2; }
.sk-link:hover, .sk-link.is-active { fill-opacity: .72; }
.sk-link:focus-visible { outline: none; filter: drop-shadow(0 0 2px var(--ttsc-text)); }
.sk-node:focus-visible { outline: none; }
.sk-node:focus-visible rect { stroke: var(--ttsc-text); stroke-width: 2.5; }
.sk-stage.is-dim .sk-link:not(.is-active) { fill-opacity: .07; }
.sk-stage.is-dim .sk-node:not(.is-active) rect { opacity: .35; }
.sk-name { font-size: 11px; font-weight: 600; fill: var(--ttsc-text-2);
           paint-order: stroke; stroke: var(--ttsc-surface); stroke-width: 3px; }
.sk-val { font-size: 10px; fill: var(--ttsc-text-muted); font-variant-numeric: tabular-nums;
          paint-order: stroke; stroke: var(--ttsc-surface); stroke-width: 3px; }
.sk-tip { position: absolute; z-index: 5; max-width: 260px; padding: 8px 10px;
          background: var(--ttsc-surface); border: 1px solid var(--ttsc-border);
          border-radius: var(--ttsc-radius-sm); box-shadow: var(--ttsc-shadow-popover);
          pointer-events: none; opacity: 0; transform: translateY(4px); transition: opacity .12s ease; }
.sk-tip.on { opacity: 1; transform: none; }
.sk-mobile { display: none; list-style: none; margin: 4px 0 0; padding: 0; }
.sk-sr { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
         overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; }
@media (max-width: 640px) {
  .sk-svg, .sk-legend { display: none; }
  .sk-mobile { display: block; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .001ms !important; transition-duration: .001ms !important; }
}
```

### JS

```js
// assets/js/core/ttsc.sankey.js — sem dependências
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var NF0 = new Intl.NumberFormat('pt-BR');
  var NF1 = new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  var seq = 0;

  function tone(t) { return 'var(--ttsc-' + (t === 'primary' ? 'primary-700' : t) + ')'; }
  function n(v) { return NF0.format(v); }
  function pct(v) { return NF1.format(v) + '%'; }
  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(e);
    return e;
  }

  function render(host, data) {
    if (!host || !data || !data.nodes || !data.links) throw new Error('TTSCSankey: dados ausentes');
    host.innerHTML = '';
    var uid = 'sk' + (++seq);
    var W = 1200, H = 330, y0 = 34, plotH = 286, gap = 11, nodeW = 10;
    var cols = [4, 300, 600, 900];
    var byId = {}, columns = [[], [], [], []];
    data.nodes.forEach(function (nd) { byId[nd.id] = nd; columns[nd.stage].push(nd); });

    var maxNodes = columns.reduce(function (m, c) { return Math.max(m, c.length); }, 1);
    var k = (plotH - gap * (maxNodes - 1)) / data.total;
    columns.forEach(function (col) {
      var y = y0;
      col.forEach(function (nd) {
        nd._h = nd.value * k;
        nd._y = y;
        nd._x = cols[nd.stage];
        y += nd._h + gap;
      });
    });

    var out = {}, inn = {};
    data.links.forEach(function (l) {
      l._s = byId[l.source]; l._t = byId[l.target];
      (out[l.source] = out[l.source] || []).push(l);
      (inn[l.target] = inn[l.target] || []).push(l);
    });
    Object.keys(out).forEach(function (id) {
      out[id].sort(function (a, b) { return a._t._y - b._t._y; });
      var off = 0;
      out[id].forEach(function (l) {
        l._sh = l._s._h * (l.value / l._s.value);
        l._sy = l._s._y + off; off += l._sh;
      });
    });
    Object.keys(inn).forEach(function (id) {
      inn[id].sort(function (a, b) { return a._s._y - b._s._y; });
      var off = 0;
      inn[id].forEach(function (l) {
        l._th = l._t._h * (l.value / l._t.value);
        l._ty = l._t._y + off; off += l._th;
      });
    });

    var stage = document.createElement('div');
    stage.className = 'sk-stage';
    var svg = el('svg', {
      viewBox: '0 0 ' + W + ' ' + H, class: 'sk-svg', role: 'group',
      'aria-labelledby': uid + '-title', 'aria-describedby': 'sk-summary'
    });
    var title = el('title', { id: uid + '-title' }, svg);
    title.textContent = 'Fluxo de aquisição: ' + n(data.total) + ' leads da origem ao desfecho.';
    data.stages.forEach(function (name, i) { el('text', { x: cols[i], y: 14, class: 'sk-col' }, svg).textContent = name; });

    var gLinks = el('g', { class: 'sk-links' }, svg);
    data.links.forEach(function (l) {
      var x0 = l._s._x + nodeW, x1 = l._t._x, mid = (x0 + x1) / 2;
      var d = 'M' + x0 + ',' + l._sy + ' C' + mid + ',' + l._sy + ' ' + mid + ',' + l._ty + ' ' + x1 + ',' + l._ty +
              ' L' + x1 + ',' + (l._ty + l._th) + ' C' + mid + ',' + (l._ty + l._th) + ' ' + mid + ',' +
              (l._sy + l._sh) + ' ' + x0 + ',' + (l._sy + l._sh) + ' Z';
      var p = el('path', { d: d, class: 'sk-link', tabindex: '0', role: 'img' }, gLinks);
      p.style.setProperty('--c', tone(l._s.tone));
      var share = l.value / l._s.value * 100;
      var label = l._s.label + ' para ' + l._t.label + ': ' + n(l.value) + ' leads, ' +
                  pct(share) + ' de ' + l._s.label + '.';
      p.setAttribute('aria-label', label);
      p._info = { title: l._s.label + ' → ' + l._t.label, value: n(l.value) + ' leads',
                  share: pct(share) + ' de ' + l._s.label + ' · ' + pct(l.value / data.total * 100) + ' do total',
                  source: l.source, target: l.target, kind: 'link' };
    });

    var gNodes = el('g', { class: 'sk-nodes' }, svg);
    data.nodes.forEach(function (nd) {
      var g = el('g', { class: 'sk-node', tabindex: '0', role: 'img' }, gNodes);
      g.style.setProperty('--c', tone(nd.tone));
      var share = nd.value / data.total * 100;
      g.setAttribute('aria-label', 'Etapa ' + data.stages[nd.stage] + ', ' + nd.label + ': ' +
        n(nd.value) + ' leads, ' + pct(share) + ' do total.');
      el('rect', { x: nd._x, y: nd._y, width: nodeW, height: Math.max(2, nd._h), rx: 3 }, g);
      el('text', { x: nd._x + nodeW + 8, y: nd._y + nd._h / 2 - 1, class: 'sk-name' }, g).textContent = nd.label;
      el('text', { x: nd._x + nodeW + 8, y: nd._y + nd._h / 2 + 12, class: 'sk-val' }, g).textContent = n(nd.value);
      g._info = { title: nd.label, value: n(nd.value) + ' leads', share: pct(share) + ' do total', id: nd.id, kind: 'node' };
    });

    var tip = document.createElement('div');
    tip.className = 'sk-tip';
    tip.id = uid + '-tip';
    tip.setAttribute('role', 'status');
    tip.setAttribute('aria-live', 'polite');
    stage.appendChild(svg);
    stage.appendChild(tip);
    host.appendChild(stage);

    function place(target, ev) {
      tip.innerHTML = '<b>' + target._info.title + '</b><span>' + target._info.value + ' · ' + target._info.share + '</span>';
      tip.classList.add('on');
      var box = stage.getBoundingClientRect(), b = target.getBoundingClientRect();
      var x = ev && ev.clientX ? ev.clientX - box.left + 12 : b.left - box.left + b.width / 2 - tip.offsetWidth / 2;
      var y = ev && ev.clientY ? ev.clientY - box.top - tip.offsetHeight - 8 : b.top - box.top - tip.offsetHeight - 8;
      tip.style.left = Math.min(Math.max(6, x), Math.max(6, box.width - tip.offsetWidth - 6)) + 'px';
      tip.style.top = Math.max(4, Math.min(y, box.height - tip.offsetHeight - 4)) + 'px';
    }
    function clear() {
      stage.classList.remove('is-dim');
      svg.querySelectorAll('.is-active').forEach(function (e) { e.classList.remove('is-active'); });
    }
    function activate(target) {
      clear(); stage.classList.add('is-dim'); target.classList.add('is-active');
      if (target._info.kind === 'link') {
        gNodes.querySelectorAll('.sk-node').forEach(function (g) {
          if (g._info.id === target._info.source || g._info.id === target._info.target) g.classList.add('is-active');
        });
      } else {
        var nb = {};
        gLinks.querySelectorAll('.sk-link').forEach(function (p, i) {
          var l = data.links[i];
          if (l.source === target._info.id || l.target === target._info.id) {
            p.classList.add('is-active'); nb[l.source] = true; nb[l.target] = true;
          }
        });
        gNodes.querySelectorAll('.sk-node').forEach(function (g) { if (nb[g._info.id]) g.classList.add('is-active'); });
      }
    }
    function pick(ev) { return ev.target.closest ? ev.target.closest('.sk-link, .sk-node') : null; }
    stage.addEventListener('mouseover', function (ev) {
      var t = pick(ev); if (t && t._info) { activate(t); place(t, ev); }
    });
    stage.addEventListener('mouseout', function (ev) {
      var t = pick(ev); if (t && !(ev.relatedTarget && t.contains(ev.relatedTarget))) { tip.classList.remove('on'); clear(); }
    });
    stage.addEventListener('focusin', function (ev) {
      var t = pick(ev); if (t && t._info) { activate(t); place(t, null); }
    });
    stage.addEventListener('focusout', function () { tip.classList.remove('on'); clear(); });
    stage.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') { tip.classList.remove('on'); clear(); } });

    return { stage: stage, svg: svg };
  }

  window.TTSCSankey = {
    render: function (host, data) {
      window.TTSCSankey.destroy(host);
      var out = render(host, data);
      host.__ttscSankey = out;
      return out;
    },
    destroy: function (host) {
      if (host && host.__ttscSankey) {
        host.innerHTML = '';
        host.__ttscSankey = null;
      }
    }
  };
})();
```

O preview completa a lista mobile com `buildMobile(data, list)`: agrupa os links por origem em cada par de etapas e escreve “Origem → Destino valor” em `<li>` com `aria-label`. O resumo `.sk-sr` é atualizado a partir do mesmo objeto `DATA`.

### SQL

O repo tem `crm_leads`, `crm_deals` e `crm_pipeline_stages`, mas **não** tem histórico de transições de etapa. Um Sankey fiel precisa desse histórico; a migration abaixo cria a tabela de eventos. Ela não existe no dump atual.

```sql
-- database/migrations/20261026_002_crm_lead_stage_events.sql (MariaDB 10.11 / MySQL 8)
CREATE TABLE IF NOT EXISTS crm_lead_stage_events (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid        CHAR(36) NOT NULL UNIQUE,
  tenant_id   CHAR(36) NOT NULL,
  lead_uuid   CHAR(36) NOT NULL,
  stage_key   ENUM('origem', 'qualificacao', 'oportunidade', 'desfecho') NOT NULL,
  stage_label VARCHAR(80) NOT NULL,
  occurred_at DATETIME NOT NULL,
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at  DATETIME NULL,
  KEY idx_lead_stage (tenant_id, lead_uuid, stage_key, occurred_at),
  KEY idx_window (tenant_id, occurred_at, stage_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Cada lead precisa de uma linha por etapa (a primeira ocorrência de cada `stage_key` no período). A consulta devolve os links já agregados, com conservação de volume:

```sql
WITH ranked AS (
  SELECT e.lead_uuid, e.stage_key, e.stage_label,
         ROW_NUMBER() OVER (PARTITION BY e.lead_uuid, e.stage_key ORDER BY e.occurred_at) AS rn
    FROM crm_lead_stage_events e
   WHERE e.tenant_id = :tenant_uuid
     AND e.deleted_at IS NULL
     AND e.occurred_at >= :cohort_start
     AND e.occurred_at <  :cohort_end
),
stage AS (
  SELECT lead_uuid,
         MAX(CASE WHEN stage_key = 'origem' THEN stage_label END)        AS origem,
         MAX(CASE WHEN stage_key = 'qualificacao' THEN stage_label END)   AS qualificacao,
         MAX(CASE WHEN stage_key = 'oportunidade' THEN stage_label END)   AS oportunidade,
         MAX(CASE WHEN stage_key = 'desfecho' THEN stage_label END)       AS desfecho
    FROM ranked
   WHERE rn = 1
   GROUP BY lead_uuid
  HAVING COUNT(DISTINCT stage_key) = 4
),
links AS (
  SELECT 'origem' AS stage_key, origem AS source, qualificacao AS target, COUNT(*) AS total
    FROM stage GROUP BY origem, qualificacao
  UNION ALL
  SELECT 'qualificacao', qualificacao, oportunidade, COUNT(*)
    FROM stage GROUP BY qualificacao, oportunidade
  UNION ALL
  SELECT 'oportunidade', oportunidade, desfecho, COUNT(*)
    FROM stage GROUP BY oportunidade, desfecho
)
SELECT stage_key, source, target, total
  FROM links
 WHERE total > 0
 ORDER BY FIELD(stage_key, 'origem', 'qualificacao', 'oportunidade'), total DESC;
```

O PHP agrega os mesmos links por `source`/`target` para montar `nodes` e calcula `total` pela soma da coluna 0. Se o `HAVING` descartar leads incompletos, o total do Sankey será menor que o total de leads da coorte: mostre essa diferença como nota (“n leads sem histórico completo”) em vez de mascará-la.

## Faça / Não faça

- **Faça:** valide a conservação antes de renderizar; um Sankey que não fecha é pior que uma tabela.
- **Faça:** use uma escala única para as quatro colunas; a altura do nó deve comparar volume entre etapas.
- **Faça:** ordene os links pela posição do destino/origem para reduzir cruzamentos.
- **Faça:** mantenha o resumo textual e a lista mobile; os dois são a alternativa ao SVG.
- **Não faça:** usar o Sankey para etapas que crescem ou para séries temporais; use [ApexCharts](../ApexCharts/README.md) ou [FunnelBars](../FunnelBars/README.md).
- **Não faça:** esconder o valor apenas na espessura ou na cor; nome e número ficam sempre visíveis.
- **Não faça:** passar de 4–5 nós por coluna ou de 36 paradas de teclado sem agregar os dados.
- **Não faça:** re-renderizar o SVG na troca de tema; as cores são `var(--ttsc-*)` e mudam sozinhas.
