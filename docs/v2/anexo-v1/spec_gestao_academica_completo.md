# SPEC — Gestão Acadêmica v2.0
**Produto:** TotusTuus SoftCloud Education
**Módulo:** Academic Management (ACM)
**Segmento:** Instituições de ensino (escolas, faculdades, universidades, cursos livres, EAD, híbrido)
**Versão:** 2.0 — Revisão completa com gaps SGE + SIS + SIGAA
**Stack:** PHP 8 puro · JavaScript · Tailwind CSS 4.2 · amCharts 5 · MariaDB
**Arquitetura:** SaaS multi-tenant · multi-entity · multi-unit · database-per-unit
**Padrão de tabelas:** `id` (PK ordenação) · `uuid` (ID interno) · `code` (ID externo)
**Nomenclatura:** Internacional (inglês · snake_case)

- Language Standard: Global English
---

## 1. VISÃO GERAL DO MÓDULO

O módulo Academic Management centraliza toda a operação acadêmica da instituição: matrículas, turmas, currículo, notas, frequência, horários, calendário, ocorrências e documentos. É o núcleo do produto educacional, consumido por todos os outros módulos (Billing, CRM, LMS, DMS, HCM).

### 1.1 Perfis de Acesso (RBAC)

| Perfil         | Sigla | Permissões-chave                                              |
|----------------|-------|---------------------------------------------------------------|
| Super Admin    | SA    | Acesso total a todas as entidades/unidades                    |
| Admin Unidade  | AU    | Gestão completa da unidade vinculada                          |
| Coordenador    | CO    | Cursos, turmas, horários, notas, frequência, conselho         |
| Secretaria     | SE    | Matrículas, documentos, requerimentos, comunicados, protocolo |
| Professor      | PR    | Diário de classe, notas, frequência, plano de aula            |
| Aluno          | AL    | Portal self-service: notas, freq., horários, docs, solicitações|
| Responsável    | RE    | Consulta boletim, frequência, comunicados (ensino básico)     |
| CPA            | CP    | Avaliação institucional, relatórios SINAES                    |

---

## 2. MAPA DE PÁGINAS

```
/academic
├── dashboard
├── enrollments
│   ├── list
│   ├── new                            # Wizard matrícula manual
│   ├── online                         # Portal matrícula online (self-service)
│   ├── selective-process              # Processo seletivo / vestibular
│   ├── pre-enrollment                 # Pré-matrícula + lista de espera
│   ├── conditional                    # Matrícula condicional
│   ├── renewals                       # Rematrículas (Kanban)
│   ├── transfers                      # Transferências
│   ├── lock                           # Trancamento com motivo + protocolo
│   ├── course-change                  # Reopção de curso
│   ├── credit-recognition             # Aproveitamento de estudos
│   └── complementary-hours            # Creditação de atividades complementares
├── students
│   ├── list
│   ├── profile/:uuid
│   ├── documents
│   └── record/:uuid                   # Prontuário digital do aluno
├── courses
│   ├── list
│   ├── curriculum/:uuid               # Grade curricular
│   ├── curriculum-equivalence         # Mapa de equivalência entre cursos
│   ├── subjects
│   └── ppc/:uuid                      # Projeto Pedagógico de Curso (versionado)
├── classes
│   ├── list
│   ├── schedule/:uuid
│   └── diary/:uuid                    # Diário de turma + diário por disciplina
├── class-diary                        # Diário por disciplina (separado)
│   ├── list
│   ├── view/:uuid
│   └── print/:uuid                    # Impressão layout oficial
├── grades
│   ├── input
│   ├── report-cards
│   └── approvals
├── attendance
│   ├── input                          # Chamada normal + QR Code + geolocalização EAD
│   ├── absences
│   └── justifications
├── schedule
│   ├── builder
│   └── rooms
├── calendar
│   ├── events
│   ├── holidays
│   └── periods
├── occurrences
│   ├── list
│   └── kanban
├── requests
│   ├── list
│   └── kanban
├── secretariat                        # Secretaria Acadêmica (módulo completo)
│   ├── queue                          # Fila virtual + atendimento presencial
│   ├── protocol                       # Protocolo de atendimento (número + senha)
│   ├── attendance-history             # Histórico de atendimentos
│   ├── documents-emission             # Emissão de documentos oficiais
│   │   ├── school-record              # Histórico escolar layout MEC
│   │   ├── enrollment-declaration     # Declaração de matrícula (ICP-Brasil)
│   │   ├── completion-certificate     # Certidão de conclusão
│   │   └── second-copies              # 2ª via de documentos
│   ├── digital-archive               # Arquivo morto / digitalização
│   ├── book-registry                  # Livro de registro digital
│   └── meeting-book                   # Livro de atas digitais
├── pedagogical                        # Coordenação Pedagógica
│   ├── lesson-plans                   # Plano de aula (PPP + semanal/bimestral)
│   ├── teaching-plans                 # Plano de ensino por disciplina
│   ├── class-council                  # Conselho de classe estruturado
│   ├── student-portfolio              # Portfólio do aluno
│   ├── parallel-recovery              # Recuperação paralela
│   └── institutional-evaluation      # Avaliação institucional CPA/SINAES
├── internship                         # Estágio curricular
│   ├── list
│   ├── supervision
│   └── reports
├── thesis                             # TCC / Trabalho final
│   ├── list
│   ├── guidance
│   └── defense
├── complementary-activities           # Atividades complementares
│   ├── list
│   └── validation
├── teachers
│   ├── list
│   └── workload
├── student-portal                     # Portal do Aluno (self-service)
├── teacher-portal                     # Portal do Professor
├── reports
│   ├── performance
│   ├── attendance-report
│   └── regulatory
└── settings
    ├── grade-scales
    ├── evaluation-types
    ├── academic-periods
    ├── course-types
    └── document-types
```

---

## 3. DASHBOARD — `/academic/dashboard`

### 3.1 Widgets KPI (topo — 6 cards)

| Widget                    | Valor          | Tendência | Ícone              |
|---------------------------|----------------|-----------|---------------------|
| Total de Alunos Ativos    | count          | vs. mês anterior | graduation-cap |
| Matrículas no Mês         | count          | vs. mês anterior | file-plus      |
| Taxa de Frequência Média  | %              | semana atual | calendar-check |
| Índice de Aprovação       | %              | período atual | check-circle   |
| Requerimentos Pendentes   | count          | urgentes em destaque | inbox   |
| Ocorrências Abertas       | count          | críticas em vermelho | alert-triangle |

### 3.2 Widgets Operacionais (segunda linha — 4 cards)

| Widget                       | Descrição                                              |
|------------------------------|--------------------------------------------------------|
| Próximas Avaliações          | Lista das 5 próximas provas agendadas                  |
| Turmas com Baixa Frequência  | Turmas abaixo de 75% na semana                         |
| Alunos em Risco              | Alunos com nota < mínimo ou falta crítica              |
| Eventos do Calendário        | Mini-calendário com próximos eventos (7 dias)          |

### 3.3 Charts amCharts 5

| # | Gráfico                         | Tipo              | Dados                                          |
|---|---------------------------------|-------------------|------------------------------------------------|
| 1 | Matrículas por Mês              | Line (dual axis)  | Novas matrículas x Cancelamentos por mês       |
| 2 | Distribuição por Curso          | Donut             | Alunos por curso/área                          |
| 3 | Frequência por Turma            | Bar Grouped       | % frequência por turma nas últimas 4 semanas   |
| 4 | Desempenho por Disciplina       | Bar Horizontal    | Média de notas por disciplina                  |
| 5 | Alunos por Status               | Stacked Bar       | Ativo / Trancado / Desistente / Concluído      |
| 6 | Evolução de Notas               | Area Spline       | Média geral por bimestre/semestre              |

### 3.4 Kanban do Dashboard — Requerimentos do Dia

**Colunas:** `Recebido` → `Em Análise` → `Aguardando Doc.` → `Resolvido` → `Negado`

Cada card exibe: tipo de requerimento, nome do aluno, data, responsável.

---

## 4. MATRÍCULAS — `/academic/enrollments`

### 4.1 Lista de Matrículas — Datatable

| Coluna           | Tipo      | Detalhe                                      |
|------------------|-----------|----------------------------------------------|
| #                | checkbox  | Seleção múltipla                             |
| Code             | badge     | Código externo da matrícula                  |
| Aluno            | avatar+nome | Foto + nome completo                       |
| Curso            | texto     | Nome do curso                                |
| Turma            | badge     | Código e turno da turma                      |
| Período Letivo   | texto     | Ex.: 2026/1                                  |
| Data Matrícula   | data      | dd/mm/aaaa                                   |
| Status           | badge-color | Ativo / Trancado / Transferido / Concluído / Cancelado / Condicional |
| Tipo             | badge     | Regular / Especial / Transferência / EAD     |
| Responsável Fin. | texto     | Nome do resp. financeiro                     |
| Ações            | botões    | Ver, Editar, Trancar, Cancelar, Histórico    |

**Filtros:** Período letivo · Curso · Turma · Turno · Status · Tipo · Data inicial/final
**Ações em lote:** Gerar boletos · Exportar · Trancamento em massa · Imprimir lista
**Totalizador no rodapé:** Total de registros · Ativos · Trancados · Cancelados

### 4.2 Wizard — Nova Matrícula Manual (6 etapas)

**Etapa 1 — Busca/Cadastro do Aluno**
- Busca por CPF / nome / código
- Se não encontrado: mini-formulário de pré-cadastro (nome, CPF, e-mail, nascimento, telefone)
- Validação: CPF único por tenant, alerta de matrícula duplicada

**Etapa 2 — Dados da Matrícula**
- Curso (select com busca) · Modalidade · Turma · Turno · Período letivo
- Data de início · Tipo: Regular / Especial / Transferência / Condicional
- Se Condicional: campo "pendência" (financeira / documental) + prazo de regularização
- Observações

**Etapa 3 — Dados do Responsável (se menor)**
- Nome completo · CPF / RG · Parentesco · Contato · Endereço (CEP + ViaCEP)

**Etapa 4 — Plano Financeiro**
- Plano de pagamento · Desconto (tipo + motivo) · Data de vencimento
- Forma de pagamento preferida · Preview das parcelas

**Etapa 5 — Documentos**
- Upload drag-and-drop · Tipos obrigatórios por curso
- Status por documento: Enviado / Pendente / Aprovado / Recusado

**Etapa 6 — Contrato e LGPD**
- Geração de contrato pedagógico digital (PDF)
- Assinatura eletrônica do aluno/responsável (ICP-Brasil ou assinatura simples)
- Aceite do termo LGPD (checkbox com texto completo)
- Botão: Finalizar e Gerar Protocolo de Matrícula

### 4.3 Portal de Matrícula Online — `/academic/enrollments/online`

Self-service para aluno/responsável acessar via portal externo:

- **Passo 1:** Login ou cadastro com CPF
- **Passo 2:** Seleção de curso e turno desejado
- **Passo 3:** Verificação de vagas em tempo real (se sem vaga → entra em lista de espera)
- **Passo 4:** Upload de documentos obrigatórios
- **Passo 5:** Plano financeiro e pagamento da taxa de matrícula (PIX/Boleto)
- **Passo 6:** Assinatura do contrato digital + aceite LGPD
- **Passo 7:** Confirmação com número de protocolo gerado automaticamente
- Status em tempo real: Em análise / Documentação pendente / Aprovada / Condicional

### 4.4 Processo Seletivo / Vestibular — `/academic/enrollments/selective-process`

**Datatable de Inscrições:**

| Coluna           | Detalhe                                              |
|------------------|------------------------------------------------------|
| Code             | Código da inscrição                                  |
| Candidato        | Nome + CPF                                           |
| Curso pretendido | Nome do curso                                        |
| Modalidade prova | Presencial / Online / Análise de histórico           |
| Status           | Inscrito / Confirmado / Ausente / Aprovado / Reprovado / Em espera |
| Nota             | Nota do processo seletivo (se aplicável)             |
| Classificação    | Posição no ranking                                   |
| Ações            | Ver, Chamar para matrícula, Mover para espera        |

**Drawer — Configurar Processo Seletivo:**
- Nome do processo · Curso(s) alvo · Período letivo destino
- Datas: inscrição, prova, resultado, matrícula
- Total de vagas · Vagas por cotas (se configurado)
- Modalidade de seleção: Prova / ENEM / Histórico / Entrevista / Múltipla
- Taxa de inscrição (link para Billing)

**Kanban do Processo:**
`Inscrito` → `Confirmado` → `Prova Realizada` → `Aprovado` → `Matrícula Efetuada` → `Desistiu`

### 4.5 Pré-matrícula / Lista de Espera — `/academic/enrollments/pre-enrollment`

- Registro de candidatos em lista de espera por curso/turno
- Ordem de prioridade configurável: data de inscrição / nota / cotas / critério manual
- Notificação automática ao candidato quando vaga abrir
- Prazo de resposta do candidato (ex.: 48h para confirmar)
- Status: Aguardando vaga / Notificado / Confirmou / Desistiu / Expirou

### 4.6 Trancamento — `/academic/enrollments/lock`

- Busca do aluno · Matrícula vinculada
- Motivo do trancamento (select configurável: pessoal, financeiro, saúde, militar, outro)
- Descrição complementar (textarea)
- Prazo máximo de trancamento (conforme regimento)
- Geração automática de protocolo de trancamento (PDF)
- Status: Trancado com prazo definido de retorno

### 4.7 Reopção de Curso — `/academic/enrollments/course-change`

- Aluno origem + curso/turma origem
- Curso/turma destino (select)
- Justificativa
- Análise de equivalência curricular automática (disciplinas cursadas vs. grade destino)
- Aprovação pelo coordenador (workflow)
- Geração de nova matrícula vinculada à anterior

### 4.8 Aproveitamento de Estudos — `/academic/enrollments/credit-recognition`

- Upload do histórico externo (PDF)
- Tabela de disciplinas externas x disciplinas da grade (mapeamento manual/automático)
- Status por disciplina: Aproveitado / Não aproveitado / Pendente análise
- Aprovação do coordenador + geração de parecer formal

### 4.9 Atividades Complementares — `/academic/enrollments/complementary-hours`

- Registro de atividade: tipo (evento, curso, projeto, extensão, publicação)
- Carga horária declarada · Documento comprobatório (upload)
- Status: Pendente validação / Validado / Recusado
- Totalizador de horas validadas vs. horas exigidas pelo curso
- Aprovação pelo coordenador

---

## 5. ALUNOS — `/academic/students`

### 5.1 Lista de Alunos — Datatable

| Coluna             | Tipo        | Detalhe                                        |
|--------------------|-------------|------------------------------------------------|
| #                  | checkbox    | Seleção múltipla                               |
| Code               | badge       | Código do aluno                                |
| Aluno              | avatar+nome | Foto + nome completo                           |
| CPF                | texto       | Mascarado: ***.***.***-**                      |
| Turma Atual        | badge       | Código + turno                                 |
| Curso              | texto       | Nome do curso                                  |
| Contato            | ícones      | E-mail, telefone, WhatsApp                     |
| Freq. Atual        | progress-bar| % de frequência no período                     |
| Média Atual        | badge-color | Média geral (verde/amarelo/vermelho)            |
| Status             | badge-color | Ativo / Trancado / Desistente / Concluído      |
| Ações              | botões      | Perfil, Notas, Frequência, Documentos, Ocorrências |

### 5.2 Perfil do Aluno — `/academic/students/profile/:uuid`

**Tabs:**
- Overview: KPIs (freq, média, ranking, créditos, horas complementares)
- Histórico Acadêmico: tabela de disciplinas, notas e status por período
- Frequência: gráfico de presença + lista de faltas + justificativas
- Documentos: grid com status por documento
- Ocorrências: timeline de ocorrências
- Requerimentos: histórico de solicitações
- Financeiro: resumo + link para Billing
- Notas: boletim interativo por período
- Portfólio: evidências de aprendizagem
- Estágio: situação do estágio curricular
- TCC: situação do trabalho final
- Atividades Complementares: horas acumuladas
- Comunicações: histórico de mensagens

### 5.3 Prontuário Digital do Aluno — `/academic/students/record/:uuid`

Pasta digital completa do aluno (digital twin do prontuário físico):

- **Seção Documentos Pessoais:** RG, CPF, certidão de nascimento, comprovante residência, foto (versionados)
- **Seção Documentos Acadêmicos:** histórico externo, diplomas anteriores, histórico interno gerado pelo sistema
- **Seção Contratos:** contrato pedagógico assinado, aditivos, termos LGPD
- **Seção Requerimentos:** todos os requerimentos e respostas archivados
- **Seção Comunicações:** correspondências oficiais enviadas/recebidas
- **Controle de versão:** cada documento tem data upload, validade, responsável e hash de integridade
- **Acesso:** Secretaria (leitura/escrita) · Coordenador (leitura) · Aluno (leitura dos seus próprios docs)
- **Digitalização:** upload de documentos físicos digitalizados com OCR opcional

---

## 6. SECRETARIA ACADÊMICA — `/academic/secretariat`

### 6.1 Fila Virtual + Atendimento Presencial — `/academic/secretariat/queue`

**Painel de Senhas:**
- Emissão de senha pelo totem ou portal do aluno (tipo de atendimento: matrícula, documentos, requerimento, financeiro, informações)
- Exibição da fila atual com estimativa de espera
- Chamada de senha pela secretaria (interface de guichê)
- Transferência de senha entre atendentes
- Status: Aguardando / Em atendimento / Atendido / Desistiu

**Histórico de Atendimento:**
| Coluna        | Detalhe                                      |
|---------------|----------------------------------------------|
| Senha         | Número sequencial + tipo                     |
| Aluno         | Nome + código                                |
| Atendente     | Nome do funcionário                          |
| Tipo          | Categoria do atendimento                     |
| Início        | Hora de chamada                              |
| Duração       | Tempo de atendimento                         |
| Resolução     | Resumo da resolução + requerimento gerado    |
| Status        | Atendido / Pendente retorno / Encaminhado    |

### 6.2 Protocolo de Atendimento — `/academic/secretariat/protocol`

- Geração de número de protocolo para qualquer demanda presencial ou online
- Formato: `ANO-UNIDADE-SEQUENCIAL` (ex.: 2026-BH-004521)
- Vinculação a requerimento, matrícula ou documento emitido
- QR Code no comprovante físico para consulta de status
- Consulta pública de protocolo (portal externo, sem login, por número + CPF)

### 6.3 Emissão de Documentos Oficiais — `/academic/secretariat/documents-emission`

#### 6.3.1 Histórico Escolar — layout oficial MEC (Res. CNE/CEB)

- Gerador de PDF com layout conforme resolução CNE/CEB vigente
- Campos: dados da instituição (MEC), dados do aluno, disciplinas por período, notas, frequência, situação, carga horária, carimbo/assinatura do diretor
- Assinatura digital com certificado ICP-Brasil (integração com token ou arquivo .pfx)
- Geração individual e em lote (por turma/período)
- QR Code de autenticidade embutido no PDF
- Registro de emissão em `document_emissions` (quem solicitou, quem emitiu, data, hash do PDF)

#### 6.3.2 Declaração de Matrícula

- Template configurável por unidade
- Campos: dados do aluno, curso, turma, período, data de matrícula, validade da declaração
- Assinatura digital ICP-Brasil (mesma integração)
- Modalidade: para fins de imposto de renda, bolsa, estágio, outros (select)
- Emissão pelo aluno via portal (self-service, sem precisar ir à secretaria)

#### 6.3.3 Certidão de Conclusão (pós-EAD)

- Emissão após conclusão de curso EAD ou módulo
- Layout com dados de conclusão, carga horária, data, código verificador
- Assinatura digital + QR Code de verificação pública
- Registro em `certificates`

#### 6.3.4 Segunda Via de Documentos

- Listagem de todos os documentos já emitidos para o aluno
- Reemissão com novo número de protocolo e carimbo "2ª VIA"
- Taxa de segunda via (integração com Billing, se configurado)

### 6.4 Arquivo Morto / Digitalização — `/academic/secretariat/digital-archive`

- Cadastro de documentos físicos (caixas, pastas, prateleiras) com localização física
- Upload da versão digitalizada (PDF/imagem)
- Indexação por: tipo, aluno, turma, ano letivo, período
- Status: Apenas físico / Digitalizado / Digitalizado e verificado
- Busca full-text nos documentos digitalizados
- Controle de empréstimo de documentos físicos (quem retirou, data, devolução)

### 6.5 Livro de Registro Digital — `/academic/secretariat/book-registry`

- Registro oficial de matrículas (equivalente ao livro físico exigido pelo MEC)
- Campos: número de ordem, nome aluno, CPF, curso, data matrícula, assinatura
- Geração do livro em PDF (formato oficial, numeração sequencial)
- Travamento de registros após publicação (imutável, com hash)
- Exportação para envio ao MEC/SIED

### 6.6 Livro de Atas Digitais — `/academic/secretariat/meeting-book`

- Registro de atas de reuniões, conselhos de classe, assembleias
- Editor de texto rico (formatação básica)
- Participantes: select de usuários do sistema com assinatura digital individual
- Status: Rascunho / Em assinatura / Assinado / Publicado
- Numeração sequencial e data de criação imutáveis após publicação
- Impressão em layout oficial

---

## 7. COORDENAÇÃO PEDAGÓGICA — `/academic/pedagogical`

### 7.1 Plano de Aula — `/academic/pedagogical/lesson-plans`

**Datatable:**

| Coluna         | Detalhe                                        |
|----------------|------------------------------------------------|
| Professor      | Nome + avatar                                  |
| Disciplina     | Nome da disciplina                             |
| Turma          | Código da turma                                |
| Tipo           | Semanal / Bimestral / Anual (PPP)              |
| Período        | Bimestre/semestre de referência                |
| Status         | Rascunho / Enviado / Aprovado / Devolvido      |
| Ações          | Ver, Aprovar, Devolver, Comentar               |

**Drawer — Criar/Editar Plano de Aula:**
- Professor (auto-fill se perfil Professor) · Disciplina · Turma · Período
- Tipo: Semanal / Bimestral / PPP (Projeto Político Pedagógico)
- Objetivos gerais e específicos
- Conteúdo programático (editor rich text por aula/semana)
- Metodologia e estratégias de ensino
- Recursos didáticos previstos (lista com links/arquivos)
- Avaliações previstas (tipo + data + peso)
- Referências bibliográficas (básica + complementar)
- Alinhamento à BNCC/DCN (campo de competências vinculadas)
- Workflow de aprovação: Professor → Coordenador → (Diretor se PPP)

### 7.2 Plano de Ensino por Disciplina — `/academic/pedagogical/teaching-plans`

- Ementa da disciplina
- Objetivos gerais e específicos
- Conteúdo programático por unidade/módulo
- Metodologia de ensino
- Critérios de avaliação (fórmulas e pesos)
- Bibliografia básica e complementar (normas ABNT)
- Carga horária teórica vs. prática
- Vinculação ao PPC do curso
- Versão: versionamento completo (histórico de alterações)
- Publicação no portal do aluno (toggle)

### 7.3 Conselho de Classe — `/academic/pedagogical/class-council`

**Agendamento:**
- Data · Hora · Local / Link videoconferência
- Turma(s) alvo
- Participantes convocados (professores + coordenador + diretor)
- Pauta pré-definida (template configurável)

**Durante o Conselho:**
- Lista de alunos com: média atual, frequência atual, status de risco
- Campo de parecer individual por aluno (texto)
- Deliberações por aluno: Aprovado / Reprovado / Recuperação / Progressão parcial
- Campo de observações gerais da turma

**Pós-Conselho:**
- Ata gerada automaticamente com dados da reunião, participantes e deliberações
- Assinatura digital de todos os participantes
- Publicação no livro de atas digitais
- Notificação aos pais/responsáveis dos alunos com deliberação especial (toggle)

### 7.4 Projeto Pedagógico de Curso (PPC) — `/academic/courses/ppc/:uuid`

- Documento estruturado por seções (justificativa, objetivos, perfil egresso, estrutura curricular, metodologia, avaliação, corpo docente, infraestrutura)
- Editor rich text por seção com formatação e inserção de tabelas
- Versionamento completo: cada publicação gera nova versão numerada
- Histórico de versões com diff visual (seção alterada destacada)
- Workflow de aprovação: Coordenador → Diretor → Conselho Acadêmico
- Status: Em elaboração / Em aprovação / Vigente / Substituído
- Exportação em PDF (layout MEC)
- Vinculação com grade curricular vigente

### 7.5 Portfólio do Aluno — `/academic/pedagogical/student-portfolio`

- Por aluno e por disciplina/período
- Tipos de evidência: texto, imagem, arquivo, link, vídeo
- Publicado pelo aluno (via portal) ou pelo professor
- Avaliação do portfólio pelo professor (comentário + nota qualitativa)
- Compartilhamento opcional com responsável
- Exportação como PDF para uso externo (emprego, concurso)

### 7.6 Recuperação Paralela — `/academic/pedagogical/parallel-recovery`

- Alunos elegíveis (abaixo da média configurada)
- Atribuição de atividades de recuperação por disciplina
- Prazo de entrega + responsável (professor)
- Status da atividade: Pendente / Entregue / Avaliado
- Nova nota registrada e impacto na média calculado automaticamente
- Notificação ao aluno e responsável

### 7.7 Avaliação Institucional (CPA/SINAES) — `/academic/pedagogical/institutional-evaluation`

- Criação de formulários de autoavaliação (builder de formulário)
- Público-alvo: alunos / professores / técnico-administrativos / comunidade
- Período de coleta configurável
- Exibição no portal do aluno/professor (banner de aviso)
- Dashboard de resultados em tempo real (charts amCharts)
- Relatório consolidado por dimensão SINAES
- Exportação para submissão ao e-MEC

---

## 8. DIÁRIO ESCOLAR / DIÁRIO DE CLASSE

### 8.1 Diário de Turma — `/academic/classes/diary/:uuid`

(já existente na v1 — mantido com as melhorias abaixo)

**Melhorias v2:**
- Registro de professor substituto eventual (campo "docente eventual" com nome + motivo)
- Vinculação de aulas de reposição ao calendário acadêmico
- Campo de habilidades/competências por aula (multi-select vinculado à BNCC/DCN)
- Campo de recursos didáticos utilizados (links + arquivos anexos)
- Assinatura digital do diário ao fechar a aula (certificado do professor)
- Impressão em layout oficial (frente e verso conforme padrão estadual)
- Alerta automático se diário não fechado em 48h após a aula

### 8.2 Diário por Disciplina — `/academic/class-diary`

Diário separado por disciplina (diferente do diário de turma):

**Datatable:**

| Coluna         | Detalhe                                              |
|----------------|------------------------------------------------------|
| Disciplina     | Nome da disciplina                                   |
| Professor      | Nome + avatar                                        |
| Turma          | Código da turma                                      |
| Período        | Período letivo                                       |
| Aulas Dadas    | X de Y planejadas                                    |
| % Cumprimento  | Progress bar                                         |
| Status         | Em andamento / Concluído / Atrasado                  |
| Ações          | Abrir diário, Imprimir, Assinar                      |

**Visualização do Diário por Disciplina:**
- Tabela de aulas: data · conteúdo ministrado · habilidades/competências · recursos · assinatura
- Chamada integrada (presença por aluno por aula)
- Conteúdo programático alinhado à BNCC/DCN (marcação de cobertura)
- Substituição de professor: campo para docente eventual + justificativa
- Aula de reposição: marcação + vínculo com evento no calendário
- Fechamento da aula: assinatura digital com certificado do professor
- Impressão: layout oficial verso/anverso com dados da instituição e do professor

### 8.3 Chamada por QR Code e Geolocalização — `/academic/attendance/input`

**Modo QR Code (presencial):**
- Professor gera QR Code único por aula (válido por X minutos, configurável)
- Aluno escaneia com câmera do celular → registro automático de presença
- Antifraude: QR Code expira + vinculação ao IP/dispositivo
- Alunos que não escanearam: aparecem como falta pendente para revisão manual

**Modo Geolocalização (EAD/híbrido):**
- Check-in do aluno via portal/app com coordenadas GPS
- Raio configurável (ex.: dentro de 500m da instituição)
- Para EAD: confirmação por IP + horário de acesso à plataforma LMS

**Modo Manual (padrão):**
- Toggle Presente / Falta / Justificada por aluno na tabela

**Consolidado Legal (LDBEN):**
- Cálculo automático de % frequência por aluno por disciplina
- Alerta em 3 níveis: Atenção (abaixo de 85%) · Crítico (abaixo de 80%) · Legal (abaixo de 75%)
- Relatório de risco de reprovação por frequência (threshold 25% de faltas = LDBEN)

---

## 9. ESTÁGIO CURRICULAR — `/academic/internship`

### 9.1 Lista de Estágios

| Coluna         | Detalhe                                              |
|----------------|------------------------------------------------------|
| Aluno          | Nome + avatar                                        |
| Curso          | Curso vinculado                                      |
| Empresa        | Nome da empresa concedente                           |
| Supervisor     | Professor supervisor                                 |
| Início / Fim   | Datas do estágio                                     |
| Horas          | Horas cumpridas vs. exigidas                         |
| Status         | Em andamento / Concluído / Interrompido / Aprovado   |

### 9.2 Drawer — Cadastrar Estágio

- Aluno (busca) · Curso · Tipo: Obrigatório / Não obrigatório
- Empresa concedente: CNPJ + nome + endereço + contato do supervisor empresarial
- Professor supervisor (select)
- Datas: início, fim previsto, fim real
- Carga horária exigida pelo curso · CH semanal combinada
- Termo de compromisso de estágio (upload ou geração pelo sistema)
- Apólice de seguro (upload + validade)

### 9.3 Supervisão e Relatórios

- Professor supervisor lança visitas de supervisão (data + observações)
- Aluno envia relatórios periódicos (upload PDF + descrição de atividades)
- Avaliação do estágio: professor supervisor + supervisor empresarial (formulário)
- Nota final do estágio calculada pela média das avaliações
- Geração de declaração de conclusão de estágio

---

## 10. TCC / TRABALHO FINAL — `/academic/thesis`

### 10.1 Lista de TCCs

| Coluna         | Detalhe                                              |
|----------------|------------------------------------------------------|
| Aluno          | Nome + avatar                                        |
| Curso          | Curso vinculado                                      |
| Título         | Título do trabalho (editável)                        |
| Orientador     | Professor orientador                                 |
| Coorientador   | Opcional                                             |
| Entrega prevista | Data limite                                        |
| Status         | Em orientação / Submetido / Em banca / Aprovado / Reprovado / Reformulação |

### 10.2 Drawer — Cadastrar TCC

- Aluno (busca) · Curso · Tipo: TCC / Monografia / Projeto final / Artigo
- Título (provisório inicialmente)
- Orientador (select de professores habilitados)
- Coorientador (opcional)
- Linha de pesquisa (select configurável por curso)
- Data de início · Data de entrega prevista
- Geração de termo de orientação (PDF com assinatura digital)

### 10.3 Banca de Defesa

- Agendamento da defesa: data · hora · local / link
- Composição da banca: orientador + 2 membros (internos ou externos)
- Membro externo: cadastro de nome + titulação + instituição
- Formulário de avaliação por membro (nota + parecer)
- Nota final: média ponderada configurável
- Resultado: Aprovado / Aprovado com ressalvas / Reprovado
- Ata de defesa gerada automaticamente + assinatura digital da banca
- Entrega da versão final: upload PDF + DOC (repositório)

---

## 11. CURSOS — `/academic/courses`

### 11.1 Lista de Cursos — Datatable (sem alteração da v1)

### 11.2 Grade Curricular — `/academic/courses/curriculum/:uuid` (sem alteração da v1)

### 11.3 Equivalência Curricular — `/academic/courses/curriculum-equivalence`

- Mapa de equivalência entre cursos da mesma instituição
- Tabela: disciplina curso A ↔ disciplina curso B + status (equivalente total / parcial / não equivalente)
- Usado no processo de reopção de curso e aproveitamento de estudos
- Aprovação pelo coordenador

### 11.4 Projeto Pedagógico de Curso (PPC) — detalhado na seção 7.4

---

## 12. TURMAS, NOTAS, FREQUÊNCIA, HORÁRIOS, CALENDÁRIO, OCORRÊNCIAS, REQUERIMENTOS

_(Seções 12–18: mantidas da v1 com as melhorias registradas nas seções de Diário e Secretaria acima)_

### 12.1 Melhorias no Diário de Classe (seção 8 deste spec)
### 12.2 Requerimentos — Workflow Multi-nível

Além do fluxo básico já existente, adicionar:

- Configuração de workflow por tipo de requerimento (ex.: trancamento requer aprovação do coordenador antes da secretaria efetivar)
- Níveis de aprovação: 1 (secretaria) / 2 (secretaria + coordenador) / 3 (secretaria + coord. + diretor)
- SLA diferente por nível
- Notificação a cada mudança de nível
- Delegação de aprovação (aprovador temporário)

---

## 13. PORTAIS DE ACESSO

### 13.1 Portal do Aluno (Self-Service) — `/academic/student-portal`

Área exclusiva do aluno, acessada com login próprio:

- **Dashboard:** notas atuais, frequência atual, avisos importantes, próximas avaliações
- **Boletim:** visualização por período letivo (tabela + gráfico evolução)
- **Frequência:** detalhamento de faltas por disciplina + status de risco
- **Horários:** grade horária da semana atual
- **Calendário:** eventos e prazos importantes
- **Documentos:** solicitação e download de histórico, declarações (self-service)
- **Requerimentos:** abertura e acompanhamento de solicitações
- **Matrícula Online:** acesso ao wizard de rematrícula
- **Contrato:** visualização e download do contrato pedagógico
- **Portfólio:** upload de evidências de aprendizagem
- **TCC/Estágio:** acompanhamento do status
- **Atividades Complementares:** registro e acompanhamento de horas
- **Notificações:** histórico de mensagens recebidas
- **Protocolo:** consulta de status de protocolos abertos

### 13.2 Portal do Professor — `/academic/teacher-portal`

Área exclusiva do professor:

- **Dashboard:** turmas do dia, aulas pendentes, diários não fechados, alertas
- **Diário de Classe:** acesso rápido ao diário por disciplina/turma
- **Chamada:** lançamento de chamada com QR Code ou manual
- **Notas:** lançamento e consulta de notas
- **Plano de Aula:** criação e envio para aprovação
- **Plano de Ensino:** cadastro e edição
- **Portfólio:** avaliação de portfólios dos alunos
- **TCC:** orientação + avaliação de bancas
- **Estágio:** supervisão e relatórios
- **Conselho de Classe:** participação e assinatura de atas
- **Comunicados:** envio de mensagens para alunos/turmas
- **Horários:** visualização da grade pessoal
- **Carga Horária:** resumo semanal/mensal

---

## 14. PROFESSORES — `/academic/teachers` _(sem alteração da v1)_

---

## 15. RELATÓRIOS — `/academic/reports`

### 15.1–15.3 _(mantidos da v1)_

### 15.4 Relatórios Adicionais v2

- **Relatório de Estágios:** alunos em estágio, horas cumpridas, empresas parceiras
- **Relatório de TCC:** status por curso, orientadores, defesas realizadas
- **Relatório de Atividades Complementares:** horas por aluno, tipos mais realizados
- **Relatório de Conselho de Classe:** deliberações por turma/período
- **Relatório CPA:** resultados de avaliação institucional por dimensão
- **Relatório de Equivalências:** aproveitamentos concedidos por curso

---

## 16. BANCO DE DADOS — NOVAS TABELAS (v2)

```sql
-- Prontuário do Aluno
CREATE TABLE student_records (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  student_uuid    CHAR(36) NOT NULL,
  document_type   VARCHAR(100) NOT NULL,
  file_path       VARCHAR(500) NOT NULL,
  file_hash       CHAR(64) NOT NULL,
  version         TINYINT UNSIGNED DEFAULT 1,
  valid_until     DATE NULL,
  uploaded_by     CHAR(36) NOT NULL,
  status          ENUM('pending','approved','rejected','expired') DEFAULT 'pending',
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  deleted_at      DATETIME NULL
);

-- Protocolo de Atendimento
CREATE TABLE service_protocols (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  code            VARCHAR(50) NOT NULL UNIQUE,
  student_uuid    CHAR(36) NOT NULL,
  unit_uuid       CHAR(36) NOT NULL,
  type            ENUM('enrollment','document','request','financial','information','other') NOT NULL,
  channel         ENUM('counter','portal','email','whatsapp','phone') NOT NULL,
  attendant_uuid  CHAR(36),
  request_uuid    CHAR(36) NULL,
  notes           TEXT NULL,
  status          ENUM('open','in_progress','resolved','cancelled') DEFAULT 'open',
  opened_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
  resolved_at     DATETIME NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Fila Virtual
CREATE TABLE service_queue (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unit_uuid       CHAR(36) NOT NULL,
  ticket_number   VARCHAR(20) NOT NULL,
  student_uuid    CHAR(36),
  service_type    VARCHAR(100) NOT NULL,
  priority        TINYINT UNSIGNED DEFAULT 5,
  status          ENUM('waiting','called','in_service','done','skipped') DEFAULT 'waiting',
  issued_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
  called_at       DATETIME NULL,
  finished_at     DATETIME NULL,
  attendant_uuid  CHAR(36) NULL
);

-- Processo Seletivo
CREATE TABLE selective_processes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  code            VARCHAR(50) NOT NULL UNIQUE,
  name            VARCHAR(255) NOT NULL,
  period_uuid     CHAR(36) NOT NULL,
  selection_type  ENUM('exam','enem','history','interview','multiple') NOT NULL,
  registration_start DATE,
  registration_end   DATE,
  exam_date          DATE NULL,
  result_date        DATE NULL,
  enrollment_start   DATE,
  enrollment_end     DATE,
  total_vacancies    SMALLINT UNSIGNED,
  status          ENUM('draft','open','closed','finished') DEFAULT 'draft',
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  deleted_at      DATETIME NULL
);

-- Candidatos do Processo Seletivo
CREATE TABLE selective_candidates (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  process_uuid        CHAR(36) NOT NULL,
  name                VARCHAR(255) NOT NULL,
  cpf                 VARCHAR(14) NOT NULL,
  email               VARCHAR(255),
  phone               VARCHAR(20),
  course_uuid         CHAR(36) NOT NULL,
  score               DECIMAL(5,2) NULL,
  rank_position       SMALLINT UNSIGNED NULL,
  status              ENUM('registered','confirmed','absent','approved','rejected','waitlisted','enrolled') DEFAULT 'registered',
  created_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Pré-matrícula / Lista de Espera
CREATE TABLE pre_enrollments (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  student_uuid    CHAR(36) NOT NULL,
  course_uuid     CHAR(36) NOT NULL,
  class_uuid      CHAR(36) NULL,
  period_uuid     CHAR(36) NOT NULL,
  priority_order  SMALLINT UNSIGNED,
  notified_at     DATETIME NULL,
  expires_at      DATETIME NULL,
  status          ENUM('waiting','notified','confirmed','declined','expired') DEFAULT 'waiting',
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Matrícula Condicional
CREATE TABLE conditional_enrollments (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  enrollment_uuid CHAR(36) NOT NULL,
  condition_type  ENUM('financial','documentary','other') NOT NULL,
  description     TEXT,
  deadline        DATE NOT NULL,
  resolved_at     DATETIME NULL,
  status          ENUM('pending','resolved','expired') DEFAULT 'pending',
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Plano de Aula
CREATE TABLE lesson_plans (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  teacher_uuid    CHAR(36) NOT NULL,
  subject_uuid    CHAR(36) NOT NULL,
  class_uuid      CHAR(36) NOT NULL,
  period_uuid     CHAR(36) NOT NULL,
  type            ENUM('weekly','bimonthly','annual','ppp') NOT NULL,
  objectives      TEXT,
  content         JSON,
  methodology     TEXT,
  resources       JSON,
  bibliography    TEXT,
  bncc_alignment  JSON NULL,
  status          ENUM('draft','submitted','approved','returned') DEFAULT 'draft',
  reviewed_by     CHAR(36) NULL,
  reviewed_at     DATETIME NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at      DATETIME NULL
);

-- Plano de Ensino
CREATE TABLE teaching_plans (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  subject_uuid    CHAR(36) NOT NULL,
  teacher_uuid    CHAR(36) NOT NULL,
  period_uuid     CHAR(36) NOT NULL,
  syllabus        TEXT,
  objectives      TEXT,
  content         JSON,
  methodology     TEXT,
  evaluation_criteria TEXT,
  bibliography_basic TEXT,
  bibliography_complementary TEXT,
  version         TINYINT UNSIGNED DEFAULT 1,
  is_published    TINYINT(1) DEFAULT 0,
  status          ENUM('draft','submitted','approved') DEFAULT 'draft',
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at      DATETIME NULL
);

-- Conselho de Classe
CREATE TABLE class_councils (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  class_uuid      CHAR(36) NOT NULL,
  period_uuid     CHAR(36) NOT NULL,
  scheduled_at    DATETIME NOT NULL,
  location        VARCHAR(255),
  meeting_link    VARCHAR(500) NULL,
  agenda          TEXT,
  general_notes   TEXT NULL,
  status          ENUM('scheduled','in_progress','done','cancelled') DEFAULT 'scheduled',
  minutes_uuid    CHAR(36) NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Deliberações do Conselho por Aluno
CREATE TABLE council_deliberations (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  council_uuid    CHAR(36) NOT NULL,
  enrollment_uuid CHAR(36) NOT NULL,
  opinion         TEXT,
  decision        ENUM('approved','failed','recovery','partial_progression','other') NOT NULL,
  notified        TINYINT(1) DEFAULT 0,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Diário por Disciplina
CREATE TABLE subject_diaries (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  subject_uuid    CHAR(36) NOT NULL,
  class_uuid      CHAR(36) NOT NULL,
  teacher_uuid    CHAR(36) NOT NULL,
  period_uuid     CHAR(36) NOT NULL,
  lesson_date     DATE NOT NULL,
  content_taught  TEXT,
  competencies    JSON NULL,
  resources_used  JSON NULL,
  substitute_uuid CHAR(36) NULL,
  is_makeup       TINYINT(1) DEFAULT 0,
  makeup_ref_uuid CHAR(36) NULL,
  signed_at       DATETIME NULL,
  signed_by       CHAR(36) NULL,
  cert_hash       CHAR(64) NULL,
  is_closed       TINYINT(1) DEFAULT 0,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Estágio
CREATE TABLE internships (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  enrollment_uuid     CHAR(36) NOT NULL,
  type                ENUM('mandatory','voluntary') DEFAULT 'mandatory',
  company_name        VARCHAR(255) NOT NULL,
  company_cnpj        VARCHAR(18),
  company_supervisor  VARCHAR(255),
  teacher_supervisor  CHAR(36) NOT NULL,
  start_date          DATE NOT NULL,
  end_date_expected   DATE NOT NULL,
  end_date_actual     DATE NULL,
  required_hours      SMALLINT UNSIGNED,
  completed_hours     SMALLINT UNSIGNED DEFAULT 0,
  final_grade         DECIMAL(5,2) NULL,
  status              ENUM('active','completed','interrupted','approved') DEFAULT 'active',
  created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
  deleted_at          DATETIME NULL
);

-- TCC
CREATE TABLE thesis_works (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  enrollment_uuid CHAR(36) NOT NULL,
  type            ENUM('tcc','monograph','final_project','article') NOT NULL,
  title           VARCHAR(500),
  advisor_uuid    CHAR(36) NOT NULL,
  co_advisor_uuid CHAR(36) NULL,
  research_line   VARCHAR(255) NULL,
  start_date      DATE,
  deadline        DATE,
  defense_date    DATE NULL,
  final_grade     DECIMAL(5,2) NULL,
  status          ENUM('in_progress','submitted','in_defense','approved','failed','revision') DEFAULT 'in_progress',
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  deleted_at      DATETIME NULL
);

-- Atividades Complementares
CREATE TABLE complementary_activities (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  enrollment_uuid CHAR(36) NOT NULL,
  type            ENUM('event','course','project','extension','publication','other') NOT NULL,
  description     TEXT NOT NULL,
  hours_declared  SMALLINT UNSIGNED NOT NULL,
  hours_validated SMALLINT UNSIGNED NULL,
  document_path   VARCHAR(500),
  validated_by    CHAR(36) NULL,
  validated_at    DATETIME NULL,
  status          ENUM('pending','validated','rejected') DEFAULT 'pending',
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  deleted_at      DATETIME NULL
);

-- PPC (Projeto Pedagógico de Curso)
CREATE TABLE course_ppcs (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  course_uuid     CHAR(36) NOT NULL,
  version         TINYINT UNSIGNED DEFAULT 1,
  content         JSON NOT NULL,
  status          ENUM('draft','in_approval','current','replaced') DEFAULT 'draft',
  approved_by     CHAR(36) NULL,
  approved_at     DATETIME NULL,
  replaces_uuid   CHAR(36) NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Portfólio do Aluno
CREATE TABLE student_portfolios (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  enrollment_uuid CHAR(36) NOT NULL,
  subject_uuid    CHAR(36) NULL,
  period_uuid     CHAR(36) NOT NULL,
  type            ENUM('text','image','file','link','video') NOT NULL,
  title           VARCHAR(255) NOT NULL,
  description     TEXT NULL,
  file_path       VARCHAR(500) NULL,
  external_url    VARCHAR(500) NULL,
  teacher_comment TEXT NULL,
  qualitative_grade VARCHAR(10) NULL,
  is_public       TINYINT(1) DEFAULT 0,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  deleted_at      DATETIME NULL
);

-- Recuperação Paralela
CREATE TABLE parallel_recoveries (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  enrollment_uuid CHAR(36) NOT NULL,
  subject_uuid    CHAR(36) NOT NULL,
  teacher_uuid    CHAR(36) NOT NULL,
  activity_desc   TEXT NOT NULL,
  deadline        DATE NOT NULL,
  submitted_at    DATETIME NULL,
  new_score       DECIMAL(5,2) NULL,
  status          ENUM('pending','submitted','graded') DEFAULT 'pending',
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Livro de Registro Digital
CREATE TABLE registry_books (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unit_uuid       CHAR(36) NOT NULL,
  order_number    INT UNSIGNED NOT NULL,
  enrollment_uuid CHAR(36) NOT NULL,
  registered_at   DATE NOT NULL,
  registered_by   CHAR(36) NOT NULL,
  record_hash     CHAR(64) NOT NULL,
  is_locked       TINYINT(1) DEFAULT 0,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Livro de Atas Digitais
CREATE TABLE meeting_books (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unit_uuid       CHAR(36) NOT NULL,
  type            ENUM('council','assembly','pedagogical','other') NOT NULL,
  title           VARCHAR(255) NOT NULL,
  content         LONGTEXT,
  meeting_date    DATE NOT NULL,
  participants    JSON,
  status          ENUM('draft','signing','signed','published') DEFAULT 'draft',
  record_hash     CHAR(64) NULL,
  created_by      CHAR(36) NOT NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Avaliação Institucional (CPA)
CREATE TABLE institutional_evaluations (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  title           VARCHAR(255) NOT NULL,
  target_audience ENUM('students','teachers','staff','community') NOT NULL,
  start_date      DATE NOT NULL,
  end_date        DATE NOT NULL,
  form_schema     JSON NOT NULL,
  status          ENUM('draft','active','closed','published') DEFAULT 'draft',
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Equivalência Curricular
CREATE TABLE curriculum_equivalences (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid                CHAR(36) NOT NULL UNIQUE,
  source_course_uuid  CHAR(36) NOT NULL,
  source_subject_uuid CHAR(36) NOT NULL,
  target_course_uuid  CHAR(36) NOT NULL,
  target_subject_uuid CHAR(36) NOT NULL,
  equivalence_type    ENUM('full','partial','none') DEFAULT 'full',
  approved_by         CHAR(36) NULL,
  created_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 17. AUTOMAÇÕES (v2 — ampliadas)

| #  | Gatilho                                           | Ação                                                          | Canal                    |
|----|---------------------------------------------------|---------------------------------------------------------------|--------------------------|
| 1  | Aluno com freq. abaixo do threshold               | Notificar responsável + registrar alerta                      | E-mail / WhatsApp        |
| 2  | Aluno com média abaixo do mínimo                  | Criar tarefa para coordenador + notificar aluno               | Sistema + E-mail         |
| 3  | Nova ocorrência grave registrada                  | Notificar responsável + coordenador imediatamente             | WhatsApp / E-mail / Push |
| 4  | Requerimento sem atendimento no SLA               | Escalar para coordenador + alerta no dashboard                | Sistema                  |
| 5  | Prazo de rematrícula a 7 dias                     | Enviar lembrete ao aluno e responsável financeiro             | E-mail / WhatsApp / SMS  |
| 6  | Nota lançada e publicada                          | Notificar aluno + atualizar boletim no portal                 | Push / E-mail            |
| 7  | Diário de classe não fechado 48h após aula        | Alertar professor + coordenador                               | Sistema + E-mail         |
| 8  | Conflito de horário detectado no builder          | Bloquear publicação + notificar coordenador                   | Sistema                  |
| 9  | Aluno sem matrícula 30 dias após prazo            | Mover para "Não Rematriculado" no kanban + CRM                | Sistema                  |
| 10 | Documento de matrícula vencido / pendente         | Notificar aluno e secretaria                                  | E-mail / WhatsApp        |
| 11 | Início de período letivo                          | Gerar turmas a partir do modelo do período anterior           | Sistema (batch)          |
| 12 | Fim de período letivo                             | Calcular situação final de todos os alunos e gerar atas       | Sistema (batch)          |
| 13 | Novo aluno cadastrado                             | Disparar fluxo de boas-vindas (e-mail + checklist docs)       | E-mail / Portal          |
| 14 | Vaga disponível na lista de espera                | Notificar candidato + iniciar contagem regressiva             | E-mail / WhatsApp / SMS  |
| 15 | Prazo de matrícula condicional vencido            | Alertar secretaria + mudar status para "Condicional expirada" | Sistema + E-mail         |
| 16 | Plano de aula não enviado 5 dias antes da aula    | Alertar professor + coordenador                               | Sistema + E-mail         |
| 17 | TCC com prazo de entrega a 30 dias                | Notificar aluno + orientador                                  | E-mail / Portal          |
| 18 | Estágio com horas abaixo do esperado (% mensal)   | Alertar aluno + supervisor                                    | Sistema + E-mail         |
| 19 | Conselho de classe agendado (48h antes)           | Lembrete a todos os participantes                             | E-mail / WhatsApp        |
| 20 | Avaliação CPA aberta                              | Notificar público-alvo com link de acesso                     | E-mail / Portal / Push   |
| 21 | Período de avaliação CPA encerrado                | Gerar relatório consolidado e notificar CPA                   | Sistema + E-mail         |
| 22 | Requerimento aprovado em todos os níveis          | Notificar aluno + gerar documento automaticamente             | E-mail / Portal          |

---

## 18. CONTROLES GLOBAIS (sem alteração da v1)

Todos os módulos incluem na toolbar superior:
- Filtros avançados (drawer lateral com estado persistido)
- Colunas visíveis (toggle por usuário com persistência)
- Exportação: CSV · Excel · PDF · Imprimir
- Importação em lote: CSV com validação e relatório de erros
- Busca global no módulo (shortcut Ctrl+K)
- Ações em lote (habilitadas somente quando há itens selecionados)
- Paginação configurável: 10 / 25 / 50 / 100 por página
- Reload (botão atualizar sem reload de página via fetch)

### Controles de Auditoria
- Toda criação, edição e exclusão registrada em `audit_logs`
- Campos: `user_uuid` · `action` · `table_name` · `record_uuid` · `old_data (JSON)` · `new_data (JSON)` · `ip` · `user_agent` · `created_at`
- Exclusão lógica obrigatória: campo `deleted_at` em todas as entidades

---

## 19. CHECKLIST DE COBERTURA — SGE + SIS + SIGAA

| Funcionalidade                                      | v1  | v2  |
|-----------------------------------------------------|-----|-----|
| Histórico escolar layout MEC (CNE/CEB)              | ❌  | ✅  |
| Declaração de matrícula c/ assinatura ICP-Brasil    | ❌  | ✅  |
| Protocolo de atendimento presencial (senha + fila)  | ❌  | ✅  |
| Arquivo morto / digitalização documentos físicos    | ❌  | ✅  |
| Certidão de conclusão (pós-EAD)                     | ❌  | ✅  |
| Prontuário digital do aluno                         | ❌  | ✅  |
| Requerimentos — workflow de aprovação multi-nível   | parcial | ✅ |
| Documentos — rastreio versão + data validade        | ❌  | ✅  |
| Atendimento ao público — fila virtual + histórico   | ❌  | ✅  |
| Livro de registro digital                           | ❌  | ✅  |
| Livro de atas digitais                              | ❌  | ✅  |
| Plano de aula (PPP + semanal/bimestral)             | ❌  | ✅  |
| Plano de ensino por disciplina                      | ❌  | ✅  |
| Conselho de classe estruturado                      | parcial | ✅ |
| PPC versionado                                      | ❌  | ✅  |
| Avaliação institucional CPA/SINAES                  | ❌  | ✅  |
| Portfólio do aluno                                  | ❌  | ✅  |
| Recuperação paralela                                | ❌  | ✅  |
| Estágio curricular                                  | ❌  | ✅  |
| TCC / Trabalho final                                | ❌  | ✅  |
| Grade curricular — mapa de equivalência             | ❌  | ✅  |
| Diário por disciplina (separado do de turma)        | ❌  | ✅  |
| Conteúdo programático BNCC/DCN por aula             | ❌  | ✅  |
| Habilidades/competências por aula                   | ❌  | ✅  |
| Recursos didáticos por aula                         | ❌  | ✅  |
| Assinatura digital diário (certificado professor)   | ❌  | ✅  |
| Impressão diário layout oficial (frente/verso)      | ❌  | ✅  |
| Substituição professor — registro docente eventual  | ❌  | ✅  |
| Aula de reposição — vínculo calendário + diário     | ❌  | ✅  |
| Chamada por QR Code                                 | ❌  | ✅  |
| Chamada por geolocalização (EAD)                    | ❌  | ✅  |
| Frequência — consolidado legal LDBEN (25%)          | parcial | ✅ |
| Portal de matrícula online (self-service)           | ❌  | ✅  |
| Processo seletivo / vestibular                      | ❌  | ✅  |
| Pré-matrícula + lista de espera + prioridade        | ❌  | ✅  |
| Matrícula condicional (financeira/documental)       | ❌  | ✅  |
| Aproveitamento de estudos (histórico externo)       | ❌  | ✅  |
| Creditação de atividades complementares             | ❌  | ✅  |
| Trancamento com motivo + protocolo formal           | parcial | ✅ |
| Reopção de curso (mudança interna)                  | ❌  | ✅  |
| Contrato pedagógico digital (assinatura eletrônica) | parcial | ✅ |
| Wizard de matrícula — assinatura + termo LGPD       | parcial | ✅ |
| Portal do Aluno (self-service)                      | ❌  | ✅  |
| Portal do Professor                                 | ❌  | ✅  |
| Atividades Complementares                           | ❌  | ✅  |


## 20. API REST ENDPOINTS PRINCIPAIS

### 20.1 Padrão de resposta

Todas as rotas seguem o padrão:

```json
{
  "status": "success",
  "data": {},
  "meta": {
    "page": 1,
    "per_page": 25,
    "total": 150
  },
  "errors": null
}
```

### 20.2 Endpoints principais

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | /api/v1/academic/dashboard | KPIs e widgets do dashboard | AU, CO, SE |
| GET | /api/v1/enrollments | Listar matrículas com filtros | AU, SE |
| POST | /api/v1/enrollments | Criar nova matrícula | SE, AU |
| GET | /api/v1/enrollments/:uuid | Detalhe da matrícula | AU, SE, AL |
| PUT | /api/v1/enrollments/:uuid | Atualizar matrícula | SE, AU |
| PATCH | /api/v1/enrollments/:uuid/status | Alterar status | AU, CO |
| GET | /api/v1/students | Listar alunos | AU, CO, SE |
| POST | /api/v1/students | Criar aluno | SE, AU |
| GET | /api/v1/students/:uuid | Perfil completo do aluno | AU, CO, SE, AL |
| PUT | /api/v1/students/:uuid | Atualizar dados do aluno | SE, AU |
| GET | /api/v1/courses | Listar cursos | ALL |
| POST | /api/v1/courses | Criar curso | AU |
| GET | /api/v1/courses/:uuid/curriculum | Grade curricular do curso | CO, AU |
| PUT | /api/v1/courses/:uuid/curriculum | Atualizar grade curricular | CO, AU |
| POST | /api/v1/classes | Criar turma | AU, CO |
| GET | /api/v1/classes/:uuid/diary | Diário de classe | PR, CO |
| POST | /api/v1/attendance | Registrar chamada | PR, SE |
| GET | /api/v1/attendance/class/:uuid | Frequência por turma | PR, CO, AU |
| GET | /api/v1/grades/enrollment/:uuid | Notas do aluno | AU, CO, PR, AL |
| POST | /api/v1/grades | Lançar nota | PR |
| PATCH | /api/v1/grades/:uuid/publish | Publicar nota | CO, AU |
| GET | /api/v1/schedule/class/:uuid | Grade de horários da turma | ALL |
| POST | /api/v1/schedule | Criar/salvar grade de horários | CO, AU |
| GET | /api/v1/calendar/events | Listar eventos do calendário | ALL |
| POST | /api/v1/calendar/events | Criar evento | AU, CO, SE |
| GET | /api/v1/occurrences | Listar ocorrências | AU, CO, SE |
| POST | /api/v1/occurrences | Registrar ocorrência | PR, SE, CO |
| PATCH | /api/v1/occurrences/:uuid/status | Atualizar status | CO, AU |
| GET | /api/v1/requests | Listar requerimentos | AU, SE |
| POST | /api/v1/requests | Criar requerimento | SE, AL, AU |
| PATCH | /api/v1/requests/:uuid/status | Atualizar status | SE, CO |
| GET | /api/v1/reports/performance | Relatório de desempenho | AU, CO, SE |
| GET | /api/v1/reports/attendance | Relatório de frequência | AU, CO, SE |
| GET | /api/v1/reports/regulatory | Relatórios regulatórios | AU, SA |
| GET | /api/v1/students/:uuid/data-export | Exportação de dados pessoais | AU, SE, AL |
| DELETE | /api/v1/students/:uuid | Exclusão lógica / anonimização agendada | AU, SE |
```

## 21. SEGURANÇA E LGPD

- Dados sensíveis de alunos, responsáveis e saúde são criptografados em repouso.
- Acesso à API exige autenticação JWT e validação de tenant em todas as rotas.
- O sistema aplica RBAC rígido para dados de menores e documentos restritos.
- Exportações de dados pessoais geram registro obrigatório em `audit_logs`.
- Consentimento de uso de dados e imagem é coletado no fluxo de matrícula.
- Alunos desligados entram em política de retenção configurável com anonimização posterior.
- O sistema oferece direito de portabilidade e exportação completa dos dados do titular.
- Exclusão lógica é imediata, com anonimização agendada conforme política da instituição.

## 22. REQUISITOS NÃO FUNCIONAIS

| Requisito | Especificação |
|---|---|
| Performance | Listagens com até 10.000 registros devem responder em até 800ms.
| Paginação | Cursor-based para listas grandes e offset para relatórios.
| Cache | Redis para KPIs do dashboard com TTL de 5 minutos.
| Upload | Máximo de 10MB por arquivo, aceitando PDF, JPG, PNG e DOCX.
| Concorrência | Optimistic locking no lançamento de notas para evitar duplo clique.
| Acessibilidade | WCAG 2.1 AA, contraste adequado, navegação por teclado e ARIA.
| Multi-tenant | Isolamento completo por unidade, com queries sempre filtradas.
| Auditoria | 100% das ações críticas auditadas.
| Internacionalização | Formatação de datas e números por tenant.
| Offline-first | Diário de classe com fila local em IndexedDB para reenvio.

## 23. CHECKLIST DE ENTREGA

### Backend

- REST API versionada em `/api/v1`.
- RBAC com 7 perfis e matriz de permissões.
- Automações com triggers configuráveis.
- Geração de PDFs para boletim, declaração, histórico e atas.
- Fila de notificações para e-mail, WhatsApp, push e SMS.

### Frontend

- Dashboard com KPIs, widgets e gráficos.
- Datatables com filtros, paginação e ações em lote.
- Drawers CRUD completos em todas as entidades.
- Wizards para matrícula e montagem de grade.
- Kanban para rematrículas, ocorrências, requerimentos e justificativas.
- Responsividade mobile, tablet e desktop.

### Banco

- Padrão `id`, `uuid`, `code`.
- Índices em FKs e campos de busca frequente.
- Constraints de integridade referencial.
- Migrations versionadas.
- Seeds para configurações padrão.

### Qualidade e conformidade

- Cobertura de audit logs em 100% das ações críticas.
- Campos LGPD: `consent_at`, `consent_ip`, `deleted_at`, `anonymized_at`.
- Testes de isolamento multi-tenant.
- Validação de conflito de horários.
- Validação de pré-requisitos na grade curricular.
