# TestimonialCard

Depoimento de uma pessoa (aluno, responsável, professor), com a citação, a nota em estrelas e a identificação de quem falou. Usado em sites institucionais e em páginas de captação.

## Quando usar

- Página de captação e site da instituição, para mostrar a experiência de famílias e alunos.
- Quando a credibilidade vem de uma pessoa identificada, não de um slogan.
- Não use depoimentos sem autorização de quem falou, nem sem identificar o vínculo (responsável, aluno, ex-aluno).

## Anatomia

```
★★★★★
“Texto do depoimento, em uma ou duas frases.”
[MO]  Marina Oliveira
      Responsável · 1º ano A
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Cartão | `figure.te` com `blockquote` | sim |
| Nota | `.te-stars` com `role="img"` e `aria-label` | recomendado |
| Autor | `figcaption.te-who` com `.av`, `.te-name`, `.te-role` | sim |

## Variantes / Estados

- **Com nota:** a linha de estrelas aparece acima do texto.
- **Sem nota:** remova `.te-stars`. Não invente uma nota.
- **Grade:** duas colunas acima de 640 px, uma abaixo.

## API

| Atributo | Efeito |
|---|---|
| `aria-label` em `.te-stars` | nota por extenso para leitores de tela |

## Acessibilidade

- `figure` e `figcaption` associam a citação a quem falou.
- A nota é lida como texto ("Avaliação: 4 de 5"), e as estrelas são `aria-hidden`.
- Use o nome real da pessoa (com autorização) e o vínculo; iniciais no avatar são só decorativas.

## Modelos

### HTML

```html
<figure class="te">
  <div class="te-stars" role="img" aria-label="Avaliação: 5 de 5">
    <i class="fa-solid fa-star" aria-hidden="true"></i><i class="fa-solid fa-star" aria-hidden="true"></i>
  </div>
  <blockquote>“O acompanhamento de reforço fez diferença.”</blockquote>
  <figcaption class="te-who">
    <span class="av" aria-hidden="true">MO</span>
    <span><span class="te-name">Marina Oliveira</span><br><span class="te-role">Responsável · 1º ano A</span></span>
  </figcaption>
</figure>
```

### CSS

Classes `.te*`. Cores de texto e de estrela vêm dos tokens `--ttsc-text`, `--ttsc-text-muted` e `--ttsc-warning-text`.

### JS

Sem JavaScript. Para uma lista vinda da base, use `textContent` para o texto da citação e o nome.

### SQL

Comentários de avaliação (nota 4 ou 5) de tickets já resolvidos, com o assunto do atendimento:

```sql
SELECT r.rating AS nota, r.comment AS depoimento, t.subject AS assunto, r.created_at
FROM sac_ticket_ratings r
JOIN sac_tickets t ON t.id = r.ticket_id
WHERE r.tenant_id = ? AND r.rating >= 4 AND r.comment IS NOT NULL AND r.comment <> ''
ORDER BY r.created_at DESC
LIMIT 6;
```

## Faça / Não faça

- Faça: peça autorização antes de publicar e mostre o vínculo da pessoa.
- Faça: use no máximo três depoimentos por bloco.
- Não faça: publicar uma nota sem o comentário que a justifica.
