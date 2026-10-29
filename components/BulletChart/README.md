# BulletChart

Bullet chart (gráfico de projétil): uma barra de valor realizado, um marcador de meta e faixas qualitativas de fundo — a leitura de "realizado vs. meta" em um só traço, sem precisar de eixos.

> Também listado em: **Gráficos**.

## Quando usar

- Comparar o realizado com a meta e com faixas de referência (ruim / aceitável / bom) em pouco espaço: arrecadação vs. meta por unidade, ocupação vs. capacidade por turno, inadimplência vs. teto.
- Em listas de metas (board) e no rodapé de cards de KPI (mini) — onde um gráfico de eixo completo (`[ApexCharts](../ApexCharts/README.md)`, `[AnalyticsPanels](../AnalyticsPanels/README.md)`) é grande demais.
- Quando a pergunta é uma só: "chegamos?" — a resposta vem da posição da barra contra o marcador de meta e a faixa.
- **Não use** para ranking puro, sem meta: use [RankedBars](../RankedBars/README.md).
- **Não use** para progresso simples de uma tarefa (0 a 100% sem faixas): use [Progress](../Progress/README.md).
- **Não use** para composição de um total: use [WidgetIncomeBreakdown](../WidgetIncomeBreakdown/README.md) ou o donut do ApexCharts.
- Nas faixas, use no máximo 3 segmentos (60/80/100 como no preview); acima disso ninguém distingue.

## Anatomia

```
Unidade Norte
┌────────────────────────────────────────────┬──────────────┐
│ ░░░░░░░░│▒▒▒▒▒▒│▓▓▓▓▓▓░░░░░░░░  ┃meta      │ R$ 96,8 mil  │
│ ░░░░░░░░│▒▒▒▒▒▒│████████░░░░░░░░  ┃         │ Perto da meta│
└────────────────────────────────────────────┴──────────────┘
  faixa 1 (0–60)  faixa 2    barra realizada   ▲ marcador     valor + status
                              faixa 3                          + nota
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Linha | `.bullets li` (rótulo, trilha, valor) | sim |
| Rótulo | `.b-label` (nome da métrica/unidade) | sim |
| Trilha | `.b-track` com 3 `.b-band` (faixas qualitativas) | sim |
| Barra | `.b-measure` (realizado, `ttsc-accent`) | sim |
| Meta | `.b-target` (marcador vertical, `ttsc-text`) | sim |
| Valor | `.b-value` (valor + status + nota) | sim |
| Status | `.st-ok` / `.st-warn` / `.st-bad` com texto | sim — nunca só cor |
| Legenda | `.legend` (Realizado, Meta, Faixas) | no primeiro bullet da página |
| Vertical | `.vcol svg` (faixas + coluna + marcador) | variante |
| Mini | `.mini` (trilha de 10 px no rodapé de KPI) | variante |

## Variantes

| Variante | Peças | Uso |
|---|---|---|
| Horizontal | rótulo + trilha + valor com status | Padrão, dentro de cards de análise |
| Board compacto | lista de 4–6 bullets com valores curtos | "Metas do semestre" — painel lateral |
| Vertical | colunas SVG com marcador de meta | Ocupação por turno, comparativos curtos |
| Mini | trilha de 10 px + rótulo + meta | Rodapé de cards de KPI e [ExecutiveStrip](../ExecutiveStrip/README.md) |
| Escala invertida | barra passa do teto → estado de risco | Inadimplência, custo, SLA violado (menor é melhor) |

## Estados

| Estado | Como aplicar |
|---|---|
| Na meta | `.st-ok` + nota "meta batida"/"acima" quando realizado ≥ 100% da meta |
| Perto da meta | `.st-warn` entre 80% e 99% da meta |
| Abaixo da meta | `.st-bad` abaixo de 80% da meta |
| Sem meta definida | sem `.b-target`; nota "meta não definida" — não invente marcador |
| Sem dados | trilha só com faixas + valor "—" + nota "sem apuração no período" |
| Escala invertida | barra em `ttsc-danger` quando ultrapassa o teto; texto carrega o alerta |

## Acessibilidade

- Cada trilha tem `role="img"` + `aria-label` com a leitura completa ("Unidade Norte: perto da meta — 74% da meta, R$ 96,8 mil"); o valor e o status também estão visíveis em texto.
- O marcador de meta é contraste alto (`ttsc-text`) nos dois temas; a barra é `ttsc-accent`.
- Faixas são fundo decorativo (diferenças sutis de tom): a informação está na barra, no marcador e no texto — nunca só na cor da faixa.
- Sem animação; não há o que pausar com `prefers-reduced-motion`.
- O board é uma lista real (`<ol>`); lido de cima para baixo, uma métrica por linha.

## Faça / Não faça

- **Faça:** manter a escala fixa (0–120% da meta) em todos os bullets do mesmo painel — a comparação visual só funciona com escala igual.
- **Faça:** escrever o corte das faixas no subtítulo ("faixas: abaixo de 60%, 60–79%, 80% ou mais").
- **Faça:** escala invertida documentada no card ("menor é melhor").
- **Não faça:** faixas coloridas por semáforo (verde/vermelho) — faixas são tons discretos; estado fica no texto.
- **Não faça:** mais de 6 bullets por card; use uma tabela ou divida em cards.
- **Não faça:** marcador de meta sem valor de referência no texto ("meta 85").

## API

| Item | Uso |
|---|---|
| `TTSCBulletChart.init(el)` | Lê `data-bullets` (JSON: `[{label, value, target, val, note}]`), retorna a instância |
| `instance.update(data)` | Redesenha com novo array (mesmo formato) |
| `value` / `target` | Percentuais na escala 0–120; acima de 120 a barra e o marcador saturam |
| `val` / `note` | Textos exibidos à direita (valor formatado e nota curta) |
| Status | Calculado de `value/target`: ≥ 100% na meta, 80–99% perto, < 80% abaixo |

## Modelos

### HTML

```html
<figure class="card">
  <h2>Arrecadação vs. meta por unidade</h2>
  <p>Novembro de 2026 · faixas: abaixo de 60%, 60–79%, 80% ou mais</p>
  <ol class="bullets" data-bullets='<?= json_encode($bullets, JSON_HEX_APOS | JSON_HEX_TAG | JSON_UNESCAPED_UNICODE) ?>'></ol>
  <ul class="legend" aria-label="Legenda do gráfico">
    <li><span class="lg-measure" aria-hidden="true"></span> Realizado</li>
    <li><span class="lg-target" aria-hidden="true"></span> Meta</li>
    <li><span class="lg-band" aria-hidden="true"></span> Faixas</li>
  </ul>
</figure>
<script src="<?= asset('js/core/ttsc.bullet-chart.js') ?>"></script>
```

### CSS

```css
.bullets{list-style:none;margin:0;padding:0;display:grid;gap:16px}
.bullets li{display:grid;grid-template-columns:minmax(88px,150px) minmax(0,1fr) 168px;gap:12px;align-items:center}
.b-track{position:relative;height:26px;border-radius:4px;overflow:hidden;display:flex}
.b-band.b1{background:var(--ttsc-surface-2)}
.b-band.b2{background:color-mix(in srgb,var(--ttsc-accent) 10%,var(--ttsc-surface))}
.b-band.b3{background:color-mix(in srgb,var(--ttsc-accent) 22%,var(--ttsc-surface))}
.b-measure{position:absolute;top:4px;bottom:4px;left:0;border-radius:3px;background:var(--ttsc-accent);min-width:3px}
.b-target{position:absolute;top:0;bottom:0;width:2px;background:var(--ttsc-text);border-radius:1px}
@media (max-width:640px){ .bullets li{grid-template-columns:1fr 118px} .b-label{grid-column:1 / -1} }
```

### JS

```js
// assets/js/core/ttsc.bullet-chart.js
window.TTSCBulletChart = (function () {
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
    return '&#' + c.charCodeAt(0) + ';';
    });
  }
  function Bullet(el) {
    this.el = el;
    this.data = [];
    try { this.data = JSON.parse(el.getAttribute('data-bullets') || '[]'); } catch (e) { this.data = []; }
    this.render();
  }
  Bullet.prototype.render = function () {
    var self = this;
    this.el.innerHTML = '';
    this.data.forEach(function (d) {
      var pct = d.target ? Math.round(100 * d.value / d.target) : d.value;
      var st = pct >= 100 ? 'st-ok' : (pct >= 80 ? 'st-warn' : 'st-bad');
      var stTxt = pct >= 100 ? 'Na meta' : (pct >= 80 ? 'Perto da meta' : 'Abaixo da meta');
      var li = document.createElement('li');
      li.innerHTML =
        '<span class="b-label">' + esc(d.label) + '</span>' +
        '<div class="b-track" role="img" aria-label="' + esc(d.label) + ': ' + stTxt.toLowerCase() + ' — ' + esc(d.note) + '.">' +
          '<span class="b-band b1" style="width:60%"></span>' +
          '<span class="b-band b2" style="width:20%"></span>' +
          '<span class="b-band b3" style="width:20%"></span>' +
          '<span class="b-measure" style="width:' + Math.min(d.value, 120) + '%"></span>' +
          '<span class="b-target" style="left:' + Math.min(d.target, 120) + '%"></span>' +
        '</div>' +
        '<span class="b-value"><b>' + esc(d.val) + ' <span class="' + st + '">' + stTxt + '</span></b><small>' + esc(d.note) + '</small></span>';
      self.el.appendChild(li);
    });
  };
  Bullet.prototype.update = function (data) { this.data = data; this.render(); };
  return { init: function (el) { return new Bullet(el); } };
})();
document.querySelectorAll('[data-bullets]').forEach(function (el) { window.TTSCBulletChart.init(el); });
```

### SQL

Metas por unidade ficam em tabela própria (DDL nova); o realizado vem das tabelas do módulo (exemplo com `enrollments` para matrículas). Calcule sempre com `deleted_at IS NULL`.

```sql
-- Metas por unidade e período (DDL nova, convenções do tenant)
CREATE TABLE IF NOT EXISTS performance_goals (
  id          bigint unsigned NOT NULL AUTO_INCREMENT,
  uuid        char(36)     NOT NULL,
  tenant_id   char(36)     NOT NULL,
  unit_uuid   char(36)     NULL COMMENT 'NULL = meta da rede',
  metric      varchar(64)  NOT NULL COMMENT 'enrollments, revenue, attendance...',
  period_key  char(7)      NOT NULL COMMENT 'YYYY-MM',
  target      decimal(15,2) NOT NULL,
  created_at  datetime DEFAULT CURRENT_TIMESTAMP,
  updated_at  datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at  datetime DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_goals_uuid (uuid),
  KEY idx_goals (tenant_id, metric, period_key, deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Metas por unidade e período';

-- Realizado vs. meta de matrículas por unidade (tabela real + goals)
SELECT u.name AS label,
       COALESCE(g.target, 0)                       AS target,
       COUNT(e.uuid)                               AS achieved,
       ROUND(100 * COUNT(e.uuid) / NULLIF(g.target, 0), 0) AS pct_of_target
  FROM units u
  LEFT JOIN performance_goals g
         ON g.unit_uuid = u.uuid
        AND g.metric = 'enrollments'
        AND g.period_key = :period_key
        AND g.deleted_at IS NULL
  LEFT JOIN enrollments e
         ON e.unit_uuid = u.uuid
        AND e.enrollment_date >= :period_start
        AND e.enrollment_date <  :period_end
        AND e.deleted_at IS NULL
 WHERE u.tenant_id = :tenant_id
   AND u.deleted_at IS NULL
 GROUP BY u.uuid, u.name, g.target
 ORDER BY pct_of_target DESC;
```

O controller monta o array `[{label, value (pct saturado em 120), target, val, note}]` com os números formatados em pt-BR e passa em `data-bullets`.
