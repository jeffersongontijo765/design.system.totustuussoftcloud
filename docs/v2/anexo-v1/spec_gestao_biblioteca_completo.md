# Spec Completo — Biblioteca UI Enterprise

- Language Standard: Global English
Documento de especificação funcional e estrutural para uma biblioteca de páginas, blocos e componentes reutilizáveis voltada a sistemas SaaS administrativos, operacionais e analíticos. O escopo cobre DataTables, widgets, charts, CRUD em drawers, Kanban, automações, controles e páginas de gerenciamento completas, com foco em consistência de design system, acessibilidade, segurança operacional e alta reutilização entre módulos.[cite:1]

## Objetivo

Esta biblioteca deve servir como base única para construção de backoffice, painéis operacionais, módulos administrativos, fluxos transacionais e interfaces analíticas, reduzindo divergência visual e técnica entre produtos.[cite:1]

A arquitetura da biblioteca deve priorizar composição por blocos, estados previsíveis, responsividade, acessibilidade, performance e capacidade de extensão por domínio, como financeiro, educacional, saúde, CRM, estoque, suporte e compliance.[cite:1]

## Princípios da biblioteca

- Design system centralizado com tokens de cor, espaçamento, tipografia, radius, sombra e estados interativos.[cite:1]
- Componentes stateless na camada visual e integração por adapters para dados, autenticação, permissão e telemetria.[cite:1]
- Todos os blocos devem prever estados de loading, vazio, erro, sucesso, bloqueado por permissão e somente leitura.[cite:1]
- Toda ação crítica deve suportar confirmação, auditoria e feedback transacional claro.[cite:1]
- Os componentes devem funcionar em tema claro e escuro, desktop e mobile, com foco inicial em desktop administrativo.[cite:1]

## Estrutura macro da biblioteca

A biblioteca deve ser organizada em sete camadas principais, permitindo adoção incremental por equipes diferentes.[cite:1]

### 1. Foundations

- Tokens de cor semântica.
- Tipografia.
- Grid e spacing.
- Iconografia.
- Elevação.
- Motion.
- Breakpoints.
- Acessibilidade.
- Internacionalização.
- Estados globais.[cite:1]

### 2. Átomos

- Button.
- IconButton.
- Input.
- Textarea.
- Select.
- MultiSelect.
- Checkbox.
- Radio.
- Switch.
- Tag.
- Badge.
- Avatar.
- Tooltip.
- Divider.
- Tabs.
- Breadcrumb.
- Pagination.
- EmptyState.
- Skeleton.
- Alert.[cite:1]

### 3. Moléculas

- Search bar.
- Filter bar.
- Date range picker.
- Field group.
- Inline validation block.
- KPI card.
- Stat block.
- Action group.
- Upload area.
- Row actions.
- Table toolbar.
- Quick filters.
- Step header.
- Audit snippet.[cite:1]

### 4. Organismos

- DataTable full.
- Form drawer.
- Detail drawer.
- Side panel.
- Modal de confirmação.
- Kanban board.
- Widget containers.
- Dashboard sections.
- Automation builder.
- Permission matrix.
- Activity timeline.
- Comment thread.
- Bulk action panel.[cite:1]

### 5. Templates

- Listagem com filtros.
- Dashboard analítico.
- CRUD master-detail.
- Gestão por Kanban.
- Tela de automações.
- Tela de configurações.
- Tela de permissões.
- Tela de auditoria.
- Tela de detalhes de entidade.[cite:1]

### 6. Pages

Cada página deve ser empacotada como blueprint completo, com áreas, componentes, estados, eventos, permissões, ações e contratos de integração.[cite:1]

### 7. Domain packs

Pacotes opcionais por domínio, como alunos, pacientes, contratos, tickets, usuários, unidades, convênios, pagamentos, estoque, documentos e consentimentos.[cite:1]

## Convenções globais

### Layout base

Toda página deve seguir a seguinte estrutura visual.[cite:1]

1. Header da página com título, subtítulo, breadcrumbs e ações primárias.
2. Barra contextual com filtros, busca, segmentadores, chips e ações secundárias.
3. Conteúdo principal em grid responsivo.
4. Painéis auxiliares opcionais, como resumo, auditoria ou atalhos.
5. Rodapé contextual com contagem, paginação, seleção ou status da operação.[cite:1]

### Estados obrigatórios por componente

Cada componente de alto nível deve suportar, no mínimo, os estados abaixo.[cite:1]

| Estado | Obrigatório | Comportamento |
|---|---|---|
| Loading | Sim | Skeleton ou spinner contextual sem quebrar layout. [cite:1] |
| Empty | Sim | Mensagem clara, CTA e orientação do próximo passo. [cite:1] |
| Error | Sim | Erro amigável, código opcional, ação de retry. [cite:1] |
| Success | Sim | Feedback visual e textual após operação. [cite:1] |
| Disabled | Sim | Bloqueio visual e semântico. [cite:1] |
| Read only | Sim | Visualização sem affordance de edição. [cite:1] |
| Permission denied | Sim | Mensagem de acesso restrito e trilha de solicitação. [cite:1] |

### Telemetria mínima

Todo bloco acionável deve permitir instrumentação de eventos como view, click, submit, error, retry, export, import, approve, reject, drag, drop, reorder e bulk_action.[cite:1]

### Segurança operacional

A biblioteca deve prever hooks para mascaramento de dados sensíveis, bloqueio por escopo, confirmação de ações destrutivas, trilha de auditoria e política de visibilidade por role, tenant, unidade e entidade.[cite:1]

## Módulo 1 — DataTable completo

O DataTable é um dos pilares da biblioteca e deve ser entregue em versão enterprise, cobrindo cenários simples e densos.[cite:1]

### Objetivos do DataTable

- Exibir grandes volumes de registros.
- Permitir busca, filtro, ordenação e paginação.
- Suportar seleção em massa e ações em lote.
- Expor colunas configuráveis por contexto e perfil.
- Ser reutilizável em qualquer entidade de negócio.[cite:1]

### Estrutura visual do DataTable

- Toolbar superior.
- Linha de filtros rápidos.
- Área de tabela.
- Cabeçalho com ordenação.
- Coluna de seleção opcional.
- Coluna de ações fixada à direita.
- Rodapé com paginação e resumo.[cite:1]

### Controles obrigatórios

- Campo de busca global.
- Filtros avançados.
- Ordenação por coluna.
- Redimensionamento de coluna.
- Reordenação de colunas.
- Toggle de visibilidade de colunas.
- Fixação de colunas críticas.
- Paginação server-side ou client-side.
- Seletor de densidade da tabela.
- Seletor de quantidade por página.
- Exportar CSV/XLSX/PDF quando permitido.
- Importar quando aplicável.
- Ações em massa.
- Reset de filtros.
- Saved views.[cite:1]

### Tipos de coluna suportados

| Tipo | Uso |
|---|---|
| Texto | Nome, título, descrição curta. [cite:1] |
| Identificador | Código, UUID parcial, protocolo. [cite:1] |
| Status | Badge colorido com legenda semântica. [cite:1] |
| Data/hora | Criação, atualização, vencimento. [cite:1] |
| Valor monetário | Faturamento, saldo, custo. [cite:1] |
| Percentual | Conversão, taxa, conclusão. [cite:1] |
| Usuário | Avatar, nome, cargo. [cite:1] |
| Relação | Unidade, turma, contrato, categoria. [cite:1] |
| Booleano | Ativo, verificado, bloqueado. [cite:1] |
| Progresso | Barra linear com label. [cite:1] |
| Tag list | Etiquetas múltiplas. [cite:1] |
| Ações | Ver, editar, duplicar, excluir, mais ações. [cite:1] |

### Funcionalidades avançadas

- Persistência de preferências de visualização por usuário.
- Seleção por página e seleção global por resultado filtrado.
- Inline row expansion para detalhes rápidos.
- Group by por campos categóricos.
- Colunas calculadas.
- Virtualização para datasets extensos.
- Modo comparação entre linhas.
- Indicadores de alteração recente ou anomalia.
- Linha clicável configurável sem conflitar com botões internos.[cite:1]

### Estados da tabela

- Sem registros iniciais.
- Sem resultado após filtros.
- Carregando primeira página.
- Carregando nova página.
- Erro na consulta.
- Modo bulk ativo.
- Linhas parcialmente indisponíveis por permissão.[cite:1]

### Ações de linha obrigatórias

- Visualizar.
- Editar.
- Duplicar.
- Arquivar ou inativar.
- Excluir com confirmação.
- Abrir histórico.
- Abrir auditoria.
- Mais ações contextuais.[cite:1]

### Saved views do DataTable

Cada tabela importante deve permitir salvar visões com os seguintes campos.[cite:1]

- Nome da view.
- Escopo pessoal ou compartilhado.
- Colunas visíveis.
- Ordenação aplicada.
- Filtros ativos.
- Densidade.
- Agrupamentos.
- Pin de colunas.
- View padrão.[cite:1]

## Módulo 2 — Widgets

Widgets são blocos compactos para dashboards, home operacionais e resumos de entidades.[cite:1]

### Tipos obrigatórios de widget

- KPI numérico.
- KPI comparativo com delta.
- Lista curta.
- Timeline.
- Alerta operacional.
- Meta e progresso.
- Ranking.
- Distribuição por categoria.
- Heat summary.
- Próximos vencimentos.
- Pendências por SLA.
- Atividade recente.[cite:1]

### Estrutura mínima do widget

- Cabeçalho com título, subtítulo e menu.
- Conteúdo principal.
- Rodapé opcional com link, insight ou atualização.
- Estado de loading, erro e vazio.[cite:1]

### Controles obrigatórios dos widgets

- Seleção de período.
- Refresh manual.
- Expandir para tela completa ou detalhe.
- Menu contextual.
- Drill-down quando houver granularidade.
- Indicador de última atualização.
- Compartilhar ou copiar link quando aplicável.[cite:1]

### Widgets recomendados para dashboard principal

| Widget | Conteúdo | Ações |
|---|---|---|
| Receita/volume | Valor atual, delta, tendência. [cite:1] | Ver relatório, alterar período. [cite:1] |
| Pendências | Total aberto por prioridade. [cite:1] | Abrir fila filtrada. [cite:1] |
| SLA | Dentro e fora do prazo. [cite:1] | Ver detalhes. [cite:1] |
| Usuários ativos | Total e crescimento. [cite:1] | Abrir analytics. [cite:1] |
| Erros recentes | Incidentes e severidade. [cite:1] | Ver log ou auditoria. [cite:1] |
| Automações | Execuções, falhas, taxa de sucesso. [cite:1] | Abrir automações. [cite:1] |

## Módulo 3 — Charts

Os charts devem ser integrados ao design system, legíveis em dashboards densos e com boa experiência de drill-down.[cite:1]

### Tipos obrigatórios

- Line chart.
- Bar chart.
- Stacked bar.
- Area chart.
- Donut chart.
- Pie apenas quando estritamente necessário.
- Horizontal bar.
- Heatmap.
- Funnel.
- Scatter.
- Mixed chart.
- Sparkline.[cite:1]

### Controles obrigatórios para charts

- Alterar período.
- Alterar granularidade, por dia, semana, mês, trimestre.
- Seleção de série.
- Mostrar ou ocultar legenda.
- Tooltip detalhado.
- Exportar imagem ou dados.
- Drill-down por ponto ou segmento.
- Reset de zoom.
- Comparar com período anterior.
- Meta/linha de referência.
- Toggle absoluto versus percentual.[cite:1]

### Regras de UX

- Não depender só de cor para diferenciar séries.
- Sempre exibir unidade de medida.
- Evitar pizza com muitas categorias.
- Em telas pequenas, priorizar sparklines, barras horizontais e resumos textuais.
- Todo gráfico deve ter fallback textual dos principais insights.[cite:1]

### Cards analíticos compostos

A biblioteca deve oferecer cards híbridos combinando KPI, chart e tabela resumida.[cite:1]

Exemplos.

- Receita mensal com delta, sparkline e top 3 origens.
- Tickets por status com donut e SLA médio.
- Ocupação por unidade com heatmap e ranking lateral.[cite:1]

## Módulo 4 — CRUD Drawers

CRUD drawers são painéis laterais para criação, edição, visualização rápida e ações transacionais sem navegação disruptiva.[cite:1]

### Tipos de drawer

- Create drawer.
- Edit drawer.
- View drawer.
- Clone drawer.
- Approval drawer.
- Side detail drawer.[cite:1]

### Estrutura padrão do drawer

1. Header com título, entidade, status e ações rápidas.
2. Corpo com formulário ou resumo estruturado.
3. Footer fixo com ações primárias e secundárias.
4. Área opcional de auditoria resumida.
5. Banner contextual para erros, alertas ou dependências.[cite:1]

### Controles obrigatórios

- Fechar.
- Salvar.
- Salvar e continuar.
- Salvar e novo.
- Cancelar.
- Confirmar saída com alterações não salvas.
- Próximo e anterior quando houver navegação entre registros.
- Duplicar.
- Excluir ou arquivar quando permitido.[cite:1]

### Recursos obrigatórios de formulário

- Validação inline.
- Máscaras configuráveis.
- Ajuda contextual.
- Campos condicionais.
- Seções expansíveis.
- Stepper interno para formulários longos.
- Autosave opcional.
- Uploads.
- Relacionamentos pesquisáveis.
- Tags.
- Checklists.
- Notas internas.
- Histórico resumido.[cite:1]

### Estados obrigatórios

- Novo registro.
- Edição.
- Somente leitura.
- Aprovando.
- Rejeitando.
- Bloqueado por conflito de edição.
- Carregando dados de apoio.
- Erro de validação de servidor.[cite:1]

### Seções padrão recomendadas em drawers complexos

| Seção | Conteúdo |
|---|---|
| Dados principais | Nome, código, descrição, status. [cite:1] |
| Classificação | Categoria, tipo, tags, origem. [cite:1] |
| Relacionamentos | Unidade, responsável, cliente, grupo. [cite:1] |
| Regras | Limites, flags, parâmetros. [cite:1] |
| Arquivos | Anexos e evidências. [cite:1] |
| Auditoria | Criado por, atualizado por, timeline curta. [cite:1] |

## Módulo 5 — Kanban

O Kanban deve atender fluxos operacionais com grande volume, múltiplas colunas e regras de transição.[cite:1]

### Estrutura do board

- Header do board.
- Filtros e visão.
- Colunas configuráveis.
- Cards arrastáveis.
- Rodapé por coluna com contagem e ações.
- Painel lateral de detalhes opcional.[cite:1]

### Controles obrigatórios

- Busca.
- Filtro por responsável.
- Filtro por status, prioridade, unidade, data e tags.
- Agrupar por pipeline, time ou categoria.
- Expandir ou colapsar colunas.
- Limite visual de WIP.
- Drag and drop com regras de negócio.
- Quick add card.
- Quick edit card.
- Abrir drawer detalhado.
- Ordenação interna da coluna.
- Modo fullscreen.[cite:1]

### Conteúdo mínimo do card Kanban

- Título.
- ID ou protocolo.
- Status ou etapa.
- Responsável.
- Prazo ou idade.
- Prioridade.
- Tags.
- Indicador de bloqueio.
- Indicador de comentários ou anexos.[cite:1]

### Regras obrigatórias do Kanban

- Validação antes da mudança de etapa.
- Confirmação para etapas críticas.
- Bloqueio de drop por permissão ou pré-condição.
- Registro de auditoria no drag and drop.
- Atualização otimista com rollback em caso de erro.
- Visualização mobile alternativa, como lista por etapa.[cite:1]

## Módulo 6 — Automações

A área de automações deve permitir criação, monitoramento, versionamento e governança de regras operacionais.[cite:1]

### Páginas obrigatórias de automação

1. Lista de automações.
2. Builder de automação.
3. Histórico de execuções.
4. Catálogo de gatilhos e ações.
5. Logs e falhas.
6. Configurações globais.[cite:1]

### Componentes obrigatórios do builder

- Nome da automação.
- Descrição.
- Status ativo/inativo.
- Escopo da automação.
- Trigger selector.
- Condições.
- Operadores lógicos.
- Ações encadeadas.
- Delay ou agendamento.
- Simulação/teste.
- Versionamento.
- Publicar/rascunho.
- Guardrails e limites.[cite:1]

### Tipos de gatilho

- Criação de registro.
- Atualização de campo.
- Mudança de status.
- Data programada.
- Webhook recebido.
- Evento manual.
- Inatividade.
- Meta atingida ou violada.[cite:1]

### Tipos de ação

- Atualizar campo.
- Enviar e-mail.
- Enviar notificação in-app.
- Criar tarefa.
- Atribuir responsável.
- Mover etapa.
- Gerar documento.
- Chamar webhook.
- Abrir aprovação.
- Inserir comentário interno.[cite:1]

### Controles obrigatórios de governança

- Duplicar automação.
- Versionar.
- Ativar/desativar.
- Testar com payload exemplo.
- Ver impacto estimado.
- Ver histórico.
- Reprocessar falhas.
- Limites de execução.
- Escopo por tenant, unidade ou entidade.[cite:1]

### Tabela de execuções

A tabela de execuções deve conter no mínimo: ID, automação, trigger, entidade, horário, duração, resultado, tentativas, originador e ação de detalhes.[cite:1]

## Módulo 7 — Controles

Controles representam interfaces de comando, filtragem, interação e configuração fina.[cite:1]

### Grupos de controles obrigatórios

- Inputs de texto.
- Inputs numéricos.
- Date e time controls.
- Range controls.
- Select simples.
- Select remoto.
- MultiSelect.
- TreeSelect.
- Checkbox e radio groups.
- Switches.
- Segment controls.
- Botões com split action.
- Toggle groups.
- Chips e tags.
- Upload controls.
- Rich text básico.
- Color/status selector quando permitido pelo domínio.[cite:1]

### Requisitos comuns dos controles

- Label.
- Hint.
- Placeholder.
- Estado obrigatório.
- Estado inválido.
- Estado desabilitado.
- Estado leitura.
- Mensagem de erro.
- Suporte a teclado.
- Ajuda contextual.[cite:1]

### Controles avançados necessários

- Filtro por data relativa, hoje, ontem, últimos 7 dias, mês atual.
- Campo de busca com debounce.
- Select com paginação remota.
- Selector de entidade com avatar e metadados.
- Controle de permissões por checkbox matrix.
- Reorder list.
- Dual list transfer.
- Cron expression helper para automações.[cite:1]

## Módulo 8 — Gerenciamentos

Gerenciamentos são páginas completas para operação administrativa e estratégica do sistema.[cite:1]

### Tipos obrigatórios de páginas de gerenciamento

- Gestão de usuários.
- Gestão de perfis e permissões.
- Gestão de unidades/filiais.
- Gestão de entidades de negócio.
- Gestão de categorias e taxonomias.
- Gestão de integrações.
- Gestão de automações.
- Gestão de notificações.
- Gestão de auditoria e logs.
- Gestão de configurações globais.
- Gestão de documentos e anexos.
- Gestão de filas e pendências.[cite:1]

## Páginas completas obrigatórias

Abaixo estão os blueprints completos mínimos para a biblioteca.

## Página 1 — Dashboard Executivo

### Objetivo

Exibir visão consolidada do negócio e permitir navegação rápida para áreas críticas.[cite:1]

### Blocos obrigatórios

- Header com período, unidade, escopo e ações.
- Linha de KPIs principais.
- Grid de widgets analíticos.
- Chart de tendência principal.
- Ranking ou distribuição.
- Feed de alertas.
- Lista de pendências críticas.
- Atalhos operacionais.[cite:1]

### Controles obrigatórios

- Período.
- Unidade.
- Segmento.
- Comparar com período anterior.
- Atualizar dados.
- Exportar visão.
- Compartilhar link interno.[cite:1]

### Estados necessários

- Sem dados do período.
- Carregando dashboard.
- Dados parciais com falha em um widget.
- Acesso limitado por escopo.[cite:1]

## Página 2 — Listagem Mestre com DataTable

### Objetivo

Servir como página padrão para qualquer entidade com operação massiva.[cite:1]

### Estrutura

- Header.
- Toolbar com busca e filtros.
- Quick filters.
- Tabela principal.
- Painel de bulk actions.
- Paginação e resumo.[cite:1]

### Controles obrigatórios

- Novo registro.
- Exportar.
- Importar.
- Salvar view.
- Editar colunas.
- Reset filtros.
- Seleção em massa.[cite:1]

### Variações obrigatórias

- Entidade simples.
- Entidade com relações.
- Entidade sensível com colunas mascaradas.
- Entidade arquivável.[cite:1]

## Página 3 — Detalhe de Entidade

### Objetivo

Apresentar visão 360 da entidade sem perder contexto operacional.[cite:1]

### Seções obrigatórias

- Cabeçalho com identidade do registro.
- Resumo geral.
- Dados principais.
- Relacionamentos.
- Timeline.
- Anexos.
- Auditoria.
- Ações rápidas.
- Blocos analíticos ou operacionais relacionados.[cite:1]

### Controles obrigatórios

- Editar.
- Duplicar.
- Arquivar.
- Excluir.
- Compartilhar referência.
- Abrir histórico.
- Abrir logs relacionados.[cite:1]

## Página 4 — CRUD com Drawer

### Objetivo

Permitir manipulação rápida de registros a partir da listagem.[cite:1]

### Fluxos obrigatórios

- Criar a partir da listagem.
- Editar sem sair da página.
- Visualizar detalhes curtos.
- Salvar e permanecer no contexto.
- Retomar edição interrompida.[cite:1]

### Controles obrigatórios

- Dirty state guard.
- Validação inline.
- Navegação por seções.
- Upload.
- Relacionamentos remotos.
- Rodapé fixo com CTA principal.[cite:1]

## Página 5 — Kanban Operacional

### Objetivo

Gerenciar pipelines operacionais, comerciais ou de atendimento.[cite:1]

### Blocos obrigatórios

- Header de pipeline.
- Filtros rápidos.
- Métricas do board.
- Colunas com cards.
- Drawer lateral.
- Indicadores de SLA e bloqueios.[cite:1]

### Controles obrigatórios

- Alterar board.
- Filtrar responsáveis.
- Adicionar card.
- Arrastar e soltar.
- Ver detalhes.
- Alternar para visão lista.[cite:1]

## Página 6 — Gestão de Automações

### Objetivo

Centralizar desenho, governança e observabilidade das automações.[cite:1]

### Blocos obrigatórios

- Listagem de automações.
- Filtros por status, trigger e escopo.
- Cards de saúde das execuções.
- Histórico recente.
- CTA para nova automação.[cite:1]

### Controles obrigatórios

- Nova automação.
- Duplicar.
- Ativar/desativar.
- Testar.
- Publicar.
- Ver logs.
- Reprocessar falhas.[cite:1]

## Página 7 — Builder de Automação

### Objetivo

Permitir criação visual e governada de regras.[cite:1]

### Seções obrigatórias

- Metadados da automação.
- Trigger.
- Condições.
- Fluxo de ações.
- Testes.
- Versionamento.
- Publicação.[cite:1]

### Controles obrigatórios

- Adicionar condição.
- Agrupar lógica.
- Adicionar ação.
- Reordenar ações.
- Testar payload.
- Validar dependências.
- Salvar rascunho.
- Publicar versão.[cite:1]

## Página 8 — Gestão de Usuários

### Objetivo

Administrar usuários, convites, status e vínculos com segurança.[cite:1]

### Seções obrigatórias

- DataTable de usuários.
- Filtros por status, role, unidade e origem.
- Drawer de criação/edição.
- Bloco de convites pendentes.
- Bloco de atividade recente.
- Ações em lote.[cite:1]

### Controles obrigatórios

- Convidar usuário.
- Ativar/desativar.
- Resetar acesso.
- Reenviar convite.
- Vincular unidade.
- Alterar perfil.
- Exportar.[cite:1]

## Página 9 — Perfis e Permissões

### Objetivo

Gerenciar RBAC e escopos operacionais.[cite:1]

### Blocos obrigatórios

- Lista de perfis.
- Drawer de perfil.
- Matriz de permissões.
- Escopos por tenant, unidade e recurso.
- Resumo de impacto do perfil.[cite:1]

### Controles obrigatórios

- Criar perfil.
- Clonar perfil.
- Editar permissões.
- Comparar perfis.
- Publicar alteração.
- Ver usuários impactados.[cite:1]

## Página 10 — Auditoria e Logs

### Objetivo

Expor rastreabilidade operacional e de segurança.[cite:1]

### Blocos obrigatórios

- DataTable de eventos.
- Filtros por ator, ação, recurso, data e severidade.
- Timeline lateral.
- JSON viewer ou payload viewer.
- Exportação permitida por perfil.[cite:1]

### Controles obrigatórios

- Buscar por ID.
- Filtrar intervalo.
- Ver diff.
- Ver contexto.
- Copiar referência.
- Exportar resultados.[cite:1]

## Página 11 — Configurações Gerais

### Objetivo

Concentrar parâmetros sistêmicos com segurança e clareza.[cite:1]

### Seções obrigatórias

- Geral.
- Branding.
- Notificações.
- Integrações.
- Segurança.
- Privacidade.
- Parametrizações avançadas.[cite:1]

### Controles obrigatórios

- Navegação por tabs ou sidebar interna.
- Modo edição seguro.
- Controle de dirty state.
- Histórico resumido.
- Validação por seção.
- Salvar por bloco ou página.[cite:1]

## Página 12 — Central de Notificações e Pendências

### Objetivo

Exibir tarefas, alertas, aprovações e itens críticos em uma fila acionável.[cite:1]

### Blocos obrigatórios

- Cards de resumo.
- Filtros por tipo, prioridade, origem e vencimento.
- Lista ou tabela de pendências.
- Ações rápidas.
- Timeline resumida.[cite:1]

### Controles obrigatórios

- Marcar como lido.
- Resolver.
- Delegar.
- Abrir detalhe.
- Filtrar minhas pendências.
- Ordenar por urgência.[cite:1]

## Página 13 — Gestão de Integrações

### Objetivo

Administrar conectores, credenciais, eventos e status de sincronização.[cite:1]

### Seções obrigatórias

- Lista de integrações.
- Status cards.
- Histórico de sync.
- Logs de erro.
- Drawer de credenciais/configuração.
- Teste de conexão.[cite:1]

### Controles obrigatórios

- Conectar.
- Desconectar.
- Testar.
- Reprocessar.
- Ver logs.
- Renovar credencial.[cite:1]

## Página 14 — Gestão de Documentos e Anexos

### Objetivo

Gerenciar arquivos vinculados a entidades com rastreabilidade.[cite:1]

### Blocos obrigatórios

- Lista ou grid de arquivos.
- Preview.
- Filtros por tipo, entidade, data, autor.
- Upload drawer.
- Histórico de versões.[cite:1]

### Controles obrigatórios

- Upload múltiplo.
- Substituir versão.
- Baixar.
- Compartilhar referência.
- Vincular entidade.
- Excluir com confirmação.[cite:1]

## Padrões transversais por página

### Header padrão

Todo header de página deve conter os itens abaixo quando aplicável.[cite:1]

- Breadcrumb.
- Título.
- Descrição curta.
- Badge de status.
- Última atualização.
- Ações primárias.
- Menu de overflow.[cite:1]

### Barra de filtros padrão

- Busca global.
- Filtros principais.
- Chips ativos.
- Contador de filtros.
- Limpar filtros.
- Salvar view.[cite:1]

### Bulk actions padrão

- Selecionados.
- Limpar seleção.
- Exportar.
- Alterar status.
- Atribuir.
- Arquivar.
- Excluir quando permitido.[cite:1]

### Timeline padrão

A timeline deve suportar eventos de negócio, sistema e auditoria, com tipo, ator, timestamp, resumo, detalhe expandível e ação de cópia de referência.[cite:1]

## Contratos de integração recomendados

A biblioteca deve padronizar interfaces de integração para facilitar o consumo por frontends diferentes.[cite:1]

### Contrato mínimo de listagem

```ts
interface ListResponse<T> {
  data: T[];
  total: number;
  page: number;
  perPage: number;
  filters?: Record<string, unknown>;
  sort?: { field: string; direction: 'asc' | 'desc' }[];
  meta?: Record<string, unknown>;
}
```

### Contrato mínimo de opção remota

```ts
interface RemoteOption {
  id: string | number;
  label: string;
  description?: string;
  avatar?: string;
  meta?: Record<string, unknown>;
  disabled?: boolean;
}
```

### Contrato de evento de auditoria

```ts
interface AuditEvent {
  id: string;
  actor: string;
  action: string;
  resource: string;
  resourceId: string;
  timestamp: string;
  summary: string;
  details?: unknown;
  severity?: 'info' | 'warning' | 'critical';
}
```

## Permissões e escopos

Todo blueprint deve permitir composição com camadas de autorização.[cite:1]

### Tipos mínimos de escopo

- Tenant.
- Unidade.
- Papel.
- Recurso.
- Ação.
- Campo sensível.
- Operação em lote.[cite:1]

### Comportamentos obrigatórios por permissão

- Esconder ação quando necessário.
- Desabilitar ação quando a existência da feature puder ser conhecida.
- Exibir motivo do bloqueio em tooltip ou helper text.
- Mascarar dados sensíveis parcialmente.
- Exigir dupla confirmação para ações críticas.[cite:1]

## Acessibilidade

A biblioteca deve nascer acessível por padrão.[cite:1]

### Requisitos mínimos

- Navegação por teclado.
- Focus visible consistente.
- Labels e descrições para inputs.
- ARIA para componentes compostos quando necessário.
- Contraste adequado.
- Mensagens de erro associadas ao campo.
- Toasts não exclusivos para feedback crítico.
- Drag and drop com alternativa por teclado quando aplicável.[cite:1]

## Responsividade

Em mobile, a biblioteca deve preservar operação essencial sem tentar replicar toda a densidade desktop.[cite:1]

### Estratégias mínimas

- Tabelas com horizontal scroll ou modo cards.
- Drawers full-screen em telas pequenas.
- Widgets empilhados em uma coluna.
- Kanban alternando para listas por etapa.
- Toolbars quebradas em menus contextuais.[cite:1]

## Performance

### Requisitos mínimos

- Virtualização para tabelas extensas.
- Lazy loading em widgets pesados.
- Debounce em buscas remotas.
- Memoização para colunas e filtros complexos.
- Atualização parcial de widgets e charts.
- Skeletons ao invés de reflow bruto.[cite:1]

## Convenção de diretórios sugerida

```txt
/ui-library
  /foundations
  /atoms
  /molecules
  /organisms
  /templates
  /pages
  /domain-packs
  /hooks
  /adapters
  /types
  /tokens
  /docs
```

## Checklist de aceite por página

| Item | Obrigatório |
|---|---|
| Header completo | Sim [cite:1] |
| Estados de loading/empty/error | Sim [cite:1] |
| Controle de permissão | Sim [cite:1] |
| Telemetria | Sim [cite:1] |
| Responsividade | Sim [cite:1] |
| Acessibilidade | Sim [cite:1] |
| Feedback transacional | Sim [cite:1] |
| Auditoria em ações críticas | Sim [cite:1] |
| Documentação de props e eventos | Sim [cite:1] |

## Entregáveis esperados da biblioteca

- Catálogo visual dos componentes.
- Guia de uso por contexto.
- Specs funcionais por página.
- Contratos de integração.
- Mapa de permissões.
- Guidelines de acessibilidade.
- Guidelines de telemetria.
- Exemplos de composição por domínio.[cite:1]

## Roadmap sugerido de implementação

### Fase 1

- Foundations.
- Controles base.
- DataTable.
- Drawers CRUD.
- Widgets KPI.
- Charts principais.[cite:1]

### Fase 2

- Kanban.
- Automações.
- Permissões.
- Auditoria.
- Integrações.[cite:1]

### Fase 3

- Domain packs.
- Saved views avançadas.
- Personalização por perfil.
- Templates analíticos avançados.[cite:1]

## Critério final de qualidade

A biblioteca só deve ser considerada pronta quando uma equipe conseguir montar qualquer tela administrativa relevante combinando templates, organismos e contratos padrão, sem redesenhar controles básicos e sem criar divergência estrutural entre módulos.[cite:1]
