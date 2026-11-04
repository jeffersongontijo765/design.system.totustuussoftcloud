# Centros de custo

- Portal: Gestão (`gestao.`)
- Área: Financeiro da entidade
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 2; [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), seção 2.4
- Fonte da v1: absorvida integralmente em [titulos.md](titulos.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Manter os centros de custo da unidade para despesas, receitas e relatórios gerenciais.

## 3. Telas

- **Centros de custo** (árvore e lista).
- **Rateio** (regras).

## 4. Permissões por portal (extraídas do SDD)

Do [71](../../../docs/v2/71-financeiro-completo-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Ver tudo: DRE, fluxo, inadimplência, caixa. Aprovar despesa e fechamento de caixa | Operar caixa. Lançar pagamento sem aprovação | E |
| **Coordenação** | Ver o financeiro da unidade, em leitura | Lançar ou aprovar lançamento | E |
| **Secretaria** | Receber pagamento de aluno na unidade, em caixa de atendimento. Emitir boleto e segunda via | Pagar despesa. Ver DRE | E |

## 5. Papéis

- `unit.finance` e `unit.accounting`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Centro de custo é citado sem especificação própria ([55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), seção 2.4); usar a divisão de dono do [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 2.

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

### 13.1 [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 2

#### 2. Divisão de dono

| Assunto | Dono | Documento |
|---|---|---|
| Título, parcela, desconto, cobrança de aluno | Financeiro da entidade | [18](../../../docs/v2/18-regras-modulos-2.md) |
| Gateway, ledger, webhook, Pix, boleto | Financeiro da entidade, com provedor | [20](../../../docs/v2/20-pagamentos-seguranca.md) |
| Conta a pagar, fornecedor, rateio | Financeiro da entidade | Este documento, seção 4 |
| Cheque | Financeiro da entidade | Este documento, seção 5 |
| Caixa físico | Financeiro da entidade, operado na unidade | Este documento, seção 6 |
| Fluxo de caixa e DRE | Financeiro da entidade | Este documento, seções 7 e 8 |
| Conciliação | Financeiro da entidade | [17](../../../docs/v2/17-regras-modulos.md), seção 2.5 |
| NFS-e, split, nota de fornecedor | Financeiro e fiscal | [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md) |
| Financeiro da empresa desenvolvedora | Plataforma | [31](../../../docs/v2/31-matriz-portais-modulos.md) |

### 13.2 [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), seção 2.4

##### 2.4 Outros módulos do menu

| Item | Cobertura | Situação |
|---|---|---|
| Financeiro (parcelas, cobrança, conciliação, NF, cheques, cartões, estoque) | [18](../../../docs/v2/18-regras-modulos-2.md), [20](../../../docs/v2/20-pagamentos-seguranca.md), [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md) | Coberto no financeiro. Cheques e estoque de cantina não têm especificação |
| Centros de custo | [17](../../../docs/v2/17-regras-modulos.md) e [31](../../../docs/v2/31-matriz-portais-modulos.md) | Citado, sem especificação |
| Controle patrimonial | [19](../../../docs/v2/19-regras-modulos-3.md), seção 8 | Coberto |
| Catraca | [35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md) | Coberto |
| Biblioteca (bibliografias, empréstimos e reservas) | [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.1 | Citado. **Sem especificação própria** |
| Administração (usuários, grupos, integrações, importação, notificações) | [06](../../../docs/v2/06-identidade-acesso.md), [16](../../../docs/v2/16-integracoes-externas.md), [19](../../../docs/v2/19-regras-modulos-3.md), seção 13 | Coberto, exceto importação de dados, que é lacuna |
| Ischolar Intelligence | [27](../../../docs/v2/27-inteligencia-artificial-e-portais.md) e [28](../../../docs/v2/28-cobertura-ia-todos-os-modulos.md) | Coberto |
