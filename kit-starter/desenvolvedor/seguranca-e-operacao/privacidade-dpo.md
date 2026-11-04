# Privacidade e encarregado (DPO) da plataforma

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Segurança e operação
- Domínio: plataforma (banco master), instância separada do módulo das entidades ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2.1)
- Status: detalhado; especificação da v1 absorvida integralmente (seção 13), com as correções da v2 e as decisões por padrão (seções 1 a 12)
- Fonte da v1: [spec_gestao_privacy_global_completo.md](../../../docs/v2/anexo-v1/spec_gestao_privacy_global_completo.md) (345 linhas); [spec-sub-sidebar-privacidade-lgpd.md](../../../docs/v2/anexo-v1/spec-sub-sidebar-privacidade-lgpd.md) (321 linhas)

## 1. Regra de leitura
As seções 1 a 12 prevalecem sobre a seção 13. A seção 13 é o texto integral da v1, sem corte, para que nenhum detalhe se perca. Quando a seção 13 disser algo diferente das seções 1 a 12, vale o que está nas seções 1 a 12.

## 2. Objetivo e escopo
Cumprir a LGPD como controladora (dados da própria plataforma) e como operadora (dados das entidades): inventário, bases legais, consentimento, pedidos de titular, ROPA, incidentes e painel do DPO.

## 3. Telas
- **Painel do DPO** (painel): pedidos de titulares abertos e vencidos, incidentes, consentimentos.
- **Pedidos de titulares** (datatable): protocolo, tipo, prazo, situação, resposta.
- **Registro de tratamento (ROPA)** (datatable): finalidade, base legal, categoria de dado, operador.
- **Incidentes de segurança** (kanban): registro, avaliação de risco, comunicação à ANPD.
**Títulos da v1 (referência, não são telas):**

**spec_gestao_privacy_global_completo.md**

- 1. Objetivo
- 2. Escopo
- 3. Regras globais
- 4. Legislações suportadas
  - 4.1 CCPA/CPRA
  - 4.2 COPPA
  - 4.3 PIPL
  - 4.4 GDPR
  - 4.5 LGPD
  - 4.6 PDPA
  - 4.7 APPI
  - 4.8 PIPEDA
- 5. Estrutura de páginas
  - 5.1 Dashboard principal
  - 5.2 Catálogo regulatório
  - 5.3 Consentimentos
  - 5.4 Solicitações do titular
  - 5.5 Inventário e RoPA
  - 5.6 Transferências internacionais
  - 5.7 Retenção e descarte
  - 5.8 Incidentes e violações
  - 5.9 DPO e governança
- 6. Datatable
  - 6.1 Requisitos gerais
  - 6.2 Colunas padrão por contexto
  - 6.3 Filtros obrigatórios
- 7. Widgets
  - 7.1 Widgets executivos
  - 7.2 Widgets operacionais
  - 7.3 Widgets por unidade
- 8. Charts
  - 8.1 Gráficos obrigatórios
  - 8.2 Interação
- 9. CRUD drawers
  - 9.1 Drawer de lei
  - 9.2 Drawer de consentimento
  - 9.3 Drawer de request
  - 9.4 Drawer de incidente
- 10. Kanban
  - 10.1 Colunas
  - 10.2 Uso
- 11. Automações
  - 11.1 Consentimento
  - 11.2 Requests
  - 11.3 Retenção
  - 11.4 Incidentes
  - 11.5 Revisões
- 12. Controles
  - 12.1 Controles de acesso
  - 12.2 Controles de segurança
  - 12.3 Controles de privacidade
  - 12.4 Controles de governança
- 13. Gerenciamentos
  - 13.1 Gerenciamento de leis
  - 13.2 Gerenciamento de titulares
  - 13.3 Gerenciamento de terceiros
  - 13.4 Gerenciamento de retenção
  - 13.5 Gerenciamento de templates
- 14. Estrutura de páginas completas
  - 14.1 Página Home
  - 14.2 Página Leis
  - 14.3 Página Consentimentos
  - 14.4 Página Requests
  - 14.5 Página Inventário
  - 14.6 Página Incidentes
  - 14.7 Página Retenção
  - 14.8 Página Relatórios
- 15. Critérios de aceite
- 16. Entregáveis de implementação
- 17. Observação final

**spec-sub-sidebar-privacidade-lgpd.md**

- 1. Contexto e Problema
- 2. Padrão de Referência — Supabase InnerSideMenu
  - Regras do padrão
- 3. Arquitetura de Grupos e Ordem
  - 3.1 Estrutura Completa
- 4. Tratamento do Contexto de Dashboard (Tenant / Master)
  - Implementação recomendada
- 5. Itens Novos a Implementar
- 6. Especificação de Estado dos Grupos
- 7. Ícones
- 8. Implementação em Código — Estrutura JSX
- 9. Checklist de Implementação
- 10. Rotas e Permissões por Item

## 4. Correções da v2 que prevalecem
- **O [07](../../../docs/v2/07-privacidade-lgpd.md) e o [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seções 3 a 5, prevalecem** ([19](../../../docs/v2/19-regras-modulos-3.md), seção 2: privacidade global consolidada no 07; cookies e sessões no 06).
- **DPO da plataforma** (LGPD-07, [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 7): a empresa desenvolvedora, por encarregado indicado por ela, com painel no portal do desenvolvedor. Cada entidade designa o próprio DPO.
- **Painel do DPO** ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 3.7); **pedido do titular** (seção 3.3); **ROPA** (seção 3.4); **incidentes e comunicação à ANPD** ([07](../../../docs/v2/07-privacidade-lgpd.md), seção 8).
- **Operadora:** a plataforma não usa dado de entidade fora do contrato de tratamento ([07](../../../docs/v2/07-privacidade-lgpd.md), seção 7).
- **Separação de funções:** o DPO não opera o módulo que audita ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5).

## 5. Decisões por padrão aplicadas
- Nenhuma decisão nova.

## 6. Permissões e papéis
- `platform.dpo` (papel **Encarregado** do [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5): relatório de impacto, relatório ao titular, aprovação de finalidade, painel do DPO.

## 7. Dados
- Consentimentos, pedidos de titular, ROPA e incidentes da plataforma no master. Modelos da v1 (seção 13) só onde não contradizem o [07](../../../docs/v2/07-privacidade-lgpd.md).

## 8. Integrações
- Atendimento: pedido de titular recebe protocolo (ATD-01).
- Auditoria: consultas por CPF e leituras de cadastro civil ([29](../../../docs/v2/29-auditoria.md), seção 5).

## 9. Exportação, auditoria e privacidade
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Auditoria conforme [29](../../../docs/v2/29-auditoria.md); dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md).
- Métricas de privacidade conforme [07](../../../docs/v2/07-privacidade-lgpd.md), seção 9.

## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
- Forma de designação e contato público do DPO (jurídico), no [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 7.
- Lacunas do [07](../../../docs/v2/07-privacidade-lgpd.md), seção 10.

## 13. Conteúdo integral da v1 (absorvido)

### Fonte: spec_gestao_privacy_global_completo.md

#### Privacy & Global Data Rights Module Spec

- Language Standard: Global English
##### 1. Objetivo

Este documento define o módulo completo de privacidade, direitos do titular e governança regulatória para o SaaS multi-entidade, multi-unidade e multi-usuário. O módulo deve cobrir CCPA/CPRA, COPPA, PIPL, GDPR, LGPD, PDPA, APPI e PIPEDA com uma experiência consistente, auditável e segura.

O sistema deve operar em modelo **tenant-aware** e **unit-aware**, com isolamento por entidade e por unidade, respeitando as regras globais de privacidade, consentimento, retenção, retenção legal, preferências, solicitações de titulares e incidentes.

##### 2. Escopo

O módulo deve incluir:
- Catálogo regulatório por lei, país, jurisdição, tipo de dado e aplicabilidade.
- Gestão de consentimentos, preferências e revogação.
- Portal de solicitações do titular e workflow interno.
- Retenção, minimização, anonimização, exclusão e bloqueio técnico.
- Inventário de processamentos, terceiros, transferências internacionais e bases legais.
- Auditoria, trilha de decisão, relatórios e dashboards.
- Automações e kanban operacional para governança e DSR.

##### 3. Regras globais

1. Cada tenant pode possuir múltiplas entidades e múltiplas unidades.
2. Cada unidade pode ter contexto regulatório próprio, inclusive país, idioma, moeda e políticas ativas.
3. Toda operação deve registrar tenant, entity, unit, user, actor_type, source_ip, user_agent e correlation_id.
4. Nenhum tracking não essencial pode ser executado antes de consentimento válido, quando aplicável.
5. Dados devem ser coletados com finalidade explícita, minimização e retenção configurável.
6. A exclusão deve respeitar exceções legais, retenção obrigatória e necessidade de preservação probatória.
7. Todas as ações relevantes devem gerar auditoria imutável.

##### 4. Legislações suportadas

###### 4.1 CCPA/CPRA

Cobrir direito de saber, corrigir, excluir, opt-out de venda/compartilhamento, limitação de uso de informação sensível, non-discrimination, notice at collection, GPC e prazos de resposta. O módulo deve permitir registro de categorias de PI, fontes, finalidades, destinatários e retenção por categoria. A política deve suportar regras de “Do Not Sell or Share My Personal Information”.

###### 4.2 COPPA

Cobrir coleta de dados de menores de 13 anos, consentimento parental verificável, limitação de coleta, retenção reduzida, proibição de publicidade comportamental em contexto infantil e revisão de fluxos educacionais. O sistema deve bloquear coleta indevida em produtos classificados como child-directed ou mixed audience, quando aplicável.

###### 4.3 PIPL

Cobrir base legal, transparência, consentimento separado quando necessário, regras para dados sensíveis, DPIA/PIA, transferência internacional, deveres de processadores e controle sobre decisão automatizada. O sistema deve permitir segmentação da aplicação por residentes na China e regras adicionais para exportação de dados.

###### 4.4 GDPR

Cobrir licitude, transparência, minimização, limitação de finalidade, exatidão, limitação de conservação, integridade/confidencialidade, accountability, direitos do titular e bases legais. Deve suportar DSAR/DSR, resposta em 30 dias, breach notification, DPIA, RoPA, transferências e SCC/IDTA quando aplicável.

###### 4.5 LGPD

Cobrir bases legais, direitos do titular, consentimento, revogação, eliminação, anonimização, portabilidade, revisão de decisões automatizadas, RIPD quando necessário e comunicação de incidentes. O sistema deve suportar encarregado, registro de operações e justificativa por tratamento.

###### 4.6 PDPA

Cobrir versões por jurisdição, com destaque para modelos como Singapura e Tailândia, incluindo consentimento, finalidade, acesso/correção, proteção, retenção e transferência. O módulo deve tratar o PDPA como configuração por país/tenant e não como regra genérica única.

###### 4.7 APPI

Cobrir finalidade, notificação, consentimento, dados sensíveis, compartilhamento com terceiros, transferências internacionais, pseudonimização e direitos do titular. O sistema deve permitir regras específicas por residência do titular e por estabelecimento do operador.

###### 4.8 PIPEDA

Cobrir accountability, identificação de propósitos, consentimento, limitação de coleta, uso, divulgação e retenção, precisão, salvaguardas, abertura, acesso individual e contestação. O sistema deve permitir matrizes de retenção e consentimento por finalidade.

##### 5. Estrutura de páginas

###### 5.1 Dashboard principal

Exibir status geral de conformidade por lei, score por tenant, score por unit, consentimentos ativos, solicitações em aberto, incidentes, retenções vencidas e atividades de risco. Deve conter widgets de atalho, visão executiva e gráficos comparativos.

###### 5.2 Catálogo regulatório

Lista todas as leis com aplicabilidade, status, data de revisão, responsável, escopo geográfico, tipo de dados cobertos e ações pendentes. Deve permitir ativar, desativar, justificar inaplicabilidade e revisar automaticamente por periodicidade.

###### 5.3 Consentimentos

Lista registros de consentimento, revogações, prova de consentimento, versão da política, canal de coleta, finalidade, cookies e SDKs vinculados. Deve permitir busca por titular, unidade, campanha, dispositivo e origem.

###### 5.4 Solicitações do titular

Kanban e datatable para requests de acesso, correção, exclusão, portabilidade, oposição, limitação e revogação. Deve suportar SLA, status, verificação de identidade, anexos, comentários internos e exportação.

###### 5.5 Inventário e RoPA

Registro de tratamentos, finalidades, bases legais, categorias de dados, titulares, destinatários, retenção, transferências, sistemas e subprocessadores. Deve ser editável por entidade e unidade com trilha de revisão.

###### 5.6 Transferências internacionais

Lista fluxos de dados entre países, base de transferência, cláusulas aplicáveis, destinatários, riscos e data de revisão. Deve registrar exceções e aprovações de compliance.

###### 5.7 Retenção e descarte

Painel de políticas de retenção, cronogramas, exclusão lógica, anonimização, bloqueio legal e retenções obrigatórias. Deve mostrar pendências e filas automáticas de purge.

###### 5.8 Incidentes e violações

Registro de incidentes, classificação de severidade, risco aos titulares, notificação regulatória, medidas de contenção e lições aprendidas. Deve suportar workflow de 72h para GDPR/LGPD quando aplicável e prazos específicos por lei.

###### 5.9 DPO e governança

Central de responsáveis, encarregado, contatos, aprovação de políticas, comentários jurídicos, revisões periódicas e evidências de decisão. Deve incluir tarefas, prazos e checklist por norma.

##### 6. Datatable

###### 6.1 Requisitos gerais

Toda tabela deve suportar paginação, ordenação, filtros avançados, colunas configuráveis, pesquisa global, exportação CSV/XLSX/PDF, seleção em massa e ações por linha. Devem existir estados para vazio, carregando, erro, sem permissão, registros arquivados e filtros salvos.

###### 6.2 Colunas padrão por contexto

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

###### 6.3 Filtros obrigatórios

- Por tenant, entidade e unidade.
- Por lei e jurisdição.
- Por status operacional.
- Por risco.
- Por período.
- Por responsável.
- Por tipo de titular.
- Por canal de coleta.
- Por versão da política.

##### 7. Widgets

###### 7.1 Widgets executivos

- Compliance score por lei.
- Consentimentos válidos vs revogados.
- Requests abertos por SLA.
- Incidentes por severidade.
- Retenção vencida.
- Transferências internacionais pendentes.
- Revisões vencidas.

###### 7.2 Widgets operacionais

- Queue de triagem DSR.
- Pendências de validação de identidade.
- Itens aguardando aprovação do DPO.
- Tarefas de atualização de política.
- Alertas de cookies sem consentimento.
- Processamentos sem base legal documentada.

###### 7.3 Widgets por unidade

Cada widget deve aceitar contexto unitário e mostrar ranking, alertas e tendências por unidade, com drill-down para entidade e tenant.

##### 8. Charts

###### 8.1 Gráficos obrigatórios

- Rosca de conformidade por lei.
- Linha de volume de requests por mês.
- Barras de incidentes por tipo.
- Heatmap de risco por unidade.
- Funil de solicitações por etapa.
- Área de consentimentos por origem.

###### 8.2 Interação

Todos os gráficos devem permitir filtro cruzado por tenant, entidade, unidade, período, lei e status. O clique em um elemento deve abrir o datatable já filtrado.

##### 9. CRUD drawers

###### 9.1 Drawer de lei

Campos para nome, sigla, jurisdição, aplicável, escopo, base legal, direitos cobertos, prazos, responsável e justificativa. Deve ter preview de impacto e bloqueio de salvar se faltar justificativa obrigatória.

###### 9.2 Drawer de consentimento

Campos para titular, finalidade, canal, versão da política, timestamp, prova, status, revogação e escopo. Deve mostrar histórico de alterações e origem técnica.

###### 9.3 Drawer de request

Campos para tipo, titular, identidade, prazo, status, evidências, anexos, resposta e exceções. Deve permitir atribuição, escalonamento e encerramento com justificativa.

###### 9.4 Drawer de incidente

Campos para categoria, severidade, sistemas afetados, dados impactados, titulares envolvidos, risco, notificação e medidas de contenção. Deve exigir análise de impacto e decisão jurídica.

##### 10. Kanban

###### 10.1 Colunas

- Novo.
- Em validação.
- Em execução.
- Aguardando aprovação.
- Aguardando resposta externa.
- Concluído.
- Bloqueado.

###### 10.2 Uso

O kanban deve ser usado para requests, incidentes, revisões de política, ações de remediação, aprovações de DPO e tarefas de retenção. Cada card deve carregar SLA, prioridade, lei relacionada e unidade responsável.

##### 11. Automações

###### 11.1 Consentimento

Bloquear tracking não essencial antes do opt-in. Revogar tags, pixels e SDKs ao mudar preferência. Registrar o evento e reprocessar a sessão atual quando necessário.

###### 11.2 Requests

Criar ticket automaticamente ao receber solicitação do titular. Classificar por lei, calcular prazo, atribuir fila e disparar lembretes antes do vencimento.

###### 11.3 Retenção

Executar jobs para expirar, anonimizar ou arquivar dados conforme política e exceções legais. Criar exceção automática quando houver litigação, obrigação legal ou hold administrativo.

###### 11.4 Incidentes

Abrir playbook de crise ao atingir severidade configurada. Gerar checklist de contenção, evidência, notificação e pós-incidente.

###### 11.5 Revisões

Agendar revisão periódica de políticas, bases legais, subprocessadores, transferências e inventário. Notificar responsáveis por unidade e por tenant.

##### 12. Controles

###### 12.1 Controles de acesso

- RBAC com permissões granulares.
- Escopo por tenant, entity e unit.
- Separação entre leitura, edição, aprovação e auditoria.
- Impedir edição de dados regulatórios por perfis não autorizados.

###### 12.2 Controles de segurança

- MFA para perfis sensíveis.
- Logs imutáveis.
- Criptografia em repouso e em trânsito.
- Máscara de dados sensíveis na interface.
- Timeout de sessão e reautenticação para ações críticas.

###### 12.3 Controles de privacidade

- Proof of consent.
- Opt-in/opt-out por finalidade.
- GPC quando aplicável.
- Minimized collection.
- Retenção configurável.
- Anonimização reversível apenas quando aprovada.

###### 12.4 Controles de governança

- Workflow de aprovação.
- Revisão dupla para exclusão massiva.
- Registro de justificativas.
- Versionamento de políticas.
- Assinatura eletrônica de aprovações internas.

##### 13. Gerenciamentos

###### 13.1 Gerenciamento de leis

Permitir ativar, desativar, editar aplicabilidade, registrar justificativa e revisar status de conformidade. O sistema deve mostrar o motivo da aplicabilidade por entidade e unidade.

###### 13.2 Gerenciamento de titulares

Permitir visualizar perfis, consentimentos, requests, preferências, categorias de dados, histórico e solicitações abertas. Deve existir relacionamento com múltiplas contas e múltiplos contextos de unidade.

###### 13.3 Gerenciamento de terceiros

Registrar operadores, subprocessadores, contratos, país, risco, base de transferência e revisão de DPA. Deve haver alerta de contrato vencido ou cláusula ausente.

###### 13.4 Gerenciamento de retenção

Permitir políticas por categoria de dado, finalidade, lei e unidade. Deve suportar retenção legal, retenção comercial e exclusão programada.

###### 13.5 Gerenciamento de templates

Manter templates de notice at collection, privacy policy, consent banners, request responses e incident notices por idioma e jurisdição.

##### 14. Estrutura de páginas completas

###### 14.1 Página Home

Dashboard executivo com widgets, gráficos, alertas e atalhos para requests, incidentes, políticas e retenção. Deve ter visão global e por unidade.

###### 14.2 Página Leis

Datatable principal de legislações, drawer de edição, filtros, score, justificativas e revisão. Deve permitir importação de baseline regulatório.

###### 14.3 Página Consentimentos

Lista de consentimentos, provas, revogações, origem, finalidade e ações em massa. Deve exibir alertas de consentimento expirado ou inválido.

###### 14.4 Página Requests

Kanban e datatable combinados, com SLA, atribuição, validação de identidade, resposta e exportação. Deve suportar busca por titular e por número de protocolo.

###### 14.5 Página Inventário

Gestão completa de processamento, bases legais, categorias, sistemas e subprocessadores. Deve incluir relatório exportável e histórico de revisão.

###### 14.6 Página Incidentes

Lista e fluxo de incidentes, severidade, prazos, notificações, evidências e ações corretivas. Deve suportar playbook e pós-incidente.

###### 14.7 Página Retenção

Cronogramas, filas de purge, holds e políticas por lei, entidade e unidade. Deve permitir simulação de impacto antes de executar exclusão.

###### 14.8 Página Relatórios

Relatórios por lei, unidade, entidade, período e tipo de evento. Deve exportar CSV, XLSX e PDF e registrar quem gerou cada relatório.

##### 15. Critérios de aceite

1. Todas as páginas devem funcionar com contexto multi-entidade, multi-unidade e multi-usuário.
2. Nenhum dado sensível pode ser processado sem regra explícita de proteção e auditoria.
3. Toda lei suportada deve ter aplicabilidade, justificativa e revisão.
4. Todo request deve ter trilha de status, SLA e resposta final.
5. Toda exclusão deve respeitar retenções e exceções legais.
6. Todo evento relevante deve ser auditado.
7. Todo widget e gráfico deve respeitar filtros de escopo.
8. Todo drawer e formulário deve validar permissão, contexto e obrigatoriedade legal.

##### 16. Entregáveis de implementação

- Banco de dados para leis, consentimentos, requests, inventário, incidentes, retenção e terceiros.
- API interna para compliance, consent, DSR, retention e incident handling.
- UI completa com datatable, widgets, gráficos, drawers e kanban.
- Jobs automáticos de retenção, alertas e revisão.
- Logs, auditoria e exportações.

##### 17. Observação final

A implementação deve nascer como padrão global, com configuração por jurisdição, e não como adaptação tardia. Em ambiente multi-entidade e multi-unidade, o módulo deve ser capaz de manter regras distintas por contexto sem quebrar a governança central.

### Fonte: spec-sub-sidebar-privacidade-lgpd.md

#### Spec: Refatoração do Sub-Sidebar — Módulo Privacidade & LGPD

**Projeto:** TotusTuusSoftCloud  
**Módulo:** Privacy Compliance  
**Componente:** Sub-Sidebar de Navegação  
**Template Base:** Supabase Design System (`ui-patterns/InnerSideMenu`)  
**Versão:** 1.0.0  
**Status:** Draft  
**Autor:** Spec gerado para revisão técnica  
**Data:** Junho 2026

- Language Standard: Global English
---

##### 1. Contexto e Problema

O sub-sidebar atual do módulo de Privacidade & LGPD apresenta os seguintes problemas estruturais:

- **Hierarquia visual fraca:** títulos de grupo têm pouco contraste em relação aos itens, dificultando a escaneabilidade
- **Ordem não segue o fluxo operacional:** o usuário não consegue navegar na sequência lógica (ver → configurar → operar → governar → publicar)
- **Itens faltantes:** DPIA, Transferências Internacionais e Incidentes de Privacidade estão previstos na spec do módulo mas ausentes do menu
- **Redundância de dashboards:** "Dashboard", "Tenant Dashboard" e "Master Dashboard" aparecem como itens paralelos, quando deveriam ser contextos do mesmo painel
- **Estado ativo inconsistente:** o último item "Dashboard" do grupo LGPD Masking usa estilo diferente do padrão do template
- **Largura insuficiente:** itens como "Preferências de Cookies" ficam visualmente comprimidos

---

##### 2. Padrão de Referência — Supabase InnerSideMenu

O template Supabase utiliza os seguintes componentes de `ui-patterns/InnerSideMenu`:

| Componente | Uso |
|---|---|
| `InnerSideMenuCollapsible` | Wrapper de grupo colapsável |
| `InnerSideMenuCollapsibleTrigger` | Título clicável do grupo com chevron |
| `InnerSideMenuCollapsibleContent` | Container dos itens do grupo |
| `InnerSideMenuItem` | Item de navegação individual |
| `InnerSideMenuSeparator` | Linha divisória entre grupos |
| `InnerSideBarTitle` | Título estático (não colapsável) |
| `InnerSideBarFilters` + `InnerSideBarFilterSearchInput` | Campo de busca no topo |
| `InnerSideMenuItemLoading` | Skeleton de carregamento |
| `InnerSideBarEmptyPanel` | Estado vazio do menu |

###### Regras do padrão

- `defaultOpen={true}` apenas nos 2–3 grupos mais utilizados operacionalmente
- Demais grupos iniciam fechados (`defaultOpen={false}`) para reduzir altura total
- O campo de busca usa `InnerSideBarFilterSearchInput` — não um `<input>` customizado
- `InnerSideMenuSeparator` substitui bordas horizontais CSS manuais entre grupos
- Item ativo é controlado pelo componente via `isActive` prop ou rota ativa — **não** via classe CSS manual

---

##### 3. Arquitetura de Grupos e Ordem

A nova estrutura deve seguir o fluxo operacional: **ver → configurar → operar → governar → publicar**.

###### 3.1 Estrutura Completa

```
[Campo de busca — InnerSideBarFilterSearchInput]
  placeholder: "Buscar páginas de privacidade..."

────────────────────────────────────────────

VISÃO GERAL  (InnerSideBarTitle — estático, não colapsável)
  └─ Dashboard                          /admin/privacy/dashboard

[InnerSideMenuSeparator]

CONFORMIDADE LEGAL  (defaultOpen: true)
  ├─ Catálogo de Leis                   /admin/privacy/laws
  └─ Leis Aplicáveis                    /admin/privacy/applicability

[InnerSideMenuSeparator]

INVENTÁRIO & DIREITOS  (defaultOpen: true)
  ├─ RoPA                               /admin/privacy/ropa
  ├─ DSR                                /admin/privacy/dsr
  ├─ DPIA / Avaliações de Impacto       /admin/privacy/dpia       ← NOVO
  └─ DPO / Encarregado                  /admin/privacy/dpo

[InnerSideMenuSeparator]

CONSENTIMENTOS  (defaultOpen: true)
  ├─ Consentimentos                     /admin/privacy/consents
  ├─ Preferências de Cookies            /admin/privacy/cookies
  └─ Gerenciar Sessões                  /admin/privacy/sessions

[InnerSideMenuSeparator]

TRANSFERÊNCIAS & INCIDENTES  (defaultOpen: false)
  ├─ Transferências Internacionais      /admin/privacy/transfers   ← NOVO
  └─ Incidentes de Privacidade          /admin/privacy/incidents   ← NOVO

[InnerSideMenuSeparator]

POLÍTICAS  (defaultOpen: false)
  ├─ Políticas de Privacidade           /admin/privacy/policies
  └─ Policy Builder                     /admin/privacy/policy-builder

[InnerSideMenuSeparator]

LGPD MASKING  (defaultOpen: false)
  └─ Dashboard                          /admin/privacy/masking/dashboard
```

---

##### 4. Tratamento do Contexto de Dashboard (Tenant / Master)

O menu atual expõe três itens de dashboard separados:
- Dashboard
- Tenant Dashboard
- Master Dashboard

**Decisão de design:** esses três itens representam o **mesmo Dashboard** em contextos diferentes de visão, não três páginas distintas. A solução correta no padrão Supabase é um **seletor de contexto** acima do menu, e não itens paralelos no sidebar.

###### Implementação recomendada

Acima do `InnerSideMenuCollapsible` da seção "Visão Geral", adicionar um `<Select>` ou segmented control com as opções:

```
[Contexto: ▾]  ○ Meu Tenant   ○ Tenant Selecionado   ○ Master (Global)
```

O item "Dashboard" no menu aponta para a mesma rota `/admin/privacy/dashboard`, mas a view renderizada muda conforme o contexto selecionado via query param ou store global (`?context=master`).

---

##### 5. Itens Novos a Implementar

Os itens abaixo estão especificados na `privacy-compliance-spec.md` porém **ausentes do menu atual**:

| Item | Grupo | Rota | Permissão |
|---|---|---|---|
| DPIA / Avaliações de Impacto | Inventário & Direitos | `/admin/privacy/dpia` | `privacy:dpia:read` |
| Transferências Internacionais | Transferências & Incidentes | `/admin/privacy/transfers` | `privacy:transfers:manage` |
| Incidentes de Privacidade | Transferências & Incidentes | `/admin/privacy/incidents` | `privacy:incidents:read` |

---

##### 6. Especificação de Estado dos Grupos

| Grupo | `defaultOpen` | Justificativa |
|---|---|---|
| Visão Geral | estático (sem collapsible) | Dashboard é o ponto de entrada — sempre visível |
| Conformidade Legal | `true` | Configuração frequente em implantação inicial |
| Inventário & Direitos | `true` | Operação diária principal (DSR, RoPA) |
| Consentimentos | `true` | Operação diária frequente |
| Transferências & Incidentes | `false` | Uso eventual — abre quando necessário |
| Políticas | `false` | Uso eventual — geração e publicação de docs |
| LGPD Masking | `false` | Subproduto separado — uso específico |

---

##### 7. Ícones

Manter os ícones existentes onde já definidos. Para os itens novos, usar ícones do conjunto já adotado no projeto (Lucide ou similar):

| Item Novo | Ícone sugerido |
|---|---|
| DPIA / Avaliações de Impacto | `shield-alert` |
| Transferências Internacionais | `arrow-right-left` |
| Incidentes de Privacidade | `triangle-alert` |

---

##### 8. Implementação em Código — Estrutura JSX

```jsx
import {
  InnerSideMenuCollapsible,
  InnerSideMenuCollapsibleContent,
  InnerSideMenuCollapsibleTrigger,
  InnerSideMenuItem,
  InnerSideMenuSeparator,
  InnerSideBarTitle,
  InnerSideBarFilters,
  InnerSideBarFilterSearchInput,
} from 'ui-patterns/InnerSideMenu'

export function PrivacySidebarMenu({ currentPath }) {
  return (
    <Card className="min-w-60 bg-dash-sidebar py-4 flex flex-col gap-4 h-full">

      {/* Campo de busca */}
      <div className="px-3">
        <InnerSideBarFilters>
          <InnerSideBarFilterSearchInput
            name="privacy-search"
            placeholder="Buscar páginas de privacidade..."
            aria-labelledby="Buscar páginas"
          />
        </InnerSideBarFilters>
      </div>

      {/* VISÃO GERAL — estático */}
      <div className="px-3">
        <InnerSideBarTitle>Visão Geral</InnerSideBarTitle>
        <div className="mt-1">
          <InnerSideMenuItem href="/admin/privacy/dashboard" isActive={currentPath === '/admin/privacy/dashboard'}>
            Dashboard
          </InnerSideMenuItem>
        </div>
      </div>

      <InnerSideMenuSeparator />

      {/* CONFORMIDADE LEGAL */}
      <InnerSideMenuCollapsible defaultOpen>
        <InnerSideMenuCollapsibleTrigger title="Conformidade Legal" />
        <InnerSideMenuCollapsibleContent className="mt-1">
          <InnerSideMenuItem href="/admin/privacy/laws">Catálogo de Leis</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/applicability">Leis Aplicáveis</InnerSideMenuItem>
        </InnerSideMenuCollapsibleContent>
      </InnerSideMenuCollapsible>

      <InnerSideMenuSeparator />

      {/* INVENTÁRIO & DIREITOS */}
      <InnerSideMenuCollapsible defaultOpen>
        <InnerSideMenuCollapsibleTrigger title="Inventário & Direitos" />
        <InnerSideMenuCollapsibleContent className="mt-1">
          <InnerSideMenuItem href="/admin/privacy/ropa">RoPA</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/dsr">DSR</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/dpia">DPIA / Avaliações de Impacto</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/dpo">DPO / Encarregado</InnerSideMenuItem>
        </InnerSideMenuCollapsibleContent>
      </InnerSideMenuCollapsible>

      <InnerSideMenuSeparator />

      {/* CONSENTIMENTOS */}
      <InnerSideMenuCollapsible defaultOpen>
        <InnerSideMenuCollapsibleTrigger title="Consentimentos" />
        <InnerSideMenuCollapsibleContent className="mt-1">
          <InnerSideMenuItem href="/admin/privacy/consents">Consentimentos</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/cookies">Preferências de Cookies</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/sessions">Gerenciar Sessões</InnerSideMenuItem>
        </InnerSideMenuCollapsibleContent>
      </InnerSideMenuCollapsible>

      <InnerSideMenuSeparator />

      {/* TRANSFERÊNCIAS & INCIDENTES */}
      <InnerSideMenuCollapsible defaultOpen={false}>
        <InnerSideMenuCollapsibleTrigger title="Transferências & Incidentes" />
        <InnerSideMenuCollapsibleContent className="mt-1">
          <InnerSideMenuItem href="/admin/privacy/transfers">Transferências Internacionais</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/incidents">Incidentes de Privacidade</InnerSideMenuItem>
        </InnerSideMenuCollapsibleContent>
      </InnerSideMenuCollapsible>

      <InnerSideMenuSeparator />

      {/* POLÍTICAS */}
      <InnerSideMenuCollapsible defaultOpen={false}>
        <InnerSideMenuCollapsibleTrigger title="Políticas" />
        <InnerSideMenuCollapsibleContent className="mt-1">
          <InnerSideMenuItem href="/admin/privacy/policies">Políticas de Privacidade</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/policy-builder">Policy Builder</InnerSideMenuItem>
        </InnerSideMenuCollapsibleContent>
      </InnerSideMenuCollapsible>

      <InnerSideMenuSeparator />

      {/* LGPD MASKING */}
      <InnerSideMenuCollapsible defaultOpen={false}>
        <InnerSideMenuCollapsibleTrigger title="LGPD Masking" />
        <InnerSideMenuCollapsibleContent className="mt-1">
          <InnerSideMenuItem href="/admin/privacy/masking/dashboard">Dashboard</InnerSideMenuItem>
        </InnerSideMenuCollapsibleContent>
      </InnerSideMenuCollapsible>

    </Card>
  )
}
```

---

##### 9. Checklist de Implementação

- [ ] Substituir `<input>` de busca customizado por `InnerSideBarFilterSearchInput`
- [ ] Substituir bordas CSS manuais entre grupos por `InnerSideMenuSeparator`
- [ ] Remover "Tenant Dashboard" e "Master Dashboard" do menu; implementar seletor de contexto acima
- [ ] Mover "Catálogo de Leis" para antes de "Leis Aplicáveis" no grupo Conformidade Legal
- [ ] Adicionar item **DPIA / Avaliações de Impacto** em Inventário & Direitos
- [ ] Mover **DPO** para depois de DPIA (final do grupo Inventário & Direitos)
- [ ] Criar grupo **Transferências & Incidentes** com os dois itens novos
- [ ] Garantir que `defaultOpen` seja `false` nos grupos: Transferências & Incidentes, Políticas, LGPD Masking
- [ ] Padronizar estado ativo via prop `isActive` ou detecção de rota — remover CSS manual de estado ativo
- [ ] Adicionar ícones nos itens novos: `shield-alert`, `arrow-right-left`, `triangle-alert`
- [ ] Verificar largura mínima do sub-sidebar para acomodar "Preferências de Cookies" sem truncamento
- [ ] Testar em dark mode (padrão Supabase)
- [ ] Testar collapse/expand de todos os grupos
- [ ] Verificar acessibilidade: `aria-label` nos ícones, navegação por teclado, foco visível

---

##### 10. Rotas e Permissões por Item

| Item | Rota | Permissão |
|---|---|---|
| Dashboard | `/admin/privacy/dashboard` | `privacy:dashboard:read` |
| Catálogo de Leis | `/admin/privacy/laws` | `privacy:laws:read` |
| Leis Aplicáveis | `/admin/privacy/applicability` | `privacy:applicability:manage` |
| RoPA | `/admin/privacy/ropa` | `privacy:ropa:manage` |
| DSR | `/admin/privacy/dsr` | `privacy:dsr:read` |
| DPIA / Avaliações de Impacto | `/admin/privacy/dpia` | `privacy:dpia:read` |
| DPO / Encarregado | `/admin/privacy/dpo` | `privacy:dpo:manage` |
| Consentimentos | `/admin/privacy/consents` | `privacy:consents:read` |
| Preferências de Cookies | `/admin/privacy/cookies` | `privacy:consents:manage` |
| Gerenciar Sessões | `/admin/privacy/sessions` | `privacy:consents:manage` |
| Transferências Internacionais | `/admin/privacy/transfers` | `privacy:transfers:manage` |
| Incidentes de Privacidade | `/admin/privacy/incidents` | `privacy:incidents:read` |
| Políticas de Privacidade | `/admin/privacy/policies` | `privacy:policies:manage` |
| Policy Builder | `/admin/privacy/policy-builder` | `privacy:policies:manage` |
| LGPD Masking — Dashboard | `/admin/privacy/masking/dashboard` | `privacy:masking:read` |

