# Séries e turmas (grade de horários)

- Portal: Gestão (`gestao.`)
- Área: Acadêmico
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md) (integral)
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Criar turmas, cadastrar salas de referência, grupos de horários, enturmar alunos e montar, validar e publicar a grade de horários da unidade sem conflito de professor, sala ou turma.

## 3. Telas

- **Turmas** (DataTable): curso, grade e versão, série/período, turno, sala, vagas, ocupação, estado; ações abrir, encerrar.
- **Turma — formulário** (página): campos da seção 13 (cadastro), capacidade, sala de referência.
- **Salas** (lista): capacidade, recursos, acessibilidade (integra [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md)).
- **Grupos de horários** (lista e editor de tempos por turno).
- **Montagem da grade** (quadro semanal com arrastar e soltar): aulas por turma, professor e sala; validação de conflito em tempo real; carga docente (limite de 40 horas-aula por semana, [37](../../../docs/v2/37-planejamento-e-empenho.md)).
- **Publicar grade** (modal): lista de conflitos bloqueantes; publicar exige aprovação da gestão; versão anterior preservada.
- **Consultas** (por professor, por sala, por turma) e **ocupação da unidade** (dashboard).

## 4. Permissões por portal (extraídas do SDD)

Do [60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Aprovar grade, abrir e encerrar turma, ver ocupação da unidade | Alterar grade publicada sem nova versão | E |
| **Coordenação** | Montar turmas, enturmar, montar e publicar grade, autorizar troca de professor | Publicar grade com conflito | E |
| **Secretaria** | Enturmar com autorização, cadastrar sala de referência, consultar grade | Criar turma ou aula | E |

## 5. Papéis

- `unit.manager`: aprovar grade, abrir e encerrar turma, ver ocupação.
- `unit.coordinator`: montar turmas, enturmar, montar e publicar grade, autorizar troca de professor.
- `unit.secretary`: enturmar com autorização, cadastrar sala, consultar grade; não cria turma nem aula.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Não se publica grade com conflito ([60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md), seção 4.2).
- Grade publicada só muda por nova versão.
- Enturmação respeita vaga com bloqueio de concorrência ([15](../../../docs/v2/15-validacoes.md), seção 7).

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

### 13.1 [60 — Turmas, Enturmação e Grade de Horários, por Portal](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Segunda e terceira lacunas da ordem de [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), seção 3. Estrutura de curso e grade em [59](../../../docs/v2/59-estrutura-academica-por-portal.md). Calendário e dias não letivos em [58](../../../docs/v2/58-calendario-e-eventos-por-portal.md). Enturmação e vagas em [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), M-03 e M-07. Salas e reservas em [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md). Carga docente em [37](../../../docs/v2/37-planejamento-e-empenho.md), PLN-05. Aula online em [40](../../../docs/v2/40-aulas-online-por-portal.md). Aviso de mudança em [57](../../../docs/v2/57-notificacoes-por-portal.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha as lacunas de turma e de grade de horários. A v1 tem as páginas `classes/list`, `classes/schedule`, `schedule/builder` e `schedule/rooms`, sem regra.

---

#### 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| Turma tem regra? | **Não.** Aparece só em [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), M-07, como destino de enturmação |
| Grade de horários tem regra? | **Não.** A v1 tem um construtor de horários, sem regra de conflito |
| Conflito de professor, sala e turma? | **Não.** Só a regra de sala de [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md) |
| Carga do professor? | **Parcial.** Limite de 40 horas-aula por semana em [37](../../../docs/v2/37-planejamento-e-empenho.md), PLN-05 |

---

#### 2. Turma

##### 2.1 Cadastro

Uma turma pertence a: unidade, curso, versão da grade, período letivo e turno.

| Campo | Regra |
|---|---|
| Código | Único na unidade e no período |
| Série ou módulo | Pertence à grade. Não é texto livre |
| Turno | Manhã, tarde, noite, integral ou EAD |
| Capacidade | Número de vagas. Matrícula não passa da capacidade ([46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), M-03) |
| Sala de referência | Ambiente padrão de [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md), quando houver |
| Professor regente | Um por turma, quando a norma exigir |
| Professores por disciplina | Um por disciplina e por turma |

##### 2.2 Cadastro de salas

Sala é o ambiente físico onde a aula acontece. Usa o mesmo registro de recurso de [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md), `recursos` do tipo `ambiente`. Não há cadastro paralelo de sala.

| Campo | Regra |
|---|---|
| Código e nome | Únicos na unidade |
| Tipo | Sala de aula, laboratório, auditório, quadra, sala multimídia, sala de reunião, sala de atendimento |
| Capacidade de aula | Número de lugares para aula. Turma maior que a capacidade é recusada na grade |
| Andar e bloco | Para orientação e para o aviso de mudança de sala |
| Recursos fixos | Projetor, quadro, ar-condicionado, acessibilidade, bancadas, computadores |
| Acessibilidade | Indicação de acesso para pessoa com deficiência. Turma com aluno que precisa dessa acessibilidade só é alocada em sala que a tenha |
| Reservável | Sim ou não. Sala de aula fixa na grade não é reservável para uso avulso |
| Status | `ativa`, `manutencao`, `inativa` |

**Regras:**

- Sala em `manutencao` não recebe aula nem reserva, com data prevista de retorno. Aula afetada é remanejada com aviso ([57](../../../docs/v2/57-notificacoes-por-portal.md)).
- Sala `inativa` não aparece na grade nova. Não é excluída se houver histórico de aula.
- Cadastro e alteração de sala geram evento de auditoria ([29](../../../docs/v2/29-auditoria.md)).
- Inativar sala com aula futura exige remanejamento antes.

**Quem cadastra:** secretaria e coordenação cadastram. Gestão aprova inativação e manutenção prolongada.

##### 2.3 Estados

`planejada` → `aberta` → `em_andamento` → `encerrada`, com `cancelada` a partir de `planejada` ou `aberta`.

- Turma `aberta` recebe matrícula.
- Turma `encerrada` não recebe lançamento de nota nem de frequência.
- Turma sem alunos ao abrir o período é `cancelada`, com aviso à coordenação.

##### 2.4 Enturmação

- Aluno matriculado é enturmado em uma turma da própria grade vigente ([59](../../../docs/v2/59-estrutura-academica-por-portal.md), seção 3.3).
- Enturmação passa da capacidade? Recusada. Vai para lista de espera ([46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), seção 4).
- Transferência de turma segue M-07 de [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), com aprovação da coordenação.

---

#### 3. Grupos de horários

Grupo de horários é o modelo de tempo da unidade: os blocos de aula, com início e fim, por turno.

- Um grupo tem blocos ordenados: número, início, fim e intervalo.
- Um grupo é usado por várias turmas do mesmo turno.
- Mudança de bloco em grupo usado por turma em andamento só vale para o período seguinte.

---

#### 4. Grade de horários

##### 4.1 Aula

Cada aula da grade tem: turma, disciplina, professor, bloco do grupo de horários, dia da semana, ambiente e tipo (presencial, online, híbrida, EAD).

##### 4.2 Regras de conflito

A grade não é salva com conflito. As regras são:

| Conflito | Regra |
|---|---|
| Professor em duas aulas no mesmo bloco | Recusado |
| Turma em duas aulas no mesmo bloco | Recusado |
| Ambiente em duas aulas no mesmo bloco | Recusado. Usa a regra de sobreposição de [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md), seção 3.2 |
| Aula em dia não letivo | Recusada. Regra de [58](../../../docs/v2/58-calendario-e-eventos-por-portal.md), seção 4 |
| Professor acima de 40 horas-aula por semana | Aviso, não bloqueio. Limite por unidade, PLN-05 de [37](../../../docs/v2/37-planejamento-e-empenho.md) |
| Aula ou exame no domingo, com professor de escola particular | Recusado. CLT, art. 319, conferido em 03/11/2026 ([39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 3.4). Em escola pública, vale o estatuto do ente |
| Aula online sem ambiente físico | Permitida. Não reserva sala. Segue [40](../../../docs/v2/40-aulas-online-por-portal.md) |
| Disciplina sem professor habilitado | Recusada. Habilitação é cadastro do professor |

##### 4.3 Publicação

- Grade é montada em `rascunho` e revisada pela coordenação.
- Publicação torna a grade `vigente` para o período.
- Grade publicada não muda sem nova versão. Mudança de um período em andamento gera aviso aos alunos e professores afetados ([57](../../../docs/v2/57-notificacoes-por-portal.md)) com 5 dias úteis de antecedência.
- Troca emergencial de professor não altera a versão: é uma substituição registrada, com data e motivo.

##### 4.4 Consultas

| Consulta | Quem vê |
|---|---|
| Horário da turma | Turma: aluno e responsáveis. Professor da turma. Coordenação |
| Horário do professor | O próprio professor. Coordenação e secretaria |
| Horário da semana da unidade | Gestão, coordenação e secretaria |
| Ocupação de sala | Gestão, coordenação e secretaria ([44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md)) |

---

#### 5. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelo de grupo de horários, sem dado | Ver turma ou grade de entidade | P |
| **Gestão** | Aprovar grade, abrir e encerrar turma, ver ocupação da unidade | Alterar grade publicada sem nova versão | E |
| **Coordenação** | Montar turmas, enturmar, montar e publicar grade, autorizar troca de professor | Publicar grade com conflito | E |
| **Secretaria** | Enturmar com autorização, cadastrar sala de referência, consultar grade | Criar turma ou aula | E |
| **Professor** | Ver o próprio horário e o horário das turmas em que leciona. Pedir troca de aula | Alterar grade. Ver horário de outro professor | E |
| **Aluno** | Ver o horário da turma | Ver horário de outra turma | E |
| **Responsáveis** | Ver o horário da turma do dependente | Ver horário de outra turma | E, só dependentes com vínculo ativo |
| **Terceiros** | Nada | Qualquer item do horário | E |

---

#### 6. Integrações

| Módulo | Relação |
|---|---|
| Estrutura acadêmica ([59](../../../docs/v2/59-estrutura-academica-por-portal.md)) | Turma aponta para curso, grade e versão |
| Calendário ([58](../../../docs/v2/58-calendario-e-eventos-por-portal.md)) | Dia letivo e período |
| Matrícula ([46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md)) | Enturmação e vaga |
| Agendamento ([44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md)) | Sala de cada aula e conflito de ambiente |
| Aula online ([40](../../../docs/v2/40-aulas-online-por-portal.md)) | Aula com sala virtual |
| Carga docente ([37](../../../docs/v2/37-planejamento-e-empenho.md)) | Limite de 40 horas-aula por semana |
| Diário ([55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), item 4) | Chamada e nota pertencem à turma e à aula |
| Notificações ([57](../../../docs/v2/57-notificacoes-por-portal.md)) | Aviso de mudança de horário |

---

#### 7. Pendências

| # | Pendência | Tipo |
|---|---|---|
| TUR-01 | Teto de 40 horas-aula por professor na grade | **Decidido** em 03/11/2026: vale como aviso na grade, não bloqueio. A unidade ajusta o valor |
| TUR-02 | Turno de aula integral e de EAD | **Decidido** em 03/11/2026: integral é turno próprio. EAD não tem turno físico, só sala virtual |
| TUR-03 | Aviso de mudança de grupo de horários em turma em andamento | **Decidido** em 03/11/2026: 5 dias úteis de antecedência |
| TUR-04 | Carga horária mínima de aula e de intervalo, por nível de ensino | **Conferido** em parte em 03/11/2026: pelo menos 4 horas diárias de aula efetiva no fundamental, salvo noturno (LDB, art. 34); 4 horas no parcial e 7 no integral na educação infantil (art. 31, III). A LDB não trata de intervalo: regra do sistema de ensino ou da escola **(verificar)** |
| TUR-05 | DDL das tabelas: turma, enturmação, grupo de horários, aula, grade publicada e substituição. Cadastro de sala usa `recursos` de [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 8 | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 15.4. Revisão do owner pendente (DDL-01). Sala usa `recursos` da seção 8 |

---

#### 8. Critérios de aceite

- [ ] Grade com conflito de professor, turma ou ambiente não é salva (teste).
- [ ] Aula em dia não letivo é recusada (teste de integração com [58](../../../docs/v2/58-calendario-e-eventos-por-portal.md)).
- [ ] Enturmação acima da capacidade vai para lista de espera (teste).
- [ ] Turma com aluno que precisa de acessibilidade não é alocada em sala sem ela (teste).
- [ ] Sala em manutenção não recebe aula nova (teste).
- [ ] Grade publicada não muda sem nova versão (teste).
- [ ] Professor não vê horário de outro professor (teste de isolamento).
- [ ] Troca emergencial de professor é registrada sem nova versão de grade (teste).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).
