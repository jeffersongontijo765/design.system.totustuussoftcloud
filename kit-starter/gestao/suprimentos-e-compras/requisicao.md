# Requisição

- Portal: Gestão (`gestao.`)
- Área: Suprimentos e compras
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [17](../../../docs/v2/17-regras-modulos.md), seção 6; [19](../../../docs/v2/19-regras-modulos-3.md), seção 2
- Fonte da v1: absorvida integralmente em [suprimentos-da-empresa.md](../../desenvolvedor/operacoes-internas/suprimentos-da-empresa.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Requisição de compra por setor com aprovação na alçada.

## 3. Telas

- **Requisições** (DataTable e kanban).
- **Nova requisição** (itens, justificativa, centro de custo).
- **Aprovações** (fila).

## 4. Permissões por portal (extraídas do SDD)

- O SDD não traz tabela por portal para este módulo; vale o escopo da seção 2 e os papéis abaixo.

## 5. Papéis

- Qualquer setor com permissão: requisitar.
- `unit.purchasing.approver`: aprovar; não é o solicitante.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Regras de suprimentos ([17](../../../docs/v2/17-regras-modulos.md), seção 6).

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

### 13.1 [17](../../../docs/v2/17-regras-modulos.md), seção 6

#### 6. Suprimentos

##### 6.1 Entidades

Requisição, aprovação, cotação, pedido de compra, recebimento, divergência, almoxarifado, itens críticos, fornecedor, avaliação de fornecedor, contrato e ata (sem DDL na v1, ver T-02).

##### 6.2 Regras de negócio (v1, seções 6.2 e 9)

| Regra | Descrição |
|---|---|
| Autoaprovação | Bloqueada acima da faixa da política. |
| Solicitante e aprovador | Não podem ser a mesma pessoa em cenários sensíveis. |
| Pedido | Só emitido por usuário com permissão. |
| Fornecedor bloqueado | Não recebe pedido nem recebimento quando a política exige. |
| Edição após encerramento | Bloqueada. |
| Cotações | Número mínimo por faixa de valor. Fonte única só com justificativa. Motivo da adjudicação registrado. |
| Comparativo | Snapshot gravado no fechamento da cotação. |
| Estoque | Movimento que deixaria saldo negativo é recusado, salvo item de consumo sob encomenda. |
| Divergência de recebimento | Tipo obrigatório (quantidade, item incorreto, avaria, validade, lote, documento fiscal, atraso). |

##### 6.3 Estados

| Entidade | Estados |
|---|---|
| Requisição | `rascunho`, `em_aprovacao`, `aprovada`, `reprovada`, `cancelada` |
| Pedido | `emitido`, `em_transito`, `recebido_parcial`, `recebido`, `cancelado` |
| Fornecedor | `ativo`, `bloqueado`, `inativo` |

##### 6.4 Campos mínimos a definir

Como a v1 não tem DDL, os campos de requisição, pedido, item e fornecedor precisam ser escritos antes. Lista mínima proposta:

- Requisição: solicitante, unidade, centro de custo, itens (item, quantidade, unidade de medida), valor estimado, justificativa, data limite de SLA.
- Item: código, descrição, unidade de medida, estoque mínimo, estoque atual, fornecedor preferencial.
- Fornecedor: CNPJ válido, situação documental, validade de certificados, situação (`ativo`, `bloqueado`).

### 13.2 [19](../../../docs/v2/19-regras-modulos-3.md), seção 2

#### 2. Duplicidades a resolver

| Módulo A | Módulo B | Sobreposição | Proposta |
|---|---|---|---|
| Armazenamento (estoque, 17 tabelas) | Suprimentos (almoxarifado) | Saldo, movimento, estoque mínimo, rastreabilidade por lote | Suprimentos é dono de estoque e movimento. Armazenamento é renomeado para sistema de arquivos e documentos, sem estoque. **Decidido** em 03/11/2026. |
| Logger | Auditoria | Registro de eventos, bloqueio de IP, alertas de segurança | Auditoria é dona de trilha de negócio e de segurança ([18](../../../docs/v2/18-regras-modulos-2.md), seção 4). Logger técnico fica em [10](../../../docs/v2/10-implantacao-operacao.md), seção 7. |
| Autenticação (v1, 1.001 linhas) | 06 e 07 | Login, sessão, MFA, senha | Consolidar em [06](../../../docs/v2/06-identidade-acesso.md). A especificação de módulo perde o conteúdo que duplica 06. |
| Privacidade global | 07 e Cookies e sessões | Direitos do titular, consentimento, cookies | Consolidar em [07](../../../docs/v2/07-privacidade-lgpd.md). Cookies e sessões fica em 06. |
| Bancos (administração de banco de dados, 305 linhas) | Financeiro (contas bancárias) | Nenhuma: são assuntos diferentes | Bancos sai do escopo. Dados bancários ficam no Financeiro. Ver [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 4. |
| SAC, Chat rápido, Helpdesk | Entre si | Atendimento e tickets | Um único módulo de atendimento. Helpdesk é a base. Proposta na seção 7. |
| Biblioteca acadêmica e Biblioteca completo | Entre si | Acervo, empréstimo, multa | Uma especificação. Escolher a mais recente como base. |
