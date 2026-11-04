# 58 — Calendário Escolar e Eventos, por Portal

> Parte do [SDD v2](00-README.md). Decidido em 03/11/2026: o módulo entra nesta versão, como módulo próprio (CFG-01 e decisão de calendário em [56](56-configuracoes-e-relatorios-lacunas.md)). Períodos letivos e enturmação em [55](55-academico-verificacao-e-lacunas.md). Reserva de ambiente em [44](44-agendamento-ambientes-equipamentos.md). Inscrição por formulário em [41](41-formularios-e-pesquisas.md). Público por targeting em [57](57-notificacoes-por-portal.md), seção 3.4. Certificado de evento em [53](53-pacote-documentos-e-contratos.md), DC-19. Eventos pastorais em [43](43-pastoral-por-portal.md). Reunião de pais 1:1 em [40](40-aulas-online-por-portal.md). Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna de calendário e eventos. Itens **(verificar)** e **[Decisão do autor]** são indicados onde aparecem.

---

## 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Existe especificação de calendário na v2? | **Não.** Só citado em [44](44-agendamento-ambientes-equipamentos.md) e [51](51-ddl-modulos-novos.md) |
| Eventos escolares têm regra? | **Só em partes.** Pastoral em [43](43-pastoral-por-portal.md), reunião 1:1 em [40](40-aulas-online-por-portal.md) |
| Feriado e recesso bloqueiam aula e reserva? | **Não especificado.** Tratado só como bloqueio em [44](44-agendamento-ambientes-equipamentos.md) |

---

## 2. Escopo

Entram:

- Calendário letivo por unidade: períodos, dias letivos, recessos e feriados.
- Calendário por turma, derivado do calendário da unidade.
- Eventos escolares: festividades, feiras, reuniões de pais coletivas, jogos internos, formaturas e outros eventos da unidade.
- Inscrição em evento, com capacidade e prazo.
- Certificado de participação em evento.
- Agenda pública de eventos para os portais.

Não entram:

- Agenda pessoal de cada usuário (CFG-01).
- Eventos pastorais, que seguem [43](43-pastoral-por-portal.md), mas aparecem no mesmo calendário da unidade.
- Reunião 1:1 com responsável, que segue [40](40-aulas-online-por-portal.md).

---

## 3. Entidades

| Entidade | Função |
|---|---|
| Calendário letivo | Ano ou semestre da unidade, com períodos e dias letivos |
| Período letivo | Bimestre, trimestre, semestre ou módulo, com datas de início e fim |
| Dia não letivo | Feriado, recesso, ponto facultativo ou dia de planejamento |
| Evento | Ocorrência com data, horário, local, público e responsável |
| Inscrição | Participação de pessoa em evento, por formulário ([41](41-formularios-e-pesquisas.md)) |
| Certificado | Documento de participação, sem valor de documento oficial ([53](53-pacote-documentos-e-contratos.md), DC-19) |

---

## 4. Regras do calendário

1. **Calendário letivo é da unidade.** Cada unidade tem o seu, dentro do calendário da entidade.
2. **Dia não letivo bloqueia aula e reserva.** Aula não pode ser agendada em dia não letivo. Reserva de ambiente também é bloqueada ([44](44-agendamento-ambientes-equipamentos.md), seção 3.2), salvo evento que o próprio calendário autorize.
3. **Mudança de calendário após início do período** exige aprovação da diretoria, da coordenação pedagógica ou da secretaria, conforme o fluxo configurado pela entidade. Gera aviso aos envolvidos e recalcula o calendário da turma. Aulas já dadas não são alteradas.
4. **Calendário por turma** é derivado do calendário da unidade, mais os eventos que atingem a turma. Não é cópia editável.
5. **Feriado nacional, estadual ou municipal** entra por três caminhos: cadastro pela secretaria, importação de site oficial ou cadastro assistido por IA. Em todos, a fonte fica registrada, e a pessoa confirma antes de salvar, como em [27](27-inteligencia-artificial-e-portais.md). Feriado municipal pode não se aplicar à unidade, por configuração.
6. **Recesso e férias escolares** ficam a critério do sistema de ensino e da escola. A LDB não fixa recesso nem férias. O calendário se adapta às peculiaridades locais, inclusive climáticas e econômicas, sem reduzir as horas letivas (art. 23, § 2º). Na escola do campo, acompanha o ciclo agrícola (art. 28, II). Ao publicar o calendário, o sistema confere o mínimo de 200 dias letivos e as horas do nível ([59](59-estrutura-academica-por-portal.md), seção 2). Conferido em 03/11/2026 no texto da LDB (Lei 9.394/1996, planalto.gov.br) (CAL-01).

---

## 5. Eventos

### 5.1 Estados

`rascunho` → `publicado` → `em_andamento` → `encerrado`, com `cancelado` a partir de `rascunho` ou `publicado`.

- Evento publicado não muda data nem local sem aviso aos inscritos.
- Cancelamento exige motivo e gera aviso pelo canal de [57](57-notificacoes-por-portal.md).
- Evento encerrado não recebe inscrição.

### 5.2 Regras

| Regra | Detalhe |
|---|---|
| Local | Reserva de ambiente pelo módulo de [44](44-agendamento-ambientes-equipamentos.md), com prioridade de evento (3) |
| Público | Definido por targeting de [57](57-notificacoes-por-portal.md), seção 3.4. Nunca lista aberta |
| Inscrição | Por formulário de [41](41-formularios-e-pesquisas.md). Capacidade e prazo definidos pelo evento |
| Capacidade | Inscrição acima da capacidade vai para lista de espera |
| Menor de idade | Participação de menor exige autorização do responsável, como em [43](43-pastoral-por-portal.md), seção 6 |
| Custo | Evento com custo gera cobrança pelo financeiro ([18](18-regras-modulos-2.md)). Sem cobrança, não gera |
| Certificado | Emitido para quem tiver presença registrada. Presença de evento segue o registro próprio do evento |

### 5.3 Tipos de evento

| Tipo | Exemplo | Regra específica |
|---|---|---|
| Festividade | Festa junina, dia da família | Público amplo, sem inscrição |
| Feira | Feira de ciências | Inscrição de expositor, com avaliação por formulário |
| Reunião coletiva | Reunião de pais por série | Público por série, com confirmação de presença |
| Esportivo | Jogos internos | Inscrição de equipe, com ambiente reservado |
| Formatura | Formatura de turma | Convite a responsáveis, com ambiente reservado |
| Pastoral | Missa, celebração, encontro | Regras de [43](43-pastoral-por-portal.md) |

---

## 6. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelos de calendário-padrão, sem dado | Ver calendário ou evento de entidade | P |
| **Gestão** | Definir calendário letivo, feriados, recesso e eventos da unidade. Aprovar evento com público acima de 500 ([57](57-notificacoes-por-portal.md), seção 3.4) | Alterar calendário de outra unidade | E |
| **Secretaria** | Cadastrar períodos, dias não letivos, eventos e inscrições. Emitir certificado | Publicar evento sem aprovação da gestão, quando o evento exigir | E |
| **Coordenação** | Criar evento pedagógico da unidade, como reunião de pais e conselho | Criar evento fora da unidade | E |
| **Professor** | Ver calendário das próprias turmas. Propor evento da turma para a coordenação | Publicar evento sem aprovação | E |
| **Aluno** | Ver calendário e eventos das próprias turmas. Inscrever-se onde houver inscrição aberta | Ver inscrição de colega | E |
| **Responsáveis** | Ver calendário e eventos dos dependentes. Inscrever dependente, com autorização | Ver inscrição de outra família | E, só dependentes com vínculo ativo |
| **Terceiros** | Ver o evento do próprio contrato, como buffet ou som ([38](38-portal-de-terceiros-prestadores.md)) | Ver público, inscrição ou calendário de turma | E |

---

## 7. Integrações

| Módulo | Relação |
|---|---|
| Acadêmico ([55](55-academico-verificacao-e-lacunas.md)) | Períodos letivos e enturmação dependem do calendário |
| Agendamento ([44](44-agendamento-ambientes-equipamentos.md)) | Dia não letivo bloqueia reserva. Evento reserva ambiente |
| Formulários ([41](41-formularios-e-pesquisas.md)) | Inscrição e pesquisa de satisfação |
| Notificações ([57](57-notificacoes-por-portal.md)) | Aviso de evento, cancelamento e lembrete |
| Documentos ([48](48-gerador-de-documentos-por-portal.md)) | Certificado de participação |
| Financeiro ([18](18-regras-modulos-2.md)) | Cobrança de evento com custo |
| Pastoral ([43](43-pastoral-por-portal.md)) | Eventos pastorais no mesmo calendário |

---

## 8. Pendências

| # | Pendência | Tipo |
|---|---|---|
| CAL-01 | Recesso e férias escolares: regra da legislação do sistema de ensino (regra 6) | **Conferido** em 03/11/2026: LDB, art. 23, § 2º, e art. 28, II. Não há prazo fixo de recesso na lei. Calendário configurável pela escola |
| CAL-02 | Carga de feriados nacionais, estaduais e municipais | **Decidido** em 03/11/2026: três formas de cadastro: pela secretaria, por importação de site oficial e por cadastro assistido por IA. Em todas, a fonte é registrada e a pessoa confirma antes de salvar |
| CAL-03 | Mudança de calendário após o início do período | **Decidido** em 03/11/2026: aprovação pela diretoria, pela coordenação pedagógica e pela secretaria, com fluxo configurável pela entidade |
| CAL-04 | Certificado de evento: prazo de guarda | (jurídico) |
| CAL-05 | DDL das tabelas de calendário, período, dia não letivo, evento, inscrição e certificado | **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.2. Revisão do owner pendente (DDL-01) |

---

## 9. Critérios de aceite

- [ ] Aula não pode ser agendada em dia não letivo (teste).
- [ ] Reserva de ambiente é recusada em dia não letivo, salvo evento que o autorize (teste de integração com [44](44-agendamento-ambientes-equipamentos.md)).
- [ ] Calendário da turma muda quando o da unidade muda, e aulas já dadas não mudam (teste).
- [ ] Evento com público fora do targeting permitido é recusado (teste de isolamento).
- [ ] Inscrição acima da capacidade vai para lista de espera (teste).
- [ ] Certificado só é emitido para presença registrada (teste).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
