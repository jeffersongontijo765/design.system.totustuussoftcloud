# 37 — Planejamento (Acadêmico, Institucional, de Desenvolvimento) e Empenho

> Parte do [SDD v2](00-README.md). Matriz de portais em [31](31-matriz-portais-modulos.md), seção 3.9. Acadêmico em [17](17-regras-modulos.md). Pessoas em [18](18-regras-modulos-2.md), seção 3. Contábil e fiscal em [18](18-regras-modulos-2.md), seção 4. Financeiro em [17](17-regras-modulos.md), seção 2. Auditoria em [29](29-auditoria.md). Validação em [15](15-validacoes.md).
> **Status:** especificação proposta, criada em 03/11/2026 a partir da decisão do autor de "analisar e implementar". Não há especificação anterior na v1 para estes módulos. Itens **(verificar)** citam norma que precisa de conferência antes da implementação. Não é parecer.

---

## 1. Análise

| Item | Situação na v1 | Análise | Decisão |
|---|---|---|---|
| Planejamento acadêmico | Termo ausente como módulo. Há planejamento de aula no diário | Planejamento de oferta, grade, turmas, vagas e carga docente é necessário para matrícula e para a folha de docentes | Implementar como módulo de tenant |
| Planejamento institucional | Termo ausente | Corresponde ao plano de desenvolvimento institucional da entidade: missão, metas, indicadores e ações. Instituições de ensino superior têm esse plano por exigência regulatória **(verificar)** | Implementar como módulo de tenant |
| Planejamento de desenvolvimento | Termo ausente. Há "plano de desenvolvimento individual" na preceptoria ([19](19-regras-modulos-3.md), seção 11) | Entendido como plano de desenvolvimento de pessoas (carreira e formação). O plano individual de preceptoria é caso particular e continua na preceptoria | Implementar como módulo de tenant, ligado a Pessoas |
| Empenho | Termo ausente | Empenho é o ato que reserva dotação orçamentária antes da despesa pública. Só se aplica a entidade que é órgão público ou que mantém contabilidade pública **(verificar)**: Lei 4.320/1964, arts. 58 a 65 | Implementar como módulo de tenant, ativado só por entidade pública |

**Separação:** o planejamento é gestão e não tem valor financeiro próprio. O empenho é execução de despesa. Os dois não compartilham tabela. O planejamento institucional pode prever recursos, mas o valor comprometido só existe no empenho.

---

## 2. Planejamento acadêmico

### 2.1 Entidades

| Entidade | Função |
|---|---|
| Período letivo | Intervalo com datas, unidade e situação |
| Oferta | Disciplina ou série oferecida em um período, com vagas e carga horária |
| Turma planejada | Divisão da oferta, com professor previsto e sala |
| Carga docente | Horas previstas por professor em cada período |
| Previsão de matrícula | Quantidade esperada por oferta, a partir de rematrícula e captação ([31](31-matriz-portais-modulos.md), seção 3.5) |

### 2.2 Estados

`rascunho` → `em_revisao` → `aprovado` → `publicado` → `encerrado`. `publicado` é o estado que alimenta matrícula. Oferta publicada não é editada. Alteração gera revisão.

### 2.3 Regras

- Turma publicada com vaga zero não aceita matrícula.
- Carga docente prevista acima do limite contratual do professor gera alerta antes da publicação. O limite vem de [18](18-regras-modulos-2.md), seção 3.
- Professor sem disciplina habilitada não é atribuído à oferta ([17](17-regras-modulos.md), seção 4).
- Oferta publicada só é alterada com motivo e aprovação de segundo papel.
- Período encerrado é somente leitura.

---

## 3. Planejamento institucional

### 3.1 Entidades

| Entidade | Função |
|---|---|
| Plano institucional | Documento com período (ex.: cinco anos), missão e valores |
| Objetivo | Meta de longo prazo dentro do plano |
| Indicador | Medida com fórmula, fonte, unidade e periodicidade |
| Ação | Tarefa com responsável, prazo e orçamento previsto |
| Acompanhamento | Registro periódico de resultado de indicador |

### 3.2 Estados

Plano: `rascunho` → `em_revisao` → `aprovado` → `vigente` → `encerrado`. Ação: `planejada` → `em_andamento` → `concluida` ou `cancelada`.

### 3.3 Regras

- Objetivo sem indicador não é aprovado.
- Indicador sem fonte de dado definida não é aprovado. A fonte é um módulo do sistema ou um campo informado com responsável.
- Ação sem responsável não entra em `em_andamento`.
- Acompanhamento é imutável. Correção gera novo registro com referência ao anterior.
- Plano aprovado tem versão. Mudança de meta gera nova versão, com aprovação registrada.
- Aprovação final do plano é de órgão colegiado da entidade **(verificar)** exigência da regulação do setor. O sistema registra a ata e o órgão aprovador.

### 3.4 Ligação com orçamento

Ação com orçamento previsto informa a dotação, mas não empenha. Para executar a despesa, a ação gera solicitação de compra ([19](19-regras-modulos-3.md), seção 2) ou, em entidade pública, solicitação de empenho (seção 5).

---

## 4. Planejamento de desenvolvimento de pessoas

### 4.1 Entidades

| Entidade | Função |
|---|---|
| Plano de desenvolvimento | Por colaborador, com período e metas de formação e carreira |
| Ação de formação | Curso, treinamento ou certificação, com carga horária |
| Trilha | Conjunto de ações para um cargo |
| Avaliação de competência | Resultado por competência, vinculado ao ciclo de avaliação de desempenho |

### 4.2 Estados

Plano: `rascunho` → `pactuado` → `em_execucao` → `concluido`. Pactuado exige assinatura do colaborador e do gestor. Ação de formação: `prevista` → `realizada` → `comprovada`.

### 4.3 Regras

- Plano sem assinatura do colaborador não entra em execução.
- Ação `realizada` sem comprovante não vira `comprovada`.
- Carga horária comprovada alimenta o registro de formação do colaborador ([18](18-regras-modulos-2.md), seção 3).
- Avaliação de competência não altera nota de desempenho. Os dois são registros separados.
- Dado de saúde ou de afastamento não entra no plano ([07](07-privacidade-lgpd.md), seção 2).

---

## 5. Empenho (entidade pública)

**Ativação:** o módulo só é habilitado para entidade que declara natureza pública. A declaração é feita pelo administrador da entidade, com MFA, e registrada em auditoria.

### 5.1 Entidades

| Entidade | Função |
|---|---|
| Dotação | Valor autorizado por rubrica, exercício e unidade |
| Empenho | Reserva de dotação para uma despesa, com credor, valor e origem |
| Liquidação | Confirmação de que o bem ou serviço foi entregue, com documento comprobatório |
| Pagamento | Saída financeira, sempre posterior à liquidação |
| Anulação | Reversão parcial ou total de empenho, com motivo |
| Restos a pagar | Empenho que passa para o exercício seguinte |

### 5.2 Modalidades

Conferido em 03/11/2026 no texto da Lei 4.320/1964 (planalto.gov.br):

| Modalidade | Base |
|---|---|
| Ordinário | Valor certo. A lei não usa o nome: é o caso comum, sem regra própria |
| Por estimativa | Despesa cujo montante não se pode determinar (art. 60, § 2º) |
| Global | Despesa contratual ou outra sujeita a parcelamento (art. 60, § 3º) |

- Empenho é o ato de autoridade competente que cria a obrigação de pagamento (art. 58). Não há despesa sem prévio empenho (art. 60), salvo dispensa da nota em lei específica (art. 60, § 1º).
- Cada empenho gera a **nota de empenho**, com credor, especificação, valor e dedução do saldo da dotação (art. 61). O sistema emite a nota com esses campos obrigatórios.
- O empenho não excede o crédito concedido (art. 59).
- **Liquidação** apura origem e objeto, valor exato e credor, com base no contrato, na nota de empenho e no comprovante de entrega ou serviço (art. 63). Pagamento só depois da liquidação regular e por **ordem de pagamento** da autoridade competente, em documento processado pela contabilidade (arts. 62 e 64).
- **Município, último mês do mandato do prefeito:** não empenha mais que um duodécimo da despesa prevista, nem assume compromisso para depois do mandato, salvo calamidade pública comprovada. Empenho em desacordo é nulo (art. 59, §§ 1º a 4º). O sistema bloqueia acima do duodécimo nesse mês, com data do fim do mandato cadastrada pela entidade, e aceita exceção só com o decreto de calamidade anexado.
- Normas do tribunal de contas de cada estado e o texto compilado da lei, com alterações posteriores, **(verificar)**.

### 5.3 Estados

Empenho: `emitido` → `liquidado` → `pago`. Pode ir para `anulado` (parcial ou total) antes de `pago`. Empenho não pago até 31 de dezembro vai para `restos_a_pagar`, separado em **processado** (já liquidado) e **não processado** (não liquidado) (Lei 4.320/1964, art. 36). Empenho de crédito plurianual não liquidado só vira restos a pagar no último ano de vigência do crédito (art. 36, parágrafo único).

### 5.4 Regras

- Empenho não pode exceder a dotação disponível da rubrica, na data de emissão.
- Liquidação exige documento comprobatório (nota fiscal, recibo ou contrato) vinculado.
- Pagamento exige liquidação. Sem liquidação, a aplicação recusa o pagamento.
- Anulação exige motivo e aprovação de segundo papel. Quem emite não aprova.
- Pagamento segue a regra de pagamento de [20](20-pagamentos-seguranca.md) e de [34](34-pagamentos-fiscal-bancos-por-portal.md).
- Período fechado não recebe novo empenho.
- Toda emissão, liquidação, pagamento e anulação gera evento de auditoria ([29](29-auditoria.md)).

### 5.5 Segregação

| Ação | Papel que executa | Papel que aprova |
|---|---|---|
| Emitir empenho | Financeiro | Contador |
| Liquidar | Responsável pelo recebimento | Financeiro |
| Pagar | Financeiro | Gestor executivo acima da faixa 2 de [33](33-contratos-por-portal.md) |
| Anular | Financeiro | Contador e gestor executivo |

---

## 6. Portais

| Portal | Planejamento acadêmico | Planejamento institucional | Desenvolvimento de pessoas | Empenho |
|---|---|---|---|---|
| Desenvolvedor | Nenhum | Plano institucional da própria empresa, se houver | Nenhum | Nenhum |
| Gestão | Completo, por permissão | Completo, por permissão | Completo, por permissão | Completo, para entidade pública, por permissão |
| Professor | Carga e turmas próprias, somente leitura | Nenhum | Plano próprio | Nenhum |
| Aluno | Oferta publicada e calendário, somente leitura | Nenhum | Nenhum | Nenhum |
| Responsáveis | Calendário e oferta publicada, somente leitura | Nenhum | Nenhum | Nenhum |
| Terceiros | Nenhum | Nenhum | Nenhum | Recebe pagamento liquidado. Ver [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 8 |

---

## 7. Integrações

| Origem | Destino | Evento |
|---|---|---|
| Planejamento acadêmico | Acadêmico | Oferta publicada |
| Planejamento acadêmico | Pessoas | Carga docente aprovada |
| Planejamento acadêmico | Financeiro | Previsão de receita por oferta |
| Planejamento institucional | Suprimentos | Solicitação de compra a partir de ação |
| Planejamento de desenvolvimento | Pessoas | Formação comprovada |
| Empenho | Contábil e fiscal | Empenho, liquidação, pagamento, anulação |
| Empenho | Financeiro | Pagamento |

Todos os eventos seguem [14](14-integracao-modulos.md), com outbox e consumidor idempotente.

---

## 8. Estrutura de dados mínima

Tabelas com `tenant_id` e índice composto ([03](03-dominio-tenancy.md)). Valores monetários em centavos ([20](20-pagamentos-seguranca.md), seção 4).

```sql
CREATE TABLE plan_strategic_goals (
  id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid         CHAR(36)     NOT NULL,
  tenant_id    CHAR(36)     NOT NULL,
  plan_id      BIGINT UNSIGNED NOT NULL,
  title        VARCHAR(200) NOT NULL,
  status       VARCHAR(30)  NOT NULL,
  owner_uuid   CHAR(36)     NULL,
  created_at   DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  UNIQUE KEY uk_goal_uuid (uuid),
  INDEX idx_tenant_plan (tenant_id, plan_id, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE budget_commitments (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36)     NOT NULL,
  tenant_id       CHAR(36)     NOT NULL,
  unit_id         CHAR(36)     NOT NULL,
  fiscal_year     SMALLINT     NOT NULL,
  budget_line     VARCHAR(40)  NOT NULL,
  modality        ENUM('ordinario','estimativo','global') NOT NULL,
  creditor_uuid   CHAR(36)     NOT NULL,
  amount_cents    BIGINT       NOT NULL,
  status          VARCHAR(30)  NOT NULL,
  supporting_doc  VARCHAR(255) NULL,
  created_by      CHAR(36)     NOT NULL,
  approved_by     CHAR(36)     NULL,
  created_at      DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  UNIQUE KEY uk_commitment_uuid (uuid),
  INDEX idx_tenant_year_line (tenant_id, fiscal_year, budget_line),
  CHECK (amount_cents > 0),
  CHECK (created_by <> approved_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Notas:

- `CHECK (created_by <> approved_by)` garante a segregação. A aplicação também valida, para dar mensagem clara.
- Liquidação e pagamento são tabelas próprias, com chave para o empenho, e não colunas de `budget_commitments`.
- Restos a pagar processado ou não processado não é coluna: sai da existência de liquidação do empenho em 31 de dezembro (seção 5.3).
- Dotação é tabela própria, por exercício e rubrica. A soma de empenhos ativos não pode passar da dotação. Essa regra é validada na transação de emissão.

---

## 9. Pendências

| # | Pendência | Tipo |
|---|---|---|
| PLN-01 | Obrigação de plano institucional e órgão colegiado aprovador, por tipo de entidade | (verificar) |
| PLN-02 | Lei 4.320/1964 e normas do órgão de controle para o empenho | **Conferido** em parte em 03/11/2026: Lei 4.320/1964, arts. 36 e 58 a 65 (seção 5.2). Faltam as normas do tribunal de contas e o texto compilado **(verificar)** |
| PLN-03 | Lista de rubricas padrão | **Decidido** em 03/11/2026: a empresa desenvolvedora define, com modelo por tipo de entidade. A entidade pode ajustar |
| PLN-04 | Quem declara a natureza pública da entidade | **Decidido** em 03/11/2026: a gestão da entidade declara, com o ato anexado |
| PLN-05 | Limite de carga docente por professor (ligado a [18](18-regras-modulos-2.md), seção 3) | **Decidido** em 03/11/2026: definido por unidade, com aviso acima de 40 horas-aula por semana |

---

## 10. Critérios de aceite

- [ ] Oferta publicada com vaga zero não aceita matrícula (teste).
- [ ] Objetivo sem indicador e ação sem responsável não avançam de estado (teste).
- [ ] Empenho acima da dotação é recusado na transação (teste de concorrência).
- [ ] Pagamento sem liquidação é recusado (teste).
- [ ] Quem emite um empenho não o aprova (teste de segregação, com `CHECK`).
- [ ] Módulo de empenho invisível para entidade que não declarou natureza pública (teste).
- [ ] Itens **(verificar)** conferidos antes da implementação.
