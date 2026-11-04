# Plano de contas da entidade

- Portal: Gestão (`gestao.`)
- Área: Contábil e fiscal da entidade
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13); especificação da v1 absorvida integralmente (seção 14)
- Fonte da v2: [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.3; [18](../../../docs/v2/18-regras-modulos-2.md), seção 6
- Fonte da v1: [spec_gestao_contabil_fiscal_completo.md](../../../docs/v2/anexo-v1/spec_gestao_contabil_fiscal_completo.md) (294 linhas) — absorvida integralmente na seção 14

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. A seção 14 é o texto integral da v1, guardado para que nenhum detalhe se perca; quando ela disser algo diferente das seções 1 a 13, vale a v2. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Plano de contas, lançamentos e fechamento contábil da entidade, separado do contábil da plataforma.

## 3. Telas

- **Plano de contas** (árvore).
- **Lançamentos** (DataTable e formulário de partidas).
- **Fechamento de período** (fluxo com revisão).

## 4. Permissões por portal (extraídas do SDD)

Do [31](../../../docs/v2/31-matriz-portais-modulos.md):

| Portal | Teste de isolamento | Teste de permissão | Teste de fluxo principal | Teste de acessibilidade |
|---|---|---|---|---|
| Gestão | Cross-tenant e cross-unidade | Papel sem permissão não vê o módulo | Matrícula, cobrança, emissão de documento | Telas principais |

Do [31](../../../docs/v2/31-matriz-portais-modulos.md):

| Portal | Autenticação | Sessão | Dados e restrições especiais |
|---|---|---|---|
| Gestão | Senha e MFA conforme política da entidade ([06](../../../docs/v2/06-identidade-acesso.md), seção 5) | Padrão | Consulta por CPF com finalidade ([21](../../../docs/v2/21-busca-e-armazenamento.md), seção 6.8) |

## 5. Papéis

- `unit.accounting`: lançar e fechar; não fecha período com lançamento que criou sem revisão.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Fronteira plataforma × entidade ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.3); controles de período ([18](../../../docs/v2/18-regras-modulos-2.md), seção 6).

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

### 13.1 [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.3

##### 3.3 Financeiro e contábil: plataforma × entidade

| Assunto | Plataforma (portal do desenvolvedor) | Entidade (portal de gestão) |
|---|---|---|
| Receita | Assinaturas dos clientes ([20](../../../docs/v2/20-pagamentos-seguranca.md)) | Mensalidades e serviços de alunos |
| Despesa | Da própria empresa | Da entidade (fornecedor, folha) |
| Contábil | Plano de contas da empresa | Plano de contas da entidade, com centro de custo por unidade |
| Tributos | Da empresa | Retenções e apurações da entidade ([19](../../../docs/v2/19-regras-modulos-3.md) e v1 [`spec_gestao_contabil_fiscal_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_contabil_fiscal_completo.md), seção 6.5) |

**Proposta:** o módulo Financeiro e o Contábil são o mesmo código com dois donos de dado (banco master e banco de cada unidade). **Decidido** em 03/11/2026: a plataforma precisa dos módulos contábil e financeiro para a própria empresa.

### 13.2 [18](../../../docs/v2/18-regras-modulos-2.md), seção 6

#### 6. Contábil e Fiscal

##### 6.1 Controles de período (v1, seção 11.1)

| Regra | Detalhe |
|---|---|
| Período fechado | Edição e exclusão de lançamento bloqueadas. Correção só por lançamento de ajuste no período aberto, com motivo. |
| Competência | Data do lançamento dentro da competência declarada; competência inválida é `422`. |
| Fechamento | Bloqueado com pendência aberta de aprovação ou de conciliação. |
| Correção | Sempre com motivo obrigatório (v1, seção 8.1). |
| Aprovação automática | Só por regra cadastrada e auditada (v1, seção 10). |

##### 6.2 Estados

| Entidade | Estados |
|---|---|
| Período | `aberto`, `em_fechamento`, `fechado`, `reaberto` (com justificativa e permissão administrativa) |
| Lançamento | `rascunho`, `em_validacao`, `aprovado`, `estornado` |
| Obrigação fiscal | `pendente`, `transmitida`, `paga`, `em_atraso` (calculado por data) |

**Defeito:** sem DDL (T-02). Não há campos, tipos de valor nem chaves definidos para validar. **Resolvido em 04/11/2026:** DDL em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 18.

## 14. Conteúdo integral da v1 (absorvido)

### SPEC.md — Módulo Contábil e Fiscal

- Language Standard: Global English
#### 1. Objetivo do módulo
Este documento especifica o módulo Contábil e Fiscal completo para o SaaS TotusTuusSoftCloud, cobrindo páginas, controles, componentes de UI, automações, regras operacionais e integrações necessárias para operação empresarial em ambiente multi-tenant, multi-unidade e multi-usuário. A estrutura segue o padrão do projeto com PHP 8 puro, sem bibliotecas externas, usando identificadores `id`, `uuid` e `code` para ordenação, identidade interna e exposição externa. [cite:1][cite:2]

#### 2. Escopo funcional
O módulo deve cobrir escrituração, apuração, validação, conferência, emissão, fechamento, monitoramento e auditoria de rotinas contábeis e fiscais. O objetivo é permitir operação diária, fechamento mensal, revisão gerencial e rastreabilidade total de alterações, aprovações e integrações. [cite:2]

##### 2.1 Áreas cobertas
- Plano de contas.
- Lançamentos contábeis.
- Centros de custo e rateios.
- Livros, balancetes e demonstrações.
- Obrigações fiscais e apurações.
- Notas, documentos e retenções.
- Conciliações, pendências e exceções.
- Aprovações, alertas e auditoria. [cite:2]

#### 3. Estrutura de páginas
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

#### 4. Padrão de páginas
Toda página do módulo deve obedecer ao mesmo padrão visual e funcional para reduzir curva de aprendizado e facilitar manutenção. O layout recomendado é: cabeçalho com título, breadcrumbs, actions primárias, barra de filtros, widgets de resumo, área principal em datatable ou kanban, drawer lateral para detalhes e seção final para auditoria e histórico. [cite:1][cite:2]

##### 4.1 Controles globais por página
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

#### 5. Dashboard contábil/fiscal
O dashboard deve ser o painel central de controle da operação, com visão executiva, operacional e de exceções. Ele precisa responder rápido à pergunta: o que está certo, o que está pendente, o que venceu e o que precisa de ação imediata. [cite:2]

##### 5.1 Widgets obrigatórios
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

##### 5.2 Charts recomendados
- Linha de lançamentos por dia.
- Barra de tributos apurados por competência.
- Donut de status de obrigações.
- Coluna de documentos por tipo.
- Área de evolução de pendências.
- Radar opcional de conformidade por domínio. [cite:1][cite:3]

#### 6. Datatables por página
Cada datatable deve ter paginação, ordenação, filtros avançados, seleção em massa, colunas configuráveis, ações de linha, exportação e carregamento assíncrono. Sempre que houver risco de duplicidade ou inconsistência, o datatable deve mostrar status operacional e trilha de origem do dado. [cite:2]

##### 6.1 Plano de Contas
Colunas: `code`, `nome`, `tipo`, `grupo`, `nível`, `natureza`, `ativo`, `padrão`, `atualizado em`, `ações`. [cite:2]

##### 6.2 Lançamentos Contábeis
Colunas: `data`, `competência`, `documento`, `histórico`, `conta débito`, `conta crédito`, `centro de custo`, `valor`, `origem`, `status`, `ações`. [cite:2]

##### 6.3 Obrigações Fiscais
Colunas: `obrigação`, `período`, `tributo`, `vencimento`, `status`, `responsável`, `competência`, `protocolo`, `ações`. [cite:2]

##### 6.4 Documentos Fiscais
Colunas: `número`, `série`, `tipo`, `emitente`, `destinatário`, `data`, `valor`, `imposto`, `status`, `xml`, `ações`. [cite:2]

##### 6.5 Retenções e Tributos
Colunas: `tributo`, `base`, `alíquota`, `valor calculado`, `valor retido`, `diferença`, `competência`, `status`, `ações`. [cite:2]

##### 6.6 Conciliações
Colunas: `origem`, `conta`, `competência`, `valor sistema`, `valor externo`, `diferença`, `status`, `tratativa`, `ações`. [cite:2]

##### 6.7 Aprovações
Colunas: `item`, `tipo`, `solicitante`, `etapa`, `aprovador`, `prazo`, `status`, `prioridade`, `ações`. [cite:2]

##### 6.8 Auditoria e Logs
Colunas: `data`, `usuário`, `ação`, `módulo`, `entidade`, `antes`, `depois`, `origem`, `ip`, `ações`. [cite:2]

#### 7. Widgets por área
Os widgets devem servir como indicadores de estado e gatilhos de ação, não apenas como elementos visuais. Cada widget deve ter título, valor principal, tendência, período de referência e link de drill-down. [cite:2]

##### 7.1 Widgets do Plano de Contas
- Contas ativas.
- Contas analíticas.
- Contas sintéticas.
- Contas sem movimentação.
- Contas com inconsistência de vínculo. [cite:2]

##### 7.2 Widgets de Lançamentos
- Lançamentos pendentes de revisão.
- Lançamentos rejeitados.
- Lançamentos automatizados.
- Lançamentos por origem.
- Lançamentos com divergência. [cite:2]

##### 7.3 Widgets de Obrigações
- Próximas obrigações.
- Obrigações vencidas.
- Obrigações entregues.
- Obrigações com protocolo.
- Obrigações em análise. [cite:2]

##### 7.4 Widgets de Conciliação
- Pendências abertas.
- Diferença total conciliável.
- Diferenças críticas.
- Conciliações automáticas.
- Conciliações manuais. [cite:2]

#### 8. Drawers CRUD
Os drawers devem ser o padrão para criar, editar, visualizar e corrigir registros sem sair da página principal. Eles precisam abrir lateralmente, manter contexto, suportar abas internas e exibir validações em tempo real. [cite:1][cite:2]

##### 8.1 Conteúdo obrigatório do drawer
- Identificação principal.
- Dados fiscais ou contábeis essenciais.
- Campos obrigatórios com máscara.
- Campos condicionais por tipo.
- Histórico de alterações.
- Anexos e documentos relacionados.
- Validações e alertas.
- Ações rápidas: salvar, salvar e novo, cancelar, duplicar, inativar. [cite:2]

##### 8.2 Tipos de drawers
- Cadastro simples.
- Cadastro hierárquico.
- Edição completa.
- Visualização detalhada.
- Aprovação/reprovação.
- Correção com motivo obrigatório.
- Importação assistida. [cite:2]

#### 9. Kanban operacional
O kanban deve ser usado sempre que o fluxo tiver etapas claras e mutáveis, como revisão, validação, aprovação, envio, pendência e encerramento. Ele deve suportar drag and drop, contadores por coluna, prioridade visual e bloqueios por permissão. [cite:2]

##### 9.1 Kanbans recomendados
- Fechamento contábil mensal.
- Obrigações fiscais.
- Conciliações pendentes.
- Aprovações de lançamento.
- Tratativa de inconsistências.

##### 9.2 Colunas padrão
- Novo.
- Em análise.
- Em validação.
- Pendente de ajuste.
- Aguardando aprovação.
- Concluído.
- Rejeitado. [cite:2]

#### 10. Automações
As automações devem reduzir trabalho manual, evitar atraso e impedir que processos críticos dependam de conferência humana tardia. O módulo precisa permitir regras agendadas, disparos por evento e automações condicionais por status, competência, valor, prazo e tipo de documento. [cite:2]

##### 10.1 Automações mínimas
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

#### 11. Controles e validações
O módulo deve impedir inconsistências operacionais, tributárias e de segurança com validações em cadastro, lançamento, aprovação e fechamento. As regras precisam ser explícitas e rastreáveis, com mensagens objetivas para o usuário e registro técnico para auditoria. [cite:2]

##### 11.1 Controles obrigatórios
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

#### 12. Gerenciamentos
Os gerenciamentos são as telas e mecanismos administrativos para manter o módulo saudável em longo prazo. Eles devem cobrir cadastros-base, regras operacionais, integrações, permissões, parâmetros fiscais e estados de processamento. [cite:2]

##### 12.1 Gerenciamentos necessários
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

#### 13. Detalhes de UX
A experiência deve ser consistente com o restante do SaaS e privilegiar produtividade. Telas críticas devem evitar troca excessiva de página, usando drawers, filtros persistentes, ações rápidas e feedback visual claro. [cite:1][cite:2]

##### 13.1 Regras de interface
- Cabeçalho fixo com ações principais.
- Filtros persistentes entre navegações.
- Estados vazios com chamada para ação.
- Skeleton loading para tabelas e widgets.
- Badge de status com cores padronizadas.
- Confirmação para ações destrutivas.
- Toasts para sucesso e erro.
- Histórico lateral acessível em qualquer detalhe. [cite:2]

#### 14. Segurança e auditoria
Como o módulo trata dados sensíveis, toda ação deve ser auditável e compatível com um ambiente empresarial multi-tenant. O sistema precisa registrar quem fez, quando fez, de onde fez e qual foi o antes/depois de cada alteração relevante. [cite:2]

##### 14.1 Eventos auditáveis
- Criação, edição e exclusão.
- Aprovação e reprovação.
- Reabertura de período.
- Importação e exportação.
- Alteração de status.
- Troca de responsável.
- Ajuste manual de valores.
- Reprocessamento de obrigação.

#### 15. Padrão de componentes
O módulo deve usar componentes reaproveitáveis para garantir consistência e velocidade de desenvolvimento. O ideal é que datatable, drawer, widget, chart, tag de status, timeline e kanban sejam componentes padrão reutilizados por todas as páginas. [cite:1][cite:2][cite:3]

##### 15.1 Componentes base
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

#### 16. Requisitos não funcionais
O módulo deve ser rápido, previsível, escalável e fácil de manter. Cada página precisa carregar com performance adequada em ambientes com muitos registros e múltiplos contextos de entidade e unidade. [cite:2]

##### 16.1 Requisitos mínimos
- Paginação server-side.
- Busca otimizada por índices.
- Cache de agregações quando aplicável.
- Proteção contra repetição de submissão.
- Logs de erro com contexto.
- Respostas JSON padronizadas em ações assíncronas.
- Estrutura pronta para crescimento incremental. [cite:2]

#### 17. Checklist de páginas completas
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

#### 18. Prioridade de implementação
A sequência recomendada é começar pelo dashboard, plano de contas, lançamentos, obrigações, documentos fiscais e conciliações. Depois disso, entram aprovações, fechamento, relatórios gerenciais, automações avançadas e refinamentos visuais. [cite:2]

#### 19. Entrega esperada
O resultado final deve permitir que o usuário trabalhe o ciclo completo: cadastrar, importar, conferir, aprovar, conciliar, apurar, fechar, auditar e reportar, tudo em páginas completas com controles suficientes para operação real. [cite:2]
