Sistema visual do chassi **TotusTuus SoftCloud**, o padrão Emerald Cloud usado em `/developer/dashboard` e `/developer/commercial`. Toda página nova dos portais (developer, admin, acadêmico, financeiro, aluno e responsável) é montada com estes tokens, com a biblioteca **ttscui** (classes `ttsc-*` e atributos `data-ttsc-*`) e com os modelos HTML, CSS, JS e SQL de cada componente.

## Como usar este sistema

1. Carregue nesta ordem: Inter → `tokens.css` → `components/bundle.css` → `components/bundle.js`. O bundle expõe `window.TTSC` e inicializa todos os `data-ttsc-*` quando o DOM fica pronto. Depois de inserir HTML dinâmico (drawer, AJAX), chame `TTSC.init()`.
2. No app, a ordem equivalente é a do `resources/views/app/layouts/main.php`: `inter.css` → `tailwind-runtime.css` → `ttsc.design-system.css` / `ttsc.supabase.css` / `ttsc.luxury-commercial.css` → `ttsc.shell-layout.css` → `ttsc.commercial.css` → widgets → módulos de rota.
3. Para montar uma tela, abra a página do componente e copie o modelo **HTML**. Aplique o **CSS** só quando a página pedir uma extensão. O **JS** vai para `assets/js/core/ttsc.<nome>.js`. O **SQL** vai para o repositório ou serviço do módulo, sempre com *prepared statements*.
4. Escreva cores, raios, sombras e espaços sempre como token `var(--ttsc-…)`, nunca como valor literal. Os módulos de rota (camada 7) não redefinem tokens nem estilizam seletores globais.

## Conteúdo e voz

- **Idioma:** pt-BR com acentuação completa. Algumas strings antigas do `lang/` estão sem acento (“Previsao”, “modulos”, “Tecnico”); nas telas novas, sempre “Previsão”, “módulos”, “Técnico”.
- **Títulos** de página, card e drawer em Title Case, como na fonte: “Razão Geral & Balancete”, “Conciliação de Gateways”, “Documentos Fiscais Recebidos”. O “&” é aceito em títulos.
- **Descrições e ajudas** em frase normal, terminadas em ponto: “Escolha o conjunto de serviços para analisar.”
- **Placeholders de busca** dizem o que se busca e terminam com reticências: “Buscar oportunidades, contatos, propostas...”.
- **Botões** levam verbo no infinitivo ou substantivo de ação: “Salvar”, “Exportar”, “Nova matrícula”, “Cancelar”.
- Tom institucional e direto, sem gírias, sem “você” enfático e sem emoji. Siglas legais por extenso na primeira menção: “Lei 13.709/2018 (LGPD)”.
- **Números** no formato pt-BR: `1.234,56`, `R$ 1.250,00`, `87%`, datas `21/10/2026`, horas `14:30`.
- **Status** chegam do banco como código (`active`, `pending`) e aparecem traduzidos pelo `lang/pt_BR/page_sources.php` (`<rota>|status|<valor>`). Exportações JSON, XML e SQL mantêm o código.

## Fundamentos visuais

### Cor

| Papel | Token | Regra |
|---|---|---|
| Fundo da página | `ttsc-canvas` | Toda tela começa aqui. |
| Superfícies | `ttsc-surface` | Cards, drawers, modais, menus. `ttsc-surface-2` para áreas rebaixadas. |
| Texto | `ttsc-text` → `ttsc-text-2` → `ttsc-text-muted` | Título/valor → corpo → rótulo/metadado. Todos ≥ 4,5:1 nos dois temas. |
| Marca/ação | `ttsc-accent` (#3ecf8e) | Só como **preenchimento** (botão primary, switch, progresso, item ativo). Texto sobre ele: `ttsc-accent-on`. |
| Texto verde | `ttsc-accent-text` | Links e valores positivos. O verde de marca como texto sobre branco fica em 2:1, por isso este token existe. |
| Estados | `ttsc-success` · `ttsc-warning` · `ttsc-danger` · `ttsc-info` | Preenchimentos e ícones. Para texto use `ttsc-warning-text`, `ttsc-danger-text`, `ttsc-info-text`. Um estado nunca depende só da cor: sempre há rótulo ou ícone. |
| Bordas | `ttsc-border` · `ttsc-border-soft` · `ttsc-border-strong` | Card e tabela → linha → hover. Bordas são decorativas e não carregam significado sozinhas. |
| Backdrop | `ttsc-scrim` | Modal e drawer. |

O verde do **logotipo** (`ttsc-logo`, #10b981) é diferente do verde da UI e fica restrito à marca. A escala `ttsc-primary-50…950` serve para gráficos e fundos tonais.

### Tipografia

Inter em toda a interface, corpo de **13px** (`body`). O tema escuro usa os mesmos pesos.

- `page-title` (20/28, 700, −0,01em) no cabeçalho da página. `hero` (24/32) só em telas de boas-vindas.
- `subheading` (16/24, 600) em títulos de card, drawer e modal.
- `body-md` (14) em formulários longos, `body` (13) em tabelas e corpo, `body-sm` (12) em hints, `meta` (11, 500, caixa alta no breadcrumb e no cabeçalho de tabela), `pill` (10, 600) em badges.
- `code` (mono 12) em IDs, valores KPI e SQL.

### Espaço, raio e elevação

- Grade de 4px: `ttsc-space-1…16`. O padding de card é `ttsc-space-5` (20px), o gap entre seções `ttsc-space-6`, entre KPIs `ttsc-widget-gap` (14px) e entre campos `ttsc-space-4`.
- Raios: `ttsc-radius-xs` (6) em badge e checkbox, `ttsc-radius-sm` (8) em menu e tooltip, `ttsc-radius-control` (12) em botão e input, `ttsc-radius-surface` (16) em card, modal e drawer, `ttsc-radius-pill` em status e avatar.
- Elevação discreta, com borda antes de sombra. `ttsc-shadow-sm` nos cards; no hover o card troca a borda para `ttsc-border-strong` e não sobe. `ttsc-shadow-md` em dropdowns, `ttsc-shadow-lg` em toasts, `ttsc-shadow-xl` em modais e drawers.
- Camadas: `ttsc-z-navigation` (30) < `ttsc-z-floating` (40) < `ttsc-z-dropdown` (105) < `ttsc-z-backdrop` (1040) < `ttsc-z-drawer` (1050) < `ttsc-z-modal` (1060) < `ttsc-z-toast` (1080) < `ttsc-z-tooltip` (1100).

### Layout do chassi

Topbar `ttsc-header-h` (56px), rail de ícones `ttsc-rail-w` (60px, expande ao hover), sub-sidebar `ttsc-sub-sidebar-w` (320px), rodapé `ttsc-footer-h` (40px). Conteúdo com padding 16px (20px ≥ sm) e 64px de folga no fim da rolagem. Drawers do CRUD genérico em `ttsc-drawer-md` (560px). Tabelas com linha `ttsc-row-normal` (48px), ou `ttsc-row-compact` (36px) em telas densas.

### Movimento

150ms para hover e foco, 200ms para abrir e fechar menus, 300–360ms para drawer e modal, com `cubic-bezier(.4,0,.2,1)`. Sem animações decorativas. Respeite `prefers-reduced-motion`.

### Foco e estados

Todo elemento interativo mostra contorno sólido de 2px em `ttsc-accent`, com offset de 2px. **Atenção:** esse anel tem 2:1 sobre `ttsc-surface` claro, abaixo dos 3:1 recomendados. O valor está mantido igual ao da fonte (`ttsc.css`); em telas críticas de acessibilidade, reforce com `box-shadow: 0 0 0 4px var(--ttsc-accent-soft)`. Desabilitado = 50% de opacidade e sem ponteiro. Erro de campo = `aria-invalid="true"` + mensagem em `ttsc-danger-text`.

### Temas

Há dois temas: **Claro** e **Escuro (Obsidian)**. Os tokens trocam por `[data-theme="dark"]`. No app, a classe `.dark` em `<html>` produz o mesmo efeito, porque o bundle aceita os dois seletores. A preferência do usuário fica em `user_preferences.theme`; ver [ThemeSwitch](components/ThemeSwitch/README.md).

## Iconografia

- Font Awesome Pro 7.2, estilo **Light** (peso 300): `<i class="fa-light fa-calendar"></i>`. Os arquivos estão no repo em `assets/fonts/fontawesome.v7.2.0`; aqui só o `fa-light-300.woff2` é carregado.
- Tamanho padrão de 1em, acompanhando o texto. Em botões o ícone vem à esquerda do rótulo, com gap de 4–8px. Ícone sozinho exige `aria-label` no botão.
- Cor herdada do texto (`currentColor`). Ícones de estado usam o token do estado.
- Sem emoji e sem ícones de outras famílias na UI. Os *keenicons* vendorizados no repo não fazem parte deste padrão.
- Nota de manutenção: `assets/fonts/fontawesome.v7.2.0/css/fontawesome.min.css` está com os códigos dos ícones corrompidos (UTF-8 duplo). O app carrega `all.css`, que está correto, e este bundle usa `fontawesome.css`. Não troque para o `.min`.

## Marca

O logotipo e o símbolo estão em **Assets › Logos**. Use `logo-light.svg` sobre superfícies claras, `logo-dark.svg` sobre escuras e `logo-mark.svg` no rail e no favicon. Nunca recolorir, aplicar sombra ou colocar sobre `ttsc-accent`.

## Componentes e bibliotecas

- **ttscui** (`assets/vendors/ttscui/ttscui.js`, derivado do KTUI) entrega Accordion, Carousel, Clipboard, Collapse, Context Menu, DataTable, Dismiss, Drawer, Dropdown, Image Input, Modal, Pin Input, Range Slider, Rating, Reparent, Repeater, Scrollable, Scrollspy, Scrollto, Select, Stepper, Sticky, Tabs, Theme Switch, Toast, Toggle, Toggle Password e Tooltip, todos em `window.TTSC`.
- **Plugins de terceiros** (DataTables, FullCalendar, ApexCharts, amCharts, TinyMCE, Select2, flatpickr…) ficam em `vendor/` deste sistema, nas mesmas versões vendorizadas no repo quando existem. Cada um é tematizado com tokens nos dois temas. Ver [3rd-Party Plugin](components/ThirdPartyPlugin/README.md).
- **Implementações TTSC** (BlockUI, Dialer, Password Meter, Quick Search, Scrolltop, Swapper, Cookie Alert, Timeline…) são JS puro, sem dependências, pronto para `assets/js/core/`.
- **Modelos aprovados** (grupo Modelos) são os blocos de página do chassi: cabeçalho, banner, abas segmentadas, KPI, Data Table, Cards, Kanban v2.3, Analytics, drawers, configurações e estado vazio. Eles vêm com o CSS e o JS reais do app (`vendor/app`) e com `TTSCModelKit`, que traz os mesmos renderizadores de `docs/model/app` alimentados por uma ficha de página (`models/academico.json`, no formato de `docs/model/app/specs`). Para montar uma página nova, comece por eles, não pelos componentes soltos.
- **Arquétipos de página**: escolha um por página (Dashboard, Records, Pipeline, History, Report, Settings, Calendar, Auth). O arquétipo define as abas, qual delas abre primeiro e as ações do cabeçalho.
- **Widgets** são os cartões de análise aprovados em `docs/model/widgets`. Os números de amostra precisam ser trocados por um provider do módulo antes de ir para produção.
- Itens que aparecem em mais de uma lista (ex.: Base › Buttons e Componentes › Button) têm **uma** página, que indica a outra lista no topo.

## SQL

- Os modelos SQL rodam em **MariaDB 10.11** (XAMPP/phpMyAdmin) e **MySQL 8**. Use crase em nomes reservados (`row_number`, `rank`).
- **Banco master** (`totustuus_master`): usuários, papéis e permissões (`permissions`, `role_permission`, `user_role`). **Banco do tenant**: dados acadêmicos (`courses`, `classes`, `enrollments`, `attendance`, `events`…).
- Convenções: chave `uuid char(36)`, FKs `<entidade>_uuid`, soft delete por `deleted_at` (sempre filtrar `deleted_at IS NULL`), `created_at` / `updated_at`, parâmetros nomeados `:param`.
- A interface nunca recebe colunas sensíveis (senha, tokens). Toda escrita passa pelo `DomainCrudController`, com `_token` CSRF, `write_permission` e validação de referências.
