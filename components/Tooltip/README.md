# Tooltip

Dica curta posicionada com Popper do ttscui (`data-ttsc-tooltip="#id"` + `.ttsc-tooltip`), acionada por hover, foco ou clique, com posição, atraso, offset e modo permanente.

> Também listado em: **Base › Tooltips**.

## Quando usar

- Nomear botões só-ícone (Exportar, Filtrar, Mais ações) — além do `aria-label`.
- Explicar uma métrica ou sigla em uma frase: “Frequência = presenças + faltas justificadas ÷ aulas lançadas”.
- Mostrar o valor completo de um texto truncado (nome longo de curso numa célula de tabela).
- Conteúdo com links, botões ou mais de ~2 linhas → [Dropdown](../Dropdown/README.md) / popover; nunca coloque elementos interativos no tooltip.
- Informação essencial para concluir a tarefa (regra de preenchimento) → texto de ajuda visível abaixo do campo, não tooltip.
- No touch não existe hover: para dicas importantes no mobile use `trigger: click`.

## Anatomia

```
[gatilho data-ttsc-tooltip="#tt" aria-describedby="tt"]
        ▲ offset "0, 5px"
┌──────────────────────────┐
│ div#tt.ttsc-tooltip       │  role="tooltip", oculto até receber .show (CSS: :not(.show){display:none})
└──────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Gatilho | `[data-ttsc-tooltip="#id"]` (ou conteúdo filho `[data-ttsc-tooltip-content]`) | sim |
| Conteúdo | `div.ttsc-tooltip` com `id` e `role="tooltip"` | sim |
| Ligação ARIA | `aria-describedby="id"` no gatilho | sim |
| Tema claro | `ttsc-tooltip-light` | não |

## Variantes

| Variante | Classe / atributo | Tokens |
|---|---|---|
| Padrão (mono) | `ttsc-tooltip` | fundo `--mono`=`ttsc-text`, texto `--mono-foreground`=`ttsc-surface` (≥ 15:1 nos dois temas; no escuro ganha borda `--border`) |
| Claro | `ttsc-tooltip ttsc-tooltip-light` | fundo `--popover`=`ttsc-surface`, borda `ttsc-border`, texto `ttsc-text` |
| Hover / Foco / Clique | `data-ttsc-tooltip-trigger="hover\|focus\|click"` | — |
| Permanente | `data-ttsc-tooltip-permanent="true"` (não fecha ao clicar fora) | — |

Tipografia: 12px (`--text-xs`), padding 6px, raio `radius - 2px`, sombra `md`.

## API

Opções (`data-ttsc-tooltip-<opção>` ou `--ttsc-tooltip-<opção>`), conferidas em `src/components/tooltip/tooltip.ts`:

| Atributo | Padrão | Efeito |
|---|---|---|
| `data-ttsc-tooltip` | — | seletor do conteúdo |
| `-target` | `""` | seletor alternativo do conteúdo |
| `-trigger` | `hover` | `hover`, `focus` ou `click` |
| `-placement` / `-placement-rtl` | `top` | qualquer placement do Popper (`top-start`, `right`, `bottom-end`…) |
| `-offset` / `-offset-rtl` | `"0, 5px"` | deslocamento `skid, distância` |
| `-strategy` | `fixed` | `fixed` ou `absolute` |
| `-container` | `""` | `body` ou seletor para mover o conteúdo ao abrir (escapa de `overflow:hidden`) |
| `-delay-show` / `-delay-hide` | `0` | atraso em ms |
| `-permanent` | `false` | não fecha no clique fora (para `click`/`focus`) |
| `-zindex` | `100` | z-index mínimo (sobe acima do maior z-index dos ancestrais) |
| `-hidden-class` | `hidden` | classe removida ao abrir |

| Método | Efeito |
|---|---|
| `TTSC.Tooltip.getInstance(el)` / `getOrCreateInstance(el, config)` | instância |
| `show()` / `hide()` / `toggle()` | controle programático |
| `isOpen()` / `isPermanent()` / `getTriggerOption()` / `getContentElement()` | consulta |

| Evento (no gatilho, bubbles) | Cancelável |
|---|---|
| `show` → `shown` | `show` sim (`detail.payload.cancel = true`) |
| `hide` → `hidden` | `hide` sim |
| `toggle` | sim |

## Acessibilidade

- Gatilho focável (`button`, `a` ou `tabindex="0"`) + `aria-describedby` apontando para o tooltip; o tooltip descreve, não nomeia — botão só-ícone também precisa de `aria-label`.
- `hover` sozinho exclui teclado: para dicas relevantes prefira `focus` ou adicione um segundo gatilho; Esc deve fechar (JS abaixo).
- Nada interativo dentro do tooltip; texto ≤ 2 linhas.
- Contraste garantido pelos tokens (mono ≥ 15:1, light ≥ 15:1).

## Modelos

### HTML

```html
<!-- Botão só-ícone na toolbar -->
<button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-icon" aria-label="Exportar" aria-describedby="tt-export"
        data-ttsc-tooltip="#tt-export" data-ttsc-tooltip-placement="bottom">
  <i class="fa-light fa-arrow-down-to-line"></i>
</button>
<div id="tt-export" class="ttsc-tooltip" role="tooltip">Exportar lista (CSV/Excel)</div>

<!-- Explicação de KPI (clique, funciona no touch) -->
<span class="inline-flex items-center gap-1" tabindex="0" aria-describedby="tt-freq-<?= $e($class['uuid']) ?>"
      data-ttsc-tooltip="#tt-freq-<?= $e($class['uuid']) ?>" data-ttsc-tooltip-trigger="click"
      data-ttsc-tooltip-placement="top-start" data-ttsc-tooltip-container="body">
  Frequência <?= number_format((float) $kpi['attendance_pct'], 1, ',', '') ?>% <i class="fa-light fa-circle-info" aria-hidden="true"></i>
</span>
<div id="tt-freq-<?= $e($class['uuid']) ?>" class="ttsc-tooltip ttsc-tooltip-light" role="tooltip">
  <?= (int) $kpi['lessons'] ?> registros · <?= (int) $kpi['absences'] ?> faltas · último lançamento <?= $e($kpi['last_lesson']) ?>
</div>
```

### CSS

```css
/* Ponte (bundle.css): --mono / --mono-foreground / --popover */
:root { --mono: var(--ttsc-text); --mono-foreground: var(--ttsc-surface); --popover: var(--ttsc-surface); }

/* Extensões TTSC: largura máxima, camada do chassi e transição de opacidade usada pelo JS */
.ttsc-tooltip { max-width: 240px; font-size: 12px; line-height: 16px; z-index: var(--ttsc-z-tooltip); transition: opacity var(--ttsc-motion-fast, .15s) ease; }
.ttsc-tooltip-light { box-shadow: var(--ttsc-shadow-md); }
```

### JS

```js
TTSC.init();

// Esc fecha qualquer tooltip aberto (requisito WCAG 1.4.13)
document.addEventListener('keydown', function (e) {
  if (e.key !== 'Escape') return;
  document.querySelectorAll('[data-ttsc-tooltip-initialized]').forEach(function (el) {
    var tip = TTSC.Tooltip.getInstance(el);
    if (tip && tip.isOpen()) tip.hide();
  });
});

// Tooltip criado dinamicamente para células truncadas da tabela
document.querySelectorAll('td.truncate').forEach(function (td, i) {
  if (td.scrollWidth <= td.clientWidth) return;
  var tip = document.createElement('div');
  tip.id = 'tt-cell-' + i; tip.className = 'ttsc-tooltip'; tip.setAttribute('role', 'tooltip');
  tip.textContent = td.textContent.trim();
  document.body.appendChild(tip);
  td.tabIndex = 0;
  td.setAttribute('aria-describedby', tip.id);
  td.setAttribute('data-ttsc-tooltip', '#' + tip.id);
  TTSC.Tooltip.getOrCreateInstance(td, { delayShow: 300 });
});
```

### SQL

Conteúdo do tooltip do KPI de frequência da turma (no período letivo):

```sql
SELECT ROUND(100 * SUM(a.status IN ('present', 'late', 'justified')) / NULLIF(COUNT(*), 0), 1) AS attendance_pct,
       COUNT(*)                  AS lessons,
       SUM(a.status = 'absent')  AS absences,
       MAX(a.lesson_date)        AS last_lesson
  FROM attendance a
  JOIN enrollments e
    ON e.uuid = a.enrollment_uuid AND e.status = 'active' AND e.deleted_at IS NULL
 WHERE a.class_uuid = :class_uuid
   AND a.lesson_date BETWEEN :period_start AND :period_end;
```

O controller entrega `$kpi` à view; o número aparece no gatilho e o detalhe (`lessons`, `absences`, `last_lesson` formatada em pt-BR) no corpo do tooltip.

## Faça / Não faça

- **Faça:** texto curto, `aria-describedby`, e `container="body"` dentro de tabelas/cards com `overflow:hidden`.
- **Faça:** `trigger="click"` para dicas que precisam funcionar no celular.
- **Não faça:** links ou botões dentro do tooltip.
- **Não faça:** tooltip como única fonte de informação obrigatória.
