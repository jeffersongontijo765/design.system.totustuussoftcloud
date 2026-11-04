# 18 — Regras de Validação: Cobrança, Notificações, Auditoria, RH e Contábil/Fiscal

> Parte do [SDD v2](00-README.md). Continua [17](17-regras-modulos.md). Padrão em [15](15-validacoes.md). Eventos e dono de dados em [14](14-integracao-modulos.md). Integrações de cobrança em [16](16-integracoes-externas.md).
> **Fonte:** especificações da v1 citadas em cada módulo. Regras não definidas na v1 aparecem como **[Pendente]**.

---

## 1. Defeitos transversais

| ID | Defeito | Onde | Correção |
|---|---|---|---|
| T-01 | Sem `tenant_id`. Contagem nos DDL: Cobrança (9 tabelas) e Auditoria (0 tabelas com DDL, mas referências a tenant ausentes). | Cobrança, Auditoria | `tenant_id` NOT NULL e índice composto ([03](03-dominio-tenancy.md)). |
| T-02 | RH e Contábil/Fiscal sem DDL. | RH, Contábil | DDL antes da implementação. |
| T-04 | Estado calculado armazenado. Cobrança tem `overdue` e `viewed` no `ENUM` de `billing_invoices.status`. `overdue` depende de data; `viewed` é fato de evento. | Cobrança | Ver seção 2.3. |
| T-07 | Duplicidade de módulo. RH e Pessoas (HCM) cobrem o mesmo colaborador, com ficha, treinamento, férias e afastamento. | RH, Pessoas | Decidir a fronteira. Proposta na seção 4.1. |

## 2. Cobrança e Mensalidades

### 2.1 Entidades com DDL na v1

`billing_plans`, `billing_subscriptions`, `billing_invoices`, `billing_payments`, `billing_discounts`, `billing_automations`, `billing_nfse`, `billing_collection_rules` e uma tabela de régua. Valores em `DECIMAL(12,2)` e alíquota de ISS em `DECIMAL(5,4)`. Esses tipos estão corretos. Os valores em `DECIMAL(12,2)` limitam a fatura a R$ 9,99 bilhões, o que basta.

### 2.2 Campos e regras

| Campo | Regra |
|---|---|
| `plans.base_amount` | Maior ou igual a zero. |
| `plans.min_amount`, `max_amount` | `min_amount ≤ base_amount ≤ max_amount`, quando informados. |
| `subscriptions.negotiated_amount` | Dentro de `[min_amount, max_amount]` do plano, quando houver faixa. |
| `subscriptions.discount_percent` | Entre 0 e 100. |
| `invoices.gross_amount` | Maior que zero. |
| `invoices.net_amount` | **Calculado pelo servidor:** `gross - discount + fine + interest`. Diferença é `422` ([17](17-regras-modulos.md), seção 2.2). |
| `invoices.paid_amount` | Não pode exceder `net_amount` sem registro de crédito. |
| `payments.amount` | Maior que zero. Soma das baixas por fatura não pode exceder o saldo. |
| `discounts.value` | Maior que zero. Para `modality = percent`, até 100. |
| `nfse.iss_amount` | Calculado: `iss_base × iss_rate`. Diferença é `422`. |
| `nfse.iss_base` | Não pode exceder `gross_amount - deductions`. |

### 2.3 Estados da fatura

A v1 define: `draft`, `pending`, `sent`, `viewed`, `paid`, `partial`, `overdue`, `negotiated`, `cancelled`, `refunded`.

Proposta de correção (T-04):

| Estado armazenado | Significado |
|---|---|
| `draft` | Não emitida |
| `issued` | Emitida e enviada ao devedor (substitui `pending`, `sent`) |
| `partial` | Baixa parcial |
| `paid` | Quitada |
| `negotiated` | Substituída por acordo; original preservado |
| `cancelled` | Cancelada antes de pagamento |
| `refunded` | Estornada, com movimento de estorno |

Calculados, não armazenados:

- `viewed`: existe registro em `invoice_views`.
- `overdue`: `status IN (issued, partial) AND due_date < data de referência`.

Transições:

| De | Para | Condição |
|---|---|---|
| `draft` | `issued` | Valor e vencimento válidos; aprovação se a política exigir |
| `issued` ou `partial` | `paid` | Soma das baixas igual a `net_amount` |
| `issued` | `partial` | Baixa menor que o saldo |
| `issued` ou `partial` | `negotiated` | Acordo registrado com nova fatura vinculada |
| `paid` | `refunded` | Estorno pelo gateway ou registro manual com motivo; novo movimento |
| `draft` ou `issued` | `cancelled` | Sem baixa registrada |

### 2.4 Pagamento e baixa

- Baixa com `write_off_type = automatic` só pode ser feita por retorno do gateway com assinatura validada ([16](16-integracoes-externas.md), seção 8).
- Baixa manual exige `write_off_type = manual`, motivo e permissão `cobranca.baixa.manual`. Acima de R$ 1.000, exige segundo aprovador. Configurável por unidade. Decidido pelo autor em 03/11/2026.
- Pagamento duplicado com o mesmo `NSU/TID` é recusado. Chave única por `gateway + NSU/TID`.
- Pagamento não pode ser registrado em fatura `cancelled` ou `refunded`.

### 2.5 Descontos e bolsas

- Desconto por pontualidade só se aplica se o pagamento ocorrer até a data limite do plano.
- Regras combinadas: a política de acumulatividade define se dois descontos somam. Não acumulam: vale o maior. Configurável por entidade. Decidido pelo autor em 03/11/2026.
- Bolsa e isenção exigem documento anexado e data de validade ([15](15-validacoes.md), seção 4.3).

### 2.6 Régua de cobrança: pontos que exigem parecer

A v1 define sete etapas de cobrança, de D+1 a D+90, com canais e ações (`spec_gestao_billing_cobranca_mensalidades.md`, seção 11). Três pontos precisam de parecer antes de implementar:

| Etapa | Ação na v1 | Risco | Tratamento proposto |
|---|---|---|---|
| D+10 SMS e e-mail; D+5 WhatsApp | Cobrança por canal de mensagem | Consentimento e LGPD ([07](07-privacidade-lgpd.md)) | **(jurídico)** base legal da comunicação de cobrança. Canal só para titular que informou o contato para esse fim. |
| D+30 aviso de negativação | Inclusão em cadastro de inadimplentes | Exige notificação prévia e regras do cadastro de crédito | **(jurídico)** prazo e forma de notificação antes da negativação. |
| D+90 bloqueio de acesso ao portal | Bloqueio do portal do aluno | Interrupção de serviço educacional a menor de idade | **(jurídico)** bloqueio não deve impedir acesso a documentos obrigatórios nem a matrícula de menor. Propor bloqueio parcial. |

### 2.7 Nota fiscal de serviço (NFSe)

- Emissão só para fatura `paid` ou `partial`, conforme política municipal **[Pendente: regra por município]**.
- Status `pending` → `processing` → `issued` ou `rejected`. `cancelled` só a partir de `issued`, com o cancelamento transmitido ao município.
- Integração com o município é externa ([16](16-integracoes-externas.md), seção 3). Resposta de rejeição guarda o código de erro do município.

### 2.8 Testes específicos

- Fatura com desconto acima do bruto: `422`.
- Dois pagamentos com o mesmo NSU/TID: um movimento.
- Fatura `paid` tentando ser cancelada: `409`.
- Desconto de pontualidade após a data limite: não aplicado.
- Régua no D+90 com aluno menor e documento obrigatório pendente: bloqueio parcial.

## 3. Notificações

### 3.1 Estados (v1, seção 6, validada)

A v1 define: `draft`, `in_review`, `scheduled`, `queued`, `processing`, `sent`, `delivered`, `read`, `failed`, `archived`, `cancelled`.

As transições da v1 estão corretas e são adotadas. Regras adicionais:

| Regra | Detalhe |
|---|---|
| Estados terminais | `read`, `archived`, `cancelled` não voltam sem ação explícita autorizada. |
| Reenvio | Cria nova tentativa. Não sobrescreve a anterior. |
| Cancelamento | Preserva histórico e auditoria. |
| Falha | Classificada por tipo: validação, transporte, provedor, conteúdo, autorização, timeout ou desconhecida. Só transporte e timeout são retentados. |

### 3.2 Validações de envio

- Campos obrigatórios por canal validados antes do envio: e-mail exige endereço verificado; SMS e WhatsApp exigem número em E.164 ([15](15-validacoes.md), seção 2).
- Conteúdo sem público-alvo válido é bloqueado.
- Anexo validado por tamanho, tipo e política de segurança ([15](15-validacoes.md), seção 4.3).
- Toda operação de envio é idempotente pela `idempotency_key`.
- Payload validado por schema. Campo obrigatório documentado por tipo de evento.

### 3.3 Dados sensíveis

- Notificação de saúde ou de RH não mostra diagnóstico nem valor de salário no corpo. Mostra aviso e link autenticado.
- Corpo de mensagem guardado com retenção configurável ([07](07-privacidade-lgpd.md)).

## 4. Auditoria

### 4.1 Fronteira com RH e Pessoas (T-07)

Proposta: RH e Pessoas são **um único módulo HCM** com submódulos. O cadastro de colaborador, a ficha e o vínculo ficam em Pessoas. Férias, afastamento, treinamento, ponto e folha ficam em RH/HCM. Essa é a decisão a confirmar.

### 4.2 Regras de auditoria

| Regra | Detalhe |
|---|---|
| Imutabilidade | Registro de auditoria não é alterado nem apagado por usuário. Correção gera novo registro referenciando o original. |
| Integridade | Cada registro guarda hash SHA-256 do conteúdo e do registro anterior do mesmo tenant (cadeia). Quebra da cadeia gera alerta. |
| Expurgo | Só por job de retenção, com aprovação para retenção estendida, e deixa um registro do expurgo. |
| Mascaramento | Campo pessoal mascarado na visualização; valor completo só com permissão e motivo. |
| Acesso | Leitura da auditoria é ela própria auditada. |
| Eventos obrigatórios | Login, falha de login, bloqueio, alteração de permissão, exportação, acesso a dado sensível, consulta por CPF ([21](21-busca-e-armazenamento.md), seção 6.8), alteração de política. |

Esses pontos reforçam [05](05-seguranca.md), seção 2, e [07](07-privacidade-lgpd.md), seção 6.

## 5. RH (fronteira com Pessoas)

Conforme a proposta da seção 4.1, as regras abaixo são do submódulo RH/HCM.

| Regra | Detalhe |
|---|---|
| Bloqueio por documento faltante | Afastamento, férias ou admissão são bloqueados se documento obrigatório não estiver anexado (v1, seção 7). |
| Treinamento obrigatório | Pendente bloqueia a função ou a tarefa, conforme regra do cargo (v1, seção 5.2). |
| Edição em campo sensível | Bloqueada sem permissão específica (v1, seção 3.3). |
| Visibilidade | Gestor vê só a própria equipe; RH vê a unidade; nenhum perfil vê salário de outro sem permissão (v1, seção 3.2). |
| Férias | Fim não anterior ao início; período não pode exceder o direito acumulado **[Pendente: regra CLT art. 130 e fracionamento]**. |
| Afastamento | Sobreposição com afastamento ativo é recusada. |

**Defeito:** a v1 não tem DDL do RH (T-02). Sem DDL, as regras acima não podem ser testadas.

## 6. Contábil e Fiscal

### 6.1 Controles de período (v1, seção 11.1)

| Regra | Detalhe |
|---|---|
| Período fechado | Edição e exclusão de lançamento bloqueadas. Correção só por lançamento de ajuste no período aberto, com motivo. |
| Competência | Data do lançamento dentro da competência declarada; competência inválida é `422`. |
| Fechamento | Bloqueado com pendência aberta de aprovação ou de conciliação. |
| Correção | Sempre com motivo obrigatório (v1, seção 8.1). |
| Aprovação automática | Só por regra cadastrada e auditada (v1, seção 10). |

### 6.2 Estados

| Entidade | Estados |
|---|---|
| Período | `aberto`, `em_fechamento`, `fechado`, `reaberto` (com justificativa e permissão administrativa) |
| Lançamento | `rascunho`, `em_validacao`, `aprovado`, `estornado` |
| Obrigação fiscal | `pendente`, `transmitida`, `paga`, `em_atraso` (calculado por data) |

**Defeito:** sem DDL (T-02). Não há campos, tipos de valor nem chaves definidos para validar.

## 7. Lacunas

| # | Lacuna | Dono sugerido |
|---|---|---|
| L-07 | Parecer sobre base legal, negativação e bloqueio de portal (seção 2.6) | Jurídico |
| L-08 | Limite de valor para baixa manual e aprovação de desconto | Financeiro |
| L-09 | Política de acumulatividade de descontos | Financeiro |
| L-10 | Regra de NFSe por município | Fiscal |
| L-11 | Fronteira RH/Pessoas (seção 4.1) | Produto |
| L-12 | Regra CLT de férias e fracionamento | Jurídico, RH |
| L-13 | DDL de RH e Contábil/Fiscal | RH, Contábil |

## 8. Critérios de aceite

- [ ] Todas as tabelas de Cobrança têm `tenant_id NOT NULL` (T-01).
- [ ] `overdue` e `viewed` saem de `status` e passam a ser calculados (T-04).
- [ ] Régua de cobrança com parecer jurídico registrado antes de ativar cada etapa (L-07).
- [ ] Auditoria com cadeia de hash e registros imutáveis (seção 4.2).
- [ ] RH e Contábil com DDL escrito (T-02).
