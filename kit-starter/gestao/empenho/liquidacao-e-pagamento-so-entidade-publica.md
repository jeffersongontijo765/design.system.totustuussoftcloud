# Liquidação e pagamento (entidade pública)

- Portal: Gestão (`gestao.`)
- Área: Empenho
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 5
- Fonte da v1: absorvida integralmente em [empenho.md](empenho.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Liquidar e pagar despesas empenhadas.

## 3. Telas

- **Liquidações** (conferência da entrega).
- **Pagamentos** (ordem de pagamento).

## 4. Permissões por portal (extraídas do SDD)

Do [37](../../../docs/v2/37-planejamento-e-empenho.md):

| Portal | Planejamento acadêmico | Planejamento institucional | Desenvolvimento de pessoas | Empenho |
|---|---|---|---|---|
| Gestão | Completo, por permissão | Completo, por permissão | Completo, por permissão | Completo, para entidade pública, por permissão |

## 5. Papéis

- `unit.finance` e `unit.finance.approver`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 5.

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

### 13.1 [37](../../../docs/v2/37-planejamento-e-empenho.md), seção 5

#### 5. Empenho (entidade pública)

**Ativação:** o módulo só é habilitado para entidade que declara natureza pública. A declaração é feita pelo administrador da entidade, com MFA, e registrada em auditoria.

##### 5.1 Entidades

| Entidade | Função |
|---|---|
| Dotação | Valor autorizado por rubrica, exercício e unidade |
| Empenho | Reserva de dotação para uma despesa, com credor, valor e origem |
| Liquidação | Confirmação de que o bem ou serviço foi entregue, com documento comprobatório |
| Pagamento | Saída financeira, sempre posterior à liquidação |
| Anulação | Reversão parcial ou total de empenho, com motivo |
| Restos a pagar | Empenho que passa para o exercício seguinte |

##### 5.2 Modalidades

Conferido em 03/11/2026 no texto da Lei 4.320/1964 (planalto.gov.br):

| Modalidade | Base |
|---|---|
| Ordinário | Valor certo. A lei não usa o nome: é o caso comum, sem regra própria |
| Por estimativa | Despesa cujo montante não se pode determinar (art. 60, § 2º) |
| Global | Despesa contratual ou outra sujeita a parcelamento (art. 60, § 3º) |

- Empenho é o ato de autoridade competente que cria a obrigação de pagamento (art. 58). Não há despesa sem prévio empenho (art. 60), salvo dispensa da nota em lei específica (art. 60, § 1º).
- Cada empenho gera a **nota de empenho**, com credor, especificação, valor e dedução do saldo da dotação (art. 61). O sistema emite a nota com esses campos obrigatórios.
- O empenho não excede o crédito concedido (art. 59).
- **Liquidação** apura origem e objeto, valor exato e credor, com base no contrato, na nota de empenho e no comprovante de entrega ou serviço (art. 63). Pagamento só depois da liquidação regular e por **ordem de pagamento** da autoridade competente, em documento processado pela contabilidade (arts. 62 e 64).
- **Município, último mês do mandato do prefeito:** não empenha mais que um duodécimo da despesa prevista, nem assume compromisso para depois do mandato, salvo calamidade pública comprovada. Empenho em desacordo é nulo (art. 59, §§ 1º a 4º). O sistema bloqueia acima do duodécimo nesse mês, com data do fim do mandato cadastrada pela entidade, e aceita exceção só com o decreto de calamidade anexado.
- Normas do tribunal de contas de cada estado e o texto compilado da lei, com alterações posteriores, **(verificar)**.

##### 5.3 Estados

Empenho: `emitido` → `liquidado` → `pago`. Pode ir para `anulado` (parcial ou total) antes de `pago`. Empenho não pago até 31 de dezembro vai para `restos_a_pagar`, separado em **processado** (já liquidado) e **não processado** (não liquidado) (Lei 4.320/1964, art. 36). Empenho de crédito plurianual não liquidado só vira restos a pagar no último ano de vigência do crédito (art. 36, parágrafo único).

##### 5.4 Regras

- Empenho não pode exceder a dotação disponível da rubrica, na data de emissão.
- Liquidação exige documento comprobatório (nota fiscal, recibo ou contrato) vinculado.
- Pagamento exige liquidação. Sem liquidação, a aplicação recusa o pagamento.
- Anulação exige motivo e aprovação de segundo papel. Quem emite não aprova.
- Pagamento segue a regra de pagamento de [20](../../../docs/v2/20-pagamentos-seguranca.md) e de [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md).
- Período fechado não recebe novo empenho.
- Toda emissão, liquidação, pagamento e anulação gera evento de auditoria ([29](../../../docs/v2/29-auditoria.md)).

##### 5.5 Segregação

| Ação | Papel que executa | Papel que aprova |
|---|---|---|
| Emitir empenho | Financeiro | Contador |
| Liquidar | Responsável pelo recebimento | Financeiro |
| Pagar | Financeiro | Gestor executivo acima da faixa 2 de [33](../../../docs/v2/33-contratos-por-portal.md) |
| Anular | Financeiro | Contador e gestor executivo |
