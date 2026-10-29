# PageAuth

Arquétipo das telas de acesso fora do shell: cartão dividido com o painel da marca à esquerda e o formulário à direita (`sb-login-*`), estilizado por `assets/css/ttsc.auth.css`, com alerta de erro, mostrar/ocultar senha, verificação humana e atalhos para os portais.

## Quando usar

- Toda tela antes da sessão: login (`/login` e as variantes `/login-developer`, `/login-student`, `/login-teacher`, `/login-parents`, `/login-thirdparty`), esqueci a senha, redefinir senha, verificar e-mail, MFA (setup/verify), cadastro, seleção de portal/unidade/entidade e confirmação de saída — todas em `resources/views/auth/pages/` sobre `auth::layouts/main`.
- Não use dentro do shell autenticado (lá é [PageModel](../PageModel/README.md) e os arquétipos de módulo) nem para modais de reautenticação.

### Regra de escolha (resumo)

Dashboard = home de módulo/portal · Records = lista de entidade (o padrão) · Pipeline = etapas reais · History = histórico/auditoria · Report = gráficos primeiro · Settings = configurações · Calendar = agenda · **Auth = qualquer tela sem sessão**. Mapa completo em [PageRecords](../PageRecords/README.md).

## Anatomia

```
                                                                     [[tema]] .auth-theme-toggle (fixo)
┌ .sb-login-page ───────────────────────────────────────────────────────────────┐
│ ┌ .sb-login-container (grid 1fr 1fr, máx. 1040px, raio 16px) ───────────────┐ │
│ │ .sb-login-brand               │ .sb-login-form > .sb-login-form-inner     │ │
│ │  [logo 48px]                  │  [!] .sb-login-alert--error               │ │
│ │  TotusTuus SoftCloud (h1)     │  Bem-vindo de volta (h2)                   │ │
│ │  tagline                      │  .sb-field  E-mail   [[@] seu@email.com   ] │ │
│ │  [v] 4 .sb-login-feature        │  .sb-field  Senha  Esqueceu?  [[cadeado] •••• [ver]] │ │
│ │                               │  [[ ] Não sou um robô]  (após 3 falhas)      │ │
│ │                               │  [ Entrar → ]  .sb-btn-primary.sb-btn-full │ │
│ │                               │  ── Acesso aos portais ──  .sb-divider-text│ │
│ │  © 2026 … (footer)            │  .sb-portal-grid (5 .sb-portal-btn)        │ │
│ │                               │  Não tem uma conta? Criar conta            │ │
│ └───────────────────────────────┴────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Página | `main#main-content.sb-login-page` (min-height 100vh, centraliza) | sim |
| Cartão | `.sb-login-container` | sim |
| Painel da marca | `.sb-login-brand` > `.sb-login-brand-content` (`.sb-login-logo`, `.sb-login-title`, `.sb-login-tagline`, `.sb-login-features > .sb-login-feature`, `.sb-login-footer-text`); some abaixo de 800 px | sim |
| Formulário | `.sb-login-form > .sb-login-form-inner` + `section('content')` da página | sim |
| Cabeçalho mobile | `.sb-login-mobile-header` + `.sb-login-mobile-brand` (só < 800 px) | sim |
| Alerta | `.sb-login-alert.sb-login-alert--error` (`$loginError`) | não |
| Campo | `.sb-field` > `label[for]` + `.sb-input-wrap` (`.sb-input-icon` + `input.sb-input` + `.sb-pw-toggle`) | sim |
| Linha do rótulo | `.sb-field-label-row` + `.sb-forgot-link` | não |
| Botão | `.sb-btn.sb-btn-primary.sb-btn-full` + `.sb-btn-arrow`; carregando: `.sb-spinner` | sim |
| Portais | `.sb-divider-text` + `.sb-portal-grid > a.sb-portal-btn` | login |
| Rodapé | `.sb-login-register` | login |
| Tema | `button#auth-theme-toggle.auth-theme-toggle` | sim |
| Verificação humana | bloco após 3 falhas (`captcha_after_attempts`); no preview, `.ttsc-captcha-placeholder` estático | condicional |

## Variantes

| Tela | View | Diferença |
|---|---|---|
| Login administrativo | `auth/pages/login.php` | `portal=admin`, grade de portais |
| Login por portal | `login-student.php`, `login-teacher.php`, `login-parents.php`, `login-thirdparty.php`, `login-developer.php` | `portal` fixo, texto do portal |
| Recuperação | `forgot-password.php`, `reset-password.php` | um campo + link de volta |
| MFA | `mfa-setup.php`, `mfa-verify.php` | código de 6 dígitos |
| Escolhas pós-login | `select-portal.php`, `select-unit.php`, `select-entity.php` | lista de opções |
| Tema | `<html data-theme="light|dark">` | tokens `--sb-*` trocam por `[data-theme="light"]` (escuro é o padrão de `:root`) |

## API

**Layout (`resources/views/auth/layouts/main.php`)**

| Item | Valor |
|---|---|
| `$this->layout('auth::layouts/main', ['title' => …, 'subtitle' => …])` | título da aba ("Entrar - TotusTuus SoftCloud") |
| `$this->section('content')` | conteúdo do formulário |
| `$this->section('styles')` / `section('scripts')` | extras por página |
| CSS | `ttsc.css`, `ttsc.supabase.css`, `ttsc.auth.css`, `fontawesome.v7.2.0/css/all.css`, `ttsc.notifications.css`, `ttsc.rtl.css` |
| JS | `ttsc.events.js`, `auth.v2.js`, `consent-cookie.js` + `js_i18n_bridge.php` |
| Tema | script anti-FOUC lê `localStorage['od-theme']` ou `prefers-color-scheme` e grava `data-theme`; `toggleAuthTheme()` alterna |

**Login (`resources/views/auth/pages/login.php` + `routes/web.php`)**

| Campo / rota | Valor |
|---|---|
| `GET /login` | `GuestMiddleware`; passa `loginError` (flash `login_error`) |
| `POST /login` | `email` (ou `username`/`cpf`), `password`, `remember`, `portal` (`admin`, `teacher`, `student`, `parents`, `thirdparty`, `developer`), `_token` (`csrf_field()`) |
| Sucesso | redireciona por portal: `/client/dashboard`, `/teacher/dashboard`, `/student/dashboard`, `/parents/dashboard`, `/thirdparty/dashboard`, `/developer/dashboard` |
| Falha | `recordFailedAttempt()` + `incrementFailedAttempts()`; volta para `/login` com `login_error` |
| Outras | `GET\|POST /forgot-password`, `GET\|POST /register`, `GET\|POST\|DELETE /logout` |

**Segurança (`app/Support/Auth.php`)**

| Configuração | Padrão |
|---|---|
| `max_login_attempts` | 5 (`AUTH_MAX_ATTEMPTS`) → `users.locked_until = agora + lockout_minutes` (30) |
| `max_login_attempts_per_ip` | 20; bloqueio manual em `rate_limits.locked_until` |
| `captcha_after_attempts` | 3 — a partir daí a verificação humana é exigida |
| `progressive_delay` | atraso base 30 s × 2, máx. 300 s |
| Tipo de identificador | e-mail (`FILTER_VALIDATE_EMAIL`), CPF (11 dígitos) ou usuário |

**JS da página**

| Elemento | Comportamento |
|---|---|
| `#pwToggle` | alterna `type=password/text` e troca o SVG `#pwEye` |
| `#loginForm` `submit` | desabilita `#submitBtn` e mostra `.sb-spinner` + "Entrando..." |
| `#auth-theme-toggle` | alterna `data-theme` e grava `od-theme` |

## Acessibilidade

- Link "Ir para o conteúdo principal" (`.sr-only-focusable`) antes de tudo; `main#main-content`.
- Rótulos com `for`; `autocomplete="email"` e `current-password`; `required` + `novalidate` (validação do servidor, mensagens no alerta).
- Alerta de erro deve ter `role="alert"` (a view real não tem — o preview adiciona).
- `#pwToggle` tem `aria-label`, mas `tabindex="-1"`: quem usa teclado não alcança o botão. Ao portar, remova o `tabindex` e use `aria-pressed`.
- O logo é `<img alt="TotusTuus Logo">`; ícones dos campos são decorativos.
- `@media (forced-colors: active)` em `ttsc.auth.css` mantém bordas e foco em alto contraste.
- Contraste: botão primário escuro `--sb-accent #3ecf8e` com texto `--sb-accent-on #0f0f0f` (9,6:1); claro `#059669` com texto branco (3,8:1 — aceitável só por ser texto de 15px semibold; prefira `#047857`, 5,5:1).

## Modelos

### HTML

1) Plates real (`resources/views/auth/pages/login.php`, trecho):

```php
<?php $this->layout('auth::layouts/main', ['title' => 'Entrar', 'subtitle' => 'Acesse o painel administrativo e os módulos de gestão.']) ?>
<?php $this->start('content') ?>
<?php if (!empty($loginError)): ?>
<div class="sb-login-alert sb-login-alert--error" role="alert">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
  <span><?= htmlspecialchars($loginError) ?></span>
</div>
<?php endif; ?>
<div class="sb-login-form-header"><h2>Bem-vindo de volta</h2><p>Entre na sua conta para continuar</p></div>
<form method="POST" action="<?= url('/login') ?>" id="loginForm" novalidate>
  <?= csrf_field() ?>
  <input type="hidden" name="portal" value="admin">
  <div class="sb-field">
    <label for="email">Endereço de e-mail</label>
    <div class="sb-input-wrap">
      <svg class="sb-input-icon" …></svg>
      <input type="email" id="email" name="email" class="sb-input" placeholder="seu@email.com" required autofocus autocomplete="email">
    </div>
  </div>
  <!-- senha com .sb-field-label-row, .sb-forgot-link e #pwToggle -->
  <?php if (($failedAttempts ?? 0) >= 3): ?>
  <div class="ttsc-captcha" data-captcha><!-- widget de verificação humana --></div>
  <?php endif; ?>
  <button type="submit" id="submitBtn" class="sb-btn sb-btn-primary sb-btn-full"><span>Entrar</span><svg class="sb-btn-arrow" …></svg></button>
</form>
<div class="sb-divider-text"><span>Acesso aos portais</span></div>
<div class="sb-portal-grid">
  <a href="<?= url('/login-developer') ?>" class="sb-portal-btn">…Desenvolvedor</a>
  <a href="<?= url('/login-student') ?>" class="sb-portal-btn">…Aluno</a>
  <!-- Professor, Responsáveis, Terceiros -->
</div>
<div class="sb-login-register"><span>Não tem uma conta?</span><a href="<?= url('/register') ?>">Criar conta</a></div>
<?php $this->end() ?>
```

A view real não renderiza captcha: o limite `captcha_after_attempts` existe na configuração do `Auth`, mas nenhum widget está ligado. O bloco condicional acima é onde ele entra.

2) HTML gerado (preview; painel da marca do layout + formulário):

```html
<main id="main-content" class="sb-login-page">
  <div class="sb-login-container">
    <div class="sb-login-brand">
      <div class="sb-login-brand-content">
        <div class="sb-login-logo"><img src="data:image/svg+xml;base64,…" alt="TotusTuus Logo" style="width:48px;height:48px;object-fit:contain"></div>
        <h1 class="sb-login-title">TotusTuus<br/>SoftCloud</h1>
        <p class="sb-login-tagline">Plataforma unificada de gestão para instituições de ensino. Segura, escalável e feita para o futuro.</p>
        <div class="sb-login-features">
          <div class="sb-login-feature"><svg …></svg><span>Criptografia de ponta a ponta</span></div>
          <!-- Autenticação multifator · Controle de acesso baseado em papéis · Monitoramento de atividade 24/7 -->
        </div>
        <div class="sb-login-footer-text">&copy; 2026 TotusTuus SoftCloud<br/><span>Todos os direitos reservados.</span></div>
      </div>
    </div>
    <div class="sb-login-form">
      <div class="sb-login-form-inner">
        <div class="sb-login-alert sb-login-alert--error" role="alert"><svg …></svg><span>E-mail ou senha inválidos. Após 3 tentativas a verificação humana é exigida.</span></div>
        <div class="sb-login-form-header"><h2>Bem-vindo de volta</h2><p>Entre na sua conta para continuar</p></div>
        <form method="POST" action="#" id="loginForm" novalidate>
          <div class="sb-field">
            <label for="email">Endereço de e-mail</label>
            <div class="sb-input-wrap"><svg class="sb-input-icon" …></svg><input type="email" id="email" name="email" class="sb-input" placeholder="seu@email.com" required autocomplete="email"></div>
          </div>
          <div class="ttsc-captcha-placeholder" data-captcha-placeholder>
            <label><input type="checkbox" id="captchaCheck" name="captcha_ack"> Não sou um robô</label>
            <small>Verificação humana<br>(placeholder do reCAPTCHA)</small>
          </div>
          <button type="submit" id="submitBtn" class="sb-btn sb-btn-primary sb-btn-full"><span>Entrar</span><svg class="sb-btn-arrow" …></svg></button>
        </form>
        <div class="sb-divider-text"><span>Acesso aos portais</span></div>
        <div class="sb-portal-grid"><a href="#" class="sb-portal-btn"><svg …></svg>Desenvolvedor</a>…</div>
        <div class="sb-login-register"><span>Não tem uma conta?</span><a href="#">Criar conta</a></div>
      </div>
    </div>
  </div>
</main>
```

### CSS

`assets/css/ttsc.auth.css` (copiado sem alteração para `vendor/app/auth/ttsc.auth.css`): tokens `--auth-*` e `--sb-*` em `:root` (escuro, padrão) e `[data-theme="light"]` (claro); `.sb-login-*`, `.sb-field`, `.sb-input`, `.sb-btn`, `.sb-portal-*`, `.auth-theme-toggle`, `.sb-spinner`, breakpoints de 800 px e 520 px e `forced-colors`. O tema é por **`data-theme`**, não por `html.dark`: por isso o preview não chama `TTSCModelKit.syncTheme()` — com `html.dark`, as regras escuras do shell (`.dark input`, botões) vazariam para o formulário, o que não acontece na tela real.

```css
/* Verificação humana (placeholder) com os tokens da própria tela de login */
.ttsc-captcha-placeholder {
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  padding: 10px 12px; margin: 0 0 16px; border: 1px dashed var(--sb-border-2); border-radius: 8px;
  background: var(--sb-surface-2); color: var(--sb-text-2); font-size: 13px;
}
.ttsc-captcha-placeholder input { width: 18px; height: 18px; accent-color: var(--sb-accent); }

/* Ponte para o design system: a tela de login segue os tokens TTSC */
.sb-login-page { --sb-accent: var(--ttsc-accent); --sb-accent-on: var(--ttsc-accent-on); --sb-border: var(--ttsc-border); }
```

### JS

```js
// Login com fetch (mesmo contrato do POST /login), captcha após 3 falhas e estado de carregamento
const form = document.getElementById('loginForm');
const btn = document.getElementById('submitBtn');
let failures = Number(sessionStorage.getItem('ttsc-login-failures') || 0);
const captcha = document.querySelector('[data-captcha-placeholder]');
captcha.hidden = failures < 3;

document.getElementById('pwToggle').addEventListener('click', () => {
  const input = document.getElementById('password');
  input.type = input.type === 'password' ? 'text' : 'password';
});

form.addEventListener('submit', async (ev) => {
  ev.preventDefault();
  if (!captcha.hidden && !document.getElementById('captchaCheck').checked) return;
  btn.disabled = true;
  btn.setAttribute('aria-busy', 'true');
  const res = await fetch('/login', { method: 'POST', body: new FormData(form), credentials: 'same-origin', redirect: 'follow' });
  if (res.redirected && !res.url.endsWith('/login')) { sessionStorage.removeItem('ttsc-login-failures'); location.href = res.url; return; }
  failures += 1;
  sessionStorage.setItem('ttsc-login-failures', String(failures));
  location.reload();                      // a view mostra $loginError do flash
});

document.getElementById('auth-theme-toggle').addEventListener('click', () => {
  const html = document.documentElement;
  const next = html.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
  html.setAttribute('data-theme', next);
  try { localStorage.setItem('od-theme', next); } catch (e) {}
});
```

### SQL

O que o `App\Support\Auth` executa no login (banco do tenant, com descoberta no master para developer):

```sql
-- Usuário pelo identificador (coluna escolhida por detectLoginType: email, cpf ou username)
SELECT uuid, name, email, type, access_level, password, password_algo, mfa_enabled, failed_attempts, locked_until
  FROM users
 WHERE email = :identifier AND status = 'active'
 LIMIT 1;

-- Conta bloqueada?
SELECT locked_until > NOW() AS bloqueada
  FROM users
 WHERE uuid = :user_uuid;

-- Falha: incrementa e bloqueia ao atingir max_login_attempts
UPDATE users
   SET locked_until = CASE WHEN failed_attempts + 1 >= 5 THEN NOW() + INTERVAL 30 MINUTE ELSE locked_until END,
       failed_attempts = failed_attempts + 1      -- depois do CASE: MySQL avalia o SET da esquerda para a direita
 WHERE uuid = :user_uuid;

-- Falha: registro da tentativa (colunas do esquema local)
INSERT INTO login_attempts (user_id, identifier, ip_address, user_agent, status, fail_reason, created_at)
VALUES (:user_uuid, :identifier, :ip, :user_agent, 'failed', 'invalid_password', NOW());

-- Exibir a verificação humana: falhas recentes do identificador ou do IP (captcha_after_attempts = 3)
SELECT COUNT(*) >= 3 AS exigir_captcha
  FROM login_attempts
 WHERE status = 'failed'
   AND (identifier = :identifier OR ip_address = :ip)
   AND created_at >= NOW() - INTERVAL 30 MINUTE;

-- Sucesso: zera o contador
UPDATE users SET failed_attempts = 0, locked_until = NULL, last_login = NOW() WHERE uuid = :user_uuid;
```

Divergência encontrada: `Auth::recordFailedAttempt()` grava `INSERT INTO login_attempts (uuid, code, identifier, ip_address, status, reason, created_at)`, mas a tabela local não tem `uuid`, `code` nem `reason` (tem `fail_reason`, `user_id`, `user_agent`). O `INSERT` acima segue o esquema real. A view recebe só `loginError` e, com o captcha ligado, `failedAttempts` = resultado da consulta de `exigir_captcha`.

## Faça / Não faça

- **Faça:** usar `auth::layouts/main` em toda tela sem sessão — painel da marca, tema e scripts vêm de lá.
- **Faça:** mensagens de erro genéricas ("E-mail ou senha inválidos"), sem dizer qual dos dois falhou.
- **Não faça:** carregar reCAPTCHA ou fontes de CDN no preview; na produção, o widget entra no bloco condicional após 3 falhas.
- **Não faça:** aplicar `html.dark` nas telas de acesso; o tema delas é `data-theme`.
