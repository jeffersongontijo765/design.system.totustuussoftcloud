# Sticky

Fixa um elemento (toolbar de ações em lote, resumo de totais, cabeçalho de formulário) no topo depois de certa rolagem e o solta ao voltar ou ao alcançar um elemento de liberação (`data-ttsc-sticky`, ttscui).

> Também listado em: **Geral › Sticky**.

## Quando usar

- Toolbar de ações em lote que precisa continuar visível enquanto o usuário rola a lista de matrículas.
- Barra de totais (“42 alunos · 3 pendências”) no topo do diário de classe.
- Rodapé de ações de formulário longo (`bottom`), liberado ao chegar no fim do formulário.
- **Prefira CSS `position: sticky`** quando basta grudar dentro do próprio contêiner, sem trocar classes nem disparar eventos.
- **Não use** para o cabeçalho global do app (o shell já o fixa) nem para índice de seções: use [Scrollspy](../Scrollspy/README.md).

## Anatomia

```
┌ [data-ttsc-sticky-wrapper] (reserva a altura enquanto fixo) ┐
│ ┌ toolbar [data-ttsc-sticky] ──────────────────────────────┐ │   rolou > offset → .active + class + position: fixed
│ │ 3 selecionadas   [Trancar] [Exportar]                     │ │   voltou / release visível → .release
│ └───────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Elemento | `[data-ttsc-sticky="true"]` | sim |
| Wrapper | ancestral `[data-ttsc-sticky-wrapper]` — recebe `height` do elemento enquanto ativo (evita salto do conteúdo) | recomendado |
| Estado | classes `active` / `release` postas pelo JS | — |
| Atributo global | `data-ttsc-sticky-<name>="on"` no `<body>` enquanto ativo (com `name`) | não |

## Estados

| Estado | Como | Tokens (extensão abaixo) |
|---|---|---|
| Em fluxo | sem `active` | fundo `ttsc-surface`, borda `ttsc-border` |
| Fixado | `active` + `class`/`activeClass` | `ttsc-shadow-md`, borda inferior `ttsc-border-strong`, `z-index: var(--ttsc-z-navigation)` |
| Liberado | `release` + `releaseClass` | volta ao fluxo; estilos inline removidos (após `releaseDelay`) |

## API

Conferida em `src/components/sticky/sticky.ts`. Opções por `data-ttsc-sticky-<opção>` (kebab-case), objeto no construtor ou `ttscGlobalComponentsConfig.sticky`; também por CSS custom property `--ttsc-sticky-<opção>` (permite valores por breakpoint).

| Opção | Padrão | Descrição |
|---|---|---|
| `target` | `"body"` | elemento cujo `scroll` é observado (`body` = janela) |
| `offset` | `0` | px de rolagem para ativar. **`offset ≤ 0` desativa o sticky** |
| `activate` | `""` | seletor: ativa quando a rolagem passa de `|offset − el.offsetTop|` |
| `release` | `""` | seletor: solta quando esse elemento entra (parcialmente) no viewport |
| `reverse` | `false` | modo reverso (mesma lógica, guarda `lastScrollTop`) |
| `top` / `bottom` | `""` | px (ou `auto` = 0) aplicados como `inset-block-*` quando ativo |
| `middle` | `false` | `inset-block-start: 50%` |
| `start` / `end` | `""` | px ou `auto` (mantém a posição horizontal atual) |
| `center` | `false` | `inset-inline-start: 50%` |
| `width` | `""` | px, seletor de outro elemento cuja largura copiar, ou `auto` (largura atual) |
| `zindex` | `""` | aplica `z-index` **e** `position: fixed` — sem ele, a classe precisa trazer o `position` |
| `class` | `""` | classes adicionadas quando ativo (ignorado se `activeClass` existir) |
| `activeClass` / `releaseClass` | `""` | classes por estado |
| `releaseDelay` | `0` | ms até limpar os estilos inline ao soltar |
| `name` | `""` | gera `data-ttsc-sticky-<name>="on"` no `<body>` |

| Método | Descrição |
|---|---|
| `ttscSticky.getInstance(el)` / `getOrCreateInstance(el, cfg)` | instância |
| `update()` | recalcula (após mudar layout) — também roda no `resize` |
| `isActive()` / `isRelease()` | estado atual |
| `dispose()` | remove listeners, estilos e o atributo do `<body>` |

| Evento (DOM, no elemento) | `detail.payload` |
|---|---|
| `change` | `{ active: true }` ao fixar, `{ active: false }` ao soltar |

Regra do fonte: se `altura + top` passar da altura do viewport, o sticky não ativa.

## Acessibilidade

- Fixar não muda a ordem de foco; mantenha a toolbar antes da lista no DOM.
- Contador de seleção com `aria-live="polite"` (“3 matrículas selecionadas”).
- Não cubra o foco: dê à lista `scroll-padding-top` igual à altura da barra fixada.
- Contraste da barra fixada é o mesmo do estado normal (`ttsc-text` sobre `ttsc-surface`); a sombra é só reforço.

## Modelos

### HTML

```html
<div data-ttsc-sticky-wrapper>
  <div class="ttsc-sticky-bar" id="enrollments-bulkbar"
       data-ttsc-sticky="true"
       data-ttsc-sticky-name="bulkbar"
       data-ttsc-sticky-offset="120"
       data-ttsc-sticky-top="60"
       data-ttsc-sticky-start="auto"
       data-ttsc-sticky-width="auto"
       data-ttsc-sticky-zindex="20"
       data-ttsc-sticky-class="is-stuck"
       data-ttsc-sticky-release="#enrollments-pagination">
    <span class="text-sm" aria-live="polite"><b data-bulk-count>0</b> matrículas selecionadas</span>
    <div class="flex items-center gap-2">
      <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-sm"><i class="fa-light fa-lock"></i> Trancar</button>
      <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-sm"><i class="fa-light fa-arrow-down-to-line"></i> Exportar</button>
    </div>
  </div>
</div>

<table class="ttsc-table"> … </table>
<nav id="enrollments-pagination" class="ttsc-pagination-standard"> … </nav>
```

### CSS

```css
.ttsc-sticky-bar {
  display: flex; align-items: center; justify-content: space-between; gap: var(--ttsc-space-3);
  padding: 8px var(--ttsc-space-4); background: var(--ttsc-surface); color: var(--ttsc-text);
  border: 1px solid var(--ttsc-border); border-radius: var(--ttsc-radius-control);
  transition: box-shadow .15s ease;
}
.ttsc-sticky-bar.is-stuck {
  border-color: var(--ttsc-border-strong); box-shadow: var(--ttsc-shadow-md);
  border-start-start-radius: 0; border-start-end-radius: 0;
}
/* Conteúdo abaixo de cabeçalhos fixos que dependem do sticky global */
body[data-ttsc-sticky-bulkbar="on"] .ttsc-table { scroll-padding-top: 56px; }
@media (prefers-reduced-motion: reduce) { .ttsc-sticky-bar { transition: none; } }
```

### JS

```js
TTSC.init();

const bar = document.getElementById('enrollments-bulkbar');
const sticky = ttscSticky.getOrCreateInstance(bar);

bar.addEventListener('change', (event) => {
  const payload = event.detail?.payload;
  if (!payload) return; // "change" de checkbox dentro da barra também borbulha
  bar.toggleAttribute('data-stuck', payload.active);
});

// Contador de seleção (checkboxes da tabela)
document.querySelector('.ttsc-table').addEventListener('change', () => {
  const n = document.querySelectorAll('.ttsc-table tbody .ttsc-checkbox:checked').length;
  bar.querySelector('[data-bulk-count]').textContent = n;
});

// Depois de abrir/fechar a sidebar, recalcula largura e posição
document.addEventListener('ttsc.sidebar.toggle', () => sticky.update());
```

### SQL

A barra mostra totais do filtro atual; uma consulta agregada evita contar no cliente:

```sql
SELECT COUNT(*)                                 AS total,
       COALESCE(SUM(e.status = 'active'), 0)    AS active,
       COALESCE(SUM(e.status = 'locked'), 0)    AS locked
  FROM enrollments e
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid;
```

O controller injeta os três números na barra (`data-total`, `data-active`, `data-locked`); as ações em lote revalidam permissão e `unit_uuid` no servidor antes do `UPDATE`.

## Faça / Não faça

- **Faça:** usar `data-ttsc-sticky-wrapper` para o conteúdo não “pular” quando a barra sai do fluxo.
- **Faça:** `offset` > 0 sempre (com 0 o componente se desativa).
- **Não faça:** fixar elementos mais altos que o viewport — o ttscui recusa.
- **Não faça:** usar sticky de JS onde `position: sticky` resolve.
