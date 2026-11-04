# Spec — Gestão Completa de Bancos de Dados

- Language Standard: Global English
## 1. Objetivo
Construir um módulo enterprise para gestão completa de bancos de dados, cobrindo inventário, conexão, modelagem, visualização, operações, segurança, auditoria, backup, restore, migração, replicação, observabilidade e automação, com suporte a múltiplos engines.

## 2. Visão do Produto
A plataforma deve oferecer uma experiência unificada para administração de bancos relacionais e não relacionais, com um núcleo comum de funcionalidades e adaptadores específicos por engine. O foco é permitir operação segura em produção, com governança e rastreabilidade completas.

## 3. Escopo Funcional
### 3.1 Inventário e Descoberta
- Cadastro de instâncias, bancos, schemas, collections, tabelas, views, índices, triggers, functions, procedures, policies, jobs e extensões.
- Descoberta automática por introspecção do engine.
- Atualização incremental do catálogo.
- Detecção de drift entre estrutura real e estrutura esperada.

### 3.2 Conectividade
- Teste de conexão.
- Armazenamento seguro de credenciais.
- Rotação de segredos.
- Classificação por ambiente, tenant e criticidade.
- Pool de conexões e health-check.

### 3.3 SQL Console e Operação de Dados
- Execução de SQL com histórico, snippets e favoritos.
- Query runner com explain plan quando suportado.
- Browse de dados com paginação e filtros.
- Edição controlada com trilha de auditoria.
- Importação e exportação em CSV, SQL, JSON e formatos suportados pelo engine.

### 3.4 Migrações
- Criação, revisão, versionamento e execução de migrations.
- Diff entre versões de schema.
- Aprovação de mudanças.
- Rollback com checksum e rastreabilidade.
- Bloqueio de alterações manuais fora do pipeline aprovado.

### 3.5 Backups e Restore
- Backup manual e agendado.
- Políticas de retenção.
- Restore total e parcial.
- Validação periódica de restaurabilidade.
- Suporte a point-in-time recovery quando o engine oferecer.

### 3.6 Replicação e Alta Disponibilidade
- Visão de primário, réplicas e lag.
- Roteamento de leitura e escrita.
- Monitoramento de failover.
- Status de sincronização.

### 3.7 Segurança e Governança
- RBAC por papel e por tenant.
- RLS para bancos e schemas compatíveis.
- Máscara de dados sensíveis.
- Aprovação para ações críticas.
- Logs imutáveis e trilha de auditoria.

### 3.8 Monitoramento e Alertas
- Tamanho por banco, schema e tabela.
- Queries lentas.
- Locks e deadlocks.
- Uso de CPU, RAM e IO quando exposto pelo provider.
- Alertas por limiar e por evento.

## 4. Suporte a Tipos de Banco
### 4.1 Relacionais
- PostgreSQL
- MySQL
- MariaDB
- SQL Server
- Oracle
- SQLite

### 4.2 Não Relacionais
- MongoDB
- Redis
- Outros via adapter

### 4.3 Estratégia de Adapters
Cada engine deve expor capabilities, como:
- suporta schema;
- suporta triggers;
- suporta functions;
- suporta constraints;
- suporta backups nativos;
- suporta RLS;
- suporta replicação;
- suporta visualização ER.

## 5. Flow do Visualizador de Esquemas
### 5.1 Objetivo
Permitir compreensão visual do banco, destacando relações, dependências, impacto de alterações e áreas críticas.

### 5.2 Entradas
- Instância selecionada.
- Schema ou domínio.
- Modo de visualização.
- Filtros por tipo de objeto.

### 5.3 Nós do Grafo
- Tabelas
- Views
- Materialized views
- Collections
- Índices
- Triggers
- Functions
- Procedures
- Policies
- Extensions
- Jobs

### 5.4 Arestas do Grafo
- Foreign keys
- Dependências lógicas
- Uso por views
- Uso por triggers
- Dependências de migration
- Relações de segurança

### 5.5 Interações
- Zoom, pan e auto-layout.
- Busca de objetos.
- Filtros por schema, tenant, tipo e status.
- Seleção de subgrafo.
- Highlight de caminho crítico.
- Exportação em PNG, SVG e PDF.
- Diff visual entre snapshots.

### 5.6 Modo de Navegação
1. Selecionar instância.
2. Selecionar schema.
3. Carregar grafo.
4. Aplicar filtros.
5. Explorar relações.
6. Abrir painel lateral.
7. Exportar ou comparar.

## 6. Entidades Principais
### 6.1 DatabaseInstance
- id
- name
- engine
- version
- environment
- host
- port
- status
- tags
- created_at
- updated_at

### 6.2 DatabaseObject
- id
- instance_id
- schema_name
- object_type
- object_name
- definition_hash
- owner
- status
- metadata

### 6.3 SchemaSnapshot
- id
- instance_id
- version
- checksum
- source
- created_at
- created_by

### 6.4 Migration
- id
- version
- name
- checksum
- status
- applied_at
- reverted_at
- approved_by

### 6.5 BackupJob
- id
- instance_id
- type
- status
- started_at
- finished_at
- storage_location
- retention_days

### 6.6 AuditLog
- id
- actor
- action
- resource_type
- resource_id
- before
- after
- ip
- user_agent
- created_at

## 7. Regras de Negócio
- Toda alteração estrutural deve ser versionada.
- Toda mudança em produção deve passar por aprovação.
- Toda ação sensível deve ser auditada.
- Todo backup deve ter política de retenção.
- Toda restauração deve ser validada.
- Todo acesso cross-tenant deve ser explicitamente autorizado.
- Toda policy de segurança deve ser documentada.

## 8. APIs Sugeridas
- GET /databases
- POST /databases
- GET /databases/:id
- POST /databases/:id/test-connection
- GET /catalog
- GET /schema-graph
- POST /schema-graph/diff
- POST /migrations
- POST /migrations/:id/approve
- POST /backups
- POST /restores
- GET /audit
- GET /monitoring/overview
- GET /monitoring/slow-queries
- GET /monitoring/locks

## 9. Segurança
- TLS obrigatório quando suportado.
- Credenciais armazenadas em cofre seguro.
- Logs com redaction para dados sensíveis.
- Permissões mínimas por papel.
- Confirmação dupla em ações destrutivas.
- Separação entre leitura e administração.

## 10. Observabilidade
- Métricas de tamanho, crescimento e fragmentação.
- Queries lentas e planos de execução.
- Locks, wait events e deadlocks.
- Erros por conexão e por engine.
- Status de backup e restore.
- Lag de replicação.

## 11. Critérios de Aceite
- Suporte a múltiplos engines sem duplicar a UX.
- Visualizador de esquema funcional com filtros e exportação.
- Migração com diff, aprovação e rollback.
- Backup e restore com validação.
- Auditoria completa das ações críticas.
- RBAC e isolamento por tenant funcionando.

## 12. Checklist de Implementação
- [ ] Camada de adapters por engine.
- [ ] Catálogo unificado de objetos.
- [ ] SQL console.
- [ ] Browse e edição de dados.
- [ ] Migrações com versionamento.
- [ ] Backup e restore.
- [ ] Visualizador de esquemas.
- [ ] RBAC e RLS.
- [ ] Auditoria e logs.
- [ ] Monitoramento e alertas.
- [ ] Exportação e importação.
- [ ] Documentação técnica.

## 13. Acompanhamentos
### 13.1 Acompanhamento de Schema
- Snapshot por ambiente.
- Comparação de drift.
- Histórico de alterações.
- Aprovação de mudanças críticas.

### 13.2 Acompanhamento de Backup
- Último backup válido.
- Percentual de sucesso.
- Tempo médio de execução.
- Retenção e expiração.
- Teste de restore periódico.

### 13.3 Acompanhamento de Performance
- Queries mais lentas.
- Índices ausentes.
- Tabelas mais acessadas.
- Crescimento anormal.
- Uso de recursos por instância.

### 13.4 Acompanhamento de Segurança
- Tentativas de acesso negadas.
- Mudanças de permissão.
- Ações administrativas.
- Eventos críticos por tenant.
- Integridade das políticas.

### 13.5 Acompanhamento de Operação
- Status das instâncias.
- Filas de jobs.
- Erros de conexão.
- Reprocessamentos.
- Incidentes e SLA.

## 14. Observação Final
O módulo deve ser pensado como um sistema de governança e operação, não apenas como um editor de tabelas. O visualizador de esquemas e os acompanhamentos operacionais são parte central da experiência, porque transformam o banco em um ativo monitorado, compreensível e controlado.
