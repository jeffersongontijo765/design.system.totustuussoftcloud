# TogglePassword

Campo de senha com botão mostrar/ocultar (`[data-ttsc-toggle-password]` do ttscui), que alterna o `type` entre `password` e `text` e marca o container com `active`.

## Quando usar

- Login, troca de senha, criação de conta, cadastro de senha de integração (SMTP, gateway) — sempre que o usuário digita um segredo e precisa conferir.
- Códigos curtos de uso único → [PinInput](../PinInput/README.md).
- Exibir um segredo já salvo (token de API) → **não** mostre o valor; ofereça "Gerar novo" e exiba uma única vez com [Clipboard](../Clipboard/README.md).

## Anatomia

```
Senha atual
┌──────────────────────────────────┬──┐
│ ••••••••••                       │👁│    div.ttsc-input[data-ttsc-toggle-password]
└──────────────────────────────────┴──┘      input[type=password] + button[data-ttsc-toggle-password-trigger]
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Container | `div.ttsc-input[data-ttsc-toggle-password="true"]` | sim |
| Campo | primeiro `input` dentro do container (`type="password"`) | sim |
| Gatilho | `button[data-ttsc-toggle-password-trigger]` (atributo real no fonte: **`-trigger`**, não `-toggle`) | sim |
| Ícones | dois `<i>`: `.ttsc-tp-show` (fa-eye) e `.ttsc-tp-hide` (fa-eye-slash), trocados por CSS via `.active` | recomendado |
| Permanente | `data-ttsc-toggle-password-permanent="true"` | não |

## Estados

| Estado | Marcação resultante |
|---|---|
| Oculto (padrão) | `input[type=password]`; container sem `active` |
| Visível | `input[type=text]`; container com classe `active` |
| Digitar com senha visível | `permanent=false` (padrão): **volta a ocultar** ao digitar; `permanent=true`: continua visível |
| Inválido | `aria-invalid="true"` no `input` interno (o anel aparece no container via `:has`) |
| Desabilitado | `disabled` no input **e** no botão |

## API

Conferido em `src/components/toggle-password/toggle-password.ts` (global `ttscTogglePassword` / `TTSC.TogglePassword`).

| Opção | Padrão | Descrição |
|---|---|---|
| `data-ttsc-toggle-password-permanent` | `false` | `false` = ao digitar com a senha visível, ela volta a ser ocultada |

| Método | Descrição |
|---|---|
| `ttscTogglePassword.getInstance(el)` / `getOrCreateInstance(el)` | instância do container |
| `instance.toggle()` | alterna (dispara eventos) |
| `instance.setVisible(true \| false)` | define direto (sem eventos, sem mexer em `active`) |
| `instance.isVisible()` | `true` quando `type="text"` |

| Evento | Quando | Cancelável |
|---|---|---|
| `toggle` (DOM no container, sem prefixo; e `instance.on('toggle')`) | antes de alternar | sim: `event.detail.payload.cancel = true` |
| `toggled` | depois de alternar | não |

## Acessibilidade

- Gatilho é `<button type="button">` com `aria-label="Mostrar senha"` e `aria-pressed` refletindo o estado (JS abaixo); troque o rótulo para "Ocultar senha".
- `autocomplete="current-password"` no login e `new-password` na troca — gerenciadores de senha dependem disso.
- Nunca use `placeholder` como única instrução da política de senha; liste os requisitos em `.ttsc-form-description`.
- Ícone `fa-eye` em `ttsc-text-muted` (≥ 4,5:1) — é o único conteúdo do botão, então o `aria-label` é obrigatório.

## Modelos

### HTML

```html
<!-- resources/views/auth/login.php -->
<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="login-password">Senha</label>
  <div class="ttsc-input ttsc-input-lg" data-ttsc-toggle-password="true">
    <input type="password" id="login-password" name="password" autocomplete="current-password" required>
    <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm -me-1.5"
            data-ttsc-toggle-password-trigger aria-label="Mostrar senha" aria-pressed="false">
      <i class="fa-light fa-eye ttsc-tp-show" aria-hidden="true"></i>
      <i class="fa-light fa-eye-slash ttsc-tp-hide" aria-hidden="true"></i>
    </button>
  </div>
</div>

<!-- Troca de senha: nova senha permanece visível enquanto digita -->
<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="new-password">Nova senha</label>
  <div class="ttsc-input" data-ttsc-toggle-password="true" data-ttsc-toggle-password-permanent="true">
    <input type="password" id="new-password" name="new_password" autocomplete="new-password"
           minlength="12" required aria-describedby="new-password-rules">
    <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm -me-1.5"
            data-ttsc-toggle-password-trigger aria-label="Mostrar senha" aria-pressed="false">
      <i class="fa-light fa-eye ttsc-tp-show" aria-hidden="true"></i>
      <i class="fa-light fa-eye-slash ttsc-tp-hide" aria-hidden="true"></i>
    </button>
  </div>
  <p class="ttsc-form-description" id="new-password-rules">Mínimo de 12 caracteres, com letra maiúscula, número e símbolo.</p>
</div>
```

### CSS

```css
/* Extensão do chassi: troca de ícone pela classe .active que o ttscui põe no container
   (o KTUI original usa a variante kt-toggle-password-active:, que não existe no bundle) */
[data-ttsc-toggle-password] .ttsc-tp-hide { display: none; }
[data-ttsc-toggle-password].active .ttsc-tp-show { display: none; }
[data-ttsc-toggle-password].active .ttsc-tp-hide { display: inline-block; }

/* Botão dentro do campo sem fundo próprio */
[data-ttsc-toggle-password] [data-ttsc-toggle-password-trigger] { color: var(--ttsc-text-muted); }
[data-ttsc-toggle-password] [data-ttsc-toggle-password-trigger]:hover { color: var(--ttsc-text); }

/* Erro no input interno pinta o container */
.ttsc-input:has(input[aria-invalid="true"]) { border-color: var(--ttsc-danger); }
```

### JS

```js
// Mantém aria-label/aria-pressed coerentes e esconde a senha ao sair da página
TTSC.init();
document.querySelectorAll('[data-ttsc-toggle-password]').forEach((container) => {
  const trigger = container.querySelector('[data-ttsc-toggle-password-trigger]');
  const sync = () => {
    const visible = container.classList.contains('active');
    trigger.setAttribute('aria-pressed', String(visible));
    trigger.setAttribute('aria-label', visible ? 'Ocultar senha' : 'Mostrar senha');
  };
  container.addEventListener('toggled', sync);

  // Exemplo de cancelamento: não revelar em campo desabilitado
  container.addEventListener('toggle', (event) => {
    if (container.querySelector('input').disabled) event.detail.payload.cancel = true;
  });
});

// Ao enviar, volta tudo para type=password (evita que o navegador salve o campo como texto)
document.addEventListener('submit', (event) => {
  event.target.querySelectorAll('[data-ttsc-toggle-password]').forEach((el) => {
    ttscTogglePassword.getInstance(el)?.setVisible(false);
    el.classList.remove('active');
  });
});
```

### SQL

`users.password` (banco master) guarda **somente o hash**: `PasswordManager` aplica `hash_hmac('sha256', $senha, $pepper)` e depois `password_hash(..., PASSWORD_ARGON2ID)`; `password_algo` (ex. `argon2id-v19`) e `password_pepper_kid` registram como o hash foi feito para rotação. A verificação é sempre no servidor com `password_verify()`; o hash **nunca** sai do PHP.

```sql
-- Login: busca o hash para verificar no PHP (nunca vai para view/JSON)
SELECT u.uuid, u.password, u.password_algo, u.password_pepper_kid, u.status, u.locked_until
  FROM users u
 WHERE u.email = :email
   AND u.deleted_at IS NULL
 LIMIT 1;

-- Troca de senha: grava o novo hash gerado no PHP (:hash = password_hash(hmac(senha, pepper), PASSWORD_ARGON2ID))
UPDATE users
   SET password = :hash,
       password_algo = 'argon2id-v19',
       password_pepper_kid = :pepper_kid,
       password_changed_at = NOW(),
       password_updated_at = NOW()
 WHERE uuid = :user_uuid
   AND deleted_at IS NULL;

-- Tela "Segurança da conta": o front só recebe metadados, jamais a coluna password
SELECT u.password_changed_at, u.mfa_enabled
  FROM users u
 WHERE u.uuid = :user_uuid
   AND u.deleted_at IS NULL;
```

A view de troca de senha nunca preenche `value` do campo. Falha de login responde a mesma mensagem para e-mail inexistente e senha errada, e incrementa `failed_attempts`.

## Faça / Não faça

- **Faça:** `autocomplete` correto; `permanent="true"` só na criação/troca de senha.
- **Faça:** voltar para `type=password` no submit; `aria-pressed` + rótulo que muda.
- **Não faça:** `SELECT password` em consulta que alimenta tela/JSON; preencher o campo com a senha salva; usar `-toggle` como nome do atributo do botão (o ttscui procura `-trigger`).
