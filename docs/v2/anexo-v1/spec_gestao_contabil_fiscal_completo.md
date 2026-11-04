# SPEC.md — Módulo Contábil e Fiscal

- Language Standard: Global English
## 1. Objetivo do módulo
Este documento especifica o módulo Contábil e Fiscal completo para o SaaS TotusTuusSoftCloud, cobrindo páginas, controles, componentes de UI, automações, regras operacionais e integrações necessárias para operação empresarial em ambiente multi-tenant, multi-unidade e multi-usuário. A estrutura segue o padrão do projeto com PHP 8 puro, sem bibliotecas externas, usando identificadores `id`, `uuid` e `code` para ordenação, identidade interna e exposição externa. [cite:1][cite:2]

## 2. Escopo funcional
O módulo deve cobrir escrituração, apuração, validação, conferência, emissão, fechamento, monitoramento e auditoria de rotinas contábeis e fiscais. O objetivo é permitir operação diária, fechamento mensal, revisão gerencial e rastreabilidade total de alterações, aprovações e integrações. [cite:2]

### 2.1 Áreas cobertas
- Plano de contas.
- Lançamentos contábeis.
- Centros de custo e rateios.
- Livros, balancetes e demonstrações.
- Obrigações fiscais e apurações.
- Notas, documentos e retenções.
- Conciliações, pendências e exceções.
- Aprovações, alertas e auditoria. [cite:2]

## 3. Estrutura de páginas
Abaixo está a estrutura completa sugerida de páginas para o módulo, com foco em cobertura operacional e controle gerencial. Cada página deve existir em versão de listagem, detalhe, criação/edição, histórico e trilha de auditoria quando aplicável. [cite:2]

| Página | Finalidade | Tipo de controle principal |
|---|---|---|
| Dashboard | Visão executiva contábil/fiscal | Widgets, charts, KPIs |
| Plano de Contas | Cadastro e hierarquia | Datatable, drawer CRUD, árvore |
| Lançamentos Contábeis | Escrituração manual e importada | Datatable, drawer, validação |
| Rateios e Centros de Custo | Distribuição analítica | Datatable, kanban de pendências |
| Fechamento Contábil | Controle do ciclo mensal | Kanban, checklist, automações |
| Obrigações Fiscais | Controle de entregas e apurações | Datatable, alertas, status |
| Documentos Fiscais | NF, XML, eventos e anexos | Datatable, preview, drawers |
| Retenções e Tributos | Regras e apurações tributárias | Datatable, charts, alertas |
| Conciliações | Bancária, contábil e fiscal | Datatable, kanban, automações |
| Relatórios Gerenciais | Análises e exportações | Charts, filtros, widgets |
| Aprovações | Workflow de revisão | Kanban, filas, decisões |
| Auditoria e Logs | Rastreabilidade completa | Datatable, timeline, filtros |

## 4. Padrão de páginas
Toda página do módulo deve obedecer ao mesmo padrão visual e funcional para reduzir curva de aprendizado e facilitar manutenção. O layout recomendado é: cabeçalho com título, breadcrumbs, actions primárias, barra de filtros, widgets de resumo, área principal em datatable ou kanban, drawer lateral para detalhes e seção final para auditoria e histórico. [cite:1][cite:2]

### 4.1 Controles globais por página
- Filtro por período.
- Filtro por unidade, entidade e filial.
- Filtro por status.
- Busca textual com debounce.
- Exportação CSV, PDF e XLSX.
- Botão de importar dados.
- Botão de recarregar.
- Seletor de colunas visíveis.
- Ações em massa.
- Botão de criar novo registro.
- Atalho para auditoria e histórico. [cite:2]

## 5. Dashboard contábil/fiscal
O dashboard deve ser o painel central de controle da operação, com visão executiva, operacional e de exceções. Ele precisa responder rápido à pergunta: o que está certo, o que está pendente, o que venceu e o que precisa de ação imediata. [cite:2]

### 5.1 Widgets obrigatórios
- Total de lançamentos do período.
- Total de documentos fiscais processados.
- Pendências de conciliação.
- Obrigações vencendo em até 7 dias.
- Obrigações em atraso.
- Valor total apurado por tributo.
- Saldo contábil consolidado.
- Alertas críticos abertos.
- Itens aguardando aprovação.
- Fechamentos mensais concluídos versus pendentes. [cite:2]

### 5.2 Charts recomendados
- Linha de lançamentos por dia.
- Barra de tributos apurados por competência.
- Donut de status de obrigações.
- Coluna de documentos por tipo.
- Área de evolução de pendências.
- Radar opcional de conformidade por domínio. [cite:1][cite:3]

## 6. Datatables por página
Cada datatable deve ter paginação, ordenação, filtros avançados, seleção em massa, colunas configuráveis, ações de linha, exportação e carregamento assíncrono. Sempre que houver risco de duplicidade ou inconsistência, o datatable deve mostrar status operacional e trilha de origem do dado. [cite:2]

### 6.1 Plano de Contas
Colunas: `code`, `nome`, `tipo`, `grupo`, `nível`, `natureza`, `ativo`, `padrão`, `atualizado em`, `ações`. [cite:2]

### 6.2 Lançamentos Contábeis
Colunas: `data`, `competência`, `documento`, `histórico`, `conta débito`, `conta crédito`, `centro de custo`, `valor`, `origem`, `status`, `ações`. [cite:2]

### 6.3 Obrigações Fiscais
Colunas: `obrigação`, `período`, `tributo`, `vencimento`, `status`, `responsável`, `competência`, `protocolo`, `ações`. [cite:2]

### 6.4 Documentos Fiscais
Colunas: `número`, `série`, `tipo`, `emitente`, `destinatário`, `data`, `valor`, `imposto`, `status`, `xml`, `ações`. [cite:2]

### 6.5 Retenções e Tributos
Colunas: `tributo`, `base`, `alíquota`, `valor calculado`, `valor retido`, `diferença`, `competência`, `status`, `ações`. [cite:2]

### 6.6 Conciliações
Colunas: `origem`, `conta`, `competência`, `valor sistema`, `valor externo`, `diferença`, `status`, `tratativa`, `ações`. [cite:2]

### 6.7 Aprovações
Colunas: `item`, `tipo`, `solicitante`, `etapa`, `aprovador`, `prazo`, `status`, `prioridade`, `ações`. [cite:2]

### 6.8 Auditoria e Logs
Colunas: `data`, `usuário`, `ação`, `módulo`, `entidade`, `antes`, `depois`, `origem`, `ip`, `ações`. [cite:2]

## 7. Widgets por área
Os widgets devem servir como indicadores de estado e gatilhos de ação, não apenas como elementos visuais. Cada widget deve ter título, valor principal, tendência, período de referência e link de drill-down. [cite:2]

### 7.1 Widgets do Plano de Contas
- Contas ativas.
- Contas analíticas.
- Contas sintéticas.
- Contas sem movimentação.
- Contas com inconsistência de vínculo. [cite:2]

### 7.2 Widgets de Lançamentos
- Lançamentos pendentes de revisão.
- Lançamentos rejeitados.
- Lançamentos automatizados.
- Lançamentos por origem.
- Lançamentos com divergência. [cite:2]

### 7.3 Widgets de Obrigações
- Próximas obrigações.
- Obrigações vencidas.
- Obrigações entregues.
- Obrigações com protocolo.
- Obrigações em análise. [cite:2]

### 7.4 Widgets de Conciliação
- Pendências abertas.
- Diferença total conciliável.
- Diferenças críticas.
- Conciliações automáticas.
- Conciliações manuais. [cite:2]

## 8. Drawers CRUD
Os drawers devem ser o padrão para criar, editar, visualizar e corrigir registros sem sair da página principal. Eles precisam abrir lateralmente, manter contexto, suportar abas internas e exibir validações em tempo real. [cite:1][cite:2]

### 8.1 Conteúdo obrigatório do drawer
- Identificação principal.
- Dados fiscais ou contábeis essenciais.
- Campos obrigatórios com máscara.
- Campos condicionais por tipo.
- Histórico de alterações.
- Anexos e documentos relacionados.
- Validações e alertas.
- Ações rápidas: salvar, salvar e novo, cancelar, duplicar, inativar. [cite:2]

### 8.2 Tipos de drawers
- Cadastro simples.
- Cadastro hierárquico.
- Edição completa.
- Visualização detalhada.
- Aprovação/reprovação.
- Correção com motivo obrigatório.
- Importação assistida. [cite:2]

## 9. Kanban operacional
O kanban deve ser usado sempre que o fluxo tiver etapas claras e mutáveis, como revisão, validação, aprovação, envio, pendência e encerramento. Ele deve suportar drag and drop, contadores por coluna, prioridade visual e bloqueios por permissão. [cite:2]

### 9.1 Kanbans recomendados
- Fechamento contábil mensal.
- Obrigações fiscais.
- Conciliações pendentes.
- Aprovações de lançamento.
- Tratativa de inconsistências.

### 9.2 Colunas padrão
- Novo.
- Em análise.
- Em validação.
- Pendente de ajuste.
- Aguardando aprovação.
- Concluído.
- Rejeitado. [cite:2]

## 10. Automações
As automações devem reduzir trabalho manual, evitar atraso e impedir que processos críticos dependam de conferência humana tardia. O módulo precisa permitir regras agendadas, disparos por evento e automações condicionais por status, competência, valor, prazo e tipo de documento. [cite:2]

### 10.1 Automações mínimas
- Geração de alerta antes do vencimento.
- Marcação de atraso automático.
- Aprovação automática por regra.
- Bloqueio de fechamento com pendência aberta.
- Sugestão de conta contábil por histórico.
- Classificação automática por natureza.
- Importação e triagem de documentos.
- Reprocessamento de inconsistências.
- Envio de notificações por status crítico.
- Registro automático em trilha de auditoria. [cite:2]

## 11. Controles e validações
O módulo deve impedir inconsistências operacionais, tributárias e de segurança com validações em cadastro, lançamento, aprovação e fechamento. As regras precisam ser explícitas e rastreáveis, com mensagens objetivas para o usuário e registro técnico para auditoria. [cite:2]

### 11.1 Controles obrigatórios
- Bloqueio de edição em período fechado.
- Permissão por perfil, unidade e entidade.
- Separação entre visualizar, editar, aprovar e excluir.
- Validação de competência e período fiscal.
- Validação de totais e saldos.
- Consistência entre documento, lançamento e obrigação.
- Rastreamento de origem do registro.
- Controle de reabertura com justificativa.
- Controle de versão do registro.
- Controle de observação obrigatória em exceções. [cite:2]

## 12. Gerenciamentos
Os gerenciamentos são as telas e mecanismos administrativos para manter o módulo saudável em longo prazo. Eles devem cobrir cadastros-base, regras operacionais, integrações, permissões, parâmetros fiscais e estados de processamento. [cite:2]

### 12.1 Gerenciamentos necessários
- Gerenciamento de plano de contas.
- Gerenciamento de tributos.
- Gerenciamento de calendários fiscais.
- Gerenciamento de obrigações.
- Gerenciamento de centros de custo.
- Gerenciamento de rotinas automáticas.
- Gerenciamento de integrações externas.
- Gerenciamento de perfis e permissões.
- Gerenciamento de status e filas.
- Gerenciamento de mensagens e alertas. [cite:2]

## 13. Detalhes de UX
A experiência deve ser consistente com o restante do SaaS e privilegiar produtividade. Telas críticas devem evitar troca excessiva de página, usando drawers, filtros persistentes, ações rápidas e feedback visual claro. [cite:1][cite:2]

### 13.1 Regras de interface
- Cabeçalho fixo com ações principais.
- Filtros persistentes entre navegações.
- Estados vazios com chamada para ação.
- Skeleton loading para tabelas e widgets.
- Badge de status com cores padronizadas.
- Confirmação para ações destrutivas.
- Toasts para sucesso e erro.
- Histórico lateral acessível em qualquer detalhe. [cite:2]

## 14. Segurança e auditoria
Como o módulo trata dados sensíveis, toda ação deve ser auditável e compatível com um ambiente empresarial multi-tenant. O sistema precisa registrar quem fez, quando fez, de onde fez e qual foi o antes/depois de cada alteração relevante. [cite:2]

### 14.1 Eventos auditáveis
- Criação, edição e exclusão.
- Aprovação e reprovação.
- Reabertura de período.
- Importação e exportação.
- Alteração de status.
- Troca de responsável.
- Ajuste manual de valores.
- Reprocessamento de obrigação.

## 15. Padrão de componentes
O módulo deve usar componentes reaproveitáveis para garantir consistência e velocidade de desenvolvimento. O ideal é que datatable, drawer, widget, chart, tag de status, timeline e kanban sejam componentes padrão reutilizados por todas as páginas. [cite:1][cite:2][cite:3]

### 15.1 Componentes base
- `datatable`
- `drawer`
- `widget-card`
- `chart-card`
- `status-badge`
- `timeline`
- `kanban-board`
- `filter-bar`
- `export-menu`
- `audit-panel`

## 16. Requisitos não funcionais
O módulo deve ser rápido, previsível, escalável e fácil de manter. Cada página precisa carregar com performance adequada em ambientes com muitos registros e múltiplos contextos de entidade e unidade. [cite:2]

### 16.1 Requisitos mínimos
- Paginação server-side.
- Busca otimizada por índices.
- Cache de agregações quando aplicável.
- Proteção contra repetição de submissão.
- Logs de erro com contexto.
- Respostas JSON padronizadas em ações assíncronas.
- Estrutura pronta para crescimento incremental. [cite:2]

## 17. Checklist de páginas completas
Use este checklist para garantir que cada página esteja pronta para produção. [cite:2]

- Lista principal com filtros.
- Resumo em widgets.
- Gráficos relevantes.
- Criação via drawer.
- Edição via drawer.
- Visualização detalhada.
- Histórico e auditoria.
- Ações em massa.
- Exportação de dados.
- Estados de erro e vazio.
- Permissões aplicadas.
- Integrações e automações visíveis.

## 18. Prioridade de implementação
A sequência recomendada é começar pelo dashboard, plano de contas, lançamentos, obrigações, documentos fiscais e conciliações. Depois disso, entram aprovações, fechamento, relatórios gerenciais, automações avançadas e refinamentos visuais. [cite:2]

## 19. Entrega esperada
O resultado final deve permitir que o usuário trabalhe o ciclo completo: cadastrar, importar, conferir, aprovar, conciliar, apurar, fechar, auditar e reportar, tudo em páginas completas com controles suficientes para operação real. [cite:2]
