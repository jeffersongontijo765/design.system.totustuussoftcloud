# Acervo

- Portal: Gestão (`gestao.`)
- Área: Biblioteca
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13); especificação da v1 absorvida integralmente (seção 14)
- Fonte da v2: [68](../../../docs/v2/68-biblioteca-por-portal.md) (integral); [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.1
- Fonte da v1: [spec_gestao_biblioteca_completo.md](../../../docs/v2/anexo-v1/spec_gestao_biblioteca_completo.md) (1182 linhas); [spec_gestao_biblioteca_academica.md](../../../docs/v2/anexo-v1/spec_gestao_biblioteca_academica.md) (275 linhas) — absorvida integralmente na seção 14

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. A seção 14 é o texto integral da v1, guardado para que nenhum detalhe se perca; quando ela disser algo diferente das seções 1 a 13, vale a v2. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Catalogar obras e exemplares, perfis e prazos, inventário e baixa da biblioteca da unidade.

## 3. Telas

- **Acervo** (DataTable de obras; drawer com exemplares).
- **Obra — cadastro** (formulário com ISBN e classificação).
- **Exemplares** (lista com tombo e situação).
- **Inventário e baixa** (fluxo com aprovação).
- **Perfis e prazos** (configuração).

## 4. Permissões por portal (extraídas do SDD)

Do [68](../../../docs/v2/68-biblioteca-por-portal.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Ver indicadores e relatórios de circulação. Aprovar baixa e descarte | Emprestar, isentar multa ou editar acervo sem perfil de biblioteca | E |
| **Coordenação** | Ver relatórios de uso por curso e disciplina | Editar acervo ou empréstimo | E |

Do [31](../../../docs/v2/31-matriz-portais-modulos.md):

| Portal | Teste de isolamento | Teste de permissão | Teste de fluxo principal | Teste de acessibilidade |
|---|---|---|---|---|
| Gestão | Cross-tenant e cross-unidade | Papel sem permissão não vê o módulo | Matrícula, cobrança, emissão de documento | Telas principais |

Do [31](../../../docs/v2/31-matriz-portais-modulos.md):

| Portal | Autenticação | Sessão | Dados e restrições especiais |
|---|---|---|---|
| Gestão | Senha e MFA conforme política da entidade ([06](../../../docs/v2/06-identidade-acesso.md), seção 5) | Padrão | Consulta por CPF com finalidade ([21](../../../docs/v2/21-busca-e-armazenamento.md), seção 6.8) |

## 5. Papéis

- `unit.librarian`: acervo, inventário, perfis.
- `unit.manager`: aprovar baixa.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Fronteira com gestão de documentos ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.1).

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

### 13.1 [68 — Biblioteca (Acervo, Empréstimos, Reservas, Multas e Salas de Leitura), por Portal](../../../docs/v2/68-biblioteca-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Décima primeira lacuna da ordem de [55](../../../docs/v2/55-academico-verificacao-e-lacunas.md), seção 3. Fronteira com Gestão de Documentos em [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.1: biblioteca e documentos são módulos separados. Multas viram cobrança em [18](../../../docs/v2/18-regras-modulos-2.md). Aquisição em [17](../../../docs/v2/17-regras-modulos.md), suprimentos. Patrimônio e baixa em [19](../../../docs/v2/19-regras-modulos-3.md), seção 8. Salas de leitura usam o cadastro de recursos de [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md) e [60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md), seção 2.2. Avisos de prazo em [57](../../../docs/v2/57-notificacoes-por-portal.md). Busca no acervo em [21](../../../docs/v2/21-busca-e-armazenamento.md), seção 6. Bibliografia do plano em [64](../../../docs/v2/64-planos-de-aula-e-de-ensino-por-portal.md). Auditoria em [29](../../../docs/v2/29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha a lacuna 11 do acadêmico. A referência de domínio é [`spec_gestao_biblioteca_academica.md`](../../../docs/v2/anexo-v1/spec_gestao_biblioteca_academica.md) (v1, Draft). O [`spec_gestao_biblioteca_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_biblioteca_completo.md) é design de interface e não é usado aqui, conforme [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.1.

---

#### 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| Biblioteca tem especificação na v2? | **Não.** Só citada como módulo em [31](../../../docs/v2/31-matriz-portais-modulos.md) e como lacuna em [56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md) |
| Domínio na v1? | **Sim, em rascunho.** Acervo, exemplar, empréstimo, reserva, multa, inventário, salas e biblioteca digital. Tem modelo de dados e API |
| Separada de documentos? | **Sim**, em [31](../../../docs/v2/31-matriz-portais-modulos.md). A página de gestão de documentos sai da UI da biblioteca |
| Problemas da v1 a corrigir? | **Sim:** tabelas sem `tenant_id` (T-01), seção 3 numerada duas vezes, salas de leitura duplicadas do agendamento, aquisição duplicada de suprimentos |

---

#### 2. Escopo

Entra: catálogo (livros, periódicos, mídias, e-books e TCCs), exemplares com código de barras, empréstimo e devolução, renovação, reserva com fila, multas, inventário, baixa e descarte, biblioteca digital e indicadores.

Não entra:

- **Documento oficial** de aluno ou funcionário. É [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md).
- **Arquivo morto** de documentos escolares. É [67](../../../docs/v2/67-livros-digitais-e-arquivo-morto-por-portal.md).
- **Pedido de compra** do acervo. Fica em suprimentos (BIB-03).
- **Cobrança de multa.** Gera fatura no financeiro, como em [18](../../../docs/v2/18-regras-modulos-2.md).
- **Sala de reunião e de aula.** Usa o cadastro de recursos de [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md).

---

#### 3. Acervo e exemplares

- **Item** é a obra: título, autores, ISBN ou ISSN, editora, edição, ano, idioma, categoria e sinopse.
- **Exemplar** é a cópia física: código de barras único, localização (estante e prateleira), estado de conservação e situação.
- **Situação do exemplar:** `disponivel`, `emprestado`, `reservado`, `em_manutencao`, `baixado`.
- **Item digital** tem arquivo, licença e número de licenças simultâneas (seção 8).
- **Tombamento:** código de tombamento é único na unidade. O acervo fica só no módulo de biblioteca, com valor de aquisição. Não entra no patrimônio (BIB-02).

---

#### 4. Perfis e prazos

| Perfil | Empréstimos simultâneos | Prazo | Renovação |
|---|---|---|---|
| Aluno | 3 itens | 7 dias | Até 2 vezes, se não houver reserva de outro usuário |
| Professor | 5 itens | 30 dias | Mesma regra do aluno |
| Servidor | 5 itens | 30 dias | Mesma regra do aluno |

**Regra:** os valores da tabela são o ponto de partida de toda unidade nova. A escola altera por perfil e por categoria de item. **Decidido** em 03/11/2026 (BIB-04).

---

#### 5. Empréstimo, devolução e reserva

##### 5.1 Empréstimo

- Só com usuário com vínculo ativo: matrícula ativa para aluno, vínculo ativo para professor e servidor ([46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md) e [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md)).
- Bloqueado com multa em aberto ou item atrasado.
- Retirada com busca por código de barras ou título. Confirmação de retirada pode ser assinada, se a escola exigir.

##### 5.2 Renovação

- Bloqueada se o item tiver reserva pendente de outro usuário.
- As renovações são contadas no empréstimo. Depois do limite, só devolução.

##### 5.3 Reserva

- Fila por item indisponível. Quando o exemplar volta, o próximo da fila é avisado ([57](../../../docs/v2/57-notificacoes-por-portal.md)).
- Reserva tem prazo de retirada. Expirado, passa ao próximo da fila.

##### 5.4 Devolução

- Devolução dentro da tolerância baixa a multa automaticamente.
- Exemplar devolvido em estado danificado vira `em_manutencao` até a avaliação do bibliotecário.

---

#### 6. Multas

- Valor por dia de atraso e teto por item são configurados pela escola, por categoria.
- Multa confirmada gera fatura no financeiro ([18](../../../docs/v2/18-regras-modulos-2.md)). A baixa da fatura volta para a biblioteca.
- Isenção exige justificativa e aprovação do bibliotecário ou da coordenação (BIB-06). Quem isenta não isenta a própria multa.
- O responsável financeiro vê só valor e situação da multa, sem título do livro. Regra de [31](../../../docs/v2/31-matriz-portais-modulos.md) e da v1.

---

#### 7. Inventário e baixa

- Inventário por estante, setor ou geral. Contagem com leitor de código de barras ou QR.
- Divergências (não encontrado, fora do lugar) geram relatório.
- Baixa por extravio exige aprovação do bibliotecário. Como o acervo não é patrimônio (BIB-02), a baixa não passa pelo patrimônio.
- Doação e descarte seguem regra própria: lista, termo e aprovação da gestão. Descarte de obra rara exige justificativa.

---

#### 8. Biblioteca digital

- E-books e PDFs com licença de uso. Quando a licença tem limite, o número de empréstimos simultâneos é controlado e expira sozinho.
- Leitura embutida, sem download quando a licença exigir.
- Marca d'água com identificação do leitor é dado pessoal. Só com base legal confirmada (BIB-05).
- Histórico de leitura é dado do aluno. Não aparece para professor nem responsável.

---

#### 9. Salas de leitura

- Salas e cabines são recursos de [44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md), com capacidade e regra de reserva. Não há cadastro de sala próprio na biblioteca.
- Reserva por aluno ou professor, com horário e duração máxima.
- Check-in obrigatório para validar a reserva.

---

#### 10. Empréstimo entre unidades

- Unidades têm banco próprio ([03](../../../docs/v2/03-dominio-tenancy.md)). Empréstimo entre unidades exige transferência de registro, não consulta direta ao banco da outra unidade.
- **Decidido** em 03/11/2026 (BIB-01): o empréstimo é pedido pela unidade de destino e aprovado pela unidade de origem. Só o registro do exemplar e do usuário é transferido.

---

#### 11. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Ver métricas agregadas de uso, sem dado de acervo ou empréstimo | Ver acervo, empréstimo, multa ou histórico de leitura | P |
| **Gestão** | Ver indicadores e relatórios de circulação. Aprovar baixa e descarte | Emprestar, isentar multa ou editar acervo sem perfil de biblioteca | E |
| **Bibliotecário** (perfil da unidade) | Gerir acervo, empréstimo, multa, inventário, salas e biblioteca digital | Aprovar a própria isenção de multa | E |
| **Auxiliar de biblioteca** (perfil da unidade) | Emprestar e devolver. Lançar reserva | Gerir acervo. Isentar multa | E |
| **Coordenação** | Ver relatórios de uso por curso e disciplina | Editar acervo ou empréstimo | E |
| **Professor** | Consultar catálogo. Emprestar com prazo próprio. Reservar sala. Ver os próprios empréstimos | Ver empréstimo ou multa de outro usuário | E |
| **Aluno** | Consultar catálogo. Emprestar, reservar e renovar. Ver as próprias multas. Biblioteca digital | Ver empréstimo ou histórico de leitura de colega | E |
| **Responsáveis** | Ver empréstimos e multas do dependente, só leitura | Pagar, isentar ou ver título e histórico de leitura | E, só dependentes com vínculo ativo |
| **Responsável financeiro** (função dentro de responsáveis) | Ver valor e situação da multa do aluno sob sua responsabilidade, com link para quitar no financeiro | Ver título, categoria ou histórico | E |
| **Terceiros** | Nada por padrão. Acesso só por permissão explícita da entidade | Qualquer item sem permissão | E |

---

#### 12. Integrações

| Módulo | Relação |
|---|---|
| Acadêmico ([46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md), [60](../../../docs/v2/60-turmas-e-grade-de-horarios-por-portal.md)) | Validação de matrícula ativa. Turma e disciplina para relatórios |
| Pessoas ([39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md)) | Vínculo ativo de professor e servidor |
| Financeiro ([18](../../../docs/v2/18-regras-modulos-2.md)) | Fatura de multa e baixa |
| Suprimentos ([17](../../../docs/v2/17-regras-modulos.md)) | Aquisição: pedido de compra e nota fiscal |
| Patrimônio ([19](../../../docs/v2/19-regras-modulos-3.md), seção 8) | Baixa de item patrimonial |
| Recursos ([44](../../../docs/v2/44-agendamento-ambientes-equipamentos.md)) | Salas e cabines |
| Plano de ensino ([64](../../../docs/v2/64-planos-de-aula-e-de-ensino-por-portal.md)) | Bibliografia referencia o acervo quando o item existe |
| Busca ([21](../../../docs/v2/21-busca-e-armazenamento.md)) | Busca no acervo, com o escopo de permissão |
| Notificações ([57](../../../docs/v2/57-notificacoes-por-portal.md)) | Vencimento, atraso, reserva liberada |
| Relatórios ([56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 7) | Circulação e busca geral de bibliografia |

---

#### 13. Pendências

| # | Pendência | Tipo |
|---|---|---|
| BIB-01 | Empréstimo entre unidades (seção 10) | **Decidido** em 03/11/2026: sim, com pedido e aprovação da origem |
| BIB-02 | O acervo é patrimônio ou fica só na biblioteca (seções 3 e 7) | **Decidido** em 03/11/2026: só na biblioteca. Confirmar com (contábil) a classificação do acervo |
| BIB-03 | Aquisição do acervo (seção 2) | **Decidido** em 03/11/2026: pelo suprimentos, com pedido de compra e nota fiscal |
| BIB-04 | Limites, prazos e renovações por perfil (seção 4) | **Decidido** em 03/11/2026: valor inicial da plataforma, que a escola ajusta |
| BIB-05 | Marca d'água de leitura digital com identificação do leitor: base legal e licença do editor (seção 8) | (jurídico) |
| BIB-06 | Quem pode isentar multa (seção 6) | **Decidido** em 03/11/2026: bibliotecário ou coordenação, sem isentar a própria multa |
| BIB-07 | Guarda de histórico de leitura e de empréstimo, e prazo de eliminação | (jurídico) |
| BIB-08 | DDL: reescrever com `unidade_uuid`, chave interna e `uuid` do padrão de [51](../../../docs/v2/51-ddl-modulos-novos.md). Corrige T-01 | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 15.13. Revisão do owner pendente (DDL-01). Corrige T-01 |

---

#### 14. Critérios de aceite

- [ ] Empréstimo com multa em aberto é recusado (teste).
- [ ] Reserva é liberada ao próximo da fila na devolução (teste).
- [ ] Renovação com reserva de outro usuário é recusada (teste).
- [ ] Usuário sem vínculo ativo não empresta (teste de integração com [46](../../../docs/v2/46-matricula-e-rematricula-por-portal.md)).
- [ ] Responsável não vê título nem histórico de leitura (teste de isolamento).
- [ ] Responsável financeiro não vê título nem categoria (varredura da API de multa).
- [ ] Bibliotecário não isenta a própria multa (teste).
- [ ] Empréstimo entre unidades não consulta o banco da outra unidade (teste de isolamento).
- [ ] Itens **(verificar)**, **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).

### 13.2 [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.1

##### 3.1 Biblioteca × Gestão de Documentos

**Problema encontrado:** a especificação [`spec_gestao_biblioteca_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_biblioteca_completo.md) (UI enterprise) inclui páginas de gestão de usuários, perfis, auditoria, integrações e **"Gestão de Documentos e Anexos"** (página 14). Isso mistura o acervo da biblioteca com o cofre de documentos da entidade.

**Decisão proposta:**

| Módulo | Dono | Guarda | Não guarda |
|---|---|---|---|
| Biblioteca | Acervo, exemplar, empréstimo, reserva, multa | Metadados do acervo; arquivo digital do acervo via [21](../../../docs/v2/21-busca-e-armazenamento.md) | Documento oficial de aluno ou de funcionário |
| Gestão de documentos | Documento oficial, versão, assinatura, validação, modelo | Declarações, históricos, certidões, contratos assinados | Exemplar físico, empréstimo |

A página 14 da UI de biblioteca sai dela. A "Interface de biblioteca (UI)" do catálogo deixa de ser módulo e passa a ser componentes de [08](../../../docs/v2/08-frontend-design-system.md). As páginas 6 a 13 da UI são padrões de tela, não módulos.

## 14. Conteúdo integral da v1 (absorvido)

### Fonte: spec_gestao_biblioteca_completo.md

#### Spec Completo — Biblioteca UI Enterprise

- Language Standard: Global English
Documento de especificação funcional e estrutural para uma biblioteca de páginas, blocos e componentes reutilizáveis voltada a sistemas SaaS administrativos, operacionais e analíticos. O escopo cobre DataTables, widgets, charts, CRUD em drawers, Kanban, automações, controles e páginas de gerenciamento completas, com foco em consistência de design system, acessibilidade, segurança operacional e alta reutilização entre módulos.[cite:1]

##### Objetivo

Esta biblioteca deve servir como base única para construção de backoffice, painéis operacionais, módulos administrativos, fluxos transacionais e interfaces analíticas, reduzindo divergência visual e técnica entre produtos.[cite:1]

A arquitetura da biblioteca deve priorizar composição por blocos, estados previsíveis, responsividade, acessibilidade, performance e capacidade de extensão por domínio, como financeiro, educacional, saúde, CRM, estoque, suporte e compliance.[cite:1]

##### Princípios da biblioteca

- Design system centralizado com tokens de cor, espaçamento, tipografia, radius, sombra e estados interativos.[cite:1]
- Componentes stateless na camada visual e integração por adapters para dados, autenticação, permissão e telemetria.[cite:1]
- Todos os blocos devem prever estados de loading, vazio, erro, sucesso, bloqueado por permissão e somente leitura.[cite:1]
- Toda ação crítica deve suportar confirmação, auditoria e feedback transacional claro.[cite:1]
- Os componentes devem funcionar em tema claro e escuro, desktop e mobile, com foco inicial em desktop administrativo.[cite:1]

##### Estrutura macro da biblioteca

A biblioteca deve ser organizada em sete camadas principais, permitindo adoção incremental por equipes diferentes.[cite:1]

###### 1. Foundations

- Tokens de cor semântica.
- Tipografia.
- Grid e spacing.
- Iconografia.
- Elevação.
- Motion.
- Breakpoints.
- Acessibilidade.
- Internacionalização.
- Estados globais.[cite:1]

###### 2. Átomos

- Button.
- IconButton.
- Input.
- Textarea.
- Select.
- MultiSelect.
- Checkbox.
- Radio.
- Switch.
- Tag.
- Badge.
- Avatar.
- Tooltip.
- Divider.
- Tabs.
- Breadcrumb.
- Pagination.
- EmptyState.
- Skeleton.
- Alert.[cite:1]

###### 3. Moléculas

- Search bar.
- Filter bar.
- Date range picker.
- Field group.
- Inline validation block.
- KPI card.
- Stat block.
- Action group.
- Upload area.
- Row actions.
- Table toolbar.
- Quick filters.
- Step header.
- Audit snippet.[cite:1]

###### 4. Organismos

- DataTable full.
- Form drawer.
- Detail drawer.
- Side panel.
- Modal de confirmação.
- Kanban board.
- Widget containers.
- Dashboard sections.
- Automation builder.
- Permission matrix.
- Activity timeline.
- Comment thread.
- Bulk action panel.[cite:1]

###### 5. Templates

- Listagem com filtros.
- Dashboard analítico.
- CRUD master-detail.
- Gestão por Kanban.
- Tela de automações.
- Tela de configurações.
- Tela de permissões.
- Tela de auditoria.
- Tela de detalhes de entidade.[cite:1]

###### 6. Pages

Cada página deve ser empacotada como blueprint completo, com áreas, componentes, estados, eventos, permissões, ações e contratos de integração.[cite:1]

###### 7. Domain packs

Pacotes opcionais por domínio, como alunos, pacientes, contratos, tickets, usuários, unidades, convênios, pagamentos, estoque, documentos e consentimentos.[cite:1]

##### Convenções globais

###### Layout base

Toda página deve seguir a seguinte estrutura visual.[cite:1]

1. Header da página com título, subtítulo, breadcrumbs e ações primárias.
2. Barra contextual com filtros, busca, segmentadores, chips e ações secundárias.
3. Conteúdo principal em grid responsivo.
4. Painéis auxiliares opcionais, como resumo, auditoria ou atalhos.
5. Rodapé contextual com contagem, paginação, seleção ou status da operação.[cite:1]

###### Estados obrigatórios por componente

Cada componente de alto nível deve suportar, no mínimo, os estados abaixo.[cite:1]

| Estado | Obrigatório | Comportamento |
|---|---|---|
| Loading | Sim | Skeleton ou spinner contextual sem quebrar layout. [cite:1] |
| Empty | Sim | Mensagem clara, CTA e orientação do próximo passo. [cite:1] |
| Error | Sim | Erro amigável, código opcional, ação de retry. [cite:1] |
| Success | Sim | Feedback visual e textual após operação. [cite:1] |
| Disabled | Sim | Bloqueio visual e semântico. [cite:1] |
| Read only | Sim | Visualização sem affordance de edição. [cite:1] |
| Permission denied | Sim | Mensagem de acesso restrito e trilha de solicitação. [cite:1] |

###### Telemetria mínima

Todo bloco acionável deve permitir instrumentação de eventos como view, click, submit, error, retry, export, import, approve, reject, drag, drop, reorder e bulk_action.[cite:1]

###### Segurança operacional

A biblioteca deve prever hooks para mascaramento de dados sensíveis, bloqueio por escopo, confirmação de ações destrutivas, trilha de auditoria e política de visibilidade por role, tenant, unidade e entidade.[cite:1]

##### Módulo 1 — DataTable completo

O DataTable é um dos pilares da biblioteca e deve ser entregue em versão enterprise, cobrindo cenários simples e densos.[cite:1]

###### Objetivos do DataTable

- Exibir grandes volumes de registros.
- Permitir busca, filtro, ordenação e paginação.
- Suportar seleção em massa e ações em lote.
- Expor colunas configuráveis por contexto e perfil.
- Ser reutilizável em qualquer entidade de negócio.[cite:1]

###### Estrutura visual do DataTable

- Toolbar superior.
- Linha de filtros rápidos.
- Área de tabela.
- Cabeçalho com ordenação.
- Coluna de seleção opcional.
- Coluna de ações fixada à direita.
- Rodapé com paginação e resumo.[cite:1]

###### Controles obrigatórios

- Campo de busca global.
- Filtros avançados.
- Ordenação por coluna.
- Redimensionamento de coluna.
- Reordenação de colunas.
- Toggle de visibilidade de colunas.
- Fixação de colunas críticas.
- Paginação server-side ou client-side.
- Seletor de densidade da tabela.
- Seletor de quantidade por página.
- Exportar CSV/XLSX/PDF quando permitido.
- Importar quando aplicável.
- Ações em massa.
- Reset de filtros.
- Saved views.[cite:1]

###### Tipos de coluna suportados

| Tipo | Uso |
|---|---|
| Texto | Nome, título, descrição curta. [cite:1] |
| Identificador | Código, UUID parcial, protocolo. [cite:1] |
| Status | Badge colorido com legenda semântica. [cite:1] |
| Data/hora | Criação, atualização, vencimento. [cite:1] |
| Valor monetário | Faturamento, saldo, custo. [cite:1] |
| Percentual | Conversão, taxa, conclusão. [cite:1] |
| Usuário | Avatar, nome, cargo. [cite:1] |
| Relação | Unidade, turma, contrato, categoria. [cite:1] |
| Booleano | Ativo, verificado, bloqueado. [cite:1] |
| Progresso | Barra linear com label. [cite:1] |
| Tag list | Etiquetas múltiplas. [cite:1] |
| Ações | Ver, editar, duplicar, excluir, mais ações. [cite:1] |

###### Funcionalidades avançadas

- Persistência de preferências de visualização por usuário.
- Seleção por página e seleção global por resultado filtrado.
- Inline row expansion para detalhes rápidos.
- Group by por campos categóricos.
- Colunas calculadas.
- Virtualização para datasets extensos.
- Modo comparação entre linhas.
- Indicadores de alteração recente ou anomalia.
- Linha clicável configurável sem conflitar com botões internos.[cite:1]

###### Estados da tabela

- Sem registros iniciais.
- Sem resultado após filtros.
- Carregando primeira página.
- Carregando nova página.
- Erro na consulta.
- Modo bulk ativo.
- Linhas parcialmente indisponíveis por permissão.[cite:1]

###### Ações de linha obrigatórias

- Visualizar.
- Editar.
- Duplicar.
- Arquivar ou inativar.
- Excluir com confirmação.
- Abrir histórico.
- Abrir auditoria.
- Mais ações contextuais.[cite:1]

###### Saved views do DataTable

Cada tabela importante deve permitir salvar visões com os seguintes campos.[cite:1]

- Nome da view.
- Escopo pessoal ou compartilhado.
- Colunas visíveis.
- Ordenação aplicada.
- Filtros ativos.
- Densidade.
- Agrupamentos.
- Pin de colunas.
- View padrão.[cite:1]

##### Módulo 2 — Widgets

Widgets são blocos compactos para dashboards, home operacionais e resumos de entidades.[cite:1]

###### Tipos obrigatórios de widget

- KPI numérico.
- KPI comparativo com delta.
- Lista curta.
- Timeline.
- Alerta operacional.
- Meta e progresso.
- Ranking.
- Distribuição por categoria.
- Heat summary.
- Próximos vencimentos.
- Pendências por SLA.
- Atividade recente.[cite:1]

###### Estrutura mínima do widget

- Cabeçalho com título, subtítulo e menu.
- Conteúdo principal.
- Rodapé opcional com link, insight ou atualização.
- Estado de loading, erro e vazio.[cite:1]

###### Controles obrigatórios dos widgets

- Seleção de período.
- Refresh manual.
- Expandir para tela completa ou detalhe.
- Menu contextual.
- Drill-down quando houver granularidade.
- Indicador de última atualização.
- Compartilhar ou copiar link quando aplicável.[cite:1]

###### Widgets recomendados para dashboard principal

| Widget | Conteúdo | Ações |
|---|---|---|
| Receita/volume | Valor atual, delta, tendência. [cite:1] | Ver relatório, alterar período. [cite:1] |
| Pendências | Total aberto por prioridade. [cite:1] | Abrir fila filtrada. [cite:1] |
| SLA | Dentro e fora do prazo. [cite:1] | Ver detalhes. [cite:1] |
| Usuários ativos | Total e crescimento. [cite:1] | Abrir analytics. [cite:1] |
| Erros recentes | Incidentes e severidade. [cite:1] | Ver log ou auditoria. [cite:1] |
| Automações | Execuções, falhas, taxa de sucesso. [cite:1] | Abrir automações. [cite:1] |

##### Módulo 3 — Charts

Os charts devem ser integrados ao design system, legíveis em dashboards densos e com boa experiência de drill-down.[cite:1]

###### Tipos obrigatórios

- Line chart.
- Bar chart.
- Stacked bar.
- Area chart.
- Donut chart.
- Pie apenas quando estritamente necessário.
- Horizontal bar.
- Heatmap.
- Funnel.
- Scatter.
- Mixed chart.
- Sparkline.[cite:1]

###### Controles obrigatórios para charts

- Alterar período.
- Alterar granularidade, por dia, semana, mês, trimestre.
- Seleção de série.
- Mostrar ou ocultar legenda.
- Tooltip detalhado.
- Exportar imagem ou dados.
- Drill-down por ponto ou segmento.
- Reset de zoom.
- Comparar com período anterior.
- Meta/linha de referência.
- Toggle absoluto versus percentual.[cite:1]

###### Regras de UX

- Não depender só de cor para diferenciar séries.
- Sempre exibir unidade de medida.
- Evitar pizza com muitas categorias.
- Em telas pequenas, priorizar sparklines, barras horizontais e resumos textuais.
- Todo gráfico deve ter fallback textual dos principais insights.[cite:1]

###### Cards analíticos compostos

A biblioteca deve oferecer cards híbridos combinando KPI, chart e tabela resumida.[cite:1]

Exemplos.

- Receita mensal com delta, sparkline e top 3 origens.
- Tickets por status com donut e SLA médio.
- Ocupação por unidade com heatmap e ranking lateral.[cite:1]

##### Módulo 4 — CRUD Drawers

CRUD drawers são painéis laterais para criação, edição, visualização rápida e ações transacionais sem navegação disruptiva.[cite:1]

###### Tipos de drawer

- Create drawer.
- Edit drawer.
- View drawer.
- Clone drawer.
- Approval drawer.
- Side detail drawer.[cite:1]

###### Estrutura padrão do drawer

1. Header com título, entidade, status e ações rápidas.
2. Corpo com formulário ou resumo estruturado.
3. Footer fixo com ações primárias e secundárias.
4. Área opcional de auditoria resumida.
5. Banner contextual para erros, alertas ou dependências.[cite:1]

###### Controles obrigatórios

- Fechar.
- Salvar.
- Salvar e continuar.
- Salvar e novo.
- Cancelar.
- Confirmar saída com alterações não salvas.
- Próximo e anterior quando houver navegação entre registros.
- Duplicar.
- Excluir ou arquivar quando permitido.[cite:1]

###### Recursos obrigatórios de formulário

- Validação inline.
- Máscaras configuráveis.
- Ajuda contextual.
- Campos condicionais.
- Seções expansíveis.
- Stepper interno para formulários longos.
- Autosave opcional.
- Uploads.
- Relacionamentos pesquisáveis.
- Tags.
- Checklists.
- Notas internas.
- Histórico resumido.[cite:1]

###### Estados obrigatórios

- Novo registro.
- Edição.
- Somente leitura.
- Aprovando.
- Rejeitando.
- Bloqueado por conflito de edição.
- Carregando dados de apoio.
- Erro de validação de servidor.[cite:1]

###### Seções padrão recomendadas em drawers complexos

| Seção | Conteúdo |
|---|---|
| Dados principais | Nome, código, descrição, status. [cite:1] |
| Classificação | Categoria, tipo, tags, origem. [cite:1] |
| Relacionamentos | Unidade, responsável, cliente, grupo. [cite:1] |
| Regras | Limites, flags, parâmetros. [cite:1] |
| Arquivos | Anexos e evidências. [cite:1] |
| Auditoria | Criado por, atualizado por, timeline curta. [cite:1] |

##### Módulo 5 — Kanban

O Kanban deve atender fluxos operacionais com grande volume, múltiplas colunas e regras de transição.[cite:1]

###### Estrutura do board

- Header do board.
- Filtros e visão.
- Colunas configuráveis.
- Cards arrastáveis.
- Rodapé por coluna com contagem e ações.
- Painel lateral de detalhes opcional.[cite:1]

###### Controles obrigatórios

- Busca.
- Filtro por responsável.
- Filtro por status, prioridade, unidade, data e tags.
- Agrupar por pipeline, time ou categoria.
- Expandir ou colapsar colunas.
- Limite visual de WIP.
- Drag and drop com regras de negócio.
- Quick add card.
- Quick edit card.
- Abrir drawer detalhado.
- Ordenação interna da coluna.
- Modo fullscreen.[cite:1]

###### Conteúdo mínimo do card Kanban

- Título.
- ID ou protocolo.
- Status ou etapa.
- Responsável.
- Prazo ou idade.
- Prioridade.
- Tags.
- Indicador de bloqueio.
- Indicador de comentários ou anexos.[cite:1]

###### Regras obrigatórias do Kanban

- Validação antes da mudança de etapa.
- Confirmação para etapas críticas.
- Bloqueio de drop por permissão ou pré-condição.
- Registro de auditoria no drag and drop.
- Atualização otimista com rollback em caso de erro.
- Visualização mobile alternativa, como lista por etapa.[cite:1]

##### Módulo 6 — Automações

A área de automações deve permitir criação, monitoramento, versionamento e governança de regras operacionais.[cite:1]

###### Páginas obrigatórias de automação

1. Lista de automações.
2. Builder de automação.
3. Histórico de execuções.
4. Catálogo de gatilhos e ações.
5. Logs e falhas.
6. Configurações globais.[cite:1]

###### Componentes obrigatórios do builder

- Nome da automação.
- Descrição.
- Status ativo/inativo.
- Escopo da automação.
- Trigger selector.
- Condições.
- Operadores lógicos.
- Ações encadeadas.
- Delay ou agendamento.
- Simulação/teste.
- Versionamento.
- Publicar/rascunho.
- Guardrails e limites.[cite:1]

###### Tipos de gatilho

- Criação de registro.
- Atualização de campo.
- Mudança de status.
- Data programada.
- Webhook recebido.
- Evento manual.
- Inatividade.
- Meta atingida ou violada.[cite:1]

###### Tipos de ação

- Atualizar campo.
- Enviar e-mail.
- Enviar notificação in-app.
- Criar tarefa.
- Atribuir responsável.
- Mover etapa.
- Gerar documento.
- Chamar webhook.
- Abrir aprovação.
- Inserir comentário interno.[cite:1]

###### Controles obrigatórios de governança

- Duplicar automação.
- Versionar.
- Ativar/desativar.
- Testar com payload exemplo.
- Ver impacto estimado.
- Ver histórico.
- Reprocessar falhas.
- Limites de execução.
- Escopo por tenant, unidade ou entidade.[cite:1]

###### Tabela de execuções

A tabela de execuções deve conter no mínimo: ID, automação, trigger, entidade, horário, duração, resultado, tentativas, originador e ação de detalhes.[cite:1]

##### Módulo 7 — Controles

Controles representam interfaces de comando, filtragem, interação e configuração fina.[cite:1]

###### Grupos de controles obrigatórios

- Inputs de texto.
- Inputs numéricos.
- Date e time controls.
- Range controls.
- Select simples.
- Select remoto.
- MultiSelect.
- TreeSelect.
- Checkbox e radio groups.
- Switches.
- Segment controls.
- Botões com split action.
- Toggle groups.
- Chips e tags.
- Upload controls.
- Rich text básico.
- Color/status selector quando permitido pelo domínio.[cite:1]

###### Requisitos comuns dos controles

- Label.
- Hint.
- Placeholder.
- Estado obrigatório.
- Estado inválido.
- Estado desabilitado.
- Estado leitura.
- Mensagem de erro.
- Suporte a teclado.
- Ajuda contextual.[cite:1]

###### Controles avançados necessários

- Filtro por data relativa, hoje, ontem, últimos 7 dias, mês atual.
- Campo de busca com debounce.
- Select com paginação remota.
- Selector de entidade com avatar e metadados.
- Controle de permissões por checkbox matrix.
- Reorder list.
- Dual list transfer.
- Cron expression helper para automações.[cite:1]

##### Módulo 8 — Gerenciamentos

Gerenciamentos são páginas completas para operação administrativa e estratégica do sistema.[cite:1]

###### Tipos obrigatórios de páginas de gerenciamento

- Gestão de usuários.
- Gestão de perfis e permissões.
- Gestão de unidades/filiais.
- Gestão de entidades de negócio.
- Gestão de categorias e taxonomias.
- Gestão de integrações.
- Gestão de automações.
- Gestão de notificações.
- Gestão de auditoria e logs.
- Gestão de configurações globais.
- Gestão de documentos e anexos.
- Gestão de filas e pendências.[cite:1]

##### Páginas completas obrigatórias

Abaixo estão os blueprints completos mínimos para a biblioteca.

##### Página 1 — Dashboard Executivo

###### Objetivo

Exibir visão consolidada do negócio e permitir navegação rápida para áreas críticas.[cite:1]

###### Blocos obrigatórios

- Header com período, unidade, escopo e ações.
- Linha de KPIs principais.
- Grid de widgets analíticos.
- Chart de tendência principal.
- Ranking ou distribuição.
- Feed de alertas.
- Lista de pendências críticas.
- Atalhos operacionais.[cite:1]

###### Controles obrigatórios

- Período.
- Unidade.
- Segmento.
- Comparar com período anterior.
- Atualizar dados.
- Exportar visão.
- Compartilhar link interno.[cite:1]

###### Estados necessários

- Sem dados do período.
- Carregando dashboard.
- Dados parciais com falha em um widget.
- Acesso limitado por escopo.[cite:1]

##### Página 2 — Listagem Mestre com DataTable

###### Objetivo

Servir como página padrão para qualquer entidade com operação massiva.[cite:1]

###### Estrutura

- Header.
- Toolbar com busca e filtros.
- Quick filters.
- Tabela principal.
- Painel de bulk actions.
- Paginação e resumo.[cite:1]

###### Controles obrigatórios

- Novo registro.
- Exportar.
- Importar.
- Salvar view.
- Editar colunas.
- Reset filtros.
- Seleção em massa.[cite:1]

###### Variações obrigatórias

- Entidade simples.
- Entidade com relações.
- Entidade sensível com colunas mascaradas.
- Entidade arquivável.[cite:1]

##### Página 3 — Detalhe de Entidade

###### Objetivo

Apresentar visão 360 da entidade sem perder contexto operacional.[cite:1]

###### Seções obrigatórias

- Cabeçalho com identidade do registro.
- Resumo geral.
- Dados principais.
- Relacionamentos.
- Timeline.
- Anexos.
- Auditoria.
- Ações rápidas.
- Blocos analíticos ou operacionais relacionados.[cite:1]

###### Controles obrigatórios

- Editar.
- Duplicar.
- Arquivar.
- Excluir.
- Compartilhar referência.
- Abrir histórico.
- Abrir logs relacionados.[cite:1]

##### Página 4 — CRUD com Drawer

###### Objetivo

Permitir manipulação rápida de registros a partir da listagem.[cite:1]

###### Fluxos obrigatórios

- Criar a partir da listagem.
- Editar sem sair da página.
- Visualizar detalhes curtos.
- Salvar e permanecer no contexto.
- Retomar edição interrompida.[cite:1]

###### Controles obrigatórios

- Dirty state guard.
- Validação inline.
- Navegação por seções.
- Upload.
- Relacionamentos remotos.
- Rodapé fixo com CTA principal.[cite:1]

##### Página 5 — Kanban Operacional

###### Objetivo

Gerenciar pipelines operacionais, comerciais ou de atendimento.[cite:1]

###### Blocos obrigatórios

- Header de pipeline.
- Filtros rápidos.
- Métricas do board.
- Colunas com cards.
- Drawer lateral.
- Indicadores de SLA e bloqueios.[cite:1]

###### Controles obrigatórios

- Alterar board.
- Filtrar responsáveis.
- Adicionar card.
- Arrastar e soltar.
- Ver detalhes.
- Alternar para visão lista.[cite:1]

##### Página 6 — Gestão de Automações

###### Objetivo

Centralizar desenho, governança e observabilidade das automações.[cite:1]

###### Blocos obrigatórios

- Listagem de automações.
- Filtros por status, trigger e escopo.
- Cards de saúde das execuções.
- Histórico recente.
- CTA para nova automação.[cite:1]

###### Controles obrigatórios

- Nova automação.
- Duplicar.
- Ativar/desativar.
- Testar.
- Publicar.
- Ver logs.
- Reprocessar falhas.[cite:1]

##### Página 7 — Builder de Automação

###### Objetivo

Permitir criação visual e governada de regras.[cite:1]

###### Seções obrigatórias

- Metadados da automação.
- Trigger.
- Condições.
- Fluxo de ações.
- Testes.
- Versionamento.
- Publicação.[cite:1]

###### Controles obrigatórios

- Adicionar condição.
- Agrupar lógica.
- Adicionar ação.
- Reordenar ações.
- Testar payload.
- Validar dependências.
- Salvar rascunho.
- Publicar versão.[cite:1]

##### Página 8 — Gestão de Usuários

###### Objetivo

Administrar usuários, convites, status e vínculos com segurança.[cite:1]

###### Seções obrigatórias

- DataTable de usuários.
- Filtros por status, role, unidade e origem.
- Drawer de criação/edição.
- Bloco de convites pendentes.
- Bloco de atividade recente.
- Ações em lote.[cite:1]

###### Controles obrigatórios

- Convidar usuário.
- Ativar/desativar.
- Resetar acesso.
- Reenviar convite.
- Vincular unidade.
- Alterar perfil.
- Exportar.[cite:1]

##### Página 9 — Perfis e Permissões

###### Objetivo

Gerenciar RBAC e escopos operacionais.[cite:1]

###### Blocos obrigatórios

- Lista de perfis.
- Drawer de perfil.
- Matriz de permissões.
- Escopos por tenant, unidade e recurso.
- Resumo de impacto do perfil.[cite:1]

###### Controles obrigatórios

- Criar perfil.
- Clonar perfil.
- Editar permissões.
- Comparar perfis.
- Publicar alteração.
- Ver usuários impactados.[cite:1]

##### Página 10 — Auditoria e Logs

###### Objetivo

Expor rastreabilidade operacional e de segurança.[cite:1]

###### Blocos obrigatórios

- DataTable de eventos.
- Filtros por ator, ação, recurso, data e severidade.
- Timeline lateral.
- JSON viewer ou payload viewer.
- Exportação permitida por perfil.[cite:1]

###### Controles obrigatórios

- Buscar por ID.
- Filtrar intervalo.
- Ver diff.
- Ver contexto.
- Copiar referência.
- Exportar resultados.[cite:1]

##### Página 11 — Configurações Gerais

###### Objetivo

Concentrar parâmetros sistêmicos com segurança e clareza.[cite:1]

###### Seções obrigatórias

- Geral.
- Branding.
- Notificações.
- Integrações.
- Segurança.
- Privacidade.
- Parametrizações avançadas.[cite:1]

###### Controles obrigatórios

- Navegação por tabs ou sidebar interna.
- Modo edição seguro.
- Controle de dirty state.
- Histórico resumido.
- Validação por seção.
- Salvar por bloco ou página.[cite:1]

##### Página 12 — Central de Notificações e Pendências

###### Objetivo

Exibir tarefas, alertas, aprovações e itens críticos em uma fila acionável.[cite:1]

###### Blocos obrigatórios

- Cards de resumo.
- Filtros por tipo, prioridade, origem e vencimento.
- Lista ou tabela de pendências.
- Ações rápidas.
- Timeline resumida.[cite:1]

###### Controles obrigatórios

- Marcar como lido.
- Resolver.
- Delegar.
- Abrir detalhe.
- Filtrar minhas pendências.
- Ordenar por urgência.[cite:1]

##### Página 13 — Gestão de Integrações

###### Objetivo

Administrar conectores, credenciais, eventos e status de sincronização.[cite:1]

###### Seções obrigatórias

- Lista de integrações.
- Status cards.
- Histórico de sync.
- Logs de erro.
- Drawer de credenciais/configuração.
- Teste de conexão.[cite:1]

###### Controles obrigatórios

- Conectar.
- Desconectar.
- Testar.
- Reprocessar.
- Ver logs.
- Renovar credencial.[cite:1]

##### Página 14 — Gestão de Documentos e Anexos

###### Objetivo

Gerenciar arquivos vinculados a entidades com rastreabilidade.[cite:1]

###### Blocos obrigatórios

- Lista ou grid de arquivos.
- Preview.
- Filtros por tipo, entidade, data, autor.
- Upload drawer.
- Histórico de versões.[cite:1]

###### Controles obrigatórios

- Upload múltiplo.
- Substituir versão.
- Baixar.
- Compartilhar referência.
- Vincular entidade.
- Excluir com confirmação.[cite:1]

##### Padrões transversais por página

###### Header padrão

Todo header de página deve conter os itens abaixo quando aplicável.[cite:1]

- Breadcrumb.
- Título.
- Descrição curta.
- Badge de status.
- Última atualização.
- Ações primárias.
- Menu de overflow.[cite:1]

###### Barra de filtros padrão

- Busca global.
- Filtros principais.
- Chips ativos.
- Contador de filtros.
- Limpar filtros.
- Salvar view.[cite:1]

###### Bulk actions padrão

- Selecionados.
- Limpar seleção.
- Exportar.
- Alterar status.
- Atribuir.
- Arquivar.
- Excluir quando permitido.[cite:1]

###### Timeline padrão

A timeline deve suportar eventos de negócio, sistema e auditoria, com tipo, ator, timestamp, resumo, detalhe expandível e ação de cópia de referência.[cite:1]

##### Contratos de integração recomendados

A biblioteca deve padronizar interfaces de integração para facilitar o consumo por frontends diferentes.[cite:1]

###### Contrato mínimo de listagem

```ts
interface ListResponse<T> {
  data: T[];
  total: number;
  page: number;
  perPage: number;
  filters?: Record<string, unknown>;
  sort?: { field: string; direction: 'asc' | 'desc' }[];
  meta?: Record<string, unknown>;
}
```

###### Contrato mínimo de opção remota

```ts
interface RemoteOption {
  id: string | number;
  label: string;
  description?: string;
  avatar?: string;
  meta?: Record<string, unknown>;
  disabled?: boolean;
}
```

###### Contrato de evento de auditoria

```ts
interface AuditEvent {
  id: string;
  actor: string;
  action: string;
  resource: string;
  resourceId: string;
  timestamp: string;
  summary: string;
  details?: unknown;
  severity?: 'info' | 'warning' | 'critical';
}
```

##### Permissões e escopos

Todo blueprint deve permitir composição com camadas de autorização.[cite:1]

###### Tipos mínimos de escopo

- Tenant.
- Unidade.
- Papel.
- Recurso.
- Ação.
- Campo sensível.
- Operação em lote.[cite:1]

###### Comportamentos obrigatórios por permissão

- Esconder ação quando necessário.
- Desabilitar ação quando a existência da feature puder ser conhecida.
- Exibir motivo do bloqueio em tooltip ou helper text.
- Mascarar dados sensíveis parcialmente.
- Exigir dupla confirmação para ações críticas.[cite:1]

##### Acessibilidade

A biblioteca deve nascer acessível por padrão.[cite:1]

###### Requisitos mínimos

- Navegação por teclado.
- Focus visible consistente.
- Labels e descrições para inputs.
- ARIA para componentes compostos quando necessário.
- Contraste adequado.
- Mensagens de erro associadas ao campo.
- Toasts não exclusivos para feedback crítico.
- Drag and drop com alternativa por teclado quando aplicável.[cite:1]

##### Responsividade

Em mobile, a biblioteca deve preservar operação essencial sem tentar replicar toda a densidade desktop.[cite:1]

###### Estratégias mínimas

- Tabelas com horizontal scroll ou modo cards.
- Drawers full-screen em telas pequenas.
- Widgets empilhados em uma coluna.
- Kanban alternando para listas por etapa.
- Toolbars quebradas em menus contextuais.[cite:1]

##### Performance

###### Requisitos mínimos

- Virtualização para tabelas extensas.
- Lazy loading em widgets pesados.
- Debounce em buscas remotas.
- Memoização para colunas e filtros complexos.
- Atualização parcial de widgets e charts.
- Skeletons ao invés de reflow bruto.[cite:1]

##### Convenção de diretórios sugerida

```txt
/ui-library
  /foundations
  /atoms
  /molecules
  /organisms
  /templates
  /pages
  /domain-packs
  /hooks
  /adapters
  /types
  /tokens
  /docs
```

##### Checklist de aceite por página

| Item | Obrigatório |
|---|---|
| Header completo | Sim [cite:1] |
| Estados de loading/empty/error | Sim [cite:1] |
| Controle de permissão | Sim [cite:1] |
| Telemetria | Sim [cite:1] |
| Responsividade | Sim [cite:1] |
| Acessibilidade | Sim [cite:1] |
| Feedback transacional | Sim [cite:1] |
| Auditoria em ações críticas | Sim [cite:1] |
| Documentação de props e eventos | Sim [cite:1] |

##### Entregáveis esperados da biblioteca

- Catálogo visual dos componentes.
- Guia de uso por contexto.
- Specs funcionais por página.
- Contratos de integração.
- Mapa de permissões.
- Guidelines de acessibilidade.
- Guidelines de telemetria.
- Exemplos de composição por domínio.[cite:1]

##### Roadmap sugerido de implementação

###### Fase 1

- Foundations.
- Controles base.
- DataTable.
- Drawers CRUD.
- Widgets KPI.
- Charts principais.[cite:1]

###### Fase 2

- Kanban.
- Automações.
- Permissões.
- Auditoria.
- Integrações.[cite:1]

###### Fase 3

- Domain packs.
- Saved views avançadas.
- Personalização por perfil.
- Templates analíticos avançados.[cite:1]

##### Critério final de qualidade

A biblioteca só deve ser considerada pronta quando uma equipe conseguir montar qualquer tela administrativa relevante combinando templates, organismos e contratos padrão, sem redesenhar controles básicos e sem criar divergência estrutural entre módulos.[cite:1]

### Fonte: spec_gestao_biblioteca_academica.md

#### SPEC — Módulo Biblioteca Acadêmica (Acervo e Empréstimos)
**Projeto:** TotusTuusSoftCloud — SaaS Multi-Entidade · Multi-Unidade · Multi-Usuário
**Módulo:** Academic Library / Circulation Management
**Stack:** PHP 8 puro · MariaDB · Tailwind CSS 4.2 · Supabase · amCharts 5
**Padrão de ID:** `id` (ordenação) · `uuid` (interno) · `code` (externo)
**Status:** Draft — gap identificado (não confundir com `spec_gestao_biblioteca_completo.md`, que é um design system de componentes UI)

- Language Standard: Global English

---

##### 1. Objetivo

Gerenciar o acervo físico e digital das unidades educacionais: catalogação, aquisição, empréstimo, devolução, reserva, multas, inventário e leitura digital, integrado ao módulo Acadêmico (alunos, professores, turmas) e ao módulo Financeiro (multas).

##### 2. Access Levels & Portal Boundaries

Este módulo é consumido por múltiplos portais da plataforma. Cada nível acessa **apenas seu recorte**, nunca a administração completa do acervo.

| Nível | Portal | Acesso neste módulo |
|---|---|---|
| Desenvolvedor (SaaS) | `/dev` | Nenhum acesso a dados de acervo/empréstimo. Apenas métricas agregadas de uso (ex.: nº de bibliotecas ativas por entidade) para suporte/billing da plataforma. |
| Entidade/Unidade (Bibliotecário/Admin) | `/admin/library` | Acesso total: catalogação, empréstimos, multas, inventário, relatórios. Escopo travado à própria entidade/unidade. |
| Site público (venda do SaaS) | — | Nenhum acesso. Não relacionado à venda da plataforma. |
| Professor | `/teacher/library` | Consulta ao catálogo, empréstimo próprio (prazo estendido), reserva de sala. **Não vê** empréstimos de outros usuários nem multas de terceiros. |
| Aluno | `/student/library` | Consulta ao catálogo, empréstimo/reserva/renovação **do próprio usuário**, biblioteca digital, próprias multas. |
| Terceiros | `/partner` | Sem acesso por padrão. Pode ser habilitado pontualmente (ex.: biblioteca comunitária) via permissão explícita da entidade. |
| Pais/Responsáveis (pedagógico) | `/guardian/library` | **Somente leitura**: empréstimos ativos e multas do(s) filho(s) vinculado(s). Não pode consultar catálogo geral fora do contexto do filho nem editar/pagar multa aqui. |
| Responsável Financeiro | `/payer/library` (ou aba financeira dedicada) | **Somente leitura financeira**: valor e status de multas vinculadas ao aluno sob sua responsabilidade de pagamento, com link direto para quitação no módulo Billing. **Não vê** título do livro, categoria ou histórico de leitura — apenas o valor e a referência da multa, para preservar privacidade pedagógica. |

**Regra de segregação:** a API deve expor endpoints diferentes por portal (`/api/v1/library/*` para admin vs. `/api/v1/me/library/*` para aluno/professor vs. `/api/v1/guardian/library/*` vs. `/api/v1/payer/library/fines` — este último retorna apenas `{fine_uuid, amount, status, due_date}`, sem join com `lib_items`).

##### 3. Escopo funcional

- Catalogação de itens (livros, periódicos, mídias, e-books, TCCs).
- Empréstimo e devolução com regras por perfil (aluno, professor, servidor).
- Reserva de itens indisponíveis com fila de espera.
- Renovação automática e manual.
- Multas por atraso e bloqueio de novo empréstimo.
- Inventário de acervo (contagem física, divergências).
- Doações e descarte de itens.
- Empréstimo entre unidades (malote/interbibliotecas).
- Sala de leitura / reserva de espaço físico.
- Biblioteca digital: e-books, PDFs protegidos, streaming de leitura.
- Indicadores de uso do acervo por curso/disciplina.

##### 3. Perfis de acesso

| Perfil | Permissões |
|---|---|
| Bibliotecário | CRUD completo, empréstimos, multas, inventário |
| Auxiliar de Biblioteca | Empréstimo/devolução, sem gestão de acervo |
| Professor | Empréstimo com prazo estendido, reserva de sala |
| Aluno | Consulta, empréstimo próprio, reserva, renovação self-service |
| Coordenador | Relatórios de uso por curso/disciplina |
| Financeiro | Consulta de multas vinculadas ao aluno |

##### 4. Páginas do módulo

```
/library/dashboard
/library/catalog                  — Catálogo de itens (datatable)
/library/catalog/:uuid             — Ficha catalográfica
/library/loans                     — Empréstimos ativos e histórico
/library/reservations              — Reservas e fila de espera
/library/fines                     — Multas
/library/inventory                 — Inventário do acervo
/library/rooms                     — Reserva de salas de leitura/estudo
/library/digital                   — Biblioteca digital (e-books)
/library/reports                   — Relatórios de circulação
/library/settings                  — Regras de empréstimo, categorias, editoras
```

##### 5. Dashboard

###### Widgets
- Total de itens no acervo.
- Empréstimos ativos.
- Empréstimos em atraso.
- Reservas pendentes.
- Multas em aberto (R$).
- Itens mais emprestados (top 5).
- Taxa de devolução no prazo.
- Novos itens catalogados no mês.

###### Charts
- Linha: empréstimos por mês.
- Donut: acervo por categoria (Literatura, Didático, Periódico, Mídia, E-book).
- Barras: circulação por curso/disciplina.
- Heatmap: horários de maior movimento no balcão.

##### 6. Catálogo — Datatable

Colunas: código de tombamento · título · autor · ISBN/ISSN · categoria · editora · exemplares totais · exemplares disponíveis · localização física (estante/prateleira) · status · ações.

###### Drawer — Ficha Catalográfica (CRUD)
Abas:
- **Dados Gerais**: título, subtítulo, autor(es), ISBN/ISSN, editora, edição, ano, idioma, categoria (CDD/CDU opcional), sinopse, capa (upload).
- **Exemplares**: lista de exemplares físicos com código de barras individual, estado de conservação, localização, status (disponível/emprestado/reservado/em manutenção/baixado).
- **Digital**: arquivo e-book/PDF protegido, licença de uso, número de licenças simultâneas, DRM opcional.
- **Aquisição**: fornecedor, nota fiscal, valor de aquisição, data de entrada, forma (compra/doação).
- **Histórico**: timeline de empréstimos do item.

##### 7. Empréstimos

###### Regras de negócio
- Prazo de empréstimo configurável por perfil (ex.: aluno 7 dias, professor 30 dias).
- Limite de itens simultâneos por perfil.
- Bloqueio automático de novo empréstimo se houver multa em aberto ou item atrasado.
- Renovação permitida até N vezes, exceto se houver reserva de outro usuário para o item.
- Devolução gera baixa automática de multa quando dentro do prazo de tolerância.

###### Datatable de Empréstimos
Colunas: código do empréstimo · usuário · item · data empréstimo · data prevista devolução · data devolução real · status (ativo/atrasado/devolvido/perdido) · multa gerada · ações.

###### Drawer — Novo Empréstimo
- Buscar usuário (aluno/professor/servidor) por matrícula/nome.
- Buscar item por código de barras (scanner) ou título.
- Data de devolução calculada automaticamente pela regra do perfil.
- Confirmação de retirada (assinatura digital opcional).

##### 8. Reservas

- Fila de espera por item indisponível.
- Notificação automática quando item é devolvido e liberado para o próximo da fila.
- Prazo de retirada da reserva (ex.: 48h), expirando automaticamente.

##### 9. Multas

###### Regras
- Valor por dia de atraso configurável por categoria de item.
- Teto máximo de multa por item.
- Geração automática de fatura no módulo Financeiro/Billing quando multa é confirmada.
- Isenção de multa mediante justificativa aprovada pelo bibliotecário.

###### Datatable de Multas
Colunas: usuário · item · dias de atraso · valor · status (pendente/pago/isento) · data geração · ações.

##### 10. Inventário do Acervo

- Criação de inventário por estante/setor ou geral.
- Contagem via leitor de código de barras/QR.
- Relatório de divergências (item não encontrado, item fora de lugar).
- Aprovação de baixa por extravio.

##### 11. Salas de Leitura / Estudo

- Cadastro de salas/cabines com capacidade.
- Reserva por aluno/professor com horário e duração máxima.
- Calendário de ocupação (dia/semana).
- Check-in obrigatório para validar reserva.

##### 12. Biblioteca Digital

- Upload de e-books com DRM/watermark dinâmico por usuário.
- Controle de licenças simultâneas (empréstimo digital com expiração automática).
- Leitor embutido (visualização sem download quando exigido por licença).
- Histórico de leitura e progresso.

##### 13. Automações

- Notificar usuário 2 dias antes do vencimento do empréstimo.
- Notificar usuário no dia do vencimento e em D+1, D+3 de atraso.
- Bloquear renovação automática se item tiver reserva pendente.
- Liberar reserva expirada e notificar o próximo da fila.
- Gerar relatório mensal de circulação por curso.
- Sincronizar baixa de multa com módulo Financeiro/Billing.

##### 14. Integrações

- **Acadêmico**: validação de matrícula ativa do aluno antes de permitir empréstimo.
- **RH/Pessoas**: validação de vínculo ativo do professor/servidor.
- **Financeiro/Billing**: geração e baixa de fatura de multa.
- **Notificações**: envio de lembretes por e-mail/push/WhatsApp.
- **Auditoria**: toda ação de empréstimo, devolução, baixa e isenção deve ser auditada.

##### 15. Modelo de dados mínimo

```sql
CREATE TABLE lib_items (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  code VARCHAR(30) NOT NULL UNIQUE,
  entity_id BIGINT UNSIGNED NOT NULL,
  unit_id BIGINT UNSIGNED NOT NULL,
  title VARCHAR(300) NOT NULL,
  authors JSON,
  isbn VARCHAR(20),
  category VARCHAR(80),
  publisher VARCHAR(150),
  edition VARCHAR(50),
  publish_year YEAR,
  language VARCHAR(30),
  synopsis TEXT,
  cover_path VARCHAR(500),
  total_copies INT UNSIGNED DEFAULT 1,
  available_copies INT UNSIGNED DEFAULT 1,
  is_digital TINYINT(1) DEFAULT 0,
  digital_file_path VARCHAR(500),
  digital_license_count INT UNSIGNED,
  status ENUM('active','archived','lost') DEFAULT 'active',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  deleted_at DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lib_copies (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  item_id BIGINT UNSIGNED NOT NULL,
  barcode VARCHAR(50) NOT NULL UNIQUE,
  location VARCHAR(100),
  condition_status ENUM('new','good','damaged','lost') DEFAULT 'good',
  status ENUM('available','loaned','reserved','maintenance','disposed') DEFAULT 'available',
  FOREIGN KEY (item_id) REFERENCES lib_items(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lib_loans (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  code VARCHAR(30) NOT NULL UNIQUE,
  copy_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  user_type ENUM('student','teacher','staff') NOT NULL,
  loaned_at DATETIME NOT NULL,
  due_at DATE NOT NULL,
  returned_at DATETIME NULL,
  renewals_count TINYINT UNSIGNED DEFAULT 0,
  status ENUM('active','overdue','returned','lost') DEFAULT 'active',
  fine_id BIGINT UNSIGNED NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lib_reservations (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  item_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  queue_position SMALLINT UNSIGNED,
  status ENUM('waiting','ready','expired','fulfilled','cancelled') DEFAULT 'waiting',
  notified_at DATETIME NULL,
  expires_at DATETIME NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lib_fines (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  loan_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  days_late INT UNSIGNED,
  amount DECIMAL(10,2),
  status ENUM('pending','paid','waived') DEFAULT 'pending',
  billing_invoice_uuid CHAR(36) NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

##### 16. API REST (principais)

- `GET/POST /api/v1/library/items`
- `GET /api/v1/library/items/{uuid}/copies`
- `POST /api/v1/library/loans` · `POST /api/v1/library/loans/{uuid}/return` · `POST /api/v1/library/loans/{uuid}/renew`
- `POST /api/v1/library/reservations` · `POST /api/v1/library/reservations/{uuid}/cancel`
- `GET /api/v1/library/fines` · `POST /api/v1/library/fines/{uuid}/waive`
- `POST /api/v1/library/inventory` · `POST /api/v1/library/inventory/{uuid}/count`
- `GET /api/v1/library/rooms/availability` · `POST /api/v1/library/rooms/bookings`

##### 17. Critérios de aceite

- Empréstimo, devolução e renovação funcionam com regras por perfil.
- Reserva libera automaticamente para o próximo da fila.
- Multa é gerada e sincronizada com o módulo Financeiro/Billing.
- Inventário identifica divergências corretamente.
- Biblioteca digital respeita limite de licenças simultâneas.
- Todas as ações críticas são auditadas.
