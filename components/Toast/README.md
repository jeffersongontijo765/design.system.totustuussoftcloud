# Toast

Notificação curta e empilhável do ttscui (`TTSC.Toast.show({…})`), com variantes, aparência, ação/cancelar, barra de tempo, pausa no hover e seis posições.

> Também listado em: **Base › Toasts**.

## Quando usar

- Confirmar uma ação concluída sem tirar o usuário da tela: “Matrícula salva”, “Boleto enviado por e-mail”.
- Erros recuperáveis de uma requisição AJAX (“Não foi possível gerar o boleto”).
- Ação reversível com “Desfazer” por alguns segundos (exclusão suave com `deleted_at`).
- Erros de validação de campo → mensagem inline no formulário, não toast.
- Decisões que exigem resposta (“Excluir 32 matrículas?”) → [Modal](../Modal/README.md) de confirmação.
- Aviso persistente da página (período letivo fechado) → Alert/banner na página, não toast.

## Anatomia

```
.ttsc-toast-container.<posição> (fixed, criado sob demanda no <body>, um por posição)
  └ div.ttsc-toast.ttsc-alert.ttsc-alert-<variante>.ttsc-alert-<aparência>.ttsc-alert-<tamanho>.ttsc-toast-<posição>
       ├ .ttsc-alert-icon        (opção icon)
       ├ .ttsc-alert-title       (opção message)
       ├ .ttsc-alert-toolbar > .ttsc-alert-actions
       │     [data-ttsc-toast-action] [data-ttsc-toast-cancel] [data-ttsc-toast-dismiss].ttsc-alert-close
       └ .ttsc-toast-progress    (opção progress)
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Container | `.ttsc-toast-container` (gerado) | gerado |
| Toast | `.ttsc-toast.ttsc-alert` + `role="status"` + `aria-live="polite"` | gerado |
| Mensagem | `.ttsc-alert-title` | sim (`message` ou `content`) |
| Ícone | `.ttsc-alert-icon` com `<i class="fa-light …">` | recomendado |
| Botões | `[data-ttsc-toast-action]`, `[data-ttsc-toast-cancel]`, `.ttsc-alert-close` | não |
| Tempo | `.ttsc-toast-progress` (`animation-duration` = `duration`) | não |

## Variantes

| Opção | Valores | Uso | Tokens (ponte) |
|---|---|---|---|
| `variant` | `success` · `info` · `warning` · `destructive` (=`error`) · `primary` · `secondary` · `mono` | semântica | `ttsc-success`, `ttsc-info` (ponte TTSC; runtime usa violeta), `ttsc-warning`, `ttsc-danger` |
| `appearance` | `solid` (padrão) · `light` · `outline` | `light` é o padrão do TotusTuus (fundo suave, texto `ttsc-text`) | fundo `color-mix(token 10%, surface)` |
| `size` | `sm` · `md` · `lg` | densidade | — |
| `position` | `top-end` (padrão) · `top-center` · `top-start` · `bottom-end` · `bottom-center` · `bottom-start` | `bottom-center` para salvamento automático | `--ttsc-z-toast` |

## API

`TTSC.Toast` (= `window.ttscToast`, classe estática) — conferido em `src/components/toast/toast.ts`:

| Método | Efeito |
|---|---|
| `TTSC.Toast.show(options)` | cria e retorna `{ id, element, timeoutId, dismiss() }` (exige `message` ou `content`) |
| `TTSC.Toast.close(idOuObjeto)` | fecha com animação `ttsc-toast-out` (250 ms) |
| `TTSC.Toast.clearAll(removeContainers = false)` | fecha todos |
| `TTSC.Toast.config(globais)` | `position`, `duration` (4000), `maxToasts` (5), `offset` (15), `gap` (10), `className`, `classNames` |
| `TTSC.Toast.update(container)` | reposiciona a pilha (uso interno) |

| Opção de `show()` | Padrão | Efeito |
|---|---|---|
| `message` | — | texto (HTML permitido — escape dados do usuário) |
| `content` | — | string HTML, elemento ou função → substitui todo o conteúdo |
| `icon` | — | HTML do ícone |
| `variant` / `appearance` / `size` / `position` | `info` / `solid` / `md` / global | ver Variantes |
| `duration` | global (4000 ms) | tempo até fechar; `important: true` = não fecha sozinho e `aria-modal` |
| `progress` | `false` | barra de tempo |
| `pauseOnHover` | `false` | pausa timer e barra no hover |
| `action` / `cancel` | `false` | `{ label, className, onClick(id) }` — clicar executa e fecha |
| `dismiss` | `true` | botão fechar (×) |
| `role` | `"status"` | use `"alert"` para erros |
| `beep` | `false` | bip curto (Web Audio) |
| `maxToasts` | global | limite por container (o mais antigo sai) |
| `onAutoClose(id)` / `onDismiss(id)` | — | callbacks |
| `className` / `classNames` | — | classes extras (`toast`, `icon`, `message`, `toolbar`, `actions`, `progress`, `container`) |

| Evento (no elemento do toast) | `detail` |
|---|---|
| `ttsc.toast.show` / `show` | `{ id }` |
| `ttsc.toast.shown` / `shown` | `{ id }` |
| `ttsc.toast.hide` / `hide` | `{ id }` |
| `ttsc.toast.hidden` / `hidden` | `{ id }` |

Atenção: scripts legados do app chamam `window.ttscToast(msg, type)` como função; com o ttscui carregado, `ttscToast` é a classe e essa chamada lança erro. Use `TTSC.Toast.show({ message, variant })` (adaptador no JS abaixo).

## Acessibilidade

- O toast nasce com `role="status"`, `aria-live="polite"`, `aria-atomic="true"` e `tabindex="0"`; para erro use `role: 'alert'`.
- Mensagem curta (≤ 2 linhas), com verbo no particípio (“Matrícula salva”), sem depender da cor: sempre ícone + texto.
- Toasts com ação: duração ≥ 6 s + `pauseOnHover`; a ação também deve existir em outro lugar (o usuário pode perder o toast).
- Contraste: aparência `light` mantém texto `ttsc-text` (≥ 12:1) sobre fundo tingido; não use `solid` amarelo com texto branco.
- `prefers-reduced-motion`: desligue `ttsc-toast-in` (CSS abaixo).

## Modelos

### HTML

O toast é criado por JS; a única marcação na view é o gatilho e, opcionalmente, o flash vindo do servidor:

```html
<!-- Flash da sessão (PHP) convertido em toast no load -->
<?php if ($flash = $session->pullFlash()): ?>
<script nonce="<?= $nonce ?>" type="application/json" id="flash-toast"><?= json_encode([
  'message' => $flash['message'],
  'variant' => $flash['type'],   // success | warning | destructive | info
], JSON_HEX_TAG | JSON_HEX_AMP) ?></script>
<?php endif; ?>

<button type="button" class="ttsc-btn ttsc-btn-primary" id="btn-save-enrollment">
  <i class="fa-light fa-floppy-disk"></i> Salvar matrícula
</button>
```

### CSS

```css
/* Ponte TTSC: info em azul do produto e aparência light com tokens */
.ttsc-alert-info.ttsc-alert-light {
  background-color: color-mix(in oklab, var(--ttsc-info) 10%, var(--ttsc-surface));
  border-color: color-mix(in oklab, var(--ttsc-info) 35%, transparent);
  color: var(--ttsc-text);
}
.ttsc-alert-info.ttsc-alert-light .ttsc-alert-icon { color: var(--ttsc-info-text); }
.ttsc-toast-container { z-index: var(--ttsc-z-toast); }
.ttsc-toast-progress { background-color: var(--ttsc-accent); }

/* Botão de ação como link sublinhado */
.ttsc-toast [data-ttsc-toast-action] { font-weight: 600; text-decoration: underline; background: none; border: 0; color: inherit; cursor: pointer; }

@media (prefers-reduced-motion: reduce) { .ttsc-toast { animation: none; opacity: 1; } }
```

### JS

```js
// assets/js/core/ttsc.notify.js — padrões do TotusTuus + adaptador do legado
TTSC.Toast.config({ position: 'top-end', duration: 4000, maxToasts: 4, offset: 16, gap: 8 });

var ICONS = { success: 'fa-circle-check', info: 'fa-circle-info', warning: 'fa-triangle-exclamation', destructive: 'fa-circle-xmark' };
function escapeHtml(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

window.notify = function (message, variant, extra) {
  variant = variant === 'error' ? 'destructive' : (variant || 'success');
  return TTSC.Toast.show(Object.assign({
    message: escapeHtml(message),
    variant: variant,
    appearance: 'light',
    icon: '<i class="fa-light ' + (ICONS[variant] || ICONS.info) + '"></i>',
    role: variant === 'destructive' ? 'alert' : 'status',
    progress: true,
    pauseOnHover: true,
  }, extra || {}));
};
// Scripts antigos chamam ttscToast(msg, tipo): redirecione para notify
window.showToast = function (msg, type) { return window.notify(msg, type); };

// Flash do servidor
var flash = document.getElementById('flash-toast');
if (flash) { var f = JSON.parse(flash.textContent); notify(f.message, f.variant); }

// Exclusão com desfazer (soft delete)
async function deleteEnrollment(uuid, code) {
  await fetch('/app/academic/enrollments/' + uuid, { method: 'DELETE', headers: { 'X-CSRF-Token': csrf } });
  notify('Matrícula ' + code + ' excluída.', 'mono', {
    appearance: 'solid', duration: 6000,
    icon: '<i class="fa-light fa-trash"></i>',
    action: {
      label: 'Desfazer',
      onClick: function () {
        fetch('/app/academic/enrollments/' + uuid + '/restore', { method: 'POST', headers: { 'X-CSRF-Token': csrf } })
          .then(function () { notify('Matrícula restaurada.', 'success'); });
      },
    },
  });
}

document.addEventListener('ttsc.toast.hidden', function (e) { console.debug('toast fechado', e.detail.id); }, true);
```

### SQL

Toasts não são persistidos; quando o aviso vem do servidor (ex.: notificações novas desde o último polling), a origem é `notification_items`:

```sql
-- GET /app/notifications/new?since=…  → cada linha vira um toast
SELECT n.id, n.type, n.priority, n.title, n.action_url, n.created_at
  FROM notification_items n
 WHERE n.user_id = :user_uuid
   AND n.is_read = 0
   AND n.created_at > :since
 ORDER BY n.created_at ASC
 LIMIT 5;

-- Clique na ação "Abrir" do toast marca como lida
UPDATE notification_items
   SET is_read = 1, read_at = CURRENT_TIMESTAMP
 WHERE id = :id
   AND user_id = :user_uuid;
```

O controller responde JSON; o JS mapeia `priority` para `variant` (`high` → `warning`, `critical` → `destructive`, demais → `info`) e cria `action: { label: 'Abrir', onClick }` com `action_url`. No máximo 5 por polling para não inundar a tela.

## Faça / Não faça

- **Faça:** `appearance: 'light'` + ícone + texto curto; `role: 'alert'` só para erro.
- **Faça:** escape o texto vindo do usuário (o `message` aceita HTML).
- **Não faça:** chamar `window.ttscToast(msg, tipo)` como função — use `TTSC.Toast.show`/`notify`.
- **Não faça:** toast para erro de validação de campo nem para confirmações que exigem decisão.
