# Calendário e eventos

- Portal: Gestão (`gestao.`)
- Área: Acadêmico
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [58](../../../docs/v2/58-calendario-e-eventos-por-portal.md) (integral)
- Fonte da v1: sem especificação própria; valem as regras do SDD v2 (seção 13)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Definir o calendário letivo da unidade (dias letivos, feriados, recesso, períodos) e os eventos escolares com inscrição, presença e certificado.

## 3. Telas

- **Calendário letivo** (calendário mensal e anual): dias letivos, não letivos, feriados e recesso; contador de dias letivos por período; publicar.
- **Eventos** (lista e calendário): título, tipo, público, local, inscrição, estado; kanban por estado.
- **Evento — formulário** (página): tipo (seção 13), público-alvo, limite de vagas, inscrição, aprovação exigida, recurso agendado ([44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md)).
- **Inscrições e presença** (DataTable por evento): inscritos, autorização de responsável para menor, check-in, emissão de certificado.
- **Aprovações** (fila): eventos que exigem aprovação da gestão (público acima de 500, seção 13).

## 4. Permissões por portal (extraídas do SDD)

Do [58](../../../docs/v2/58-calendario-e-eventos-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Definir calendário letivo, feriados, recesso e eventos da unidade. Aprovar evento com público acima de 500 ([57](../../../docs/v2/57-notificacoes-por-portal.md), seção 3.4) | Alterar calendário de outra unidade | E |
| **Secretaria** | Cadastrar períodos, dias não letivos, eventos e inscrições. Emitir certificado | Publicar evento sem aprovação da gestão, quando o evento exigir | E |
| **Coordenação** | Criar evento pedagógico da unidade, como reunião de pais e conselho | Criar evento fora da unidade | E |

## 5. Papéis

- `unit.manager`: definir calendário, aprovar evento.
- `unit.secretary`: períodos, dias não letivos, eventos e inscrições; emitir certificado.
- `unit.coordinator`: eventos pedagógicos (reunião de pais, conselho).
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Evento só é publicado depois da aprovação da gestão quando o tipo exigir.
- Calendário de uma unidade não altera o de outra.
- Mudança de data publicada gera notificação ([57](../../../docs/v2/57-notificacoes-por-portal.md)).

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

### 13.1 [58 — Calendário Escolar e Eventos, por Portal](../../../docs/v2/58-calendario-e-eventos-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Decidido em 03/11/2026: o módulo entra nesta versão, como módulo próprio (CFG-01 e decisão de calendário em [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md)). Períodos letivos e enturmação em [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md). Reserva de ambiente em [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md). Inscrição por formulário em [41](../../../docs/v2/41-formularios-e-pesquisas.md). Público por targeting em [57](../../../docs/v2/57-notificacoes-por-portal.md), seção 3.4. Certificado de evento em [53](../../../docs/v2/53-pacote-documentos-e-contratos.md), DC-19. Eventos pastorais em [43](../../../docs/v2/43-pastoral-por-portal.md). Reunião de pais 1:1 em [40](../../../docs/v2/40-aulas-online-por-portal.md). Auditoria em [29](../../../docs/v2/29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna de calendário e eventos. Itens **(verificar)** e **[Decisão do autor]** são indicados onde aparecem.

---

#### 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Existe especificação de calendário na v2? | **Não.** Só citado em [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md) e [51](../../../docs/v2/51-ddl-modulos-novos.md) |
| Eventos escolares têm regra? | **Só em partes.** Pastoral em [43](../../../docs/v2/43-pastoral-por-portal.md), reunião 1:1 em [40](../../../docs/v2/40-aulas-online-por-portal.md) |
| Feriado e recesso bloqueiam aula e reserva? | **Não especificado.** Tratado só como bloqueio em [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md) |

---

#### 2. Escopo

Entram:

- Calendário letivo por unidade: períodos, dias letivos, recessos e feriados.
- Calendário por turma, derivado do calendário da unidade.
- Eventos escolares: festividades, feiras, reuniões de pais coletivas, jogos internos, formaturas e outros eventos da unidade.
- Inscrição em evento, com capacidade e prazo.
- Certificado de participação em evento.
- Agenda pública de eventos para os portais.

Não entram:

- Agenda pessoal de cada usuário (CFG-01).
- Eventos pastorais, que seguem [43](../../../docs/v2/43-pastoral-por-portal.md), mas aparecem no mesmo calendário da unidade.
- Reunião 1:1 com responsável, que segue [40](../../../docs/v2/40-aulas-online-por-portal.md).

---

#### 3. Entidades

| Entidade | Função |
|---|---|
| Calendário letivo | Ano ou semestre da unidade, com períodos e dias letivos |
| Período letivo | Bimestre, trimestre, semestre ou módulo, com datas de início e fim |
| Dia não letivo | Feriado, recesso, ponto facultativo ou dia de planejamento |
| Evento | Ocorrência com data, horário, local, público e responsável |
| Inscrição | Participação de pessoa em evento, por formulário ([41](../../../docs/v2/41-formularios-e-pesquisas.md)) |
| Certificado | Documento de participação, sem valor de documento oficial ([53](../../../docs/v2/53-pacote-documentos-e-contratos.md), DC-19) |

---

#### 4. Regras do calendário

1. **Calendário letivo é da unidade.** Cada unidade tem o seu, dentro do calendário da entidade.
2. **Dia não letivo bloqueia aula e reserva.** Aula não pode ser agendada em dia não letivo. Reserva de ambiente também é bloqueada ([44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md), seção 3.2), salvo evento que o próprio calendário autorize.
3. **Mudança de calendário após início do período** exige aprovação da diretoria, da coordenação pedagógica ou da secretaria, conforme o fluxo configurado pela entidade. Gera aviso aos envolvidos e recalcula o calendário da turma. Aulas já dadas não são alteradas.
4. **Calendário por turma** é derivado do calendário da unidade, mais os eventos que atingem a turma. Não é cópia editável.
5. **Feriado nacional, estadual ou municipal** entra por três caminhos: cadastro pela secretaria, importação de site oficial ou cadastro assistido por IA. Em todos, a fonte fica registrada, e a pessoa confirma antes de salvar, como em [27](../../../docs/v2/27-inteligencia-artificial-e-portais.md). Feriado municipal pode não se aplicar à unidade, por configuração.
6. **Recesso e férias escolares** ficam a critério do sistema de ensino e da escola. A LDB não fixa recesso nem férias. O calendário se adapta às peculiaridades locais, inclusive climáticas e econômicas, sem reduzir as horas letivas (art. 23, § 2º). Na escola do campo, acompanha o ciclo agrícola (art. 28, II). Ao publicar o calendário, o sistema confere o mínimo de 200 dias letivos e as horas do nível ([59](../../../docs/v2/59-estrutura-academica-por-portal.md), seção 2). Conferido em 03/11/2026 no texto da LDB (Lei 9.394/1996, planalto.gov.br) (CAL-01).

---

#### 5. Eventos

##### 5.1 Estados

`rascunho` → `publicado` → `em_andamento` → `encerrado`, com `cancelado` a partir de `rascunho` ou `publicado`.

- Evento publicado não muda data nem local sem aviso aos inscritos.
- Cancelamento exige motivo e gera aviso pelo canal de [57](../../../docs/v2/57-notificacoes-por-portal.md).
- Evento encerrado não recebe inscrição.

##### 5.2 Regras

| Regra | Detalhe |
|---|---|
| Local | Reserva de ambiente pelo módulo de [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md), com prioridade de evento (3) |
| Público | Definido por targeting de [57](../../../docs/v2/57-notificacoes-por-portal.md), seção 3.4. Nunca lista aberta |
| Inscrição | Por formulário de [41](../../../docs/v2/41-formularios-e-pesquisas.md). Capacidade e prazo definidos pelo evento |
| Capacidade | Inscrição acima da capacidade vai para lista de espera |
| Menor de idade | Participação de menor exige autorização do responsável, como em [43](../../../docs/v2/43-pastoral-por-portal.md), seção 6 |
| Custo | Evento com custo gera cobrança pelo financeiro ([18](../../../docs/v2/18-regras-modulos-2.md)). Sem cobrança, não gera |
| Certificado | Emitido para quem tiver presença registrada. Presença de evento segue o registro próprio do evento |

##### 5.3 Tipos de evento

| Tipo | Exemplo | Regra específica |
|---|---|---|
| Festividade | Festa junina, dia da família | Público amplo, sem inscrição |
| Feira | Feira de ciências | Inscrição de expositor, com avaliação por formulário |
| Reunião coletiva | Reunião de pais por série | Público por série, com confirmação de presença |
| Esportivo | Jogos internos | Inscrição de equipe, com ambiente reservado |
| Formatura | Formatura de turma | Convite a responsáveis, com ambiente reservado |
| Pastoral | Missa, celebração, encontro | Regras de [43](../../../docs/v2/43-pastoral-por-portal.md) |

---

#### 6. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Publicar modelos de calendário-padrão, sem dado | Ver calendário ou evento de entidade | P |
| **Gestão** | Definir calendário letivo, feriados, recesso e eventos da unidade. Aprovar evento com público acima de 500 ([57](../../../docs/v2/57-notificacoes-por-portal.md), seção 3.4) | Alterar calendário de outra unidade | E |
| **Secretaria** | Cadastrar períodos, dias não letivos, eventos e inscrições. Emitir certificado | Publicar evento sem aprovação da gestão, quando o evento exigir | E |
| **Coordenação** | Criar evento pedagógico da unidade, como reunião de pais e conselho | Criar evento fora da unidade | E |
| **Professor** | Ver calendário das próprias turmas. Propor evento da turma para a coordenação | Publicar evento sem aprovação | E |
| **Aluno** | Ver calendário e eventos das próprias turmas. Inscrever-se onde houver inscrição aberta | Ver inscrição de colega | E |
| **Responsáveis** | Ver calendário e eventos dos dependentes. Inscrever dependente, com autorização | Ver inscrição de outra família | E, só dependentes com vínculo ativo |
| **Terceiros** | Ver o evento do próprio contrato, como buffet ou som ([38](../../../docs/v2/38-portal-de-terceiros-prestadores.md)) | Ver público, inscrição ou calendário de turma | E |

---

#### 7. Integrações

| Módulo | Relação |
|---|---|
| Acadêmico ([55](../../../docs/v2/55-academico-verificacao-e-lacunas.md)) | Períodos letivos e enturmação dependem do calendário |
| Agendamento ([44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md)) | Dia não letivo bloqueia reserva. Evento reserva ambiente |
| Formulários ([41](../../../docs/v2/41-formularios-e-pesquisas.md)) | Inscrição e pesquisa de satisfação |
| Notificações ([57](../../../docs/v2/57-notificacoes-por-portal.md)) | Aviso de evento, cancelamento e lembrete |
| Documentos ([48](../../../docs/v2/48-gerador-de-documentos-por-portal.md)) | Certificado de participação |
| Financeiro ([18](../../../docs/v2/18-regras-modulos-2.md)) | Cobrança de evento com custo |
| Pastoral ([43](../../../docs/v2/43-pastoral-por-portal.md)) | Eventos pastorais no mesmo calendário |

---

#### 8. Pendências

| # | Pendência | Tipo |
|---|---|---|
| CAL-01 | Recesso e férias escolares: regra da legislação do sistema de ensino (regra 6) | **Conferido** em 03/11/2026: LDB, art. 23, § 2º, e art. 28, II. Não há prazo fixo de recesso na lei. Calendário configurável pela escola |
| CAL-02 | Carga de feriados nacionais, estaduais e municipais | **Decidido** em 03/11/2026: três formas de cadastro: pela secretaria, por importação de site oficial e por cadastro assistido por IA. Em todas, a fonte é registrada e a pessoa confirma antes de salvar |
| CAL-03 | Mudança de calendário após o início do período | **Decidido** em 03/11/2026: aprovação pela diretoria, pela coordenação pedagógica e pela secretaria, com fluxo configurável pela entidade |
| CAL-04 | Certificado de evento: prazo de guarda | (jurídico) |
| CAL-05 | DDL das tabelas de calendário, período, dia não letivo, evento, inscrição e certificado | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 15.2. Revisão do owner pendente (DDL-01) |

---

#### 9. Critérios de aceite

- [ ] Aula não pode ser agendada em dia não letivo (teste).
- [ ] Reserva de ambiente é recusada em dia não letivo, salvo evento que o autorize (teste de integração com [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md)).
- [ ] Calendário da turma muda quando o da unidade muda, e aulas já dadas não mudam (teste).
- [ ] Evento com público fora do targeting permitido é recusado (teste de isolamento).
- [ ] Inscrição acima da capacidade vai para lista de espera (teste).
- [ ] Certificado só é emitido para presença registrada (teste).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).
