# Lacunas do design system

Registro pedido pelo `AGENTS.md`: quando um componente ou regra do DS falta ou quebra,
registra-se aqui em vez de inventar. Cada lacuna diz onde aparece, o que foi feito
enquanto isso e o que o DS precisa publicar.

| ID | Situação | Resumo |
|---|---|---|
| GAP-01 | Aberta, contornada no kit | Classes de KPI documentadas sem CSS no bundle |
| GAP-02 | Corrigida em `components/ttsc.css` | Bundle sobrescrevia 7 tokens no tema claro e criava ciclo em `--border` |
| GAP-03 | Aberta, contornada no kit | `--accent` do bundle é o verde da marca; tecla, avatar e skeleton ficam verdes |
| GAP-04 | Aberta, contornada no kit | `.ttsc-skeleton-line` e `.ttsc-skeleton-block` sem tamanho |
| GAP-05 | Aberta, proposta de entrada | Não há chassi (AppShell) no catálogo sem utilitários de cor crus |
| GAP-06 | Aberta, proposta de variante | Variante `kpi-table` para o arquétipo `records` |
| GAP-07 | Aberta, contornada no kit | Rail com foco a `z-index: 50 !important` fica sob o fundo das gavetas |

## GAP-01 — classes de KPI sem CSS

- **Onde:** `components/Card/README.md` usa `.ttsc-kpi-label`, `.ttsc-kpi-value`, `.ttsc-kpi-delta` (com `is-up` e `is-down`) e `.ttsc-kpi-icon`. O `bundle.css` não tem regra para nenhuma delas. O `ttsc-responsive.css` só tem `.ttsc-kpi-value-fluid`.
- **Contorno:** `layout-main/css/components.css`, seção 6, traz um estilo mínimo só com tokens.
- **O DS precisa:** publicar essas classes no bundle ou na camada responsiva. Depois, apague a seção 6 do kit.

## GAP-02 — tokens sobrescritos pelo bundle no tema claro (corrigida)

- **Onde:** o `bundle.css` contém um bloco `:root` de apelidos do chassi, com o comentário "This file must not redefine base colour tokens". Mesmo assim ele define:
  - `--ttsc-canvas: var(--bg, #f8fafc)`
  - `--ttsc-surface: var(--surface, #ffffff)`
  - `--ttsc-border: var(--border, #e2e8f0)`
  - `--ttsc-text: var(--fg, #0f172a)`
  - `--ttsc-text-muted: var(--fg-2, #475569)`
  - `--ttsc-accent: var(--accent, #10b981)`
  - `--ttsc-accent-strong`
- **Efeito medido:** o `ttsc.css` carregava os tokens antes do bundle, então esses apelidos venciam no tema claro. `--bg`, `--fg` e `--fg-2` não existem, então valiam os valores de reserva (cores slate, diferentes dos tokens). Além disso, a ponte define `--border: var(--ttsc-border)`. Isso fecha o ciclo `--ttsc-border → --border → --ttsc-border`, e as duas variáveis ficavam **vazias**: todas as bordas com `var(--ttsc-border)` sumiam no tema claro, inclusive nas páginas de `paginas/referencia/`. O tema escuro não tinha o problema, porque `[data-theme="dark"]` é mais específico que `:root`.
- **Correção:** o `components/ttsc.css` agora carrega o bundle primeiro e os tokens depois. Verificado em `layout-main/index.html`, `paginas/referencia/registros-tabela.html` e `dashboard-operacional.html`, nos dois temas: nenhum token vazio, e os valores são os de `__tokens.css`.
- **O DS ainda pode:** remover do bundle o bloco de apelidos de cor, deixando só as medidas do chassi.

## GAP-03 — `--accent` verde no bundle

- **Onde:** o `bundle.css` define `--accent: #3ecf8e` / `oklch(0.78 0.16 162)` (por volta das linhas 18111 e 18252). Na convenção dos componentes do bundle (shadcn), `--accent` é um fundo **neutro** de destaque. O resultado é que `.ttsc-kbd`, `.ttsc-avatar-fallback` e `.ttsc-skeleton` ficam verdes. Isso aparece também nos avatares de `paginas/referencia/registros-tabela.html`.
- **Contorno:** `layout-main/css/components.css`, seção 6, troca o fundo só desses três por tokens neutros (`--ttsc-surface-2`, `--ttsc-accent-soft`, `--ttsc-border`).
- **O DS precisa:** decidir se `--accent` é a marca ou o neutro. Se for a marca, os três componentes devem usar `--muted`. Se for o neutro, a ponte deve apelidar `--accent` para `--ttsc-surface-2` e medir o contraste.

## GAP-04 — tamanhos do skeleton

- **Onde:** o `components/Skeleton/README.md` usa `.ttsc-skeleton-line` e `.ttsc-skeleton-block` com largura e altura em `style=""`. O bundle só tem `.ttsc-skeleton` (cor e pulso).
- **Contorno:** o kit define altura e larguras alternadas por classe, sem estilo inline.
- **O DS precisa:** publicar os tamanhos de `-line`, `-block` e `-circle`.

## GAP-05 — chassi (AppShell) no catálogo

- **Onde:** o `components/Navigation/shell.html` é o chassi real do app, mas usa utilitários de cor crus (`text-slate-400`, `hover:bg-emerald-50`…). Isso é proibido pela R4, então não serve de modelo para tela nova.
- **Proposta:** o `layout-main/` é o mesmo chassi, com os mesmos IDs e classes do app (`#primary-rail`, `#sub-sidebar`, `.rail-item`, `.sb-section-btn`, `.subnav-link`…). Ele usa só tokens e componentes `ttsc-*` e passa no `ds-check`. Sugestão: registrar no catálogo uma entrada `AppShell` apontando para `layout-main/README.md`.

## GAP-06 — variante `kpi-table` em `records`

- **Onde:** `layout-main/index.html` é uma lista de registros com uma faixa de KPIs acima da tabela. É uma composição diferente de `dense-table` (`paginas/referencia/registros-tabela.html`), e a R7 não aceita duas páginas com a mesma variante.
- **Proposta:** acrescentar `kpi-table` às variantes permitidas de `records` no `docs/ai/START-HERE.md`, com a regra: KPIs calculados sobre o mesmo conjunto da tabela, no máximo 4, acima da lista.

## GAP-07 — gaveta do rail embaixo do fundo

- **Onde:** o `bundle.css` (regras do chassi) põe `#navigation-backdrop:not([hidden])` em `z-index: var(--ttsc-z-backdrop)` (1040). Também tem `#primary-rail-wrapper:hover, #primary-rail-wrapper:focus-within { z-index: 50 !important; }`. Com a gaveta aberta o foco está dentro do rail, então o rail cai para 50 e fica **embaixo** do fundo: no celular a gaveta aparecia borrada (`backdrop-filter: blur`) e não recebia toque.
- **Contorno:** `layout-main/css/layout.css`, seção 7, põe o fundo em `calc(var(--ttsc-z-floating) + 5)` (45): acima do header e do rail fechado, abaixo das gavetas. Não usa `!important`.
- **O DS precisa:** tirar o `z-index: 50 !important` do rail quando ele é gaveta, ou usar `--ttsc-z-drawer` nos dois casos.
