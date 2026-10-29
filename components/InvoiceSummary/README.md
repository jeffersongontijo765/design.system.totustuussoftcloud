# InvoiceSummary

Resumo de uma fatura ou boleto: número, vencimento e situação, a lista de itens com valores, o subtotal, o desconto e o total a pagar, com as ações de pagamento e de download.

## Quando usar

- Resumo de mensalidade, material ou taxa que a família precisa pagar.
- Quando o total precisa ficar claro, com cada item e desconto visíveis.
- Para uma lista de faturas, use uma tabela (ver [DataTable](../DataTable/README.md)); este cartão é para uma fatura só.

## Anatomia

```
Fatura nº 2026-11-0412                              [Vence em 5 dias]
Mensalidade de novembro · Ana Souza
Item                                         Valor
Mensalidade · 2º ano B                 R$ 890,00
Material didático (parcela 2 de 3)     R$ 120,00
Subtotal                                R$ 1.010,00
Desconto                                  − R$ 45,00
Total a pagar                              R$ 965,00
                                   [Baixar PDF] [Pagar com PIX]
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Contêiner | `section.iv` | sim |
| Número e título | `.iv-num`, `h2.iv-title` | sim |
| Situação | `.pill` (vence em, pago, em atraso) | sim |
| Itens | `table.iv-table` com `caption`, `th.num` e `td.num` | sim |
| Totais | `.iv-totals` com `.grand` | sim |
| Ações | `.iv-acts` | recomendado |

## Variantes / Estados

- **Em aberto:** `pill-warn` ou `pill-info` com o prazo.
- **Paga:** `pill-ok` com a data do pagamento; esconda "Pagar com PIX".
- **Em atraso:** `pill-bad` com os dias de atraso e, se houver, a multa.

## API

| Atributo | Efeito |
|---|---|
| `.num` em `th`/`td` | alinha valores à direita |
| `.grand` | linha de total destacada |

## Acessibilidade

- Os valores são alinhados à direita e têm `tabular-nums`, para comparação fácil.
- A situação é texto ("Vence em 5 dias"), não só a cor do selo.
- A tabela tem `caption` e cabeçalhos com `scope`.

## Modelos

### HTML

```html
<section class="iv" aria-labelledby="iv-t">
  <div class="iv-head">
    <div><div class="iv-num">Fatura nº 2026-11-0412</div><h2 id="iv-t" class="iv-title">Mensalidade de novembro</h2></div>
    <span class="pill pill-warn">Vence em 5 dias</span>
  </div>
  <table class="iv-table">
    <thead><tr><th scope="col">Item</th><th scope="col" class="num">Valor</th></tr></thead>
    <tbody><tr><td>Mensalidade · 2º ano B</td><td class="num">R$ 890,00</td></tr></tbody>
  </table>
  <div class="iv-totals"><div class="grand"><span>Total a pagar</span><span>R$ 965,00</span></div></div>
  <div class="iv-acts"><button class="iv-btn primary" type="button">Pagar com PIX</button></div>
</section>
```

### CSS

Classes `.iv*`. Os totais ficam alinhados à direita e a linha de total tem borda superior.

### JS

Os valores vêm formatados do servidor; o cartão só exibe. O botão de pagamento abre o fluxo de pagamento do módulo financeiro.

### SQL

Itens em aberto da fatura (títulos a receber de um aluno), com valor líquido e vencimento:

```sql
SELECT r.code AS fatura, r.description AS descricao, r.net_amount AS valor,
       r.due_date AS vencimento, r.status AS situacao
FROM financial_receivables r
WHERE r.customer_id = ? AND r.deleted_at IS NULL
  AND r.status IN ('pending', 'overdue')
ORDER BY r.due_date;
```

## Faça / Não faça

- Faça: mostre cada item e cada desconto, para a família conferir o total.
- Faça: mostre o vencimento em dias, além da data.
- Não faça: exibir o total sem o subtotal e os descontos.
