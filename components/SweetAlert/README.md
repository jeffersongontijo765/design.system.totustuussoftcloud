# SweetAlert

Diálogos de confirmação, sucesso e entrada de dados com SweetAlert2 11.14.5 (`sweetalert2.all.min.js`, CSS embutido) — sem estilos próprios de botão (`buttonsStyling: false`) e botões do chassi via `customClass` (`ttsc-btn`).

## Quando usar

- Confirmar ação **destrutiva ou irreversível** antes de chamar o servidor: excluir matrícula, estornar pagamento, encerrar diário.
- Pedir **um** dado curto para concluir a ação: motivo do cancelamento, justificativa de falta.
- Feedback de sucesso que exige atenção (operação em lote concluída) — com `timer`.
- **Não use** para confirmações rotineiras ou mensagens de sucesso comuns: use [Toast](../Toast/README.md) (não bloqueia).
- **Não use** para formulários com mais de 1–2 campos: [Modal](../Modal/README.md) ou [Drawer](../Drawer/README.md) com validação.
- **Não use** `alert()`/`confirm()`/`prompt()` nativos (ainda presentes em `ttsc.smt.kanban.js`).

## Anatomia

```
.swal2-container (fixed, véu --ttsc-scrim)
└── .swal2-popup.ttsc-swal [role=dialog][aria-modal]
    ├── .swal2-icon (warning | success | question | error | info)
    ├── h2.swal2-title         "Excluir a matrícula MAT-2026-0102?"
    ├── .swal2-html-container  consequência em 1–2 frases
    ├── .swal2-input | .swal2-textarea + .swal2-validation-message   (opcional)
    └── .swal2-actions   [Cancelar .ttsc-btn-ghost] [Excluir matrícula .ttsc-btn-destructive]
```

| Parte | Classe / opção | Obrigatório |
|---|---|---|
| Popup | `customClass.popup: 'ttsc-swal'` | sim |
| Confirmar | `customClass.confirmButton: 'ttsc-btn ttsc-btn-primary'` (ou `-destructive`) | sim |
| Cancelar | `customClass.cancelButton: 'ttsc-btn ttsc-btn-ghost'` + `cancelButtonText: 'Cancelar'` | em confirmações |
| Sem estilo próprio | `buttonsStyling: false` | sim |
| Ordem | `reverseButtons: true` (primária à direita, como no rodapé do chassi) | sim |
| Ícone | `icon` | recomendado |

## Variantes

| Variante | Configuração | Botão principal | Tokens do ícone |
|---|---|---|---|
| Confirmação destrutiva | `icon: 'warning'`, `showCancelButton`, `focusCancel: true`, `showLoaderOnConfirm` + `preConfirm` | `ttsc-btn-destructive` | borda `ttsc-warning`, “!” `ttsc-warning-text` |
| Sucesso | `icon: 'success'`, `timer: 2500`, `timerProgressBar` | `ttsc-btn-primary` | `ttsc-success` |
| Input | `input: 'textarea' \| 'text' \| 'select'`, `inputValidator` | `ttsc-btn-primary` | `question` → `ttsc-info` |
| Erro | `icon: 'error'` | `ttsc-btn-primary` (“Entendi”) | `ttsc-danger` |

Superfícies: popup `ttsc-surface` + `ttsc-border` + `ttsc-shadow-xl` + `ttsc-radius-surface`; título `ttsc-text`; texto `ttsc-text-2`; véu `ttsc-scrim`. **Nunca** `confirmButtonColor`/`cancelButtonColor` (cores cruas, ignoram o tema).

## API

### Opções principais (`Swal.fire({...})` / `Swal.mixin({...})`)

| Opção | Uso TTSC |
|---|---|
| `title`, `text` / `html` | título com o objeto (“Excluir a matrícula MAT-2026-0102?”); `html` só com dados escapados |
| `icon` | `warning`, `success`, `question`, `error`, `info` |
| `showCancelButton`, `confirmButtonText`, `cancelButtonText`, `showDenyButton`, `denyButtonText` | textos com verbo no infinitivo |
| `buttonsStyling: false`, `customClass: { popup, title, htmlContainer, confirmButton, cancelButton, denyButton, input }` | tema do chassi |
| `reverseButtons: true`, `focusCancel: true` | segurança em destrutivas |
| `input`, `inputLabel`, `inputPlaceholder`, `inputAttributes`, `inputValidator(value)` | coleta de motivo |
| `showLoaderOnConfirm`, `preConfirm()` | chamada ao servidor dentro do diálogo; retornar `false` ou `Swal.showValidationMessage()` mantém aberto |
| `allowOutsideClick`, `allowEscapeKey` | `() => !Swal.isLoading()` |
| `timer`, `timerProgressBar` | sucesso |
| `target` | contêiner do diálogo (padrão `body`) |
| `didOpen`, `willClose`, `didClose` | ganchos |

### Resultado (Promise)

`{ isConfirmed, isDenied, isDismissed, value, dismiss }` — `dismiss`: `Swal.DismissReason.cancel | backdrop | close | esc | timer`.

### Métodos estáticos

| Método | Uso |
|---|---|
| `Swal.mixin(defaults)` | instância `TtscSwal` com o tema |
| `Swal.isLoading()` / `showLoading()` / `hideLoading()` | estado de carregamento |
| `Swal.showValidationMessage(msg)` / `resetValidationMessage()` | erro do servidor no `preConfirm` |
| `Swal.close()` / `Swal.isVisible()` / `Swal.update({...})` | controle |

## Acessibilidade

- SweetAlert2 cria `role="dialog"`, `aria-modal="true"`, `aria-labelledby` (título) e `aria-describedby` (texto), prende o foco e devolve ao elemento de origem ao fechar.
- Em destrutivas, `focusCancel: true`: Enter acidental não exclui.
- O título diz **o objeto** e o botão diz **a ação** (“Excluir matrícula”, nunca “OK/Sim”).
- Inputs com `inputLabel` ou `inputAttributes['aria-label']`; mensagem de validação em `ttsc-danger-text`.
- Contraste: texto `ttsc-text`/`ttsc-text-2` sobre `ttsc-surface`; botões herdam os pares do [Button](../Button/README.md).

## Modelos

### HTML

```html
<!-- Botão na linha da tabela de matrículas -->
<button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm"
        aria-label="Excluir matrícula <?= $this->e($row['code']) ?>"
        data-ttsc-confirm-delete="/admin/academic/enrollments/<?= $this->e($row['uuid']) ?>"
        data-code="<?= $this->e($row['code']) ?>" data-student="<?= $this->e($row['student_name']) ?>"
        data-class="<?= $this->e($row['class_name']) ?>">
  <i class="fa-light fa-trash"></i>
</button>
<script src="/assets/vendors/sweetalert2/sweetalert2.all.min.js"></script>
```

### CSS

```css
.ttsc-swal.swal2-popup { background: var(--ttsc-surface); color: var(--ttsc-text); border: 1px solid var(--ttsc-border);
  border-radius: var(--ttsc-radius-surface); box-shadow: var(--ttsc-shadow-xl); padding: 20px; width: 26em; font-family: inherit; }
.ttsc-swal .swal2-title { color: var(--ttsc-text); font-size: 17px; font-weight: 600; }
.ttsc-swal .swal2-html-container { color: var(--ttsc-text-2); font-size: 13px; line-height: 1.55; }
.ttsc-swal .swal2-actions { gap: var(--ttsc-space-2); }
.ttsc-swal .swal2-actions .ttsc-btn { margin: 0; }
.ttsc-swal .swal2-input, .ttsc-swal .swal2-textarea { background: var(--ttsc-surface); color: var(--ttsc-text);
  border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control); box-shadow: none; font-size: 13px; }
.ttsc-swal .swal2-input:focus, .ttsc-swal .swal2-textarea:focus { border-color: var(--ttsc-accent-border); box-shadow: 0 0 0 3px var(--ttsc-accent-soft); }
.ttsc-swal .swal2-validation-message { background: transparent; color: var(--ttsc-danger-text); }
.ttsc-swal .swal2-icon.swal2-warning { border-color: var(--ttsc-warning); color: var(--ttsc-warning-text); }
.ttsc-swal .swal2-icon.swal2-success { border-color: var(--ttsc-success); color: var(--ttsc-success); }
.ttsc-swal .swal2-icon.swal2-success [class^=swal2-success-line] { background-color: var(--ttsc-success); }
.ttsc-swal .swal2-icon.swal2-success [class^=swal2-success-circular-line],
.ttsc-swal .swal2-icon.swal2-success .swal2-success-fix { background: var(--ttsc-surface) !important; }
.ttsc-swal .swal2-icon.swal2-question { border-color: var(--ttsc-info); color: var(--ttsc-info-text); }
.swal2-container.swal2-backdrop-show { background: var(--ttsc-scrim); }
```

### JS

```js
// assets/js/core/ttsc.swal.js — requer sweetalert2.all.min.js
export const TtscSwal = Swal.mixin({
  buttonsStyling: false,
  reverseButtons: true,
  cancelButtonText: 'Cancelar',
  customClass: {
    popup: 'ttsc-swal',
    confirmButton: 'ttsc-btn ttsc-btn-primary',
    cancelButton: 'ttsc-btn ttsc-btn-ghost',
    denyButton: 'ttsc-btn ttsc-btn-outline',
  },
});

const token = () => document.querySelector('meta[name="csrf-token"]')?.content || '';
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// Exclusão de matrícula com chamada dentro do diálogo
document.addEventListener('click', async (event) => {
  const btn = event.target.closest('[data-ttsc-confirm-delete]');
  if (!btn) return;
  const { code, student, class: className } = btn.dataset;
  const result = await TtscSwal.fire({
    icon: 'warning',
    title: `Excluir a matrícula ${esc(code)}?`,
    html: `${esc(student)} será removido da turma <b>${esc(className)}</b>. Mensalidades em aberto continuam no financeiro.`,
    showCancelButton: true,
    confirmButtonText: 'Excluir matrícula',
    focusCancel: true,
    customClass: { popup: 'ttsc-swal', confirmButton: 'ttsc-btn ttsc-btn-destructive', cancelButton: 'ttsc-btn ttsc-btn-ghost' },
    showLoaderOnConfirm: true,
    allowOutsideClick: () => !Swal.isLoading(),
    preConfirm: async () => {
      const res = await fetch(btn.dataset.ttscConfirmDelete, { method: 'DELETE', headers: { 'X-CSRF-TOKEN': token(), Accept: 'application/json' } });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        Swal.showValidationMessage(body.message || 'Não foi possível excluir a matrícula.');
        return false;
      }
      return true;
    },
  });
  if (result.isConfirmed) {
    btn.closest('tr')?.remove();
    TtscSwal.fire({ icon: 'success', title: 'Matrícula excluída', text: 'O histórico foi mantido para auditoria.', confirmButtonText: 'Fechar', timer: 2500, timerProgressBar: true });
  }
});

// Cancelar solicitação de matrícula pedindo o motivo
export async function cancelEnrollmentRequest(uuid) {
  const { isConfirmed, value } = await TtscSwal.fire({
    icon: 'question',
    title: 'Cancelar a solicitação?',
    input: 'textarea',
    inputLabel: 'Motivo (visível ao responsável)',
    inputAttributes: { maxlength: 500 },
    showCancelButton: true,
    confirmButtonText: 'Cancelar solicitação',
    cancelButtonText: 'Voltar',
    inputValidator: (v) => (!v || v.trim().length < 10 ? 'Descreva o motivo com ao menos 10 caracteres.' : undefined),
  });
  if (!isConfirmed) return false;
  const res = await fetch(`/admin/enrollment/requests/${encodeURIComponent(uuid)}/cancel`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRF-TOKEN': token() },
    body: JSON.stringify({ reason: value.trim() }),
  });
  return res.ok;
}
```

### SQL

O diálogo mostra o impacto antes de confirmar e o servidor executa a ação; ambas as escritas são soft delete / mudança de status com histórico:

```sql
-- Dados exibidos na confirmação
SELECT e.code, s.name AS student_name, cl.name AS class_name
  FROM enrollments e
  LEFT JOIN users s    ON s.uuid = e.student_uuid
  LEFT JOIN classes cl ON cl.uuid = e.class_uuid
 WHERE e.uuid = :enrollment_uuid
   AND e.unit_uuid = :unit_uuid
   AND e.deleted_at IS NULL;

-- Exclusão confirmada (soft delete)
UPDATE enrollments
   SET deleted_at = NOW(), updated_at = NOW()
 WHERE uuid = :enrollment_uuid
   AND unit_uuid = :unit_uuid
   AND deleted_at IS NULL;

-- Cancelamento com motivo (input do diálogo) + histórico
UPDATE enrollment_requests
   SET status = 'cancelled', rejection_reason = :reason, reviewed_by = :user_uuid, reviewed_at = NOW()
 WHERE uuid = :request_uuid
   AND deleted_at IS NULL
   AND status IN ('submitted', 'pending_review');

INSERT INTO enrollment_request_history
       (uuid, request_uuid, action, old_status, new_status, actor_uuid, actor_name, actor_type, details)
VALUES (:uuid, :request_uuid, 'cancelled', :old_status, 'cancelled', :user_uuid, :user_name, 'admin', :reason);
```

O controller responde `204` (ou `422 {"message": …}`, mostrado por `Swal.showValidationMessage`) e roda as duas escritas do cancelamento na mesma transação.

## Faça / Não faça

- **Faça:** `buttonsStyling: false` + `customClass` com `ttsc-btn`; `reverseButtons: true`.
- **Faça:** destrutiva com `ttsc-btn-destructive`, `focusCancel` e o nome do objeto no título.
- **Faça:** chamar o servidor no `preConfirm` e mostrar erro no próprio diálogo.
- **Não faça:** `confirmButtonColor`/`cancelButtonColor` nem `html` com dados não escapados.
- **Não faça:** empilhar dois SweetAlerts ou usar para avisos que um [Toast](../Toast/README.md) resolve.
- **Não faça:** “Tem certeza?” genérico com botões “Sim/Não”.
