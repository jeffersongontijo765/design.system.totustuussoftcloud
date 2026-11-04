# 20 — Pagamentos e Recebimentos: Segurança, Validação e Conformidade

> Parte do [SDD v2](00-README.md). Integrações com gateways em [16](16-integracoes-externas.md), seção 8. Validação geral em [15](15-validacoes.md). Regras de cobrança em [18](18-regras-modulos-2.md), seção 2. Criptografia e cofre em [05](05-seguranca.md).
> **Status:** requisitos de segurança e de validação. Decisões de fluxo de recursos (seção 2) precisam de aprovação do autor. Conformidade PCI DSS e BCB exige parecer antes da produção.

---

## 1. Princípios

1. **Nenhum dado de cartão toca os servidores da plataforma.** Captura é feita pelos campos hospedados do provedor (iframe ou SDK), e o sistema recebe só um token.
2. **O valor é sempre calculado no servidor.** O valor enviado pelo navegador é ignorado e comparado. Diferença é recusada.
3. **Toda movimentação de dinheiro passa por um ledger de partidas dobradas, somente de inserção.** Saldo é derivado do ledger, nunca editado.
4. **Todo evento de provedor é autenticado antes de qualquer efeito.** Webhook sem assinatura válida não altera estado.
5. **Toda operação é idempotente.** Repetir uma chamada, um webhook ou um job não gera segundo efeito financeiro.
6. **Privilégio mínimo e separação de funções.** Quem cria um estorno não o aprova. Quem configura a conta do gateway não consulta o cartão de um pagador.
7. **Falha fecha, não abre.** Em dúvida sobre status, a operação fica `pendente_conciliacao`, sem liberar produto nem recurso.

## 2. Fluxo de recursos

**[Decidida D-10, seção 19]** Quem recebe o dinheiro?

| Opção | Mecanismo | Vantagem | Risco e condição de falha |
|---|---|---|---|
| (a) Conta do tenant no gateway (**proposta**) | Cada entidade tem a própria conta no provedor (D-07). O dinheiro vai direto para ela. A plataforma só registra. | Plataforma não custodia recursos. Menor exigência regulatória. | Depende de o tenant manter a conta e as credenciais. A plataforma precisa conciliar contas que não controla diretamente. |
| (b) Conta da plataforma com repasse | A plataforma recebe e repassa ao tenant. | Um único ponto de conciliação. | A plataforma passa a custodiar recursos de terceiros. Exige autorização de instituição de pagamento ou arranjo com instituição autorizada. **(jurídico)** Falha de repasse vira passivo da plataforma. |
| (c) Split no provedor | O provedor divide o pagamento entre a plataforma (taxa) e o tenant. | Taxa automática, sem custódia da plataforma. | Depende de suporte do provedor e de contrato de subcontas. |

Padrão desta versão: (a). A plataforma não guarda saldo de tenant. Se a escolha for (b) ou (c), esta seção será revisada.

## 3. Escopo PCI DSS

Objetivo: manter a plataforma no menor escopo possível (SAQ A ou equivalente).

| Requisito | Regra |
|---|---|
| Número do cartão (PAN) | Nunca transita, nunca é gravado, nunca é logado. Captura só pelo campo hospedado do provedor. |
| CVV / CVC | Nunca é gravado em nenhum momento, nem criptografado, nem em memória além da autorização. |
| Token | Armazenado. Formato `provider_token_id`. Sem utilidade fora do provedor e da conta do tenant. |
| Dado exibido | Somente marca, final (4 dígitos), validade mês/ano e nome parcial, quando o provedor devolve. |
| Página de pagamento | Carregada apenas de origem permitida. Política CSP restrita a `frame-src` e `script-src` do provedor, com SRI ([08](08-frontend-design-system.md), seção 2). |
| Logs e erros | Filtro que remove qualquer sequência de 13 a 19 dígitos com validação de Luhn antes de gravar log ou enviar erro. |
| Auditoria | Registra tokens mascarados e identificadores, nunca dados brutos de cartão. |
| Dados de teste | Cartões de teste do provedor apenas em ambiente `sandbox` ([16](16-integracoes-externas.md), seção 4). |

**Verificação:** varredura automatizada do código, dos logs e do banco por padrão de PAN antes de cada release.

## 4. Valor e moeda

| Regra | Detalhe |
|---|---|
| Representação | **[Decidida D-11, seção 19]** Inteiros em centavos (`BIGINT`, por exemplo `1234` = R$ 12,34). A v1 usa `DECIMAL(12,2)`, que é aceitável para exibição, mas arredondamento em cálculo de juros e multa pode gerar diferença de centavo. Converter para centavos antes de qualquer cálculo. |
| Cálculo | Juros, multa e desconto calculados no servidor, com regra de arredondamento única do tenant ([15](15-validacoes.md), seção 4.2). |
| Comparação | Valor cobrado deve ser igual ao valor da fatura calculado no momento da cobrança. Diferença é recusada. |
| Moeda | Só a moeda da conta do tenant. Moeda diferente é `422`. |
| Limites | Mínimo e máximo por meio de pagamento, configurados por tenant. Valor acima do limite exige step-up de MFA. Padrão de R$ 1.000 por operação, confirmado pelo autor em 03/11/2026. |
| Valor negativo | Nunca em cobrança. Crédito é lançamento próprio. |

## 5. Ledger

Todo movimento de dinheiro, inclusive taxa, estorno e chargeback, gera partidas dobradas em tabela append-only.

```sql
CREATE TABLE payment_ledger_entries (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36)     NOT NULL,
  tenant_id       CHAR(36)     NOT NULL,
  transaction_id  CHAR(36)     NOT NULL,
  account_code    VARCHAR(40)  NOT NULL,
  direction       ENUM('debit','credit') NOT NULL,
  amount_cents    BIGINT UNSIGNED NOT NULL,
  currency        CHAR(3)      NOT NULL,
  posted_at       DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  created_by      CHAR(36)     NULL,
  UNIQUE KEY uk_uuid (uuid),
  INDEX idx_tenant_tx (tenant_id, transaction_id),
  INDEX idx_tenant_account (tenant_id, account_code, posted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Regras:

- Tabela sem `UPDATE` nem `DELETE` para a aplicação. Permissão de banco concedida só `INSERT` e `SELECT`.
- Cada transação tem soma de débitos igual à soma de créditos, verificada na mesma transação de banco. Divergência reverte a operação.
- Correção é lançamento de estorno, nunca alteração.
- Saldo de conta é consulta agregada, com cache invalidado a cada inserção.
- `amount_cents` é sempre positivo. Direção indica o sinal.

## 6. Ciclo de vida da transação

### 6.1 Estados

| Estado | Significado |
|---|---|
| `criada` | Intenção registrada, sem chamada ao provedor |
| `autorizacao_pendente` | Enviada ao provedor, aguardando resposta |
| `autorizada` | Aprovada, ainda não capturada (cartão com captura posterior) |
| `capturada` | Dinheiro confirmado pelo provedor |
| `recusada` | Negada pelo provedor ou antifraude. Motivo código do provedor. |
| `expirada` | Pix ou boleto passou do vencimento sem pagamento |
| `estornada_parcial` / `estornada_total` | Estorno registrado no ledger |
| `em_contestacao` | Chargeback aberto |
| `pendente_conciliacao` | Status não confirmado dentro do prazo |
| `cancelada` | Cancelada antes de captura |

Transições válidas são as da tabela. Qualquer outra é `409` e gera alerta.

### 6.2 Regras de transição

- `capturada` nunca volta para `autorizada`. Só estorno ou chargeback.
- `estornada_total` exige soma dos estornos igual ao valor capturado.
- `estornada_parcial` acumula até o valor capturado. Acima disso, `422`.
- `pendente_conciliacao` expira em 24 h e vai para análise humana, sem liberar o produto.

## 7. Webhooks e confirmação

| Regra | Detalhe |
|---|---|
| Assinatura | Validada com o método do provedor, usando o segredo da conexão do tenant ([16](16-integracoes-externas.md), seção 4). Assinatura inválida: resposta `401`, nenhum efeito, alerta. |
| Janela | Timestamp com tolerância de 300 s, quando o provedor envia timestamp. |
| Deduplicação | Chave única por `provider + event_id`. Repetido: resposta `200` sem efeito. |
| Resposta | `200` após gravar na fila. Processamento assíncrono ([14](14-integracao-modulos.md), seção 5). |
| Ordem | Eventos da mesma transação aplicados por versão de estado. Evento antigo registrado e descartado. |
| Consulta de confirmação | Webhook não é a única fonte. Job consulta provedor para transações em `autorizacao_pendente` depois de N minutos. |
| Origem | IP de origem do provedor, quando publicado, é verificado como controle adicional, não como único controle. |

## 8. Cartão

- Autorização com 3DS2 obrigatório acima de valor configurado e para transações de risco alto pelo antifraude do provedor.
- Captura posterior à autorização tem prazo máximo configurado pelo provedor. Autorização vencida é cancelada automaticamente.
- Cartão tokenizado não é reaproveitado entre tenants.
- Tentativas recusadas: limite de 5 por cartão e 10 por IP em 15 min. Acima disso, bloqueio temporário.
- Cadastro de cartão recorrente (assinatura) exige consentimento registrado, com texto e data.

## 9. Pix

| Regra | Detalhe |
|---|---|
| Cobrança | `txid` único por tenant e conta. Valor fixo na criação. Expiração obrigatória. |
| Reuso | QR expirado não é reaberto. Nova cobrança gera novo `txid`. |
| Confirmação | Webhook do provedor e consulta por `txid` na conciliação. |
| Valor pago | Diferente do valor da cobrança: pagamento parcial ou excedente vai para pendência, nunca é aceito silenciosamente. |
| Chave Pix | Chave do recebedor cadastrada na conta do tenant. Não é dado pessoal do pagador. |

## 10. Boleto

| Regra | Detalhe |
|---|---|
| Identificador | `nosso_numero` único por tenant e convênio. |
| Cancelamento | Só antes do pagamento. Após pagamento, é estorno. |
| Pagamento após vencimento | Aceito conforme regra do provedor, com juros e multa calculados no servidor e validados contra o valor pago. Diferença gera pendência. |
| Registro | Baixa por retorno de arquivo ou webhook, assinado. Arquivo de retorno validado por checksum e por número de linhas. |

## 11. Estornos e contestações

- Estorno exige permissão `pagamento.estorno.solicitar` e aprovação por outra pessoa com `pagamento.estorno.aprovar`.
- Estorno acima de limite configurado exige MFA recente (ver [06](06-identidade-acesso.md), seção 5).
- Prazo de estorno respeita a janela do provedor e do meio de pagamento. Fora do prazo, só por crédito em conta, com aprovação dupla.
- Chargeback abre estado `em_contestacao` e reserva o valor no ledger, em conta de bloqueio.
- Evidências de contestação são arquivos com validação de tipo e tamanho ([15](15-validacoes.md), seção 4.3), com prazo do provedor controlado por alerta.

## 12. Conciliação

- Diária, por conta de gateway: extrato do provedor contra o ledger.
- Diferença de valor, de quantidade ou de status gera item na fila de conciliação, com alerta ao financeiro.
- Conciliação não corrige sozinha. Ajuste é lançamento com motivo e aprovação.
- Relatório de conciliação fica disponível para auditoria e não contém dado de cartão.

## 13. Antifraude e abuso

| Controle | Regra |
|---|---|
| Velocidade | Limite de tentativas por cartão, IP, pagador e conta de tenant (seção 8). |
| Lista de bloqueio | Cartão, e-mail e IP bloqueados por motivo registrado, com revisão. |
| Score do provedor | Transação acima do limite de risco é recusada ou vai para revisão, conforme configuração do tenant. |
| Padrão anômalo | Muitas recusas seguidas de um mesmo pagador gera alerta, não bloqueio automático de conta. |

## 14. Acesso e segregação de funções

| Papel | Pode | Não pode |
|---|---|---|
| Operador financeiro | Consultar cobranças e recebimentos | Estornar, alterar valor, ver token completo |
| Gestor financeiro | Solicitar estorno e aprovar até o limite | Aprovar o próprio pedido |
| Administrador do tenant | Configurar conta de gateway (com MFA) | Ver segredo em texto claro |
| Equipe da plataforma | Ver status e erros resumidos | Ver cartão, token ou segredo de tenant. Acesso excepcional segue [06](06-identidade-acesso.md), seção 10. |

## 15. Segurança de dados e logs

- Dados de pagador tratados conforme [07](07-privacidade-lgpd.md). CPF do pagador é exigido só quando o meio de pagamento exigir, e é cifrado.
- Logs de pagamento: identificador da transação, valor, estado, código do provedor. Sem PAN, CVV, token em claro, segredo de webhook ou chave Pix completa.
- Erro retornado ao cliente: código e mensagem genérica. Mensagem do provedor é traduzida, nunca repassada crua.
- Comunicação com o provedor: TLS 1.2 mínimo, validação de certificado, sem redirecionamento.

## 16. Monitoramento e alertas

| Alerta | Condição |
|---|---|
| Assinatura inválida | Qualquer ocorrência |
| Divergência de ledger | Qualquer ocorrência |
| Conciliação com diferença | Qualquer ocorrência acima de zero |
| Transição inválida | Qualquer ocorrência |
| Recusas acima do normal | Taxa de recusa acima de limite configurado por tenant |
| Estorno incomum | Volume ou valor acima da média do tenant |
| Webhook sem processamento | Mais de 5 min em fila |
| Chargeback aberto | Prazo de resposta em 3 dias |

## 17. Incidentes de pagamento

- Suspeita de vazamento de token ou de segredo de gateway: revogação imediata no provedor e rotação ([16](16-integracoes-externas.md), seção 5.3). Suspensão automática da conexão.
- Suspeita de PAN em log ou banco: tratar como incidente de dados ([07](07-privacidade-lgpd.md), seção 8) e acionar o provedor e a equipe de conformidade.
- Notificação ao provedor e ao tenant conforme contrato.

## 18. Testes obrigatórios

- PAN de teste nunca aparece em log, banco ou resposta de erro (varredura automatizada).
- Webhook com assinatura adulterada, com timestamp antigo e sem assinatura são recusados sem efeito.
- Webhook repetido não gera segundo lançamento.
- Valor enviado pelo cliente diferente do calculado é recusado.
- Estorno acima do capturado é recusado.
- Aprovador igual ao solicitante é recusado.
- Ledger não aceita `UPDATE` e `DELETE` pela conta da aplicação.
- Pix expirado não aceita pagamento.
- Boleto cancelado após pagamento é recusado.
- Conciliação com diferença gera item e alerta, sem ajuste automático.
- Tentativas acima do limite bloqueiam temporariamente.

## 19. Decisões pendentes

| # | Decisão | Proposta |
|---|---|---|
| D-10 | Fluxo de recursos | **Decidida:** (a) conta do tenant no gateway, sem custódia pela plataforma. O tenant pode usar gateway de terceiro ou gateway operado pela plataforma. Gateway operado pela plataforma é **condicionado a parecer jurídico** sobre arranjo de pagamento, porque o recurso passaria pela plataforma (seção 2). |
| D-11 | Representação de valor | **Decidida:** inteiros em centavos (seção 4). |
| D-12 | Limite de valor e MFA para operações | **Decidida pelo autor em 02/11/2026: MFA configurável por tenant, com piso.** Limite padrão definido pelo autor: operação acima de R$ 1.000,00 exige MFA forte e aprovação dupla. Valor ajustável por tenant, com piso não reduzível pelo tenant. Métodos e piso na seção 5 de [06](06-identidade-acesso.md). |

### 19.1 D-10: gateway da plataforma

Se o tenant contratar o gateway da plataforma, a conta do provedor fica no nome da plataforma e o recurso passa por ela antes de chegar ao tenant. Isso caracteriza custódia. Até o parecer jurídico, a plataforma não oferece essa opção. O tenant contrata gateway de terceiro, em conta própria, conectada por [16](16-integracoes-externas.md), seção 4.

Parecer necessário: enquadramento como arranjo de pagamento, exigências do Banco Central, responsabilidade por repasse e por estorno, e contrato com o tenant.

### 19.2 D-12: regras aplicadas

- MFA forte (TOTP, passkey ou certificado) para aprovação de estorno, baixa manual e pagamento acima do limite.
- Canais de mensagem (e-mail, SMS, WhatsApp, Telegram) nunca aprovam operação financeira.
- Limite padrão de R$ 1.000,00 por operação, com MFA forte e aprovação dupla acima dele. O tenant pode reduzir o limite, nunca aumentar acima do piso da plataforma. O piso do aumento fica **[Pendente]** com o autor.
- Alteração do limite e do método de MFA gera registro de auditoria e notificação em todos os canais cadastrados.

## 20. Pareceres necessários

| Tema | Responsável |
|---|---|
| Enquadramento de arranjo de pagamento (se D-10 não for (a)) | Jurídico, com parecer do BCB |
| Escopo e nível PCI DSS e questionário SAQ | Segurança e provedor |
| Prazos de estorno e chargeback por meio | Financeiro e jurídico |
| Consentimento para cobrança recorrente | Jurídico |

## 21. Critérios de aceite

- [ ] Nenhum dado de cartão é armazenado ou logado (varredura).
- [ ] Todo webhook passa por validação de assinatura antes de qualquer efeito.
- [ ] Todo valor é calculado e comparado no servidor.
- [ ] Ledger somente de inserção, com verificação de partidas dobradas.
- [ ] Estorno com segregação de funções e limite de MFA.
- [ ] Conciliação diária com alerta.
- [ ] Testes da seção 18 passando em CI.
- [ ] Pareceres da seção 20 registrados antes de produção.
