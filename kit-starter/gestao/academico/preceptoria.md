# Preceptoria

- Portal: Gestão (`gestao.`)
- Área: Acadêmico
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13); especificação da v1 absorvida integralmente (seção 14)
- Fonte da v2: [42](../../../docs/v2/42-preceptoria-por-portal.md) (integral)
- Fonte da v1: [spec-gestao-preceptoria-autoavaliacao.md](../../../docs/v2/anexo-v1/spec-gestao-preceptoria-autoavaliacao.md) (409 linhas) — absorvida integralmente na seção 14

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. A seção 14 é o texto integral da v1, guardado para que nenhum detalhe se perca; quando ela disser algo diferente das seções 1 a 13, vale a v2. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Gerir a preceptoria em duas partes: (A) avaliação e autoavaliação de residentes por instrumentos e ciclos com cálculo e alertas de divergência; (B) tutoria, metas, PDI e evidências.

## 3. Telas

- **Programas e ciclos** (lista e formulário): instrumentos, pesos, ciclos de avaliação.
- **Instrumentos** (editor de questões e escalas).
- **Relatório agregado** (dashboard): médias por competência, divergência entre avaliação e autoavaliação.
- **Alertas de divergência** (fila).
- **Devoluções** (fila de aprovação).

## 4. Permissões por portal (extraídas do SDD)

Do [42](../../../docs/v2/42-preceptoria-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Criar instrumento, ciclo, programa e pesos. Ver relatório agregado. Gerenciar alertas de divergência. Aprovar devolução. Exportar com auditoria | Ver resposta individual de avaliação do preceptor. Ver anotação de tutoria. Ver PDI sem vínculo de coordenação | E |

## 5. Papéis

- `unit.preceptoria.manager`: criar instrumento, ciclo, programa e pesos; relatório agregado; alertas; aprovar devolução; exportar com auditoria. Não vê resposta individual nem anotação de tutoria.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Avaliação do preceptor é anônima para o residente (seção 13, 5).
- Campo de estágio (terceiro) vê só o mínimo para supervisionar (seção 13, 5; [38](../../../docs/v2/38-portal-de-terceiros-prestadores.md)).

## 7. Dados

- Tabelas e campos conforme a seção 13 e o DDL do [51](../../../docs/v2/51-ddl-modulos-novos.md), quando o módulo estiver lá. Toda tabela tem `entidade_id`, `unidade_id`, `created_at`, `updated_at`, `created_by` e exclusão lógica com `deleted_at` e `deleted_by` ([03](../../../docs/v2/03-dominio-tenancy.md), seção 6; [15](../../../docs/v2/15-validacoes.md); [19](../../../docs/v2/19-regras-modulos-3.md), seção 14).

## 8. Integrações

- Ver a seção de integrações do documento de origem, na seção 13.

## 9. Exportação, auditoria e privacidade

- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Toda criação, alteração, aprovação, exclusão lógica, exportação e leitura de dado sensível gera evento de auditoria no banco da unidade ([29](../../../docs/v2/29-auditoria.md)).
- Dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md): mínimo necessário, mascaramento em listas, base legal registrada.

## 10. Estados de interface

- Carregando (skeleton), vazio com chamada para ação, sem resultado de filtro, erro com nova tentativa, acesso negado, registro bloqueado, fechado ou baixado (somente leitura), conflito de edição (versão).

## 11. Requisitos de frontend

- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`): página de lista com DataTable, KPIs, drawer de detalhe, formulário em página ou modal, kanban quando houver fluxo de estados.
- Seletor de unidade no topo quando o usuário tiver mais de uma; a troca reemite o token com o novo contexto ([06](../../../docs/v2/06-identidade-acesso.md), seção 12).

## 12. Critérios de aceite e pendências

- Critérios de aceite: os do documento de origem (seção 13) e os de [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 6.
- Testes de isolamento: usuário de outra unidade ou entidade recebe 404 em toda rota do módulo ([03](../../../docs/v2/03-dominio-tenancy.md)).
- As pendências do documento de origem estão na seção 13 e consolidadas no [45](../../../docs/v2/45-pendencias-consolidadas.md).

## 13. Regras da v2 (texto integral das fontes, sem corte)

### 13.1 [42 — Preceptoria e Autoavaliação, por Portal](../../../docs/v2/42-preceptoria-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Motor de formulários em [41](../../../docs/v2/41-formularios-e-pesquisas.md). Anonimato em [41](../../../docs/v2/41-formularios-e-pesquisas.md), seção 3. Regras já existentes em [19](../../../docs/v2/19-regras-modulos-3.md), seção 11. Estágio e campos de prática em [17](../../../docs/v2/17-regras-modulos.md). Planejamento de desenvolvimento de colaborador em [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 4. Terceiros (campo de estágio) em [38](../../../docs/v2/38-portal-de-terceiros-prestadores.md). Auditoria em [29](../../../docs/v2/29-auditoria.md).
> **Status:** análise e especificação proposta, criada em 03/11/2026 a partir de [`spec-gestao-preceptoria-autoavaliacao.md`](../../../docs/v2/anexo-v1/spec-gestao-preceptoria-autoavaliacao.md) (409 linhas, v1) e da linha "Preceptoria PRO" de [`12-portals-navigation-sidebar-pages-spec.md`](../../../docs/v2/anexo-v1/12-portals-navigation-sidebar-pages-spec.md) (v1, seção 4.2). Itens **[Decisão do autor]** e **(verificar)** dependem de resposta ou de conferência de norma. Não é parecer.

---

#### 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| A preceptoria está especificada? | **Em parte.** A v1 tem especificação de avaliação e autoavaliação. Não tem DDL (T-02), não tem regra de portal além de telas, e a navegação usa o mesmo nome para outra coisa |
| Está organizada por portal? | **Não.** A v1 descreve telas, mas não diz quem vê o quê entre preceptor, residente, gestão e campo de estágio |
| Tem todas as ferramentas? | **Não.** Falta tutoria com registro de encontros, metas com prazo, PDI com plano, evidências com validação, e vínculo com carga de prática |
| Avaliação de preceptor é anônima? | **Pendente.** Regra de anonimato ainda aberta (L-16). Proposta em [41](../../../docs/v2/41-formularios-e-pesquisas.md), seção 3 |
| Usa o motor de formulários? | **Deve usar.** A v1 construiu um editor próprio de perguntas, que duplica [41](../../../docs/v2/41-formularios-e-pesquisas.md) |

---

#### 2. Conflito de nome

| Nome na v1 | Onde | O que é de fato | Decisão proposta |
|---|---|---|---|
| "Preceptoria e autoavaliação médica" | Especificação completa | Avaliação de residente ou estagiário por preceptor, e autoavaliação do próprio residente | Módulo **Preceptoria**, parte A |
| "Preceptoria PRO" | Navegação, seção 4.2 | Tutoria individual de alunos, metas acadêmicas e PDI | Módulo **Preceptoria**, parte B |
| "Plano de Desenvolvimento Individual" | Navegação de preceptoria, e também [37](../../../docs/v2/37-planejamento-e-empenho.md) seção 4 para colaborador | PDI do aluno ou do residente em preceptoria. PDI do colaborador fica em RH | Separado por dono: aluno em preceptoria, colaborador em RH |

**Decidido:** é um módulo só, chamado Preceptoria. A parte A é avaliação e autoavaliação: o instrumento, o ciclo, as respostas e os pesos. A parte B é acompanhamento: tutoria, metas, PDI e evidências. As duas valem para os mesmos residentes e alunos, com a mesma pessoa como preceptor ou tutor.

---

#### 3. Preceptoria, parte A: avaliação e autoavaliação

##### 3.1 Instrumento

| Campo | Regra |
|---|---|
| Tipo | Autoavaliação, avaliação do preceptor, ou híbrido (as duas, com comparação) |
| Vínculo | Programa, especialidade, unidade e período. Um instrumento pode valer para mais de um programa |
| Tópicos | Conhecimento clínico, raciocínio clínico, conduta, comunicação, ética, segurança do paciente, procedimentos, organização do trabalho, consciência de limites |
| Peso | Por tópico e por pergunta, configurável. Soma dos pesos de tópicos fecha em 100% |
| Versão | Instrumento publicado não muda. Mudança gera versão nova ([41](../../../docs/v2/41-formularios-e-pesquisas.md), seção 2.3) |
| Modelos | Modelos da plataforma, sem dado. Entidade copia e ajusta |

Pergunta com tipo, peso, obrigatoriedade, ordem, competência e dependência condicional. O motor de [41](../../../docs/v2/41-formularios-e-pesquisas.md) faz a construção. Esta seção define só o que é de preceptoria.

##### 3.2 Ciclo de avaliação

Um ciclo agrupa instrumentos e participantes em um período. Estados do ciclo: `planejado` → `aberto` → `em_revisao` → `encerrado`.

Estados de cada avaliação individual (guardados em coluna):

`rascunho` → `enviada_pelo_residente` → `em_avaliacao_preceptor` → `em_revisao` → `devolvida` ou `concluida`.

`atrasada` é calculada por prazo, sem coluna ([18](../../../docs/v2/18-regras-modulos-2.md), T-04).

##### 3.3 Cálculo

Regra da v1, mantida:

- Nota da pergunta = resposta normalizada.
- Nota do tópico = média ponderada das perguntas.
- Nota do instrumento = média ponderada dos tópicos.
- Nota final = combinação de autoavaliação e avaliação do preceptor, com pesos configuráveis por programa.

A nota final junta as duas notas: a do próprio residente e a do preceptor. **Decidido pelo autor em 03/11/2026:** o peso de cada nota é definido ao criar a autoavaliação, e não há valor padrão fixo. O exemplo da v1 (40% autoavaliação e 60% preceptor) serve só de referência.

Regra que não muda: divergência entre autoavaliação e avaliação do preceptor acima de limiar gera alerta e tarefa de revisão. Limiar configurável por programa.

##### 3.4 Regras de negócio

- Avaliação fechada não é editada. Resposta enviada fica versionada.
- Autoavaliação e avaliação do preceptor coexistem no mesmo ciclo.
- Avaliação do preceptor é **anônima para o residente**, pela regra de [41](../../../docs/v2/41-formularios-e-pesquisas.md), seção 3. A autoavaliação é identificada.
- Relatório de preceptor, por grupo de residentes, só aparece acima do mínimo de respostas.
- Nota abaixo da meta do programa gera plano de desenvolvimento (parte B), por regra, mas não é publicada sem revisão do preceptor.

---

#### 4. Preceptoria, parte B: tutoria e PDI

##### 4.1 Tutoria

| Recurso | Regra |
|---|---|
| Encontro de tutoria | Data, duração, presença, tópicos, encaminhamentos. Registro feito pelo tutor |
| Anotações | Anotação do tutor é do tutor. Não é visível ao residente, salvo quando o tutor publica como parecer |
| Encaminhamento | Vira tarefa ao responsável pelo encaminhamento (ex.: coordenação, saúde mental, secretaria) |
| Sigilo | Registro de tutoria com menção a saúde ou a dificuldade pessoal é dado sensível. Acesso restrito ao tutor e à coordenação, com auditoria ([07](../../../docs/v2/07-privacidade-lgpd.md), seção 2) |

##### 4.2 Metas e PDI

| Recurso | Regra |
|---|---|
| Meta | Texto, prazo, indicador, responsável e status: `planejada`, `em_andamento`, `atingida`, `nao_atingida`, `cancelada` |
| PDI | Plano que agrupa metas, com ações e prazos. Assinado pelo residente e pelo preceptor |
| Revisão | Revisão periódica com data e parecer. Cada revisão é uma versão do PDI |
| Vínculo | Meta pode ligar a competência da avaliação (parte A) |

##### 4.3 Evidências

Arquivo ou link anexado a uma resposta ou meta (certificado, registro de procedimento, relatório de caso). Regras:

- Evidência com dado de paciente é recusada. O residente anonimiza antes de anexar, e o sistema bloqueia nomes e registros de prontuário no texto.
- Evidência é validada pelo preceptor. Estado: `enviada`, `validada`, `recusada`.
- Armazenamento segue [21](../../../docs/v2/21-busca-e-armazenamento.md). Retenção pelo prazo do programa **(verificar)**.

---

#### 5. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelos de instrumento, sem dado | Ver avaliação, PDI ou tutoria de qualquer entidade | P |
| **Gestão** | Criar instrumento, ciclo, programa e pesos. Ver relatório agregado. Gerenciar alertas de divergência. Aprovar devolução. Exportar com auditoria | Ver resposta individual de avaliação do preceptor. Ver anotação de tutoria. Ver PDI sem vínculo de coordenação | E |
| **Preceptor** | Responder avaliação dos seus residentes. Registrar tutoria e metas dos seus tutorados. Validar evidência. Devolver ou aprovar | Ver residente sem vínculo ativo no programa. Ver avaliação de outro preceptor | E |
| **Residente / aluno** | Responder autoavaliação. Ver a própria avaliação depois da conclusão. Ver PDI e metas. Enviar evidência | Ver avaliação de colega. Ver anotação de tutoria. Ver resposta de avaliação de preceptor, que é anônima | E |
| **Responsáveis** | Nada, por padrão. Residente é adulto | Ver avaliação, PDI, tutoria | E. Para aluno **menor** em preceptoria de tutoria, ver regra de consentimento abaixo |
| **Campo de estágio (terceiro)** | Os dados necessários para supervisionar cada estagiário do próprio campo: nome, frequência na prática, metas de prática, avaliação de desempenho na prática e ocorrências do campo | Tutoria, anotação, PDI, avaliação de outro campo e dado de saúde além de apto ou inapto para a prática | E, pelo contrato em [38](../../../docs/v2/38-portal-de-terceiros-prestadores.md) |

**Menor de idade:** tutoria de aluno menor em preceptoria de tutoria (parte B) exige consentimento do responsável para o registro de tutoria com dado sensível. Sem consentimento, o registro fica limitado a dado de acompanhamento acadêmico ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md)) **(jurídico)**.

---

#### 6. Integrações

| Módulo | Integração |
|---|---|
| Formulários ([41](../../../docs/v2/41-formularios-e-pesquisas.md)) | Motor de construção, convite, resposta e relatório |
| Acadêmico ([17](../../../docs/v2/17-regras-modulos.md)) | Programa, turma, matrícula do residente, carga de prática |
| Agendamento ([44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md)) | Sala de tutoria e de avaliação prática, quando houver |
| RH ([39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md)) | Só para preceptor que também é colaborador da entidade. O PDI do colaborador não fica aqui |
| Terceiros ([38](../../../docs/v2/38-portal-de-terceiros-prestadores.md)) | Campo de estágio, pela regra de contrato |

---

#### 7. Pendências

| # | Pendência | Tipo |
|---|---|---|
| PRE-01 | Preceptoria com partes A e B (seção 2) | **Decidido** em 03/11/2026 |
| PRE-02 | Peso entre autoavaliação e preceptor (seção 3.3) | **Decidido** em 03/11/2026: definido ao criar a autoavaliação |
| PRE-03 | Anonimato da avaliação de preceptor e mínimo de respostas (L-16) | **Decidido** em 03/11/2026: anônima, com mínimo de 2 respostas por grupo ([41](../../../docs/v2/41-formularios-e-pesquisas.md), FRM-01) |
| PRE-04 | Regra de regulamento de residência e avaliação por programa | (verificar) |
| PRE-05 | Prazo de guarda de avaliação, tutoria e PDI | (jurídico) |
| PRE-06 | Consentimento para tutoria de aluno menor com dado sensível (seção 5) | (jurídico) |
| PRE-07 | Campo de estágio como terceiro: os dados necessários para supervisão (seção 5) | **Decidido** em 03/11/2026 |
| PRE-08 | DDL de instrumento, ciclo, avaliação, tutoria, meta, PDI e evidência | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 6. Revisão do owner pendente (DDL-01) |

---

#### 8. Critérios de aceite

- [ ] Residente não vê avaliação do preceptor, que é anônima, e não vê anotação de tutoria (teste).
- [ ] Preceptor não vê residente fora do programa dele (teste de isolamento).
- [ ] Relatório de preceptor abaixo do mínimo de respostas não aparece (teste).
- [ ] Avaliação concluída não é editada, e resposta enviada fica versionada (teste).
- [ ] Divergência acima do limiar gera tarefa de revisão (teste).
- [ ] Evidência com dado de paciente é recusada (teste).
- [ ] Campo de estágio não vê avaliação de estagiário de outro campo (teste de isolamento).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).

## 14. Conteúdo integral da v1 (absorvido)

### Spec Completo — Gestão de Preceptoria e Autoavaliação Médica

- Language Standard: Global English
#### Visão geral

O módulo de **Gestão de Preceptoria e Autoavaliação Médica** organiza avaliações por ciclos, tópicos, perguntas e respostas, com foco em acompanhamento formativo, feedback estruturado e evolução de competências. Ele cobre o fluxo completo de **avaliação -> tópicos -> perguntas -> respostas**, com autoavaliação do profissional, avaliação do preceptor e consolidação de indicadores. [web:1][web:9]

O desenho abaixo foi pensado para um SaaS enterprise multi-entity/multi-unit, com controle por unidade, perfis de acesso, trilhas de auditoria e automações de acompanhamento. [web:5][web:7]

#### Objetivos do módulo

- Permitir criação de instrumentos de avaliação por especialidade, unidade, programa ou turma. [web:1]
- Estruturar o processo em avaliação, tópicos, perguntas e respostas, com pontuação, comentários e evidências. [web:1][web:4]
- Suportar autoavaliação médica, avaliação do preceptor e comparação entre ambas. [web:1][web:9]
- Disponibilizar gestão visual com datatables, widgets, charts, kanban, drawers e automações. [web:3][web:6]
- Garantir rastreabilidade, segurança, controle de acesso e conformidade com regras de privacidade. [web:5]

#### Entidades principais

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

#### Fluxo funcional

1. O administrador ou coordenador cria uma avaliação. [web:1]
2. A avaliação é dividida em tópicos. [web:1]
3. Cada tópico contém perguntas configuráveis por tipo, peso e obrigatoriedade. [web:1][web:4]
4. O médico responde a autoavaliação. [web:4]
5. O preceptor responde a avaliação correspondente. [web:1]
6. O sistema consolida as respostas, gera indicadores e compara autoavaliação versus avaliação do preceptor. [web:1][web:9]
7. Automations disparam alertas, tarefas ou encaminhamentos quando houver divergências, atraso ou baixa performance. [web:3][web:5]

#### Estrutura do domínio

##### Avaliação

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

##### Tópicos

Agrupam perguntas por tema:
- Conhecimento técnico.
- Raciocínio clínico.
- Comunicação.
- Ética.
- Postura profissional.
- Segurança do paciente.
- Procedimentos.
- Auto conhecimento. [web:4][web:7]

##### Perguntas

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

##### Respostas

Devem aceitar:
- Nota numérica.
- Texto livre.
- Opção única.
- Múltipla escolha.
- Escala Likert.
- Arquivo/anexo.
- Observação do preceptor.
- Auto comentário do médico. [web:1][web:4]

#### Tipos de autoavaliação médica

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

#### Páginas do sistema

##### Dashboard geral

Deve conter:
- Widgets de avaliações abertas, pendentes, concluídas e atrasadas. [web:9]
- Gráfico de evolução de notas por período. [web:9]
- Gráfico de comparação autoavaliação x preceptor. [web:9]
- Lista de alertas e divergências críticas. [web:5]
- Atalhos para criar avaliação, tópico, pergunta e ciclo. [web:3]

##### Lista de avaliações

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

##### Editor de avaliação

Tela principal para montar a estrutura:
- Cabeçalho da avaliação.
- Aba de tópicos.
- Aba de perguntas.
- Aba de regras.
- Aba de preview.
- Aba de publicações. [web:1]

##### Gerador de autoavaliação

Tela para montar a autoavaliação médica com:
- Tópicos organizados por competência.
- Perguntas editáveis.
- Ordenação por drag and drop.
- Tipos de resposta.
- Regras de obrigatoriedade.
- Critério de cálculo de resultado final. [web:1][web:4]

##### Tela do respondente

Fluxo de resposta com:
- Barra de progresso.
- Salvamento automático.
- Indicação de pendência.
- Navegação por tópico.
- Validação por pergunta.
- Upload de evidência.
- Resumo final antes do envio. [web:1]

##### Tela do preceptor

Inclui:
- Visualização das respostas do médico.
- Campo de avaliação paralela.
- Comparação lado a lado.
- Campo de feedback por tópico.
- Campo de feedback geral.
- Aprovação, devolução ou solicitação de revisão. [web:1][web:9]

##### Kanban de acompanhamento

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

#### Componentes obrigatórios

##### Datatable

Deve suportar:
- Paginação server-side.
- Busca textual.
- Ordenação por coluna.
- Filtros avançados.
- Seleção múltipla.
- Ações em lote.
- Colunas configuráveis.
- Exportação. [web:9]

##### Widgets

Widgets recomendados:
- Total de avaliações ativas.
- Avaliações em atraso.
- Média geral por competência.
- Divergência média auto x preceptor.
- Taxa de conclusão.
- Número de alertas ativos. [web:9]

##### Charts

Gráficos obrigatórios:
- Linha: evolução temporal das notas.
- Barra: comparação por tópico.
- Radar: perfil de competência.
- Pizza/donut: status das avaliações.
- Heatmap: tópicos x unidades. [web:9]

##### CRUD drawers

Usar drawers laterais para:
- Criar/editar avaliação.
- Criar/editar tópico.
- Criar/editar pergunta.
- Ver resposta.
- Registrar feedback.
- Configurar automação. [web:1][web:3]

##### Kanban

Deve permitir:
- Drag and drop.
- Filtros por unidade e ciclo.
- WIP limits.
- Regras por coluna.
- Atualização em tempo real. [web:3]

#### Regras de negócio

- Uma avaliação pode ter múltiplos tópicos.
- Um tópico pode ter múltiplas perguntas.
- Uma pergunta pode ser obrigatória ou condicional.
- Autoavaliação e avaliação do preceptor podem coexistir no mesmo ciclo.
- O resultado final pode ser ponderado por peso de tópico, peso da pergunta e peso da origem da resposta.
- Avaliações fechadas não podem ser editadas.
- Respostas enviadas devem ficar versionadas.
- Toda alteração deve registrar auditoria. [web:5][web:7]

#### Modelo de cálculo

Sugestão:
- Nota da pergunta = resposta normalizada.
- Nota do tópico = média ponderada das perguntas.
- Nota da avaliação = média ponderada dos tópicos.
- Nota final = combinação entre autoavaliação e preceptoria, com pesos configuráveis. [web:1][web:4]

Exemplo:
- Autoavaliação: 40%.
- Preceptoria: 60%.
- Divergência superior a limite gera alerta. [web:1]

#### Automações

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

#### Controles administrativos

- Gerenciar unidades.
- Gerenciar perfis e permissões.
- Gerenciar modelos de avaliação.
- Gerenciar pesos e fórmulas de cálculo.
- Gerenciar regras de automação.
- Gerenciar retenção de dados.
- Gerenciar auditoria e logs. [web:5][web:7]

#### API sugerida

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

#### Banco de dados

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

#### Segurança e compliance

- Controle de acesso por papel e unidade.
- Registro de auditoria em todas as ações sensíveis.
- Sanitização de respostas livres.
- Proteção contra CSRF e XSS.
- Criptografia de dados sensíveis.
- Políticas de retenção e anonimização. [web:5]

#### Estrutura de telas completas

##### 1. Gestão de Avaliações
- Lista.
- Criar.
- Editar.
- Duplicar.
- Publicar.
- Encerrar.
- Arquivar.

##### 2. Gestão de Tópicos
- Lista.
- Criar.
- Editar.
- Reordenar.
- Vincular competência.
- Definir peso.

##### 3. Gestão de Perguntas
- Lista.
- Criar.
- Editar.
- Reordenar.
- Definir tipo.
- Definir regra condicional.
- Definir resposta obrigatória.

##### 4. Gestão de Respostas
- Visualizar.
- Corrigir.
- Revisar.
- Comparar auto x preceptor.
- Exportar.

##### 5. Gestão de Autoavaliação médica
- Configurar instrumento.
- Aplicar.
- Responder.
- Consolidar.
- Analisar gaps.
- Gerar plano de desenvolvimento.

#### O que pode entrar na próxima versão

- OpenAPI completo.
- SQL migration completo.
- Mockup textual de cada página.
- Layout em React/Next.js ou Vue.
- Documento técnico para backend em PHP 8.
- Documento de regras de cálculo por especialidade. [web:1][web:9]
