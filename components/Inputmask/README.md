# Inputmask

Máscaras de digitação com Inputmask 5.0.9 para os formatos brasileiros (CPF, CNPJ, telefone, CEP, moeda R$ e data), enviando ao servidor só os dígitos.

## Quando usar

- Campos com formato fixo e conhecido: CPF, CNPJ, telefone fixo/celular, CEP, data `dd/mm/aaaa`, valores em R$.
- Quando o banco guarda o valor **sem** formatação (`users.cpf`, `users.phone`) e a tela precisa mostrar formatado.
- **Não use** para ajustar números pequenos com passo: use [Dialer](../Dialer/README.md).
- **Não use** para datas com calendário: use o Date Picker (flatpickr); a máscara de data serve para digitação rápida (nascimento).
- A validação (dígito verificador do CPF, unicidade) é feita por [FormValidation](../FormValidation/README.md) ou no servidor; a máscara só formata.

## Anatomia

```
CPF
[ 529.982.247-25 ]     input.ttsc-input[data-ttsc-mask="cpf"]
enviado: 52998224725   (unmaskedvalue / removeMaskOnSubmit)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Campo | `input.ttsc-input` com `name` e `<label for>` | sim |
| Tipo de máscara | `data-ttsc-mask="cpf|cnpj|phone|cep|money|date"` | sim |
| Teclado móvel | `inputmode="numeric|tel|decimal"` | sim |
| Mensagem de erro | `span` em `ttsc-danger-text` + `aria-invalid="true"` no input | quando inválido |

## Variantes

| `data-ttsc-mask` | Opções Inputmask | Exibe | Envia |
|---|---|---|---|
| `cpf` | `mask: '999.999.999-99'` | 529.982.247-25 | `52998224725` |
| `cnpj` | `mask: '99.999.999/9999-99'` | 11.222.333/0001-81 | `11222333000181` |
| `phone` | `mask: ['(99) 9999-9999', '(99) 99999-9999'], keepStatic: true` | (31) 98765-4321 | `31987654321` |
| `cep` | `mask: '99999-999'` | 30130-010 | `30130010` |
| `money` | `alias: 'currency', prefix: 'R$ ', groupSeparator: '.', radixPoint: ',', digits: 2, unmaskAsNumber: true` | R$ 1.250,50 | `1250.5` |
| `date` | `alias: 'datetime', inputFormat: 'dd/mm/yyyy', outputFormat: 'yyyy-mm-dd'` | 14/03/2008 | `2008-03-14` |

Tokens: o campo é o `.ttsc-input` do runtime (`--input`, `--background`, `--foreground`); placeholder da máscara (`_`) herda `--foreground`; erro usa `--destructive` na borda e `ttsc-danger-text` no texto.

## API

Opções (Inputmask 5.0.9) mais usadas:

| Opção | Descrição |
|---|---|
| `mask` | String ou array (o array escolhe a máscara que couber: telefone 8/9 dígitos) |
| `alias` | `currency`, `numeric`, `decimal`, `integer`, `percentage`, `datetime`, `email`, `ip`… |
| `placeholder` | Caractere/forma de preenchimento (`_`, `dd/mm/aaaa`) |
| `keepStatic` | Mantém a máscara curta até o usuário digitar o 9º dígito |
| `clearIncomplete` | Limpa no blur se incompleto (padrão `false` aqui, para não apagar o que o usuário digitou) |
| `removeMaskOnSubmit` | Envia o valor sem máscara num submit nativo |
| `autoUnmask` | `el.value` já devolve sem máscara |
| `unmaskAsNumber` | Em `currency`, `unmaskedvalue()` vira número |
| `oncomplete` / `onincomplete` / `oncleared` | Callbacks |

Métodos: `Inputmask(opts).mask(el|seletor)`, `el.inputmask.unmaskedvalue()`, `el.inputmask.isComplete()`, `el.inputmask.isValid()`, `el.inputmask.setValue(v)`, `el.inputmask.remove()`, `Inputmask.format(valor, opts)` (formata texto para exibição, ex. em tabelas), `Inputmask.unmask(valor, opts)`.

## Acessibilidade

- Sempre `<label for>` visível; a máscara não substitui o rótulo (“CPF”, não só o placeholder).
- `inputmode` correto abre o teclado numérico no celular.
- Erros com `aria-invalid="true"` + texto ligado por `aria-describedby`, em `ttsc-danger-text` (4,5:1 nos dois temas).
- Não bloqueie colar: o Inputmask aceita colar “529.982.247-25” ou “52998224725”.

## Modelos

### HTML

```html
<div class="grid grid-cols-3 gap-4">
  <div class="ttsc-form-item">
    <label class="ttsc-form-label" for="user-cpf">CPF</label>
    <input class="ttsc-input" id="user-cpf" name="cpf" data-ttsc-mask="cpf" inputmode="numeric"
           value="<?= $this->e($user['cpf'] ?? '') ?>" aria-describedby="user-cpf-err">
    <span class="ttsc-form-message" id="user-cpf-err" hidden></span>
  </div>
  <div class="ttsc-form-item">
    <label class="ttsc-form-label" for="user-phone">Celular</label>
    <input class="ttsc-input" id="user-phone" name="phone" data-ttsc-mask="phone" inputmode="tel"
           value="<?= $this->e($user['phone'] ?? '') ?>">
  </div>
  <div class="ttsc-form-item">
    <label class="ttsc-form-label" for="inv-amount">Mensalidade</label>
    <input class="ttsc-input" id="inv-amount" name="gross_amount" data-ttsc-mask="money" inputmode="decimal"
           value="<?= $this->e(number_format((float) $invoice['gross_amount'], 2, ',', '.')) ?>">
  </div>
</div>
```

### CSS

```css
/* Números alinhados (CPF, valores) e marcador de máscara discreto */
.ttsc-input[data-ttsc-mask] { font-variant-numeric: tabular-nums; }
.ttsc-input[data-ttsc-mask="money"] { text-align: right; }
.ttsc-input[data-ttsc-mask]::placeholder { color: var(--ttsc-text-muted); }

/* Erro: borda já vem do runtime (.ttsc-input[aria-invalid=true]); o texto usa o token de texto */
.ttsc-input[aria-invalid="true"] + .ttsc-form-message { color: var(--ttsc-danger-text); }
```

### JS

```js
// assets/js/core/ttsc.masks.js — requer vendor/inputmask/inputmask.min.js
export const TTSC_MASKS = {
  cpf:   { mask: '999.999.999-99' },
  cnpj:  { mask: '99.999.999/9999-99' },
  phone: { mask: ['(99) 9999-9999', '(99) 99999-9999'], keepStatic: true },
  cep:   { mask: '99999-999' },
  money: { alias: 'currency', prefix: 'R$ ', groupSeparator: '.', radixPoint: ',', digits: 2,
           digitsOptional: false, rightAlign: false, unmaskAsNumber: true },
  date:  { alias: 'datetime', inputFormat: 'dd/mm/yyyy', outputFormat: 'yyyy-mm-dd', placeholder: 'dd/mm/aaaa' },
};

export function cpfValid(d) {
  if (!/^\d{11}$/.test(d) || /^(\d)\1{10}$/.test(d)) return false;
  for (let t = 9; t < 11; t++) {
    let s = 0;
    for (let i = 0; i < t; i++) s += +d[i] * (t + 1 - i);
    if (((s * 10) % 11) % 10 !== +d[t]) return false;
  }
  return true;
}

export function initMasks(root = document) {
  root.querySelectorAll('[data-ttsc-mask]').forEach((el) => {
    if (el.inputmask) return;                                  // idempotente (drawers)
    Inputmask(TTSC_MASKS[el.dataset.ttscMask]).mask(el);
  });
  root.querySelectorAll('[data-ttsc-mask="cpf"]').forEach((el) => {
    el.addEventListener('blur', () => {
      const digits = el.inputmask.unmaskedvalue();
      el.setAttribute('aria-invalid', digits === '' || cpfValid(digits) ? 'false' : 'true');
    });
  });
}

// Envio por fetch: troca o valor formatado pelo valor cru antes do POST
export function unmaskedFormData(form) {
  const data = new FormData(form);
  form.querySelectorAll('[data-ttsc-mask]').forEach((el) => {
    data.set(el.name, el.inputmask ? el.inputmask.unmaskedvalue() : el.value);
  });
  return data;
}

// Exibição em tabela sem input:
// Inputmask.format('52998224725', TTSC_MASKS.cpf) → "529.982.247-25"
document.addEventListener('DOMContentLoaded', () => initMasks());
```

### SQL

```sql
-- Banco master. users.cpf varchar(14) e users.phone varchar(20) guardam SÓ dígitos.
-- CPF já usado por outro usuário? (chave única `cpf`)
SELECT u.uuid, u.name
  FROM users u
 WHERE u.cpf = :cpf_digits                 -- '52998224725'
   AND u.uuid <> COALESCE(:user_uuid, '')
   AND u.deleted_at IS NULL
 LIMIT 1;

-- Gravação (o PHP aplica preg_replace('/\D+/', '', $valor) antes)
UPDATE users
   SET cpf = :cpf_digits, phone = :phone_digits, updated_at = NOW()
 WHERE uuid = :user_uuid AND deleted_at IS NULL;

-- Auditoria de legado: linhas que ainda têm máscara gravada
SELECT COUNT(*) AS masked_rows
  FROM users
 WHERE cpf REGEXP '[^0-9]' OR phone REGEXP '[^0-9]';
```

O PHP envia o valor cru no `value` do input (a máscara formata ao montar) e, no POST, normaliza com `preg_replace('/\D+/', '', …)` e revalida o dígito verificador antes do `UPDATE`. Moeda chega como `1250.5` (`unmaskAsNumber`) e vai para colunas `decimal(12,2)`.

## Faça / Não faça

- **Faça:** guardar só dígitos e formatar na exibição (`Inputmask.format`).
- **Faça:** telefone com array de máscaras (8 e 9 dígitos) e `keepStatic: true`.
- **Faça:** validar o CPF (dígitos verificadores) além da máscara completa.
- **Não faça:** `type="number"` com máscara (o navegador descarta pontos e hífens) nem `clearIncomplete: true` em campos longos.
- **Não faça:** comparar CPF formatado com CPF cru no SQL; normalize antes.
