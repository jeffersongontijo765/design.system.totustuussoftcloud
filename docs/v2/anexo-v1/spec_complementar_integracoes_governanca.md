# Spec Complementar de Lacunas Funcionais e Integrações

- Language Standard: Global English
## 1. Objetivo
Este documento complementa os specs existentes de RH/HCMRH, SMT e Suprimentos, fechando lacunas de integração, governança, automações, observabilidade, segurança e padronização operacional.

## 2. Escopo
Este spec cobre funcionalidades transversais e itens ainda não formalizados nos anexos, com foco em:
- Integração entre RH, SMT e Suprimentos.
- Padronização de eventos, filas, notificações e auditoria.
- Regras de retenção, anonimização, exportação e mascaramento LGPD.
- Monitoramento operacional, retries, idempotência e trilha de execução.
- Checklist de implementação para fechamento de backlog.

## 3. Lacunas Prioritárias
### 3.1 Integração RH ↔ SMT
- Criação automática de exames ocupacionais a partir de admissão, movimentação e retorno.
- Criação automática de eventos de eSocial S-2220, S-2230 e S-2240 a partir de gatilhos do RH e SMT.
- Sincronização de status de afastamento, restrições médicas e aptidão do colaborador.
- Exposição de status consolidado de saúde ocupacional no perfil do colaborador.

### 3.2 Integração SMT ↔ Suprimentos
- Geração automática de solicitação de compra ao atingir estoque mínimo de EPI.
- Bloqueio e liberação de fornecedores por conformidade documental e CA vencido.
- Consumo de contratos e atas em compras de EPI, insumos e serviços de segurança.
- Registro de evidência de reposição, devolução e auditoria da cadeia de suprimentos.

### 3.3 Integração RH ↔ Suprimentos
- Solicitação automática de itens de onboarding e offboarding.
- Integração de centro de custo, cargo e unidade nas requisições.
- Controle de ativos e itens entregues ao colaborador com histórico unificado.

### 3.4 Padronização global
- Todos os módulos devem usar id, uuid e code em entidades principais.
- Todos os listados devem suportar paginação server-side, filtros, ordenação, busca global e exportação auditada.
- Todos os drawers críticos devem possuir abas, histórico, comentários, anexos e auditoria.
- Todas as ações críticas devem gerar audit log com before/after, IP e user-agent.

## 4. Módulos Transversais
### 4.1 Event Bus Interno
Um barramento interno deve centralizar eventos de domínio para permitir automações desacopladas. Eventos mínimos:
- employee.created.
- employee.terminated.
- employee.department-changed.
- exam.scheduled.
- exam.performed.
- cat.created.
- absence.created.
- epi.stock-minimum-reached.
- training.expired.
- supplier.blocked.
- request.approved.

#### Requisitos
- Persistência de eventos em fila.
- Status pending, queued, sent, processed, rejected.
- Reprocessamento manual e automático.
- Idempotência por chave de evento.
- Retenção de logs de processamento.

### 4.2 Central de Notificações
- Canal e-mail.
- Canal in-app.
- Canal webhook.
- Canal push interno.
- Canal SMS opcional.
- Preferências por perfil, unidade e evento.
- Templates com variáveis e preview.

### 4.3 Auditoria Unificada
- Registrar toda criação, atualização, exclusão lógica, exportação, aprovação, reprovação e alteração de status.
- Auditoria com entityid, unitid, userid, action, resource, resourceid, beforejson, afterjson, ip, useragent, createdat.
- Tela de consulta com filtros por período, usuário, módulo, ação e recurso.
- Exportação de auditoria somente para perfis autorizados.

### 4.4 LGPD e Segurança
- Dados sensíveis criptografados em repouso.
- CPF, CID, salário e dados bancários mascarados em listagens para perfis sem permissão.
- Portabilidade de dados por colaborador em arquivo estruturado.
- Anonimização automática conforme política de retenção.
- Bloqueio de exportação sem motivo e sem trilha de auditoria.

## 5. Telas Complementares
### 5.1 Hub de Integrações
Página central para visualizar integrações ativas, filas, falhas, retentativas, jobs e webhooks.

#### Blocos
- KPIs de integrações.
- Lista de eventos em fila.
- Lista de webhooks.
- Jobs com erro.
- Histórico de transmissões.
- Alertas de falha.

#### Colunas da fila
- Código.
- Evento.
- Origem.
- Referência.
- Status.
- Tentativas.
- Próxima tentativa.
- Protocolo.
- Mensagem.
- Ações.

### 5.2 Central de Governança
Tela para parametrizar políticas globais de integração, retenção, mascaramento, notificações e automações.

#### Seções
- Políticas de retenção.
- Regras de máscara de dados.
- Templates de eventos.
- Destinatários padrão.
- Regras de retry.
- Rate limits.
- Configurações por entidade e unidade.

### 5.3 Timeline Operacional
Linha do tempo unificada exibindo eventos de RH, SMT e Suprimentos em ordem cronológica.

#### Filtros
- Módulo.
- Evento.
- Usuário.
- Unidade.
- Período.
- Status.

## 6. Fluxos Obrigatórios
### 6.1 Admissão
Ao criar um colaborador ativo, o sistema deve:
- Criar evento de onboarding.
- Agendar exame admissional.
- Gerar checklist de documentos.
- Criar solicitações de EPI e treinamentos obrigatórios.
- Registrar auditoria completa.

### 6.2 Afastamento
Ao registrar afastamento:
- Atualizar status do colaborador.
- Gerar eSocial S-2230.
- Notificar gestor, RH e ocupacional.
- Recalcular pendências de ponto e folha se necessário.

### 6.3 CAT
Ao registrar CAT:
- Criar evento eSocial S-2210.
- Abrir investigação de acidente.
- Disponibilizar anexos e testemunhas.
- Notificar SESMT e perfis autorizados.

### 6.4 EPI
Ao atingir estoque mínimo ou CA vencendo:
- Abrir alerta automático.
- Gerar solicitação de compra no módulo Suprimentos.
- Notificar SESMT.
- Registrar trilha de decisão.

### 6.5 Treinamentos
Ao vencer treinamento obrigatório:
- Notificar colaborador, gestor e RH.
- Bloquear conformidade do cargo, quando aplicável.
- Abrir tarefa de renovação.

## 7. APIs REST Complementares
### 7.1 Integrações
- GET /api/v1/integrations/dashboard
- GET /api/v1/integrations/queue
- POST /api/v1/integrations/queue/{uuid}/retry
- POST /api/v1/integrations/queue/{uuid}/cancel
- GET /api/v1/integrations/webhooks
- POST /api/v1/integrations/webhooks/test
- GET /api/v1/integrations/audit

### 7.2 Governança
- GET /api/v1/governance/policies
- PUT /api/v1/governance/policies/{uuid}
- GET /api/v1/governance/templates
- PUT /api/v1/governance/templates/{uuid}
- GET /api/v1/governance/retention
- PUT /api/v1/governance/retention/{uuid}

### 7.3 Timeline
- GET /api/v1/timeline/events
- GET /api/v1/timeline/events/{uuid}
- POST /api/v1/timeline/events/export

## 8. Schema SQL Complementar
### 8.1 Event Queue
```sql
CREATE TABLE sys_event_queue (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT UUID(),
  entityid BIGINT UNSIGNED NOT NULL,
  unitid BIGINT UNSIGNED NULL,
  eventkey VARCHAR(120) NOT NULL,
  eventtype VARCHAR(80) NOT NULL,
  payload JSON NOT NULL,
  status ENUM('pending','queued','sent','processed','rejected','cancelled') NOT NULL DEFAULT 'pending',
  attempts TINYINT UNSIGNED NOT NULL DEFAULT 0,
  maxattempts TINYINT UNSIGNED NOT NULL DEFAULT 5,
  nextattemptat DATETIME NULL,
  lastattemptat DATETIME NULL,
  lastresponse TEXT NULL,
  idempotencykey VARCHAR(120) NOT NULL,
  createdby BIGINT UNSIGNED NULL,
  createdat DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updatedat DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_entity_status (entityid, status),
  INDEX idx_eventkey (eventkey),
  UNIQUE KEY uk_idempotency (idempotencykey)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 8.2 Notification Log
```sql
CREATE TABLE sys_notification_log (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT UUID(),
  entityid BIGINT UNSIGNED NOT NULL,
  unitid BIGINT UNSIGNED NULL,
  eventkey VARCHAR(120) NOT NULL,
  channel ENUM('email','inapp','push','webhook','sms') NOT NULL,
  recipient VARCHAR(200) NOT NULL,
  subject VARCHAR(200) NULL,
  message TEXT NULL,
  status ENUM('queued','sent','failed','cancelled') NOT NULL DEFAULT 'queued',
  sentat DATETIME NULL,
  errortext TEXT NULL,
  createdat DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_event_channel (eventkey, channel)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 8.3 Governance Policy
```sql
CREATE TABLE sys_governance_policies (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT UUID(),
  entityid BIGINT UNSIGNED NOT NULL,
  policycode VARCHAR(60) NOT NULL,
  policyname VARCHAR(150) NOT NULL,
  policytype ENUM('retention','masking','notification','retry','rate_limit','export') NOT NULL,
  rulesjson JSON NOT NULL,
  status ENUM('active','inactive') NOT NULL DEFAULT 'active',
  createdat DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updatedat DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_entity_policy (entityid, policycode)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## 9. Regras de Negócio
- Não permitir integração sem entityid válido.
- Não permitir evento duplicado com mesma chave de idempotência.
- Não permitir exportação de dados sensíveis sem permissão explícita e justificativa.
- Não permitir mudança de status final sem auditoria.
- Não permitir reprocessamento de evento já confirmado sem permissão especial.
- Não permitir notificação de dados sensíveis em canal não autorizado.

## 10. RBAC Complementar
### Perfis de acesso
- SA Super Admin.
- GE Gestor de Entidade.
- GP Gestor de Pessoas.
- GPRH Gestor de Processos RH.
- SESMT Saúde e Segurança.
- MED Médico do Trabalho.
- RH Recursos Humanos.
- SUP Suprimentos.
- AUD Auditor.
- DPO Encarregado LGPD.

### Permissões novas
- integrations.view.
- integrations.retry.
- integrations.cancel.
- notifications.manage.
- governance.manage.
- timeline.view.
- timeline.export.
- retention.manage.
- masking.manage.

## 11. Critérios de Aceite
- Todas as integrações críticas devem ter fila, retry e auditoria.
- Todos os eventos de RH, SMT e Suprimentos devem ser rastreáveis.
- Toda exportação deve gerar log com motivo e usuário.
- Todo dado sensível deve respeitar mascaramento por perfil.
- Toda tela complementar deve seguir o padrão enterprise do sistema.
- Todo fluxo crítico deve possuir tratamento de erro e estado de reprocessamento.
- Toda política de retenção deve ser configurável por entidade.

## 12. Checklist de Entrega
- Hub de integrações implementado.
- Central de governança implementada.
- Timeline operacional implementada.
- Event bus persistente com retries.
- Logs de notificação e auditoria unificados.
- Regras LGPD consolidadas.
- APIs e rotas documentadas.
- Schemas SQL aplicados e indexados.
- RBAC ajustado para perfis novos.
- Testes de integração e regressão executados.

## 13. Conclusão
Este spec complementar fecha as lacunas transversais mais importantes entre RH, SMT e Suprimentos, consolidando uma base única de eventos, auditoria, governança e conformidade para a plataforma.
