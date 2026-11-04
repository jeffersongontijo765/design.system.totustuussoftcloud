# Spec — Gestão de Documentos

- Language Standard: Global English
## 1. Objetivo do módulo

O módulo de **Gestão de Documentos** deve centralizar cadastro, organização, tramitação, aprovação, assinatura digital, arquivamento e auditoria de documentos físicos e digitais, com suporte completo a fluxo operacional, segurança e conformidade.

## 2. Escopo funcional

### 2.1 Tipos de documento
- Documentos internos.
- Documentos externos.
- Contratos.
- Ofícios.
- Procurações.
- Políticas e procedimentos.
- Requisições.
- Relatórios.
- Documentos com assinatura digital.
- Documentos sem assinatura digital.

### 2.2 Ciclo de vida
- Rascunho.
- Em revisão.
- Aguardando aprovação.
- Aguardando assinatura.
- Assinado.
- Publicado.
- Arquivado.
- Expirado.
- Cancelado.
- Rejeitado.

### 2.3 Capacidades centrais
- Upload, indexação e versionamento.
- Busca avançada e filtros combinados.
- Fluxo de aprovação e assinatura.
- Controle de acesso por perfil, unidade e entidade.
- Histórico, trilha de auditoria e logs.
- Automação de tarefas e alertas.
- Gestão por Kanban e lista.
- Indicadores e dashboards.

## 3. Páginas do módulo

### 3.1 Dashboard principal
**Objetivo:** visão executiva e operacional do ambiente documental.

**Widgets:**
- Total de documentos.
- Documentos pendentes por status.
- Documentos aguardando assinatura.
- Documentos vencendo em X dias.
- Documentos com SLA estourado.
- Documentos arquivados por período.
- Volume de upload por dia.
- Taxa de aprovação.
- Taxa de rejeição.
- Assinaturas pendentes por aprovador.

**Charts:**
- Linha: volume de documentos por tempo.
- Barras: documentos por status.
- Pizza: distribuição por tipo.
- Donut: documentos com e sem assinatura digital.
- Área: evolução de assinaturas concluídas.
- Heatmap: atividade por dia da semana e hora.

**Controles:**
- Filtros por entidade, unidade, tipo, status, período, responsável e prioridade.
- Atalho para novo documento.
- Atalho para iniciar fluxo.
- Atalho para documentos vencidos.
- Exportação CSV/PDF.
- Atualização automática.

### 3.2 Lista de documentos
**Objetivo:** visualização tabular robusta para operação diária.

**Datatable com colunas:**
- Checkbox de seleção.
- Código.
- Título.
- Tipo.
- Categoria.
- Status.
- Assinatura digital.
- Versão.
- Responsável.
- Unidade.
- Entidade.
- Criado em.
- Atualizado em.
- Validade.
- Prioridade.
- SLA.
- Ações.

**Recursos do datatable:**
- Ordenação por qualquer coluna.
- Paginação.
- Busca global.
- Busca por colunas.
- Filtros salvos.
- Agrupamento por status, tipo ou unidade.
- Colunas configuráveis.
- Multi-select.
- Ações em massa.
- Exportar CSV, XLSX e PDF.
- Pin de colunas.
- Lazy loading.

**Ações por linha:**
- Visualizar.
- Editar.
- Duplicar.
- Enviar para revisão.
- Solicitar assinatura.
- Aprovar.
- Rejeitar.
- Arquivar.
- Reabrir.
- Cancelar.
- Ver histórico.
- Baixar arquivo.
- Gerenciar permissões.

### 3.3 Cadastro de documento
**Objetivo:** criar e editar documentos com controle de metadados e anexos.

**Campos principais:**
- Título.
- Código interno.
- Tipo.
- Categoria.
- Subcategoria.
- Descrição.
- Tags.
- Unidade.
- Entidade.
- Responsável.
- Solicitante.
- Data de emissão.
- Data de validade.
- Confidencialidade.
- Nível de acesso.
- Requer assinatura digital.
- Requer aprovação.
- Observações.

**Campos de arquivo:**
- Upload principal.
- Anexos complementares.
- Versão inicial.
- Formato aceito.
- Preview.

**Campos de fluxo:**
- Roteiro de aprovação.
- Roteiro de assinatura.
- Prazo por etapa.
- Prioridade.
- SLA.

### 3.4 Drawer de CRUD
**Objetivo:** criação e edição rápida sem sair da lista.

**Seções do drawer:**
- Dados básicos.
- Classificação.
- Arquivos.
- Fluxo.
- Assinatura.
- Permissões.
- Auditoria resumida.

**Comportamentos:**
- Salvar rascunho.
- Salvar e continuar editando.
- Salvar e iniciar fluxo.
- Salvar e anexar outro arquivo.
- Validação inline.
- Autosave opcional.
- Histórico de mudanças no próprio drawer.

### 3.5 Visualização detalhada
**Objetivo:** página completa do documento.

**Blocos da página:**
- Cabeçalho com título, status e ações.
- Resumo do documento.
- Preview do arquivo.
- Timeline de eventos.
- Histórico de versões.
- Aprovações.
- Assinaturas.
- Comentários.
- Anexos.
- Permissões.
- Auditoria.

**Ações no cabeçalho:**
- Editar.
- Baixar.
- Compartilhar.
- Solicitar revisão.
- Solicitar assinatura.
- Aprovar.
- Rejeitar.
- Arquivar.
- Cancelar.
- Criar nova versão.

### 3.6 Kanban
**Objetivo:** acompanhar o fluxo documental por estágio.

**Colunas sugeridas:**
- Rascunho.
- Em revisão.
- Aguardando aprovação.
- Aguardando assinatura.
- Em assinatura.
- Concluído.
- Arquivado.
- Rejeitado.

**Cards com:**
- Título.
- Tipo.
- Responsável.
- Prazo.
- Alertas.
- Ícone de assinatura.
- Indicador de prioridade.
- Última atualização.

**Interações:**
- Drag and drop.
- Filtro por responsável.
- Filtro por unidade.
- Filtro por tipo.
- Atalhos de ação no card.
- Expansão rápida do card.

### 3.7 Assinatura digital
**Objetivo:** controlar documentos que exigem assinatura eletrônica/digital.

**Funcionalidades:**
- Marcar documento como assinável.
- Definir signatários em ordem ou paralelos.
- Exibir status de cada assinatura.
- Capturar evidências da assinatura.
- Validar certificado.
- Registrar IP, data, hora e trilha.
- Bloquear edição após assinatura, conforme política.
- Reenvio de solicitação.
- Expiração de pedido de assinatura.

**Estados de assinatura:**
- Não iniciado.
- Enviado.
- Visualizado.
- Em andamento.
- Assinado.
- Recusado.
- Expirado.
- Revogado.

### 3.8 Automações
**Objetivo:** reduzir trabalho manual com regras de negócio.

**Automations examples:**
- Ao subir documento, classificar automaticamente por tipo via regra.
- Ao atingir status “Aguardando assinatura”, notificar signatários.
- Ao vencer prazo, gerar alerta e escalar.
- Ao aprovar, mover para próximo estágio.
- Ao rejeitar, devolver ao solicitante com motivo.
- Ao expirar validade, arquivar automaticamente.
- Ao criar nova versão, invalidar versão anterior.
- Ao anexar documento sensível, aplicar nível de acesso restrito.

**Tipos de automação:**
- Baseada em evento.
- Baseada em tempo.
- Baseada em condição.
- Baseada em regra de classificação.
- Baseada em SLA.

### 3.9 Controles
**Objetivo:** governança e segurança do módulo.

**Controles obrigatórios:**
- Permissões por papel.
- Permissões por entidade.
- Permissões por unidade.
- Controle de leitura, edição, exclusão, aprovação, assinatura e exportação.
- Máscara de campos sensíveis.
- Bloqueio de download em documentos restritos.
- Watermark no preview e exportação.
- Expiração de links compartilhados.
- Auditoria de acesso.
- Versionamento imutável.
- Retenção por política.
- Lock de documento em workflow.
- Dupla validação para ações críticas.

### 3.10 Gerenciamentos
**Objetivo:** administrar a estrutura documental.

**Subáreas:**
- Tipos de documento.
- Categorias e subcategorias.
- Modelos e templates.
- Tags.
- Status e transições.
- Regras de SLA.
- Níveis de confidencialidade.
- Papéis e permissões.
- Assinantes.
- Integrações externas.
- Políticas de retenção.
- Logs e auditoria.

## 4. Estrutura de páginas

### 4.1 Navegação
- Dashboard.
- Documentos.
- Kanban.
- Assinaturas.
- Aprovações.
- Categorias.
- Templates.
- Automações.
- Auditoria.
- Configurações.

### 4.2 Rotas sugeridas
- `/documentos`
- `/documentos/novo`
- `/documentos/:id`
- `/documentos/:id/editar`
- `/documentos/:id/versoes`
- `/documentos/:id/auditoria`
- `/documentos/kanban`
- `/documentos/assinaturas`
- `/documentos/aprovacoes`
- `/documentos/automacoes`
- `/documentos/configuracoes`

## 5. Widgets essenciais

- Total de documentos ativos.
- Pendências por usuário.
- Assinaturas atrasadas.
- Fluxos em andamento.
- Documentos por vencimento.
- Documentos por unidade.
- Documentos por categoria.
- Últimas movimentações.
- Alertas críticos.
- Documentos sensíveis.
- Aprovações recentes.
- Uploads recentes.

## 6. Charts recomendados

- Linha: criação de documentos ao longo do tempo.
- Barras verticais: documentos por status.
- Barras horizontais: documentos por unidade.
- Pizza: distribuição por tipo.
- Donut: com assinatura vs sem assinatura.
- Radar: desempenho por área.
- Funil: etapa de aprovação.
- Heatmap: atividade por horário.
- Área empilhada: crescimento por categoria.

## 7. Regras de negócio

- Documento com assinatura digital não pode ser editado após assinatura final, exceto nova versão autorizada.
- Documentos confidenciais exigem permissão explícita para leitura e download.
- Toda ação crítica deve ser registrada em auditoria.
- Toda mudança de status deve respeitar transições válidas.
- Documento vencido deve gerar alerta e política de tratamento.
- Documentos arquivados ficam somente leitura.
- Rejeição deve exigir motivo obrigatório.
- A exclusão física deve ser substituída por exclusão lógica, salvo política especial.
- Deve existir rastreabilidade completa de versões.

## 8. Permissões sugeridas

- `document.view`
- `document.create`
- `document.edit`
- `document.delete`
- `document.export`
- `document.archive`
- `document.approve`
- `document.reject`
- `document.sign`
- `document.manage_permissions`
- `document.manage_workflow`
- `document.manage_templates`
- `document.manage_automations`
- `document.view_audit`

## 9. Estados e feedbacks

### Estados de interface
- Loading.
- Empty state.
- Error state.
- Permission denied.
- Draft saved.
- Action success.
- Action failed.
- Syncing signature.
- File uploading.
- Processing preview.

### Feedbacks obrigatórios
- Toasts.
- Confirm dialog para ações destrutivas.
- Banner para pendências críticas.
- Badge por status.
- Alertas por SLA.

## 10. Validações

- Título obrigatório.
- Tipo obrigatório.
- Arquivo obrigatório para documentos publicados.
- Assinante obrigatório quando assinatura digital estiver ativa.
- Fluxo obrigatório quando aprovação for requerida.
- Data de validade não pode ser anterior à emissão.
- Campos sensíveis precisam de justificativa quando exigido.
- Regras de transição devem ser respeitadas.
- Upload deve validar extensão, tamanho e integridade.

## 11. Auditoria e rastreabilidade

Registrar:
- Criação.
- Edição.
- Troca de status.
- Upload e remoção de anexos.
- Visualização de documento sensível.
- Download.
- Exportação.
- Aprovação.
- Rejeição.
- Assinatura.
- Reabertura.
- Arquivamento.
- Cancelamento.
- Mudança de permissão.
- Alteração de automação.

Cada evento deve guardar:
- Usuário.
- Data/hora.
- IP.
- Unidade.
- Entidade.
- Ação.
- Dados antes/depois.
- Correlation ID.

## 12. Componentes front-end

- DataTable avançada.
- Drawer CRUD.
- Modal de confirmação.
- Modal de assinatura.
- Modal de compartilhamento.
- Preview de documento.
- Timeline.
- Kanban board.
- Badge de status.
- KPI cards.
- Chart cards.
- Tabs de detalhes.
- Comment thread.
- Permission matrix.
- Version list.
- Audit log table.
- Workflow stepper.

## 13. Integrações

- Serviço de assinatura digital.
- Storage de arquivos.
- OCR/indexação.
- Notificações por e-mail.
- Notificações in-app.
- Webhooks.
- API para integrações externas.
- SSO/IdP, se aplicável.
- Logs centralizados.
- Antivírus/scan de upload.

## 14. MVP e evolução

### MVP
- Cadastro de documentos.
- Lista com datatable.
- Preview.
- Upload.
- Versionamento.
- Aprovação simples.
- Assinatura digital básica.
- Kanban.
- Dashboard.
- Auditoria.

### Evolução
- OCR.
- Busca full-text.
- Classificação automática.
- Regras avançadas de automação.
- SLA por perfil.
- Compartilhamento externo seguro.
- Templates dinâmicos.
- Assinatura múltipla em fluxo paralelo.
- Expiração e retenção automatizada.

## 15. Critérios de aceite

- O usuário consegue criar, editar, visualizar e arquivar documentos com segurança.
- O sistema suporta documentos com e sem assinatura digital.
- A lista suporta filtros, busca, exportação e ações em massa.
- O Kanban reflete o fluxo real do documento.
- As automações disparam corretamente por evento e tempo.
- As permissões impedem acesso indevido.
- Toda ação crítica é auditável.
- Os dashboards exibem indicadores confiáveis e atualizados.

## 16. Observação de implementação

Para sua stack, esse módulo pode ser implementado com:
- Backend com API REST bem versionada.
- Banco com tabelas para documentos, versões, assinaturas, aprovações, auditoria, automações e permissões.
- Frontend com páginas modulares, drawers, tabs e componentes reutilizáveis.
- Storage separado para binários.
- Índice de busca para metadados e texto extraído.
- Camada de workflow para transições e automações.
