# Spec Funcional e Técnica — Gestão de Notificações

## 1. Objetivo
A Gestão de Notificações centraliza a criação, segmentação, distribuição, acompanhamento e automação de notificações da plataforma multi-entity/multi-unit. O módulo deve suportar notificações operacionais, transacionais, informativas, críticas e automatizadas, com visão por entidade, unidade, canal, status, prioridade e origem do evento.

- Language Standard: Global English
## 2. Princípios de Produto
- O módulo deve ser assíncrono por padrão.
- Toda notificação deve ser rastreável do evento de origem até o resultado final.
- O sistema deve ser seguro por padrão e configurável por escopo.
- A operação deve ser rápida, com baixa fricção para criação, revisão, envio e auditoria.
- O comportamento em falhas deve ser previsível, idempotente e observável.

## 3. Escopo
O módulo cobre:
- Criação e disparo de notificações manuais e automáticas.
- Gestão de filas, agendamentos, regras, canais, templates e provedores.
- Monitoramento de entrega, leitura, falhas, retry e escalonamento.
- Organização em board Kanban por estágio operacional.
- Dashboards com widgets, métricas, alertas e gráficos analíticos.
- CRUD completo em drawers para operação rápida.
- Controles de segurança, auditoria, LGPD, governança e retenção.

## 4. Perfis de Acesso
- Super Admin.
- Admin da Entidade.
- Gestor da Unidade.
- Operador.
- Auditor/Compliance.
- Usuário Final.

### 4.1 Escopo de Permissão
O acesso deve considerar:
- Entidade.
- Unidade.
- Canal.
- Tipo de notificação.
- Ação permitida.
- Status do objeto.
- Sensibilidade do conteúdo.

### 4.2 Regras Gerais de Acesso
- Toda ação sensível deve ser auditada.
- Usuário final só pode visualizar notificações permitidas ao seu contexto.
- Operador não pode alterar políticas globais sem permissão explícita.
- Auditor/Compliance deve ter acesso de leitura ampliado e sem poder de mutação.
- A API deve aplicar RBAC e, quando necessário, ABAC.

## 5. Conceitos do Domínio
### 5.1 Notification Event
Evento de domínio que dispara ou alimenta uma automação. Exemplo: novo cadastro, mudança de status, atraso, falha de processamento, mensagem recebida, tarefa pendente, aniversário, expiração.

### 5.2 Notification Rule
Regra que associa eventos, condições e ações. Pode criar notificações, escalar, abrir tarefa, registrar log, acionar retry ou notificar em canal específico.

### 5.3 Notification Template
Modelo parametrizado para título, assunto, corpo e variáveis por canal.

### 5.4 Notification Instance
Registro concreto de uma notificação criada a partir de evento manual ou automático.

### 5.5 Delivery Attempt
Tentativa individual de envio da notificação em um canal/provedor específico.

### 5.6 Delivery Log
Registro técnico de processamento, bloqueio, envio, resposta do provedor, erro, retry e conclusão.

### 5.7 Queue Item
Item enfileirado para processamento assíncrono com bloqueio, prioridade, agendamento e política de retry.

## 6. Estados e Transições
### 6.1 Estados Principais
- Draft.
- In Review.
- Scheduled.
- Queued.
- Processing.
- Sent.
- Delivered.
- Read.
- Failed.
- Archived.
- Cancelled.

### 6.2 Transições Permitidas
- Draft -> In Review.
- In Review -> Scheduled.
- In Review -> Queued.
- Scheduled -> Queued.
- Queued -> Processing.
- Processing -> Sent.
- Sent -> Delivered.
- Delivered -> Read.
- Any active state -> Cancelled.
- Failed -> Queued quando houver retry válido.
- Any non-terminal state -> Archived quando permitido.

### 6.3 Regras de Transição
- Transições inválidas devem ser rejeitadas com erro padronizado.
- Estados terminais não devem ser reabertos sem ação explícita autorizada.
- Cancelamento deve preservar histórico e auditoria.
- Reenvio deve criar nova tentativa sem sobrescrever evidências da tentativa anterior.

## 7. Regras Gerais
- Toda notificação deve possuir entidade, unidade, tipo, canal, prioridade, status e responsável.
- O sistema deve permitir escopo global, por entidade, por unidade e por público segmentado.
- Notificações críticas devem exigir confirmação de leitura quando aplicável.
- Notificações com falha devem entrar em fila de retry com política configurável.
- Toda alteração relevante deve ser registrada em auditoria.
- Campos sensíveis devem respeitar LGPD, mascaramento e retenção configurável.
- Toda operação de envio deve ser idempotente.
- Toda entrega deve ser observável de ponta a ponta.

## 8. Contratos de Evento
### 8.1 Identificação do Evento
Cada evento deve possuir:
- event_name.
- event_version.
- event_id.
- source.
- occurred_at.
- entity_id.
- unit_id.
- actor_id.
- correlation_id.
- causation_id.
- payload.

### 8.2 Versionamento
- Todo evento deve ter versão explícita.
- Alterações incompatíveis exigem nova versão.
- Consumidores devem suportar coexistência de versões por período de migração.

### 8.3 Schema de Payload
- O payload deve ser validado por schema.
- Campos obrigatórios devem ser documentados por tipo de evento.
- Campos opcionais devem ter comportamento de fallback definido.
- O schema deve ser versionado junto ao evento.

### 8.4 Convenção de Nomes
Exemplos:
- student.created.
- enrollment.status_changed.
- payment.overdue.
- message.received.
- task.assigned.
- automation.rule_triggered.

## 9. Idempotência e Deduplicação
- Toda requisição de criação, disparo ou reprocessamento deve aceitar uma idempotency_key.
- Se a mesma chave for reapresentada, o sistema deve retornar o resultado anterior sem criar duplicidade.
- O worker deve deduplicar por combinação de event_id, notification_template_id e target context quando aplicável.
- Em reprocessamento, a tentativa anterior deve permanecer preservada como evidência.
- A deduplicação deve respeitar janela configurável por tipo de evento e canal.

## 10. Retry, Backoff e Reprocessamento
- O sistema deve suportar retry configurável por notificação, canal e provedor.
- O backoff deve suportar estratégia fixa, exponencial ou híbrida.
- Deve existir limite máximo de tentativas por política.
- O retry deve respeitar janelas de silêncio, rate limits e prioridade.
- Falhas permanentes devem ser classificadas por tipo: validação, transporte, provedor, conteúdo, autorização, timeout ou desconhecida.

### 10.1 Política de Retry
Campos mínimos:
- retry_policy_id.
- max_attempts.
- initial_delay_seconds.
- backoff_strategy.
- max_delay_seconds.
- jitter_enabled.
- active.

## 11. Entidades Principais
### 11.1 Notification
Campos mínimos:
- id.
- uuid.
- entity_id.
- unit_id.
- event_id.
- title.
- subject.
- message.
- type.
- category.
- priority.
- channel.
- target_audience.
- sender_type.
- sender_id.
- status.
- scheduled_at.
- queued_at.
- processing_at.
- sent_at.
- delivered_at.
- read_at.
- failed_at.
- expires_at.
- cancelled_at.
- retry_count.
- max_retries.
- idempotency_key.
- correlation_id.
- metadata.
- created_by.
- updated_by.
- created_at.
- updated_at.
- deleted_at.

### 11.2 Notification Template
- id.
- uuid.
- entity_id.
- unit_id.
- name.
- code.
- channel.
- subject_template.
- body_template.
- variables_schema.
- locale.
- active.
- version.
- created_at.
- updated_at.

### 11.3 Notification Rule / Automation
- id.
- uuid.
- entity_id.
- unit_id.
- name.
- trigger_event.
- trigger_version.
- conditions.
- actions.
- cooldown.
- priority.
- active.
- version.
- created_at.
- updated_at.

### 11.4 Notification Delivery Log
- id.
- notification_id.
- channel.
- provider.
- recipient.
- status.
- response_code.
- response_payload.
- attempt.
- sent_at.
- delivered_at.
- read_at.
- locked_at.
- worker_id.
- error_type.
- error_message.
- created_at.

### 11.5 Notification Queue
- id.
- notification_id.
- scheduled_at.
- processed_at.
- locked_at.
- lock_expires_at.
- worker_id.
- status.
- retry_count.
- priority.
- partition_key.
- created_at.
- updated_at.

### 11.6 Notification Subscription
- id.
- uuid.
- entity_id.
- unit_id.
- user_id.
- channel.
- topic.
- consent_status.
- opt_in_at.
- opt_out_at.
- source.
- created_at.
- updated_at.

### 11.7 Notification Provider
- id.
- uuid.
- name.
- code.
- channel.
- endpoint.
- credentials_ref.
- active.
- rate_limit.
- health_status.
- last_checked_at.
- created_at.
- updated_at.

## 12. Validações de Dados
- Campos obrigatórios por canal devem ser validados antes do envio.
- Limites de caracteres por canal devem ser respeitados.
- Variáveis do template devem ser resolvidas antes do envio.
- Conteúdo sem público-alvo válido deve ser bloqueado.
- Anexos devem ser validados por tamanho, tipo e política de segurança.
- Conteúdo sensível deve ser mascarado quando aplicável.
- Datas devem respeitar timezone da entidade/unidade e timezone do usuário quando relevante.

## 13. Canais e Provedores
### 13.1 Canais Suportados
- In-app.
- Email.
- SMS.
- Push.
- WhatsApp, quando habilitado.
- Webhook interno, quando necessário.

### 13.2 Regras por Canal
- In-app pode ser padrão para avisos internos.
- Email e SMS exigem validações adicionais de entrega e opt-in conforme política.
- Push depende de dispositivo/token válido.
- WhatsApp depende de provedor e template compatível.
- Webhook deve assinar a requisição e validar assinatura na recepção, quando aplicável.

### 13.3 Gestão de Provedores
- Cada canal pode ter múltiplos provedores.
- Deve existir health check por provedor.
- Deve existir fallback configurável entre provedores do mesmo canal.
- Falhas repetidas devem desativar o roteamento automático para o provedor com health crítico.

## 14. Fluxos Principais
### 14.1 Fluxo Manual
1. Usuário cria notificação.
2. Define público, canal e conteúdo.
3. Sistema valida regras e permissões.
4. Notificação entra em fila ou é enviada imediatamente.
5. Logs, métricas e auditoria são atualizados.

### 14.2 Fluxo Automático
1. Evento dispara automação.
2. Motor avalia condições e versão da regra.
3. Sistema gera notificação baseada em template.
4. Envio ocorre pelo canal definido.
5. Status, logs e auditoria são persistidos.

### 14.3 Fluxo de Falha
1. Provider retorna erro ou timeout.
2. Sistema registra falha categorizada.
3. Retry é agendado conforme política.
4. Se exceder o limite, status vira falhou definitivo.
5. Caso crítico, abrir alerta interno e opcionalmente escalar.

### 14.4 Fluxo de Cancelamento
1. Usuário autorizado solicita cancelamento.
2. Sistema valida se o estado permite cancelamento.
3. Itens ainda não processados são retirados da fila quando possível.
4. Logs preservam histórico da tentativa de cancelamento.
5. Auditoria registra autor, motivo e horário.

## 15. Observabilidade
### 15.1 Logs
- Todo processamento deve gerar logs estruturados.
- Logs devem incluir correlation_id, event_id, notification_id, provider e worker_id.
- Dados sensíveis devem ser redigidos.

### 15.2 Métricas
- Total por período.
- Enviadas hoje.
- Pendentes na fila.
- Taxa de entrega.
- Taxa de leitura.
- Falhas últimas 24h.
- Retries em andamento.
- Tempo médio até envio.
- Tempo médio até entrega.
- Falhas por provedor.
- SLA cumprido versus violado.

### 15.3 Tracing
- O tracing deve permitir acompanhar evento -> regra -> fila -> worker -> provedor -> resultado.
- O correlation_id deve ser propagado em toda a cadeia.

### 15.4 Alertas
- Falha elevada por provedor.
- Crescimento anormal da fila.
- Aumento de retry.
- SLA violado.
- Worker parado ou sem heartbeat.
- Taxa de erro acima do limiar por canal.

## 16. Segurança e Compliance
- Mascaramento de dados sensíveis.
- Criptografia em repouso e em trânsito.
- Controle de acesso por perfil e escopo.
- Consentimento e base legal quando aplicável.
- Direito de exclusão/anonimização conforme LGPD.
- Registros de acesso e alteração.
- Bloqueio de canais não autorizados.
- Rotação de segredos e credenciais.
- Segredos devem ser armazenados fora do código-fonte.
- Logs não devem expor tokens, documentos pessoais ou payload sensível completo.
- Anexos devem ser validados contra malware quando aplicável.

## 17. Requisitos Não Funcionais
- Escalabilidade horizontal.
- Baixa latência na fila.
- Processamento assíncrono.
- Alta disponibilidade.
- Tolerância a falhas de provedor.
- Reprocessamento controlado.
- Compatibilidade com multi-entity e multi-unit.
- Auditoria completa com retenção configurável.
- Suporte a internacionalização, fuso horário e formatos locais.
- Backpressure sob carga elevada.
- Deploy sem downtime sempre que possível.

## 18. Arquitetura de Execução
### 18.1 Componentes
- API de gestão.
- API de automação.
- Worker de fila.
- Scheduler.
- Provider adapters.
- Rules engine.
- Audit logger.
- Metrics exporter.

### 18.2 Separação de Responsabilidades
- A API valida e persiste intenções.
- O worker processa envio e retry.
- O scheduler dispara agendamentos.
- O rules engine avalia eventos e condições.
- Os adapters encapsulam integrações externas.

### 18.3 Backpressure
- Quando a fila exceder limite, o sistema deve priorizar notificações críticas.
- Notificações de baixa prioridade podem ser adiadas conforme política.
- O sistema deve registrar saturação e acionar alerta operacional.

## 19. API Suggested
### 19.1 Endpoints Principais
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
- GET /notification-subscriptions
- POST /notification-subscriptions
- GET /notification-providers
- POST /notification-providers

### 19.2 Padrões de API
- Paginação server-side.
- Filtros normalizados.
- Erros padronizados.
- IDs UUID.
- Auditoria automática.
- Suporte a idempotency-key.
- Suporte a correlation-id.
- Respostas consistentes por endpoint.

### 19.3 Erros Padronizados
- invalid_payload.
- unauthorized.
- forbidden.
- not_found.
- conflict.
- rate_limited.
- provider_unavailable.
- template_validation_failed.
- duplicate_request.
- retry_exhausted.

### 19.4 Exemplo de Resposta
```json
{
  "success": false,
  "error": {
    "code": "template_validation_failed",
    "message": "Variável required_name ausente.",
    "details": {
      "field": "required_name"
    }
  },
  "correlation_id": "c-123"
}
```

## 20. Modelos de Payload
### 20.1 Evento de Exemplo
```json
{
  "event_name": "student.created",
  "event_version": "1.0",
  "event_id": "evt_01",
  "source": "core-school",
  "occurred_at": "2026-07-02T20:00:00-03:00",
  "entity_id": 10,
  "unit_id": 3,
  "actor_id": 99,
  "correlation_id": "cor_001",
  "causation_id": "cause_001",
  "payload": {
    "student_id": 123,
    "name": "Aluno Exemplo"
  }
}
```

### 20.2 Criação de Notificação
```json
{
  "title": "Novo aluno cadastrado",
  "subject": "Aluno criado com sucesso",
  "message": "O aluno {{name}} foi cadastrado.",
  "type": "informational",
  "category": "academic",
  "priority": "normal",
  "channel": ["in_app", "email"],
  "target_audience": {
    "role": ["admin", "manager"]
  },
  "scheduled_at": null,
  "idempotency_key": "idem_001",
  "metadata": {
    "event_name": "student.created"
  }
}
```

### 20.3 Regra de Automação
```json
{
  "name": "Boas-vindas novo aluno",
  "trigger_event": "student.created",
  "trigger_version": "1.0",
  "conditions": [
    { "field": "unit_id", "operator": "in", "value": [3, 4] }
  ],
  "actions": [
    { "type": "create_notification", "template_code": "student_welcome" }
  ],
  "cooldown": 300,
  "priority": 50,
  "active": true,
  "version": 1
}
```

## 21. Testabilidade
### 21.1 Tipos de Teste
- Testes unitários de validação, template e regra.
- Testes de integração com API, fila e banco.
- Testes de contrato para eventos e payloads.
- Testes de ponta a ponta para fluxos críticos.
- Testes de carga para fila, worker e dashboard.
- Testes de falha com provedor indisponível.
- Testes de segurança para autenticação, autorização e mascaramento.

### 21.2 Cenários Mínimos
- Criar notificação manual.
- Agendar notificação.
- Disparar automação por evento.
- Validar template com variável ausente.
- Processar retry.
- Cancelar agendamento.
- Marcar como lida.
- Falha de provedor com fallback.
- Rate limit excedido.
- Idempotency key duplicada.

### 21.3 Ambiente de Homologação
- Deve existir sandbox para provedores.
- Deve existir mock para envio e leitura.
- Deve existir dataset de teste com múltiplas entidades e unidades.
- Deve existir modo seguro para simular automações sem envio real.

## 22. Critérios de Aceite
- Criar, editar, agendar, reenviar, cancelar, marcar como lida e arquivar notificações.
- Visualizar notificações em tabela, cards e Kanban.
- Operar automações baseadas em eventos com versionamento.
- Monitorar entrega, leitura, erro, retry e SLA.
- Gerenciar templates, regras, canais, provedores e permissões.
- Exibir dashboards com widgets e charts atualizados.
- Registrar auditoria e obedecer políticas de segurança e LGPD.
- Processar eventos de forma idempotente e observável.
- Suportar falha de provedor com retry e fallback.

## 23. Componentes Frontend
- NotificationDashboard.
- NotificationDatatable.
- NotificationDrawerForm.
- NotificationKanbanBoard.
- NotificationWidgets.
- NotificationCharts.
- NotificationAutomationBuilder.
- NotificationTemplateManager.
- NotificationDeliveryLogTable.
- NotificationSettingsPanel.
- NotificationSubscriptionPanel.
- NotificationProviderPanel.

## 24. Layout UI Recomendado
- Topbar com busca global, filtros rápidos e ações primárias.
- Sidebar com Dashboard, Lista, Kanban, Automação, Templates, Logs, Provedores e Configurações.
- Área central com cards, datatable e gráficos.
- Drawers laterais para CRUD rápido.
- Modal apenas para confirmações críticas.
- Estado de carregamento, vazio, erro e parcial devem ser tratados explicitamente.

## 25. Prioridades de Implementação
### Fase 1
- Lista, drawer CRUD, detalhes, dashboard básico, templates e logs.

### Fase 2
- Kanban, automações, retry, alertas, provedores e métricas avançadas.

### Fase 3
- SLA, auditoria ampliada, fallback multi-provedor, integrações externas e observabilidade avançada.

## 26. Observações Finais
O módulo deve ser projetado para operação intensiva, com foco em governança, produtividade, rastreabilidade e resiliência. A interface precisa permitir navegação rápida entre visão analítica, ação operacional e configuração administrativa, sem perder consistência entre entidade e unidade. O comportamento técnico deve permanecer previsível sob falha, carga elevada e mudanças de versão.
