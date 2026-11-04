# Régua de cobrança

- Portal: Gestão (`gestao.`)
- Área: Financeiro da entidade
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [18](../../../docs/v2/18-regras-modulos-2.md), seção 2.6; [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 4; [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 5
- Fonte da v1: absorvida integralmente em [mensalidades.md](mensalidades.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Configurar a régua de cobrança (lembretes antes e depois do vencimento, canais, negativação com comunicação prévia) dentro das regras de consumo e de consentimento.

## 3. Telas

- **Réguas** (lista e editor de etapas: dias, canal, modelo).
- **Execuções** (log por título).
- **Negociação e renegociação** (acordos).

## 4. Permissões por portal (extraídas do SDD)

- O SDD não traz tabela por portal para este módulo; vale o escopo da seção 2 e os papéis abaixo.

## 5. Papéis

- `unit.finance`: configurar e acompanhar.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Pontos que exigem parecer ([18](../../../docs/v2/18-regras-modulos-2.md), seção 2.6); negativação com comunicação prévia ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 4.4); bloqueio de serviço só parcial ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 4.6).

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

### 13.1 [18](../../../docs/v2/18-regras-modulos-2.md), seção 2.6

##### 2.6 Régua de cobrança: pontos que exigem parecer

A v1 define sete etapas de cobrança, de D+1 a D+90, com canais e ações ([`spec_gestao_billing_cobranca_mensalidades.md`](../../../docs/v2/anexo-v1/spec_gestao_billing_cobranca_mensalidades.md), seção 11). Três pontos precisam de parecer antes de implementar:

| Etapa | Ação na v1 | Risco | Tratamento proposto |
|---|---|---|---|
| D+10 SMS e e-mail; D+5 WhatsApp | Cobrança por canal de mensagem | Consentimento e LGPD ([07](../../../docs/v2/07-privacidade-lgpd.md)) | **(jurídico)** base legal da comunicação de cobrança. Canal só para titular que informou o contato para esse fim. |
| D+30 aviso de negativação | Inclusão em cadastro de inadimplentes | Exige notificação prévia e regras do cadastro de crédito | **(jurídico)** prazo e forma de notificação antes da negativação. |
| D+90 bloqueio de acesso ao portal | Bloqueio do portal do aluno | Interrupção de serviço educacional a menor de idade | **(jurídico)** bloqueio não deve impedir acesso a documentos obrigatórios nem a matrícula de menor. Propor bloqueio parcial. |

### 13.2 [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 4

#### 4. Relação de consumo e cobrança

##### 4.1 Contrato e cláusulas

- Contrato de adesão deve ter redação clara e destaque para cláusulas que limitem direitos (CDC, art. 54, §4º) [A].
- Cláusula de rescisão, multa e reajuste devem estar no contrato e na área do cliente, com histórico [A].
- Prática abusiva é vedada (CDC, art. 39) [A]. Exemplo: exigir vantagem sem causa ou condicionar serviço a aceite de cobrança indevida.

##### 4.2 Direito de arrependimento em venda online

Quando a matrícula ou a assinatura é contratada fora do estabelecimento, o consumidor tem sete dias para desistir, sem custo (CDC, art. 49) [A]. O sistema:

- Mostra o prazo no fluxo de contratação.
- Registra a data da contratação e a data da desistência.
- Gera estorno integral dentro do prazo do meio de pagamento ([20](../../../docs/v2/20-pagamentos-seguranca.md), seção 11).

##### 4.3 Multa, juros e reajuste de mensalidade

- Multa moratória em relação de consumo tem limite de 2% (CDC, art. 52, §1º) [A].
- Anuidades e mensalidades escolares têm regras próprias de reajuste e de cobrança de encargos (Lei 9.870/1999) [V]. O sistema aplica os limites da norma como padrão, e o tenant não pode ultrapassá-los.
- Juros de mora e correção seguem a regra do contrato, dentro dos limites legais [V].

##### 4.4 Negativação e comunicação prévia

- A abertura de cadastro de inadimplente exige comunicação por escrito ao consumidor antes da inclusão (CDC, art. 43, §2º) [A].
- O sistema envia a comunicação e registra a data e o canal. A inclusão só ocorre depois do prazo de comunicação, que o jurídico confirma [V].
- Consulta a cadastro de inadimplentes sem finalidade legítima é vedada. Ver [21](../../../docs/v2/21-busca-e-armazenamento.md), seção 6.8, para a regra de finalidade.

##### 4.5 Superendividamento e renegociação

- Antes de bloqueios e negativação, o sistema oferece renegociação com plano de pagamento (Lei 14.181/2021) [A para a existência; V para a aplicação à régua].
- Renegociação registra as condições, o consentimento do consumidor e o histórico.

##### 4.6 Bloqueio de serviço

- Bloqueio total do portal por inadimplência é vedado para serviço educacional essencial e para menor de idade. O sistema aplica bloqueio parcial: documentos obrigatórios, matrícula de rematrícula e comunicação com a família continuam acessíveis [P].
- Documentos escolares não são retidos como forma de cobrança sem previsão legal [V].

### 13.3 [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 5

#### 5. Consentimento e comunicação por canal

| Canal | Base para contato comercial | Base para cobrança | Prova exigida | Observação |
|---|---|---|---|---|
| E-mail | Consentimento [A] | Execução de contrato [V] | Registro do aceite e da versão | Link de descadastro obrigatório em marketing |
| SMS | Consentimento [A] | Execução de contrato [V] | Registro do aceite | Número verificado |
| WhatsApp | Consentimento e regras da plataforma [V] | Execução de contrato [V] | Registro do opt-in | Não enviar mensagem proativa sem opt-in ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 3) |
| Telegram | Consentimento e regras da plataforma [V] | Execução de contrato [V] | Registro do opt-in | Mesmo tratamento do WhatsApp |
| Instagram e Messenger | Consentimento e regras da plataforma [V] | Não usado para cobrança | Registro do opt-in | Só conversa iniciada pelo usuário |
| Telefone | Consentimento [A] | Execução de contrato [V] | Aviso de gravação e registro | Gravação só com aviso |

Regras:

- Revogação é tão fácil quanto a concessão. Efeito imediato.
- Menor de idade: consentimento do responsável, específico e em destaque (LGPD, art. 14) [A].
- Mensagem de cobrança segue o horário permitido pelo tenant e o limite de frequência ([18](../../../docs/v2/18-regras-modulos-2.md), seção 2.6).
