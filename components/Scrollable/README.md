# Scrollable

Área com rolagem interna do ttscui (`data-ttsc-scrollable`): altura fixa, máxima ou **automática** (viewport menos cabeçalhos e offset), recalculada no resize, com barra fina do chassi (`.ttsc-scrollable-*`).

> Também listado em: **Geral › Scroll**.

## Quando usar

- Listas longas dentro de cards e painéis que não podem empurrar a página: avisos da turma, chamada do dia, timeline de um aluno, itens do sub-sidebar.
- Painéis que devem ocupar “o resto da tela” abaixo do topbar e da toolbar (`height="auto"` + `dependencies`).
- Para tabelas grandes com paginação use [DataTable](../DataTable/README.md) (rolagem horizontal via `.ttsc-table-wrapper`).
- A página inteira **não** usa scrollable: o chassi já rola em `.ttsc-content`.
- Se o conteúdo cabe quase sempre, prefira `max-height` a `height` fixa (sem espaço vazio).

## Anatomia

```
.card
  ├ cabeçalho fixo
  └ div.ttsc-scrollable-y-auto[data-ttsc-scrollable]   ← style height/max-height aplicado pelo JS
       └ conteúdo (lista, timeline…)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Container | `[data-ttsc-scrollable="true"]` | sim |
| Altura | `data-ttsc-scrollable-height` **ou** `-min-height` **ou** `-max-height` | sim |
| Estilo da barra | `ttsc-scrollable` · `-y` · `-x` · `-auto` · `-y-auto` · `-x-auto` · `-hover` · `-y-hover` · `-x-hover` | recomendado |
| Persistência | `id` + `data-ttsc-scrollable-state="true"` | não |

## Variantes

| Classe | Overflow | Barra |
|---|---|---|
| `ttsc-scrollable-y-auto` | vertical, só quando precisa | sempre visível (fina, 0,35 rem) |
| `ttsc-scrollable-y-hover` | vertical | aparece só no hover |
| `ttsc-scrollable-x-auto` | horizontal | carrosséis de cards, kanban |
| `ttsc-scrollable` / `-auto` | ambos | tabelas pivô |

Tokens: polegar `--scrollbar-thumb-color` (padrão `--color-input` → ponte `ttsc-border-strong`), trilho transparente, raio `1.25rem`.

## API

Opções por atributo `data-ttsc-scrollable-<opção>` ou variável CSS `--ttsc-scrollable-<opção>` (a variável CSS tem prioridade — permite alturas diferentes por breakpoint):

| Atributo | Padrão | Efeito |
|---|---|---|
| `data-ttsc-scrollable` | — | ativa |
| `-height` | — | número (px) ou `auto` |
| `-min-height` / `-max-height` | — | idem, aplicado como `min-height`/`max-height` (tem prioridade sobre `height`) |
| `-dependencies` | `""` | seletores cujas **alturas** (+ margens/bordas) são subtraídas no modo `auto` |
| `-wrappers` | `""` | seletores cujos **paddings/margens/bordas** são subtraídos no modo `auto` |
| `-offset` | `""` | px extras subtraídos no `auto` — **use com unidade** (`"24px"`): um número puro vira `Number` e é ignorado pela versão atual |
| `-state` | — | `true` + `id` no elemento: restaura o `scrollTop` salvo em `localStorage["<id>st"]` |

Fórmula do `auto`: `altura do viewport − espaçamento do próprio elemento − Σ dependencies − Σ wrappers − offset`.

| Método | Efeito |
|---|---|
| `TTSC.Scrollable.getInstance(el)` / `getOrCreateInstance(el, config)` | instância |
| `inst.update()` | recalcula altura e estado (chame após mostrar/ocultar dependências) |
| `inst.getHeight()` | altura calculada, ex. `"412px"` |
| `TTSC.Scrollable.init()` | cria instâncias + listener de resize (throttle 200 ms), uma vez |

Sem eventos próprios; o scroll grava `localStorage` sempre que o elemento tem `id`.

## Acessibilidade

- Área rolável com conteúdo não focável precisa ser alcançável por teclado: `tabindex="0"`, `role="region"` e `aria-label` (“Lista de chamada”).
- Não esconda a barra em listas críticas (`-hover` só em listas secundárias): usuários de trackpad sem hover não percebem que há mais itens.
- Contraste do texto interno segue os tokens normais; o polegar `ttsc-border-strong` é decorativo.
- Respeite `prefers-reduced-motion` ao rolar programaticamente (`behavior: 'auto'`).

## Modelos

### HTML

```html
<!-- Chamada do dia: ocupa o resto da tela abaixo do topbar e da toolbar -->
<div class="ttsc-card">
  <div class="ttsc-card-header" id="attendance-head">
    <h3 class="ttsc-card-title">Chamada · 3º A · 21/10/2026</h3>
  </div>
  <div id="attendance-list"
       class="ttsc-scrollable-y-auto"
       role="region" aria-label="Lista de chamada" tabindex="0"
       data-ttsc-scrollable="true"
       data-ttsc-scrollable-height="auto"
       data-ttsc-scrollable-dependencies="#topbar, #attendance-head, #attendance-toolbar"
       data-ttsc-scrollable-wrappers=".ttsc-content"
       data-ttsc-scrollable-offset="24px"
       data-ttsc-scrollable-state="true">
    <?php foreach ($students as $s): ?>
      <div class="flex items-center justify-between px-4 py-2"> … </div>
    <?php endforeach; ?>
  </div>
</div>

<!-- Avisos: no máximo 240px -->
<div class="ttsc-scrollable-y-hover" data-ttsc-scrollable="true" data-ttsc-scrollable-max-height="240"> … </div>
```

### CSS

```css
/* Ponte: cor do polegar com token */
[data-ttsc-scrollable] { --scrollbar-thumb-color: var(--ttsc-border-strong); }
[data-ttsc-scrollable]:hover { --scrollbar-thumb-color: var(--ttsc-border-prominent); }

/* Altura por breakpoint via variável CSS (tem prioridade sobre o atributo) */
@media (max-width: 767.98px) {
  #attendance-list { --ttsc-scrollable-height: 360; }
}

/* Sombra de "há mais conteúdo" no rodapé da área */
.ttsc-scrollable-fade { mask-image: linear-gradient(to bottom, #000 calc(100% - var(--ttsc-space-6)), transparent); }
```

### JS

```js
TTSC.init();

var list = document.getElementById('attendance-list');
var scroll = TTSC.Scrollable.getOrCreateInstance(list);

// Dependência mudou de altura (ex.: banner de aviso fechado) → recalcula
document.addEventListener('dismissed', function () { scroll.update(); }); // evento do Dismiss (bubbles)

// Rola até o primeiro aluno sem registro
var pending = list.querySelector('[data-status="pending"]');
if (pending) {
  list.scrollTo({
    top: pending.offsetTop - list.offsetTop,
    behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
  });
}
console.debug('altura da chamada', scroll.getHeight());
```

### SQL

A área rolável exibe a chamada do dia da turma (uma linha por matrícula ativa, com o status já lançado):

```sql
SELECT e.uuid AS enrollment_uuid,
       u.name AS student_name,
       COALESCE(a.status, 'pending') AS status
  FROM enrollments e
  JOIN users u ON u.uuid = e.student_uuid
  LEFT JOIN attendance a
         ON a.enrollment_uuid = e.uuid
        AND a.lesson_date = :lesson_date
        AND a.subject_uuid = :subject_uuid
 WHERE e.class_uuid = :class_uuid
   AND e.status = 'active'
   AND e.deleted_at IS NULL
 ORDER BY u.name;
```

O controller entrega `$students` à view; cada linha recebe `data-status="<?= $e($s['status']) ?>"`, usado pelo JS para rolar até o primeiro pendente.

## Faça / Não faça

- **Faça:** use `height="auto"` com `dependencies` para painéis de tela cheia e `max-height` para cards.
- **Faça:** passe `offset` com unidade (`"24px"`).
- **Não faça:** aninhar duas áreas roláveis verticais.
- **Não faça:** área rolável sem `tabindex`/`aria-label` quando o conteúdo não tem elementos focáveis.
