# RiskList

Lista de pessoas ou itens com um percentual de risco, o motivo em uma linha e uma barra que muda de cor pela faixa. Serve para alerta precoce: evasão, inadimplência, atraso.

## Quando usar

- Alunos em risco de evasão, parcelas em risco de inadimplência, pedidos atrasados.
- Quando a ação é individual (abrir a ficha, enviar um contato) e a lista deve ser priorizada.
- O percentual deve vir de uma regra explicável (faltas, notas, atrasos). Não é uma previsão de IA.

## Anatomia

```
[KF]  Kenji Fujita · 2º A                     Risco ████████░ 82%   [→]
      Faltas em 38% das aulas; 3 semanas sem entrega
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Lista | `ul.risk` | sim |
| Item | `li` com `.is-mid` ou `.is-high` (sem classe = baixo) | sim |
| Avatar | `.av` (`aria-hidden`) | recomendado |
| Nome e motivo | `.risk-name`, `.risk-why` | sim |
| Medidor | `.risk-meter` com `.risk-track > i` (`--p`) | sim |
| Ação | `button.ib` com `aria-label` | sim |

## Variantes / Estados

- **Baixo (verde):** sem classe no `li`, abaixo de 30%.
- **Médio (amarelo):** `.is-mid`, de 30% a 59%.
- **Alto (vermelho):** `.is-high`, 60% ou mais.

As faixas são regra de negócio; defina-as uma vez e documente na tela.

## API

| Atributo | Efeito |
|---|---|
| `--p` no `i` (0–100) | largura do medidor |
| `li.is-mid` / `li.is-high` | cor por faixa |
| `aria-label` no `button` | ação com nome da pessoa |

## Acessibilidade

- O percentual é texto ao lado do medidor e o medidor tem `aria-label`.
- O motivo é texto, para que a lista não dependa de cor.
- A faixa de risco também aparece no texto do cabeçalho ("3 com risco alto").

## Modelos

### HTML

```html
<ul class="risk">
  <li class="is-high">
    <span class="av" aria-hidden="true">KF</span>
    <div><div class="risk-name">Kenji Fujita · 2º A</div><div class="risk-why">Faltas em 38% das aulas</div></div>
    <div class="risk-meter"><div class="risk-meter-top"><span>Risco</span><b>82%</b></div>
      <div class="risk-track" role="img" aria-label="Risco 82%"><i style="--p:82"></i></div></div>
    <button class="ib" type="button" aria-label="Abrir ficha de Kenji Fujita"><i class="fa-light fa-arrow-right" aria-hidden="true"></i></button>
  </li>
</ul>
```

### CSS

Classes `.risk*`. Cores de faixa vêm de `--ttsc-success`, `--ttsc-warning` e `--ttsc-danger`.

### JS

```js
function faixa(percentual) {
  if (percentual >= 60) return 'is-high';
  if (percentual >= 30) return 'is-mid';
  return '';
}
```

### SQL

Alunos com faltas acima de 25% no período (taxa de faltas por matrícula):

```sql
SELECT
  e.uuid,
  ROUND(100 * SUM(a.status = 'absent') / NULLIF(COUNT(*), 0), 1) AS risco_faltas
FROM enrollments e
JOIN attendance a ON a.enrollment_uuid = e.uuid
WHERE e.deleted_at IS NULL AND e.period_uuid = ? AND e.status = 'active'
GROUP BY e.uuid
HAVING risco_faltas >= 25
ORDER BY risco_faltas DESC
LIMIT 20;
```

## Faça / Não faça

- Faça: mostre o motivo com o número que o gerou ("faltas em 38% das aulas").
- Faça: deixe a ação de abrir a ficha da pessoa, nunca uma ação automática sobre ela.
- Não faça: exibir o percentual sem a regra de cálculo acessível na tela.
