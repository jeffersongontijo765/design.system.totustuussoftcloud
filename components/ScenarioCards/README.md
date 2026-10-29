# ScenarioCards

Três cartões lado a lado (pessimista, base, otimista) com o mesmo indicador calculado com premissas diferentes. Um deles fica selecionado e mostra as premissas.

## Quando usar

- Previsão de receita, de matrícula ou de custo com premissas explícitas.
- Quando a decisão depende de ver o intervalo de resultados, não só um número.
- Para uma série temporal, use gráfico de linha; para cenários, use este componente.

## Anatomia

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Pessimista  │ │ Base  ●     │ │ Otimista    │
│ R$ 1,62 mi  │ │ R$ 1,75 mi  │ │ R$ 1,84 mi  │
│ ↓ 7,4%      │ │ Igual       │ │ ↑ 5,1%      │
│ premissa…   │ │ premissa…   │ │ premissa…   │
└─────────────┘ └─────────────┘ └─────────────┘
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Grupo | `.scen` com `role="group"` | sim |
| Cartão | `button` com `aria-pressed` | sim |
| Tom | `.bad` (pessimista), `.good` (otimista) | não |
| Valor | `.scen-value` | sim |
| Variação | `.scen-delta` com `.up`, `.down` ou `.flat` | recomendado |
| Premissa | `.scen-note` | sim |

## Variantes / Estados

- **Selecionado:** `aria-pressed="true"` com borda de destaque. Só um cartão pode estar selecionado.
- **Sem seleção:** nenhum cartão selecionado mostra só os valores.

## API

| Atributo | Efeito |
|---|---|
| `aria-pressed` | cartão selecionado (`true` ou `false`) |
| `role="group"` + `aria-label` | nomeia o conjunto de cenários |

## Acessibilidade

- Os cartões são `button` com `aria-pressed`, então funcionam por teclado e informam o estado.
- A variação tem texto ("↓ 7,4% vs. base"), não só cor.
- A premissa fica visível no próprio cartão.

## Modelos

### HTML

```html
<div class="scen" role="group" aria-label="Cenários de receita">
  <button class="bad" type="button" aria-pressed="false">
    <span class="scen-label">Pessimista</span>
    <span class="scen-value">R$ 1,62 mi</span>
    <span class="scen-delta down">↓ 7,4% vs. base</span>
    <span class="scen-note">Inadimplência de 9,4%.</span>
  </button>
  <button type="button" aria-pressed="true">
    <span class="scen-label">Base</span>
    <span class="scen-value">R$ 1,75 mi</span>
    <span class="scen-delta flat">Igual ao orçamento</span>
    <span class="scen-note">Inadimplência de 6,1%.</span>
  </button>
</div>
```

### CSS

Classes `.scen*`. Os tons usam `color-mix` com `--ttsc-danger` e `--ttsc-success`.

### JS

```js
function selecionar(grupo, botao) {
  grupo.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', b === botao ? 'true' : 'false'));
}
document.querySelector('.scen').addEventListener('click', (e) => {
  const b = e.target.closest('button');
  if (b) selecionar(b.parentElement, b);
});
```

### SQL

Receita a receber por cenário: o total em aberto do período é a base; cada cenário aplica a inadimplência da premissa.

```sql
SELECT
  SUM(net_amount) AS receita_base,
  SUM(net_amount) * (1 - 0.094) AS receita_pessimista,
  SUM(net_amount) * (1 - 0.032) AS receita_otimista
FROM financial_receivables
WHERE deleted_at IS NULL AND status IN ('pending', 'overdue')
  AND due_date >= ? AND due_date < ?;
```

## Faça / Não faça

- Faça: escreva as premissas de cada cenário no próprio cartão.
- Faça: mantenha os mesmos três cenários em toda a tela que os usa.
- Não faça: apresentar o pessimista e o otimista sem a base de comparação.
