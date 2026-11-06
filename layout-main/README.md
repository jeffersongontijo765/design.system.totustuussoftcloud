# Layout main — chassi completo do TotusTuus

Página base com as cinco regiões do sistema: **header | sidebar (rail) | sub-sidebar | container | footer**.

- **Design system:** a página é montada sobre `components/ttsc.css` (tokens, bundle, ponte de tema e camada responsiva). Usa os componentes `ttsc-*` do catálogo e os primitivos `ttsc-container`, `ttsc-stack`, `ttsc-grid` e `ttsc-toolbar`.
- **Arquivos separados:** o HTML tem só a estrutura, cada CSS tem uma responsabilidade e o JS é feito de módulos pequenos. Tudo comentado.
- **Mesmos IDs e classes do chassi real do app** (`layouts/main.php`, `components/Navigation/README.md`): dá para levar ao app sem renomear nada.
- **Validação:** passa no `node scripts/ds-check.mjs layout-main/index.html` com 0 erros e 0 avisos (R1 a R19).

## Como abrir

Os scripts são módulos ES (`type="module"`, regra R18). O navegador não carrega módulos de `file://`, então sirva a pasta **acima** de `layout-main/`, a que contém `components/`:

```bash
# na raiz do repositório (ou na pasta extraída do zip)
python3 -m http.server 8000
# abra http://localhost:8000/layout-main/index.html
```

Para ver os estados do bloco de dados: `index.html?estado=vazio`, `?estado=carregando` e `?estado=erro`.

## Arquivos

```
layout-main/
├── index.html              Estrutura das 5 regiões, sprite de ícones, página de exemplo com 4 estados
├── css/
│   ├── base.css            Corpo, foco visível, ícones do sprite, link "pular para o conteúdo"
│   ├── layout.css          Posição e tamanho das regiões; gavetas abaixo de 1100px
│   └── components.css      Peças próprias do chassi (hdr-*, rail-*, sb-*, subnav-*, ftr-*) e lacunas do DS
├── js/
│   ├── layout.js           Entrada do chassi: importa e inicia os módulos
│   ├── chassi/
│   │   ├── util.js         Corte de 1100px, chaves das preferências, localStorage com try/catch
│   │   ├── theme.js        Tema claro/escuro
│   │   ├── drawers.js      Gavetas do rail e do sub-sidebar
│   │   ├── rail.js         Fixar o rail expandido; grupos lembram o estado
│   │   ├── sub-sidebar.js  Recolher/expandir, seções sanfona, filtro e atalho "/"
│   │   ├── search.js       Busca global, Ctrl+K / ⌘K, busca no celular
│   │   └── menus.js        Menus do header e seletores de contexto
│   └── pagina-turmas.js    Controller só desta página: busca na tabela e estados
└── README.md               Este documento
```

Ordem de carga:

```html
<link rel="stylesheet" href="../components/ttsc.css">   <!-- design system -->
<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="css/layout.css">
<link rel="stylesheet" href="css/components.css">
…
<script type="module" src="js/layout.js"></script>         <!-- chassi -->
<script type="module" src="js/pagina-turmas.js"></script>  <!-- página -->
```

## Anatomia

```
┌─────────────────────────────── header 56px ───────────────────────────────┐
│ [☰][▤] TT TotusTuus │ Organização ▾ Unidade ▾ Período ▾   🔍 Ctrl K 📅 🔔 ? ◐ AR │
├────────┬─────────────────────┬───────────────────────────────────────────┤
│ rail   │ sub-sidebar 320px   │ container (main#main-viewport) rola sozinho │
│ 60px   │ cabeçalho do módulo │  breadcrumb · título · ações                │
│  ↓     │ filtro (/)          │  KPIs (ttsc-grid--kpi)                      │
│ 288px  │ ▾ Seção        (3)  │  card com tabela (ttsc-table-wrapper)       │
│ hover, │   link ativo        │  estados: vazio · carregando · erro         │
│ foco   │ ▸ Seção        (4)  ├───────────────────────────────────────────┤
│ ou pino│ ação principal      │ footer 40px (quebra linha no celular)       │
└────────┴─────────────────────┴───────────────────────────────────────────┘
```

| Região | Elemento | Medida (token) | Camada |
|---|---|---|---|
| 1. Header | `header.app-header[data-od-id="topnav"]` | `--ttsc-header-h` 56px | `--ttsc-z-navigation` |
| 2. Rail | `#primary-rail-wrapper > aside#primary-rail` | `--ttsc-rail-w` 60px; 288px expandido | `--ttsc-z-floating` |
| 3. Sub-sidebar | `aside#sub-sidebar` | `--ttsc-sub-sidebar-w` 320px | normal |
| 4. Container | `main#main-viewport[data-od-id="content"]` > `.ttsc-container` | o que sobra | normal |
| 5. Footer | `footer.app-footer` | `--ttsc-footer-h` 40px (mínimo) | normal |
| Fundo das gavetas | `#navigation-backdrop` | tela toda, cor `--ttsc-scrim` | `--ttsc-z-backdrop` |
| Gavetas (< 1100px) | rail e sub-sidebar | até 320px | `--ttsc-z-drawer` |
| Menus | `.ttsc-dropdown-menu` | 220 a 320px | `--ttsc-z-dropdown` |

Só o container rola; header e footer ficam fixos.

## Componentes do design system usados

| Onde | Componente (catálogo) | Classes |
|---|---|---|
| Botões do header, rail e página | Button | `ttsc-btn`, `-ghost`, `-outline`, `-primary`, `-icon`, `-sm` |
| Busca global e filtro do menu | Input | `ttsc-input`, `ttsc-input-sm` (ícone dentro) |
| Atalhos | Kbd | `ttsc-kbd`, `ttsc-kbd-xs` |
| Menus (contexto, notificações, conta) | Dropdown | `ttsc-dropdown-menu`, `-sub`, `-link`, `-separator` |
| Contador, contagem das seções, situação | Badge | `ttsc-badge`, `-sm`, `-light`, `-outline`, `-success`, `-warning`, `-destructive` |
| Usuário | Avatar | `ttsc-avatar`, `ttsc-avatar-fallback` |
| Trilha | Breadcrumb | `ttsc-breadcrumb`, `-item`, `-link`, `-separator`, `-page` |
| Cabeçalho da página | primitivos | `ttsc-page-header`, `__actions`, `ttsc-title-fluid`, `ttsc-toolbar` |
| Indicadores | Card (KPI) | `ttsc-grid--kpi`, `ttsc-card-kpi`, `ttsc-kpi-label`, `-value`, `-delta` |
| Lista | Card + Table | `ttsc-card-header`, `-heading`, `-title`, `-toolbar`, `ttsc-card-table`, `ttsc-table-wrapper--scroll`, `ttsc-table-highlight`, `ttsc-hide-sm` |
| Paginação | Pagination | `ttsc-pagination-standard`, `ttsc-pagination`, `-item` |
| Vazio, sem resultado e erro | EmptyState | `ttsc-empty-state`, `is-no-data`, `is-no-results`, `is-error` |
| Carregando | Skeleton | `ttsc-skeleton`, `-line`, `-block` |

O que o DS ainda não tem fica em `css/components.css`, seção 6, e em `css/layout.css`, seção 7. Tudo está registrado em [`docs/ai/gaps.md`](../docs/ai/gaps.md) (GAP-01, GAP-03, GAP-04 e GAP-07).

O `bundle.css` já traz as regras do chassi do app (`#primary-rail`, `#sub-sidebar`, gavetas, `.sb-app …`). O `css/layout.css` do kit repete a mesma geometria, para o kit funcionar mesmo sem essas regras, e não briga com elas: nenhum `!important`.

## IDs e classes do chassi

### Header
| Seletor | Função |
|---|---|
| `.hdr-left`, `.hdr-right` | Lados do header |
| `.hdr-nav-toggles` > `#btn-mobile`, `#btn-sub-sidebar` | Abrem as gavetas (só abaixo de 1100px); `[data-drawer-toggle][aria-controls]` |
| `.hdr-context-group` > `#btn-org-dropdown`, `#btn-unit-dropdown`, `#btn-period-dropdown` | Contexto ativo: organização, unidade, período letivo |
| `#btn-context-sm` | Os três contextos num menu só (abaixo de 1200px) |
| `#global-search` | Busca global (Ctrl+K / ⌘K); `#btn-search-sm` no celular |
| `#btn-notifications` + `.hdr-counter` | Notificações com contador |
| `.hdr-shortcut` | Calendário e ajuda (abaixo de 600px ficam só no menu da conta) |
| `#btn-theme` | Tema claro/escuro |
| `#btn-user-menu` | Menu da conta |
| `.hdr-menu-anchor` | Âncora de cada menu suspenso |

### Rail
| Seletor | Função |
|---|---|
| `#btn-sidebar-portal` | Troca de portal |
| `details.portal-rail-group[data-group]` | Grupo com subitens; `data-group` é a chave do estado salvo |
| `a.rail-item` + `.rail-label` | Item; o rótulo aparece com o rail expandido |
| `.rail-item.is-active` + `aria-current="page"` | Página atual |
| `#btn-rail-pin` | Fixa o rail expandido (desktop) |

### Sub-sidebar
| Seletor | Função |
|---|---|
| `.sb-head` (`.sb-tile`, `.sb-title`, `.sb-sub`) | Cabeçalho do módulo |
| `#subsidebar-collapse-btn` / `#sub-sidebar-expand-btn` | Recolhe / reabre (o segundo fica no cabeçalho da página) |
| `.sb-search-filter` > `#subsidebar-filter` | Filtro (atalho "/") |
| `.subnav-group` > `button.sb-section-btn[aria-expanded][aria-controls]` + `.sb-count-pill` | Seção sanfona com contagem |
| `.subnav-accordion-content.is-open` / `.is-closed` | Lista da seção |
| `a.subnav-link.is-active` + `aria-current="page"` | Link atual |
| `#subsidebar-empty` | "Nenhum item encontrado" |
| `.sb-foot` | Ação principal do módulo |

### Container e footer
O container usa `.ttsc-container.ttsc-stack[data-turmas]`, com um bloco por estado: `[data-state="data|empty|loading|error"]`. O footer `.app-footer` tem versão, `.ftr-links` e `.ftr-status`.

## Comportamentos

| Módulo | O que faz | Preferência salva |
|---|---|---|
| `drawers.js` | Abaixo de 1100px abre e fecha as gavetas e atualiza `aria-expanded`. A gaveta fechada fica `inert`. Ao abrir, o foco vai ao filtro. Esc, clique no fundo ou num link fecham, e o foco volta ao botão. Abre uma gaveta por vez. Dispara `ttsc:drawer-change`. | — |
| `rail.js` | Controla `.is-expanded`: rail fixado no desktop, ou gaveta do rail aberta no celular (evento `ttsc:drawer-change`). Os grupos lembram se estão abertos, e o grupo da página atual sempre abre. | `ttsc.layout.railPinned`, `ttsc.layout.portalGroups` |
| `sub-sidebar.js` | Recolhe e expande levando o foco junto; no celular, recolher fecha a gaveta. As seções são sanfonas. O filtro ignora acentos, abre as seções com resultado e esconde as vazias. "/" foca o filtro e Esc limpa. | `ttsc.layout.subSidebarCollapsed` |
| `search.js` | Ctrl+K / ⌘K foca a busca. Abaixo de 600px a busca abre sobre o header e fecha com Esc. | — |
| `menus.js` | Menus com `.open` (contrato do `.ttsc-dropdown-menu`). Teclado: ↓ abre, ↑ ↓ Home End navegam, Esc fecha e devolve o foco, Tab fecha. Os itens de contexto sincronizam o desktop e o celular, atualizam os textos `[data-context-value]` e disparam `ttsc:context-change`. | — |
| `theme.js` | Muda `data-theme` no `<html>`. Na primeira visita segue o sistema operacional. | `ttsc.layout.theme` |
| `pagina-turmas.js` | Busca na tabela com contador e "sem resultado". Mostra um estado por vez. "Tentar novamente" e "Limpar busca". | — |

Todo acesso ao `localStorage` tem `try/catch`: sem armazenamento o layout funciona igual, só não lembra a escolha.

Para reagir à troca de contexto (recarregar dados da unidade, por exemplo):

```js
document.addEventListener("ttsc:context-change", (e) => {
  // e.detail.context: "org" | "unit" | "period"
  // e.detail.value:   valor escolhido
});
```

## Larguras

O corte de 1100px é o do chassi real. Dentro do container valem os breakpoints do DS (480 / 768 / 1024 / 1280).

| Largura | O que muda (nada some, só muda de lugar) |
|---|---|
| ≥ 1200px | Tudo no header; rail de 60px que expande; sub-sidebar fixo e recolhível |
| < 1200px | Organização, unidade e período viram o botão `#btn-context-sm`, com as mesmas opções |
| < 1100px | Rail e sub-sidebar viram gavetas; aparecem os botões ☰ e ▤ |
| < 900px | Sai a dica "Ctrl K" (só dica) e o nome do usuário (continua no `aria-label` e no menu) |
| < 768px | A tabela esconde curso, turno e sala (`ttsc-hide-sm`), nunca a coluna da turma |
| < 600px | Calendário e ajuda ficam só no menu da conta; a busca vira ícone e abre sobre o header; o rodapé quebra linha |

Verificado no Chromium em 1440, 1280, 1024, 768, 390, 360 e 320px, nos dois temas: sem rolagem horizontal, sem erro de JavaScript, com gavetas, filtro, menus, atalhos e os quatro estados funcionando.

## Acessibilidade (WCAG 2.2 AA)

- "Pular para o conteúdo" leva a `main#main-viewport`.
- Marcos com rótulo: header, "Menu principal", "Menu do módulo", trilha, main e footer.
- Botão só com ícone tem `aria-label`; ícones têm `aria-hidden="true"`; todo `<button>` tem `type`.
- Foco visível em `--ttsc-accent-text`. O rail expande também com o foco do teclado (`:focus-within`).
- Estados expostos: `aria-expanded`, `aria-pressed`, `aria-current`, `aria-checked`, `aria-busy`. Atalhos em `aria-keyshortcuts`.
- Gaveta fechada fica `inert`. Os menus seguem o padrão de menu do ARIA (setas, Home/End, Esc).
- Mensagens de estado com `role="status"` ou `role="alert"`.
- Movimento reduzido vem do DS (`.ttsc-page`). Sem evento inline e sem `<script>` inline.

## Temas

O `__tokens.css` do DS define o claro em `:root` / `[data-theme="light"]` e o escuro em `[data-theme="dark"]`. O kit usa só variáveis `--ttsc-*` e componentes `ttsc-*`, então os dois temas funcionam sem CSS extra.

**Correção feita no DS junto com este kit** (GAP-02): o `components/ttsc.css` carregava os tokens antes do bundle. Um bloco de apelidos dentro do bundle sobrescrevia 7 tokens no tema claro e deixava `--ttsc-border` e `--border` vazias, por causa de um ciclo entre as duas, e as bordas sumiam. Agora o bundle vem primeiro e os tokens depois. A correção também vale para as páginas de `paginas/referencia/`.

## Ícones

Sprite SVG no topo do `index.html` (`<symbol id="i-*">`), com traço `currentColor`, como no modelo de `paginas/referencia/`. Uso:

```html
<svg class="icon" aria-hidden="true"><use href="#i-academic"/></svg>
```

O Font Awesome Pro é licenciado e não está no repositório. Em produção, o shell pode servir `fonts/` e usar `<i class="fa-light …">`.

## Como levar para o app

1. Em `layouts/main.php`, use a estrutura do `index.html`: `body.sb-app > .app-shell.ttsc-page > header + .app-body > (#primary-rail-wrapper, #sub-sidebar, .app-column > (main + footer))`, com `#navigation-backdrop` no fim. A classe `sb-app` é o contrato do chassi do app (Navigation/README.md): o bundle usa essa classe para expandir o rail no hover e no foco.
2. Carregue `components/ttsc.css` e depois os três CSS do kit. Carregue `js/layout.js` como módulo, uma vez por página.
3. Gere os itens do rail e do sub-sidebar no servidor a partir das permissões do usuário (SDD, doc 78). Marque a página atual com `.is-active` e `aria-current="page"`.
4. Cada página escreve o próprio template dentro de `main#main-viewport > .ttsc-container`, com `page-spec`, primitivos e os quatro estados, e tem um controller próprio de até 8 KB (como `pagina-turmas.js`). Não use renderizador genérico (`data-model*`, R16).
5. Rode `node scripts/ds-check.mjs <página>` antes de publicar.

## Zip

`entregas/layout-main.zip` é gerado pelo `layout-main/empacotar.sh` e traz `layout-main/` junto com os cinco arquivos de `components/` que o `ttsc.css` importa. Basta extrair e servir a pasta.
