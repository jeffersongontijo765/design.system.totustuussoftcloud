# Ribbon

Fita/etiqueta de canto (`.ttsc-ribbon`) presa à borda de um card para destacar uma condição do item inteiro — “Novo”, “Vagas esgotadas”, “Últimas vagas”, “Bolsa 50%”.

## Quando usar

- Vitrine de cursos/turmas (processo seletivo, rematrícula, portal do aluno) com uma condição comercial ou de disponibilidade.
- Um único destaque por card, lido antes do conteúdo.
- **Não use** para status operacionais em listas e tabelas — use [Badge](../Badge/README.md).
- **Não use** mais de uma fita por card nem em todos os cards da grade (perde o destaque).
- Para avisos com texto longo, use [Alert](../Alert/README.md) dentro do card.

## Anatomia

```
┌──────────────────────[ Novo ]   .ttsc-ribbon (tag, borda direita)
│ ícone                    │
│ Análise de Sistemas      │      .ttsc-ribbon-host (position: relative; overflow: hidden)
└──────────────────────────┘
┌──────────────────────╲Bolsa╲    .ttsc-ribbon.ttsc-ribbon-corner (faixa diagonal 45°)
```

| Parte | Classe | Obrigatório |
|---|---|---|
| Card | `.ttsc-ribbon-host` (com `ttsc-card` ou equivalente) | sim |
| Fita | `span.ttsc-ribbon` (texto curto, ≤ 16 caracteres) | sim |
| Lado | (direita) · `ttsc-ribbon-start` (esquerda) | não |
| Forma | (tag) · `ttsc-ribbon-corner` (diagonal) | não |
| Cor | (accent) · `ttsc-ribbon-danger` · `-warning` · `-info` · `-mono` | não |
| Ícone | `<i class="fa-light …">` antes do texto | não |

## Variantes

| Variante | Classe | Uso | Tokens (fundo / texto) |
|---|---|---|---|
| Accent | `ttsc-ribbon` | Novo, inscrições abertas | `ttsc-accent` / `ttsc-accent-on` |
| Danger | `ttsc-ribbon-danger` | Vagas esgotadas, encerrado | `ttsc-danger` / branco (4,8:1) |
| Warning | `ttsc-ribbon-warning` | Últimas vagas, prazo final | `ttsc-warning` / `ttsc-accent-on` |
| Info | `ttsc-ribbon-info` | Bolsa, convênio | `ttsc-info` / `ttsc-accent-on` |
| Mono | `ttsc-ribbon-mono` | Destaque neutro (“Recomendado”) | `ttsc-text` / `ttsc-surface` |
| Corner | `ttsc-ribbon-corner` | promoção/condição visual forte | mesma cor da variante |

Card esgotado: além da fita danger, aplique fundo `ttsc-canvas-2` e desabilite o botão “Inscrever”.

## API

Somente CSS (implementação TTSC). Personalização por variáveis no elemento:

| Variável | Padrão | Efeito |
|---|---|---|
| `--ttsc-ribbon-bg` | `var(--ttsc-accent)` | fundo da fita |
| `--ttsc-ribbon-fg` | `var(--ttsc-accent-on)` | texto da fita |

## Acessibilidade

- O texto da fita é conteúdo real: o leitor o lê. Para que venha junto do nome, inclua a condição no `aria-label` do card (“Enfermagem, vagas esgotadas”) ou posicione a fita após o título no DOM.
- Cor nunca sozinha: a fita sempre tem texto (“Vagas esgotadas”), não só vermelho.
- Contrastes ≥ 4,5:1 conforme tabela; o texto da fita tem 11px/600 — não reduza mais.
- Na faixa diagonal o texto é rotacionado: mantenha 1–2 palavras.

## Modelos

### HTML

```html
<?php foreach ($classes as $cl): ?>
  <article class="ttsc-card p-4 ttsc-ribbon-host<?= $cl['ribbon'] === 'sold_out' ? ' is-full' : '' ?>"
           aria-label="<?= $this->e($cl['course_name'] . ' ' . $cl['name'] . ($cl['ribbon'] === 'sold_out' ? ', vagas esgotadas' : '')) ?>">
    <?php if ($cl['ribbon'] === 'new'): ?>
      <span class="ttsc-ribbon">Novo</span>
    <?php elseif ($cl['ribbon'] === 'sold_out'): ?>
      <span class="ttsc-ribbon ttsc-ribbon-danger"><i class="fa-light fa-ban"></i> Vagas esgotadas</span>
    <?php elseif ($cl['ribbon'] === 'last_seats'): ?>
      <span class="ttsc-ribbon ttsc-ribbon-warning">Últimas vagas</span>
    <?php endif ?>
    <h3 class="font-semibold"><?= $this->e($cl['course_name']) ?></h3>
    <p class="text-xs text-muted-foreground"><?= $this->e($cl['name']) ?></p>
    <p class="text-xs"><?= (int) $cl['enrolled'] ?> de <?= (int) $cl['max_students'] ?> vagas ocupadas</p>
    <button type="button" class="ttsc-btn ttsc-btn-primary ttsc-btn-sm" <?= $cl['ribbon'] === 'sold_out' ? 'disabled' : '' ?>>Inscrever</button>
  </article>
<?php endforeach ?>
```

### CSS

```css
.ttsc-ribbon-host { position: relative; overflow: hidden; }
.ttsc-ribbon-host.is-full { background: var(--ttsc-canvas-2); }
.ttsc-ribbon { --ttsc-ribbon-bg: var(--ttsc-accent); --ttsc-ribbon-fg: var(--ttsc-accent-on);
  position: absolute; top: 12px; right: 0; z-index: 1; display: inline-flex; align-items: center; gap: 6px;
  padding: 3px 10px 3px 12px; font-size: 11px; line-height: 16px; font-weight: 600; letter-spacing: .02em;
  background: var(--ttsc-ribbon-bg); color: var(--ttsc-ribbon-fg);
  border-radius: var(--ttsc-radius-xs) 0 0 var(--ttsc-radius-xs); box-shadow: var(--ttsc-shadow-sm); }
.ttsc-ribbon-start { right: auto; left: 0; border-radius: 0 var(--ttsc-radius-xs) var(--ttsc-radius-xs) 0; padding: 3px 12px 3px 10px; }
.ttsc-ribbon-corner { top: 18px; right: -34px; width: 132px; justify-content: center; padding: 4px 0; border-radius: 0; transform: rotate(45deg); }
.ttsc-ribbon-danger  { --ttsc-ribbon-bg: var(--ttsc-danger);  --ttsc-ribbon-fg: #fff; }
.ttsc-ribbon-warning { --ttsc-ribbon-bg: var(--ttsc-warning); --ttsc-ribbon-fg: var(--ttsc-accent-on); }
.ttsc-ribbon-info    { --ttsc-ribbon-bg: var(--ttsc-info);    --ttsc-ribbon-fg: var(--ttsc-accent-on); }
.ttsc-ribbon-mono    { --ttsc-ribbon-bg: var(--ttsc-text);    --ttsc-ribbon-fg: var(--ttsc-surface); }
```

### JS

```js
// Sem JS obrigatório. Atualização ao vivo de vagas (ex.: após inscrição via AJAX)
function ensureRibbon(card) {
  let ribbon = card.querySelector(':scope > .ttsc-ribbon');
  if (!ribbon) {
    ribbon = document.createElement('span');
    card.prepend(ribbon);
  }
  return ribbon;
}

export function updateSeats(card, enrolled, max) {
  const free = max - enrolled;
  if (free <= 0) {
    const ribbon = ensureRibbon(card);
    ribbon.className = 'ttsc-ribbon ttsc-ribbon-danger';
    ribbon.textContent = 'Vagas esgotadas';
    card.classList.add('is-full');
    card.querySelector('.ttsc-btn-primary')?.setAttribute('disabled', '');
  } else if (free <= 5) {
    const ribbon = ensureRibbon(card);
    ribbon.className = 'ttsc-ribbon ttsc-ribbon-warning';
    ribbon.textContent = 'Últimas vagas';
  }
}
```

### SQL

```sql
-- Turmas com ocupação e a fita calculada (sold_out / last_seats / new)
SELECT cl.uuid, cl.code, cl.name, co.name AS course_name, cl.shift, cl.modality, cl.max_students,
       COUNT(en.id) AS enrolled,
       CASE
         WHEN cl.max_students IS NOT NULL AND COUNT(en.id) >= cl.max_students     THEN 'sold_out'
         WHEN cl.max_students IS NOT NULL AND cl.max_students - COUNT(en.id) <= 5 THEN 'last_seats'
         WHEN cl.created_at >= NOW() - INTERVAL 30 DAY                           THEN 'new'
         ELSE NULL
       END AS ribbon
  FROM classes cl
  JOIN courses co ON co.uuid = cl.course_uuid AND co.deleted_at IS NULL
  LEFT JOIN enrollments en
         ON en.class_uuid = cl.uuid AND en.deleted_at IS NULL AND en.status IN ('active', 'pending')
 WHERE cl.deleted_at IS NULL
   AND cl.is_active = 1
   AND cl.unit_uuid = :unit_uuid
 GROUP BY cl.uuid, cl.code, cl.name, co.name, cl.shift, cl.modality, cl.max_students, cl.created_at
 ORDER BY co.name, cl.name;
```

O controller passa `$classes`; a view escolhe a fita pelo campo `ribbon` (a regra fica no SQL, não espalhada no HTML). O servidor revalida a vaga no momento da inscrição.

## Faça / Não faça

- **Faça:** texto curto e em pt-BR; uma fita por card.
- **Faça:** card esgotado também com botão desabilitado e fundo `ttsc-canvas-2`.
- **Não faça:** fita verde com texto branco (≈2:1) ou fita amarela com texto branco.
- **Não faça:** usar fita como badge de status em tabela.
