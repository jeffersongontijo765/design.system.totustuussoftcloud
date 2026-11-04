# 59 — Estrutura Acadêmica, por Portal: Cursos, Disciplinas, Grades, Períodos e Sistemas Avaliativos

> Parte do [SDD v2](00-README.md). Primeira lacuna da ordem de fechamento de [55](55-academico-verificacao-e-lacunas.md), seção 3. Escopo decidido: os três níveis, básico, técnico e superior (ACA-01). Calendário letivo em [58](58-calendario-e-eventos-por-portal.md). Matrícula e enturmação em [46](46-matricula-e-rematricula-por-portal.md). Regras de nota e de frequência em [17](17-regras-modulos.md), seção 4. Plano pedagógico em [55](55-academico-verificacao-e-lacunas.md), item 7. Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna 1 do acadêmico. Pontos que dependem de norma de ensino estão marcados **(verificar)**.

---

## 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Cursos, disciplinas e grades estão especificados? | **Não.** Aparecem como nomes de entidades em [17](17-regras-modulos.md), seção 4.1 |
| Versão de grade e de PPC? | **Não.** A v1 cita PPC versionado, sem regra de vigência |
| Sistemas avaliativos? | **Não.** A v1 cita escalas e tipos de avaliação em configuração, sem regra |
| Equivalência entre cursos? | **Não.** A v1 cita mapa de equivalência, sem regra |

---

## 2. Tipos de curso

| Tipo | Nível | Exige |
|---|---|---|
| Educação infantil | Básico | Idade. Avaliação sem objetivo de promoção (LDB, art. 31, I). 800 horas anuais em 200 dias, 4 horas diárias no turno parcial e 7 no integral (art. 31, II e III) |
| Ensino fundamental | Básico | Série. 800 horas anuais em 200 dias letivos (LDB, art. 24, I). Pelo menos 4 horas diárias de aula efetiva, salvo noturno (art. 34) |
| Ensino médio | Básico | Série ou itinerário. Duração mínima de 3 anos (art. 35). 1.000 horas anuais em 200 dias, com ampliação progressiva até 1.400 (art. 24, I e § 1º). Formação geral básica de pelo menos 2.400 horas, ou 2.100 no técnico (art. 35-C) |
| Curso técnico de nível médio | Técnico | Eixo tecnológico, carga horária, estágio se o curso exigir. Forma **integrada** (matrícula única, para quem concluiu o fundamental), **concomitante** (matrículas distintas, na mesma ou em outra instituição) ou **subsequente** (para quem concluiu o médio) (LDB, arts. 36-B e 36-C). Segue as diretrizes do CNE, as normas do sistema de ensino e o Catálogo Nacional de Cursos Técnicos (arts. 36-B, § 1º, e 42-A, § 3º). Pode ter etapas com certificado de qualificação (art. 36-D, parágrafo único) |
| Formação inicial e continuada | Técnico | Qualificação profissional (LDB, art. 39, § 2º, I). Matrícula pela capacidade de aproveitamento, não necessariamente pela escolaridade (art. 42) |
| Graduação tecnológica | Superior | Organizada pelas diretrizes do CNE e pelo Catálogo Nacional de Cursos Superiores de Tecnologia (LDB, arts. 39, § 3º, e 42-A, § 3º) |
| Graduação | Superior | Créditos ou carga horária, atividades complementares, TCC se o curso exigir. Ano letivo de pelo menos 200 dias de trabalho acadêmico (art. 47). Carga horária pela diretriz curricular de cada curso **(verificar)** |
| Pós-graduação lato sensu | Superior | Especialização ou aperfeiçoamento, para diplomado em graduação (LDB, art. 44, III). Carga horária, trabalho final |
| Pós-graduação stricto sensu | Superior | Mestrado ou doutorado (art. 44, III) |
| Curso sequencial e extensão | Superior | Abertos conforme requisitos da instituição; o sequencial exige ensino médio concluído (art. 44, I e IV) |
| Curso livre | Livre | Sem regra de grade oficial |

Tipo de curso define quais campos são obrigatórios. Não há campo fixo comum a todos.

**Publicação no superior** (LDB, art. 47, § 1º, com a Lei 13.168/2015): antes de cada período letivo, a instituição publica programas, componentes curriculares, duração, requisitos, qualificação dos professores, recursos e critérios de avaliação, em página com o título "Grade e Corpo Docente", em toda propaganda eletrônica e em local visível. A página traz a data da última atualização, é publicada até um mês antes das aulas e é atualizada a cada semestre ou ano. O sistema gera essa página a partir da grade e dos docentes do curso e avisa o aluno de mudança até o início das aulas.

---

## 3. Entidades e regras

### 3.1 Curso

- Tem tipo, nome, código, carga horária total, duração prevista e situação.
- Situação: `rascunho`, `ativo`, `suspenso`, `extinto`. Curso extinto não recebe nova matrícula, mas mantém o histórico dos alunos.
- Ato de autorização ou reconhecimento do curso, quando exigido, é anexo com validade **(verificar)**.

### 3.2 Disciplina

- Catálogo por entidade. Campos: código, nome, carga horária, tipo (obrigatória, optativa, eletiva, estágio, TCC, atividade complementar).
- Pré-requisito é lista de disciplinas, com regra de cumprimento.
- Disciplina em uso não é excluída. Só pode ficar `inativa`.

### 3.3 Grade curricular

- Grade pertence a um curso e tem **vigência**: data de início e, quando houver, data de fim.
- Estados: `rascunho`, `vigente`, `substituida`.
- Grade vigente não muda. Mudança gera nova versão, e os alunos já matriculados permanecem na versão em que entraram. A migração para a nova versão é autorizada pela coordenação e executada pela secretaria, com registro.
- Cada item da grade tem: disciplina, período ou semestre, carga horária, pré-requisitos e se é obrigatório.

### 3.4 Projeto pedagógico (PPC)

- Versionado, por curso. Mesma regra de vigência da grade.
- Contém objetivos, perfil, organização e regras de avaliação. O texto final é aprovado pelo órgão colegiado da entidade ([37](37-planejamento-e-empenho.md), PLN-01) **(verificar)**.

### 3.5 Equivalência entre cursos

- Mapa de disciplinas entre duas grades, com equivalência total, parcial ou sem equivalência.
- Equivalência é usada por reopção de curso ([46](46-matricula-e-rematricula-por-portal.md), seção 5) e por aproveitamento de estudos.
- Equivalência não é automática sem registro. Cada equivalência tem responsável e data.

### 3.6 Períodos letivos

- Período pertence ao calendário da unidade ([58](58-calendario-e-eventos-por-portal.md)): bimestre, trimestre, semestre ou módulo.
- Estados: `planejado`, `aberto`, `em_fechamento`, `fechado`, `reaberto` (com justificativa).
- Período fechado não aceita lançamento de nota nem de frequência, salvo reabertura autorizada ([17](17-regras-modulos.md), seção 4.3).

---

## 4. Sistemas avaliativos

Cada curso usa um sistema avaliativo. Um sistema define:

| Elemento | Opções | Regra |
|---|---|---|
| Escala | Numérica (ex.: 0 a 10), conceitual (ex.: A a E), percentual | Uma escala por sistema |
| Tipos de avaliação | Prova, trabalho, seminário, atividade prática, autoavaliação | Cada tipo tem peso |
| Método de média | Aritmética ou ponderada | Pesos somam 100% por período |
| Recuperação | Paralela, final, ou ambas | Nota de recuperação substitui ou compõe a média, conforme o sistema |
| Nota mínima de aprovação | Valor da escala | Por sistema |
| Frequência mínima | Percentual de presença | 75% do total de horas letivas no fundamental e no médio (LDB, art. 24, VI). 60% na pré-escola (art. 31, IV). No superior, a frequência de alunos e professores é obrigatória, salvo nos programas de educação a distância (art. 47, § 3º, texto literal conferido). A LDB não fixa percentual para o superior: o valor vem do regimento da instituição e é configurado por curso. O valor fica no sistema avaliativo, com esses mínimos como piso |
| Aprovação por conselho | Sim ou não | Casos fora da regra passam por conselho de classe ([55](55-academico-verificacao-e-lacunas.md), item 5) |

**Regras:**

- Nota fora da escala é recusada.
- Sistema avaliativo em uso não muda. Mudança gera nova versão, aplicada ao próximo período.
- Arredondamento padrão: uma casa decimal, arredondando para cima a partir de 0,05. A entidade pode definir outra regra, registrada no próprio sistema avaliativo.

---

## 5. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelos de curso e de sistema avaliativo, sem dado | Ver grade, PPC ou dado de entidade | P |
| **Gestão** | Criar e aprovar cursos, grades, PPC e sistemas avaliativos. Definir vigência | Alterar grade vigente sem nova versão | E |
| **Coordenação pedagógica** | Montar grade, disciplinas, equivalências e PPC. Propor sistema avaliativo | Publicar PPC sem aprovação do colegiado | E |
| **Secretaria** | Consultar grade e sistema. Cadastrar período letivo e equivalência aprovada | Criar disciplina ou grade | E |
| **Professor** | Ver grade e sistema das próprias disciplinas | Alterar grade ou sistema | E |
| **Aluno** | Ver grade da própria matrícula e o sistema avaliativo do curso | Ver grade de outro curso | E |
| **Responsáveis** | Ver grade e sistema do dependente | Ver grade de outro aluno | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada | Qualquer item da estrutura | E |

---

## 6. Integrações

| Módulo | Relação |
|---|---|
| Calendário ([58](58-calendario-e-eventos-por-portal.md)) | Período letivo pertence ao calendário |
| Matrícula ([46](46-matricula-e-rematricula-por-portal.md)) | Matrícula aponta para curso, grade e versão |
| Diário ([17](17-regras-modulos.md)) | Nota e frequência seguem o sistema avaliativo do curso |
| Conselho de classe ([55](55-academico-verificacao-e-lacunas.md), item 5) | Aprovação fora da regra |
| Estágio e TCC ([55](55-academico-verificacao-e-lacunas.md), item 8) | Disciplinas do tipo estágio e TCC |
| Agendamento ([44](44-agendamento-ambientes-equipamentos.md)) | Turma e disciplina reservam ambiente |
| Relatórios ([56](56-configuracoes-e-relatorios-lacunas.md)) | Grade curricular e sistema avaliativo |

---

## 7. Pendências

| # | Pendência | Tipo |
|---|---|---|
| EST-01 | Frequência mínima de aprovação por nível de ensino (seção 4) | **Conferido** em 03/11/2026: 75% no fundamental e no médio (LDB, art. 24, VI) e 60% na pré-escola (art. 31, IV). No superior, a LDB só torna a frequência obrigatória (art. 47, § 3º) e não fixa percentual: vale o regimento da instituição, configurado por curso |
| EST-02 | Carga horária mínima por nível, e regra de créditos no superior (seção 2) | **Conferido** em parte em 03/11/2026: educação básica na LDB (arts. 24, 31, 34 e 35-C). Superior depende da diretriz de cada curso **(verificar)** |
| EST-03 | Tipos de curso e nomenclatura do ensino técnico e superior, conforme norma do sistema de ensino | **Conferido** em 03/11/2026: LDB, arts. 36-B a 36-D, 39, 42, 42-A e 44 (seção 2). Os catálogos CNCT e CNCST entram como tabela de referência carregada do MEC |
| EST-04 | Arredondamento padrão das notas | **Decidido** em 03/11/2026: uma casa decimal, arredondando para cima a partir de 0,05. A entidade pode trocar |
| EST-05 | Autorização de migração de aluno entre versões da grade | **Decidido** em 03/11/2026: a coordenação autoriza, e a secretaria executa a migração com autorização registrada |
| EST-06 | Ato de autorização e reconhecimento do curso: formato e validade (seção 3.1) | (jurídico) |
| EST-07 | DDL das tabelas: curso, disciplina, grade, item de grade, PPC, equivalência, período e sistema avaliativo | **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.3. Revisão do owner pendente (DDL-01) |

---

## 8. Critérios de aceite

- [ ] Grade vigente não muda; mudança gera nova versão (teste).
- [ ] Matrícula aponta para a versão da grade em que entrou (teste).
- [ ] Disciplina em uso não é excluída, só inativada (teste).
- [ ] Nota fora da escala do sistema é recusada (teste).
- [ ] Período fechado não aceita lançamento (teste).
- [ ] Equivalência sem responsável e data não é usada em aproveitamento (teste).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
