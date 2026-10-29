# KpiGoalCard

Indicador com meta e visualização de apoio: valor atual, variação, barra até a meta com o quanto falta e um espaço opcional para uma visualização pequena (pontos, etapas de funil). Diferente do cartão de meta, este mostra o volume ("41 de 48") e pode trazer a etapa ou o detalhe em uma visualização.

## Quando usar

- Volume contra meta, onde o número absoluto importa ("2.846 de 3.200 pré-matrículas").
- Quando o detalhe cabe em uma visualização pequena: quantos de quantos estão ativos (pontos) ou em qual etapa estão as pessoas (funil).
- Para só a meta com valor percentual, prefira [MetaProgressCard](../MetaProgressCard/README.md).

## Anatomia

```
Pré-matrículas 2027                      ↑ 9,3%
2.846
184 novas esta semana
89% de 3.200                          faltam 11%
[████████████████████████████░░░]
──────────────────────────────────────
[184 Interesse][96 Visita][41 Proposta][18 Matric.]
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Cartão | `article.kg` com `aria-labelledby` | sim |
| Título e ícone | `.kg-title` com `.kg-ic` | sim |
| Variação | `.kg-delta` | recomendado |
| Valor | `.kg-val` (volume com "de N" quando couber) | sim |
| Meta | `.kg-goal` (percentual e quanto falta) + `.kg-bar` com `--p` | sim |
| Visualização | `.kg-viz` com `.kg-dots` ou `.kg-chev` (opcional) | não |

## Variantes / Estados

- **Pontos (`.kg-dots`):** um ponto por unidade; `.on` marca as ativas. Até 48 pontos cabem em 12 colunas.
- **Etapas (`.kg-chev`):** lista de etapas em forma de chevron; a cor fica mais escura a cada etapa (`--i`).
- **Sem visualização:** remova `.kg-viz`; o cartão continua completo.

## API

| Atributo | Efeito |
|---|---|
| `--p` no `.kg-bar` | percentual da meta atingido (0–100) |
| `.on` em `.kg-dots i` | unidade ativa |
| `--i` em `.kg-chev li` | posição da etapa (0 a 3) |

## Acessibilidade

- A visualização é decorativa (`aria-hidden`) quando o número já aparece no texto; a barra tem `role="img"` com o valor por extenso.
- As etapas do funil são uma lista ordenada com `aria-label`, e cada etapa diz seu número e seu nome.
- "faltam 11%" é texto, não cor.

## Modelos

### HTML

```html
<article class="kg" aria-labelledby="kg-2">
  <div class="kg-head"><p class="kg-title" id="kg-2">Pré-matrículas 2027</p><span class="kg-delta">↑ 9,3%</span></div>
  <div class="kg-val">2.846</div>
  <div class="kg-goal"><span>89% de 3.200</span><b>faltam 11%</b></div>
  <div class="kg-bar" role="img" aria-label="2.846 de 3.200, 89%" style="--p:89"><i></i></div>
</article>
```

### CSS

Classes `.kg*`. A barra e os pontos usam `--ttsc-accent` e `--ttsc-surface-2`; as etapas do funil escurecem com `--i`.

### JS

```js
// Atualiza o cartão com o valor e a meta vindos do servidor
function atualizarKpi(card, { valor, meta }) {
  const pct = Math.min(100, Math.round((valor / meta) * 100));
  card.querySelector('.kg-val').textContent = valor.toLocaleString('pt-BR');
  card.querySelector('.kg-goal span').textContent = `${pct}% de ${meta.toLocaleString('pt-BR')}`;
  card.querySelector('.kg-goal b').textContent = `faltam ${100 - pct}%`;
  card.querySelector('.kg-bar').style.setProperty('--p', pct);
}
```

### SQL

Pré-matrículas do período e situação por etapa (para o funil e o valor do cartão):

```sql
SELECT COUNT(*) AS total,
       SUM(e.status = 'active') AS matriculadas,
       SUM(e.status = 'pending') AS pendentes
  FROM enrollments e
 WHERE e.deleted_at IS NULL
   AND e.period_uuid = ?;
```

## Faça / Não faça

- Faça: mostre o volume e a meta juntos ("2.846 de 3.200").
- Faça: use no máximo uma visualização por cartão.
- Não faça: mostrar a porcentagem sem a meta; o leitor não sabe se é bom.
