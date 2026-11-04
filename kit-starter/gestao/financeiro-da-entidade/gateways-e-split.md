# Gateways e split

- Portal: Gestão (`gestao.`)
- Área: Financeiro da entidade
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 2; [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 3; [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 6; [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 7; [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 8
- Fonte da v1: absorvida integralmente em [mensalidades.md](mensalidades.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Configurar o gateway de pagamento da unidade, a contingência e o split de pagamento, com credenciais no cofre do tenant.

## 3. Telas

- **Gateways** (lista e configuração por unidade; credencial por referência ao cofre).
- **Split** (regras e extrato).
- **Carteiras digitais e débito automático** (configuração).

## 4. Permissões por portal (extraídas do SDD)

Do [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md):

| Portal | Pagamento | Recurso |
|---|---|---|
| Gestão | Cobrança de alunos e fornecedores; configuração do gateway | Gateway da entidade, split (se adotado), NFS-e da entidade, conciliação |

## 5. Papéis

- `entity.admin` e `unit.manager`: configurar com step-up.
- `unit.finance`: consultar.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Gateway e contingência por unidade ([34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seções 2 e 3); credencial nunca em texto claro ([16](../../../docs/v2/16-integracoes-externas.md), seção 1).

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

### 13.1 [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 2

#### 2. Gateways de pagamento

##### 2.1 Lista consolidada

| Provedor | Métodos | Credencial (v1) | Origem |
|---|---|---|---|
| Asaas | Pix, boleto, cartão, carteira | Chave de API, identificador de carteira, URL de webhook | v1 billing, 17.1 |
| Mercado Pago | Pix, boleto, cartão | Access token, chave pública | v1 billing, 17.1 |
| PagSeguro | Boleto, cartão, Pix | Token, e-mail, modo sandbox | v1 billing, 17.1 |
| Gerencianet / EFÍ | Pix, boleto | Client ID, client secret, certificado Pix (.p12 ou .pem) | v1 billing, 17.1. Incluído na v2 em 03/11/2026 (PAG-01) |
| Stripe | Cartão | Chave secreta, chave pública, segredo de webhook | v1 billing, 17.1 |

**Regras que faltam na v2:**

- Certificado Pix (.p12 ou .pem) é segredo. Fica no cofre ([05](../../../docs/v2/05-seguranca.md), seção 2), nunca no banco comum.
- Modo sandbox não pode ser ativado em produção. O sistema recusa a credencial de teste em ambiente de produção.
- Contingência: quando o gateway primário cai, o sistema não troca de provedor sozinho. Troca é decisão do financeiro, com registro. Regra completa na seção 2.3.
- Teste de conectividade com resultado imediato (v1, 17.1) é permitido, mas não grava o dado de teste.

##### 2.2 Gateway por escala

| Escala | Quem configura | Conta de quem | Fonte |
|---|---|---|---|
| Entidade (cobrança de alunos) | Administrador da entidade, com MFA | Entidade | [20](../../../docs/v2/20-pagamentos-seguranca.md), opção (a) |
| Plataforma (cobrança de clientes SaaS) | Financeiro da plataforma | Plataforma | [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 19.1 |

Gateway da plataforma que recebe por conta de entidade é custódia. Só existe se o parecer de [20](../../../docs/v2/20-pagamentos-seguranca.md) for favorável.

##### 2.3 Gateway por unidade e contingência (PAG-01)

Cada unidade tem **um gateway primário** (SRC-05). A unidade pode cadastrar **um gateway de contingência**, de outro provedor, com conta da própria entidade.

| Situação | Regra |
|---|---|
| Primário saudável | Toda cobrança nova sai pelo primário |
| Primário com falha | O monitor marca o provedor como degradado depois de 3 falhas seguidas de criação de cobrança ou de 5 minutos sem resposta ([20](../../../docs/v2/20-pagamentos-seguranca.md), seção 16). O financeiro da unidade recebe aviso |
| Troca para contingência | Decisão do financeiro da unidade, com MFA e motivo. Vale só para cobrança nova. Fica na auditoria ([29](../../../docs/v2/29-auditoria.md)) |
| Cobrança já emitida | Continua no gateway que a emitiu. Não é cancelada nem reemitida em outro provedor, para não haver dois boletos ou dois Pix válidos para o mesmo título |
| Webhook e conciliação | Cada gateway concilia as próprias cobranças. A conciliação diária roda para os dois enquanto houver cobrança aberta em algum deles ([20](../../../docs/v2/20-pagamentos-seguranca.md), seção 12) |
| Volta ao primário | Decisão do financeiro, com registro, depois de teste de conectividade aprovado |
| Sem contingência cadastrada | A unidade aceita só os meios manuais ([71](../../../docs/v2/71-financeiro-completo-por-portal.md): caixa e cheque) até o primário voltar |

**Regras gerais:**

- Os dois gateways da unidade não podem ser do mesmo provedor. Contingência no mesmo provedor não protege de queda do provedor.
- A credencial de cada gateway fica no cofre, separada por unidade ([05](../../../docs/v2/05-seguranca.md), seção 2). Certificado Pix da EFÍ segue a mesma regra.
- Unidades da mesma entidade podem usar provedores diferentes. A troca numa unidade não afeta as outras.
- O provedor que emitiu cada título fica gravado no título. Relatório de recebimento mostra o provedor por título.

### 13.2 [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 3

#### 3. Split de pagamento

**Estado:** opção (c) em [20](../../../docs/v2/20-pagamentos-seguranca.md), seção 2. Padrão desta versão é a opção (a): cada entidade tem a própria conta, sem custódia da plataforma.

**Se o split for adotado**, a especificação precisa de:

| Item | Regra proposta |
|---|---|
| Subconta | Cada entidade tem uma subconta no provedor, com identificador de carteira guardado. O identificador é dado de configuração, não segredo, mas fica vinculado à entidade. |
| Taxa | Percentual ou valor fixo da plataforma, por contrato. Gravado no momento da cobrança. Não muda retroativamente. |
| Divisão | Valor bruto, taxa, valor líquido da entidade e valor da plataforma gravados no lançamento do ledger ([20](../../../docs/v2/20-pagamentos-seguranca.md), seção 4). |
| Estorno | Estorno devolve da subconta da entidade e da plataforma na proporção gravada. Taxa estornada só se o contrato permitir. |
| Conciliação | Diária por subconta, contra o extrato do provedor ([20](../../../docs/v2/20-pagamentos-seguranca.md), seção 12). |
| Falha parcial | Se o provedor confirma uma parte, a diferença vira item de conciliação. Nunca é lançada automaticamente. |
| Contrato | Subcontas e taxa exigem contrato com o provedor e com a entidade. **(jurídico)** |

**Por portal:**

- Desenvolvedor: visão de taxas recebidas por entidade e por período.
- Gestão: visão do líquido recebido e do que foi retido como taxa.
- Responsáveis e aluno: aparecem só o valor pago e o estado. Taxa nunca aparece para o pagador.

**Decidido** em 03/11/2026: split em duas formas, automática e pelo gateway. Entidade sem fins lucrativos: mesmo split, com taxa da plataforma menor.

### 13.3 [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 6

#### 6. Bancos, Open Finance e débito automático

| Recurso | Quem usa | Regra proposta |
|---|---|---|
| Conta bancária da entidade | Financeiro da entidade | Cadastro no Financeiro. Alteração exige MFA e dupla aprovação |
| Conta bancária da plataforma | Financeiro da plataforma | Mesma regra, no portal do desenvolvedor |
| Dados bancários de fornecedor | Compras, terceiros | Terceiros cadastra. Compras aprova. Alteração gera alerta de possível fraude |
| Conciliação por extrato (OFX) | Financeiro | Já em [17](../../../docs/v2/17-regras-modulos.md), seção 2.5 |
| Open Finance (leitura de extrato, consentimento) | Financeiro | Só com consentimento do titular da conta e regra do Open Finance. **(jurídico)**. Não especificado |
| Débito automático | Responsáveis | Autorização do pagador, revogável. Regra de cobrança em [18](../../../docs/v2/18-regras-modulos-2.md). **(jurídico)** |

### 13.4 [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 7

#### 7. Carteiras digitais

**Estado:** ausente. Não há especificação de carteira digital (Apple Pay, Google Pay, carteira do provedor).

**Proposta mínima:** carteira digital é um **método de pagamento do gateway**, não módulo. O sistema não guarda token de carteira. Cada carteira aceita só o que o provedor suporta. Pagamento por carteira segue [20](../../../docs/v2/20-pagamentos-seguranca.md), inclusive 3-D Secure.

**Decidido** em 03/11/2026: Pix e cartão pelo gateway da unidade, sem carteira própria.

### 13.5 [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 8

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
