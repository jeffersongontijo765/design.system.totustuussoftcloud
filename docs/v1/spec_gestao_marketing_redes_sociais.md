# Spec — Gestão de Marketing e Redes Sociais Integradas

- Language Standard: Global English
## Objetivo
Definir o módulo completo de Marketing com redes sociais integradas, automação avançada, operação multicanal, governança corporativa e analytics em uma plataforma SaaS multi-empresa e multi-unidade.

## Escopo
O módulo deve cobrir planejamento, produção, agendamento, publicação, monitoramento, interação, automação, relatórios e governança de marketing e social media em um único ecossistema operacional.

## Princípios
- Operação omnichannel com visão unificada por empresa, unidade, canal e campanha.
- Execução rápida com datatables, drawers, Kanban e ações em massa.
- Automação orientada a eventos com rastreabilidade total.
- Governança com aprovação, auditoria, compliance e permissões granulares.
- Analytics acionável com widgets, charts e relatórios exportáveis.

## Páginas do módulo
### 1. Dashboard Executivo
Visão consolidada com KPIs, funil, performance por canal, alertas, aprovações pendentes e atalhos operacionais.

### 2. Campanhas
Gestão completa de campanhas de marketing, mídia paga, inbound, outbound e campanhas sociais.

### 3. Redes Sociais Integradas
Gestão de contas conectadas, publicações, interações, inbox unificada, escuta social e agendamento.

### 4. Conteúdo e Ativos
Biblioteca de criativos, templates, vídeos, artes, documentos, versões e aprovações.

### 5. Automação
Fluxos automáticos, regras, eventos, condições, ações, logs e testes.

### 6. Calendário Editorial
Planejamento de conteúdos, campanhas, posts, stories, reels, lives e eventos.

### 7. Kanban Operacional
Fluxos de produção, revisão, aprovação, publicação e follow-up.

### 8. Leads e Conversão
Gestão de leads, qualificação, atribuição, origem, status e conversão.

### 9. Relatórios e BI
Análises, comparativos, exportações, dashboards analíticos e agendamento de relatórios.

### 10. Configurações e Governança
Integrações, permissões, tags, listas, compliance, auditoria e parâmetros gerais.

## Dashboard Executivo
### Objetivo
Oferecer visão rápida de desempenho e prioridades do marketing e social media.

### Widgets obrigatórios
- Leads gerados hoje.
- Leads convertidos.
- Campanhas ativas.
- Posts agendados.
- Publicações com falha.
- Menções não respondidas.
- DMs pendentes.
- Aprovações aguardando.
- Orçamento consumido.
- ROI por canal.
- Taxa de abertura e clique.
- Engajamento por rede.

### Charts
- Linha: evolução de leads, engajamento e conversões.
- Barras: performance por canal, campanha e unidade.
- Funil: jornada do lead.
- Rosca: distribuição por origem, status e rede social.
- Área: orçamento versus gasto ao longo do tempo.
- Heatmap: engajamento por dia e horário.
- Radar: comparação de canais sociais.

### Controles
- Filtro por período.
- Filtro por empresa, unidade, usuário, canal, campanha e status.
- Comparação com período anterior.
- Atualização manual e automática.
- Exportação PDF, CSV e XLSX.

## Campanhas
### Objetivo
Gerenciar campanhas com ciclo completo de criação, aprovação, execução e análise.

### DataTable
Colunas: nome, tipo, canal, objetivo, público, orçamento, gasto, conversões, ROI, status, responsável, início, fim, atualização, ações.

### Drawer CRUD
Campos: nome, descrição, tipo, objetivo, canal, empresa, unidade, orçamento, datas, público, tags, responsáveis, mídia vinculada, UTM, aprovação.

### Controles
- Criar, editar, duplicar e arquivar.
- Pausar e reativar.
- Enviar para aprovação.
- Vincular a posts e automações.
- Ações em massa.
- Observações e anexos.

### Estados
Rascunho, Em revisão, Aprovada, Ativa, Pausada, Encerrada, Arquivada.

## Redes Sociais Integradas
### Objetivo
Centralizar contas sociais, publicações, interações e monitoramento.

### Subpáginas
- Contas conectadas.
- Inbox unificada.
- Agendador de publicações.
- Social listening.
- Comentários e menções.
- Templates e respostas rápidas.
- Performance por rede.

### DataTable — Contas Conectadas
Colunas: rede, conta, perfil, unidade, status da conexão, token, validade, permissões, última sincronização, ações.

### DataTable — Publicações
Colunas: título, rede, tipo, campanha, agendamento, status, autor, aprovador, métricas, ações.

### DataTable — Inbox Unificada
Colunas: origem, contato, mensagem, tipo, sentimento, prioridade, responsável, status, última interação, ações.

### Drawer CRUD — Publicação
Campos: título, texto, mídia, legenda, hashtags, link, rede, data/hora, recorrência, campanha, unidade, aprovação, UTM, CTA.

### Drawer CRUD — Conta
Campos: rede, nome da conta, URL, credenciais/tokens, permissões, webhook, status, unidade, observações.

### Controles
- Conectar/desconectar conta.
- Renovar token.
- Agendar, publicar agora ou salvar rascunho.
- Reaproveitar conteúdo.
- Responder comentários e DMs.
- Criar resposta rápida.
- Marcar como lido, pendente ou resolvido.
- Transferir atendimento.
- Bloquear, silenciar ou priorizar contato.

### Estados
Rascunho, Agendado, Em aprovação, Publicado, Falha, Reagendado, Arquivado.

## Conteúdo e Ativos
### Objetivo
Gerenciar toda a produção criativa reutilizável.

### DataTable
Colunas: nome, tipo, formato, tamanho, campanha, versão, status, autor, aprovação, ações.

### Controles
- Upload múltiplo.
- Pré-visualização.
- Versionamento.
- Aprovação e reprovação.
- Tags e categorias.
- Reutilização em campanhas e posts.

## Automação
### Objetivo
Permitir automações completas com eventos, condições e ações multicanal.

### DataTable
Colunas: nome, gatilho, condição, ação, canal, status, execuções, sucesso, falhas, último disparo.

### Drawer CRUD — Fluxo
Campos: nome, descrição, evento gatilho, filtros, condições, ramificações, ações, tempo de espera, retries, canal, unidade, aprovação, logs.

### Gatilhos
- Lead criado.
- Lead qualificado.
- Comentário recebido.
- DM recebida.
- Menção detectada.
- Post publicado.
- Conteúdo aprovado.
- Campanha aprovada.
- Formulário enviado.
- Link clicado.
- Compra realizada.
- Carrinho abandonado.

### Ações
- Responder automaticamente.
- Criar tarefa.
- Notificar equipe.
- Atribuir responsável.
- Mover Kanban.
- Registrar evento.
- Publicar conteúdo.
- Enviar e-mail, WhatsApp ou notificação.
- Escalar para humano.

### Controles
- Testar fluxo.
- Ativar, pausar e duplicar.
- Versionar fluxos.
- Simular eventos.
- Ver logs e auditoria.
- Aprovação antes de ativação.

### Estados
Rascunho, Em teste, Aguardando aprovação, Ativa, Pausada, Erro, Encerrada.

## Calendário Editorial
### Objetivo
Planejar publicações, campanhas e eventos por canal e unidade.

### Controles
- Visões diária, semanal e mensal.
- Arrastar e soltar itens.
- Filtrar por rede, campanha, usuário e status.
- Bloquear datas críticas.
- Vincular ao fluxo de aprovação.
- Reagendar itens com falha.

### Tipos de item
Post, story, reel, live, vídeo, campanha, evento, lembrete, ação promocional.

## Kanban Operacional
### Objetivo
Acompanhar execução de conteúdo, campanhas e aprovações.

### Colunas sugeridas
Backlog, Em produção, Em revisão, Em aprovação, Agendado, Publicado, Medindo resultados, Encerrado.

### Controles
- Drag and drop.
- WIP limit.
- Responsável por card.
- Comentários, anexos e checklist.
- Etiquetas e prioridade.
- Histórico de movimentações.

## Leads e Conversão
### Objetivo
Gerenciar captação, qualificação e conversão de leads.

### DataTable
Colunas: nome, empresa, contato, origem, campanha, score, estágio, responsável, prioridade, último contato, próximo passo, status.

### Drawer CRUD
Campos: nome, email, telefone, empresa, cargo, origem, campanha, tags, score, consentimento, observações, histórico.

### Controles
- Importar e exportar.
- Deduplicar.
- Qualificar e converter.
- Reatribuir responsável.
- Registrar interações.

## Relatórios e BI
### Objetivo
Oferecer análises estratégicas e operacionais.

### Charts
- Linha de tendência.
- Barras por canal.
- Funil de conversão.
- Rosca por rede social.
- Área de orçamento.
- Heatmap de engajamento.

### Controles
- Drill-down.
- Filtros avançados.
- Comparação de períodos.
- Exportação agendada.
- Compartilhamento por permissão.

## Configurações e Governança
### Objetivo
Garantir padronização, segurança e rastreabilidade.

### Controles
- Perfis de acesso.
- Permissões por ação e por canal.
- Trilhas de auditoria.
- Integrações externas.
- Webhooks e chaves de API.
- Lista de palavras bloqueadas.
- Regras de consentimento LGPD.
- Templates aprovados.
- Políticas de retenção.

## Regras de negócio
- Todo registro deve pertencer a empresa e unidade.
- Toda publicação precisa de canal e status de execução.
- Toda automação precisa de log e versionamento.
- Toda interação social precisa de rastreabilidade.
- Alterações críticas exigem auditoria.
- Campanhas com orçamento acima do limite exigem aprovação.
- Exclusão física deve ser evitada; usar arquivamento ou soft delete.

## Permissões sugeridas
- Visualizar.
- Criar.
- Editar.
- Excluir.
- Aprovar.
- Publicar.
- Responder interações.
- Gerenciar contas sociais.
- Executar automações.
- Gerenciar integrações.
- Exportar relatórios.
- Ver auditoria.

## Integrações sugeridas
- Instagram.
- Facebook.
- LinkedIn.
- X.
- YouTube.
- TikTok.
- WhatsApp Business.
- CRM.
- E-mail marketing.
- Analytics.
- Webhooks.
- API pública.

## Estrutura de navegação
- Dashboard.
- Campanhas.
- Redes Sociais.
- Conteúdo.
- Automação.
- Calendário.
- Kanban.
- Leads.
- Relatórios.
- Configurações.

## Critérios de aceite
- Todas as páginas principais devem existir e estar funcionalmente completas.
- Social media deve permitir contas conectadas, inbox, publicação e monitoramento.
- Automações devem cobrir eventos, condições, ações e logs.
- Widgets e charts devem refletir dados em tempo real ou quase real.
- Kanban e drawers devem permitir operação sem troca de página.
- Relatórios devem exportar e comparar períodos.

## Entregáveis esperados
- Especificação funcional completa.
- Estrutura de páginas e navegação.
- Lista de componentes UI.
- Regras de negócio e permissões.
- Fluxos de automação e status.
- Base para implementação frontend e backend.
