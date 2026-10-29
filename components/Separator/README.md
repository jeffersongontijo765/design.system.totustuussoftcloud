# Separator

Linha divisória de 1px do runtime (`.ttsc-separator`), horizontal ou vertical (`.ttsc-separator-vertical`), com extensão TTSC para separador com texto (`.ttsc-separator-label`).

> Também listado em: **Base › Separator**.

## Quando usar

- Separar grupos de conteúdo **dentro** de um mesmo card, drawer ou menu: dados da matrícula × responsáveis, ações × ação destrutiva.
- Separar itens de metadados em linha (toolbar: “32 alunos | 2026/1 | Unidade Centro”) com a versão vertical.
- Agrupar uma lista cronológica por período (“Hoje”, “Ontem”, “Setembro”) com a versão com texto.
- Entre cards ou seções da página **não** use separador: o espaçamento (`--ttsc-section-gap`) e a borda do card já separam.
- Para itens de [Menu](../Menu/README.md) use `.ttsc-menu-separator`; em [Table](../Table/README.md) as bordas de linha já existem.

## Anatomia

```
────────────────────────────          .ttsc-separator               (1px, width 100%)
│                                     .ttsc-separator.ttsc-separator-vertical (1px, height 100%)
──────────  HOJE  ──────────          .ttsc-separator-label > .ttsc-separator + texto + .ttsc-separator
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Linha | `div.ttsc-separator` + `role="separator"` | sim |
| Orientação | `ttsc-separator-vertical` + `aria-orientation="vertical"` | só vertical |
| Com texto | `div.ttsc-separator-label` (extensão TTSC) contendo duas `span.ttsc-separator` | não |

## Variantes

| Variante | Classe | Uso | Tokens |
|---|---|---|---|
| Horizontal | `ttsc-separator` | dentro de cards/drawers | `--border` = `ttsc-border` |
| Vertical | `ttsc-separator ttsc-separator-vertical` | toolbars, metadados em linha (pai com altura definida e `align-items: center`) | idem |
| Com texto | `ttsc-separator-label` | agrupamento por data/categoria | linha `ttsc-border`, texto `ttsc-text-muted` 11px caixa-alta |
| Suave | `ttsc-separator ttsc-separator-soft` (extensão) | listas densas | `ttsc-border-soft` |

## API

Somente CSS — não há JS nem atributos `data-ttsc-*`. A versão vertical ocupa `height: 100%` do pai: o pai precisa de altura (ex.: `height: 32px` ou `align-self: stretch` num flex).

## Acessibilidade

- Separador com significado estrutural: `role="separator"` (vertical também com `aria-orientation="vertical"`).
- Separador puramente decorativo (entre ícones de toolbar): `aria-hidden="true"` em vez de `role`.
- Com texto: `role="separator"` + `aria-label="Hoje"`; o texto visível usa `ttsc-text-muted` (4,9:1 no claro, 5,3:1 no escuro).
- A linha `ttsc-border` é decorativa (não precisa de 3:1); não transmita estado por ela.

## Modelos

### HTML

```html
<!-- Card de matrícula -->
<div class="ttsc-card">
  <div class="ttsc-card-content flex flex-col gap-3">
    <div>
      <div class="font-semibold">Matrícula <?= $e($enrollment['code']) ?></div>
      <div class="text-xs"><?= $e($student['name']) ?> · <?= $e($course['name']) ?></div>
    </div>
    <div class="ttsc-separator" role="separator"></div>
    <dl class="grid grid-cols-2 gap-2 text-xs"> … </dl>
    <div class="ttsc-separator-label" role="separator" aria-label="Responsáveis">
      <span class="ttsc-separator"></span>Responsáveis<span class="ttsc-separator"></span>
    </div>
    …
  </div>
</div>

<!-- Metadados em linha -->
<div class="flex items-center gap-3 text-xs" style="height: 32px">
  <span><i class="fa-light fa-users"></i> 32 alunos</span>
  <div class="ttsc-separator ttsc-separator-vertical" aria-hidden="true"></div>
  <span><i class="fa-light fa-calendar"></i> 2026/1</span>
</div>
```

### CSS

```css
/* Ponte (bundle.css): a linha usa --border */
:root { --border: var(--ttsc-border); }

/* Extensão TTSC: separador com texto */
.ttsc-separator-label {
  display: flex; align-items: center; gap: var(--ttsc-space-3);
  font-size: 11px; font-weight: 500; letter-spacing: .04em; text-transform: uppercase;
  color: var(--ttsc-text-muted);
}
.ttsc-separator-label > .ttsc-separator { flex: 1 1 0; width: auto; }
.ttsc-separator-label.is-start > .ttsc-separator:first-child { display: none; } /* texto alinhado à esquerda */

/* Extensão: variante suave e espaçamento padrão em pilhas */
.ttsc-separator-soft { background-color: var(--ttsc-border-soft); }
.ttsc-separator-spaced { margin-block: var(--ttsc-space-3); }
```

### JS

```js
// Agrupa uma lista cronológica inserindo separadores com texto (Hoje / Ontem / dd/mm/aaaa)
function dayLabel(iso) {
  var d = new Date(iso + 'T00:00:00');
  var today = new Date(); today.setHours(0, 0, 0, 0);
  var diff = Math.round((today - d) / 86400000);
  if (diff === 0) return 'Hoje';
  if (diff === 1) return 'Ontem';
  return d.toLocaleDateString('pt-BR');
}

function renderGrouped(container, rows) {
  var last = null;
  container.innerHTML = '';
  rows.forEach(function (row) {
    var day = row.created_at.slice(0, 10);
    if (day !== last) {
      var sep = document.createElement('div');
      sep.className = 'ttsc-separator-label';
      sep.setAttribute('role', 'separator');
      sep.setAttribute('aria-label', dayLabel(day));
      sep.innerHTML = '<span class="ttsc-separator"></span>' + dayLabel(day) + '<span class="ttsc-separator"></span>';
      container.appendChild(sep);
      last = day;
    }
    var item = document.createElement('div');
    item.className = 'flex justify-between text-xs';
    item.textContent = row.student_name + ' · ' + row.code;
    container.appendChild(item);
  });
}
```

### SQL

O separador não guarda dados; ele agrupa a lista de matrículas recentes por dia (o grupo vem pronto do banco):

```sql
SELECT e.uuid, e.code, u.name AS student_name, e.type, e.created_at,
       CASE WHEN DATE(e.created_at) = CURRENT_DATE THEN 'today'
            WHEN DATE(e.created_at) = CURRENT_DATE - INTERVAL 1 DAY THEN 'yesterday'
            ELSE DATE_FORMAT(e.created_at, '%Y-%m-%d') END AS day_group
  FROM enrollments e
  JOIN users u ON u.uuid = e.student_uuid
 WHERE e.unit_uuid = :unit_uuid
   AND e.deleted_at IS NULL
   AND e.created_at >= CURRENT_DATE - INTERVAL 7 DAY
 ORDER BY e.created_at DESC
 LIMIT 50;
```

Na view Plates, um separador com texto é emitido sempre que `day_group` muda em relação à linha anterior (`today` → “Hoje”, `yesterday` → “Ontem”).

## Faça / Não faça

- **Faça:** use separador só dentro de um container; entre seções use espaço.
- **Faça:** dê altura ao pai do separador vertical.
- **Não faça:** empilhar separador + borda de card no mesmo lugar (linha dupla).
- **Não faça:** usar `<hr>` com estilos próprios ou cores fixas — use a classe e o token.
