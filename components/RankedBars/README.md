# RankedBars

Lista ordenada em que cada item mostra posição, nome, valor e uma barra proporcional. Serve para comparar itens de uma mesma métrica e destacar os extremos.

## Quando usar

- Ranking de turmas por ocupação, cursos por matrículas, professores por carga.
- Quando a posição importa e os valores podem ser comparados diretamente.
- Para comparar etapas de um processo (que só diminuem), prefira [FunnelBars](../FunnelBars/README.md).
- Quando cada valor tem uma meta e faixas de referência (realizado vs. meta), prefira [BulletChart](../BulletChart/README.md).

## Anatomia

```
(1) 1º A · Manhã                         38/40  95%
    ██████████████████████████████████████████░░
(2) 2º B · Tarde                         34/40  85%
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Lista | `ol.ranked` | sim |
| Posição | `.ranked-pos` | sim |
| Nome e subtítulo | `.ranked-name` com `small` | sim |
| Valor e percentual | `.ranked-value` com `small` | recomendado |
| Barra | `.ranked-bar > i` com `--p` (0–100) | sim |
| Estado | `li.is-warn` (amarelo), `li.is-bad` (vermelho) | não |

## Variantes / Estados

- **Destaque do primeiro:** o primeiro item recebe a cor de destaque automaticamente.
- **Alerta:** `.is-warn` e `.is-bad` trocam a cor da barra. Use só quando houver uma regra clara (abaixo de 60%, por exemplo).

## API

| Atributo | Efeito |
|---|---|
| `--p` na barra (0–100) | largura proporcional |
| `li.is-warn` / `li.is-bad` | cor da barra por alerta |
| `role="img"` + `aria-label` na barra | o percentual é lido |

## Acessibilidade

- A lista é `ol`, então a posição é anunciada.
- O percentual aparece em texto, não só na barra.

## Modelos

### HTML

```html
<ol class="ranked">
  <li>
    <span class="ranked-pos">1</span>
    <span class="ranked-name">1º A · Manhã<small>Ensino Médio</small></span>
    <span class="ranked-value">38/40<small>95%</small></span>
    <div class="ranked-bar" style="--p:95" role="img" aria-label="Ocupação 95%"><i></i></div>
  </li>
</ol>
```

### CSS

Classes `.ranked*`. A barra usa `calc(var(--p) * 1%)`.

### JS

```js
function renderRanked(el, itens) {
  const ordenados = [...itens].sort((a, b) => b.percentual - a.percentual);
  el.replaceChildren(...ordenados.map((item, i) => {
    const li = document.createElement('li');
    li.innerHTML = `<span class="ranked-pos">${i + 1}</span>
      <span class="ranked-name"></span>
      <span class="ranked-value">${item.valor}<small>${item.percentual}%</small></span>
      <div class="ranked-bar" style="--p:${item.percentual}" role="img" aria-label="Ocupação ${item.percentual}%"><i></i></div>`;
    li.querySelector('.ranked-name').textContent = item.nome; // texto do banco: nunca innerHTML
    return li;
  }));
}
```

### SQL

Ocupação das turmas (matrículas ativas sobre a capacidade):

```sql
SELECT
  c.name AS turma,
  c.max_students AS capacidade,
  COUNT(e.id) AS matriculados,
  ROUND(100 * COUNT(e.id) / NULLIF(c.max_students, 0), 1) AS ocupacao
FROM classes c
LEFT JOIN enrollments e
  ON e.class_uuid = c.uuid AND e.deleted_at IS NULL AND e.status = 'active'
WHERE c.deleted_at IS NULL AND c.is_active = 1 AND c.period_uuid = ?
GROUP BY c.id, c.name, c.max_students
ORDER BY ocupacao DESC
LIMIT 10;
```

## Faça / Não faça

- Faça: ordene pela métrica e mostre o valor absoluto junto da proporção (38/40 e 95%).
- Faça: limite a dez itens e leve o resto para a listagem completa.
- Não faça: comparar métricas diferentes na mesma lista.
