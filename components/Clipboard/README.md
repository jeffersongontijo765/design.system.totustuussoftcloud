# Clipboard

Copiar para a área de transferência com um clique — código de matrícula, link de convite, chave PIX — usando o **Clipboard do ttscui** (`data-ttsc-clipboard`, recomendado) ou **clipboard.js 2.0.11** (`data-clipboard-*`, alternativa já presente no repo).

## Quando usar

- Valores que o usuário vai colar em outro lugar: código da matrícula, link de convite do responsável, chave/código PIX, token de integração.
- Ao lado de um valor somente leitura (`readonly`), nunca no lugar de um campo editável.
- **Não use** para compartilhar com envio real (e-mail/WhatsApp) — ofereça a ação de envio.
- **Não use** para segredos permanentes (senhas): mostre uma vez e ofereça copiar só no momento da criação.

## Recomendação

**Use o ttscui (`data-ttsc-clipboard`).** Já vem no bundle (`TTSC.init()` inicializa), usa `navigator.clipboard.writeText` com fallback `execCommand('copy')`, aplica `copiedClass` sozinho e emite eventos no padrão `ttsc.*`. O clipboard.js (`assets/vendors/clipboard/clipboard.min.js`) só se justifica em páginas legadas que já o carregam; não adicione as duas bibliotecas na mesma tela.

| Critério | ttscui Clipboard | clipboard.js 2.0.11 |
|---|---|---|
| Dependência extra | nenhuma (bundle) | +9 KB |
| API | Clipboard API assíncrona + fallback | `execCommand` (seleção) |
| Feedback visual | `copiedClass` automático | manual no evento |
| Recortar (`cut`) | só `input/textarea` | sim |
| Eventos | `ttsc.clipboard.success/error` (`detail.payload`) | `success/error` (`e.text`, `e.trigger`) |

## Anatomia

```
┌ MAT-2026-0412  [copiar] ┐        valor + botão só-ícone
[ https://…/convite/RSP-8F2K7Q ][ Copiar ]   input readonly + botão
                                 ↳ .ttsc-clipboard-copied → "Copiado" por 1,5 s
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Gatilho | `button[data-ttsc-clipboard="true"]` | sim |
| Origem fixa | `data-ttsc-clipboard-text="…"` | um dos dois |
| Origem por alvo | `data-ttsc-clipboard-target="#input"` (lê `value` ou `textContent`) | um dos dois |
| Feedback | `data-ttsc-clipboard-copied-class="ttsc-clipboard-copied"` + spans `.cb-idle`/`.cb-done` | recomendado |
| Status | elemento `role="status" aria-live="polite"` | recomendado |

## Estados

| Estado | Visual |
|---|---|
| Parado | ícone `fa-copy` + “Copiar” |
| Copiado | classe `ttsc-clipboard-copied`: ícone `fa-check`, texto “Copiado” em `ttsc-accent-text`, borda `ttsc-accent-border` (removida após 1,5 s pelo seu JS) |
| Erro | mensagem `ttsc-danger-text`: “Não foi possível copiar. Selecione o texto e use Ctrl+C.” |

## API

### ttscui (`src/components/clipboard/clipboard.ts`)

| Atributo `data-ttsc-clipboard-*` | Padrão | Descrição |
|---|---|---|
| `text` | `""` | texto fixo a copiar (tem prioridade sobre `target`) |
| `target` | `""` | seletor do elemento de origem |
| `action` | `copy` | `copy` ou `cut` (cut só em `input/textarea`) |
| `copied-class` | `""` | classe adicionada ao gatilho no sucesso |
| `success-event` | `ttsc.clipboard.success` | nome do evento de sucesso |
| `error-event` | `ttsc.clipboard.error` | nome do evento de erro |

| Método | Descrição |
|---|---|
| `ttscClipboard.getInstance(el)` / `getOrCreateInstance(el, cfg)` | instância |
| `instance.dispose()` | remove o listener |
| `instance.on('ttsc.clipboard.success', fn)` | handler interno |

| Evento (`CustomEvent` no gatilho, `bubbles`) | `event.detail.payload` |
|---|---|
| `ttsc.clipboard.success` | `{ action, text, target }` |
| `ttsc.clipboard.error` | `{ action, text: null, target, error }` (alvo vazio, não encontrado, permissão negada) |

### clipboard.js

| Atributo | Descrição |
|---|---|
| `data-clipboard-target="#id"` | copia o conteúdo do alvo |
| `data-clipboard-text="…"` | copia texto fixo |
| `data-clipboard-action="cut"` | recorta |

`new ClipboardJS(seletor, { container, text(trigger), target(trigger) })`; eventos `success`/`error` com `e.action`, `e.text`, `e.trigger`, `e.clearSelection()`; `ClipboardJS.isSupported()`; `instance.destroy()`.

## Acessibilidade

- Botão só-ícone com `aria-label` específico (“Copiar código da matrícula”).
- Resultado anunciado em `role="status" aria-live="polite"` — a troca de ícone sozinha não é percebida por leitores.
- O valor fica visível e selecionável (input `readonly`, não `disabled`) para cópia manual em caso de erro.
- `navigator.clipboard` exige HTTPS e gesto do usuário; o erro sempre tem mensagem textual.

## Modelos

### HTML

```html
<!-- Código da matrícula -->
<span class="inline-flex items-center gap-2">
  <code><?= $this->e($enrollment['code']) ?></code>
  <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" aria-label="Copiar código da matrícula"
          data-ttsc-clipboard="true" data-ttsc-clipboard-text="<?= $this->e($enrollment['code']) ?>"
          data-ttsc-clipboard-copied-class="ttsc-clipboard-copied">
    <i class="fa-light fa-copy cb-idle"></i><i class="fa-light fa-check cb-done"></i>
  </button>
</span>

<!-- Link de convite (gerado na criação do convite) -->
<label class="ttsc-form-label" for="invite-link">Link de convite do responsável</label>
<div class="flex gap-2">
  <input class="ttsc-input" id="invite-link" readonly value="<?= $this->e($inviteUrl) ?>">
  <button type="button" class="ttsc-btn ttsc-btn-outline" data-ttsc-clipboard="true" data-ttsc-clipboard-target="#invite-link"
          data-ttsc-clipboard-copied-class="ttsc-clipboard-copied">
    <span class="cb-idle"><i class="fa-light fa-copy"></i> Copiar</span>
    <span class="cb-done"><i class="fa-light fa-check"></i> Copiado</span>
  </button>
</div>
<div class="text-xs text-muted-foreground" data-clipboard-status role="status" aria-live="polite"></div>
```

### CSS

```css
[data-ttsc-clipboard] .cb-done { display: none; }
.ttsc-clipboard-copied .cb-idle { display: none; }
.ttsc-clipboard-copied .cb-done { display: inline; color: var(--ttsc-accent-text); }
.ttsc-clipboard-copied { border-color: var(--ttsc-accent-border); }
[data-clipboard-status].is-ok { color: var(--ttsc-accent-text); }
[data-clipboard-status].is-error { color: var(--ttsc-danger-text); }
```

### JS

```js
// assets/js/core/ttsc.clipboard-feedback.js — feedback padrão para todos os [data-ttsc-clipboard]
TTSC.init();

function status(trigger) {
  return trigger.closest('form, section, .ttsc-card, body').querySelector('[data-clipboard-status]');
}

document.addEventListener('ttsc.clipboard.success', (event) => {
  const trigger = event.target;
  const out = status(trigger);
  if (out) { out.className = 'text-xs is-ok'; out.textContent = 'Copiado para a área de transferência.'; }
  setTimeout(() => trigger.classList.remove('ttsc-clipboard-copied'), 1500);
});

document.addEventListener('ttsc.clipboard.error', (event) => {
  const out = status(event.target);
  if (out) { out.className = 'text-xs is-error'; out.textContent = 'Não foi possível copiar. Selecione o texto e use Ctrl+C.'; }
  console.warn('[clipboard]', event.detail.payload.error);
});

// Alternativa legada (somente se a página já usa clipboard.js)
if (window.ClipboardJS && document.querySelector('[data-clipboard-target], [data-clipboard-text]')) {
  const cjs = new ClipboardJS('[data-clipboard-target], [data-clipboard-text]');
  cjs.on('success', (e) => {
    e.clearSelection();
    e.trigger.classList.add('ttsc-clipboard-copied');
    setTimeout(() => e.trigger.classList.remove('ttsc-clipboard-copied'), 1500);
  });
  cjs.on('error', (e) => { status(e.trigger).textContent = 'Use Ctrl+C para copiar.'; });
}
```

### SQL

```sql
-- Código da matrícula
SELECT en.code
  FROM enrollments en
 WHERE en.uuid = :enrollment_uuid AND en.deleted_at IS NULL;

-- Convites pendentes e válidos da unidade (lista com "Copiar link")
SELECT i.uuid, i.code, i.email, i.role_code, i.expires_at
  FROM invitations i
 WHERE i.deleted_at IS NULL
   AND i.is_deleted = 0
   AND i.unit_uuid = :unit_uuid
   AND i.status = 'pending'
   AND i.accepted_at IS NULL
   AND i.expires_at > NOW()
 ORDER BY i.expires_at;
```

`invitations` guarda só `token_hash`: o link completo (`/convite/{token}`) existe apenas na resposta de criação do convite, quando o botão “Copiar link” é mostrado. Nas listagens, copie o `code` do convite ou ofereça “Gerar novo link”.

## Faça / Não faça

- **Faça:** usar o ttscui; feedback “Copiado” por ~1,5 s + mensagem em `aria-live`.
- **Faça:** manter o valor visível ao lado do botão.
- **Não faça:** carregar clipboard.js e ttscui na mesma página.
- **Não faça:** copiar dados sensíveis sem o usuário vê-los antes.
