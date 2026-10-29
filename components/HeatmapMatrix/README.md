# HeatmapMatrix

Matriz de linhas × colunas em que a intensidade da cor representa um valor (presença, ocupação, carga). Permite ver padrões de uma vez: uma turma inteira, um dia da semana ou um horário específico.

## Quando usar

- Frequência por turma e dia da semana, notas por série e disciplina, ocupação por sala e horário.
- Quando o número exato importa pouco e o padrão importa muito.
- Não use quando há menos de 3 linhas ou colunas: uma tabela comum é mais legível.

## Anatomia

```
              Seg    Ter    Qua    Qui    Sex
1º A · Manhã  [96%] [94%]  [95%]  [89%]  [87%]
1º B · Tarde  [88%] [86%]  [81%]  [79%]  [72%]
Legenda: Menos ▢▢▢▢▢ Mais
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Tabela | `table.heat` com `caption` | sim |
| Cabeçalhos | `th` de coluna e `th[scope=row]` de linha | sim |
| Célula | `td` com `--lv` (0–4) e `data-lv` | sim |
| Legenda | `.heat-legend` | recomendado |

## Variantes / Estados

- **Níveis:** cinco níveis (0 a 4). O nível vem de faixas de valor definidas pela regra de negócio, não de uma escala automática.
- **Destaque de alerta:** use um `.pill-bad` no cabeçalho para contar células abaixo do limite.

## API

| Atributo | Efeito |
|---|---|
| `--lv` no `td` (0–4) | intensidade da cor |
| `data-lv` no `td` | mesmo nível, usado para trocar a cor do texto em níveis altos |
| `caption` | título acessível da matriz |

## Acessibilidade

- O valor está escrito em cada célula; a cor não é a única informação.
- A tabela tem `caption`, `scope` nos cabeçalhos e a legenda fica como `aria-hidden` porque repete a informação.
- Níveis 3 e 4 usam texto claro sobre fundo escuro, para contraste.

## Modelos

### HTML

```html
<table class="heat">
  <caption>Quanto mais escuro, maior a presença</caption>
  <thead><tr><th scope="col">Turma</th><th scope="col">Seg</th><th scope="col">Ter</th></tr></thead>
  <tbody>
    <tr><th scope="row">1º A · Manhã</th><td class="hc" style="--lv:4" data-lv="4">96%</td><td class="hc" style="--lv:3" data-lv="3">89%</td></tr>
    <tr><th scope="row">1º B · Tarde</th><td class="hc" style="--lv:2" data-lv="2">81%</td><td class="hc" style="--lv:1" data-lv="1">72%</td></tr>
  </tbody>
</table>
```

### CSS

Classes `.heat`, `.heat td` e `.heat-legend`. A cor de cada célula é `color-mix` entre `--ttsc-accent` e `--ttsc-surface-2`, então acompanha o tema.

### JS

Calcule o nível a partir do valor e das faixas:

```js
function nivel(valor, faixas) {
  // faixas em ordem crescente, ex.: [60, 70, 80, 90] -> 0..4
  return faixas.filter((limite) => valor >= limite).length;
}

function preencher(td, valor) {
  const lv = nivel(valor, [60, 70, 80, 90]);
  td.style.setProperty('--lv', lv);
  td.dataset.lv = lv;
  td.textContent = valor + '%';
}
```

### SQL

Presença média por turma e dia da semana, nas últimas quatro semanas:

```sql
SELECT
  c.name AS turma,
  DAYOFWEEK(a.lesson_date) AS dia_semana,
  ROUND(100 * SUM(a.status = 'present') / NULLIF(COUNT(*), 0), 1) AS presenca
FROM attendance a
JOIN classes c ON c.uuid = a.class_uuid
WHERE a.lesson_date >= CURDATE() - INTERVAL 28 DAY
GROUP BY c.uuid, c.name, DAYOFWEEK(a.lesson_date)
ORDER BY c.name, dia_semana;
```

## Faça / Não faça

- Faça: ordene linhas pela métrica de interesse (a pior no topo) ou pela ordem natural da escola.
- Faça: defina as faixas de cor uma vez e use a mesma legenda em toda a tela.
- Não faça: usar mais de cinco níveis; a diferença entre eles deixa de ser visível.
