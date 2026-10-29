# FormValidation

Validação de formulários no cliente com FormValidation 2.4.0 (do repo): regras por campo, verificação assíncrona de unicidade e erros acessíveis com `aria-invalid` e texto em `ttsc-danger-text`.

## Quando usar

- Formulários de cadastro e edição com regras além do `required` do HTML: formato de código, faixas numéricas, unicidade no banco (código do curso), campos dependentes.
- Drawers do CRUD genérico em que o erro precisa aparecer **antes** do POST, campo a campo.
- **Não use** como única barreira: o `DomainCrudController` revalida tudo (campos obrigatórios → 422, chave duplicada → 409).
- **Não use** para formatar enquanto digita (CPF, telefone, moeda): combine com [Inputmask](../Inputmask/README.md) e valide o valor sem máscara.
- Para força de senha visual, use [PasswordMeter](../PasswordMeter/README.md) junto com o validador `callback`.

## Anatomia

```
.ttsc-form-item
 ├ label.ttsc-form-label   Código *
 ├ input.ttsc-input        [aria-invalid="true"] [aria-describedby="…-message"]   ← plugin Aria
 └ [data-fv-message]       ⓘ Este código já está em uso nesta unidade.        ← plugin Message
… footer: [Limpar] [Salvar curso]   ← plugin SubmitButton
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Formulário | `<form novalidate>` | sim |
| Item | `.ttsc-form-item` (label + campo + mensagem) | sim |
| Campo | `.ttsc-input` com `name` igual à chave em `fields` | sim |
| Contêiner de mensagem | `<div data-fv-message="<campo>">` (usado por `Message.container`) | sim |
| Mensagem | `.fv-plugins-message-container > .fv-help-block[role=alert]` (gerado) | — |
| Botão | `button[type=submit]` | sim |

## Estados

| Estado | Como aparece | Tokens |
|---|---|---|
| Não validado | borda padrão | `--input` (`ttsc-border`) |
| Validando (assíncrono) | `.fv-validating` no form, ícone do botão gira | — |
| Inválido | `aria-invalid="true"` → borda vermelha (runtime `.ttsc-input[aria-invalid=true]`) + mensagem com ícone | `--destructive`, texto `ttsc-danger-text` |
| Válido | `.is-valid` → borda verde suave | `ttsc-accent-border` |
| Formulário válido | evento `core.form.valid` → envio por `fetch` | — |

## API

Plugins disponíveis no bundle 2.4.0 (`FormValidation.plugins.*`): `Alias`, `Aria`, `Declarative`, `DefaultSubmit`, `Dependency`, `Excluded`, `FieldStatus`, `Framework`, `Icon`, `Message`, `Sequence`, `SubmitButton`, `Tooltip`, `Trigger`, `Bootstrap5`. Padrão TTSC:

| Plugin | Opções usadas | Papel |
|---|---|---|
| `Trigger` | `{ event: { code: 'blur', name: 'blur input' } }` | Quando validar cada campo |
| `Sequence` | `{ enabled: true }` | Para no primeiro validador que falha (evita chamar o `remote` com formato inválido) |
| `Aria` | — | Gerencia `aria-invalid` e `aria-describedby` |
| `Message` | `{ clazz: 'fv-help-block', container: (field) => el }` | Onde a mensagem é inserida |
| `SubmitButton` | — | Valida no submit e bloqueia o envio inválido |
| `DefaultSubmit` | — | **Não use** no CRUD (o envio é por `fetch`) |

Validadores usados (há 50+ em `FormValidation.validators`, inclusive `id`/`vat` com país `BR` para CPF/CNPJ):

| Validador | Opções |
|---|---|
| `notEmpty` | `message` |
| `regexp` | `regexp: /^[A-Z0-9-]{2,20}$/` |
| `stringLength` | `min`, `max` |
| `integer` | `thousandsSeparator: '.'`, `decimalSeparator: ','` |
| `between` | `min`, `max` |
| `remote` | `url`, `method`, `data`, `headers` — servidor responde `{ "valid": true|false, "message"? }` |
| `promise` | `promise: (input) => Promise<{valid}>` (usado no preview, sem servidor) |

Métodos da instância (`fv = FormValidation.formValidation(form, opts)`): `validate()` → `Promise<'Valid'|'Invalid'|'NotValidated'>`, `validateField(name)`, `revalidateField(name)`, `resetForm(reset?)`, `resetField(name)`, `updateFieldStatus(name, 'Invalid'|'Valid'|'NotValidated', validator?)`, `addField(name, opts)`, `removeField(name)`, `enableValidator` / `disableValidator`, `destroy()`.

Eventos (`fv.on(...)`): `core.form.validating`, `core.form.valid`, `core.form.invalid`, `core.element.validated` (`{element, field, valid}`), `core.validator.validated`, `core.field.added`.

## Acessibilidade

- O plugin `Aria` liga a mensagem ao campo (`aria-describedby`) e marca `aria-invalid`; a mensagem tem `role="alert"`.
- No `core.form.invalid`, o foco vai para o primeiro campo inválido.
- Obrigatório indicado por `*` visual **e** `aria-required="true"`; o asterisco tem `aria-hidden`.
- Mensagem em `ttsc-danger-text` (4,5:1 claro e escuro) com ícone, nunca só a borda vermelha.
- Mensagens em pt-BR dizem como corrigir: “Use de 2 a 20 caracteres: A–Z, 0–9 e hífen.”

## Modelos

### HTML

```html
<form id="course-form" class="grid grid-cols-3 gap-4" novalidate
      action="/api/v1/crud/academic/courses" data-ttsc-crud>
  <input type="hidden" name="_token" value="<?= $this->e($csrfToken) ?>">
  <input type="hidden" name="uuid" value="<?= $this->e($course['uuid'] ?? '') ?>">
  <div class="ttsc-form-item">
    <label class="ttsc-form-label" for="course-code">Código <span class="req" aria-hidden="true">*</span></label>
    <input class="ttsc-input" id="course-code" name="code" autocomplete="off" aria-required="true"
           value="<?= $this->e($course['code'] ?? '') ?>">
    <div data-fv-message="code"></div>
  </div>
  <div class="ttsc-form-item">
    <label class="ttsc-form-label" for="course-name">Nome do curso <span class="req" aria-hidden="true">*</span></label>
    <input class="ttsc-input" id="course-name" name="name" aria-required="true" value="<?= $this->e($course['name'] ?? '') ?>">
    <div data-fv-message="name"></div>
  </div>
  <div class="ttsc-form-item">
    <label class="ttsc-form-label" for="course-hours">Carga horária (h) <span class="req" aria-hidden="true">*</span></label>
    <input class="ttsc-input" id="course-hours" name="total_hours" inputmode="numeric" aria-required="true"
           value="<?= $this->e($course['total_hours'] ?? '') ?>">
    <div data-fv-message="total_hours"></div>
  </div>
  <div class="flex justify-end gap-2" style="grid-column: 1 / -1">
    <button type="button" class="ttsc-btn ttsc-btn-ghost" data-ttsc-drawer-dismiss="true">Cancelar</button>
    <button type="submit" class="ttsc-btn ttsc-btn-primary"><i class="fa-light fa-floppy-disk"></i> Salvar curso</button>
  </div>
</form>
```

### CSS

```css
/* assets/css/ttsc.form-validation.css — carregar depois de vendor/form-validation/form-validation.min.css */
.fv-plugins-message-container { display: block; min-height: 16px; font-size: 12px; line-height: 16px; color: var(--ttsc-danger-text); }
.fv-plugins-message-container .fv-help-block { display: flex; gap: 6px; align-items: center; }
.fv-plugins-message-container .fv-help-block::before {   /* fa-circle-exclamation, peso light */
  content: "\f06a"; font-family: "Font Awesome 7 Pro"; font-weight: 300;
}
/* inválido já vem do runtime: .ttsc-input[aria-invalid=true] { border-color: var(--destructive) } */
.ttsc-input.is-valid { border-color: var(--ttsc-accent-border); }
.ttsc-form-label .req { color: var(--ttsc-danger-text); }
.fv-validating [type="submit"] i { animation: ttsc-spin .8s linear infinite; }
@keyframes ttsc-spin { to { transform: rotate(360deg); } }

/* Tooltip do plugin Tooltip (padrão preto) nos tokens */
.fv-plugins-tooltip .fv-plugins-tooltip__content {
  background: var(--ttsc-text); color: var(--ttsc-surface); border-radius: var(--ttsc-radius-sm); box-shadow: var(--ttsc-shadow-popover);
}
```

### JS

```js
// assets/js/core/ttsc.course-form.js — requer vendor/form-validation/form-validation.bundle.js
const form = document.getElementById('course-form');
const token = form.querySelector('[name="_token"]').value;

const fv = FormValidation.formValidation(form, {
  fields: {
    code: {
      validators: {
        notEmpty: { message: 'Informe o código do curso.' },
        regexp: { regexp: /^[A-Z0-9-]{2,20}$/, message: 'Use de 2 a 20 caracteres: A–Z, 0–9 e hífen.' },
        remote: {
          url: '/academic/courses/check-code',
          method: 'GET',
          data: () => ({ uuid: form.querySelector('[name="uuid"]').value }),   // ignora o próprio curso na edição
          message: 'Este código já está em uso nesta unidade.',
        },
      },
    },
    name: {
      validators: {
        notEmpty: { message: 'Informe o nome do curso.' },
        stringLength: { min: 3, max: 255, message: 'O nome deve ter entre 3 e 255 caracteres.' },
      },
    },
    total_hours: {
      validators: {
        notEmpty: { message: 'Informe a carga horária.' },
        integer: { message: 'Use apenas números inteiros.', thousandsSeparator: '.', decimalSeparator: ',' },
        between: { min: 20, max: 10000, message: 'Entre 20 e 10.000 horas.' },
      },
    },
  },
  plugins: {
    trigger: new FormValidation.plugins.Trigger({ event: { code: 'blur', name: 'blur input', total_hours: 'blur input' } }),
    sequence: new FormValidation.plugins.Sequence({ enabled: true }),
    aria: new FormValidation.plugins.Aria(),
    message: new FormValidation.plugins.Message({
      clazz: 'fv-help-block',
      container: (field) => form.querySelector(`[data-fv-message="${field}"]`),
    }),
    submitButton: new FormValidation.plugins.SubmitButton(),
  },
});

form.querySelector('[name="code"]').addEventListener('input', (e) => { e.target.value = e.target.value.toUpperCase(); });
fv.on('core.element.validated', (e) => e.element.classList.toggle('is-valid', e.valid));
fv.on('core.form.validating', () => form.classList.add('fv-validating'));
fv.on('core.form.invalid', () => {
  form.classList.remove('fv-validating');
  form.querySelector('[aria-invalid="true"]')?.focus();
});
fv.on('core.form.valid', async () => {
  try {
    const res = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'X-CSRF-Token': token } });
    if (res.status === 409) {                                   // corrida: outro usuário gravou o mesmo código
      fv.updateFieldStatus('code', 'Invalid', 'remote');
      return;
    }
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    TTSC.Toast.show({ message: 'Curso salvo.', variant: 'success' });
  } finally {
    form.classList.remove('fv-validating');
  }
});
```

### SQL

```sql
-- GET /academic/courses/check-code?code=ADM-01&uuid=  → {"valid": true|false}
-- A chave única é uk_course_unit_code (unit_uuid, code) e vale também para linhas com deleted_at,
-- por isso a consulta NÃO filtra deleted_at: um código de curso excluído continua ocupado.
SELECT COUNT(*) = 0                                AS valid,
       COALESCE(MAX(c.deleted_at IS NOT NULL), 0) AS taken_by_deleted
  FROM courses c
 WHERE c.unit_uuid = :unit_uuid
   AND c.code = UPPER(TRIM(:code))
   AND c.uuid <> COALESCE(:course_uuid, '');      -- vazio na criação
```

O endpoint devolve `{"valid": <valid>, "message": "Código pertence a um curso excluído."}` quando `taken_by_deleted = 1`. No POST, o `DomainCrudController` ainda converte o erro 1062 da chave única em **409**, tratado no JS com `updateFieldStatus`.

## Faça / Não faça

- **Faça:** `Sequence` ligado para não chamar o `remote` quando o formato já falhou.
- **Faça:** mensagens que dizem como corrigir, em pt-BR; foco no primeiro erro.
- **Faça:** revalidar tudo no servidor e mapear 409/422 de volta para o campo.
- **Não faça:** `DefaultSubmit` em formulários do CRUD (recarrega a página e perde o drawer).
- **Não faça:** usar a borda vermelha como único sinal de erro, nem esconder a mensagem em tooltip em telas de toque.
