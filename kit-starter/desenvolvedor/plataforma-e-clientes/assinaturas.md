# Assinaturas

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Plataforma e clientes
- Domínio: plataforma (banco master)
- Escopo: Assinatura do SaaS contratada pela entidade (plano, ciclo e renovação)
- Status: detalhado

## 1. Identificação
- Especificações: `docs/v2/16-integracoes-externas.md` (cobrança da assinatura do SaaS); `docs/v2/20-pagamentos-seguranca.md`

## 2. Objetivo e escopo
Gerir a assinatura de cada entidade: plano, ciclo de cobrança, renovação e cancelamento.

## 3. Telas
- **Assinaturas** (datatable): entidade, plano, situação, próxima renovação, valor.
- **Detalhe da assinatura** (drawer de visualização e página com histórico).
- Sem telas adicionais detalhadas.

## 4. Dados
- Cobrança da assinatura do SaaS: dados do cliente, sem dados bancários no sistema; tokenização no provedor (SDD 16, integração de cobrança).
- Modelo da assinatura: **[Sem detalhamento]**.

## 5. Campos e validações
- Plano, ciclo, valor, data de início e de renovação: **[Sem detalhamento]**.

## 6. Indicadores e gráficos
- Assinaturas ativas, inadimplentes, canceladas no período: **[Sem detalhamento]** da fórmula.

## 7. Ações e confirmações
- Criar, alterar plano, cancelar, reativar: **[Sem detalhamento]** das regras.

## 8. Permissões e papéis
- Papel de plataforma: **[Sem detalhamento]**.

## 9. Exportação e auditoria
- Mudanças de plano e cancelamentos auditados: **[Sem detalhamento]**.

## 10. Estados de interface
- Padrão de estados de tela (SDD 08).

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
Todo o módulo: regras de plano, ciclo e inadimplência **[Sem detalhamento]**. Pagamentos de assinatura seguem SDD 20 (pagamentos) e SDD 16 (integrações).
