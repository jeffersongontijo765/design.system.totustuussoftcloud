# StarterKitAppShellCollapsed

O mesmo `app/layouts/main.php` do [StarterKitAppShell](../StarterKitAppShell/README.md) com o sub-sidebar recolhido pelo mecanismo real de `assets/js/ttsc.shell.js`: só o rail de 60px, o botão "Menu" ao lado do título e o conteúdo em largura total.

## Quando usar

- Telas que precisam de largura (kanban, grade de horários, planilha de notas, mapa de sala) em que o usuário recolhe o menu do módulo e o app lembra a escolha.
- Ponto de partida para validar que uma página nova continua legível sem os 320px do sub-sidebar.
- Página que **nunca** deve ter sub-sidebar → não use a preferência; passe `'hideSubSidebar' => true` no `layout()` (o `<aside>` nem é impresso).
- Menu em gaveta no celular/tablet → é automático em ≤ 1099px; a preferência de recolher é ignorada nessa faixa (ver Estados).

## Anatomia

```
header (56px) ───────────────────────────────────────────────────────────────────────────
rail │ [▯ Menu]  [ícone] Título da página                                       [Atualizar]
60px │           breadcrumb
     │ banner de contexto ...................................................................
     │ [KPI 4][Tabela 0][Cartões 0][Kanban][Analytics]                     [Filtrar][Exportar]
     │ SLOT de conteúdo (largura total) ......................................................
footer ──────────────────────────────────────────────────────────────────────────────────
```

| Parte | Seletor real | Obrigatório |
|---|---|---|
| Sub-sidebar recolhido | `aside#sub-sidebar.collapsed` (largura 0, conteúdo oculto) | sim |
| Botão de expandir | `button#sub-sidebar-expand-btn` (sem `.hidden`; `onclick="toggleSubSidebar()"`) | sim |
| Preferência | `localStorage['ttsc:sub-sidebar:collapsed'] = '1'` | sim |
| Botão de recolher (dentro do sub-sidebar) | `button#subsidebar-collapse-btn[data-sidebar-collapse]` (o `«`), delegado por `ttsc.drawer.js` para `toggleSubSidebar()` | sim |
| Atalho | `Ctrl+B` / `Cmd+B` (registrado por `ttsc.shell.js`) | sim |

## Estados

| Estado | Como acontece | Resultado |
|---|---|---|
| Expandido (padrão) | sem a chave ou `'0'` | `#sub-sidebar` com 320px, `#sub-sidebar-expand-btn.hidden` |
| Recolhido | `toggleSubSidebar()` em ≥ 1100px → `classList.toggle('collapsed')` + grava `'1'` | `#sub-sidebar.collapsed`, botão "Menu" visível |
| Restaurado no load | `restoreSidebarPreference()` no `DOMContentLoaded` (só se `!matchMedia('(max-width: 1099px)').matches`) | volta recolhido |
| ≤ 1099px | `media.addEventListener('change')` esconde o botão "Menu"; `toggleSubSidebar()` passa a abrir/fechar a gaveta (`.is-mobile-open`) | gaveta, preferência ignorada |
| Voltou para ≥ 1100px | o mesmo listener reexibe o botão se `.collapsed` | recolhido de novo |

## API

| Função / evento (`ttsc.shell.js`) | Efeito |
|---|---|
| `window.toggleSubSidebar()` | ≥ 1100px: alterna `.collapsed` e grava `ttsc:sub-sidebar:collapsed`; ≤ 1099px: alterna `.is-mobile-open` e fecha o rail |
| `window.toggleMainSidebar()` | gaveta do rail (≤ 1099px) |
| `keydown` `Ctrl/Cmd+B` | `toggleSubSidebar()` |
| `keydown` `Esc` | `closeNavigation()` |
| `syncSubSidebarExpandButton()` (interna) | posiciona o botão "Menu" ao lado do título |

## Acessibilidade

- O botão "Menu" tem `title="Expandir Barra Lateral"` e texto visível; ao recolher, mova o foco para ele (exemplo no JS abaixo) para o usuário não perder a posição.
- Com o sub-sidebar recolhido, a navegação de módulo continua no rail (`aria-current="page"` no item ativo).
- `Ctrl+B` não conflita com campos de texto do app; anuncie o estado com `aria-expanded` no botão de recolher.

## Modelos

### HTML

```php
<?php
// Página larga que começa recolhida na primeira visita (o usuário pode expandir; a escolha dele vale depois)
$this->layout('app::layouts/main', [
    'title' => 'Grade de Horários — 2027',
    'icon' => 'fa-light fa-calendar-week',
    'pageHasHeader' => true,
    'railKey' => 'admin',
    'subSidebarModule' => 'academic',
]);
?>
<?php $this->start('content') ?>
<div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
  <div class="flex items-start space-x-3.5">
    <div class="w-11 h-11 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center shrink-0">
      <i class="fa-light fa-calendar-week text-emerald-600 text-lg" aria-hidden="true"></i>
    </div>
    <div><h1 class="text-xl font-semibold text-slate-900 tracking-tight">Grade de Horários — 2027</h1></div>
  </div>
</div>
<div id="grade-horarios" class="space-y-4">…</div>
<?php $this->stop() ?>
<?php $this->start('scripts') ?>
<script nonce="<?= \App\Security\CspNonce::get() ?>">
  try { if (localStorage.getItem('ttsc:sub-sidebar:collapsed') === null) localStorage.setItem('ttsc:sub-sidebar:collapsed', '1'); } catch (e) {}
</script>
<?php $this->stop() ?>
```

### CSS

O estado vem de `ttsc.shell-layout.css` / `ttsc.design-system.css` (no bundle). Extensão: transição suave e conteúdo que aproveita a largura.

```css
#sub-sidebar { transition: flex-basis .2s cubic-bezier(.2,.8,.2,1), width .2s cubic-bezier(.2,.8,.2,1); }
#sub-sidebar.collapsed { flex-basis: 0; width: 0; min-width: 0; border-right: 0; overflow: hidden; }
#sub-sidebar-expand-btn { border-color: var(--ttsc-border); background: var(--ttsc-surface); color: var(--ttsc-text); border-radius: var(--ttsc-radius-control); }
#sub-sidebar-expand-btn:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
/* grade que ganha colunas quando o menu está recolhido */
body:has(#sub-sidebar.collapsed) .grade-horarios { grid-template-columns: repeat(6, minmax(0, 1fr)); }
@media (prefers-reduced-motion: reduce) { #sub-sidebar { transition: none; } }
```

### JS

```js
// Mesmo contrato do ttsc.shell.js, com foco e aria para quem cria um botão próprio de recolher
(function () {
  var KEY = 'ttsc:sub-sidebar:collapsed';
  var media = window.matchMedia('(max-width: 1099px)');
  var sub = document.getElementById('sub-sidebar');
  var expand = document.getElementById('sub-sidebar-expand-btn');
  if (!sub) return;

  function setCollapsed(collapsed) {
    if (media.matches) return;                        // gaveta: a preferência não se aplica
    sub.classList.toggle('collapsed', collapsed);
    if (expand) expand.classList.toggle('hidden', !collapsed);
    try { localStorage.setItem(KEY, collapsed ? '1' : '0'); } catch (e) {}
    document.querySelectorAll('[data-sub-sidebar-toggle]').forEach(function (b) {
      b.setAttribute('aria-expanded', String(!collapsed));
    });
    (collapsed ? expand : sub.querySelector('#subsidebar-filter'))?.focus();
  }
  document.querySelectorAll('[data-sub-sidebar-toggle]').forEach(function (b) {
    b.addEventListener('click', function () { setCollapsed(!sub.classList.contains('collapsed')); });
  });
  // estado inicial (o ttsc.shell.js faz o mesmo no DOMContentLoaded)
  try { if (!media.matches && localStorage.getItem(KEY) === '1') setCollapsed(true); } catch (e) {}
})();
```

O `kit.html` grava `ttsc:sub-sidebar:collapsed = '1'` no `<head>` e usa o mesmo shim de `DOMContentLoaded` do StarterKitAppShell para que o `restoreSidebarPreference()` real rode dentro do bundle.

### SQL

A preferência é só do navegador (`localStorage`); o shell usa as mesmas consultas do [StarterKitAppShell](../StarterKitAppShell/README.md#sql). Para levar a escolha entre dispositivos, guarde-a no JSON `dashboard_settings` que já existe em `user_preferences` (banco master):

```sql
-- ler junto com o tema na montagem do layout
SELECT theme,
       JSON_UNQUOTE(JSON_EXTRACT(dashboard_settings, '$.shell.subSidebarCollapsed')) AS sub_sidebar_collapsed
  FROM user_preferences
 WHERE user_uuid = :user_uuid
 LIMIT 1;

-- gravar a escolha (POST disparado pelo botão de recolher)
UPDATE user_preferences
   SET dashboard_settings = JSON_SET(COALESCE(dashboard_settings, '{}'), '$.shell.subSidebarCollapsed', :collapsed),
       updated_at = NOW()
 WHERE user_uuid = :user_uuid;
```

O layout passaria `sub_sidebar_collapsed` para o `<aside>` (`class="… collapsed"`) e o JS sincronizaria o `localStorage`; hoje o app real não persiste no servidor.

## Como começar um projeto a partir do kit

- Layout, partials, CSS e JS: idênticos ao [StarterKitAppShell](../StarterKitAppShell/README.md#como-começar-um-projeto-a-partir-do-kit) — o recolhimento não exige arquivo extra, só `ttsc.shell.js` e as regras `.collapsed` de `ttsc.shell-layout.css`.
- Para outro projeto: mantenha o `id="sub-sidebar"`, o `id="sub-sidebar-expand-btn"` e a chave `ttsc:sub-sidebar:collapsed`; o media query de 1099px precisa ser o mesmo no CSS e no JS.

## Faça / Não faça

- **Faça:** deixe o usuário decidir; no máximo defina o padrão da primeira visita (exemplo HTML).
- **Faça:** use `hideSubSidebar => true` quando a página não pertence a um módulo com menu.
- **Não faça:** esconder o sub-sidebar com `display:none` na página — quebra o botão "Menu" e o `Ctrl+B`.
- **Não faça:** gravar a preferência em outra chave (a Navigation antiga citava `ttsc-subsidebar-collapsed`; a real é `ttsc:sub-sidebar:collapsed`).
