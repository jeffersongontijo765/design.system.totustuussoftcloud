# PinInput

Campo segmentado para códigos curtos (`[data-ttsc-pin-input]` do ttscui): uma célula por caractere, avanço automático, colar distribuído e valor consolidado num `input hidden`.

## Quando usar

- Código MFA de 6 dígitos (e-mail/TOTP) na tela de verificação do login, código de confirmação de e-mail, PIN de 4 dígitos do totem de frequência.
- Códigos alfanuméricos curtos e de tamanho fixo (`availableChars: "[0-9A-Z]"`), ex.: código de validação de documento.
- Texto livre ou tamanho variável → [Input](../Input/README.md). Senha → [TogglePassword](../TogglePassword/README.md).

## Anatomia

```
┌───┐┌───┐┌───┐  ┌───┐┌───┐┌───┐
│ 4 ││ 8 ││ 1 │ ·│ 9 ││   ││   │      div[data-ttsc-pin-input]
└───┘└───┘└───┘  └───┘└───┘└───┘        input.ttsc-input[data-ttsc-pin-input-item] × N
<input type="hidden" name="mfa_code" data-ttsc-pin-input-hidden>   (criado pelo JS se faltar)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Container | `div[data-ttsc-pin-input="true"]` (+ `flex gap-2`) | sim |
| Célula | `input.ttsc-input[data-ttsc-pin-input-item]` — o JS força `maxlength=1` | sim (≥ 1) |
| Nome do campo | `data-ttsc-pin-input-name="mfa_code"` → cria/usa `input[type=hidden][data-ttsc-pin-input-hidden]` | recomendado |
| Caracteres aceitos | `data-ttsc-pin-input-available-chars="[0-9]"` (regex de **um** caractere) | não (padrão `[0-9]`) |
| Inicialização adiada | `data-ttsc-pin-input-lazy="true"` (ignorado por `TTSC.init()`) | não |
| Separador visual | qualquer elemento sem `-item` entre as células | não |

## Estados

| Estado | Como aplicar | Visual |
|---|---|---|
| Vazio / preenchendo | automático | foco anda para a próxima célula habilitada |
| Completo | evento `ttsc.pin-input.complete` | (extensão) borda `ttsc-accent-border` |
| Inválido (código errado) | `aria-invalid="true"` em cada célula | borda/anel `ttsc-danger` + `.ttsc-form-message` |
| Desabilitado | `disabled` na célula (é pulada e não entra no valor) | opacidade 0,6 |
| Verificando | `aria-busy="true"` no container + células `readonly` | — |

## API

Conferido em `src/components/pin-input/pin-input.ts` (global `ttscPinInput` / `TTSC.PinInput`).

| Opção (`data-ttsc-pin-input-*`) | Padrão | Efeito |
|---|---|---|
| `name` | `""` | nome do `input hidden` que recebe o valor concatenado |
| `available-chars` | `"[0-9]"` | `RegExp` testada por caractere (inválida → volta para `[0-9]`) |
| `lazy` | `false` | `true` = não inicializa em `TTSC.init()`; crie com `getOrCreateInstance` |

| Método | Retorno |
|---|---|
| `ttscPinInput.getInstance(el)` / `getOrCreateInstance(el, config?)` | instância ou `null` (sem células) |
| `ttscPinInput.createInstances()` / `init()` | inicializa todos os `[data-ttsc-pin-input]` não-lazy |
| `instance.getValue()` | string com o valor das células habilitadas |
| `instance.setValue("481920")` | filtra pelos caracteres aceitos, preenche e emite eventos |
| `instance.on('input', fn)` / `off('input', id)` | callback com o payload |
| `instance.dispose()` | remove listeners e o vínculo |

| Evento DOM (bubbles, em `[data-ttsc-pin-input]`) | `event.detail.payload` |
|---|---|
| `ttsc.pin-input.input` e `ttsc.pin-input.change` | `{ value, complete, cellCount, filledCount, cellIndex }` |
| `ttsc.pin-input.complete` | idem — disparado **uma vez** ao completar (de novo só se ficar incompleto e completar) |

Teclado tratado pelo módulo: dígito válido preenche e avança; inválido é bloqueado; `Backspace` apaga a célula ou volta; `←`/`→`, `Home`/`End` navegam; colar ("481 920") filtra e distribui a partir da célula atual.

## Acessibilidade

- Envolva com `role="group"` + `aria-labelledby` (rótulo "Código de verificação") e dê a cada célula `aria-label="Dígito 1 de 6"`.
- `inputmode="numeric"` e `autocomplete="one-time-code"` **na primeira célula** (o iOS/Android sugere o código do SMS/e-mail e o colar distribui).
- Erro anunciado por `.ttsc-form-message` com `role="alert"`; não apague as células sem avisar.
- Células usam `ttsc-input`: texto `ttsc-text` sobre `ttsc-surface` (≥ 15:1).

## Modelos

### HTML

```html
<!-- resources/views/auth/mfa-verify.php -->
<form method="post" action="/auth/mfa/verify" id="form-mfa" class="flex flex-col gap-4">
  <input type="hidden" name="_token" value="<?= csrf_token() ?>">
  <div class="ttsc-form-item">
    <span class="ttsc-form-label" id="mfa-label">Código de verificação</span>
    <p class="ttsc-form-description">Enviamos 6 dígitos para <?= $this->e($maskedEmail) ?> (válido por 10 minutos).</p>
    <div class="flex items-center gap-2" role="group" aria-labelledby="mfa-label"
         data-ttsc-pin-input="true" data-ttsc-pin-input-name="mfa_code"
         data-ttsc-pin-input-available-chars="[0-9]">
      <?php for ($i = 1; $i <= 6; $i++): ?>
        <?php if ($i === 4): ?><span class="text-muted-foreground" aria-hidden="true">–</span><?php endif; ?>
        <input class="ttsc-input ttsc-input-lg ttsc-pin-cell" data-ttsc-pin-input-item
               inputmode="numeric" <?= $i === 1 ? 'autocomplete="one-time-code" autofocus' : 'autocomplete="off"' ?>
               aria-label="Dígito <?= $i ?> de 6">
      <?php endfor; ?>
    </div>
    <div class="ttsc-form-message" role="alert">Código inválido ou expirado.</div>
  </div>
  <button type="submit" class="ttsc-btn ttsc-btn-primary ttsc-btn-lg" disabled>Verificar</button>
</form>
```

### CSS

```css
/* Extensão do chassi: células quadradas e centralizadas */
.ttsc-pin-cell {
  width: 44px; padding: 0; text-align: center;
  font-size: 18px; font-weight: 600; font-variant-numeric: tabular-nums;
}
/* Completo: realça todas as células */
[data-ttsc-pin-input].is-complete .ttsc-pin-cell { border-color: var(--ttsc-accent-border); }
/* Verificando */
[data-ttsc-pin-input][aria-busy="true"] .ttsc-pin-cell { background: var(--ttsc-canvas-2); color: var(--ttsc-text-2); }
```

### JS

```js
// assets/js/auth/ttsc.mfa-verify.js — envia ao completar, trata erro e limpa
const form = document.getElementById('form-mfa');
const group = form.querySelector('[data-ttsc-pin-input]');
const submit = form.querySelector('[type="submit"]');
TTSC.init();
const pin = ttscPinInput.getOrCreateInstance(group);

function setInvalid(invalid) {
  group.querySelectorAll('[data-ttsc-pin-input-item]').forEach((cell) =>
    cell.setAttribute('aria-invalid', invalid ? 'true' : 'false'));
}

group.addEventListener('ttsc.pin-input.change', (event) => {
  const { complete } = event.detail.payload;
  group.classList.toggle('is-complete', complete);
  submit.disabled = !complete;
  setInvalid(false);
});

group.addEventListener('ttsc.pin-input.complete', async () => {
  group.setAttribute('aria-busy', 'true');
  const res = await fetch(form.action, {
    method: 'POST',
    body: new FormData(form), // inclui mfa_code (hidden) e _token
    headers: { Accept: 'application/json' },
  });
  group.removeAttribute('aria-busy');
  if (res.ok) { window.location.assign((await res.json()).redirect || '/'); return; }
  setInvalid(true);
  pin.setValue('');
  group.querySelector('[data-ttsc-pin-input-item]').focus();
});
```

### SQL

O código **nunca** é guardado em claro: o servidor gera 6 dígitos com `random_int`, grava `hash_hmac('sha256', $code, $key)` em `mfa_sessions.code_hash` (banco master) e envia o código por e-mail. Na verificação:

```sql
-- 1) Usuário precisa de MFA? (totustuus_master)
SELECT u.uuid, u.mfa_enabled, u.mfa_default_method
  FROM users u
 WHERE u.uuid = :user_uuid
   AND u.deleted_at IS NULL;

-- 2) Sessão de MFA pendente e válida; o PHP compara com hash_equals(code_hash, hmac(:mfa_code))
SELECT s.id, s.code_hash, s.type, s.expires_at
  FROM mfa_sessions s
 WHERE s.user_id = :user_uuid
   AND s.session_id = :session_id
   AND s.verified = 0
   AND s.expires_at > NOW()
 ORDER BY s.created_at DESC
 LIMIT 1;

-- 3) Sucesso: consome a sessão (uso único)
UPDATE mfa_sessions
   SET verified = 1, verified_at = NOW()
 WHERE id = :mfa_session_id
   AND verified = 0;
```

Para confirmação de e-mail o fluxo é o mesmo com `email_verifications` (`token`, `used = 0`, `expires_at > NOW()`, depois `used = 1, used_at = NOW()`). Erro devolve 422 JSON; o JS marca `aria-invalid` e limpa as células. Limite de tentativas por usuário em `mfa_attempts`.

## Faça / Não faça

- **Faça:** `data-ttsc-pin-input-name` para enviar um único campo; `autocomplete="one-time-code"` na primeira célula.
- **Faça:** comparar com `hash_equals` no servidor e consumir a sessão após o uso.
- **Não faça:** `name` em cada célula (o servidor receberia 6 campos); guardar o código em claro; enviar automaticamente sem estado visual de "verificando".
