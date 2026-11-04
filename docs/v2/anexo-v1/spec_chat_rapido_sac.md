# SPEC — Chat Rápido e Abertura de Ticket no SAC Multitenant

- Language Standard: Global English
## 1. Visão geral
Este documento descreve o módulo de chat rápido do SAC, pensado como um canal de entrada leve para o usuário abrir demandas com poucos cliques. O chat deve funcionar no mesmo ecossistema multitenant do help desk, com suporte a tenant raiz, tenants clientes e subtenants, mantendo isolamento, herança de configuração e trilha de auditoria.

## 2. Objetivo
Permitir que qualquer usuário autorizado consiga:
- iniciar atendimento por um chat flutuante no sistema;
- abrir demanda por e-mail;
- abrir demanda por WhatsApp;
- acompanhar conversas e tickets;
- converter conversas em tickets sem perder histórico, anexos ou contexto.

## 3. Princípios do produto
- O ticket continua sendo a entidade central.
- O chat é um canal rápido de captura de demanda.
- E-mail e WhatsApp são canais de entrada equivalentes ao chat.
- Cada tenant pode operar como prestador de suporte para seus próprios clientes.
- A mesma estrutura deve servir para a plataforma, seus clientes e os clientes dos clientes.

## 4. Modelo hierárquico de tenant
### 4.1 Estrutura
- Tenant raiz: empresa dona da plataforma.
- Tenant cliente: empresa contratante da plataforma.
- Subtenant: cliente do tenant cliente, quando aplicável.

### 4.2 Regras
- Todo registro relevante deve carregar `tenant_id`.
- A hierarquia deve permitir `parent_tenant_id` para herança e segmentação.
- O tenant filho pode herdar marca, categorias, SLAs, filas, artigos e fluxos do tenant pai.
- O isolamento de dados deve ser mantido em todas as camadas.

## 5. Canais de entrada
### 5.1 Chat rápido
O sistema deve exibir um botão flutuante fixo no canto inferior direito, visível nas telas autorizadas. Ao clicar, o usuário abre o painel do chat com saudação, atalhos de ajuda, histórico de mensagens e ação para enviar nova mensagem.

### 5.2 E-mail
O cliente deve poder abrir demanda por e-mail. Mensagens recebidas devem ser ingeridas automaticamente, vinculadas a uma sessão ou ticket e com resposta possível no mesmo thread. O sistema deve identificar remetente, assunto, corpo, anexos e mensagem original.

### 5.3 WhatsApp
O cliente deve poder abrir demanda por WhatsApp. Conversas recebidas devem gerar sessão de atendimento e, quando necessário, converter-se em ticket com o histórico completo anexado. O canal precisa preservar número, autoria, tempo e anexos.

## 6. Experiência do chat rápido
### 6.1 Botão flutuante
- Ícone circular fixo no canto inferior direito.
- Abertura do widget com animação leve.
- Não pode bloquear ações críticas do sistema.
- Deve funcionar em desktop e mobile.

### 6.2 Tela inicial do chat
- Saudação personalizada com o nome do usuário.
- Texto explicativo curto sobre como o sistema ajuda.
- Card de ação principal para “Envie uma mensagem”.
- Campo de busca de ajuda.
- Navegação inferior com Início, Mensagens e Ajuda.

### 6.3 Aba Início
- Mostrar saudação e contexto do usuário.
- Exibir atalho para iniciar conversa.
- Exibir sugestões de temas mais comuns.
- Exibir tempo estimado de resposta, quando configurado.

### 6.4 Aba Mensagens
- Listar conversas anteriores.
- Mostrar autor, prévia, data relativa e status.
- Permitir abrir conversa existente.
- Permitir iniciar nova conversa.

### 6.5 Aba Ajuda
- Exibir busca de artigos.
- Exibir coleções e categorias.
- Permitir navegação por área funcional.
- Permitir sugerir artigo antes de abrir ticket.

## 7. Fluxos funcionais
### 7.1 Fluxo do chat
1. Usuário clica no botão flutuante.
2. Widget abre com saudação e atalhos.
3. Usuário envia mensagem.
4. O sistema cria ou reutiliza uma sessão de chat.
5. A conversa pode ser resolvida ali mesmo ou convertida em ticket.

### 7.2 Fluxo de abertura por e-mail
1. Usuário envia e-mail para o endereço do SAC.
2. O sistema recebe e identifica o tenant correto.
3. Uma conversa ou ticket é criado automaticamente.
4. Respostas posteriores são associadas à mesma thread.
5. O usuário recebe retorno no e-mail original.

### 7.3 Fluxo de abertura por WhatsApp
1. Usuário envia mensagem pelo número oficial.
2. O sistema cria sessão de atendimento.
3. O agente ou regra automática pode converter a conversa em ticket.
4. O histórico é preservado e vinculado ao ticket.
5. O usuário continua sendo atendido pelo mesmo canal.

### 7.4 Fluxo de conversão em ticket
1. Atendimento inicia em chat, e-mail ou WhatsApp.
2. Se a demanda exigir acompanhamento formal, o sistema gera ticket.
3. O ticket herda histórico, anexos, categoria sugerida e canal de origem.
4. O ticket é encaminhado para fila, unidade ou departamento adequado.

## 8. Regras de negócio
- Um usuário autenticado deve ser identificado automaticamente sempre que possível.
- Se o usuário não estiver autenticado, o sistema deve permitir abertura assistida com e-mail ou telefone.
- Não deve haver duplicidade de ticket aberto para a mesma demanda, salvo regra explícita.
- A categoria do ticket pode ser sugerida por artigo acessado, palavras-chave, fila, unidade ou seleção manual.
- O sistema deve permitir que tenant filho crie e administre sua própria operação de suporte.
- Um tenant filho deve conseguir atender os próprios clientes com a mesma estrutura de chat, e-mail e WhatsApp.

## 9. Entidades principais
### 9.1 chat_sessions
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

### 9.2 chat_messages
- id
- session_id
- tenant_id
- sender_type
- sender_id
- body
- attachments
- is_internal
- created_at

### 9.3 tickets
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

### 9.4 ticket_messages
- id
- ticket_id
- tenant_id
- sender_type
- sender_id
- body
- attachments
- is_public
- created_at

### 9.5 help_articles
- id
- tenant_id
- visibility
- title
- content
- category_id
- tags
- created_at
- updated_at

### 9.6 inbound_channel_configs
- id
- tenant_id
- type
- address_or_number
- status
- routing_rules
- created_at
- updated_at

## 10. Regras por canal
### 10.1 Chat web
- Deve existir widget embutido com abertura rápida.
- Deve permitir resposta em tempo real ou assíncrona.
- Deve converter para ticket quando houver necessidade de formalização ou quando o agente assumir.

### 10.2 E-mail
- Deve suportar captura de mensagens recebidas.
- Deve manter thread por Message-ID, References ou regra equivalente.
- Deve anexar arquivos ao ticket e preservar mensagem original.

### 10.3 WhatsApp
- Deve suportar ingestão de mensagens via integração oficial.
- Deve preservar número de origem, mensagens e anexos.
- Deve permitir escalonamento da conversa para ticket.

## 11. Interface e UX
- O chat deve seguir a identidade visual do tenant.
- O cabeçalho deve exibir nome da marca e estado do atendimento.
- A área de mensagens deve ser rolável.
- O campo de composição deve ficar fixo na base do widget.
- A navegação inferior deve permanecer fixa dentro do componente.
- Os atalhos devem ser configuráveis por tenant.

## 12. Operação e atendimento
- O chat pode iniciar com bot, triagem humana ou fila híbrida.
- A mensagem deve entrar na sessão adequada antes de virar ticket.
- O agente pode assumir a conversa e converter em ticket manualmente ou por regra.
- A conversa deve manter contexto ao trocar de canal.
- O ticket deve carregar histórico consolidado de todos os canais usados.

## 13. SLA e priorização
- O ticket derivado do chat, e-mail ou WhatsApp deve herdar SLA aplicável.
- A prioridade pode ser inferida por palavras-chave, fila ou categoria.
- O sistema deve suportar primeira resposta, próxima resposta e resolução.
- O tempo em espera do cliente deve ser contabilizado conforme política do tenant.

## 14. Segurança e privacidade
- O acesso deve respeitar RBAC por tenant, unidade, fila e departamento.
- O conteúdo das mensagens deve ser sanitizado.
- Anexos devem ter validação de tipo e tamanho.
- Logs de auditoria devem registrar abertura, leitura, resposta, conversão e fechamento.
- Dados sensíveis devem seguir a política de retenção e LGPD.

## 15. Auditoria e rastreio
- Toda entrada por chat, e-mail ou WhatsApp deve gerar evento de auditoria.
- Toda conversão de conversa para ticket deve ser auditável.
- Toda troca de status, atribuição e encerramento deve ficar registrada.
- O histórico deve ser recuperável por ticket e por sessão.

## 16. API sugerida
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

## 17. Eventos de domínio
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

## 18. Critérios de aceite
- O usuário consegue abrir o chat rápido pelo botão flutuante.
- O usuário consegue iniciar demanda pela interface do chat.
- O cliente consegue abrir ticket por e-mail.
- O cliente consegue abrir ticket por WhatsApp.
- O sistema preserva histórico, anexos e origem em todos os canais.
- O mesmo modelo funciona para tenant raiz, tenant cliente e subtenant.
- O ticket é criado ou associado sem perda de contexto.

## 19. MVP
### Inclui
- Botão flutuante de chat.
- Tela com Início, Mensagens e Ajuda.
- Envio de mensagem no chat.
- Conversão de chat em ticket.
- Ingestão de e-mail.
- Ingestão de WhatsApp.
- Base de conhecimento básica.
- Auditoria de eventos principais.

### Não inclui no MVP
- IA generativa avançada.
- BI preditivo.
- RPA.
- Discador telefônico.
- Marketplace de extensões.
- Automação complexa multietapa.

## 20. Observações finais
- O módulo deve ser pensado como um canal plugável dentro do SAC.
- A mesma estrutura deve ser reaproveitada em todos os níveis da hierarquia do SaaS.
- O chat rápido é apenas a interface; o domínio continua sendo ticket, sessão e auditoria.
- A implementação deve nascer preparada para expansão omnichannel.

