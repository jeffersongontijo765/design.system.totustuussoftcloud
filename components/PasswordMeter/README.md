# PasswordMeter

Medidor de força de senha (implementação TTSC, JS puro): 4 barras, rótulo de força e checklist dos critérios da política do sistema — comprimento, maiúscula, minúscula, número e símbolo.

## Quando usar

- Telas de criação e troca de senha: primeiro acesso, “Alterar senha” no perfil, redefinição por token, expiração da senha.
- Sempre que a política do servidor (`App\Support\Auth::validatePassword`) puder recusar a senha — o medidor mostra **antes** do POST o que falta.
- **Não use** no login (não dê pistas sobre a senha digitada) nem em campos de PIN/código: use o [Pin Input](../PinInput/README.md).
- Para validar o formulário inteiro, combine com [FormValidation](../FormValidation/README.md) (validador `callback` usando `isValid()`).

## Anatomia

```
Nova senha
[ ••••••••••••••              (olho) ]   input[type=password] + botão mostrar/ocultar
▬▬▬▬ ▬▬▬▬ ▬▬▬▬ ────                       .ttsc-pm-bars (4 barras, data-score 0–4)
Força: Boa · faltam 1 critério(s)        .ttsc-pm-label (aria-live)
✓ Pelo menos 8 caracteres   ✓ Uma letra maiúscula
✓ Uma letra minúscula       ✓ Um número            .ttsc-pm-rules
○ Um símbolo (!@#$…)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Campo | `input[type=password][autocomplete=new-password]` com `aria-describedby` → rótulo e regras | sim |
| Medidor | `.ttsc-password-meter[data-ttsc-password-meter="#id-do-input"]` | sim |
| Barras | `.ttsc-pm-bars` com 4 `<span>` (`aria-hidden`) | sim |
| Rótulo | `.ttsc-pm-label[aria-live=polite]` | sim |
| Critérios | `ul.ttsc-pm-rules` (preenchida pelo JS) | recomendado |
| Mostrar senha | `button.ttsc-btn-ghost.ttsc-btn-icon[aria-pressed]` (ou [TogglePassword](../TogglePassword/README.md) do ttscui) | recomendado |

## Variantes

| `data-score` | Rótulo | Barras | Tokens (barra / texto) |
|---|---|---|---|
| 0 | Muito fraca / “Digite a nova senha.” | nenhuma | `ttsc-surface-2` |
| 1 | Fraca | 1 | `ttsc-danger` / `ttsc-danger-text` |
| 2 | Razoável | 2 | `ttsc-warning` / `ttsc-warning-text` |
| 3 | Boa | 3 | `ttsc-info` / `ttsc-info-text` |
| 4 | Forte | 4 | `ttsc-accent` / `ttsc-accent-text` |

Pontuação: `round(critérios atendidos / total × 4)`; abaixo do comprimento mínimo o teto é 1; todos os critérios + 4 caracteres além do mínimo = 4. A senha só é **válida** com todos os critérios (`isValid()`), igual ao servidor.

## API

Atributos:

| Atributo | Padrão | Descrição |
|---|---|---|
| `data-ttsc-password-meter` | — | Seletor do input observado |
| `data-ttsc-pm-min-length` | `8` | Comprimento mínimo (`password_min_length`) |

Opções JS (`new TTSCPasswordMeter(el, opts)`): `minLength`, `rules` (subconjunto de `['length','upper','lower','number','special']`, conforme a política).

| Método | Descrição |
|---|---|
| `TTSCPasswordMeter.init(root?)` | Inicializa todos os medidores (idempotente) |
| `check()` | Recalcula e devolve o score (0–4) |
| `getScore()` | Último score |
| `isValid()` | `true` só com todos os critérios atendidos |

Evento: `ttsc.passwordmeter.change` (bubbles) com `detail: { score, valid }`.

## Acessibilidade

- O rótulo de força é texto (“Força: Boa”), não só cor; anunciado por `aria-live="polite"`.
- Critérios em lista ligada ao input por `aria-describedby`; cada item recebe `aria-label` “…: atendido / pendente”.
- Ícone ✓/○ acompanha a mudança de cor (nunca só cor).
- Botão mostrar/ocultar com `aria-pressed` e `aria-label` que alterna (“Mostrar senha” / “Ocultar senha”).
- Textos de força usam os tokens `*-text` (≥ 4,5:1 nos dois temas); barras são decorativas.

## Modelos

### HTML

```html
<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="new-password">Nova senha</label>
  <div class="pm-wrap">
    <input type="password" class="ttsc-input" id="new-password" name="password" autocomplete="new-password"
           aria-describedby="pm-label pm-rules" required>
    <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" data-pm-reveal
            aria-label="Mostrar senha" aria-pressed="false"><i class="fa-light fa-eye"></i></button>
  </div>
  <div class="ttsc-password-meter" data-ttsc-password-meter="#new-password"
       data-ttsc-pm-min-length="<?= (int) $policy['password_min_length'] ?>">
    <div class="ttsc-pm-bars" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
    <div class="ttsc-pm-label" id="pm-label" aria-live="polite"></div>
    <ul class="ttsc-pm-rules" id="pm-rules"></ul>
  </div>
</div>
```

### CSS

```css
/* assets/css/ttsc.password-meter.css */
.ttsc-password-meter { display: flex; flex-direction: column; gap: 8px; }
.ttsc-pm-bars { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; }
.ttsc-pm-bars span { height: 4px; border-radius: var(--ttsc-radius-pill); background: var(--ttsc-surface-2); transition: background-color .15s; }
.ttsc-password-meter[data-score="1"] .ttsc-pm-bars span:nth-child(-n+1) { background: var(--ttsc-danger); }
.ttsc-password-meter[data-score="2"] .ttsc-pm-bars span:nth-child(-n+2) { background: var(--ttsc-warning); }
.ttsc-password-meter[data-score="3"] .ttsc-pm-bars span:nth-child(-n+3) { background: var(--ttsc-info); }
.ttsc-password-meter[data-score="4"] .ttsc-pm-bars span { background: var(--ttsc-accent); }
.ttsc-pm-label { font-size: 12px; color: var(--ttsc-text-muted); }
.ttsc-pm-label strong { font-weight: 600; }
.ttsc-password-meter[data-score="1"] .ttsc-pm-label strong { color: var(--ttsc-danger-text); }
.ttsc-password-meter[data-score="2"] .ttsc-pm-label strong { color: var(--ttsc-warning-text); }
.ttsc-password-meter[data-score="3"] .ttsc-pm-label strong { color: var(--ttsc-info-text); }
.ttsc-password-meter[data-score="4"] .ttsc-pm-label strong { color: var(--ttsc-accent-text); }
.ttsc-pm-rules { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 4px 16px;
  font-size: 12px; color: var(--ttsc-text-muted); }
.ttsc-pm-rules li { display: flex; gap: 6px; align-items: center; }
.ttsc-pm-rules li::before { content: "\f111"; font-family: "Font Awesome 7 Pro"; font-weight: 300; font-size: 11px; width: 12px; }
.ttsc-pm-rules li.ok { color: var(--ttsc-text-2); }
.ttsc-pm-rules li.ok::before { content: "\f00c"; color: var(--ttsc-accent-text); }
.pm-wrap { position: relative; }
.pm-wrap .ttsc-input { padding-inline-end: 40px; }
.pm-wrap .ttsc-btn { position: absolute; inset-inline-end: 2px; top: 50%; transform: translateY(-50%); }
```

### JS

```js
// assets/js/core/ttsc.password-meter.js — implementação TTSC (sem dependências)
(function (w) {
  'use strict';
  var RULES = [
    { id: 'length', text: function (o) { return 'Pelo menos ' + o.minLength + ' caracteres'; }, test: function (v, o) { return v.length >= o.minLength; } },
    { id: 'upper', text: function () { return 'Uma letra maiúscula'; }, test: function (v) { return /[A-Z]/.test(v); } },
    { id: 'lower', text: function () { return 'Uma letra minúscula'; }, test: function (v) { return /[a-z]/.test(v); } },
    { id: 'number', text: function () { return 'Um número'; }, test: function (v) { return /[0-9]/.test(v); } },
    { id: 'special', text: function () { return 'Um símbolo (!@#$…)'; }, test: function (v) { return /[^A-Za-z0-9]/.test(v); } }
  ];
  var LABELS = ['Muito fraca', 'Fraca', 'Razoável', 'Boa', 'Forte'];
  function TTSCPasswordMeter(el, opts) {
    if (el.ttscPasswordMeter) return el.ttscPasswordMeter;
    this.el = el;
    this.input = document.querySelector(el.dataset.ttscPasswordMeter);
    this.o = Object.assign({ minLength: +(el.dataset.ttscPmMinLength || 8), rules: ['length', 'upper', 'lower', 'number', 'special'] }, opts || {});
    this.rules = RULES.filter(function (r) { return this.o.rules.indexOf(r.id) > -1; }, this);
    this.label = el.querySelector('.ttsc-pm-label');
    this.list = el.querySelector('.ttsc-pm-rules');
    var self = this;
    if (this.list) this.list.innerHTML = this.rules.map(function (r) { return '<li data-rule="' + r.id + '">' + r.text(self.o) + '</li>'; }).join('');
    this.input.addEventListener('input', function () { self.check(); });
    el.ttscPasswordMeter = this;
    this.check();
  }
  TTSCPasswordMeter.prototype.check = function () {
    var v = this.input.value, o = this.o, self = this, passed = 0;
    this.rules.forEach(function (r) {
      var ok = r.test(v, o); if (ok) passed++;
      var li = self.list && self.list.querySelector('[data-rule="' + r.id + '"]');
      if (li) { li.classList.toggle('ok', ok); li.setAttribute('aria-label', r.text(o) + (ok ? ': atendido' : ': pendente')); }
    });
    var score = v ? Math.round(passed / this.rules.length * 4) : 0;
    if (v.length >= o.minLength + 4 && passed === this.rules.length) score = 4;
    if (v && v.length < o.minLength) score = Math.min(score, 1);
    this.score = score;
    this.valid = passed === this.rules.length;
    this.el.dataset.score = score;
    if (this.label) this.label.innerHTML = v ? 'Força: <strong>' + LABELS[score] + '</strong>' + (this.valid ? '' : ' · faltam ' + (this.rules.length - passed) + ' critério(s)') : 'Digite a nova senha.';
    this.el.dispatchEvent(new CustomEvent('ttsc.passwordmeter.change', { bubbles: true, detail: { score: score, valid: this.valid } }));
    return score;
  };
  TTSCPasswordMeter.prototype.getScore = function () { return this.score; };
  TTSCPasswordMeter.prototype.isValid = function () { return this.valid; };
  TTSCPasswordMeter.init = function (root) {
    (root || document).querySelectorAll('[data-ttsc-password-meter]').forEach(function (el) { new TTSCPasswordMeter(el); });
  };
  w.TTSCPasswordMeter = TTSCPasswordMeter;
  document.addEventListener('DOMContentLoaded', function () { TTSCPasswordMeter.init(); });
})(window);

// Mostrar/ocultar senha
document.querySelectorAll('[data-pm-reveal]').forEach((btn) => btn.addEventListener('click', () => {
  const input = btn.previousElementSibling;
  const show = input.type === 'password';
  input.type = show ? 'text' : 'password';
  btn.setAttribute('aria-pressed', show);
  btn.setAttribute('aria-label', show ? 'Ocultar senha' : 'Mostrar senha');
  btn.querySelector('i').className = show ? 'fa-light fa-eye-slash' : 'fa-light fa-eye';
}));

// Bloqueia o botão "Salvar" até a senha atender à política
document.addEventListener('ttsc.passwordmeter.change', (e) => {
  e.target.closest('form').querySelector('[type="submit"]').disabled = !e.detail.valid;
});
```

### SQL

```sql
-- Política (banco do tenant): valor da empresa sobrepõe o global (company_id NULL). MariaDB 10.11 / MySQL 8
SELECT s.setting_key, s.value, s.type
  FROM settings s
 WHERE s.category = 'security'
   AND s.setting_key IN ('password_min_length', 'password_require_uppercase', 'password_require_lowercase',
                         'password_require_number', 'password_require_special', 'password_expiry_days')
   AND (s.company_id = :company_id OR s.company_id IS NULL)
 ORDER BY s.setting_key, s.company_id IS NULL;     -- a linha da empresa vem primeiro

-- Banco master: a senha expirou? (mostra o medidor na tela "Sua senha expirou")
SELECT u.uuid,
       COALESCE(u.password_updated_at, u.password_changed_at)                                     AS last_change,
       DATEDIFF(NOW(), COALESCE(u.password_updated_at, u.password_changed_at, u.created_at))      AS days_since_change,
       DATEDIFF(NOW(), COALESCE(u.password_updated_at, u.password_changed_at, u.created_at)) >= :expiry_days AS must_change
  FROM users u
 WHERE u.uuid = :user_uuid AND u.deleted_at IS NULL;

-- Gravação após Auth::validatePassword() (hash no PHP; a senha em texto nunca chega ao SQL)
UPDATE users
   SET password = :password_hash, password_algo = :password_algo,
       password_changed_at = NOW(), password_updated_at = NOW(), updated_at = NOW()
 WHERE uuid = :user_uuid AND deleted_at IS NULL;
```

O PHP lê a política (padrões de `Auth`: mínimo 8 e os quatro critérios ligados; expiração 90 dias em `brand_settings.security.password_expiry_days`) e passa `password_min_length` em `data-ttsc-pm-min-length`. O medidor é só orientação: o servidor sempre roda `validatePassword()` antes do `UPDATE`.

## Faça / Não faça

- **Faça:** espelhar exatamente a política do servidor (mesmos critérios e mínimo).
- **Faça:** mostrar o que falta (“faltam 1 critério(s)”) e não só a cor.
- **Faça:** `autocomplete="new-password"` para o gerenciador de senhas sugerir uma senha forte.
- **Não faça:** enviar a senha a um serviço externo para medir força, nem registrá-la em logs/eventos.
- **Não faça:** mostrar o medidor no login ou bloquear colar no campo.
