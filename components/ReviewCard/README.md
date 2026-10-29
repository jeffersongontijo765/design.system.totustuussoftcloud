# ReviewCard

Avaliação de uma pessoa ou serviço: nota com estrelas e número, a origem de quem avaliou, o texto e a contagem de quem achou útil. Usado para avaliar disciplinas, professores e atendimentos.

## Quando usar

- Avaliação de disciplina ou de atendimento pelos alunos e responsáveis.
- Quando a nota precisa vir acompanhada do comentário que a justifica.
- Para depoimentos publicados num site institucional, use [TestimonialCard](../TestimonialCard/README.md).

## Anatomia

```
★★★★★ 5,0                                  [Responsável]
Texto da avaliação em um ou dois parágrafos.
Marina O. · 12/11/2026                     [Útil (14)]
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Cartão | `article.rv` | sim |
| Nota | `.rv-stars` com `role="img"` e `aria-label` + `b` | sim |
| Origem | `.pill` (Responsável, Aluno) | recomendado |
| Texto | `p.rv-text` | sim |
| Rodapé | `.rv-foot` com autor, data e `button.rv-help` | sim |

## Variantes / Estados

- **Nota alta / média / baixa:** a nota é sempre escrita, nunca só a cor.
- **Sem texto:** o cartão só tem a nota e a origem; não mostre um cartão vazio.
- **Útil marcado:** o botão mostra `aria-pressed="true"` e o total atualizado.

## API

| Atributo | Efeito |
|---|---|
| `aria-label` em `.rv-stars` | nota por extenso |
| `aria-pressed` em `.rv-help` | voto de "útil" marcado |

## Acessibilidade

- A nota é lida por extenso ("Nota 5 de 5"); as estrelas são decorativas.
- O botão de "útil" informa o estado com `aria-pressed`.
- A data é texto (não só ícone), para que a ordem cronológica seja clara.

## Modelos

### HTML

```html
<article class="rv">
  <div class="rv-head">
    <div class="rv-score"><span class="rv-stars" role="img" aria-label="Nota 5 de 5">★★★★★</span><b>5,0</b></div>
    <span class="pill pill-info">Responsável</span>
  </div>
  <p class="rv-text">Professor explica com paciência.</p>
  <div class="rv-foot"><span>Marina O. · 12/11/2026</span><button class="rv-help" type="button" aria-pressed="false">Útil (14)</button></div>
</article>
```

### CSS

Classes `.rv*`. As estrelas usam `--ttsc-warning-text`.

### JS

```js
function marcarUtil(botao, avaliacaoId) {
  const marcado = botao.getAttribute('aria-pressed') !== 'true';
  botao.setAttribute('aria-pressed', String(marcado));
  fetch(`/api/v1/avaliacoes/${avaliacaoId}/util`, { method: marcado ? 'POST' : 'DELETE' });
}
```

### SQL

Avaliações de atendimentos resolvidos, com a contagem de notas por faixa (4-5, 3, 1-2):

```sql
SELECT
  CASE WHEN r.rating >= 4 THEN 'alta' WHEN r.rating = 3 THEN 'media' ELSE 'baixa' END AS faixa,
  COUNT(*) AS avaliacoes,
  ROUND(AVG(r.rating), 2) AS nota_media
FROM sac_ticket_ratings r
WHERE r.tenant_id = ?
GROUP BY faixa;
```

## Faça / Não faça

- Faça: mostre a nota e o número de avaliações juntos.
- Faça: mostre a origem de quem avaliou (responsável, aluno) para dar contexto.
- Não faça: esconder avaliações negativas; elas são a informação mais útil para a gestão.
