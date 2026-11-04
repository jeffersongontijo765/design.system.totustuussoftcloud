# SPEC — Módulo: Gestão de Pessoas (HCM/RH)
**Plataforma:** TotusTuusSoftCloud SaaS  
**Stack:** PHP 8 puro · JavaScript Vanilla · Fetch API · Tailwind CSS 4.2 · Supabase · amCharts 5  
**Arquitetura:** Multi-entidade · Multi-unidade · Multi-usuário · Banco segregado por unidade  
**Versão:** 1.0.0 · **Data:** 2026-06-07  
**Autor:** Jefferson Augusto · TotusTuusSoftCloud  

- Language Standard: Global English
---

## Sumário

1. [Visão Geral](#visão-geral)
2. [Mapa de Páginas](#mapa-de-páginas)
3. [Dashboard Principal](#dashboard-principal)
4. [Colaboradores](#colaboradores)
5. [Recrutamento e Seleção](#recrutamento-e-seleção)
6. [Onboarding e Offboarding](#onboarding-e-offboarding)
7. [Cargos e Salários](#cargos-e-salários)
8. [Ponto e Jornada](#ponto-e-jornada)
9. [Folha de Pagamento](#folha-de-pagamento)
10. [Férias e Afastamentos](#férias-e-afastamentos)
11. [Treinamento e Desenvolvimento](#treinamento-e-desenvolvimento)
12. [Avaliação de Desempenho](#avaliação-de-desempenho)
13. [Benefícios](#benefícios)
14. [Saúde e Segurança do Trabalho](#saúde-e-segurança-do-trabalho)
15. [Documentos e Contratos RH](#documentos-e-contratos-rh)
16. [Relatórios e Analytics](#relatórios-e-analytics)
17. [Automações](#automações)
18. [API REST](#api-rest)
19. [Schema SQL](#schema-sql)
20. [RBAC — Perfis e Permissões](#rbac)
21. [LGPD / Compliance](#lgpd--compliance)
22. [Critérios de Aceite](#critérios-de-aceite)

---

## 1. Visão Geral

### Descrição
Módulo completo de Gestão de Capital Humano (HCM/RH) para gestão de colaboradores, recrutamento, folha de pagamento, ponto eletrônico, treinamentos, avaliações de desempenho, benefícios e saúde/segurança do trabalho (SST). Opera em contexto multi-entidade e multi-unidade.

### Perfis de Acesso (RBAC)
| Código | Perfil               | Nível de Acesso                                  |
|--------|----------------------|--------------------------------------------------|
| SA     | Super Admin          | Acesso total a todas entidades e unidades        |
| GE     | Gestor de Entidade   | Acesso total à entidade                          |
| GP     | Gestor de Pessoas    | Acesso total ao módulo RH                        |
| GU     | Gestor de Unidade    | Acesso restrito à unidade                        |
| RH     | Analista RH          | Operações RH sem exclusão e sem folha            |
| FIN    | Financeiro           | Leitura folha, benefícios, provisões             |
| COL    | Colaborador          | Autoatendimento (próprios dados, holerite, férias)|
| AUD    | Auditor              | Leitura total + audit_log                        |

### Rotas Base
```
/pessoas/dashboard
/pessoas/colaboradores
/pessoas/recrutamento
/pessoas/onboarding
/pessoas/cargos-salarios
/pessoas/ponto-jornada
/pessoas/folha
/pessoas/ferias-afastamentos
/pessoas/treinamentos
/pessoas/desempenho
/pessoas/beneficios
/pessoas/sst
/pessoas/documentos
/pessoas/relatorios
/pessoas/configuracoes
```

---

## 2. Mapa de Páginas

```
/pessoas/
├── dashboard/
├── colaboradores/
│   ├── index.php              — Listagem DataTable
│   ├── perfil.php             — Perfil completo colaborador
│   └── organograma.php        — Organograma interativo
├── recrutamento/
│   ├── vagas/index.php        — DataTable vagas
│   ├── candidatos/index.php   — DataTable candidatos
│   └── pipeline/index.php     — Kanban pipeline seleção
├── onboarding/
│   ├── index.php              — Kanban onboarding/offboarding
│   └── checklists/index.php   — DataTable checklists
├── cargos-salarios/
│   ├── cargos/index.php       — DataTable cargos
│   ├── faixas/index.php       — DataTable faixas salariais
│   └── estrutura/index.php    — Organograma hierárquico
├── ponto-jornada/
│   ├── registros/index.php    — DataTable batidas
│   ├── espelho/index.php      — Espelho de ponto mensal
│   ├── escalas/index.php      — DataTable escalas/turnos
│   └── ocorrencias/index.php  — DataTable ocorrências
├── folha/
│   ├── processamento/index.php — Kanban processamento folha
│   ├── holerites/index.php    — DataTable holerites
│   ├── eventos/index.php      — DataTable eventos/verbas
│   └── encargos/index.php     — DataTable encargos/FGTS/INSS
├── ferias-afastamentos/
│   ├── ferias/index.php       — DataTable + calendário
│   ├── afastamentos/index.php — DataTable afastamentos
│   └── programacao/index.php  — Calendário anual férias
├── treinamentos/
│   ├── index.php              — DataTable treinamentos
│   ├── turmas/index.php       — DataTable turmas
│   └── presenca/index.php     — Controle presença
├── desempenho/
│   ├── ciclos/index.php       — DataTable ciclos avaliação
│   ├── avaliacoes/index.php   — DataTable avaliações
│   └── metas/index.php        — Kanban metas/OKRs
├── beneficios/
│   ├── planos/index.php       — DataTable planos benefícios
│   └── colaboradores/index.php — DataTable vínculos benefícios
├── sst/
│   ├── exames/index.php       — DataTable exames ocupacionais
│   ├── acidentes/index.php    — DataTable CAT/acidentes
│   └── epi/index.php          — DataTable EPIs
├── documentos/
│   └── index.php              — DataTable documentos RH
└── relatorios/
    └── index.php              — Relatórios e analytics
```

---

## 3. Dashboard Principal

**Rota:** `/pessoas/dashboard/index.php`

### Widgets KPI — Linha 1 (6 cards)
| Widget                  | Valor         | Ícone               | Cor      | Tendência |
|-------------------------|---------------|---------------------|----------|-----------|
| Total Colaboradores     | `#total`      | ki-people           | primary  | vs. mês anterior |
| Admissões no Mês        | `#admissoes`  | ki-user-tick        | success  | vs. mês anterior |
| Desligamentos no Mês    | `#demissoes`  | ki-user-minus       | danger   | vs. mês anterior |
| Turnover (%)            | `#turnover`   | ki-arrows-circle    | warning  | vs. trimestre    |
| Headcount Ativo         | `#headcount`  | ki-briefcase        | info     | vs. mês anterior |
| Custo Total RH (R$)     | `#custo_rh`   | ki-dollar           | primary  | vs. mês anterior |

### Widgets KPI — Linha 2 (6 cards operacionais)
| Widget                     | Métrica           | Ação Rápida                  |
|----------------------------|-------------------|------------------------------|
| Vagas em Aberto            | count vagas        | → /recrutamento/vagas        |
| Onboardings Pendentes      | count onboarding   | → /onboarding                |
| Ponto Irregular Hoje       | count ocorrências  | → /ponto-jornada/ocorrencias |
| Folha em Processamento     | status folha mês   | → /folha/processamento       |
| Treinamentos Vencendo      | próximos 30 dias   | → /treinamentos              |
| Exames Médicos Vencidos    | count vencidos     | → /sst/exames                |

### Charts amCharts 5
| # | Tipo           | Título                          | Dados                                         |
|---|----------------|---------------------------------|-----------------------------------------------|
| 1 | Line dual-axis | Admissões vs Desligamentos      | 12 meses, linha verde + linha vermelha        |
| 2 | Donut          | Distribuição por Departamento   | % colaboradores por depto                    |
| 3 | Bar Grouped    | Headcount por Unidade           | agrupado por unidade/entidade                 |
| 4 | Bar Horizontal | Top 10 Cargos por Headcount     | ranking cargos mais ocupados                  |
| 5 | Area Stacked   | Custo RH Mensal (Salário+Encargos+Benefícios) | 12 meses stacked |
| 6 | Gauge          | Índice de Turnover              | meta vs realizado, gauge colorido             |

### DataTable — Admissões e Desligamentos Recentes
- Colunas: Colaborador · Cargo · Departamento · Unidade · Tipo (Admissão/Desligamento) · Data · Responsável · Status
- Filtros: Tipo · Departamento · Unidade · Período
- Ações: Ver perfil · Ver processo

### Painel de Alertas
- Ponto não registrado (colaboradores sem batida hoje)
- Férias vencendo nos próximos 30 dias
- Exames ocupacionais vencidos ou próximos do vencimento
- Treinamentos obrigatórios pendentes
- Documentos com prazo de validade próximo
- Contratos de experiência vencendo nos próximos 15 dias

---

## 4. Colaboradores

### 4.1 Listagem — `/pessoas/colaboradores/index.php`

#### Toolbar
```
[+ Novo Colaborador] [Importar CSV] [Exportar ▾] [Colunas ▾] [Filtros ▾]
```

#### Filtros Avançados (drawer lateral)
- Empresa/Entidade (multi-select)
- Unidade (multi-select)
- Departamento (multi-select)
- Cargo (multi-select)
- Status: Ativo · Férias · Afastado · Desligado
- Tipo Vínculo: CLT · PJ · Estágio · Temporário · Aprendiz
- Período de Admissão (date range)
- Centro de Custo (multi-select)
- Gestor (select)

#### DataTable Colaboradores
| Coluna           | Tipo        | Ordenável | Visível Padrão |
|------------------|-------------|-----------|----------------|
| #ID              | number      | sim       | não            |
| Avatar + Nome    | text+image  | sim       | sim            |
| Matrícula        | text        | sim       | sim            |
| Cargo            | text        | sim       | sim            |
| Departamento     | text        | sim       | sim            |
| Unidade          | text        | sim       | sim            |
| Tipo Vínculo     | badge       | sim       | sim            |
| Data Admissão    | date        | sim       | sim            |
| Status           | badge color | sim       | sim            |
| Gestor Direto    | text        | sim       | não            |
| Salário Base     | currency    | sim       | não (restrito) |
| Ações            | buttons     | não       | sim            |

**Ações por linha:** Ver Perfil · Editar · Afastar · Desligar · Mais (▾ Transferir / Holerites / Documentos)

**Bulk Actions:** Exportar selecionados · Enviar notificação · Atualizar status · Gerar relatório

#### Drawer — Novo/Editar Colaborador
**Abas do drawer:**
1. **Dados Pessoais** — Nome completo · CPF · RG · Data nascimento · Gênero · Estado civil · Nacionalidade · Naturalidade · PIS/NIS · Foto
2. **Dados de Contato** — E-mail pessoal · E-mail corporativo · Telefone · Celular · Endereço completo (CEP, logradouro, número, complemento, bairro, cidade, estado)
3. **Dados Contratuais** — Matrícula · Data admissão · Tipo vínculo · Regime trabalho (CLT/PJ) · CBO · CTPS número/série/UF · Data contrato experiência · Data término experiência · Data efetivação
4. **Cargo e Salário** — Cargo · Departamento · Centro de custo · Unidade · Nível hierárquico · Salário base · Data última promoção · Gestor direto
5. **Dados Bancários** — Banco · Agência · Conta · Tipo conta · Chave PIX
6. **Benefícios** — Selecionar planos ativos (checkbox list)
7. **Documentos** — Upload documentos (RG, CPF, CTPS, comprovante residência, certidões, diplomas)
8. **Acesso ao Sistema** — Criar login · Perfil de acesso · E-mail corporativo · Notificar colaborador

**Validações:**
- CPF: formato + dígito verificador
- PIS: dígito verificador
- CTPS: obrigatório para CLT
- Salário: mínimo maior que piso salarial da categoria
- Data experiência: máximo 90 dias (prorrogável 1× até 90 dias)

### 4.2 Perfil Completo — `/pessoas/colaboradores/perfil.php?id=:id`

**Layout tipo Supabase Profile Page:**
- Header: foto · nome · cargo · departamento · badges (status, vínculo) · botões ação (Editar · Afastar · Desligar · Holerites)
- Sidebar esquerda: informações pessoais · documentos · contatos de emergência
- Conteúdo principal (abas):
  - **Resumo** — KPIs do colaborador (tempo empresa, salário atual, férias disponíveis, treinamentos concluídos)
  - **Histórico** — Timeline de eventos (admissão, promoções, transferências, afastamentos, demissão)
  - **Documentos** — Lista de documentos com status validade
  - **Holerites** — Lista últimos 12 meses com download PDF
  - **Avaliações** — Histórico de avaliações de desempenho
  - **Treinamentos** — Treinamentos concluídos e pendentes
  - **Benefícios** — Benefícios ativos e histórico
  - **Ponto** — Espelho de ponto do mês atual

### 4.3 Organograma — `/pessoas/colaboradores/organograma.php`
- Visualização hierárquica interativa (amCharts 5 ForceDirected ou OrgChart)
- Filtros: Entidade · Unidade · Departamento · Nível hierárquico
- Interação: clique no card → abre modal com resumo do colaborador
- Exportar como PNG/SVG/PDF
- Toggle: Visão por departamento / Visão por gestor

---

## 5. Recrutamento e Seleção

### 5.1 Vagas — `/pessoas/recrutamento/vagas/index.php`

#### Toolbar
```
[+ Nova Vaga] [Exportar ▾] [Filtros ▾]
```

#### DataTable Vagas
| Coluna            | Tipo        |
|-------------------|-------------|
| Código            | text        |
| Título da Vaga    | text        |
| Departamento      | text        |
| Unidade           | text        |
| Tipo              | badge (Efetivo/Substituição/Estágio/Temp) |
| Modalidade        | badge (Presencial/Híbrido/Remoto) |
| Data Abertura     | date        |
| Prazo Encerramento | date       |
| Candidatos        | number      |
| Status            | badge       |
| Responsável       | text        |
| Ações             | buttons     |

#### Drawer — Nova/Editar Vaga
- Título · Código interno · Departamento · Cargo destino · Unidade · Tipo vaga · Modalidade · Quantidade vagas
- Salário ofertado (ou "a combinar") · Benefícios ofertados
- Descrição da vaga (editor rico) · Requisitos mínimos · Requisitos desejáveis · Atividades
- Responsável pelo processo · Gestor solicitante · Data prevista encerramento
- Status (Rascunho · Publicada · Em Seleção · Encerrada · Cancelada)
- Publicar em portais (checkboxes: site institucional, LinkedIn, Indeed, Gupy)

### 5.2 Candidatos — `/pessoas/recrutamento/candidatos/index.php`

#### DataTable Candidatos
| Coluna              | Tipo    |
|---------------------|---------|
| Nome                | text    |
| CPF / E-mail        | text    |
| Vaga Aplicada       | text    |
| Data Inscrição      | date    |
| Etapa Atual         | badge   |
| Fonte (Indicação/Portal/LinkedIn) | badge |
| Avaliação (score 0-10) | stars |
| Status              | badge   |
| Responsável         | text    |
| Ações               | buttons |

#### Drawer — Candidato
- Dados pessoais · Currículo (upload/visualização) · LinkedIn URL
- Vaga associada · Etapa atual · Score de triagem
- Histórico de etapas (timeline) · Anotações do recrutador
- Agendar entrevista (data/hora/local/responsável)

### 5.3 Kanban — Pipeline de Seleção — `/pessoas/recrutamento/pipeline/index.php`

#### Colunas do Kanban
| Coluna              | Cor     | Descrição                                 |
|---------------------|---------|-------------------------------------------|
| Triagem             | gray    | Candidatos recebidos, aguardando triagem  |
| Triagem Aprovada    | blue    | Aprovados na triagem inicial              |
| Teste/Prova         | yellow  | Em processo de avaliação técnica          |
| Entrevista RH       | purple  | Agendados para entrevista com RH          |
| Entrevista Gestor   | indigo  | Entrevista com gestor da área             |
| Proposta Enviada    | cyan    | Proposta de emprego enviada               |
| Contratado          | green   | Aceito e em processo de admissão          |
| Reprovado           | red     | Reprovado em qualquer etapa               |
| Desistência         | orange  | Candidato desistiu do processo            |

**Card do Kanban:**
- Avatar + Nome · Vaga · Score · Data entrada etapa · Responsável · Badge fonte
- Ações rápidas: Ver perfil · Mover etapa · Agendar entrevista · Reprovar

**Controles do Kanban:**
- Filtrar por: Vaga · Responsável · Período · Fonte
- Toggle: Visualização Kanban / DataTable
- Drag & drop entre colunas (atualiza via Fetch PATCH)
- Contador de cards por coluna

---

## 6. Onboarding e Offboarding

### 6.1 Kanban — `/pessoas/onboarding/index.php`

#### Colunas Onboarding
| Coluna                   | Cor    |
|--------------------------|--------|
| Pré-Admissão             | gray   |
| Documentação Pendente    | yellow |
| Documentação Completa    | blue   |
| Integração TI            | purple |
| Treinamento Inicial      | indigo |
| Integração Concluída     | green  |

#### Colunas Offboarding
| Coluna                   | Cor    |
|--------------------------|--------|
| Aviso Prévio             | orange |
| Devoluções Pendentes     | yellow |
| Acesso Revogado          | red    |
| Documentação Rescisão    | blue   |
| Homologação Pendente     | purple |
| Desligado                | gray   |

**Card do Kanban:**
- Avatar + Nome · Cargo · Departamento · Data admissão/desligamento
- Checklist de tarefas (progress bar %) · Responsável · Prazo
- Alertas: itens vencidos (badge vermelho)

### 6.2 Checklists — `/pessoas/onboarding/checklists/index.php`
- Templates de checklist configuráveis por tipo de vínculo
- Drawer CRUD: Nome da tarefa · Responsável · Prazo (dias após admissão) · Obrigatória · Departamento executor
- DataTable: Colaborador · Tipo · Progresso · Itens pendentes · Responsável · Prazo · Status

---

## 7. Cargos e Salários

### 7.1 Cargos — `/pessoas/cargos-salarios/cargos/index.php`

#### DataTable Cargos
| Coluna              | Tipo    |
|---------------------|---------|
| Código              | text    |
| Título do Cargo     | text    |
| CBO                 | text    |
| Departamento        | text    |
| Nível Hierárquico   | badge   |
| Colaboradores       | number  |
| Salário Mínimo      | currency|
| Salário Médio       | currency|
| Salário Máximo      | currency|
| Status              | badge   |
| Ações               | buttons |

#### Drawer — Cargo
- Título · Código · CBO · Descrição sumária · Atribuições e responsabilidades (editor)
- Departamento · Área · Nível hierárquico (Jr/Pl/Sr/Coordenador/Gerente/Diretor)
- Competências técnicas requeridas · Competências comportamentais
- Requisito de formação · Requisito de experiência (anos)
- Faixa salarial (mínimo, médio, máximo) · Gratificações e adicionais típicos

### 7.2 Faixas Salariais — `/pessoas/cargos-salarios/faixas/index.php`
- DataTable: Cargo · Nível · Faixa A (início) · Faixa B · Faixa C (meio) · Faixa D · Faixa E (máximo) · Vigência · Revisão
- Drawer CRUD: definir faixas por cargo/nível com vigência
- Histórico de revisões salariais

### 7.3 Estrutura Hierárquica — `/pessoas/cargos-salarios/estrutura/index.php`
- Organograma de cargos (visual interativo)
- Filtros por departamento/área
- Exportar PDF

---

## 8. Ponto e Jornada

### 8.1 Registros de Ponto — `/pessoas/ponto-jornada/registros/index.php`

#### Toolbar
```
[Importar Registros] [Processar Período ▾] [Exportar ▾] [Filtros ▾]
```

#### DataTable Registros
| Coluna              | Tipo        |
|---------------------|-------------|
| Colaborador         | text        |
| Matrícula           | text        |
| Data                | date        |
| Entrada             | time        |
| Saída Intervalo     | time        |
| Retorno Intervalo   | time        |
| Saída               | time        |
| Horas Trabalhadas   | duration    |
| Horas Previstas     | duration    |
| Diferença           | duration    |
| Ocorrência          | badge       |
| Status              | badge       |
| Ações               | buttons     |

**Filtros:** Colaborador · Departamento · Unidade · Período · Ocorrência · Status

#### Drawer — Ajuste Manual de Ponto
- Colaborador (somente leitura se acessado da linha)
- Data · Tipo batida (Entrada/Saída Intervalo/Retorno Intervalo/Saída)
- Hora original · Nova hora · Motivo do ajuste (select: Esquecimento/Viagem/Home Office/Falha Equipamento/Outro)
- Descrição complementar · Aprovador · Anexar documento justificativo
- Histórico de ajustes anteriores na data

### 8.2 Espelho de Ponto — `/pessoas/ponto-jornada/espelho/index.php`
- Seletor colaborador + mês/ano
- Tabela mensal: dia · dia semana · jornada prevista · entrada/saídas registradas · horas trabalhadas · saldo · ocorrências · status
- Totalizadores: horas normais · horas extras 50% · horas extras 100% · DSR · faltas · atrasos · banco de horas
- Botão: Fechar Espelho · Enviar para Colaborador · Exportar PDF

### 8.3 Escalas e Turnos — `/pessoas/ponto-jornada/escalas/index.php`
- DataTable: Nome da escala · Tipo (fixo/variável/turno/12x36/6x1) · Jornada semanal · Colaboradores · Vigência · Status
- Drawer CRUD: definir horários por dia da semana · tolerância · intervalo mínimo/máximo · DSR

### 8.4 Ocorrências — `/pessoas/ponto-jornada/ocorrencias/index.php`
- DataTable: Colaborador · Data · Tipo ocorrência · Justificativa · Documento · Status (Pendente/Justificado/Injustificado/Aprovado)
- Drawer resolução: aceitar justificativa · reprovar · adicionar observação
- Bulk: aprovar selecionados

---

## 9. Folha de Pagamento

### 9.1 Kanban — Processamento — `/pessoas/folha/processamento/index.php`

#### Colunas Kanban Folha
| Coluna                    | Cor     |
|---------------------------|---------|
| Aguardando Fechamento Ponto | gray  |
| Ponto Fechado             | blue    |
| Processando Eventos       | yellow  |
| Aguardando Aprovação      | purple  |
| Aprovada                  | indigo  |
| Geração de Pagamento      | cyan    |
| Paga / Encerrada          | green   |
| Com Pendência             | red     |

**Card do Kanban (por competência/unidade):**
- Competência (mês/ano) · Unidade · Quantidade colaboradores · Valor total bruto
- Responsável · Data processamento · Prazo pagamento · Alertas de pendências

### 9.2 Holerites — `/pessoas/folha/holerites/index.php`
- DataTable: Colaborador · Matrícula · Competência · Salário Bruto · Descontos · Salário Líquido · Status (Gerado/Enviado/Visualizado) · Ações (Ver · Download PDF · Reenviar)
- Filtros: Competência · Departamento · Unidade · Status
- Bulk: Enviar todos por e-mail/portal

### 9.3 Eventos e Verbas — `/pessoas/folha/eventos/index.php`
- DataTable: Código · Descrição · Tipo (Provento/Desconto/Informativo) · Natureza · Incidência INSS/FGTS/IRRF · Status
- Drawer CRUD: Cadastro completo de verbas com fórmulas de cálculo

### 9.4 Encargos — `/pessoas/folha/encargos/index.php`
- DataTable por competência: INSS Patronal · FGTS · RAT/SAT · Terceiros · Total encargos · Guia gerada · Status pagamento
- Resumo: visão consolidada por entidade/unidade
- Drawer: gerar guias DARF/GPS/GFIP

---

## 10. Férias e Afastamentos

### 10.1 Férias — `/pessoas/ferias-afastamentos/ferias/index.php`

#### DataTable Férias
| Coluna              | Tipo        |
|---------------------|-------------|
| Colaborador         | text        |
| Período Aquisitivo  | date range  |
| Dias Disponíveis    | number      |
| Dias Vendidos       | number      |
| Data Início Gozo    | date        |
| Data Fim Gozo       | date        |
| Data Pagamento      | date        |
| Status              | badge       |
| Ações               | buttons     |

**Status Férias:** Aquisitivo em Curso · Período Disponível · Programadas · Em Gozo · Concluídas · Vencidas

#### Drawer — Programar Férias
- Colaborador · Período aquisitivo (auto)
- Dias de gozo · Abono pecuniário (dias vendidos, máx 1/3)
- Data início · Data fim (calculada) · Data pagamento (obrigatório: 2 dias antes)
- Gestor aprovador · Observações

#### Alerta: Férias Vencidas
- Widget destacado quando colaborador atingir 24 meses sem férias
- Fila de férias urgentes no dashboard

### 10.2 Afastamentos — `/pessoas/ferias-afastamentos/afastamentos/index.php`
- DataTable: Colaborador · Tipo (INSS/Acidente/Licença/Outro) · Data Início · Data Retorno Previsto · Data Retorno Real · CID (mascarado LGPD) · Status
- Drawer CRUD: Tipos configuráveis · upload atestado/laudo · protocolo INSS (B31/B91/B94) · impacto folha

### 10.3 Calendário Férias — `/pessoas/ferias-afastamentos/programacao/index.php`
- Visualização anual em linha do tempo (amCharts 5 timeline/gantt)
- Filtros: Departamento · Unidade · Ano
- Identificação de conflitos (mesmo período, mesmo depto)
- Exportar PDF calendário anual

---

## 11. Treinamento e Desenvolvimento

### 11.1 Treinamentos — `/pessoas/treinamentos/index.php`

#### DataTable Treinamentos
| Coluna              | Tipo        |
|---------------------|-------------|
| Código              | text        |
| Nome do Treinamento | text        |
| Tipo (Interno/Externo/EAD) | badge |
| Categoria           | text        |
| Carga Horária       | number      |
| Obrigatório         | boolean     |
| Periodicidade (meses) | number   |
| Inscritos           | number      |
| Concluídos          | number      |
| Status              | badge       |
| Ações               | buttons     |

#### Drawer — Treinamento
- Nome · Código · Tipo · Categoria · Descrição · Objetivo
- Carga horária · Modalidade (Presencial/Online/Híbrido) · Fornecedor/Instrutor
- Obrigatório (sim/não) · Público alvo (cargos/departamentos) · Periodicidade de renovação
- Material de apoio (upload) · Certificado automático (sim/não)

### 11.2 Turmas — `/pessoas/treinamentos/turmas/index.php`
- DataTable: Treinamento · Turma · Data Início · Data Fim · Local/Link · Vagas · Inscritos · Status
- Drawer: criar turma com calendário de aulas
- Inscrever colaboradores em massa (import CSV ou seleção na datatable)

### 11.3 Controle de Presença — `/pessoas/treinamentos/presenca/index.php`
- Seletor turma/data
- Listagem colaboradores com toggle presente/ausente
- Observações por colaborador
- Emitir lista de presença PDF
- Emitir certificados em lote (PDF gerado server-side)

---

## 12. Avaliação de Desempenho

### 12.1 Ciclos de Avaliação — `/pessoas/desempenho/ciclos/index.php`

#### DataTable Ciclos
| Coluna              | Tipo        |
|---------------------|-------------|
| Nome do Ciclo       | text        |
| Tipo (360°/180°/90°/Autoavaliação) | badge |
| Período             | date range  |
| Colaboradores Avaliados | number  |
| Concluídos (%)      | progress    |
| Status              | badge       |
| Ações               | buttons     |

#### Drawer — Novo Ciclo
- Nome · Período (data início/fim) · Tipo de avaliação
- Formulário de avaliação (construtor de perguntas/critérios com peso)
- Incluir autoavaliação (sim/não) · Avaliação pelo gestor (sim/não) · 360° (sim/não)
- Público alvo (todos / por cargo / por departamento / por unidade)
- Notificações automáticas (e-mail/push)

### 12.2 Avaliações — `/pessoas/desempenho/avaliacoes/index.php`
- DataTable: Avaliado · Avaliador · Ciclo · Tipo · Nota Final · Status (Pendente/Em Preenchimento/Concluída) · Data conclusão
- Ação: Preencher avaliação (abre formulário inline ou drawer)

### 12.3 Kanban — Metas e OKRs — `/pessoas/desempenho/metas/index.php`

#### Colunas Kanban Metas
| Coluna         | Cor     |
|----------------|---------|
| Backlog        | gray    |
| Em Progresso   | blue    |
| Em Revisão     | yellow  |
| Concluída      | green   |
| Cancelada      | red     |

**Card de Meta:**
- Título da meta · Responsável · Período · Indicador KPI · Progresso (%) · Prazo

---

## 13. Benefícios

### 13.1 Planos de Benefícios — `/pessoas/beneficios/planos/index.php`

#### DataTable Planos
| Coluna              | Tipo    |
|---------------------|---------|
| Nome do Benefício   | text    |
| Tipo (Saúde/Odonto/VA/VR/Transporte/Seguro/Outro) | badge |
| Fornecedor          | text    |
| Custo Empresa (R$)  | currency|
| Desconto Colaborador (R$) | currency |
| Elegíveis           | number  |
| Ativos              | number  |
| Vigência            | date    |
| Status              | badge   |
| Ações               | buttons |

#### Drawer — Plano Benefício
- Nome · Tipo · Fornecedor/Operadora · CNPJ fornecedor
- Descricão · Regras de elegibilidade (tipo vínculo, tempo empresa, cargo)
- Custo empresa · Desconto colaborador · Forma desconto (fixo/percentual)
- Vigência (início/fim) · Cobertura (colaborador/dependentes)
- Upload apólice/contrato

### 13.2 Benefícios Colaboradores — `/pessoas/beneficios/colaboradores/index.php`
- DataTable: Colaborador · Benefício · Fornecedor · Vigência · Custo Empresa · Desconto Col. · Status (Ativo/Suspenso/Cancelado)
- Filtros: Tipo benefício · Unidade · Status
- Bulk: suspender/reativar benefícios

---

## 14. Saúde e Segurança do Trabalho (SST)

### 14.1 Exames Ocupacionais — `/pessoas/sst/exames/index.php`

#### DataTable Exames
| Coluna              | Tipo        |
|---------------------|-------------|
| Colaborador         | text        |
| Tipo Exame (Adm/Periódico/Retorno/Demissional) | badge |
| Data Realização     | date        |
| Data Vencimento     | date        |
| Médico / Clínica    | text        |
| ASO Resultado (Apto/Inapto/Apto com Restr.) | badge |
| Status              | badge color |
| Ações               | buttons     |

**Alertas visuais:** vencido (vermelho) · vencendo em 30 dias (amarelo)

#### Drawer — Exame
- Colaborador · Tipo exame · Data realização · Próximo vencimento
- Médico/Clínica · CRM médico · Resultado ASO · Restrições
- Upload ASO (PDF) · CID se afastamento (mascarado LGPD)

### 14.2 Acidentes e CAT — `/pessoas/sst/acidentes/index.php`
- DataTable: Colaborador · Data Acidente · Tipo (Típico/Trajeto/Doença Ocupacional) · CID · CAT Emitida · INSS Comunicado · Dias Afastado · Status
- Drawer CRUD: relatório de acidente completo com circunstâncias, testemunhas, CAT número
- Gerar CAT automático (e-CAT)

### 14.3 EPIs — `/pessoas/sst/epi/index.php`
- DataTable: Colaborador · EPI · CA (Certificado Aprovação) · Data Entrega · Validade · Devolvido · Responsável
- Drawer CRUD: registrar entrega/devolução de EPI com assinatura digital (canvas)
- Alerta EPIs vencidos ou não entregues

---

## 15. Documentos e Contratos RH

### `/pessoas/documentos/index.php`

#### DataTable Documentos
| Coluna              | Tipo        |
|---------------------|-------------|
| Colaborador         | text        |
| Tipo Documento      | badge       |
| Nome Arquivo        | text        |
| Data Upload         | date        |
| Validade            | date        |
| Status Validação    | badge       |
| Responsável         | text        |
| Ações               | buttons     |

**Tipos de documentos:** RG · CPF · CTPS · CNH · Diploma · Certidão civil · ASO · Contrato trabalho · Aditivo · Termo rescisão · Certificados treinamento · Outros

#### Drawer — Documento
- Colaborador · Tipo · Descrição · Data emissão · Data validade
- Upload arquivo (PDF/JPEG/PNG, máx 10MB) · Validado (sim/não) · Observações

#### Controles extras
- Alerta documentos vencendo (30/15/7 dias)
- Exportar pasta ZIP com documentos do colaborador
- Histórico de versões de documentos

---

## 16. Relatórios e Analytics

### `/pessoas/relatorios/index.php`

#### Relatórios Disponíveis
| Relatório                          | Filtros Principais                    | Exportação       |
|------------------------------------|---------------------------------------|------------------|
| Headcount por Período              | Entidade, Unidade, Depto, Data        | Excel/CSV/PDF    |
| Admissões e Demissões              | Período, Tipo, Motivo                 | Excel/CSV/PDF    |
| Turnover Mensal/Anual              | Período, Departamento, Cargo          | Excel/PDF        |
| Custo de Pessoal Consolidado       | Competência, Unidade, CC             | Excel/PDF        |
| Folha Analítica                    | Competência, Colaborador, Verba       | Excel/PDF        |
| Banco de Horas                     | Colaborador, Período, Unidade         | Excel/PDF        |
| Absenteísmo                        | Período, Tipo ocorrência, Depto       | Excel/PDF        |
| Férias Pendentes / Vencidas        | Unidade, Departamento                 | Excel/PDF        |
| Exames Vencidos / Próximos         | Tipo, Unidade, Período                | Excel/PDF        |
| Treinamentos por Colaborador       | Treinamento, Período, Status          | Excel/PDF        |
| Avaliações de Desempenho           | Ciclo, Departamento, Nota             | Excel/PDF        |
| Declaração de Benefícios           | Colaborador, Competência              | PDF              |
| RAIS (layout oficial)              | Ano base, Entidade                    | TXT (RAIS)       |
| CAGED (layout oficial)             | Competência, Entidade                 | TXT (CAGED)      |
| eSocial — eventos pendentes        | Competência, Tipo evento              | XML/Visualização |
| DIRF                               | Ano base                              | TXT (DIRF)       |

---

## 17. Automações

### 17.1 Engine de Automações
- Trigger-based: evento → condição → ação
- Configurável por perfil GP/SA via interface

### 17.2 Automações Disponíveis

| ID  | Trigger                                     | Condição                          | Ação                                                        |
|-----|---------------------------------------------|-----------------------------------|-------------------------------------------------------------|
| A01 | Admissão registrada                         | Tipo vínculo = CLT                | Criar checklist onboarding · Notificar TI · Agendar exame admissional |
| A02 | Data = 15 dias antes fim experiência        | Status = Ativo                    | Notificar gestor para decisão de efetivação/desligamento    |
| A03 | Desligamento registrado                     | Sempre                            | Criar checklist offboarding · Revogar acessos · Notificar TI/Financeiro |
| A04 | Período aquisitivo completado (12 meses)    | Status = Ativo                    | Notificar RH e gestor · Atualizar saldo férias              |
| A05 | Férias não programadas com 60+ dias aviso   | Saldo ≥ 30 dias                   | Alertar RH e gestor com urgência                            |
| A06 | Exame médico vencido                        | Data vencimento < hoje            | Notificar RH · Badge alerta no perfil do colaborador        |
| A07 | Treinamento obrigatório vencendo            | 30 dias antes vencimento          | Notificar colaborador e RH · Criar tarefa no onboarding     |
| A08 | Fechamento de ponto mensal                  | Dia = config empresa              | Iniciar processamento de folha · Notificar RH               |
| A09 | Avaliação de desempenho não concluída       | 3 dias antes do prazo             | Notificar avaliador por e-mail/push                         |
| A10 | Aniversário de empresa (N anos)             | Configurável por entidade         | Notificar RH · Gerar badge/certificado de tempo de casa     |
| A11 | Colaborador atingir piso faixa salarial     | Revisão anual programada          | Notificar GP para revisão salarial                          |
| A12 | CAT registrada (acidente)                   | Sempre                            | Notificar SESMT · Iniciar comunicação eSocial               |
| A13 | Documento vencendo em 30 dias               | Tipo = ASO/CNH/Certidão           | Notificar colaborador e RH para renovação                   |
| A14 | Folha aprovada                              | Status = Aprovada                 | Gerar arquivo de pagamento · Notificar financeiro           |

### 17.3 Configuração de Automações
- Ativar/desativar por entidade/unidade
- Definir canal de notificação: e-mail · push interno · webhook · SMS (externo)
- Delay configurável (imediato / X horas / X dias)
- Log de execuções (sucesso/falha) auditável

---

## 18. API REST

### Padrão
```
Base URL: /api/v1/pessoas/
Auth: Bearer JWT (header Authorization)
Content-Type: application/json
Rate Limit: 1000 req/min por token
```

### Endpoints Principais

| Método | Rota                                      | Descrição                          | Permissão |
|--------|-------------------------------------------|------------------------------------|-----------|
| GET    | /colaboradores                            | Listar colaboradores               | GP/GU/RH  |
| POST   | /colaboradores                            | Criar colaborador                  | GP        |
| GET    | /colaboradores/:id                        | Detalhes colaborador               | GP/GU/RH  |
| PUT    | /colaboradores/:id                        | Atualizar colaborador              | GP        |
| DELETE | /colaboradores/:id                        | Desativar colaborador              | SA/GE     |
| GET    | /colaboradores/:id/historico              | Timeline histórico                 | GP/RH     |
| GET    | /colaboradores/:id/documentos             | Documentos do colaborador          | GP/RH     |
| POST   | /colaboradores/:id/documentos             | Upload documento                   | GP/RH     |
| GET    | /colaboradores/:id/holerites              | Holerites do colaborador           | GP/FIN/COL|
| GET    | /recrutamento/vagas                       | Listar vagas                       | GP/RH     |
| POST   | /recrutamento/vagas                       | Criar vaga                         | GP        |
| PUT    | /recrutamento/vagas/:id                   | Atualizar vaga                     | GP        |
| GET    | /recrutamento/candidatos                  | Listar candidatos                  | GP/RH     |
| POST   | /recrutamento/candidatos                  | Criar candidato                    | GP/RH     |
| PATCH  | /recrutamento/candidatos/:id/etapa        | Mover etapa kanban                 | GP/RH     |
| GET    | /ponto/registros                          | Listar registros ponto             | GP/GU/RH  |
| POST   | /ponto/registros                          | Criar batida manual                | GP        |
| PUT    | /ponto/registros/:id                      | Ajustar batida                     | GP        |
| GET    | /ponto/espelho/:colaborador_id/:mes       | Espelho mensal                     | GP/RH/COL |
| GET    | /folha                                    | Listar folhas por competência      | GP/FIN    |
| POST   | /folha/processar                          | Iniciar processamento              | GP        |
| PATCH  | /folha/:id/aprovar                        | Aprovar folha                      | GE/GP     |
| GET    | /folha/:id/holerites                      | Holerites da competência           | GP/FIN    |
| GET    | /ferias                                   | Listar férias                      | GP/GU/RH  |
| POST   | /ferias                                   | Programar férias                   | GP        |
| PUT    | /ferias/:id                               | Atualizar programação              | GP        |
| GET    | /afastamentos                             | Listar afastamentos                | GP/GU/RH  |
| POST   | /afastamentos                             | Registrar afastamento              | GP/RH     |
| GET    | /treinamentos                             | Listar treinamentos                | GP/RH/COL |
| POST   | /treinamentos/turmas/:id/presenca         | Registrar presença                 | GP/RH     |
| GET    | /desempenho/ciclos                        | Listar ciclos                      | GP/RH     |
| POST   | /desempenho/avaliacoes                    | Salvar avaliação                   | GP/RH/COL |
| GET    | /beneficios/planos                        | Listar planos                      | GP/FIN    |
| POST   | /sst/exames                               | Registrar exame                    | GP/RH     |
| GET    | /sst/exames/vencidos                      | Exames vencidos                    | GP/RH     |
| GET    | /relatorios/:tipo                         | Gerar relatório                    | GP/FIN/AUD|
| GET    | /dashboard/kpis                           | KPIs do dashboard                  | GP/GU     |
| POST   | /automacoes/:id/executar                  | Executar automação manualmente     | SA/GP     |

---

## 19. Schema SQL

```sql
-- Tabela principal de colaboradores
CREATE TABLE hcm_employees (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    user_id         BIGINT UNSIGNED NULL,        -- link para users (login sistema)
    registration    VARCHAR(20) NOT NULL,         -- matrícula
    full_name       VARCHAR(150) NOT NULL,
    cpf             VARCHAR(14) NOT NULL,         -- criptografado (LGPD)
    rg              VARCHAR(20) NULL,             -- criptografado (LGPD)
    birth_date      DATE NULL,                    -- criptografado (LGPD)
    gender          ENUM('M','F','NB','NI') DEFAULT 'NI',
    marital_status  ENUM('solteiro','casado','divorciado','viuvo','uniao_estavel','outro') NULL,
    nationality     VARCHAR(50) DEFAULT 'brasileiro',
    pis_nis         VARCHAR(11) NULL,             -- criptografado (LGPD)
    email_personal  VARCHAR(150) NULL,            -- criptografado (LGPD)
    email_corporate VARCHAR(150) NULL,
    phone           VARCHAR(20) NULL,
    mobile          VARCHAR(20) NULL,
    address_zip     VARCHAR(9) NULL,
    address_street  VARCHAR(200) NULL,
    address_number  VARCHAR(10) NULL,
    address_complement VARCHAR(50) NULL,
    address_neighborhood VARCHAR(100) NULL,
    address_city    VARCHAR(100) NULL,
    address_state   CHAR(2) NULL,
    photo_path      VARCHAR(255) NULL,
    -- Dados contratuais
    admission_date  DATE NOT NULL,
    contract_type   ENUM('clt','pj','estagio','temporario','aprendiz','autonomo') NOT NULL,
    work_regime     ENUM('presencial','hibrido','remoto') DEFAULT 'presencial',
    ctps_number     VARCHAR(20) NULL,
    ctps_series     VARCHAR(10) NULL,
    ctps_uf         CHAR(2) NULL,
    experience_end_date DATE NULL,
    effective_date  DATE NULL,
    termination_date DATE NULL,
    termination_reason VARCHAR(100) NULL,
    termination_type ENUM('voluntario','involuntario','acordo','aposentadoria','morte','outro') NULL,
    status          ENUM('ativo','ferias','afastado','desligado','suspenso') DEFAULT 'ativo',
    -- Cargo e depto
    job_id          BIGINT UNSIGNED NULL,
    department_id   BIGINT UNSIGNED NULL,
    cost_center_id  BIGINT UNSIGNED NULL,
    manager_id      BIGINT UNSIGNED NULL,
    -- Salário
    base_salary     DECIMAL(12,2) NULL,          -- criptografado (LGPD)
    salary_date     DATE NULL,
    -- LGPD
    consent_at      DATETIME NULL,
    consent_ip      VARCHAR(45) NULL,
    anonymized_at   DATETIME NULL,
    -- Controle
    created_by      BIGINT UNSIGNED NULL,
    updated_by      BIGINT UNSIGNED NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at      TIMESTAMP NULL,
    INDEX idx_entity_unit (entity_id, unit_id),
    INDEX idx_status (status),
    INDEX idx_admission (admission_date),
    INDEX idx_job (job_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Cargos
CREATE TABLE hcm_jobs (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    entity_id       BIGINT UNSIGNED NOT NULL,
    code            VARCHAR(20) NOT NULL,
    title           VARCHAR(150) NOT NULL,
    cbo             VARCHAR(10) NULL,
    department_id   BIGINT UNSIGNED NULL,
    hierarchy_level ENUM('assistente','analista_jr','analista_pl','analista_sr','especialista','coordenador','supervisor','gerente','diretor','vp','ceo') NOT NULL,
    description     TEXT NULL,
    min_salary      DECIMAL(12,2) NULL,
    mid_salary      DECIMAL(12,2) NULL,
    max_salary      DECIMAL(12,2) NULL,
    status          ENUM('ativo','inativo') DEFAULT 'ativo',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_entity (entity_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Registro de ponto
CREATE TABLE hcm_time_records (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    employee_id     BIGINT UNSIGNED NOT NULL,
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    record_date     DATE NOT NULL,
    entry           TIME NULL,
    break_start     TIME NULL,
    break_end       TIME NULL,
    exit            TIME NULL,
    worked_minutes  SMALLINT UNSIGNED NULL,
    expected_minutes SMALLINT UNSIGNED NULL,
    balance_minutes SMALLINT NULL,
    occurrence_type ENUM('normal','falta','atraso','hora_extra','abono','feriado','dsrao') DEFAULT 'normal',
    status          ENUM('aberto','ajustado','aprovado','fechado') DEFAULT 'aberto',
    adjustment_reason VARCHAR(200) NULL,
    adjusted_by     BIGINT UNSIGNED NULL,
    adjusted_at     DATETIME NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_employee_date (employee_id, record_date),
    INDEX idx_entity_unit (entity_id, unit_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Folha de pagamento
CREATE TABLE hcm_payroll (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    competence      CHAR(7) NOT NULL,            -- YYYY-MM
    payroll_type    ENUM('mensal','ferias','13_primeiro','13_segundo','rescisao','adiantamento') DEFAULT 'mensal',
    status          ENUM('aguardando_ponto','ponto_fechado','processando','aguardando_aprovacao','aprovada','paga','pendencia') DEFAULT 'aguardando_ponto',
    total_gross     DECIMAL(14,2) DEFAULT 0,
    total_discounts DECIMAL(14,2) DEFAULT 0,
    total_net       DECIMAL(14,2) DEFAULT 0,
    total_employees INT UNSIGNED DEFAULT 0,
    payment_date    DATE NULL,
    approved_by     BIGINT UNSIGNED NULL,
    approved_at     DATETIME NULL,
    processed_by    BIGINT UNSIGNED NULL,
    processed_at    DATETIME NULL,
    notes           TEXT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_entity_competence (entity_id, competence)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Itens da folha (holerite)
CREATE TABLE hcm_payroll_items (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payroll_id      BIGINT UNSIGNED NOT NULL,
    employee_id     BIGINT UNSIGNED NOT NULL,
    event_code      VARCHAR(10) NOT NULL,
    event_name      VARCHAR(100) NOT NULL,
    event_type      ENUM('provento','desconto','informativo') NOT NULL,
    reference       DECIMAL(10,4) NULL,           -- horas/dias/percentual
    value           DECIMAL(12,2) NOT NULL,
    inss_incidence  TINYINT(1) DEFAULT 0,
    fgts_incidence  TINYINT(1) DEFAULT 0,
    irrf_incidence  TINYINT(1) DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_payroll_employee (payroll_id, employee_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Férias
CREATE TABLE hcm_vacations (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    employee_id     BIGINT UNSIGNED NOT NULL,
    acquisitive_start DATE NOT NULL,
    acquisitive_end   DATE NOT NULL,
    available_days  TINYINT UNSIGNED DEFAULT 30,
    sold_days       TINYINT UNSIGNED DEFAULT 0,
    start_date      DATE NULL,
    end_date        DATE NULL,
    payment_date    DATE NULL,
    status          ENUM('aquisitivo','disponivel','programadas','em_gozo','concluidas','vencidas') DEFAULT 'aquisitivo',
    approved_by     BIGINT UNSIGNED NULL,
    approved_at     DATETIME NULL,
    notes           TEXT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_employee (employee_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Afastamentos
CREATE TABLE hcm_absences (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    employee_id     BIGINT UNSIGNED NOT NULL,
    absence_type    ENUM('inss_doenca','inss_acidente','maternidade','paternidade','licenca_remunerada','licenca_nao_remunerada','suspensao','outro') NOT NULL,
    cid_code        VARCHAR(10) NULL,             -- criptografado (LGPD)
    start_date      DATE NOT NULL,
    expected_return DATE NULL,
    actual_return   DATE NULL,
    inss_protocol   VARCHAR(30) NULL,
    document_path   VARCHAR(255) NULL,
    status          ENUM('ativo','encerrado','cancelado') DEFAULT 'ativo',
    notes           TEXT NULL,
    created_by      BIGINT UNSIGNED NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_employee (employee_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Vagas de recrutamento
CREATE TABLE hcm_job_openings (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NOT NULL,
    code            VARCHAR(20) NOT NULL,
    title           VARCHAR(150) NOT NULL,
    job_id          BIGINT UNSIGNED NULL,
    department_id   BIGINT UNSIGNED NULL,
    opening_type    ENUM('efetivo','substituicao','estagio','temporario','aprendiz') NOT NULL,
    work_mode       ENUM('presencial','hibrido','remoto') DEFAULT 'presencial',
    quantity        TINYINT UNSIGNED DEFAULT 1,
    salary_from     DECIMAL(12,2) NULL,
    salary_to       DECIMAL(12,2) NULL,
    salary_hidden   TINYINT(1) DEFAULT 0,
    description     LONGTEXT NULL,
    requirements    TEXT NULL,
    desired         TEXT NULL,
    activities      TEXT NULL,
    owner_id        BIGINT UNSIGNED NULL,
    open_date       DATE NOT NULL,
    close_date      DATE NULL,
    status          ENUM('rascunho','publicada','em_selecao','encerrada','cancelada') DEFAULT 'rascunho',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_entity_status (entity_id, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Candidatos
CREATE TABLE hcm_candidates (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    job_opening_id  BIGINT UNSIGNED NOT NULL,
    full_name       VARCHAR(150) NOT NULL,
    cpf             VARCHAR(14) NULL,             -- criptografado (LGPD)
    email           VARCHAR(150) NULL,            -- criptografado (LGPD)
    phone           VARCHAR(20) NULL,
    linkedin_url    VARCHAR(255) NULL,
    source          ENUM('indicacao','site','linkedin','indeed','gupy','outro') DEFAULT 'outro',
    cv_path         VARCHAR(255) NULL,
    pipeline_stage  ENUM('triagem','triagem_aprovada','teste','entrevista_rh','entrevista_gestor','proposta','contratado','reprovado','desistencia') DEFAULT 'triagem',
    score           TINYINT UNSIGNED NULL,
    notes           TEXT NULL,
    recruiter_id    BIGINT UNSIGNED NULL,
    hired_at        DATETIME NULL,
    status          ENUM('ativo','inativo') DEFAULT 'ativo',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_opening_stage (job_opening_id, pipeline_stage)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Exames ocupacionais
CREATE TABLE hcm_medical_exams (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    employee_id     BIGINT UNSIGNED NOT NULL,
    exam_type       ENUM('admissional','periodico','retorno','mudanca_funcao','demissional') NOT NULL,
    exam_date       DATE NOT NULL,
    due_date        DATE NULL,
    doctor_name     VARCHAR(150) NULL,
    clinic          VARCHAR(150) NULL,
    crm             VARCHAR(20) NULL,
    result          ENUM('apto','inapto','apto_restricoes') NOT NULL,
    restrictions    TEXT NULL,
    aso_path        VARCHAR(255) NULL,
    created_by      BIGINT UNSIGNED NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_employee (employee_id),
    INDEX idx_due_date (due_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Treinamentos
CREATE TABLE hcm_trainings (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    entity_id       BIGINT UNSIGNED NOT NULL,
    code            VARCHAR(20) NOT NULL,
    name            VARCHAR(200) NOT NULL,
    training_type   ENUM('interno','externo','ead','outro') NOT NULL,
    category        VARCHAR(100) NULL,
    description     TEXT NULL,
    workload_hours  DECIMAL(6,2) NULL,
    modality        ENUM('presencial','online','hibrido') DEFAULT 'presencial',
    mandatory       TINYINT(1) DEFAULT 0,
    renewal_months  TINYINT UNSIGNED NULL,
    status          ENUM('ativo','inativo') DEFAULT 'ativo',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Audit log RH
CREATE TABLE hcm_audit_logs (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    entity_id       BIGINT UNSIGNED NOT NULL,
    unit_id         BIGINT UNSIGNED NULL,
    user_id         BIGINT UNSIGNED NULL,
    employee_id     BIGINT UNSIGNED NULL,
    action          VARCHAR(50) NOT NULL,
    resource        VARCHAR(50) NOT NULL,
    resource_id     BIGINT UNSIGNED NULL,
    old_data        JSON NULL,
    new_data        JSON NULL,
    ip_address      VARCHAR(45) NULL,
    user_agent      VARCHAR(255) NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_entity (entity_id),
    INDEX idx_employee (employee_id),
    INDEX idx_action_resource (action, resource),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 20. RBAC — Perfis e Permissões

| Funcionalidade                 | SA  | GE  | GP  | GU  | RH  | FIN | COL | AUD |
|-------------------------------|-----|-----|-----|-----|-----|-----|-----|-----|
| Dashboard                     | ✅  | ✅  | ✅  | ✅  | ✅  | 👁  | 👁  | 👁  |
| Colaboradores — Listar         | ✅  | ✅  | ✅  | ✅  | ✅  | ❌  | 👁  | 👁  |
| Colaboradores — CRUD           | ✅  | ✅  | ✅  | ❌  | 🖊  | ❌  | ❌  | ❌  |
| Desligar colaborador           | ✅  | ✅  | ✅  | ❌  | ❌  | ❌  | ❌  | ❌  |
| Recrutamento completo          | ✅  | ✅  | ✅  | ❌  | ✅  | ❌  | ❌  | 👁  |
| Ponto — Visualizar             | ✅  | ✅  | ✅  | ✅  | ✅  | ❌  | 👁  | 👁  |
| Ponto — Ajuste manual          | ✅  | ✅  | ✅  | ❌  | ✅  | ❌  | ❌  | ❌  |
| Folha — Visualizar             | ✅  | ✅  | ✅  | ❌  | ❌  | 👁  | ❌  | 👁  |
| Folha — Processar/Aprovar      | ✅  | ✅  | ✅  | ❌  | ❌  | ❌  | ❌  | ❌  |
| Holerite próprio               | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ❌  |
| Férias — Programar             | ✅  | ✅  | ✅  | ✅  | ✅  | ❌  | 🖊  | ❌  |
| Treinamentos — Gerenciar       | ✅  | ✅  | ✅  | ❌  | ✅  | ❌  | 👁  | 👁  |
| Avaliações — Criar ciclo       | ✅  | ✅  | ✅  | ❌  | ✅  | ❌  | ❌  | ❌  |
| Avaliações — Preencher         | ✅  | ✅  | ✅  | ✅  | ✅  | ❌  | ✅  | ❌  |
| Benefícios — Gerenciar         | ✅  | ✅  | ✅  | ❌  | ✅  | 👁  | ❌  | 👁  |
| SST — Gerenciar                | ✅  | ✅  | ✅  | ❌  | ✅  | ❌  | ❌  | 👁  |
| Documentos — Upload            | ✅  | ✅  | ✅  | ❌  | ✅  | ❌  | 🖊  | ❌  |
| Relatórios                     | ✅  | ✅  | ✅  | ✅  | ✅  | 👁  | ❌  | ✅  |
| Automações — Configurar        | ✅  | ✅  | ✅  | ❌  | ❌  | ❌  | ❌  | ❌  |
| Configurações do módulo        | ✅  | ✅  | ✅  | ❌  | ❌  | ❌  | ❌  | ❌  |
| Audit Log                      | ✅  | ✅  | ✅  | ❌  | ❌  | ❌  | ❌  | ✅  |

**Legenda:** ✅ Total · 👁 Somente leitura · 🖊 Próprios dados · ❌ Sem acesso

---

## 21. LGPD / Compliance

### Dados Sensíveis Criptografados (AES-256-GCM)
| Campo               | Tabela              | Categoria LGPD         |
|---------------------|---------------------|------------------------|
| cpf                 | hcm_employees       | Dado pessoal identificador |
| rg                  | hcm_employees       | Dado pessoal identificador |
| birth_date          | hcm_employees       | Dado pessoal            |
| pis_nis             | hcm_employees       | Dado pessoal identificador |
| email_personal      | hcm_employees       | Dado pessoal de contato |
| base_salary         | hcm_employees       | Dado financeiro pessoal |
| cid_code            | hcm_absences        | Dado sensível (saúde)   |
| cpf                 | hcm_candidates      | Dado pessoal identificador |
| email               | hcm_candidates      | Dado pessoal de contato |

### Regras LGPD
- **Consentimento:** `consent_at` + `consent_ip` registrado na admissão e atualizado a cada revisão de política
- **Portabilidade:** Endpoint `GET /api/v1/pessoas/colaboradores/:id/dados-pessoais` exporta todos os dados em JSON estruturado
- **Eliminação:** `DELETE` (soft delete + anonimização) aplica `anonymized_at`; após 5 anos de desligamento, dados pessoais são substituídos por hash irreversível
- **Acesso restrito:** Salário e dados de saúde visíveis apenas para GP/SA/GE; CID mascarado na UI (exibe apenas categoria)
- **Auditoria:** 100% das operações em `hcm_audit_logs` com retenção de 10 anos
- **Candidatos:** Dados de candidatos não contratados apagados após 6 meses (automação A15, configurável)
- **Exames:** ASO e resultados médicos com acesso restrito + log de visualização

### Campos Mascarados na UI
| Campo         | Exibição padrão   | Desmascarar por  |
|---------------|-------------------|------------------|
| CPF           | ***.***.***-**    | SA/GP/GE         |
| Salário       | oculto            | SA/GP/GE/FIN     |
| CID           | Categoria (ex: J) | SA/GP (com log)  |
| Dados bancários | ****...XXXX      | SA/GP            |

---

## 22. Critérios de Aceite

### Funcionais
- [ ] Dashboard carrega KPIs em ≤ 1,5s com dados em tempo real
- [ ] DataTable colaboradores suporta ≥ 10.000 registros com paginação server-side
- [ ] Drawer de admissão valida CPF, PIS e CTPS antes de salvar
- [ ] Kanban de recrutamento atualiza status via drag & drop sem reload
- [ ] Espelho de ponto calcula corretamente horas extras 50% e 100%
- [ ] Folha processa corretamente INSS, IRRF e FGTS conforme tabelas vigentes
- [ ] Férias calcula automaticamente período aquisitivo e saldo de dias
- [ ] Automações disparam notificações corretas por canal configurado
- [ ] Exportação CAGED/RAIS gera layout oficial aceito pelo eSocial
- [ ] Perfil do colaborador carrega todas as abas sem erros em contexto multi-entidade

### Segurança
- [ ] Todos os endpoints validam JWT e perfil RBAC antes de retornar dados
- [ ] Dados criptografados não são expostos em logs ou respostas de erro
- [ ] CPF e dados sensíveis mascarados na UI para perfis não autorizados
- [ ] Audit log registra 100% das operações de escrita com user_id + IP
- [ ] Rate limiting ativo (1000 req/min por token) com resposta 429
- [ ] Upload de documentos validado: tipo MIME + tamanho + scan antivírus (ClamAV)

### UX / Performance
- [ ] Todos os formulários possuem validação client-side imediata (Vanilla JS)
- [ ] Feedback visual (toast/spinner) em todas as operações assíncronas
- [ ] Kanban responsivo em tablets (min 768px)
- [ ] Drawers fecham ao pressionar ESC ou clicar fora
- [ ] Relatórios com > 5.000 linhas gerados em background com notificação de download
- [ ] Tema claro/escuro respeitado em todos os componentes do módulo

### Compliance
- [ ] Consentimento LGPD registrado na criação de todo colaborador e candidato
- [ ] Dados de candidatos não contratados expiram em 6 meses (automação ativa)
- [ ] Endpoint de portabilidade retorna todos os dados pessoais em JSON estruturado
- [ ] CID nunca exposto em listagens — somente em visualização individual com log
- [ ] Anonimização automática ativa 5 anos após desligamento

---

*Documento gerado automaticamente — TotusTuusSoftCloud SaaS Platform*  
*Revisão: 1.0.0 · 2026-06-07 · Módulo: HCM/RH — Gestão de Pessoas*
