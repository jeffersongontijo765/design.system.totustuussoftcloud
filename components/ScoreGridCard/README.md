# ScoreGridCard

Painel de índice: uma nota geral grande com classificação, ranking e resumo de um lado, e uma grade de métricas do outro. Cada métrica tem valor, barra, e uma linha de contexto que diz o que está acontecendo ("18 famílias em atraso"). Usado para a visão geral da escola ou da unidade.

## Quando usar

- Visão executiva de uma escola ou unidade, com uma nota que resume vários indicadores.
- Quando a diretoria precisa ver em uma tela o que está bem e o que exige ação.
- Para uma meta única, use [MetaProgressCard](../MetaProgressCard/README.md); para um KPI com volume e visualização, use [KpiGoalCard](../KpiGoalCard/README.md).

## Anatomia

```
┌──────────────────┬──────────────────────────────────────┐
│ [Excelente]      │ Frequência   Desempenho   Aprovação  │
│   (troféu)       │ 96,1%        92,4%        97,8%      │
│ 98%              │ ▓▓▓▓▓▓▓▓     ▓▓▓▓▓▓▓▓     ▓▓▓▓▓▓▓▓    │
│ Índice da escola │ ↑1,4 pt      ↑3,1 pt      ↑0,6 pt    │
│ [#3][6][A+]      │ Adimplência  Segurança    Engajamento│
│                  │ 82,3% ⚠      99,2%        88,6%      │
└──────────────────┴──────────────────────────────────────┘
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Contêiner | `section.sg` | sim |
| Painel da nota | `.sg-score` com `.sg-num`, `.sg-cap`, `.sg-chips` | sim |
| Selo | `.sg-badge` (classificação textual) | recomendado |
| Grade | `.sg-grid` com `article.sg-tile` | sim |
| Métrica | `.sg-tile-label`, `.sg-tile-val`, `.sg-bar` (`--p`), `.sg-ctx` | sim |
| Alerta | `.sg-tile.is-warn` com `.sg-ctx.warn` | quando houver pendência |

## Variantes / Estados

- **Métrica em dia:** barra em `--ttsc-accent`, contexto com `.ok`.
- **Métrica com pendência:** `.is-warn` pinta barra e valor de âmbar; o contexto diz o que é a pendência.
- **Sem ranking:** remova a linha de "#3" e mantenha os outros chips.
- **Telas médias:** a grade vira duas colunas; no celular, uma coluna e o painel da nota fica acima.

## API

| Atributo | Efeito |
|---|---|
| `--p` no `.sg-bar` | valor de 0 a 100 |
| `.is-warn` no `article.sg-tile` | métrica com pendência |
| `aria-label` no `.sg-bar` | valor por extenso para leitor de tela |

## Acessibilidade

- O valor e o contexto estão em texto; a pendência não depende da cor (diz "18 famílias em atraso").
- Cada barra tem `role="img"` com `aria-label` com o nome e o valor.
- A nota geral tem `aria-label` no bloco ("98 por cento").

## Modelos

### HTML

```html
<section class="sg" aria-label="Índice de desempenho da escola">
  <div class="sg-score">
    <div class="sg-num"><span>98</span><small>%</small></div>
    <p class="sg-cap">Índice de desempenho da escola</p>
  </div>
  <div class="sg-grid">
    <article class="sg-tile is-warn">
      <div class="sg-tile-head"><p class="sg-tile-label">Adimplência</p></div>
      <div class="sg-tile-val">82,3%</div>
      <div class="sg-bar" role="img" aria-label="Adimplência 82,3%" style="--p:82.3"><i></i></div>
      <div class="sg-ctx warn">18 famílias em atraso · vence 15/ago</div>
    </article>
  </div>
</section>
```

### CSS

Classes `.sg*`. O painel da nota usa `--ttsc-accent` e `--ttsc-accent-on`; as métricas usam tokens de superfície e de aviso. A grade responde em três, duas e uma coluna.

### JS

```js
// Preenche a grade a partir do endpoint do índice; o painel recebe a nota e as métricas
async function carregarIndice(escolaId) {
  const res = await fetch(`/api/v1/escolas/${escolaId}/indice`, { headers: { Accept: 'application/json' } });
  if (!res.ok) throw new Error('Não foi possível carregar o índice');
  const { nota, classificacao, metricas } = await res.json();
  document.querySelector('.sg-num span').textContent = nota;
  document.querySelector('.sg-badge').textContent = classificacao;
  // cada métrica chega com nome, valor, posição e contexto
  document.querySelector('.sg-grid').replaceChildren(...metricas.map(montarTile));
}
```

A função `montarTile` (não listada) cria `article.sg-tile` com `textContent` para nome e contexto, e marca `is-warn` quando a métrica tem pendência.

### SQL

Adimplência (valor recebido sobre valor devido) e famílias em atraso no período:

```sql
SELECT ROUND(100 * SUM(r.amount_paid) / NULLIF(SUM(r.net_amount), 0), 1) AS adimplencia,
       COUNT(DISTINCT CASE WHEN r.status = 'overdue' THEN r.customer_id END) AS familias_em_atraso
  FROM financial_receivables r
 WHERE r.deleted_at IS NULL
   AND r.due_date BETWEEN ? AND ?;
```

## Faça / Não faça

- Faça: escreva o contexto de cada métrica com a pendência e o prazo.
- Faça: use até seis métricas; mais que isso vai para uma tela de detalhe.
- Não faça: mostrar nota sem a base de cálculo (quais indicadores entram).
