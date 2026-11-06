# Contrato para agentes — Design System TotusTuus SoftCloud

Este repositório é a **base visual** do chassi. Toda tela de qualquer projeto é
montada com estes componentes. Não invente componente, classe, cor ou layout.

## Leia antes de codar (nesta ordem)

1. `docs/ai/START-HERE.md` — fluxo obrigatório em 6 passos.
2. `docs/ai/catalog.json` — catálogo por necessidade (197 componentes).
3. `docs/ai/rules.md` — proibições verificáveis (R1–R15).

## Regras rígidas (o validador reprova)

| # | Regra |
|---|---|
| R1 | Toda página tem `<meta name="viewport" content="width=device-width, initial-scale=1">`. |
| R2 | Nada de evento inline (`onclick=`, `onchange=`…); eventos em `.js` externo. |
| R3 | Cor só por token: `var(--ttsc-*)` ou classe `ttsc-*`. Proibido `#hex`, `rgb()`, `hsl()` em página. |
| R4 | Proibido utilitário de cor Tailwind (`bg-slate-200`, `text-emerald-600`, `border-rose-200`…). |
| R5 | Proibida largura fixa: `width`/`min-width` em px > 240. Use grid, flex e `clamp()`. |
| R6 | Toda página declara `<!-- page-spec {...} -->` com `archetype`, `variant`, `intent`, `density`. |
| R7 | Duas páginas do mesmo arquétipo **não** podem usar a mesma `variant`. |
| R8 | Página ≤ 80 KB (orçamento de contexto e de render). |
| R9 | `<table>` sempre dentro de `.ttsc-table-wrapper`. |
| R10 | Layout só com primitivos `.ttsc-container`, `.ttsc-stack`, `.ttsc-grid`, `.ttsc-split`, `.ttsc-toolbar`. |
| R11 | Ícone sozinho em botão exige `aria-label`; `<img>` exige `alt`. |
| R12 | `<button>` exige `type="button"` (ou `submit` em formulário). |
| R13 | IDs não podem repetir na mesma página. |
| R14 | Estados obrigatórios: vazio, carregando, erro — e o estado real dos dados. |
| R15 | Tema claro e escuro: nenhuma cor fixa; contraste AA verificado. |
| R16 | Proibido `data-model*` em página — não use renderizador genérico. |
| R17 | Proibido `<script>` inline; comportamento em arquivo externo. |
| R18 | Script de página `type="module"`, ≤ 8 KB, sem conhecer outras páginas. |
| R19 | Controller de página ≤ 8 KB (medido pelo validador, inclusive `.js`). |

> **JS:** componente = comportamento reutilizável; página = template próprio +
> controller pequeno. Ficha de dados só define conteúdo, nunca layout.
> Detalhes em `docs/ai/js-architecture.md`.

> **Ícones:** o repositório não versiona a fonte Font Awesome Pro (`fonts/`
> está no `.gitignore`) — `<i class="fa-light …">` vira quadrado vazio em clone
> limpo. Use SVG inline com `currentColor` (modelo em
> `paginas/referencia/assets/referencia.css`). Em produção, o shell pode servir
> `fonts/`.

## Como compor uma tela

```
archetype (dashboard | records | detail | settings | calendar | auth)
  → page-spec (variant + density + intent)
  → blocos do catálogo (não componentes soltos)
  → primitivos de layout
  → estados (vazio/carregando/erro)
  → ds:check
```

## Comandos

```bash
node scripts/ds-index.mjs              # regenera docs/ai/catalog.json
node scripts/ds-check.mjs <arquivos>   # valida páginas (exit 1 = reprovado)
node scripts/ds-check.mjs --all --report  # mede a dívida atual das 576 páginas
```

## Estrutura

- `components/<Nome>/README.md` — contrato do componente (fonte da verdade).
- `components/<Nome>/preview.html` — demonstração ao vivo.
- `components/ttsc.css` — **entrada única**: tokens + bundle + responsivo.
- `components/ttsc-responsive.css` — breakpoints, primitivos e correções mobile.
- `paginas/referencia/` — páginas-modelo aprovadas (copie a composição, não o HTML inteiro).
- `docs/ai/` — catálogo, regras e fluxo para agentes.
- `docs/v2/` e `docs/sdd/` — especificação do produto (consulta, não instrução de UI).

## Definição de pronto

- [ ] `node scripts/ds-check.mjs` passa nos arquivos alterados.
- [ ] Verificado em **360 / 768 / 1280** px, sem rolagem horizontal da página.
- [ ] Tema claro e escuro.
- [ ] Estados vazio, carregando e erro implementados (não só o caminho feliz).
- [ ] Nenhum componente novo fora do catálogo (lacuna registrada em `docs/ai/gaps.md`).

> Componente ausente não se resolve inventando: registre a lacuna, use o mais
> próximo e proponha a entrada no catálogo.
