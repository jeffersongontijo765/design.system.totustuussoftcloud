# Razão

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Contábil da plataforma
- Domínio: plataforma (banco master). Mesmo código do contábil da entidade, com outro dono de dado ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.3)
- Escopo: Lançamentos contábeis e livros (razão e balancete) da empresa
- Status: detalhado (SDD 18, 22 e v1)

## 1. Identificação
- Especificações: [18](../../../docs/v2/18-regras-modulos-2.md), seção 6 (período, competência, estados); [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.3 (plataforma × entidade); [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5 (segregação do contábil); v1 [spec_gestao_contabil_fiscal_completo.md](../../../docs/v2/anexo-v1/spec_gestao_contabil_fiscal_completo.md) (telas, colunas, widgets, drawers, kanban).
- Regra de fonte: onde a v1 e a v2 divergem, vale a v2.

## 2. Objetivo e escopo
Escriturar os lançamentos contábeis da empresa e consultar o razão e o balancete por conta e por período.

## 3. Telas
- **Lançamentos contábeis** (datatable; v1 seção 6.2). Colunas: data, competência, documento, histórico, conta débito, conta crédito, centro de custo, valor, origem, situação, ações.
- **Drawer de lançamento** (edição completa e correção com motivo; v1 seção 8): partidas, competência, histórico, anexos, validações em tempo real.
- **Importação assistida** de lançamentos (v1 seção 8.2), com prévia e relatório de erros por linha ([15](../../../docs/v2/15-validacoes.md), importar).
- **Razão por conta** e **balancete** do período (v1 seção 2.1, livros e balancetes).
- **Aprovações de lançamento** (kanban; v1 seção 9.1), com as colunas dos estados de lançamento da v2.

## 4. Dados
- Estados do lançamento ([18](../../../docs/v2/18-regras-modulos-2.md), seção 6.2): `rascunho`, `em_validacao`, `aprovado`, `estornado`.
- Origem do lançamento rastreada (manual, importado, automático a partir do financeiro).

## 5. Campos e validações
- Data dentro da competência declarada; competência inválida é recusada (`422`).
- Débitos e créditos fecham (validação de totais e saldos, v1 seção 11.1).
- Período fechado: lançamento não é editado nem excluído; correção é lançamento de ajuste no período aberto, com motivo ([18](../../../docs/v2/18-regras-modulos-2.md), seção 6.1).
- Proteção contra envio repetido (v1 seção 16.1).

## 6. Indicadores e gráficos
- Lançamentos pendentes de revisão, rejeitados, automáticos, por origem e com divergência (v1 seção 7.2).
- Gráfico de lançamentos por dia (v1 seção 5.2).

## 7. Ações e confirmações
- Criar, enviar para validação, aprovar, rejeitar, estornar, importar. Aprovação automática só por regra cadastrada e auditada ([18](../../../docs/v2/18-regras-modulos-2.md), seção 6.1).

## 8. Permissões e papéis
- `platform.accounting` (papel Contábil) lança, fecha período e exporta; `platform.fiscal` (papel Fiscal) cuida de tributos e notas; ambos definidos no [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5, com códigos no [78](../../../docs/v2/78-permissoes-e-papeis.md), seção 4.1.
- Segregação: quem criou o lançamento não fecha o período sem revisão de outra pessoa ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5).

## 9. Exportação e auditoria
- Auditoria de criação, edição, aprovação, reprovação, estorno, importação e ajuste manual de valor (v1 seção 14.1). Exportação do razão e do balancete em CSV, XLSX e PDF.

## 10. Estados de interface
- Carregando (skeleton nas tabelas e widgets), vazio com chamada para ação, sem resultado, erro, acesso negado, período fechado (somente leitura).

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
- **Divergências v1 × v2 (vale a v2):** obrigação em atraso é calculada por data, não marcada por automação ([18](../../../docs/v2/18-regras-modulos-2.md), seção 6.2); estados de período e de lançamento são os da v2, não as colunas genéricas do kanban da v1; sem filtro de unidade, entidade ou filial (a plataforma não tem).
- **Sem DDL** para o contábil (defeito T-02 do [18](../../../docs/v2/18-regras-modulos-2.md), seção 6.2): campos, tipos e chaves ainda não definidos.
- Tributos e obrigações da empresa: ficha [tributos-e-obrigacoes-fiscais-da-empresa.md](tributos-e-obrigacoes-fiscais-da-empresa.md).
