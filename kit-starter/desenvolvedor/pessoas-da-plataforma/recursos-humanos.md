# Recursos humanos da empresa

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Pessoas da plataforma
- Domínio: plataforma (banco master), instância separada do módulo das entidades ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2.1)
- Status: detalhado; especificação da v1 absorvida integralmente (seção 13), com as correções da v2 e as decisões por padrão (seções 1 a 12)
- Fonte da v1: [spec_gestao_rh_completo.md](../../../docs/v2/anexo-v1/spec_gestao_rh_completo.md) (1319 linhas)

## 1. Regra de leitura
As seções 1 a 12 prevalecem sobre a seção 13. A seção 13 é o texto integral da v1, sem corte, para que nenhum detalhe se perca. Quando a seção 13 disser algo diferente das seções 1 a 12, vale o que está nas seções 1 a 12.

## 2. Objetivo e escopo
Gerir recrutamento, onboarding, avaliação de desempenho, clima, treinamento e movimentação interna dos funcionários da própria empresa desenvolvedora.

## 3. Telas
- **Recrutamento** (kanban): vaga, etapas, candidatos.
- **Avaliações de desempenho** (datatable): ciclo, colaborador, situação, consolidação.
**Títulos da v1 (referência, não são telas):**

- 1.1 Objetivo
- 1.2 Escopo funcional
- 1.3 Princípios de arquitetura
- 2.1 Metas operacionais
- 2.2 Metas técnicas
- 3.1 Perfis principais
- 3.2 Regras de visibilidade
- 3.3 Regras especiais
- 3.4 Matriz de permissão mínima
- 4.1 Menu lateral
- 4.2 Navegação interna por páginas
- 5.1 Objetivo
- 5.2 Widgets obrigatórios
- 5.3 Charts obrigatórios
- 5.4 Blocos operacionais
- 5.5 Filtros do dashboard
- 6.1 Objetivo
- 6.2 Datatable principal
- 6.3 Recursos da datatable
- 6.4 Filtros avançados
- 6.5 Ações por linha
- 7.1 Estrutura da página
- 7.2 Cards da aba Resumo
- 7.3 Controles necessários
- 8.1 Páginas
- 8.2 Datatables
  - Departamentos
  - Cargos
  - Organograma
- 8.3 Drawers de CRUD
- 9.1 Páginas
- 9.2 Datatable de vagas
- 9.3 Kanban de recrutamento
- 9.4 Drawers de recrutamento
- 10.1 Objetivo
- 10.2 Páginas
- 10.3 Kanban de onboarding
- 10.4 Controles
- 11.1 Páginas
- 11.2 Datatable de frequência
- 11.3 Controles
- 12.1 Páginas
- 12.2 Datatable
- 12.3 Controles
- 13.1 Páginas
- 13.2 Datatable de avaliações
- 13.3 Drawers
- 13.4 Charts
- 14.1 Páginas
- 14.2 Datatable
- 14.3 Controles
- 15.1 Tipos documentais
- 15.2 Datatable
- 15.3 Controles
- 16.1 Tipos
- 16.2 Página de movimentações
- 16.3 Fluxo
- 17.1 Páginas
- 17.2 Kanban de desligamento
- 17.3 Controles
- 18.1 Tipos de solicitação
- 18.2 Página
- 18.3 Controles
- 19.1 Indicadores estratégicos
- 19.2 Páginas analíticas
- 19.3 Recursos
- 20.1 Estrutura padrão
- 20.2 Drawers obrigatórios do módulo
- 20.3 Campos comuns
- 21.1 Kanbans previstos
- 21.2 Controles globais do Kanban
- 22.1 Gatilhos automáticos
- 22.2 Automações por agenda
- 22.3 Automações por regra
- 23.1 Controles obrigatórios
- 23.2 LGPD e privacidade
- 23.3 Auditoria
- 24.1 Cadastros mestres
- 24.2 Configurações do módulo
- 25.1 Lista principal de páginas
- 25.2 Padrão visual de cada página
- 26.1 Comportamentos obrigatórios
- 26.2 Toolbar padrão
- 27.1 Tipos de widgets
- 27.2 Regras visuais
- 28.1 Biblioteca
- 28.2 Regras
- 28.3 Charts mínimos por área
- 29.1 Exemplos principais
- 29.2 Regras de API
- 30.1 Status de colaborador
- 30.2 Status de vaga
- 30.3 Status de solicitação
- 30.4 Status de documento
- 31.1 Colaborador
- 31.2 Vaga
- 31.3 Movimentação
- 32.1 Funcional
- 32.2 Segurança
- 32.3 UX/UI
- 33.1 Fase 1
- 33.2 Fase 2
- 33.3 Fase 3

## 4. Correções da v2 que prevalecem
- **Módulo separado de Pessoas** (HCM-01 do [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 11): RH é dono de recrutamento, onboarding, avaliação, clima e movimentação interna; não é dono de folha, admissão no eSocial nem cadastro civil. Candidato contratado passa para Pessoas por referência, sem cópia de dado.
- **Currículo de candidato não contratado** (HCM-09): guardado por prazo fixo e depois excluído; o candidato é informado no envio; nenhum uso fora do processo em que se candidatou.
- **Sem acesso a dado de saúde:** o RH não vê CID, diagnóstico nem prontuário em nenhuma tela ou API ([39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 5.1).
- **Avaliação e clima:** formulários pelo motor de formulários e pesquisas ([41](../../../docs/v2/41-formularios-e-pesquisas.md)).
- **Perfis da v1:** substituídos pelos papéis da seção 6 desta ficha.
- **Instância da empresa:** sem filtro de unidade ou entidade.

## 5. Decisões por padrão aplicadas
- Prazo de guarda do currículo (HCM-09): valor jurídico, configurado como parâmetro obrigatório; sem prazo configurado, o recrutamento não recebe currículo (critério 3 do [80](../../../docs/v2/80-decisoes-por-padrao.md)).

## 6. Permissões e papéis
- `platform.hr` (RH do [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5, no escopo do HCM-01; nível 1): recrutamento, onboarding, avaliação, clima, treinamento.
- Aprovação de movimentação interna e de contratação: `platform.manager` ou gestor da área (nível 2 ou acima), nunca o próprio solicitante ([78](../../../docs/v2/78-permissoes-e-papeis.md), seção 2.2).
- Funcionário: o próprio plano de desenvolvimento e treinamentos.

## 7. Dados
- Modelo de dados da v1 (seção 13), com `tenant_id` e referência à pessoa por `person_id`.

## 8. Integrações
- Pessoas (DP): contratação passa a pessoa por referência.
- Motor de formulários ([41](../../../docs/v2/41-formularios-e-pesquisas.md)): avaliações e pesquisas de clima.
- Notificações: etapas do processo seletivo e do onboarding.

## 9. Exportação, auditoria e privacidade
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Auditoria conforme [29](../../../docs/v2/29-auditoria.md); dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md).
- Dados de candidato: finalidade restrita ao processo seletivo e exclusão no fim do prazo (HCM-09).

## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
- HCM-09: valor do prazo de guarda do currículo (jurídico), no [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 9.

## 13. Conteúdo integral da v1 (absorvido)

### SPEC — Módulo Recursos Humanos
Versão: 1.0  
Status: Draft funcional completo  
Módulo: Human Resources / HR / Workforce Management  
Contexto: SaaS multi-entidade, multi-unidade e multi-usuário, com segregação por tenant, controle por RBAC, trilha de auditoria, APIs seguras e interface administrativa padrão enterprise. [cite:1][cite:2][cite:7][web:18][web:21]

- Language Standard: Global English
---

### 1. Visão Geral

#### 1.1 Objetivo
O módulo de Recursos Humanos será responsável por centralizar o ciclo de vida do colaborador dentro da plataforma, desde requisição de vaga, recrutamento, onboarding, cadastro funcional, alocações, documentos, jornada, férias, afastamentos, desempenho, treinamentos, movimentações internas, desligamento e indicadores gerenciais. [web:15][web:20][web:23]

O módulo deve operar de forma integrada com:
- IAM / perfis e permissões
- DP / folha / eventos trabalhistas
- Financeiro / centros de custo / provisões
- Patrimônio / ativos sob responsabilidade
- Compliance / LGPD / retenção documental
- Workflow / aprovações / notificações
- Assinatura eletrônica / aceite de documentos
- Auditoria / logs / trilhas de alteração [cite:2][web:15][web:18][web:21]

#### 1.2 Escopo funcional
O módulo RH deverá contemplar:
- Gestão de colaboradores
- Estrutura organizacional
- Recrutamento e seleção
- Onboarding e offboarding
- Jornada e frequência
- Férias e ausências
- Cargos, trilhas e carreira
- Avaliações e desempenho
- Treinamentos e capacitações
- Documentos e compliance trabalhista
- Solicitações internas de RH
- Indicadores e analytics
- Kanban operacional de admissões, movimentações e pendências [web:15][web:20][web:23]

#### 1.3 Princípios de arquitetura
- Multi-tenant por entidade e multi-unit por unidade
- Todos os registros com `id`, `uuid`, `code`
- APIs REST seguras e versionadas
- Frontend desacoplado consumindo via `fetch`
- Controle forte de escopo por entidade, unidade, departamento e vínculo
- Soft delete quando aplicável
- Auditoria full para operações sensíveis
- Campos internacionais em inglês no banco e endpoints
- UI padronizada conforme design system do sistema [cite:1][cite:2][cite:6][cite:7]

---

### 2. Objetivos de negócio

#### 2.1 Metas operacionais
- Reduzir tempo de admissão
- Diminuir retrabalho cadastral
- Centralizar documentos do colaborador
- Melhorar rastreabilidade de movimentações
- Padronizar solicitações e aprovações
- Aumentar visibilidade de headcount, absenteísmo, turnover e pendências [web:14][web:20][web:23]

#### 2.2 Metas técnicas
- Escalabilidade por tenant
- Segurança por escopo e perfil
- Baixo acoplamento entre páginas
- Componentização de drawers, tabelas, filtros e cards
- Estrutura pronta para internacionalização e integrações futuras [cite:1][cite:2][cite:6]

---

### 3. Perfis e permissões

#### 3.1 Perfis principais
- Super Admin
- Entity Admin
- Unit Admin
- HR Director
- HR Manager
- HR Analyst
- Recruiter
- Department Manager
- Payroll Analyst
- Occupational Health Analyst
- Employee Self-Service
- Auditor / Compliance / DPO
- Readonly Executive [web:15][web:18][web:21]

#### 3.2 Regras de visibilidade
Cada perfil deve possuir acesso por:
- entidade
- unidade
- departamento
- centro de custo
- vínculo funcional
- tipo de dado sensível
- tipo de documento
- ação: view, create, update, approve, export, delete, manage [web:18][web:21]

#### 3.3 Regras especiais
- Dados sensíveis exigem permissão explícita
- Salário, documentos pessoais, dados médicos e dados disciplinares devem ter acesso segregado
- Gestores visualizam apenas subordinados diretos ou indiretos conforme política
- Employee Self-Service visualiza apenas seus próprios dados
- Exportações devem ser registradas com motivo e usuário responsável [web:18][web:21]

#### 3.4 Matriz de permissão mínima
Permissões por recurso:
- `employees.view`
- `employees.create`
- `employees.update`
- `employees.archive`
- `employees.documents.manage`
- `employees.salary.view`
- `employees.sensitive.view`
- `positions.manage`
- `departments.manage`
- `recruitment.manage`
- `onboarding.manage`
- `attendance.view`
- `attendance.adjust`
- `leave.manage`
- `performance.manage`
- `training.manage`
- `movement.approve`
- `termination.manage`
- `reports.export`
- `audit.view` [web:15][web:18][web:21]

---

### 4. Navegação do módulo

#### 4.1 Menu lateral
- Dashboard RH
- Colaboradores
- Estrutura Organizacional
- Recrutamento
- Onboarding
- Jornada e Frequência
- Férias e Ausências
- Cargos e Carreiras
- Desempenho
- Treinamentos
- Documentos RH
- Movimentações
- Desligamentos
- Solicitações RH
- Analytics
- Configurações RH [web:13][web:15][web:20]

#### 4.2 Navegação interna por páginas
Cada página deve conter:
- breadcrumb
- header com título, subtítulo e ações
- toolbar com filtros
- widgets superiores
- área principal com datatable, tabs ou kanban
- drawers laterais para CRUD
- modais apenas para ações críticas
- rodapé técnico com paginação, totalizadores e status de carregamento [cite:6][web:12][web:16]

---

### 5. Dashboard RH

#### 5.1 Objetivo
Entregar visão executiva e operacional do RH com indicadores, alertas, tendências e pendências acionáveis. [web:14][web:20][web:23]

#### 5.2 Widgets obrigatórios
- Total de colaboradores ativos
- Headcount por unidade
- Admissões no mês
- Desligamentos no mês
- Turnover mensal
- Turnover acumulado
- Férias programadas próximas
- Colaboradores com documentos pendentes
- Absenteísmo do período
- Tempo médio de contratação
- Vagas abertas
- Onboardings pendentes
- Avaliações vencidas
- Treinamentos vencendo
- Colaboradores em experiência
- Distribuição por tipo de vínculo [web:14][web:20][web:23]

#### 5.3 Charts obrigatórios
- Linha: evolução de headcount por mês
- Barras: admissões x desligamentos por período
- Donut: distribuição por departamento
- Donut: distribuição por vínculo
- Barras horizontais: turnover por unidade
- Heatmap: ausências por dia/semana
- Barras: vagas por etapa do recrutamento
- Linha: SLA médio de contratação
- Barras empilhadas: status de onboarding
- Radar opcional: competências médias por área [web:14][web:20][web:23]

#### 5.4 Blocos operacionais
- Tarefas pendentes
- Aprovações pendentes
- Alertas críticos
- Aniversariantes
- Experiência vencendo
- Contratos próximos do fim
- Documentos vencidos ou a vencer
- Treinamentos obrigatórios não concluídos [web:20][web:23]

#### 5.5 Filtros do dashboard
- período
- entidade
- unidade
- departamento
- centro de custo
- gestor
- vínculo
- status
- tipo de contratação
- regime de trabalho [web:20][web:23]

---

### 6. Página Colaboradores

#### 6.1 Objetivo
Ser a página central de gestão de pessoas com visão cadastral, contratual, organizacional e operacional. [web:13][web:21]

#### 6.2 Datatable principal
Colunas:
- Foto/avatar
- Matrícula
- Nome completo
- Nome social
- CPF/passaporte mascarado
- Cargo atual
- Departamento
- Gestor imediato
- Unidade
- Tipo de vínculo
- Regime de trabalho
- Data de admissão
- Tempo de empresa
- Status funcional
- Status do onboarding
- Status documental
- Jornada
- Última avaliação
- Score de compliance documental
- Ações [web:13][web:21]

#### 6.3 Recursos da datatable
- busca global
- filtros avançados
- ordenação
- paginação server-side
- colunas fixas
- ocultar/exibir colunas
- salvar visão personalizada
- exportar CSV/XLSX/PDF conforme permissão
- seleção em massa
- bulk actions
- chips por status
- totalizadores no topo
- click row para perfil 360 do colaborador [web:12][web:13]

#### 6.4 Filtros avançados
- entidade
- unidade
- departamento
- centro de custo
- gestor
- cargo
- vínculo
- regime
- sexo
- PCD
- faixa etária
- faixa salarial
- situação contratual
- admissão entre datas
- experiência vencendo
- férias previstas
- documentação pendente
- com/sem avaliação
- com/sem treinamento pendente [web:20][web:23]

#### 6.5 Ações por linha
- visualizar perfil
- editar cadastro
- alterar lotação
- promover / transferir
- anexar documento
- registrar ocorrência
- iniciar férias
- lançar afastamento
- abrir solicitação
- gerar termo
- bloquear acesso
- iniciar desligamento
- arquivar [web:13][web:21]

---

### 7. Perfil 360 do colaborador

#### 7.1 Estrutura da página
Header com:
- foto
- nome
- matrícula
- cargo
- unidade
- gestor
- status
- badges de vínculo e regime
- ações rápidas [cite:4][web:13]

Tabs obrigatórias:
- Resumo
- Dados pessoais
- Dados contratuais
- Organização
- Jornada
- Férias e ausências
- Documentos
- Benefícios
- Treinamentos
- Avaliações
- Movimentações
- Equipamentos
- Solicitações
- Auditoria [cite:4][web:13][web:21]

#### 7.2 Cards da aba Resumo
- dados principais
- próximos eventos
- pendências documentais
- férias futuras
- avaliações pendentes
- treinamentos obrigatórios
- ativos vinculados
- últimas movimentações
- observações internas [cite:4][web:13]

#### 7.3 Controles necessários
- timeline de eventos
- upload de documentos
- aceite digital
- observações privadas por perfil
- histórico completo
- bloqueio de edição em campos sensíveis
- visualização condicional por permissão [cite:4][web:18][web:21]

---

### 8. Estrutura organizacional

#### 8.1 Páginas
- Departamentos
- Cargos
- Funções
- Níveis
- Centros de custo RH
- Organograma
- Gestores e subordinações
- Unidades e lotações [web:13][web:20]

#### 8.2 Datatables
##### Departamentos
- code
- nome
- sigla
- unidade
- gestor responsável
- total de colaboradores
- orçamento vinculado
- status
- ações

##### Cargos
- code
- título do cargo
- família
- nível
- CBO/ocupação
- faixa salarial
- regime aplicável
- requisitos
- status
- ações

##### Organograma
Visualização híbrida:
- árvore hierárquica
- modo grid
- modo lista
- filtros por unidade, área e gestor [web:12][web:13]

#### 8.3 Drawers de CRUD
Campos obrigatórios:
- identificação
- descrições
- vínculo hierárquico
- competências requeridas
- salários/faixas
- regime/jornada
- ativo/inativo
- motivos de inativação
- anexos e observações [web:13][web:21]

---

### 9. Recrutamento e seleção

#### 9.1 Páginas
- Dashboard de recrutamento
- Requisições de vaga
- Banco de vagas
- Pipeline de candidatos
- Banco de talentos
- Entrevistas
- Avaliações
- Propostas
- Aprovações de contratação [web:15][web:20]

#### 9.2 Datatable de vagas
- code
- título da vaga
- departamento
- unidade
- gestor requisitante
- quantidade
- prioridade
- SLA alvo
- status
- etapa atual
- data de abertura
- tempo em aberto
- ações [web:15][web:20]

#### 9.3 Kanban de recrutamento
Colunas:
- Nova candidatura
- Triagem
- Entrevista RH
- Entrevista técnica
- Teste
- Referências
- Proposta
- Aprovado
- Reprovado
- Banco de talentos [web:15][web:16]

Controles do Kanban:
- drag and drop
- limite por coluna opcional
- busca
- filtros rápidos
- comentários
- anexos
- checklist
- scorecard
- mudança em lote
- histórico de mudança
- ordenação por prioridade, SLA e data
- swimlanes por vaga ou recrutador [web:16]

#### 9.4 Drawers de recrutamento
- Nova vaga
- Editar vaga
- Novo candidato
- Agendar entrevista
- Registrar feedback
- Enviar proposta
- Converter para admissão [web:15]

---

### 10. Onboarding

#### 10.1 Objetivo
Controlar a entrada do colaborador com checklist, responsáveis, documentos, acessos, treinamentos e status por etapa. [web:15]

#### 10.2 Páginas
- Dashboard de onboarding
- Onboardings ativos
- Templates de onboarding
- Pendências por responsável
- Kits por cargo/unidade [web:15]

#### 10.3 Kanban de onboarding
Colunas:
- Pré-admissão
- Documentação
- Contrato
- Cadastro em sistemas
- Equipamentos
- Integração
- Treinamentos iniciais
- Concluído
- Bloqueado [web:15][web:16]

#### 10.4 Controles
- checklist por etapa
- responsável por tarefa
- data limite
- anexos
- assinatura/aceite
- dependências entre tarefas
- bloqueios por documento faltante
- gatilho para criação de usuário IAM
- gatilho para solicitação de equipamentos
- gatilho para treinamento obrigatório [web:15][web:16]

---

### 11. Jornada e frequência

#### 11.1 Páginas
- Espelho de ponto
- Ajustes e ocorrências
- Escalas
- Banco de horas
- Faltas e atrasos
- Aprovações de ponto [web:15][web:20]

#### 11.2 Datatable de frequência
- colaborador
- matrícula
- unidade
- escala
- período
- horas previstas
- horas trabalhadas
- extra
- atraso
- falta
- inconsistências
- status de aprovação
- ações [web:20]

#### 11.3 Controles
- filtros por período e gestor
- justificativas
- anexar comprovantes
- aprovação em lote
- recálculo
- travamento por competência
- alerta de extrapolação
- integração futura com relógio/REP [web:20]

---

### 12. Férias e ausências

#### 12.1 Páginas
- Calendário de férias
- Solicitações
- Aprovações
- Saldos
- Afastamentos
- Licenças
- Retornos [web:20][web:23]

#### 12.2 Datatable
- colaborador
- período aquisitivo
- saldo
- data solicitada
- data aprovada
- quantidade de dias
- tipo
- cobertura/substituto
- status
- ações [web:20]

#### 12.3 Controles
- calendário anual
- conflito entre equipes
- bloqueios por período crítico
- aprovação em cadeia
- anexos médicos ou jurídicos
- retorno previsto
- alertas de vencimento de férias [web:20][web:23]

---

### 13. Desempenho

#### 13.1 Páginas
- Ciclos de avaliação
- Avaliações 90/180/360
- PDI
- Competências
- Metas
- Feedbacks contínuos
- Ranking interno controlado [web:20][web:23]

#### 13.2 Datatable de avaliações
- ciclo
- colaborador
- avaliador
- tipo
- peso
- nota final
- competências críticas
- status
- prazo
- ações [web:20][web:23]

#### 13.3 Drawers
- criar ciclo
- configurar formulário
- lançar feedback
- aprovar PDI
- registrar evidências
- fechar avaliação [web:20][web:23]

#### 13.4 Charts
- distribuição de notas
- evolução por ciclo
- heatmap de competências
- notas por área
- PDIs concluídos x pendentes [web:20][web:23]

---

### 14. Treinamentos

#### 14.1 Páginas
- Catálogo de treinamentos
- Trilhas por cargo
- Turmas
- Certificações
- Treinamentos obrigatórios
- Treinamentos vencendo
- Presença e conclusão [web:20][web:23]

#### 14.2 Datatable
- code
- treinamento
- tipo
- modalidade
- carga horária
- obrigatório
- público-alvo
- validade
- instrutor
- status
- ações [web:20]

#### 14.3 Controles
- matricular em lote
- conclusão manual
- upload de certificado
- score
- validade e recertificação
- integração com onboarding
- bloqueio por obrigatoriedade não concluída [web:20][web:23]

---

### 15. Documentos RH

#### 15.1 Tipos documentais
- documentos pessoais
- contrato
- aditivos
- comprovantes
- certificados
- documentos admissionais
- documentos periódicos
- termos e políticas
- laudos e ASO com acesso segregado
- documentos de desligamento [web:21]

#### 15.2 Datatable
- code
- colaborador
- tipo documental
- nome do arquivo
- versão
- validade
- obrigatoriedade
- status
- confidencialidade
- enviado por
- data de envio
- ações [web:21]

#### 15.3 Controles
- upload múltiplo
- versionamento
- expiração
- assinatura eletrônica
- aceite
- retenção
- anonimização conforme política
- bloqueio por perfil
- trilha de acesso ao documento [cite:2][web:21]

---

### 16. Movimentações internas

#### 16.1 Tipos
- promoção
- transferência
- mudança salarial
- alteração de jornada
- alteração de gestor
- alteração de unidade
- alteração de departamento
- alteração de cargo
- alteração de regime [web:21]

#### 16.2 Página de movimentações
Widgets:
- promoções no período
- transferências
- mudanças salariais
- pendências de aprovação
- movimentações futuras [web:20][web:23]

Datatable:
- code
- colaborador
- tipo
- origem
- destino
- data efetiva
- solicitante
- aprovador
- status
- impacto financeiro
- ações [web:20]

#### 16.3 Fluxo
- solicitação
- validação RH
- validação gestor
- validação financeira quando necessário
- efetivação
- comunicação
- auditoria [web:18][web:20]

---

### 17. Desligamentos

#### 17.1 Páginas
- Desligamentos ativos
- Checklist de offboarding
- Entrevistas de saída
- Pendências de devolução
- Relatórios de turnover [web:20][web:23]

#### 17.2 Kanban de desligamento
Colunas:
- Solicitação aberta
- Validação RH
- Cálculo e documentos
- Revogação de acessos
- Devolução de ativos
- Entrevista de saída
- Concluído [web:16][web:20]

#### 17.3 Controles
- data efetiva
- tipo de desligamento
- motivo
- bloqueio de acessos
- devolução de ativos
- documentos obrigatórios
- homologação
- questionário de saída
- evidências anexas [web:20][web:23]

---

### 18. Solicitações RH

#### 18.1 Tipos de solicitação
- atualização cadastral
- segunda via de documento
- férias
- abono
- declaração
- alteração de conta
- alteração de endereço
- contestação de ponto
- mudança de benefício
- pedido de movimentação [web:20][web:23]

#### 18.2 Página
- fila de solicitações
- solicitações por status
- SLA médio
- responsáveis
- automações pendentes [web:20]

#### 18.3 Controles
- formulário dinâmico por tipo
- anexos
- workflow configurável
- aprovação por alçada
- histórico de comentários
- templates de resposta
- encerramento com motivo [web:16][web:20]

---

### 19. Analytics RH

#### 19.1 Indicadores estratégicos
- headcount
- turnover
- turnover voluntário
- turnover involuntário
- absenteísmo
- tempo médio de contratação
- custo por contratação
- taxa de conclusão de onboarding
- taxa de treinamento obrigatório
- distribuição por diversidade
- movimentações por período
- férias vencidas
- tempo médio no cargo
- taxa de promoções internas [web:14][web:20][web:23]

#### 19.2 Páginas analíticas
- People Analytics
- Recruitment Analytics
- Workforce Cost
- Attrition Analysis
- Leave & Absence Analysis
- Performance Analytics
- Training Analytics [web:14][web:20][web:23]

#### 19.3 Recursos
- filtros persistentes
- drill-down
- exportação controlada
- snapshots por período
- comparação entre unidades
- metas vs realizado [web:14][web:20][web:23]

---

### 20. CRUD Drawers padrão

#### 20.1 Estrutura padrão
Todo drawer deverá possuir:
- header com título e subtítulo
- body com tabs ou seções
- footer fixo com ações
- validação inline
- loading states
- bloqueio de submit duplo
- autosave opcional quando permitido
- confirmação em ações destrutivas [cite:6][web:12]

#### 20.2 Drawers obrigatórios do módulo
- Novo colaborador
- Editar colaborador
- Nova vaga
- Novo candidato
- Nova movimentação
- Novo afastamento
- Nova solicitação
- Novo treinamento
- Novo documento
- Novo ciclo de avaliação
- Novo desligamento
- Configurar estrutura organizacional [web:13][web:15]

#### 20.3 Campos comuns
- entity_id
- unit_id
- department_id
- status
- responsible_id
- tags
- notes
- attachments
- effective_date
- start_date
- end_date [cite:2][cite:7]

---

### 21. Kanban padrão

#### 21.1 Kanbans previstos
- Recrutamento
- Onboarding
- Solicitações RH
- Desligamentos
- Pendências documentais
- Avaliações em andamento [web:15][web:16]

#### 21.2 Controles globais do Kanban
- drag and drop
- filtros
- busca
- ordenação
- swimlanes
- comentários
- checklist
- anexos
- histórico
- undo/redo
- atalhos de teclado
- limite por coluna
- cards colapsáveis
- visualização por responsável [web:16]

---

### 22. Automações

#### 22.1 Gatilhos automáticos
- Ao aprovar candidato, criar pré-colaborador
- Ao concluir admissão, criar vínculo ativo
- Ao iniciar onboarding, gerar checklist padrão
- Ao admitir, criar usuário IAM se política permitir
- Ao admitir, solicitar kit de equipamentos conforme cargo
- Ao mover colaborador, atualizar gestor/lotação
- Ao marcar desligamento, abrir fluxo de offboarding
- Ao vencer documento, notificar responsável
- Ao avaliação vencer, abrir tarefa para gestor
- Ao treinamento obrigatório expirar, notificar e bloquear conformidades específicas [web:15][web:18][web:20]

#### 22.2 Automações por agenda
- lembrete de férias vencendo
- experiência vencendo
- contrato temporário vencendo
- documentos vencendo
- aniversários
- integrações pendentes
- avaliações vencendo
- recertificações [web:20][web:23]

#### 22.3 Automações por regra
- alçada de aprovação por tipo e impacto
- roteamento por unidade/departamento
- bloqueio por ausência de documentação
- criação automática de tasks
- abertura de incidentes para inconsistências críticas [web:18][web:20]

---

### 23. Controles e compliance

#### 23.1 Controles obrigatórios
- RBAC granular
- segregação de dados sensíveis
- mascaramento parcial de PII
- logs de acesso
- logs de exportação
- versionamento de alterações
- retenção documental configurável
- anonimização conforme política
- aceite de termos
- rastreabilidade por usuário, data e origem [cite:2][web:18][web:21]

#### 23.2 LGPD e privacidade
- base legal por processamento quando necessário
- minimização de dados
- consentimento apenas onde aplicável
- acesso restrito a dados sensíveis
- trilha de acesso a documentos sensíveis
- política de retenção por categoria documental [cite:2][web:18][web:21]

#### 23.3 Auditoria
Todo evento crítico deve registrar:
- entity_id
- unit_id
- actor_user_id
- resource_type
- resource_id
- action
- before_json
- after_json
- ip
- user_agent
- created_at [cite:2][web:18]

---

### 24. Gerenciamentos e configurações

#### 24.1 Cadastros mestres
- tipos de vínculo
- regimes de trabalho
- escalas
- motivos de afastamento
- motivos de desligamento
- tipos documentais
- templates de onboarding
- templates de avaliação
- trilhas de treinamento
- motivos de movimentação
- status customizados [web:15][web:20][web:21]

#### 24.2 Configurações do módulo
- parâmetros de SLA
- regras de aprovação
- notificações
- templates de e-mail
- templates de documentos
- regras de visibilidade
- retenção documental
- políticas de bloqueio
- numeração `code`
- cores e status padrão [web:18][web:21]

---

### 25. Estrutura de páginas

#### 25.1 Lista principal de páginas
1. `/hr/dashboard`
2. `/hr/employees`
3. `/hr/employees/{uuid}`
4. `/hr/org/departments`
5. `/hr/org/positions`
6. `/hr/org/structure`
7. `/hr/recruitment/dashboard`
8. `/hr/recruitment/jobs`
9. `/hr/recruitment/candidates`
10. `/hr/recruitment/kanban`
11. `/hr/onboarding`
12. `/hr/onboarding/kanban`
13. `/hr/attendance`
14. `/hr/attendance/adjustments`
15. `/hr/leave`
16. `/hr/leave/calendar`
17. `/hr/performance`
18. `/hr/training`
19. `/hr/documents`
20. `/hr/movements`
21. `/hr/terminations`
22. `/hr/requests`
23. `/hr/analytics`
24. `/hr/settings` [cite:6][web:13][web:15]

#### 25.2 Padrão visual de cada página
- topo com título e ações
- widgets contextuais
- bloco de filtros
- conteúdo principal
- drawer manager global
- toaster notifications
- estado vazio orientado
- skeleton loading
- paginação server-side [cite:6][web:12][web:13]

---

### 26. Padrão de datatables

#### 26.1 Comportamentos obrigatórios
- server-side processing
- filtros persistentes
- busca debounce
- ordenação múltipla quando aplicável
- paginação
- seleção em massa
- exportação com auditoria
- ações rápidas
- row details
- refresh manual
- atualização automática opcional [web:12]

#### 26.2 Toolbar padrão
- busca
- filtros
- salvar visualização
- exportar
- colunas
- atualizar
- criar novo
- ações em massa [web:12]

---

### 27. Padrão de widgets

#### 27.1 Tipos de widgets
- KPI simples
- KPI com variação percentual
- KPI com sparkline
- KPI com meta
- alerta crítico
- card de SLA
- card de pendência
- card de ranking
- card de timeline [web:14][web:20][web:23]

#### 27.2 Regras visuais
- no máximo 4 por linha em desktop
- cores semânticas padronizadas
- ícones consistentes
- tooltip explicativo
- clique opcional para drill-down [cite:6]

---

### 28. Padrão de charts

#### 28.1 Biblioteca
Usar amCharts 5 já padronizado no sistema. [cite:1]

#### 28.2 Regras
- todos os charts com loading state
- export opcional conforme permissão
- legenda clicável
- tooltip detalhado
- cores consistentes
- acessibilidade por contraste
- filtros sincronizados com página [cite:1][cite:6][web:20]

#### 28.3 Charts mínimos por área
- Dashboard RH: 8+
- Recrutamento: 5+
- Frequência: 4+
- Férias: 3+
- Desempenho: 5+
- Treinamentos: 4+
- Analytics: 8+ [web:20][web:23]

---

### 29. Endpoints esperados

#### 29.1 Exemplos principais
- `GET /api/v1/hr/dashboard`
- `GET /api/v1/hr/employees`
- `POST /api/v1/hr/employees`
- `GET /api/v1/hr/employees/{uuid}`
- `PUT /api/v1/hr/employees/{uuid}`
- `POST /api/v1/hr/employees/{uuid}/documents`
- `POST /api/v1/hr/recruitment/jobs`
- `GET /api/v1/hr/recruitment/kanban`
- `POST /api/v1/hr/onboarding`
- `POST /api/v1/hr/movements`
- `POST /api/v1/hr/terminations`
- `GET /api/v1/hr/analytics/turnover` [cite:1][cite:6]

#### 29.2 Regras de API
- autenticação forte
- escopo por tenant
- validação server-side
- paginação padrão
- filtros whitelisted
- auditoria de mutações
- responses consistentes
- errors padronizados [cite:1][cite:2][web:18]

---

### 30. Modelo de status

#### 30.1 Status de colaborador
- draft
- pre_onboarding
- active
- inactive
- on_leave
- suspended
- terminated
- archived

#### 30.2 Status de vaga
- draft
- open
- paused
- in_review
- closed
- canceled

#### 30.3 Status de solicitação
- open
- pending
- approved
- rejected
- canceled
- completed

#### 30.4 Status de documento
- pending
- submitted
- approved
- rejected
- expired
- archived [web:15][web:21]

---

### 31. Campos mínimos por cadastro principal

#### 31.1 Colaborador
- code
- first_name
- last_name
- social_name
- document_number
- birth_date
- gender
- marital_status
- nationality
- email
- phone
- address
- hire_date
- employee_type
- work_regime
- department_id
- position_id
- manager_id
- unit_id
- cost_center_id
- status
- notes [cite:4][web:13][web:21]

#### 31.2 Vaga
- code
- title
- department_id
- unit_id
- requester_id
- target_start_date
- openings
- seniority_level
- salary_range
- job_type
- work_model
- description
- requirements
- status [web:15]

#### 31.3 Movimentação
- code
- employee_id
- movement_type
- from_department_id
- to_department_id
- from_position_id
- to_position_id
- effective_date
- reason
- requested_by
- approved_by
- status [web:20]

---

### 32. Checklist de aceite

#### 32.1 Funcional
- Todas as páginas renderizam corretamente
- Todos os filtros funcionam server-side
- Drawers salvam com validação
- Kanbans persistem mudança de coluna
- Widgets refletem filtros
- Charts respeitam escopo
- Ações em massa funcionam
- Perfil 360 está completo [web:12][web:16][web:20]

#### 32.2 Segurança
- RBAC aplicado em rotas, botões e dados
- Dados sensíveis protegidos
- Exportações auditadas
- APIs com escopo por tenant
- Logs críticos habilitados [cite:2][web:18][web:21]

#### 32.3 UX/UI
- Responsivo
- Acessível
- Hierarquia visual consistente
- Estados vazios, loading e erro tratados
- Feedback visual em ações críticas [cite:6][web:13]

---

### 33. Roadmap de implementação

#### 33.1 Fase 1
- Dashboard RH
- Colaboradores
- Perfil 360
- Estrutura organizacional
- Documentos RH
- Solicitações RH [web:13][web:20]

#### 33.2 Fase 2
- Recrutamento
- Onboarding
- Jornada
- Férias e ausências [web:15][web:20]

#### 33.3 Fase 3
- Desempenho
- Treinamentos
- Movimentações
- Desligamentos
- Analytics avançado [web:20][web:23]

---

### 34. Observações finais de implementação
Toda página deve seguir o padrão visual consolidado do sistema, com layout PHP base, componentes reutilizáveis, Tailwind + Supabase, JS limpo, drawers padronizados, tabelas server-side e integração exclusiva por API com `fetch`. [cite:1][cite:6]

Todos os ícones devem usar Font Awesome 7.2.0 e todo CSS específico do módulo deve ser isolado em arquivo próprio do módulo ou integrado ao `ttsc.css` conforme padrão do projeto. [cite:6]

Todos os eventos críticos do módulo RH devem ser auditáveis, principalmente visualização de dados sensíveis, downloads, alterações de vínculo, movimentações, desligamentos e documentos. [cite:2][web:18][web:21]
