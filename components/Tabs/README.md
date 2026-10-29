# Tabs

Abas que alternam painéis de conteúdo na mesma página sem recarregar (`data-ttsc-tabs` + `data-ttsc-tab-toggle`, ttscui), no estilo linha `.ttsc-tabs-line` do chassi.

> Também listado em: **Base › Tabs**.

## Quando usar

- Visões irmãs de um mesmo registro: ficha do aluno (Matrículas · Financeiro · Frequência · Documentos), configurações por área.
- Filtros de status com contagem (Ativas 186 · Trancadas 12 · Encerradas 40) quando cada aba tem conteúdo próprio.
- **Não use** para alternar só o modo de exibição (Tabela/Cards/Kanban): use [SegmentedTabs](../SegmentedTabs/README.md).
- **Não use** para processo em ordem com validação: use [Stepper](../Stepper/README.md).
- **Não use** quando o usuário precisa comparar o conteúdo de duas abas — empilhe com [Scrollspy](../Scrollspy/README.md).

## Anatomia

```
 Matrículas (3)   Financeiro   Frequência   Documentos        ← .ttsc-tabs.ttsc-tabs-line [data-ttsc-tabs]
 ━━━━━━━━━━━━━━                                                  .ttsc-tab-toggle.active  [data-ttsc-tab-toggle="#tab-…"]
┌──────────────────────────────────────────────────────────┐
│ painel #tab-enrollments (os outros com .hidden)          │
└──────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Lista | `.ttsc-tabs.ttsc-tabs-line` + `data-ttsc-tabs="true"` + `role="tablist"` | sim |
| Aba | `button.ttsc-tab-toggle` + `data-ttsc-tab-toggle="#painel"` (ou `a[href="#painel"]`) + `role="tab"` | sim |
| Aba inicial | classe `active` na aba e painel **sem** `hidden` | sim |
| Painel | `id` + `role="tabpanel"` + `aria-labelledby`; inativos com `hidden` | sim |
| Contagem | `span.ttsc-badge.ttsc-badge-sm` dentro da aba | não |

## Variantes

| Variante | Classe | Tokens |
|---|---|---|
| Linha (padrão do chassi) | `ttsc-tabs ttsc-tabs-line` | texto `ttsc-text`; ativa com borda 2px `ttsc-accent` e texto `ttsc-accent-text` (extensão) |
| Com ícone | `<i class="fa-light fa-…">` antes do rótulo | ícone `ttsc-text-muted`, ativo `ttsc-accent-text` |
| Com contagem | `ttsc-badge ttsc-badge-sm ttsc-badge-outline` | ativo: fundo `ttsc-accent-soft` |
| Pílula (sub-abas em card) | `.ttsc-tabs.ttsc-tabs-pill` (extensão) | fundo `ttsc-canvas-2`, ativa `ttsc-surface` + `ttsc-shadow-xs` |

## Estados

| Estado | Como | Visual |
|---|---|---|
| Ativa | classes `active` + `selected` (postas pelo JS) | borda inferior `ttsc-accent` |
| Hover | CSS | texto `ttsc-text` (o runtime usa `--primary`; a extensão troca por token de texto) |
| Foco | CSS | contorno 2px `ttsc-accent` |
| Desabilitada | `disabled` no botão | opacidade 50%, não recebe clique |

## API

Conferida em `src/components/tabs/tabs.ts`.

| Opção | Atributo | Padrão | Descrição |
|---|---|---|---|
| `hiddenClass` | `data-ttsc-tabs-hidden-class` | `"hidden"` | classe posta nos painéis inativos |

| Método | Descrição |
|---|---|
| `ttscTabs.getInstance(el)` / `getOrCreateInstance(el, cfg)` | instância (no elemento `[data-ttsc-tabs]`) |
| `show(tabEl)` | ativa a aba (mesmo fluxo do clique) |
| `isShown(tabEl)` | `true` se a aba tem `active` |
| `on('show', fn)` / `on('shown', fn)` / `off` | callbacks internos |

| Evento (DOM, no `[data-ttsc-tabs]`) | `detail.payload` | Observação |
|---|---|---|
| `show` | `{ cancel: false }` | cancelável: `payload.cancel = true` mantém a aba atual |
| `shown` | `null` | após a transição de opacidade do painel |

O fonte só trata clique (`keyboardArrow`, `keyboardJump` e `handleAccessibility` estão vazios no build): setas, Home/End e `aria-selected` vêm da extensão JS abaixo. Abas dentro de um [Dropdown](../Dropdown/README.md) marcam também o toggle do dropdown como `active`.

## Acessibilidade

- `role="tablist"` / `role="tab"` / `role="tabpanel"`, com `aria-controls` e `aria-labelledby` cruzados.
- `aria-selected="true"` e `tabindex="0"` só na aba ativa; as demais `tabindex="-1"` (roving tabindex). ← → movem e ativam; Home/End vão às pontas.
- Rótulo ativo em `ttsc-accent-text` (6,9:1 claro / 9,6:1 escuro). O runtime usa `--primary` (`#3ecf8e`) como cor de texto, 2:1 sobre branco — a extensão CSS corrige.
- Contagens fazem parte do nome: “Matrículas, 3”.

## Modelos

### HTML

```html
<div class="ttsc-tabs ttsc-tabs-line" data-ttsc-tabs="true" role="tablist" aria-label="Ficha do aluno">
  <button type="button" class="ttsc-tab-toggle active" id="t-enr" role="tab" aria-controls="tab-enrollments" aria-selected="true"
          data-ttsc-tab-toggle="#tab-enrollments">
    <i class="fa-light fa-graduation-cap"></i> Matrículas
    <span class="ttsc-badge ttsc-badge-sm ttsc-badge-outline"><?= (int) $tabs['tab_active'] ?></span>
  </button>
  <button type="button" class="ttsc-tab-toggle" id="t-fin" role="tab" aria-controls="tab-billing" aria-selected="false" tabindex="-1"
          data-ttsc-tab-toggle="#tab-billing">
    <i class="fa-light fa-receipt"></i> Financeiro
  </button>
  <button type="button" class="ttsc-tab-toggle" id="t-att" role="tab" aria-controls="tab-attendance" aria-selected="false" tabindex="-1"
          data-ttsc-tab-toggle="#tab-attendance">
    <i class="fa-light fa-calendar-check"></i> Frequência
  </button>
</div>

<div id="tab-enrollments" role="tabpanel" aria-labelledby="t-enr" tabindex="0"> … </div>
<div id="tab-billing" class="hidden" role="tabpanel" aria-labelledby="t-fin" tabindex="0" data-src="/academic/students/<?= $this->e($uuid) ?>/billing"> … </div>
<div id="tab-attendance" class="hidden" role="tabpanel" aria-labelledby="t-att" tabindex="0"> … </div>
```

### CSS

```css
/* Ponte: o runtime pinta a aba ativa com --primary (= --ttsc-accent). Mantenha a BORDA verde e use token de texto: */
.ttsc-tabs.ttsc-tabs-line .ttsc-tab-toggle { color: var(--ttsc-text-2); border-bottom: 2px solid transparent; background: none; }
.ttsc-tabs.ttsc-tabs-line .ttsc-tab-toggle:hover { color: var(--ttsc-text); }
.ttsc-tabs.ttsc-tabs-line .ttsc-tab-toggle.active { color: var(--ttsc-accent-text); border-color: var(--ttsc-accent); }
.ttsc-tabs .ttsc-tab-toggle i { color: var(--ttsc-text-muted); }
.ttsc-tabs .ttsc-tab-toggle.active i { color: var(--ttsc-accent-text); }
.ttsc-tabs .ttsc-tab-toggle.active .ttsc-badge { background: var(--ttsc-accent-soft); border-color: var(--ttsc-accent-border); color: var(--ttsc-accent-text); }
.ttsc-tabs .ttsc-tab-toggle:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; border-radius: var(--ttsc-radius-xs); }
.ttsc-tabs .ttsc-tab-toggle:disabled { opacity: .5; cursor: not-allowed; }

/* Extensão: sub-abas em pílula dentro de cards */
.ttsc-tabs.ttsc-tabs-pill { display: inline-flex; gap: 2px; padding: 3px; background: var(--ttsc-canvas-2); border-radius: var(--ttsc-radius-control); }
.ttsc-tabs-pill .ttsc-tab-toggle { padding: 4px 10px; font-size: 12px; font-weight: 500; color: var(--ttsc-text-2); border: 0; background: none; border-radius: var(--ttsc-radius-sm); cursor: pointer; }
.ttsc-tabs-pill .ttsc-tab-toggle.active { background: var(--ttsc-surface); color: var(--ttsc-text); box-shadow: var(--ttsc-shadow-xs); }
```

### JS

```js
TTSC.init();

// assets/js/core/ttsc.tabs-a11y.js — teclado + ARIA (o build do ttscui só trata clique)
export function enhanceTabs(list) {
  const tabs = () => [...list.querySelectorAll('[data-ttsc-tab-toggle]:not(:disabled)')];
  const instance = ttscTabs.getOrCreateInstance(list);
  const sync = () => tabs().forEach((t) => {
    const on = t.classList.contains('active');
    t.setAttribute('aria-selected', String(on));
    t.tabIndex = on ? 0 : -1;
  });
  list.addEventListener('shown', sync);
  list.addEventListener('keydown', (e) => {
    const all = tabs(), i = all.indexOf(document.activeElement);
    if (i < 0) return;
    const next = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: all.length - 1 }[e.key];
    if (next === undefined) return;
    e.preventDefault();
    const tab = all[(next + all.length) % all.length];
    tab.focus();
    instance.show(tab);
  });
  sync();
  return instance;
}

document.querySelectorAll('[data-ttsc-tabs]').forEach((list) => {
  enhanceTabs(list);

  // Carregamento preguiçoso: painel com data-src só busca na primeira exibição
  list.addEventListener('show', () => queueMicrotask(async () => {
    const panel = document.querySelector(list.querySelector('.active[data-ttsc-tab-toggle]').dataset.ttscTabToggle);
    if (!panel?.dataset.src || panel.dataset.loaded) return;
    panel.dataset.loaded = 'true';
    panel.innerHTML = await (await fetch(panel.dataset.src)).text();
  }));
});

// Abrir a aba pedida na URL (?tab=billing)
const wanted = new URLSearchParams(location.search).get('tab');
if (wanted) {
  const tab = document.querySelector(`[data-ttsc-tab-toggle="#tab-${CSS.escape(wanted)}"]`);
  if (tab) ttscTabs.getInstance(tab.closest('[data-ttsc-tabs]')).show(tab);
}
```

### SQL

As contagens das abas de status de matrícula do aluno saem de uma consulta só:

```sql
SELECT COALESCE(SUM(e.status = 'active'), 0)                         AS tab_active,
       COALESCE(SUM(e.status = 'locked'), 0)                         AS tab_locked,
       COALESCE(SUM(e.status IN ('cancelled', 'transferred')), 0)    AS tab_closed,
       COUNT(*)                                                      AS tab_all
  FROM enrollments e
 WHERE e.deleted_at IS NULL
   AND e.student_uuid = :student_uuid;
```

O controller passa `$tabs` à view; o conteúdo de cada aba vem de endpoints próprios (`data-src`), carregados só quando a aba é aberta. Os rótulos dos status vêm da tabela de enum `ref_enum_enrollments_status_*` (coluna `label`).

## Faça / Não faça

- **Faça:** deixar exatamente uma aba `active` e o painel dela sem `hidden` no HTML inicial.
- **Faça:** usar `ttsc-accent-text` no rótulo ativo e manter a borda em `ttsc-accent`.
- **Não faça:** mais de 6 abas ou abas com rótulos de duas linhas.
- **Não faça:** formulário dividido em abas com um único “Salvar” que esconde erros em abas fechadas.
