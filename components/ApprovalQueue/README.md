# ApprovalQueue

Lista de solicitações que dependem de uma decisão (aprovar ou recusar), com quem pediu, o valor ou a quantidade e os dois botões de decisão. Cada botão tem nome completo para leitores de tela.

## Quando usar

- Reembolsos, descontos, ajustes de carga, trancamentos e outros pedidos com aprovação.
- Quando a decisão precisa ficar registrada com autor e data (a ação deve gravar quem decidiu).
- Para uma fila de atendimento sem decisão formal, use [QueueList](../QueueList/README.md).

## Anatomia

```
[AV]  Reembolso de taxa · Matrícula 2026-0412        R$ 180,00   [✓] [✕]
      Marina Rocha · pedido há 2 dias · [Financeiro]
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Lista | `ul.appr` | sim |
| Avatar | `.av` (iniciais, `aria-hidden`) | recomendado |
| Título e metadado | `.appr-title`, `.appr-meta` | sim |
| Valor | `.appr-amount` | quando houver |
| Decisão | `.appr-acts` com `button.ib.ib-ok` e `button.ib.ib-no` | sim |

## Variantes / Estados

- **Pendente:** o padrão. Os dois botões ficam ativos.
- **Decidido:** após a ação, remova o item ou troque por um `pill-ok` / `pill-bad` com quem decidiu e quando. Não deixe os botões ativos.

## API

| Atributo | Efeito |
|---|---|
| `aria-label` em cada botão | nome completo da ação e do solicitante |
| `.ib-ok` / `.ib-no` | cor de hover de aprovar e recusar |

## Acessibilidade

- Os botões são só ícone; o `aria-label` diz a ação e o nome ("Aprovar reembolso de Marina Rocha").
- O avatar é `aria-hidden` porque o nome já aparece no título.
- Em ação de alto impacto, confirme antes (use [Modal](../Modal/README.md) ou um passo extra).

## Modelos

### HTML

```html
<ul class="appr">
  <li>
    <span class="av" aria-hidden="true">MR</span>
    <div><div class="appr-title">Reembolso de taxa</div><div class="appr-meta">Marina Rocha · 2 dias</div></div>
    <span class="appr-amount">R$ 180,00</span>
    <div class="appr-acts">
      <button class="ib ib-ok" type="button" aria-label="Aprovar reembolso de Marina Rocha"><i class="fa-light fa-check" aria-hidden="true"></i></button>
      <button class="ib ib-no" type="button" aria-label="Recusar reembolso de Marina Rocha"><i class="fa-light fa-xmark" aria-hidden="true"></i></button>
    </div>
  </li>
</ul>
```

### CSS

Classes `.appr*`, `.av`, `.ib`. Os botões usam `--ttsc-success` e `--ttsc-danger-text` no hover.

### JS

Decida no servidor e atualize a lista só depois da resposta:

```js
async function decidir(item, aprovar, el) {
  const res = await fetch(`/api/v1/aprovacoes/${item.uuid}/decisao`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ aprovar }),
  });
  if (!res.ok) throw new Error('Falha ao registrar a decisão');
  el.remove();
}
```

### SQL

Pendências de aprovação (`sac_approvals`), com o solicitante (`users.uuid`):

```sql
SELECT a.uuid, a.approval_type, a.reason, a.priority, a.created_at,
       u.name AS solicitante
FROM sac_approvals a
LEFT JOIN users u ON u.uuid = a.requested_by
WHERE a.tenant_id = ? AND a.status = 'pending'
ORDER BY a.created_at ASC
LIMIT 50;
```

Registro da decisão (dentro de uma transação, com quem decidiu):

```sql
UPDATE sac_approvals
SET status = ?, approved_at = NOW(), approved_by = ?, comment = ?
WHERE uuid = ? AND tenant_id = ? AND status = 'pending';
```

## Faça / Não faça

- Faça: mostre quem pediu, o valor e o motivo antes do botão.
- Faça: registre quem decidiu e quando; a auditoria depende disso.
- Não faça: aprovar com um clique em ação irreversível sem confirmação.
