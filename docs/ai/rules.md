# Regras verificáveis — design system

Cada regra tem ID, exemplo errado e exemplo certo. O `scripts/ds-check.mjs`
implementa R1–R19 e falha com exit 1.

Arquétipos aceitos no `page-spec`: `dashboard`, `records`, `detail`, `settings`,
`calendar`, `auth` e `catalog` (galeria/documentação — isenta de R14, porque não
tem ciclo de dados).

## Cor

| ID | Errado | Certo |
|---|---|---|
| R3 | `<div style="background:#10b981">` | `<div class="ttsc-badge ttsc-badge-light ttsc-badge-success">` |
| R3 | `<i style="color:rgb(16,185,129)">` | `<i class="ttsc-text-success">` ou `color: var(--ttsc-success)` |
| R4 | `<div class="bg-slate-50 text-emerald-600">` | `<div class="ttsc-card ttsc-text-accent">` |

Motivo: o tema escuro só funciona se toda cor passar por token. Utilitário cru
(`slate-*`, `emerald-*`) não troca de tema e cria uma segunda linguagem visual —
foi a causa da divergência entre README e páginas.

## Layout e responsividade

| ID | Errado | Certo |
|---|---|---|
| R5 | `style="width:560px"` | `class="ttsc-split"` ou `width: min(560px, 100%)` |
| R10 | `style="display:flex;flex-direction:column;gap:16px"` | `class="ttsc-stack"` |
| R9 | `<table class="ttsc-table">` solta | `<div class="ttsc-table-wrapper"><table …>` |
| R1 | sem viewport | `<meta name="viewport" content="width=device-width, initial-scale=1">` |

Breakpoints oficiais (mobile-first):

| Token | Largura | Uso |
|---|---|---|
| `--ttsc-bp-sm` | 480px | telefone grande |
| `--ttsc-bp-md` | 768px | tablet retrato |
| `--ttsc-bp-lg` | 1024px | desktop / split ativa |
| `--ttsc-bp-xl` | 1280px | desktop largo |

Regras de comportamento:

- Abaixo de 640px: toolbar empilha, ações ocupam a linha, drawer vira tela cheia.
- Abaixo de 768px: colunas de baixa prioridade somem da tabela (`.ttsc-hide-sm`),
  nunca a coluna de identificação.
- Abaixo de 1024px: `ttsc-split` colapsa em uma coluna; o detalhe vem depois da lista.
- Tabela rola **dentro** do wrapper; a página nunca rola na horizontal.
- Tipografia usa `clamp()`; nunca um tamanho fixo que quebre em 360px.

## JavaScript

| ID | Errado | Certo |
|---|---|---|
| R16 | `<main data-model="page" data-model-tab="table">` | `<main class="ttsc-container">` com o template escrito na página |
| R17 | `<script>TTSCModelKit.render(ficha)</script>` | `<script type="module" src="./assets/registros.js"></script>` |
| R18 | Um `bundle.js` de 966 KB montando todas as telas | Módulo de componente + controller da página (≤ 8 KB) |

Teste rápido: se o layout da página muda porque você editou um JSON em
`models/`, há um renderizador genérico no caminho — e ele é o problema.

## Composição

| ID | Regra |
|---|---|
| R6 | `<!-- page-spec {...} -->` obrigatório, com `archetype`, `variant`, `intent`, `density`. |
| R7 | `variant` única por arquétipo entre as páginas do conjunto validado. |
| R8 | Página ≤ 80 KB. Acima disso, extraia blocos para partials. |

## Acessibilidade

| ID | Regra |
|---|---|
| R2 | Sem `onclick=`/`onchange=` inline. |
| R11 | Ícone sozinho → `aria-label`; imagem → `alt`. |
| R12 | `<button type="button">` (ou `submit`). |
| R13 | Nenhum `id` duplicado na página. |
| R14 | Estados vazio, carregando e erro implementados. |
| R15 | Contraste AA nos dois temas. |

## Ícones

O repositório **não versiona** a fonte Font Awesome Pro (licença; `fonts/` está
no `.gitignore`). Num clone limpo, `<i class="fa-light fa-…">` renderiza um
quadrado vazio.

- Referência: SVG inline com `stroke="currentColor"` — sprite no topo do
  `<body>` e `<svg class="ref-icon"><use href="#i-…"/></svg>`.
- Produção: o shell da aplicação pode servir `fonts/fa-light-300.woff2`.
- Nunca dependa de CDN de ícone em tela de produto (offline e CSP).

## O que **não** fazer

- Copiar uma página inteira e trocar os dados. É assim que se chega a 92% de
  similaridade entre 576 telas.
- Criar classe nova com prefixo próprio (`minha-tela-*`). Se o componente não
  existe, registre a lacuna.
- Esconder conteúdo no mobile para "resolver" overflow.
- Usar `!important` para vencer o bundle.
- Colocar número de exemplo (mock) sem indicar a origem do provider.
