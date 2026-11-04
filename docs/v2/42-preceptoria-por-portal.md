# 42 — Preceptoria e Autoavaliação, por Portal

> Parte do [SDD v2](00-README.md). Motor de formulários em [41](41-formularios-e-pesquisas.md). Anonimato em [41](41-formularios-e-pesquisas.md), seção 3. Regras já existentes em [19](19-regras-modulos-3.md), seção 11. Estágio e campos de prática em [17](17-regras-modulos.md). Planejamento de desenvolvimento de colaborador em [37](37-planejamento-e-empenho.md), seção 4. Terceiros (campo de estágio) em [38](38-portal-de-terceiros-prestadores.md). Auditoria em [29](29-auditoria.md).
> **Status:** análise e especificação proposta, criada em 03/11/2026 a partir de [`spec-gestao-preceptoria-autoavaliacao.md`](anexo-v1/spec-gestao-preceptoria-autoavaliacao.md) (409 linhas, v1) e da linha "Preceptoria PRO" de [`12-portals-navigation-sidebar-pages-spec.md`](anexo-v1/12-portals-navigation-sidebar-pages-spec.md) (v1, seção 4.2). Itens **[Decisão do autor]** e **(verificar)** dependem de resposta ou de conferência de norma. Não é parecer.

---

## 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| A preceptoria está especificada? | **Em parte.** A v1 tem especificação de avaliação e autoavaliação. Não tem DDL (T-02), não tem regra de portal além de telas, e a navegação usa o mesmo nome para outra coisa |
| Está organizada por portal? | **Não.** A v1 descreve telas, mas não diz quem vê o quê entre preceptor, residente, gestão e campo de estágio |
| Tem todas as ferramentas? | **Não.** Falta tutoria com registro de encontros, metas com prazo, PDI com plano, evidências com validação, e vínculo com carga de prática |
| Avaliação de preceptor é anônima? | **Pendente.** Regra de anonimato ainda aberta (L-16). Proposta em [41](41-formularios-e-pesquisas.md), seção 3 |
| Usa o motor de formulários? | **Deve usar.** A v1 construiu um editor próprio de perguntas, que duplica [41](41-formularios-e-pesquisas.md) |

---

## 2. Conflito de nome

| Nome na v1 | Onde | O que é de fato | Decisão proposta |
|---|---|---|---|
| "Preceptoria e autoavaliação médica" | Especificação completa | Avaliação de residente ou estagiário por preceptor, e autoavaliação do próprio residente | Módulo **Preceptoria**, parte A |
| "Preceptoria PRO" | Navegação, seção 4.2 | Tutoria individual de alunos, metas acadêmicas e PDI | Módulo **Preceptoria**, parte B |
| "Plano de Desenvolvimento Individual" | Navegação de preceptoria, e também [37](37-planejamento-e-empenho.md) seção 4 para colaborador | PDI do aluno ou do residente em preceptoria. PDI do colaborador fica em RH | Separado por dono: aluno em preceptoria, colaborador em RH |

**Decidido:** é um módulo só, chamado Preceptoria. A parte A é avaliação e autoavaliação: o instrumento, o ciclo, as respostas e os pesos. A parte B é acompanhamento: tutoria, metas, PDI e evidências. As duas valem para os mesmos residentes e alunos, com a mesma pessoa como preceptor ou tutor.

---

## 3. Preceptoria, parte A: avaliação e autoavaliação

### 3.1 Instrumento

| Campo | Regra |
|---|---|
| Tipo | Autoavaliação, avaliação do preceptor, ou híbrido (as duas, com comparação) |
| Vínculo | Programa, especialidade, unidade e período. Um instrumento pode valer para mais de um programa |
| Tópicos | Conhecimento clínico, raciocínio clínico, conduta, comunicação, ética, segurança do paciente, procedimentos, organização do trabalho, consciência de limites |
| Peso | Por tópico e por pergunta, configurável. Soma dos pesos de tópicos fecha em 100% |
| Versão | Instrumento publicado não muda. Mudança gera versão nova ([41](41-formularios-e-pesquisas.md), seção 2.3) |
| Modelos | Modelos da plataforma, sem dado. Entidade copia e ajusta |

Pergunta com tipo, peso, obrigatoriedade, ordem, competência e dependência condicional. O motor de [41](41-formularios-e-pesquisas.md) faz a construção. Esta seção define só o que é de preceptoria.

### 3.2 Ciclo de avaliação

Um ciclo agrupa instrumentos e participantes em um período. Estados do ciclo: `planejado` → `aberto` → `em_revisao` → `encerrado`.

Estados de cada avaliação individual (guardados em coluna):

`rascunho` → `enviada_pelo_residente` → `em_avaliacao_preceptor` → `em_revisao` → `devolvida` ou `concluida`.

`atrasada` é calculada por prazo, sem coluna ([18](18-regras-modulos-2.md), T-04).

### 3.3 Cálculo

Regra da v1, mantida:

- Nota da pergunta = resposta normalizada.
- Nota do tópico = média ponderada das perguntas.
- Nota do instrumento = média ponderada dos tópicos.
- Nota final = combinação de autoavaliação e avaliação do preceptor, com pesos configuráveis por programa.

A nota final junta as duas notas: a do próprio residente e a do preceptor. **Decidido pelo autor em 03/11/2026:** o peso de cada nota é definido ao criar a autoavaliação, e não há valor padrão fixo. O exemplo da v1 (40% autoavaliação e 60% preceptor) serve só de referência.

Regra que não muda: divergência entre autoavaliação e avaliação do preceptor acima de limiar gera alerta e tarefa de revisão. Limiar configurável por programa.

### 3.4 Regras de negócio

- Avaliação fechada não é editada. Resposta enviada fica versionada.
- Autoavaliação e avaliação do preceptor coexistem no mesmo ciclo.
- Avaliação do preceptor é **anônima para o residente**, pela regra de [41](41-formularios-e-pesquisas.md), seção 3. A autoavaliação é identificada.
- Relatório de preceptor, por grupo de residentes, só aparece acima do mínimo de respostas.
- Nota abaixo da meta do programa gera plano de desenvolvimento (parte B), por regra, mas não é publicada sem revisão do preceptor.

---

## 4. Preceptoria, parte B: tutoria e PDI

### 4.1 Tutoria

| Recurso | Regra |
|---|---|
| Encontro de tutoria | Data, duração, presença, tópicos, encaminhamentos. Registro feito pelo tutor |
| Anotações | Anotação do tutor é do tutor. Não é visível ao residente, salvo quando o tutor publica como parecer |
| Encaminhamento | Vira tarefa ao responsável pelo encaminhamento (ex.: coordenação, saúde mental, secretaria) |
| Sigilo | Registro de tutoria com menção a saúde ou a dificuldade pessoal é dado sensível. Acesso restrito ao tutor e à coordenação, com auditoria ([07](07-privacidade-lgpd.md), seção 2) |

### 4.2 Metas e PDI

| Recurso | Regra |
|---|---|
| Meta | Texto, prazo, indicador, responsável e status: `planejada`, `em_andamento`, `atingida`, `nao_atingida`, `cancelada` |
| PDI | Plano que agrupa metas, com ações e prazos. Assinado pelo residente e pelo preceptor |
| Revisão | Revisão periódica com data e parecer. Cada revisão é uma versão do PDI |
| Vínculo | Meta pode ligar a competência da avaliação (parte A) |

### 4.3 Evidências

Arquivo ou link anexado a uma resposta ou meta (certificado, registro de procedimento, relatório de caso). Regras:

- Evidência com dado de paciente é recusada. O residente anonimiza antes de anexar, e o sistema bloqueia nomes e registros de prontuário no texto.
- Evidência é validada pelo preceptor. Estado: `enviada`, `validada`, `recusada`.
- Armazenamento segue [21](21-busca-e-armazenamento.md). Retenção pelo prazo do programa **(verificar)**.

---

## 5. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelos de instrumento, sem dado | Ver avaliação, PDI ou tutoria de qualquer entidade | P |
| **Gestão** | Criar instrumento, ciclo, programa e pesos. Ver relatório agregado. Gerenciar alertas de divergência. Aprovar devolução. Exportar com auditoria | Ver resposta individual de avaliação do preceptor. Ver anotação de tutoria. Ver PDI sem vínculo de coordenação | E |
| **Preceptor** | Responder avaliação dos seus residentes. Registrar tutoria e metas dos seus tutorados. Validar evidência. Devolver ou aprovar | Ver residente sem vínculo ativo no programa. Ver avaliação de outro preceptor | E |
| **Residente / aluno** | Responder autoavaliação. Ver a própria avaliação depois da conclusão. Ver PDI e metas. Enviar evidência | Ver avaliação de colega. Ver anotação de tutoria. Ver resposta de avaliação de preceptor, que é anônima | E |
| **Responsáveis** | Nada, por padrão. Residente é adulto | Ver avaliação, PDI, tutoria | E. Para aluno **menor** em preceptoria de tutoria, ver regra de consentimento abaixo |
| **Campo de estágio (terceiro)** | Os dados necessários para supervisionar cada estagiário do próprio campo: nome, frequência na prática, metas de prática, avaliação de desempenho na prática e ocorrências do campo | Tutoria, anotação, PDI, avaliação de outro campo e dado de saúde além de apto ou inapto para a prática | E, pelo contrato em [38](38-portal-de-terceiros-prestadores.md) |

**Menor de idade:** tutoria de aluno menor em preceptoria de tutoria (parte B) exige consentimento do responsável para o registro de tutoria com dado sensível. Sem consentimento, o registro fica limitado a dado de acompanhamento acadêmico ([26](26-sdd-juridico-regulatorio.md)) **(jurídico)**.

---

## 6. Integrações

| Módulo | Integração |
|---|---|
| Formulários ([41](41-formularios-e-pesquisas.md)) | Motor de construção, convite, resposta e relatório |
| Acadêmico ([17](17-regras-modulos.md)) | Programa, turma, matrícula do residente, carga de prática |
| Agendamento ([44](44-agendamento-ambientes-equipamentos.md)) | Sala de tutoria e de avaliação prática, quando houver |
| RH ([39](39-departamento-pessoal-rh-medicina-por-portal.md)) | Só para preceptor que também é colaborador da entidade. O PDI do colaborador não fica aqui |
| Terceiros ([38](38-portal-de-terceiros-prestadores.md)) | Campo de estágio, pela regra de contrato |

---

## 7. Pendências

| # | Pendência | Tipo |
|---|---|---|
| PRE-01 | Preceptoria com partes A e B (seção 2) | **Decidido** em 03/11/2026 |
| PRE-02 | Peso entre autoavaliação e preceptor (seção 3.3) | **Decidido** em 03/11/2026: definido ao criar a autoavaliação |
| PRE-03 | Anonimato da avaliação de preceptor e mínimo de respostas (L-16) | **Decidido** em 03/11/2026: anônima, com mínimo de 2 respostas por grupo ([41](41-formularios-e-pesquisas.md), FRM-01) |
| PRE-04 | Regra de regulamento de residência e avaliação por programa | (verificar) |
| PRE-05 | Prazo de guarda de avaliação, tutoria e PDI | (jurídico) |
| PRE-06 | Consentimento para tutoria de aluno menor com dado sensível (seção 5) | (jurídico) |
| PRE-07 | Campo de estágio como terceiro: os dados necessários para supervisão (seção 5) | **Decidido** em 03/11/2026 |
| PRE-08 | DDL de instrumento, ciclo, avaliação, tutoria, meta, PDI e evidência | **Escrito** em [51](51-ddl-modulos-novos.md), seção 6. Revisão do owner pendente (DDL-01) |

---

## 8. Critérios de aceite

- [ ] Residente não vê avaliação do preceptor, que é anônima, e não vê anotação de tutoria (teste).
- [ ] Preceptor não vê residente fora do programa dele (teste de isolamento).
- [ ] Relatório de preceptor abaixo do mínimo de respostas não aparece (teste).
- [ ] Avaliação concluída não é editada, e resposta enviada fica versionada (teste).
- [ ] Divergência acima do limiar gera tarefa de revisão (teste).
- [ ] Evidência com dado de paciente é recusada (teste).
- [ ] Campo de estágio não vê avaliação de estagiário de outro campo (teste de isolamento).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
