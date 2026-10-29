# FunnelBars

Funil horizontal em barras decrescentes, com o valor de cada etapa e a porcentagem em relação ao topo. Mostra onde a coorte perde pessoas.

## Quando usar

- Captação e matrícula: interessados → inscritos → matriculados → frequentando.
- Qualquer processo com etapas que só diminuem (cobrança, certificação, rematrícula).
- Para comparar etapas de tamanhos muito diferentes, prefira [RankedBars](../RankedBars/README.md).

## Anatomia

```
Etapa        [██████████████████████████████████]  6.840   100%
Etapa        [████████████████████]                4.644   67,9%
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Lista | `ol.funnel` | sim |
| Etapa | `li` com `--i` (0 = topo, 1, 2…) | sim |
| Rótulo | `.funnel-label` | sim |
| Trilho e barra | `.funnel-track` > `.funnel-bar` com `--w` (0–100) | sim |
| Valor e porcentagem | `.funnel-value` > `small` | recomendado |

## Variantes / Estados

- **Tonalidade:** a cor da barra escurece do topo para o fim (`--i`). Não use cores diferentes por etapa sem motivo.
- **Queda:** a queda entre etapas pode ser mostrada abaixo em `.funnel-drop`.
- **Mobile:** abaixo de 640 px cada etapa vira uma linha só.

## API

| Atributo | Efeito |
|---|---|
| `--w` na barra (0–100) | largura proporcional ao topo |
| `--i` no `li` (0, 1, 2…) | intensidade da cor |
| `role="img"` + `aria-label` na barra | o número é lido mesmo com a barra visual |

## Acessibilidade

- O valor fica em texto ao lado da barra; a cor não carrega a informação sozinha.
- A barra tem `aria-label` com etapa e valor. A lista é `ol`, então a ordem é anunciada.

## Modelos

### HTML

```html
<ol class="funnel">
  <li style="--i:0">
    <span class="funnel-label">Interessados</span>
    <div class="funnel-track"><div class="funnel-bar" style="--w:100" role="img" aria-label="Interessados: 6.840">6.840</div></div>
    <span class="funnel-value">6.840 <small>100%</small></span>
  </li>
  <li style="--i:1">
    <span class="funnel-label">Inscritos</span>
    <div class="funnel-track"><div class="funnel-bar" style="--w:68" role="img" aria-label="Inscritos: 4.644">4.644</div></div>
    <span class="funnel-value">4.644 <small>67,9%</small></span>
  </li>
</ol>
```

### CSS

Classes `.funnel*`. A largura usa `calc(var(--w) * 1%)`, então um valor de `--w` fora de 0–100 quebra o layout.

### JS

Largura e cor vêm de atributos. Para gerar a partir de dados:

```js
function renderFunnel(el, etapas) {
  const topo = etapas[0].valor;
  el.innerHTML = etapas.map((e, i) => `
    <li style="--i:${i}">
      <span class="funnel-label">${e.rotulo}</span>
      <div class="funnel-track"><div class="funnel-bar" style="--w:${(e.valor / topo * 100).toFixed(1)}" role="img" aria-label="${e.rotulo}: ${e.valor}">${e.valor}</div></div>
      <span class="funnel-value">${e.valor} <small>${(e.valor / topo * 100).toFixed(1).replace('.', ',')}%</small></span>
    </li>`).join('');
}
```

Use `textContent` (ou escape) para `e.rotulo` quando o texto vier do banco.

### SQL

Contagem por etapa a partir de `enrollment_requests` (inscrições) e `enrollments` (matrículas), no período `?`:

```sql
SELECT
  COUNT(*) AS inscritos,
  SUM(status IN ('approved', 'confirmed')) AS aprovados
FROM enrollment_requests
WHERE deleted_at IS NULL AND period_uuid = ?;

SELECT COUNT(*) AS matriculados
FROM enrollments
WHERE deleted_at IS NULL AND period_uuid = ? AND status = 'active';
```

## Faça / Não faça

- Faça: ordene as etapas do topo para o fim, sem misturar etapas paralelas.
- Faça: mostre a porcentagem em relação ao topo; é o número que a gestão compara.
- Não faça: usar funil para dados que podem subir e descer (use um gráfico de linha).
