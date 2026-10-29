# CountUp

Animação de contagem numérica com countUp.js 2.8.0 (`countUp.CountUp`) para valores de KPI em pt-BR — separador de milhar `.`, decimal `,`, prefixo `R$ ` e sufixo `%`.

## Quando usar

- Número principal de um card de KPI em dashboard (matrículas ativas, receita do mês, adimplência), na primeira exibição ou quando o valor é atualizado em tempo real (`update()`).
- Com `enableScrollSpy` para KPIs abaixo da dobra (anima ao entrar na tela).
- **Não use** em células de tabela, formulários ou valores que o usuário precisa ler/copiar imediatamente (extratos, boletos): mostre o número formatado direto.
- **Não use** para progresso de uma tarefa: use `ttsc-progress`. O card completo do KPI é o [KpiCard](../KpiCard/README.md); o CountUp anima só o número dentro dele.

## Anatomia

```
.ttsc-kpi-card
├── cabeçalho: rótulo "Receita do mês"  + ícone fa-light
├── [data-countup="386452.9" data-decimals="2" data-prefix="R$ "]  → "R$ 386.452,90"
└── variação: "+R$ 12.310,00 vs. set."
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Alvo | elemento com `data-countup="<número final, ponto decimal>"` | sim |
| Casas decimais | `data-decimals` (`0` padrão, `2` para moeda, `1` para %) | não |
| Prefixo / sufixo | `data-prefix="R$ "` · `data-suffix="%"` | não |
| Valor acessível | `aria-label` com o valor final já formatado | sim |
| Números tabulares | `font-variant-numeric: tabular-nums` (evita “tremer”) | sim |

## Variantes

| Variante | Opções | Exemplo | Tokens |
|---|---|---|---|
| Inteiro | `decimalPlaces: 0` | `1.248` matrículas | valor `ttsc-text` 22/28 600 |
| Moeda BRL | `decimalPlaces: 2, prefix: 'R$ '` | `R$ 386.452,90` | idem |
| Percentual | `decimalPlaces: 1, suffix: '%'` | `93,7%` | idem |
| Variação positiva | texto fora do CountUp | `+4,2%` | `ttsc-accent-text` |
| Variação negativa | texto fora do CountUp | `−0,8 p.p.` | `ttsc-danger-text` |

## API

### Opções (`new countUp.CountUp(target, endVal, options)`)

| Opção | Padrão | Valor TTSC |
|---|---|---|
| `startVal` | `0` | `0` (ou o valor anterior em atualizações) |
| `decimalPlaces` | `0` | `data-decimals` |
| `duration` | `2` (s) | `1.2`; `0` com `prefers-reduced-motion` |
| `useGrouping` | `true` | `true` |
| `separator` | `','` | `'.'` |
| `decimal` | `'.'` | `','` |
| `prefix` / `suffix` | `''` | `'R$ '` / `'%'` |
| `useEasing` / `easingFn` | `true` / easeOutExpo | padrão |
| `smartEasingThreshold` / `smartEasingAmount` | `999` / `333` | padrão |
| `enableScrollSpy` / `scrollSpyDelay` / `scrollSpyOnce` | `false` / `200` / `false` | `true` / `200` / `true` abaixo da dobra |
| `formattingFn` | — | só se precisar de `Intl.NumberFormat` customizado |
| `onStartCallback` / `onCompleteCallback` | — | ex.: revelar a variação ao fim |

### Métodos e propriedades

| Método | Efeito |
|---|---|
| `start(callback?)` | inicia a animação |
| `pauseResume()` | pausa/retoma |
| `reset()` | volta ao `startVal` sem animar |
| `update(newEndVal)` | anima do valor atual até o novo (tempo real) |
| `error` | string não vazia se o alvo/valor for inválido — mostre o valor estático |
| `countUp.CountUp.version` | `"2.8.0"` |

## Acessibilidade

- Leitores de tela leem o texto intermediário; por isso o alvo carrega `aria-label` com o valor final formatado e o card não é `aria-live`.
- Respeite `prefers-reduced-motion: reduce` com `duration: 0`.
- Contraste: valor em `ttsc-text`, rótulo em `ttsc-text-muted`, variação em `ttsc-accent-text`/`ttsc-danger-text` (≥ 4,5:1). Nunca `ttsc-accent` como cor de número.
- O número final precisa existir sem JS: o PHP imprime o valor formatado e o JS só reanima (progressive enhancement).

## Modelos

### HTML

```html
<?php $brl = fn($v) => 'R$ ' . number_format((float) $v, 2, ',', '.'); ?>
<div class="ttsc-card ttsc-kpi-card">
  <div class="ttsc-card-content">
    <div class="ttsc-kpi-head">Receita do mês <i class="fa-light fa-sack-dollar"></i></div>
    <div class="ttsc-kpi-value" data-countup="<?= (float) $kpi['revenue_month'] ?>"
         data-decimals="2" data-prefix="R$ " aria-label="<?= $brl($kpi['revenue_month']) ?> de receita no mês">
      <?= $brl($kpi['revenue_month']) ?>
    </div>
  </div>
</div>

<div class="ttsc-kpi-value" data-countup="<?= (int) $kpi['active_enrollments'] ?>"
     aria-label="<?= number_format((int) $kpi['active_enrollments'], 0, ',', '.') ?> matrículas ativas">
  <?= number_format((int) $kpi['active_enrollments'], 0, ',', '.') ?>
</div>
```

### CSS

```css
.ttsc-kpi-head  { display: flex; justify-content: space-between; font-size: 12px; color: var(--ttsc-text-muted); }
.ttsc-kpi-value { font-size: 22px; line-height: 28px; font-weight: 600; color: var(--ttsc-text); font-variant-numeric: tabular-nums; }
.ttsc-kpi-delta.is-up   { color: var(--ttsc-accent-text); }
.ttsc-kpi-delta.is-down { color: var(--ttsc-danger-text); }
```

### JS

```js
// assets/js/core/ttsc.countup.js — requer /assets/vendors/countup/countUp.umd.js (global countUp)
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const registry = new WeakMap();

export function initCountUps(root = document) {
  root.querySelectorAll('[data-countup]').forEach((el) => {
    if (registry.has(el)) return;
    const counter = new countUp.CountUp(el, parseFloat(el.dataset.countup), {
      decimalPlaces: parseInt(el.dataset.decimals || '0', 10),
      separator: '.',
      decimal: ',',
      prefix: el.dataset.prefix || '',
      suffix: el.dataset.suffix || '',
      duration: reduceMotion ? 0 : 1.2,
      enableScrollSpy: el.hasAttribute('data-countup-spy'),
      scrollSpyOnce: true,
    });
    if (counter.error) { console.warn(counter.error); return; } // mantém o valor impresso pelo PHP
    registry.set(el, counter);
    if (!el.hasAttribute('data-countup-spy')) counter.start();
  });
}

// Atualização em tempo real (ex.: polling do dashboard a cada 60 s)
export function updateCountUp(el, value) {
  const counter = registry.get(el);
  if (counter) counter.update(value);
  el.dataset.countup = value;
}

document.addEventListener('DOMContentLoaded', () => initCountUps());
```

### SQL

KPIs do dashboard acadêmico/financeiro, numa única ida ao banco (cada subconsulta filtra soft delete):

```sql
SELECT
  (SELECT COUNT(*)
     FROM enrollments e
    WHERE e.deleted_at IS NULL
      AND e.status = 'active'
      AND e.unit_uuid = :unit_uuid)                                         AS active_enrollments,
  (SELECT COALESCE(SUM(r.amount_paid), 0)
     FROM financial_receivables r
    WHERE r.deleted_at IS NULL
      AND r.status IN ('paid', 'partial')
      AND r.payment_date >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
      AND r.payment_date <  DATE_FORMAT(CURDATE() + INTERVAL 1 MONTH, '%Y-%m-01')) AS revenue_month,
  (SELECT ROUND(100 * SUM(r.status = 'paid') / NULLIF(COUNT(*), 0), 1)
     FROM financial_receivables r
    WHERE r.deleted_at IS NULL
      AND r.due_date < CURDATE())                                           AS paid_rate;
```

O controller passa a linha para a view; o PHP imprime o valor formatado (fallback) e o número cru em `data-countup` (ponto decimal, sem separador). `paid_rate` pode vir `NULL` sem títulos — trate como `0`.

## Faça / Não faça

- **Faça:** `separator: '.'`, `decimal: ','`, prefixo `R$ ` com espaço, `tabular-nums`.
- **Faça:** imprimir o valor final no HTML e usar `aria-label`; `update()` em vez de recriar a instância.
- **Não faça:** animar dezenas de números na mesma tela — limite aos 4–6 KPIs do topo.
- **Não faça:** passar string formatada (`"1.248"`) em `data-countup`: seria lido como `1,248`.
- **Não faça:** durações longas (> 2 s) ou repetir a animação a cada polling sem mudança de valor.
