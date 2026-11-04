# Spec Completo — Gestão de Preceptoria e Autoavaliação Médica

- Language Standard: Global English
## Visão geral

O módulo de **Gestão de Preceptoria e Autoavaliação Médica** organiza avaliações por ciclos, tópicos, perguntas e respostas, com foco em acompanhamento formativo, feedback estruturado e evolução de competências. Ele cobre o fluxo completo de **avaliação -> tópicos -> perguntas -> respostas**, com autoavaliação do profissional, avaliação do preceptor e consolidação de indicadores. [web:1][web:9]

O desenho abaixo foi pensado para um SaaS enterprise multi-entity/multi-unit, com controle por unidade, perfis de acesso, trilhas de auditoria e automações de acompanhamento. [web:5][web:7]

## Objetivos do módulo

- Permitir criação de instrumentos de avaliação por especialidade, unidade, programa ou turma. [web:1]
- Estruturar o processo em avaliação, tópicos, perguntas e respostas, com pontuação, comentários e evidências. [web:1][web:4]
- Suportar autoavaliação médica, avaliação do preceptor e comparação entre ambas. [web:1][web:9]
- Disponibilizar gestão visual com datatables, widgets, charts, kanban, drawers e automações. [web:3][web:6]
- Garantir rastreabilidade, segurança, controle de acesso e conformidade com regras de privacidade. [web:5]

## Entidades principais

- Avaliação.
- Tópico de avaliação.
- Pergunta.
- Resposta.
- Ciclo de avaliação.
- Participante.
- Preceptor.
- Autoavaliação.
- Avaliação do preceptor.
- Competência.
- Evidência/anexo.
- Regra de automação.
- Log de auditoria. [web:1][web:4][web:5]

## Fluxo funcional

1. O administrador ou coordenador cria uma avaliação. [web:1]
2. A avaliação é dividida em tópicos. [web:1]
3. Cada tópico contém perguntas configuráveis por tipo, peso e obrigatoriedade. [web:1][web:4]
4. O médico responde a autoavaliação. [web:4]
5. O preceptor responde a avaliação correspondente. [web:1]
6. O sistema consolida as respostas, gera indicadores e compara autoavaliação versus avaliação do preceptor. [web:1][web:9]
7. Automations disparam alertas, tarefas ou encaminhamentos quando houver divergências, atraso ou baixa performance. [web:3][web:5]

## Estrutura do domínio

### Avaliação

Representa o formulário ou instrumento principal. Deve ter:
- Título.
- Descrição.
- Unidade.
- Programa.
- Especialidade.
- Status.
- Versão.
- Período de vigência.
- Público-alvo.
- Tipo: autoavaliação, preceptoria ou híbrida. [web:1][web:9]

### Tópicos

Agrupam perguntas por tema:
- Conhecimento técnico.
- Raciocínio clínico.
- Comunicação.
- Ética.
- Postura profissional.
- Segurança do paciente.
- Procedimentos.
- Auto conhecimento. [web:4][web:7]

### Perguntas

Cada pergunta deve suportar:
- Texto.
- Tipo de resposta.
- Peso.
- Obrigatória ou opcional.
- Ordem.
- Tags de competência.
- Critério de pontuação.
- Ajuda contextual.
- Dependência lógica de resposta anterior. [web:1][web:4]

### Respostas

Devem aceitar:
- Nota numérica.
- Texto livre.
- Opção única.
- Múltipla escolha.
- Escala Likert.
- Arquivo/anexo.
- Observação do preceptor.
- Auto comentário do médico. [web:1][web:4]

## Tipos de autoavaliação médica

O módulo deve contemplar autoavaliação médica com foco em:
- Conhecimento clínico.
- Conduta e tomada de decisão.
- Relacionamento interpessoal.
- Organização do trabalho.
- Comunicação com equipe e paciente.
- Gestão do tempo.
- Postura ética.
- Consciência de limites e necessidade de supervisão.
- Reconhecimento de pontos fortes e pontos de melhoria. [web:4][web:7]

## Páginas do sistema

### Dashboard geral

Deve conter:
- Widgets de avaliações abertas, pendentes, concluídas e atrasadas. [web:9]
- Gráfico de evolução de notas por período. [web:9]
- Gráfico de comparação autoavaliação x preceptor. [web:9]
- Lista de alertas e divergências críticas. [web:5]
- Atalhos para criar avaliação, tópico, pergunta e ciclo. [web:3]

### Lista de avaliações

Datatable com:
- Nome.
- Tipo.
- Unidade.
- Especialidade.
- Status.
- Período.
- Total de respondentes.
- Percentual concluído.
- Ações. [web:9]

Controles:
- Filtro por unidade.
- Filtro por período.
- Filtro por status.
- Filtro por especialidade.
- Busca global.
- Exportação CSV/PDF.
- Ações em massa. [web:9]

### Editor de avaliação

Tela principal para montar a estrutura:
- Cabeçalho da avaliação.
- Aba de tópicos.
- Aba de perguntas.
- Aba de regras.
- Aba de preview.
- Aba de publicações. [web:1]

### Gerador de autoavaliação

Tela para montar a autoavaliação médica com:
- Tópicos organizados por competência.
- Perguntas editáveis.
- Ordenação por drag and drop.
- Tipos de resposta.
- Regras de obrigatoriedade.
- Critério de cálculo de resultado final. [web:1][web:4]

### Tela do respondente

Fluxo de resposta com:
- Barra de progresso.
- Salvamento automático.
- Indicação de pendência.
- Navegação por tópico.
- Validação por pergunta.
- Upload de evidência.
- Resumo final antes do envio. [web:1]

### Tela do preceptor

Inclui:
- Visualização das respostas do médico.
- Campo de avaliação paralela.
- Comparação lado a lado.
- Campo de feedback por tópico.
- Campo de feedback geral.
- Aprovação, devolução ou solicitação de revisão. [web:1][web:9]

### Kanban de acompanhamento

Colunas sugeridas:
- Rascunho.
- Em aplicação.
- Em preenchimento.
- Em revisão.
- Devolvido.
- Concluído.
- Atrasado. [web:3]

Cada card mostra:
- Nome do avaliado.
- Ciclo.
- Tópico atual.
- Percentual concluído.
- Responsável.
- Prazo.
- Alertas. [web:3]

## Componentes obrigatórios

### Datatable

Deve suportar:
- Paginação server-side.
- Busca textual.
- Ordenação por coluna.
- Filtros avançados.
- Seleção múltipla.
- Ações em lote.
- Colunas configuráveis.
- Exportação. [web:9]

### Widgets

Widgets recomendados:
- Total de avaliações ativas.
- Avaliações em atraso.
- Média geral por competência.
- Divergência média auto x preceptor.
- Taxa de conclusão.
- Número de alertas ativos. [web:9]

### Charts

Gráficos obrigatórios:
- Linha: evolução temporal das notas.
- Barra: comparação por tópico.
- Radar: perfil de competência.
- Pizza/donut: status das avaliações.
- Heatmap: tópicos x unidades. [web:9]

### CRUD drawers

Usar drawers laterais para:
- Criar/editar avaliação.
- Criar/editar tópico.
- Criar/editar pergunta.
- Ver resposta.
- Registrar feedback.
- Configurar automação. [web:1][web:3]

### Kanban

Deve permitir:
- Drag and drop.
- Filtros por unidade e ciclo.
- WIP limits.
- Regras por coluna.
- Atualização em tempo real. [web:3]

## Regras de negócio

- Uma avaliação pode ter múltiplos tópicos.
- Um tópico pode ter múltiplas perguntas.
- Uma pergunta pode ser obrigatória ou condicional.
- Autoavaliação e avaliação do preceptor podem coexistir no mesmo ciclo.
- O resultado final pode ser ponderado por peso de tópico, peso da pergunta e peso da origem da resposta.
- Avaliações fechadas não podem ser editadas.
- Respostas enviadas devem ficar versionadas.
- Toda alteração deve registrar auditoria. [web:5][web:7]

## Modelo de cálculo

Sugestão:
- Nota da pergunta = resposta normalizada.
- Nota do tópico = média ponderada das perguntas.
- Nota da avaliação = média ponderada dos tópicos.
- Nota final = combinação entre autoavaliação e preceptoria, com pesos configuráveis. [web:1][web:4]

Exemplo:
- Autoavaliação: 40%.
- Preceptoria: 60%.
- Divergência superior a limite gera alerta. [web:1]

## Automações

Regras possíveis:
- Se avaliação atrasar, notificar médico e preceptor.
- Se divergência entre auto e preceptor exceder limiar, abrir tarefa de revisão.
- Se nota final for abaixo de meta, criar plano de desenvolvimento.
- Se avaliação for concluída, consolidar relatório e notificar os envolvidos. [web:3][web:5]

Eventos:
- evaluation.created.
- evaluation.published.
- response.started.
- response.submitted.
- review.completed.
- divergence.detected.
- evaluation.closed. [web:3]

## Controles administrativos

- Gerenciar unidades.
- Gerenciar perfis e permissões.
- Gerenciar modelos de avaliação.
- Gerenciar pesos e fórmulas de cálculo.
- Gerenciar regras de automação.
- Gerenciar retenção de dados.
- Gerenciar auditoria e logs. [web:5][web:7]

## API sugerida

- POST /evaluations.
- GET /evaluations.
- GET /evaluations/:id.
- PATCH /evaluations/:id.
- POST /evaluations/:id/publish.
- POST /evaluations/:id/close.
- POST /evaluations/:id/topics.
- POST /topics/:id/questions.
- POST /responses.
- PATCH /responses/:id.
- POST /responses/:id/submit.
- POST /reviews/:id.
- GET /dashboards/medical-preceptorship.
- GET /reports/evaluation-summary. [web:1][web:9]

## Banco de dados

Tabelas centrais:
- evaluations.
- evaluation_topics.
- evaluation_questions.
- evaluation_answers.
- evaluation_cycles.
- evaluation_participants.
- evaluation_reviews.
- competencies.
- automation_rules.
- audit_logs. [web:5][web:7]

Campos importantes:
- uuid.
- unit_id.
- status.
- version.
- created_by.
- updated_by.
- deleted_at.
- metadata json.
- score_numeric.
- score_weighted. [web:5]

## Segurança e compliance

- Controle de acesso por papel e unidade.
- Registro de auditoria em todas as ações sensíveis.
- Sanitização de respostas livres.
- Proteção contra CSRF e XSS.
- Criptografia de dados sensíveis.
- Políticas de retenção e anonimização. [web:5]

## Estrutura de telas completas

### 1. Gestão de Avaliações
- Lista.
- Criar.
- Editar.
- Duplicar.
- Publicar.
- Encerrar.
- Arquivar.

### 2. Gestão de Tópicos
- Lista.
- Criar.
- Editar.
- Reordenar.
- Vincular competência.
- Definir peso.

### 3. Gestão de Perguntas
- Lista.
- Criar.
- Editar.
- Reordenar.
- Definir tipo.
- Definir regra condicional.
- Definir resposta obrigatória.

### 4. Gestão de Respostas
- Visualizar.
- Corrigir.
- Revisar.
- Comparar auto x preceptor.
- Exportar.

### 5. Gestão de Autoavaliação médica
- Configurar instrumento.
- Aplicar.
- Responder.
- Consolidar.
- Analisar gaps.
- Gerar plano de desenvolvimento.

## O que pode entrar na próxima versão

- OpenAPI completo.
- SQL migration completo.
- Mockup textual de cada página.
- Layout em React/Next.js ou Vue.
- Documento técnico para backend em PHP 8.
- Documento de regras de cálculo por especialidade. [web:1][web:9]
