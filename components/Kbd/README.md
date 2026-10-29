# Kbd

Tecla ou combinação de teclas (`.ttsc-kbd`) exibida em dicas de atalho, menus e na busca global — `Ctrl K` no Windows/Linux, `⌘ K` no macOS.

## Quando usar

- Mostrar o atalho de uma ação ao lado do rótulo: busca global (`Ctrl K`), nova matrícula (`N`), salvar drawer (`Ctrl S`), fechar (`Esc`).
- No placeholder/sufixo do campo de busca do cabeçalho e no rodapé de paletas de comando (“↑ ↓ navegar · Enter abrir”).
- Na página “Atalhos de teclado” das preferências do usuário.
- Não use para código-fonte ou valores (use `<code>`) nem para códigos de registro como `MAT-2026-0381` (use [Badge](../Badge/README.md) `ttsc-badge-stroke`).
- Não mostre atalhos em telas de toque/mobile — a extensão CSS esconde `.ttsc-kbd-combo` abaixo de 768px.

## Anatomia

```
[ Ctrl ] + [ K ]        kbd.ttsc-kbd (uma tecla por elemento)
   │          └ .ttsc-kbd  (ou .ttsc-kbd-outline sobre fundos claros)
   └ separador opcional: texto "+" em ttsc-text-muted
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Tecla | `<kbd class="ttsc-kbd">` | sim |
| Estilo | (preenchido) · `ttsc-kbd-outline` | não |
| Tamanho | `ttsc-kbd-xs` (20px) · `ttsc-kbd-sm` (24px) · padrão (28px) | não |
| Combinação | `<kbd>` externo agrupando as teclas (`.ttsc-kbd-combo`, extensão) | não |
| Ícone de tecla | `<i class="fa-light fa-arrow-turn-down-left">` dentro do `kbd` (Enter) | não |

## Variantes

| Variante | Classe | Uso | Tokens |
|---|---|---|---|
| Preenchida | `ttsc-kbd` | dicas em menus e tooltips | fundo `--accent` (= `ttsc-canvas-2`), borda `ttsc-border`, texto `ttsc-text` (16:1) |
| Outline | `ttsc-kbd ttsc-kbd-outline` | dentro de inputs e cabeçalho (sobre `ttsc-surface`) | borda `--input` (= `ttsc-border-strong`), fundo transparente |
| Discreta (extensão) | `ttsc-kbd ttsc-kbd-muted` | sufixo do campo de busca | texto `ttsc-text-muted` (4,8:1 claro / 4,5:1 escuro sobre `canvas-2`) |
| Tamanhos | `ttsc-kbd-xs` · `ttsc-kbd-sm` · padrão | xs em menus densos, sm em inputs | fonte `--font-mono` 11–12px |

## API

Sem JavaScript no ttscui. A extensão `ttsc.shortcuts.js` (modelo JS) faz duas coisas:

| Atributo (extensão) | Efeito |
|---|---|
| `data-ttsc-kbd="mod+k"` | renderiza as teclas certas por plataforma: `mod` vira `⌘` no macOS e `Ctrl` nos demais |
| `data-ttsc-shortcut="mod+k"` em um botão/link | registra o atalho global que dispara `click()` no elemento |

Teclas reconhecidas: `mod`, `ctrl`, `alt` (`⌥` no Mac), `shift` (`⇧`), `enter` (`↵`), `esc`, `up`/`down`/`left`/`right` (setas), letras e dígitos.

## Acessibilidade

- Use `<kbd>` (semântica nativa); para combinação, aninhe: `<kbd><kbd class="ttsc-kbd">Ctrl</kbd> <kbd class="ttsc-kbd">K</kbd></kbd>`.
- Símbolos do Mac ganham nome acessível: `<kbd class="ttsc-kbd" title="Command" aria-label="Command">⌘</kbd>`.
- No botão, o atalho também vai para `aria-keyshortcuts="Control+K Meta+K"`.
- Atalhos globais não disparam com foco em `input`, `textarea`, `select` ou `[contenteditable]` (exceto `Esc` e combinações com `mod`).
- Nunca sobrescreva atalhos do navegador/leitor de tela (`Ctrl L`, `Ctrl T`, `Alt` + letra).

## Modelos

### HTML

```html
<!-- Busca global no cabeçalho -->
<button type="button" class="ttsc-btn ttsc-btn-outline" data-ttsc-modal-toggle="#search_modal"
        data-ttsc-shortcut="mod+k" aria-keyshortcuts="Control+K Meta+K">
  <i class="fa-light fa-magnifying-glass"></i> Buscar alunos, cursos…
  <kbd class="ttsc-kbd-combo" data-ttsc-kbd="mod+k"></kbd>
</button>

<!-- Item de dropdown com atalho -->
<a class="ttsc-dropdown-menu-link" href="/academic/enrollments/new" data-ttsc-shortcut="n">
  <i class="fa-light fa-user-plus"></i> Nova matrícula
  <kbd class="ttsc-kbd ttsc-kbd-xs">N</kbd>
</a>

<!-- Rodapé da paleta de comandos -->
<div class="flex items-center gap-3 text-xs text-muted-foreground">
  <span><kbd class="ttsc-kbd ttsc-kbd-xs" aria-label="Seta para cima">↑</kbd> <kbd class="ttsc-kbd ttsc-kbd-xs" aria-label="Seta para baixo">↓</kbd> navegar</span>
  <span><kbd class="ttsc-kbd ttsc-kbd-xs" aria-label="Enter"><i class="fa-light fa-arrow-turn-down-left"></i></kbd> abrir</span>
  <span><kbd class="ttsc-kbd ttsc-kbd-xs">Esc</kbd> fechar</span>
</div>
```

### CSS

```css
/* Ponte (bundle.css): fundo e texto da tecla vêm do hover neutro e do texto principal */
:root { --accent: var(--ttsc-canvas-2); --accent-foreground: var(--ttsc-text); --input: var(--ttsc-border-strong); }

/* Extensão TTSC */
.ttsc-kbd { font-weight: 500; box-shadow: inset 0 -1px 0 var(--ttsc-border); }
.ttsc-kbd-outline { box-shadow: none; }
.ttsc-kbd-muted { color: var(--ttsc-text-muted); }
.ttsc-kbd-combo { display: inline-flex; align-items: center; gap: var(--ttsc-space-1); font: inherit; }
.ttsc-kbd i { font-size: 11px; }
.ttsc-dropdown-menu-link > .ttsc-kbd, .ttsc-dropdown-menu-link > .ttsc-kbd-combo { margin-inline-start: auto; }
@media (max-width: 767px) { .ttsc-kbd-combo, .ttsc-dropdown-menu-link > .ttsc-kbd { display: none; } }
```

### JS

```js
// assets/js/core/ttsc.shortcuts.js — renderiza <kbd> por plataforma e registra atalhos globais
const IS_MAC = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);
const LABEL = {
  mod: IS_MAC ? ['⌘', 'Command'] : ['Ctrl', 'Control'],
  ctrl: ['Ctrl', 'Control'], alt: IS_MAC ? ['⌥', 'Option'] : ['Alt', 'Alt'],
  shift: IS_MAC ? ['⇧', 'Shift'] : ['Shift', 'Shift'], enter: ['↵', 'Enter'], esc: ['Esc', 'Escape'],
  up: ['↑', 'Seta para cima'], down: ['↓', 'Seta para baixo'], left: ['←', 'Seta para a esquerda'], right: ['→', 'Seta para a direita'],
};

export function renderKbd(el, combo, size = 'ttsc-kbd-sm') {
  el.textContent = '';
  combo.split('+').forEach((key) => {
    const [text, name] = LABEL[key] || [key.toUpperCase(), key.toUpperCase()];
    const k = document.createElement('kbd');
    k.className = `ttsc-kbd ttsc-kbd-outline ${size}`;
    k.textContent = text;
    if (text !== name) k.setAttribute('aria-label', name);
    el.appendChild(k);
  });
}

function matches(event, combo) {
  const keys = combo.split('+');
  const key = keys[keys.length - 1];
  const wantMod = keys.includes('mod');
  const hasMod = IS_MAC ? event.metaKey : event.ctrlKey;
  return event.key.toLowerCase() === (key === 'esc' ? 'escape' : key)
    && wantMod === hasMod
    && keys.includes('shift') === event.shiftKey
    && keys.includes('alt') === event.altKey;
}

export function initShortcuts(prefs = { enabled: true }) {
  document.querySelectorAll('[data-ttsc-kbd]').forEach((el) => renderKbd(el, el.dataset.ttscKbd));
  if (!prefs.enabled) return;
  document.addEventListener('keydown', (event) => {
    const t = event.target;
    const typing = t.closest('input, textarea, select, [contenteditable="true"]');
    document.querySelectorAll('[data-ttsc-shortcut]').forEach((el) => {
      const combo = (prefs.bindings && prefs.bindings[el.dataset.shortcutId]) || el.dataset.ttscShortcut;
      if (typing && !combo.startsWith('mod')) return;
      if (matches(event, combo)) { event.preventDefault(); el.click(); }
    });
  });
}

// Preferências vêm do PHP: <script>window.TTSC_SHORTCUTS = <?= json_encode($shortcuts) ?></script>
document.addEventListener('DOMContentLoaded', () => initShortcuts(window.TTSC_SHORTCUTS || { enabled: true }));
```

### SQL

O esquema não tem tabela de atalhos; a plataforma (`⌘` × `Ctrl`) é detectada no navegador e **não** é persistida. O que persiste é a preferência do usuário (ligar/desligar atalhos e remapear), guardada no JSON `user_preferences.dashboard_settings` — sem DDL nova:

```sql
-- Ler a preferência (MariaDB 10.11 / MySQL 8)
SELECT up.user_uuid,
       COALESCE(JSON_UNQUOTE(JSON_EXTRACT(up.dashboard_settings, '$.shortcuts.enabled')), '1') AS shortcuts_enabled,
       JSON_EXTRACT(up.dashboard_settings, '$.shortcuts.bindings') AS bindings
  FROM user_preferences up
 WHERE up.user_uuid = :user_uuid;

-- Salvar (página Preferências › Atalhos de teclado)
UPDATE user_preferences
   SET dashboard_settings = JSON_SET(COALESCE(dashboard_settings, '{}'), '$.shortcuts',
         JSON_OBJECT('enabled', :enabled, 'bindings', JSON_OBJECT('search', :bind_search, 'new_enrollment', :bind_new)))
 WHERE user_uuid = :user_uuid;
```

O PHP converte a linha em `['enabled' => (bool) $row['shortcuts_enabled'], 'bindings' => json_decode($row['bindings'] ?? '{}', true)]` e imprime em `window.TTSC_SHORTCUTS`; o JS usa `bindings[data-shortcut-id]` no lugar do padrão.

## Faça / Não faça

- **Faça:** uma tecla por `ttsc-kbd`; escreva `mod` no HTML e deixe o JS decidir `⌘`/`Ctrl`.
- **Faça:** `ttsc-kbd-xs` em menus, `ttsc-kbd-sm` dentro de inputs e botões.
- **Faça:** atalhos de letra única só fora de campos de texto.
- **Não faça:** texto “Ctrl+K” solto sem `<kbd>`; atalhos que conflitam com o navegador.
- **Não faça:** mostrar atalhos em mobile ou no portal do aluno em telas pequenas.
