# SPEC-HELPDESK.md

- Language Standard: Global English
## 1. Visão Geral

Este documento especifica um sistema SaaS multi-tenant de SAC / Help Desk / Service Desk inspirado em plataformas como Movidesk/Zenvia, com foco em centralização de canais, padronização de tickets, automação operacional, SLA, base de conhecimento, portal do cliente, relatórios e integrações. O sistema deve permitir atendimento omnichannel com rastreabilidade total, auditoria completa e flexibilidade para múltiplas empresas, unidades, equipes e perfis de acesso [web:32][web:11][web:51].

O objetivo é servir como especificação funcional e técnica base para desenvolvimento incremental, começando por um MVP sólido e evoluindo para automação avançada, múltiplos canais e recursos inteligentes de atendimento [web:32][web:7][web:54].

## 2. Objetivos do Produto

- Centralizar todos os canais de contato em uma única operação.
- Normalizar qualquer solicitação em um Ticket.
- Reduzir tempo de resposta e tempo de resolução.
- Garantir rastreabilidade e auditoria de ponta a ponta.
- Disponibilizar autoatendimento via portal e base de conhecimento.
- Automatizar triagem, roteamento, escalonamento e notificações.
- Suportar múltiplos tenants, unidades e equipes com segurança.
- Oferecer indicadores operacionais e gerenciais em tempo real.

## 3. Escopo

### 3.1 Incluído

- Gestão completa de tickets.
- Omnichannel de entrada e saída.
- Portal do cliente.
- Base de conhecimento.
- SLA e calendários de atendimento.
- Automação baseada em regras e eventos.
- Catálogo de serviços.
- Aprovações.
- Relatórios e dashboards.
- Administração e governança.
- Integrações e API.
- Auditoria e trilha de eventos.

### 3.2 Excluído no MVP

- Telefonia nativa com discador avançado.
- Inteligência artificial generativa para respostas automáticas.
- RPA para processos externos.
- Marketplace de extensões.
- BI avançado com cubos multidimensionais.

## 4. Definições

- **Tenant**: empresa cliente isolada logicamente dentro da plataforma.
- **Unidade**: subestrutura organizacional do tenant.
- **Fila**: agrupamento operacional de tickets.
- **Ticket**: unidade central de atendimento.
- **Solicitante**: pessoa que abre ou possui o ticket.
- **Contato**: pessoa relacionada ao ticket, podendo ser solicitante ou observador.
- **Agente**: usuário interno que atende tickets.
- **SLA**: compromisso de tempo de resposta e resolução.
- **Base de conhecimento**: artigos e conteúdos de autoatendimento.

## 5. Requisitos Funcionais

### 5.1 Multi-tenant

O sistema deve isolar dados por tenant em todos os níveis, incluindo tickets, usuários, canais, artigos, automações, relatórios e configurações. Um usuário autenticado só pode acessar dados autorizados pelo seu escopo de tenant, unidade, fila e permissão.

### 5.2 Gestão de tickets

O sistema deve permitir criação, leitura, atualização, vinculação, merge, split, reabertura, cancelamento, encerramento e exclusão lógica de tickets. Cada ticket deve manter histórico completo de campos, mensagens, status, responsáveis e SLAs.

### 5.3 Omnichannel

O sistema deve receber interações por múltiplos canais, normalizar a entrada e associá-la ao mesmo ticket ou criar um novo conforme regra de negócio. Todos os canais precisam preservar autoria, timestamp, anexos e origem.

### 5.4 Portal do cliente

O portal deve permitir abertura e acompanhamento de tickets, respostas públicas, envio de anexos, consulta a artigos da base e avaliação do atendimento.

### 5.5 Base de conhecimento

O sistema deve permitir criação, revisão, publicação, versionamento, busca e categorização de artigos. O conteúdo pode ser público, restrito ou interno.

### 5.6 Automação

O sistema deve suportar regras automáticas acionadas por eventos ou agendamentos, com condições, ações, exceções e logs.

### 5.7 SLA

O sistema deve calcular prazos de primeira resposta, próxima resposta e resolução, com base em regras por tenant, cliente, fila, prioridade, categoria e horário útil.

### 5.8 Relatórios

O sistema deve oferecer dashboards operacionais e relatórios exportáveis com métricas de volume, tempo, backlog, produtividade, SLA e satisfação.

### 5.9 Auditoria

Todas as ações críticas devem gerar eventos auditáveis com usuário, data, contexto, origem e alteração realizada.

## 6. Canais de Entrada de Ticket

### 6.1 Canais obrigatórios

- Portal do cliente.
- E-mail.
- Formulário web.
- WhatsApp Business API.
- Chat web.
- API REST.
- Webhook externo.
- Criação interna por agente.
- Importação em lote.
- Telefonia registrada manualmente.

### 6.2 Regras de normalização

- Toda entrada deve gerar evento de origem.
- Toda mensagem deve ser associada a um ticket novo ou existente.
- O sistema deve identificar o solicitante por e-mail, telefone, ID externo ou autenticação.
- O canal de origem deve ser preservado em toda a vida do ticket.
- Anexos devem ser vinculados ao ticket e à mensagem de origem.

### 6.3 Regras por canal

#### E-mail

- O sistema deve monitorar caixas de entrada configuradas.
- Assuntos e cabeçalhos devem ser preservados.
- Respostas devem manter thread.
- O sistema deve evitar duplicidade por heurística configurável.

#### WhatsApp

- Mensagens devem entrar como tickets ou mensagens vinculadas a tickets ativos.
- O sistema deve registrar número, nome exibido, mensagem e anexos.
- Respostas devem ser enviadas pela mesma sessão/canal.

#### Chat web

- O sistema deve abrir sessão de chat e, quando necessário, converter a conversa em ticket.
- O histórico do chat deve ser anexado ao ticket.

#### Formulário web

- O formulário deve ser configurável por tenant, categoria e fila.
- Campos obrigatórios devem variar por tipo de solicitação.

#### API

- A API deve aceitar payload autenticado e validado.
- O sistema deve suportar criação, atualização e consulta.

#### Webhook

- Integrações externas devem poder criar ou atualizar tickets por evento.

#### Criação interna

- Agentes devem poder abrir tickets para clientes, departamentos ou terceiros.

## 7. Modelo de Ticket

### 7.1 Identificação

- id.
- tenant_id.
- external_id.
- number.
- root_ticket_id.
- parent_ticket_id.
- merged_into_ticket_id.
- source_type.
- channel_id.

### 7.2 Solicitante

- requester_id.
- requester_name.
- requester_email.
- requester_phone.
- requester_document.
- requester_company.
- requester_department.
- requester_role.
- requester_locale.

### 7.3 Organização

- company_id.
- unit_id.
- department_id.
- queue_id.
- team_id.
- owner_user_id.
- owner_team_id.
- assigned_by.
- assigned_at.

### 7.4 Classificação

- type_id.
- category_id.
- subcategory_id.
- topic_id.
- priority.
- severity.
- impact.
- urgency.
- reason_code.
- resolution_code.
- close_reason_id.
- tags.

### 7.5 Conteúdo

- subject.
- description.
- public_description.
- internal_summary.
- resolution_summary.
- customer_expectation.
- initial_contact_channel.
- customer_language.

### 7.6 Estado

- status.
- substatus.
- visibility.
- is_urgent.
- is_vip.
- is_blocked.
- is_on_hold.
- is_escalated.
- is_reopened.
- reopened_count.

### 7.7 Datas e tempos

- created_at.
- updated_at.
- first_response_at.
- first_response_due_at.
- next_response_due_at.
- resolution_due_at.
- closed_at.
- resolved_at.
- reopened_at.
- last_activity_at.
- last_customer_message_at.
- last_agent_message_at.
- first_assignment_at.
- last_assignment_at.
- wait_started_at.
- wait_ended_at.
- sla_paused_at.
- sla_resumed_at.
- total_wait_minutes.
- total_work_minutes.
- total_pending_customer_minutes.
- total_pending_third_party_minutes.

### 7.8 Satisfação

- satisfaction_score.
- satisfaction_comment.
- satisfaction_answered_at.
- csat_sent_at.
- csat_status.

### 7.9 Metadados

- custom_fields.
- json_metadata.
- labels.
- attachments_count.
- messages_count.
- internal_notes_count.
- public_messages_count.
- views_count.
- source_reference.
- correlation_id.

## 8. Campos do Ticket

### 8.1 Campos padrão obrigatórios

- Assunto.
- Descrição.
- Solicitante.
- Canal.
- Categoria.
- Prioridade.
- Status.
- Fila.
- Responsável.
- SLA.
- Tipo.
- Tenant.

### 8.2 Campos recomendados

- Unidade.
- Departamento.
- Severidade.
- Impacto.
- Urgência.
- Tags.
- Motivo.
- Solução.
- Tempo estimado.
- Tempo gasto.
- Data de vencimento.
- Data de fechamento.
- Canal secundário.
- Observador.
- Ticket relacionado.

### 8.3 Campos customizáveis

- Texto curto.
- Texto longo.
- Número inteiro.
- Decimal.
- Moeda.
- Data.
- Data e hora.
- Booleano.
- Lista única.
- Lista múltipla.
- Upload.
- URL.
- E-mail.
- Telefone.
- CPF/CNPJ.
- Dependente.
- Calculado.
- Oculto.

### 8.4 Regras para campos customizáveis

- Devem ser configuráveis por tenant.
- Devem ser condicionais por categoria, fila, tipo ou canal.
- Devem suportar obrigatoriedade dinâmica.
- Devem ter validação de formato.
- Devem ser auditáveis quando alterados.

## 9. Estados do Ticket

- Novo.
- Aberto.
- Em triagem.
- Em atendimento.
- Aguardando cliente.
- Aguardando terceiro.
- Aguardando aprovação.
- Em pausa.
- Resolvido.
- Fechado.
- Cancelado.
- Reaberto.
- Escalonado.

### 9.1 Regras de transição

- Novo só pode ir para aberto, triagem ou cancelado.
- Resolvido pode ir para fechado ou reaberto.
- Aguardando cliente pausa contagem de trabalho conforme regra de SLA.
- Ticket fechado pode ser reaberto por janela configurável.

## 10. Prioridade, Impacto e Severidade

### 10.1 Prioridade

- Baixa.
- Média.
- Alta.
- Crítica.
- Urgente.

### 10.2 Impacto

- Individual.
- Setorial.
- Unidade.
- Empresa inteira.
- Múltiplos tenants em casos de fornecedor compartilhado.

### 10.3 Severidade

- S1 - Crítica.
- S2 - Alta.
- S3 - Média.
- S4 - Baixa.

### 10.4 Matriz de cálculo

A prioridade pode ser determinada por combinação de impacto e urgência, com overrides manuais permitidos por perfil autorizado.

## 11. Ferramentas do Agente

### 11.1 Operação

- Lista de tickets com filtros avançados.
- Visão Kanban.
- Busca global.
- Timeline completa.
- Thread de mensagens.
- Comentários internos.
- Respostas públicas.
- Respostas prontas.
- Macros.
- Templates.
- Encaminhamento.
- Reatribuição.
- Merge.
- Split.
- Link de tickets.
- Atribuição em lote.
- Edição em massa.
- Fechamento em massa.
- Reabertura.
- Cancelamento.
- Pausa de SLA.

### 11.2 Produtividade

- Atalhos de teclado.
- Editor rico.
- Preenchimento automático.
- Assinatura por equipe.
- Checklist.
- Tarefas internas.
- Menções.
- Agendamento de follow-up.
- Visualização do histórico do cliente.
- Visualização de tickets relacionados.
- Sugestão de artigo da base.

### 11.3 Supervisão

- Monitoramento de fila.
- Monitoramento de SLA.
- Visão de backlog.
- Reatribuição assistida.
- Escalonamento manual.
- Auditoria de operações.
- Dashboards por equipe e agente.

## 12. Portal do Cliente

### 12.1 Funcionalidades

- Criar ticket.
- Acompanhar ticket.
- Responder ticket.
- Anexar arquivo.
- Consultar histórico.
- Consultar base de conhecimento.
- Visualizar status.
- Receber notificações.
- Avaliar atendimento.
- Atualizar dados cadastrais.
- Consultar catálogo de serviços.

### 12.2 Regras

- O cliente só pode acessar seus próprios tickets e os tickets compartilhados com ele.
- Respostas no portal devem ser públicas por padrão.
- Campos do formulário podem variar por tenant, serviço ou fila.
- Artigos relevantes podem ser sugeridos antes da abertura do ticket.

## 13. Base de Conhecimento

### 13.1 Estrutura

- Categoria.
- Subcategoria.
- Artigo.
- Versão.
- Autor.
- Revisor.
- Publicador.
- Tags.
- Anexos.
- Estado de publicação.

### 13.2 Estados do artigo

- Rascunho.
- Em revisão.
- Agendado.
- Publicado.
- Arquivado.
- Restrito.

### 13.3 Funcionalidades

- Busca textual.
- Filtros por categoria.
- Artigos relacionados.
- FAQ.
- Feedback de utilidade.
- Histórico de versão.
- Controle de permissão.
- Sugestão automática no portal e no atendimento.

## 14. SLA

### 14.1 Tipos de SLA

- Primeira resposta.
- Próxima resposta.
- Resolução.
- Fechamento.

### 14.2 Regras de aplicação

- Por tenant.
- Por cliente.
- Por fila.
- Por tipo.
- Por categoria.
- Por prioridade.
- Por canal.
- Por contrato.
- Por horário de atendimento.
- Por feriado.

### 14.3 Estados do SLA

- Ativo.
- Em risco.
- Violado.
- Pausado.
- Reiniciado.

### 14.4 Ações automáticas

- Notificar agente.
- Notificar supervisor.
- Reatribuir ticket.
- Escalonar fila.
- Criar alerta.
- Marcar como violado.
- Registrar evento.

## 15. Automação

### 15.1 Tipos

- Gatilho por evento.
- Regra condicional.
- Workflow multi-etapa.
- Agendamento.
- Webhook.
- Ação manual.

### 15.2 Eventos

- Ticket criado.
- Ticket atualizado.
- Ticket atribuído.
- Status alterado.
- Mensagem recebida.
- Mensagem enviada.
- SLA próximo.
- SLA violado.
- Aprovação concluída.
- Artigo publicado.

### 15.3 Condições

- Canal.
- Categoria.
- Prioridade.
- Tenant.
- Unidade.
- Fila.
- Palavra-chave.
- Campo customizado.
- Horário.
- Usuário.
- Origem externa.

### 15.4 Ações

- Alterar status.
- Alterar prioridade.
- Alterar fila.
- Alterar responsável.
- Alterar campo.
- Aplicar tag.
- Remover tag.
- Enviar e-mail.
- Enviar WhatsApp.
- Criar tarefa.
- Criar subticket.
- Criar alerta.
- Chamar webhook.
- Notificar supervisor.
- Pausar SLA.
- Retomar SLA.

## 16. Aprovações

### 16.1 Casos de uso

- Solicitação de acesso.
- Solicitação de mudança.
- Solicitação financeira.
- Solicitação administrativa.
- Solicitação de exceção.
- Compra e contratação.

### 16.2 Campos de aprovação

- id.
- ticket_id.
- requested_by.
- requested_to.
- approver_id.
- status.
- requested_at.
- decided_at.
- decision_reason.
- approval_step.
- due_at.

## 17. Notificações

### 17.1 Canais

- E-mail.
- WhatsApp.
- In-app.
- Push.
- Webhook.

### 17.2 Eventos notificados

- Ticket criado.
- Ticket atribuído.
- Resposta recebida.
- SLA em risco.
- SLA violado.
- Aprovação pendente.
- Aprovação concluída.
- Ticket resolvido.
- Ticket fechado.

## 18. Relatórios e Indicadores

### 18.1 Operacionais

- Tickets por canal.
- Tickets por fila.
- Tickets por status.
- Tickets por prioridade.
- Tempo médio de primeira resposta.
- Tempo médio de resolução.
- Backlog.
- Aging de tickets.
- Reaberturas.
- Violação de SLA.
- Tickets por agente.
- Tickets por equipe.

### 18.2 Gerenciais

- CSAT.
- NPS.
- Volume por período.
- Tendência de atendimento.
- Produtividade individual.
- Produtividade da equipe.
- Motivos mais recorrentes.
- Causas de atraso.

### 18.3 Exportação

- CSV.
- XLSX.
- PDF.
- JSON.

## 19. API

### 19.1 Princípios

- RESTful.
- Autenticada.
- Versionada.
- Documentada com OpenAPI.
- Rate limited.
- Auditável.

### 19.2 Recursos principais

- /auth
- /tenants
- /users
- /customers
- /contacts
- /tickets
- /ticket-messages
- /ticket-attachments
- /sla-policies
- /queues
- /categories
- /custom-fields
- /knowledge-base/articles
- /workflows
- /approvals
- /reports
- /webhooks
- /audit-logs

### 19.3 Operações mínimas em tickets

- Criar.
- Atualizar.
- Consultar.
- Listar.
- Encerrar.
- Reabrir.
- Atribuir.
- Alterar status.
- Adicionar mensagem.
- Anexar arquivo.
- Aplicar tag.
- Consultar histórico.

## 20. Modelo de Banco de Dados

### 20.1 Entidades principais

- tenants
- organizations
- units
- departments
- users
- roles
- permissions
- user_roles
- customers
- contacts
- channels
- queues
- categories
- subcategories
- ticket_types
- tickets
- ticket_messages
- ticket_attachments
- ticket_tags
- ticket_custom_values
- sla_policies
- sla_targets
- automation_rules
- automation_events
- knowledge_articles
- knowledge_categories
- knowledge_tags
- approvals
- notifications
- audit_logs
- holidays
- calendars
- service_catalog_items
- service_requests
- integrations
- webhooks
- templates

### 20.2 Índices mínimos

- tenant_id em todas as tabelas multi-tenant.
- requester_id, owner_user_id, queue_id, status e priority em tickets.
- created_at e updated_at em tabelas transacionais.
- full-text em subject, description e article content.

## 21. Segurança

- Autenticação com JWT e refresh token.
- Opção de SSO.
- RBAC com escopo por tenant.
- Criptografia de dados sensíveis.
- Logs de auditoria imutáveis.
- Rate limiting por rota e por token.
- Proteção contra abuso de API.
- Validação forte de entrada.
- Sessões seguras.
- Controle de anexos e tipos de arquivo.
- Política de retenção e expurgo.

## 22. Observabilidade

- Logs estruturados.
- Métricas de sistema.
- Tracing de requisições.
- Alertas de fila e SLA.
- Monitoramento de integrações.
- Health checks.
- Métricas de erro por canal.

## 23. Requisitos Não Funcionais

- Alta disponibilidade.
- Escalabilidade horizontal.
- Baixa latência no atendimento.
- Processamento assíncrono para integrações e notificações.
- Backup automatizado.
- Restore testado.
- Governança de retenção.
- Compatibilidade com LGPD.
- Suporte a múltiplos idiomas no futuro.

## 24. Roadmap

### Fase 1 - MVP

- Tickets.
- Portal.
- E-mail.
- Base de conhecimento.
- SLA básico.
- Automação simples.
- Relatórios básicos.

### Fase 2

- WhatsApp.
- Chat.
- Aprovações.
- Catálogo de serviços.
- Relatórios avançados.
- Campos dinâmicos.

### Fase 3

- Telefonia.
- Automações avançadas.
- Sugestão inteligente de respostas.
- Classificação automática.
- Previsão de SLA.
- BI avançado.

## 25. Critérios de Aceite

- Todo canal válido deve gerar ou atualizar ticket.
- Todo ticket deve ter histórico completo.
- Todo SLA deve ser calculado automaticamente.
- Toda ação crítica deve ser auditada.
- Todo cliente deve conseguir acompanhar seus tickets no portal.
- Toda automação deve ser configurável sem alterar código.
- Todo relatório essencial deve ser exportável.

## 26. Regras de Implementação

- O Ticket deve ser a entidade central do domínio.
- Campos customizados devem ser configuráveis por tenant.
- Automações devem ser desacopladas do core de ticket.
- O portal deve consumir a mesma API do backoffice com permissões adequadas.
- O sistema deve tratar canais como adaptadores de entrada e saída.
- Mensagens, anexos e histórico nunca devem ser perdidos em merge ou split.

## 27. Convenções Técnicas

- Nomes de tabelas em inglês, minúsculas e plural.
- Campos de auditoria padrão em todas as tabelas relevantes.
- Soft delete preferencial.
- IDs preferencialmente UUID em camadas expostas.
- Eventos de domínio para integrações assíncronas.
- Separação entre domínio, aplicação e infraestrutura.

## 28. Apêndice - Entidades Resumidas

### 28.1 TicketMessage

- id.
- ticket_id.
- author_type.
- author_id.
- body.
- is_public.
- channel_id.
- created_at.

### 28.2 TicketAttachment

- id.
- ticket_id.
- message_id.
- file_name.
- file_size.
- mime_type.
- storage_path.
- created_at.

### 28.3 SLAPolicy

- id.
- tenant_id.
- name.
- first_response_minutes.
- next_response_minutes.
- resolution_minutes.
- schedule_id.
- priority_rules.

### 28.4 AutomationRule

- id.
- tenant_id.
- name.
- event_type.
- conditions.
- actions.
- is_active.

### 28.5 KnowledgeArticle

- id.
- tenant_id.
- title.
- slug.
- content.
- category_id.
- status.
- version.
- author_id.
- published_at.
