# 44 — Agendamento de Ambientes e Equipamentos, por Portal (Acadêmico)

> Parte do [SDD v2](00-README.md). Turmas em [17](17-regras-modulos.md). Aulas online, que não ocupam ambiente físico, em [40](40-aulas-online-por-portal.md). Equipamento como bem patrimonial em [19](19-regras-modulos-3.md), seção 8. Chamados de manutenção em [36](36-tecnologia-da-informacao-por-portal.md). Matriz de portais em [31](31-matriz-portais-modulos.md). Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. A v1 tem "Agendamento Espaços PRO" (laboratórios, quadras, auditórios, salas multimídia, termos de uso) só como item de navegação, em `12-portals-navigation-sidebar-pages-spec.md`, seção 4.2. Não há especificação, DDL nem regra de conflito. Itens **[Decisão do autor]** dependem de resposta.

---

## 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| Há gestão de agendamento de ambientes na v2? | **Não.** Só aparece "reserva de laboratório" como exemplo de pedido no portal do professor ([31](31-matriz-portais-modulos.md), seção 2) |
| Há gestão de equipamentos? | **Não.** Equipamento não é reservável em nenhum documento |
| Há regra de conflito? | **Não.** Dois professores podem reservar a mesma sala no mesmo horário |
| Liga com a grade horária? | **Não.** A aula da grade e a reserva avulsa são tratadas como coisas separadas, quando deveriam competir pelo mesmo ambiente |

---

## 2. Recursos

### 2.1 Ambientes

| Tipo | Exemplos | Atributos |
|---|---|---|
| Sala de aula | Sala 12, sala 3º ano | Capacidade, recursos fixos (projetor, quadro, ar-condicionado), andar |
| Laboratório | Ciências, informática, robótica | Capacidade, bancadas, equipamentos fixos, exigência de responsável técnico |
| Espaço esportivo | Quadra, campo | Capacidade, horário de uso permitido, bloqueio por chuva |
| Auditório e salão | Auditório, salão de eventos, capela | Capacidade, palco, uso para evento externo |
| Sala de reunião e de atendimento | Sala de reunião, sala de tutoria, sala de atendimento | Capacidade, privacidade |
| Biblioteca | Sala de estudo em grupo | Regra da biblioteca ([17](17-regras-modulos.md)) |

### 2.2 Equipamentos

| Tipo | Exemplos | Regra |
|---|---|---|
| Móvel e portátil | Notebook, tablet, projetor portátil, caixa de som, câmera | Reservável por unidade. Retirada com termo de responsabilidade |
| Kit | Kit de microscópio com 10 peças, kit robótica | Reservado como um item. Peças conferidas na devolução |
| Fixo | Lousa digital, projetor de sala | Não reservável. Aparece só como recurso do ambiente |

Equipamento reservável é um bem patrimonial. O cadastro é o mesmo do patrimônio ([19](19-regras-modulos-3.md), seção 8), com a marca "reservável". Não se cria um segundo cadastro de equipamento. Equipamento de TI segue [36](36-tecnologia-da-informacao-por-portal.md).

### 2.3 Finalidade da reserva

| Origem | Prioridade | Exemplo |
|---|---|---|
| Grade horária (aula) | 1. Fixa, não cancelável por reserva | Aula do 3º ano B na sala 12, segunda, 7h30 |
| Prova e simulado | 2 | Prova de recuperação, simulado ENEM |
| Evento institucional | 3 | Feira de ciências, formatura |
| Pastoral ([43](43-pastoral-por-portal.md)) | 3 | Missa na capela |
| Preceptoria e tutoria ([42](42-preceptoria-por-portal.md)) | 4 | Sala de tutoria |
| Reunião administrativa | 4 | Reunião de coordenação |
| Uso avulso de professor ou responsável | 5 | Grupo de estudo, ensaio, agendamento liberado pela gestão |

Prioridade só decide conflito entre reservas em aberto. Reserva de prioridade menor não é cancelada automaticamente. A regra é de aviso e de remanejamento, com aprovação.

---

## 3. Reserva

### 3.1 Estados

`solicitada` → `aprovada` → `em_uso` → `concluida`, com `recusada`, `cancelada` e `nao_utilizada` como saídas.

- `nao_utilizada`: reserva aprovada sem check-in até **15 minutos** depois do início. Libera o ambiente automaticamente. Valor de 15 minutos, configurável por unidade. Decidido pelo autor em 03/11/2026
- Check-in e check-out são feitos pelo responsável da reserva, no portal.

### 3.2 Regras

| Regra | Detalhe |
|---|---|
| Aprovação | Professor reserva direto, sem aprovação, se o ambiente estiver livre e dentro do limite. Responsável reserva só ambiente liberado pela gestão. Só a gestão cancela reserva de outra pessoa. Decidido pelo autor em 03/11/2026 |
| Sem sobreposição | Duas reservas aprovadas não ocupam o mesmo ambiente no mesmo horário. Checagem dentro de transação, com bloqueio do registro do ambiente, porque MySQL não tem restrição de sobreposição de intervalo |
| Grade horária | Horário de aula é bloqueio fixo. Reserva avulsa não cabe nele |
| Capacidade | Número de participantes não passa a capacidade do ambiente |
| Antecedência | Solicitação com antecedência mínima por tipo. Decidido em 03/11/2026: 50 minutos, configurável por unidade |
| Limite | Sem limite semanal de reservas avulsas de professor. Decidido pelo autor em 03/11/2026 |
| Recorrência | Reserva semanal, com exceções. Cada ocorrência é reservada separadamente, e conflito em uma não cancela as outras |
| Fuso | Horário em UTC no banco, exibido no fuso da unidade |
| Bloqueio | Manutenção, feriado, chuva e uso institucional bloqueiam o ambiente. Bloqueio aparece na checagem de conflito |
| Cancelamento | Pelo responsável ou pela gestão, com motivo. Cancelamento de reserva aprovada menos de 24 h antes exige aprovação da gestão. Decidido pelo autor em 03/11/2026 |

### 3.3 Equipamento

| Regra | Detalhe |
|---|---|
| Retirada | Termo de responsabilidade aceito no portal. Data, item e responsável |
| Devolução | Conferência de estado e de peças. Problema gera chamado de manutenção ([36](36-tecnologia-da-informacao-por-portal.md)) |
| Atraso | Após o prazo, aviso ao responsável. Sem bloqueio automático de conta de aluno |
| Equipamento em manutenção | Bloqueado para reserva, com motivo e data prevista |
| Vínculo com ambiente | Equipamento pode ser reservado junto com o ambiente (ex.: projetor portátil para sala sem projetor fixo) |

---

## 4. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Nada sobre ambiente de entidade | Ver reserva de qualquer entidade | P |
| **Gestão** | Cadastrar ambiente e equipamento, definir regra de antecedência, liberar ambientes para responsáveis, cancelar qualquer reserva, ver ocupação, aplicar bloqueio | Alterar grade horária sem passar pelo módulo de grade | E |
| **Professor** | Ver ambientes e equipamentos da unidade. Agendar e reservar ambiente e equipamento para a própria turma e para uso próprio, dentro do limite. Retirar equipamento. Ver a própria reserva e a agenda do ambiente | Reservar ambiente de aula de outra turma. Cancelar reserva de outro professor | E |
| **Aluno** | Ver a agenda pública dos ambientes. Não reserva nenhum ambiente nem equipamento | Reservar qualquer ambiente ou equipamento | E |
| **Responsáveis** | Agendar somente os ambientes que a gestão liberou para eles. Ver a própria reserva | Reservar ambiente não liberado. Reservar equipamento. Ver reserva de outra pessoa | E |
| **Terceiros** | Fornecedor de evento vê a reserva do evento e o ambiente reservado, sem agenda de aulas | Ver agenda de turma, aluno ou professor | E, pelo contrato em [38](38-portal-de-terceiros-prestadores.md) |

---

## 5. Integrações

| Módulo | Relação |
|---|---|
| Grade horária ([17](17-regras-modulos.md)) | Aula é bloqueio fixo. Mudança de grade gera reserva de remanejamento |
| Simulados ([31](31-matriz-portais-modulos.md)) | Prova presencial reserva sala e pode reservar equipamento |
| Pastoral ([43](43-pastoral-por-portal.md)) | Missa e evento em capela, auditório e pátio |
| Preceptoria ([42](42-preceptoria-por-portal.md)) | Sala de tutoria e de avaliação prática |
| Patrimônio e TI ([19](19-regras-modulos-3.md), seção 8; [36](36-tecnologia-da-informacao-por-portal.md)) | Equipamento é o mesmo bem. Manutenção gera chamado |
| Eventos ([17](17-regras-modulos.md)) | Feira, formatura e reunião de pais reservam ambiente pelo mesmo motor |
| Aulas online ([40](40-aulas-online-por-portal.md)) | Não reserva ambiente físico. A sala virtual é separada |

---

## 6. Modelo de dados proposto

Não é o DDL final. Horários em UTC, `utf8mb4`.

| Tabela | Campos principais |
|---|---|
| `recursos` | `uuid`, `unidade_uuid`, `tipo` (ambiente, equipamento, kit), `nome`, `capacidade`, `reservavel`, `estado` (ativo, manutencao, inativo), `patrimonio_uuid` (quando for bem) |
| `recurso_composicao` | `kit_uuid`, `item_uuid`, `quantidade`. Liga kit a peças |
| `reservas` | `uuid`, `unidade_uuid`, `origem_tipo`, `origem_uuid`, `solicitante_uuid`, `inicio_utc`, `fim_utc`, `estado`, `prioridade`, `motivo_cancelamento` |
| `reserva_recursos` | `reserva_id`, `recurso_id`, `quantidade`, `retirada_em`, `devolucao_em`, `estado_devolucao` |
| `bloqueios` | `recurso_id`, `inicio_utc`, `fim_utc`, `motivo` (manutencao, feriado, uso_institucional) |

Verificação de conflito: consulta de `reservas` aprovadas e `bloqueios` sobrepostos ao intervalo, dentro de transação com bloqueio do registro de `recursos`.

---

## 7. Pendências

| # | Pendência | Tipo |
|---|---|---|
| AMB-01 | Tempo de `nao_utilizada`: 15 min (seção 3.1) | **Decidido** em 03/11/2026 |
| AMB-02 | Antecedência mínima: 50 minutos, configurável por unidade (seção 3.2) | **Decidido** em 03/11/2026 |
| AMB-03 | Aluno reservar: não reserva. Professor reserva direto; responsável reserva só o que for liberado (seção 4) | **Decidido** em 03/11/2026 |
| AMB-04 | Limite semanal de reserva avulsa de professor | **Decidido** em 03/11/2026: sem limite. Conflito e antecedência continuam valendo |
| AMB-05 | Cancelamento com menos de 24 h: aprovação da gestão (seção 3.2) | **Decidido** em 03/11/2026: sim, exige aprovação |
| AMB-06 | Termo de responsabilidade de equipamento: texto e guarda | (jurídico) |
| AMB-07 | Regra de uso de espaço esportivo por menor fora do horário escolar | (jurídico) |
| AMB-08 | DDL das tabelas da seção 6, com teste de conflito concorrente | **Escrito** em [51](51-ddl-modulos-novos.md), seção 8. Revisão do owner pendente (DDL-01) |

---

## 8. Critérios de aceite

- [ ] Duas reservas aprovadas não ocupam o mesmo ambiente no mesmo horário, mesmo em solicitações simultâneas (teste de concorrência).
- [ ] Reserva avulsa não sobrepõe horário de aula da grade (teste).
- [ ] Número de participantes não passa a capacidade do ambiente (teste).
- [ ] Reserva sem check-in libera o ambiente no tempo configurado (teste).
- [ ] Equipamento em manutenção não aceita reserva (teste).
- [ ] Equipamento reservável é o mesmo registro do patrimônio (teste de integridade).
- [ ] Professor não reserva ambiente de outra turma (teste de isolamento).
- [ ] Itens **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
