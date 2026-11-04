# Spec — Cookies e Sessions

- Language Standard: Global English
## Visão geral
Este documento define a especificação funcional e técnica do módulo **Cookies e Sessions** para uma plataforma SaaS enterprise multi-entity e multi-unit. O objetivo é centralizar o gerenciamento de sessões autenticadas, políticas de cookies, auditoria de acesso, automações de expiração e controles de segurança, com interfaces completas para operação, governança e conformidade LGPD.

## Objetivos do módulo
- Gerenciar sessões de usuários, dispositivos e tokens de acesso.
- Controlar políticas de cookies por domínio, ambiente, unidade e entidade.
- Permitir auditoria detalhada de login, logout, renovação, revogação e anomalias.
- Oferecer dashboards com métricas, gráficos e widgets operacionais.
- Disponibilizar CRUD completo com drawers para criação, edição, visualização e revisão.
- Suportar Kanban operacional para triagem e tratamento de sessões suspeitas.
- Automatizar ações de expiração, revogação, limpeza e notificação.
- Garantir conformidade com segurança, rastreabilidade e LGPD.

## Escopo funcional
### Entidades principais
- CookiePolicy.
- Session.
- SessionDevice.
- SessionEvent.
- SessionRule.
- SessionAutomation.
- ConsentRecord.
- SecurityIncident.

### Perfis de uso
- Administrador global.
- Administrador de entidade.
- Administrador de unidade.
- Time de segurança.
- Auditor.
- Suporte técnico.
- Usuário final autenticado.

## Requisitos de negócio
- O sistema deve permitir configuração de políticas de cookies por ambiente, domínio e unidade.
- O sistema deve registrar todas as sessões autenticadas com metadados de dispositivo, IP, geolocalização, user agent e contexto de login.
- O sistema deve permitir revogação manual e automática de sessões.
- O sistema deve permitir visualização de consentimentos de cookies e histórico de aceite.
- O sistema deve suportar políticas de retenção e expiração por tipo de sessão e tipo de cookie.
- O sistema deve registrar ações administrativas em trilha de auditoria imutável.
- O sistema deve permitir bloqueio de sessão por risco, geolocalização incomum, múltiplos logins ou alteração de fingerprint.
- O sistema deve suportar alertas e automações baseadas em regras.

## Regras de segurança
- Cookies sensíveis devem ser marcados como HttpOnly, Secure e SameSite adequadamente.
- Sessões devem possuir identificador aleatório de alta entropia.
- O sistema deve suportar rotação de sessão após autenticação e elevação de privilégio.
- O sistema deve invalidar sessões após logout, expiração, risco detectado ou revogação administrativa.
- O sistema deve registrar tentativa de uso de sessão expirada ou revogada.
- O sistema deve permitir políticas distintas por ambiente: local, homologação, produção.
- O sistema deve suportar limitação de taxa para operações sensíveis.

## Páginas do módulo
### 1. Dashboard de sessões
#### Componentes
- KPIs de sessões ativas, expiradas, revogadas e suspeitas.
- Gráfico de linhas com evolução de sessões por período.
- Gráfico de pizza por tipo de dispositivo.
- Gráfico de barras por unidade, entidade ou domínio.
- Widget de alertas críticos.
- Widget de sessões em risco.
- Widget de consentimentos pendentes.
- Widget de automações executadas hoje.

#### Controles
- Filtro por período.
- Filtro por entidade.
- Filtro por unidade.
- Filtro por ambiente.
- Filtro por status.
- Filtro por tipo de dispositivo.
- Exportar CSV/PDF.
- Atualizar dados.
- Alternar visualização resumida/detalhada.

### 2. Sessões
#### Datatable
Colunas:
- ID.
- Usuário.
- Entidade.
- Unidade.
- Status.
- IP.
- País.
- Dispositivo.
- Browser.
- Sistema operacional.
- Criada em.
- Última atividade.
- Expira em.
- Risco.
- Ações.

#### Ações de linha
- Visualizar.
- Editar atributos administrativos.
- Revogar sessão.
- Forçar logout.
- Marcar como suspeita.
- Reprocessar risco.
- Ver histórico.

#### Drawer de sessão
Campos:
- Usuário.
- E-mail.
- Token hash.
- Session ID.
- IP inicial.
- IP atual.
- User agent.
- Fingerprint.
- Localização.
- Status.
- Origem do login.
- MFA aplicado.
- Escopo.
- Última renovação.
- Expiração.
- Motivo de revogação.
- Observações.

### 3. Políticas de cookies
#### Datatable
Colunas:
- Nome.
- Domínio.
- Ambiente.
- Categoria.
- Obrigatório.
- Duração.
- SameSite.
- Secure.
- HttpOnly.
- Ativo.
- Última revisão.
- Ações.

#### Drawer de política
Campos:
- Nome da política.
- Domínio alvo.
- Entidade.
- Unidade.
- Ambiente.
- Categoria do cookie.
- Descrição.
- Duração em dias.
- SameSite.
- Secure.
- HttpOnly.
- Consentimento obrigatório.
- Banner exibido.
- Texto legal.
- Versão.
- Vigência.
- Status.

### 4. Consentimentos
#### Datatable
Colunas:
- Usuário.
- Política.
- Status.
- Aceite em.
- Revogado em.
- IP.
- Canal.
- Versão.
- Ações.

#### Drawer de consentimento
Campos:
- Identificador do usuário.
- Política relacionada.
- Status.
- Timestamp de aceite.
- Canal de aceite.
- Versão exibida.
- Registro de prova.
- IP.
- User agent.
- Observações.

### 5. Regras e automações
#### Datatable
Colunas:
- Nome.
- Tipo.
- Condição.
- Ação.
- Severidade.
- Ativo.
- Agenda.
- Última execução.
- Próxima execução.
- Ações.

#### Drawer de automação
Campos:
- Nome.
- Descrição.
- Gatilho.
- Condição lógica.
- Ação executada.
- Escopo.
- Limite de execução.
- Janela de execução.
- Severidade.
- Notificar por.
- Ativo.

### 6. Auditoria
#### Datatable
Colunas:
- Data/hora.
- Usuário.
- Ação.
- Recurso.
- Resultado.
- IP.
- Origem.
- Correlation ID.
- Ações.

#### Filtros
- Período.
- Usuário.
- Entidade.
- Unidade.
- Ação.
- Resultado.
- IP.
- Recurso.

## Widgets obrigatórios
- Total de sessões ativas.
- Sessões expirando em breve.
- Sessões suspeitas.
- Cookies obrigatórios ativos.
- Consentimentos pendentes.
- Revogações hoje.
- Alertas de risco.
- Automações falhas.

## Charts obrigatórios
- Linha: sessões ao longo do tempo.
- Barras: sessões por unidade.
- Pizza: distribuição por dispositivo.
- Área: volume de eventos de sessão.
- Heatmap: horários de maior atividade.
- Funil: login, consentimento, sessão ativa, renovação, logout.

## Kanban operacional
### Colunas
- Novas suspeitas.
- Em análise.
- Aguardando ação.
- Revogadas.
- Resolved.
- Ignoradas.

### Cards
Cada card deve exibir:
- Usuário.
- Tipo de risco.
- Severidade.
- IP.
- Unidade.
- Data/hora.
- Última ação.
- Responsável.

### Ações no card
- Abrir drawer.
- Mover coluna.
- Reatribuir.
- Marcar como resolvido.
- Revogar sessão.
- Abrir incidente.

## Controles gerais
- Busca global.
- Filtros avançados.
- Ordenação por qualquer coluna.
- Paginação.
- Seleção múltipla.
- Ações em lote.
- Exportação.
- Importação de regras.
- Atualização automática.
- Toggle de colunas.
- Modo compacto e expandido.
- Painel lateral de contexto.

## Ações em lote
- Revogar múltiplas sessões.
- Marcar múltiplos consentimentos como revisados.
- Ativar/desativar políticas.
- Executar automações manualmente.
- Exportar evidências.
- Enviar notificações.
- Encaminhar para análise.

## Fluxos principais
### Login e criação de sessão
1. Usuário autentica.
2. Sistema valida credenciais e MFA.
3. Sistema cria sessão com fingerprint e metadados.
4. Sistema registra eventos de auditoria.
5. Sistema aplica política de cookies e consentimento.

### Revogação de sessão
1. Operador seleciona a sessão.
2. Sistema exibe motivo e impacto.
3. Operador confirma revogação.
4. Sistema invalida token.
5. Sistema registra evento e notifica responsáveis.

### Tratamento de risco
1. Motor de regras identifica anomalia.
2. Sessão é sinalizada.
3. Card é movido para Kanban.
4. Operador analisa dados.
5. Ação final é aplicada e auditada.

## Automações
- Revogar sessão inativa por X minutos.
- Encerrar sessão após alteração de IP suspeita.
- Notificar login em novo dispositivo.
- Exigir reautenticação em ação crítica.
- Expirar cookies fora da política.
- Bloquear sessão após múltiplas falhas.
- Abrir incidente ao detectar risco alto.
- Enviar resumo diário de sessões e consentimentos.

## Integrações
- Serviço de autenticação.
- Serviço de auditoria.
- Serviço de notificações.
- Serviço de risco e antifraude.
- Serviço de consentimento LGPD.
- Webhooks para incidentes.
- Logs centralizados.

## Requisitos de API
### Endpoints principais
- GET /sessions
- GET /sessions/{id}
- POST /sessions/{id}/revoke
- POST /sessions/{id}/flag
- POST /sessions/{id}/refresh
- GET /cookie-policies
- POST /cookie-policies
- PUT /cookie-policies/{id}
- DELETE /cookie-policies/{id}
- GET /consents
- POST /consents/{id}/revoke
- GET /automations
- POST /automations/{id}/run
- GET /audit-logs

## Modelo de dados mínimo
### Session
- id.
- user_id.
- entity_id.
- unit_id.
- status.
- ip_address.
- user_agent.
- device_type.
- browser.
- os.
- fingerprint.
- risk_score.
- created_at.
- last_activity_at.
- expires_at.
- revoked_at.
- revoked_reason.

### CookiePolicy
- id.
- name.
- domain.
- environment.
- category.
- same_site.
- secure.
- http_only.
- duration_days.
- consent_required.
- banner_enabled.
- version.
- active.

### ConsentRecord
- id.
- user_id.
- policy_id.
- status.
- accepted_at.
- revoked_at.
- ip_address.
- user_agent.
- evidence_hash.

## UX/UI
- Layout com sidebar, topbar e área principal.
- Cards com status por cor e ícone.
- Drawers laterais para edição sem sair da página.
- Tabelas responsivas com colunas configuráveis.
- Kanban com drag and drop.
- Gráficos com legenda e tooltip.
- Estados vazios, loading e erro bem definidos.
- Confirmação para ações destrutivas.

## Validações
- Campos obrigatórios devem ser validados no frontend e backend.
- Duração de cookie deve respeitar limites mínimos e máximos.
- Regra de SameSite deve aceitar apenas valores válidos.
- Revogação exige motivo quando em produção.
- Ações em lote devem exigir confirmação explícita.

## Logs e auditoria
- Registrar quem executou a ação.
- Registrar data/hora com timezone.
- Registrar origem da requisição.
- Registrar antes e depois quando aplicável.
- Registrar falhas, exceções e tentativas indevidas.

## Permissões
- Visualizar sessões.
- Revogar sessões.
- Gerenciar políticas.
- Gerenciar consentimentos.
- Executar automações.
- Visualizar auditoria.
- Exportar dados.
- Configurar regras de risco.

## Critérios de aceite
- O módulo deve exibir dashboards com widgets e gráficos funcionais.
- O módulo deve permitir CRUD completo de cookies, sessões e automações.
- O módulo deve permitir Kanban para tratamento operacional.
- O módulo deve executar automações agendadas e manuais.
- O módulo deve registrar auditoria completa de ações críticas.
- O módulo deve suportar filtros, busca, exportação e ações em lote.
- O módulo deve estar pronto para uso multi-entity e multi-unit.

## Entregáveis esperados
- Página de dashboard.
- Página de sessões.
- Página de políticas de cookies.
- Página de consentimentos.
- Página de automações.
- Página de auditoria.
- Painel Kanban.
- Drawers de cadastro, edição e detalhe.
- Gráficos e widgets operacionais.
- API backend documentada.

## Observações técnicas
- Recomenda-se UUID como chave primária.
- Recomenda-se indexação por status, usuário, entidade, unidade e expiração.
- Recomenda-se soft delete para políticas e regras.
- Recomenda-se cache para consultas de dashboard.
- Recomenda-se separação de sessão ativa e evento histórico.
- Recomenda-se versionamento de políticas e consentimentos.
