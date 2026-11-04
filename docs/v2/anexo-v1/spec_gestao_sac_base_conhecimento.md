# Spec - Gestão de SAC e Base de Conhecimento

- Language Standard: Global English
## Objetivo
Criar um módulo completo de Gestão de SAC com base de conhecimento integrada, cobrindo atendimento omnichannel, triagem, categorização, SLA, automações, dashboards, relatórios, controle operacional e gestão de conteúdo.

## Escopo funcional
O sistema deve permitir:
- Receber, classificar, priorizar e acompanhar tickets de atendimento.
- Gerenciar base de conhecimento pública e interna.
- Automatizar regras de distribuição, resposta, escalonamento e encerramento.
- Visualizar operações por datatables, widgets, charts, Kanban e drawers de CRUD.
- Controlar usuários, filas, permissões, categorias, macros, SLAs, tags, canais e auditoria.
- Operar com múltiplas unidades, departamentos e equipes.

## Módulos principais

### 1. Gestão de Tickets SAC
Função central para abertura, triagem, atendimento e encerramento de solicitações.

#### Funcionalidades
- Criar ticket manualmente, via portal, e-mail, API ou integração.
- Identificar cliente, unidade, canal, assunto e origem.
- Classificar por tipo, prioridade, categoria, subcategoria e motivo.
- Definir status, SLA, responsável, fila e equipe.
- Registrar mensagens, anexos, notas internas e histórico completo.
- Vincular ticket a pedido, contrato, aluno, paciente, colaborador ou ativo.
- Encaminhar, transferir, escalar, resolver, reabrir e encerrar.
- Gerenciar tempo de atendimento, primeira resposta e resolução.

#### Controles necessários
- Botão Novo Ticket.
- Botão Responder.
- Botão Encaminhar.
- Botão Escalar.
- Botão Resolver.
- Botão Reabrir.
- Botão Encerrar.
- Botão Adicionar nota interna.
- Botão Anexar arquivo.
- Botão Vincular entidade.
- Dropdown de fila.
- Dropdown de prioridade.
- Dropdown de canal.
- Dropdown de status.
- Dropdown de tags.
- Seletor de unidade.
- Seletor de responsável.
- Campo de busca global.

### 2. Kanban de Atendimento
Visão operacional para acompanhamento dos tickets por etapa.

#### Colunas sugeridas
- Novo.
- Triagem.
- Em atendimento.
- Aguardando cliente.
- Aguardando interno.
- Escalado.
- Resolvido.
- Encerrado.

#### Controles necessários
- Arrastar e soltar tickets.
- Filtros por fila, agente, SLA, prioridade e unidade.
- Atalhos para abrir drawer do ticket.
- Indicadores de atraso por cartão.
- Seleção múltipla em lote.
- Ações rápidas por card.

### 3. Datatables Operacionais
Listagens completas para gestão diária.

#### Listas obrigatórias
- Tickets.
- Clientes.
- Interações.
- Categorias.
- Subcategorias.
- Filas.
- Agentes.
- Equipes.
- SLA.
- Macros.
- Tags.
- Canal de atendimento.
- Base de conhecimento.
- Avaliações de atendimento.
- Logs e auditoria.

#### Controles necessários
- Paginação.
- Ordenação por coluna.
- Busca textual.
- Filtro avançado.
- Exportação CSV/XLSX/PDF.
- Seleção em lote.
- Ações em massa.
- Colunas ocultáveis.
- Ajuste de densidade.
- Fixação de colunas.
- Salvar visão.

### 4. Widgets Executivos
Painéis resumidos para operação e gestão.

#### Widgets sugeridos
- Total de tickets abertos.
- Tickets novos hoje.
- Tickets vencidos.
- Tempo médio de primeira resposta.
- Tempo médio de resolução.
- Tickets por fila.
- Tickets por canal.
- Taxa de reabertura.
- Índice de satisfação.
- Base de conhecimento mais acessada.
- Agentes com maior backlog.
- Produtividade por equipe.
- SLA em risco.

#### Controles necessários
- Troca de período.
- Filtro por unidade.
- Filtro por fila.
- Filtro por canal.
- Drill-down para lista detalhada.
- Atualização automática.

### 5. Charts Analíticos
Dashboards visuais para monitoramento e decisão.

#### Gráficos recomendados
- Linha de volume de tickets por dia.
- Barras de tickets por categoria.
- Pizza de distribuição por canal.
- Área de SLA cumprido vs vencido.
- Funil de status do atendimento.
- Heatmap por horário e dia da semana.
- Barras empilhadas por equipe e prioridade.
- Linha de tempo de atendimento por unidade.

#### Controles necessários
- Período personalizado.
- Comparação entre períodos.
- Filtro por unidade, canal, equipe e categoria.
- Exportar imagem e dados.
- Alternar tipo de visualização.

### 6. CRUD Drawers
Edição rápida sem sair da tela principal.

#### Entidades com drawer
- Ticket.
- Cliente.
- Categoria.
- Subcategoria.
- Fila.
- SLA.
- Macro.
- Tag.
- Canal.
- Artigo da base de conhecimento.
- Usuário agente.
- Equipe.
- Regra de automação.

#### Controles necessários
- Abrir em modo criar, editar ou visualizar.
- Salvar e continuar.
- Salvar e fechar.
- Cancelar.
- Validadores inline.
- Upload de imagens e anexos.
- Editor rich text para artigos.
- Preview antes de publicar.

### 7. Base de Conhecimento
Gestão de artigos internos e públicos para autoatendimento e padronização.

#### Funcionalidades
- Criar artigos com título, resumo, categoria, tags, conteúdo e anexos.
- Controlar versões e histórico de revisão.
- Publicar, agendar, arquivar e restaurar artigos.
- Definir visibilidade pública, interna ou restrita por unidade.
- Relacionar artigos a tickets e macros.
- Exibir sugestões automáticas durante atendimento.
- Avaliação de utilidade e feedback do usuário.

#### Controles necessários
- Editor WYSIWYG.
- Inserção de blocos.
- Upload de mídia.
- Busca por conteúdo.
- Filtro por status.
- Filtro por categoria.
- Botão publicar.
- Botão arquivar.
- Botão duplicar.
- Botão revisar.
- Botão versionar.

### 8. Automação
Regras para redução de tempo operacional e padronização.

#### Automação obrigatória
- Distribuição automática por fila, categoria ou carga do agente.
- Resposta automática de recebimento.
- Escalonamento por tempo de inatividade.
- Fechamento automático por regra.
- Abertura de tarefa derivada.
- Notificação para cliente e equipe.
- Sugestão de artigo da base.
- Macro por palavra-chave ou evento.
- Regras por prioridade, unidade, canal e horário.

#### Controles necessários
- Criar regra.
- Ativar/desativar regra.
- Ordenar prioridade da regra.
- Simular execução.
- Auditar execuções.
- Testar condição.
- Definir gatilho, condição e ação.

### 9. Controles Operacionais
Recursos de governança, segurança e conformidade.

#### Itens obrigatórios
- Perfis e permissões por papel.
- Escopo por unidade e departamento.
- Auditoria de alterações.
- Trilhas de conversa completas.
- Controle de anexos.
- LGPD com anonimização e retenção.
- Histórico de acesso.
- Logs de ação do agente.
- Bloqueio de exclusão sem permissão.
- Controle de visibilidade de notas internas.

### 10. Gerenciamentos
Cadastros administrativos do módulo.

#### Cadastros essenciais
- Categorias e subcategorias.
- Fila e grupos de atendimento.
- Equipes e agentes.
- Status e prioridades.
- SLAs e escalonamentos.
- Macros e respostas prontas.
- Tags e motivos de contato.
- Canais de atendimento.
- Templates de mensagens.
- Tipos de interação.
- Regras de automação.
- Base de conhecimento.

## Páginas completas

### 1. Dashboard SAC
Conteúdo:
- Widgets principais.
- Charts analíticos.
- Lista de tickets críticos.
- SLA em risco.
- Últimos artigos acessados.
- Atalhos de criação.

Controles:
- Filtro global.
- Filtro por período.
- Filtro por unidade.
- Filtro por canal.
- Atualização automática.

### 2. Lista de Tickets
Conteúdo:
- Datatable principal.
- Filtros avançados.
- Ações em massa.
- Exportação.
- Painel lateral com resumo.

Controles:
- Busca.
- Ordenação.
- Paginação.
- Filtro por status.
- Filtro por SLA.
- Filtro por responsável.
- Filtro por categoria.

### 3. Detalhe do Ticket
Conteúdo:
- Cabeçalho com status e SLA.
- Linha do tempo.
- Mensagens.
- Notas internas.
- Anexos.
- Dados do cliente.
- Relações com outros registros.
- Sugestões da base de conhecimento.

Controles:
- Responder.
- Encaminhar.
- Escalar.
- Reabrir.
- Encerrar.
- Adicionar nota.
- Vincular artigo.
- Adicionar tag.
- Alterar prioridade.
- Alterar responsável.

### 4. Kanban de Tickets
Conteúdo:
- Board por status.
- Cards com SLA e prioridade.
- Indicadores visuais de atraso.

Controles:
- Drag and drop.
- Filtros.
- Ações rápidas.
- Seleção múltipla.

### 5. Base de Conhecimento
Conteúdo:
- Lista de artigos.
- Status de publicação.
- Métricas de acesso.
- Categorias e tags.

Controles:
- Criar artigo.
- Editar.
- Publicar.
- Arquivar.
- Revisar.
- Versionar.
- Buscar conteúdo.

### 6. Automações
Conteúdo:
- Lista de regras.
- Histórico de execuções.
- Status de ativação.

Controles:
- Criar regra.
- Testar regra.
- Ativar/desativar.
- Duplicar.
- Excluir com confirmação.

### 7. Relatórios e BI
Conteúdo:
- Charts.
- Tabelas analíticas.
- Exportações.
- Filtros por unidade, período e equipe.

Controles:
- Drill-down.
- Salvar relatório.
- Agendar envio.
- Exportar PDF/XLSX/CSV.

### 8. Administração
Conteúdo:
- Cadastros mestres.
- Usuários.
- Perfis.
- Permissões.
- SLAs.
- Canais.
- Tags.
- Macros.
- Auditoria.

Controles:
- CRUD completo.
- Busca.
- Filtros.
- Importação e exportação.
- Histórico de alterações.

## Modelo de dados sugerido
- tickets
- ticket_messages
- ticket_notes
- ticket_attachments
- ticket_tags
- ticket_history
- customers
- agents
- teams
- queues
- categories
- subcategories
- sla_policies
- automations
- knowledge_articles
- knowledge_versions
- knowledge_feedback
- channels
- macros
- permissions
- audit_logs

## Requisitos não funcionais
- Performance com paginação e lazy loading.
- Permissões granulares por módulo, ação e unidade.
- LGPD com consentimento, retenção e anonimização.
- Auditoria completa de eventos críticos.
- Escalabilidade para múltiplas filas e canais.
- UI responsiva para desktop e tablet.
- Suporte a multilíngua, se necessário.

## Critérios de aceite
- O usuário consegue abrir, responder, encaminhar e encerrar tickets sem sair do fluxo principal.
- O gestor consegue acompanhar fila, SLA, volume e produtividade em tempo real.
- A equipe consegue consultar e publicar artigos com controle de versão.
- As automações executam ações por regra com rastreabilidade.
- Todas as páginas possuem datatable, widgets ou charts quando aplicável, além de drawers e controles de gestão.

## Entregáveis de UI
- Página dashboard.
- Página lista de tickets.
- Página detalhe do ticket.
- Página kanban.
- Página base de conhecimento.
- Página automações.
- Página relatórios.
- Página administração.
- Drawers de cadastro rápido.
- Modais de confirmação e exclusão.
- Estados vazios, loading, erro e sucesso.

## Observações finais
O módulo deve seguir padrão enterprise, com foco em operação intensiva, rastreabilidade, segurança e extensibilidade. A experiência precisa permitir atendimento rápido, gestão centralizada e autoatendimento eficiente.
