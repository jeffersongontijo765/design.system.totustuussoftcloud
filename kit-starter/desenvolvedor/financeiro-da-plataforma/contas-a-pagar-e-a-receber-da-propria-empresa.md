# Financeiro da plataforma (contas a pagar e a receber da própria empresa)

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Financeiro da plataforma
- Domínio: plataforma (banco master), instância separada do financeiro das entidades ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2.1)
- Escopo: contas, movimentação, contas a pagar, contas a receber, fluxo de caixa, conciliação, centros de custo, orçamento e DRE **da empresa desenvolvedora**
- Status: detalhado (SDD 71 e v1), com D-42 e D-43 pendentes

## 1. Identificação
- Especificações: [71](../../../docs/v2/71-financeiro-completo-por-portal.md) (regras do financeiro), [17](../../../docs/v2/17-regras-modulos.md) seção 2 (aprovação, conciliação), [20](../../../docs/v2/20-pagamentos-seguranca.md) (pagamentos), v1 [spec_gestao_financeiro_completo.md](../../../docs/v2/anexo-v1/spec_gestao_financeiro_completo.md) (telas, colunas, drawers, kanban, painel).
- Regra de fonte: onde a v1 e a v2 divergem, vale a v2. Divergências tratadas na seção 12.

## 2. Objetivo e escopo
Gerir o dinheiro da própria empresa desenvolvedora: o que ela recebe (assinaturas e faturas dos clientes) e o que ela paga (fornecedores e despesas). O portal do desenvolvedor vê e gere só esse financeiro e **nunca vê o financeiro de uma entidade** ([71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 11).

Fora daqui: títulos e cobrança de alunos (financeiro da entidade, [18](../../../docs/v2/18-regras-modulos-2.md)); contabilidade da empresa (área Contábil da plataforma).

## 3. Telas
- **Painel financeiro** (dashboard; v1 seção 3): KPIs e gráficos da seção 6; aprovações do dia em kanban (Pendente, Em análise, Aprovado, Rejeitado); controles de período, centro de custo, exportar e atualizar. **Sem filtro de unidade**: a plataforma não tem unidades.
- **Contas a pagar** (datatable; v1 seção 5.2). Colunas: seleção, código, fornecedor, descrição, categoria, documento ou nota, emissão, vencimento (destaque quando vencido), valor, centro de custo, aprovação, situação, método de pagamento, pago em, ações (ver, editar, pagar, aprovar, cancelar). Filtros: situação, categoria, fornecedor, vencimento, centro de custo, aprovação, faixa de valor, busca.
- **Drawer de despesa** (criar e editar; v1 seção 5.3): identificação (código automático, categoria, fornecedor, centro de custo, descrição, número do documento), valores (bruto, desconto, juros e multa, líquido calculado, rateio por centro de custo), datas e parcelas, aprovação, pagamento (método, conta de origem, dados de pagamento, anexos). Rodapé: salvar, salvar e enviar para aprovação, cancelar.
- **Drawer de pagamento** (v1 seção 5.4): valor original, desconto, juros e multa, valor pago calculado, data, conta de origem, método, comprovante.
- **Pagamento em lote** (página de confirmação): despesas aprovadas da mesma conta, total conferido antes de confirmar ([71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 4.2).
- **Kanban de contas a pagar** (v1 seção 5.5, ajustado): Pendente, Aguardando aprovação, Aprovado, Pago, Cancelado. "Vencido" é **filtro**, não coluna (seção 12).
- **Contas a receber**: as faturas dos clientes da plataforma. Ficam em [faturamento-de-clientes.md](../plataforma-e-clientes/faturamento-de-clientes.md); aqui aparecem só no fluxo de caixa e nos indicadores, sem cadastro duplicado.
- **Contas e movimentação**: contas bancárias e de gateway da empresa; extratos.
- **Fluxo de caixa** (diário e projetado; [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 7).
- **Conciliação** (v1 seção 7): widgets, rosca de situação, tela em duas colunas (extrato e sistema), importação de extrato OFX ou CSV.
- **Centros de custo** e **orçamento** (orçado contra realizado; [71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 8.3).
- **DRE** por competência ([71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 8).
- **Configurações**: categorias financeiras (cada uma ligada a uma linha da DRE), métodos de pagamento, parâmetros (tolerância de conciliação, limite de desvio do orçamento).

## 4. Dados
- Conta: corrente, poupança, gateway ou carteira digital do gateway ([71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 3). Caixa físico: ver D-42.
- Movimentação: conta, data, valor, categoria, centro de custo, origem e estado: `previsto`, `lancado`, `conciliado`, `estornado`. Lançamento conciliado não muda: correção é estorno e novo lançamento, com motivo.
- Tabelas (v1 seção 1.2): `financial_payables`, `financial_transactions`, `financial_bank_accounts`, `financial_bank_statements`, `financial_reconciliations`, `financial_cost_centers`, `financial_budgets`, `financial_categories`, `financial_payment_methods`, no banco master. DDL de referência em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 15.16.

## 5. Campos e validações
- Despesa: fornecedor, categoria, centro de custo, vencimento e valor obrigatórios ([71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 4.1).
- Rateio: soma dos percentuais igual a 100%; diferença bloqueia o lançamento.
- Pagamento com chave de idempotência: reenvio não paga duas vezes ([15](../../../docs/v2/15-validacoes.md), seção 4).
- Extrato OFX importado com hash por linha, sem duplicar.
- Categoria sem linha de DRE aparece como pendência, não some.

## 6. Indicadores e gráficos
- KPIs (v1 seção 3.1): saldo em conta, a receber em 30 dias, a pagar em 30 dias, inadimplência de clientes, receita do mês, despesa do mês. Cada KPI leva à página relacionada.
- Operacional (v1 seção 3.2): próximos vencimentos, contas abaixo do saldo mínimo, aprovações pendentes, conciliação pendente.
- Gráficos (v1 seção 3.3): fluxo de caixa em 12 meses (receitas, despesas, saldo acumulado); composição de receitas por categoria; a receber contra a pagar nos próximos 6 meses; inadimplência por faixa de atraso (1 a 30, 31 a 60, 61 a 90, mais de 90 dias); orçado contra realizado.

## 7. Ações e confirmações
- Despesa: criar, enviar para aprovação, aprovar, rejeitar, pagar, pagar em lote, cancelar. Cancelar exige motivo.
- Conciliação: conciliar, ignorar, criar lançamento a partir do extrato. Ajuste é lançamento com motivo e aprovação, nunca automático.
- Orçamento: aprovado não muda; ajuste é nova versão aprovada pela gestão.

## 8. Permissões e papéis
- O portal do desenvolvedor vê só o financeiro da empresa ([71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 11).
- Separação de funções: quem solicita não aprova a própria despesa; despesa acima de R$ 10.000 exige segundo aprovador ([17](../../../docs/v2/17-regras-modulos.md), seção 2.4; [78](../../../docs/v2/78-permissoes-e-papeis.md), seção 2.2).
- Papéis que operam e aprovam: **pendência D-43**.

## 9. Exportação e auditoria
- Exportação de listas: CSV e XLSX, com permissão e step-up; DRE e fluxo em PDF.
- Auditoria: aprovação, pagamento, estorno, ajuste de conciliação, mudança de orçamento.

## 10. Estados de interface
- Carregando, vazio, sem resultado, erro, acesso negado. Pagamento aguardando confirmação do provedor. Conciliação com divergência.

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
- **Divergências v1 × v2 (vale a v2):** atraso não é estado gravado, é filtro por data ([71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 3); tolerância de conciliação é parâmetro, não os R$ 0,01 fixos da v1; aprovação não é opcional como na v1; sem filtro de unidade.
- **D-42:** cheques e caixa físico ([71](../../../docs/v2/71-financeiro-completo-por-portal.md), seções 5 e 6) foram escritos para as escolas. Aplicam-se à empresa desenvolvedora? Proposta: **não**, até haver necessidade.
- **D-43:** papéis do financeiro da plataforma. Proposta: `platform.finance` (nível 1, opera contas, pagamentos e conciliação) e `platform.finance.manager` (nível 2, aprova despesas e orçamento; segundo aprovador acima de R$ 10.000).
- Saldo mínimo por conta e limite de desvio do orçamento: **[Sem detalhamento]** de valor.
