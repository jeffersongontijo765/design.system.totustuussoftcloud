# Privacy & Global Data Rights Module Spec

- Language Standard: Global English
## 1. Objetivo

Este documento define o módulo completo de privacidade, direitos do titular e governança regulatória para o SaaS multi-entidade, multi-unidade e multi-usuário. O módulo deve cobrir CCPA/CPRA, COPPA, PIPL, GDPR, LGPD, PDPA, APPI e PIPEDA com uma experiência consistente, auditável e segura.

O sistema deve operar em modelo **tenant-aware** e **unit-aware**, com isolamento por entidade e por unidade, respeitando as regras globais de privacidade, consentimento, retenção, retenção legal, preferências, solicitações de titulares e incidentes.

## 2. Escopo

O módulo deve incluir:
- Catálogo regulatório por lei, país, jurisdição, tipo de dado e aplicabilidade.
- Gestão de consentimentos, preferências e revogação.
- Portal de solicitações do titular e workflow interno.
- Retenção, minimização, anonimização, exclusão e bloqueio técnico.
- Inventário de processamentos, terceiros, transferências internacionais e bases legais.
- Auditoria, trilha de decisão, relatórios e dashboards.
- Automações e kanban operacional para governança e DSR.

## 3. Regras globais

1. Cada tenant pode possuir múltiplas entidades e múltiplas unidades.
2. Cada unidade pode ter contexto regulatório próprio, inclusive país, idioma, moeda e políticas ativas.
3. Toda operação deve registrar tenant, entity, unit, user, actor_type, source_ip, user_agent e correlation_id.
4. Nenhum tracking não essencial pode ser executado antes de consentimento válido, quando aplicável.
5. Dados devem ser coletados com finalidade explícita, minimização e retenção configurável.
6. A exclusão deve respeitar exceções legais, retenção obrigatória e necessidade de preservação probatória.
7. Todas as ações relevantes devem gerar auditoria imutável.

## 4. Legislações suportadas

### 4.1 CCPA/CPRA

Cobrir direito de saber, corrigir, excluir, opt-out de venda/compartilhamento, limitação de uso de informação sensível, non-discrimination, notice at collection, GPC e prazos de resposta. O módulo deve permitir registro de categorias de PI, fontes, finalidades, destinatários e retenção por categoria. A política deve suportar regras de “Do Not Sell or Share My Personal Information”.

### 4.2 COPPA

Cobrir coleta de dados de menores de 13 anos, consentimento parental verificável, limitação de coleta, retenção reduzida, proibição de publicidade comportamental em contexto infantil e revisão de fluxos educacionais. O sistema deve bloquear coleta indevida em produtos classificados como child-directed ou mixed audience, quando aplicável.

### 4.3 PIPL

Cobrir base legal, transparência, consentimento separado quando necessário, regras para dados sensíveis, DPIA/PIA, transferência internacional, deveres de processadores e controle sobre decisão automatizada. O sistema deve permitir segmentação da aplicação por residentes na China e regras adicionais para exportação de dados.

### 4.4 GDPR

Cobrir licitude, transparência, minimização, limitação de finalidade, exatidão, limitação de conservação, integridade/confidencialidade, accountability, direitos do titular e bases legais. Deve suportar DSAR/DSR, resposta em 30 dias, breach notification, DPIA, RoPA, transferências e SCC/IDTA quando aplicável.

### 4.5 LGPD

Cobrir bases legais, direitos do titular, consentimento, revogação, eliminação, anonimização, portabilidade, revisão de decisões automatizadas, RIPD quando necessário e comunicação de incidentes. O sistema deve suportar encarregado, registro de operações e justificativa por tratamento.

### 4.6 PDPA

Cobrir versões por jurisdição, com destaque para modelos como Singapura e Tailândia, incluindo consentimento, finalidade, acesso/correção, proteção, retenção e transferência. O módulo deve tratar o PDPA como configuração por país/tenant e não como regra genérica única.

### 4.7 APPI

Cobrir finalidade, notificação, consentimento, dados sensíveis, compartilhamento com terceiros, transferências internacionais, pseudonimização e direitos do titular. O sistema deve permitir regras específicas por residência do titular e por estabelecimento do operador.

### 4.8 PIPEDA

Cobrir accountability, identificação de propósitos, consentimento, limitação de coleta, uso, divulgação e retenção, precisão, salvaguardas, abertura, acesso individual e contestação. O sistema deve permitir matrizes de retenção e consentimento por finalidade.

## 5. Estrutura de páginas

### 5.1 Dashboard principal

Exibir status geral de conformidade por lei, score por tenant, score por unit, consentimentos ativos, solicitações em aberto, incidentes, retenções vencidas e atividades de risco. Deve conter widgets de atalho, visão executiva e gráficos comparativos.

### 5.2 Catálogo regulatório

Lista todas as leis com aplicabilidade, status, data de revisão, responsável, escopo geográfico, tipo de dados cobertos e ações pendentes. Deve permitir ativar, desativar, justificar inaplicabilidade e revisar automaticamente por periodicidade.

### 5.3 Consentimentos

Lista registros de consentimento, revogações, prova de consentimento, versão da política, canal de coleta, finalidade, cookies e SDKs vinculados. Deve permitir busca por titular, unidade, campanha, dispositivo e origem.

### 5.4 Solicitações do titular

Kanban e datatable para requests de acesso, correção, exclusão, portabilidade, oposição, limitação e revogação. Deve suportar SLA, status, verificação de identidade, anexos, comentários internos e exportação.

### 5.5 Inventário e RoPA

Registro de tratamentos, finalidades, bases legais, categorias de dados, titulares, destinatários, retenção, transferências, sistemas e subprocessadores. Deve ser editável por entidade e unidade com trilha de revisão.

### 5.6 Transferências internacionais

Lista fluxos de dados entre países, base de transferência, cláusulas aplicáveis, destinatários, riscos e data de revisão. Deve registrar exceções e aprovações de compliance.

### 5.7 Retenção e descarte

Painel de políticas de retenção, cronogramas, exclusão lógica, anonimização, bloqueio legal e retenções obrigatórias. Deve mostrar pendências e filas automáticas de purge.

### 5.8 Incidentes e violações

Registro de incidentes, classificação de severidade, risco aos titulares, notificação regulatória, medidas de contenção e lições aprendidas. Deve suportar workflow de 72h para GDPR/LGPD quando aplicável e prazos específicos por lei.

### 5.9 DPO e governança

Central de responsáveis, encarregado, contatos, aprovação de políticas, comentários jurídicos, revisões periódicas e evidências de decisão. Deve incluir tarefas, prazos e checklist por norma.

## 6. Datatable

### 6.1 Requisitos gerais

Toda tabela deve suportar paginação, ordenação, filtros avançados, colunas configuráveis, pesquisa global, exportação CSV/XLSX/PDF, seleção em massa e ações por linha. Devem existir estados para vazio, carregando, erro, sem permissão, registros arquivados e filtros salvos.

### 6.2 Colunas padrão por contexto

- ID interno.
- Código externo.
- Tenant.
- Entidade.
- Unidade.
- Lei/regulação.
- Status.
- Responsável.
- Data de criação.
- Última revisão.
- Próxima revisão.
- SLA.
- Risco.
- Ações.

### 6.3 Filtros obrigatórios

- Por tenant, entidade e unidade.
- Por lei e jurisdição.
- Por status operacional.
- Por risco.
- Por período.
- Por responsável.
- Por tipo de titular.
- Por canal de coleta.
- Por versão da política.

## 7. Widgets

### 7.1 Widgets executivos

- Compliance score por lei.
- Consentimentos válidos vs revogados.
- Requests abertos por SLA.
- Incidentes por severidade.
- Retenção vencida.
- Transferências internacionais pendentes.
- Revisões vencidas.

### 7.2 Widgets operacionais

- Queue de triagem DSR.
- Pendências de validação de identidade.
- Itens aguardando aprovação do DPO.
- Tarefas de atualização de política.
- Alertas de cookies sem consentimento.
- Processamentos sem base legal documentada.

### 7.3 Widgets por unidade

Cada widget deve aceitar contexto unitário e mostrar ranking, alertas e tendências por unidade, com drill-down para entidade e tenant.

## 8. Charts

### 8.1 Gráficos obrigatórios

- Rosca de conformidade por lei.
- Linha de volume de requests por mês.
- Barras de incidentes por tipo.
- Heatmap de risco por unidade.
- Funil de solicitações por etapa.
- Área de consentimentos por origem.

### 8.2 Interação

Todos os gráficos devem permitir filtro cruzado por tenant, entidade, unidade, período, lei e status. O clique em um elemento deve abrir o datatable já filtrado.

## 9. CRUD drawers

### 9.1 Drawer de lei

Campos para nome, sigla, jurisdição, aplicável, escopo, base legal, direitos cobertos, prazos, responsável e justificativa. Deve ter preview de impacto e bloqueio de salvar se faltar justificativa obrigatória.

### 9.2 Drawer de consentimento

Campos para titular, finalidade, canal, versão da política, timestamp, prova, status, revogação e escopo. Deve mostrar histórico de alterações e origem técnica.

### 9.3 Drawer de request

Campos para tipo, titular, identidade, prazo, status, evidências, anexos, resposta e exceções. Deve permitir atribuição, escalonamento e encerramento com justificativa.

### 9.4 Drawer de incidente

Campos para categoria, severidade, sistemas afetados, dados impactados, titulares envolvidos, risco, notificação e medidas de contenção. Deve exigir análise de impacto e decisão jurídica.

## 10. Kanban

### 10.1 Colunas

- Novo.
- Em validação.
- Em execução.
- Aguardando aprovação.
- Aguardando resposta externa.
- Concluído.
- Bloqueado.

### 10.2 Uso

O kanban deve ser usado para requests, incidentes, revisões de política, ações de remediação, aprovações de DPO e tarefas de retenção. Cada card deve carregar SLA, prioridade, lei relacionada e unidade responsável.

## 11. Automações

### 11.1 Consentimento

Bloquear tracking não essencial antes do opt-in. Revogar tags, pixels e SDKs ao mudar preferência. Registrar o evento e reprocessar a sessão atual quando necessário.

### 11.2 Requests

Criar ticket automaticamente ao receber solicitação do titular. Classificar por lei, calcular prazo, atribuir fila e disparar lembretes antes do vencimento.

### 11.3 Retenção

Executar jobs para expirar, anonimizar ou arquivar dados conforme política e exceções legais. Criar exceção automática quando houver litigação, obrigação legal ou hold administrativo.

### 11.4 Incidentes

Abrir playbook de crise ao atingir severidade configurada. Gerar checklist de contenção, evidência, notificação e pós-incidente.

### 11.5 Revisões

Agendar revisão periódica de políticas, bases legais, subprocessadores, transferências e inventário. Notificar responsáveis por unidade e por tenant.

## 12. Controles

### 12.1 Controles de acesso

- RBAC com permissões granulares.
- Escopo por tenant, entity e unit.
- Separação entre leitura, edição, aprovação e auditoria.
- Impedir edição de dados regulatórios por perfis não autorizados.

### 12.2 Controles de segurança

- MFA para perfis sensíveis.
- Logs imutáveis.
- Criptografia em repouso e em trânsito.
- Máscara de dados sensíveis na interface.
- Timeout de sessão e reautenticação para ações críticas.

### 12.3 Controles de privacidade

- Proof of consent.
- Opt-in/opt-out por finalidade.
- GPC quando aplicável.
- Minimized collection.
- Retenção configurável.
- Anonimização reversível apenas quando aprovada.

### 12.4 Controles de governança

- Workflow de aprovação.
- Revisão dupla para exclusão massiva.
- Registro de justificativas.
- Versionamento de políticas.
- Assinatura eletrônica de aprovações internas.

## 13. Gerenciamentos

### 13.1 Gerenciamento de leis

Permitir ativar, desativar, editar aplicabilidade, registrar justificativa e revisar status de conformidade. O sistema deve mostrar o motivo da aplicabilidade por entidade e unidade.

### 13.2 Gerenciamento de titulares

Permitir visualizar perfis, consentimentos, requests, preferências, categorias de dados, histórico e solicitações abertas. Deve existir relacionamento com múltiplas contas e múltiplos contextos de unidade.

### 13.3 Gerenciamento de terceiros

Registrar operadores, subprocessadores, contratos, país, risco, base de transferência e revisão de DPA. Deve haver alerta de contrato vencido ou cláusula ausente.

### 13.4 Gerenciamento de retenção

Permitir políticas por categoria de dado, finalidade, lei e unidade. Deve suportar retenção legal, retenção comercial e exclusão programada.

### 13.5 Gerenciamento de templates

Manter templates de notice at collection, privacy policy, consent banners, request responses e incident notices por idioma e jurisdição.

## 14. Estrutura de páginas completas

### 14.1 Página Home

Dashboard executivo com widgets, gráficos, alertas e atalhos para requests, incidentes, políticas e retenção. Deve ter visão global e por unidade.

### 14.2 Página Leis

Datatable principal de legislações, drawer de edição, filtros, score, justificativas e revisão. Deve permitir importação de baseline regulatório.

### 14.3 Página Consentimentos

Lista de consentimentos, provas, revogações, origem, finalidade e ações em massa. Deve exibir alertas de consentimento expirado ou inválido.

### 14.4 Página Requests

Kanban e datatable combinados, com SLA, atribuição, validação de identidade, resposta e exportação. Deve suportar busca por titular e por número de protocolo.

### 14.5 Página Inventário

Gestão completa de processamento, bases legais, categorias, sistemas e subprocessadores. Deve incluir relatório exportável e histórico de revisão.

### 14.6 Página Incidentes

Lista e fluxo de incidentes, severidade, prazos, notificações, evidências e ações corretivas. Deve suportar playbook e pós-incidente.

### 14.7 Página Retenção

Cronogramas, filas de purge, holds e políticas por lei, entidade e unidade. Deve permitir simulação de impacto antes de executar exclusão.

### 14.8 Página Relatórios

Relatórios por lei, unidade, entidade, período e tipo de evento. Deve exportar CSV, XLSX e PDF e registrar quem gerou cada relatório.

## 15. Critérios de aceite

1. Todas as páginas devem funcionar com contexto multi-entidade, multi-unidade e multi-usuário.
2. Nenhum dado sensível pode ser processado sem regra explícita de proteção e auditoria.
3. Toda lei suportada deve ter aplicabilidade, justificativa e revisão.
4. Todo request deve ter trilha de status, SLA e resposta final.
5. Toda exclusão deve respeitar retenções e exceções legais.
6. Todo evento relevante deve ser auditado.
7. Todo widget e gráfico deve respeitar filtros de escopo.
8. Todo drawer e formulário deve validar permissão, contexto e obrigatoriedade legal.

## 16. Entregáveis de implementação

- Banco de dados para leis, consentimentos, requests, inventário, incidentes, retenção e terceiros.
- API interna para compliance, consent, DSR, retention e incident handling.
- UI completa com datatable, widgets, gráficos, drawers e kanban.
- Jobs automáticos de retenção, alertas e revisão.
- Logs, auditoria e exportações.

## 17. Observação final

A implementação deve nascer como padrão global, com configuração por jurisdição, e não como adaptação tardia. Em ambiente multi-entidade e multi-unidade, o módulo deve ser capaz de manter regras distintas por contexto sem quebrar a governança central.
