# Spec Funcional e Técnica — Gestão de Notificações

- Language Standard: Global English
## 1. Objetivo
A Gestão de Notificações centraliza a criação, segmentação, distribuição, acompanhamento e automação de notificações da plataforma multi-entity/multi-unit. O módulo deve suportar notificações operacionais, transacionais, informativas, críticas e automatizadas, com visão por entidade, unidade, canal, status e prioridade.

## 2. Escopo
O módulo cobre:
- Criação e disparo de notificações manuais e automáticas.
- Gestão de filas, agendamentos, regras, canais e templates.
- Monitoramento de entrega, leitura, falhas e retry.
- Organização em board Kanban por estágio operacional.
- Dashboards com widgets e gráficos analíticos.
- CRUD completo em drawers para operação rápida.
- Controles de segurança, auditoria, LGPD e governança.

## 3. Perfis de Acesso
- Super Admin.
- Admin da Entidade.
- Gestor da Unidade.
- Operador.
- Auditor/Compliance.
- Usuário Final.

## 4. Regras Gerais
- Toda notificação deve possuir entidade, unidade, tipo, canal, prioridade, status e responsável.
- O sistema deve permitir escopo global, por entidade, por unidade e por público segmentado.
- Notificações críticas devem exigir confirmação de leitura quando aplicável.
- Notificações com falha devem entrar em fila de retry com política configurável.
- Toda alteração relevante deve ser registrada em auditoria.
- Campos sensíveis devem respeitar LGPD, mascaramento e retenção configurável.

## 5. Entidades Principais
### 5.1 Notification
Campos mínimos:
- id
- uuid
- entity_id
- unit_id
- title
- subject
- message
- type
- category
- priority
- channel
- target_audience
- sender_type
- sender_id
- status
- scheduled_at
- sent_at
- delivered_at
- read_at
- failed_at
- expires_at
- retry_count
- max_retries
- metadata
- created_by
- updated_by
- created_at
- updated_at
- deleted_at

### 5.2 Notification Template
- id, uuid, entity_id, unit_id, name, code, channel, subject_template, body_template, variables_schema, active, created_at, updated_at.

### 5.3 Notification Rule / Automation
- id, uuid, entity_id, unit_id, name, trigger_event, conditions, actions, cooldown, active, priority, created_at, updated_at.

### 5.4 Notification Delivery Log
- id, notification_id, channel, provider, recipient, status, response_code, response_payload, attempt, sent_at, delivered_at, read_at, error_message.

### 5.5 Notification Queue
- id, notification_id, scheduled_at, processed_at, locked_at, worker_id, status, retry_count.

## 6. Páginas do Módulo
### 6.1 Dashboard Geral
Objetivo: mostrar visão executiva das notificações.
Controles obrigatórios:
- Filtro por período.
- Filtro por entidade.
- Filtro por unidade.
- Filtro por canal.
- Filtro por prioridade.
- Filtro por status.
- Busca global.
- Exportação CSV/PDF.

Widgets obrigatórios:
- Total de notificações.
- Enviadas hoje.
- Pendentes na fila.
- Taxa de entrega.
- Taxa de leitura.
- Falhas últimas 24h.
- Retries em andamento.
- Notificações críticas.

Charts obrigatórios:
- Linha: volume por dia.
- Barra: notificações por status.
- Pizza ou donut: distribuição por canal.
- Barras empilhadas: sucesso vs falha por canal.
- Heatmap: volume por hora/dia.

### 6.2 Lista de Notificações
Componente principal: datatable avançada.
Colunas:
- seleção.
- título.
- tipo.
- canal.
- prioridade.
- entidade.
- unidade.
- status.
- agendada para.
- enviada em.
- leitura.
- tentativas.
- responsável.
- ações.

Controles da datatable:
- pesquisa textual.
- filtros avançados.
- ordenação por coluna.
- paginação server-side.
- seleção múltipla.
- ações em lote.
- colunas configuráveis.
- densidade de visualização.
- salvar filtros favoritos.
- exportar lista.
- atualizar em tempo real.

Ações por linha:
- visualizar.
- editar.
- duplicar.
- reenviar.
- cancelar.
- marcar como lida.
- arquivar.
- excluir lógico.

### 6.3 Criação e Edição
Formato: drawer lateral com etapas.
Seções obrigatórias:
- Dados básicos.
- Público-alvo.
- Conteúdo.
- Canal.
- Agendamento.
- Regras e automações.
- Revisão final.

Campos obrigatórios:
- título.
- assunto.
- mensagem.
- canal.
- prioridade.
- entidades/unidades de destino.
- tipo de disparo.
- data e hora agendada, se aplicável.
- template.
- anexos, se suportado.
- confirmação de leitura.
- expiração.

Validações:
- campos obrigatórios por canal.
- limite de caracteres por canal.
- preview de variáveis do template.
- bloqueio de envio sem público válido.

### 6.4 Detalhe da Notificação
Conteúdo da página:
- resumo geral.
- timeline de eventos.
- histórico de entrega.
- destinatários.
- respostas e interações.
- logs técnicos.
- auditoria completa.
- dados de automação relacionada.

Ações:
- reenviar.
- cancelar agendamento.
- editar rascunho.
- gerar cópia.
- abrir incidente se falha crítica.

### 6.5 Kanban Operacional
Colunas recomendadas:
- Rascunho.
- Em revisão.
- Agendada.
- Processando.
- Enviada.
- Entregue.
- Lida.
- Falhou.
- Arquivada.

Controles do Kanban:
- drag and drop.
- filtros por responsável, canal e prioridade.
- cards compactos e expandíveis.
- badges de status.
- contadores por coluna.
- ações rápidas no card.
- WIP limit por coluna.

### 6.6 Automações
Página dedicada para regras automáticas.
Funcionalidades:
- criar automação.
- testar regra.
- simular disparo.
- habilitar/desabilitar.
- versionar regra.
- visualizar dependências.

Tipos de gatilhos:
- evento de cadastro.
- mudança de status.
- atraso.
- falha de processamento.
- aniversário.
- expiração.
- tarefa pendente.

Ações suportadas:
- criar notificação.
- notificar por canal específico.
- escalar para superior.
- abrir tarefa.
- registrar log.
- enviar para fila de retry.

### 6.7 Controles e Governança
Página de configuração global.
Seções:
- canais habilitados.
- provedores externos.
- templates.
- limites de envio.
- rate limit.
- janelas de silêncio.
- política de retry.
- retenção de logs.
- assinatura e branding.
- permissões por perfil.
- políticas LGPD.
- trilha de auditoria.

## 7. Widgets do Painel
Widgets mínimos obrigatórios:
- cards KPI com tendência.
- gráfico de leitura por canal.
- falhas por provedor.
- fila por prioridade.
- notificações críticas pendentes.
- tempo médio de entrega.
- SLA cumprido vs violado.
- atividade recente.

## 8. Fluxos Principais
### 8.1 Fluxo Manual
1. Usuário cria notificação.
2. Define público, canal e conteúdo.
3. Sistema valida regras.
4. Notificação entra em fila ou é enviada imediatamente.
5. Logs e métricas são atualizados.

### 8.2 Fluxo Automático
1. Evento dispara automação.
2. Motor avalia condições.
3. Sistema gera notificação baseada em template.
4. Envio ocorre pelo canal definido.
5. Status e auditoria são persistidos.

### 8.3 Fluxo de Falha
1. Provider retorna erro.
2. Sistema registra falha.
3. Retry é agendado conforme política.
4. Se exceder o limite, status vira falhou definitivo.
5. Caso crítico, abrir alerta interno.

## 9. Requisitos Não Funcionais
- Escalabilidade horizontal.
- Baixa latência na fila.
- Processamento assíncrono.
- Observabilidade com logs, métricas e tracing.
- Segurança por JWT, CSRF, rate limiting e RBAC.
- Compatibilidade com multi-entity e multi-unit.
- Auditoria completa com retenção configurável.
- Suporte a internacionalização, fuso horário e formatos locais.

## 10. Segurança e Compliance
- Mascaramento de dados sensíveis.
- Criptografia em repouso e em trânsito.
- Controle de acesso por perfil e escopo.
- Consentimento e base legal quando aplicável.
- Direito de exclusão/anonimização conforme LGPD.
- Registros de acesso e alteração.
- Bloqueio de canais não autorizados.

## 11. API Suggested
### Endpoints principais
- GET /notifications
- POST /notifications
- GET /notifications/{id}
- PUT /notifications/{id}
- DELETE /notifications/{id}
- POST /notifications/{id}/resend
- POST /notifications/{id}/cancel
- POST /notifications/{id}/mark-read
- GET /notification-templates
- POST /notification-templates
- GET /notification-rules
- POST /notification-rules
- GET /notification-queue
- GET /notification-logs
- GET /notification-dashboard

### Padrões de resposta
- Paginação server-side.
- Filtros normalizados.
- Erros padronizados.
- IDs UUID.
- Auditoria automática.

## 12. Layout UI Recomendado
- Topbar com busca global, filtros rápidos e ações primárias.
- Sidebar com Dashboard, Lista, Kanban, Automação, Templates, Logs e Configurações.
- Área central com cards, datatable e gráficos.
- Drawers laterais para CRUD rápido.
- Modal apenas para confirmações críticas.

## 13. Critérios de Aceite
- Criar, editar, agendar, reenviar, cancelar e arquivar notificações.
- Visualizar notificações em tabela, cards e Kanban.
- Operar automações baseadas em eventos.
- Monitorar entrega, leitura, erro e retry.
- Gerenciar templates, regras, canais e permissões.
- Exibir dashboards com widgets e charts atualizados.
- Registrar auditoria e obedecer políticas de segurança e LGPD.

## 14. Componentes Frontend
- NotificationDashboard
- NotificationDatatable
- NotificationDrawerForm
- NotificationKanbanBoard
- NotificationWidgets
- NotificationCharts
- NotificationAutomationBuilder
- NotificationTemplateManager
- NotificationDeliveryLogTable
- NotificationSettingsPanel

## 15. Prioridades de Implementação
### Fase 1
- Lista, drawer CRUD, detalhes, dashboard básico.

### Fase 2
- Kanban, automações, templates, logs e alertas.

### Fase 3
- métricas avançadas, SLA, auditoria ampliada, integrações externas.

## 16. Observações Finais
O módulo deve ser projetado para operação intensiva, com foco em governança, produtividade e rastreabilidade. A interface precisa permitir navegação rápida entre visão analítica, ação operacional e configuração administrativa, sem perder consistência entre entidade e unidade.
