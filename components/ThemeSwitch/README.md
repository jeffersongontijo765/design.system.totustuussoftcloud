# ThemeSwitch

Seletor de tema do ttscui (`data-ttsc-theme-switch-toggle` / `data-ttsc-theme-switch-set`) com modos `light`, `dark` e `system`, persistido em `localStorage` e, no TotusTuus, em `user_preferences.theme`.

## Quando usar

- Controle de tema no menu do perfil (drawer de configurações) e um atalho de alternância no topbar.
- Telas públicas (login, portal) que respeitam a preferência do sistema operacional (`system`).
- **Não use** para alternar outras preferências visuais (densidade, idioma): use [Toggle](../Toggle/README.md) ou um formulário de preferências.
- Para um interruptor genérico liga/desliga use o `ttsc-switch`; o ThemeSwitch sempre age sobre o `<html>`.

## Tema: design system × aplicação

| Onde | Como o tema é aplicado | Quem lê |
|---|---|---|
| Design system (este catálogo, `tokens.css`) | atributo **`data-theme="light\|dark"`** no `<html>` (ou em qualquer container — os tokens são definidos em `[data-theme="dark"]`) | `--ttsc-*` |
| Runtime ttscui / Tailwind | classe **`.dark`** no `<html>` (o CSS usa `:is(.dark,[data-theme=dark])`) | variantes `dark:` e componentes `.ttsc-*` |
| ThemeSwitch do ttscui | troca a **classe** `light`/`dark` no `<html>` e grava `localStorage['ttsc-theme']` | — |
| App (`ttsc.js`, `setAppTheme`) | classe `.dark` + `data-ttsc-theme-mode`; telas de auth/portal usam `data-theme` | — |

Regra do TotusTuus: no evento `changed`, espelhe o modo aplicado em **`data-theme`** também (modelo JS abaixo). Assim tokens (`data-theme`) e runtime (`.dark`) ficam sempre iguais.

## Anatomia

```
<html class="dark" data-theme="dark" data-ttsc-theme-switch-mode="system">   ← instância única (documentElement)
  [data-ttsc-theme-switch-set="light|dark|system"]   botões de escolha (segmentado)
  [data-ttsc-theme-switch-toggle]                    botão de alternância (claro ↔ escuro)
  input[type=checkbox][data-ttsc-theme-switch-state="dark"]   checkbox marcado quando o modo bate
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Instância | criada automaticamente no `<html>` por `TTSC.init()` | sim |
| Escolha | `[data-ttsc-theme-switch-set="light\|dark\|system"]` | um dos dois |
| Alternância | `[data-ttsc-theme-switch-toggle]` | um dos dois |
| Estado em checkbox | `input[type=checkbox][data-ttsc-theme-switch-state]` | não |
| Modo inicial | `data-ttsc-theme-switch-mode` no `<html>` | não (padrão `light`) |

## Estados

| Modo | Aplicado | Observação |
|---|---|---|
| `light` | `light` | — |
| `dark` | `dark` | — |
| `system` | `prefers-color-scheme` no momento da escolha | para seguir mudanças do SO em tempo real, ouça o `matchMedia` (JS abaixo) |

Tokens: o segmentado usa `ttsc-canvas-2` (trilho), `ttsc-surface` + `shadow-xs` (item ativo), texto `ttsc-text`/`ttsc-text-2`, foco `ttsc-accent`.

## API

| Atributo | Efeito |
|---|---|
| `data-ttsc-theme-switch-set="<modo>"` | clique define o modo (delegado no `body`) |
| `data-ttsc-theme-switch-toggle` | clique alterna entre `light` e `dark` (a partir do aplicado) |
| `data-ttsc-theme-switch-mode` (no `<html>`) | modo inicial quando não há `localStorage['ttsc-theme']`; é reescrito a cada troca |
| `data-ttsc-theme-switch-state="<modo>"` | checkbox marcado quando o modo atual é esse |

| Método | Efeito |
|---|---|
| `TTSC.ThemeSwitch.getInstance()` | instância do `<html>` (sem argumento) |
| `inst.getMode()` | modo salvo (`light`/`dark`/`system`) |
| `inst.setMode(mode)` | define e persiste |
| `inst.on('change', fn)` | antes de trocar; `fn(evt)` pode fazer `evt.cancel = true` |

| Evento (no `<html>`, bubbles) | Quando |
|---|---|
| `change` | antes da troca (`detail.payload.cancel` cancela) |
| `changed` | depois da troca e do `localStorage` |

## Acessibilidade

- Segmentado: `role="group"` + `aria-label="Tema da interface"`; cada botão com `aria-pressed` refletindo o modo.
- Botão só-ícone de alternância com `aria-label="Alternar tema"` e ícone que indica o próximo estado (lua no claro, sol no escuro).
- Não anime cores de fundo da página inteira (flash); troque de uma vez.
- Os dois temas são validados pelos tokens: texto `ttsc-text` ≥ 15:1, `ttsc-text-muted` ≥ 4,5:1, verde de texto `ttsc-accent-text` (#006e46 no claro, #3ecf8e no escuro).

## Modelos

### HTML

```html
<!-- Drawer de perfil: escolha do tema -->
<div class="flex flex-col gap-2">
  <span class="text-xs font-medium" id="theme-label">Tema</span>
  <div class="ttsc-theme-seg" role="group" aria-labelledby="theme-label">
    <button type="button" data-ttsc-theme-switch-set="light" aria-pressed="false"><i class="fa-light fa-sun"></i> Claro</button>
    <button type="button" data-ttsc-theme-switch-set="dark" aria-pressed="false"><i class="fa-light fa-moon"></i> Escuro</button>
    <button type="button" data-ttsc-theme-switch-set="system" aria-pressed="false"><i class="fa-light fa-desktop"></i> Sistema</button>
  </div>
</div>

<!-- Topbar: alternância rápida -->
<button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon" data-ttsc-theme-switch-toggle="true" aria-label="Alternar tema">
  <i class="fa-light fa-moon when-light"></i><i class="fa-light fa-sun when-dark"></i>
</button>

<!-- Layout: tema do servidor antes do primeiro paint (evita flash) -->
<html lang="pt-BR" data-theme="<?= $e($resolvedTheme) ?>" class="<?= $e($resolvedTheme) ?>"
      data-ttsc-theme-switch-mode="<?= $e($userTheme) ?>">
```

### CSS

```css
/* Tokens: [data-theme="dark"] redefine --ttsc-*; a ponte liga o runtime */
:root { --background: var(--ttsc-surface); --foreground: var(--ttsc-text); }

/* Segmentado de tema (extensão TTSC) */
.ttsc-theme-seg { display: inline-flex; gap: 2px; padding: 3px; border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control); background: var(--ttsc-canvas-2); }
.ttsc-theme-seg button { display: inline-flex; align-items: center; gap: 6px; height: 30px; padding: 0 12px; border: 0; border-radius: var(--ttsc-radius-sm); background: transparent; color: var(--ttsc-text-2); font-size: 12px; cursor: pointer; }
.ttsc-theme-seg button[aria-pressed="true"] { background: var(--ttsc-surface); color: var(--ttsc-text); box-shadow: var(--ttsc-shadow-xs); font-weight: 600; }
.ttsc-theme-seg button:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 1px; }

/* Ícone do toggle conforme o tema aplicado: dois ícones, um visível por tema */
[data-ttsc-theme-switch-toggle] .when-dark { display: none; }
[data-theme="dark"] [data-ttsc-theme-switch-toggle] .when-dark { display: inline-block; }
[data-theme="dark"] [data-ttsc-theme-switch-toggle] .when-light { display: none; }
```

### JS

```js
TTSC.init();
var themeSwitch = TTSC.ThemeSwitch.getInstance();
var html = document.documentElement;

function syncTheme() {
  var mode = themeSwitch.getMode();                       // light | dark | system
  var applied = html.classList.contains('dark') ? 'dark' : 'light';
  html.setAttribute('data-theme', applied);               // tokens do design system
  document.querySelectorAll('[data-ttsc-theme-switch-set]').forEach(function (b) {
    b.setAttribute('aria-pressed', String(b.getAttribute('data-ttsc-theme-switch-set') === mode));
  });
  return { mode: mode, applied: applied };
}

// Depois de cada troca: espelha em data-theme e persiste no servidor
html.addEventListener('changed', function () {
  var state = syncTheme();
  fetch('/app/profile/preferences/theme', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content },
    body: JSON.stringify({ theme: state.mode }),
  });
});

// Modo "system": acompanha a mudança do sistema operacional em tempo real
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
  if (themeSwitch.getMode() === 'system') themeSwitch.setMode('system');
});

syncTheme();
```

### SQL

A preferência fica em `user_preferences.theme` (`varchar(64)`, padrão `'system'`, valores do catálogo `ref_enum_user_preferences_theme_c102ece3a5fe`; `user_uuid` é único):

```sql
-- Layout: tema do usuário logado (antes de renderizar o <html>)
SELECT COALESCE(up.theme, 'system') AS theme
  FROM user_preferences up
 WHERE up.user_uuid = :user_uuid
 LIMIT 1;

-- POST /app/profile/preferences/theme  (:theme validado em ['light','dark','system'])
UPDATE user_preferences
   SET theme = :theme, updated_at = CURRENT_TIMESTAMP
 WHERE user_uuid = :user_uuid;

-- Primeiro acesso (sem linha ainda): upsert pela chave única user_uuid
INSERT INTO user_preferences (uuid, user_uuid, theme)
VALUES (UUID(), :user_uuid, :theme)
ON DUPLICATE KEY UPDATE theme = :theme_again, updated_at = CURRENT_TIMESTAMP;
```

O layout resolve `system` no servidor como `light` (o JS corrige no load se o SO estiver escuro) e escreve `data-theme`, `class` e `data-ttsc-theme-switch-mode` no `<html>`; o PDO usa `:theme_again` porque placeholders nomeados não podem se repetir com emulação desligada.

## Faça / Não faça

- **Faça:** mantenha `data-theme` e `.dark` sincronizados no `changed`.
- **Faça:** renderize o tema no servidor para evitar flash no carregamento.
- **Não faça:** gravar o tema só no `localStorage` — o usuário perde a escolha em outro dispositivo.
- **Não faça:** cores fixas (`bg-white`, `text-slate-900`) em telas novas: elas não mudam com o tema; use tokens.
