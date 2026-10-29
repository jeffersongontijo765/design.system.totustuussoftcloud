# ButtonGroup

Botões colados em uma faixa única (`.ttsc-toggle-group`), usados como controle segmentado de escolha única/múltipla ou como toolbar de ações relacionadas.

## Quando usar

- **Segmentado (escolha única):** alternar vista da listagem (Tabela · Kanban · Calendário), período (Hoje · Semana · Mês), turno (Manhã · Tarde · Noite) quando são 2–5 opções curtas.
- **Seleção múltipla:** filtros rápidos combináveis (Ativas, Trancadas, Condicionais).
- **Toolbar:** ações irmãs sobre o mesmo alvo — anterior/próximo, zoom, alinhamento, exportar CSV/PDF/XLSX.
- Mais de 5 opções ou rótulos longos: use um select ou o [Dropdown](../Dropdown/README.md).
- Para navegar entre seções de conteúdo use abas (`ttsc-tabs`); para ações independentes use [Button](../Button/README.md) separados com `gap-2`.

## Anatomia

```
┌──────────┬──────────┬──────────────┐
│ ▦ Tabela │ ▤ Kanban │ ▣ Calendário │   .ttsc-toggle-group  (role="radiogroup" | "toolbar")
└──────────┴──────────┴──────────────┘
   .ttsc-btn.active  ← selecionado (ou label.ttsc-btn:has(input:checked))
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Grupo | `div.ttsc-toggle-group` + `role` (`radiogroup`, `group` ou `toolbar`) + `aria-label` | sim |
| Item | `.ttsc-btn` (qualquer tamanho: `ttsc-btn-sm`, padrão, `ttsc-btn-lg`) | sim |
| Selecionado | `.active` no botão **ou** `<label class="ttsc-btn"><input type="radio" …>` (o CSS usa `:has(input:checked)` e esconde o input) | segmentado |
| Ícone | `<i class="fa-light fa-…">` | não |
| Só ícone | `ttsc-btn-icon` + `aria-label` | não |

O runtime remove o raio interno (`:not(:first-child)` / `:not(:last-child)`) e a borda da direita, deixando uma borda única de `--border` (`ttsc-border`).

## Variantes

| Variante | Marcação | Uso | Tokens |
|---|---|---|---|
| Segmentado (radio) | `label.ttsc-btn > input[type=radio]` | vista, período, turno | item: transparente, texto `ttsc-text`, ícone `ttsc-text-muted`; selecionado (extensão): fundo `ttsc-accent-soft`, texto `ttsc-accent-text` |
| Múltipla escolha | `label.ttsc-btn > input[type=checkbox]` | filtros combináveis | idem |
| Toolbar | `button.ttsc-btn` sem estado | ações irmãs | hover/focus: fundo `--accent` (= `ttsc-canvas-2`) |
| Compacto | `.ttsc-btn-sm` nos itens | cabeçalho de card, toolbar de tabela | altura 32px |
| Bloco | `.ttsc-toggle-group.w-full` | mobile, drawers | itens `flex-grow: 1` (runtime) |

## Estados

| Estado | Como aplicar |
|---|---|
| Selecionado | `input:checked` (radio/checkbox) ou `.active` + `aria-pressed="true"` no botão |
| Hover / foco | automático — fundo `--accent`; foco com contorno 2px `ttsc-accent` |
| Desabilitado | `disabled` no `<button>`/`<input>` (o label ganha `aria-disabled="true"`) |

## API

Sem módulo JS no ttscui: o estado vem do input nativo (radio/checkbox) — o formulário envia o valor sem JavaScript. Para botões com `.active`, a extensão `ttsc.button-group.js` (modelo JS) alterna `active`/`aria-pressed` e dispara:

| Evento (no grupo) | `detail` |
|---|---|
| `ttsc.buttongroup.change` | `{ value, values, button }` |

| Atributo (extensão) | Efeito |
|---|---|
| `data-ttsc-button-group="single"` | um `.active` por vez (`aria-pressed`) |
| `data-ttsc-button-group="multiple"` | cada botão alterna sozinho |
| `data-value="kanban"` no botão | valor reportado no evento |

## Acessibilidade

- Segmentado com radio: o teclado já funciona (`Tab` entra no grupo, setas trocam a opção). Envolva em `role="radiogroup"` + `aria-label="Visualização"`.
- Botões com `.active`: use `aria-pressed="true|false"` e `role="group"`.
- Toolbar: `role="toolbar"` + `aria-label="Paginação do calendário"`; botões só-ícone com `aria-label`.
- O estado selecionado não pode depender só do fundo `canvas-2` (≈1,1:1 contra `surface`): a extensão aplica `ttsc-accent-soft` + texto `ttsc-accent-text` (5,7:1 claro / 6,5:1 escuro) e peso 600.

## Modelos

### HTML

```html
<!-- Vista da listagem (envia ?view=…) -->
<form method="get" class="flex items-center gap-2">
  <div class="ttsc-toggle-group" role="radiogroup" aria-label="Visualização">
    <label class="ttsc-btn ttsc-btn-sm"><input type="radio" name="view" value="table" <?= $view === 'table' ? 'checked' : '' ?> onchange="this.form.submit()"><i class="fa-light fa-table"></i> Tabela</label>
    <label class="ttsc-btn ttsc-btn-sm"><input type="radio" name="view" value="kanban" <?= $view === 'kanban' ? 'checked' : '' ?> onchange="this.form.submit()"><i class="fa-light fa-square-kanban"></i> Kanban</label>
    <label class="ttsc-btn ttsc-btn-sm"><input type="radio" name="view" value="calendar" <?= $view === 'calendar' ? 'checked' : '' ?> onchange="this.form.submit()"><i class="fa-light fa-calendar"></i> Calendário</label>
  </div>
</form>

<!-- Turno com contagem (dados da consulta SQL) -->
<div class="ttsc-toggle-group" role="radiogroup" aria-label="Turno">
  <?php foreach ($shifts as $s): ?>
  <label class="ttsc-btn ttsc-btn-sm">
    <input type="radio" name="shift" value="<?= $this->e($s['shift']) ?>" <?= $shift === $s['shift'] ? 'checked' : '' ?>>
    <?= $this->e($s['label']) ?> <span class="ttsc-badge ttsc-badge-xs ttsc-badge-secondary"><?= (int) $s['total'] ?></span>
  </label>
  <?php endforeach; ?>
</div>

<!-- Toolbar do calendário -->
<div class="ttsc-toggle-group" role="toolbar" aria-label="Navegação do calendário">
  <button type="button" class="ttsc-btn ttsc-btn-sm ttsc-btn-icon" aria-label="Semana anterior"><i class="fa-light fa-chevron-left"></i></button>
  <button type="button" class="ttsc-btn ttsc-btn-sm">Hoje</button>
  <button type="button" class="ttsc-btn ttsc-btn-sm ttsc-btn-icon" aria-label="Próxima semana"><i class="fa-light fa-chevron-right"></i></button>
</div>
```

### CSS

```css
/* Ponte (bundle.css): o grupo usa --background, --border, --accent (hover neutro) e --muted-foreground (ícones) */
:root { --background: var(--ttsc-surface); --border: var(--ttsc-border); --accent: var(--ttsc-canvas-2); --muted-foreground: var(--ttsc-text-muted); }

/* Extensão TTSC: selecionado visível (o runtime usa só --accent, ~1,1:1 contra a superfície) */
.ttsc-toggle-group { border-radius: var(--ttsc-radius-sm); }
.ttsc-toggle-group .ttsc-btn { color: var(--ttsc-text); }
.ttsc-toggle-group .ttsc-btn:has(input:checked),
.ttsc-toggle-group .ttsc-btn.active {
  background: var(--ttsc-accent-soft);
  color: var(--ttsc-accent-text);
  font-weight: 600;
  box-shadow: inset 0 0 0 1px var(--ttsc-accent-border);
}
.ttsc-toggle-group .ttsc-btn:has(input:checked) i,
.ttsc-toggle-group .ttsc-btn.active i { color: var(--ttsc-accent-text); }
.ttsc-toggle-group .ttsc-btn:has(input:focus-visible) { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; z-index: 1; }
.ttsc-toggle-group .ttsc-btn:has(input:disabled) { opacity: .5; pointer-events: none; }
```

### JS

```js
// assets/js/core/ttsc.button-group.js — grupos de botões com .active (sem inputs)
export function initButtonGroups(root = document) {
  root.querySelectorAll('[data-ttsc-button-group]').forEach((group) => {
    const mode = group.dataset.ttscButtonGroup; // single | multiple
    const buttons = () => [...group.querySelectorAll('.ttsc-btn[data-value]')];
    buttons().forEach((b) => b.setAttribute('aria-pressed', b.classList.contains('active') ? 'true' : 'false'));

    group.addEventListener('click', (event) => {
      const button = event.target.closest('.ttsc-btn[data-value]');
      if (!button || button.disabled) return;
      if (mode === 'single') {
        buttons().forEach((b) => { b.classList.toggle('active', b === button); b.setAttribute('aria-pressed', b === button ? 'true' : 'false'); });
      } else {
        const on = !button.classList.contains('active');
        button.classList.toggle('active', on);
        button.setAttribute('aria-pressed', on ? 'true' : 'false');
      }
      const values = buttons().filter((b) => b.classList.contains('active')).map((b) => b.dataset.value);
      group.dispatchEvent(new CustomEvent('ttsc.buttongroup.change', {
        bubbles: true, detail: { value: button.dataset.value, values, button },
      }));
    });
  });
}

document.addEventListener('DOMContentLoaded', () => initButtonGroups());

// Ex.: filtros rápidos recarregam o DataTable remoto
document.addEventListener('ttsc.buttongroup.change', (event) => {
  if (event.target.id !== 'status-filter') return;
  const table = ttscDataTable.getInstance(document.querySelector('#enrollments-table'));
  table.setFilter({ column: 'status', type: 'in', value: event.detail.values }).reload();
});
```

### SQL

O grupo não persiste dados; ele **filtra**. A consulta abaixo alimenta o segmentado de turno com a contagem de matrículas ativas:

```sql
-- Matrículas ativas por turno, com o rótulo do enum (MariaDB 10.11 / MySQL 8)
SELECT e.shift,
       COALESCE(r.label, e.shift) AS label,
       COUNT(*)                   AS total
  FROM enrollments e
  LEFT JOIN ref_enum_enrollments_shift_3dacc9afe6c9 r
         ON r.value = e.shift AND r.deleted_at IS NULL
 WHERE e.unit_uuid = :unit_uuid
   AND e.status = 'active'
   AND e.deleted_at IS NULL
 GROUP BY e.shift, r.label, r.sort_order
 ORDER BY COALESCE(r.sort_order, 999);
```

O controller passa `$shifts` (linhas acima) e `$shift` (valor de `$_GET['shift']`, validado contra a lista) para a view; o radio marcado reflete o filtro atual e a listagem aplica `AND e.shift = :shift`.

## Faça / Não faça

- **Faça:** 2–5 opções, rótulos de 1 palavra, mesmo tamanho de botão no grupo.
- **Faça:** radio/checkbox nativos para estado — funciona sem JS e com teclado.
- **Faça:** `ttsc-btn-sm` em cabeçalhos de card e toolbars de tabela.
- **Não faça:** misturar `ttsc-btn-primary` dentro do grupo; ação principal fica fora, à direita.
- **Não faça:** usar o grupo para navegação entre páginas (use abas ou links).
