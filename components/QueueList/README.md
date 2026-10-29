# QueueList

Lista numerada de itens que aguardam atendimento, com prioridade, tempo de espera e uma ação. Usada para filas de secretaria, financeiro e suporte.

## Quando usar

- Atendimentos pendentes em ordem de chegada, com prioridade visível.
- Quando cada item precisa de uma ação imediata (atender, responder, aprovar).
- Para aprovar ou recusar com decisão registrada, use [ApprovalQueue](../ApprovalQueue/README.md).

## Anatomia

```
(1)  Transferência entre campus · Ana Souza      2 h 10 min [Alta]   [Atender]
     Solicitação · SOL-2026-0412
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Lista | `ol.queue` | sim |
| Número | `.queue-num` | sim |
| Título e metadado | `.queue-title`, `.queue-meta` | sim |
| Espera e prioridade | `.queue-wait` com `.pill` | recomendado |
| Ação | `button.queue-act` | sim |

## Variantes / Estados

- **Prioridade:** `pill-bad` (alta), `pill-warn` (média), `pill-info` (baixa).
- **Vazia:** quando não há itens, use [EmptyState](../EmptyState/README.md) no lugar da lista.

## API

| Atributo | Efeito |
|---|---|
| Ordem do `ol` | ordem de atendimento |
| `.pill-*` | prioridade |
| `.queue-act` | ação do item |

## Acessibilidade

- A lista é `ol`, então a posição na fila é anunciada.
- A prioridade é texto no `pill`, não só cor.
- O botão deve ter nome completo em tela grande: "Atender Transferência…" se a tela tiver muitos itens; use `aria-label` nesse caso.

## Modelos

### HTML

```html
<ol class="queue">
  <li>
    <span class="queue-num">1</span>
    <div><div class="queue-title">Transferência entre campus · Ana Souza</div><div class="queue-meta">SOL-2026-0412</div></div>
    <span class="queue-wait">2 h 10 min <span class="pill pill-bad">Alta</span></span>
    <button class="queue-act" type="button" aria-label="Atender SOL-2026-0412">Atender</button>
  </li>
</ol>
```

### CSS

Classes `.queue*`. Abaixo de 640 px a espera e a ação descem para a segunda linha.

### JS

Ordene pela prioridade e depois pela chegada, e atualize a lista ao receber um item:

```js
const PESO = { alta: 0, media: 1, baixa: 2 };

function ordenarFila(itens) {
  return [...itens].sort((a, b) =>
    PESO[a.prioridade] - PESO[b.prioridade] || new Date(a.chegada) - new Date(b.chegada));
}
```

### SQL

Atendimentos em aberto da central (`sac_tickets`), do mais antigo ao mais recente:

```sql
SELECT t.number, t.subject, t.priority_id, t.status, t.created_at,
       TIMESTAMPDIFF(MINUTE, t.created_at, NOW()) AS espera_min
FROM sac_tickets t
WHERE t.tenant_id = ? AND t.status NOT IN ('resolved', 'closed') AND t.is_archived = 0
ORDER BY t.created_at ASC
LIMIT 50;
```

## Faça / Não faça

- Faça: mostre o tempo de espera em minutos ou horas, nunca só a data.
- Faça: limite a 10 itens na tela e tenha um link para a fila completa.
- Não faça: reordenar a fila sem avisar quem está atendendo o item.
