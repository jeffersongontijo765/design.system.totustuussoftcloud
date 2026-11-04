# Faturamento de clientes

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Plataforma e clientes
- Domínio: plataforma (banco master)
- Escopo: Cobrança das entidades clientes pela plataforma (faturas e recebimentos)
- Status: detalhado

## 1. Identificação
- Especificações: `docs/v2/20-pagamentos-seguranca.md`; `docs/v2/34-pagamentos-fiscal-bancos-por-portal.md`

## 2. Objetivo e escopo
Emitir e acompanhar as faturas das entidades clientes da plataforma.

## 3. Telas
- **Faturas de clientes** (datatable): entidade, competência, valor, vencimento, situação.
- **Detalhe da fatura** (drawer de visualização).
- Sem telas adicionais detalhadas.

## 4. Dados
- Fatura e recebimento: **[Sem detalhamento]** das entidades e do vínculo com a assinatura.
- Pagamento e conciliação: SDD 20 e 34 (regras gerais da plataforma).

## 5. Campos e validações
- Campos da fatura: **[Sem detalhamento]**.

## 6. Indicadores e gráficos
- Valor em aberto, vencido e recebido no período: **[Sem detalhamento]** da fórmula.

## 7. Ações e confirmações
- Emitir, reenviar, registrar pagamento, estornar: **[Sem detalhamento]**.

## 8. Permissões e papéis
- Faturas de clientes: `platform.manager` (SDD 78, §4.1); estorno exige `platform.developer`.

## 9. Exportação e auditoria
- Emissão e estorno auditados (SDD 29).

## 10. Estados de interface
- Padrão de estados de tela (SDD 08).

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
Todo o módulo: regras de faturamento de clientes **[Sem detalhamento]**. Nota fiscal: a NFS-e da assinatura do SaaS está **ausente** no SDD e é a pendência PAG-05 ([34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seções 5.1 e 9); emissão e regras na ficha de tributos da área Contábil.
