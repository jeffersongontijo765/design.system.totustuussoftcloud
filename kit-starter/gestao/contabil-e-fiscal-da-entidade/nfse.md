# NFS-e

- Portal: Gestão (`gestao.`)
- Área: Contábil e fiscal da entidade
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [18](../../../docs/v2/18-regras-modulos-2.md), seção 2.7; [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 5
- Fonte da v1: absorvida integralmente em [plano-de-contas-da-entidade.md](plano-de-contas-da-entidade.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Emitir e cancelar NFS-e dos serviços da entidade.

## 3. Telas

- **Notas** (DataTable por estado).
- **Emitir** (a partir do título pago ou em lote).
- **Cancelar** (pedido e aprovação do contábil).

## 4. Permissões por portal (extraídas do SDD)

Do [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md):

| Portal | Pagamento | Recurso |
|---|---|---|
| Gestão | Cobrança de alunos e fornecedores; configuração do gateway | Gateway da entidade, split (se adotado), NFS-e da entidade, conciliação |

## 5. Papéis

- `unit.fiscal`: emitir e pedir cancelamento.
- `unit.accounting`: aprovar cancelamento.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- NFS-e ([18](../../../docs/v2/18-regras-modulos-2.md), seção 2.7; [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 5).

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

### 13.1 [18](../../../docs/v2/18-regras-modulos-2.md), seção 2.7

##### 2.7 Nota fiscal de serviço (NFSe)

- Emissão só para fatura `paid` ou `partial`, conforme política municipal **[Pendente: regra por município]**.
- Status `pending` → `processing` → `issued` ou `rejected`. `cancelled` só a partir de `issued`, com o cancelamento transmitido ao município.
- Integração com o município é externa ([16](../../../docs/v2/16-integracoes-externas.md), seção 3). Resposta de rejeição guarda o código de erro do município.

### 13.2 [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 5

#### 5. Nota fiscal

##### 5.1 Quem emite, por escala e por portal

| Nota | Quem emite | Portal de origem | Estado |
|---|---|---|---|
| NFS-e de mensalidade e serviço educacional | Entidade, por município | Gestão | Parcial. Ver 5.2 |
| NFS-e da assinatura SaaS (plataforma cobra a entidade) | Plataforma | Desenvolvedor | **Ausente.** Precisa de especificação própria |
| NF-e de serviço de fornecedor (terceiros) | Fornecedor, no próprio sistema ou no município | Terceiros | Conflito. Ver 5.3 |
| NF-e de produto (SEFAZ) | — | Desenvolvedor (v1, "Gestão de integração") | **Fora de escopo.** Não há venda de produto no escopo. Confirmar |

##### 5.2 Regras da NFS-e (entidade)

Já definido: emissão só para fatura paga ou parcial, conforme regra municipal; estados `pending`, `processing`, `issued`, `rejected`, `cancelled`; cancelamento transmitido ao município ([18](../../../docs/v2/18-regras-modulos-2.md), seção 2.7).

Faltam:

- **NFS-e Nacional** (padrão ABRASF e nacional, citado na v1). Lista de municípios que usam cada padrão. **(jurídico)** e fiscal.
- **Certificado digital A1 ou A3** da entidade: guardado no cofre, nunca em arquivo ([16](../../../docs/v2/16-integracoes-externas.md), seção 3).
- **Cancelamento:** prazo e justificativa exigidos pelo município. Cancelamento após o prazo exige processo fiscal, não ação do operador.
- **Reenvio** de nota rejeitada: só após correção do motivo. Nota rejeitada não é reemitida com o mesmo número.
- **Guarda:** XML e PDF guardados pelo prazo fiscal **(jurídico)**, com hash ([21](../../../docs/v2/21-busca-e-armazenamento.md)).
- **Pagamento e nota:** emissão automática após pagamento é opcional. Se for automática, a nota tem o valor do pagamento confirmado, não o valor da fatura.
- **Tomador:** dado do responsável financeiro. Se o tomador tem dado pessoal, o campo segue a regra de [07](../../../docs/v2/07-privacidade-lgpd.md).

##### 5.3 Nota do fornecedor (terceiros)

A v1 ([`12-portals-navigation-sidebar-pages-spec.md`](../../../docs/v2/anexo-v1/12-portals-navigation-sidebar-pages-spec.md), portal de terceiros, "Emissão e Upload de NF-e de Serviços") diz que o portal **emite** a nota. Isso não se sustenta: a nota é emitida pelo prestador, no município ou no seu sistema.

**Proposta:** o portal de terceiros **recebe e valida** a nota (XML, valor, tomador, competência), vincula à ordem de compra e ao pagamento, e não emite. Qualquer mudança de "emissão" para "envio" passa por revisão **(jurídico)** e fiscal.

**Decidido** em 03/11/2026: o portal de terceiros recebe e valida, sem emitir.
