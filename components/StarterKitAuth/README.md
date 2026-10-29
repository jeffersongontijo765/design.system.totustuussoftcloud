# StarterKitAuth

Kit das telas sem sessão: o render real de `resources/views/auth/layouts/main.php` (cartão dividido com painel da marca e formulário) com `auth/pages/login.php` e as variantes login por perfil, seleção de portal, seleção de instituição, MFA e esqueci a senha.

> Também listado em: **Páginas › PageAuth** (anatomia detalhada do cartão `sb-login-*`).

## Quando usar

- Toda tela antes da sessão ou de escolha de contexto: login (`/login` e `/login-developer|student|teacher|parents|thirdparty`), `forgot-password`, `reset-password`, `verify-email`, `register`, `request-access-parents`, `mfa-setup`, `mfa-verify`, `select-portal`, `select-entity`, `select-unit`, `logout_confirm`, `cookies_policy` — todas em `resources/views/auth/pages/` sobre `auth::layouts/main`.
- Não use dentro do shell autenticado (reautenticação dentro do app = modal) → [StarterKitAppShell](../StarterKitAppShell/README.md).
- Portal de suporte do cliente (login por e-mail + código) tem layout próprio → [StarterKitSupportPortal](../StarterKitSupportPortal/README.md).

## Anatomia

```
                                                     [idioma v] [tema]   (fixos, top:20px right:20px)
main#main-content.sb-login-page
└─ .sb-login-container (grid 1fr 1fr, máx. 1040px, raio 16px)
   ├─ .sb-login-brand  (logo 48px · "TotusTuus SoftCloud" · tagline · 4 garantias · copyright)
   └─ .sb-login-form > .sb-login-form-inner
        └─ section('content')  ← a página: .sb-login-mobile-header, título, form#loginForm, portais, rodapé
#toast-container · xss-helper · toggleAuthTheme() · section('scripts') · ttsc.events.js · auth.v2.js · consent-cookie.js
```

| Parte | Arquivo / seletor real | Obrigatório |
|---|---|---|
| Layout | `auth/layouts/main.php` (`$this->layout('auth::layouts/main', ['title' => …, 'subtitle' => …])`) | sim |
| Link de pular | `a.sr-only.sr-only-focusable[href="#main-content"]` | sim |
| Idioma | `app/partials/language_selector.php` (`position => 'login'`) | sim |
| Tema | `button#auth-theme-toggle.auth-theme-toggle` → `toggleAuthTheme()` | sim |
| Painel da marca | `.sb-login-brand` (compartilhado por todas as páginas) | sim |
| Formulário | `.sb-login-form-inner` ← `section('content')` | sim |
| Cabeçalho mobile | `.sb-login-mobile-header` (na página; aparece quando a marca some) | sim |
| Toasts | `#toast-container` + `showToast()` de `auth.v2.js` | sim |
| Slots | `section('styles')` (no `<head>`), `section('content')`, `section('scripts')` | — |

## Variantes / Estados

| Variante (botão do preview) | Página | O que muda |
|---|---|---|
| Login | `auth/pages/login.php` | e-mail + senha, `input[name=portal]=admin`, atalhos para os 5 portais, "Criar conta" |
| Login aluno | `login-student.php` | mesmo cartão, `portal=student`, rótulos do aluno (as outras: `login-teacher`, `login-parents`, `login-thirdparty`, `login-developer`) |
| Portal | `select-portal.php` | grade de portais + "Login Administrativo" |
| Entidade | `select-entity.php` | lista vinda de `GET api/v1/entities` (fixture no kit: `api/v1/entities`), busca por nome/código |
| MFA | `mfa-verify.php` | 6 caixas de código, Verificar, Reenviar código |
| Senha | `forgot-password.php` | e-mail + envio do link |
| Erro de login | `$loginError` (flash `login_error`) | alerta acima do formulário |
| Carregando | `setLoading()` em `auth.v2.js` | botão desabilitado com spinner |
| > 800px | — | cartão dividido |
| ≤ 800px | `ttsc.auth.css` | uma coluna, máx. 440px, marca escondida, `.sb-login-mobile-header` visível |
| ≤ 520px | `ttsc.auth.css` | margens de 12px |
| Tema | `data-theme` em `<html>` + `localStorage['od-theme']` (chave própria do auth; o app usa `ttsc-theme`) | |

No kit o banner de cookies (`consent-cookie.js`) vem marcado como aceito (`localStorage['ttsc_cookie_consent']='accepted_all'`); apague a chave para vê-lo. Observado no render atual: no tema escuro o botão "Entrar" fica escuro com borda clara (estilo de `ttsc.auth.css`).

## API

| Ponto (`assets/js/auth.v2.js`) | Efeito |
|---|---|
| `initLoginForm()` | intercepta `form#loginForm`, valida (`validateLoginForm()`), `POST {base}login` com `FormData`, `Accept: application/json` |
| resposta `{ mfa_required: true, user_id }` | esconde `#loginForm` (`.auth-hidden`) e mostra o formulário MFA (`#mfaUserId`) |
| `initMfaForm()` | `POST {base}api/v1/auth/mfa-verify` |
| `checkInstalledStatus()` | `GET {base}api/v1/installed` → `{success, installed}`; esconde `#installLink` se instalado |
| `initPasswordToggle()`, `initCpfMask()`, `initTabSwitching()` | mostrar senha, máscara de CPF, abas `.auth-tab` |
| `showFieldError(id, msg)` / `clearFieldError(id)` | erro por campo |
| `showToast(msg, tipo)` | toast em `#toast-container` |
| `toggleAuthTheme()` | alterna `data-theme` e grava `od-theme` |

## Acessibilidade

- Link "Ir para o conteúdo principal" é o primeiro foco; `main#main-content`.
- `h1` da marca no painel e `h2` do formulário; cada `input` com `label for` e `autocomplete` (`email`, `current-password`, `one-time-code` no MFA).
- Erros: texto no campo (`showFieldError`) + toast; não dependem só da borda vermelha.
- Botão de tema com `aria-label="Alternar tema de cores"`; ícones SVG com `aria-hidden` no painel da marca.
- Contraste: textos do formulário em `--sb-text`/`--sb-text-3` (ponte do `ttsc.auth.css`); link "Esqueceu a senha?" em verde de texto.

## Modelos

### HTML

```php
<?php
// resources/views/auth/pages/login-secretaria.php — nova variante de login
$this->layout('auth::layouts/main', [
    'title' => 'Entrar — Secretaria',
    'subtitle' => 'Acesso da secretaria escolar.',
]);
?>
<?php $this->start('content') ?>
<div class="sb-login-mobile-header">
  <svg width="32" height="32" viewBox="0 0 32 32" fill="none" aria-hidden="true"><rect width="32" height="32" rx="8"/></svg>
  <span class="sb-login-mobile-brand">TotusTuus</span>
</div>

<?php if (!empty($loginError)): ?>
<div class="sb-login-alert sb-login-alert--error" role="alert">
  <i class="fa-light fa-circle-exclamation" aria-hidden="true"></i>
  <span><?= $this->e($loginError) ?></span>
</div>
<?php endif; ?>

<div class="sb-login-form-header">
  <h2>Bem-vindo de volta</h2>
  <p>Entre com o e-mail institucional da secretaria</p>
</div>

<form method="POST" action="<?= url('/login') ?>" id="loginForm" novalidate>
  <?= csrf_field() ?>
  <input type="hidden" name="portal" value="admin">
  <div class="sb-field">
    <label for="email">Endereço de e-mail</label>
    <div class="sb-input-wrap">
      <i class="sb-input-icon fa-light fa-envelope" aria-hidden="true"></i>
      <input type="email" id="email" name="email" class="sb-input" placeholder="secretaria@colegio.edu.br" required autofocus autocomplete="email">
    </div>
  </div>
  <div class="sb-field">
    <div class="sb-field-label-row">
      <label for="password">Senha</label>
      <a href="<?= url('/forgot-password') ?>" class="sb-forgot-link">Esqueceu a senha?</a>
    </div>
    <div class="sb-input-wrap">
      <i class="sb-input-icon fa-light fa-lock" aria-hidden="true"></i>
      <input type="password" id="password" name="password" class="sb-input" placeholder="Digite sua senha" required autocomplete="current-password">
      <button type="button" class="sb-pw-toggle" id="pwToggle" aria-label="Alternar visibilidade da senha" tabindex="-1">
        <i class="fa-light fa-eye" aria-hidden="true"></i>
      </button>
    </div>
  </div>
  <button type="submit" id="submitBtn" class="sb-btn sb-btn-primary sb-btn-full"><span>Entrar</span></button>
</form>

<div class="sb-divider-text"><span>Acesso aos portais</span></div>
<div class="sb-portal-grid">
  <a href="<?= url('/login-student') ?>" class="sb-portal-btn"><i class="fa-light fa-graduation-cap" aria-hidden="true"></i> Aluno</a>
  <a href="<?= url('/login-parents') ?>" class="sb-portal-btn"><i class="fa-light fa-people-roof" aria-hidden="true"></i> Responsáveis</a>
</div>
<?php $this->stop() ?>
```

Rota (mesmo padrão de `routes/web.php`):

```php
$router->get('/login-secretaria', function ($request) {
    return view('auth::pages/login-secretaria', ['loginError' => session()->flash('login_error')]);
})->middleware(\App\Http\Middleware\GuestMiddleware::class);
```

### CSS

Ordem real no `<head>` do layout: `ttsc.css`, `ttsc.supabase.css`, `ttsc.auth.css`, `fonts/fontawesome.v7.2.0/css/all.css`, `ttsc.notifications.css`, `ttsc.rtl.css`, depois `section('styles')`. Extensão com tokens (alerta de bloqueio por tentativas):

```css
.sb-login-lockout {
  display: flex; gap: var(--ttsc-space-2); align-items: flex-start;
  padding: var(--ttsc-space-3) var(--ttsc-space-4); margin-bottom: var(--ttsc-space-4);
  border: 1px solid var(--ttsc-warning); border-radius: var(--ttsc-radius-control);
  background: color-mix(in srgb, var(--ttsc-warning) 10%, var(--ttsc-surface));
  color: var(--ttsc-warning-text); font-size: 13px;
}
.sb-login-lockout strong { color: var(--ttsc-text); }
```

### JS

Ordem real no fim do `<body>`: `toggleAuthTheme()` inline, `section('scripts')`, `ttsc.events.js`, `auth.v2.js`, `consent-cookie.js`.

```js
// Contagem regressiva do bloqueio (resposta 429 do POST /login com { locked_until })
(function () {
  var form = document.getElementById('loginForm');
  var btn = document.getElementById('submitBtn');
  if (!form || !btn) return;
  window.showLockout = function (lockedUntilIso) {
    var box = document.createElement('div');
    box.className = 'sb-login-lockout'; box.setAttribute('role', 'status');
    form.parentNode.insertBefore(box, form);
    btn.disabled = true;
    (function tick() {
      var s = Math.max(0, Math.round((new Date(lockedUntilIso) - Date.now()) / 1000));
      box.innerHTML = '<i class="fa-light fa-lock" aria-hidden="true"></i><span><strong>Acesso bloqueado.</strong> Tente novamente em ' +
        Math.floor(s / 60) + ' min ' + (s % 60) + ' s.</span>';
      if (s > 0) { setTimeout(tick, 1000); } else { box.remove(); btn.disabled = false; }
    })();
  };
})();
```

No kit há duas fixtures estáticas: `api/v1/installed` (`{"success":true,"installed":true}`, o mesmo de `SystemController::installed`) e `api/v1/entities` (3 instituições ilustrativas no formato de `EntityUnitController::entities`).

### SQL

Banco **master** (o `Auth` consulta o banco corrente e cai para o master). O PHP só devolve mensagens genéricas ao formulário.

```sql
-- 1) IP bloqueado manualmente (antes de tudo) — Auth::attempt()
SELECT 1 FROM rate_limits WHERE ip_address = :ip_address AND locked_until > NOW() LIMIT 1;

-- 2) Usuário pelo identificador (coluna escolhida por detectLoginType: email, cpf ou username)
SELECT uuid, name, email, type, status, mfa_enabled, mfa_default_method, failed_attempts, locked_until
  FROM users
 WHERE email = :identifier
   AND status = 'active'
   AND deleted_at IS NULL
 LIMIT 1;

-- 3) Falhas recentes do identificador (alerta e painel de segurança; janela de 15 min como o AlertEngine)
SELECT COUNT(*) AS failed_last_window
  FROM login_attempts
 WHERE identifier = :identifier
   AND status = 'failed'
   AND created_at > DATE_SUB(NOW(), INTERVAL :window_minutes MINUTE);

-- 4) Ao errar a senha: incrementa e bloqueia ao atingir max_login_attempts (5, config/security.php)
UPDATE users SET failed_attempts = :attempts, locked_until = :locked_until WHERE uuid = :user_uuid;
```

`isUserLocked()` compara `locked_until` com o relógio; no sucesso o `Auth` zera `failed_attempts` e grava `last_login`. A lista de instituições de `select-entity` vem de `TenantManager::getAccessibleTenants()` (consulta 1 do [StarterKitAppShell](../StarterKitAppShell/README.md#sql)). As divergências de esquema que existiam aqui foram corrigidas no repo (commit `a2b03b61a` fix(mail,auth,logging)): a migração `2026_10_22_000003` acrescentou `uuid` e `code` a `login_attempts`/`security_logs` (o `INSERT` de `Auth::recordFailedAttempt()` funciona) e a `2026_10_22_000002` criou `users.is_master_user`, usada no fallback do master.

## Como começar um projeto a partir do kit

1. **Arquivos do kit**: `kit.html` (login) e `kit-login-student.html`, `kit-select-portal.html`, `kit-select-entity.html`, `kit-mfa-verify.html`, `kit-forgot-password.html`; `assets/css/` (cópias reais de `ttsc.css`, `ttsc.supabase.css`, `ttsc.auth.css`, `ttsc.notifications.css`, `ttsc.rtl.css`), `assets/js/` (`ttsc.events.js`, `auth.v2.js`, `consent-cookie.js`), `assets/fa.css` (Font Awesome reduzido aos ícones usados) e `assets/media/` (logo e bandeiras). Gerados por `$SPD/dsh/gen_kits.py` a partir de `php $SPD/app/view_harness.php /login auth::pages/login …` (renderiza pelo `App\View\PlatesEngine` real).
2. **Nova tela de auth no repo**: view em `resources/views/auth/pages/`, rota com `GuestMiddleware` (ou `AuthMiddleware` para `select-entity`/`select-unit`), `$this->layout('auth::layouts/main', ['title' => …])`.
3. **Outro projeto**: copie `auth/layouts/main.php`, `app/partials/{locale_init,ttsc_format,language_selector}.php`, `components/xss-helper.php`, os 5 CSS e 3 JS acima, `fonts/fontawesome.v7.2.0/` e `media/app/favicon.svg`; o layout precisa dos helpers `asset()`, `url()`, `csrf_token()`, `CspNonce::get()`.
4. **HTML estático**: o `kit.html` já funciona sozinho (sem rede); troque os `href="#/login-…"` pelas rotas do novo projeto.

## Faça / Não faça

- **Faça:** uma página por variante em `auth/pages/`, sempre sobre `auth::layouts/main` — o painel da marca é único.
- **Faça:** mensagens genéricas ("e-mail ou senha inválidos") e o bloqueio no servidor (`locked_until`, `rate_limits`).
- **Faça:** `autocomplete` correto e `novalidate` + validação do `auth.v2.js` para mensagens em pt-BR.
- **Não faça:** carregar o shell (`app/layouts/main.php`) numa tela sem sessão.
- **Não faça:** gravar o tema do auth em `ttsc-theme` sem também ler `od-theme` — são chaves diferentes hoje.
