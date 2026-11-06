# Layout main — chassi completo do TotusTuus

Página base com as cinco regiões do sistema: **header | sidebar (rail) | sub-sidebar | container | footer**. HTML, CSS e JS ficam em arquivos separados e comentados. Usa os tokens do design system e os mesmos IDs e classes do chassi real do app (`layouts/main.php`, `components/Navigation/README.md`). Assim você cola o kit no app sem renomear nada.

Para ver: abra `index.html` no navegador. Não precisa de servidor nem de build.

## Arquivos

```
layout-main/
├── index.html           Estrutura das 5 regiões, sprite de ícones e página de exemplo
├── css/
│   ├── tokens.css       Variáveis do design system (cores, espaços, raios, sombras, camadas, medidas do layout)
│   ├── base.css         Reset, tipografia, foco visível, ícones, utilitários, movimento reduzido
│   ├── layout.css       Posição e tamanho das regiões e as gavetas abaixo de 1100px
│   └── components.css   Aparência das peças: botões, header, menus, rail, sub-sidebar, container, footer
├── js/
│   └── layout.js        Comportamento: gavetas, rail, sub-sidebar, sanfonas, filtro, busca, menus, tema
└── README.md            Este documento
```

Carregue os CSS nesta ordem: `tokens.css → base.css → layout.css → components.css`. O JS vai com `defer`.

## Anatomia

```
┌──────────────────────────────── header 56px ─────────────────────────────────┐
│ [☰][▤] TT TotusTuus │ Organização ▾ │ Unidade ▾ │ Período ▾   🔍 Ctrl K  📅 🔔 ? ◐ AR │
├────────┬──────────────────────┬──────────────────────────────────────────────┤
│ rail   │ sub-sidebar 320px    │ container (main#main-viewport) — rola sozinho │
│ 60px   │ ┌ cabeçalho módulo ┐ │  breadcrumb                                    │
│  ↓     │ │ filtro  (/)      │ │  título + ações                                │
│ 288px  │ │ ▾ Seção      (4) │ │  conteúdo da página                            │
│ (hover │ │   link ativo     │ │                                                │
│  foco  │ │ ▸ Seção      (3) │ │                                                │
│  ou    │ └ ação principal ┘ ├──────────────────────────────────────────────┤
│  pino) │                      │ footer 40px                                    │
└────────┴──────────────────────┴──────────────────────────────────────────────┘
```

| Região | Elemento | Medida (token) | Camada |
|---|---|---|---|
| 1. Header | `header.app-header[data-od-id="topnav"]` | `--ttsc-header-h` 56px | `--ttsc-z-navigation` 30 |
| 2. Sidebar (rail) | `#primary-rail-wrapper > aside#primary-rail` | `--ttsc-rail-w` 60px; 288px expandido | `--ttsc-z-floating` 40 |
| 3. Sub-sidebar | `aside#sub-sidebar` | `--ttsc-sub-sidebar-w` 320px | normal |
| 4. Container | `main#main-viewport[data-od-id="content"]` | o que sobra; padding 16/20px e 64px no fim | normal |
| 5. Footer | `footer.app-footer` | `--ttsc-footer-h` 40px | normal |
| Fundo das gavetas | `#navigation-backdrop` | tela toda | `--ttsc-z-backdrop` 1040 |
| Gavetas (< 1100px) | rail e sub-sidebar | até 320px | `--ttsc-z-drawer` 1050 |
| Menus suspensos | `.menu` | 220px mínimo | `--ttsc-z-dropdown` 105 |

Só o container rola. O header e o footer ficam fixos na tela.

## IDs e classes

### Header
| Seletor | Função |
|---|---|
| `.hdr-left`, `.hdr-right` | Lados esquerdo e direito |
| `.hdr-nav-toggles` | Botões das gavetas; só aparecem abaixo de 1100px |
| `#btn-mobile` | Abre o rail (`aria-controls="primary-rail-wrapper"`) |
| `#btn-sub-sidebar` | Abre o sub-sidebar (`aria-controls="sub-sidebar"`) |
| `#btn-org-dropdown`, `#btn-unit-dropdown`, `#btn-period-dropdown` | Contexto: organização, unidade e período letivo |
| `#global-search` | Busca global (Ctrl+K ou ⌘K) |
| `#btn-search-sm` | Busca no celular (abaixo de 600px) |
| `#btn-notifications` + `.badge` | Notificações com contador |
| `#btn-theme` | Alterna entre tema claro e escuro |
| `#btn-user-menu` | Menu da conta |

### Rail
| Seletor | Função |
|---|---|
| `#btn-sidebar-portal` | Troca de portal |
| `details.portal-rail-group[data-group]` | Grupo com subitens; lembra se está aberto (`data-group` é a chave) |
| `a.rail-item` | Item; `.rail-label` é o texto e só aparece com o rail expandido |
| `.rail-item.is-active` + `aria-current="page"` | Página atual |
| `#btn-rail-pin` | Fixa o rail expandido (só no desktop) |

### Sub-sidebar
| Seletor | Função |
|---|---|
| `.sb-head` (`.sb-tile`, `.sb-title`, `.sb-sub`) | Cabeçalho do módulo |
| `#subsidebar-collapse-btn` | Recolhe o sub-sidebar (no celular, fecha a gaveta) |
| `#sub-sidebar-expand-btn` | Reabre o sub-sidebar; fica no cabeçalho da página |
| `.sb-search-filter > input#subsidebar-filter` | Filtro dos links (atalho "/") |
| `.subnav-group` | Seção |
| `button.sb-section-btn[aria-expanded][aria-controls]` | Abre e fecha a seção; `.sb-count-pill` mostra a contagem |
| `.subnav-accordion-content.is-open` / `.is-closed` | Lista de links da seção |
| `a.subnav-link.is-active` + `aria-current="page"` | Link atual; `.subnav-link__tag` é o selo de pendência |
| `#subsidebar-empty` | Mensagem quando o filtro não encontra nada |
| `.sb-foot` | Ação principal do módulo |

### Container (exemplo)
`.page`, `.breadcrumb`, `.page-header` (`__lead`, `__actions`), `.kpis`, `.card` (`__head`, `__body`, `__foot`), `.table-wrap > .table`, `.status--ok|warn|danger`, `.btn`, `.btn--primary`. São peças de exemplo: troque pelos componentes do design system (DataTable, KPI, PageModel) na página real.

### Footer
`.app-footer` contém a versão, os links `.ftr-links` e o estado do sistema `.ftr-status`.

## Comportamentos (`js/layout.js`)

| Função | O que faz | Guarda preferência |
|---|---|---|
| `initDrawers` | Abaixo de 1100px abre e fecha as gavetas. Atualiza `aria-expanded` e mostra o fundo. A gaveta fechada recebe `inert`. Esc ou clique no fundo fecha a gaveta e devolve o foco ao botão. Abrir uma gaveta fecha a outra. Um link clicado fecha a gaveta. | — |
| `initRailPin` | Fixa o rail expandido | `ttsc.layout.railPinned` |
| `initPortalGroups` | Lembra os grupos abertos do rail. O grupo da página atual sempre abre. | `ttsc.layout.portalGroups` |
| `initSubSidebar` | Recolhe e expande o sub-sidebar no desktop, levando o foco junto | `ttsc.layout.subSidebarCollapsed` |
| `initAccordions` | Abre e fecha as seções do sub-sidebar | — |
| `initFilter` | Filtra os links sem considerar acentos. Abre as seções que têm resultado e esconde as vazias. "/" foca o filtro e Esc limpa. | — |
| `initSearch` | Ctrl+K ou ⌘K foca a busca. No celular a busca abre sobre o header. | — |
| `initMenus` | Menus do header: setas, Home/End, Esc e Tab. Itens de escolha marcam `aria-checked`, atualizam o texto do botão e disparam o evento `ttsc:context-change`. | — |
| `initTheme` | Alterna `data-theme` no `<html>`. Na primeira visita segue o tema do sistema operacional. | `ttsc.layout.theme` |

As preferências ficam em `localStorage`. Todo acesso tem `try/catch`: com armazenamento bloqueado o layout funciona igual, só não lembra a escolha.

Para reagir à troca de organização, unidade ou período:

```js
document.addEventListener('ttsc:context-change', function (e) {
  // e.detail.context: 'btn-org-dropdown' | 'btn-unit-dropdown' | 'btn-period-dropdown'
  // e.detail.value:   valor escolhido (data-value do item)
});
```

## Larguras

| Largura | O que muda |
|---|---|
| ≥ 1100px | Rail de 60px que expande, sub-sidebar fixo e recolhível |
| < 1100px | Rail e sub-sidebar viram gavetas; aparecem os botões ☰ e ▤ no header |
| < 900px | Somem os seletores de unidade e período, o nome do usuário e o atalho da busca |
| < 600px | Somem a marca por extenso, a organização, o calendário, a ajuda e os links do rodapé. A busca vira ícone e as ações da página ocupam a largura toda. |
| 320px | Sem rolagem horizontal (testado) |

No celular, a troca de organização, unidade e período precisa de outro acesso. No app ela fica na tela de contexto ou no menu da conta. O kit só esconde os seletores.

## Acessibilidade (WCAG 2.2 AA)

- Link "Pular para o conteúdo" leva ao `main#main-viewport`.
- Marcos com rótulo: `header`, `aside` "Menu principal", `aside` "Menu do módulo", `nav` do breadcrumb, `main` e `footer`.
- Todo botão só com ícone tem `aria-label`, e todo ícone tem `aria-hidden="true"`.
- O foco visível usa o contorno de 2px na cor de destaque. O rail expande também com o foco do teclado (`:focus-within`), não só com o mouse.
- O estado de cada controle fica em `aria-expanded`, `aria-pressed`, `aria-current` e `aria-checked`.
- A gaveta fechada recebe `inert`, então o Tab não entra nela.
- Com `prefers-reduced-motion` as transições ficam praticamente instantâneas.
- O kit não usa JavaScript inline nem atributos `on*=` (ADR-07, ACH-01).

## Temas

`tokens.css` define o tema claro em `:root` e `[data-theme="light"]` e o tema escuro em `[data-theme="dark"]`. As peças usam só variáveis, então os dois temas funcionam sem CSS extra. Para mudar cores, altere `tokens.json` no design system e copie de novo para `tokens.css`. Não escreva cores soltas nos componentes.

## Ícones

Os ícones são um sprite SVG no topo do `index.html` (`<symbol id="i-*">`), com traço na cor do texto. Uso:

```html
<svg class="icon" aria-hidden="true"><use href="#i-academic"/></svg>
```

O Font Awesome Pro do app é licenciado e não pode ser distribuído no kit. No app, você pode trocar os `<svg>` por `<i class="fa-...">` sem mudar o resto.

## Como levar para o app

1. Copie os quatro CSS e o `layout.js` para os assets do app. Se o app já carrega os tokens do design system, use o dele em vez de `tokens.css`.
2. Em `layouts/main.php`, use a estrutura do `index.html`: `.app-shell > header + .app-body > (#primary-rail-wrapper, #sub-sidebar, .app-column > (main + footer))` e `#navigation-backdrop` no fim.
3. Gere os itens do rail e do sub-sidebar no servidor a partir das permissões do usuário (doc 78 do SDD). Marque a página atual com `.is-active` e `aria-current="page"`.
4. Coloque o conteúdo da página dentro de `main#main-viewport`. Mantenha o `#sub-sidebar-expand-btn` no cabeçalho da página.
5. Carregue o `layout.js` com `defer`. Não ligue eventos com `onclick=`.
6. Fonte: Inter pelo Google Fonts. Sem internet, o kit usa a fonte do sistema (`--font-sans`).
