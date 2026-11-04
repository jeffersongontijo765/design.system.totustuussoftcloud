# 14 — Integração entre Módulos

> Parte do [SDD v2](00-README.md). Integrações com sistemas de terceiros ficam em [16](16-integracoes-externas.md). Validação de entrada em [15](15-validacoes.md).
> **Status:** proposta. Itens marcados **[Decisão pendente]** precisam de aprovação do autor antes da implementação.

---

## 1. Princípios

1. **Dono exclusivo.** Cada dado tem um único módulo dono. Outro módulo nunca lê nem grava na tabela desse dono.
2. **Leitura por contrato.** Um módulo lê dados de outro por uma interface de serviço versionada, com tenant obrigatório. Nunca por SQL direto.
3. **Escrita derivada por evento.** Quando a mudança em um módulo precisa gerar efeito em outro, o módulo dono publica um evento. O consumidor decide o que fazer.
4. **Tenant em tudo.** Evento, chamada e consumo carregam `tenant_id` e `entity_id`. Consumidor sem contexto de tenant rejeita a mensagem.
5. **Idempotência e auditoria.** Entrega duplicada não gera efeito duplicado. Toda ação entre módulos gera registro com ator, origem e correlação.
6. **Mínimo de dados.** Evento carrega identificadores e o estado mínimo. Dado pessoal e dado de saúde não viajam no payload (ver seção 8).

## 2. Estilos de comunicação

| Estilo | Quando usar | Garantia | Limites |
|---|---|---|---|
| **Evento assíncrono** (outbox + fila) | Efeito derivado em outro módulo; escrita que pode ser processada depois | At-least-once com consumidor idempotente | Atraso de segundos a minutos |
| **Comando síncrono** (serviço interno) | Validação curta que bloqueia a operação, por exemplo "a unidade existe e está ativa" | Resposta imediata | Timeout de 2 s; não encadear mais de dois saltos |
| **Consulta de projeção** (read model) | Listagem ou painel que combina dados de vários módulos | Dado pode estar defasado em poucos segundos | Nunca usada como fonte para decisão de escrita |

**[Decidida D-05 — aprovada com a proposta (02/11/2026)]** Padrão: eventos assíncronos para toda escrita derivada, comando síncrono só para validação, projeção para painéis. Alternativa: chamadas síncronas diretas entre serviços. Ela é mais simples de depurar, mas acopla a disponibilidade de um módulo à de outro. Condição de falha da alternativa: queda do módulo chamado derruba a operação do módulo chamador.

## 3. Dono dos dados compartilhados

| Entidade | Módulo dono | Consumidores principais | Regra |
|---|---|---|---|
| Pessoa (identidade civil: nome, documento, contato) | Pessoas (HCM) | Acadêmico, RH, Financeiro, Portal do aluno | Um `person_id` por pessoa por tenant. Nenhum outro módulo copia nome ou documento. |
| Vínculo de aluno | Acadêmico | Financeiro, Portal do aluno, Portal dos pais | Referencia `person_id`. |
| Vínculo de colaborador | RH | SMT, Suprimentos, Financeiro (folha) | Referencia `person_id`. |
| Responsável legal | Pessoas (família) | Acadêmico, Financeiro, Portal dos pais | Vínculo com aluno guardado no Acadêmico, dados civis no Pessoas. |
| Entidade, unidade, usuário, papel | Identidade (ver [06](06-identidade-acesso.md)) | Todos | Só o módulo Identidade altera. |
| Centro de custo, cargo | Financeiro (centro de custo) e RH (cargo) | Suprimentos, RH | Código e nome são do dono; o consumidor guarda só o código. |
| Item de estoque e saldo | Suprimentos | SMT (EPI), Financeiro | Saldo só muda por movimento registrado. |
| Exame ocupacional e aptidão | SMT | RH | RH recebe só o status de aptidão, não o laudo. |
| Afastamento | RH | SMT, Financeiro (folha) | RH é o dono do afastamento; SMT referencia o CAT pelo ID. |
| Contrato e ata | Contratos | Suprimentos, Financeiro | Consumo de saldo é movimento no Contratos. |

**[Decidida D-06 — aprovada com a proposta (02/11/2026)]** Pessoa única: `person_id` único no Pessoas. Alternativa: cada módulo mantém a própria cópia de pessoa, com sincronização. A alternativa gera divergência de nome e documento entre módulos. Condição de falha da proposta: se o Pessoas ficar indisponível, nenhum módulo consegue criar vínculo novo. Mitigação: o Pessoas é consultado por comando de leitura, com cache por tenant de vida curta.

**[Decidida D-19 — pessoa única entre unidades, com cadastro civil no banco de identidade da entidade (opção a). Decisão proposta por esta versão em 02/11/2026 e adotada pelo autor. Substitui a decisão de manter o cadastro civil no master. Ver [06](06-identidade-acesso.md), seção 12.]**

O master guarda somente conta, vínculos e índice de pessoas (`person_id` e e-mail verificado), sem dado civil. Cada entidade tem um banco de identidade com o cadastro civil cifrado. As unidades da entidade guardam apenas o `person_id`.

Motivos: limita o impacto de incidente a uma entidade, mantém a entidade como controladora do dado do aluno e facilita exportação e exclusão na saída do cliente.

**Salvaguardas obrigatórias:**

- Cadastro civil cifrado com chave da entidade (envelope, ADR-05 em [02](02-arquitetura.md)).
- Acesso ao banco de identidade só com vínculo ativo na entidade ([06](06-identidade-acesso.md), seção 12.4).
- Auditoria de cada leitura do cadastro civil ([18](18-regras-modulos-2.md), seção 4.2).
- Backup do banco de identidade separado e com teste de restauração.
- Relatório de impacto e aprovação do DPO antes da produção ([07](07-privacidade-lgpd.md)).
- Teste de isolamento entre entidades, inclusive pelo identificador exato.

## 4. Catálogo de eventos de domínio

Nome: `<modulo>.<entidade>.<fato-no-passado>`, em inglês, minúsculo, com hífen. Exemplo: `hcm.employee.created`.

| Evento | Produtor | Consumidores | Efeito derivado |
|---|---|---|---|
| `hcm.employee.created` | RH | SMT, Suprimentos | SMT agenda exame admissional. Suprimentos abre onboarding de itens. |
| `hcm.employee.terminated` | RH | SMT, Suprimentos | SMT encerra exames pendentes. Suprimentos abre devolução de ativos. |
| `hcm.employee.department-changed` | RH | Suprimentos, Financeiro | Atualiza centro de custo nas requisições abertas. |
| `hcm.absence.created` | RH | SMT | SMT registra restrição de função, se houver. |
| `smt.exam.scheduled` | SMT | Notificações | Aviso ao colaborador. |
| `smt.exam.performed` | SMT | RH | RH atualiza status de aptidão do colaborador. |
| `smt.cat.created` | SMT | RH, Financeiro | RH abre afastamento. Financeiro registra evento de folha. |
| `suprimentos.epi.stock-minimum-reached` | Suprimentos | Suprimentos (compra), SMT | Gera solicitação de compra. SMT é avisado da indisponibilidade. |
| `suprimentos.supplier.blocked` | Suprimentos | Suprimentos (compra), Contratos | Bloqueia emissão de pedido ao fornecedor. |
| `smt.training.expired` | SMT | Notificações, RH | Aviso e bloqueio de função, conforme regra. |
| `suprimentos.request.approved` | Suprimentos | Financeiro | Cria obrigação a pagar. |
| `academico.matricula.efetivada` | Acadêmico | Financeiro, Notificações, Biblioteca | Gera a cobrança da primeira parcela. Avisa o aluno. Libera o acesso à biblioteca. ([46](46-matricula-e-rematricula-por-portal.md)) |
| `diario.falta.registrada` | Diário | Notificações, Boletim | Aviso ao responsável a cada 5 faltas na disciplina. Atualiza a frequência do boletim. ([61](61-diario-escolar-por-portal.md)) |
| `boletim.resultado.fechado` | Boletim | Matrícula, Notificações | Define avanço ou rematrícula. Avisa o responsável. ([62](62-boletim-e-conselho-de-classe-por-portal.md)) |
| `ocorrencia.registrada` | Ocorrências | Notificações, Conselho | Aviso imediato se a gravidade for grave. Entra na pauta do conselho. ([63](63-ocorrencias-disciplinares-por-portal.md)) |
| `biblioteca.multa.gerada` | Biblioteca | Financeiro | Gera fatura de multa. ([68](68-biblioteca-por-portal.md)) |
| `financeiro.titulo.pago` | Financeiro | Matrícula, Notificações | Libera o bloqueio parcial por inadimplência. Confirma o pagamento ao responsável. ([18](18-regras-modulos-2.md)) |
| `calendario.dia.alterado` | Calendário | Turmas, Diário, Notificações | Recalcula o calendário da turma. Avisa os envolvidos. ([58](58-calendario-e-eventos-por-portal.md)) |
| `relatorio.envio.gerado` | Relatórios | Auditoria | Registra a geração do arquivo do censo. ([69](69-relatorios-e-censo-por-portal.md)) |

Eventos de módulos acadêmicos incluídos por decisão SRC-04, em 03/11/2026 ([75](75-busca-notificacoes-perfil-integracoes-por-escopo.md), seção 5).

Os nomes da v1 (`employee.created`, `exam.performed` etc.) eram em inglês sem módulo. A v2 acrescenta o módulo no nome para evitar colisão.

### 4.1 Envelope obrigatório

```json
{
  "event_id": "0190c2f4-7a1e-7b3c-9d2a-5c8e1f0a6b21",
  "event_type": "hcm.employee.created",
  "schema_version": 1,
  "occurred_at": "2026-11-02T14:03:11-03:00",
  "tenant_id": "…",
  "entity_id": "…",
  "unit_id": "…",
  "producer": "hcm",
  "actor_id": "…",
  "correlation_id": "…",
  "aggregate": { "type": "employee", "id": "…", "version": 7 },
  "payload": { }
}
```

Regras:

- `event_id` é UUID v7 ou v4, gerado pelo produtor. Serve de chave de idempotência.
- `schema_version` é incrementado a cada mudança incompatível do payload. O consumidor aceita a versão que suporta e rejeita as demais para revisão.
- `aggregate.version` permite descartar evento antigo que chegou depois de um mais novo.
- `payload` tem somente identificadores e campos de estado. Ver seção 8.

## 5. Outbox e entrega

1. O produtor grava a mudança de negócio e o evento na mesma transação do banco (tabela `outbox`).
2. Um processo relay lê a `outbox` em ordem, publica na fila e marca o registro como enviado.
3. O consumidor recebe a mensagem, verifica se `event_id` já foi processado (tabela `processed_events` com chave única por consumidor e evento) e só então aplica o efeito.
4. Se o efeito e o registro de `processed_events` estiverem na mesma transação, a entrega duplicada não repete o efeito.

### 5.1 Estados

Estados da fila de envio: `pending` → `queued` → `sent` → `processed`. Estados de exceção: `rejected` (falha definitiva) e `cancelled` (cancelado por regra de negócio).

| Transição | Condição |
|---|---|
| `pending` → `queued` | Relay leu o registro |
| `queued` → `sent` | Fila confirmou recebimento |
| `sent` → `processed` | Consumidor confirmou o efeito |
| `sent` → `rejected` | Consumidor recusou (schema não suportado, regra violada) ou esgotou tentativas |
| `pending` ou `queued` → `cancelled` | Regra de negócio invalidou o evento antes do envio |

### 5.2 Retentativa

- Backoff: 1 min, 5 min, 30 min, 2 h, 12 h. Máximo de 5 tentativas.
- Após a última tentativa, o evento vai para `rejected` e gera alerta ao responsável pelo módulo consumidor.
- Reprocessamento manual é permitido por ação de administrador com permissão `integracao.fila.reprocessar`, registrada em auditoria.

### 5.3 Ordem

- Eventos do mesmo agregado (mesmo `aggregate.type` e `aggregate.id`) são consumidos em ordem de `aggregate.version`.
- Evento com versão menor que a já processada é marcado como `processed` sem efeito, com registro de descarte.

## 6. Contratos síncronos

- Cada módulo publica uma interface de serviço versionada (`Hcm\Contracts\EmployeeReader v1`).
- Toda chamada recebe o `TenantContext`. Chamada sem contexto lança erro antes de executar.
- Timeout de 2 s. Falha de timeout não é retentada automaticamente, porque a escrita pode não ter ocorrido.
- Circuit breaker por par chamador-chamado: após 5 falhas em 30 s, a chamada falha rápido por 60 s.
- Resposta de leitura não expõe campo que a permissão do chamador não cobre (mesma regra de BOPLA em [04](04-api.md), seção 5).

## 7. Integrações obrigatórias da v1

A v1 ([`spec_complementar_integracoes_governanca.md`](anexo-v1/spec_complementar_integracoes_governanca.md), seção 3) lista três integrações. A v2 define a forma de cada uma.

### 7.1 RH ↔ SMT

- **Admissão:** `hcm.employee.created` gera agendamento de exame admissional no SMT.
- **Afastamento:** `hcm.absence.created` registra restrição quando o afastamento tem causa ocupacional.
- **Aptidão:** `smt.exam.performed` atualiza o status de aptidão no RH. O RH recebe status, não o laudo.
- **Evento eSocial** (S-2220, S-2230, S-2240): a montagem do XML é do SMT ou do RH, conforme a decisão de D-08 em [16](16-integracoes-externas.md). A transmissão passa pela integração externa do tenant.

### 7.2 SMT ↔ Suprimentos

- **Estoque mínimo de EPI:** `suprimentos.epi.stock-minimum-reached` gera solicitação de compra.
- **Bloqueio de fornecedor:** `suprimentos.supplier.blocked` ocorre quando CA vence ou documento fica inválido. A regra de bloqueio pertence ao Suprimentos, que consulta o SMT por contrato de leitura para saber o CA vigente.
- **Contrato e ata:** consumo de saldo é movimento no Contratos, disparado pelo Suprimentos.
- **Evidência de reposição e devolução:** registrada no Suprimentos com referência ao CA do SMT, sem duplicar o cadastro do EPI.

### 7.3 RH ↔ Suprimentos

- **Onboarding e offboarding:** `hcm.employee.created` e `hcm.employee.terminated` abrem solicitações de itens e de devolução.
- **Centro de custo e cargo:** `hcm.employee.department-changed` atualiza as requisições em aberto. Requisição já aprovada mantém o centro de custo original, com registro da mudança.
- **Ativos entregues:** histórico no Suprimentos, com `person_id` como referência.

## 8. Dados pessoais e de saúde nos eventos

- Payload de evento carrega identificadores, status e datas. Nome, documento, e-mail e telefone **não** vão no payload. O consumidor busca esses dados por contrato de leitura, com permissão.
- Dado de saúde (laudo, CID, resultado de exame) **nunca** vai no payload. Vai somente o status (`apto`, `inapto`, `apto-com-restricao`) e o ID do exame.
- Evento com dado sensível tem retenção de fila de 7 dias. Após o processamento, o payload é apagado e fica só o registro de metadados.
- Logs de fila mostram tipo, ID, estado e tenant. Nunca o payload completo.

## 9. Modelo de dados da fila (correção da v1)

A v1 (`sys_event_queue`, seção 8.1) usa `entityid` e não tem `tenant_id`. Isso viola [03](03-dominio-tenancy.md), seção 3. A v2 corrige o modelo:

```sql
CREATE TABLE integration_outbox (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  event_id        CHAR(36)     NOT NULL,
  tenant_id       CHAR(36)     NOT NULL,
  entity_id       CHAR(36)     NOT NULL,
  unit_id         CHAR(36)     NULL,
  event_type      VARCHAR(120) NOT NULL,
  schema_version  SMALLINT UNSIGNED NOT NULL DEFAULT 1,
  aggregate_type  VARCHAR(60)  NOT NULL,
  aggregate_id    CHAR(36)     NOT NULL,
  aggregate_version INT UNSIGNED NOT NULL,
  payload         JSON         NOT NULL,
  status          ENUM('pending','queued','sent','processed','rejected','cancelled') NOT NULL DEFAULT 'pending',
  attempts        TINYINT UNSIGNED NOT NULL DEFAULT 0,
  next_attempt_at DATETIME     NULL,
  last_error      VARCHAR(500) NULL,
  correlation_id  CHAR(36)     NOT NULL,
  actor_id        CHAR(36)     NULL,
  created_at      DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  UNIQUE KEY uk_event (event_id),
  INDEX idx_tenant_status (tenant_id, status, next_attempt_at),
  INDEX idx_aggregate (tenant_id, aggregate_type, aggregate_id, aggregate_version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE integration_processed_events (
  consumer     VARCHAR(60) NOT NULL,
  event_id     CHAR(36)    NOT NULL,
  tenant_id    CHAR(36)    NOT NULL,
  processed_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (consumer, event_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Notas sobre o modelo:

- `payload` JSON é apagado após o processamento quando o evento tem dado sensível (seção 8). Nesse caso, a coluna é zerada por job, e o registro de metadados permanece.
- Os identificadores seguem UUID, conforme [03](03-dominio-tenancy.md), seção 2. A v1 misturava `id`, `uuid` e `code`. A v2 usa UUID como identificador público e `id` interno numérico só para ordenação.

## 10. Observabilidade

- Métricas: profundidade da fila por tenant, idade do registro mais antigo em `pending`, taxa de `rejected`, latência de consumo.
- Alerta: `rejected` acima de 0 para evento de dado sensível; idade acima de 15 min para `pending`.
- Painel de integrações (API `GET /api/v1/integrations/queue`, da v1, seção 7.1) exige escopo de tenant e não mostra payload.

## 11. Testes obrigatórios

- Contrato: cada evento tem teste de payload com schema validado.
- Entrega duplicada: mesmo `event_id` processado duas vezes gera um efeito.
- Fora de ordem: versão 3 antes da versão 2 não sobrescreve estado.
- Falha de consumidor: retentativa e transição para `rejected` após 5 tentativas.
- Isolamento: evento de tenant A não é consumido por consumidor de tenant B.
- Dado sensível: payload de exame não contém laudo nem CID.

## 12. Critérios de aceite

- [ ] Todo evento do catálogo (seção 4) tem produtor, consumidores, schema e teste de contrato.
- [ ] Nenhum módulo lê tabela de outro módulo (verificação automatizada por lista de tabelas proibidas).
- [ ] Toda tabela de fila tem `tenant_id NOT NULL`.
- [ ] Nenhum payload de evento contém dado de saúde em texto.
- [ ] Reprocessamento manual é auditado.
