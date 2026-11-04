# 17 — Regras de Validação dos Módulos Prioritários

> Parte do [SDD v2](00-README.md). Padrão de validação em [15](15-validacoes.md). Eventos e dono de dados em [14](14-integracao-modulos.md). Tipos de campo em [15](15-validacoes.md), seção 2.
> **Fonte:** especificações da v1 citadas em cada módulo. Onde a v1 não define a regra, o item aparece como **[Pendente]** e precisa de confirmação do owner.
> **Escopo:** módulos Financeiro, Pessoas (HCM), Acadêmico, SMT, Suprimentos e Contratos. Os demais módulos do [catálogo](12-catalogo-modulos.md) seguem a mesma estrutura em versões futuras deste documento.

---

## 1. Defeitos transversais da v1

Estes defeitos aparecem em mais de um módulo. Eles têm de ser corrigidos antes de qualquer implementação.

| ID | Defeito | Onde | Correção obrigatória |
|---|---|---|---|
| T-01 | Nenhuma tabela tem `tenant_id`. Contagem: 0 ocorrências em Financeiro (11 tabelas) e Acadêmico (22 tabelas). Pessoas e SMT usam `entityid`, sem `tenant_id`. Suprimentos isola por `entity_uuid` e `unit_uuid`. | Todos | Adicionar `tenant_id CHAR(36) NOT NULL` e índice composto que começa por `tenant_id`. Ver [03](03-dominio-tenancy.md), seção 3. |
| T-02 | Suprimentos e Contratos não têm DDL. Só descrição de tela. | Suprimentos, Contratos | Escrever o DDL antes da implementação, no padrão da seção 4 de [15](15-validacoes.md). |
| T-03 | Campos de chave interna com nomes diferentes (`id`, `uuid`, `code`, `entity_uuid`, `entityid`). | Todos | Padronizar: `id` numérico interno, `uuid` público, `tenant_id`, `entity_id`, `unit_id`. |
| T-04 | Estado derivado armazenado como estado. Ex.: `overdue` (Atrasado) está no `ENUM` de status, mas depende de data. | Financeiro | Status armazenado só com fatos. "Atrasado" é calculado por `due_date < hoje` com status `open` ou `partial`. |
| T-05 | Regras de unicidade dizem "por tenant" mas o DDL não tem tenant. | Acadêmico | Restrição composta `(tenant_id, cpf_hash)`. |
| T-06 | Status em inglês no banco e em português na tela. | Financeiro | Código e banco em inglês; rótulos pelo sistema de i18n ([09](09-internacionalizacao.md)). |

## 2. Financeiro

### 2.1 Entidades com DDL na v1

`financial_receivables`, `financial_payables`, `financial_transactions`, contas bancárias, centros de custo, orçamentos e outras (11 tabelas). Valores em `DECIMAL(15,2)` e taxas em `DECIMAL(5,4)`. Esses tipos estão corretos.

### 2.2 Campos e regras

| Campo | Tipo (v1) | Regra |
|---|---|---|
| `gross_amount` | DECIMAL(15,2) | Maior que zero. |
| `discount_amount` | DECIMAL(15,2) | Zero ou positivo; não pode ser maior que `gross_amount`. |
| `interest_rate`, `fine_rate` | DECIMAL(5,4) | Entre 0 e 1 (0% a 100%). Ajustar para percentual na tela, não no banco. |
| `net_amount` | DECIMAL(15,2) | **Calculado pelo servidor** e validado: `gross - discount + juros + multa`. Gravado com a regra de arredondamento do tenant ([15](15-validacoes.md), seção 4.2). Diferença é `422`. |
| `issue_date`, `due_date` | DATE | `due_date` não anterior a `issue_date`. |
| `payment_date` | DATE | Não pode ser futura na baixa. Não pode ser anterior a `issue_date`. |
| `amount_paid` | DECIMAL(15,2) | Maior que zero na baixa. Não pode exceder o saldo do título. |
| `installment_number`, `total_installments` | SMALLINT | `installment_number` entre 1 e `total_installments`. |
| `parent_id` | BIGINT | Aponta para o título-mãe do mesmo tenant. Parcelas não são títulos independentes para estorno. |
| `status` | ENUM | Ver seção 2.3. |
| `category_id`, `cost_center_id`, `bank_account_id` | BIGINT | Existem no tenant e estão ativos na data de lançamento. |
| `approval_status` (pagar) | ENUM | Ver seção 2.4. |

### 2.3 Estados do título

Estados armazenados: `open`, `partial`, `paid`, `cancelled`.

| De | Para | Condição |
|---|---|---|
| `open` | `partial` | Baixa menor que o saldo. |
| `open` ou `partial` | `paid` | Soma das baixas igual ao líquido. |
| `open` ou `partial` | `cancelled` | Sem baixa registrada. Com baixa, só por estorno. |
| `paid` | `cancelled` | Não permitido. Estorno gera movimento novo. |

"Atrasado" (`overdue`) não é estado. É filtro calculado: `status IN (open, partial) AND due_date < data de referência`. Resolve T-04.

### 2.4 Aprovação de despesa

- `approval_status` `pending` bloqueia a baixa.
- Solicitante não pode aprovar a própria despesa. Regra da v1 em Suprimentos vale aqui também.
- Aprovação acima de R$ 10.000 exige segundo aprovador. Decidido pelo autor em 03/11/2026.

### 2.5 Conciliação bancária

A v1 define matching automático (seção 7.5):

| Regra | Classificação |
|---|---|
| Valor exato e data ± 1 dia | Match automático, confiança alta |
| Valor exato e data ± 3 dias | Match sugerido, confiança média |
| Valor ± R$ 0,01 e data ± 1 dia | Match sugerido |
| Sem match | Pendente manual |

**[Pendente]** A regra de R$ 0,01 é tolerância de arredondamento. Ela deve ser parâmetro do tenant, e não constante. Um lançamento só pode ser conciliado uma vez: `financial_transactions.status = matched` impede novo vínculo.

### 2.6 Idempotência

- Baixa e emissão de cobrança exigem chave de idempotência ([15](15-validacoes.md), seção 4).
- Importação de extrato OFX é idempotente pelo hash da linha (data, valor, descrição, identificador do banco).

### 2.7 Testes específicos

- Título com desconto maior que o bruto: `422`.
- Baixa de valor maior que o saldo: `422`.
- Duas baixas com a mesma chave de idempotência: um movimento.
- Título pago com estorno: novo movimento, original inalterado.

## 3. Pessoas (HCM)

### 3.1 Entidades

Colaborador, cargo, faixa salarial, documentos, ponto, férias, afastamentos, treinamentos, folha, recrutamento e onboarding (12 tabelas na v1). O cadastro de pessoa civil deve ser único (decisão D-06, [14](14-integracao-modulos.md), seção 3).

### 3.2 Campos e regras (v1, seção 4 e 2)

| Campo | Regra |
|---|---|
| CPF | Formato e dígito verificador ([15](15-validacoes.md), seção 2). Mascarado na lista. Único por tenant. |
| RG, PIS/NIS | Formato por tipo de documento **[Pendente: regra por UF para RG]**. |
| Data de nascimento | Não futura. Idade mínima para vínculo **[Pendente: regra legal por tipo de vínculo]**. |
| CTPS | Obrigatória para vínculo CLT. |
| Salário base | Maior que o piso da categoria. Campo restrito: só quem tem permissão `hcm.salario.ler` vê. |
| Experiência (contrato de experiência) | A v1 diz "máximo 90 dias (prorrogável 1× até 90 dias)". Esse texto é contraditório: duas prorrogações somariam mais de 90 dias. **[Pendente: confirmação jurídica da CLT, art. 445]**. |
| Documento anexado | PDF, JPEG ou PNG; máximo 10 MB. Versão e validade obrigatórias para documento com vencimento. |
| Treinamento obrigatório | Alerta 30 dias antes do vencimento. |

### 3.3 Estados

| Entidade | Estados |
|---|---|
| Colaborador | `ativo`, `afastado`, `desligado` (transições por evento de RH) |
| Vaga | `aberta`, `pausada`, `preenchida`, `cancelada` |
| Candidato | conforme pipeline do Kanban; cada etapa tem entrada e saída declaradas |
| Folha | `em_processamento`, `fechada`, `paga`. Folha fechada não é alterada; correção é folha complementar. |

### 3.4 Dados sensíveis

- Dado de saúde (tipo sanguíneo, alergias) do SMT: criptografado, conforme a v1 (ver seção 5.1).
- Salário: campo restrito; o listado não exibe o valor sem permissão.
- Folha: só o próprio colaborador vê o holerite; RH vê os de sua unidade.

### 3.5 Integrações

- `hcm.employee.created`, `hcm.employee.terminated`, `hcm.employee.department-changed`, `hcm.absence.created` ([14](14-integracao-modulos.md), seção 4).

## 4. Acadêmico

### 4.1 Entidades

Matrícula, aluno, turma, disciplina, diário, avaliação, plano de aula, plano de ensino, conselho de classe, estágio, documentos da secretaria, presença (22 tabelas na v1).

### 4.2 Campos e regras (v1, seções 4 a 9)

| Campo | Regra |
|---|---|
| CPF do aluno ou candidato | Único por tenant. Busca antes de cadastrar; alerta de matrícula duplicada (v1, seção 4.2). |
| Documentos pessoais | Versionados, com data de upload, validade, responsável e hash de integridade (v1, seção 5). |
| Matrícula | Um vínculo ativo por aluno e turma. Vaga disponível com bloqueio de concorrência ([15](15-validacoes.md), seção 7). |
| Trancamento | Prazo máximo conforme regimento **[Pendente: valor do regimento, por curso]**. |
| Nota | Dentro da faixa do método de avaliação; período de lançamento aberto. |
| Presença por QR Code | Válido por 5 minutos por padrão, configurável pela escola. Decidido pelo autor em 03/11/2026. Geolocalização só com consentimento, conforme [07](07-privacidade-lgpd.md). |
| Horas de atividade complementar | Status `pendente_validacao`, `validado`, `recusado`. Total validado nunca ultrapassa o limite do curso. |
| Estágio | CNPJ válido da empresa concedente. Apólice de seguro com validade. |
| Protocolo de atendimento | Consulta pública por número e CPF, sem login, com limite de tentativas. |

### 4.3 Estados

| Entidade | Estados |
|---|---|
| Matrícula | `pre_matricula`, `ativa`, `trancada`, `concluida`, `cancelada`, `transferida` |
| Diário | `aberto`, `fechado`, `reaberto` (com justificativa) |
| Estágio | `solicitado`, `ativo`, `concluido`, `cancelado` |

### 4.4 Segurança específica

- Dados de aluno menor de idade: acesso do responsável legal, com vínculo verificado ([07](07-privacidade-lgpd.md), seção 1).
- Diário e notas: professor vê só as turmas em que está vinculado.

## 5. SMT (Segurança e Medicina do Trabalho)

### 5.1 Entidades

Funcionário e ASO, PCMSO, PGR/GHE, LTCAT, CAT, EPI, treinamentos NR, afastamentos, CIPA.

### 5.2 Campos e regras (v1, seções 4 a 12)

| Campo | Regra |
|---|---|
| Ficha de saúde | Dado sensível. Criptografado. Acesso restrito a profissional de saúde e ao próprio colaborador. |
| ASO | Tipo (admissional, periódico, retorno, mudança, demissional) obrigatório. Resultado somente por profissional responsável. |
| CAT | Data do acidente não futura. Testemunhas por CPF válido. Emissão exige ocorrência registrada. |
| EPI | CA com validade. Entrega com registro de assinatura (FIEPI). Estoque não negativo. |
| Treinamento NR | Validade obrigatória quando a NR exige reciclagem. |
| Afastamento | Data fim não anterior à início. Sobreposição com afastamento ativo é recusada. |
| GHE | Pertence a um PGR ativo do tenant. |

### 5.3 Estados

| Entidade | Estados |
|---|---|
| CAT | `emitida`, `em_investigacao`, `encerrada` |
| EPI (entrega) | `entregue`, `devolvido`, `extraviado` |
| Plano de ação | `aberto`, `em_andamento`, `concluido`, `vencido` (calculado por prazo) |

### 5.4 Integrações

- SMT consome `hcm.employee.created` para agendar exame admissional.
- SMT publica `smt.exam.performed`, `smt.cat.created`, `smt.training.expired` ([14](14-integracao-modulos.md), seção 4).
- Transmissão de eSocial (S-2220, S-2230, S-2240) conforme decisão D-08 ([16](16-integracoes-externas.md), seção 6).

## 6. Suprimentos

### 6.1 Entidades

Requisição, aprovação, cotação, pedido de compra, recebimento, divergência, almoxarifado, itens críticos, fornecedor, avaliação de fornecedor, contrato e ata (sem DDL na v1, ver T-02).

### 6.2 Regras de negócio (v1, seções 6.2 e 9)

| Regra | Descrição |
|---|---|
| Autoaprovação | Bloqueada acima da faixa da política. |
| Solicitante e aprovador | Não podem ser a mesma pessoa em cenários sensíveis. |
| Pedido | Só emitido por usuário com permissão. |
| Fornecedor bloqueado | Não recebe pedido nem recebimento quando a política exige. |
| Edição após encerramento | Bloqueada. |
| Cotações | Número mínimo por faixa de valor. Fonte única só com justificativa. Motivo da adjudicação registrado. |
| Comparativo | Snapshot gravado no fechamento da cotação. |
| Estoque | Movimento que deixaria saldo negativo é recusado, salvo item de consumo sob encomenda. |
| Divergência de recebimento | Tipo obrigatório (quantidade, item incorreto, avaria, validade, lote, documento fiscal, atraso). |

### 6.3 Estados

| Entidade | Estados |
|---|---|
| Requisição | `rascunho`, `em_aprovacao`, `aprovada`, `reprovada`, `cancelada` |
| Pedido | `emitido`, `em_transito`, `recebido_parcial`, `recebido`, `cancelado` |
| Fornecedor | `ativo`, `bloqueado`, `inativo` |

### 6.4 Campos mínimos a definir

Como a v1 não tem DDL, os campos de requisição, pedido, item e fornecedor precisam ser escritos antes. Lista mínima proposta:

- Requisição: solicitante, unidade, centro de custo, itens (item, quantidade, unidade de medida), valor estimado, justificativa, data limite de SLA.
- Item: código, descrição, unidade de medida, estoque mínimo, estoque atual, fornecedor preferencial.
- Fornecedor: CNPJ válido, situação documental, validade de certificados, situação (`ativo`, `bloqueado`).

## 7. Contratos

### 7.1 Entidades

Contrato, parte, valor, vigência, cláusula, obrigação, aprovação, assinatura, aditivo, solicitação contratual (sem DDL na v1, ver T-02).

### 7.2 Regras de negócio (v1, seções 8, 10 e 12)

| Regra | Descrição |
|---|---|
| Edição após assinatura | Bloqueada, exceto por aditivo. |
| Alteração estrutural após assinatura | Gera aditivo. |
| Parte | CPF ou CNPJ válido; duplicidade por documento bloqueada. |
| Contratação | Bloqueada com documentação vencida. |
| Anexo obrigatório | Avanço de etapa bloqueado sem o documento obrigatório. |
| Parecer | Jurídico obrigatório por tipo de contrato. Financeiro obrigatório acima de faixa **[Pendente: faixa]**. |
| Cláusula obrigatória | Lista por tipo de contrato; ausência bloqueia envio para assinatura. |

### 7.3 Estados

| Entidade | Estados |
|---|---|
| Contrato | `negociacao`, `aprovacao`, `assinado`, `vigente`, `em_renovacao`, `encerrado`, `cancelado` |
| Aditivo | `rascunho`, `aprovado`, `assinado` |
| Solicitação contratual | `aberta`, `em_validacao`, `bloqueada`, `concluida` |

### 7.4 Validação de datas

- Vigência: data fim posterior à data início.
- Renovação automática: aviso antes do vencimento, com prazo em dias configurável. Padrão de 60 dias, decidido pelo autor em 03/11/2026.

## 8. Lacunas abertas

| # | Lacuna | Dono sugerido | Situação em 04/11/2026 |
|---|---|---|---|
| LAC-01 | Faixas de valor para aprovação de despesa e contrato | Financeiro | Parcial: despesa decidida (acima de R$ 10.000, segundo aprovador; [17](17-regras-modulos.md), seção 2.4). Alçada de contrato em aberto ([33](33-contratos-por-portal.md), seção 4) |
| LAC-02 | Regra de RG por UF e idade mínima por vínculo | Pessoas | Aberta |
| LAC-03 | Prazo de experiência (CLT art. 445) | Jurídico | Aberta (jurídico) |
| LAC-04 | Prazo de trancamento por curso e validade de QR Code | Acadêmico | Parcial: QR Code de 5 minutos decidido ([17](17-regras-modulos.md), seção 4.2). Prazo de trancamento depende do regimento de cada curso ([46](46-matricula-e-rematricula-por-portal.md), M-06) |
| LAC-05 | Campos e DDL de Suprimentos e Contratos | Suprimentos, Contratos | Parcial: DDL de contratos em [51](51-ddl-modulos-novos.md), seção 3. Campos de suprimentos na v1 (especificação de suprimentos, seção 18). DDL de suprimentos a escrever |
| LAC-06 | Tolerância de conciliação como parâmetro do tenant | Financeiro | Resolvida: parâmetro da entidade ([71](71-financeiro-completo-por-portal.md), seção 9) |

## 9. Critérios de aceite

- [ ] Todas as tabelas dos módulos têm `tenant_id NOT NULL` e índice composto por ele (T-01).
- [ ] Nenhum estado calculado é armazenado como estado (T-04).
- [ ] Cada regra marcada **[Pendente]** tem dono e data na seção 8 deste documento.
- [ ] Suprimentos e Contratos têm DDL escrito (T-02).
- [ ] Cada módulo tem tabela de transição de estado para as entidades com status.
