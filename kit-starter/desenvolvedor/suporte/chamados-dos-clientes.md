# Chamados dos clientes (suporte da plataforma)

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Suporte
- Domínio: plataforma (banco master), instância separada do módulo das entidades ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2.1)
- Status: detalhado; especificação da v1 absorvida integralmente (seção 13), com as correções da v2 e as decisões por padrão (seções 1 a 12)
- Fonte da v1: [SPEC-HELPDESK.md](../../../docs/v2/anexo-v1/SPEC-HELPDESK.md) (929 linhas); [spec_chat_rapido_sac.md](../../../docs/v2/anexo-v1/spec_chat_rapido_sac.md) (294 linhas); [SPEC-LAYOUT-TICKET.md](../../../docs/v2/anexo-v1/SPEC-LAYOUT-TICKET.md) (350 linhas)

## 1. Regra de leitura
As seções 1 a 12 prevalecem sobre a seção 13. A seção 13 é o texto integral da v1, sem corte, para que nenhum detalhe se perca. Quando a seção 13 disser algo diferente das seções 1 a 12, vale o que está nas seções 1 a 12.

## 2. Objetivo e escopo
Atender as entidades clientes da plataforma: abertura, triagem, atendimento, escalonamento e encerramento dos chamados, por todos os canais.

## 3. Telas
- **Chamados dos clientes** (kanban): aberto, em atendimento, aguardando cliente, resolvido.
- **Chamado — detalhe** (detalhe): conversa, anexos, SLA, histórico.
- **SLA** (painel): tempo de primeira resposta e de resolução por fila.
**Títulos da v1 (referência, não são telas):**

**SPEC-HELPDESK.md**

- 1. Visão Geral
- 2. Objetivos do Produto
- 3. Escopo
  - 3.1 Incluído
  - 3.2 Excluído no MVP
- 4. Definições
- 5. Requisitos Funcionais
  - 5.1 Multi-tenant
  - 5.2 Gestão de tickets
  - 5.3 Omnichannel
  - 5.4 Portal do cliente
  - 5.5 Base de conhecimento
  - 5.6 Automação
  - 5.7 SLA
  - 5.8 Relatórios
  - 5.9 Auditoria
- 6. Canais de Entrada de Ticket
  - 6.1 Canais obrigatórios
  - 6.2 Regras de normalização
  - 6.3 Regras por canal
- 7. Modelo de Ticket
  - 7.1 Identificação
  - 7.2 Solicitante
  - 7.3 Organização
  - 7.4 Classificação
  - 7.5 Conteúdo
  - 7.6 Estado
  - 7.7 Datas e tempos
  - 7.8 Satisfação
  - 7.9 Metadados
- 8. Campos do Ticket
  - 8.1 Campos padrão obrigatórios
  - 8.2 Campos recomendados
  - 8.3 Campos customizáveis
  - 8.4 Regras para campos customizáveis
- 9. Estados do Ticket
  - 9.1 Regras de transição
- 10. Prioridade, Impacto e Severidade
  - 10.1 Prioridade
  - 10.2 Impacto
  - 10.3 Severidade
  - 10.4 Matriz de cálculo
- 11. Ferramentas do Agente
  - 11.1 Operação
  - 11.2 Produtividade
  - 11.3 Supervisão
- 12. Portal do Cliente
  - 12.1 Funcionalidades
  - 12.2 Regras
- 13. Base de Conhecimento
  - 13.1 Estrutura
  - 13.2 Estados do artigo
  - 13.3 Funcionalidades
- 14. SLA
  - 14.1 Tipos de SLA
  - 14.2 Regras de aplicação
  - 14.3 Estados do SLA
  - 14.4 Ações automáticas
- 15. Automação
  - 15.1 Tipos
  - 15.2 Eventos
  - 15.3 Condições
  - 15.4 Ações
- 16. Aprovações
  - 16.1 Casos de uso
  - 16.2 Campos de aprovação
- 17. Notificações
  - 17.1 Canais
  - 17.2 Eventos notificados
- 18. Relatórios e Indicadores
  - 18.1 Operacionais
  - 18.2 Gerenciais
  - 18.3 Exportação
- 19. API
  - 19.1 Princípios
  - 19.2 Recursos principais
  - 19.3 Operações mínimas em tickets
- 20. Modelo de Banco de Dados
  - 20.1 Entidades principais
  - 20.2 Índices mínimos
- 21. Segurança
- 22. Observabilidade
- 23. Requisitos Não Funcionais
- 24. Roadmap
  - Fase 1 - MVP
  - Fase 2
  - Fase 3
- 25. Critérios de Aceite
- 26. Regras de Implementação
- 27. Convenções Técnicas
- 28. Apêndice - Entidades Resumidas
  - 28.1 TicketMessage
  - 28.2 TicketAttachment
  - 28.3 SLAPolicy
  - 28.4 AutomationRule
  - 28.5 KnowledgeArticle

**spec_chat_rapido_sac.md**

- 1. Visão geral
- 2. Objetivo
- 3. Princípios do produto
- 4. Modelo hierárquico de tenant
  - 4.1 Estrutura
  - 4.2 Regras
- 5. Canais de entrada
  - 5.1 Chat rápido
  - 5.2 E-mail
  - 5.3 WhatsApp
- 6. Experiência do chat rápido
  - 6.1 Botão flutuante
  - 6.2 Tela inicial do chat
  - 6.3 Aba Início
  - 6.4 Aba Mensagens
  - 6.5 Aba Ajuda
- 7. Fluxos funcionais
  - 7.1 Fluxo do chat
  - 7.2 Fluxo de abertura por e-mail
  - 7.3 Fluxo de abertura por WhatsApp
  - 7.4 Fluxo de conversão em ticket
- 8. Regras de negócio
- 9. Entidades principais
  - 9.1 chat_sessions
  - 9.2 chat_messages
  - 9.3 tickets
  - 9.4 ticket_messages
  - 9.5 help_articles
  - 9.6 inbound_channel_configs
- 10. Regras por canal
  - 10.1 Chat web
  - 10.2 E-mail
  - 10.3 WhatsApp
- 11. Interface e UX
- 12. Operação e atendimento
- 13. SLA e priorização
- 14. Segurança e privacidade
- 15. Auditoria e rastreio
- 16. API sugerida
- 17. Eventos de domínio
- 18. Critérios de aceite
- 19. MVP
  - Inclui
  - Não inclui no MVP
- 20. Observações finais

**SPEC-LAYOUT-TICKET.md**

- 1. Objetivo
- 2. Diretrizes de Layout
- 3. Estrutura Geral
  - 3.1 Região 1 - Sidebar
  - 3.2 Região 2 - Topbar
  - 3.3 Região 3 - Conteúdo Principal
- 4. Coluna Esquerda
  - 4.1 Bloco superior
  - 4.2 Bloco intermediário
  - 4.3 Regras visuais
- 5. Painel Central
  - 5.1 Cabeçalho do ticket
  - 5.2 Editor de resposta
  - 5.3 Linha de ações e metadados
  - 5.4 Botões
- 6. Componentes da Interface
  - 6.1 Inputs
  - 6.2 Navegação
  - 6.3 Feedback visual
- 7. Mapeamento de Dados Supabase
  - 7.1 Tabelas principais
  - 7.2 Relações principais
- 8. Regras de RLS
- 9. Interações da Tela
  - 9.1 Abrir ticket
  - 9.2 Alterar solicitante
  - 9.3 Alterar responsável
  - 9.4 Enviar ação pública
  - 9.5 Inserir ação interna
  - 9.6 Aplicar macro
- 10. Comportamento Responsivo
  - 10.1 Desktop
  - 10.2 Tablet
  - 10.3 Mobile
- 11. Estados da Página
- 12. Validações
- 13. Stack Sugerida
- 14. Componentes React Sugeridos
- 15. Estrutura de Pastas
- 16. Tokens Visuais
- 17. Regras de Auditoria
- 18. Critérios de Aceite
- 19. Próximos Entregáveis

## 4. Correções da v2 que prevalecem
- **Modelo único** ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.1; [19](../../../docs/v2/19-regras-modulos-3.md), seção 7): Helpdesk é a base; SAC e chat rápido são canais ou tipos do mesmo registro. As três especificações da v1 da seção 13 descrevem partes desse mesmo módulo.
- **Protocolo** (ATD-01): todo pedido com responsável e prazo recebe número de protocolo; pergunta resolvida pelo bot ou pela base de conhecimento, sem fila, não recebe.
- **Estados e transições** ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.2): `novo`, `aberto`, `em_triagem`, `em_atendimento`, `aguardando_cliente`, `aguardando_terceiro`, `aguardando_aprovacao`, `em_pausa`, `resolvido`, `fechado`, `reaberto`, `escalonado`, `cancelado`. Transição inválida é recusada pela aplicação. Cancelar, escalonar e reabrir gravam motivo.
- **Prioridade, categoria e fila** (seção 2.4): baixa, média, alta e urgente; urgente só em categoria que permita; atribuição automática por fila.
- **Canais** (seção 2.5; [22](../../../docs/v2/22-crm-canais-e-papeis.md), seções 2 e 3): opção "Abrir ticket" sem IA em todo ponto de atendimento (D-18); texto do solicitante guardado literal; campos obrigatórios por tipo e lista fixa de campos padrão.
- **Portal do cliente** (seção 2.6): nota interna nunca aparece para o solicitante; respostas públicas por padrão; avaliação do atendimento.
- **Visibilidade no portal do desenvolvedor** (seção 2.8): chamados das entidades; nenhum dado de aluno sem chamado vinculado ([29](../../../docs/v2/29-auditoria.md), seção 8).
- **Bots** (seção 2.9): categoria sensível (saúde, denúncia, conflito) vai para humano (ATD-05).
- **Perfis da v1:** substituídos pelos papéis da seção 6.

## 5. Decisões por padrão aplicadas
- Nenhuma decisão nova: modelo, estados, SLA e categoria sensível já decididos no [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md) (ATD-01, ATD-02, ATD-05).

## 6. Permissões e papéis
- `platform.operator` (nível 5): atender chamados das entidades; consulta de dado de cliente só com motivo registrado ([78](../../../docs/v2/78-permissoes-e-papeis.md), seção 4.1).
- `platform.manager` (nível 6): redistribuir filas, ver estouros de SLA, aprovar escalonamento.
- `platform.chatbot.operator`: atender as conversas dos canais e transferir.
- Solicitante (usuário da entidade): o próprio chamado.

## 7. Dados
- DDL do atendimento em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 1 (ATD-04, revisão do owner pendente), que prevalece sobre os modelos da v1.

## 8. Integrações
- SLA (ficha [sla.md](sla.md)); base de conhecimento ([base-de-conhecimento.md](base-de-conhecimento.md)).
- Notificações por mudança de estado e por alerta de SLA ([57](../../../docs/v2/57-notificacoes-por-portal.md)).
- CRM da plataforma: conversa de canal que vira oportunidade comercial.

## 9. Exportação, auditoria e privacidade
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Auditoria conforme [29](../../../docs/v2/29-auditoria.md); dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md).
- Retenção de tickets e transcrições: ATD-03 (jurídico), ligado ao L-24 do [22](../../../docs/v2/22-crm-canais-e-papeis.md).

## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
- ATD-03 (retenção) e revisão do DDL (ATD-04), no [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.10.

## 13. Conteúdo integral da v1 (absorvido)

### Fonte: SPEC-HELPDESK.md

#### SPEC-HELPDESK.md

- Language Standard: Global English
##### 1. Visão Geral

Este documento especifica um sistema SaaS multi-tenant de SAC / Help Desk / Service Desk inspirado em plataformas como Movidesk/Zenvia, com foco em centralização de canais, padronização de tickets, automação operacional, SLA, base de conhecimento, portal do cliente, relatórios e integrações. O sistema deve permitir atendimento omnichannel com rastreabilidade total, auditoria completa e flexibilidade para múltiplas empresas, unidades, equipes e perfis de acesso [web:32][web:11][web:51].

O objetivo é servir como especificação funcional e técnica base para desenvolvimento incremental, começando por um MVP sólido e evoluindo para automação avançada, múltiplos canais e recursos inteligentes de atendimento [web:32][web:7][web:54].

##### 2. Objetivos do Produto

- Centralizar todos os canais de contato em uma única operação.
- Normalizar qualquer solicitação em um Ticket.
- Reduzir tempo de resposta e tempo de resolução.
- Garantir rastreabilidade e auditoria de ponta a ponta.
- Disponibilizar autoatendimento via portal e base de conhecimento.
- Automatizar triagem, roteamento, escalonamento e notificações.
- Suportar múltiplos tenants, unidades e equipes com segurança.
- Oferecer indicadores operacionais e gerenciais em tempo real.

##### 3. Escopo

###### 3.1 Incluído

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

###### 3.2 Excluído no MVP

- Telefonia nativa com discador avançado.
- Inteligência artificial generativa para respostas automáticas.
- RPA para processos externos.
- Marketplace de extensões.
- BI avançado com cubos multidimensionais.

##### 4. Definições

- **Tenant**: empresa cliente isolada logicamente dentro da plataforma.
- **Unidade**: subestrutura organizacional do tenant.
- **Fila**: agrupamento operacional de tickets.
- **Ticket**: unidade central de atendimento.
- **Solicitante**: pessoa que abre ou possui o ticket.
- **Contato**: pessoa relacionada ao ticket, podendo ser solicitante ou observador.
- **Agente**: usuário interno que atende tickets.
- **SLA**: compromisso de tempo de resposta e resolução.
- **Base de conhecimento**: artigos e conteúdos de autoatendimento.

##### 5. Requisitos Funcionais

###### 5.1 Multi-tenant

O sistema deve isolar dados por tenant em todos os níveis, incluindo tickets, usuários, canais, artigos, automações, relatórios e configurações. Um usuário autenticado só pode acessar dados autorizados pelo seu escopo de tenant, unidade, fila e permissão.

###### 5.2 Gestão de tickets

O sistema deve permitir criação, leitura, atualização, vinculação, merge, split, reabertura, cancelamento, encerramento e exclusão lógica de tickets. Cada ticket deve manter histórico completo de campos, mensagens, status, responsáveis e SLAs.

###### 5.3 Omnichannel

O sistema deve receber interações por múltiplos canais, normalizar a entrada e associá-la ao mesmo ticket ou criar um novo conforme regra de negócio. Todos os canais precisam preservar autoria, timestamp, anexos e origem.

###### 5.4 Portal do cliente

O portal deve permitir abertura e acompanhamento de tickets, respostas públicas, envio de anexos, consulta a artigos da base e avaliação do atendimento.

###### 5.5 Base de conhecimento

O sistema deve permitir criação, revisão, publicação, versionamento, busca e categorização de artigos. O conteúdo pode ser público, restrito ou interno.

###### 5.6 Automação

O sistema deve suportar regras automáticas acionadas por eventos ou agendamentos, com condições, ações, exceções e logs.

###### 5.7 SLA

O sistema deve calcular prazos de primeira resposta, próxima resposta e resolução, com base em regras por tenant, cliente, fila, prioridade, categoria e horário útil.

###### 5.8 Relatórios

O sistema deve oferecer dashboards operacionais e relatórios exportáveis com métricas de volume, tempo, backlog, produtividade, SLA e satisfação.

###### 5.9 Auditoria

Todas as ações críticas devem gerar eventos auditáveis com usuário, data, contexto, origem e alteração realizada.

##### 6. Canais de Entrada de Ticket

###### 6.1 Canais obrigatórios

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

###### 6.2 Regras de normalização

- Toda entrada deve gerar evento de origem.
- Toda mensagem deve ser associada a um ticket novo ou existente.
- O sistema deve identificar o solicitante por e-mail, telefone, ID externo ou autenticação.
- O canal de origem deve ser preservado em toda a vida do ticket.
- Anexos devem ser vinculados ao ticket e à mensagem de origem.

###### 6.3 Regras por canal

####### E-mail

- O sistema deve monitorar caixas de entrada configuradas.
- Assuntos e cabeçalhos devem ser preservados.
- Respostas devem manter thread.
- O sistema deve evitar duplicidade por heurística configurável.

####### WhatsApp

- Mensagens devem entrar como tickets ou mensagens vinculadas a tickets ativos.
- O sistema deve registrar número, nome exibido, mensagem e anexos.
- Respostas devem ser enviadas pela mesma sessão/canal.

####### Chat web

- O sistema deve abrir sessão de chat e, quando necessário, converter a conversa em ticket.
- O histórico do chat deve ser anexado ao ticket.

####### Formulário web

- O formulário deve ser configurável por tenant, categoria e fila.
- Campos obrigatórios devem variar por tipo de solicitação.

####### API

- A API deve aceitar payload autenticado e validado.
- O sistema deve suportar criação, atualização e consulta.

####### Webhook

- Integrações externas devem poder criar ou atualizar tickets por evento.

####### Criação interna

- Agentes devem poder abrir tickets para clientes, departamentos ou terceiros.

##### 7. Modelo de Ticket

###### 7.1 Identificação

- id.
- tenant_id.
- external_id.
- number.
- root_ticket_id.
- parent_ticket_id.
- merged_into_ticket_id.
- source_type.
- channel_id.

###### 7.2 Solicitante

- requester_id.
- requester_name.
- requester_email.
- requester_phone.
- requester_document.
- requester_company.
- requester_department.
- requester_role.
- requester_locale.

###### 7.3 Organização

- company_id.
- unit_id.
- department_id.
- queue_id.
- team_id.
- owner_user_id.
- owner_team_id.
- assigned_by.
- assigned_at.

###### 7.4 Classificação

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

###### 7.5 Conteúdo

- subject.
- description.
- public_description.
- internal_summary.
- resolution_summary.
- customer_expectation.
- initial_contact_channel.
- customer_language.

###### 7.6 Estado

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

###### 7.7 Datas e tempos

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

###### 7.8 Satisfação

- satisfaction_score.
- satisfaction_comment.
- satisfaction_answered_at.
- csat_sent_at.
- csat_status.

###### 7.9 Metadados

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

##### 8. Campos do Ticket

###### 8.1 Campos padrão obrigatórios

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

###### 8.2 Campos recomendados

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

###### 8.3 Campos customizáveis

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

###### 8.4 Regras para campos customizáveis

- Devem ser configuráveis por tenant.
- Devem ser condicionais por categoria, fila, tipo ou canal.
- Devem suportar obrigatoriedade dinâmica.
- Devem ter validação de formato.
- Devem ser auditáveis quando alterados.

##### 9. Estados do Ticket

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

###### 9.1 Regras de transição

- Novo só pode ir para aberto, triagem ou cancelado.
- Resolvido pode ir para fechado ou reaberto.
- Aguardando cliente pausa contagem de trabalho conforme regra de SLA.
- Ticket fechado pode ser reaberto por janela configurável.

##### 10. Prioridade, Impacto e Severidade

###### 10.1 Prioridade

- Baixa.
- Média.
- Alta.
- Crítica.
- Urgente.

###### 10.2 Impacto

- Individual.
- Setorial.
- Unidade.
- Empresa inteira.
- Múltiplos tenants em casos de fornecedor compartilhado.

###### 10.3 Severidade

- S1 - Crítica.
- S2 - Alta.
- S3 - Média.
- S4 - Baixa.

###### 10.4 Matriz de cálculo

A prioridade pode ser determinada por combinação de impacto e urgência, com overrides manuais permitidos por perfil autorizado.

##### 11. Ferramentas do Agente

###### 11.1 Operação

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

###### 11.2 Produtividade

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

###### 11.3 Supervisão

- Monitoramento de fila.
- Monitoramento de SLA.
- Visão de backlog.
- Reatribuição assistida.
- Escalonamento manual.
- Auditoria de operações.
- Dashboards por equipe e agente.

##### 12. Portal do Cliente

###### 12.1 Funcionalidades

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

###### 12.2 Regras

- O cliente só pode acessar seus próprios tickets e os tickets compartilhados com ele.
- Respostas no portal devem ser públicas por padrão.
- Campos do formulário podem variar por tenant, serviço ou fila.
- Artigos relevantes podem ser sugeridos antes da abertura do ticket.

##### 13. Base de Conhecimento

###### 13.1 Estrutura

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

###### 13.2 Estados do artigo

- Rascunho.
- Em revisão.
- Agendado.
- Publicado.
- Arquivado.
- Restrito.

###### 13.3 Funcionalidades

- Busca textual.
- Filtros por categoria.
- Artigos relacionados.
- FAQ.
- Feedback de utilidade.
- Histórico de versão.
- Controle de permissão.
- Sugestão automática no portal e no atendimento.

##### 14. SLA

###### 14.1 Tipos de SLA

- Primeira resposta.
- Próxima resposta.
- Resolução.
- Fechamento.

###### 14.2 Regras de aplicação

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

###### 14.3 Estados do SLA

- Ativo.
- Em risco.
- Violado.
- Pausado.
- Reiniciado.

###### 14.4 Ações automáticas

- Notificar agente.
- Notificar supervisor.
- Reatribuir ticket.
- Escalonar fila.
- Criar alerta.
- Marcar como violado.
- Registrar evento.

##### 15. Automação

###### 15.1 Tipos

- Gatilho por evento.
- Regra condicional.
- Workflow multi-etapa.
- Agendamento.
- Webhook.
- Ação manual.

###### 15.2 Eventos

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

###### 15.3 Condições

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

###### 15.4 Ações

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

##### 16. Aprovações

###### 16.1 Casos de uso

- Solicitação de acesso.
- Solicitação de mudança.
- Solicitação financeira.
- Solicitação administrativa.
- Solicitação de exceção.
- Compra e contratação.

###### 16.2 Campos de aprovação

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

##### 17. Notificações

###### 17.1 Canais

- E-mail.
- WhatsApp.
- In-app.
- Push.
- Webhook.

###### 17.2 Eventos notificados

- Ticket criado.
- Ticket atribuído.
- Resposta recebida.
- SLA em risco.
- SLA violado.
- Aprovação pendente.
- Aprovação concluída.
- Ticket resolvido.
- Ticket fechado.

##### 18. Relatórios e Indicadores

###### 18.1 Operacionais

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

###### 18.2 Gerenciais

- CSAT.
- NPS.
- Volume por período.
- Tendência de atendimento.
- Produtividade individual.
- Produtividade da equipe.
- Motivos mais recorrentes.
- Causas de atraso.

###### 18.3 Exportação

- CSV.
- XLSX.
- PDF.
- JSON.

##### 19. API

###### 19.1 Princípios

- RESTful.
- Autenticada.
- Versionada.
- Documentada com OpenAPI.
- Rate limited.
- Auditável.

###### 19.2 Recursos principais

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

###### 19.3 Operações mínimas em tickets

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

##### 20. Modelo de Banco de Dados

###### 20.1 Entidades principais

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

###### 20.2 Índices mínimos

- tenant_id em todas as tabelas multi-tenant.
- requester_id, owner_user_id, queue_id, status e priority em tickets.
- created_at e updated_at em tabelas transacionais.
- full-text em subject, description e article content.

##### 21. Segurança

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

##### 22. Observabilidade

- Logs estruturados.
- Métricas de sistema.
- Tracing de requisições.
- Alertas de fila e SLA.
- Monitoramento de integrações.
- Health checks.
- Métricas de erro por canal.

##### 23. Requisitos Não Funcionais

- Alta disponibilidade.
- Escalabilidade horizontal.
- Baixa latência no atendimento.
- Processamento assíncrono para integrações e notificações.
- Backup automatizado.
- Restore testado.
- Governança de retenção.
- Compatibilidade com LGPD.
- Suporte a múltiplos idiomas no futuro.

##### 24. Roadmap

###### Fase 1 - MVP

- Tickets.
- Portal.
- E-mail.
- Base de conhecimento.
- SLA básico.
- Automação simples.
- Relatórios básicos.

###### Fase 2

- WhatsApp.
- Chat.
- Aprovações.
- Catálogo de serviços.
- Relatórios avançados.
- Campos dinâmicos.

###### Fase 3

- Telefonia.
- Automações avançadas.
- Sugestão inteligente de respostas.
- Classificação automática.
- Previsão de SLA.
- BI avançado.

##### 25. Critérios de Aceite

- Todo canal válido deve gerar ou atualizar ticket.
- Todo ticket deve ter histórico completo.
- Todo SLA deve ser calculado automaticamente.
- Toda ação crítica deve ser auditada.
- Todo cliente deve conseguir acompanhar seus tickets no portal.
- Toda automação deve ser configurável sem alterar código.
- Todo relatório essencial deve ser exportável.

##### 26. Regras de Implementação

- O Ticket deve ser a entidade central do domínio.
- Campos customizados devem ser configuráveis por tenant.
- Automações devem ser desacopladas do core de ticket.
- O portal deve consumir a mesma API do backoffice com permissões adequadas.
- O sistema deve tratar canais como adaptadores de entrada e saída.
- Mensagens, anexos e histórico nunca devem ser perdidos em merge ou split.

##### 27. Convenções Técnicas

- Nomes de tabelas em inglês, minúsculas e plural.
- Campos de auditoria padrão em todas as tabelas relevantes.
- Soft delete preferencial.
- IDs preferencialmente UUID em camadas expostas.
- Eventos de domínio para integrações assíncronas.
- Separação entre domínio, aplicação e infraestrutura.

##### 28. Apêndice - Entidades Resumidas

###### 28.1 TicketMessage

- id.
- ticket_id.
- author_type.
- author_id.
- body.
- is_public.
- channel_id.
- created_at.

###### 28.2 TicketAttachment

- id.
- ticket_id.
- message_id.
- file_name.
- file_size.
- mime_type.
- storage_path.
- created_at.

###### 28.3 SLAPolicy

- id.
- tenant_id.
- name.
- first_response_minutes.
- next_response_minutes.
- resolution_minutes.
- schedule_id.
- priority_rules.

###### 28.4 AutomationRule

- id.
- tenant_id.
- name.
- event_type.
- conditions.
- actions.
- is_active.

###### 28.5 KnowledgeArticle

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

### Fonte: spec_chat_rapido_sac.md

#### SPEC — Chat Rápido e Abertura de Ticket no SAC Multitenant

- Language Standard: Global English
##### 1. Visão geral
Este documento descreve o módulo de chat rápido do SAC, pensado como um canal de entrada leve para o usuário abrir demandas com poucos cliques. O chat deve funcionar no mesmo ecossistema multitenant do help desk, com suporte a tenant raiz, tenants clientes e subtenants, mantendo isolamento, herança de configuração e trilha de auditoria.

##### 2. Objetivo
Permitir que qualquer usuário autorizado consiga:
- iniciar atendimento por um chat flutuante no sistema;
- abrir demanda por e-mail;
- abrir demanda por WhatsApp;
- acompanhar conversas e tickets;
- converter conversas em tickets sem perder histórico, anexos ou contexto.

##### 3. Princípios do produto
- O ticket continua sendo a entidade central.
- O chat é um canal rápido de captura de demanda.
- E-mail e WhatsApp são canais de entrada equivalentes ao chat.
- Cada tenant pode operar como prestador de suporte para seus próprios clientes.
- A mesma estrutura deve servir para a plataforma, seus clientes e os clientes dos clientes.

##### 4. Modelo hierárquico de tenant
###### 4.1 Estrutura
- Tenant raiz: empresa dona da plataforma.
- Tenant cliente: empresa contratante da plataforma.
- Subtenant: cliente do tenant cliente, quando aplicável.

###### 4.2 Regras
- Todo registro relevante deve carregar `tenant_id`.
- A hierarquia deve permitir `parent_tenant_id` para herança e segmentação.
- O tenant filho pode herdar marca, categorias, SLAs, filas, artigos e fluxos do tenant pai.
- O isolamento de dados deve ser mantido em todas as camadas.

##### 5. Canais de entrada
###### 5.1 Chat rápido
O sistema deve exibir um botão flutuante fixo no canto inferior direito, visível nas telas autorizadas. Ao clicar, o usuário abre o painel do chat com saudação, atalhos de ajuda, histórico de mensagens e ação para enviar nova mensagem.

###### 5.2 E-mail
O cliente deve poder abrir demanda por e-mail. Mensagens recebidas devem ser ingeridas automaticamente, vinculadas a uma sessão ou ticket e com resposta possível no mesmo thread. O sistema deve identificar remetente, assunto, corpo, anexos e mensagem original.

###### 5.3 WhatsApp
O cliente deve poder abrir demanda por WhatsApp. Conversas recebidas devem gerar sessão de atendimento e, quando necessário, converter-se em ticket com o histórico completo anexado. O canal precisa preservar número, autoria, tempo e anexos.

##### 6. Experiência do chat rápido
###### 6.1 Botão flutuante
- Ícone circular fixo no canto inferior direito.
- Abertura do widget com animação leve.
- Não pode bloquear ações críticas do sistema.
- Deve funcionar em desktop e mobile.

###### 6.2 Tela inicial do chat
- Saudação personalizada com o nome do usuário.
- Texto explicativo curto sobre como o sistema ajuda.
- Card de ação principal para “Envie uma mensagem”.
- Campo de busca de ajuda.
- Navegação inferior com Início, Mensagens e Ajuda.

###### 6.3 Aba Início
- Mostrar saudação e contexto do usuário.
- Exibir atalho para iniciar conversa.
- Exibir sugestões de temas mais comuns.
- Exibir tempo estimado de resposta, quando configurado.

###### 6.4 Aba Mensagens
- Listar conversas anteriores.
- Mostrar autor, prévia, data relativa e status.
- Permitir abrir conversa existente.
- Permitir iniciar nova conversa.

###### 6.5 Aba Ajuda
- Exibir busca de artigos.
- Exibir coleções e categorias.
- Permitir navegação por área funcional.
- Permitir sugerir artigo antes de abrir ticket.

##### 7. Fluxos funcionais
###### 7.1 Fluxo do chat
1. Usuário clica no botão flutuante.
2. Widget abre com saudação e atalhos.
3. Usuário envia mensagem.
4. O sistema cria ou reutiliza uma sessão de chat.
5. A conversa pode ser resolvida ali mesmo ou convertida em ticket.

###### 7.2 Fluxo de abertura por e-mail
1. Usuário envia e-mail para o endereço do SAC.
2. O sistema recebe e identifica o tenant correto.
3. Uma conversa ou ticket é criado automaticamente.
4. Respostas posteriores são associadas à mesma thread.
5. O usuário recebe retorno no e-mail original.

###### 7.3 Fluxo de abertura por WhatsApp
1. Usuário envia mensagem pelo número oficial.
2. O sistema cria sessão de atendimento.
3. O agente ou regra automática pode converter a conversa em ticket.
4. O histórico é preservado e vinculado ao ticket.
5. O usuário continua sendo atendido pelo mesmo canal.

###### 7.4 Fluxo de conversão em ticket
1. Atendimento inicia em chat, e-mail ou WhatsApp.
2. Se a demanda exigir acompanhamento formal, o sistema gera ticket.
3. O ticket herda histórico, anexos, categoria sugerida e canal de origem.
4. O ticket é encaminhado para fila, unidade ou departamento adequado.

##### 8. Regras de negócio
- Um usuário autenticado deve ser identificado automaticamente sempre que possível.
- Se o usuário não estiver autenticado, o sistema deve permitir abertura assistida com e-mail ou telefone.
- Não deve haver duplicidade de ticket aberto para a mesma demanda, salvo regra explícita.
- A categoria do ticket pode ser sugerida por artigo acessado, palavras-chave, fila, unidade ou seleção manual.
- O sistema deve permitir que tenant filho crie e administre sua própria operação de suporte.
- Um tenant filho deve conseguir atender os próprios clientes com a mesma estrutura de chat, e-mail e WhatsApp.

##### 9. Entidades principais
###### 9.1 chat_sessions
- id
- tenant_id
- parent_tenant_id
- user_id
- customer_id
- channel_id
- status
- subject
- last_message_at
- created_at
- updated_at

###### 9.2 chat_messages
- id
- session_id
- tenant_id
- sender_type
- sender_id
- body
- attachments
- is_internal
- created_at

###### 9.3 tickets
- id
- tenant_id
- parent_tenant_id
- requester_id
- requester_name
- requester_email
- requester_phone
- channel_id
- queue_id
- category_id
- priority_id
- status
- subject
- description
- created_at
- updated_at

###### 9.4 ticket_messages
- id
- ticket_id
- tenant_id
- sender_type
- sender_id
- body
- attachments
- is_public
- created_at

###### 9.5 help_articles
- id
- tenant_id
- visibility
- title
- content
- category_id
- tags
- created_at
- updated_at

###### 9.6 inbound_channel_configs
- id
- tenant_id
- type
- address_or_number
- status
- routing_rules
- created_at
- updated_at

##### 10. Regras por canal
###### 10.1 Chat web
- Deve existir widget embutido com abertura rápida.
- Deve permitir resposta em tempo real ou assíncrona.
- Deve converter para ticket quando houver necessidade de formalização ou quando o agente assumir.

###### 10.2 E-mail
- Deve suportar captura de mensagens recebidas.
- Deve manter thread por Message-ID, References ou regra equivalente.
- Deve anexar arquivos ao ticket e preservar mensagem original.

###### 10.3 WhatsApp
- Deve suportar ingestão de mensagens via integração oficial.
- Deve preservar número de origem, mensagens e anexos.
- Deve permitir escalonamento da conversa para ticket.

##### 11. Interface e UX
- O chat deve seguir a identidade visual do tenant.
- O cabeçalho deve exibir nome da marca e estado do atendimento.
- A área de mensagens deve ser rolável.
- O campo de composição deve ficar fixo na base do widget.
- A navegação inferior deve permanecer fixa dentro do componente.
- Os atalhos devem ser configuráveis por tenant.

##### 12. Operação e atendimento
- O chat pode iniciar com bot, triagem humana ou fila híbrida.
- A mensagem deve entrar na sessão adequada antes de virar ticket.
- O agente pode assumir a conversa e converter em ticket manualmente ou por regra.
- A conversa deve manter contexto ao trocar de canal.
- O ticket deve carregar histórico consolidado de todos os canais usados.

##### 13. SLA e priorização
- O ticket derivado do chat, e-mail ou WhatsApp deve herdar SLA aplicável.
- A prioridade pode ser inferida por palavras-chave, fila ou categoria.
- O sistema deve suportar primeira resposta, próxima resposta e resolução.
- O tempo em espera do cliente deve ser contabilizado conforme política do tenant.

##### 14. Segurança e privacidade
- O acesso deve respeitar RBAC por tenant, unidade, fila e departamento.
- O conteúdo das mensagens deve ser sanitizado.
- Anexos devem ter validação de tipo e tamanho.
- Logs de auditoria devem registrar abertura, leitura, resposta, conversão e fechamento.
- Dados sensíveis devem seguir a política de retenção e LGPD.

##### 15. Auditoria e rastreio
- Toda entrada por chat, e-mail ou WhatsApp deve gerar evento de auditoria.
- Toda conversão de conversa para ticket deve ser auditável.
- Toda troca de status, atribuição e encerramento deve ficar registrada.
- O histórico deve ser recuperável por ticket e por sessão.

##### 16. API sugerida
- `POST /chat/sessions`
- `GET /chat/sessions`
- `POST /chat/sessions/{id}/messages`
- `POST /tickets`
- `POST /tickets/from-session/{sessionId}`
- `GET /tickets/{id}`
- `POST /inbound/email/webhook`
- `POST /inbound/whatsapp/webhook`
- `GET /knowledge/articles`
- `GET /knowledge/articles/{id}`

##### 17. Eventos de domínio
- `chat.session_opened`
- `chat.message_received`
- `chat.message_sent`
- `chat.session_converted_to_ticket`
- `ticket.created`
- `ticket.assigned`
- `ticket.status_changed`
- `ticket.closed`
- `inbound.email_received`
- `inbound.whatsapp_received`

##### 18. Critérios de aceite
- O usuário consegue abrir o chat rápido pelo botão flutuante.
- O usuário consegue iniciar demanda pela interface do chat.
- O cliente consegue abrir ticket por e-mail.
- O cliente consegue abrir ticket por WhatsApp.
- O sistema preserva histórico, anexos e origem em todos os canais.
- O mesmo modelo funciona para tenant raiz, tenant cliente e subtenant.
- O ticket é criado ou associado sem perda de contexto.

##### 19. MVP
###### Inclui
- Botão flutuante de chat.
- Tela com Início, Mensagens e Ajuda.
- Envio de mensagem no chat.
- Conversão de chat em ticket.
- Ingestão de e-mail.
- Ingestão de WhatsApp.
- Base de conhecimento básica.
- Auditoria de eventos principais.

###### Não inclui no MVP
- IA generativa avançada.
- BI preditivo.
- RPA.
- Discador telefônico.
- Marketplace de extensões.
- Automação complexa multietapa.

##### 20. Observações finais
- O módulo deve ser pensado como um canal plugável dentro do SAC.
- A mesma estrutura deve ser reaproveitada em todos os níveis da hierarquia do SaaS.
- O chat rápido é apenas a interface; o domínio continua sendo ticket, sessão e auditoria.
- A implementação deve nascer preparada para expansão omnichannel.


### Fonte: SPEC-LAYOUT-TICKET.md

#### SPEC-LAYOUT-TICKET.md

##### 1. Objetivo

Este documento define a implementação da tela de detalhe de ticket inspirada no layout Movidesk da imagem de referência, usando Supabase como backend, autenticação, banco de dados, storage e controle de acesso. O objetivo é reproduzir a mesma densidade visual, organização dos campos e hierarquia de ações mostradas na interface [file:62].

##### 2. Diretrizes de Layout

- Interface desktop-first.
- Sidebar fixa à esquerda.
- Topbar fixa no topo.
- Área principal dividida em coluna lateral de formulário e painel central de atendimento.
- Visual administrativo limpo, com fundo branco, bordas cinza claras e acento azul.
- Espaçamento compacto, típico de sistema de help desk profissional.

##### 3. Estrutura Geral

###### 3.1 Região 1 - Sidebar

- Largura fixa: 64px.
- Fundo: azul-acinzentado escuro.
- Ícones centralizados verticalmente.
- Estado ativo com contraste visual sutil.
- Conteúdo: navegação principal do sistema.

###### 3.2 Região 2 - Topbar

- Altura fixa: 48px.
- Fundo branco.
- Linha inferior azul fina.
- À esquerda: identificação do ticket.
- À direita: ícones de busca, relógio, notificação, telefone, chat e avatar.
- Canto superior direito: menu de opções e status do ticket.

###### 3.3 Região 3 - Conteúdo Principal

- Coluna esquerda: 340px aproximadamente.
- Painel central: restante da largura.
- O conteúdo deve ter rolagem vertical independente.

##### 4. Coluna Esquerda

###### 4.1 Bloco superior

- Tabs: Público e Interno.
- Link rápido: Colocar-me como solicitante.
- Campo: Solicitante.
- Campo: Serviço.
- Campo: Categoria.
- Campo: Urgência.
- Seção Ativos com radio buttons: Solicitante, Organização, Todos.

###### 4.2 Bloco intermediário

- Campo: Previsão de solução.
- Campo: Responsável.
- Link rápido: Atribuir para mim.
- Campo: Tags.
- Campo: CC.

###### 4.3 Regras visuais

- Labels acima dos inputs.
- Inputs com altura compacta.
- Bordas finas cinza claras.
- Largura total da coluna.
- Espaçamento vertical consistente.

##### 5. Painel Central

###### 5.1 Cabeçalho do ticket

- Campo largo: Assunto.
- Deve ocupar praticamente toda a largura útil do painel central.
- Posicionado imediatamente abaixo da topbar.

###### 5.2 Editor de resposta

- Tabs: Ação pública e Ação interna.
- Ação pública ativa por padrão.
- Área de texto grande logo abaixo das tabs.
- Deve aceitar rich text futuramente.
- Deve suportar anexos, menções e macros.

###### 5.3 Linha de ações e metadados

Campos na mesma linha:

- Data.
- Início.
- Fim.
- Tempo.
- Tipo.
- Tempo contabilizado.
- Atividade.
- Valor.
- Opções.

###### 5.4 Botões

- Botão secundário: Aplicar macro.
- Botão de destaque: Nova ação.
- Botão final: Salvar.
- Menu Opções no canto direito da linha de status.

##### 6. Componentes da Interface

###### 6.1 Inputs

- Text input.
- Select com busca.
- Date picker.
- Time picker.
- Radio group.
- Textarea.
- Rich text editor.
- File uploader.

###### 6.2 Navegação

- Sidebar icons.
- Tabs da esquerda.
- Tabs do editor.
- Menu de opções.

###### 6.3 Feedback visual

- Badges de status.
- Hover sutil nos botões.
- Foco visível nos campos.
- Estado ativo em tabs e ícones.

##### 7. Mapeamento de Dados Supabase

###### 7.1 Tabelas principais

- tenants.
- users.
- user_profiles.
- customers.
- contacts.
- companies.
- units.
- departments.
- services.
- categories.
- queues.
- tickets.
- ticket_messages.
- ticket_activities.
- ticket_attachments.
- ticket_tags.
- sla_policies.
- macros.
- audit_logs.
- notifications.

###### 7.2 Relações principais

- tickets.requester_id -> contacts.id.
- tickets.owner_user_id -> users.id.
- tickets.queue_id -> queues.id.
- tickets.category_id -> categories.id.
- tickets.service_id -> services.id.
- ticket_messages.ticket_id -> tickets.id.
- ticket_attachments.ticket_id -> tickets.id.
- ticket_tags.ticket_id -> tickets.id.

##### 8. Regras de RLS

- Um usuário só acessa tickets do seu tenant.
- Cliente só acessa tickets próprios ou compartilhados.
- Agente só acessa filas autorizadas.
- Supervisores podem acessar tickets da unidade ou equipe sob responsabilidade.
- Todas as tabelas sensíveis devem ter RLS habilitado.

##### 9. Interações da Tela

###### 9.1 Abrir ticket

- Carregar ticket por id.
- Preencher colunas esquerda e central.
- Buscar mensagens, anexos e histórico.

###### 9.2 Alterar solicitante

- Atualizar requester_id.
- Recalcular contexto do ticket.
- Registrar no audit log.

###### 9.3 Alterar responsável

- Atualizar owner_user_id.
- Registrar timestamp da atribuição.
- Atualizar SLA se necessário.

###### 9.4 Enviar ação pública

- Inserir mensagem pública na timeline.
- Notificar solicitante.
- Registrar evento.

###### 9.5 Inserir ação interna

- Inserir nota interna apenas para agentes.
- Não notificar cliente.
- Registrar autor e data.

###### 9.6 Aplicar macro

- Mostrar modal de seleção.
- Aplicar texto, tags, status e ações associadas.

##### 10. Comportamento Responsivo

###### 10.1 Desktop

- Layout completo conforme referência.

###### 10.2 Tablet

- Sidebar colapsável.
- Coluna esquerda retrátil.
- Painel central priorizado.

###### 10.3 Mobile

- Sidebar em drawer.
- Coluna esquerda vira seção expansível.
- Editor e metadados empilhados verticalmente.

##### 11. Estados da Página

- Carregando.
- Ticket encontrado.
- Ticket não encontrado.
- Sem permissão.
- Erro de rede.
- Salvando.
- Salvo com sucesso.
- Alteração pendente.

##### 12. Validações

- Assunto obrigatório.
- Solicitante obrigatório em ticket novo.
- Serviço obrigatório quando a fila exigir.
- Responsável obrigatório em status de atendimento, quando configurado.
- Mensagem pública não pode ser enviada vazia.
- Arquivos devem respeitar limite de tamanho e tipo.

##### 13. Stack Sugerida

- Frontend: Next.js ou React.
- Estilo: Tailwind CSS.
- UI kit: componentes próprios ou shadcn/ui adaptado.
- Backend: Supabase.
- Auth: Supabase Auth.
- Banco: PostgreSQL do Supabase.
- Storage: Supabase Storage.
- Realtime: Supabase Realtime.

##### 14. Componentes React Sugeridos

- TicketLayout.
- SidebarNav.
- TopBar.
- TicketHeader.
- TicketField.
- TicketTabs.
- PublicActionEditor.
- InternalActionEditor.
- MetadataRow.
- TicketMacroPicker.
- TicketStatusBadge.
- TicketAssigneePicker.
- TicketServicePicker.
- TicketCategoryPicker.
- TicketAttachments.
- TicketTimeline.

##### 15. Estrutura de Pastas

```txt
app/
  tickets/
    [id]/
      page.tsx
components/
  ticket/
    SidebarNav.tsx
    TopBar.tsx
    TicketHeader.tsx
    TicketFields.tsx
    TicketEditor.tsx
    TicketMetaRow.tsx
    TicketActions.tsx
lib/
  supabase/
  auth/
  tickets/
  permissions/
  validations/
```

##### 16. Tokens Visuais

- primary: #2F6FED
- sidebar: #3C4A57
- background: #F6F7FA
- surface: #FFFFFF
- border: #D9DEE6
- text: #2C2C2C
- text-muted: #6B7280
- success: #22C55E
- warning: #F59E0B
- danger: #EF4444

##### 17. Regras de Auditoria

Registrar em audit_logs:

- criação do ticket.
- alteração de campo.
- troca de responsável.
- envio de mensagem.
- alteração de status.
- aplicação de macro.
- anexos adicionados.
- ações internas.
- fechamento.
- reabertura.

##### 18. Critérios de Aceite

- A tela deve reproduzir fielmente a composição visual da referência.
- A hierarquia visual deve permitir leitura rápida e operação eficiente.
- O layout deve funcionar em desktop sem quebra de alinhamento.
- O ticket deve carregar e salvar dados via Supabase.
- Os campos devem ser consistentes com o modelo de dados do help desk.
- Todas as ações relevantes devem ser auditadas.

##### 19. Próximos Entregáveis

- Wireframe detalhado por bloco.
- Schema SQL do Supabase.
- RLS policies.
- Componentes React base.
- Contrato de API para o ticket.
- Lista de validações front-end e back-end.
