# ToggleGroup

Controle segmentado (`.ttsc-toggle-group` com `.ttsc-btn` filhos) para escolher uma opção (radio) ou várias (checkbox) numa faixa compacta de botões colados.

## Quando usar

- Alternar a visão de uma página: Tabela / Kanban / Calendário; Dia / Semana / Mês.
- Filtros de toolbar com poucas opções: dias da semana da grade horária (múltiplo), turno (único).
- Formatação de texto em barras de ferramentas (negrito/itálico — múltiplo).
- Trocar de **conteúdo** com painéis → [SegmentedTabs](../SegmentedTabs/README.md) (tabs com `aria-selected`). Opções com descrição → [Radio](../Radio/README.md) em cartões. Uma configuração on/off → [Switch](../Switch/README.md).

## Anatomia

```
┌──────────┬──────────┬────────────┐
│ ▦ Tabela │ ▥ Kanban │ ▣ Calendário│   div.ttsc-toggle-group[role=radiogroup]
└──────────┴──────────┴────────────┘     label.ttsc-btn > input[type=radio] + ícone + texto
   ativo = fundo --accent (ttsc-canvas-2), texto --accent-foreground (ttsc-text)
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Container | `div.ttsc-toggle-group` (inline-flex, fundo `--background`) | sim |
| Item | `label.ttsc-btn` (ou `button.ttsc-btn`) — bordas internas e raios são ajustados pelo grupo | sim |
| Controle | `input[type=radio]` (único) ou `input[type=checkbox]` (múltiplo) **dentro** do item — o runtime o esconde | sim (modo formulário) |
| Ativo | automático por `:has(input:checked)`; ou classe `active` (modo botão/JS) | sim |
| Tamanho | `ttsc-btn-sm` / `ttsc-btn-lg` em cada item | não |
| Só ícone | `ttsc-btn-icon` + `aria-label` no item | não |

Classes confirmadas no `bundle.css`: `.ttsc-toggle-group`, `.ttsc-toggle-group .ttsc-btn` (+ `:first-child`, `:last-child`, `:has(input:checked)`, `.active`). Não há classes de tamanho próprias do grupo.

## Variantes

| Variante | Marcação | Tokens |
|---|---|---|
| Único | radios com o mesmo `name` | borda `--border` → `ttsc-border`; ativo `--accent` → `ttsc-canvas-2` + texto `ttsc-text` |
| Múltiplo | checkboxes | idem |
| Botões (sem form) | `button.ttsc-btn` + `active` + `aria-pressed` | idem |
| Ênfase (extensão) | `.ttsc-toggle-group-accent` | ativo `ttsc-accent-soft` + texto `ttsc-accent-text` |

## Estados

| Estado | Como |
|---|---|
| Ativo | `checked` no input, ou `active` no botão |
| Hover / foco | fundo `--accent` (o runtime trata `:hover`, `:focus` e `:active` igual ao ativo — use a extensão de foco abaixo para diferenciar) |
| Desabilitado | `disabled` no input + `aria-disabled="true"` e `pointer-events:none` no label (extensão) |

## API

Sem JavaScript: é CSS sobre radios/checkboxes nativos. No modo botões (`button.active`), alterne `active`/`aria-pressed` você mesmo (JS abaixo).

## Acessibilidade

- **Problema do runtime:** `input { display: none }` remove o controle da ordem de `Tab` e das setas. A extensão `.ttsc-toggle-group-a11y` (CSS abaixo) esconde o input só visualmente e devolve teclado + anel de foco. Use-a sempre no modo formulário.
- Modo único: container com `role="radiogroup"` + `aria-label`; modo múltiplo: `role="group"`.
- Modo botões: `aria-pressed="true|false"` em cada `<button>`.
- Só ícone: `aria-label` no `label`/`button`; o ícone fica `aria-hidden`.
- Contraste: o ativo depende de fundo `ttsc-canvas-2` vs `ttsc-surface` (sutil). Por isso o rótulo ativo ganha peso 600 na extensão — a seleção não depende só de cor.

## Modelos

### HTML

```html
<!-- Toolbar da página de turmas: visão (único) -->
<div class="ttsc-toggle-group ttsc-toggle-group-a11y" role="radiogroup" aria-label="Visualização">
  <?php foreach (['table' => ['fa-table', 'Tabela'], 'kanban' => ['fa-square-kanban', 'Kanban'], 'calendar' => ['fa-calendar', 'Calendário']] as $v => [$icon, $label]): ?>
    <label class="ttsc-btn ttsc-btn-sm">
      <input type="radio" name="view" value="<?= $v ?>" <?= $view === $v ? 'checked' : '' ?>>
      <i class="fa-light <?= $icon ?>" aria-hidden="true"></i> <?= $label ?>
    </label>
  <?php endforeach; ?>
</div>

<!-- Filtro da grade horária: dias da semana (múltiplo) — valores = schedules.weekday (0=Dom…6=Sáb) -->
<div class="ttsc-toggle-group ttsc-toggle-group-a11y" role="group" aria-label="Dias da semana">
  <?php foreach ([1 => 'Seg', 2 => 'Ter', 3 => 'Qua', 4 => 'Qui', 5 => 'Sex', 6 => 'Sáb'] as $d => $label): ?>
    <label class="ttsc-btn ttsc-btn-sm">
      <input type="checkbox" name="weekdays[]" value="<?= $d ?>" <?= in_array($d, $weekdays, true) ? 'checked' : '' ?>> <?= $label ?>
    </label>
  <?php endforeach; ?>
</div>
```

### CSS

```css
/* Ponte (bundle.css) */
:root { --accent: var(--ttsc-canvas-2); --accent-foreground: var(--ttsc-text); --border: var(--ttsc-border); }

/* Extensão de acessibilidade: input acessível por teclado (o runtime usa display:none) */
.ttsc-toggle-group.ttsc-toggle-group-a11y .ttsc-btn { position: relative; }
.ttsc-toggle-group.ttsc-toggle-group-a11y .ttsc-btn input[type=radio],
.ttsc-toggle-group.ttsc-toggle-group-a11y .ttsc-btn input[type=checkbox] {
  display: block; position: absolute; inset: 0; opacity: 0; margin: 0; cursor: pointer;
}
.ttsc-toggle-group .ttsc-btn:has(input:focus-visible) { outline: 2px solid var(--ttsc-accent); outline-offset: -2px; z-index: 1; }
.ttsc-toggle-group .ttsc-btn:has(input:checked), .ttsc-toggle-group .ttsc-btn.active { font-weight: 600; }
.ttsc-toggle-group .ttsc-btn:has(input:disabled) { opacity: .5; pointer-events: none; }

/* Variante de ênfase */
.ttsc-toggle-group-accent .ttsc-btn:has(input:checked),
.ttsc-toggle-group-accent .ttsc-btn.active { background: var(--ttsc-accent-soft); color: var(--ttsc-accent-text); }
```

### JS

```js
// Visão da página: troca sem recarregar e lembra a escolha
const viewGroup = document.querySelector('[role="radiogroup"][aria-label="Visualização"]');
viewGroup.addEventListener('change', (event) => {
  const view = event.target.value;
  document.querySelectorAll('[data-view-panel]').forEach((panel) => {
    panel.classList.toggle('hidden', panel.dataset.viewPanel !== view);
  });
  const url = new URL(location.href);
  url.searchParams.set('view', view);
  history.replaceState(null, '', url);
  try { localStorage.setItem('ttsc:classes:view', view); } catch (e) { /* modo privado */ }
});

// Modo botões (sem form): aria-pressed + active
document.querySelectorAll('.ttsc-toggle-group[data-mode="buttons"]').forEach((group) => {
  group.addEventListener('click', (event) => {
    const button = event.target.closest('button.ttsc-btn');
    if (!button) return;
    const pressed = button.getAttribute('aria-pressed') !== 'true';
    button.setAttribute('aria-pressed', String(pressed));
    button.classList.toggle('active', pressed);
  });
});
```

### SQL

```sql
-- Grade horária filtrada pelos dias marcados no grupo múltiplo.
-- :weekdays_csv = implode(',', array_map('intval', $weekdays)) → ex. '1,3,5' (um único parâmetro)
SELECT s.uuid, s.weekday, s.start_time, s.end_time, s.room, s.subject_uuid, s.teacher_uuid
  FROM schedules s
 WHERE s.class_uuid = :class_uuid
   AND s.is_active = 1
   AND FIND_IN_SET(s.weekday, :weekdays_csv) > 0
 ORDER BY s.weekday, s.start_time;

-- Contagem de aulas por dia (badge dentro de cada item do grupo)
SELECT s.weekday, COUNT(*) AS lessons
  FROM schedules s
 WHERE s.class_uuid = :class_uuid
   AND s.is_active = 1
 GROUP BY s.weekday;
```

`weekdays[]` chega como array; o controller converte com `intval` e filtra 0–6 antes de montar o CSV. O modo único (visão) não toca o banco — é estado de interface na URL.

## Faça / Não faça

- **Faça:** `.ttsc-toggle-group-a11y` no modo formulário; 2 a 6 itens curtos.
- **Faça:** radio para exclusivo, checkbox para múltiplo — o comportamento vem do HTML.
- **Não faça:** usar para navegar entre páginas (use links/tabs); itens com textos longos; misturar radio e checkbox no mesmo grupo.
