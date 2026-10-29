# Input

Campo de texto de linha única do chassi (`.ttsc-input`), com três tamanhos, versão com ícone interno, estados desabilitado, somente leitura e inválido.

## Quando usar

- Entrada curta e livre: nome do aluno, e-mail, CPF, código da turma, busca em toolbar.
- Com prefixo/sufixo **fora** da borda (R$, %, @, botão anexado) use [InputGroup](../InputGroup/README.md).
- Texto longo (observações da matrícula) → [Textarea](../Textarea/README.md). Lista fechada de opções → [Select](../Select/README.md) ou [Radio](../Radio/README.md).
- Senha → [TogglePassword](../TogglePassword/README.md). Código MFA de 6 dígitos → [PinInput](../PinInput/README.md). Datas: `<input type="date">` (o chassi aplica o datepicker TTSC automaticamente).

## Anatomia

```
Rótulo *                         .ttsc-form-label
┌──────────────────────────────┐
│ [ícone]  valor / placeholder │  input.ttsc-input  ou  div.ttsc-input > i + input
└──────────────────────────────┘
Texto de ajuda / mensagem de erro  .ttsc-form-description / .ttsc-form-message
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Campo | `input.ttsc-input` | sim |
| Tamanho | `ttsc-input-sm` · (padrão 34px) · `ttsc-input-lg` | não |
| Com ícone | `div.ttsc-input` contendo `<i class="fa-light …">` + `<input>` sem classe | não |
| Item de formulário | `div.ttsc-form-item` (coluna, gap 10px) | recomendado |
| Rótulo | `label.ttsc-form-label[for]` | sim |
| Ajuda | `.ttsc-form-description` (some quando há erro) | não |
| Erro | `.ttsc-form-message` (só aparece quando o item contém `[aria-invalid=true]`) | não |

## Variantes

| Variante | Classe | Altura | Uso |
|---|---|---|---|
| Pequeno | `ttsc-input-sm` | 28px | filtros de toolbar, células editáveis de tabela |
| Padrão | — | 34px | formulários de drawer |
| Grande | `ttsc-input-lg` | 40px | telas de login/auth |
| Com ícone | `div.ttsc-input` | herda | busca, e-mail, telefone |

Tokens: borda `--input` → `ttsc-border-strong`; fundo `--background` → `ttsc-surface`; texto `ttsc-text`; placeholder `ttsc-text-muted`; foco `--ring` → `ttsc-accent` (anel 3px a 30%); erro `--destructive` → `ttsc-danger`.

## Estados

| Estado | Como aplicar | Visual |
|---|---|---|
| Foco | automático | borda `ttsc-accent` + anel 3px |
| Desabilitado | `disabled` | opacidade 0,6, cursor bloqueado, **não é enviado** no POST |
| Somente leitura | `readonly` | enviado no POST; fundo `ttsc-canvas-2` (extensão abaixo) |
| Inválido | `aria-invalid="true"` + `aria-describedby` → mensagem | borda/anel `ttsc-danger`, mostra `.ttsc-form-message` |

## API

Sem JavaScript. Atributos HTML relevantes: `type` (`text`, `email`, `tel`, `search`, `number`, `date`), `inputmode` (`numeric` para CPF/CEP), `autocomplete` (`name`, `email`, `tel`), `maxlength`, `required`, `pattern`. Máscaras (CPF, telefone) via Inputmask — ver [Inputmask](../Inputmask/README.md).

## Acessibilidade

- Todo campo tem `<label for>` visível; placeholder não substitui rótulo.
- Erro: `aria-invalid="true"` + `aria-describedby="<id da .ttsc-form-message>"`; a mensagem é texto, não só cor.
- Campo com ícone: o ícone é decorativo (`aria-hidden="true"`); o `<input>` interno recebe o `id` e o rótulo.
- Placeholder usa `ttsc-text-muted` (≥ 4,5:1 nos dois temas); não use `ttsc-meta` para texto.
- Prefira `readonly` a `disabled` quando o valor precisa ser lido por leitor de tela e enviado.

## Modelos

### HTML

```html
<!-- Drawer "Novo aluno" — resources/views/app/partials/academic/student-form.php -->
<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="student-name">Nome completo *</label>
  <input class="ttsc-input" id="student-name" name="name" autocomplete="name" required
         value="<?= $this->e($student['name'] ?? '') ?>" placeholder="Ex.: Ana Beatriz Souza">
</div>

<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="student-email">E-mail</label>
  <div class="ttsc-input">
    <i class="fa-light fa-envelope" aria-hidden="true"></i>
    <input id="student-email" name="email" type="email" autocomplete="email" placeholder="aluno@escola.com.br">
  </div>
</div>

<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="student-cpf">CPF</label>
  <input class="ttsc-input" id="student-cpf" name="cpf" inputmode="numeric" maxlength="14"
         aria-invalid="true" aria-describedby="student-cpf-msg" value="123.456.789-00">
  <div class="ttsc-form-description">Somente números; a máscara é aplicada automaticamente.</div>
  <div class="ttsc-form-message" id="student-cpf-msg">CPF inválido.</div>
</div>

<div class="ttsc-form-item">
  <label class="ttsc-form-label" for="student-code">Matrícula</label>
  <input class="ttsc-input" id="student-code" name="code" readonly value="MAT-2026-00412">
</div>

<!-- Busca compacta de toolbar -->
<div class="ttsc-input ttsc-input-sm w-[220px]">
  <i class="fa-light fa-magnifying-glass" aria-hidden="true"></i>
  <input type="search" name="q" placeholder="Buscar aluno" aria-label="Buscar aluno">
</div>
```

### CSS

```css
/* Ponte (já em bundle.css): o runtime lê estas variáveis */
:root {
  --input: var(--ttsc-border-strong);
  --background: var(--ttsc-surface);
  --ring: var(--ttsc-accent);
  --destructive: var(--ttsc-danger);
}

/* Extensão do chassi: readonly visualmente distinto de editável */
.ttsc-input[readonly],
.ttsc-input:not(input):has(input[readonly]) {
  background-color: var(--ttsc-canvas-2);
  color: var(--ttsc-text-2);
}

/* Mensagem de erro com o tom de TEXTO (contraste garantido no escuro) */
.ttsc-form-message { color: var(--ttsc-danger-text); }
```

### JS

```js
// assets/js/core/ttsc.input-validation.js — liga aria-invalid à validação nativa do navegador
export function bindValidation(form) {
  form.querySelectorAll('input.ttsc-input, .ttsc-input > input').forEach((input) => {
    const msg = input.closest('.ttsc-form-item')?.querySelector('.ttsc-form-message');
    const update = () => {
      const invalid = !input.checkValidity();
      input.setAttribute('aria-invalid', invalid ? 'true' : 'false');
      if (msg) {
        msg.id ||= `${input.id}-msg`;
        input.setAttribute('aria-describedby', msg.id);
        if (invalid && !msg.dataset.fixed) msg.textContent = input.validationMessage;
      }
    };
    input.addEventListener('blur', update);
    input.addEventListener('input', () => input.getAttribute('aria-invalid') === 'true' && update());
  });
  form.addEventListener('submit', (event) => {
    form.querySelectorAll('input').forEach((i) => i.dispatchEvent(new Event('blur')));
    if (!form.checkValidity()) {
      event.preventDefault();
      form.querySelector('[aria-invalid="true"]')?.focus();
    }
  });
}

document.querySelectorAll('form[data-ttsc-crud]').forEach(bindValidation);
```

### SQL

```sql
-- Carrega o aluno para o drawer de edição (tenant). Usuários do tenant ficam em `users`.
SELECT u.uuid, u.code, u.name, u.email, u.cpf, u.phone
  FROM users u
 WHERE u.uuid = :student_uuid
   AND u.deleted_at IS NULL;

-- Unicidade de e-mail antes de salvar (gera aria-invalid no campo quando > 0)
SELECT COUNT(*) AS taken
  FROM users
 WHERE email = :email
   AND uuid <> :student_uuid
   AND deleted_at IS NULL;
```

O controller entrega a linha à view Plates, que escreve cada coluna em `value="<?= $this->e(...) ?>"` (escape obrigatório). Se `taken > 0`, a view recebe `$errors['email']` e renderiza o campo com `aria-invalid="true"` e a mensagem.

## Faça / Não faça

- **Faça:** rótulo visível + `ttsc-form-item`; `ttsc-input-sm` em toolbars e tabelas; `readonly` para códigos gerados.
- **Faça:** `inputmode`/`autocomplete` corretos (teclado numérico para CPF no celular).
- **Não faça:** placeholder como rótulo; erro só com borda vermelha; `disabled` em campo que precisa ir no POST.
