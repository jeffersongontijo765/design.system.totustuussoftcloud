# InputGroup

Agrupa um [Input](../Input/README.md) com complementos externos (`.ttsc-input-group` + `.ttsc-input-addon`) como R$, %, @ ou um botão anexado, fundindo bordas e raios.

## Quando usar

- A unidade ou prefixo faz parte da leitura do valor: **R$** na mensalidade, **%** no desconto da bolsa, **@** no usuário, domínio `@escola.com.br` no e-mail institucional.
- Uma ação curta pertence ao campo: "Buscar CEP", "Gerar código", "Copiar link".
- Ícone decorativo **dentro** da borda (lupa de busca) → use o `div.ttsc-input` com ícone do [Input](../Input/README.md), não um addon.
- Várias ações ou menu → coloque um [Button](../Button/README.md) ao lado, fora do grupo.

## Anatomia

```
┌──────┬───────────────────────┬────────────┐
│  R$  │ 1.250,00              │  / mês     │   .ttsc-input-group
└──────┴───────────────────────┴────────────┘
 addon        .ttsc-input          addon  (ou .ttsc-btn)
```

| Parte | Classe | Obrigatório |
|---|---|---|
| Container | `div.ttsc-input-group` (flex, `align-items: stretch`) | sim |
| Campo | `input.ttsc-input` (cresce: `flex-grow: 1`, `z-index: 1`) | sim |
| Complemento | `span.ttsc-input-addon` antes e/ou depois do campo | não |
| Complemento só-ícone | `ttsc-input-addon ttsc-input-addon-icon` (sem padding lateral, quadrado) | não |
| Botão anexado | `button.ttsc-btn` (qualquer variante; `-outline` perde a borda de junção) | não |
| Tamanhos | `ttsc-input-addon-sm` / `-lg` junto com `ttsc-input-sm` / `-lg` | não |

Classes confirmadas no `bundle.css`: `.ttsc-input-group`, `.ttsc-input-addon`, `.ttsc-input-addon-sm`, `.ttsc-input-addon-lg`, `.ttsc-input-addon-icon`. As regras de junção usam `:has(+ .ttsc-input)` e `.ttsc-input + .ttsc-input-addon` — **a ordem dos irmãos importa** (addon, input, addon/botão), sem wrappers entre eles.

## Variantes

| Variante | Marcação | Uso | Tokens |
|---|---|---|---|
| Prefixo | `addon + input` | R$, @, https:// | addon: fundo `--muted` → `ttsc-canvas-2`, texto `--secondary-foreground` → `ttsc-text`, borda `--input` |
| Sufixo | `input + addon` | %, kg, h/aula, `@escola.com.br` | idem |
| Prefixo + sufixo | `addon + input + addon` | R$ … / mês | idem |
| Botão anexado | `input + .ttsc-btn` | Buscar CEP, Copiar | variante do botão |
| Pequeno / grande | `-sm` / `-lg` em addon **e** input | toolbar / auth | alturas 28 / 34 / 40px |

## Estados

O estado vem do `.ttsc-input` interno: `disabled`, `readonly`, `aria-invalid="true"` (borda `ttsc-danger`). O addon não muda; para erro, a mensagem vai abaixo do grupo em `.ttsc-form-message` (exibida quando o `.ttsc-form-item` contém `[aria-invalid=true]`).

## API

Sem JavaScript. A formatação de moeda/porcentagem é responsabilidade de [Inputmask](../Inputmask/README.md) ou do `Intl.NumberFormat` (modelo JS abaixo).

## Acessibilidade

- O addon é texto visível mas **não** faz parte do rótulo: diga a unidade no `<label>` ("Valor da mensalidade (R$)") ou via `aria-describedby` apontando para o addon.
- Botão anexado: `type="button"` e rótulo próprio ("Buscar CEP"); só-ícone exige `aria-label`.
- Use `inputmode="decimal"` para valores; o teclado do celular mostra vírgula.
- Texto do addon usa `ttsc-text` sobre `ttsc-canvas-2` (> 12:1 claro, > 10:1 escuro).

## Modelos

### HTML

```html
<!-- Drawer "Bolsa do aluno" — percentual e valor -->
<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="sch-percentage">Percentual de desconto</label>
  <div class="ttsc-input-group">
    <input class="ttsc-input" id="sch-percentage" name="percentage" inputmode="decimal"
           value="<?= $this->e($scholarship['percentage'] ?? '') ?>" aria-describedby="sch-percentage-unit">
    <span class="ttsc-input-addon" id="sch-percentage-unit">%</span>
  </div>
</div>

<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="sch-amount">Valor fixo</label>
  <div class="ttsc-input-group">
    <span class="ttsc-input-addon">R$</span>
    <input class="ttsc-input" id="sch-amount" name="amount" inputmode="decimal" data-ttsc-money placeholder="0,00">
    <span class="ttsc-input-addon">/ mês</span>
  </div>
</div>

<!-- E-mail institucional -->
<div class="ttsc-input-group">
  <span class="ttsc-input-addon ttsc-input-addon-icon"><i class="fa-light fa-at" aria-hidden="true"></i></span>
  <input class="ttsc-input" name="username" aria-label="Usuário" placeholder="ana.souza">
  <span class="ttsc-input-addon">@escola.com.br</span>
</div>

<!-- Botão anexado -->
<div class="ttsc-input-group">
  <input class="ttsc-input" name="zip_code" inputmode="numeric" maxlength="9" aria-label="CEP" placeholder="00000-000">
  <button type="button" class="ttsc-btn ttsc-btn-outline" data-ttsc-cep-lookup>
    <i class="fa-light fa-magnifying-glass"></i> Buscar CEP
  </button>
</div>
```

### CSS

```css
/* Extensão: o addon usa as cores do DS (o bundle usa --muted, que vira cinza fixo no escuro) */
.ttsc-input-group .ttsc-input-addon {
  background-color: var(--ttsc-surface-2);
  color: var(--ttsc-text-2);
  border-color: var(--ttsc-border);
}

/* Extensão: foco do campo destaca o grupo inteiro (o anel do input fica por cima do addon) */
.ttsc-input-group:focus-within .ttsc-input-addon { border-color: var(--ttsc-accent); }

/* Extensão: ícone do addon só-ícone em texto mutado, não preto */
.ttsc-input-group .ttsc-input-addon-icon i { color: var(--ttsc-text-muted); }

/* Extensão: addon com texto secundário (unidades longas) */
.ttsc-input-addon.ttsc-input-addon-muted { color: var(--ttsc-text-muted); font-size: 12px; }
```

### JS

```js
// assets/js/core/ttsc.money.js — máscara simples pt-BR para [data-ttsc-money] dentro de input groups
const brl = new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

export function toCents(text) {
  const digits = String(text).replace(/\D/g, '');
  return digits === '' ? null : parseInt(digits, 10);
}

export function bindMoney(input) {
  const render = () => {
    const cents = toCents(input.value);
    input.value = cents === null ? '' : brl.format(cents / 100);
  };
  input.addEventListener('input', render);
  input.form?.addEventListener('formdata', (event) => {
    // envia "1250.00" para o servidor, não "1.250,00"
    const cents = toCents(input.value);
    event.formData.set(input.name, cents === null ? '' : (cents / 100).toFixed(2));
  });
  render();
}

document.querySelectorAll('[data-ttsc-money]').forEach(bindMoney);

// Botão anexado: busca de CEP
document.querySelectorAll('[data-ttsc-cep-lookup]').forEach((button) => {
  button.addEventListener('click', async () => {
    const input = button.previousElementSibling;
    const cep = input.value.replace(/\D/g, '');
    input.setAttribute('aria-invalid', cep.length === 8 ? 'false' : 'true');
    if (cep.length !== 8) return;
    const res = await fetch(`/api/v1/zip-codes/${cep}`, { headers: { Accept: 'application/json' } });
    if (res.ok) button.dispatchEvent(new CustomEvent('ttsc:cep', { bubbles: true, detail: await res.json() }));
  });
});
```

### SQL

```sql
-- Preenche o drawer de bolsa (tenant): percentual e valor fixo
SELECT s.uuid, s.code, s.student_name, s.scholarship_type,
       s.percentage, s.amount, s.currency, s.status
  FROM student_scholarships s
 WHERE s.uuid = :scholarship_uuid
   AND s.deleted_at IS NULL;

-- Salva (valores já normalizados pelo JS: "15.00", "1250.00")
UPDATE student_scholarships
   SET percentage = :percentage,
       amount     = :amount,
       updated_at = NOW()
 WHERE uuid = :scholarship_uuid
   AND deleted_at IS NULL;
```

O PHP formata `amount` com `number_format($v, 2, ',', '.')` ao escrever o `value` do campo e o addon mostra `currency` (`BRL` → "R$"). O servidor valida `0 ≤ percentage ≤ 100` antes do `UPDATE`.

## Faça / Não faça

- **Faça:** unidade no addon e no rótulo; mesmo tamanho (`-sm`/`-lg`) em addon e input.
- **Faça:** enviar o valor normalizado (ponto decimal) ao servidor.
- **Não faça:** envolver o input em `<div>` dentro do grupo (quebra os seletores de junção); addon como único rótulo; mais de um botão anexado.
