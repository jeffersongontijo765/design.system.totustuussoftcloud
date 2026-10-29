# MetaProgressCard

Cartão de indicador com meta: valor principal, barra de progresso com um marcador na meta, a diferença em relação a ela e uma linha de contexto. Usado para indicadores que têm um objetivo definido (frequência contra 75%, aprovação contra 85%, adimplência contra 90%).

## Quando usar

- O indicador tem uma meta oficial ou um limite (frequência mínima, taxa de adimplência, metas do plano de ensino).
- A pergunta do leitor é "estamos perto da meta?", não só "quanto é?".
- Para um indicador sem meta, use um cartão de métrica simples; para meta com valor próximo de 100%, use [KpiGoalCard](../KpiGoalCard/README.md) que mostra também o volume.

## Anatomia

```
Frequência geral                               [↗]
96,1%
[████████████████████████████▌ ▏ ]   ← marcador na meta (95%)
Meta 95% · 1,1 pt acima                     +1,4 pt
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Cartão | `article.mp` | sim |
| Rótulo | `p.mp-label` com `id` (nome do cartão) | sim |
| Valor | `.mp-value` | sim |
| Barra | `.mp-track` com `--p` (valor), `--t` (meta) e `role="img"` + `aria-label` | sim |
| Marcador da meta | `.mp-track b` | sim |
| Rodapé | `.mp-foot` com a diferença para a meta e a variação | recomendado |

## Variantes / Estados

- **Na meta ou acima:** barra em `--ttsc-accent`, rodapé neutro.
- **Abaixo da meta:** `.is-below` pinta a barra e o rodapé de âmbar; o texto diz quanto falta.
- **Variação negativa:** `.mp-delta.down` em vermelho, com sinal "−".
- **Grade:** três colunas, duas em telas médias, uma no celular.

## API

| Atributo | Efeito |
|---|---|
| `--p` no `.mp-track` | valor atual em percentual (0–100) |
| `--t` no `.mp-track` | posição da meta em percentual (0–100) |
| `.is-below` no `article` | estado abaixo da meta |

## Acessibilidade

- O valor e a meta ficam em texto; a cor não é o único indicador de "abaixo da meta" (há o texto "faltam 6,6 pt").
- A barra tem `role="img"` com `aria-label` que cita valor e meta.
- O cartão é `article` com nome próprio (`aria-labelledby`).

## Modelos

### HTML

```html
<article class="mp is-below" aria-labelledby="mp-2">
  <div class="mp-head"><p class="mp-label" id="mp-2">Aprovação no 1º ano</p></div>
  <div class="mp-value">78,4%</div>
  <div class="mp-track" role="img" aria-label="78,4% de 100%, meta de 85%" style="--p:78.4;--t:85"><i></i><b></b></div>
  <div class="mp-foot"><span>Meta 85% · faltam 6,6 pt</span><span class="mp-delta">+0,8 pt</span></div>
</article>
```

### CSS

Classes `.mp*`. A barra e o marcador usam `--ttsc-accent`, `--ttsc-warning` e `--ttsc-text`; a grade responde em três, duas e uma coluna.

### JS

```js
// Calcula a posição da barra e o texto da diferença a partir do valor e da meta
function renderMeta(el, valor, meta) {
  const diff = (valor - meta).toFixed(1).replace('.', ',');
  el.style.setProperty('--p', valor);
  el.style.setProperty('--t', meta);
  el.closest('.mp').classList.toggle('is-below', valor < meta);
  el.closest('.mp').querySelector('.mp-foot span').textContent =
    valor < meta ? `Meta ${meta}% · faltam ${Math.abs(diff).replace('-', '')} pt` : `Meta ${meta}% · ${diff} pt acima`;
}
```

### SQL

Frequência por turma no período, para comparar com a meta de 75%:

```sql
SELECT c.name AS turma,
       ROUND(100 * SUM(a.status IN ('present', 'late', 'justified')) / NULLIF(COUNT(*), 0), 1) AS frequencia
  FROM attendance a
  JOIN classes c ON c.uuid = a.class_uuid AND c.deleted_at IS NULL
 WHERE a.lesson_date BETWEEN ? AND ?
 GROUP BY c.id, c.name
 ORDER BY frequencia;
```

## Faça / Não faça

- Faça: mostre a meta no texto, não só no marcador.
- Faça: use no máximo três cartões por linha.
- Não faça: marcar "abaixo da meta" só com a cor; o texto precisa dizer quanto falta.
