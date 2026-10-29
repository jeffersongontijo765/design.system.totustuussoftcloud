# QuadrantMatrix

Matriz 2×2 que classifica itens em quatro quadrantes conforme dois indicadores. Cada quadrante tem nome, regra e a lista de itens que caem nele.

## Quando usar

- Priorização: cursos por ocupação × conversão, turmas por ocupação × receita, unidades por desempenho × custo.
- Quando a decisão depende de dois critérios ao mesmo tempo e uma tabela não deixa o padrão visível.
- Não use com mais de 30 itens por quadrante: a lista vira uma tabela escondida.

## Anatomia

```
              ┌──────────────┬──────────────┐
Conversão ↑   │ Oportunidade │   Destaque   │
              ├──────────────┼──────────────┤
              │   Revisar    │ Lista espera │
              └──────────────┴──────────────┘
                 ocupação →
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Contêiner | `.quad` | sim |
| Eixo vertical | `.quad-y` | sim |
| Eixo horizontal | `.quad-x` | sim |
| Quadrantes | `.quad-grid > .quad-cell` com `.star`, `.opp`, `.watch` ou `.bad` | sim |
| Item | `.quad-item` (nome + valor) | não |

## Variantes / Estados

- **Cores:** `.star` (destaque), `.opp` (oportunidade), `.watch` (lista de espera) e `.bad` (revisar).
- **Limiar:** o corte entre alto e baixo deve ser uma regra escrita e visível na página.

## API

| Atributo | Efeito |
|---|---|
| Classe do quadrante | cor e papel |
| `role="group"` + `aria-label` no grupo | nomeia a matriz |

## Acessibilidade

- Os rótulos dos quadrantes são texto (`h3`), não só cor.
- Os eixos são textos. Se a matriz for lida por leitor de tela, mantenha a ordem: eixo, quadrantes, eixo.

## Modelos

### HTML

```html
<div class="quad">
  <span class="quad-y">Conversão</span>
  <div class="quad-grid" role="group" aria-label="Quadrantes de cursos">
    <div class="quad-cell star">
      <h3>Destaque</h3><p>Conversão e ocupação altas</p>
      <div class="quad-item"><span>Ensino Médio</span><b>86%</b></div>
    </div>
    <div class="quad-cell bad">
      <h3>Revisar</h3><p>Conversão e ocupação baixas</p>
    </div>
  </div>
  <div class="quad-x" aria-hidden="true"><span>Ocupação baixa</span><span>Ocupação alta</span></div>
</div>
```

### CSS

Classes `.quad*`. Quadrantes usam `color-mix` com as cores de estado, então funcionam no tema escuro.

### JS

Classifique os itens pelos limiares e preencha cada quadrante:

```js
function quadrante(item, limiarX, limiarY) {
  const alto_x = item.ocupacao >= limiarX;
  const alto_y = item.conversao >= limiarY;
  if (alto_x && alto_y) return 'star';
  if (!alto_x && alto_y) return 'opp';
  if (alto_x && !alto_y) return 'watch';
  return 'bad';
}
```

### SQL

Ocupação e conversão de cada curso no período (conversão = matriculados / inscritos):

```sql
SELECT
  co.name AS curso,
  ROUND(100 * COUNT(DISTINCT e.id) / NULLIF(co.max_students, 0), 1) AS ocupacao,
  ROUND(100 * SUM(r.status IN ('approved', 'confirmed')) / NULLIF(COUNT(DISTINCT r.id), 0), 1) AS conversao
FROM courses co
LEFT JOIN enrollment_requests r ON r.course_uuid = co.uuid AND r.deleted_at IS NULL AND r.period_uuid = ?
LEFT JOIN enrollments e ON e.course_uuid = co.uuid AND e.deleted_at IS NULL AND e.period_uuid = ? AND e.status = 'active'
WHERE co.deleted_at IS NULL AND co.is_active = 1
GROUP BY co.id, co.name, co.max_students;
```

## Faça / Não faça

- Faça: escreva a regra de cada quadrante na própria página.
- Faça: use os mesmos limiares em todas as telas que usam a matriz.
- Não faça: usar mais de dois indicadores; nesse caso use uma tabela com colunas.
