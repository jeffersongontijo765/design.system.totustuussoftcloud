# Plano de contas

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Contábil da plataforma
- Domínio: plataforma (banco master). Mesmo código do contábil da entidade, com outro dono de dado ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.3)
- Escopo: Plano de contas da empresa desenvolvedora, com hierarquia
- Status: detalhado (SDD 18 e v1); D-44 e D-45 pendentes

## 1. Identificação
- Especificações: [18](../../../docs/v2/18-regras-modulos-2.md), seção 6 (período, competência, estados); [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.3 (plataforma × entidade); [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5 (segregação do contábil); v1 [spec_gestao_contabil_fiscal_completo.md](../../../docs/v2/anexo-v1/spec_gestao_contabil_fiscal_completo.md) (telas, colunas, widgets, drawers, kanban).
- Regra de fonte: onde a v1 e a v2 divergem, vale a v2.

## 2. Objetivo e escopo
Manter o plano de contas da própria empresa, separado do plano de contas de cada entidade ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.3).

## 3. Telas
- **Plano de contas** (datatable e árvore; v1 seções 3 e 6.1). Colunas: código, nome, tipo, grupo, nível, natureza, ativo, padrão, atualizado em, ações.
- **Drawer de conta** (cadastro hierárquico; v1 seção 8): identificação, natureza, conta pai, situação, histórico de alterações.
- **Widgets** do plano (v1 seção 7.1) na seção 6.

## 4. Dados
- Conta: código, nome, tipo (sintética ou analítica), grupo, nível, natureza, conta pai, situação.
- Relação entre conta contábil e linha da DRE do financeiro ([71](../../../docs/v2/71-financeiro-completo-por-portal.md), seção 8): **[Sem detalhamento]**.

## 5. Campos e validações
- Código único no plano. Conta com movimentação não é excluída: só inativada.
- Conta analítica não tem filhas; sintética não recebe lançamento: **[Sem detalhamento]** (regra usual, não escrita no SDD).

## 6. Indicadores e gráficos
- Contas ativas, analíticas, sintéticas, sem movimentação e com inconsistência de vínculo (v1 seção 7.1).

## 7. Ações e confirmações
- Criar, editar, inativar, duplicar. Excluir conta sem uso: confirmação digitando o código da conta (SDD 08, seção 3).

## 8. Permissões e papéis
- Papéis do contábil da plataforma: **pendência D-45** ([78](../../../docs/v2/78-permissoes-e-papeis.md), seção 6).
- Segregação: quem criou o lançamento não fecha o período sem revisão de outra pessoa ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5).

## 9. Exportação e auditoria
- Auditoria de criação, edição, inativação e mudança de hierarquia (v1 seção 14.1). Exportação CSV, XLSX e PDF.

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
