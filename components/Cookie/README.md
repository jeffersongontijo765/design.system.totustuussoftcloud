# Cookie

Leitura e gravação de cookies no navegador com js-cookie 3.0.5 (`Cookies.get/set/remove`) para preferências leves de interface — menu lateral recolhido, densidade de tabela, idioma — com `SameSite=Lax` e `Secure` em HTTPS.

## Quando usar

- Preferência de UI que **o servidor precisa ler antes de renderizar** (evita “piscar”): sidebar recolhida, `ttsc-locale`, densidade da tabela. O PHP lê `$_COOKIE` e já imprime a classe certa no `<body>`.
- Preferência válida por dispositivo/navegador (o usuário quer o menu recolhido no notebook, aberto no monitor grande).
- Estado anônimo, antes do login (idioma da tela de login).
- **Não use** para dados que devem seguir o usuário entre dispositivos (tema, fuso, formato de data, notificações): grave em `user_preferences` pela tela de Preferências.
- **Não use** para tokens/sessão: esses são cookies `HttpOnly` gravados só pelo PHP (`App\Support\Cookie`, `remember_me`) — JS não deve lê-los.
- **Não use** para consentimento LGPD: o fluxo próprio está em [CookieAlert](../CookieAlert/README.md) (`cookie_consent`).
- Estado só do cliente que o servidor nunca lê (filtro aberto, aba ativa) → `localStorage`, que não viaja em toda requisição.

### Cookie × `user_preferences`

| Critério | Cookie (`ttsc_*`) | `user_preferences` |
|---|---|---|
| Escopo | navegador/dispositivo | usuário (todos os dispositivos) |
| Lido por | PHP em toda requisição + JS | PHP ao montar a sessão/página |
| Antes do login | sim | não |
| Exemplos | `ttsc_sidebar_collapsed`, `ttsc_table_density`, `ttsc-locale` | `theme`, `language`, `timezone`, `date_format`, `notify_*`, `dashboard_settings` |
| Tamanho | < 4 KB total por domínio, poucos bytes por chave | JSON livre (`dashboard_settings`, `kanban_settings`) |

## Anatomia

```
Set-Cookie: ttsc_sidebar_collapsed=1; Path=/; Expires=<+365d>; SameSite=Lax; Secure
            └ nome (prefixo ttsc_)   └ valor curto  └ atributos padrão do chassi
```

| Parte | Valor | Obrigatório |
|---|---|---|
| Nome | `ttsc_<preferencia>` em snake_case (exceção histórica: `ttsc-locale`) | sim |
| Valor | string curta (`'1'`, `'0'`, `'compact'`); nunca JSON grande nem PII | sim |
| `path` | `/` | sim |
| `expires` | `365` (dias) | sim para preferências |
| `sameSite` | `'Lax'` | sim |
| `secure` | `location.protocol === 'https:'` | sim em produção |
| `domain` | omitir (host atual do tenant) | não |

## Variantes

| Variante | Chave | Valores | Efeito visual | Tokens |
|---|---|---|---|---|
| Menu recolhido | `ttsc_sidebar_collapsed` | `'1'` / `'0'` | sub-sidebar de `--ttsc-sub-sidebar-w` para só ícones | item ativo `ttsc-accent-soft` + `ttsc-accent-text` |
| Densidade | `ttsc_table_density` | `'compact'` / ausente | linhas `--ttsc-row-compact` | divisória `ttsc-border-soft` |
| Idioma | `ttsc-locale` | `pt-BR`, `en`… | lido por `Helpers.php` / `Auth.php` | — |

## API

js-cookie 3.0.5 (global `Cookies`):

| Método | Retorno | Uso |
|---|---|---|
| `Cookies.get(name)` | string \| undefined | lê um cookie |
| `Cookies.get()` | objeto `{nome: valor}` | todos os cookies legíveis |
| `Cookies.set(name, value, attrs?)` | string escrita | grava |
| `Cookies.remove(name, attrs?)` | — | apaga (use os **mesmos** `path`/`domain` da gravação) |
| `Cookies.withAttributes(attrs)` | nova instância | fixa atributos padrão (`path`, `expires`, `sameSite`, `secure`) |
| `Cookies.withConverter({ read, write })` | nova instância | codificação customizada |
| `Cookies.attributes` / `Cookies.converter` | objeto | padrões da instância |

Atributos: `expires` (dias ou `Date`), `path`, `domain`, `secure` (bool), `sameSite` (`'Strict' | 'Lax' | 'None'`).

Servidor: `App\Support\Cookie::get/set/forever/forget/has` (`set` grava `HttpOnly=true` por padrão — passe `httpOnly: false` só para preferências que o JS também altera).

## Acessibilidade

- O controle que grava a preferência é um switch real (`input.ttsc-switch` com `<label>`), operável por teclado.
- Recolher o menu não pode esconder rótulos sem alternativa: no modo recolhido, cada link mantém `aria-label`/tooltip com o nome (“Matrículas”).
- Preferência aplicada no servidor evita mudança de layout após o carregamento (sem salto de conteúdo para leitores de tela e zoom).
- Texto do item ativo em `ttsc-accent-text` (≥ 4,5:1), nunca `ttsc-accent`.

## Modelos

### HTML

```html
<?php $collapsed = ($_COOKIE['ttsc_sidebar_collapsed'] ?? '0') === '1'; ?>
<body class="<?= $collapsed ? 'ttsc-sidebar-collapsed' : '' ?>">
  …
  <label class="flex items-center gap-2 text-sm">
    <input type="checkbox" class="ttsc-switch" data-ttsc-ui-pref="ttsc_sidebar_collapsed"
           <?= $collapsed ? 'checked' : '' ?>>
    Recolher menu lateral
  </label>
  <label class="flex items-center gap-2 text-sm">
    <input type="checkbox" class="ttsc-switch" data-ttsc-ui-pref="ttsc_table_density" value="compact"
           <?= ($_COOKIE['ttsc_table_density'] ?? '') === 'compact' ? 'checked' : '' ?>>
    Linhas compactas
  </label>
</body>
```

### CSS

```css
/* Sub-sidebar recolhida pela preferência em cookie */
.ttsc-sidebar-collapsed { --ttsc-sub-sidebar-w: 56px; }
.ttsc-sidebar-collapsed .ttsc-sub-sidebar .ttsc-menu-title { display: none; }
.ttsc-sub-sidebar { width: var(--ttsc-sub-sidebar-w); transition: width .2s ease; }

/* Densidade compacta das tabelas */
.ttsc-density-compact .ttsc-table td { height: var(--ttsc-row-compact); padding-block: 0; }
```

### JS

```js
// assets/js/core/ttsc.ui-prefs.js — requer /assets/vendors/js-cookie/js.cookie.min.js
const UiCookies = Cookies.withAttributes({
  path: '/',
  expires: 365,
  sameSite: 'Lax',
  secure: location.protocol === 'https:',
});

const APPLY = {
  ttsc_sidebar_collapsed: (on) => document.body.classList.toggle('ttsc-sidebar-collapsed', on),
  ttsc_table_density: (on) => document.body.classList.toggle('ttsc-density-compact', on),
};

export function setUiPref(name, input) {
  const on = input.checked;
  if (name === 'ttsc_sidebar_collapsed') UiCookies.set(name, on ? '1' : '0');
  else if (on) UiCookies.set(name, input.value || '1');
  else UiCookies.remove(name);           // mesmos atributos da gravação (withAttributes)
  APPLY[name]?.(on);
}

document.addEventListener('change', (event) => {
  const input = event.target.closest('[data-ttsc-ui-pref]');
  if (input) setUiPref(input.dataset.ttscUiPref, input);
});

// Botão "Restaurar padrão"
export function resetUiPrefs() {
  Object.keys(APPLY).forEach((name) => { UiCookies.remove(name); APPLY[name](false); });
}
```

### SQL

Preferências que acompanham o usuário vão para `user_preferences` (uma linha por `user_uuid`, chave única). Os ajustes de layout que precisam sobreviver à troca de dispositivo usam o JSON `dashboard_settings`:

```sql
-- Ler as preferências do usuário ao montar a sessão
SELECT up.theme, up.language, up.timezone, up.date_format,
       JSON_EXTRACT(up.dashboard_settings, '$.sidebar_collapsed') AS sidebar_collapsed
  FROM user_preferences up
 WHERE up.user_uuid = :user_uuid;

-- Gravar o tema (upsert pela chave única user_uuid)
INSERT INTO user_preferences (uuid, user_uuid, theme, code)
VALUES (:uuid, :user_uuid, :theme, :code)
ON DUPLICATE KEY UPDATE theme = VALUES(theme);

-- Promover a preferência do cookie para o perfil (opcional, "usar em todos os dispositivos")
UPDATE user_preferences
   SET dashboard_settings = JSON_SET(COALESCE(dashboard_settings, '{}'),
                                     '$.sidebar_collapsed', JSON_EXTRACT(:bool_json, '$'))  -- 'true' | 'false'
 WHERE user_uuid = :user_uuid;
```

No login, o PHP lê `user_preferences` e, se `sidebar_collapsed` estiver definido, emite `Set-Cookie: ttsc_sidebar_collapsed=…` — a partir daí o cookie é a fonte rápida do layout.

## Faça / Não faça

- **Faça:** prefixo `ttsc_`, valores curtos, `SameSite=Lax`, `Secure` em HTTPS, `path=/`.
- **Faça:** apague com os mesmos atributos usados na gravação (`withAttributes` garante).
- **Faça:** aplique a classe no servidor a partir de `$_COOKIE` para não piscar.
- **Não faça:** guardar nome, CPF, e-mail ou qualquer dado pessoal em cookie.
- **Não faça:** ler/gravar `access_token`, `remember_me` ou cookies de sessão via JS.
- **Não faça:** gravar cookies não essenciais (analytics, marketing) sem consentimento — consulte `cookie_consent` primeiro ([CookieAlert](../CookieAlert/README.md)). Preferências de UI são da categoria `preferences`.
