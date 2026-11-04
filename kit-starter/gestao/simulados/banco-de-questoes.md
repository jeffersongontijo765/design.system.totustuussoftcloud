# Banco de questões

- Portal: Gestão (`gestao.`)
- Área: Simulados
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13); especificação da v1 absorvida integralmente (seção 14)
- Fonte da v2: [47](../../../docs/v2/47-simulados-por-portal.md) (integral); [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.6; [19](../../../docs/v2/19-regras-modulos-3.md), seção 12
- Fonte da v1: [spec_gestao_simulados_ia.md](../../../docs/v2/anexo-v1/spec_gestao_simulados_ia.md) (683 linhas) — absorvida integralmente na seção 14

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. A seção 14 é o texto integral da v1, guardado para que nenhum detalhe se perca; quando ela disser algo diferente das seções 1 a 13, vale a v2. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Manter o banco de questões da unidade com origem, autoria, revisão e situação, base para provas e simulados.

## 3. Telas

- **Questões** (DataTable): enunciado resumido, disciplina, habilidade, dificuldade, autor, situação (`rascunho`, `revisada`, `publicada`, `arquivada`).
- **Questão — editor** (página): enunciado com mídia, alternativas, gabarito, comentário, classificação.
- **Fila de revisão** (aprovação por revisor diferente do autor).

## 4. Permissões por portal (extraídas do SDD)

Do [47](../../../docs/v2/47-simulados-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Criar perfil custom, ver relatórios agregados, ver kanban da unidade, exportar com auditoria | Ver redação individual sem papel de correção. Alterar nota confirmada sem motivo | E |
| **Coordenação pedagógica** | Ver relatório consolidado, confirmar nota em revisão, aprovar reprocessamento | Editar questão de simulado já publicado | E |

## 5. Papéis

- `unit.coordinator`: revisar e publicar.
- `teacher`: elaborar (portal do professor).
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Questão passa por revisão antes de publicar ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.6).
- IA só sugere; nota final nunca é só da IA ([27](../../../docs/v2/27-inteligencia-artificial-e-portais.md)).

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

### 13.1 [47 — Simulados e Correção de Redação, por Portal](../../../docs/v2/47-simulados-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Matriz em [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2, e pendências MOD-05, MOD-06 e MOD-08. Gateway de IA e regras de nota por IA em [27](../../../docs/v2/27-inteligencia-artificial-e-portais.md). Formulários de pesquisa em [41](../../../docs/v2/41-formularios-e-pesquisas.md). Agendamento de sala de prova em [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md). Dado de aluno e de menor em [07](../../../docs/v2/07-privacidade-lgpd.md). Armazenamento de redação e imagem em [21](../../../docs/v2/21-busca-e-armazenamento.md). Auditoria em [29](../../../docs/v2/29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026 a partir de [`spec_gestao_simulados_ia.md`](../../../docs/v2/anexo-v1/spec_gestao_simulados_ia.md) (v1, seções de escopo, perfis, fluxo, correção, OCR e automações). Fecha MOD-08 da [31](../../../docs/v2/31-matriz-portais-modulos.md). Itens **[Decisão do autor]** e **(jurídico)** dependem de resposta.

---

#### 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| O simulado está completo? | **Em parte.** A v1 tem escopo, perfis (ENEM, MEC, Harvard, custom), fluxo, OCR, correção por IA, rubricas, kanban e relatórios. Não tem estados, DDL, nem regra de quem publica e de quem confirma a nota |
| Há conflito com regra da v2? | **Sim.** A v1 gera "nota final estimada" pela IA. A v2 decide que a IA sugere e o professor confirma (MOD-06) |
| Está organizado por portal? | **Não.** A v1 não diz o que o aluno vê antes e depois da correção |
| Há item excluído? | **Sim.** Proctoring com biometria e reconhecimento facial estão fora do escopo, conforme a v1 e a regra de [35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md) |

---

#### 2. Decisões já tomadas que se aplicam aqui

- **MOD-05 (decidido):** o plano PRO libera correção por IA e ranking. O plano básico tem simulado e gabarito.
- **MOD-06 (decidido):** a IA sugere nota e feedback. O professor e a coordenação pedagógica confirmam. Nada chega ao aluno sem aprovação.
- **MOD-04 (decidido):** gabarito óptico pode ser próprio ou de terceiro, por configuração da entidade.

---

#### 3. Perfis de prova

| Perfil | Uso | Regra |
|---|---|---|
| ENEM | Preparação com estrutura do exame, redação dissertativo-argumentativa e competências | Rubrica e competências do perfil, versionadas. Tema central obrigatório |
| MEC | Correção rápida, com envio por foto ou PDF | Mesma estrutura de envio, rubrica simplificada |
| Harvard | Redação analítica longa | Rubrica própria, com peso maior para profundidade crítica |
| Custom | Vestibular, concurso, curso interno | Entidade cria a rubrica. Sem nome de exame oficial sem direito de uso |

Perfil publicado não muda. Mudança gera nova versão, como em [41](../../../docs/v2/41-formularios-e-pesquisas.md), seção 2.3.

---

#### 4. Estados

**Simulado:** `rascunho` → `publicado` → `em_aplicacao` → `encerrado` → `arquivado`.

**Redação:** `enviada` → `ocr_em_andamento` → `ocr_concluido` ou `revisao_ocr` → `em_correcao_ia` → `sugerida_pela_ia` → `em_revisao_professor` → `confirmada` ou `devolvida`.

- `revisao_ocr`: confiança baixa ou página ilegível. Pede novo envio ou leitura manual.
- `devolvida`: o professor pede reprocessamento ou nova entrega. Registrada com motivo.
- Prazo vencido é calculado, não gravado ([18](../../../docs/v2/18-regras-modulos-2.md), T-04).

---

#### 5. Entrada: envio, OCR e fallback

| Etapa | Regra |
|---|---|
| Upload | Imagem, PDF digitalizado, PDF com texto selecionável, ou texto digitado. Tamanho e tipo são validados na entrada ([21](../../../docs/v2/21-busca-e-armazenamento.md)) |
| Conversão | PDF é separado em páginas. Cada página guarda a ordem |
| OCR | Motor de código aberto com versão fixada, em ADR próprio, como na [21](../../../docs/v2/21-busca-e-armazenamento.md), seção 3.10 |
| Confiança | Abaixo do limite configurável, a redação vai para `revisao_ocr`. Limite padrão a definir (SIM-03) |
| Falha em várias páginas | Abre ticket de análise no atendimento ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md)) |

**Dado do aluno na imagem:** a foto da redação pode conter nome e documento do aluno. O sistema recorta o cabeçalho e guarda o nome só como vínculo, não no texto enviado à IA.

---

#### 6. Correção por IA

##### Entrada enviada ao gateway

- Texto transcrito, sem nome e sem identificador do aluno.
- Rubrica ativa e perfil de prova.
- Tema.

Histórico do aluno não é enviado. A comparação com o histórico é feita pelo sistema, depois da resposta.

##### Saída guardada

- Nota por competência e nota total **sugerida**. A v1 chama de "nota final estimada". Na v2 o nome é **nota sugerida**.
- Feedback textual por competência.
- Alerta de fuga do tema e de incoerência.
- Versão do modelo e do prompt, e o hash da entrada.

##### Regras

- A IA não grava nota final. Só o professor ou a coordenação confirma ([27](../../../docs/v2/27-inteligencia-artificial-e-portais.md)).
- Reprocessamento com prompt revisado cria nova versão, sem apagar a anterior.
- Toda chamada passa pelo gateway de IA, com registro ([27](../../../docs/v2/27-inteligencia-artificial-e-portais.md), seção 3).

---

#### 7. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar perfis-modelo, sem dado de aluno | Ver redação ou nota de qualquer entidade | P |
| **Gestão** | Criar perfil custom, ver relatórios agregados, ver kanban da unidade, exportar com auditoria | Ver redação individual sem papel de correção. Alterar nota confirmada sem motivo | E |
| **Professor** | Montar simulado para a própria turma, publicar, revisar sugestão da IA, confirmar ou devolver nota, ver relatório da turma | Ver simulado ou redação de outra turma. Confirmar a própria redação, se for aluno | E |
| **Coordenação pedagógica** | Ver relatório consolidado, confirmar nota em revisão, aprovar reprocessamento | Editar questão de simulado já publicado | E |
| **Aluno** | Enviar redação dentro do prazo, ver a nota e o feedback depois de confirmados. Ver o próprio ranking, se a unidade publicar | Ver nota da IA antes da confirmação. Ver redação de colega. Ver ranking nominal de colegas sem opção da unidade | E |
| **Responsáveis** | Ver a nota confirmada do dependente e o relatório do simulado | Ver redação do dependente com dado de terceiro. Ver outro aluno | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada, por padrão | Ver simulado, redação ou nota | E, [38](../../../docs/v2/38-portal-de-terceiros-prestadores.md) |

**Aluno e nota da IA:** a regra de MOD-06 vale para qualquer nota. A IA nunca aparece ao aluno como nota.

---

#### 8. Relatórios e ranking

- Relatório por competência, por turma e por unidade, com média e distribuição. Abaixo do mínimo de respostas da [41](../../../docs/v2/41-formularios-e-pesquisas.md), seção 3, o grupo não aparece.
- Ranking é do plano PRO (MOD-05). Mostra posição com nome só se a unidade permitir. O padrão é não expor nome de colega.
- Exportação de notas gera evento de auditoria ([29](../../../docs/v2/29-auditoria.md)).

---

#### 9. Automações

- Publicar simulado: aviso à turma, com data de abertura e fechamento.
- Receber redação: OCR automático.
- Concluir OCR com confiança suficiente: correção por IA.
- Confiança baixa: `revisao_ocr` e aviso ao professor.
- Confirmar nota: aviso ao aluno.
- Nota abaixo da meta da rubrica: trilha de reforço, com sugestão de atividade para o professor aprovar.
- Encerrar simulado: relatório consolidado.

---

#### 10. Retenção e segurança

- Redação original (imagem e PDF) segue o prazo de guarda de documentos escolares, a definir **(jurídico)**.
- Texto transcrito segue o mesmo prazo.
- Sem proctoring biométrico e sem reconhecimento facial, como na v1.
- Gravação de vídeo de prova é fora do escopo.

---

#### 11. Pendências

| # | Pendência | Tipo |
|---|---|---|
| SIM-01 | Prazo de guarda de redação original e de transcrição (seção 10) | (jurídico) |
| SIM-02 | Uso de nome de exame oficial (ENEM e outros) no perfil, e a permissão de uso | (jurídico) |
| SIM-03 | Limite padrão de confiança do OCR, abaixo do qual vai para revisão | **Decidido** em 03/11/2026: 80% |
| SIM-04 | Ranking (seção 8) | **Decidido** em 03/11/2026: vários tipos de ranking e de análise, escolhidos pela unidade. Nome do aluno aparece só no ranking da própria turma |
| SIM-05 | Quem aprova a trilha de reforço após nota baixa | **Decidido** em 03/11/2026: a escola configura. Pode ser o professor, a coordenação ou os dois. Prazo padrão de 15 dias para refazer a atividade, ajustável pela escola |
| SIM-06 | Nomenclatura da nota da IA | **Decidido** em 03/11/2026: "nota sugerida", para professor e aluno |
| SIM-07 | DDL de simulado, perfil, questão, redação, OCR, correção e rubrica | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 15.19. Revisão do owner pendente (DDL-01) |

---

#### 12. Critérios de aceite

- [ ] Aluno não vê nota sugerida pela IA antes da confirmação (teste).
- [ ] Nota confirmada não muda sem motivo e sem evento de auditoria (teste).
- [ ] Texto enviado ao gateway não contém nome nem identificador do aluno (varredura).
- [ ] Redação de uma turma não aparece para professor de outra turma (teste de isolamento).
- [ ] OCR com confiança abaixo do limite vai para `revisao_ocr` (teste).
- [ ] Ranking não mostra nome de colega sem a opção da unidade (teste).
- [ ] Itens **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).

### 13.2 [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.6

##### 3.6 Simulados

A v2 tem só a regra de IA em [19](../../../docs/v2/19-regras-modulos-3.md), seção 12, e a linha da tabela em [28](../../../docs/v2/28-cobertura-ia-todos-os-modulos.md). Faltam:

- **Banco de questões**, com origem, autoria, revisão e situação (`rascunho`, `revisada`, `publicada`, `arquivada`).
- **Geração de prova** por perfil (ENEM, vestibular, interna) e gabarito.
- **Gabarito óptico**: a v1 cita, mas não há especificação do leitor. **Decidido** em 03/11/2026: as duas opções, próprio e de terceiro, por configuração da entidade.
- **Correção por IA**. **Conflito:** a v1 ([`spec_gestao_simulados_ia.md`](../../../docs/v2/anexo-v1/spec_gestao_simulados_ia.md), seção "Correção automática por IA") tem como saída "nota final estimada". A v2 proíbe nota final dada só pela IA ([27](../../../docs/v2/27-inteligencia-artificial-e-portais.md), princípio 2 e seção 5.11). Ação: a v2 fica com a regra da [27](../../../docs/v2/27-inteligencia-artificial-e-portais.md). A nota da IA é sugestão; o professor confirma.
- **Anonimização** do aluno enviado ao provedor de IA ([19](../../../docs/v2/19-regras-modulos-3.md), seção 12).
- **Relatórios por portal**: professor vê a turma; aluno vê as próprias provas; responsável vê os filhos; gestor vê a unidade.
- **Plano**: a v1 marca o simulado como "PRO" no portal de gestão. **Decidido** em 03/11/2026: o PRO libera correção por IA e ranking.

### 13.3 [19](../../../docs/v2/19-regras-modulos-3.md), seção 12

#### 12. Simulados com IA

| Regra | Detalhe |
|---|---|
| Auditoria | Obrigatória em notas e revisões (linha 610). |
| Conteúdo gerado | Revisão humana antes de publicar **[Pendente: regra de quem revisa]**. |
| Dados enviados ao provedor | Só o conteúdo do simulado, sem dado pessoal do aluno. Registrar o provedor e a retenção dele ([16](../../../docs/v2/16-integracoes-externas.md)). |

**Defeito:** sem DDL (T-02). Sem definição de como o aluno é identificado nas respostas enviadas à IA.

## 14. Conteúdo integral da v1 (absorvido)

### Spec — Gestão de Simulados e Correção de Redações por IA

- Language Standard: Global English
#### Visão geral

Este módulo atende a gestão completa de simulados de provas, com foco principal em correção automática de redações via IA, suportando perfis de prova como ENEM, MEC, Harvard e perfis customizados. O sistema deve funcionar em ambiente multi-tenant e multi-unidade, com segregação de dados por instituição, unidade, turma e usuário.

O objetivo é centralizar criação, aplicação, correção, auditoria e acompanhamento pedagógico dos simulados, reduzindo o tempo de correção e aumentando a precisão do feedback ao aluno.

---

#### Objetivos do produto

- Criar simulados com perfis prontos e configuráveis.
- Permitir redação digital, manuscrita via imagem e envio em PDF.
- Executar OCR para transcrição automática do conteúdo.
- Aplicar correção automática por IA com rubricas configuráveis.
- Fornecer feedback detalhado por competência e por critério.
- Exibir dashboards, widgets, datatables, charts e fluxos Kanban.
- Permitir revisão humana, override de nota e auditoria completa.
- Integrar automações de notificações, trilhas de reforço e reprocessamento.

---

#### Escopo funcional

##### Inclui

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

##### Não inclui

- Marketplace de questões.
- Correção humana terceirizada.
- Proctoring com biometria.
- Reconhecimento facial avançado.
- Banco público de temas externos sem curadoria.

---

#### Perfis de prova

##### ENEM

Perfil com estrutura inspirada no exame ENEM, incluindo redação dissertativo-argumentativa, competências avaliativas, tema central e trilha de feedback por competência.

##### MEC

Perfil orientado a preparação e correção automatizada, com foco em praticidade, correção rápida e fluxo de envio por foto ou PDF.

##### Harvard

Perfil avançado para redações analíticas, argumentativas e dissertativas longas, com rubricas próprias, maior peso de profundidade crítica e clareza textual.

##### Custom

Perfil livre para vestibulares, concursos, cursos internos e simulados proprietários.

---

#### Requisitos de páginas

##### 1. Dashboard principal

O dashboard deve apresentar visão executiva e operacional do módulo.

###### Widgets obrigatórios

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

###### Gráficos obrigatórios

- Linha de evolução das notas.
- Barras de redações por status.
- Pizza de distribuição por perfil de prova.
- Heatmap de competências mais fracas.
- Funil de processamento OCR → IA → revisão → publicação.

###### Ações rápidas

- Novo simulado.
- Nova rubrica.
- Revisar redações pendentes.
- Criar tema.
- Exportar relatório.

---

##### 2. Lista de simulados

###### Datatable obrigatória

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

###### Controles

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

###### CRUD drawer

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

##### 3. Perfis de prova

###### Lista

- Nome.
- Tipo.
- Base de correção.
- Competências.
- Peso da redação.
- Peso de questões objetivas.
- Status.

###### Configuração

- Número de questões.
- Tempo total.
- Tempo por seção.
- Peso da redação.
- Rubrica associada.
- Modelo de feedback.
- Regra de revisão humana.
- Integração com automações.

###### Ações

- Criar perfil.
- Editar perfil.
- Clonar perfil.
- Arquivar perfil.
- Associar rubrica.

---

##### 4. Redações

###### Lista principal

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

###### Status possíveis

- Pendente.
- Em OCR.
- Texto extraído.
- Em correção.
- Corrigida.
- Em revisão.
- Aprovada.
- Reprovada.
- Reprocessar.

###### Funcionalidades

- Visualizar imagem/PDF original.
- Comparar original vs transcrito.
- Editar transcrição.
- Reprocessar OCR.
- Reprocessar correção.
- Aprovar correção.
- Ajustar nota manualmente.
- Adicionar comentário do professor.

---

##### 5. Tela de correção

A tela de correção deve ser o núcleo operacional do módulo.

###### Seções

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

###### Controles

- Aprovar correção.
- Salvar rascunho.
- Reprocessar.
- Marcar para revisão.
- Aplicar override.
- Registrar observação.
- Enviar feedback ao aluno.

---

##### 6. Kanban de correções

O Kanban deve organizar o fluxo de redações por status.

###### Colunas

- Recebidas.
- OCR em andamento.
- Transcritas.
- Em correção IA.
- Em revisão humana.
- Aprovadas.
- Reprocessar.

###### Regras

- Drag and drop permitido conforme permissão.
- Atualização automática de status.
- Indicadores de SLA por coluna.
- Filtros por unidade, turma e professor.

---

##### 7. Rubricas e competências

###### Cadastro de rubricas

- Nome.
- Tipo de prova.
- Descrição.
- Competências avaliadas.
- Peso por competência.
- Critérios de aprovação.
- Templates de feedback.

###### Exemplo de competências

- Aderência ao tema.
- Estrutura textual.
- Coesão.
- Coerência.
- Argumentação.
- Norma culta.
- Proposta de intervenção.

---

##### 8. Relatórios

###### Relatórios obrigatórios

- Desempenho por aluno.
- Desempenho por turma.
- Desempenho por unidade.
- Evolução por período.
- Média por competência.
- Correlação entre OCR e revisão humana.
- Taxa de reprocessamento.
- Tempo médio de correção.

###### Exportações

- PDF.
- CSV.
- Excel.
- Imagem do gráfico.

---

#### Fluxo de negócio

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

#### Correção automática por IA

##### Entrada

- Texto OCR.
- Redação digitada.
- Rubrica ativa.
- Perfil de prova.
- Histórico do aluno.

##### Saída

- Nota final estimada.
- Nota por competência.
- Classificação de qualidade.
- Feedback textual.
- Observações técnicas.
- Alertas de fuga ao tema.
- Sinalização de incoerências.

##### Regras da IA

- Não sobrescrever automaticamente nota final quando o modo humano estiver ativo.
- Sempre registrar versão da resposta da IA.
- Permitir reprocessamento com prompt revisado.
- Guardar evidência da entrada usada.
- Manter trilha de auditoria.

---

#### OCR e ingestão de PDF

##### Cenários suportados

- Foto de folha manuscrita.
- PDF digitalizado.
- PDF com texto selecionável.
- Imagem isolada por página.

##### Etapas

1. Upload.
2. Validação de formato.
3. Conversão e extração de páginas.
4. Pré-processamento de imagem.
5. OCR.
6. Normalização.
7. Conferência da confiança.
8. Envio para IA.

##### Critérios de fallback

- Se confiança baixa, marcar para revisão manual.
- Se arquivo ilegível, solicitar novo envio.
- Se OCR falhar em múltiplas páginas, criar ticket de análise.

---

#### Automações

- Ao publicar simulado, notificar turma.
- Ao receber redação, iniciar OCR automaticamente.
- Ao concluir OCR, disparar correção por IA.
- Ao detectar baixa confiança, enviar para revisão.
- Ao concluir correção, notificar aluno e professor.
- Ao identificar nota baixa, criar trilha de reforço.
- Ao encerrar simulado, gerar relatório consolidado.

---

#### Requisitos de interface

##### DataTables

As tabelas devem ter:

- Busca global.
- Filtro avançado.
- Ordenação por coluna.
- Paginação.
- Seleção múltipla.
- Ações em massa.
- Colunas configuráveis.
- Estado persistido por usuário.

##### Widgets

- Cards de KPI.
- Estado vazio com CTA.
- Indicadores com cores semânticas.
- Alarmes de SLA.
- Contadores de fila.

##### Charts

- Linha.
- Barra.
- Donut.
- Radar de competências.
- Funil de processamento.
- Heatmap.

##### Drawers CRUD

Usar drawers para:

- Novo simulado.
- Nova rubrica.
- Nova competência.
- Novo tema.
- Revisão de correção.
- Override de nota.

---

#### Permissões

##### Perfis

- Super Admin.
- Admin da instituição.
- Coordenador.
- Professor.
- Corretor.
- Aluno.

##### Ações controladas

- Criar simulado.
- Publicar simulado.
- Corrigir redação.
- Revisar correção.
- Exportar relatório.
- Ajustar nota.
- Gerenciar rubricas.
- Gerenciar perfis.

---

#### Auditoria e logs

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

#### Modelo de dados

##### Tabelas principais

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

##### Relacionamentos

- Um tenant possui várias unidades.
- Uma unidade possui várias turmas.
- Um simulado pertence a um tenant, unidade e turma.
- Uma redação pertence a um aluno e a um simulado.
- Uma redação possui múltiplas versões de correção.
- Uma rubrica possui várias competências.
- Um job OCR pode gerar uma ou mais tentativas de processamento.

---

#### APIs

##### Simulados

- `GET /api/simulations`
- `POST /api/simulations`
- `GET /api/simulations/{id}`
- `PUT /api/simulations/{id}`
- `DELETE /api/simulations/{id}`
- `POST /api/simulations/{id}/publish`
- `POST /api/simulations/{id}/archive`

##### Redações

- `GET /api/essays`
- `POST /api/essays`
- `GET /api/essays/{id}`
- `POST /api/essays/{id}/ocr`
- `POST /api/essays/{id}/correct`
- `POST /api/essays/{id}/review`
- `POST /api/essays/{id}/override`

##### Rubricas

- `GET /api/rubrics`
- `POST /api/rubrics`
- `PUT /api/rubrics/{id}`
- `DELETE /api/rubrics/{id}`

##### Relatórios

- `GET /api/reports/simulations`
- `GET /api/reports/essays`
- `GET /api/reports/performance`

---

#### Requisitos não funcionais

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

#### Segurança

- Autenticação JWT ou sessão segura.
- RBAC por perfil.
- CSRF em ações sensíveis.
- Rate limiting em upload e correção.
- Sanitização de texto enviado por usuário.
- Criptografia em repouso para arquivos sensíveis.
- Assinatura de URLs temporárias para arquivos.
- Auditoria obrigatória em notas e revisões.

---

#### Custos estimados

Os custos devem ser calculados separadamente para OCR e IA, pois cada etapa tem modelo de cobrança próprio. APIs OCR modernas costumam cobrar por página ou imagem processada, enquanto APIs de IA cobram por volume de tokens ou por chamada, dependendo do modelo [web:17][web:18][web:20][web:26][web:29].

##### Estratégia de custo

- OCR apenas quando houver imagem ou PDF escaneado.
- Correção por IA apenas após validação do OCR.
- Cache de resultados de transcrição e correção.
- Reprocessamento manual apenas sob demanda.
- Batch processing para reduzir custo unitário.

##### Observação operacional

Como os preços mudam por provedor e por modelo, a camada de configuração deve permitir trocar o fornecedor de OCR e o fornecedor de IA sem alterar o core do sistema [web:18][web:20][web:26][web:29].

---

#### Critérios de aceite

- É possível criar e publicar simulados com perfil ENEM, MEC, Harvard e custom.
- O aluno consegue enviar redação por imagem, PDF ou texto.
- O sistema executa OCR automaticamente.
- A IA gera correção com nota por competência.
- O professor consegue revisar e sobrescrever a correção.
- O dashboard exibe métricas e gráficos em tempo real.
- O Kanban organiza o fluxo operacional.
- Toda ação crítica fica auditada.

---

#### Prioridade de implementação

##### Fase 1

- Cadastro de perfis.
- Cadastro de rubricas.
- Upload de redações.
- OCR básico.
- Correção por IA.

##### Fase 2

- Dashboard.
- Datatables avançados.
- Kanban.
- Relatórios.
- Notificações.

##### Fase 3

- Automações avançadas.
- Reprocessamento inteligente.
- Trilhas de reforço.
- Otimização de custos.
- Suporte multi-tenant completo.

---

#### Entregáveis finais

- Especificação funcional completa.
- Fluxos de UI.
- Modelo de dados.
- Contratos de API.
- Regras de negócio.
- Requisitos de segurança.
- Estratégia de custos.
- Pipeline OCR + IA.

