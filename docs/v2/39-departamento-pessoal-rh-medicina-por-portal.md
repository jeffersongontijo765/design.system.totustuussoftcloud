# 39 — Departamento Pessoal, Recursos Humanos e Medicina do Trabalho, por Portal

> Parte do [SDD v2](00-README.md). Regras atuais de RH e Pessoas em [17](17-regras-modulos.md), seção 3, e [18](18-regras-modulos-2.md), seção 3. Medicina e segurança em [17](17-regras-modulos.md), seção 5. Integrações e eSocial em [16](16-integracoes-externas.md), seção 6 (D-08) e em [14](14-integracao-modulos.md). Dado de saúde em [07](07-privacidade-lgpd.md), seção 2. Planejamento de desenvolvimento em [37](37-planejamento-e-empenho.md), seção 4. Prestadores em [38](38-portal-de-terceiros-prestadores.md).
> **Status:** análise e especificação proposta, criada em 03/11/2026 a partir de [`spec_gestao_pessoas_completo.md`](anexo-v1/spec_gestao_pessoas_completo.md) (1.217 linhas), [`spec_gestao_rh_completo.md`](anexo-v1/spec_gestao_rh_completo.md) e [`spec_gestao_seguranca_medicina_trabalho_completo.md`](anexo-v1/spec_gestao_seguranca_medicina_trabalho_completo.md). Itens **(verificar)** dependem de conferência de norma trabalhista, previdenciária ou de saúde. Não é parecer.

---

## 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Área | Completa? | Principal falha |
|---|---|---|
| Departamento pessoal (admissão, folha, férias, rescisão, benefícios, ponto) | **Não** | Sem regras de folha, rescisão e admissão. eSocial só cobre SST (S-2220, S-2230, S-2240), não cobre admissão, remuneração, pagamento e desligamento |
| Recursos humanos (recrutamento, onboarding, desempenho, clima, treinamento) | **Não** | Duplicidade com Pessoas (T-07) ainda sem decisão. Sem regra de recrutamento, onboarding, clima ou avaliação |
| Medicina e segurança do trabalho | **Parcial** | Regras de ASO, CAT, EPI, NR e afastamento existem ([17](17-regras-modulos.md), seção 5). Faltam PCMSO, PGR/GHE, LTCAT, CIPA e ergonomia. **Falha de privacidade:** a v1 dá ao RH e à gestão a permissão "SST — Gerenciar" e mostra CID no cadastro de exame |
| Organização por portal | **Não** | Os três assuntos aparecem em portais diferentes na v1 sem regra clara de quem vê o quê |

---

## 2. Organização: um módulo, submódulos e donos

**Decisão proposta (já registrada como T-07 em [18](18-regras-modulos-2.md)):** RH e Pessoas são **um único módulo HCM**, com estes submódulos:

| Submódulo | Dono | Banco |
|---|---|---|
| Cadastro e vínculo (colaborador, cargo, unidade, documentos) | HCM | Banco da unidade ([03](03-dominio-tenancy.md)) |
| Departamento pessoal (admissão, folha, férias, rescisão, benefícios, ponto) | HCM | Banco da unidade |
| Recursos humanos (recrutamento, onboarding, desempenho, clima, treinamento) | HCM | Banco da unidade |
| Medicina e segurança do trabalho | SST | Banco da unidade, com acesso restrito (seção 5) |

Dados civis do colaborador ficam no banco de identidade da entidade, como manda D-19 ([14](14-integracao-modulos.md), seção 3). O HCM referencia `person_id`.

---

## 3. Departamento pessoal

### 3.1 Admissão

| Etapa | Regra |
|---|---|
| Cadastro | Dados civis no banco de identidade. Dados contratuais no banco da unidade |
| Documentos | Obrigatórios por cargo. Admissão bloqueada se faltar documento ([18](18-regras-modulos-2.md), seção 3) |
| Exame admissional | Agendado pelo SST. Admissão só com ASO apto ([17](17-regras-modulos.md), seção 5) |
| Registro | Evento de admissão para o eSocial (S-2200) **(verificar)** |

### 3.2 Folha

**Estados (v2, já definidos):** `em_processamento`, `fechada`, `paga`. Folha fechada não é alterada; a correção é folha complementar ([17](17-regras-modulos.md), seção 2).

**Lacunas:**

| # | Falta | Origem |
|---|---|---|
| DP-01 | Catálogo de verbas (proventos, descontos, informativos), com natureza e incidência de INSS, FGTS e IRRF | v1, seção 9.3 |
| DP-02 | Fórmulas de cálculo versionadas, com vigência. Tabela de INSS e IRRF por competência | **(verificar)** |
| DP-03 | Processamento por competência e unidade, com pendências bloqueando o fechamento | v1, seção 9.1 |
| DP-04 | Holerite: geração, envio e registro de visualização. Holerite só para o próprio colaborador | v1, seção 9.2; [17](17-regras-modulos.md), seção 2 |
| DP-05 | Eventos eSocial de remuneração (S-1200) e de pagamento (S-1210) **(verificar)** | Ausente |

### 3.3 Férias e afastamentos

- Período aquisitivo e concessivo com cálculo de direito. **(verificar)** art. 130 da CLT e fracionamento. Pendência LAC-12 de [18](18-regras-modulos-2.md).
- Programação pelo colaborador ou gestor, com aprovação do RH.
- Afastamento com data fim não anterior ao início e sem sobreposição ([17](17-regras-modulos.md), seção 5.2).

### 3.4 Ponto e jornada

- Registro de ponto por unidade. Regras da CLT, com a redação da Lei 13.874/2019 (planalto.gov.br, Conferido em 03/11/2026):
  - O horário de trabalho é anotado em registro de empregados (art. 74, caput).
  - **Estabelecimento com mais de 20 trabalhadores:** anotação obrigatória de entrada e saída, em registro manual, mecânico ou eletrônico, conforme instruções do Ministério, com pré-assinalação do repouso permitida (art. 74, § 2º). O sistema conta os trabalhadores **por estabelecimento** e exige o registro acima de 20. Abaixo disso, o registro fica opcional por unidade.
  - Trabalho fora do estabelecimento: registro em poder do empregado (art. 74, § 3º), por exemplo no aplicativo.
  - **Ponto por exceção:** permitido por acordo individual escrito, convenção ou acordo coletivo (art. 74, § 4º). O sistema só ativa o modo por exceção com o documento do acordo anexado.
  - **Intervalos:** mínimo de 11 horas entre duas jornadas (art. 66). Intervalo de 1 a 2 horas em trabalho contínuo acima de 6 horas, salvo acordo ou contrato coletivo (art. 71, caput), e de 15 minutos quando passar de 4 horas e não exceder 6 (art. 71, § 1º). O sistema alerta a violação, não bloqueia o registro.
  - Requisitos técnicos do registro eletrônico (REP) são da Portaria MTP nº 671/2021 **(verificar)**. Regra do servidor público vem do estatuto do ente **(verificar)** por ente.
  - **Professor de escola particular** (CLT, arts. 317 a 323, texto compilado lido em 03/11/2026 no Planalto):
    - Pode dar aula em mais de um turno no mesmo estabelecimento, sem passar da jornada semanal legal, com intervalo para refeição assegurado e não contado (art. 318, Lei 13.415/2017). O sistema soma as aulas de todos os turnos do professor na unidade e alerta acima da jornada semanal do contrato.
    - Não dá aula nem trabalha em exame aos domingos (art. 319). A grade ([60](60-turmas-e-grade-de-horarios-por-portal.md)) recusa aula de professor no domingo.
    - **Remuneração por aulas semanais**, paga por mês de **quatro semanas e meia** (art. 320, § 1º). Falta desconta as aulas não dadas (§ 2º), salvo até 9 dias por casamento ou luto de cônjuge, pai, mãe ou filho (§ 3º). Aula acima do horário é paga no fim do mês (art. 321). A folha recebe do diário ([61](61-diario-escolar-por-portal.md)) as aulas dadas e as excedentes de cada mês.
    - Em exames e férias escolares, recebe a mesma remuneração do período de aulas (art. 322). Em exames, no máximo 8 horas por dia, salvo pagamento de cada hora extra pelo valor de uma aula (§ 1º). Nas férias, só serviço de exame (§ 2º). Dispensa sem justa causa no fim do ano letivo ou nas férias garante essa remuneração (§ 3º).
- Ajuste manual só por RH, com motivo e evento de auditoria ([29](29-auditoria.md)).
- Ponto fechado não é alterado sem ajuste rastreado.
- Entrada e saída pela catraca, quando houver, é fonte auxiliar, não única ([35](35-acesso-e-seguranca-fisica-por-portal.md), seção 3.4).

### 3.5 Rescisão e desligamento

**Ausente na v2.** Proposta de estados: `solicitado` → `calculado` → `homologado` (se a regra exigir) → `pago` → `encerrado`.

- Cálculo com aviso prévio, férias proporcionais, 13.º e multa do FGTS **(verificar)**.
- Evento de desligamento para o eSocial (S-2299) **(verificar)**.
- Desligamento de quem tem afastamento ativo bloqueado até a regularização.

### 3.6 Benefícios

Vale-transporte, vale-refeição e plano. Regra de desconto e de elegibilidade por cargo **(verificar)**. Benefício concedido gera evento de folha.

---

## 4. Recursos humanos

| Submódulo | Estado na v2 | Proposta mínima |
|---|---|---|
| Recrutamento | Ausente | Vaga → candidato → entrevista → aprovação → oferta. Estados por etapa. Candidato sem consentimento para guarda de currículo é descartado ao fim do prazo ([07](07-privacidade-lgpd.md)) |
| Onboarding | Ausente | Checklist de admissão por cargo, com responsável por item. Convite de acesso ao sistema com validade de 72 h ([06](06-identidade-acesso.md)) |
| Desempenho | Ausente | Ciclo, metas e avaliação. Avaliação não altera a nota de desempenho do aluno, nem a folha |
| Clima | Ausente | Pesquisa anônima. Resultado só com mínimo de respostas por grupo, para não identificar pessoa ([19](19-regras-modulos-3.md), seção 11) |
| Treinamento e desenvolvimento | Parcial | Ver [37](37-planejamento-e-empenho.md), seção 4 |
| Movimentação interna | Ausente | Transferência de unidade e de cargo, com histórico. Não apaga o histórico anterior |

---

## 5. Medicina e segurança do trabalho

### 5.1 Regra central de privacidade

**O RH e a gestão não veem diagnóstico, CID ou prontuário.** A v1 dá a eles a permissão "SST — Gerenciar" e mostra CID no cadastro de exame. Correção proposta:

| Papel | Vê | Não vê |
|---|---|---|
| Médico do trabalho | ASO completo, prontuário, CID, restrição detalhada | Nada de outros médicos sem vínculo |
| Técnico de segurança (SESMT) | Ocorrências, EPI, NR, PGR, CAT sem diagnóstico | CID, prontuário |
| RH e gestão | Apto, inapto ou apto com restrição; data de validade do ASO; restrição funcional **sem motivo clínico**; afastamento sem CID | CID, diagnóstico, prontuário |
| Colaborador | O próprio ASO e o próprio resultado | Dado de outro colaborador |
| Auditor | Acesso de leitura com motivo ([29](29-auditoria.md), seção 5) | Conteúdo de dado de saúde |

**Base:** LGPD, art. 11, e o princípio de necessidade ([07](07-privacidade-lgpd.md), seção 1). A CAT exige CID para o INSS, e isso é emitido pelo médico, não pela gestão **(verificar)**.

**Correção necessária na v1:** a permissão "SST — Gerenciar" deixa de ser concedida por nome de cargo a RH e gestão. Cada portal ou papel que precisa gerir SST recebe a sua própria permissão, limitada ao que esse papel faz (ver seção 11).

### 5.2 Exames ocupacionais (ASO)

- Tipos: admissional, periódico, retorno ao trabalho, mudança de função e demissional ([17](17-regras-modulos.md), seção 5.2).
- Vencimento calculado pelo tipo e pela NR aplicável **(verificar)**. Alerta aos 30 dias.
- ASO só é emitido por médico com CRM válido.

### 5.3 PCMSO, PGR e LTCAT

**Ausentes na v2.** Proposta:

- **PCMSO:** programa anual, com exames e calendário por grupo de risco. Responsável médico.
- **PGR:** inventário de riscos por setor (GHE). Plano de ação com prazo e responsável. Versão vigente única por unidade.
- **LTCAT:** laudo técnico de exposição, com validade. Base de cálculo de adicional de insalubridade e aposentadoria especial **(verificar)**.

Estados do plano de ação: `aberto`, `em_andamento`, `concluido`, `vencido` (calculado, [17](17-regras-modulos.md), seção 5.3).

### 5.4 CAT, acidente e afastamento

- CAT com data não futura, testemunhas por CPF válido e ocorrência registrada ([17](17-regras-modulos.md), seção 5.2).
- CID do acidente vai só para a CAT e para o médico.
- Afastamento gerado pela CAT é do RH ([14](14-integracao-modulos.md), seção 2).
- Envio da CAT ao INSS **(verificar)** o canal e o prazo.

### 5.5 EPI

Entrega com assinatura. CA com validade. Estoque não negativo ([17](17-regras-modulos.md), seção 5.2). A entrega é registrada no HCM, e o estoque fica no Suprimentos ([18](18-regras-modulos-2.md), seção 6).

### 5.6 CIPA e ergonomia

**Ausentes.** Proposta: eleição, composição e atas da CIPA **(verificar)** conforme NR-5. Laudo de ergonomia com versão e responsável técnico.

### 5.7 Treinamento em NR

Validade por NR, com alerta. Treinamento vencido bloqueia a função que exige a NR **(verificar)**.

---

## 6. Por portal

| Portal | Departamento pessoal | Recursos humanos | Medicina e SST |
|---|---|---|---|
| Desenvolvedor | HCM da própria empresa desenvolvedora, se houver equipe própria. Banco master, separado de qualquer entidade | Idem | SST da própria empresa, se houver |
| Gestão | Completo, por permissão ([17](17-regras-modulos.md), seção 3) | Completo, por permissão | Apto, inapto, restrição, EPI, NR, CAT, afastamento. **Sem CID nem prontuário** |
| Professor | Próprio holerite, férias, ponto e documentos | Próprio plano de desenvolvimento e treinamentos | Próprio ASO e resultado. Ciência de restrição funcional |
| Aluno | Nenhum | Nenhum | Nenhum |
| Responsáveis | Nenhum | Nenhum | Nenhum |
| Terceiros | Nenhum. Contabilidade recebe só totais ([38](38-portal-de-terceiros-prestadores.md), seção 3.2) | Nenhum | Clínica de ASO recebe agendamento e devolve resultado ([38](38-portal-de-terceiros-prestadores.md), seção 3.11) |

---

## 7. Permissões

A matriz da v1 (seção 20 de [`spec_gestao_pessoas_completo.md`](anexo-v1/spec_gestao_pessoas_completo.md)) é aproveitada, com estas correções:

| Permissão | v1 | Proposta |
|---|---|---|
| SST — Gerenciar | Por papel e portal que precisa (seção 11). RH e gestão não recebem essa permissão | SESMT e médico do trabalho, cada um com escopo próprio. RH e gestão só veem o resultado sem CID |
| Folha — Processar e aprovar | GE, GP, SA | Mantido. Quem processa não aprova ([22](22-crm-canais-e-papeis.md), seção 5) |
| Ponto — Ajuste manual | RH e GP | Mantido, com motivo obrigatório |
| Audit Log | SA, GE, GP, AUD | Mantido. Leitura do audit log gera evento ([29](29-auditoria.md), seção 5) |
| Holerite próprio | Todos | Mantido |

---

## 8. Integrações

| Evento | Origem | Destino | Estado |
|---|---|---|---|
| `hcm.employee.created` | HCM | SST (agenda admissional), Financeiro | Definido em [14](14-integracao-modulos.md) |
| `smt.cat.created` | SST | HCM (afastamento) | Definido |
| eSocial S-2200, S-1200, S-1210, S-2299 | HCM | Transmissor | **Ausente.** Só S-2220, S-2230, S-2240 estão definidos |
| `hcm.leave.started` | HCM | Financeiro (folha) | Definido em [14](14-integracao-modulos.md) |

Transmissão do eSocial segue D-08 ([16](16-integracoes-externas.md), seção 6): certificado da entidade, com transmissor da plataforma.

---

## 9. Pendências

| # | Pendência | Tipo |
|---|---|---|
| HCM-01 | RH e Pessoas como módulos separados, com fronteira definida (seção 11) | **Decidido** em 03/11/2026 |
| HCM-02 | Catálogo de verbas e tabelas de INSS, IRRF e FGTS por competência | (verificar) e Documento |
| HCM-03 | Regra de férias, 13.º e rescisão (LAC-12) | (verificar) e (jurídico) |
| HCM-04 | Eventos eSocial S-2200, S-1200, S-1210, S-2299 | (verificar) e Documento |
| HCM-05 | Ponto e jornada: regra de registro e controle | **Conferido** em parte em 03/11/2026: CLT, arts. 66, 71 e 74 (seção 3.4). Professor conferido nos arts. 317 a 323. Faltam a Portaria MTP nº 671/2021 (REP) e o estatuto do servidor de cada ente **(verificar)** |
| HCM-06 | Permissão "SST — Gerenciar" por papel e portal que precisa, fora de RH e gestão (seção 11) | **Decidido** em 03/11/2026 |
| HCM-07 | PCMSO, PGR, LTCAT, CIPA e ergonomia: escrever as especificações | **Escrito** em [52](52-medicina-do-trabalho-especificacao.md). Revisão do owner pendente |
| HCM-08 | Guarda do prontuário médico e de ASO por prazo | **Conferido** em 03/11/2026: no mínimo 20 anos após o desligamento (NR-7, 7.6.1.1). Detalhe em [52](52-medicina-do-trabalho-especificacao.md), seção 2 |
| HCM-09 | Recrutamento: prazo de guarda de currículo de não contratado (seção 11) | **Incluído.** Valor a fixar pelo (jurídico) |
| HCM-10 | HCM da empresa desenvolvedora e das entidades clientes (seção 11) | **Decidido** em 03/11/2026 |

---

## 10. Critérios de aceite

- [ ] Perfil de RH e de gestão não recebe CID nem prontuário em nenhuma tela ou API (varredura de resposta).
- [ ] ASO com restrição mostra restrição funcional sem motivo clínico para RH e gestão (teste).
- [ ] Folha fechada não é alterada (teste).
- [ ] Ajuste de ponto sem motivo é recusado (teste).
- [ ] Desligamento com afastamento ativo fica bloqueado (teste).
- [ ] Eventos eSocial definidos e testados em homologação antes da produção.
- [ ] Itens **(verificar)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).

---

## 11. Decisões de 03/11/2026

**HCM-01 (RH e Pessoas): módulos separados.** Cada um tem suas telas, permissões e dados próprios. O vínculo entre eles é só por referência à pessoa, sem cópia de dado.

| Módulo | Dono de | Não é dono de |
|---|---|---|
| RH | Recrutamento, onboarding, avaliação de desempenho, clima, movimentação interna | Folha, admissão no eSocial, cadastro civil |
| Pessoas (DP) | Cadastro funcional, folha, férias, rescisão, eSocial, ponto | Processo seletivo, avaliação, clima |

Quando um candidato é contratado, o RH passa a pessoa para Pessoas por referência. O cadastro funcional nasce em Pessoas, não no RH.

**HCM-06 (permissão "SST — Gerenciar"): por papel e por portal, não por cargo.** Não há uma permissão geral de SST para RH ou gestão. Cada papel que precisa gerir SST recebe permissão própria, limitada ao que faz:

- Médico do trabalho: ASO, prontuário, CID.
- Técnico de SESMT: ocorrências, EPI, NR, PGR, CAT, sem diagnóstico.
- Gestor de RH ou de unidade: resultado apto, inapto ou restrição, validade e afastamento, sem CID nem motivo clínico.

A permissão de cada papel aparece na matriz de permissões do portal onde ela é usada, e não como um item genérico de RH.

**HCM-09 (currículo de candidato não contratado): incluído.** O currículo e os dados do candidato não contratado são guardados por prazo fixo e depois excluídos. **Valor do prazo: (jurídico).** O candidato é informado da guarda no ato de envio. Não há uso desses dados fora do processo seletivo em que se candidatou.

**HCM-10 (HCM da plataforma e dos clientes): dois usos do mesmo módulo, isolados.**

- **Empresa desenvolvedora:** HCM próprio, para os seus funcionários, no portal do desenvolvedor, com dados no banco master e acesso restrito à equipe da própria empresa.
- **Entidades clientes:** cada entidade tem o seu HCM no portal de gestão, com banco da entidade e unidade. Nenhuma entidade vê dado de outra, e a empresa desenvolvedora não acessa o HCM de cliente como funcionário.
