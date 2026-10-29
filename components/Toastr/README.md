# Toastr

Notificações toastr 2.1.4 (jQuery) — sucesso, informação, alerta e erro — com tema ligado aos tokens, ícones Font Awesome light e wrapper que escapa o texto; mantido para telas legadas, **o padrão do chassi é o [Toast](../Toast/README.md) nativo (`TTSC.Toast.show`)**.

## Quando usar

- Telas legadas que já usam `toastr.*` (e jQuery) e ainda não migraram — mantenha o visual consistente com este tema.
- Plugins jQuery que disparam `toastr` internamente.
- **Para código novo, use o [Toast](../Toast/README.md) do ttscui**: sem jQuery, já no tema, com variantes (`success`, `destructive`, `warning`, `info`…), ação/cancelar, barra de tempo e posições. Compare:

| Critério | Toastr | Toast (ttscui) |
|---|---|---|
| Dependência | jQuery + toastr (≈ 6 KB) | nenhuma (runtime) |
| API | `toastr.success(msg, título, opts)` | `TTSC.Toast.show({ message, variant, … })` |
| Tema | CSS de override (este README) | nativo (`ttsc-alert-*`) |
| Ação no toast | HTML manual | `action` / `cancel` |
| HTML | `escapeHtml: false` por padrão (risco XSS) | texto |

- **Não use** toast (qualquer um) para erros de validação de campo (mostre no campo) nem para confirmações destrutivas ([SweetAlert](../SweetAlert/README.md)).

## Anatomia

```
#toast-container.toast-top-right  (target; z --ttsc-z-toast)
└── .toast.ttsc-toastr-success  [role=alert|status, aria-live]
    ├── button.toast-close-button  (fa-xmark, aria-label)
    ├── .toast-title    (ícone fa-circle-check) "Matrícula salva"
    ├── .toast-message  "Matrícula MAT-2026-0142 confirmada."
    └── .toast-progress (progressBar)
```

| Parte | Classe | Obrigatório |
|---|---|---|
| Contêiner | `#toast-container` + `positionClass` | gerado |
| Toast | `.toast` + classe do tipo via `iconClasses` (`ttsc-toastr-*`) | gerado |
| Título | `.toast-title` (ícone + texto) | recomendado |
| Mensagem | `.toast-message` | sim |
| Fechar | `.toast-close-button` (`closeHtml` com `aria-label`) | sim |
| Progresso | `.toast-progress` | não |

## Variantes

| Tipo | Método | Classe | Ícone | Tokens (barra lateral / ícone) |
|---|---|---|---|---|
| Sucesso | `toastr.success` | `ttsc-toastr-success` | `fa-circle-check` | `ttsc-success` / `ttsc-accent-text` |
| Informação | `toastr.info` | `ttsc-toastr-info` | `fa-circle-info` | `ttsc-info` / `ttsc-info-text` |
| Alerta | `toastr.warning` | `ttsc-toastr-warning` | `fa-triangle-exclamation` | `ttsc-warning` / `ttsc-warning-text` |
| Erro | `toastr.error` | `ttsc-toastr-error` | `fa-circle-xmark` | `ttsc-danger` / `ttsc-danger-text` |

Superfície: `ttsc-surface` + `ttsc-border` + `ttsc-shadow-xl`; título `ttsc-text`; mensagem `ttsc-text-2` — nada das cores sólidas e PNGs do `toastr.css`.

## API

### Opções (`toastr.options`)

| Opção | Padrão | Valor TTSC |
|---|---|---|
| `positionClass` | `'toast-top-right'` | `'toast-top-right'` (igual ao Toast nativo) |
| `target` | `'body'` | `'body'` |
| `timeOut` / `extendedTimeOut` | `5000` / `1000` | `5000` / `2000` (erro: `0` = fixo) |
| `closeButton` / `closeHtml` | `false` / `&times;` | `true` / botão com `fa-xmark` + `aria-label` |
| `progressBar` | `false` | `true` |
| `newestOnTop` / `preventDuplicates` | `true` / `false` | `true` / `true` |
| `escapeHtml` | `false` | `false`, **mas** o wrapper `notify()` escapa tudo |
| `iconClasses` | `{ success: 'toast-success', … }` | `{ success: 'ttsc-toastr-success', … }` (sem PNG) |
| `tapToDismiss` / `closeOnHover` | `true` / `true` | padrão |
| `onShown`, `onHidden`, `onclick`, `onCloseClick` | — | ganchos |

### Métodos

| Método | Uso |
|---|---|
| `toastr.success / info / warning / error(message, title?, overrides?)` | mostrar (retorna o `$toast`) |
| `toastr.clear($toast?)` | remover com animação |
| `toastr.remove($toast?)` | remover imediatamente |
| `toastr.subscribe(fn)` | observar mostrar/esconder |

## Acessibilidade

- toastr usa `aria-live="polite"` (info/sucesso) e `assertive` (erro/alerta); não force `assertive` em sucesso.
- Erros ficam **sem expirar** (`timeOut: 0`) — o usuário precisa de tempo para ler; `closeOnHover` pausa.
- Botão de fechar com `aria-label="Fechar notificação"`; ícone com `aria-hidden`.
- O tipo é dado por ícone **e** título (“Falha na geração”), não só pela cor da barra.
- Contraste: título `ttsc-text`, mensagem `ttsc-text-2` sobre `ttsc-surface` (≥ 7:1 nos dois temas).

## Modelos

### HTML

```html
<!-- Só em telas legadas que já carregam jQuery -->
<link rel="stylesheet" href="/assets/vendors/toastr/toastr.min.css">
<link rel="stylesheet" href="/assets/css/ttsc.toastr.css">
<script src="/assets/vendors/jquery/jquery.min.js"></script>
<script src="/assets/vendors/toastr/toastr.min.js"></script>
<script src="/assets/js/core/ttsc.toastr.js"></script>

<!-- Mensagem flash do PHP repassada ao toast -->
<?php if ($flash = $this->session()->getFlash('success')): ?>
  <script>document.addEventListener('DOMContentLoaded', () => TTSC.notify('success', <?= json_encode($flash, JSON_HEX_TAG | JSON_HEX_APOS | JSON_HEX_QUOT | JSON_HEX_AMP) ?>, 'Tudo certo'));</script>
<?php endif; ?>
```

### CSS

```css
/* assets/css/ttsc.toastr.css */
#toast-container { z-index: var(--ttsc-z-toast); }
#toast-container > .toast {
  background-image: none !important; background-color: var(--ttsc-surface); color: var(--ttsc-text-2);
  border: 1px solid var(--ttsc-border); border-left: 3px solid var(--tc, var(--ttsc-info));
  border-radius: var(--ttsc-radius-surface); box-shadow: var(--ttsc-shadow-xl);
  opacity: 1; padding: 12px 14px; width: 340px; font-size: 12px;
}
#toast-container .toast-title { display: flex; align-items: center; gap: 8px; color: var(--ttsc-text); font-size: 13px; font-weight: 600; }
#toast-container .toast-title i { color: var(--tc-text, var(--ttsc-info-text)); font-size: 15px; }
#toast-container .toast-message { color: var(--ttsc-text-2); line-height: 1.5; padding-left: 23px; }
#toast-container .toast-close-button { color: var(--ttsc-text-muted); text-shadow: none; opacity: 1; font-size: 14px; }
#toast-container .toast-close-button:hover, #toast-container .toast-close-button:focus { color: var(--ttsc-text); }
#toast-container .toast-progress { background: var(--tc, var(--ttsc-info)); opacity: .6; height: 3px; }
.ttsc-toastr-success { --tc: var(--ttsc-success); --tc-text: var(--ttsc-accent-text); }
.ttsc-toastr-info    { --tc: var(--ttsc-info);    --tc-text: var(--ttsc-info-text); }
.ttsc-toastr-warning { --tc: var(--ttsc-warning); --tc-text: var(--ttsc-warning-text); }
.ttsc-toastr-error   { --tc: var(--ttsc-danger);  --tc-text: var(--ttsc-danger-text); }
```

### JS

```js
// assets/js/core/ttsc.toastr.js — wrapper do toastr com escape, ícones e tema
(function (w, $) {
  toastr.options = {
    positionClass: 'toast-top-right',
    newestOnTop: true,
    closeButton: true,
    progressBar: true,
    timeOut: 5000,
    extendedTimeOut: 2000,
    preventDuplicates: true,
    escapeHtml: false, // o wrapper escapa; o HTML é só o ícone
    closeHtml: '<button type="button" aria-label="Fechar notificação"><i class="fa-light fa-xmark"></i></button>',
    iconClasses: { success: 'ttsc-toastr-success', info: 'ttsc-toastr-info', warning: 'ttsc-toastr-warning', error: 'ttsc-toastr-error' },
  };
  const ICON = { success: 'fa-circle-check', info: 'fa-circle-info', warning: 'fa-triangle-exclamation', error: 'fa-circle-xmark' };
  const esc = (s) => $('<div>').text(String(s ?? '')).html();

  function notify(type, message, title, overrides) {
    const opts = Object.assign(type === 'error' ? { timeOut: 0, extendedTimeOut: 0 } : {}, overrides || {});
    const head = title ? `<i class="fa-light ${ICON[type]}" aria-hidden="true"></i><span>${esc(title)}</span>` : '';
    return toastr[type](esc(message), head, opts);
  }

  w.TTSC = w.TTSC || {};
  // Ponte de migração: se o runtime ttscui estiver presente, prefira o Toast nativo
  w.TTSC.notify = function (type, message, title, overrides) {
    if (w.TTSC.Toast && !(overrides && overrides.forceToastr)) {
      const variant = { success: 'success', info: 'info', warning: 'warning', error: 'destructive' }[type];
      return w.TTSC.Toast.show({ message: title ? `${title}: ${message}` : message, variant });
    }
    return notify(type, message, title, overrides);
  };
})(window, jQuery);

// Uso
TTSC.notify('success', 'Matrícula MAT-2026-0142 confirmada.', 'Matrícula salva');
TTSC.notify('error', 'Não foi possível gerar os boletos. Tente novamente.', 'Falha na geração');
```

### SQL

O toast não persiste nada; as notificações assíncronas vêm de `notification_items` (polling a cada 60 s) e são marcadas como lidas depois de exibidas:

```sql
-- Novas notificações do usuário desde o último polling
SELECT n.id, n.type, n.priority, n.title, n.body, n.action_url, n.created_at
  FROM notification_items n
 WHERE n.user_id = :user_uuid
   AND n.is_read = 0
   AND n.created_at > :since          -- timestamp do último polling
 ORDER BY n.created_at
 LIMIT 5;

-- Após exibir
UPDATE notification_items
   SET is_read = 1, read_at = NOW()
 WHERE user_id = :user_uuid
   AND id IN (:id_1, :id_2);
```

O endpoint devolve o JSON; o JS mapeia `priority` → tipo (`critical` → `error`, `high` → `warning`, demais → `info`) e chama `TTSC.notify`. Mais de 5 novas: mostre um único toast “Você tem 12 notificações” com link.

## Faça / Não faça

- **Faça:** usar o wrapper `TTSC.notify` (escape + ícone) em vez de chamar `toastr.*` com HTML cru.
- **Faça:** erros sem expirar e com título explícito; sucesso em 5 s.
- **Faça:** migrar para `TTSC.Toast` ao tocar na tela.
- **Não faça:** passar dados do usuário para `toastr.*` com `escapeHtml: false` sem escapar.
- **Não faça:** usar as cores sólidas e ícones PNG do `toastr.css` (ilegíveis no tema escuro, fora do sistema).
- **Não faça:** empilhar mais de 3 toasts; `preventDuplicates: true`.
