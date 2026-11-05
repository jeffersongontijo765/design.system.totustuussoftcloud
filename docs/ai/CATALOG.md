# Catálogo de componentes

> Gerado por `scripts/ds-index.mjs` a partir de 196 READMEs. Não editar à mão.
> Consulte `catalog.json` para dados estruturados (variantes, estados, acessibilidade).

Arquétipos: `dashboard` · `records` · `detail` · `settings` · `calendar` · `auth` · `catalog`
Componentes com responsividade documentada: 37/196

## Modelos de página (42)

| Componente | Para que serve | Responsivo | README |
|---|---|---|---|
| **LayoutVisaoGeral** | Modelo de página para a visão geral acadêmica. Mostra como montar uma tela inteira com os componentes do painel: o cabeçalho com o índice de saúde, o  | sim | [abrir](components/LayoutVisaoGeral/README.md) |
| **PageAuth** | Arquétipo das telas de acesso fora do shell: cartão dividido com o painel da marca à esquerda e o formulário à direita (sb-login-), estilizado por ass | sim | [abrir](components/PageAuth/README.md) |
| **PageCalendar** | Arquétipo de página de agenda: cabeçalho e banner do chassi seguidos de um FullCalendar 6.1.20 (mês, semana, lista) com os eventos da tabela events co | — | [abrir](components/PageCalendar/README.md) |
| **PageDashboard** | Arquétipo de home de módulo ou de portal: cabeçalho, banner, KPI com distribuição e lista de atenção, e Analytics — sem "Novo", sem tabela como protag | — | [abrir](components/PageDashboard/README.md) |
| **PageHeader** | Cabeçalho de toda página do chassi: tile de ícone 44×44, título h1, breadcrumb e o botão verde "Atualizar". | — | [abrir](components/PageHeader/README.md) |
| **PageHistory** | Arquétipo de histórico e auditoria somente leitura: abre na Tabela de Dados, tem KPI e Analytics, exporta CSV/PDF e não oferece "Novo", editar nem exc | — | [abrir](components/PageHistory/README.md) |
| **PageModel** | A página padrão do chassi montada inteira a partir de uma ficha: cabeçalho, banner, abas segmentadas com ações, KPI + distribuição, tabela, cards, Kan | — | [abrir](components/PageModel/README.md) |
| **PagePipeline** | Arquétipo de página para itens que andam por etapas reais: abre no Quadro Kanban, com KPI, Tabela, Cards e Analytics nas outras abas; mover um cartão  | — | [abrir](components/PagePipeline/README.md) |
| **PageRecords** | Arquétipo padrão das páginas de módulo: lista de uma entidade com KPI, Tabela de Dados, Cards e Analytics, ações Filtrar · Exportar · Novo e os drawer | — | [abrir](components/PageRecords/README.md) |
| **PageReport** | Arquétipo de relatório: abre direto em Analytics (gráficos primeiro), com KPI e Tabela de Dados como apoio, exportação e nenhuma ação de criação. | — | [abrir](components/PageReport/README.md) |
| **PageSettings** | Arquétipo de configurações de módulo: cabeçalho, banner com o escopo das regras, abas segmentadas por grupo de parâmetros e o par Descartar / Salvar a | — | [abrir](components/PageSettings/README.md) |
| **StarterKitAppShell** | Ponto de partida para qualquer tela autenticada: o render real de resources/views/app/layouts/main.php (header global, rail, sub-sidebar, rodapé, açõe | sim | [abrir](components/StarterKitAppShell/README.md) |
| **StarterKitAppShellCollapsed** | O mesmo app/layouts/main.php do StarterKitAppShell com o sub-sidebar recolhido pelo mecanismo real de assets/js/ttsc.shell.js: só o rail de 60px, o bo | sim | [abrir](components/StarterKitAppShellCollapsed/README.md) |
| **StarterKitAuth** | Kit das telas sem sessão: o render real de resources/views/auth/layouts/main.php (cartão dividido com painel da marca e formulário) com auth/pages/log | sim | [abrir](components/StarterKitAuth/README.md) |
| **StarterKitEmail** | Kit de e-mail transacional: o layout real resources/views/emails/sac/layout.php (contêiner de 600px, cabeçalho em degradê azul, corpo, botão de ação e | — | [abrir](components/StarterKitEmail/README.md) |
| **StarterKitError** | Kit das páginas de erro reais: 404 e 500 renderizadas dentro do shell (errors/pages/404.php e 500.php sobre app/layouts/main.php), a página genérica i | sim | [abrir](components/StarterKitError/README.md) |
| **StarterKitInstall** | Kit da instalação inicial: o render real de resources/views/install/index.php — um formulário único em três blocos (banco de dados, empresa, administr | sim | [abrir](components/StarterKitInstall/README.md) |
| **StarterKitPortalStudent** | Kit dos portais de pessoas (aluno, responsável, professor, terceiros): o mesmo app/layouts/main.php do shell administrativo, trocando o rail e o sub-s | sim | [abrir](components/StarterKitPortalStudent/README.md) |
| **StarterKitPrint** | Kit de impressão e documento com três modelos: relatório institucional (A4 paisagem), declaração oficial com número e código de validação (A4 retrato) | — | [abrir](components/StarterKitPrint/README.md) |
| **StarterKitPublicSite** | Kit do site institucional: o render real de resources/views/web/layouts/main.php com a landing web/pages/home.php — barra de portais, navbar fixa, her | sim | [abrir](components/StarterKitPublicSite/README.md) |
| **StarterKitSupportPortal** | Kit do portal de suporte do cliente (SAC): o render real de resources/views/web/layouts/portal.php com o painel web/pages/supportportaldashboard.php — | sim | [abrir](components/StarterKitSupportPortal/README.md) |
| **WidgetBalance** | Card “Total balance”: saldo de fechamento do último mês, variação contra o mês anterior e colunas mensais (Chart.js) com linha de média tracejada. | — | [abrir](components/WidgetBalance/README.md) |
| **WidgetCategoryLimit** | Card “Category limit”: medidor semicircular do quanto do limite do período já foi consumido, com estado (dentro/perto/acima do limite) e barras de pro | — | [abrir](components/WidgetCategoryLimit/README.md) |
| **WidgetConversionRate** | Card “Conversion rate”: rosca SVG com a distribuição de itens por etapa (concluído, em andamento, a fazer), legenda e três chamadas de percentual. | — | [abrir](components/WidgetConversionRate/README.md) |
| **WidgetEntityMap** | Card “Entity exposure”: treemap de botões proporcional ao volume (recebido + enviado) por tipo de contraparte ou por contraparte, com painel de detalh | — | [abrir](components/WidgetEntityMap/README.md) |
| **WidgetEntityTable** | Card “Entity connections”: tabela de contrapartes com tipo (ícone de status), recebido e enviado, alternância Todas/Diretas, chips de filtros ativos e | — | [abrir](components/WidgetEntityTable/README.md) |
| **WidgetIncomeBreakdown** | Card “Income breakdown”: percentual da receita já gasto, saldo restante e uma barra segmentada por categoria com legenda de valores e percentuais. | — | [abrir](components/WidgetIncomeBreakdown/README.md) |
| **WidgetIncomeFlow** | Card “Income”: total recebido no período, variação contra o período anterior e um fluxo em três camadas roxas que cresce até o total, com marcos (sema | — | [abrir](components/WidgetIncomeFlow/README.md) |
| **WidgetIncomeStatistics** | Card largo “Income statistics”: total recebido no período e linha histórica mensal (Chart.js, área preenchida) com média de referência. | — | [abrir](components/WidgetIncomeStatistics/README.md) |
| **WidgetIncomeTrend** | Card “Income · Monthly income trend”: valor do último mês, variação contra o anterior e fluxo azul em quatro camadas ao longo de 8 ou 12 meses, com ma | — | [abrir](components/WidgetIncomeTrend/README.md) |
| **WidgetMarket** | Card largo de série de preço/saldo: valor atual com variação, três visões (linha, colunas de desvio da média, candles OHLC) e cinco intervalos (24 H,  | — | [abrir](components/WidgetMarket/README.md) |
| **WidgetMonthlyConversions** | Card “Monthly conversions”: total de conversões no período e barras mensais em SVG com eixo, rótulo de valor e destaque no mês de maior resultado. | — | [abrir](components/WidgetMonthlyConversions/README.md) |
| **WidgetPortfolio** | Card de atividade de portfólio (“Total value”): patrimônio total, saudação ao usuário, mapa hexagonal de atividade diária (nível 0–4) com seleção de d | — | [abrir](components/WidgetPortfolio/README.md) |
| **WidgetPurchases** | Card “Total purchases”: total de compras da semana, barras por dia (seg–dom) em SVG com balão de valor no dia destacado e troca de moeda USD/BRL. | — | [abrir](components/WidgetPurchases/README.md) |
| **WidgetSalesReport** | Família “Sales report”: receita por período (semana, mês, ano) e por região em sete variações — fluxo empilhado com tabela, multi-série, compacto, áre | — | [abrir](components/WidgetSalesReport/README.md) |
| **WidgetsLarge** | Seção “Large size widgets”: 51 cards grandes — barras e chuvas diárias, heatmaps, quatro calendários, linhas e corridas, 15 radiais, perspectivas 3D e | — | [abrir](components/WidgetsLarge/README.md) |
| **WidgetsMedium** | Seção “Medium size widgets”: 19 cards médios com cabeçalho, valor (ou bloco duplo mensal/anual) e gráfico maior — colunas agrupadas, empilhadas 100%,  | — | [abrir](components/WidgetsMedium/README.md) |
| **WidgetsSmallHorizontal** | Seção “Horizontal small widgets”: 24 cards compactos em linha — título, valor, variação e legenda à esquerda e um mini-gráfico SVG à direita (barras,  | — | [abrir](components/WidgetsSmallHorizontal/README.md) |
| **WidgetsSmallVertical** | Seção “Vertical small widgets”: 21 cards compactos em coluna — título, valor, variação e mini-gráfico abaixo (cascata, barras, chuva, heatmaps, fluxo  | — | [abrir](components/WidgetsSmallVertical/README.md) |
| **WidgetSubscriptions** | Card “Subscriptions”: custo/receita recorrente total e a participação de três provedores (ou planos) em anéis concêntricos SVG com legenda de valores. | — | [abrir](components/WidgetSubscriptions/README.md) |
| **WidgetsXL** | Seção “XL size widgets”: 42 painéis extragrandes — heatmaps com KPIs e regiões, painéis de linhas, radiais e radares, tendência CCR/TTM e oito dashboa | — | [abrir](components/WidgetsXL/README.md) |
| **WidgetTimeByCategory** | Card “Time by category”: média diária de horas por categoria em barras horizontais proporcionais (roxas), com a duração em “Xh YYm”. | — | [abrir](components/WidgetTimeByCategory/README.md) |

## Formulários (32)

| Componente | Para que serve | Responsivo | README |
|---|---|---|---|
| **AdvancedSelect** | Opções avançadas do TTSCSelect (assets/js/ttsc.select.js), o motor que o app aplica sozinho a todo <select: cabeçalho de categoria, ícone por opção, b | — | [abrir](components/AdvancedSelect/README.md) |
| **Checkbox** | Caixa de seleção do chassi (.ttsc-checkbox, runtime ttscui) em três tamanhos, com estados marcado, indeterminado, desabilitado e inválido — usada em l | — | [abrir](components/Checkbox/README.md) |
| **ColorPicker** | Campo de cor do chassi para dados que guardam uma cor hexadecimal (ex.: events.color varchar(7) da agenda): <input type="color" estilizado + campo hex | — | [abrir](components/ColorPicker/README.md) |
| **Cropper** | Recorte de imagem com Cropper.js 1.6.2 para a foto de perfil (avatar 1:1), com prévia redonda, zoom/rotação e exportação em canvas 256×256 enviada ao  | — | [abrir](components/Cropper/README.md) |
| **DatePicker** | Seletor de data padrão do chassi: <input type="date" class="ttsc-input" aprimorado automaticamente pelo TTSCDatepicker (implementação TTSC, assets/js/ | — | [abrir](components/DatePicker/README.md) |
| **DateRangePicker** | Seletor de período daterangepicker 3.1.0 (jQuery 3.7.1 + moment 2.30.1) com presets em pt-BR (Hoje, Últimos 7 dias, Este mês…) e dois calendários, usa | — | [abrir](components/DateRangePicker/README.md) |
| **Dropzone** | Área de arrastar e soltar arquivos (Dropzone 5.9.3 do repo) com fila, barra de progresso, validação de tipo/tamanho e mensagens pt-BR, em lista temati | — | [abrir](components/Dropzone/README.md) |
| **FileInput** | Campo de arquivo do chassi: input[type=file].ttsc-input com o botão “Escolher arquivo” estilizado pelo runtime (::file-selector-button), lista dos arq | — | [abrir](components/FileInput/README.md) |
| **FileManager** | Explorador de arquivos de uma pasta: caminho (breadcrumb), lista com ícone por tipo, tamanho, data, situação e ações por arquivo. Usado para documento | — | [abrir](components/FileManager/README.md) |
| **Forms** | Guia de formulários do chassi: grade de campos, rótulo, dica, erro com aria-invalid, obrigatório, seções e rodapé de ações, montados com as classes .t | sim | [abrir](components/Forms/README.md) |
| **FormValidation** | Validação de formulários no cliente com FormValidation 2.4.0 (do repo): regras por campo, verificação assíncrona de unicidade e erros acessíveis com a | — | [abrir](components/FormValidation/README.md) |
| **ImageInput** | Seletor de imagem com prévia circular (data-ttsc-image-input, ttscui) para avatar de usuário, foto do aluno e logotipo da unidade: troca, remove e res | — | [abrir](components/ImageInput/README.md) |
| **Input** | Campo de texto de linha única do chassi (.ttsc-input), com três tamanhos, versão com ícone interno, estados desabilitado, somente leitura e inválido. | — | [abrir](components/Input/README.md) |
| **InputGroup** | Agrupa um Input com complementos externos (.ttsc-input-group + .ttsc-input-addon) como R$, %, @ ou um botão anexado, fundindo bordas e raios. | — | [abrir](components/InputGroup/README.md) |
| **Inputmask** | Máscaras de digitação com Inputmask 5.0.9 para os formatos brasileiros (CPF, CNPJ, telefone, CEP, moeda R$ e data), enviando ao servidor só os dígitos | — | [abrir](components/Inputmask/README.md) |
| **MultiSelectSplitter** | Implementação TTSC (JS puro) que transforma um <select multiple com <optgroup em duas colunas — grupo à esquerda, itens com checkbox à direita — mante | — | [abrir](components/MultiSelectSplitter/README.md) |
| **PasswordMeter** | Medidor de força de senha (implementação TTSC, JS puro): 4 barras, rótulo de força e checklist dos critérios da política do sistema — comprimento, mai | — | [abrir](components/PasswordMeter/README.md) |
| **PinInput** | Campo segmentado para códigos curtos ([data-ttsc-pin-input] do ttscui): uma célula por caractere, avanço automático, colar distribuído e valor consoli | — | [abrir](components/PinInput/README.md) |
| **Radio** | Botão de opção nativo estilizado (input[type=radio].ttsc-radio) para escolher uma opção entre poucas, em lista, linha ou cartões selecionáveis. | — | [abrir](components/Radio/README.md) |
| **Rating** | Avaliação por estrelas (ou corações) do ttscui (data-ttsc-rating): interativa com radios nativos ou somente leitura, com max, value, name e evento tts | — | [abrir](components/Rating/README.md) |
| **Repeater** | Lista de blocos de formulário repetíveis ([data-ttsc-repeater] do ttscui): um botão clona um modelo para dentro de um wrapper, com limite máximo e bot | — | [abrir](components/Repeater/README.md) |
| **SegmentedTabs** | Barra de abas segmentadas do chassi (chassis-segmented-tabs.ttsc-segmented-tabs) com contador por aba, à esquerda, e as ações da página — Filtrar, Exp | sim | [abrir](components/SegmentedTabs/README.md) |
| **Select** | Lista suspensa de escolha única: um <select nativo que o TTSCSelect (assets/js/ttsc.select.js) troca automaticamente por gatilho + painel do app, ou q | — | [abrir](components/Select/README.md) |
| **Slider** | Controle deslizante de valor único sobre <input type="range" nativo, com preenchimento e saída de valor sincronizados pelo [data-ttsc-range-slider] do | — | [abrir](components/Slider/README.md) |
| **Stepper** | Assistente em etapas (data-ttsc-stepper, ttscui) que mostra um passo por vez, marca os passos concluídos e permite validar antes de avançar — ex.: wiz | — | [abrir](components/Stepper/README.md) |
| **Switch** | Interruptor liga/desliga (input[type=checkbox].ttsc-switch) para configurações binárias com efeito imediato ou salvas no formulário, em três tamanhos. | — | [abrir](components/Switch/README.md) |
| **Textarea** | Campo de texto multilinha do chassi (textarea.ttsc-textarea), com tamanhos, contador de caracteres, controle de redimensionamento e estado inválido. | — | [abrir](components/Textarea/README.md) |
| **ThemeSwitch** | Seletor de tema do ttscui (data-ttsc-theme-switch-toggle / data-ttsc-theme-switch-set) com modos light, dark e system, persistido em localStorage e, n | — | [abrir](components/ThemeSwitch/README.md) |
| **Tiny Slider** | Carrossel tiny-slider 2.9.4 (tns()) para avisos e destaques — 1/2/3 cartões por vista conforme a largura, controles e paginação com botões do chassi,  | sim | [abrir](components/TinySlider/README.md) |
| **Toggle** | Alternador genérico do ttscui (data-ttsc-toggle): um gatilho liga/desliga uma classe ou um atributo num elemento alvo e marca a si mesmo com activeCla | — | [abrir](components/Toggle/README.md) |
| **ToggleGroup** | Controle segmentado (.ttsc-toggle-group com .ttsc-btn filhos) para escolher uma opção (radio) ou várias (checkbox) numa faixa compacta de botões colad | — | [abrir](components/ToggleGroup/README.md) |
| **TogglePassword** | Campo de senha com botão mostrar/ocultar ([data-ttsc-toggle-password] do ttscui), que alterna o type entre password e text e marca o container com act | — | [abrir](components/TogglePassword/README.md) |

## Plugins de terceiros (32)

| Componente | Para que serve | Responsivo | README |
|---|---|---|---|
| **AmCharts** | Gráficos amCharts 5.17.2 (colunas e rosca) com cores da escala ttsc-primary, rótulos em ttsc-text-muted, grade em ttsc-border e tooltip invertido, lid | — | [abrir](components/AmCharts/README.md) |
| **ApexCharts** | Gráficos ApexCharts 8.5.0 — área (frequência %), barras, donut e sparkline de KPI — com theme.mode conforme o data-theme, cores resolvidas dos tokens  | — | [abrir](components/ApexCharts/README.md) |
| **ApexChartsAdvanced** | Galeria de sete gráficos ApexCharts 8.5.0 — candlestick, radar, treemap, waterfall, gauge radial, barras empilhadas/agrupadas e linha com faixa de pre | — | [abrir](components/ApexChartsAdvanced/README.md) |
| **Autosize** | Plugin autosize 6.0.1 aplicado a textarea.ttsc-textarea[data-ttsc-autosize]: a altura acompanha o conteúdo enquanto o usuário digita, com teto opciona | — | [abrir](components/Autosize/README.md) |
| **ChartKit** | Galeria completa de gráficos de gestão — 41 modelos em 8 seções numeradas, com índice clicável e mapa de decisão no topo: famílias nativas do ApexChar | — | [abrir](components/ChartKit/README.md) |
| **CKEditor** | Editor de texto formatado CKEditor 5 (build classic 41.4.2) com toolbar em pt-BR, cores ligadas aos tokens por variáveis --ck-color- e HTML sanitizado | — | [abrir](components/CKEditor/README.md) |
| **Clipboard** | Copiar para a área de transferência com um clique — código de matrícula, link de convite, chave PIX — usando o Clipboard do ttscui (data-ttsc-clipboar | — | [abrir](components/Clipboard/README.md) |
| **CountUp** | Animação de contagem numérica com countUp.js 2.8.0 (countUp.CountUp) para valores de KPI em pt-BR — separador de milhar ., decimal ,, prefixo R$ e suf | — | [abrir](components/CountUp/README.md) |
| **DataTables** | Tabela de dados DataTables 2.3.7 (jQuery) com processamento server-side, idioma pt-BR e tema ligado aos tokens TTSC, para listagens grandes que o serv | sim | [abrir](components/DataTablesNet/README.md) |
| **Flatpickr** | Seletor de data flatpickr 4.6.13 com l10n pt — data única, intervalo e hora (24 h) — e tema TTSC por tokens válido nos dois temas; é o seletor de data | — | [abrir](components/Flatpickr/README.md) |
| **FullCalendar** | Calendário FullCalendar 6.1.20 (bundle global do repo) para a agenda acadêmica — visões mês/semana/lista, locale pt-br inline, eventos coloridos por t | sim | [abrir](components/FullCalendar/README.md) |
| **Hover** | Efeitos de hover padronizados (.ttsc-hover-) — elevar sombra, borda de destaque, cor do ícone, fundo e mostrar ações — que também respondem a foco de  | — | [abrir](components/Hover/README.md) |
| **jsTree** | Árvore hierárquica com jsTree 3.3.17 (jQuery) para navegar e marcar unidade › curso › turma — plugins checkbox, types, search e wholerow, ícones Font  | — | [abrir](components/JsTree/README.md) |
| **Lozad** | Carregamento preguiçoso (lazy load) de imagens e fundos com lozad 1.16.0 — data-src, data-srcset e data-background-image só viram requisição quando o  | — | [abrir](components/Lozad/README.md) |
| **NoUiSlider** | Controle deslizante de valor único ou faixa com noUiSlider 15.8.1, com tooltips, marcas (pips) e formatação pt-BR (R$, anos, %), tematizado por tokens | — | [abrir](components/NoUiSlider/README.md) |
| **Quill** | Editor de texto leve Quill 2.0.3 com o tema snow ajustado aos tokens, toolbar declarada em HTML (com rótulos pt-BR) e saída em HTML semântico para com | — | [abrir](components/Quill/README.md) |
| **Recaptcha** | Integração do Google reCAPTCHA (v2 checkbox e v3 invisível) no login e em formulários públicos, exibido só após tentativas suspeitas e sempre verifica | — | [abrir](components/Recaptcha/README.md) |
| **Rotate** | Rotação animada de ícones (.ttsc-rotate + ttsc-rotate-90/180/270/n90) quando o gatilho fica ativo — chevron de collapse/accordion, seta de ordenação — | — | [abrir](components/Rotate/README.md) |
| **Scrollspy** | Índice lateral que destaca a seção visível de uma página longa ou de um painel rolável e rola suavemente até ela ao clicar (data-ttsc-scrollspy, ttscu | — | [abrir](components/Scrollspy/README.md) |
| **Scrollto** | Gatilho que rola a janela ou um painel até um elemento-alvo (data-ttsc-scrollto, ttscui), com rolagem suave e deslocamento para compensar cabeçalhos f | — | [abrir](components/Scrollto/README.md) |
| **Scrolltop** | Botão flutuante “Voltar ao topo” que aparece depois de N px de rolagem e sobe a página (ou um contêiner) com rolagem suave — implementação TTSC em JS  | — | [abrir](components/Scrolltop/README.md) |
| **Select2** | Select com busca, seleção múltipla, criação de tags e carregamento remoto (Select2 4.1.0-rc.0 + jQuery 3.7.1), com textos pt-BR e tema por tokens nos  | — | [abrir](components/Select2/README.md) |
| **SmoothScroll** | Rolagem suave para âncoras internas com smooth-scroll 16.1.3 (global SmoothScroll), descontando o header fixo de 56px (data-scroll-header), atualizand | — | [abrir](components/SmoothScroll/README.md) |
| **Sticky** | Fixa um elemento (toolbar de ações em lote, resumo de totais, cabeçalho de formulário) no topo depois de certa rolagem e o solta ao voltar ou ao alcan | sim | [abrir](components/Sticky/README.md) |
| **Swapper** | Move um bloco de marcação entre contêineres conforme o breakpoint usando matchMedia — mapa declarativo “media query → destino” em data-ttsc-swapper; i | sim | [abrir](components/Swapper/README.md) |
| **SweetAlert** | Diálogos de confirmação, sucesso e entrada de dados com SweetAlert2 11.14.5 (sweetalert2.all.min.js, CSS embutido) — sem estilos próprios de botão (bu | — | [abrir](components/SweetAlert/README.md) |
| **Tagify** | Campo de tags com Tagify 4.17.9: tags livres ou restritas a uma whitelist (etiquetas reais de crmtags, com cor), dropdown de sugestões e tags inválida | — | [abrir](components/Tagify/README.md) |
| **TempusDominus** | Seletor de data e hora Tempus Dominus 6.9.4 (com Popper 2.11.8), localizado em pt-BR, com ícones Font Awesome Light e tema ligado aos tokens TTSC — pa | — | [abrir](components/TempusDominus/README.md) |
| **ThirdPartyPlugin** | Guia para integrar uma biblioteca de terceiros (flatpickr, Select2, FullCalendar, TinyMCE…) ao chassi TTSC: onde ficam os arquivos, ordem de carga, in | — | [abrir](components/ThirdPartyPlugin/README.md) |
| **TinyMCE** | Editor de documentos TinyMCE 8.3.2 (licença GPL) com skin oxide/oxide-dark e contentcss default/dark escolhidos pelo data-theme, plugins lists link ta | — | [abrir](components/TinyMCE/README.md) |
| **Toastr** | Notificações toastr 2.1.4 (jQuery) — sucesso, informação, alerta e erro — com tema ligado aos tokens, ícones Font Awesome light e wrapper que escapa o | — | [abrir](components/Toastr/README.md) |
| **Underline** | Sublinhado decorativo para títulos (.ttsc-underline: barra curta ou cheia, marca-texto suave) e links com sublinhado animado (.ttsc-underline-link), c | — | [abrir](components/Underline/README.md) |

## Dados e conteúdo (28)

| Componente | Para que serve | Responsivo | README |
|---|---|---|---|
| **ApprovalQueue** | Lista de solicitações que dependem de uma decisão (aprovar ou recusar), com quem pediu, o valor ou a quantidade e os dois botões de decisão. Cada botã | — | [abrir](components/ApprovalQueue/README.md) |
| **ArticleCard** | Cartão de notícia ou artigo: imagem de capa, categoria, título (link), resumo curto e data com o tempo de leitura. Usado em listas de notícias, comuni | — | [abrir](components/ArticleCard/README.md) |
| **Card** | Superfície agrupadora do ttscui (.ttsc-card) com cabeçalho, toolbar, conteúdo, tabela e rodapé — a base de painéis de dashboard, KPIs e blocos de form | — | [abrir](components/Card/README.md) |
| **Carousel** | Faixa rolável horizontal do ttscui (data-ttsc-carousel) com anterior/próximo, paginação, contador “2 / 5”, autoplay, arraste e vários itens por vista  | — | [abrir](components/Carousel/README.md) |
| **ChatPanel** | Caixa de entrada de atendimento embutida no painel, com lista de conversas, histórico com anexos, contexto do contato e campo de resposta com atalhos  | sim | [abrir](components/ChatPanel/README.md) |
| **ChecklistGrid** | Grade de verificações de um processo (fechamento, início de semestre, auditoria) com estado por item, responsável e uma barra de conclusão no topo. | — | [abrir](components/ChecklistGrid/README.md) |
| **CommentThread** | Lista de comentários em uma conversa, com respostas aninhadas, autor, papel, horário e ação de responder. Diferencia mensagem para a família de nota i | — | [abrir](components/CommentThread/README.md) |
| **DataTable** | Visão “Tabela” do modelo aprovado de página (/developer/dashboard): cabeçalho da visão, barra de busca, barra de lote, tabela com seleção, linha expan | — | [abrir](components/DataTable/README.md) |
| **GalleryGrid** | Grade de fotos em mosaico, com tamanhos variados, legenda curta e um contador "+N" para as fotos que não cabem. Cada foto é um botão que abre a visual | — | [abrir](components/GalleryGrid/README.md) |
| **InsightPanel** | Painel de insights de IA com resumo executivo, recomendações priorizadas, confiança, fontes e decisão humana explícita. | sim | [abrir](components/InsightPanel/README.md) |
| **jKanban Board** | Quadro kanban com jKanban 1.3.1 (dragula embutido) para solicitações com status — colunas vindas de kanbanboards.columnscfg, cartões arrastáveis entre | sim | [abrir](components/Kanban/README.md) |
| **KanbanBoard** | Quadro Kanban v2.3 do chassi (SoftCloud.KanbanBoard.mount): colunas por etapa com contagem e soma, chips de etapa, busca e paginação por coluna, arras | — | [abrir](components/KanbanBoard/README.md) |
| **Fullscreen Lightbox** | Visualizador de imagens em tela cheia com fslightbox 3.4.1 — galerias por data-fslightbox, navegação por setas/teclado/gesto, tela cheia e reinicializ | sim | [abrir](components/Lightbox/README.md) |
| **OrderBuilder** | Monta um pedido de venda em uma tela: catálogo pesquisável, carrinho com quantidades, desconto, forma de pagamento e total, com estados de carrinho va | sim | [abrir](components/OrderBuilder/README.md) |
| **PricingCards** | Três (ou mais) cartões de plano lado a lado, com preço, o que está incluído e um destaque para a opção recomendada. Usado para planos de mensalidade,  | — | [abrir](components/PricingCards/README.md) |
| **ProfileHeader** | Cabeçalho de perfil de uma pessoa: foto (ou iniciais), nome, papel e vínculo, etiquetas de situação e três indicadores. Usado na ficha do aluno, do pr | — | [abrir](components/ProfileHeader/README.md) |
| **QueueList** | Lista numerada de itens que aguardam atendimento, com prioridade, tempo de espera e uma ação. Usada para filas de secretaria, financeiro e suporte. | — | [abrir](components/QueueList/README.md) |
| **RecordCards** | Aba "Cards / Grade" do chassi: os mesmos registros da tabela em cartões de 3 colunas, cada um com título, linha secundária, badge de etapa/status, cai | — | [abrir](components/RecordCards/README.md) |
| **RecordsTable** | Aba "Tabela de Dados" do chassi: cabeçalho da visão, busca com contador e "Limpar filtros", barra de lote, tabela com colunas fixas (seleção e ações), | — | [abrir](components/RecordsTable/README.md) |
| **ReviewCard** | Avaliação de uma pessoa ou serviço: nota com estrelas e número, a origem de quem avaliou, o texto e a contagem de quem achou útil. Usado para avaliar  | — | [abrir](components/ReviewCard/README.md) |
| **RiskList** | Lista de pessoas ou itens com um percentual de risco, o motivo em uma linha e uma barra que muda de cor pela faixa. Serve para alerta precoce: evasão, | — | [abrir](components/RiskList/README.md) |
| **ScenarioCards** | Três cartões lado a lado (pessimista, base, otimista) com o mesmo indicador calculado com premissas diferentes. Um deles fica selecionado e mostra as  | — | [abrir](components/ScenarioCards/README.md) |
| **ScoreGridCard** | Painel de índice: uma nota geral grande com classificação, ranking e resumo de um lado, e uma grade de métricas do outro. Cada métrica tem valor, barr | — | [abrir](components/ScoreGridCard/README.md) |
| **Table** | Tabela estática do runtime (.ttsc-table dentro de .ttsc-table-wrapper) com realce de linha, bordas, e extensões TTSC para zebra, compacta, cabeçalho f | sim | [abrir](components/Table/README.md) |
| **TeamMemberCard** | Cartão de uma pessoa da equipe (professor, coordenador, atendente), com foto ou iniciais, nome, função, indicador de disponibilidade e contato. Usado  | — | [abrir](components/TeamMemberCard/README.md) |
| **TestimonialCard** | Depoimento de uma pessoa (aluno, responsável, professor), com a citação, a nota em estrelas e a identificação de quem falou. Usado em sites institucio | — | [abrir](components/TestimonialCard/README.md) |
| **Timeline** | Linha do tempo vertical de eventos de um registro — ícone por ação, autor, mudança de status (antigo → novo) e observação — em CSS com tokens (impleme | — | [abrir](components/Timeline/README.md) |
| **UnitGrid** | Grade de unidades (salas, mesas, leitos, docas) em que cada célula mostra o nome, o estado e um detalhe, com cor por estado. Dá uma visão de ocupação  | — | [abrir](components/UnitGrid/README.md) |

## Feedback e sobreposição (22)

| Componente | Para que serve | Responsivo | README |
|---|---|---|---|
| **Alert** | Faixa de aviso inline (.ttsc-alert) para mensagens persistentes da página — seis cores, três estilos (solid, light, outline), com ícone, título, descr | — | [abrir](components/Alert/README.md) |
| **Badge** | Etiqueta curta (.ttsc-badge) para status de registro, contagem ou código, com variantes sólida, light, outline, ghost e ponto, em quatro tamanhos. | — | [abrir](components/Badge/README.md) |
| **BlockUI** | Bloqueio visual de um card, seção ou da página inteira durante uma operação assíncrona — implementação TTSC em JS puro com overlay, spinner e mensagem | — | [abrir](components/BlockUI/README.md) |
| **ContextBanner** | Faixa verde de contexto abaixo do cabeçalho: ícone, título do recorte, descrição curta e uma pill de contagem cujo ponto fica âmbar quando há itens qu | — | [abrir](components/ContextBanner/README.md) |
| **Cookie** | Leitura e gravação de cookies no navegador com js-cookie 3.0.5 (Cookies.get/set/remove) para preferências leves de interface — menu lateral recolhido, | — | [abrir](components/Cookie/README.md) |
| **Cookie Alert** | Banner de consentimento de cookies da LGPD (Privacy First) com “Aceitar todos”, “Rejeitar não essenciais” e “Personalizar” por categoria — mesma lógic | — | [abrir](components/CookieAlert/README.md) |
| **Dismiss** | Botão que fecha um elemento com fade (data-ttsc-dismiss="alvo"), removendo-o do DOM (mode: remove) ou apenas escondendo-o com .hidden (mode: hide) par | — | [abrir](components/Dismiss/README.md) |
| **Drawer** | Painel lateral do ttscui (data-ttsc-drawer) que desliza da borda com backdrop — o formulário padrão do CRUD (criar/editar registro) e a ficha de detal | sim | [abrir](components/Drawer/README.md) |
| **EmptyState** | Estado vazio do chassi (.ttsc-empty-state): caixa tracejada com ícone em tile verde, título, descrição e no máximo uma ação, nas variantes sem dados,  | — | [abrir](components/EmptyState/README.md) |
| **HeroBanner** | Faixa de destaque da página com título, status, um índice de saúde em anel e uma linha de quatro KPIs. Substitui o cabeçalho simples quando a visão ge | — | [abrir](components/HeroBanner/README.md) |
| **Indicator** | Indicador de carregamento (data-indicator="on/off") que troca o rótulo de um botão por texto + spinner, mais spinners avulsos e barra de progresso ind | — | [abrir](components/Indicator/README.md) |
| **MetaProgressCard** | Cartão de indicador com meta: valor principal, barra de progresso com um marcador na meta, a diferença em relação a ela e uma linha de contexto. Usado | — | [abrir](components/MetaProgressCard/README.md) |
| **Modal** | Diálogo sobreposto do ttscui (data-ttsc-modal) com backdrop, cabeçalho, corpo e rodapé — usado para confirmações curtas, como a exclusão de uma matríc | — | [abrir](components/Modal/README.md) |
| **Overlay** | Camada sobre um card ou imagem (.ttsc-overlay) que revela ações no hover/foco, e camada de carregamento (.ttsc-overlay-loading) que bloqueia um bloco  | — | [abrir](components/Overlay/README.md) |
| **Popover** | Balão flutuante com conteúdo rico (.ttsc-popover com header, conteúdo e rodapé) aberto por clique, hover ou foco através do componente tooltip do ttsc | — | [abrir](components/Popover/README.md) |
| **Progress** | Barra de progresso do runtime (.ttsc-progress + .ttsc-progress-indicator) em seis cores, com extensões TTSC para estado indeterminado e anel circular  | — | [abrir](components/Progress/README.md) |
| **Pulse** | Ponto com anel pulsante (.ttsc-pulse) que sinaliza algo ao vivo ou em andamento — aula acontecendo agora, serviço monitorado, chamada ativa — padroniz | — | [abrir](components/Pulse/README.md) |
| **RecordDrawers** | Os três drawers laterais (480 px) das páginas do chassi no padrão viewitem: View (detalhes do registro com métricas e seções), Novo (formulário dos ca | — | [abrir](components/RecordDrawers/README.md) |
| **Ribbon** | Fita/etiqueta de canto (.ttsc-ribbon) presa à borda de um card para destacar uma condição do item inteiro — “Novo”, “Vagas esgotadas”, “Últimas vagas” | — | [abrir](components/Ribbon/README.md) |
| **Skeleton** | Placeholder animado (.ttsc-skeleton, animação pulse) que reserva o formato de cards, tabelas e listas enquanto os dados chegam por AJAX. | — | [abrir](components/Skeleton/README.md) |
| **Toast** | Notificação curta e empilhável do ttscui (TTSC.Toast.show({…})), com variantes, aparência, ação/cancelar, barra de tempo, pausa no hover e seis posiçõ | — | [abrir](components/Toast/README.md) |
| **Tooltip** | Dica curta posicionada com Popper do ttscui (data-ttsc-tooltip="id" + .ttsc-tooltip), acionada por hover, foco ou clique, com posição, atraso, offset  | sim | [abrir](components/Tooltip/README.md) |

## Gráficos e análise (13)

| Componente | Para que serve | Responsivo | README |
|---|---|---|---|
| **AnalyticsPanels** | Aba Analytics do chassi: grade de painéis TTSCAnalytics (Chart.js 4) — barras, rosca ou linha — cada um com badges, legenda, total e um drawer de filt | — | [abrir](components/AnalyticsPanels/README.md) |
| **BulletChart** | Bullet chart (gráfico de projétil): uma barra de valor realizado, um marcador de meta e faixas qualitativas de fundo — a leitura de "realizado vs. met | — | [abrir](components/BulletChart/README.md) |
| **Bullets** | Marcadores decorativos (.ttsc-bullet) — ponto, linha e barra vertical — para listas, legendas de status e agendas, com cores de status por token. | — | [abrir](components/Bullets/README.md) |
| **FunnelBars** | Funil horizontal em barras decrescentes, com o valor de cada etapa e a porcentagem em relação ao topo. Mostra onde a coorte perde pessoas. | sim | [abrir](components/FunnelBars/README.md) |
| **GeoMap** | Mapa do Brasil por unidade federativa para leitura de operação: volume de entregas ou SLA, hubs que concentram a rede, rotas ativas, filtros por regiã | sim | [abrir](components/GeoMap/README.md) |
| **HeatmapMatrix** | Matriz de linhas × colunas em que a intensidade da cor representa um valor (presença, ocupação, carga). Permite ver padrões de uma vez: uma turma inte | — | [abrir](components/HeatmapMatrix/README.md) |
| **InvoiceSummary** | Resumo de uma fatura ou boleto: número, vencimento e situação, a lista de itens com valores, o subtotal, o desconto e o total a pagar, com as ações de | — | [abrir](components/InvoiceSummary/README.md) |
| **KpiGoalCard** | Indicador com meta e visualização de apoio: valor atual, variação, barra até a meta com o quanto falta e um espaço opcional para uma visualização pequ | — | [abrir](components/KpiGoalCard/README.md) |
| **KpiView** | Aba KPI do chassi: faixa de 4 cards de indicador (rótulo, valor mono, unidade, chips ou barra, rodapé) seguida do painel de distribuição e da lista de | — | [abrir](components/KpiView/README.md) |
| **OrgChart** | Organograma hierárquico com conectores, recolher e expandir, busca e ficha rápida da pessoa selecionada. | — | [abrir](components/OrgChart/README.md) |
| **QuadrantMatrix** | Matriz 2×2 que classifica itens em quatro quadrantes conforme dois indicadores. Cada quadrante tem nome, regra e a lista de itens que caem nele. | — | [abrir](components/QuadrantMatrix/README.md) |
| **RankedBars** | Lista ordenada em que cada item mostra posição, nome, valor e uma barra proporcional. Serve para comparar itens de uma mesma métrica e destacar os ext | — | [abrir](components/RankedBars/README.md) |
| **SankeyFlow** | Fluxo Sankey em SVG puro, em quatro colunas, com volumes conservados, links Bézier proporcionais, destaque por foco e uma lista vertical equivalente n | sim | [abrir](components/SankeyFlow/README.md) |

## Outros (11)

| Componente | Para que serve | Responsivo | README |
|---|---|---|---|
| **Accordion** | Lista de seções recolhíveis do ttscui (data-ttsc-accordion) em que cada item abre e fecha o próprio painel, com uma ou várias seções abertas ao mesmo  | — | [abrir](components/Accordion/README.md) |
| **Collapse** | Gatilho que mostra e esconde um bloco com animação de altura (data-ttsc-collapse="alvo"), sem precisar de lista como o Accordion. | — | [abrir](components/Collapse/README.md) |
| **Dialer** | Campo numérico com botões − / + (implementação TTSC, JS puro), com mínimo, máximo, passo, casas decimais e prefixo como R$ , formatado em pt-BR. | — | [abrir](components/Dialer/README.md) |
| **DragAndDrop** | Arrastar e soltar nativo do HTML5 no chassi — reordenar itens de uma lista (ex.: fila de espera de vagas) e soltar arquivos numa área de envio — como  | — | [abrir](components/DragAndDrop/README.md) |
| **Draggable** | Reordenação por arrastar com @shopify/draggable 1.0.0-beta.12 (Draggable.Sortable) — cards de painel, séries, etapas — com alça, espelho (mirror), alt | — | [abrir](components/Draggable/README.md) |
| **Dropdown** | Menu flutuante do ttscui (data-ttsc-dropdown, posicionado com Popper) com itens ttsc-dropdown-menu-link, divisor, cabeçalho, item selecionado e submen | — | [abrir](components/Dropdown/README.md) |
| **ExecutiveStrip** | Faixa executiva do topo do dashboard: ticker ao vivo, score composto em anel com frentes, tiles de KPI com delta, progresso de meta, limites de orçame | — | [abrir](components/ExecutiveStrip/README.md) |
| **Gantt** | Cronograma de projeto com uma linha por tarefa, barras proporcionais ao período, progresso, marcos, dependências e caminho crítico. | — | [abrir](components/Gantt/README.md) |
| **ProductTour** | Cartão de passo a passo que aponta um elemento da tela e explica o que ele faz. Tem indicador de progresso, botões Voltar e Próximo e a saída "Pular t | — | [abrir](components/ProductTour/README.md) |
| **Reparent** | Move um bloco de marcação para outro container (prepend ou append) via data-ttsc-reparent, reavaliando no redimensionamento — usado para levar filtros | sim | [abrir](components/Reparent/README.md) |
| **SettingsPanel** | Corpo das páginas de configuração: abas segmentadas = grupos de parâmetros, cada grupo com seções em cartão (tile, título, origem dos dados) e campos  | — | [abrir](components/SettingsPanel/README.md) |

## Fundação (9)

| Componente | Para que serve | Responsivo | README |
|---|---|---|---|
| **Avatar** | Foto ou iniciais de uma pessoa (.ttsc-avatar), com ponto de presença online/ausente/ocupado/offline e versão empilhada para grupos. | — | [abrir](components/Avatar/README.md) |
| **Button** | Botão de ação do chassi TotusTuus (.ttsc-btn), com seis variantes, três tamanhos, versão só-ícone e estado de carregamento. | sim | [abrir](components/Button/README.md) |
| **ButtonGroup** | Botões colados em uma faixa única (.ttsc-toggle-group), usados como controle segmentado de escolha única/múltipla ou como toolbar de ações relacionada | sim | [abrir](components/ButtonGroup/README.md) |
| **Helpers** | Funções e classes de apoio do chassi: helpers JS do ttscui (src/helpers/: dom, data, event-handler, utils), API comum dos componentes (getInstance, ge | sim | [abrir](components/Helpers/README.md) |
| **Kbd** | Tecla ou combinação de teclas (.ttsc-kbd) exibida em dicas de atalho, menus e na busca global — Ctrl K no Windows/Linux, ⌘ K no macOS. | sim | [abrir](components/Kbd/README.md) |
| **Link** | Texto navegável do chassi (.ttsc-link) em verde de texto ttsc-accent-text, com variantes de sublinhado (hover, fixo, tracejado), mono, inversa, tamanh | — | [abrir](components/Link/README.md) |
| **Separator** | Linha divisória de 1px do runtime (.ttsc-separator), horizontal ou vertical (.ttsc-separator-vertical), com extensão TTSC para separador com texto (.t | — | [abrir](components/Separator/README.md) |
| **Symbol** | Marca visual de uma entidade (.ttsc-symbol) — quadrado ou círculo com ícone ou iniciais, em cinco tamanhos e cores por token — e grupo empilhado com “ | — | [abrir](components/Symbol/README.md) |
| **Utilities** | Catálogo das classes utilitárias Tailwind v4 realmente compiladas no bundle.css (subconjunto do tailwind-runtime.css do app) e dos helpers ds- de docu | sim | [abrir](components/Utilities/README.md) |

## Navegação (7)

| Componente | Para que serve | Responsivo | README |
|---|---|---|---|
| **Breadcrumb** | Trilha de navegação hierárquica do chassi (.ttsc-breadcrumb): unidade › módulo › registro, com separador decorativo em ttsc-meta e item atual marcado  | — | [abrir](components/Breadcrumb/README.md) |
| **Menu** | Menu vertical do runtime (.ttsc-menu.ttsc-menu-default) com itens, ícones, títulos, badges, bullets, títulos de seção, separadores e submenus em accor | — | [abrir](components/Menu/README.md) |
| **Navigation** | Shell de navegação real do app (resources/views/app/layouts/main.php): topbar de 56px, rail de portais e módulos primary-rail (60px, expande para 288p | sim | [abrir](components/Navigation/README.md) |
| **Pagination** | Rodapé único de toda lista paginada do chassi (tabelas, grades de cards, colunas de kanban): faixa “Mostrando 1–10 de 52”, seletor “Por página” e botõ | sim | [abrir](components/Pagination/README.md) |
| **Quick Search** | Busca rápida global (command palette) aberta com Ctrl/⌘ K — resultados agrupados por tipo (páginas, cursos, turmas, pessoas), navegação por ↑ ↓ Enter  | — | [abrir](components/QuickSearch/README.md) |
| **Scrollable** | Área com rolagem interna do ttscui (data-ttsc-scrollable): altura fixa, máxima ou automática (viewport menos cabeçalhos e offset), recalculada no resi | sim | [abrir](components/Scrollable/README.md) |
| **Tabs** | Abas que alternam painéis de conteúdo na mesma página sem recarregar (data-ttsc-tabs + data-ttsc-tab-toggle, ttscui), no estilo linha .ttsc-tabs-line  | — | [abrir](components/Tabs/README.md) |
