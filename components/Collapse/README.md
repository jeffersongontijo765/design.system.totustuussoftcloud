# Collapse

Gatilho que mostra e esconde **um** bloco com animação de altura (`data-ttsc-collapse="#alvo"`), sem precisar de lista como o Accordion.

## Quando usar

- “Filtros avançados” na toolbar de uma listagem (matrículas, mensalidades).
- “Mostrar mais” em blocos longos do drawer do aluno (observações, histórico de ocorrências).
- Detalhe opcional de um formulário: “Adicionar responsável financeiro diferente do aluno”.
- Grupo de várias seções exclusivas → [Accordion](../Accordion/README.md).
- Conteúdo sobreposto que fecha ao clicar fora → [Dropdown](../Dropdown/README.md).
- Remover/esconder definitivamente um aviso → [Dismiss](../Dismiss/README.md).

## Anatomia

```
[ ⚙ Filtros avançados  ˅ ]   button[data-ttsc-collapse="#filtros"]  (.active + aria-expanded quando aberto)
┌ #filtros  .hidden | .active ──────────────────────────────┐
│ conteúdo (transição de height, overflow hidden)           │
└───────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Gatilho | `button[data-ttsc-collapse="#id"]` + `aria-controls="id"` + `aria-expanded` | sim |
| Alvo | elemento `#id` com `.hidden` (fechado) **ou** `.active` (aberto) | sim |
| Animação | `transition: height …` no alvo (classe `ttsc-collapse-target`, extensão) — o JS espera `transition-duration` | recomendado |
| Indicador | ícone dentro do gatilho girado via `.active` (extensão) | não |

Um alvo pode ter vários gatilhos (ex.: botão no topo e link “Fechar” no fim): cada `[data-ttsc-collapse]` cria a própria instância e lê o estado pela classe `active` do alvo.

## Estados

| Estado | Gatilho | Alvo |
|---|---|---|
| Fechado | `aria-expanded="false"` | `.hidden` |
| Abrindo | `.active`, `aria-expanded="true"` | `.hidden` removida, `height: 0 → scrollHeight`, `overflow: hidden` |
| Aberto | `.active` | `.active`, `height` livre |
| Fechando | `.active` removida | `height: scrollHeight → 0`, depois `.hidden` |

## API

Opções (`data-ttsc-collapse-<opção>` no gatilho):

| Atributo / opção | Padrão | Efeito |
|---|---|---|
| `data-ttsc-collapse="#id"` | — | seletor do alvo (obrigatório; alternativa: opção `target`) |
| `hiddenClass` | `hidden` | classe do alvo fechado |
| `activeClass` | `active` | classe do gatilho e do alvo aberto |

Métodos (`const c = ttscCollapse.getInstance(botao)` ou `TTSC.Collapse.getOrCreateInstance(botao)`):

| Método | Descrição |
|---|---|
| `expand()` / `collapse()` | abre / fecha (ignorado durante animação) |
| `isOpen()` | `true` se o alvo tem `activeClass` |
| `on(evt, fn)` / `off(evt, id)` | ouvintes da instância |

Eventos (CustomEvent no **gatilho**, `bubbles`; `detail.payload.cancel = true` cancela):

| Evento | Quando | Cancelável |
|---|---|---|
| `toggle` | clique, antes de decidir | sim |
| `expand` / `expanded` | antes / depois de abrir | `expand` sim |
| `collapse` / `collapsed` | antes / depois de fechar | `collapse` sim |

## Acessibilidade

- Gatilho é `<button type="button">` (o JS chama `preventDefault`, então `<a href>` também funciona, mas prefira botão).
- O runtime atualiza `aria-expanded` no gatilho; declare o valor inicial no HTML e `aria-controls` com o id do alvo.
- Ao abrir “Filtros avançados”, mova o foco para o primeiro campo (evento `expanded`), e ao fechar devolva o foco ao gatilho.
- O ícone indicador é `aria-hidden="true"`; o rótulo pode trocar (“Mostrar mais” / “Mostrar menos”).
- Rótulo do gatilho em `ttsc-text`; link de texto em `ttsc-accent-text` (nunca `ttsc-accent`).

## Modelos

### HTML

```html
<!-- Toolbar da listagem de matrículas -->
<div class="flex items-center gap-2">
  <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-sm ttsc-collapse-toggle"
          data-ttsc-collapse="#filtros-avancados" aria-controls="filtros-avancados" aria-expanded="false">
    <i class="fa-light fa-sliders"></i> Filtros avançados <i class="fa-light fa-chevron-down ttsc-collapse-indicator" aria-hidden="true"></i>
  </button>
</div>
<div id="filtros-avancados" class="ttsc-collapse-target hidden">
  <form class="grid grid-cols-3 gap-3 pt-3" method="get">
    <label class="ttsc-label">Curso
      <select class="ttsc-select" name="course_uuid">
        <option value="">Todos</option>
        <?php foreach ($courses as $c): ?>
        <option value="<?= $this->e($c['uuid']) ?>"><?= $this->e($c['name']) ?> (<?= (int) $c['active_enrollments'] ?>)</option>
        <?php endforeach; ?>
      </select>
    </label>
    <!-- turno, período… -->
  </form>
</div>

<!-- Mostrar mais (drawer do aluno), aberto por padrão -->
<button type="button" class="ttsc-link ttsc-link-sm ttsc-collapse-toggle active" data-ttsc-collapse="#obs-aluno" aria-controls="obs-aluno" aria-expanded="true">
  Observações <i class="fa-light fa-chevron-down ttsc-collapse-indicator" aria-hidden="true"></i>
</button>
<div id="obs-aluno" class="ttsc-collapse-target active">…</div>
```

### CSS

```css
/* Extensão TTSC: o módulo anima height, mas só espera a transição se ela existir */
.ttsc-collapse-target { transition: height .25s ease; }
.ttsc-collapse-indicator { transition: transform .2s ease; font-size: 12px; color: var(--ttsc-text-muted); }
.ttsc-collapse-toggle.active .ttsc-collapse-indicator { transform: rotate(180deg); }
.ttsc-collapse-toggle.active.ttsc-btn-outline { background: var(--ttsc-canvas-2); border-color: var(--ttsc-border-strong); }

/* Painel de filtros */
#filtros-avancados > form { border-top: 1px dashed var(--ttsc-border); margin-top: var(--ttsc-space-3); }

@media (prefers-reduced-motion: reduce) { .ttsc-collapse-target, .ttsc-collapse-indicator { transition: none; } }
```

### JS

```js
// Foco e persistência do painel "Filtros avançados" (localStorage por usuário/página)
const toggle = document.querySelector('[data-ttsc-collapse="#filtros-avancados"]');
const key = `ttsc:filters-open:${location.pathname}`;
const collapse = TTSC.Collapse.getOrCreateInstance(toggle);

try { if (localStorage.getItem(key) === '1' && !collapse.isOpen()) collapse.expand(); } catch (e) { /* storage bloqueado */ }

toggle.addEventListener('expanded', () => {
  document.querySelector('#filtros-avancados select, #filtros-avancados input')?.focus();
  try { localStorage.setItem(key, '1'); } catch (e) {}
});
toggle.addEventListener('collapsed', () => {
  toggle.focus();
  try { localStorage.removeItem(key); } catch (e) {}
});

// Não fecha se houver filtro preenchido e não aplicado
toggle.addEventListener('collapse', (event) => {
  const form = document.querySelector('#filtros-avancados form');
  if (form.dataset.dirty === 'true') event.detail.payload.cancel = true;
});
document.querySelector('#filtros-avancados form').addEventListener('change', (e) => { e.currentTarget.dataset.dirty = 'true'; });
```

### SQL

O collapse não guarda dados (o estado aberto/fechado fica no navegador). A consulta alimenta o conteúdo do painel — opções de curso com a contagem de matrículas ativas:

```sql
SELECT c.uuid, c.name, COUNT(e.id) AS active_enrollments
  FROM courses c
  LEFT JOIN enrollments e
         ON e.course_uuid = c.uuid AND e.status = 'active' AND e.deleted_at IS NULL
 WHERE c.unit_uuid = :unit_uuid
   AND c.is_active = 1
   AND c.deleted_at IS NULL
 GROUP BY c.uuid, c.name
 ORDER BY c.name;
```

O controller passa `$courses` para a view; se a URL já trouxer algum filtro avançado (`?course_uuid=…`), renderize o alvo com `active` (sem `hidden`) e o gatilho com `active` + `aria-expanded="true"`.

## Faça / Não faça

- **Faça:** um gatilho com rótulo explícito do que abre; ícone chevron girando.
- **Faça:** abrir já expandido quando há filtro avançado aplicado.
- **Faça:** `transition: height` no alvo (sem ela a troca é instantânea, mas o JS funciona).
- **Não faça:** esconder campos obrigatórios dentro de collapse.
- **Não faça:** collapse dentro de collapse; acima de dois níveis use outra página ou drawer.
