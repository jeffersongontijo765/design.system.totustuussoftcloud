# Recaptcha

Integração do Google reCAPTCHA (v2 checkbox e v3 invisível) no login e em formulários públicos, exibido só após tentativas suspeitas e sempre verificado no servidor (`siteverify`), com a secret fora do front-end.

## Quando usar

- Login depois de N falhas (`captcha_after_attempts`, padrão **3** em `App\Support\Auth`), recuperação de senha, formulários públicos (pré-matrícula, contato, portal de suporte).
- v2 checkbox quando o usuário deve **ver** a verificação (após falhas); v3 invisível em formulários públicos de baixo atrito, com decisão por *score*.
- **Não use** em telas autenticadas internas (CRUD, dashboards): a sessão, o CSRF e o `RateLimiter` já protegem.
- **Não use** como única defesa: o bloqueio por `users.locked_until` e o rate limit por IP continuam valendo.

> O preview é uma **réplica estática** do widget: o script do Google (`https://www.google.com/recaptcha/api.js`) não carrega neste sistema. O widget real é um iframe de 304×78 px com tema `light`/`dark` próprio; o código JS abaixo é o da integração real.

## Anatomia

```
┌──────────────────────────────────────────┐
│ [ ]  Não sou um robô          (logo)     │   div#recaptcha (iframe do Google no app)
│                          Privacidade-Termos│
└──────────────────────────────────────────┘
 mensagem de erro (aria-live)                  .rc-err  → ttsc-danger-text
 input[name=g-recaptcha-response] (hidden)     token preenchido pelo callback
 [ Entrar ]  desabilitado até o callback       .ttsc-btn-primary
```

| Parte | Elemento | Obrigatório |
|---|---|---|
| Container do widget | `<div id="recaptcha" data-sitekey="…">` | sim (v2) |
| Token | `input[type=hidden][name=g-recaptcha-response]` (o v2 cria sozinho dentro do form) | sim |
| Erro | `.rc-err[aria-live=assertive]` | sim |
| Aviso de contexto | `.rc-alert` (“Detectamos 3 tentativas…”) | recomendado |
| Selo v3 | texto “protegido por reCAPTCHA · Privacidade · Termos” quando o selo flutuante é ocultado | sim (v3, exigência do Google) |

## Estados

| Estado | Origem (v2) | Visual no TTSC | Tokens |
|---|---|---|---|
| Não verificado | render | botão Entrar desabilitado | — |
| Verificando | clique | spinner no widget | — (iframe) |
| Verificado | `callback(token)` | botão habilitado | — |
| Expirado (2 min) | `expired-callback` | mensagem de erro, botão desabilitado | `ttsc-danger-text` |
| Erro de rede | `error-callback` | “Não foi possível carregar a verificação. Recarregue a página.” | `ttsc-danger-text` |
| Recusado no servidor | `siteverify` → `success:false` ou score baixo | erro 422 no formulário + `grecaptcha.reset()` | `ttsc-danger-text` |

## API

`grecaptcha` (script `api.js?render=explicit&hl=pt-BR` para v2, `api.js?render=SITE_KEY` para v3):

| Chamada | Descrição |
|---|---|
| `grecaptcha.ready(fn)` | Executa quando a API carregou |
| `grecaptcha.render(el, { sitekey, theme, size, callback, 'expired-callback', 'error-callback' })` | Renderiza o v2 e devolve `widgetId`; `theme: 'light' \| 'dark'` (ler `data-theme` do `<html>`), `size: 'normal' \| 'compact'` |
| `grecaptcha.getResponse(widgetId)` | Token atual (string vazia se não verificado) |
| `grecaptcha.reset(widgetId)` | Limpa — obrigatório após erro do servidor (o token é de uso único) |
| `grecaptcha.execute(SITE_KEY, { action: 'login' })` | v3: devolve `Promise<token>`; `action` só com `[A-Za-z/_]` |

Servidor — `POST https://www.google.com/recaptcha/api/siteverify` (form-urlencoded):

| Campo enviado | Resposta |
|---|---|
| `secret` (do `.env`, `RECAPTCHA_SECRET`) | `success` (bool) |
| `response` (token do cliente) | `challenge_ts`, `hostname` |
| `remoteip` (opcional, `ClientIp::get()`) | v3: `score` (0.0–1.0), `action`; `error-codes` |

Regras: confira `success`, `hostname` igual ao domínio do tenant, e no v3 `action` igual à esperada e `score >= 0.5` (configurável). Timeout curto (5 s); se o Google não responder, trate como falha **sem** liberar o login.

## Acessibilidade

- O desafio de imagens do v2 tem alternativa de áudio fornecida pelo Google; não esconda o iframe nem limite sua altura.
- `hl=pt-BR` no script para textos em português.
- Erros em texto (`aria-live="assertive"`), não só a borda; o botão desabilitado tem motivo visível no aviso acima do e-mail.
- Tema: passe `theme: 'dark'` quando `data-theme="dark"`, senão o widget claro fica isolado na tela escura.
- No v3, se ocultar o selo flutuante (`.grecaptcha-badge { visibility: hidden }`), o texto de atribuição tem de aparecer no formulário.

## Modelos

### HTML

```html
<?php if ($captchaRequired): ?>
  <div class="rc-alert" role="status">
    <i class="fa-light fa-triangle-exclamation"></i>
    <span>Detectamos <?= (int) $recentFailures ?> tentativas sem sucesso. Confirme que você não é um robô para continuar.</span>
  </div>
  <div id="recaptcha" data-sitekey="<?= $this->e($recaptchaSiteKey) ?>"></div>
  <div class="rc-err" id="rc-err" aria-live="assertive"></div>
  <script src="https://www.google.com/recaptcha/api.js?render=explicit&hl=pt-BR" async defer></script>
<?php endif; ?>
<button type="submit" class="ttsc-btn ttsc-btn-primary" id="btn-login" <?= $captchaRequired ? 'disabled' : '' ?>>
  <i class="fa-light fa-right-to-bracket"></i> Entrar
</button>

<!-- v3 (formulário público de pré-matrícula) -->
<input type="hidden" name="g-recaptcha-response" id="rc-token">
<p class="ds-note">Protegido por reCAPTCHA · <a class="ttsc-link" href="https://policies.google.com/privacy">Privacidade</a> ·
  <a class="ttsc-link" href="https://policies.google.com/terms">Termos</a></p>
```

### CSS

```css
/* O widget é um iframe: só o entorno é tematizável */
#recaptcha { min-height: 78px; }                          /* evita salto de layout ao carregar */
.rc-err { min-height: 16px; font-size: 12px; color: var(--ttsc-danger-text); }
.rc-alert { display: flex; gap: 8px; padding: 8px 10px; font-size: 12px; border-radius: var(--ttsc-radius-sm);
  background: var(--ttsc-canvas-2); border: 1px solid var(--ttsc-border); color: var(--ttsc-text-2); }
.rc-alert i { color: var(--ttsc-warning-text); }
/* v3: selo substituído pelo texto de atribuição no formulário */
.grecaptcha-badge { visibility: hidden; }
@media (max-width: 360px) { #recaptcha { transform: scale(.9); transform-origin: 0 0; } }
```

### JS

```js
// assets/js/core/ttsc.recaptcha.js — carregado só quando a view renderiza o widget
window.ttscRecaptchaV2 = function initRecaptchaV2() {
  const el = document.getElementById('recaptcha');
  if (!el || !window.grecaptcha) return;
  const submit = document.getElementById('btn-login');
  const err = document.getElementById('rc-err');
  const theme = document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';

  grecaptcha.ready(() => {
    const widgetId = grecaptcha.render(el, {
      sitekey: el.dataset.sitekey,
      theme,
      callback: () => { submit.disabled = false; err.textContent = ''; },
      'expired-callback': () => { submit.disabled = true; err.textContent = 'Verificação expirada. Marque a caixa de seleção novamente.'; },
      'error-callback': () => { submit.disabled = true; err.textContent = 'Não foi possível carregar a verificação. Recarregue a página.'; },
    });

    el.closest('form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const form = e.target;
      const res = await fetch(form.action, { method: 'POST', body: new FormData(form) }); // inclui g-recaptcha-response
      if (res.status === 422) {                                 // captcha recusado no servidor
        grecaptcha.reset(widgetId);                             // token é de uso único
        submit.disabled = true;
        err.textContent = 'Verificação recusada. Tente novamente.';
        return;
      }
      if (res.redirected) window.location.href = res.url;
    });
  });
};
document.addEventListener('DOMContentLoaded', () => {
  // api.js é async: espera o objeto existir
  const wait = setInterval(() => { if (window.grecaptcha && grecaptcha.render) { clearInterval(wait); ttscRecaptchaV2(); } }, 100);
  setTimeout(() => clearInterval(wait), 10000);
});

// v3 invisível: gera o token no envio (expira em 2 min, não gere no load)
export async function withRecaptchaV3(form, siteKey, action = 'pre_enrollment') {
  const token = await new Promise((resolve) => grecaptcha.ready(() => grecaptcha.execute(siteKey, { action }).then(resolve)));
  form.querySelector('#rc-token').value = token;
  return fetch(form.action, { method: 'POST', body: new FormData(form) });
}
```

Servidor (PHP) — a secret só existe aqui:

```php
// App\Security\RecaptchaVerifier::verify(string $token, string $expectedAction = null): bool
$ch = curl_init('https://www.google.com/recaptcha/api/siteverify');
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => http_build_query([
        'secret'   => env('RECAPTCHA_SECRET'),          // nunca na view, no JS ou no banco do tenant
        'response' => $token,
        'remoteip' => \App\Security\ClientIp::get(),
    ]),
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 5,
]);
$data = json_decode((string) curl_exec($ch), true) ?: [];
$ok = ($data['success'] ?? false) === true
   && ($data['hostname'] ?? '') === $_SERVER['HTTP_HOST']
   && ($expectedAction === null || (($data['action'] ?? '') === $expectedAction && ($data['score'] ?? 0) >= 0.5));
```

### SQL

```sql
-- Banco master. Mostrar o captcha? (falhas recentes por identificador OU por IP) — MariaDB 10.11 / MySQL 8
SELECT COUNT(*)      AS recent_failures,
       COUNT(*) >= 3 AS captcha_required          -- captcha_after_attempts
  FROM login_attempts la
 WHERE la.status = 'failed'
   AND (la.identifier = :identifier OR la.ip_address = :ip_address)
   AND la.created_at >= NOW() - INTERVAL 30 MINUTE;

-- Conta bloqueada? (Auth incrementa users.failed_attempts e grava locked_until na 5ª falha)
SELECT u.failed_attempts, u.locked_until,
       (u.locked_until IS NOT NULL AND u.locked_until > NOW()) AS is_locked
  FROM users u
 WHERE u.email = :email AND u.deleted_at IS NULL;

-- Captcha recusado também conta como tentativa
INSERT INTO login_attempts (user_id, identifier, ip_address, user_agent, status, fail_reason, created_at)
VALUES (:user_id, :identifier, :ip_address, :user_agent, 'failed', 'captcha_invalid', NOW());
```

O controller de login roda a primeira consulta antes de renderizar a view e passa `$captchaRequired`/`$recentFailures`; no POST, valida o token (`RecaptchaVerifier`) **antes** de conferir a senha. Com `is_locked = 1`, nem o captcha libera: a tela mostra o horário de `locked_until`. (`users.login_attempts` existe no esquema, mas o `Auth` usa `failed_attempts`.)

## Faça / Não faça

- **Faça:** exibir o captcha só após falhas (ou em formulários públicos) e verificar no servidor toda vez.
- **Faça:** `grecaptcha.reset()` após qualquer recusa do servidor; tema conforme `data-theme`.
- **Faça:** registrar a recusa em `login_attempts` (`fail_reason = 'captcha_invalid'`).
- **Não faça:** expor a secret (view, JS, `settings` do tenant, logs) nem confiar só em `getResponse()` no cliente.
- **Não faça:** gerar o token v3 no carregamento da página (expira em 2 minutos) nem usar o captcha no lugar do bloqueio por `locked_until`.
