# PricingCards

Três (ou mais) cartões de plano lado a lado, com preço, o que está incluído e um destaque para a opção recomendada. Usado para planos de mensalidade, pacotes de cursos e níveis de assinatura.

## Quando usar

- Comparar planos de mensalidade ou pacotes de curso antes de a pessoa escolher.
- Quando o diferencial entre os planos é o que está incluído (não só o preço).
- Não use para cobrança de um item só: nesse caso, o cartão de resumo da fatura é o componente certo.

## Anatomia

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│             │ │ Mais escolhido│ │             │
│ Básico      │ │ Completo    │ │ Integral    │
│ R$ 690/mês  │ │ R$ 890/mês  │ │ R$ 1.240/mês│
│ ✓ itens     │ │ ✓ itens     │ │ ✓ itens     │
│ [Escolher]  │ │ [Escolher]  │ │ [Escolher]  │
└─────────────┘ └─────────────┘ └─────────────┘
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Grade | `.pc-grid` | sim |
| Cartão | `article.pc` | sim |
| Destaque | `.pc.is-featured` e `.pc-badge` | não (no máximo um por grade) |
| Nome e descrição | `.pc-name`, `.pc-desc` | sim |
| Preço | `.pc-price` com `b` e `small` | sim |
| Itens incluídos | `ul > li` (`li.no` = não incluído) | recomendado |
| Ação | `button.pc-btn` | sim |

## Variantes / Estados

- **Recomendado:** um cartão com `.is-featured`. Só um por grade.
- **Item não incluído:** `li.no` mostra o ícone de X e a cor apagada. Não omita o item; ele precisa aparecer para comparar.
- **Sem destaque:** remova o `.pc-badge` ou deixe-o oculto (`visibility:hidden`) para manter a altura igual entre os cartões.

## API

| Atributo | Efeito |
|---|---|
| `.is-featured` no `article` | destaca o plano recomendado |
| `li.no` | item não incluído |

## Acessibilidade

- Cada plano é um `article` com título `h3`, então a leitura por cabeçalho funciona.
- O ícone de check e o de X são `aria-hidden`; o estado ("não incluído") precisa estar no texto ou na classe, não só na cor.
- O botão deve nomear o plano ("Escolher Completo"), não só "Escolher".

## Modelos

### HTML

```html
<div class="pc-grid">
  <article class="pc is-featured">
    <span class="pc-badge">Mais escolhido</span>
    <h3 class="pc-name">Completo</h3>
    <p class="pc-desc">Inclui reforço e acompanhamento pedagógico.</p>
    <div class="pc-price"><b>R$ 890</b><small>/mês</small></div>
    <ul>
      <li><i class="fa-light fa-check" aria-hidden="true"></i>Aulas de reforço</li>
      <li class="no"><i class="fa-light fa-xmark" aria-hidden="true"></i>Transporte escolar</li>
    </ul>
    <button class="pc-btn" type="button">Escolher Completo</button>
  </article>
</div>
```

### CSS

Classes `.pc*`. Três colunas acima de 760 px, uma coluna abaixo. O destaque usa `--ttsc-accent-border` e `--ttsc-accent`, então acompanha o tema.

### JS

Os planos vêm do cadastro de regras de mensalidade (ver SQL). A renderização é direta:

```js
function renderPlanos(el, planos) {
  el.replaceChildren(...planos.map((p) => {
    const art = document.createElement('article');
    art.className = 'pc' + (p.destaque ? ' is-featured' : '');
    art.innerHTML = `<h3 class="pc-name"></h3><p class="pc-desc"></p>
      <div class="pc-price"><b></b><small>/mês</small></div>
      <ul></ul><button class="pc-btn" type="button"></button>`;
    art.querySelector('.pc-name').textContent = p.nome;
    art.querySelector('.pc-desc').textContent = p.descricao;
    art.querySelector('.pc-price b').textContent = p.precoFormatado;
    art.querySelector('.pc-btn').textContent = 'Escolher ' + p.nome;
    return art;
  }));
}
```

### SQL

Mensalidades ativas por curso (regras de cobrança por curso):

```sql
SELECT
  c.name AS curso,
  r.monthly_tuition AS mensalidade,
  r.enrollment_fee AS taxa_matricula,
  r.due_day AS dia_vencimento
FROM academic_billing_rules r
JOIN courses c ON c.uuid = r.course_uuid
WHERE r.tenant_id = ? AND r.status = 'active'
ORDER BY r.monthly_tuition;
```

## Faça / Não faça

- Faça: mantenha o mesmo conjunto de itens em todos os planos, marcando os que não estão incluídos.
- Faça: destaque no máximo um plano.
- Não faça: mostrar preço sem período ("/mês", "/semestre").
