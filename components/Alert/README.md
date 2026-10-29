# Alert

Faixa de aviso inline (`.ttsc-alert`) para mensagens persistentes da página — seis cores, três estilos (solid, light, outline), com ícone, título, descrição, ações e fechar via `data-ttsc-dismiss`.

> Também listado em: **Base › Alerts**.

## Quando usar

- Avisar algo que vale para a página inteira e precisa ficar visível até ser resolvido: documentação pendente, mensalidades vencendo, período de rematrícula aberto.
- Resultado de uma ação que o usuário precisa ler com calma (ex.: “Importação concluída com 3 linhas rejeitadas”), no topo do formulário.
- Avisos institucionais ativos vindos de `notification_items` (ver SQL).
- **Não use** para confirmação passageira (“Salvo”) — use [Toast](../Toast/README.md).
- **Não use** para decisão bloqueante (“Excluir matrícula?”) — use [Modal](../Modal/README.md).
- **Não use** para rótulo de status em linha de tabela — use [Badge](../Badge/README.md).

## Anatomia

```
┌──────────────────────────────────────────────────────────────┐
│ [ícone]  Título                         [ação] [ação]   [×]  │
│          Descrição (opcional, 1–2 linhas)                    │
└──────────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Container | `div.ttsc-alert` + `role="alert"` (urgente) ou `role="status"` | sim |
| Cor | `ttsc-alert-primary` · `-success` · `-warning` · `-destructive` · `-info` · `-mono` | não (padrão = neutro `--muted`) |
| Estilo | (solid, padrão) · `ttsc-alert-light` · `ttsc-alert-outline` | não |
| Tamanho | `ttsc-alert-sm` · (padrão) · `ttsc-alert-lg` | não |
| Ícone | `.ttsc-alert-icon > i.fa-light` | recomendado |
| Conteúdo | `.ttsc-alert-content` envolvendo `.ttsc-alert-title` + `.ttsc-alert-description` | quando há descrição |
| Título | `.ttsc-alert-title` (pode ser filho direto quando não há descrição) | sim |
| Barra de ações | `.ttsc-alert-toolbar > .ttsc-alert-actions` | não |
| Fechar | `button.ttsc-alert-close[data-ttsc-dismiss="#id"]` + `aria-label` | não |

## Variantes

| Estilo | Cor | Uso | Tokens (após a ponte do CSS abaixo) |
|---|---|---|---|
| Solid | primary | Anúncio institucional positivo | fundo `ttsc-accent`, texto `ttsc-accent-on` |
| Solid | success | Operação concluída com destaque | fundo `ttsc-primary-800`, texto branco (6,9:1) |
| Solid | warning | Prazo próximo | fundo `ttsc-warning`, texto `ttsc-accent-on` |
| Solid | destructive | Erro de processamento | fundo `ttsc-danger`, texto branco (4,8:1) |
| Solid | info | Agenda/comunicado | fundo `ttsc-info`, texto `ttsc-accent-on` |
| Solid | mono | Manutenção do sistema | fundo `--mono` (= `ttsc-text`), texto `ttsc-surface` |
| Light | todas | **Padrão para avisos de página** | fundo 5–8% da cor, borda 10–25%, texto `ttsc-text`, ícone `ttsc-*-text` |
| Outline | todas | Aviso discreto em cards | borda `ttsc-border`, fundo `ttsc-surface`, texto `ttsc-*-text` |

O runtime ttscui usa `green-500`/`yellow-500` com texto branco em success/warning (≈2:1) e violeta em info. A ponte do CSS troca essas cores pelos tokens.

## API

Sem JS próprio. O fechamento usa o componente **Dismiss** do ttscui (`src/components/dismiss/dismiss.ts`).

| Atributo (no botão fechar) | Padrão | Efeito |
|---|---|---|
| `data-ttsc-dismiss="#id"` | — | alvo a remover (seletor) |
| `data-ttsc-dismiss-mode` | `remove` | `remove` tira do DOM; `hide` adiciona a classe `hidden` |
| `data-ttsc-dismiss-hidden-class` | `hidden` | classe usada no modo `hide` |
| `data-ttsc-dismiss-interrupt` | `true` | chama `stopPropagation()` no clique |

| Método (`ttscDismiss.getInstance(botão)`) | Efeito |
|---|---|
| `dismiss()` | fecha programaticamente |
| `getTargetElement()` | retorna o alerta |

| Evento (no botão, `CustomEvent`) | Quando | Cancelável |
|---|---|---|
| `dismiss` | antes de fechar | sim (`instance.on('dismiss', e => e.cancel = true)`) |
| `dismissed` | após remover/ocultar | — |

## Acessibilidade

- `role="alert"` só para avisos urgentes (destructive/warning) — é anunciado imediatamente; os demais usam `role="status"`.
- O ícone é decorativo; a cor nunca é o único sinal: o título diz o problema.
- Botão fechar é `<button>` com `aria-label="Fechar aviso"`; foco visível com contorno `ttsc-accent`.
- Ao fechar, devolva o foco para um elemento estável (título da página) se o alerta continha o foco.
- Texto colorido usa sempre os tokens `*-text` (`ttsc-warning-text`, `ttsc-danger-text`, `ttsc-info-text`, `ttsc-accent-text`) — ≥ 4,5:1 nos dois temas.

## Modelos

### HTML

```html
<!-- Aviso de página (light) com ações e fechar -->
<div class="ttsc-alert ttsc-alert-light ttsc-alert-warning" id="alert-docs-<?= $this->e($notice['id']) ?>" role="alert">
  <div class="ttsc-alert-icon"><i class="fa-light fa-triangle-exclamation"></i></div>
  <div class="ttsc-alert-content">
    <div class="ttsc-alert-title"><?= $this->e($notice['title']) ?></div>
    <div class="ttsc-alert-description"><?= $this->e($notice['body']) ?></div>
  </div>
  <div class="ttsc-alert-toolbar">
    <div class="ttsc-alert-actions">
      <a href="<?= $this->e($notice['action_url']) ?>" class="ttsc-btn ttsc-btn-outline ttsc-btn-sm">Ver alunos</a>
      <button type="button" class="ttsc-alert-close" data-ttsc-dismiss="#alert-docs-<?= $this->e($notice['id']) ?>"
              data-notice-id="<?= $this->e($notice['id']) ?>" aria-label="Fechar aviso">
        <i class="fa-light fa-xmark"></i>
      </button>
    </div>
  </div>
</div>

<!-- Solid curto, sem descrição -->
<div class="ttsc-alert ttsc-alert-primary" role="status">
  <div class="ttsc-alert-icon"><i class="fa-light fa-circle-info"></i></div>
  <div class="ttsc-alert-title">Período letivo 2026.2 aberto para rematrícula.</div>
</div>

<!-- Outline pequeno dentro de card -->
<div class="ttsc-alert ttsc-alert-outline ttsc-alert-destructive ttsc-alert-sm" role="alert">
  <div class="ttsc-alert-icon"><i class="fa-light fa-circle-xmark"></i></div>
  <div class="ttsc-alert-title">Aluno com frequência abaixo de 75%.</div>
</div>
```

### CSS

```css
/* Ponte de tokens para .ttsc-alert (incluir após bundle.css / tailwind-runtime.css) */
.ttsc-alert .ttsc-alert-icon i { font-size: 16px; line-height: 20px; }
.ttsc-alert-close { background: none; border: 0; padding: 0; display: inline-flex; align-items: center; justify-content: center; border-radius: var(--ttsc-radius-xs); }
.ttsc-alert-close:focus-visible { outline: 2px solid var(--ttsc-accent); outline-offset: 2px; }
.ttsc-alert:not(.ttsc-alert-light):not(.ttsc-alert-outline) .ttsc-alert-close i { color: currentColor; opacity: .8; }

/* Solid: contraste ≥ 4,5:1 */
.ttsc-alert-success:not(.ttsc-alert-light):not(.ttsc-alert-outline) { background: var(--ttsc-primary-800); color: #fff; }
.ttsc-alert-warning:not(.ttsc-alert-light):not(.ttsc-alert-outline) { background: var(--ttsc-warning); color: var(--ttsc-accent-on); }
.ttsc-alert-info:not(.ttsc-alert-light):not(.ttsc-alert-outline)    { background: var(--ttsc-info);    color: var(--ttsc-accent-on); }

/* Light: fundo suave + ícone na cor de texto do token (o runtime só colore <svg>) */
.ttsc-alert-light.ttsc-alert-success { background: var(--ttsc-accent-soft); border-color: var(--ttsc-accent-border); }
.ttsc-alert-light.ttsc-alert-info    { background: color-mix(in oklab, var(--ttsc-info) 8%, transparent); border-color: color-mix(in oklab, var(--ttsc-info) 25%, transparent); }
.ttsc-alert-light.ttsc-alert-primary .ttsc-alert-icon i,
.ttsc-alert-light.ttsc-alert-success .ttsc-alert-icon i     { color: var(--ttsc-accent-text); }
.ttsc-alert-light.ttsc-alert-warning .ttsc-alert-icon i     { color: var(--ttsc-warning-text); }
.ttsc-alert-light.ttsc-alert-info .ttsc-alert-icon i        { color: var(--ttsc-info-text); }
.ttsc-alert-light.ttsc-alert-destructive .ttsc-alert-icon i { color: var(--ttsc-danger-text); }
.ttsc-alert-light .ttsc-alert-description,
.ttsc-alert-outline .ttsc-alert-description { color: var(--ttsc-text-2); }

/* Outline: texto colorido somente com tokens *-text */
.ttsc-alert-outline.ttsc-alert-primary,
.ttsc-alert-outline.ttsc-alert-success     { color: var(--ttsc-accent-text); }
.ttsc-alert-outline.ttsc-alert-warning     { color: var(--ttsc-warning-text); }
.ttsc-alert-outline.ttsc-alert-info        { color: var(--ttsc-info-text); }
.ttsc-alert-outline.ttsc-alert-destructive { color: var(--ttsc-danger-text); }
```

### JS

```js
// assets/js/core/ttsc.alert.js — marca o aviso como lido quando o usuário fecha
TTSC.init();

document.querySelectorAll('.ttsc-alert-close[data-notice-id]').forEach((button) => {
  const dismiss = ttscDismiss.getInstance(button);
  if (!dismiss) return;
  dismiss.on('dismissed', async () => {
    const token = document.querySelector('meta[name="csrf-token"]')?.content || '';
    await fetch(`/api/v1/notifications/${button.dataset.noticeId}/read`, {
      method: 'POST',
      headers: { 'X-CSRF-Token': token, 'Accept': 'application/json' },
    });
  });
});

// Alerta criado depois de um AJAX (ex.: importação de notas)
export function showAlert(container, { variant = 'info', title, description = '' }) {
  const id = `alert-${Date.now()}`;
  const icons = { success: 'circle-check', warning: 'triangle-exclamation', destructive: 'circle-xmark', info: 'circle-info', primary: 'circle-info' };
  const el = document.createElement('div');
  el.id = id;
  el.className = `ttsc-alert ttsc-alert-light ttsc-alert-${variant}`;
  el.setAttribute('role', variant === 'destructive' || variant === 'warning' ? 'alert' : 'status');
  el.innerHTML = `
    <div class="ttsc-alert-icon"><i class="fa-light fa-${icons[variant] || 'circle-info'}"></i></div>
    <div class="ttsc-alert-content"><div class="ttsc-alert-title"></div><div class="ttsc-alert-description"></div></div>
    <button type="button" class="ttsc-alert-close" data-ttsc-dismiss="#${id}" aria-label="Fechar aviso"><i class="fa-light fa-xmark"></i></button>`;
  el.querySelector('.ttsc-alert-title').textContent = title;
  el.querySelector('.ttsc-alert-description').textContent = description;
  container.prepend(el);
  TTSC.Dismiss.getOrCreateInstance(el.querySelector('.ttsc-alert-close'));
  return el;
}
```

### SQL

Avisos ativos do usuário logado (até 3, os mais urgentes primeiro) — `notification_items` não tem `deleted_at`; “ativo” = não resolvido e não lido. A prioridade vira a variante:

```sql
SELECT ni.id,
       ni.title,
       ni.body,
       ni.action_url,
       ni.due_at,
       COALESCE(p.label, ni.priority) AS priority_label,
       CASE ni.priority
            WHEN 'critical' THEN 'destructive'
            WHEN 'high'     THEN 'warning'
            WHEN 'low'      THEN 'info'
            ELSE 'primary'
       END AS variant
  FROM notification_items ni
  LEFT JOIN ref_enum_notification_items_priority_9069567d0ab0 p ON p.value = ni.priority
 WHERE ni.tenant_id = :tenant_id
   AND ni.user_id   = :user_uuid
   AND ni.type      = 'alert'
   AND ni.resolved  = 0
   AND ni.is_read   = 0
 ORDER BY FIELD(ni.priority, 'critical', 'high', 'normal', 'low'), ni.created_at DESC
 LIMIT 3;

-- Ao fechar (POST /api/v1/notifications/{id}/read)
UPDATE notification_items
   SET is_read = 1, read_at = NOW()
 WHERE id = :id AND user_id = :user_uuid;
```

O controller passa o array `$notices` para a view; cada linha vira um `.ttsc-alert.ttsc-alert-light.ttsc-alert-<?= $notice['variant'] ?>` com `role="alert"` quando a variante é `destructive`/`warning`.

## Faça / Não faça

- **Faça:** use `light` como estilo padrão de aviso de página; reserve `solid` para no máximo um anúncio por tela.
- **Faça:** título curto que diga o problema + ação concreta (“Ver alunos”, “Gerar boletos”).
- **Faça:** aplique a ponte de tokens — sem ela success/warning sólidos ficam com contraste ≈2:1.
- **Não faça:** empilhar mais de 3 alertas; agrupe em um com contagem (“12 mensalidades vencem amanhã”).
- **Não faça:** usar alerta para sucesso passageiro (use Toast) nem `role="alert"` em avisos informativos.
