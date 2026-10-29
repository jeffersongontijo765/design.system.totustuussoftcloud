# ExecutiveStrip

Faixa executiva do topo do dashboard: ticker ao vivo, score composto em anel com frentes, tiles de KPI com delta, progresso de meta, limites de orçamento e watchlist de indicadores.

> Também listado em: **Componentes do painel**.

## Quando usar

- Home de módulo ou de portal que precisa abrir com um retrato de estado: um índice composto, os indicadores do período e o que exige atenção (limite, meta, watchlist) — o padrão do topo dos dashboards de referência (Executive School Intelligence, Operations Health Score, Corporate Accounting Control Center).
- Quando o "quanto estamos bem" importa mais do que a lista de registros — e o usuário decide em segundos.
- Use as peças separadas conforme a página pede: só hero + tiles (compacta), ou hero + frentes + tiles + limites (completa).
- **Não use** para boas-vindas e contexto institucional: use [HeroBanner](../HeroBanner/README.md).
- **Não use** para faixa de KPI pura, sem score composto: use [KpiView](../KpiView/README.md).
- **Não use** para recomendações e previsões de IA: use [InsightPanel](../InsightPanel/README.md) — e pode combinar: a faixa em cima, os insights abaixo.
- Os números de amostra do preview são ilustrativos; troque por um provider do módulo antes de ir para produção.

## Anatomia

```
┌ ticker ─ AO VIVO ─ evento ─│─ evento ─│─ evento ────────────────── (rolagem) ┐
├ es-hero (anel 91/100) ─┬ es-fronts ──────────────────────────────────────────┤
│ Excelente · A+ · Top 4%│ Acadêmico     ▓▓▓▓▓▓▓▓▓░  91                          │
│ +2,3 pts vs. anterior  │ Pessoas       ▓▓▓▓▓▓▓▓▓░  88                          │
├────────────────────────┴ Financeiro    ▓▓▓▓▓▓▓▓░░  84 (abaixo da meta) ────────┤
│ [tile KPI] [tile KPI] [tile KPI] [tile KPI] [tile KPI] [tile KPI]              │
│  valor + delta + nota                                                         │
├ [progresso 62% · dia 6/10] [limites 82/100 · aviso] [watchlist Selic · chip] ──┤
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Ticker | `.es-ticker` + `.es-tape` (lista rolável) | não |
| Score | `.es-hero` + `.es-ring` (`role="img"` com resumo) | sim |
| Estado | `.es-hero .state` (chip do conceito) | sim |
| Badges | `.es-badges .badge` (ranking, conceito, streak) | não |
| Frentes | `.es-fronts .fronts` (medidores horizontais por frente) | quando houver índice composto |
| Tiles | `.es-tiles .tile` (rótulo, valor, delta, nota) | sim |
| Delta | `.d.up` / `.d.down` / `.d.flat` (ícone + texto) | sim — nunca só cor |
| Progresso | `.es-wide` com `.goal-bar` + passos ("dia X de Y") | não |
| Limites | `.limits` (rubrica, medidor, usado/limite) + `.limits-warn` | não |
| Watchlist | `.watch` (nome, valor, chip de estado) | não |
| Período | `.seg [data-period]` (Mês/Semestre) com `aria-pressed` | não |

## Variantes

| Variante | Peças | Uso |
|---|---|---|
| Completa | ticker + hero + frentes + 6 tiles + progresso + limites + watchlist | Home executiva do módulo |
| Compacta | hero + 3–4 tiles | Topo de páginas internas |
| Financeira | hero com receita líquida + índice de saúde com subnotas + tiles monetários | `/financeiro` — troque as frentes por subnotas do índice |
| Logística | hero "saúde da operação" + frentes por frente operacional + 12 tiles de operação | `/logistica` |
| Contábil | hero com filtros de período (exercício/período, entidade) + tiles + progresso de fechamento | `/contabil` — os filtros entram no cabeçalho do card |

## Estados

| Estado | Como aplicar |
|---|---|
| Carregando | `.tile` com `Skeleton` no lugar do valor e do delta; anel com traço da trilha apenas |
| Indisponível | valor `—` + nota "Indicador indisponível"; nunca esconder o tile |
| Meta atingida | delta em `ttsc-accent-text` + nota "meta atingida"; anel pode ir a 100 |
| Atenção | frente/tile abaixo da meta: medidor `warn` + nota com o que fazer (o texto carrega o estado, não a cor) |
| Ao vivo | `.live` pulsando (desliga com `prefers-reduced-motion`) e itens com "há X min" |

## Acessibilidade

- O anel é decorativo para o leitor: o container tem `role="img"` + `aria-label` com o valor e o conceito ("91 de 100, Excelente"); o número permanece visível no interior.
- Deltas nunca dependem de cor: ícone + texto ("+1,4 p.p. vs. mês"); chips de estado têm rótulo ("Alta", "Estável", "Queda").
- Medidores (frentes, limites, progresso) têm `role="img"` + `aria-label` com o número exato; o valor também está visível ao lado.
- Ticker: lista real (`ul/li`) com rolagem horizontal — não use `marquee` nem animação contínua; o ponto "AO VIVO" pulsante desliga com `prefers-reduced-motion: reduce`.
- "Atualizar" anuncia em `role="status"` (`aria-live="polite"`); o seletor de período é grupo com `aria-pressed` por botão.
- Foco visível global (`:focus-visible` com `ttsc-accent`); contraste garantido pelos tokens em claro e escuro.

## Faça / Não faça

- **Faça:** um índice composto calculado no servidor (média ponderada documentada), nunca no cliente.
- **Faça:** no máximo 6 tiles; acima disso vira parede de números — distribua em seções da página.
- **Faça:** aviso de limite sempre com texto acionável ("revise antes de novo compromisso").
- **Não faça:** tickers animados com `marquee` ou `setInterval` sem pausa; lista rolável é mais acessível.
- **Não faça:** vermelho/verde como único sinal de estado; sempre com rótulo.
- **Não faça:** repetir o mesmo KPI no hero e nos tiles.

## API

| Item | Uso |
|---|---|
| `TTSCExecutiveStrip.init(el)` | Retorna a instância (um por página) |
| `instance.setPeriod('month' \| 'semester')` | Troca o período; atualiza todo `[data-month]`/`[data-semester]` |
| `ttsc:executive-strip:period` | CustomEvent (bubbles) com `detail.period` — recarregue os dados do servidor aqui |
| `ttsc:executive-strip:refresh` | CustomEvent (bubbles) disparado pelo botão Atualizar |
| `#es-updated` (`role="status"`) | Região viva do "Atualizado há X min" |

## Modelos

### HTML

```html
<section class="es-strip" data-executive-strip
         aria-labelledby="es-hero-t">
  <section class="card es-hero">
    <div class="es-ring" role="img"
         aria-label="Índice de desempenho institucional: <?= (int) $score ?> de 100, <?= $this->e($scoreLabel) ?>.">
      <svg viewBox="0 0 120 120" aria-hidden="true">
        <circle class="track" cx="60" cy="60" r="52"></circle>
        <circle class="fill" cx="60" cy="60" r="52"
                style="stroke-dashoffset: <?= number_format(326.7 * (1 - $score / 100), 1, '.', '') ?>"></circle>
      </svg>
      <div class="val"><b><?= (int) $score ?></b><span>de 100</span></div>
    </div>
    <div class="info">
      <span class="state"><i class="fa-light fa-award" aria-hidden="true"></i> <?= $this->e($scoreLabel) ?></span>
      <h3 id="es-hero-t">Índice de desempenho institucional</h3>
      <p><?= $this->e($scoreSummary) ?></p>
      <span class="es-delta <?= $delta >= 0 ? 'up' : 'down' ?>">
        <i class="fa-light fa-arrow-trend-<?= $delta >= 0 ? 'up' : 'down' ?>" aria-hidden="true"></i>
        <?= $delta >= 0 ? '+' : '' ?><?= number_format($delta, 1, ',', '') ?> pts vs. período anterior
      </span>
    </div>
  </section>

  <ul class="es-tiles" aria-label="Indicadores do período">
    <?php foreach ($tiles as $t): ?>
    <li class="card tile">
      <span class="lbl"><?= $this->e($t['label']) ?></span>
      <span class="val" data-month="<?= $this->e($t['month']) ?>" data-semester="<?= $this->e($t['semester']) ?>"><?= $this->e($t['month']) ?></span>
      <span class="d <?= $this->e($t['trend']) ?>">
        <i class="fa-light fa-arrow-trend-<?= $t['trend'] === 'up' ? 'up' : ($t['trend'] === 'down' ? 'down' : 'minus') ?>" aria-hidden="true"></i>
        <span data-month="<?= $this->e($t['delta_month']) ?>" data-semester="<?= $this->e($t['delta_semester']) ?>"><?= $this->e($t['delta_month']) ?></span>
      </span>
      <span class="note"><?= $this->e($t['note']) ?></span>
    </li>
    <?php endforeach; ?>
  </ul>
</section>
```

### CSS

```css
/* Faixa executiva — extensão de página, tokens obrigatórios. Sem cores literais. */
.es-strip{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:14px}
.es-hero{grid-column:span 5;padding:16px;display:flex;gap:16px;align-items:center}
.es-ring{position:relative;width:128px;height:128px;flex:0 0 auto}
.es-ring .track{stroke:var(--ttsc-surface-2);fill:none;stroke-width:10}
.es-ring .fill{stroke:var(--ttsc-accent);fill:none;stroke-width:10;stroke-linecap:round;
  stroke-dasharray:326.7} /* 2πr, r=52 */
.es-tiles{grid-column:span 12;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:14px;list-style:none;margin:0;padding:0}
.tile .val{font-size:22px;font-weight:700;color:var(--ttsc-text);font-variant-numeric:tabular-nums}
.tile .d.up{color:var(--ttsc-accent-text)} .tile .d.down{color:var(--ttsc-danger-text)}
@media (prefers-reduced-motion: reduce){ .live::before{animation:none} }
@media (max-width:1024px){ .es-tiles{grid-template-columns:repeat(3,minmax(0,1fr))} }
@media (max-width:640px){ .es-tiles{grid-template-columns:repeat(2,minmax(0,1fr))} }
```

### JS

```js
// assets/js/core/ttsc.executive-strip.js
window.TTSCExecutiveStrip = (function () {
  function Strip(root) {
    this.root = root;
    var self = this;
    root.querySelectorAll('[data-period]').forEach(function (btn) {
      btn.addEventListener('click', function () { self.setPeriod(btn.getAttribute('data-period')); });
    });
    var updated = root.querySelector('[role="status"]');
    root.querySelector('[data-refresh]').addEventListener('click', function () {
      if (updated) updated.textContent = 'Atualizado agora · ' + new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
      root.dispatchEvent(new CustomEvent('ttsc:executive-strip:refresh', { bubbles: true }));
    });
  }
  Strip.prototype.setPeriod = function (period) {
    var root = this.root;
    root.querySelectorAll('[data-period]').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-period') === period ? 'true' : 'false');
    });
    root.querySelectorAll('[data-' + period + ']').forEach(function (el) {
      el.textContent = el.getAttribute('data-' + period);
    });
    // Recarregue os dados reais do servidor aqui (fetch com AbortController e credenciais same-origin).
    root.dispatchEvent(new CustomEvent('ttsc:executive-strip:period', { bubbles: true, detail: { period: period } }));
  };
  return { init: function (el) { return new Strip(el); } };
})();
document.querySelectorAll('[data-executive-strip]').forEach(function (el) { window.TTSCExecutiveStrip.init(el); });
```

### SQL

O índice composto e os tiles vêm de um snapshot diário — não recalculados a cada visita. Frequência usa tabela real do tenant; arrecadação e orçamento vêm do módulo financeiro (ajuste os nomes de tabela ao seu repositório).

```sql
-- Snapshot do índice composto (DDL nova, convenções do tenant)
CREATE TABLE IF NOT EXISTS exec_metric_snapshots (
  id          bigint unsigned NOT NULL AUTO_INCREMENT,
  uuid        char(36)     NOT NULL,
  tenant_id   char(36)     NOT NULL,
  unit_uuid   char(36)     DEFAULT NULL COMMENT 'NULL = consolidação da rede',
  period_key  char(7)      NOT NULL COMMENT 'YYYY-MM',
  score       tinyint unsigned NOT NULL,
  fronts      json         NOT NULL COMMENT '{"academic":91,"people":88,"finance":84,"infra":79}',
  delta_score decimal(5,1) NOT NULL DEFAULT 0.0 COMMENT 'vs. snapshot anterior',
  created_at  datetime DEFAULT CURRENT_TIMESTAMP,
  updated_at  datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at  datetime DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_exec_snap_uuid (uuid),
  KEY idx_exec_snap (tenant_id, unit_uuid, period_key, deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Snapshots do painel executivo, calculados por job diário';

-- Frequência média do mês (tabela real do tenant)
SELECT ROUND(100 * SUM(a.status IN ('present', 'late', 'justified')) / COUNT(*), 1) AS attendance_pct
  FROM attendance a
  JOIN enrollments e ON e.uuid = a.enrollment_uuid AND e.deleted_at IS NULL
 WHERE a.lesson_date >= :month_start AND a.lesson_date < :month_end
   AND e.unit_uuid = :unit_uuid;

-- Último snapshot do índice + delta vs. anterior (função de janela: MariaDB 10.2+ / MySQL 8)
SELECT s.period_key, s.score, s.fronts,
       s.score - LAG(s.score) OVER (ORDER BY s.period_key) AS delta_score
  FROM exec_metric_snapshots s
 WHERE s.tenant_id = :tenant_id
   AND (s.unit_uuid = :unit_uuid OR s.unit_uuid IS NULL)
   AND s.deleted_at IS NULL
 ORDER BY s.period_key DESC
 LIMIT 12;
```

O job diário grava o snapshot com a média ponderada documentada (pesos por frente no repositório do módulo); a view lê apenas o último registro por período.
