# Progress

Barra de progresso do runtime (`.ttsc-progress` + `.ttsc-progress-indicator`) em seis cores, com extensões TTSC para estado indeterminado e anel circular em SVG.

## Quando usar

- Mostrar uma proporção conhecida: frequência do aluno (%), ocupação da turma, parcelas pagas, etapas de um processo de matrícula concluídas.
- Mostrar uma operação em andamento sem fim conhecido (importação de planilha, geração de boletos) com a variante **indeterminada**.
- Em KPIs, use o anel **circular** ao lado do número; em linhas de tabela, a barra fina.
- Para etapas nomeadas (Dados → Documentos → Contrato) use o [Stepper](../Stepper/README.md), não uma barra.
- Para “carregando conteúdo” de um card ou lista use [Skeleton](../Skeleton/README.md); a barra é para progresso de **uma tarefa**.

## Anatomia

```
[████████████░░░░░░░░]   .ttsc-progress (trilho)  >  .ttsc-progress-indicator (preenchimento, width: N%)
  rótulo · valor          (texto fora da barra, opcional)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Trilho | `div.ttsc-progress` + `role="progressbar"` + `aria-valuenow/min/max` | sim |
| Preenchimento | `div.ttsc-progress-indicator` com `style="width: 72%"` | sim |
| Cor | `ttsc-progress-primary` · `-success` · `-warning` · `-info` · `-destructive` · `-mono` (no trilho) | não (padrão = primary) |
| Indeterminado | `ttsc-progress-indeterminate` (extensão TTSC, sem `aria-valuenow`) | não |
| Circular | `svg.ttsc-progress-ring` com `circle.ttsc-progress-ring-track` + `circle.ttsc-progress-ring-value` (extensão TTSC) | não |
| Rótulo | texto em `--ttsc-text-2` + valor em `--ttsc-text` (`tabular-nums`) | recomendado |

## Variantes

| Variante | Classe | Uso | Tokens |
|---|---|---|---|
| Primary | `ttsc-progress-primary` (padrão) | progresso neutro, upload | indicador `--primary` = `ttsc-accent` |
| Success | `ttsc-progress-success` | frequência ≥ 75% (regular) | `ttsc-success` (ponte TTSC; runtime usa `--color-green-500`) |
| Warning | `ttsc-progress-warning` | frequência entre 60% e 75% (alerta) | `ttsc-warning` |
| Destructive | `ttsc-progress-destructive` | frequência < 60% (risco de reprovação) | `--destructive` = `ttsc-danger` |
| Info | `ttsc-progress-info` | processos informativos | `ttsc-info` (ponte TTSC; runtime usa violeta) |
| Mono | `ttsc-progress-mono` | gráficos discretos | `--mono` = `ttsc-text` |
| Trilho | — | — | `--secondary` = `ttsc-surface-2`, altura 4px, `radius-pill` |

## Estados

| Estado | Como aplicar |
|---|---|
| Determinado | `style="width: N%"` no indicador + `aria-valuenow="N"` |
| Indeterminado | `ttsc-progress-indeterminate` no trilho, remova `aria-valuenow` e adicione `aria-busy="true"` |
| Concluído | troque a cor para `ttsc-progress-success` e o rótulo para “Concluído” |
| Faixa (regra de negócio) | 75% é o mínimo legal de frequência (LDB art. 24, VI); use `success` ≥ 75, `warning` 60–74, `destructive` < 60 |

## API

Componente **somente CSS** — o ttscui não registra JS para progress (não existe `data-ttsc-progress`). O valor é controlado pelo `width` inline do indicador. A API programática abaixo é implementação TTSC (`assets/js/core/ttsc.progress.js`):

| Função | Efeito |
|---|---|
| `TTSCProgress.set(el, value)` | atualiza `width`, `aria-valuenow`, texto `[data-progress-value]` e a cor pela faixa de frequência |
| `TTSCProgress.ring(svg, value)` | atualiza `stroke-dashoffset` do anel circular |
| Evento `ttsc.progress.change` | disparado no trilho com `detail: { value }` |

## Acessibilidade

- Sempre `role="progressbar"`, `aria-valuemin="0"`, `aria-valuemax="100"`, `aria-valuenow` e um nome (`aria-label` ou `aria-labelledby` apontando para o rótulo).
- A cor não pode ser a única informação: mostre o número (“58%”) e, em risco, um texto (“Abaixo do mínimo”).
- Texto do valor em `--ttsc-text` (≥ 12:1); legenda em `--ttsc-text-2`. Nunca escreva o número em `--ttsc-accent` (2:1) — se quiser verde, use `--ttsc-accent-text`.
- Indeterminado: `aria-busy="true"` no container que está carregando; respeite `prefers-reduced-motion` (a animação para).

## Modelos

### HTML

```html
<!-- Frequência por matrícula (linha de lista do diário de classe) -->
<div class="flex flex-col gap-1">
  <div class="flex items-center justify-between text-xs">
    <span id="freq-label-2026001" style="color: var(--ttsc-text-2)">Ana Beatriz Moreira · 2026001</span>
    <span data-progress-value style="color: var(--ttsc-text); font-variant-numeric: tabular-nums">82%</span>
  </div>
  <div class="ttsc-progress ttsc-progress-success" role="progressbar"
       aria-labelledby="freq-label-2026001" aria-valuemin="0" aria-valuemax="100" aria-valuenow="82">
    <div class="ttsc-progress-indicator" style="width: 82%"></div>
  </div>
</div>

<!-- Indeterminado: importação de alunos -->
<div class="ttsc-progress ttsc-progress-indeterminate" role="progressbar" aria-label="Importando planilha de alunos" aria-busy="true">
  <div class="ttsc-progress-indicator"></div>
</div>

<!-- Circular (KPI de frequência média da turma) -->
<svg class="ttsc-progress-ring" viewBox="0 0 40 40" width="56" height="56" role="progressbar"
     aria-label="Frequência média da turma" aria-valuemin="0" aria-valuemax="100" aria-valuenow="76">
  <circle class="ttsc-progress-ring-track" cx="20" cy="20" r="17"></circle>
  <circle class="ttsc-progress-ring-value" cx="20" cy="20" r="17" pathLength="100" style="stroke-dashoffset: 24"></circle>
  <text x="20" y="20" class="ttsc-progress-ring-label">76%</text>
</svg>
```

### CSS

```css
/* Ponte (bundle.css): trilho = --secondary, indicador = --primary */
:root { --secondary: var(--ttsc-surface-2); --primary: var(--ttsc-accent); }

/* Cores do runtime ligadas aos tokens semânticos do TotusTuus */
.ttsc-progress-success .ttsc-progress-indicator { background-color: var(--ttsc-success); }
.ttsc-progress-warning .ttsc-progress-indicator { background-color: var(--ttsc-warning); }
.ttsc-progress-info    .ttsc-progress-indicator { background-color: var(--ttsc-info); }
.ttsc-progress-lg { height: var(--ttsc-space-2); }

/* Extensão TTSC: indeterminado */
.ttsc-progress-indeterminate .ttsc-progress-indicator {
  position: absolute; inset-block: 0; width: 40%;
  animation: ttsc-progress-slide 1.2s var(--ttsc-ease, ease-in-out) infinite;
}
@keyframes ttsc-progress-slide { from { left: -40%; } to { left: 100%; } }
@media (prefers-reduced-motion: reduce) {
  .ttsc-progress-indeterminate .ttsc-progress-indicator { animation: none; left: 0; width: 100%; opacity: .5; }
}

/* Extensão TTSC: anel circular em SVG (pathLength=100 → offset = 100 - valor) */
.ttsc-progress-ring { transform: rotate(-90deg); }
.ttsc-progress-ring circle { fill: none; stroke-width: 4; }
.ttsc-progress-ring-track { stroke: var(--ttsc-surface-2); }
.ttsc-progress-ring-value { stroke: var(--ttsc-accent); stroke-linecap: round; stroke-dasharray: 100; transition: stroke-dashoffset .4s var(--ttsc-ease, ease); }
.ttsc-progress-ring-label { transform: rotate(90deg); transform-origin: center; fill: var(--ttsc-text); font-size: 10px; font-weight: 600; text-anchor: middle; dominant-baseline: central; }
```

### JS

```js
// assets/js/core/ttsc.progress.js — implementação TTSC (o ttscui não tem módulo progress)
(function (w) {
  var COLORS = ['ttsc-progress-success', 'ttsc-progress-warning', 'ttsc-progress-destructive', 'ttsc-progress-primary'];

  function bandFor(value) {            // regra de frequência mínima (75%)
    if (value >= 75) return 'ttsc-progress-success';
    if (value >= 60) return 'ttsc-progress-warning';
    return 'ttsc-progress-destructive';
  }

  function set(el, value, opts) {
    opts = opts || {};
    var v = Math.max(0, Math.min(100, Math.round(Number(value) || 0)));
    var bar = el.querySelector('.ttsc-progress-indicator');
    if (bar) bar.style.width = v + '%';
    el.setAttribute('aria-valuenow', String(v));
    if (opts.attendance) {
      COLORS.forEach(function (c) { el.classList.remove(c); });
      el.classList.add(bandFor(v));
    }
    var label = el.parentElement && el.parentElement.querySelector('[data-progress-value]');
    if (label) label.textContent = v + '%';
    el.dispatchEvent(new CustomEvent('ttsc.progress.change', { bubbles: true, detail: { value: v } }));
  }

  function ring(svg, value) {
    var v = Math.max(0, Math.min(100, Number(value) || 0));
    svg.querySelector('.ttsc-progress-ring-value').style.strokeDashoffset = String(100 - v);
    svg.setAttribute('aria-valuenow', String(v));
    var t = svg.querySelector('.ttsc-progress-ring-label');
    if (t) t.textContent = Math.round(v) + '%';
  }

  w.TTSCProgress = { set: set, ring: ring, bandFor: bandFor };
})(window);

// Atualiza as barras da tela de frequência com o JSON do endpoint
fetch('/app/academic/attendance/summary?class_uuid=' + encodeURIComponent(classUuid), { headers: { Accept: 'application/json' } })
  .then(function (r) { return r.json(); })
  .then(function (rows) {
    rows.forEach(function (row) {
      var el = document.querySelector('[data-enrollment="' + row.enrollment_uuid + '"] .ttsc-progress');
      if (el) TTSCProgress.set(el, row.attendance_pct ?? 0, { attendance: true });
    });
  });
```

### SQL

Percentual de frequência por matrícula de uma turma (presença, atraso e falta justificada contam como frequentes):

```sql
-- MariaDB 10.11 / MySQL 8 — banco do tenant
SELECT e.uuid  AS enrollment_uuid,
       e.code  AS enrollment_code,
       u.name  AS student_name,
       COUNT(a.uuid) AS total_lessons,
       SUM(a.status IN ('present', 'late', 'justified')) AS attended,
       ROUND(100 * SUM(a.status IN ('present', 'late', 'justified'))
             / NULLIF(COUNT(a.uuid), 0), 1) AS attendance_pct
  FROM enrollments e
  JOIN users u           ON u.uuid = e.student_uuid
  LEFT JOIN attendance a ON a.enrollment_uuid = e.uuid
 WHERE e.class_uuid = :class_uuid
   AND e.status = 'active'
   AND e.deleted_at IS NULL
 GROUP BY e.uuid, e.code, u.name
 ORDER BY attendance_pct ASC;
```

O controller entrega as linhas à view Plates; cada linha vira um `.ttsc-progress` com `width: <?= (float) $row['attendance_pct'] ?>%` e a classe de cor calculada no PHP pela mesma regra de `bandFor()` (`attendance_pct` nulo = sem aulas lançadas: mostre “—” e não a barra).

## Faça / Não faça

- **Faça:** mostre o número ao lado da barra e use a faixa de cor da regra de 75%.
- **Faça:** use o anel circular apenas em KPIs (um por card).
- **Não faça:** barra sem `role="progressbar"` e sem valor; texto verde `--ttsc-accent` sobre fundo claro.
- **Não faça:** barra indeterminada para operações que duram menos de 1 s (use o estado de carregamento do [Button](../Button/README.md)).
