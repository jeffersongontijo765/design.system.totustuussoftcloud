# Cobrança

- Portal: Gestão (`gestao.`)
- Área: Financeiro da entidade
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 6; [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 7; [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 8; [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 9; [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 10; [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 11; [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 8
- Fonte da v1: absorvida integralmente em [mensalidades.md](mensalidades.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Cobrar por boleto, Pix e cartão pelo gateway da unidade, com webhooks, confirmação, estornos e contestações.

## 3. Telas

- **Cobranças** (DataTable por meio de pagamento e estado da transação).
- **Transação — detalhe** (drawer com eventos do gateway).
- **Contestações** (fila).

## 4. Permissões por portal (extraídas do SDD)

Do [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md):

| Portal | Pagamento | Recurso |
|---|---|---|
| Gestão | Cobrança de alunos e fornecedores; configuração do gateway | Gateway da entidade, split (se adotado), NFS-e da entidade, conciliação |

## 5. Papéis

- `unit.finance`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Ciclo da transação e webhooks ([20](../../../docs/v2/20-pagamentos-seguranca.md), seções 6 e 7); PCI fora do escopo do sistema ([20](../../../docs/v2/20-pagamentos-seguranca.md), seção 3).

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

### 13.1 [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 6

#### 6. Ciclo de vida da transação

##### 6.1 Estados

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

##### 6.2 Regras de transição

- `capturada` nunca volta para `autorizada`. Só estorno ou chargeback.
- `estornada_total` exige soma dos estornos igual ao valor capturado.
- `estornada_parcial` acumula até o valor capturado. Acima disso, `422`.
- `pendente_conciliacao` expira em 24 h e vai para análise humana, sem liberar o produto.

### 13.2 [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 7

#### 7. Webhooks e confirmação

| Regra | Detalhe |
|---|---|
| Assinatura | Validada com o método do provedor, usando o segredo da conexão do tenant ([16](../../../docs/v2/16-integracoes-externas.md), seção 4). Assinatura inválida: resposta `401`, nenhum efeito, alerta. |
| Janela | Timestamp com tolerância de 300 s, quando o provedor envia timestamp. |
| Deduplicação | Chave única por `provider + event_id`. Repetido: resposta `200` sem efeito. |
| Resposta | `200` após gravar na fila. Processamento assíncrono ([14](../../../docs/v2/14-integracao-modulos.md), seção 5). |
| Ordem | Eventos da mesma transação aplicados por versão de estado. Evento antigo registrado e descartado. |
| Consulta de confirmação | Webhook não é a única fonte. Job consulta provedor para transações em `autorizacao_pendente` depois de N minutos. |
| Origem | IP de origem do provedor, quando publicado, é verificado como controle adicional, não como único controle. |

### 13.3 [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 8

#### 8. Cartão

- Autorização com 3DS2 obrigatório acima de valor configurado e para transações de risco alto pelo antifraude do provedor.
- Captura posterior à autorização tem prazo máximo configurado pelo provedor. Autorização vencida é cancelada automaticamente.
- Cartão tokenizado não é reaproveitado entre tenants.
- Tentativas recusadas: limite de 5 por cartão e 10 por IP em 15 min. Acima disso, bloqueio temporário.
- Cadastro de cartão recorrente (assinatura) exige consentimento registrado, com texto e data.

### 13.4 [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 9

#### 9. Pix

| Regra | Detalhe |
|---|---|
| Cobrança | `txid` único por tenant e conta. Valor fixo na criação. Expiração obrigatória. |
| Reuso | QR expirado não é reaberto. Nova cobrança gera novo `txid`. |
| Confirmação | Webhook do provedor e consulta por `txid` na conciliação. |
| Valor pago | Diferente do valor da cobrança: pagamento parcial ou excedente vai para pendência, nunca é aceito silenciosamente. |
| Chave Pix | Chave do recebedor cadastrada na conta do tenant. Não é dado pessoal do pagador. |

### 13.5 [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 10

#### 10. Boleto

| Regra | Detalhe |
|---|---|
| Identificador | `nosso_numero` único por tenant e convênio. |
| Cancelamento | Só antes do pagamento. Após pagamento, é estorno. |
| Pagamento após vencimento | Aceito conforme regra do provedor, com juros e multa calculados no servidor e validados contra o valor pago. Diferença gera pendência. |
| Registro | Baixa por retorno de arquivo ou webhook, assinado. Arquivo de retorno validado por checksum e por número de linhas. |

### 13.6 [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 11

#### 11. Estornos e contestações

- Estorno exige permissão `pagamento.estorno.solicitar` e aprovação por outra pessoa com `pagamento.estorno.aprovar`.
- Estorno acima de limite configurado exige MFA recente (ver [06](../../../docs/v2/06-identidade-acesso.md), seção 5).
- Prazo de estorno respeita a janela do provedor e do meio de pagamento. Fora do prazo, só por crédito em conta, com aprovação dupla.
- Chargeback abre estado `em_contestacao` e reserva o valor no ledger, em conta de bloqueio.
- Evidências de contestação são arquivos com validação de tipo e tamanho ([15](../../../docs/v2/15-validacoes.md), seção 4.3), com prazo do provedor controlado por alerta.

### 13.7 [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 8

#### 8. Pagamento por portal

| Portal | Pagamento | Recurso |
|---|---|---|
| Desenvolvedor | Cobrança de clientes SaaS; recebimento da plataforma | Gateway da plataforma (com parecer), NFS-e da plataforma (ausente), taxas |
| Gestão | Cobrança de alunos e fornecedores; configuração do gateway | Gateway da entidade, split (se adotado), NFS-e da entidade, conciliação |
| Professor | Nenhum pagamento recebido. Holerite e pagamento de salário fora do escopo deste módulo | Só consulta do próprio holerite ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2.3) |
| Aluno | Pagar mensalidade: Pix, boleto, cartão | Cobrança, comprovante, segunda via |
| Responsáveis | Pagar fatura dos filhos; débito automático | Mesmos métodos, central financeira, débito automático (se aprovado) |
| Terceiros | Receber pagamento; enviar nota | Extrato, status da liquidação, envio de NF-e (seção 5.3), dados bancários com MFA |

**Regra:** nenhum portal, exceto Gestão e Desenvolvedor, mostra taxa, split ou conta de recebimento da entidade.
