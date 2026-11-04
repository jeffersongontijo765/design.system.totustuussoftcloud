# 16 — Integrações Externas: Plataforma (master) e Tenant

> Parte do [SDD v2](00-README.md). Credenciais e cofre em [05](05-seguranca.md) e [10](10-implantacao-operacao.md). Validação de entrada e de saída em [15](15-validacoes.md). Eventos internos em [14](14-integracao-modulos.md).
> **Status:** proposta. Itens **[Decisão pendente]** precisam de aprovação do autor.

---

## 1. Dois níveis

| Nível | Quem contrata e paga | Quem configura | Credencial fica em | Quem usa |
|---|---|---|---|---|
| **Plataforma (master)** | TotusTuus SoftCloud | Equipe da plataforma, com permissão `plataforma.integracao.*` | Cofre da plataforma | Todos os tenants, de forma transparente |
| **Tenant** | A entidade (cliente) | Administrador da entidade, com permissão `integracao.conexao.*` | Cofre, com chave de cifragem por tenant | Só o próprio tenant |

Regras:

1. Credencial de um tenant nunca é visível para outro tenant, nem para a equipe da plataforma em texto claro.
2. A equipe da plataforma vê status, erros resumidos e metadados de uma conexão de tenant. Para ver o segredo, é preciso step-up, motivo registrado e alerta ao canal de segurança (ver [06](06-identidade-acesso.md), seção 10).
3. Uma integração de plataforma pode ser usada por um tenant só quando o plano contratado inclui o recurso. O controle é feito pela configuração do tenant, não pelo código.
4. Integração de tenant não pode substituir integração de plataforma em funções de segurança, como e-mail de verificação e MFA.

## 2. Catálogo de integrações de plataforma

| Provedor (tipo) | Finalidade | Dado enviado | Regra |
|---|---|---|---|
| E-mail transacional | Verificação de cadastro, recuperação de conta, notificações | E-mail e conteúdo do aviso | Obrigatório. Única via de recuperação (D-04). |
| SMS | Notificação não crítica, opcional | Número e texto curto | **Não é fator de MFA** ([06](06-identidade-acesso.md), seção 5). Desligado por padrão. |
| Armazenamento de objetos | Uploads e exportações | Arquivo cifrado no envio | Região declarada; URL assinada com validade curta |
| Antivírus de upload | Verificação de arquivo enviado | Arquivo | Arquivo recusado se o serviço não responder |
| Captcha | Proteção de login e cadastro após tentativas (ver [06](06-identidade-acesso.md), seção 6) | Token do navegador | Escolha do provedor em ADR próprio |
| Cobrança da assinatura do SaaS | Cobrança dos tenants pela plataforma | Dados do cliente da plataforma | Dados bancários nunca passam pelo sistema; tokenização no provedor |
| Backup externo | Cópia de segurança fora da região principal | Backup cifrado | Chave de backup fora do provedor |
| Monitoramento e erros | Métricas e rastreamento de erro | Metadados; sem PII | Filtro de PII antes do envio |
| Verificação de documento (opcional) | Conferência de identidade, para suporte | Documento enviado pelo titular | Só com consentimento específico; sem armazenamento no provedor |

## 3. Catálogo de integrações de tenant

| Integração | Finalidade | Credencial típica | Regra |
|---|---|---|---|
| Gateway de pagamento | Cobrança de mensalidades, Pix, cartão | Chave da conta do tenant | Um gateway primário por unidade, dentro da entidade. Decidido em 03/11/2026 (SRC-05). Adapters: Asaas, Mercado Pago, Gerencianet / EFÍ, PagSeguro e Stripe (lista da v1, [`spec_gestao_billing_cobranca_mensalidades.md`](anexo-v1/spec_gestao_billing_cobranca_mensalidades.md), seção 17.1). Contingência em [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 2.3. |
| ERP ou contabilidade | Exportação de lançamentos | Chave ou usuário do ERP | Envio por lote diário; idempotência por número de lançamento |
| Emissão de nota fiscal (NFS-e, por município) | Nota de serviço educacional | Certificado digital e credencial da prefeitura | Certificado do tenant; sem certificado, a emissão não é habilitada |
| eSocial (transmissão) | Eventos S-2220, S-2230, S-2240 e demais do RH e SMT | Certificado digital A1 ou A3 da entidade | Ver decisão D-08 (seção 6) |
| SSO institucional (SAML ou OIDC) | Login com o provedor de identidade da escola | Metadados e certificado do provedor | Fora desta versão, salvo decisão D-09 |
| Webhook de saída | Enviar eventos para o sistema da unidade. Um endpoint por unidade. Decidido em 03/11/2026 (SRC-06) | Segredo HMAC do endpoint | Ver [04](04-api.md), seção 7 |
| Importação de sistema legado | Carga inicial de dados | Arquivo ou acesso de leitura ao banco legado | Carga por arquivo; acesso direto ao banco de terceiros não é permitido |

## 4. Modelo de conexão

Cada conexão é um registro, em tabela com `tenant_id` quando o nível é tenant.

| Campo | Tipo | Regra |
|---|---|---|
| `id` | UUID | Público |
| `level` | enum | `platform` ou `tenant` |
| `tenant_id` | UUID | Obrigatório se `level = tenant`; nulo se `platform` |
| `provider` | enum | Lista fechada da seção 2 ou 3 |
| `environment` | enum | `sandbox` ou `production` |
| `status` | enum | `rascunho`, `testando`, `ativa`, `suspensa`, `revogada`, `expirada` |
| `config` | JSON | Só dado não secreto (ex.: identificador da conta, região) |
| `secret_ref` | string | Referência ao segredo no cofre; nunca o segredo |
| `scopes` | lista | Permissões que a conexão pede ao provedor |
| `expires_at` | data | Data de vencimento da credencial, quando o provedor informa |
| `last_tested_at`, `last_test_result` | data, enum | Resultado do último teste |
| `created_by`, `rotated_at`, `revoked_at` | identificador, data | Auditoria |

Regras do modelo:

- `production` e `sandbox` não compartilham credencial. Conexão de produção não pode ser usada em ambiente de homologação.
- Credencial de tenant é cifrada com a chave de dados do tenant, que por sua vez é protegida pela chave-mestra do cofre (ADR-05 em [02](02-arquitetura.md)).
- Um tenant tem no máximo uma conexão `ativa` por provedor e ambiente, salvo gateway com múltiplas contas (regra do provedor).

## 5. Ciclo de vida

```
rascunho → testando → ativa ⇄ suspensa
                  ↘ (falha)    ↓
                  rascunho   revogada
                              expirada (automática, se a credencial vencer)
```

### 5.1 Criação e teste

1. Administrador informa os dados não secretos e envia a credencial. A credencial é gravada no cofre antes de qualquer teste.
2. Sistema faz uma chamada de teste ao provedor (sandbox ou produção, conforme `environment`). Teste usa operação somente leitura.
3. Resultado do teste é gravado. Sucesso leva a `testando → ativa` só depois da confirmação do administrador.
4. Falha mantém o status `rascunho` e mostra a mensagem do provedor, sem o segredo.

### 5.2 Ativação

- Ativar conexão de produção exige permissão específica e step-up de MFA.
- Ativar conexão de plataforma exige dupla aprovação de dois responsáveis da equipe da plataforma.

### 5.3 Rotação

- Credencial tem data de rotação. Padrão: 180 dias, ou o prazo do provedor, se for menor.
- Rotação cria o novo segredo, testa, troca a referência e só depois revoga o antigo. Se o teste falhar, o antigo continua ativo.
- Janela de sobreposição máxima de 24 h.

### 5.4 Revogação e exclusão

- Revogar desativa a conexão e tenta revogar a credencial no provedor, quando a API permitir.
- O segredo é apagado do cofre após 30 dias de carência. Durante a carência, a restauração é possível pelo administrador da plataforma com motivo registrado.
- Registro da conexão permanece para auditoria.

## 6. Decisões aprovadas (02/11/2026, com a proposta indicada)

| # | Decisão | Proposta | Alternativa e condição de falha |
|---|---|---|---|
| D-07 | Tenant pode trazer as próprias credenciais de gateway e ERP? | Sim, para cobrança e ERP. Comunicação e infraestrutura ficam na plataforma. | Centralizar tudo na plataforma: menos trabalho para o tenant, mas a plataforma passa a ser cobradora e responsável por todas as contas bancárias. |
| D-08 | Quem transmite o eSocial? | Certificado A1 ou A3 do tenant, com transmissor da plataforma. Montagem do XML no SMT ou RH. | Transmissão feita pela própria entidade: menos carga para a plataforma, mas exige equipe técnica no cliente. |
| D-09 | SSO institucional entra nesta versão? | Não. Fica para a versão seguinte, com [06](06-identidade-acesso.md) já preparada para OIDC. | Entrar agora: aumenta o escopo de identidade e de testes. |

## 7. Segurança das chamadas externas

- **Lista de destinos permitidos** por provedor. Chamada para domínio fora da lista é bloqueada.
- **Proteção contra SSRF** (ver [04](04-api.md), seção 7): sem redirecionamento, IP resolvido uma vez, bloqueio de redes privadas.
- **TLS verificado.** Certificado inválido é erro, sem opção de desligar verificação.
- **Segredo nunca em log**, em mensagem de erro, em URL ou em corpo de resposta gravado.
- **Chamada de saída com `timeout`:** conexão 3 s e total 15 s. Falha segue a regra da seção 6 de [15](15-validacoes.md).
- **Circuit breaker por conexão:** após 5 falhas em 60 s, a conexão fica `suspensa` por 5 min e o administrador é avisado.

## 8. Operações financeiras

- Chave de idempotência por cobrança: o identificador da cobrança no sistema. Repetir a chamada não gera segunda cobrança.
- Conciliação diária entre o registro interno e o extrato do gateway. Diferença gera tarefa para o financeiro.
- Webhook de pagamento tem assinatura específica do provedor, validada antes de qualquer efeito.
- Estorno passa pelo gateway, nunca só no sistema.

## 9. Auditoria e observabilidade

- Registro de cada mudança de configuração, rotação, ativação, suspensão e revogação: ator, antes, depois, motivo.
- Registro de cada chamada de saída: provedor, operação, código de resposta, latência, identificador de correlação. Sem payload com dado pessoal.
- Painel de status por conexão. O painel da plataforma mostra só conexões de plataforma e contagem de erros por tenant, sem nome de cliente, salvo permissão.
- Alerta quando uma credencial vence em 30 dias ou quando uma conexão de produção fica `suspensa`.

## 10. Testes obrigatórios

- Conexão de tenant A não é usada por requisição do tenant B.
- Credencial de produção recusada em ambiente de sandbox.
- Rotação falha não derruba a credencial antiga.
- Segredo não aparece em log nem em resposta de API, mesmo em erro.
- Chamada a domínio fora da lista é bloqueada.
- Webhook com assinatura inválida é recusado antes de qualquer efeito.
- Cobrança repetida com a mesma chave de idempotência gera uma cobrança.

## 11. Critérios de aceite

- [ ] Todo provedor de plataforma e de tenant tem linha no catálogo com finalidade, dado enviado e regra.
- [ ] Nenhuma credencial em texto claro em banco, log ou resposta.
- [ ] Todo ciclo de vida (criação, teste, ativação, rotação, revogação) tem registro de auditoria.
- [ ] Decisões D-07, D-08 e D-09 tomadas pelo autor e registradas aqui.
