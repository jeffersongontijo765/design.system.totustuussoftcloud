# Rotate

Rotação animada de ícones (`.ttsc-rotate` + `ttsc-rotate-90/180/270/n90`) quando o gatilho fica ativo — chevron de collapse/accordion, seta de ordenação — e utilitários de rotação fixa (`rotate-90/180/270`).

## Quando usar

- Chevron que indica aberto/fechado em [Collapse](../Collapse/README.md)/accordion, grupos de menu e linhas expansíveis de tabela.
- Seta de ordenação de coluna (crescente ↔ decrescente).
- Ícone que precisa apontar para outra direção sem trocar de ícone (`rotate-90` numa seta).
- **Não use** para indicar carregamento — use o spinner do [Indicator](../Indicator/README.md).
- **Não use** rotação decorativa contínua.

## Anatomia

```
[ > ] 1º período      →  clique  →   [ v ] 1º período       .ttsc-rotate.ttsc-rotate-90
  .ttsc-rotate-target gira 90° quando o gatilho tem .active ou aria-expanded="true"
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Gatilho | `.ttsc-rotate` + `ttsc-rotate-90` · `-180` · `-270` · `-n90` | sim |
| Estado | `.active` ou `aria-expanded="true"` no gatilho (o ttscui Collapse define os dois) | sim |
| Ícone | `i.ttsc-rotate-target` (ex.: `fa-chevron-right`, `fa-chevron-down`, `fa-arrow-up`) | sim |
| Rotação fixa | `rotate-90` · `rotate-180` · `rotate-270` no próprio ícone | não |

## Variantes

| Classe | Ângulo ativo | Ícone base típico | Uso |
|---|---|---|---|
| `ttsc-rotate-90` | 90° | `fa-chevron-right` | árvore, accordion lateral (› vira ⌄) |
| `ttsc-rotate-180` | 180° | `fa-chevron-down`, `fa-arrow-up` | accordion, ordenação |
| `ttsc-rotate-270` | 270° | `fa-chevron-right` | abrir para cima |
| `ttsc-rotate-n90` | −90° | `fa-chevron-left` | painéis laterais |

Transição: `transform .2s ease`; cor do ícone `ttsc-text-muted`.

## API

CSS da implementação TTSC. O estado vem do componente que controla o gatilho:

| Fonte do estado | O que o JS faz no gatilho |
|---|---|
| ttscui Collapse (`data-ttsc-collapse="#alvo"`) | alterna `aria-expanded` e a classe `active` (`activeClass`), e `hidden` no alvo |
| ttscui Accordion | alterna `active` no item |
| Código próprio | `el.classList.toggle('active')` ou `aria-pressed`/`aria-expanded` |

Eventos do Collapse (no gatilho): `expand`, `expanded`, `collapse`, `collapsed`, `toggle` (canceláveis os três de “antes”).

## Acessibilidade

- O ícone é decorativo (`aria-hidden` implícito para `<i>` vazio); o estado é comunicado por `aria-expanded` (collapse) ou `aria-pressed`/`aria-sort` (ordenação).
- Em cabeçalho de tabela ordenável, use `aria-sort="ascending|descending"` no `<th>` e atualize o `aria-label` do botão.
- `prefers-reduced-motion: reduce`: a rotação acontece sem transição.
- Gatilho é `<button>`; área de clique inclui o texto, não só o ícone.

## Modelos

### HTML

```html
<!-- Grade curricular por período (collapse do ttscui) -->
<?php foreach ($periods as $number => $period): ?>
  <button type="button" class="ttsc-rotate ttsc-rotate-90 flex items-center gap-2 w-full p-3 <?= $number === 1 ? 'active' : '' ?>"
          aria-expanded="<?= $number === 1 ? 'true' : 'false' ?>" data-ttsc-collapse="#period-<?= (int) $number ?>">
    <i class="fa-light fa-chevron-right ttsc-rotate-target"></i>
    <span class="font-semibold"><?= (int) $number ?>º período</span>
    <span class="text-xs text-muted-foreground"><?= (int) $period['subjects'] ?> disciplinas · <?= (int) $period['hours'] ?> h</span>
  </button>
  <div id="period-<?= (int) $number ?>" class="<?= $number === 1 ? 'active' : 'hidden' ?>" style="transition: height .2s ease">
    <ul>
      <?php foreach ($period['items'] as $s): ?>
        <li><?= $this->e($s['name']) ?> · <?= (int) $s['workload'] ?> h<?= $s['is_optional'] ? ' (optativa)' : '' ?></li>
      <?php endforeach ?>
    </ul>
  </div>
<?php endforeach ?>

<!-- Ordenação de coluna -->
<th aria-sort="ascending">
  <button type="button" class="ttsc-rotate ttsc-rotate-180 inline-flex items-center gap-1" data-sort="student_name" aria-label="Ordenar por nome, crescente">
    Nome do aluno <i class="fa-light fa-arrow-up ttsc-rotate-target"></i>
  </button>
</th>
```

### CSS

```css
.ttsc-rotate-target { display: inline-block; transition: transform .2s ease; }
.ttsc-rotate.active.ttsc-rotate-90  .ttsc-rotate-target, .ttsc-rotate[aria-expanded="true"].ttsc-rotate-90  .ttsc-rotate-target { transform: rotate(90deg); }
.ttsc-rotate.active.ttsc-rotate-180 .ttsc-rotate-target, .ttsc-rotate[aria-expanded="true"].ttsc-rotate-180 .ttsc-rotate-target { transform: rotate(180deg); }
.ttsc-rotate.active.ttsc-rotate-270 .ttsc-rotate-target, .ttsc-rotate[aria-expanded="true"].ttsc-rotate-270 .ttsc-rotate-target { transform: rotate(270deg); }
.ttsc-rotate.active.ttsc-rotate-n90 .ttsc-rotate-target, .ttsc-rotate[aria-expanded="true"].ttsc-rotate-n90 .ttsc-rotate-target { transform: rotate(-90deg); }
.rotate-90 { transform: rotate(90deg); }
.rotate-180 { transform: rotate(180deg); }
.rotate-270 { transform: rotate(270deg); }
.ttsc-rotate .ttsc-rotate-target { color: var(--ttsc-text-muted); }
@media (prefers-reduced-motion: reduce) { .ttsc-rotate-target { transition: none; } }
```

### JS

```js
// Collapse: nada a fazer além de TTSC.init() — o ttscui alterna .active/aria-expanded.
TTSC.init();

// Ordenação: gira a seta e atualiza aria-sort no <th>
document.querySelectorAll('th button[data-sort].ttsc-rotate').forEach((button) => {
  button.addEventListener('click', () => {
    const desc = button.classList.toggle('active');
    const th = button.closest('th');
    th.setAttribute('aria-sort', desc ? 'descending' : 'ascending');
    button.setAttribute('aria-label', `Ordenar por nome, ${desc ? 'decrescente' : 'crescente'}`);
    const url = new URL(window.location.href);
    url.searchParams.set('sort', button.dataset.sort);
    url.searchParams.set('dir', desc ? 'desc' : 'asc');
    window.location.assign(url);
  });
});

// Reagir ao collapse (ex.: carregar disciplinas sob demanda)
document.querySelectorAll('[data-ttsc-collapse]').forEach((toggle) => {
  toggle.addEventListener('expanded', () => toggle.closest('section')?.classList.add('is-open'));
});
```

### SQL

```sql
-- Disciplinas da matriz por período (alimenta os collapses com chevron)
SELECT cs.period_number, s.code, s.name, cs.workload, cs.is_optional,
       SUM(cs.workload) OVER (PARTITION BY cs.period_number) AS period_hours,
       COUNT(*)         OVER (PARTITION BY cs.period_number) AS period_subjects
  FROM curriculum_subjects cs
  JOIN subjects s ON s.uuid = cs.subject_uuid AND s.deleted_at IS NULL
 WHERE cs.curriculum_uuid = :curriculum_uuid
 ORDER BY cs.period_number, s.name;
```

O controller agrupa as linhas por `period_number` em `$periods[n] = ['subjects' => …, 'hours' => …, 'items' => […]]`; o primeiro período vem aberto. Funções de janela rodam em MariaDB 10.2+ e MySQL 8.

## Faça / Não faça

- **Faça:** um ícone só que gira (chevron), em vez de trocar `fa-chevron-right` por `fa-chevron-down`.
- **Faça:** manter `aria-expanded` como fonte de verdade.
- **Não faça:** girar ícones com significado próprio (lixeira, calendário).
- **Não faça:** transições acima de 300 ms.
