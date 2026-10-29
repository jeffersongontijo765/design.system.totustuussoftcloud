# Popover

Balão flutuante com conteúdo rico (`.ttsc-popover` com header, conteúdo e rodapé) aberto por clique, hover ou foco através do componente tooltip do ttscui (`data-ttsc-tooltip`).

> Também listado em: **Base › Popovers**.

## Quando usar

- Resumo rápido de um registro sem sair da lista: aluno (matrícula, turma, frequência), turma, boleto.
- Explicação de um termo/campo com mais de uma frase (“Carga horária mínima”), aberta por ícone de ajuda.
- Pequena confirmação contextual com 1–2 ações (“Abrir ficha”, “Enviar mensagem”).
- **Não use** para dica de uma linha — use [Tooltip](../Tooltip/README.md) (`.ttsc-tooltip`).
- **Não use** para lista de ações/menu — use [Dropdown](../Dropdown/README.md).
- **Não use** para formulários ou conteúdo longo — use [Drawer](../Drawer/README.md) ou [Modal](../Modal/README.md).

## Anatomia

```
[ gatilho ]  data-ttsc-tooltip="#pop-id"
   ┌─────────────────────────────┐
   │ .ttsc-popover-header        │
   ├─────────────────────────────┤
   │ .ttsc-popover-content       │
   ├─────────────────────────────┤
   │        .ttsc-popover-footer │  (extensão TTSC)
   └─────────────────────────────┘   .ttsc-popover  (+ .show quando aberto)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Gatilho | `button[data-ttsc-tooltip="#id"]` | sim |
| Balão | `div.ttsc-popover#id` (`display:none` até receber `.show`) | sim |
| Cabeçalho | `.ttsc-popover-header` | não |
| Conteúdo | `.ttsc-popover-content` | sim |
| Rodapé | `.ttsc-popover-footer` (extensão TTSC, ações) | não |
| Estático | `.ttsc-popover.show.is-static` — balão aberto no fluxo (documentação, onboarding) | não |

O bundle contém `.ttsc-popover`, `.ttsc-popover-header` e `.ttsc-popover-content` (confirmado em `bundle.css`), mas **não** há módulo JS `popover` no ttscui: o comportamento vem do `tooltip.ts`, que adiciona/remove `.show` e posiciona com Popper.

## Variantes

| Gatilho | Atributos | Uso |
|---|---|---|
| Clique | `data-ttsc-tooltip-trigger="click"` | conteúdo rico com ações (fecha ao clicar fora) |
| Hover | (padrão `hover`) | ajuda de campo, sem ações dentro |
| Foco | `data-ttsc-tooltip-trigger="focus"` | campos de formulário |
| Permanente | `data-ttsc-tooltip-permanent="true"` + click | não fecha ao clicar fora (onboarding) |

Tokens: fundo `--popover` (= `ttsc-surface`), borda `--border`, texto `ttsc-text`/`ttsc-text-2`, sombra `ttsc-shadow-lg`, raio `ttsc-radius-sm`.

## API

Opções do tooltip (`data-ttsc-tooltip-<opção>` ou objeto em `new ttscTooltip(el, {...})`), conferidas em `src/components/tooltip/tooltip.ts`:

| Opção | Padrão | Descrição |
|---|---|---|
| `target` | `""` | seletor do balão (alternativa ao valor de `data-ttsc-tooltip` ou a um filho `[data-ttsc-tooltip-content]`) |
| `trigger` | `hover` | `hover` · `click` · `focus` |
| `placement` / `placementRtl` | `top` | posições Popper: `top`, `bottom-start`, `right`… |
| `offset` / `offsetRtl` | `0, 5px` | deslocamento `skid, distance` |
| `strategy` | `fixed` | estratégia Popper |
| `container` | `""` | `body` ou seletor para onde mover o balão |
| `delayShow` / `delayHide` | `0` | atraso em ms |
| `permanent` | `false` | não fecha no clique externo |
| `zindex` | `100` | z-index mínimo (ajustado ao maior z-index ancestral) |
| `hiddenClass` | `hidden` | classe removida ao abrir |

| Método (`ttscTooltip.getInstance(gatilho)`) | Efeito |
|---|---|
| `show()` · `hide()` · `toggle()` | abre/fecha |
| `isOpen()` | estado |
| `getContentElement()` | o `.ttsc-popover` |

| Evento (`CustomEvent` no gatilho / `instance.on`) | Cancelável |
|---|---|
| `show`, `hide`, `toggle` | sim (`payload.cancel = true`) |
| `shown`, `hidden` | — |

## Acessibilidade

- Gatilho é `<button>`; para popover de clique use `aria-haspopup="dialog"`, `aria-controls` e `role="dialog"` + `aria-label` no balão; atualize `aria-expanded` nos eventos `shown/hidden`.
- Popover de hover/foco é texto auxiliar: `role="tooltip"` + `aria-describedby` no gatilho, e sem elementos focáveis dentro.
- `Esc` fecha (handler no JS abaixo) e o foco volta para o gatilho.
- Ícone de ajuda só-ícone com `aria-label` (“O que é carga horária mínima?”).
- Texto `ttsc-text-2` sobre `ttsc-surface`: ≥ 7:1 no claro e ≥ 8:1 no escuro.

## Modelos

### HTML

```html
<!-- Resumo do aluno ao clicar no nome (linha de tabela) -->
<button type="button" class="ttsc-link" data-ttsc-tooltip="#pop-<?= $this->e($en['uuid']) ?>"
        data-ttsc-tooltip-trigger="click" data-ttsc-tooltip-placement="bottom-start" data-ttsc-tooltip-container="body"
        aria-haspopup="dialog" aria-controls="pop-<?= $this->e($en['uuid']) ?>" aria-expanded="false">
  <?= $this->e($en['student_name']) ?>
</button>
<div class="ttsc-popover" id="pop-<?= $this->e($en['uuid']) ?>" role="dialog" aria-label="Resumo do aluno">
  <div class="ttsc-popover-header"><?= $this->e($en['code']) ?></div>
  <div class="ttsc-popover-content">
    <dl class="grid grid-cols-2 gap-1">
      <dt>Curso</dt><dd><?= $this->e($en['course_name']) ?></dd>
      <dt>Turma</dt><dd><?= $this->e($en['class_code'] ?? '—') ?></dd>
      <dt>Frequência</dt><dd><?= $en['attendance_pct'] === null ? '—' : (int) $en['attendance_pct'] . '%' ?></dd>
    </dl>
  </div>
  <div class="ttsc-popover-footer">
    <a href="/secretaria/matriculas/<?= $this->e($en['uuid']) ?>" class="ttsc-btn ttsc-btn-sm ttsc-btn-primary">Abrir ficha</a>
  </div>
</div>

<!-- Ajuda de campo (hover/foco) -->
<label class="ttsc-form-label" for="min_hours">Carga horária mínima</label>
<button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" data-ttsc-tooltip="#pop-help-hours"
        data-ttsc-tooltip-placement="right" aria-describedby="pop-help-hours" aria-label="O que é carga horária mínima?">
  <i class="fa-light fa-circle-question"></i>
</button>
<div class="ttsc-popover" id="pop-help-hours" role="tooltip">
  <div class="ttsc-popover-header">Carga horária mínima</div>
  <div class="ttsc-popover-content">Total de horas exigido no período para aprovação por frequência (75% da carga da disciplina).</div>
</div>
```

### CSS

```css
/* Runtime (bundle.css): .ttsc-popover { border; background: var(--popover); color: var(--popover-foreground); } .ttsc-popover:not(.show) { display: none } */
.ttsc-popover { width: 280px; max-width: calc(100vw - 32px); box-shadow: var(--ttsc-shadow-lg); border-radius: var(--ttsc-radius-sm); }
.ttsc-popover-header { color: var(--ttsc-text); }
.ttsc-popover-content { color: var(--ttsc-text-2); }
.ttsc-popover-footer { display: flex; justify-content: flex-end; gap: 6px; padding: var(--ttsc-space-2) 10px; border-top: 1px solid var(--ttsc-border); }
.ttsc-popover.is-static { position: static; }
.ttsc-popover-lg { width: 360px; }
```

### JS

```js
// assets/js/core/ttsc.popover.js — popover = ttscTooltip apontando para .ttsc-popover
TTSC.init();

document.querySelectorAll('[data-ttsc-tooltip][aria-haspopup="dialog"]').forEach((trigger) => {
  const tip = ttscTooltip.getInstance(trigger);
  if (!tip) return;
  tip.on('shown', () => {
    trigger.setAttribute('aria-expanded', 'true');
    tip.getContentElement().querySelector('a, button')?.focus();
  });
  tip.on('hidden', () => trigger.setAttribute('aria-expanded', 'false'));
});

// Esc fecha qualquer popover aberto e devolve o foco
document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape') return;
  document.querySelectorAll('[data-ttsc-tooltip-initialized]').forEach((trigger) => {
    const tip = ttscTooltip.getInstance(trigger);
    if (tip?.isOpen()) { tip.hide(); trigger.focus(); }
  });
});

// Conteúdo sob demanda: carrega o resumo na primeira abertura
export function lazyPopover(trigger, url) {
  const tip = ttscTooltip.getOrCreateInstance(trigger, { trigger: 'click', placement: 'bottom-start' });
  let loaded = false;
  tip.on('show', async () => {
    if (loaded) return;
    loaded = true;
    const res = await fetch(url, { headers: { Accept: 'text/html' } });
    tip.getContentElement().querySelector('.ttsc-popover-content').innerHTML = await res.text();
  });
}
```

### SQL

```sql
-- Resumo do aluno exibido no popover (por matrícula)
SELECT en.uuid, en.code, en.status, en.shift,
       u.name   AS student_name,
       co.name  AS course_name,
       cl.code  AS class_code,
       (SELECT ROUND(100 * SUM(a.status IN ('present', 'late')) / NULLIF(COUNT(*), 0))
          FROM attendance a
         WHERE a.enrollment_uuid = en.uuid) AS attendance_pct
  FROM enrollments en
  JOIN users u    ON u.uuid = en.student_uuid
  JOIN courses co ON co.uuid = en.course_uuid
  LEFT JOIN classes cl ON cl.uuid = en.class_uuid AND cl.deleted_at IS NULL
 WHERE en.uuid = :enrollment_uuid
   AND en.deleted_at IS NULL;
```

Na listagem, a mesma consulta (sem o `WHERE en.uuid`) alimenta a tabela e cada linha renderiza seu `.ttsc-popover`; para listas grandes, use `lazyPopover()` com um endpoint que devolve o parcial Plates do resumo.

## Faça / Não faça

- **Faça:** popover de clique para conteúdo com ações; de hover só para texto.
- **Faça:** `data-ttsc-tooltip-container="body"` dentro de tabelas/cards com `overflow: hidden`.
- **Não faça:** colocar formulário ou mais de 2 ações no popover.
- **Não faça:** depender só do hover para informação essencial (não existe em touch).
