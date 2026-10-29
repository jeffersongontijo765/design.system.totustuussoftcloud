# Dismiss

Botão que fecha um elemento com fade (`data-ttsc-dismiss="#alvo"`), removendo-o do DOM (`mode: remove`) ou apenas escondendo-o com `.hidden` (`mode: hide`) para reabrir depois.

## Quando usar

- Fechar alertas e avisos informativos (“Rematrícula aberta até 20/12”), banners do portal.
- Remover um filtro aplicado representado por [Badge](../Badge/README.md) (`ttsc-badge-btn`).
- Esconder temporariamente um card de dica do dashboard (mode `hide`), com opção “Mostrar dicas” para trazer de volta.
- Fechar modal/drawer: **não** use dismiss — use `data-ttsc-modal-dismiss` ([Modal](../Modal/README.md)) / `data-ttsc-drawer-dismiss` ([Drawer](../Drawer/README.md)), que cuidam de backdrop e foco.
- Avisos que exigem ação (mensalidade vencida, documento pendente) não devem ser dispensáveis.

## Anatomia

```
┌ #aviso-rematricula  .ttsc-alert ─────────────────────────┐
│ (i) Rematrícula 2027.1 aberta até 20/12          [ x ]   │  ← button[data-ttsc-dismiss="#aviso-rematricula"]
└──────────────────────────────────────────────────────────┘
        clique → opacity 0 (transição) → remove()  ou  .hidden
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Gatilho | `button[data-ttsc-dismiss="#id"]` + `aria-label` | sim |
| Alvo | elemento `#id` (alerta, badge, card) com `transition: opacity` (classe `ttsc-dismissible`, extensão) | sim |
| Modo | `data-ttsc-dismiss-mode="remove"` (padrão) · `"hide"` | não |
| Ícone | `<i class="fa-light fa-xmark">` (`.ttsc-alert-close` / `.ttsc-badge-btn`) | não |

## Variantes

| Variante | Configuração | Uso | Tokens |
|---|---|---|---|
| Remover | `mode="remove"` (padrão) | filtro aplicado, notificação lida | — |
| Esconder | `mode="hide"` | dica reabrível, banner por sessão | `.hidden` |
| Sem interromper | `data-ttsc-dismiss-interrupt="false"` | quando outro ouvinte de clique no pai precisa do evento | — |
| Alerta | `.ttsc-alert.ttsc-alert-info` + `.ttsc-alert-close` | avisos | fundo tonal `ttsc-info` 8%, texto `ttsc-text`, ícone `ttsc-info-text` |

## API

Opções (`data-ttsc-dismiss-<opção>` no gatilho):

| Atributo / opção | Padrão | Efeito |
|---|---|---|
| `data-ttsc-dismiss="#id"` | — | seletor do alvo (ou opção `target`) |
| `mode` | `remove` | `remove` tira do DOM; `hide` adiciona `hiddenClass` |
| `hiddenClass` | `hidden` | classe usada no `mode: hide` |
| `interrupt` | `true` | chama `stopPropagation()` no clique |

Métodos (`ttscDismiss.getInstance(botao)` / `TTSC.Dismiss.getOrCreateInstance(botao, opts)`):

| Método | Descrição |
|---|---|
| `dismiss()` | executa o fechamento (ignorado durante a animação) |
| `getTargetElement()` | elemento alvo |

Eventos (CustomEvent no **gatilho**, `bubbles`):

| Evento | Quando | Cancelável |
|---|---|---|
| `dismiss` | antes do fade | sim (`event.detail.payload.cancel = true`) |
| `dismissed` | após remover/esconder | não |

Para reexibir um alvo em `mode: hide`, remova a classe: `alvo.classList.remove('hidden')` (a opacidade já volta ao normal).

## Acessibilidade

- Gatilho `<button type="button">` com `aria-label` específico (“Fechar aviso de rematrícula”, “Remover filtro Turno: Noite”).
- Após remover, mova o foco para um elemento estável (título da seção ou próximo item), pois o botão focado deixa de existir.
- Alertas usam `role="status"` (informativos) ou `role="alert"` (urgentes, que não devem ser dispensáveis).
- Respeite `prefers-reduced-motion`: a extensão CSS zera a transição; o módulo usa a duração computada, então o fechamento fica instantâneo.
- O “x” fica em `ttsc-text-muted` (≥4,5:1) e ganha `ttsc-text` no hover/foco.

## Modelos

### HTML

```html
<!-- Aviso dispensável (persistido como lido) -->
<?php foreach ($notices as $n): ?>
<div class="ttsc-alert ttsc-alert-info ttsc-dismissible" id="aviso-<?= $this->e($n['id']) ?>" role="status">
  <div class="ttsc-alert-icon"><i class="fa-light fa-circle-info"></i></div>
  <div class="ttsc-alert-content">
    <div class="ttsc-alert-title"><?= $this->e($n['title']) ?></div>
    <div class="ttsc-alert-description"><?= $this->e($n['body']) ?></div>
  </div>
  <button type="button" class="ttsc-alert-close" data-ttsc-dismiss="#aviso-<?= $this->e($n['id']) ?>"
          data-notification-id="<?= $this->e($n['id']) ?>" aria-label="Fechar aviso: <?= $this->e($n['title']) ?>">
    <i class="fa-light fa-xmark"></i>
  </button>
</div>
<?php endforeach; ?>

<!-- Dica reabrível (mode hide) -->
<div class="ttsc-card ttsc-dismissible" id="dica-kanban">
  <div class="ttsc-card-content flex items-center gap-3">
    <i class="fa-light fa-lightbulb"></i> Arraste os cards para mudar a etapa da matrícula.
    <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm ms-auto"
            data-ttsc-dismiss="#dica-kanban" data-ttsc-dismiss-mode="hide" aria-label="Esconder dica">
      <i class="fa-light fa-xmark"></i>
    </button>
  </div>
</div>
<button type="button" class="ttsc-link ttsc-link-sm" data-show-tip="#dica-kanban">Mostrar dica</button>
```

### CSS

```css
/* Extensão TTSC: o módulo espera a transição de opacidade do alvo antes de remover */
.ttsc-dismissible { transition: opacity .2s ease; }
@media (prefers-reduced-motion: reduce) { .ttsc-dismissible { transition: none; } }

/* Alerta informativo com tokens */
.ttsc-alert.ttsc-alert-info { background: color-mix(in oklab, var(--ttsc-info) 8%, var(--ttsc-surface)); border: 1px solid color-mix(in oklab, var(--ttsc-info) 30%, transparent); color: var(--ttsc-text); }
.ttsc-alert.ttsc-alert-info .ttsc-alert-icon { color: var(--ttsc-info-text); }
.ttsc-alert-close, .ttsc-badge-btn { color: var(--ttsc-text-muted); background: none; border: 0; cursor: pointer; }
.ttsc-alert-close:hover, .ttsc-alert-close:focus-visible { color: var(--ttsc-text); }
```

### JS

```js
// Marca a notificação como lida ao dispensar e devolve o foco
document.addEventListener('dismissed', async (event) => {
  const trigger = event.target;
  const id = trigger.dataset && trigger.dataset.notificationId;
  document.querySelector('#avisos-titulo')?.focus();
  if (!id) return;
  await fetch(`/api/v1/notifications/${encodeURIComponent(id)}/read`, {
    method: 'POST',
    headers: { 'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content },
  });
});

// Impede dispensar enquanto o upload do anexo ainda está em andamento
document.addEventListener('dismiss', (event) => {
  const target = TTSC.Dismiss.getInstance(event.target)?.getTargetElement();
  if (target && target.querySelector('[aria-busy="true"]')) event.detail.payload.cancel = true;
});

// Reabrir dica escondida (mode: hide)
document.querySelectorAll('[data-show-tip]').forEach((btn) => {
  btn.addEventListener('click', () => document.querySelector(btn.dataset.showTip).classList.remove('hidden'));
});

// Dismiss criado em JS para alertas injetados via AJAX
export function addDismissible(alertEl) {
  const btn = alertEl.querySelector('[data-ttsc-dismiss]');
  TTSC.Dismiss.getOrCreateInstance(btn, { mode: 'remove' });
}
```

### SQL

O dismiss em si não persiste nada; quando o alvo é uma notificação, o fechamento marca o item como lido em `notification_items`:

```sql
-- Avisos não lidos do usuário (alimentam os alertas dispensáveis)
SELECT n.id, n.type, n.priority, n.title, n.body, n.action_url, n.created_at
  FROM notification_items n
 WHERE n.tenant_id = :tenant_id
   AND n.user_id = :user_uuid
   AND n.is_read = 0
   AND n.resolved = 0
 ORDER BY FIELD(n.priority, 'urgent', 'high', 'normal', 'low'), n.created_at DESC
 LIMIT 5;

-- POST /api/v1/notifications/{id}/read (disparado no evento "dismissed")
UPDATE notification_items
   SET is_read = 1, read_at = NOW()
 WHERE id = :id AND user_id = :user_uuid AND tenant_id = :tenant_id;
```

O controller passa `$notices` para a view; avisos com `priority = 'urgent'` são renderizados **sem** botão de dismiss (exigem ação em `action_url`).

## Faça / Não faça

- **Faça:** `mode: hide` para coisas que o usuário pode querer de volta; `remove` para o que é descartável.
- **Faça:** `transition: opacity` no alvo (classe `ttsc-dismissible`).
- **Faça:** persistir no servidor quando o aviso não deve voltar no próximo login.
- **Não faça:** usar `data-ttsc-dismiss` para fechar modal ou drawer.
- **Não faça:** permitir dispensar avisos de bloqueio/urgentes.
