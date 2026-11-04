# 22 — CRM: Dois Contextos, Canais de Captação e Papéis

> Parte do [SDD v2](00-README.md). Substitui e amplia a v1 [`spec_crm_funil_comercial.md`](anexo-v1/spec_crm_funil_comercial.md) (ver [19](19-regras-modulos-3.md), seção 6). Integrações de canal em [16](16-integracoes-externas.md). Consentimento e papéis de LGPD em [07](07-privacidade-lgpd.md). Permissões em [06](06-identidade-acesso.md). Pagamentos em [20](20-pagamentos-seguranca.md). Chatbots e captação usam a mesma camada de mensagens descrita aqui.
> **Interpretação:** "papilanes" foi lido como **papéis** (perfis de usuário e de operação). Se a intenção for outra, esta seção será revisada.
> **Status:** D-16, D-17 e D-18 decididas pelo autor em 02/11/2026 (seção 9).

---

## 1. Dois CRMs, não um

Existem dois CRMs com donos, leads e finalidades diferentes. Misturá-los seria erro de dados e de LGPD.

| Aspecto | CRM da plataforma (vendas do SaaS) | CRM do tenant (captação de alunos) |
|---|---|---|
| Quem vende | TotusTuus SoftCloud | Colégio, faculdade ou instituição (tenant) |
| Quem é o lead | Instituição ou empresa que pode contratar o SaaS | Aluno, responsável ou candidato |
| Dono dos dados (controlador, LGPD) | Plataforma | Tenant |
| Papel da plataforma sobre os dados | Controlador | Operadora, quando a plataforma executa o canal para o tenant |
| Funil | Pré-venda, demonstração, proposta, contrato, implantação | Interesse, contato, pré-cadastro, inscrição, documentos, matrícula |
| Dados pessoais típicos | Nome do decisor, e-mail corporativo, telefone comercial | Nome do aluno e do responsável, telefone, e-mail, série de interesse |
| Dados que nunca entram | Dado de aluno de tenant | Dado comercial da plataforma, preço negociado com outro tenant |
| Banco | **Banco master** (`totustuus.matriz.bd`) | **Banco da unidade** (um por entidade + unidade, ver [03](03-dominio-tenancy.md), seção 1.1) |

**Regra de separação:** nenhum registro de tenant aparece no CRM da plataforma, e nenhum registro do CRM da plataforma aparece em tenant. A ligação entre os dois é apenas o contrato comercial.

**Operação pela plataforma de canal de tenant:** quando o chatbot da plataforma atende o aluno de um tenant, a plataforma atua como operadora. Isso exige contrato de tratamento de dados entre plataforma e tenant ([07](07-privacidade-lgpd.md), seção 7).

---

## 2. Canais

### 2.1 CRM da plataforma

| Canal | Entrada | Identidade capturada | Atendimento | Consentimento |
|---|---|---|---|---|
| Chatbot no site (totustuussoftcloud.com.br) | Widget no site institucional | E-mail corporativo, telefone, nome, instituição | Bot com handoff para vendedor | Aviso e aceite antes de coletar |
| Chatbot WhatsApp | Número oficial da plataforma | Número de telefone | Bot com handoff | Opt-in na primeira mensagem |
| Chatbot Telegram | Bot oficial da plataforma | Identificador do usuário e, se fornecido, telefone | Bot com handoff | Opt-in na primeira mensagem |
| Chatbot Instagram | Conta oficial, mensagem direta | Identificador da conta | Bot com handoff | Opt-in e aviso de que o contato é registrado |
| Chatbot Messenger | Página oficial | Identificador da página | Bot com handoff | Opt-in e aviso de que o contato é registrado |
| Telefone | Ligação recebida ou feita | Número e nome informado | Vendedor | Aviso de gravação, quando houver gravação |
| Presencial | Evento, visita, feira | Cartão ou formulário em papel digitalizado | Vendedor | Termo no formulário, com aceite |

### 2.2 CRM do tenant (captação de alunos)

| Canal | Entrada | Identidade capturada | Atendimento | Consentimento |
|---|---|---|---|---|
| Formulário embutido no site do tenant (iframe ou script) | Página do tenant, com origem permitida | Nome, telefone, e-mail, série de interesse | Equipe de admissões | Aceite com finalidade, na própria página |
| Chatbot WhatsApp do tenant | Número do tenant ([16](16-integracoes-externas.md), D-07) | Número de telefone | Bot do tenant com handoff | Opt-in na primeira mensagem |
| Chatbot Telegram do tenant | Bot do tenant | Identificador e telefone, se fornecido | Bot com handoff | Opt-in |
| Chatbot Instagram do tenant | Conta do tenant | Identificador da conta | Bot com handoff | Opt-in |
| Chatbot Messenger do tenant | Página do tenant | Identificador da página | Bot com handoff | Opt-in |
| Telefone | Central do tenant | Número e nome | Atendente | Aviso de gravação |
| Presencial | Visita, feira, open day | Ficha de inscrição | Atendente | Termo de consentimento na ficha |

**Regra comum a todos os canais:** a captura começa só depois do aviso de finalidade. Lead sem consentimento de contato para a finalidade informada fica em estado `sem_consentimento` e não recebe mensagem de marketing.

---

## 3. Regras por canal

| Regra | Aplicação |
|---|---|
| Identificação de bot | O chatbot se identifica como automático na primeira mensagem e oferece transferência para humano. |
| Dados que o bot não coleta | Dado de saúde, CPF completo, número de cartão, senha e documento de imagem. Quando necessário para a matrícula, o coleta acontece em formulário autenticado. |
| Pagamento | Nenhum pagamento é feito no chat. O bot envia link de pagamento ([20](20-pagamentos-seguranca.md)). |
| Opt-out | Palavra de saída reconhecida em todos os canais (`PARAR`, `SAIR`). Efeito imediato sobre marketing. |
| Horário e frequência | Limite de mensagens proativas por lead e por dia. Mensagem de cobrança segue a régua de [18](18-regras-modulos-2.md), seção 2.6. |
| Transcrição | Guardada como interação do lead, com retenção configurável por tenant ([07](07-privacidade-lgpd.md), seção 5). |
| Gravação de ligação | Só com aviso no início e registro do consentimento. |
| Mensagem de terceiro | Nunca encaminhar a conversa a outro lead ou a outro tenant. |
| Políticas das plataformas | Cada canal cumpre as regras de uso da plataforma de mensagens (WhatsApp Business, Telegram Bot API, Meta para Instagram e Messenger). Mudança de regra vira tarefa de adequação. |
| Chatbot com IA (D-18) | A IA responde **somente com base em fonte cadastrada** (catálogo de cursos, preços, calendário, FAQ aprovada). Pergunta fora da fonte não recebe resposta inventada: é encaminhada para humano. Preço, bolsa, prazo ou condição nunca saem de fonte não cadastrada. |
| Abertura de ticket sem IA (D-18) | Todo ponto de atendimento oferece a opção "Abrir ticket" por menu fixo, sem interpretação por IA. O ticket é criado no módulo de atendimento ([19](19-regras-modulos-3.md), seção 7) com categoria escolhida no menu e texto digitado pelo contato, guardado como texto literal. Esse caminho funciona mesmo com IA desligada. |
| Injeção de instrução | Texto do lead é dado, nunca instrução ao bot. Teste contra tentativa de alterar o comportamento do bot ([05](05-seguranca.md)). |

---

## 4. Papéis do CRM

### 4.1 CRM da plataforma

| Papel | Escopo | Pode | Não pode |
|---|---|---|---|
| Pré-vendas (SDR) | Leads da plataforma | Qualificar, agendar demonstração, registrar interação | Fechar proposta, alterar preço, ver contrato |
| Vendedor (AE) | Leads e oportunidades atribuídos a ele | Criar proposta, avançar funil até negociação | Aprovar desconto acima da alçada, alterar contrato assinado |
| Gerente comercial | Equipe | Atribuir leads, aprovar desconto dentro da alçada, ver funil da equipe | Aprovar a própria proposta |
| Operador de chatbot | Conversas em atendimento | Atender, transferir, registrar | Acessar carteira fora da fila |
| Sucesso do cliente | Clientes ativos (tenants) | Acompanhar implantação e uso | Alterar cobrança |

### 4.2 CRM do tenant

| Papel | Escopo | Pode | Não pode |
|---|---|---|---|
| Atendente de admissões | Leads da unidade | Atender, registrar interação, agendar visita | Exportar base, ver dado de matrícula de outro aluno |
| Coordenador de admissões | Leads de todas as unidades permitidas | Redistribuir, ver funil, configurar régua de contato | Alterar a finalidade de consentimento |
| Gestor comercial da entidade | Entidade | Ver indicadores, configurar canais | Ver dado pessoal além da lista de leads com permissão de exportação |
| Operador de bot do tenant | Conversas do canal | Atender e transferir | Editar a base de conhecimento do bot sem permissão |
| Responsável pela unidade | Unidade | Ver funil da unidade | Ver outra unidade |

---

## 5. Papéis dos departamentos

Papéis internos da organização que usa o sistema (plataforma ou tenant). Cada papel define acesso a módulos. Os nomes de permissão seguem `modulo.recurso.acao` ([06](06-identidade-acesso.md), seção 9).

| Papel | Módulos principais | Permissões-chave | Segregação de funções |
|---|---|---|---|
| **Financeiro** | Financeiro, Cobrança, Pagamentos | Emitir e baixar títulos; solicitar estorno; conciliar | Não aprova o próprio estorno |
| **Contábil** | Contábil e Fiscal, Financeiro (leitura) | Lançar, fechar período, exportar para ERP | Não fecha período com lançamento que criou sem revisão |
| **Fiscal** | Contábil e Fiscal, Cobrança (NFSe) | Emitir e cancelar NFSe, apurar tributos | Cancelamento exige aprovação do contábil |
| **Comercial** | CRM (conforme 4.1 ou 4.2), Contratos (leitura) | Criar proposta, negociar | Não aprova desconto acima da alçada |
| **Compras** | Suprimentos (requisição, pedido, cotação), Contratos | Criar cotação e pedido; cadastrar fornecedor | Não aprova a própria requisição; não recebe a própria compra |
| **Almoxarifado** | Suprimentos (estoque) | Registrar recebimento e movimento | Não ajusta estoque sem motivo e aprovação |
| **Aprovador de compras** | Suprimentos | Aprovar requisição dentro da alçada | Não é o solicitante |
| **RH** | HCM (Pessoas e RH) | Cadastrar colaborador, férias, afastamento | Campos salariais só com permissão própria |
| **Folha** | HCM (folha) | Processar folha | Folha fechada não é alterada |
| **SMT** | Segurança e medicina do trabalho | Registrar ASO, CAT, EPI | Resultado de exame só por profissional responsável |
| **Acadêmico (secretaria)** | Acadêmico | Matrícula, documentos | Nota só pelo professor da turma |
| **Professor** | Acadêmico (turmas próprias) | Lançar nota, presença, diário | Só turmas vinculadas |
| **Jurídico** | Contratos, Documentos, Auditoria (leitura) | Parecer, bloqueio legal | Não altera contrato assinado |
| **Encarregado (DPO)** | Privacidade, Auditoria, Busca por CPF | Relatório de impacto, relatório ao titular, aprovação de finalidade | Não opera o módulo que audita |
| **Segurança** | Auditoria, Configuração de MFA, Cofre (leitura de status) | Investigar, bloquear conta | Não concede permissão a si mesmo |
| **TI / Operação** | Infraestrutura, filas, monitoramento | Operar serviços | Sem acesso a dado pessoal de tenant |

**Regra geral de segregação:** nenhuma pessoa cria e aprova o mesmo objeto financeiro, de compra ou de consentimento. A aplicação verifica isso, não só o processo.

---

## 6. Funil e estados

### 6.1 CRM da plataforma

Leads: `novo` → `contatado` → `qualificado` → `demonstracao` → `proposta` → `negociacao` → `ganho` ou `perdido`.
Após ganho: `implantacao` → `ativo`.

Estados de lead descartado: `desqualificado`, `sem_consentimento`, `duplicado`.

### 6.2 CRM do tenant

Leads: `interessado` → `contatado` → `pre_cadastro` → `inscrito` → `documentos_pendentes` → `matriculado`.
Estado de saída: `desistente`, `sem_consentimento`, `duplicado`.

Regras:

- "Fechado perdido" exige motivo (preço, concorrência, sem vaga, timing ou outro), como já definido na v1.
- Lead `matriculado` nunca volta a `interessado`. Novo interesse gera novo lead, vinculado ao anterior.
- Vaga do curso é reservada só em `inscrito`, com bloqueio de concorrência ([15](15-validacoes.md), seção 7).

---

## 7. Captura por formulário embutido

- Origem permitida: lista de domínios cadastrada por tenant. Outro domínio não recebe o envio.
- O formulário é carregado de origem da plataforma com `frame-ancestors` limitado aos domínios permitidos.
- Campos mínimos. A série de interesse é lista fechada.
- Proteção contra robô: desafio antes do envio, sem terceiro não aprovado.
- Aceite de finalidade e de contato antes do envio, com texto e versão registrados.
- Confirmação por e-mail ou WhatsApp quando marketing estiver marcado (duplo opt-in).
- Nenhum script de terceiro na página do formulário além dos aprovados ([08](08-frontend-design-system.md), seção 2).

---

## 8. Dados

Tabelas mínimas. Todas com `tenant_id` (no CRM da plataforma, `tenant_id` aponta para a própria plataforma).

```sql
CREATE TABLE crm_leads (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36)     NOT NULL,
  tenant_id       CHAR(36)     NOT NULL,
  context         ENUM('plataforma','tenant') NOT NULL,
  origin_channel  ENUM('site','formulario','whatsapp','telegram','instagram','messenger','telefone','presencial','indicacao') NOT NULL,
  owner_uuid      CHAR(36)     NULL,
  unit_id         CHAR(36)     NULL,
  name            VARCHAR(150) NOT NULL,
  phone_e164      VARCHAR(20)  NULL,
  email           VARCHAR(254) NULL,
  email_hash      CHAR(64)     NULL,
  phone_hash      CHAR(64)     NULL,
  status          VARCHAR(40)  NOT NULL,
  lost_reason     VARCHAR(60)  NULL,
  created_at      DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  UNIQUE KEY uk_lead_uuid (uuid),
  INDEX idx_tenant_status (tenant_id, context, status),
  INDEX idx_tenant_phone (tenant_id, phone_hash),
  INDEX idx_tenant_email (tenant_id, email_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE crm_consents (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36)     NOT NULL,
  tenant_id       CHAR(36)     NOT NULL,
  lead_id         BIGINT UNSIGNED NOT NULL,
  purpose         ENUM('contato_comercial','marketing','admissao','cobranca','gravacao_ligacao') NOT NULL,
  channel         VARCHAR(20)  NOT NULL,
  text_version    VARCHAR(40)  NOT NULL,
  granted_at      DATETIME(6)  NOT NULL,
  revoked_at      DATETIME(6)  NULL,
  evidence_ref    VARCHAR(255) NULL,
  UNIQUE KEY uk_consent_uuid (uuid),
  INDEX idx_lead_purpose (tenant_id, lead_id, purpose),
  FOREIGN KEY (lead_id) REFERENCES crm_leads(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Notas:

- `email_hash` e `phone_hash` são HMAC com pepper, para deduplicação e busca exata ([15](15-validacoes.md), seção 2). Dado em claro é cifrado conforme [05](05-seguranca.md).
- Consentimento nunca é apagado. Revogação preenche `revoked_at`.
- Interações (mensagens, ligações, visitas) vão para tabela própria, com canal, direção e referência à transcrição. A transcrição segue a retenção do tenant.
- Deduplicação: mesmo `phone_hash` ou `email_hash` dentro do mesmo `tenant_id` e contexto gera alerta de possível duplicidade, sem fusão automática.

---

## 9. Decisões

| # | Decisão | Proposta | Alternativa e condição de falha |
|---|---|---|---|
| D-16 | Separação dos CRMs | **Decidida:** CRM da plataforma no banco master; CRM do tenant no banco de cada unidade (entidade + unidade). | — |
| D-17 | Contas de canal (WhatsApp, Telegram, Instagram, Messenger) | **Decidida:** no CRM da plataforma, contas oficiais da plataforma. No CRM do tenant, contas do próprio tenant, conforme D-07 ([16](16-integracoes-externas.md), seção 6). | — |
| D-18 | Uso de IA no chatbot | **Decidida:** IA só com fonte cadastrada; pergunta fora da fonte vai para humano; sempre disponível a opção "Abrir ticket" sem IA (seção 3) | — |

---

## 10. Lacunas

| # | Lacuna | Dono sugerido | Situação em 04/11/2026 |
|---|---|---|---|
| LAC-21 | Texto de aceite de finalidade por contexto | Jurídico | Aberta (jurídico) |
| LAC-22 | Limite de mensagens proativas por canal | Comercial, Jurídico | Parcial: padrão seguro provisório DP-08 ([80](80-decisoes-por-padrao.md)); o limite por canal continua dependendo do jurídico |
| LAC-23 | Alçada de desconto do CRM da plataforma | Comercial | Resolvida por padrão: DP-07 ([80](80-decisoes-por-padrao.md)). Parâmetro sem valor inventado; até a configuração, todo desconto fora da regra passa pelo gerente comercial |
| LAC-24 | Retenção de transcrição e de gravação de ligação | Jurídico, DPO | Aberta (jurídico): ATD-03 ([32](32-atendimento-privacidade-por-portal.md)) |
| LAC-25 | Contrato de operadora entre plataforma e tenant para atendimento de canal | Jurídico | Aberta (jurídico) |

---

## 11. Critérios de aceite

- [ ] Nenhum lead de tenant aparece no CRM da plataforma, e o contrário (teste de isolamento).
- [ ] Todo canal da seção 2 tem regra de consentimento antes da primeira mensagem proativa.
- [ ] Todo papel das seções 4 e 5 tem permissões testadas, incluindo as restrições.
- [ ] Segregação de funções testada nas operações financeiras, de compra e de consentimento.
- [ ] Chatbot se identifica como automático e transfere para humano.
- [ ] Formulário embutido só envia para origem permitida.
