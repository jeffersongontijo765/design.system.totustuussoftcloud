# Fechamento da empresa

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Contábil da plataforma
- Domínio: plataforma (banco master). Mesmo código do contábil da entidade, com outro dono de dado ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.3)
- Escopo: Ciclo de fechamento contábil mensal da empresa
- Status: detalhado (SDD 18 e v1); D-44 e D-45 pendentes

## 1. Identificação
- Especificações: [18](../../../docs/v2/18-regras-modulos-2.md), seção 6 (período, competência, estados); [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.3 (plataforma × entidade); [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5 (segregação do contábil); v1 [spec_gestao_contabil_fiscal_completo.md](../../../docs/v2/anexo-v1/spec_gestao_contabil_fiscal_completo.md) (telas, colunas, widgets, drawers, kanban).
- Regra de fonte: onde a v1 e a v2 divergem, vale a v2.

## 2. Objetivo e escopo
Controlar o fechamento mensal da contabilidade da empresa, impedindo fechar com pendências e registrando toda reabertura.

## 3. Telas
- **Painel contábil** (v1 seção 5): widgets e gráficos da seção 6.
- **Fechamento mensal** (kanban e checklist; v1 seções 3 e 9.1): um cartão por período, nos estados da v2; checklist das pendências que bloqueiam o fechamento.
- **Conciliações pendentes** (datatable; v1 seção 6.6): origem, conta, competência, valor no sistema, valor externo, diferença, situação, tratativa.
- **Histórico de reaberturas** (linha do tempo).

## 4. Dados
- Estados do período ([18](../../../docs/v2/18-regras-modulos-2.md), seção 6.2): `aberto`, `em_fechamento`, `fechado`, `reaberto` (com justificativa e permissão administrativa).

## 5. Campos e validações
- Fechamento bloqueado com pendência aberta de aprovação ou de conciliação ([18](../../../docs/v2/18-regras-modulos-2.md), seção 6.1).
- Reabertura exige justificativa e permissão administrativa.

## 6. Indicadores e gráficos
- Widgets do painel (v1 seção 5.1, sem os itens fiscais até a D-44): lançamentos do período, pendências de conciliação, saldo contábil consolidado, alertas críticos, itens aguardando aprovação, fechamentos concluídos contra pendentes.
- Gráficos (v1 seção 5.2): lançamentos por dia; evolução de pendências.

## 7. Ações e confirmações
- Iniciar fechamento, concluir fechamento, reabrir período (justificativa obrigatória).

## 8. Permissões e papéis
- Papéis do contábil da plataforma: **pendência D-45** ([78](../../../docs/v2/78-permissoes-e-papeis.md), seção 6).
- Segregação: quem criou o lançamento não fecha o período sem revisão de outra pessoa ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5).

## 9. Exportação e auditoria
- Auditoria de reabertura de período, mudança de estado e troca de responsável (v1 seção 14.1). Relatório do fechamento em PDF.

## 10. Estados de interface
- Carregando (skeleton nas tabelas e widgets), vazio com chamada para ação, sem resultado, erro, acesso negado, período fechado (somente leitura).

## 11. Requisitos de frontend (SDD 08)
- Sem JavaScript inline; textos por i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal.
- Exportação CSV com células neutralizadas (`=`, `+`, `@`, tab, retorno de carro).

## 12. Pendências e decisões
- **Divergências v1 × v2 (vale a v2):** obrigação em atraso é calculada por data, não marcada por automação ([18](../../../docs/v2/18-regras-modulos-2.md), seção 6.2); estados de período e de lançamento são os da v2, não as colunas genéricas do kanban da v1; sem filtro de unidade, entidade ou filial (a plataforma não tem).
- **Sem DDL** para o contábil (defeito T-02 do [18](../../../docs/v2/18-regras-modulos-2.md), seção 6.2): campos, tipos e chaves ainda não definidos.
- **D-44:** tributos e obrigações fiscais da empresa desenvolvedora ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.3) não estão no inventário desta área. Proposta: incluir um módulo "Tributos e obrigações da empresa".
- **D-45:** papéis do contábil da plataforma. Proposta: `platform.accounting` (nível 1, lança e concilia) e `platform.accounting.manager` (nível 2, revisa, fecha e reabre período).
