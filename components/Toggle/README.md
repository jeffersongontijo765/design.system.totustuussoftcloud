# Toggle

Alternador genérico do ttscui (`data-ttsc-toggle`): um gatilho liga/desliga uma classe ou um atributo num elemento alvo e marca a si mesmo com `activeClass`, disparando `toggle`/`toggled`.

> Também listado em: **Geral › Toggle**.

## Quando usar

- Mostrar/ocultar um bloco simples sem animação: filtros avançados, detalhes de uma parcela, campos opcionais do formulário.
- Ligar um modo visual num container: lista compacta, sidebar recolhida (`data-collapsed`), modo foco.
- Gatilho com seta que gira quando ativo (`ttsc-toggle-active:rotate-180`).
- Painel com altura animada e ARIA completo → [Collapse](../Collapse/README.md) ou Accordion.
- Grupo de botões exclusivos (lista/cards/kanban) → `.ttsc-toggle-group` ou [SegmentedTabs](../SegmentedTabs/README.md).
- Interruptor de formulário (valor enviado) → `input.ttsc-switch`; tema → [ThemeSwitch](../ThemeSwitch/README.md).

## Anatomia

```
button[data-ttsc-toggle="#alvo"] (.active quando ligado)  ──click──▶  #alvo (+/- classe | +/- atributo)
  └ i.ttsc-toggle-active:rotate-180  (gira com o gatilho .active)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Gatilho | `[data-ttsc-toggle="#seletor"]` (ou `data-ttsc-toggle-target`) | sim |
| Ação no alvo | `data-ttsc-toggle-class="…"` e/ou `data-ttsc-toggle-attribute="…"` | sim (um dos dois) |
| Classe do gatilho | `data-ttsc-toggle-active-class` (padrão `active`) | não |
| Ícone que gira | `ttsc-toggle-active:rotate-180` dentro do gatilho | não |
| ARIA | `aria-controls` + `aria-expanded` ou `aria-pressed` | sim |

## Variantes

| Variante | Atributos | Uso | Tokens |
|---|---|---|---|
| Mostrar/ocultar | `-class="hidden"` | filtros avançados | — (classe do runtime) |
| Modo por atributo | `-attribute="data-compact"` + CSS `[data-compact]` | lista densa | linhas `ttsc-border-soft`, altura `--ttsc-row-compact` |
| Gatilho destacado | `-active-class="ttsc-btn-secondary"` | botão que fica “pressionado” | `ttsc-surface-2` |
| Seta | `ttsc-toggle-active:rotate-180` | expansores | — |
| Grupo | `.ttsc-toggle-group > .ttsc-btn.active` | escolha exclusiva visual | ativo `--accent`=`ttsc-canvas-2` |

## API

Opções (`data-ttsc-toggle-<opção>` ou `--ttsc-toggle-<opção>`), conferidas em `src/components/toggle/toggle.ts`:

| Atributo | Padrão | Efeito |
|---|---|---|
| `data-ttsc-toggle` | — | seletor do alvo (tem prioridade sobre `-target`) |
| `-target` | `""` | seletor do alvo (alternativo) |
| `-class` | `""` | classe(s) alternadas no alvo (separadas por espaço) |
| `-attribute` | `""` | atributo alternado no alvo (valor `"true"` quando presente) |
| `-remove-class` | `""` | classe(s) sempre removidas do alvo a cada clique |
| `-active-class` | `"active"` | classe alternada no **gatilho** |

Lógica: se o alvo **tem** a classe/atributo, o clique remove; se não tem, adiciona. Ou seja, `-class="hidden"` num alvo visível o esconde no primeiro clique — sincronize a classe ativa inicial do gatilho com o estado do alvo.

| Método | Efeito |
|---|---|
| `TTSC.Toggle.getInstance(el)` / `getOrCreateInstance(el, config)` | instância |
| `inst.toggle()` | mesmo efeito do clique |
| `inst.update()` | reaplica a regra ao alvo |
| `inst.isActive()` | `true` se o alvo tem a classe/atributo |
| `inst.dispose()` | remove o listener |

| Evento (no gatilho, bubbles) | Quando |
|---|---|
| `toggle` | antes; `event.detail.payload.cancel = true` (ou `inst.on('toggle', e => { e.cancel = true; })`) cancela a troca |
| `toggled` | depois de alternar |

## Acessibilidade

- O gatilho é sempre `<button type="button">`.
- Mostrar/ocultar: `aria-controls="id"` + `aria-expanded` atualizado no `toggled`. Modo (compacto, foco): `aria-pressed`.
- A seta é decorativa (`aria-hidden="true"`); o estado vem do ARIA, não da rotação.
- Conteúdo escondido com `hidden` sai da árvore de acessibilidade — correto para filtros; não esconda mensagens de erro assim.
- Estado ativo não só por cor: `ttsc-btn-secondary` muda fundo **e** `aria-pressed`.

## Modelos

### HTML

```html
<!-- Filtros avançados da listagem de matrículas (começa fechado) -->
<button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-sm"
        data-ttsc-toggle="#enrollment-advanced-filters" data-ttsc-toggle-class="hidden"
        aria-controls="enrollment-advanced-filters" aria-expanded="false">
  <i class="fa-light fa-sliders"></i> Filtros avançados
  <i class="fa-light fa-chevron-down ttsc-toggle-active:rotate-180" aria-hidden="true"></i>
</button>
<div id="enrollment-advanced-filters" class="hidden"> … </div>

<!-- Lista compacta (estado salvo no perfil) -->
<button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-sm <?= $compact ? 'ttsc-btn-secondary' : '' ?>"
        data-ttsc-toggle="#students-list" data-ttsc-toggle-attribute="data-compact"
        data-ttsc-toggle-active-class="ttsc-btn-secondary" data-pref="enrollments_list_compact"
        aria-pressed="<?= $compact ? 'true' : 'false' ?>">
  <i class="fa-light fa-list"></i> Lista compacta
</button>
<ul id="students-list" <?= $compact ? 'data-compact="true"' : '' ?>> … </ul>
```

Atenção ao “começa fechado”: como o alvo **já tem** `hidden`, o ttscui considera o toggle ativo e o primeiro clique remove `hidden` (abre). A classe do gatilho (`active`) inverte a cada clique; inicie o gatilho sem `active` quando fechado.

### CSS

```css
/* A seta gira com o gatilho .active (classe já existe no runtime) — só adicionamos a transição */
[data-ttsc-toggle] .ttsc-toggle-active\:rotate-180 { transition: rotate var(--ttsc-motion-base, .2s) var(--ttsc-ease, ease); }

/* Modo compacto controlado por atributo */
[data-compact] > li { padding-block: 4px; min-height: var(--ttsc-row-compact); font-size: 12px; }

/* Grupo de botões do runtime (lista / cards) com tokens */
.ttsc-toggle-group .ttsc-btn.active { background-color: var(--ttsc-surface-2); color: var(--ttsc-text); }
```

### JS

```js
TTSC.init();

// ARIA sincronizado em todos os toggles
document.addEventListener('toggled', function (event) {
  var trigger = event.target.closest('[data-ttsc-toggle]');
  if (!trigger) return;
  var target = document.querySelector(trigger.getAttribute('data-ttsc-toggle'));
  if (trigger.hasAttribute('aria-expanded')) {
    trigger.setAttribute('aria-expanded', String(!target.classList.contains('hidden')));
  }
  if (trigger.hasAttribute('aria-pressed')) {
    var attr = trigger.getAttribute('data-ttsc-toggle-attribute');
    trigger.setAttribute('aria-pressed', String(attr ? target.hasAttribute(attr) : trigger.classList.contains('active')));
  }

  // Persiste preferências de exibição (data-pref)
  if (trigger.dataset.pref) {
    fetch('/app/profile/preferences/display', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content },
      body: JSON.stringify({ key: trigger.dataset.pref, value: trigger.getAttribute('aria-pressed') === 'true' }),
    });
  }
});

// Programático: atalho "c" liga/desliga a lista compacta
document.addEventListener('keydown', function (e) {
  if (e.key === 'c' && !e.target.closest('input, textarea, select, [contenteditable]')) {
    TTSC.Toggle.getInstance(document.querySelector('[data-pref="enrollments_list_compact"]')).toggle();
  }
});
```

### SQL

Preferências de exibição ficam no JSON `user_preferences.dashboard_settings` (valor 1/0, compatível com MariaDB e MySQL):

```sql
-- Ler ao renderizar a listagem
SELECT COALESCE(JSON_EXTRACT(up.dashboard_settings, '$.enrollments_list_compact'), 0) AS compact
  FROM user_preferences up
 WHERE up.user_uuid = :user_uuid
 LIMIT 1;

-- POST /app/profile/preferences/display  (key validada contra uma lista branca)
UPDATE user_preferences
   SET dashboard_settings = JSON_SET(COALESCE(dashboard_settings, '{}'), '$.enrollments_list_compact', :value),
       updated_at = CURRENT_TIMESTAMP
 WHERE user_uuid = :user_uuid;
```

O controller converte o booleano do JSON em `1`/`0` antes do bind e a view usa `$compact` para renderizar o alvo já com `data-compact` e o gatilho com a classe ativa (sem “pulo” no carregamento). O caminho JSON vem de lista branca, nunca do request.

## Faça / Não faça

- **Faça:** sincronize `aria-expanded`/`aria-pressed` no `toggled`.
- **Faça:** renderize o estado inicial no servidor (alvo e classe do gatilho coerentes).
- **Não faça:** usar Toggle para conteúdo com transição de altura — use Collapse.
- **Não faça:** dois gatilhos diferentes para o mesmo alvo com classes ativas independentes (ficam dessincronizados).
