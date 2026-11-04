# Spec — Gestão de Simulados e Correção de Redações por IA

- Language Standard: Global English
## Visão geral

Este módulo atende a gestão completa de simulados de provas, com foco principal em correção automática de redações via IA, suportando perfis de prova como ENEM, MEC, Harvard e perfis customizados. O sistema deve funcionar em ambiente multi-tenant e multi-unidade, com segregação de dados por instituição, unidade, turma e usuário.

O objetivo é centralizar criação, aplicação, correção, auditoria e acompanhamento pedagógico dos simulados, reduzindo o tempo de correção e aumentando a precisão do feedback ao aluno.

---

## Objetivos do produto

- Criar simulados com perfis prontos e configuráveis.
- Permitir redação digital, manuscrita via imagem e envio em PDF.
- Executar OCR para transcrição automática do conteúdo.
- Aplicar correção automática por IA com rubricas configuráveis.
- Fornecer feedback detalhado por competência e por critério.
- Exibir dashboards, widgets, datatables, charts e fluxos Kanban.
- Permitir revisão humana, override de nota e auditoria completa.
- Integrar automações de notificações, trilhas de reforço e reprocessamento.

---

## Escopo funcional

### Inclui

- Gestão de simulados.
- Gestão de perfis de prova.
- Gestão de questões objetivas.
- Gestão de redações.
- Upload de imagens e PDFs.
- OCR e extração de texto.
- Correção por IA.
- Rubricas e competências.
- Relatórios analíticos.
- Dashboard operacional.
- Kanban de correções.
- Automações e notificações.
- Controle de permissões e auditoria.

### Não inclui

- Marketplace de questões.
- Correção humana terceirizada.
- Proctoring com biometria.
- Reconhecimento facial avançado.
- Banco público de temas externos sem curadoria.

---

## Perfis de prova

### ENEM

Perfil com estrutura inspirada no exame ENEM, incluindo redação dissertativo-argumentativa, competências avaliativas, tema central e trilha de feedback por competência.

### MEC

Perfil orientado a preparação e correção automatizada, com foco em praticidade, correção rápida e fluxo de envio por foto ou PDF.

### Harvard

Perfil avançado para redações analíticas, argumentativas e dissertativas longas, com rubricas próprias, maior peso de profundidade crítica e clareza textual.

### Custom

Perfil livre para vestibulares, concursos, cursos internos e simulados proprietários.

---

## Requisitos de páginas

### 1. Dashboard principal

O dashboard deve apresentar visão executiva e operacional do módulo.

#### Widgets obrigatórios

- Total de simulados criados.
- Total de simulados publicados.
- Total de redações enviadas.
- Total de redações corrigidas por IA.
- Redações pendentes de revisão humana.
- Tempo médio de OCR.
- Tempo médio de correção por IA.
- Taxa de sucesso de OCR.
- Taxa de aprovação por competência.
- Média geral por turma.
- Evolução mensal.
- Alertas críticos.

#### Gráficos obrigatórios

- Linha de evolução das notas.
- Barras de redações por status.
- Pizza de distribuição por perfil de prova.
- Heatmap de competências mais fracas.
- Funil de processamento OCR → IA → revisão → publicação.

#### Ações rápidas

- Novo simulado.
- Nova rubrica.
- Revisar redações pendentes.
- Criar tema.
- Exportar relatório.

---

### 2. Lista de simulados

#### Datatable obrigatória

A listagem deve conter:

- Nome do simulado.
- Perfil de prova.
- Unidade.
- Turma.
- Status.
- Data de abertura.
- Data de encerramento.
- Total de alunos inscritos.
- Total de redações recebidas.
- Média geral.
- Ações.

#### Controles

- Busca global.
- Filtros por status, perfil, unidade, turma e período.
- Ordenação por coluna.
- Paginação.
- Exportação CSV/PDF.
- Ações em massa.
- Duplicar simulado.
- Arquivar.
- Publicar.
- Encerrar.

#### CRUD drawer

O cadastro e edição devem acontecer preferencialmente em drawer lateral com:

- Nome.
- Descrição.
- Perfil de prova.
- Unidade.
- Turma(s).
- Datas.
- Regras de envio.
- Configurações de correção.
- Regras de pontuação.
- Status.

---

### 3. Perfis de prova

#### Lista

- Nome.
- Tipo.
- Base de correção.
- Competências.
- Peso da redação.
- Peso de questões objetivas.
- Status.

#### Configuração

- Número de questões.
- Tempo total.
- Tempo por seção.
- Peso da redação.
- Rubrica associada.
- Modelo de feedback.
- Regra de revisão humana.
- Integração com automações.

#### Ações

- Criar perfil.
- Editar perfil.
- Clonar perfil.
- Arquivar perfil.
- Associar rubrica.

---

### 4. Redações

#### Lista principal

- Aluno.
- Simulado.
- Perfil.
- Status do OCR.
- Status da correção IA.
- Nota estimada.
- Revisão humana.
- Data de envio.
- Data de processamento.
- Ações.

#### Status possíveis

- Pendente.
- Em OCR.
- Texto extraído.
- Em correção.
- Corrigida.
- Em revisão.
- Aprovada.
- Reprovada.
- Reprocessar.

#### Funcionalidades

- Visualizar imagem/PDF original.
- Comparar original vs transcrito.
- Editar transcrição.
- Reprocessar OCR.
- Reprocessar correção.
- Aprovar correção.
- Ajustar nota manualmente.
- Adicionar comentário do professor.

---

### 5. Tela de correção

A tela de correção deve ser o núcleo operacional do módulo.

#### Seções

- Cabeçalho com aluno, simulado e status.
- Visualização do arquivo enviado.
- Transcrição OCR lado a lado.
- Rubrica de avaliação.
- Nota por competência.
- Explicação gerada pela IA.
- Pontos fortes.
- Pontos de melhoria.
- Sugestão de reescrita.
- Campo para revisão humana.
- Campo para override de nota.
- Histórico de versões da correção.

#### Controles

- Aprovar correção.
- Salvar rascunho.
- Reprocessar.
- Marcar para revisão.
- Aplicar override.
- Registrar observação.
- Enviar feedback ao aluno.

---

### 6. Kanban de correções

O Kanban deve organizar o fluxo de redações por status.

#### Colunas

- Recebidas.
- OCR em andamento.
- Transcritas.
- Em correção IA.
- Em revisão humana.
- Aprovadas.
- Reprocessar.

#### Regras

- Drag and drop permitido conforme permissão.
- Atualização automática de status.
- Indicadores de SLA por coluna.
- Filtros por unidade, turma e professor.

---

### 7. Rubricas e competências

#### Cadastro de rubricas

- Nome.
- Tipo de prova.
- Descrição.
- Competências avaliadas.
- Peso por competência.
- Critérios de aprovação.
- Templates de feedback.

#### Exemplo de competências

- Aderência ao tema.
- Estrutura textual.
- Coesão.
- Coerência.
- Argumentação.
- Norma culta.
- Proposta de intervenção.

---

### 8. Relatórios

#### Relatórios obrigatórios

- Desempenho por aluno.
- Desempenho por turma.
- Desempenho por unidade.
- Evolução por período.
- Média por competência.
- Correlação entre OCR e revisão humana.
- Taxa de reprocessamento.
- Tempo médio de correção.

#### Exportações

- PDF.
- CSV.
- Excel.
- Imagem do gráfico.

---

## Fluxo de negócio

1. Admin cria um perfil de prova.
2. Professor monta um simulado.
3. Simulado é publicado para uma turma.
4. O aluno envia a redação por imagem, PDF ou texto.
5. O sistema executa OCR.
6. O texto é normalizado.
7. A IA corrige com base na rubrica.
8. O professor pode revisar e ajustar.
9. O feedback é entregue ao aluno.
10. Os dados entram nos relatórios e dashboards.

---

## Correção automática por IA

### Entrada

- Texto OCR.
- Redação digitada.
- Rubrica ativa.
- Perfil de prova.
- Histórico do aluno.

### Saída

- Nota final estimada.
- Nota por competência.
- Classificação de qualidade.
- Feedback textual.
- Observações técnicas.
- Alertas de fuga ao tema.
- Sinalização de incoerências.

### Regras da IA

- Não sobrescrever automaticamente nota final quando o modo humano estiver ativo.
- Sempre registrar versão da resposta da IA.
- Permitir reprocessamento com prompt revisado.
- Guardar evidência da entrada usada.
- Manter trilha de auditoria.

---

## OCR e ingestão de PDF

### Cenários suportados

- Foto de folha manuscrita.
- PDF digitalizado.
- PDF com texto selecionável.
- Imagem isolada por página.

### Etapas

1. Upload.
2. Validação de formato.
3. Conversão e extração de páginas.
4. Pré-processamento de imagem.
5. OCR.
6. Normalização.
7. Conferência da confiança.
8. Envio para IA.

### Critérios de fallback

- Se confiança baixa, marcar para revisão manual.
- Se arquivo ilegível, solicitar novo envio.
- Se OCR falhar em múltiplas páginas, criar ticket de análise.

---

## Automações

- Ao publicar simulado, notificar turma.
- Ao receber redação, iniciar OCR automaticamente.
- Ao concluir OCR, disparar correção por IA.
- Ao detectar baixa confiança, enviar para revisão.
- Ao concluir correção, notificar aluno e professor.
- Ao identificar nota baixa, criar trilha de reforço.
- Ao encerrar simulado, gerar relatório consolidado.

---

## Requisitos de interface

### DataTables

As tabelas devem ter:

- Busca global.
- Filtro avançado.
- Ordenação por coluna.
- Paginação.
- Seleção múltipla.
- Ações em massa.
- Colunas configuráveis.
- Estado persistido por usuário.

### Widgets

- Cards de KPI.
- Estado vazio com CTA.
- Indicadores com cores semânticas.
- Alarmes de SLA.
- Contadores de fila.

### Charts

- Linha.
- Barra.
- Donut.
- Radar de competências.
- Funil de processamento.
- Heatmap.

### Drawers CRUD

Usar drawers para:

- Novo simulado.
- Nova rubrica.
- Nova competência.
- Novo tema.
- Revisão de correção.
- Override de nota.

---

## Permissões

### Perfis

- Super Admin.
- Admin da instituição.
- Coordenador.
- Professor.
- Corretor.
- Aluno.

### Ações controladas

- Criar simulado.
- Publicar simulado.
- Corrigir redação.
- Revisar correção.
- Exportar relatório.
- Ajustar nota.
- Gerenciar rubricas.
- Gerenciar perfis.

---

## Auditoria e logs

Registrar eventos de:

- Criação de simulado.
- Alteração de perfil.
- Upload de redação.
- Início de OCR.
- Finalização de OCR.
- Correção por IA.
- Revisão humana.
- Override de nota.
- Envio de feedback.
- Reprocessamento.

Campos mínimos de auditoria:

- Usuário.
- Data e hora.
- Ação.
- Entidade afetada.
- Antes.
- Depois.
- Origem da requisição.

---

## Modelo de dados

### Tabelas principais

- tenants
- units
- classrooms
- users
- exam_profiles
- rubrics
- rubric_competencies
- simulations
- simulation_classrooms
- prompts
- essays
- essay_files
- ocr_jobs
- ai_corrections
- correction_versions
- feedbacks
- notifications
- audit_logs
- automation_jobs

### Relacionamentos

- Um tenant possui várias unidades.
- Uma unidade possui várias turmas.
- Um simulado pertence a um tenant, unidade e turma.
- Uma redação pertence a um aluno e a um simulado.
- Uma redação possui múltiplas versões de correção.
- Uma rubrica possui várias competências.
- Um job OCR pode gerar uma ou mais tentativas de processamento.

---

## APIs

### Simulados

- `GET /api/simulations`
- `POST /api/simulations`
- `GET /api/simulations/{id}`
- `PUT /api/simulations/{id}`
- `DELETE /api/simulations/{id}`
- `POST /api/simulations/{id}/publish`
- `POST /api/simulations/{id}/archive`

### Redações

- `GET /api/essays`
- `POST /api/essays`
- `GET /api/essays/{id}`
- `POST /api/essays/{id}/ocr`
- `POST /api/essays/{id}/correct`
- `POST /api/essays/{id}/review`
- `POST /api/essays/{id}/override`

### Rubricas

- `GET /api/rubrics`
- `POST /api/rubrics`
- `PUT /api/rubrics/{id}`
- `DELETE /api/rubrics/{id}`

### Relatórios

- `GET /api/reports/simulations`
- `GET /api/reports/essays`
- `GET /api/reports/performance`

---

## Requisitos não funcionais

- Tempo de resposta da interface abaixo de 300 ms em telas críticas.
- Processamento assíncrono para OCR e IA.
- Suporte a filas e retries.
- Logs estruturados.
- Escalabilidade horizontal.
- Controle de acesso por tenant.
- LGPD por design.
- Backup e recuperação.
- Observabilidade com métricas e tracing.

---

## Segurança

- Autenticação JWT ou sessão segura.
- RBAC por perfil.
- CSRF em ações sensíveis.
- Rate limiting em upload e correção.
- Sanitização de texto enviado por usuário.
- Criptografia em repouso para arquivos sensíveis.
- Assinatura de URLs temporárias para arquivos.
- Auditoria obrigatória em notas e revisões.

---

## Custos estimados

Os custos devem ser calculados separadamente para OCR e IA, pois cada etapa tem modelo de cobrança próprio. APIs OCR modernas costumam cobrar por página ou imagem processada, enquanto APIs de IA cobram por volume de tokens ou por chamada, dependendo do modelo [web:17][web:18][web:20][web:26][web:29].

### Estratégia de custo

- OCR apenas quando houver imagem ou PDF escaneado.
- Correção por IA apenas após validação do OCR.
- Cache de resultados de transcrição e correção.
- Reprocessamento manual apenas sob demanda.
- Batch processing para reduzir custo unitário.

### Observação operacional

Como os preços mudam por provedor e por modelo, a camada de configuração deve permitir trocar o fornecedor de OCR e o fornecedor de IA sem alterar o core do sistema [web:18][web:20][web:26][web:29].

---

## Critérios de aceite

- É possível criar e publicar simulados com perfil ENEM, MEC, Harvard e custom.
- O aluno consegue enviar redação por imagem, PDF ou texto.
- O sistema executa OCR automaticamente.
- A IA gera correção com nota por competência.
- O professor consegue revisar e sobrescrever a correção.
- O dashboard exibe métricas e gráficos em tempo real.
- O Kanban organiza o fluxo operacional.
- Toda ação crítica fica auditada.

---

## Prioridade de implementação

### Fase 1

- Cadastro de perfis.
- Cadastro de rubricas.
- Upload de redações.
- OCR básico.
- Correção por IA.

### Fase 2

- Dashboard.
- Datatables avançados.
- Kanban.
- Relatórios.
- Notificações.

### Fase 3

- Automações avançadas.
- Reprocessamento inteligente.
- Trilhas de reforço.
- Otimização de custos.
- Suporte multi-tenant completo.

---

## Entregáveis finais

- Especificação funcional completa.
- Fluxos de UI.
- Modelo de dados.
- Contratos de API.
- Regras de negócio.
- Requisitos de segurança.
- Estratégia de custos.
- Pipeline OCR + IA.

