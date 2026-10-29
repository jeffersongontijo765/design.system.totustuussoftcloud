# Forms

Guia de formulários do chassi: grade de campos, rótulo, dica, erro com `aria-invalid`, obrigatório, seções e rodapé de ações, montados com as classes `.ttsc-form-*` do runtime e o validador `TTSCFormValidator` (`assets/js/ttsc.form.js`).

> Também listado em: **Base › Forms**.

## Quando usar

- Todo cadastro e edição do CRUD genérico (`DomainCrudController`): curso, turma, aluno, unidade — em página, [Drawer](../Drawer/README.md) ou modal.
- Campos especializados têm páginas próprias: [Checkbox](../Checkbox/README.md), [DatePicker](../DatePicker/README.md), [ColorPicker](../ColorPicker/README.md), [FileInput](../FileInput/README.md), [ImageInput](../ImageInput/README.md); máscara em [Inputmask](../Inputmask/README.md); validação declarativa avançada em [FormValidation](../FormValidation/README.md).
- **Não use** um formulário único para processos em etapas: use [Stepper](../Stepper/README.md).
- **Não use** formulário para filtrar listas — filtros ficam na toolbar da página, aplicados sem botão “Salvar”.

## Anatomia

```
form.ttsc-form
├─ fieldset.ttsc-form-section  (legend + descrição)
│   └─ .ttsc-form-grid  (2 colunas; .col-span-2 ocupa a linha)
│       └─ .ttsc-form-item
│           ├─ label.ttsc-form-label  "Código *"
│           ├─ input.ttsc-input  [required] [aria-invalid] [aria-describedby]
│           ├─ .ttsc-form-description  (dica — some quando há erro)
│           └─ .ttsc-form-message      (erro — aparece com aria-invalid="true")
└─ .ttsc-form-actions  [Cancelar] [Salvar]
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Formulário | `form.ttsc-form` (+ `novalidate` quando o JS valida) + `_token` CSRF | sim |
| Seção | `fieldset.ttsc-form-section` + `legend` | quando > 6 campos |
| Grade | `.ttsc-form-grid` (extensão) ou `grid grid-cols-2 gap-4` | sim |
| Item | `.ttsc-form-item` (coluna, gap 10px) | sim |
| Rótulo | `label.ttsc-form-label[for]`; obrigatório com `<span class="ttsc-form-required" aria-hidden="true">*</span>` | sim |
| Controle | `.ttsc-input` · `.ttsc-select` · `.ttsc-textarea` · `.ttsc-switch` · `.ttsc-checkbox` | sim |
| Dica | `.ttsc-form-description` com `id` referenciado por `aria-describedby` | não |
| Erro | `.ttsc-form-message` — exibido pelo runtime quando o item `:has([aria-invalid=true])` | sim (quando validável) |
| Linha inline | `.ttsc-form-control-inline` (switch/checkbox + rótulo) | não |
| Rodapé | `.ttsc-form-actions` (alinhado à direita, gap 10px) | sim |
| Erro geral | `.ttsc-form-banner.ttsc-form-banner--error[role=alert]` (criado pelo validador para `errors._form`) | não |

O atom PHP `app::components/atoms/input` gera a variante legada `.ttsc-field` / `.ttsc-field-label` / `.ttsc-field-error` / `.ttsc-help`, que é a que o `TTSCFormValidator` marca com `has-error` / `is-valid`. Em telas novas use `.ttsc-form-item` + `aria-invalid`; o validador funciona nas duas (ver JS).

## Estados

| Estado | Como aplicar | Tokens |
|---|---|---|
| Normal | — | borda `ttsc-border-strong` (`--input`), fundo `ttsc-surface` |
| Foco | automático | anel `ttsc-accent` (`--ring`) |
| Obrigatório | `required` + asterisco `aria-hidden` | asterisco `ttsc-danger-text` |
| Erro | `aria-invalid="true"` no controle | borda `ttsc-danger`; mensagem `ttsc-danger-text` (4,8:1 claro / 6,0:1 escuro) |
| Válido | `.is-valid` (validador) — opcional | sem cor extra; não pinte de verde |
| Desabilitado | `disabled` | opacidade 50% |
| Somente leitura | `readonly` | fundo `ttsc-canvas-2` (extensão) |
| Enviando | botão submit `disabled` + `aria-busy` ([Button](../Button/README.md)) | — |

## API

| `TTSCFormValidator` (`ttsc.form.js`) | Descrição |
|---|---|
| `new TTSCFormValidator(form, opts)` | liga validação no `blur`/`input`/`submit` de todos os `input, textarea, select` |
| `validate()` | valida tudo de forma síncrona; retorna `true/false` |
| `applyServerErrors({ campo: 'msg', _form: 'msg' })` | mostra erros do 422 por `name`; `_form` vira banner |
| `serialize()` | objeto a partir do `FormData` (campos repetidos viram array) |
| `clear()` | `reset()` + limpa estados e mensagens |

| Regra | Origem no HTML | Mensagem padrão |
|---|---|---|
| obrigatório | `required` ou `data-required="true"` | `required` |
| e-mail / URL | `type="email"` / `type="url"` | — |
| CPF / CNPJ | `data-mask="cpf"` / `"cnpj"` (máscara aplicada no `input`) | — |
| min / max / minlength / maxlength / pattern | atributos nativos | — |
| igual a | `data-equal-to="#senha"` | “Values do not match” |
| máscaras | `data-mask="cpf|cnpj|phone|cep|date|currency"` dentro de `.ttsc-field` | — |

## Acessibilidade

- Todo controle tem `<label for>`; placeholder nunca substitui rótulo.
- Dica e erro ligados por `aria-describedby="code-hint code-error"`; erro com `role="alert"` só quando aparece após ação do usuário.
- `aria-invalid="true"` é o gatilho visual **e** semântico — não use só cor.
- Obrigatório: atributo `required` (anunciado) + asterisco visual `aria-hidden`; explique “* obrigatório” no topo do formulário.
- Ao falhar o envio, foque o primeiro campo inválido ([Scrollto](../Scrollto/README.md) quando estiver fora da tela).
- Agrupe radios/checkboxes em `fieldset` + `legend`.

## Modelos

### HTML

```html
<form class="ttsc-form" method="post" action="/academic/courses" data-ttsc-crud novalidate>
  <input type="hidden" name="_token" value="<?= $this->e($csrf) ?>">
  <p class="ttsc-form-note"><span class="ttsc-form-required" aria-hidden="true">*</span> campos obrigatórios</p>

  <fieldset class="ttsc-form-section">
    <legend>Identificação</legend>
    <div class="ttsc-form-grid">
      <div class="ttsc-form-item">
        <label class="ttsc-form-label" for="course-code">Código <span class="ttsc-form-required" aria-hidden="true">*</span></label>
        <input class="ttsc-input" id="course-code" name="code" required maxlength="50"
               value="<?= $this->e($old['code'] ?? '') ?>"
               aria-invalid="<?= isset($errors['code']) ? 'true' : 'false' ?>"
               aria-describedby="course-code-hint course-code-error" data-unique-url="/academic/courses/check-code">
        <div class="ttsc-form-description" id="course-code-hint">Único por unidade. Ex.: ADM-01.</div>
        <div class="ttsc-form-message" id="course-code-error" role="alert"><?= $this->e($errors['code'] ?? 'Informe o código.') ?></div>
      </div>
      <div class="ttsc-form-item">
        <label class="ttsc-form-label" for="course-name">Nome <span class="ttsc-form-required" aria-hidden="true">*</span></label>
        <input class="ttsc-input" id="course-name" name="name" required maxlength="255">
        <div class="ttsc-form-message" role="alert">Informe o nome do curso.</div>
      </div>
      <div class="ttsc-form-item col-span-2">
        <label class="ttsc-form-label" for="course-description">Descrição</label>
        <textarea class="ttsc-textarea" id="course-description" name="description" rows="3"></textarea>
      </div>
    </div>
  </fieldset>

  <fieldset class="ttsc-form-section">
    <legend>Oferta</legend>
    <div class="ttsc-form-grid">
      <div class="ttsc-form-item">
        <label class="ttsc-form-label" for="course-modality">Modalidade</label>
        <select class="ttsc-select" id="course-modality" name="modality">
          <option value="in_person">Presencial</option><option value="online">EAD</option><option value="hybrid">Híbrido</option>
        </select>
      </div>
      <div class="ttsc-form-item">
        <label class="ttsc-form-label" for="course-max">Vagas por turma</label>
        <input class="ttsc-input" id="course-max" name="max_students" type="number" min="1" max="500">
        <div class="ttsc-form-message" role="alert">Entre 1 e 500.</div>
      </div>
      <div class="ttsc-form-control-inline col-span-2">
        <input class="ttsc-switch" type="checkbox" id="course-active" name="is_active" value="1" checked>
        <label class="ttsc-form-label" for="course-active">Curso ativo para novas matrículas</label>
      </div>
    </div>
  </fieldset>

  <div class="ttsc-form-actions">
    <button type="button" class="ttsc-btn ttsc-btn-ghost" data-ttsc-drawer-dismiss="true">Cancelar</button>
    <button type="submit" class="ttsc-btn ttsc-btn-primary"><i class="fa-light fa-floppy-disk"></i> Salvar curso</button>
  </div>
</form>
```

### CSS

```css
/* Ponte (bundle.css): .ttsc-form-message usa --destructive (= --ttsc-danger); para texto no escuro, troque pelo token de texto */
.ttsc-form-message { color: var(--ttsc-danger-text); }
.ttsc-form-description { color: var(--ttsc-text-muted); }

/* Extensões do chassi */
.ttsc-form-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--ttsc-space-4); }
@media (max-width: 640px) { .ttsc-form-grid { grid-template-columns: 1fr; } .ttsc-form-grid .col-span-2 { grid-column: auto; } }
.ttsc-form-section { border: 0; margin: 0; padding: 0 0 var(--ttsc-space-5); border-bottom: 1px solid var(--ttsc-border-soft); }
.ttsc-form-section + .ttsc-form-section { padding-top: var(--ttsc-space-5); }
.ttsc-form-section > legend { font-size: 13px; font-weight: 600; color: var(--ttsc-text); padding: 0; margin-bottom: var(--ttsc-space-3); }
.ttsc-form-required { color: var(--ttsc-danger-text); margin-inline-start: 2px; }
.ttsc-form-note { font-size: 12px; color: var(--ttsc-text-muted); }
.ttsc-input[readonly], .ttsc-textarea[readonly] { background: var(--ttsc-canvas-2); }
.ttsc-form-actions { padding-top: var(--ttsc-space-4); border-top: 1px solid var(--ttsc-border-soft); }
.ttsc-form-banner--error {
  padding: 10px 12px; border-radius: var(--ttsc-radius-control); font-size: 13px;
  background: color-mix(in srgb, var(--ttsc-danger) 10%, transparent); color: var(--ttsc-danger-text);
}
```

### JS

```js
// assets/js/core/ttsc.forms.js — liga validação nativa ao contrato aria-invalid + unicidade remota
function setInvalid(field, message) {
  field.setAttribute('aria-invalid', message ? 'true' : 'false');
  const msg = field.closest('.ttsc-form-item')?.querySelector('.ttsc-form-message');
  if (msg && message) msg.textContent = message;
}

function messageFor(field) {
  const v = field.validity;
  if (v.valueMissing) return 'Campo obrigatório.';
  if (v.rangeUnderflow || v.rangeOverflow) return `Entre ${field.min} e ${field.max}.`;
  if (v.tooLong) return `Máximo de ${field.maxLength} caracteres.`;
  if (v.typeMismatch || v.patternMismatch) return 'Formato inválido.';
  return '';
}

async function checkUnique(field) {
  const url = new URL(field.dataset.uniqueUrl, location.origin);
  url.searchParams.set('value', field.value.trim());
  const ignore = field.form.querySelector('[name="uuid"]')?.value;
  if (ignore) url.searchParams.set('ignore', ignore);
  const { taken } = await (await fetch(url, { headers: { Accept: 'application/json' } })).json();
  return taken ? 'Já existe um curso com este código nesta unidade.' : '';
}

export function initForm(form) {
  const fields = form.querySelectorAll('input:not([type=hidden]), select, textarea');
  fields.forEach((field) => {
    field.addEventListener('blur', async () => {
      let message = messageFor(field);
      if (!message && field.dataset.uniqueUrl && field.value.trim()) message = await checkUnique(field);
      setInvalid(field, message);
    });
    field.addEventListener('input', () => { if (field.getAttribute('aria-invalid') === 'true' && field.checkValidity()) setInvalid(field, ''); });
  });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    let first = null;
    fields.forEach((f) => { const m = messageFor(f); setInvalid(f, m); if (m && !first) first = f; });
    if (first) { first.focus(); return; }
    const res = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
    if (res.status === 422) {
      const { errors } = await res.json();
      Object.entries(errors).forEach(([name, msg]) => { const f = form.elements[name]; if (f) setInvalid(f, msg); });
      form.querySelector('[aria-invalid="true"]')?.focus();
      return;
    }
    location.href = (await res.json()).redirect;
  });
}

document.querySelectorAll('form.ttsc-form').forEach(initForm);

// Telas legadas com .ttsc-field: o validador do repositório
document.querySelectorAll('form[data-ttsc-validate]').forEach((f) => new TTSCFormValidator(f));
```

### SQL

Unicidade de `courses.code` por unidade (`uk_course_unit_code`) checada antes de gravar, e INSERT com prepared statement:

```sql
-- Endpoint /academic/courses/check-code (blur) e revalidação no store/update
SELECT EXISTS (
  SELECT 1 FROM courses
   WHERE unit_uuid = :unit_uuid
     AND code = :code
     AND deleted_at IS NULL
     AND uuid <> :ignore_uuid          -- '' no cadastro; uuid do próprio curso na edição
) AS code_taken;

-- Gravação (PDO prepare + execute; nunca interpolar valores)
INSERT INTO courses (uuid, code, name, description, type, modality, duration_periods, period_type,
                     total_hours, max_students, unit_uuid, is_active)
VALUES (:uuid, :code, :name, :description, :type, :modality, :duration_periods, :period_type,
        :total_hours, :max_students, :unit_uuid, :is_active);
```

O `DomainCrudController` valida tipos e obrigatórios, roda o `EXISTS` e responde 422 com `{"errors": {"code": "Já existe um curso com este código nesta unidade."}}`; mesmo assim captura `SQLSTATE 23000` do índice único (corrida entre dois envios) e devolve o mesmo 422. Registros com `deleted_at` ainda ocupam o índice: para reaproveitar o código, restaure o curso excluído.

## Faça / Não faça

- **Faça:** uma coluna no mobile, duas no desktop; campos longos (`textarea`, endereço) em `col-span-2`.
- **Faça:** validar no `blur` e no envio; mostrar a mensagem do servidor no mesmo lugar.
- **Não faça:** desabilitar “Salvar” até o formulário ficar válido — deixe enviar e mostre os erros.
- **Não faça:** mensagens genéricas (“Campo inválido”); diga como corrigir.
