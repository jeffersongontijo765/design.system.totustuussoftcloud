# SPEC — Módulo Auditoria

- Language Standard: Global English
## 1. Visão geral

O módulo de Auditoria centraliza rastreabilidade, conformidade, revisão de eventos, trilhas de alteração, investigação de incidentes, monitoramento de integridade e governança operacional para um SaaS multi-entidade, multi-unidade e multi-usuário.

Este módulo deve cobrir toda a jornada de auditoria da plataforma, incluindo:
- Eventos de acesso.
- Alterações em cadastros e configurações.
- Aprovações e rejeições operacionais.
- Logs de API.
- Logs de segurança.
- Logs de automação.
- Logs de integrações externas.
- Revisões por fila, kanban e status.
- Evidências de conformidade.
- Exportação e retenção de registros.
- Controles de privacidade, sigilo e LGPD/GDPR.

A auditoria deve ser consultável por filtros avançados, organizada em datatables de alta densidade, acompanhada por widgets operacionais, charts executivos, drawers CRUD para investigação e painéis Kanban para tratamento de ocorrências.

---

## 2. Objetivos do módulo

- Garantir rastreabilidade completa de ações críticas.
- Permitir investigação rápida de incidentes.
- Expor trilhas de alteração antes/depois.
- Controlar acesso a registros sensíveis.
- Atender requisitos de compliance e governança.
- Reduzir risco operacional e fraude.
- Prover evidências para revisões internas e externas.
- Permitir correlação entre eventos, usuários, unidades e entidades.

---

## 3. Escopo funcional

### 3.1. Entidades principais
- Audit Log.
- Security Event.
- Access Event.
- Change Event.
- API Request Log.
- Automation Run Log.
- Integration Log.
- Evidence Record.
- Review Case.
- Audit Rule.
- Retention Policy.
- Exception/Alert.
- Correlation Session.

### 3.2. Públicos do módulo
- Administrador do sistema.
- Gestor de unidade.
- Gestor de entidade.
- Auditor interno.
- Segurança da informação.
- Compliance/LGPD.
- Suporte técnico.
- Usuário final com permissão restrita de consulta.

---

## 4. Páginas do módulo

### 4.1. Dashboard de Auditoria
Página inicial com visão consolidada do ecossistema de auditoria.

#### Controles
- Filtro de período.
- Filtro por entidade.
- Filtro por unidade.
- Filtro por tipo de evento.
- Filtro por gravidade.
- Filtro por usuário.
- Filtro por módulo.
- Filtro por origem IP.
- Filtro por canal.
- Salvar filtro.
- Exportar dados.
- Atualização automática.
- Modo investigação.
- Modo compliance.

#### Widgets
- Total de eventos no período.
- Eventos críticos.
- Tentativas de acesso negadas.
- Alterações sensíveis.
- Incidentes abertos.
- APIs com erro.
- Automations com falha.
- Evidências pendentes.

#### Charts
- Eventos por dia.
- Eventos por tipo.
- Eventos críticos por módulo.
- Volume por entidade/unidade.
- Taxa de falhas por integração.
- Distribuição por usuário.
- Heatmap por horário.
- Linha de tendência de risco.

#### Seções
- Últimos eventos relevantes.
- Casos em investigação.
- Alertas ativos.
- Top usuários com maior volume de ações.
- Top módulos com maior incidência.

---

### 4.2. Audit Trail
Página principal de consulta de trilhas de auditoria.

#### Datatable
Colunas:
- ID.
- Data/hora.
- Entidade.
- Unidade.
- Módulo.
- Recurso.
- Ação.
- Usuário.
- Perfil.
- Origem.
- IP.
- Resultado.
- Gravidade.
- Correlation ID.
- Status de revisão.

#### Controles
- Busca textual.
- Filtros por coluna.
- Ordenação persistente.
- Paginação server-side.
- Exportação CSV/XLSX/PDF.
- Copiar linha.
- Abrir drawer.
- Comparar versões.
- Marcar para revisão.
- Encaminhar para incidente.

#### Drawer CRUD
- Visualizar evento.
- Ver antes/depois.
- Ver payload.
- Ver headers.
- Ver metadados.
- Ver timeline correlacionada.
- Ver anexos/evidências.
- Marcar como revisado.
- Criar caso.
- Adicionar observação.

---

### 4.3. Security Logs
Página dedicada a eventos de segurança.

#### Eventos
- Login bem-sucedido.
- Login negado.
- Logout.
- MFA validado.
- MFA falhou.
- Troca de senha.
- Reset de senha.
- Bloqueio de conta.
- Desbloqueio de conta.
- Troca de dispositivo.
- Detecção de sessão suspeita.
- Alteração de permissões.

#### Widgets
- Logins por hora.
- Falhas de autenticação.
- Contas bloqueadas.
- Dispositivos novos.
- Sessões anômalas.
- Alertas de brute force.

#### Controles
- Filtro por risco.
- Filtro por dispositivo.
- Filtro por geolocalização.
- Filtro por status.
- Filtro por MFA.
- Filtro por sessão.

---

### 4.4. API Logs
Página para auditoria de chamadas REST.

#### Datatable
Colunas:
- Timestamp.
- Método.
- Endpoint.
- Status HTTP.
- Latência.
- Usuário.
- Client ID.
- Correlation ID.
- IP.
- Unidade.
- Entidade.
- Request size.
- Response size.
- Erro.

#### Controles
- Filtrar por endpoint.
- Filtrar por status.
- Filtrar por método.
- Filtrar por latência.
- Filtrar por cliente.
- Filtrar por token.
- Ver request body.
- Ver response body.
- Reexecutar em ambiente de teste.
- Abrir incidente.

#### Charts
- Requests por minuto.
- Distribuição de status HTTP.
- Latência média por endpoint.
- Top endpoints com erro.
- Erros por integração.

---

### 4.5. Change History
Página de versionamento de registros críticos.

#### Escopo
- Usuários.
- Papéis.
- Permissões.
- Entidades.
- Unidades.
- Parâmetros.
- Configurações.
- Cadastro de terceiros.
- Regras de automação.
- Templates e layouts.

#### Drawer
- Versão atual.
- Versão anterior.
- Diff linha a linha.
- Autor da alteração.
- Motivo.
- Campo alterado.
- Valor antigo.
- Valor novo.
- Reverter versão.
- Registrar justificativa.

---

### 4.6. Incidents
Página de gestão de incidentes de auditoria.

#### Kan Ban
Colunas:
- Novo.
- Em análise.
- Em contenção.
- Em correção.
- Em validação.
- Resolvido.
- Encerrado.

#### Cards
- ID do incidente.
- Severidade.
- Tipo.
- Impacto.
- SLA.
- Responsável.
- Relacionamento com evento.
- Prazo.
- Quantidade de evidências.

#### Controles
- Criar incidente.
- Atribuir responsável.
- Alterar severidade.
- Adicionar evidências.
- Mover etapa.
- Registrar ação corretiva.
- Encerrar com justificativa.
- Reabrir.

---

### 4.7. Evidence Center
Página para armazenamento e consulta de evidências.

#### Itens
- Captura de tela.
- Arquivo PDF.
- Log bruto.
- Exportação CSV.
- Assinatura digital.
- Documento de justificativa.
- Anexos de incidente.
- Comprovantes externos.

#### Controles
- Upload.
- Download.
- Controle de retenção.
- Controle de acesso.
- Assinatura/hash.
- Versionamento.
- Vincular a incidente.
- Vincular a evento.

---

### 4.8. Rules and Policies
Página de gerenciamento das regras de auditoria.

#### Regras
- Eventos obrigatórios.
- Limiares de risco.
- Alertas por tentativas repetidas.
- Alertas por alterações sensíveis.
- Alertas por acesso fora do horário.
- Alertas por IP suspeito.
- Alertas por exportação massiva.
- Alertas por falha de integração.

#### Controles
- Ativar/desativar regra.
- Prioridade.
- Severidade.
- Escopo por entidade/unidade.
- Canal de notificação.
- Janela de tempo.
- Ação automática.
- Exceções.

---

### 4.9. Retention and Compliance
Página de gestão de retenção e conformidade.

#### Funções
- Política de retenção por tipo de evento.
- Política por categoria legal.
- Expurgo controlado.
- Anonimização.
- Mascaramento.
- Bloqueio de alteração.
- Exportação sob demanda.
- Registros para LGPD/GDPR.

#### Controles
- Criar política.
- Revisar política.
- Agendar expurgo.
- Aprovar retenção estendida.
- Exportar evidências.
- Registrar base legal.

---

## 5. Datatables por página

### 5.1. Padrão global
Toda datatable deve ter:
- Busca global.
- Filtros avançados.
- Ordenação por colunas.
- Paginação server-side.
- Estado salvo por usuário.
- Ações por linha.
- Seleção múltipla.
- Exportação.
- Colunas configuráveis.
- Resposta responsiva.

### 5.2. Colunas padrão
- ID.
- UUID.
- Data.
- Usuário.
- Entidade.
- Unidade.
- Módulo.
- Ação.
- Severidade.
- Status.
- Origem.
- IP.
- Correlation ID.
- Observação.

---

## 6. Widgets

### 6.1. Widgets executivos
- Total de eventos.
- Total de eventos críticos.
- Total de acessos suspeitos.
- Total de alterações sensíveis.
- Total de incidentes.
- Total de evidências.
- Total de regras ativas.
- Taxa de conformidade.

### 6.2. Widgets operacionais
- Eventos sem revisão.
- Casos em SLA.
- Falhas por integração.
- Alertas em aberto.
- Logs com erro.
- Sessões suspeitas.
- Ações em lote recentes.
- Exportações pendentes.

---

## 7. Charts

### 7.1. Gráficos obrigatórios
- Line chart de eventos no tempo.
- Bar chart de eventos por módulo.
- Donut chart por severidade.
- Area chart de risco acumulado.
- Heatmap de atividade por horário.
- Stacked bar por entidade/unidade.
- Sankey de origem → ação → resultado.
- Scatter de latência x volume para APIs.

### 7.2. Objetivo dos gráficos
- Identificar picos de risco.
- Encontrar módulos problemáticos.
- Medir comportamento anômalo.
- Acompanhar incidentes por período.
- Apoiar comitês de segurança e compliance.

---

## 8. Drawers CRUD

### 8.1. Drawer de evento
Campos:
- Tipo de evento.
- Data/hora.
- Usuário.
- Entidade.
- Unidade.
- Ação.
- Recurso.
- Resultado.
- Gravidade.
- IP.
- User agent.
- Correlation ID.
- Payload.
- Before.
- After.
- Observação.

### 8.2. Drawer de incidente
Campos:
- Título.
- Descrição.
- Severidade.
- Categoria.
- Status.
- Responsável.
- SLA.
- Datas.
- Evidências.
- Ações corretivas.

### 8.3. Drawer de regra
Campos:
- Nome.
- Descrição.
- Evento alvo.
- Condição.
- Operador.
- Limite.
- Frequência.
- Canal.
- Ação automática.
- Escopo.

---

## 9. Kan Ban

### 9.1. Casos de uso
- Tratamento de incidentes.
- Revisão de alertas.
- Aprovação de exceções.
- Validação de expurgo.
- Investigação de logs suspeitos.

### 9.2. Metadados do card
- Tipo.
- Severidade.
- Prazo.
- Responsável.
- Evidências.
- Tags.
- Unidade.
- Entidade.

### 9.3. Ações do card
- Arrastar e soltar.
- Comentar.
- Anexar evidências.
- Reatribuir.
- Bloquear.
- Escalar.
- Encerrar.

---

## 10. Automações

### 10.1. Regras automáticas
- Criar incidente ao exceder limiar.
- Enviar alerta ao detectar acesso suspeito.
- Registrar evidência ao exportar dados.
- Marcar revisão obrigatória para evento sensível.
- Bloquear sessão em padrão anômalo.
- Notificar compliance em falha crítica.
- Gerar resumo diário.
- Gerar relatório semanal.

### 10.2. Canais
- E-mail.
- Notificação interna.
- Webhook.
- Slack/Teams.
- SMS.
- Tarefa interna.

---

## 11. Controles

### 11.1. Controles globais
- Filtro de entidade.
- Filtro de unidade.
- Filtro de usuário.
- Filtro temporal.
- Filtro por severidade.
- Filtro por origem.
- Filtro por módulo.
- Filtro por tipo de ação.

### 11.2. Controles de segurança
- Mascarar dados sensíveis.
- Bloquear exportação sem permissão.
- Registrar toda consulta.
- Controlar acesso por RBAC.
- Aplicar escopo por entidade/unidade.
- Registrar justificativa para acesso sensível.

### 11.3. Controles de auditoria
- Aprovação de revisão.
- Aprovação de expurgo.
- Reabertura de incidente.
- Reclassificação de severidade.
- Reprocessamento de regra.
- Marcação de falso positivo.

---

## 12. Gerenciamentos

### 12.1. Gestão de perfis
- Administrador.
- Auditor.
- Compliance.
- Suporte.
- Gestor.
- Leitura restrita.

### 12.2. Gestão de políticas
- Retenção.
- Expurgo.
- Segurança.
- Revisão.
- Alertas.
- Exportação.

### 12.3. Gestão de integrações
- ERP.
- Identity provider.
- Webhooks.
- Monitoramento.
- SIEM.
- Ferramentas de BI.

### 12.4. Gestão de evidências
- Coleta.
- Assinatura.
- Versionamento.
- Retenção.
- Consulta.
- Exportação.

---

## 13. Permissões

### 13.1. Acesso por perfil
- Visualizar auditoria.
- Exportar auditoria.
- Reverter alteração.
- Criar incidente.
- Aprovar expurgo.
- Configurar regra.
- Ver payload sensível.
- Ver antes/depois.
- Atribuir responsável.
- Encerrar caso.

### 13.2. Restrições
- Usuários comuns não acessam payload sensível.
- Exportação massiva exige permissão especial.
- Reversão de alteração exige perfil elevado.
- Evidências criptografadas para dados protegidos.
- Logs com PII devem ser mascarados conforme política.

---

## 14. Requisitos técnicos

### 14.1. Backend
- PHP 8 puro.
- API REST.
- RBAC.
- Middleware de escopo por entidade/unidade.
- Logs imutáveis.
- Correlation ID por requisição.
- Hash de integridade por evento.

### 14.2. Frontend
- Tailwind CSS 4.2.
- Supabase.
- DataTables responsivos.
- Drawers assíncronos.
- Kan Ban drag-and-drop.
- Charts com amCharts 5.

### 14.3. Banco de dados
- MariaDB.
- Índices compostos por data, entidade, unidade, tipo e severidade.
- Particionamento por período quando necessário.
- Tabelas de retenção e purga.
- Colunas UUID para rastreabilidade.

---

## 15. Segurança e compliance

- Registrar toda ação crítica.
- Aplicar princípio do menor privilégio.
- Mascarar dados pessoais sempre que possível.
- Logar acesso a registros sensíveis.
- Manter trilha imutável para auditoria.
- Proteger evidências com hash.
- Suportar retenção configurável.
- Atender LGPD/GDPR com base legal e minimização.
- Registrar consentimento quando aplicável.
- Garantir exportação e eliminação sob política.

---

## 16. Páginas complementares

- Configurações de auditoria.
- Alertas e notificações.
- Relatórios executivos.
- Histórico de exportações.
- Trilha de revisão.
- Logs de retenção e expurgo.
- Configuração de integrações.
- Centro de evidências.
- Fila de incidentes.
- Painel de risco.

---

## 17. Checklist de entrega

- Dashboard funcional.
- Datatables com filtros avançados.
- Widgets por domínio.
- Charts operacionais e executivos.
- Drawers CRUD completos.
- Kan Ban para incidentes.
- Automações configuráveis.
- Controles por perfil.
- Gestão de retenção.
- Exportação segura.
- Integrações e webhooks.
- Logs de integridade.
- Conformidade LGPD/GDPR.

---

## 18. Critérios de aceite

- Cada evento crítico deve ser rastreável do início ao fim.
- Cada alteração sensível deve mostrar before/after.
- Cada incidente deve ter responsável e SLA.
- Cada exportação deve gerar log próprio.
- Cada acesso sensível deve ser auditável.
- Cada regra deve ser configurável por escopo.
- Cada evidência deve poder ser vinculada ao caso.
- O módulo deve operar com multi-entidade e multi-unidade sem vazamento de escopo.
