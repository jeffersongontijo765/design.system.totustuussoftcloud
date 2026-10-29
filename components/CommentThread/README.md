# CommentThread

Lista de comentários em uma conversa, com respostas aninhadas, autor, papel, horário e ação de responder. Diferencia mensagem para a família de nota interna da equipe, que não aparece para quem é atendido.

## Quando usar

- Conversa de uma ocorrência, de um atendimento ou de uma solicitação, entre família e equipe.
- Notas internas da equipe sobre um caso, separadas das mensagens visíveis.
- Para o chat em tempo real (mensagens instantâneas), use [ChatPanel](../ChatPanel/README.md).

## Anatomia

```
(MO) Marina Oliveira  [Família]  19/11 · 09:14
     Gostaria de saber se a falta foi justificada.
     Responder
        (JS) Joana Silva  [Secretaria]  19/11 · 10:02
             Registrada como justificada.
(RL) Rui Lima  [Nota interna]  19/11 · 11:30     ← fundo amarelo
     Confirmar com a coordenação…
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Lista | `.ct` | sim |
| Comentário | `article.ct-item` | sim |
| Resposta | `.ct-item.ct-reply` (recuo) | não |
| Nota interna | `.ct-item.internal` + `.pill-warn` "Nota interna" | quando for interna |
| Cabeçalho | `.ct-head` com autor, papel e `time datetime` | sim |
| Ação | `.ct-acts button` | recomendado |

## Variantes / Estados

- **Mensagem para a família:** padrão.
- **Nota interna:** fundo amarelo, selo "Nota interna" e nunca enviada à família.
- **Resposta:** `ct-reply` recua o comentário, mas a ordem cronológica se mantém.

## API

| Atributo | Efeito |
|---|---|
| `.internal` no `article` | marca como nota interna (não visível para a família) |
| `.ct-reply` | recuo de resposta |
| `time[datetime]` | horário legível pelo leitor |

## Acessibilidade

- O selo "Nota interna" é texto, não só a cor amarela.
- Os comentários são `article` e o horário é `time`, para navegação por leitor de tela.
- Responder é um `button`; a caixa de resposta deve ter rótulo ("Responder à mensagem de Marina Oliveira").

## Modelos

### HTML

```html
<article class="ct-item">
  <span class="av" aria-hidden="true">MO</span>
  <div class="ct-body">
    <div class="ct-head">
      <span class="ct-name">Marina Oliveira</span><span class="pill pill-info">Família</span>
      <span class="ct-time"><time datetime="2026-11-19T09:14">19/11 · 09:14</time></span>
    </div>
    <p class="ct-text">Gostaria de saber se a falta foi justificada.</p>
    <div class="ct-acts"><button type="button">Responder</button></div>
  </div>
</article>
```

### CSS

Classes `.ct*`. A nota interna usa `--ttsc-warning`; a resposta recua 42 px.

### JS

```js
async function enviarComentario(ocorrenciaId, texto, interno) {
  const res = await fetch(`/api/v1/ocorrencias/${ocorrenciaId}/comentarios`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ texto, interno }),
  });
  if (!res.ok) throw new Error('Não foi possível enviar o comentário');
  return res.json();
}
```

### SQL

Mensagens de uma ocorrência, na ordem em que foram escritas. Notas internas (`is_internal = 1`) só aparecem para a equipe:

```sql
SELECT m.uuid, m.sender_name AS autor, m.sender_type AS papel, m.message AS texto,
       m.is_internal AS interna, m.created_at
FROM sac_ticket_messages m
WHERE m.tenant_id = ? AND m.ticket_id = ?
  AND (m.is_internal = 0 OR ? = 1)
ORDER BY m.created_at ASC;
```

## Faça / Não faça

- Faça: marque a nota interna de forma clara e nunca a envie à família.
- Faça: mantenha a ordem cronológica, mesmo com respostas.
- Não faça: exibir uma nota interna para quem não é da equipe; confira no servidor, não só na tela.
