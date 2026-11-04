# SDD 12 — Especificação de Portais, Navegação (Sidebar & Sub-Sidebar) e Arquitetura de Páginas Completas

> **Documento Derivado do SDD Mestre** · **Data:** 05/09/2026  
> **Status:** Aprovado / Normativo  
> **Conformidade de Design:** [`totustuus-layout-design/SKILL.md`](file:///c:/Xampp/htdocs/totustuussoftcloud/.agents/skills/totustuus-layout-design/SKILL.md) (Checklist de 21 Itens / Supabase 3-Layer Dark Emerald)  
> **Conformidade de Segurança:** [`totustuus-security-auditor-v3/SKILL.md`](file:///c:/Xampp/htdocs/totustuussoftcloud/.agents/skills/totustuus-security-auditor-v3/SKILL.md) (ASVS Level 2, OWASP Top 10:2025, STRIDE, ASM, Argon2id, Tenant-Strict, Zero Inline JS)

---

## 1. Visão Geral e Fundamentação

Este documento estabelece a Especificação de Design de Software (SDD) canônica para a implementação das **Sidebars Principais**, **Sub-Sidebars Modulares com Accordions** e **Páginas Completas** em todo o ecossistema TotusTuus SoftCloud.

O desenho arquitetural é derivado das **6 especificações definitivas de portais**:
1. [Portal do Desenvolvedor Completo](file:///c:/Xampp/htdocs/totustuussoftcloud/docs/portais/portal-do-desenvolvedor-completo.md) (`/developer/*`)
2. [SAAS Acadêmico Completo](file:///c:/Xampp/htdocs/totustuussoftcloud/docs/portais/saas-academico-completo.md) (`/admin/*`, `/academic/*`, `/app/*`)
3. [Portal do Professor Completo](file:///c:/Xampp/htdocs/totustuussoftcloud/docs/portais/portal-do-professor-completo.md) (`/teacher/*`)
4. [Portal do Aluno Completo](file:///c:/Xampp/htdocs/totustuussoftcloud/docs/portais/portal-do-aluno-completo.md) (`/student/*`)
5. [Portal dos Pais e Responsáveis Completo](file:///c:/Xampp/htdocs/totustuussoftcloud/docs/portais/portal-dos-pais-responsaveis-completo.md) (`/parents/*`, `/guardian/*`)
6. [Portal de Terceiros Completo](file:///c:/Xampp/htdocs/totustuussoftcloud/docs/portais/portal-de-terceiros-completo.md) (`/thirdparty/*`)

---

## 2. Princípios Globais de Implementação

1. **Contexto Estrito de Domínio**: Cada página deve exibir **única e exclusivamente** os dados, indicadores (KPIs), colunas, cards e telemetria pertinentes ao seu assunto (vedado copiar dados genéricos entre telas).
2. **Padrão 5-View Supabase Dark Emerald**: Toda página de gestão implementa o container unificado `.tb-card` com abas segmentadas em pílula (`.ud-tab-segmented`):
   - **`KPI` (Overview)**: Ativa por padrão ao carregar a página.
   - **`Data Table`**: Tabela com scroll horizontal, busca debounced, filtros e colunas fixas (`.col-check`, `.col-actions`).
   - **`Cards / Grid`**: Grade de cartões de entidades com paginação independente.
   - **`Kanban Board`**: Quadro em 4 estágios com Drag & Drop HTML5 nativo e atualização otimista.
   - **`Analytics / Charts`**: Visualizações Chart.js 4.4 específicas (barras, linhas e doughnut).
3. **Exportação Universal em 7 Formatos**: Dropdown padronizado com CSV, XLSX, PDF, JSON, XML, SQL Dump e TXT.
4. **Operação 100% via Drawers Laterais**:
   - **Drawer de Leitura (View)**: Exibição de detalhes e metadados.
   - **Drawer de Criação/Edição (Stepper de 5 Passos)**: `Geral` $\rightarrow$ `Configurações` $\rightarrow$ `Parâmetros` $\rightarrow$ `Segurança` $\rightarrow$ `Revisão`.
   - **Drawer de Exclusão (Delete)**: Destravamento do botão perigoso apenas após digitação exata da palavra-chave `"DELETE"`.
5. **Segurança e Zero Inline JS**:
   - **Zero `onclick`, `onchange`, `oninput`**. Todos os eventos usam `data-action="..."` capturados por delegação no `document`.
   - Script tag com atributo `nonce="<?= \App\Security\CspNonce::get() ?>"`.
   - Isolamento de Tenant estrito: nunca aceitar `tenant_id` do cliente em requisições de modificação.
   - Prevenção rigorosa de BOLA/IDOR na abertura e submissão de dados dos Drawers.

---

## 3. Arquitetura de Navegação: Sidebars & Sub-Sidebars

### 3.1 Camada de Configuração Central (`app/Config/sidebar-nav.php`)
A navegação do sistema é governada por uma matriz PHP canônica que registra todos os portais e módulos com:
- `sidebarId`: ID DOM único para controle de visibilidade.
- `i18nGroup`: Domínio de tradução no `TranslationService`.
- `key` e `title`: Chave de localização e título padrão.
- `icon`: Ícone oficial FontAwesome Pro 7.2 Light (`fa-light`).
- `sections`: Lista de seções/accordions, suportando:
  - Links diretos no topo (`'isDirect' => true`): Renderizados sem botão de toggle ou seta, funcionando como link direto para a página de visão geral do módulo.
  - Grupos de Accordion normais: Expansíveis com múltiplos itens, preservando expansão automática com base no `currentUrl`.

### 3.2 Sub-Sidebar Partial (`resources/views/app/partials/sub_sidebar.php`)
O componente parcial do sub-sidebar implementa:
- Detecção da rota atual via `SidebarRouter::path()`.
- Destaque ativo (`.is-active`, `aria-current="page"`).
- Internacionalização dinâmica em 10 idiomas com fallback (`__('key', 'group', 'Fallback')`).
- Isolamento de busca client-side de menus com atalho `Ctrl+K`.

---

## 4. Matriz Completa dos 6 Portais

### 4.1 Portal do Desenvolvedor (`/developer/*`)

| Seção Principal (Sidebar) | Módulo / Sub-Sidebar | Accordions & Páginas Requisitadas |
|---|---|---|
| **Portal do Desenvolvedor** | Dashboard | Métricas do Cluster, Nós Ativos, Uptime, APM |
| **Plataforma & Locatários** | Clientes (Tenants) | **Visão Geral Clientes (Tenants)** (Direto)<br>▸ *CLIENTES / TENANTS*: Clientes / Escolas<br>▸ *Comercial e Cobrança*: Licenciamento e Planos, Assinaturas e Renovações, Faturamento e Cobranças, Pagamentos e Transações, Créditos, Descontos e Cupons<br>▸ *Contrato e Provisionamento*: Módulos e Recursos Contratados, Limites e Consumo, Domínios e Subdomínios, Onboarding e Migrações<br>▸ *Administração do Tenant*: Administradores e Acessos, Integrações e APIs, Comunicação e Notificações<br>▸ *Governança e Operação*: Suporte e Solicitações, Auditoria e Conformidade, Configurações |
| | System Builder & Portais | Portais e Aplicações, Navegação e Menus, Páginas e Rotas, Layouts e Templates, Temas e Identidade Visual, Componentes e Widgets, Formulários e Jornadas, Conteúdo, Localização (10 Locales), Feature Flags, Publicação e Auditoria |
| **Gestão & Negócios** | Administrativo | Empresas Desenvolvedoras, Unidades e Filiais, Departamentos, Cargos, Organograma, Governança, Contratos Administrativos, Riscos |
| | Comercial | Catálogo de Produtos e Planos, Módulos/Add-ons, Tabelas de Preço, CRM, Leads, Oportunidades, Propostas, Comissões |
| | Marketing | Campanhas, Landing Pages, Formulários de Captura, Automações de E-mail, Tracking & Pixel, ROI e Leads |
| | Contábil | Plano de Contas, Lançamentos Contábeis, Balancetes, Razão, Fechamento Contábil, DRE, SPED, Conciliação |
| | Documentos | Documentos Corporativos, Contratos Internos, Assinaturas Digitais, Políticas e Normas, Templates |
| | Eventos | Calendário Corporativo, Eventos Técnicos, Hackathons, Treinamentos Internos, Participantes |
| | Financeiro | Contas a Pagar, Contas a Receber, Fluxo de Caixa, DRE Financeiro, Bancos e Contas, Conciliação Bancária |
| | Projetos | Roadmap do Produto, Sprints e Backlog, Quadro Kanban, Milestones, Tarefas Técnicas, Apontamento de Horas |
| | Qualidade & Testes | Casos de Teste, Execuções Automatizadas, Relatórios de Cobertura, Bugs e Defeitos, Pentests e Varreduras |
| **Pessoas & RH** | Departamento Pessoal | Admissões, Folha de Pagamento, Férias, Rescisões, eSocial, Benefícios, Controle de Ponto |
| | Recursos Humanos | Recrutamento e Seleção, Avaliação de Desempenho, Clima Organizacional, Treinamento e Desenvolvimento |
| | Medicina do Trabalho | ASO e Exames Ocupacionais, PCMSO, PGR, CAT, Laudos de Ergonomia e Insalubridade |
| **Operações & Logística** | Suprimentos | Requisições de Compra, Cotações, Pedidos de Compra, Fornecedores Homologados |
| | Armazenamento (WMS) | Almoxarifados, Locais de Estoque, Itens e SKUs, Entradas, Saídas, Lotes e Validades, Inventário |
| | Frotas | Veículos Corporativos, Manutenções, Abastecimentos, Multas e Sinistros, Rotas e Checklists |
| | Patrimônio | Bens Patrimoniais, Plaquetas/Tombamento, Depreciação, Transferências, Termos de Cautela |
| **Segurança & Acesso** | Portaria & Acesso | Catracas e Bloqueios, Visitantes, Crachás/Biometria, Encomendas e Correspondências |
| | Gestão de Acesso | Usuários, Papéis e Perfis (RBAC), Permissões Granulares, Sessões Ativas, MFA e Chaves WebAuthn |
| | Gestão de Auditoria | Logs de Sistema, Trilha de Operações (Quem/Onde/Quando), Mudanças em BD, Tentativas de Invasão |
| | Gestão de Privacidade | DPO / Encarregado, Registro de Atividades (ROPA), Consentimentos, Requisições DSR, Incidentes LGPD |
| | Gestão de TI | Infraestrutura em Nuvem, Clusters Kubernetes, Bancos de Dados, DNS, Certificados TLS, Backups |
| **Entidade & Unidades** | Configurações da Entidade | Dados Cadastrais da Mantenedora, Unidades Operacionais, Certidões e Documentos Regulatórios |
| **Suporte** | Gestão de Tickets | Fila de Chamados, SLA, Atendimento Helpdesk, Base de Conhecimento, Avaliações CSAT |
| **Configurações & Sistema**| Configurações do Sistema | Parâmetros Globais, Logs do Servidor, Filas/Workers, Cache Redis, Manutenção Programada |
| | Gestão de Integração | Webhooks, Chaves de API, Conectores Bancários, SEFAZ / Prefeituras, Gateways de E-mail/SMS |

---

### 4.2 SAAS Acadêmico (`/admin/*`, `/academic/*`)

| Seção Principal (Sidebar) | Módulo / Sub-Sidebar | Accordions & Páginas Requisitadas |
|---|---|---|
| **SAAS Acadêmico** | Dashboard | KPIs de Matrículas, Adimplência Escolar, Frequência Global, Ocorrências |
| **Ensino & Acadêmico** | Administração Escolar | Estrutura Acadêmica, Calendário Letivo, Séries e Turmas, Horários de Aula, Regras de Aprovação |
| | Gestão de Documentos | Declarações Escolares, Certificados, Boletins, Históricos Oficiais, Protocolos e Validações |
| | Gestão de Eventos | Feiras de Ciências, Festividades, Reuniões de Pais, Jogos Internos, Inscrições e Certificados |
| | Gestão Pedagógica | Matriz Curricular, Planos de Aula, Conteúdos e Trilhas, Banco de Avaliações, Conselho de Classe |
| | Secretaria Digital | Matrículas e Rematrículas, Transferências, Enturmação, Ficha Médica/Cadastral, Protocolos |
| | Biblioteca | Acervo Físico e Digital, Empréstimos, Reservas, Controle de Atrasos e Multas, Catálogo AACR2 |
| | Relatórios Acadêmicos | Boletim de Desempenho, Mapa de Notas e Faltas, Ata de Resultados Finais, Censo Escolar MEC |
| **Módulos PRO** | Simulados PRO | Banco de Questões ENEM/Vestibulares, Geração de Provas, Correção TRI, Gabarito Óptico, Rankings |
| | Gestão Pastoral PRO | Acompanhamento Espiritual, Encontros de Jovens, Ações Sociais, Confissões, Capelania Escolar |
| | Preceptoria PRO | Tutoria Individual de Alunos, Metas Acadêmicas, Plano de Desenvolvimento Individual (PDI) |
| | Projetos PRO | Feiras de Inovação, Clubes de Robótica, Iniciação Científica, Tarefas e Marcos dos Alunos |
| | Agendamento Espaços PRO | Laboratórios de Ciências/Informática, Quadras, Auditórios, Salas Multimídia, Termos de Uso |
| **Gestão & Negócios** | Comercial / Matrículas | Funil de Captação de Alunos, Visitas Agendadas, Bolsas de Estudo, Conversão de Leads |
| | Contábil Escolar | Centro de Custo por Unidade, Contabilidade Integrada, Livro Razão, Retenção Tributária |
| | Financeiro Escolar | Mensalidades Escolares, Carnês/Boletos, Cobrança Recorrente PIX/Cartão, Renegociação, Régua |
| **Pessoas & RH** | Corpo Docente & Pessoal | Quadro de Professores, Atribuição de Aulas, Grade Horária, Ponto Eletrônico, Licenças |
| **Operações & Logística** | Suprimentos & Merenda | Alimentação Escolar / Cardápio Nutricional, Uniformes, Materiais Didáticos, Compras |
| | Transporte Escolar | Rotas de Ônibus/Vans, Motoristas Credenciados, Alunos por Ponto, Rastreamento de Trajeto |
| **Segurança & Acesso** | Portaria Escolar | Reconhecimento Facial / Catracas, Autorização de Saída com Responsáveis, Visitantes |
| | Gestão de Privacidade | LGPD Escolar, Proteção de Dados de Menores, Termos de Imagem, Consentimentos |
| **Instituição & Unidades**| Configurações Escolares | Dados do MEC/INEP, Dados da Entidade Mantenedora, Unidades e Campi, Brasão e Cores |

---

### 4.3 Portal do Professor (`/teacher/*`)

| Seção Principal (Sidebar) | Módulo / Sub-Sidebar | Accordions & Páginas Requisitadas |
|---|---|---|
| **Portal do Professor** | Dashboard do Docente | Aulas de Hoje, Alertas de Pendências, Próximas Avaliações, Mensagens da Coordenação |
| **Ensino & Acadêmico** | Classe de Aula | Minhas Turmas e Disciplinas, Mural de Avisos, Materiais de Apoio, Trabalhos e Tarefas |
| | Diário Escolar | Lançamento de Frequência Diária, Registro de Conteúdos Lecionados, Lançamento de Notas |
| | Eventos & Calendário | Calendário de Aulas, Reuniões Pedagógicas, Plantão de Dúvidas, Datas de Provas |
| | Notificações | Comunicados da Direção, Mensagens para Turmas, Avisos Importantes |
| | Biblioteca do Professor | Acervo Técnico Pedagógico, Livros Adotados, Indicação de Leituras |
| | Simulados | Elaboração de Questões, Agendamento de Simulados, Resultados da Turma |
| | Relatórios do Docente | Rendimento por Turma, Ficha de Acompanhamento Individual, Mapa Comparativo |
| **Serviços** | Protocolos & Pedidos | Solicitação de Materiais, Reserva de Equipamentos/Laboratórios, Justificativas |
| | Documentos | Diplomas e Certificados do Professor, Contratos de Trabalho, Declarações |
| | Privacidade | Minhas Configurações de Privacidade, Consentimentos e Termos de Uso |
| **Financeiro & Carreira** | Ponto & Frequência | Registro de Ponto Docente, Histórico de Marcações, Horas-Aula Cumpridas |
| | Holerites & Rendimentos | Contracheques / Holerites Mensais, Informe de Rendimentos, Benefícios |

---

### 4.4 Portal do Aluno (`/student/*`)

| Seção Principal (Sidebar) | Módulo / Sub-Sidebar | Accordions & Páginas Requisitadas |
|---|---|---|
| **Portal do Aluno** | Dashboard do Aluno | Horário das Aulas, Próximas Entregas, Últimas Notas Lançadas, Avisos do Dia |
| **Ensino & Acadêmico** | Classe de Aula | Minhas Disciplinas, Aulas e Conteúdos, Download de Materiais, Envio de Trabalhos |
| | Diário Escolar | Boletim Online, Histórico Parcial de Notas, Percentual de Presença por Disciplina |
| | Entradas e Saídas | Histórico de Acesso na Catraca/Portaria, Registro de Presença com Horário |
| | Eventos | Feiras, Campeonatos, Excursões, Calendário Acadêmico |
| | Notificações | Avisos da Coordenação, Notificações dos Professores, Lembretes de Provas |
| | Biblioteca | Livros Emprestados, Prazo de Devolução, Renovação Online, Pesquisa de Acervo |
| | Simulados & Testes | Simulados Agendados, Realização de Provas Online, Gabaritos e Comentários |
| **Serviços** | Protocolos Online | Requerimento de 2ª Chamada, Solicitação de Declaração de Matrícula, Carteirinha |
| | Documentos | Boletins Oficiais em PDF, Histórico Escolar, Termos e Declarações |
| | Privacidade | Meus Dados Cadastrais, Solicitações de Privacidade LGPD |
| **Financeiro** | Financeiro do Aluno | Mensalidades, Segunda Via de Boletos, Código PIX Copia e Cola, Comprovantes |
| | Matrícula Online | Confirmação de Matrícula para o Próximo Ano, Escolha de Eletivas e Trilhas |

---

### 4.5 Portal dos Pais e Responsáveis (`/parents/*` ou `/guardian/*`)

| Seção Principal (Sidebar) | Módulo / Sub-Sidebar | Accordions & Páginas Requisitadas |
|---|---|---|
| **Portal dos Pais** | Dashboard Familiar | Seletor de Filho/Dependente, Resumo de Notas, Faltas da Semana, Boletos a Vencer |
| **Ensino & Acompanhamento**| Classe & Atividades | Tarefas de Casa dos Filhos, Materiais Didáticos, Comunicados dos Professores |
| | Diário Escolar | Notas e Avaliações de Cada Dependente, Boletim Escolar, Ocorrências Disciplinares |
| | Entradas e Saídas | Registro em Tempo Real de Entrada/Saída na Portaria, Notificação de Atraso |
| | Eventos & Reuniões | Agendamento de Atendimento com Professores, Reuniões de Pais, Festividades |
| | Notificações | Avisos da Diretoria, Notificações de Saúde/Enfermaria, Avisos Gerais |
| | Biblioteca | Empréstimos Ativos dos Filhos, Prazos de Devolução e Multas Pendentes |
| | Simulados | Desempenho dos Filhos nos Simulados, Análise Comparativa e Evolução |
| **Serviços & Protocolos** | Protocolos da Família | Solicitação de Mudança de Turno, Autorização de Saída Antecipada, Documentos |
| | Documentação | Contratos de Prestação de Serviços Educacionais, Declarações de Quitação |
| | Privacidade & Menores | Consentimento de Uso de Imagem, Gerenciamento de Dados Pessoais dos Filhos |
| **Financeiro & Matrícula**| Central Financeira | Faturas e Mensalidades de Todos os Filhos, Pagamento via PIX Instantâneo, Carnê |
| | Matrícula & Contrato | Rematrícula Online dos Filhos, Assinatura Digital do Contrato de Matrícula |

---

### 4.6 Portal de Terceiros / Parceiros (`/thirdparty/*`)

| Seção Principal (Sidebar) | Módulo / Sub-Sidebar | Accordions & Páginas Requisitadas |
|---|---|---|
| **Portal de Terceiros** | Dashboard do Fornecedor | Faturas a Receber, Pedidos de Compra Pendentes, Contratos em Vigor, Mensagens |
| **Financeiro & Cobrança** | Faturamento de Serviços | Emissão e Upload de NF-e de Serviços, Acompanhamento de Liquidação Bancária, Extrato |
| **Serviços & Operações** | Documentos da Empresa | Certidões Negativas (CNDs), Contrato Social, Alvarás e Licenças, Seguro |
| | Prestação de Serviços | Ordens de Serviço (OS), Relatórios de Execução de Obra/Manutenção, Cronograma |
| | Solicitações & Chamados | Abertura de Chamados com a Manutenção Escolar, Solicitação de Acesso à Unidade |
| **Entidade & Governança** | Configurações do Fornecedor| Dados Cadastrais da Empresa, Responsáveis Técnicos, Dados Bancários |
| | Gestão de Integração | Integrações via API (Catracas, Fornecimento de Merenda, Livraria), Webhooks |
| | Privacidade & Segurança | Acordo de Processamento de Dados (DPA), Termo de Confidencialidade e LGPD |

---

## 5. Padrão Arquitetural de Páginas (Checklist 21 Itens de Layout)

Toda página nos 6 portais deve ser implementada com fidelidade ao modelo Master:

```
[ Banner de Contexto: Folder Tree + Nome do Accordion + Título da Página + Badge de Domínio Exclusivo ]

[ Card Master Unificado (.tb-card) ]
  ├── Header da Toolbar:
  │    ├── Segmented Pill Tabs: [ KPI (Ativo) ] [ Data Table ] [ Cards / Grid ] [ Kanban ] [ Analytics / Charts ]
  │    └── Ações: [ Dropdown Exportar (7 formatos) ] [ + Novo Registro ]
  │
  ├── Visão 1: KPI Overview
  │    ├── Grid responsivo de 4 a 6 KPI tiles com minibarras CSS/SVG e tendências
  │    └── Caixa de Destaques Operacionais e Governança do domínio
  │
  ├── Visão 2: Data Table
  │    ├── Barra de Ferramentas: Busca com Debounce (200ms) + Select de Status + Reset
  │    ├── Barra de Ações em Lote (Batch Bar): Contagem de seleção, Exportar e Excluir
  │    ├── Tabela: Coluna checkbox fixa à esquerda (.col-check) + Colunas de dados + Ações fixas à direita (.col-actions)
  │    │    └── Botões de ação mínimos: [ 👁️ Ver ] [ ✏️ Editar ] [ 🗑️ Excluir ]
  │    └── Barra de Paginação: Mostrando X-Y de Z, botões de página (‹‹ ‹ 1 2 3 › ››) e Seletor Por Página (5, 10, 25, 50)
  │
  ├── Visão 3: Cards / Grid
  │    ├── Grid responsivo de cartões com status badges temáticos e botões de ação
  │    └── Paginação independente do grid (cards por página: 6, 12, 24)
  │
  ├── Visão 4: Kanban Board
  │    ├── 4 Estágios de fluxo de trabalho operacional do domínio
  │    ├── Cards arrastáveis (draggable="true") com identificador, tag de cor, título e descrição
  │    └── Eventos HTML5 Drag & Drop delegados, com classe .drag-over na coluna e atualização otimista de contadores
  │
  └── Visão 5: Analytics & Charts
       ├── Gráfico 1: Barras ou Linhas com Chart.js 4.4 para volumetria do domínio
       └── Gráfico 2: Doughnut / Rosca para composição percentual de categorias

[ Drawers Laterais Supabase (Modais Deslizantes) ]
  ├── Drawer 1: Visualização de Detalhes (Read-Only)
  ├── Drawer 2: Cadastro / Edição com Stepper de 5 Passos (Geral → Configurações → Parâmetros → Segurança → Revisão)
  └── Drawer 3: Exclusão Segura com Destravamento por Digitação Obrigatória de "DELETE"
```

---

## 6. Governança de Segurança e Auditoria (Skills de Segurança)

Para cada página e rota especificada nos 6 portais, os seguintes requisitos de segurança são mandatórios:

1. **Prevenção de BOLA / IDOR**:
   - Abertura de Drawer de visualização, edição ou exclusão deve obrigatoriamente validar se o recurso pertence ao `tenant_id` ativo da sessão.
2. **Segurança de Autenticação e Hashing**:
   - Todas as senhas da plataforma utilizam **Argon2id** (OWASP 2025: $m=65536, t=4, p=1$).
3. **Isolamento Multi-Tenant**:
   - Queries preparadas PDO vinculam explicitamente `WHERE tenant_id = ? AND deleted_at IS NULL`.
4. **Política de Scripts e CSP Nonce**:
   - Proibição absoluta de manipuladores inline (`onclick`, `onchange`).
   - Todos os scripts embutidos utilizam `nonce="<?= \App\Security\CspNonce::get() ?>"`.
5. **Trilha de Auditoria Universal**:
   - Qualquer mutação realizada pelos Drawers registra evento estruturado em `audit_logs` contendo: `user_id`, `tenant_id`, `portal`, `action`, `entity_type`, `entity_id`, `ip_address`, `user_agent` e `payload_diff` (antes/depois).
6. **LGPD / Proteção de PII**:
   - CPF, e-mails, telefones e dados de saúde/menores mascarados na interface por padrão, com botão de revelação auditado.

---

## 7. Roteiro e Estratégia de Entrega dos Portais

A implementação física das páginas segue o padrão de catálogo e serviço modular:
1. **Configuração de Navegação**: Registro no arquivo `app/Config/sidebar-nav.php`.
2. **Camada de Serviço e Catálogo**: Criação de `PageService` de domínio (como `TenantPageService`, `AcademicPageService`, `TeacherPageService`, etc.) contendo KPIs reais, colunas, itens estruturados, estágios kanban e configurações analíticas de gráficos.
3. **Controladores**: Despacho no Controller correspondente resolvendo sub-caminhos e alimentando a view.
4. **Views**: Renderização sob o padrão 5-View Supabase Dark Emerald.
5. **Garantia de Qualidade**: Validação contínua através do suite `tests/SidebarNavConfigTest.php` e testes de renderização.
