# Inventário

Cada item das listas pedidas e a página que o documenta. Itens repetidos entre listas (ex.: **Base › Buttons** e **Componentes › Button**) apontam para a mesma página, que traz HTML, CSS, JS e SQL.

## Componentes

| Item | Página | Resumo |
|---|---|---|
| Accordion | [Accordion](components/Accordion/README.md) | Lista de seções recolhíveis do ttscui (`data-ttsc-accordion`) em que cada item abre e fecha o próprio painel, com uma ou várias seções abertas ao mesmo tempo (` |
| Avatar | [Avatar](components/Avatar/README.md) | Foto ou iniciais de uma pessoa (`.ttsc-avatar`), com ponto de presença online/ausente/ocupado/offline e versão empilhada para grupos. |
| Badge | [Badge](components/Badge/README.md) | Etiqueta curta (`.ttsc-badge`) para status de registro, contagem ou código, com variantes sólida, light, outline, ghost e ponto, em quatro tamanhos. |
| Kbd | [Kbd](components/Kbd/README.md) | Tecla ou combinação de teclas (`.ttsc-kbd`) exibida em dicas de atalho, menus e na busca global — `Ctrl K` no Windows/Linux, `⌘ K` no macOS. |
| Button | [Button](components/Button/README.md) | Botão de ação do chassi TotusTuus (`.ttsc-btn`), com seis variantes, três tamanhos, versão só-ícone e estado de carregamento. |
| Button Group | [ButtonGroup](components/ButtonGroup/README.md) | Botões colados em uma faixa única (`.ttsc-toggle-group`), usados como controle segmentado de escolha única/múltipla ou como toolbar de ações relacionadas. |
| Card | [Card](components/Card/README.md) | Superfície agrupadora do ttscui (`.ttsc-card`) com cabeçalho, toolbar, conteúdo, tabela e rodapé — a base de painéis de dashboard, KPIs e blocos de formulário. |
| Carousel | [Carousel](components/Carousel/README.md) | Faixa rolável horizontal do ttscui (`data-ttsc-carousel`) com anterior/próximo, paginação, contador “2 / 5”, autoplay, arraste e vários itens por vista (`perVie |
| Collapse | [Collapse](components/Collapse/README.md) | Gatilho que mostra e esconde **um** bloco com animação de altura (`data-ttsc-collapse="#alvo"`), sem precisar de lista como o Accordion. |
| DataTable | [DataTable](components/DataTable/README.md) | Tabela de registros do ttscui (`data-ttsc-datatable`) com busca, ordenação por coluna, paginação, tamanho de página e seleção de linhas — local (lê o `<tbody>`) |
| Dismiss | [Dismiss](components/Dismiss/README.md) | Botão que fecha um elemento com fade (`data-ttsc-dismiss="#alvo"`), removendo-o do DOM (`mode: remove`) ou apenas escondendo-o com `.hidden` (`mode: hide`) para |
| Drawer | [Drawer](components/Drawer/README.md) | Painel lateral do ttscui (`data-ttsc-drawer`) que desliza da borda com backdrop — o formulário padrão do CRUD (criar/editar registro) e a ficha de detalhe, na l |
| Dropdown | [Dropdown](components/Dropdown/README.md) | Menu flutuante do ttscui (`data-ttsc-dropdown`, posicionado com Popper) com itens `ttsc-dropdown-menu-link`, divisor, cabeçalho, item selecionado e submenu anin |
| Link | [Link](components/Link/README.md) | Texto navegável do chassi (`.ttsc-link`) em verde de texto `ttsc-accent-text`, com variantes de sublinhado (hover, fixo, tracejado), mono, inversa, tamanhos e d |
| Modal | [Modal](components/Modal/README.md) | Diálogo sobreposto do ttscui (`data-ttsc-modal`) com backdrop, cabeçalho, corpo e rodapé — usado para confirmações curtas, como a exclusão de uma matrícula. |
| Progress | [Progress](components/Progress/README.md) | Barra de progresso do runtime (`.ttsc-progress` + `.ttsc-progress-indicator`) em seis cores, com extensões TTSC para estado indeterminado e anel circular em SVG |
| Rating | [Rating](components/Rating/README.md) | Avaliação por estrelas (ou corações) do ttscui (`data-ttsc-rating`): interativa com radios nativos ou somente leitura, com `max`, `value`, `name` e evento `ttsc |
| Reparent | [Reparent](components/Reparent/README.md) | Move um bloco de marcação para outro container (`prepend` ou `append`) via `data-ttsc-reparent`, reavaliando no redimensionamento — usado para levar filtros, aç |
| Advanced Select | [AdvancedSelect](components/AdvancedSelect/README.md) | Select aprimorado do ttscui (`<select data-ttsc-select>`): busca, múltipla escolha com tags, combobox digitável e carregamento remoto paginado, mantendo o `<sel |
| Scrollable | [Scrollable](components/Scrollable/README.md) | Área com rolagem interna do ttscui (`data-ttsc-scrollable`): altura fixa, máxima ou **automática** (viewport menos cabeçalhos e offset), recalculada no resize,  |
| Separator | [Separator](components/Separator/README.md) | Linha divisória de 1px do runtime (`.ttsc-separator`), horizontal ou vertical (`.ttsc-separator-vertical`), com extensão TTSC para separador com texto (`.ttsc-s |
| Skeleton | [Skeleton](components/Skeleton/README.md) | Placeholder animado (`.ttsc-skeleton`, animação `pulse`) que reserva o formato de cards, tabelas e listas enquanto os dados chegam por AJAX. |
| Table | [Table](components/Table/README.md) | Tabela estática do runtime (`.ttsc-table` dentro de `.ttsc-table-wrapper`) com realce de linha, bordas, e extensões TTSC para zebra, compacta, cabeçalho fixo, l |
| Theme Switch | [ThemeSwitch](components/ThemeSwitch/README.md) | Seletor de tema do ttscui (`data-ttsc-theme-switch-toggle` / `data-ttsc-theme-switch-set`) com modos `light`, `dark` e `system`, persistido em `localStorage` e, |
| Toggle | [Toggle](components/Toggle/README.md) | Alternador genérico do ttscui (`data-ttsc-toggle`): um gatilho liga/desliga uma classe ou um atributo num elemento alvo e marca a si mesmo com `activeClass`, di |
| Toast | [Toast](components/Toast/README.md) | Notificação curta e empilhável do ttscui (`TTSC.Toast.show({…})`), com variantes, aparência, ação/cancelar, barra de tempo, pausa no hover e seis posições. |
| Tooltip | [Tooltip](components/Tooltip/README.md) | Dica curta posicionada com Popper do ttscui (`data-ttsc-tooltip="#id"` + `.ttsc-tooltip`), acionada por hover, foco ou clique, com posição, atraso, offset e mod |

## Navegação

| Item | Página | Resumo |
|---|---|---|
| Navigation | [Navigation](components/Navigation/README.md) | Estrutura de navegação do chassi TotusTuus: topbar de 56px (`--ttsc-header-h`), rail de módulos de 60px (`--ttsc-rail-w`, `#primary-rail`) e sub-sidebar de 320p |
| Menu | [Menu](components/Menu/README.md) | Menu vertical do runtime (`.ttsc-menu.ttsc-menu-default`) com itens, ícones, títulos, badges, bullets, títulos de seção, separadores e submenus em accordion, ma |
| Breadcrumb | [Breadcrumb](components/Breadcrumb/README.md) | Trilha de navegação hierárquica do chassi (`.ttsc-breadcrumb`): unidade › módulo › registro, com separador decorativo em `ttsc-meta` e item atual marcado com `a |
| Pagination | [Pagination](components/Pagination/README.md) | Rodapé único de toda lista paginada do chassi (tabelas, grades de cards, colunas de kanban): faixa “Mostrando 1–10 de 52”, seletor “Por página” e botões de pági |
| Scrollspy | [Scrollspy](components/Scrollspy/README.md) | Índice lateral que destaca a seção visível de uma página longa ou de um painel rolável e rola suavemente até ela ao clicar (`data-ttsc-scrollspy`, ttscui). |
| Scrollto | [Scrollto](components/Scrollto/README.md) | Gatilho que rola a janela ou um painel até um elemento-alvo (`data-ttsc-scrollto`, ttscui), com rolagem suave e deslocamento para compensar cabeçalhos fixos. |
| Stepper | [Stepper](components/Stepper/README.md) | Assistente em etapas (`data-ttsc-stepper`, ttscui) que mostra um passo por vez, marca os passos concluídos e permite validar antes de avançar — ex.: wizard de m |
| Sticky | [Sticky](components/Sticky/README.md) | Fixa um elemento (toolbar de ações em lote, resumo de totais, cabeçalho de formulário) no topo depois de certa rolagem e o solta ao voltar ou ao alcançar um ele |
| Tabs | [Tabs](components/Tabs/README.md) | Abas que alternam painéis de conteúdo na mesma página sem recarregar (`data-ttsc-tabs` + `data-ttsc-tab-toggle`, ttscui), no estilo linha `.ttsc-tabs-line` do c |

## Formulários

| Item | Página | Resumo |
|---|---|---|
| Forms | [Forms](components/Forms/README.md) | Guia de formulários do chassi: grade de campos, rótulo, dica, erro com `aria-invalid`, obrigatório, seções e rodapé de ações, montados com as classes `.ttsc-for |
| Date Picker | [DatePicker](components/DatePicker/README.md) | Seletor de data padrão do chassi: `<input type="date" class="ttsc-input">` aprimorado automaticamente pelo **TTSCDatepicker** (implementação TTSC, `assets/js/tt |
| Color Picker | [ColorPicker](components/ColorPicker/README.md) | Campo de cor do chassi para dados que guardam uma cor hexadecimal (ex.: `events.color varchar(7)` da agenda): `<input type="color">` estilizado + campo hex + pa |
| Drag and Drop | [DragAndDrop](components/DragAndDrop/README.md) | Arrastar e soltar nativo do HTML5 no chassi — reordenar itens de uma lista (ex.: fila de espera de vagas) e soltar arquivos numa área de envio — como implementa |
| Checkbox | [Checkbox](components/Checkbox/README.md) | Caixa de seleção do chassi (`.ttsc-checkbox`, runtime ttscui) em três tamanhos, com estados marcado, indeterminado, desabilitado e inválido — usada em listas co |
| File Input | [FileInput](components/FileInput/README.md) | Campo de arquivo do chassi: `input[type=file].ttsc-input` com o botão “Escolher arquivo” estilizado pelo runtime (`::file-selector-button`), lista dos arquivos  |
| Image Input | [ImageInput](components/ImageInput/README.md) | Seletor de imagem com prévia circular (`data-ttsc-image-input`, ttscui) para avatar de usuário, foto do aluno e logotipo da unidade: troca, remove e restaura a  |
| Pin Input | [PinInput](components/PinInput/README.md) | Campo segmentado para códigos curtos (`[data-ttsc-pin-input]` do ttscui): uma célula por caractere, avanço automático, colar distribuído e valor consolidado num |
| Input | [Input](components/Input/README.md) | Campo de texto de linha única do chassi (`.ttsc-input`), com três tamanhos, versão com ícone interno, estados desabilitado, somente leitura e inválido. |
| Input Group | [InputGroup](components/InputGroup/README.md) | Agrupa um [Input](../Input/README.md) com complementos externos (`.ttsc-input-group` + `.ttsc-input-addon`) como R$, %, @ ou um botão anexado, fundindo bordas e |
| Radio | [Radio](components/Radio/README.md) | Botão de opção nativo estilizado (`input[type=radio].ttsc-radio`) para escolher **uma** opção entre poucas, em lista, linha ou cartões selecionáveis. |
| Repeater | [Repeater](components/Repeater/README.md) | Lista de blocos de formulário repetíveis (`[data-ttsc-repeater]` do ttscui): um botão clona um modelo para dentro de um wrapper, com limite máximo e botão de re |
| Select | [Select](components/Select/README.md) | Lista suspensa **nativa** estilizada (`<select class="ttsc-select">`), com seta própria nos dois temas, três tamanhos e estados desabilitado e inválido. |
| Switch | [Switch](components/Switch/README.md) | Interruptor liga/desliga (`input[type=checkbox].ttsc-switch`) para configurações binárias com efeito imediato ou salvas no formulário, em três tamanhos. |
| Slider | [Slider](components/Slider/README.md) | Controle deslizante de valor único sobre `<input type="range">` nativo, com preenchimento e saída de valor sincronizados pelo `[data-ttsc-range-slider]` do ttsc |
| Textarea | [Textarea](components/Textarea/README.md) | Campo de texto multilinha do chassi (`textarea.ttsc-textarea`), com tamanhos, contador de caracteres, controle de redimensionamento e estado inválido. |
| Toggle Password | [TogglePassword](components/TogglePassword/README.md) | Campo de senha com botão mostrar/ocultar (`[data-ttsc-toggle-password]` do ttscui), que alterna o `type` entre `password` e `text` e marca o container com `acti |
| Toggle Group | [ToggleGroup](components/ToggleGroup/README.md) | Controle segmentado (`.ttsc-toggle-group` com `.ttsc-btn` filhos) para escolher uma opção (radio) ou várias (checkbox) numa faixa compacta de botões colados. |
| 3rd-Party Plugin | [ThirdPartyPlugin](components/ThirdPartyPlugin/README.md) | Guia para integrar uma biblioteca de terceiros (flatpickr, Select2, FullCalendar, TinyMCE…) ao chassi TTSC: onde ficam os arquivos, ordem de carga, inicializaçã |

## Base

| Item | Página | Resumo |
|---|---|---|
| Utilities | [Utilities](components/Utilities/README.md) | Catálogo das classes utilitárias Tailwind v4 **realmente compiladas** no `bundle.css` (subconjunto do `tailwind-runtime.css` do app) e dos helpers `ds-*` de doc |
| Helpers | [Helpers](components/Helpers/README.md) | Funções e classes de apoio do chassi: helpers JS do ttscui (`src/helpers/*`: dom, data, event-handler, utils), API comum dos componentes (`getInstance`, `getOrC |
| Forms | [Forms](components/Forms/README.md) | Guia de formulários do chassi: grade de campos, rótulo, dica, erro com `aria-invalid`, obrigatório, seções e rodapé de ações, montados com as classes `.ttsc-for |
| Buttons | [Button](components/Button/README.md) | Botão de ação do chassi TotusTuus (`.ttsc-btn`), com seis variantes, três tamanhos, versão só-ícone e estado de carregamento. |
| Accordion | [Accordion](components/Accordion/README.md) | Lista de seções recolhíveis do ttscui (`data-ttsc-accordion`) em que cada item abre e fecha o próprio painel, com uma ou várias seções abertas ao mesmo tempo (` |
| Alerts | [Alert](components/Alert/README.md) | Faixa de aviso inline (`.ttsc-alert`) para mensagens persistentes da página — seis cores, três estilos (solid, light, outline), com ícone, título, descrição, aç |
| Badges | [Badge](components/Badge/README.md) | Etiqueta curta (`.ttsc-badge`) para status de registro, contagem ou código, com variantes sólida, light, outline, ghost e ponto, em quatro tamanhos. |
| Breadcrumb | [Breadcrumb](components/Breadcrumb/README.md) | Trilha de navegação hierárquica do chassi (`.ttsc-breadcrumb`): unidade › módulo › registro, com separador decorativo em `ttsc-meta` e item atual marcado com `a |
| Bullets | [Bullets](components/Bullets/README.md) | Marcadores decorativos (`.ttsc-bullet`) — ponto, linha e barra vertical — para listas, legendas de status e agendas, com cores de status por token. |
| Cards | [Card](components/Card/README.md) | Superfície agrupadora do ttscui (`.ttsc-card`) com cabeçalho, toolbar, conteúdo, tabela e rodapé — a base de painéis de dashboard, KPIs e blocos de formulário. |
| Carousel | [Carousel](components/Carousel/README.md) | Faixa rolável horizontal do ttscui (`data-ttsc-carousel`) com anterior/próximo, paginação, contador “2 / 5”, autoplay, arraste e vários itens por vista (`perVie |
| Indicator | [Indicator](components/Indicator/README.md) | Indicador de carregamento (`data-indicator="on|off"`) que troca o rótulo de um botão por texto + spinner, mais spinners avulsos e barra de progresso indetermina |
| Modal | [Modal](components/Modal/README.md) | Diálogo sobreposto do ttscui (`data-ttsc-modal`) com backdrop, cabeçalho, corpo e rodapé — usado para confirmações curtas, como a exclusão de uma matrícula. |
| Overlay | [Overlay](components/Overlay/README.md) | Camada sobre um card ou imagem (`.ttsc-overlay`) que revela ações no hover/foco, e camada de carregamento (`.ttsc-overlay-loading`) que bloqueia um bloco enquan |
| Pagination | [Pagination](components/Pagination/README.md) | Rodapé único de toda lista paginada do chassi (tabelas, grades de cards, colunas de kanban): faixa “Mostrando 1–10 de 52”, seletor “Por página” e botões de pági |
| Popovers | [Popover](components/Popover/README.md) | Balão flutuante com conteúdo rico (`.ttsc-popover` com header, conteúdo e rodapé) aberto por clique, hover ou foco através do componente tooltip do ttscui (`dat |
| Hover | [Hover](components/Hover/README.md) | Efeitos de hover padronizados (`.ttsc-hover-*`) — elevar sombra, borda de destaque, cor do ícone, fundo e mostrar ações — que também respondem a foco de teclado |
| Pulse | [Pulse](components/Pulse/README.md) | Ponto com anel pulsante (`.ttsc-pulse`) que sinaliza algo **ao vivo** ou em andamento — aula acontecendo agora, serviço monitorado, chamada ativa — padronizando |
| Rating | [Rating](components/Rating/README.md) | Avaliação por estrelas (ou corações) do ttscui (`data-ttsc-rating`): interativa com radios nativos ou somente leitura, com `max`, `value`, `name` e evento `ttsc |
| Ribbon | [Ribbon](components/Ribbon/README.md) | Fita/etiqueta de canto (`.ttsc-ribbon`) presa à borda de um card para destacar uma condição do item inteiro — “Novo”, “Vagas esgotadas”, “Últimas vagas”, “Bolsa |
| Rotate | [Rotate](components/Rotate/README.md) | Rotação animada de ícones (`.ttsc-rotate` + `ttsc-rotate-90/180/270/n90`) quando o gatilho fica ativo — chevron de collapse/accordion, seta de ordenação — e uti |
| Separator | [Separator](components/Separator/README.md) | Linha divisória de 1px do runtime (`.ttsc-separator`), horizontal ou vertical (`.ttsc-separator-vertical`), com extensão TTSC para separador com texto (`.ttsc-s |
| Symbol | [Symbol](components/Symbol/README.md) | Marca visual de uma entidade (`.ttsc-symbol`) — quadrado ou círculo com ícone ou iniciais, em cinco tamanhos e cores por token — e grupo empilhado com “+N”. |
| Datatable | [DataTable](components/DataTable/README.md) | Tabela de registros do ttscui (`data-ttsc-datatable`) com busca, ordenação por coluna, paginação, tamanho de página e seleção de linhas — local (lê o `<tbody>`) |
| Tables | [Table](components/Table/README.md) | Tabela estática do runtime (`.ttsc-table` dentro de `.ttsc-table-wrapper`) com realce de linha, bordas, e extensões TTSC para zebra, compacta, cabeçalho fixo, l |
| Tabs | [Tabs](components/Tabs/README.md) | Abas que alternam painéis de conteúdo na mesma página sem recarregar (`data-ttsc-tabs` + `data-ttsc-tab-toggle`, ttscui), no estilo linha `.ttsc-tabs-line` do c |
| Toasts | [Toast](components/Toast/README.md) | Notificação curta e empilhável do ttscui (`TTSC.Toast.show({…})`), com variantes, aparência, ação/cancelar, barra de tempo, pausa no hover e seis posições. |
| Tooltips | [Tooltip](components/Tooltip/README.md) | Dica curta posicionada com Popper do ttscui (`data-ttsc-tooltip="#id"` + `.ttsc-tooltip`), acionada por hover, foco ou clique, com posição, atraso, offset e mod |
| Underline | [Underline](components/Underline/README.md) | Sublinhado decorativo para títulos (`.ttsc-underline`: barra curta ou cheia, marca-texto suave) e links com sublinhado animado (`.ttsc-underline-link`), com cor |

## Formulários · Plugins

| Item | Página | Resumo |
|---|---|---|
| Autosize | [Autosize](components/Autosize/README.md) | Plugin **autosize 6.0.1** aplicado a `textarea.ttsc-textarea[data-ttsc-autosize]`: a altura acompanha o conteúdo enquanto o usuário digita, com teto opcional po |
| Clipboard | [Clipboard](components/Clipboard/README.md) | Copiar para a área de transferência com um clique — código de matrícula, link de convite, chave PIX — usando o **Clipboard do ttscui** (`data-ttsc-clipboard`, r |
| Tempus Dominus Datepicker | [TempusDominus](components/TempusDominus/README.md) | Seletor de data e hora **Tempus Dominus 6.9.4** (com **Popper 2.11.8**), localizado em pt-BR, com ícones Font Awesome Light e tema ligado aos tokens TTSC — para |
| Flatpickr | [Flatpickr](components/Flatpickr/README.md) | Seletor de data **flatpickr 4.6.13** com **l10n pt** — data única, intervalo e hora (24 h) — e tema TTSC por tokens válido nos dois temas; é o seletor de data p |
| Date Range Picker | [DateRangePicker](components/DateRangePicker/README.md) | Seletor de período **daterangepicker 3.1.0** (jQuery 3.7.1 + moment 2.30.1) com presets em pt-BR (Hoje, Últimos 7 dias, Este mês…) e dois calendários, usado com |
| Dialer | [Dialer](components/Dialer/README.md) | Campo numérico com botões − / + (implementação TTSC, JS puro), com mínimo, máximo, passo, casas decimais e prefixo como `R$ `, formatado em pt-BR. |
| DropzoneJS | [Dropzone](components/Dropzone/README.md) | Área de arrastar e soltar arquivos (Dropzone 5.9.3 do repo) com fila, barra de progresso, validação de tipo/tamanho e mensagens pt-BR, em lista tematizada por t |
| FormValidation | [FormValidation](components/FormValidation/README.md) | Validação de formulários no cliente com FormValidation 2.4.0 (do repo): regras por campo, verificação assíncrona de unicidade e erros acessíveis com `aria-inval |
| Form Repeater | [Repeater](components/Repeater/README.md) | Lista de blocos de formulário repetíveis (`[data-ttsc-repeater]` do ttscui): um botão clona um modelo para dentro de um wrapper, com limite máximo e botão de re |
| Image Input | [ImageInput](components/ImageInput/README.md) | Seletor de imagem com prévia circular (`data-ttsc-image-input`, ttscui) para avatar de usuário, foto do aluno e logotipo da unidade: troca, remove e restaura a  |
| Inputmask | [Inputmask](components/Inputmask/README.md) | Máscaras de digitação com Inputmask 5.0.9 para os formatos brasileiros (CPF, CNPJ, telefone, CEP, moeda R$ e data), enviando ao servidor só os dígitos. |
| Multiselectsplitter | [MultiSelectSplitter](components/MultiSelectSplitter/README.md) | Implementação TTSC (JS puro) que transforma um `<select multiple>` com `<optgroup>` em duas colunas — grupo à esquerda, itens com checkbox à direita — mantendo  |
| noUiSlider | [NoUiSlider](components/NoUiSlider/README.md) | Controle deslizante de valor único ou faixa com noUiSlider 15.8.1, com tooltips, marcas (pips) e formatação pt-BR (R$, anos, %), tematizado por tokens. |
| Password Meter | [PasswordMeter](components/PasswordMeter/README.md) | Medidor de força de senha (implementação TTSC, JS puro): 4 barras, rótulo de força e checklist dos critérios da política do sistema — comprimento, maiúscula, mi |
| reCAPTCHA | [Recaptcha](components/Recaptcha/README.md) | Integração do Google reCAPTCHA (v2 checkbox e v3 invisível) no login e em formulários públicos, exibido só após tentativas suspeitas e sempre verificado no serv |
| Select2 | [Select2](components/Select2/README.md) | Select com busca, seleção múltipla, criação de tags e carregamento remoto (Select2 4.1.0-rc.0 + jQuery 3.7.1), com textos pt-BR e tema por tokens nos dois temas |
| Tagify | [Tagify](components/Tagify/README.md) | Campo de tags com Tagify 4.17.9: tags livres ou restritas a uma whitelist (etiquetas reais de `crm_tags`, com cor), dropdown de sugestões e tags inválidas sinal |

## Editores

| Item | Página | Resumo |
|---|---|---|
| CKEditor | [CKEditor](components/CKEditor/README.md) | Editor de texto formatado CKEditor 5 (build classic 41.4.2) com toolbar em pt-BR, cores ligadas aos tokens por variáveis `--ck-color-*` e HTML sanitizado no ser |
| Quill | [Quill](components/Quill/README.md) | Editor de texto leve Quill 2.0.3 com o tema snow ajustado aos tokens, toolbar declarada em HTML (com rótulos pt-BR) e saída em HTML semântico para comunicados e |
| TinyMCE | [TinyMCE](components/TinyMCE/README.md) | Editor de documentos TinyMCE 8.3.2 (licença GPL) com skin `oxide`/`oxide-dark` e `content_css` `default`/`dark` escolhidos pelo `data-theme`, plugins `lists lin |

## Gráficos

| Item | Página | Resumo |
|---|---|---|
| AmCharts | [AmCharts](components/AmCharts/README.md) | Gráficos amCharts 5.17.2 (colunas e rosca) com cores da escala `ttsc-primary`, rótulos em `ttsc-text-muted`, grade em `ttsc-border` e tooltip invertido, lidos d |
| ApexCharts | [ApexCharts](components/ApexCharts/README.md) | Gráficos ApexCharts 8.5.0 — área (frequência %), barras, donut e sparkline de KPI — com `theme.mode` conforme o `data-theme`, cores resolvidas dos tokens e loca |
| ApexCharts Advanced | [ApexChartsAdvanced](components/ApexChartsAdvanced/README.md) | Galeria avançada do ApexCharts 8.5.0 — candlestick, radar, treemap, waterfall (ponte de caixa), gauge radial, barras empilhadas/agrupadas e linha com faixa de previsão — com tokens, tema e tabela de dados textual. |
| Sankey Flow | [SankeyFlow](components/SankeyFlow/README.md) | Fluxo Sankey em SVG puro, sem dependências — origem, qualificação, proposta e desfecho com curvas proporcionais, foco por teclado, tooltip e lista vertical no mobile. |
| Geo Map | [GeoMap](components/GeoMap/README.md) | Mapa de operações do Brasil em SVG inline — estados coloridos por volume ou SLA, hubs com status, filtros por região, ranking e tooltip; alternativa textual pelo ranking. |
| Bullet Chart | [BulletChart](components/BulletChart/README.md) | Bullet chart — barra de realizado, marcador de meta e faixas qualitativas em um só traço; horizontal, vertical, board compacto e mini para rodapé de KPI. |
| Chart Kit | [ChartKit](components/ChartKit/README.md) | Catálogo completo de gráficos de gestão — 41 modelos em 8 seções numeradas (do básico ao avançado: boxplot, pareto, pirâmide, bump, slope, streamgraph, sunburst, waffle, marimekko, venn, calendar heatmap, OHLC com volume), com índice clicável e mapa de decisão; tudo em tokens, com tooltip personalizado e acessibilidade. |

## Componentes do painel

Blocos analíticos e operacionais das páginas de painel, documentados como os demais componentes (HTML, CSS, JS e SQL).

| Item | Página | Resumo |
|---|---|---|
| Hero Banner | [HeroBanner](components/HeroBanner/README.md) | Hero com status, índice em anel e linha de KPIs — destaque da visão geral. |
| Funnel Bars | [FunnelBars](components/FunnelBars/README.md) | Funil de etapas com barras decrescentes, valor de cada etapa e porcentagem em relação ao topo. |
| Heatmap Matrix | [HeatmapMatrix](components/HeatmapMatrix/README.md) | Matriz de linhas × colunas em que a intensidade da cor representa um valor, com legenda e níveis. |
| Quadrant Matrix | [QuadrantMatrix](components/QuadrantMatrix/README.md) | Matriz 2×2 que classifica itens em quatro quadrantes conforme dois indicadores. |
| Ranked Bars | [RankedBars](components/RankedBars/README.md) | Ranking com posição, valor absoluto, percentual e barra por estado. |
| Unit Grid | [UnitGrid](components/UnitGrid/README.md) | Grade de unidades (salas, mesas, leitos, docas) com estado por cor e texto. |
| Scenario Cards | [ScenarioCards](components/ScenarioCards/README.md) | Três cenários (pessimista, base, otimista) com premissas e seleção. |
| Approval Queue | [ApprovalQueue](components/ApprovalQueue/README.md) | Aprovações com solicitante, valor e decisão de aprovar ou recusar. |
| Checklist Grid | [ChecklistGrid](components/ChecklistGrid/README.md) | Checklist em grade com progresso e estado por item. |
| Queue List | [QueueList](components/QueueList/README.md) | Fila de atendimento com número, prioridade, espera e ação. |
| Risk List | [RiskList](components/RiskList/README.md) | Lista de risco com motivo, medidor por faixa e ação de abrir a ficha. |
| Executive Strip | [ExecutiveStrip](components/ExecutiveStrip/README.md) | Faixa executiva do topo do dashboard — ticker ao vivo, score composto em anel com frentes, tiles de KPI com delta, progresso de meta, limites de orçamento e watchlist de indicadores. |
| Gantt | [Gantt](components/Gantt/README.md) | Cronograma de projetos com barras por tarefa, progresso, marcos, dependências, caminho crítico e visão semanal/mensal. |
| Org Chart | [OrgChart](components/OrgChart/README.md) | Organograma com hierarquia, conectores, recolher/expandir, busca e ficha rápida da pessoa. |
| Chat Panel | [ChatPanel](components/ChatPanel/README.md) | Caixa de entrada embutida com conversas, thread, painel de contexto e composer; digitação, resposta do assistente, teclado e ARIA. |
| Insight Panel | [InsightPanel](components/InsightPanel/README.md) | Insights de IA com resumo executivo, recomendações priorizadas por tipo, confiança, fontes, aplicar/descartar e filtros. |
| Order Builder | [OrderBuilder](components/OrderBuilder/README.md) | Pedido de venda com catálogo, busca, carrinho, desconto, forma de pagamento e total; estados vazio e sucesso. |

## Geral

| Item | Página | Resumo |
|---|---|---|
| DataTables | [DataTablesNet](components/DataTablesNet/README.md) | Tabela de dados DataTables 2.3.7 (jQuery) com processamento server-side, idioma pt-BR e tema ligado aos tokens TTSC, para listagens grandes que o servidor pagin |
| Menu | [Menu](components/Menu/README.md) | Menu vertical do runtime (`.ttsc-menu.ttsc-menu-default`) com itens, ícones, títulos, badges, bullets, títulos de seção, separadores e submenus em accordion, ma |
| BlockUI | [BlockUI](components/BlockUI/README.md) | Bloqueio visual de um card, seção ou da página inteira durante uma operação assíncrona — implementação TTSC em JS puro com overlay, spinner e mensagem (`TTSC.Bl |
| Cookie | [Cookie](components/Cookie/README.md) | Leitura e gravação de cookies no navegador com js-cookie 3.0.5 (`Cookies.get/set/remove`) para preferências leves de interface — menu lateral recolhido, densida |
| Cookie Alert | [CookieAlert](components/CookieAlert/README.md) | Banner de consentimento de cookies da LGPD (Privacy First) com “Aceitar todos”, “Rejeitar não essenciais” e “Personalizar” por categoria — mesma lógica e chaves |
| CountUp | [CountUp](components/CountUp/README.md) | Animação de contagem numérica com countUp.js 2.8.0 (`countUp.CountUp`) para valores de KPI em pt-BR — separador de milhar `.`, decimal `,`, prefixo `R$ ` e sufi |
| Cropper | [Cropper](components/Cropper/README.md) | Recorte de imagem com Cropper.js 1.6.2 para a foto de perfil (avatar 1:1), com prévia redonda, zoom/rotação e exportação em canvas 256×256 enviada ao perfil do  |
| Draggable | [Draggable](components/Draggable/README.md) | Reordenação por arrastar com @shopify/draggable 1.0.0-beta.12 (`Draggable.Sortable`) — cards de painel, séries, etapas — com alça, espelho (mirror), alternativa |
| Drawer | [Drawer](components/Drawer/README.md) | Painel lateral do ttscui (`data-ttsc-drawer`) que desliza da borda com backdrop — o formulário padrão do CRUD (criar/editar registro) e a ficha de detalhe, na l |
| Fullcalendar | [FullCalendar](components/FullCalendar/README.md) | Calendário FullCalendar 6.1.20 (bundle global do repo) para a agenda acadêmica — visões mês/semana/lista, locale `pt-br` inline, eventos coloridos por tipo e te |
| Fullscreen Lightbox | [Lightbox](components/Lightbox/README.md) | Visualizador de imagens em tela cheia com fslightbox 3.4.1 — galerias por `data-fslightbox`, navegação por setas/teclado/gesto, tela cheia e reinicialização com |
| jKanban Board | [Kanban](components/Kanban/README.md) | Quadro kanban com jKanban 1.3.1 (dragula embutido) para solicitações com status — colunas vindas de `kanban_boards.columns_cfg`, cartões arrastáveis entre colun |
| jsTree | [JsTree](components/JsTree/README.md) | Árvore hierárquica com jsTree 3.3.17 (jQuery) para navegar e marcar **unidade › curso › turma** — plugins `checkbox`, `types`, `search` e `wholerow`, ícones Fon |
| Scroll | [Scrollable](components/Scrollable/README.md) | Área com rolagem interna do ttscui (`data-ttsc-scrollable`): altura fixa, máxima ou **automática** (viewport menos cabeçalhos e offset), recalculada no resize,  |
| Scrolltop | [Scrolltop](components/Scrolltop/README.md) | Botão flutuante “Voltar ao topo” que aparece depois de N px de rolagem e sobe a página (ou um contêiner) com rolagem suave — implementação TTSC em JS puro (`TTS |
| Quick Search | [QuickSearch](components/QuickSearch/README.md) | Busca rápida global (command palette) aberta com Ctrl/⌘ K — resultados agrupados por tipo (páginas, cursos, turmas, pessoas), navegação por ↑ ↓ Enter Esc e comp |
| Smooth Scroll | [SmoothScroll](components/SmoothScroll/README.md) | Rolagem suave para âncoras internas com smooth-scroll 16.1.3 (global `SmoothScroll`), descontando o header fixo de 56px (`data-scroll-header`), atualizando a UR |
| Stepper | [Stepper](components/Stepper/README.md) | Assistente em etapas (`data-ttsc-stepper`, ttscui) que mostra um passo por vez, marca os passos concluídos e permite validar antes de avançar — ex.: wizard de m |
| Sticky | [Sticky](components/Sticky/README.md) | Fixa um elemento (toolbar de ações em lote, resumo de totais, cabeçalho de formulário) no topo depois de certa rolagem e o solta ao voltar ou ao alcançar um ele |
| Swapper | [Swapper](components/Swapper/README.md) | Move um bloco de marcação entre contêineres conforme o breakpoint usando `matchMedia` — mapa declarativo “media query → destino” em `data-ttsc-swapper`; impleme |
| SweetAlert | [SweetAlert](components/SweetAlert/README.md) | Diálogos de confirmação, sucesso e entrada de dados com SweetAlert2 11.14.5 (`sweetalert2.all.min.js`, CSS embutido) — sem estilos próprios de botão (`buttonsSt |
| Lozad | [Lozad](components/Lozad/README.md) | Carregamento preguiçoso (lazy load) de imagens e fundos com lozad 1.16.0 — `data-src`, `data-srcset` e `data-background-image` só viram requisição quando o elem |
| Tiny Slider | [TinySlider](components/TinySlider/README.md) | Carrossel tiny-slider 2.9.4 (`tns()`) para avisos e destaques — 1/2/3 cartões por vista conforme a largura, controles e paginação com botões do chassi, autoplay |
| Toastr | [Toastr](components/Toastr/README.md) | Notificações toastr 2.1.4 (jQuery) — sucesso, informação, alerta e erro — com tema ligado aos tokens, ícones Font Awesome light e wrapper que escapa o texto; ma |
| Toggle | [Toggle](components/Toggle/README.md) | Alternador genérico do ttscui (`data-ttsc-toggle`): um gatilho liga/desliga uma classe ou um atributo num elemento alvo e marca a si mesmo com `activeClass`, di |
| Timeline | [Timeline](components/Timeline/README.md) | Linha do tempo vertical de eventos de um registro — ícone por ação, autor, mudança de status (antigo → novo) e observação — em CSS com tokens (implementação TTS |

## Modelos aprovados

Blocos de página do chassi, reconstruídos com o CSS e o JS reais do app e os renderizadores de `docs/model/app`.

| Página | Resumo |
|---|---|
| [AnalyticsPanels](components/AnalyticsPanels/README.md) | Aba Analytics do chassi: grade de painéis `TTSCAnalytics` (Chart.js 4) — barras, rosca ou linha — cada um com badges, legenda, total e um drawer de filtros próprio por gráfico. |
| [ContextBanner](components/ContextBanner/README.md) | Faixa verde de contexto abaixo do cabeçalho: ícone, título do recorte, descrição curta e uma pill de contagem cujo ponto fica âmbar quando há itens que exigem atenção. |
| [EmptyState](components/EmptyState/README.md) | Estado vazio do chassi (`.ttsc-empty-state`): caixa tracejada com ícone em tile verde, título, descrição e no máximo uma ação, nas variantes sem dados, sem resultado de busca e erro de carregamento. |
| [KanbanBoard](components/KanbanBoard/README.md) | Quadro Kanban v2.3 do chassi (`SoftCloud.KanbanBoard.mount`): colunas por etapa com contagem e soma, chips de etapa, busca e paginação por coluna, arrastar e soltar (mouse, toque e teclado), recolher/expandir e reordenar colunas com persistência. |
| [KpiView](components/KpiView/README.md) | Aba KPI do chassi: faixa de 4 cards de indicador (rótulo, valor mono, unidade, chips ou barra, rodapé) seguida do painel de distribuição e da lista de atenção. |
| [PageHeader](components/PageHeader/README.md) | Cabeçalho de toda página do chassi: tile de ícone 44×44, título `h1`, breadcrumb e o botão verde "Atualizar". |
| [PageModel](components/PageModel/README.md) | A página padrão do chassi montada inteira a partir de uma ficha: cabeçalho, banner, abas segmentadas com ações, KPI + distribuição, tabela, cards, Kanban, Analytics e os drawers View / Novo / Filtrar — o mesmo esqueleto de `developer/dashboard.php` e `chassis/domain_page.php`. |
| [RecordCards](components/RecordCards/README.md) | Aba "Cards / Grade" do chassi: os mesmos registros da tabela em cartões de 3 colunas, cada um com título, linha secundária, badge de etapa/status, caixa de linha + código, métricas da ficha, barra opcional e ações; busca e paginação próprias. |
| [RecordDrawers](components/RecordDrawers/README.md) | Os três drawers laterais (480 px) das páginas do chassi no padrão `view_item`: **View** (detalhes do registro com métricas e seções), **Novo** (formulário dos campos da ficha) e **Filtrar** (selects de status/enum), abertos por `window.openDrawer(id)` sobre o `#backdrop-overlay`. |
| [RecordsTable](components/RecordsTable/README.md) | Aba "Tabela de Dados" do chassi: cabeçalho da visão, busca com contador e "Limpar filtros", barra de lote, tabela com colunas fixas (seleção e ações), linha expansível e a paginação global `ttsc-pagination-standard`. |
| [SegmentedTabs](components/SegmentedTabs/README.md) | Barra de abas segmentadas do chassi (`#chassis-segmented-tabs.ttsc-segmented-tabs`) com contador por aba, à esquerda, e as ações da página — Filtrar, Exportar (menu de formatos) e Novo — à direita. |
| [SettingsPanel](components/SettingsPanel/README.md) | Corpo das páginas de configuração: abas segmentadas = grupos de parâmetros, cada grupo com seções em cartão (tile, título, origem dos dados) e campos em grade de 2 colunas — texto, número, select, toggle e textarea — com Descartar / Salvar alterações na barra de abas. |

## Arquétipos de página

| Página | Resumo |
|---|---|
| [PageAuth](components/PageAuth/README.md) | Arquétipo das telas de acesso fora do shell: cartão dividido com o painel da marca à esquerda e o formulário à direita (`sb-login-*`), estilizado por `assets/css/ttsc.auth.css`, com alerta de erro, mostrar/ocultar senha, verificação humana e atalhos para os portais. |
| [PageCalendar](components/PageCalendar/README.md) | Arquétipo de página de agenda: cabeçalho e banner do chassi seguidos de um FullCalendar 6.1.20 (mês, semana, lista) com os eventos da tabela `events` coloridos por tipo e um drawer de detalhe ao clicar. |
| [PageDashboard](components/PageDashboard/README.md) | Arquétipo de home de módulo ou de portal: cabeçalho, banner, KPI com distribuição e lista de atenção, e Analytics — sem "Novo", sem tabela como protagonista. |
| [PageHistory](components/PageHistory/README.md) | Arquétipo de histórico e auditoria somente leitura: abre na Tabela de Dados, tem KPI e Analytics, exporta CSV/PDF e não oferece "Novo", editar nem excluir. |
| [PagePipeline](components/PagePipeline/README.md) | Arquétipo de página para itens que andam por etapas reais: abre no Quadro Kanban, com KPI, Tabela, Cards e Analytics nas outras abas; mover um cartão grava o novo status. |
| [PageRecords](components/PageRecords/README.md) | Arquétipo padrão das páginas de módulo: lista de uma entidade com KPI, Tabela de Dados, Cards e Analytics, ações Filtrar · Exportar · Novo e os drawers de CRUD. |
| [PageReport](components/PageReport/README.md) | Arquétipo de relatório: abre direto em Analytics (gráficos primeiro), com KPI e Tabela de Dados como apoio, exportação e nenhuma ação de criação. |
| [PageSettings](components/PageSettings/README.md) | Arquétipo de configurações de módulo: cabeçalho, banner com o escopo das regras, abas segmentadas por grupo de parâmetros e o par Descartar / Salvar alterações no lugar de Filtrar / Exportar / Novo. |

## Widgets de análise

| Página | Resumo |
|---|---|
| [WidgetBalance](components/WidgetBalance/README.md) | Card “Total balance”: saldo de fechamento do último mês, variação contra o mês anterior e colunas mensais (Chart.js) com linha de média tracejada. |
| [WidgetCategoryLimit](components/WidgetCategoryLimit/README.md) | Card “Category limit”: medidor semicircular do quanto do limite do período já foi consumido, com estado (dentro/perto/acima do limite) e barras de progresso por categoria. |
| [WidgetConversionRate](components/WidgetConversionRate/README.md) | Card “Conversion rate”: rosca SVG com a distribuição de itens por etapa (concluído, em andamento, a fazer), legenda e três chamadas de percentual. |
| [WidgetEntityMap](components/WidgetEntityMap/README.md) | Card “Entity exposure”: treemap de botões proporcional ao volume (recebido + enviado) por tipo de contraparte ou por contraparte, com painel de detalhe do segmento selecionado e atalho para a tabela de conexões. |
| [WidgetEntityTable](components/WidgetEntityTable/README.md) | Card “Entity connections”: tabela de contrapartes com tipo (ícone de status), recebido e enviado, alternância Todas/Diretas, chips de filtros ativos e diálogo de filtros (datas, valor enviado, tipo, entidade). |
| [WidgetIncomeBreakdown](components/WidgetIncomeBreakdown/README.md) | Card “Income breakdown”: percentual da receita já gasto, saldo restante e uma barra segmentada por categoria com legenda de valores e percentuais. |
| [WidgetIncomeFlow](components/WidgetIncomeFlow/README.md) | Card “Income”: total recebido no período, variação contra o período anterior e um fluxo em três camadas roxas que cresce até o total, com marcos (semana 1, semana 2, total). |
| [WidgetIncomeStatistics](components/WidgetIncomeStatistics/README.md) | Card largo “Income statistics”: total recebido no período e linha histórica mensal (Chart.js, área preenchida) com média de referência. |
| [WidgetIncomeTrend](components/WidgetIncomeTrend/README.md) | Card “Income · Monthly income trend”: valor do último mês, variação contra o anterior e fluxo azul em quatro camadas ao longo de 8 ou 12 meses, com marcos no início, meio e fim. |
| [WidgetMarket](components/WidgetMarket/README.md) | Card largo de série de preço/saldo: valor atual com variação, três visões (linha, colunas de desvio da média, candles OHLC) e cinco intervalos (24 H, 1W, 1M, 1Y, ALL) em SVG com seleção de ponto. |
| [WidgetMonthlyConversions](components/WidgetMonthlyConversions/README.md) | Card “Monthly conversions”: total de conversões no período e barras mensais em SVG com eixo, rótulo de valor e destaque no mês de maior resultado. |
| [WidgetPortfolio](components/WidgetPortfolio/README.md) | Card de atividade de portfólio (“Total value”): patrimônio total, saudação ao usuário, mapa hexagonal de atividade diária (nível 0–4) com seleção de dia e lista das últimas transações com menu por linha e diálogo de detalhes. |
| [WidgetPurchases](components/WidgetPurchases/README.md) | Card “Total purchases”: total de compras da semana, barras por dia (seg–dom) em SVG com balão de valor no dia destacado e troca de moeda USD/BRL. |
| [WidgetSalesReport](components/WidgetSalesReport/README.md) | Família “Sales report”: receita por período (semana, mês, ano) e por região em sete variações — fluxo empilhado com tabela, multi-série, compacto, área, linha, snapshot com marcador e compacto “glow”. |
| [WidgetsLarge](components/WidgetsLarge/README.md) | Seção “Large size widgets”: 51 cards grandes — barras e chuvas diárias, heatmaps, quatro calendários, linhas e corridas, 15 radiais, perspectivas 3D e quatro gráficos de categoria (barras por divisão, rosca, pizza, radar). |
| [WidgetsMedium](components/WidgetsMedium/README.md) | Seção “Medium size widgets”: 19 cards médios com cabeçalho, valor (ou bloco duplo mensal/anual) e gráfico maior — colunas agrupadas, empilhadas 100%, cascata, heatmaps, círculos, treemaps e tiles de KPI. |
| [WidgetsSmallHorizontal](components/WidgetsSmallHorizontal/README.md) | Seção “Horizontal small widgets”: 24 cards compactos em linha — título, valor, variação e legenda à esquerda e um mini-gráfico SVG à direita (barras, cascata, heatmaps, medidor, sparkline…). |
| [WidgetsSmallVertical](components/WidgetsSmallVertical/README.md) | Seção “Vertical small widgets”: 21 cards compactos em coluna — título, valor, variação e mini-gráfico abaixo (cascata, barras, chuva, heatmaps, fluxo de receita), alguns com bloco de detalhes. |
| [WidgetSubscriptions](components/WidgetSubscriptions/README.md) | Card “Subscriptions”: custo/receita recorrente total e a participação de três provedores (ou planos) em anéis concêntricos SVG com legenda de valores. |
| [WidgetsXL](components/WidgetsXL/README.md) | Seção “XL size widgets”: 42 painéis extragrandes — heatmaps com KPIs e regiões, painéis de linhas, radiais e radares, tendência CCR/TTM e oito dashboards completos (receita recorrente, finanças pessoais, carteira, portfólio, plataformas, ocupação, medicamentos, qualidade do ar). |
| [WidgetTimeByCategory](components/WidgetTimeByCategory/README.md) | Card “Time by category”: média diária de horas por categoria em barras horizontais proporcionais (roxas), com a duração em “Xh YYm”. |

**Total:** 149 páginas únicas: 108 componentes cobrindo os 154 itens das listas pedidas, 12 modelos, 8 arquétipos e 21 páginas de widgets.
