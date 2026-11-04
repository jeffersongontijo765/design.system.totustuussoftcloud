# Fluxo de caixa e DRE

- Portal: Gestão (`gestao.`)
- Área: Financeiro da entidade
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 7; [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 8; [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 10; [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 11
- Fonte da v1: absorvida integralmente em [titulos.md](titulos.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Projetar o fluxo de caixa e apresentar a DRE gerencial da unidade.

## 3. Telas

- **Fluxo de caixa** (gráfico e tabela por período).
- **DRE** (relatório por competência e centro de custo).

## 4. Permissões por portal (extraídas do SDD)

Do [71](../../../docs/v2/71-financeiro-completo-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Ver tudo: DRE, fluxo, inadimplência, caixa. Aprovar despesa e fechamento de caixa | Operar caixa. Lançar pagamento sem aprovação | E |
| **Coordenação** | Ver o financeiro da unidade, em leitura | Lançar ou aprovar lançamento | E |
| **Secretaria** | Receber pagamento de aluno na unidade, em caixa de atendimento. Emitir boleto e segunda via | Pagar despesa. Ver DRE | E |

## 5. Papéis

- `unit.finance`, `unit.accounting`, `unit.manager` (leitura).
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Regras do fluxo e da DRE ([71](../../../docs/v2/71-financeiro-completo-por-portal.md), seções 7 e 8).

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

### 13.1 [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 7

#### 7. Fluxo de caixa

- **Realizado:** movimentações lançadas e conciliadas, por conta e por data.
- **Projetado:** títulos a receber e contas a pagar em aberto, pela data de vencimento. Não grava nada: é consulta.
- **Diário:** entradas, saídas e saldo por dia, com a linha de saldo projetado.
- Projeção usa somente títulos com estado válido. Estorno e título cancelado saem da projeção.

### 13.2 [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 8

#### 8. DRE

##### 8.1 Estrutura

- Cada categoria financeira aponta para uma linha da DRE. Categoria sem linha não entra no demonstrativo e aparece como pendência.
- Centro de custo é filtro, não linha.
- A DRE tem as linhas da v1 (receita bruta, deduções, receita líquida, custos, despesas, resultado), com o detalhamento que a entidade configurar.

##### 8.2 Regime

- A DRE pode ser por **caixa** (pelo que foi pago e recebido) ou por **competência** (pelo período a que o valor se refere).
- **Decidido** em 03/11/2026 (FIN-01): a DRE é por competência. A escolha é por entidade e não muda no meio do exercício. Lançamento de caixa entra no período a que se refere.

---

##### 8.3 Orçamento

**Decidido** em 03/11/2026 (FIN-07): o orçamento fica no financeiro.

- Orçamento é por centro de custo e categoria, por mês e por exercício. Estado: `rascunho`, `aprovado`, `encerrado`.
- Orçado versus realizado: o realizado vem dos lançamentos da seção 4 e da seção 3. Não é digitado.
- Desvio acima do limite configurado pela escola gera aviso à gestão. O aviso não bloqueia lançamento.
- Orçamento aprovado não muda. Ajuste é nova versão, com aprovação da gestão.

### 13.3 [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 10

#### 10. Inadimplência e fiscal

- Inadimplência, régua e cadastro de inadimplente seguem [18](../../../docs/v2/18-regras-modulos-2.md) e [26](../../../docs/v2/26-sdd-juridico-regulatorio.md). Comunicação prévia por escrito antes de qualquer cadastro (CDC, art. 43, §2º) **(jurídico)**.
- Comprovante de IRPF do pagador: regra fiscal a confirmar (FIN-03).
- NFS-e de mensalidade e de serviço seguem [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md).

### 13.4 [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 11

#### 11. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Ver e gerir o financeiro da própria empresa, separado da entidade | Ver financeiro de entidade | P |
| **Gestão** | Ver tudo: DRE, fluxo, inadimplência, caixa. Aprovar despesa e fechamento de caixa | Operar caixa. Lançar pagamento sem aprovação | E |
| **Financeiro** (perfil da unidade) | Operar contas, cheques, caixa, pagamentos, conciliação. Gerar relatório financeiro | Aprovar a própria despesa. Aprovar a própria diferença de caixa | E |
| **Coordenação** | Ver o financeiro da unidade, em leitura | Lançar ou aprovar lançamento | E |
| **Secretaria** | Receber pagamento de aluno na unidade, em caixa de atendimento. Emitir boleto e segunda via | Pagar despesa. Ver DRE | E |
| **Professor** | Nada | Qualquer item financeiro | E |
| **Aluno** | Ver e pagar os próprios títulos. Ver comprovantes e informe de pagamento | Ver título de colega | E |
| **Responsáveis** | Ver e pagar faturas dos dependentes. Ver comprovantes | Ver título de outra família | E, só dependentes com vínculo ativo |
| **Terceiros** (fornecedores) | Ver a própria conta a receber, enviar nota e acompanhar o pagamento | Ver outros fornecedores ou o caixa | E |
