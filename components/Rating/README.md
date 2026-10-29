# Rating

Avaliação por estrelas (ou corações) do ttscui (`data-ttsc-rating`): interativa com radios nativos ou somente leitura, com `max`, `value`, `name` e evento `ttsc.rating.change`.

> Também listado em: **Base › Rating**.

## Quando usar

- Coletar uma nota de 1 a N: avaliação do atendimento da secretaria (SAC), satisfação com um evento, avaliação de disciplina pelo aluno.
- Exibir uma média já calculada (somente leitura) em cards e linhas de tabela.
- Para notas acadêmicas (0 a 10 com decimais) use um campo numérico do formulário, **não** estrelas: rating é inteiro e subjetivo.
- Para “sim/não” ou “gostei” use [Toggle](../Toggle/README.md) ou um botão; para intervalos contínuos use o Range Slider.

## Anatomia

```
<div data-ttsc-rating>                     ← host (vazio no HTML)
  └ div.ttsc-rating (gerado, role=group)    ← flex-row-reverse: DOM = max…1, visual = 1…max
      ├ input[type=radio][name][value=N]    ← escondido (fora da tela), recebe foco/teclado
      └ label.ttsc-rating-label[data-ttsc-rating-value=N] > svg
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Host | `div[data-ttsc-rating="true"]` | sim |
| Container gerado | `.ttsc-rating` (`role="group"`; `role="img"` quando readonly) | gerado |
| Radio | `input[type=radio]` com `name` = `data-ttsc-rating-name` | gerado (interativo) |
| Rótulo/ícone | `label.ttsc-rating-label` + SVG (estrela ou coração) | gerado |
| Cor ativa/inativa | classes `text-yellow-400` / `text-red-500` (heart) / `text-muted-foreground/50` — ver CSS da ponte | gerado |

## Variantes

| Variante | Atributos | Uso | Tokens |
|---|---|---|---|
| Interativa | `data-ttsc-rating="true"` | formulários de avaliação | ativa `ttsc-warning`, inativa `ttsc-border-prominent`, foco `ttsc-accent` |
| Somente leitura | `data-ttsc-rating-readonly="true"` | médias em cards/tabelas | idem, sem hover/radios |
| Coração | `data-ttsc-rating-symbol="heart"` | satisfação/afeto (pesquisa com responsáveis) | ativa `ttsc-danger` |
| Escala | `data-ttsc-rating-max="10"` | NPS simplificado | — |

## API

Atributos (lidos por `getDataAttributes` com prefixo `data-ttsc-rating-`; também aceitam variável CSS `--ttsc-rating-<opção>`):

| Atributo | Padrão | Efeito |
|---|---|---|
| `data-ttsc-rating` | — | ativa o componente |
| `data-ttsc-rating-value` | `0` | nota inicial (inteiro de 0 a `max`) |
| `data-ttsc-rating-max` | `5` | número de símbolos (≥ 1) |
| `data-ttsc-rating-readonly` | `false` | só exibe; sem radios |
| `data-ttsc-rating-name` | `"rating"` | `name` dos radios — é o campo enviado no `<form>` |
| `data-ttsc-rating-symbol` | `"star"` | `star` ou `heart` |
| `data-ttsc-rating-lazy` | `false` | `true` = não inicializa no `TTSC.init()` (crie com `new TTSC.Rating(el)`) |

| Método | Retorno |
|---|---|
| `TTSC.Rating.getInstance(el)` | instância (cria se o atributo existir) |
| `inst.getValue()` | número selecionado ou `null` |
| `inst.setValue(n \| null)` | marca o radio `n`; `null` limpa |
| `inst.dispose()` | remove listeners |

| Evento | Onde | `detail` |
|---|---|---|
| `ttsc.rating.change` | no host (bubbles) | `{ payload: { value } }` |
| `inst.on('change', fn)` | callback interno | `{ value }` |

## Acessibilidade

- Os radios nativos dão teclado de graça: Tab entra no grupo, setas mudam a nota, o valor vai no `FormData`.
- O container recebe `aria-label="Rating: N of M"` (texto fixo em inglês no ttscui): sobrescreva no `ttsc.rating.change` com “Nota N de M” e coloque um rótulo visível ao lado (“4 de 5”) com `aria-live="polite"`.
- Somente leitura vira `role="img"` com `aria-valuenow/min/max`; acompanhe de texto (“4,0 · 128 avaliações”).
- Estrela ativa `ttsc-warning` (#eab308) é ícone, não texto; o número ao lado usa `--ttsc-text-2`. Foco visível com contorno `ttsc-accent`.

## Modelos

### HTML

```html
<!-- Avaliação do chamado no portal do responsável (form POST) -->
<form method="post" action="/app/sac/tickets/<?= $e($ticket['uuid']) ?>/rating" class="flex flex-col gap-2">
  <input type="hidden" name="_token" value="<?= $e($csrf) ?>">
  <label class="text-sm font-medium" id="rating-label">Como foi o atendimento da secretaria?</label>
  <div class="flex items-center gap-2">
    <div data-ttsc-rating="true" data-ttsc-rating-value="0" data-ttsc-rating-max="5"
         data-ttsc-rating-name="rating" aria-labelledby="rating-label"></div>
    <span class="text-xs" data-rating-out aria-live="polite">Sem nota</span>
  </div>
  <textarea name="comment" class="ttsc-textarea" rows="2" placeholder="Comentário (opcional)"></textarea>
  <button type="submit" class="ttsc-btn ttsc-btn-primary ttsc-btn-sm self-start">Enviar avaliação</button>
</form>

<!-- Média somente leitura em card -->
<div class="flex items-center gap-2">
  <div data-ttsc-rating="true" data-ttsc-rating-value="<?= (int) round($avg) ?>" data-ttsc-rating-readonly="true"></div>
  <span class="text-xs"><?= number_format($avg, 1, ',', '') ?> · <?= (int) $total ?> avaliações</span>
</div>
```

### CSS

O JS gera classes utilitárias (`text-yellow-400`, `flex-row-reverse`, `text-muted-foreground/50`) que **não** estão no runtime Tailwind do chassi. Esta ponte é obrigatória:

```css
/* assets/css/ttsc.rating.css — ponte do markup gerado pelo ttscui para tokens */
[data-ttsc-rating] .ttsc-rating { flex-direction: row-reverse; justify-content: flex-end; }
[data-ttsc-rating] .ttsc-rating > span,
[data-ttsc-rating] .ttsc-rating-label { display: inline-flex; padding: 1px; }
[data-ttsc-rating] .text-yellow-400 { color: var(--ttsc-warning); }
[data-ttsc-rating] .text-red-500 { color: var(--ttsc-danger); }
[data-ttsc-rating] [class*="text-muted-foreground"] { color: var(--ttsc-border-prominent); }

/* Pré-visualização no hover: DOM é max…1, então "label:hover ~ label" = notas menores */
[data-ttsc-rating] .ttsc-rating:hover .ttsc-rating-label { color: var(--ttsc-border-prominent); }
[data-ttsc-rating] .ttsc-rating .ttsc-rating-label:hover,
[data-ttsc-rating] .ttsc-rating .ttsc-rating-label:hover ~ .ttsc-rating-label { color: var(--ttsc-warning); }

/* Foco do teclado (o radio fica fora da tela; o contorno vai no label irmão) */
[data-ttsc-rating] input:focus-visible + .ttsc-rating-label {
  outline: 2px solid var(--ttsc-accent); outline-offset: 1px; border-radius: var(--ttsc-radius-xs);
}
```

### JS

```js
// Inicialização automática: TTSC.init() cria todas as instâncias [data-ttsc-rating]
TTSC.init();

// Rótulo acessível e saída de texto em pt-BR
document.addEventListener('ttsc.rating.change', function (event) {
  var host = event.target.closest('[data-ttsc-rating]');
  var value = event.detail.payload.value;
  var max = Number(host.getAttribute('data-ttsc-rating-max') || 5);
  host.querySelector('.ttsc-rating').setAttribute('aria-label', 'Nota ' + (value || 0) + ' de ' + max);
  var out = host.parentElement.querySelector('[data-rating-out]');
  if (out) out.textContent = value ? value + ' de ' + max : 'Sem nota';
});

// Envio assíncrono (sem recarregar) — valida a nota antes
document.querySelectorAll('form[action$="/rating"]').forEach(function (form) {
  form.addEventListener('submit', async function (event) {
    event.preventDefault();
    var rating = TTSC.Rating.getInstance(form.querySelector('[data-ttsc-rating]'));
    if (!rating.getValue()) {
      TTSC.Toast.show({ message: 'Escolha uma nota de 1 a 5.', variant: 'warning' });
      return;
    }
    var response = await fetch(form.action, { method: 'POST', body: new FormData(form) });
    TTSC.Toast.show(response.ok
      ? { message: 'Obrigado! Avaliação registrada.', variant: 'success' }
      : { message: 'Não foi possível registrar a avaliação.', variant: 'destructive' });
  });
});
```

### SQL

Tabela real: `sac_ticket_ratings` (tenant) — `rating tinyint unsigned` (1–5), `comment`, `ticket_id → sac_tickets.id`, `tenant_id`. Estrutura existente:

```sql
-- Já existe no esquema (referência)
CREATE TABLE IF NOT EXISTS sac_ticket_ratings (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  uuid       VARCHAR(36)  NOT NULL UNIQUE,
  ticket_id  BIGINT UNSIGNED NOT NULL,
  tenant_id  VARCHAR(36)  NOT NULL,
  rating     TINYINT UNSIGNED NOT NULL COMMENT '1-5',
  comment    TEXT NULL,
  created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_ticket (ticket_id),
  KEY idx_tenant (tenant_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Gravar a nota (uma por chamado, só depois de resolvido/fechado)
INSERT INTO sac_ticket_ratings (uuid, ticket_id, tenant_id, rating, comment)
SELECT UUID(), t.id, t.tenant_id, :rating, :comment
  FROM sac_tickets t
 WHERE t.uuid = :ticket_uuid
   AND t.status IN ('resolved', 'closed')
   AND NOT EXISTS (SELECT 1 FROM sac_ticket_ratings r WHERE r.ticket_id = t.id);

-- Média e distribuição (card somente leitura)
SELECT ROUND(AVG(r.rating), 1) AS avg_rating,
       COUNT(*)                AS total,
       SUM(r.rating = 5) AS five, SUM(r.rating = 4) AS four, SUM(r.rating = 3) AS three,
       SUM(r.rating = 2) AS two,  SUM(r.rating = 1) AS one
  FROM sac_ticket_ratings r
  JOIN sac_tickets t ON t.id = r.ticket_id
 WHERE r.tenant_id = :tenant_id
   AND r.created_at >= :since;
```

O controller valida `rating` como inteiro 1–5 antes do `INSERT` (o `NOT EXISTS` impede segunda nota). Na leitura, `avg_rating` arredondado vira `data-ttsc-rating-value` e o decimal original aparece no texto ao lado.

## Faça / Não faça

- **Faça:** inclua a ponte CSS; sem ela as estrelas ficam sem cor e em ordem invertida.
- **Faça:** mostre a nota em texto ao lado das estrelas.
- **Não faça:** use rating para notas de prova ou médias com decimais.
- **Não faça:** confie só no front — revalide 1 ≤ nota ≤ `max` no servidor.
