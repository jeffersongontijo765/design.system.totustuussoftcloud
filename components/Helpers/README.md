# Helpers

Funções e classes de apoio do chassi: helpers JS do ttscui (`src/helpers/*`: dom, data, event-handler, utils), API comum dos componentes (`getInstance`, `getOrCreateInstance`, `init`, eventos `ttsc.*`) e helpers CSS presentes no bundle.

## Quando usar

- Escrever um adaptador ou script de página que precisa achar a instância de um componente ttscui, reagir aos eventos dele ou reinicializar após injetar HTML.
- Guardar instâncias de plugins por elemento (`ttscData`), sem variáveis globais soltas.
- Esconder texto visualmente, truncar, impedir seleção — com as classes que realmente existem.
- Layout e cor → [Utilities](../Utilities/README.md). Integração de bibliotecas → [ThirdPartyPlugin](../ThirdPartyPlugin/README.md).

## Anatomia

```
ttscui.js (webpack)                       expostos em window?
├─ src/helpers/data.ts           → window.ttscData        sim  (set/get/has/remove/clear por elemento)
├─ src/helpers/dom.ts            → interno                 não  (ready, getElement, getDataAttributes, getCssProp…)
├─ src/helpers/event-handler.ts  → interno                 não  (on/off com delegação)
├─ src/helpers/utils.ts          → interno                 não  (geUID, parseDataAttribute, camelCase…)
├─ src/components/component.ts   → base de todos: _getOption, _buildConfig, on/off, _dispatchEvent
└─ src/index.ts                  → window.ttscComponents.init()  ← TTSC.init() chama isto
assets/js/ttsc.js (app)          → window.TTSCDom          ready, transitionEnd, isVisibleInParent, getRelativeTopPosition
```

| Helper | Origem | Uso |
|---|---|---|
| `TTSC.init()` | namespace do DS (`bundle.js`) → `ttscComponents.init()` | (re)inicializa todos os `data-ttsc-*`; seguro chamar de novo — cada `init` pula elementos com instância |
| `ttscX.getInstance(el)` | cada componente | instância ou `null` |
| `ttscX.getOrCreateInstance(el, config?)` | cada componente | cria se faltar |
| `ttscX.createInstances()` / `ttscX.init()` | cada componente | varre o documento pelo seletor `[data-ttsc-x]` |
| `instance.on(evt, fn)` → id / `off(evt, id)` | `component.ts` | callbacks internos (podem ser `async`) |
| `instance.getOption(nome)` / `getElement()` / `dispose()` | `component.ts` | leitura de config, elemento, limpeza |
| `ttscData.set/get/has/remove/clear` | `helpers/data.ts` | `Map<Element, Map<nome, valor>>` — onde o ttscui guarda as instâncias |
| `window.ttscGlobalComponentsConfig` | `component.ts` | config global por componente (`{ toast: {...} }`), mesclada antes dos `data-*` |
| `TTSCDom.ready(fn)` | app `assets/js/ttsc.js` | executa já ou no `DOMContentLoaded` |

## Variantes

Ordem de configuração de um componente (`_buildConfig`): `_defaultConfig` → `ttscGlobalComponentsConfig[nome]` → atributos `data-ttsc-<nome>-*` → objeto passado ao construtor. `_getOption` ainda deixa uma **variável CSS** `--ttsc-<nome>-<opção>` no elemento sobrescrever tudo (útil para mudar opção por breakpoint, ex. `lg:[--ttsc-drawer-enable:false]`).

Conversão dos `data-*` (`utils.parseDataAttribute`): `"true"`/`"false"` → booleano, `"12"` → número, `""`/`"null"` → `null`, JSON válido → objeto, resto → string.

## API

### Eventos

| Padrão | Exemplos (conferidos no fonte) | Onde ouvir |
|---|---|---|
| `ttsc.<componente>.<ação>` | `ttsc.pin-input.input/change/complete`, `ttsc.range-slider.input/change` | no elemento do componente (bubbles) |
| nome curto | drawer/modal: `show`, `shown`, `hide`, `hidden`, `toggle`; repeater: `add`; toggle-password: `toggle`, `toggled` | idem |
| eventos do app | `ttsc:drawer:open`, `ttsc:drawer:close`, `ttsc:filter:apply`, `ttsc:dt:sort`… | `document` |

Todos são `CustomEvent` com `bubbles: true, cancelable: true` e dados em **`event.detail.payload`**. Eventos "antes" (`show`, `hide`, `toggle`) aceitam cancelamento pelo payload (`payload.cancel = true`) quando o componente o lê.

### Helpers CSS presentes no `bundle.css`

| Classe | Efeito | Observação |
|---|---|---|
| `hidden` | `display: none` | é a classe que o ttscui alterna (dropdown, collapse) |
| `truncate` | uma linha com reticências | dê `min-w-0` ao pai flex |
| `whitespace-nowrap` / `text-nowrap` | sem quebra | — |
| `select-none` | impede seleção | alças de drag |
| `cursor-pointer` | cursor de clique | — |
| `dark:hidden` / `dark:block` / `light:hidden` | mostrar/ocultar por tema | — |
| `ttsc-kbd` (`-sm`, `-xs`, `-outline`) | tecla de atalho | — |
| `ttsc-separator` / `ttsc-separator-vertical` | divisor | — |
| `sr-only` | **não está no bundle** (existe em `assets/css/tailwind.css` do app) | use `.ttsc-sr-only` (CSS abaixo) |

Estados alternados pelo JS: `open` (modal/drawer/dropdown aberto), `active` (item ativo, toggle-password visível), `selected` (tab), `hidden`, e `data-ttsc-<nome>-initialized="true"` em todo elemento inicializado.

## Acessibilidade

- Texto só para leitor de tela: `.ttsc-sr-only`; nunca `hidden`/`display:none` (também esconde do leitor).
- Ao injetar HTML e chamar `TTSC.init()`, mova o foco para o conteúdo novo se ele resultou de uma ação do usuário.
- Para atualizações assíncronas, um contêiner `aria-live="polite"` com o resumo ("12 alunos encontrados").

## Modelos

### HTML

```html
<!-- Busca de alunos: resultado injetado via fetch + rótulo só para leitor de tela -->
<form class="flex items-center gap-2" id="student-search" role="search">
  <label class="ttsc-sr-only" for="q">Buscar aluno por nome ou e-mail</label>
  <div class="ttsc-input ttsc-input-sm w-[240px]">
    <i class="fa-light fa-magnifying-glass" aria-hidden="true"></i>
    <input id="q" name="q" type="search" placeholder="Buscar aluno" autocomplete="off">
  </div>
  <kbd class="ttsc-kbd ttsc-kbd-sm">/</kbd>
</form>
<p class="text-xs text-muted-foreground" id="student-search-status" aria-live="polite"></p>
<div id="student-results"></div>
```

### CSS

```css
/* Equivalente do sr-only do Tailwind (ausente no bundle) */
.ttsc-sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip-path: inset(50%); white-space: nowrap; border-width: 0;
}
.ttsc-sr-only-focusable:focus { position: static; width: auto; height: auto; margin: 0; clip-path: none; }

/* Truncamento em 2 linhas (line-clamp não está no bundle) */
.ttsc-line-clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

/* Destaque do termo buscado */
mark.ttsc-mark { background: var(--ttsc-accent-soft); color: var(--ttsc-text); border-radius: var(--ttsc-radius-xs); padding: 0 2px; }
```

### JS

```js
// assets/js/core/ttsc.helpers.js — utilitários de página sobre a API real do ttscui
export const ready = (fn) => (window.TTSCDom ? TTSCDom.ready(fn)
  : document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', fn) : fn());

// Ouve um evento ttsc.* já entregando o payload
export function onTtsc(target, type, handler) {
  const listener = (event) => handler(event.detail?.payload ?? null, event);
  target.addEventListener(type, listener);
  return () => target.removeEventListener(type, listener);
}

// Injeta HTML do servidor e reinicializa só o que é novo (instâncias existentes são puladas)
export function inject(container, html) {
  container.innerHTML = html;           // HTML já escapado pela view Plates
  window.TTSC.init();
}

// Debounce para busca
export const debounce = (fn, ms = 300) => {
  let t; return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
};

ready(() => {
  const form = document.getElementById('student-search');
  const status = document.getElementById('student-search-status');
  const results = document.getElementById('student-results');
  let controller;
  form.q.addEventListener('input', debounce(async () => {
    controller?.abort();
    controller = new AbortController();
    const res = await fetch(`/academic/students/search?q=${encodeURIComponent(form.q.value)}&page=1`,
      { signal: controller.signal, headers: { Accept: 'text/html' } });
    inject(results, await res.text());
    status.textContent = `${res.headers.get('X-Total-Count') ?? 0} alunos encontrados`;
  }));
  document.addEventListener('keydown', (e) => { if (e.key === '/' && e.target === document.body) { e.preventDefault(); form.q.focus(); } });

  // Exemplo com instância: drawer aberto → foca o primeiro campo
  document.querySelectorAll('[data-ttsc-drawer]').forEach((el) => {
    onTtsc(el, 'shown', () => el.querySelector('input, select, textarea')?.focus());
  });
});
```

### SQL

Não há helper SQL "mágico": o padrão do chassi é **PDO com prepared statement**, placeholders nomeados e escape dos curingas do `LIKE` (`%` e `_`) antes de envolver o termo — como em `LoggerController::searchLogs` (`addcslashes($q, '%_')`). Usar `!` como caractere de escape evita a diferença de barra invertida entre `NO_BACKSLASH_ESCAPES` ligado/desligado e funciona igual em MariaDB 10.11 e MySQL 8.

```php
// PHP: o termo vira dado, nunca SQL
$term = strtr(trim($q), ['!' => '!!', '%' => '!%', '_' => '!_']);   // "50%_off" → "50!%!_off"
$perPage = 20;
$offset  = max(0, ((int) $page - 1) * $perPage);                     // inteiro validado
```

```sql
-- Página de resultados (tenant). :term já escapado; LIMIT/OFFSET como inteiros (PDO::PARAM_INT)
SELECT u.uuid, u.code, u.name, u.email
  FROM users u
 WHERE u.deleted_at IS NULL
   AND (u.name  LIKE CONCAT('%', :term, '%') ESCAPE '!'
     OR u.email LIKE CONCAT('%', :term2, '%') ESCAPE '!')
 ORDER BY u.name, u.id
 LIMIT :limit OFFSET :offset;

-- Total para a paginação / X-Total-Count
SELECT COUNT(*) AS total
  FROM users u
 WHERE u.deleted_at IS NULL
   AND (u.name  LIKE CONCAT('%', :term, '%') ESCAPE '!'
     OR u.email LIKE CONCAT('%', :term2, '%') ESCAPE '!');
```

O mesmo valor vai em `:term` e `:term2` (PDO nativo não repete placeholder nomeado). O controller renderiza as linhas num partial Plates (`$this->e()` em cada campo) e devolve o HTML para `inject()`; ordenação por coluna vem de uma whitelist (`match ($sort)`), nunca do request direto.

## Faça / Não faça

- **Faça:** `getOrCreateInstance` em vez de `new ttscX()`; ouvir eventos no elemento e ler `event.detail.payload`.
- **Faça:** escapar `%`/`_` com `ESCAPE '!'` e `LIMIT/OFFSET` como inteiros.
- **Não faça:** depender de `dom`/`utils` internos do ttscui (não são globais); usar `hidden` para texto de leitor de tela; concatenar o termo de busca no SQL.
