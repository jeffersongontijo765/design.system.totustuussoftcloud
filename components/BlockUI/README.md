# BlockUI

Bloqueio visual de um card, seção ou da página inteira durante uma operação assíncrona — implementação TTSC em JS puro com overlay, spinner e mensagem (`TTSC.BlockUI`, métodos `block()`/`release()`).

## Quando usar

- Recarregar um card de dashboard (KPI, gráfico, lista) sem permitir cliques no conteúdo desatualizado.
- Operações em lote que **não podem** ser interrompidas por outro clique: rematrícula em lote, fechamento de diário, geração de boletos (modo página).
- Formulário dentro de drawer enquanto o `DomainCrudController` responde (bloqueie o corpo do drawer, não a página).
- **Não use** para o botão que disparou a ação — use o estado carregando do [Button](../Button/README.md) (`aria-busy`).
- **Não use** para carregamento inicial de listas: prefira skeleton/[EmptyState](../EmptyState/README.md). Para progresso com percentual use `ttsc-progress`.
- **Não use** para confirmar algo ao usuário: isso é [SweetAlert](../SweetAlert/README.md) ou [Toast](../Toast/README.md).

## Anatomia

```
.ttsc-card.ttsc-blockui-target  [aria-busy="true"]
└── .ttsc-blockui  (role="status", absolute, inset 0)
    └── .ttsc-blockui-box
        ├── .ttsc-blockui-spinner
        └── .ttsc-blockui-msg   "Atualizando títulos…"
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Alvo | qualquer elemento; recebe `.ttsc-blockui-target` (position: relative) e `aria-busy="true"` | sim (ou `'page'`) |
| Overlay | `.ttsc-blockui` + `.is-visible` (fade 150ms) | gerado |
| Modo página | `.ttsc-blockui-page` (fixed, `--ttsc-z-modal`, fundo `--ttsc-scrim`) | não |
| Caixa | `.ttsc-blockui-box` | gerado |
| Spinner | `.ttsc-blockui-spinner` | gerado |
| Mensagem | `.ttsc-blockui-msg` | gerado |

## Variantes

| Variante | Como | Uso | Tokens |
|---|---|---|---|
| Elemento | `new TTSC.BlockUI('#card')` | card / seção / corpo de drawer | véu `color-mix(--ttsc-surface 72%)`, caixa `ttsc-surface` + `ttsc-border` + `ttsc-shadow-md` |
| Página | `new TTSC.BlockUI('page')` | lote crítico | véu `ttsc-scrim`, z `ttsc-z-modal` |
| Mensagem | `{ message }` ou `block('…')` / `setMessage('…')` | etapas (“Gerando boletos 3/10…”) | texto `ttsc-text` |
| Spinner | sempre | — | trilho `ttsc-border`, arco `ttsc-accent` (decorativo) |

## Estados

| Estado | Marca |
|---|---|
| Livre | sem overlay, sem `aria-busy` |
| Bloqueado | `.ttsc-blockui.is-visible` no alvo, `aria-busy="true"` |
| Liberando | `.is-visible` removido, overlay sai do DOM após 150ms |

## API

| Opção | Tipo | Padrão | Descrição |
|---|---|---|---|
| `message` | string | `'Carregando…'` | texto da caixa |
| `zIndex` | number \| null | `null` | sobrescreve o z do overlay (ex.: dentro de modal) |

| Método | Retorno | Descrição |
|---|---|---|
| `new TTSC.BlockUI(target, options)` | instância | `target`: seletor, elemento ou `'page'` |
| `block(message?)` | this | cria/mostra o overlay; se já bloqueado, só troca a mensagem |
| `setMessage(text)` | this | atualiza a mensagem sem piscar |
| `release()` | this | remove o overlay e `aria-busy` |
| `isBlocked()` | boolean | estado atual |

| Evento (bubbles, no alvo ou `body`) | Quando |
|---|---|
| `ttsc:blockui:blocked` | após inserir o overlay |
| `ttsc:blockui:released` | ao liberar |

## Acessibilidade

- O overlay tem `role="status"` + `aria-live="polite"`: o leitor anuncia a mensagem; o alvo recebe `aria-busy="true"`.
- O overlay captura cliques, mas **não o teclado**: em modo elemento, desabilite os botões do card (`inert` no conteúdo) se a ação não puder ser repetida; em modo página, use `document.body.inert` com cuidado ou prefira bloquear só a região.
- Sempre chame `release()` em `finally` — um bloqueio esquecido trava a tela.
- Mensagem em `ttsc-text` sobre `ttsc-surface` (≥ 12:1); o véu mantém o conteúdo legível mas visivelmente inativo. `prefers-reduced-motion` desacelera o spinner.

## Modelos

### HTML

```html
<!-- Card de dashboard financeiro que se atualiza -->
<div class="ttsc-card" id="card-open-titles" data-endpoint="/admin/financial/kpis/open-titles">
  <div class="ttsc-card-header">
    <h3 class="ttsc-card-title">Mensalidades em aberto</h3>
    <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm"
            aria-label="Atualizar" data-ttsc-blockui-reload="#card-open-titles">
      <i class="fa-light fa-arrows-rotate"></i>
    </button>
  </div>
  <div class="ttsc-card-content">
    <div class="text-2xl font-semibold" data-kpi="open_amount">R$ 48.320,00</div>
    <div class="text-xs"><span data-kpi="open_titles">57</span> títulos vencidos</div>
  </div>
</div>
```

### CSS

```css
/* assets/css/ttsc.blockui.css */
.ttsc-blockui-target { position: relative; }
.ttsc-blockui {
  position: absolute; inset: 0; z-index: 5;
  display: flex; align-items: center; justify-content: center;
  background: color-mix(in srgb, var(--ttsc-surface) 72%, transparent);
  border-radius: inherit; opacity: 0; transition: opacity .15s ease; cursor: wait;
}
.ttsc-blockui.is-visible { opacity: 1; }
.ttsc-blockui-page { position: fixed; z-index: var(--ttsc-z-modal); background: var(--ttsc-scrim); border-radius: 0; }
.ttsc-blockui-box {
  display: inline-flex; align-items: center; gap: var(--ttsc-space-2); padding: 10px 14px;
  background: var(--ttsc-surface); color: var(--ttsc-text); font-size: 13px; font-weight: 500;
  border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control); box-shadow: var(--ttsc-shadow-md);
}
.ttsc-blockui-spinner {
  width: 16px; height: 16px; border-radius: 50%;
  border: 2px solid var(--ttsc-border); border-top-color: var(--ttsc-accent);
  animation: ttsc-blockui-spin .7s linear infinite;
}
@keyframes ttsc-blockui-spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .ttsc-blockui-spinner { animation-duration: 2s; } }
```

### JS

```js
// assets/js/core/ttsc.blockui.js — implementação TTSC
(function (w) {
  function BlockUI(target, options) {
    this.target = target === 'page' || !target ? null
      : (typeof target === 'string' ? document.querySelector(target) : target);
    this.options = Object.assign({ message: 'Carregando…', zIndex: null }, options || {});
    this.overlay = null;
  }
  BlockUI.prototype.block = function (message) {
    if (this.overlay) return this.setMessage(message || this.options.message);
    const host = this.target || document.body;
    const o = document.createElement('div');
    o.className = 'ttsc-blockui' + (this.target ? '' : ' ttsc-blockui-page');
    o.setAttribute('role', 'status');
    o.setAttribute('aria-live', 'polite');
    o.innerHTML = '<div class="ttsc-blockui-box"><span class="ttsc-blockui-spinner" aria-hidden="true"></span><span class="ttsc-blockui-msg"></span></div>';
    o.querySelector('.ttsc-blockui-msg').textContent = message || this.options.message;
    if (this.options.zIndex) o.style.zIndex = this.options.zIndex;
    if (this.target) { this.target.classList.add('ttsc-blockui-target'); this.target.setAttribute('aria-busy', 'true'); }
    host.appendChild(o);
    requestAnimationFrame(() => o.classList.add('is-visible'));
    this.overlay = o;
    host.dispatchEvent(new CustomEvent('ttsc:blockui:blocked', { bubbles: true }));
    return this;
  };
  BlockUI.prototype.setMessage = function (text) {
    if (this.overlay) this.overlay.querySelector('.ttsc-blockui-msg').textContent = text;
    return this;
  };
  BlockUI.prototype.release = function () {
    if (!this.overlay) return this;
    const o = this.overlay, host = this.target || document.body;
    this.overlay = null;
    o.classList.remove('is-visible');
    setTimeout(() => o.remove(), 150);
    if (this.target) this.target.removeAttribute('aria-busy');
    host.dispatchEvent(new CustomEvent('ttsc:blockui:released', { bubbles: true }));
    return this;
  };
  BlockUI.prototype.isBlocked = function () { return !!this.overlay; };
  w.TTSC = w.TTSC || {};
  w.TTSC.BlockUI = BlockUI;
})(window);

// Uso: botão "Atualizar" do card de KPI
document.addEventListener('click', async (event) => {
  const btn = event.target.closest('[data-ttsc-blockui-reload]');
  if (!btn) return;
  const card = document.querySelector(btn.dataset.ttscBlockuiReload);
  const blocker = new TTSC.BlockUI(card, { message: 'Atualizando títulos…' }).block();
  try {
    const res = await fetch(card.dataset.endpoint, { headers: { Accept: 'application/json' } });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const brl = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
    card.querySelector('[data-kpi="open_amount"]').textContent = brl.format(data.open_amount);
    card.querySelector('[data-kpi="open_titles"]').textContent = data.open_titles;
  } catch (e) {
    TTSC.Toast?.show({ message: 'Não foi possível atualizar o card.', variant: 'destructive' });
  } finally {
    blocker.release();
  }
});
```

### SQL

O BlockUI não persiste nada; ele cobre consultas lentas como a agregação do card “Mensalidades em aberto”:

```sql
-- Títulos vencidos e saldo em aberto (financial_receivables)
SELECT COUNT(*) AS open_titles,
       COALESCE(SUM(r.net_amount - COALESCE(r.amount_paid, 0)), 0) AS open_amount
  FROM financial_receivables r
 WHERE r.deleted_at IS NULL
   AND r.status IN ('open', 'partial', 'overdue')
   AND r.due_date < CURDATE();
```

O endpoint devolve `{"open_titles": 57, "open_amount": 48320.00}` em JSON; o JS formata em pt-BR e libera o bloqueio no `finally`.

## Faça / Não faça

- **Faça:** bloqueie a menor região possível (o card), e só por operações > 300ms.
- **Faça:** `release()` em `finally`; troque a mensagem por etapa em processos longos.
- **Faça:** no modo página, descreva o que está acontecendo (“Processando rematrícula em lote…”).
- **Não faça:** bloquear a página para salvar um formulário simples.
- **Não faça:** empilhar dois BlockUI no mesmo alvo — reutilize a instância (`block()` é idempotente).
- **Não faça:** usar o véu como “desabilitado” permanente; para isso use `disabled`/`inert`.
