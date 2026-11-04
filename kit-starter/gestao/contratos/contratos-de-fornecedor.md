# Contratos de fornecedor

- Portal: Gestão (`gestao.`)
- Área: Contratos
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13); especificação da v1 absorvida integralmente (seção 14)
- Fonte da v2: [33](../../../docs/v2/33-contratos-por-portal.md) (integral); [17](../../../docs/v2/17-regras-modulos.md), seção 7
- Fonte da v1: [spec_gestao_contratos_completo.md](../../../docs/v2/anexo-v1/spec_gestao_contratos_completo.md) (1377 linhas) — absorvida integralmente na seção 14

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. A seção 14 é o texto integral da v1, guardado para que nenhum detalhe se perca; quando ela disser algo diferente das seções 1 a 13, vale a v2. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Ciclo de vida dos contratos com fornecedores: elaboração, alçadas, assinatura, obrigações, vigência, renovação e compliance.

## 3. Telas

- **Contratos** (DataTable por tipo e estado).
- **Contrato — detalhe** (abas: dados, cláusulas, obrigações, aditivos, assinaturas).
- **Vencimentos e renovações** (painel).

## 4. Permissões por portal (extraídas do SDD)

- O SDD não traz tabela por portal para este módulo; vale o escopo da seção 2 e os papéis abaixo.

## 5. Papéis

- `unit.purchasing` e `unit.manager`; `unit.legal` emite parecer e bloqueio legal.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Contratos ([33](../../../docs/v2/33-contratos-por-portal.md)); validação de datas ([17](../../../docs/v2/17-regras-modulos.md), seção 7.4).

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

### 13.1 [33 — Gestão de Contratos, por Portal](../../../docs/v2/33-contratos-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Regras atuais em [17](../../../docs/v2/17-regras-modulos.md), seção 7. Matriz de portais em [31](../../../docs/v2/31-matriz-portais-modulos.md). Assinatura e base legal em [26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 6. Auditoria em [29](../../../docs/v2/29-auditoria.md). Privacidade em [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 3.
> **Status:** aprovada pelo autor em 03/11/2026, com as propostas adotadas. Itens sem valor definido continuam pendentes, criada em 03/11/2026 a partir de [`spec_gestao_contratos_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_contratos_completo.md) (v1, 1.376 linhas). Itens **[Decisão do autor]** dependem de resposta. Itens **(jurídico)** dependem de parecer. Este documento não é parecer contratual.
> **Atualização de 03/11/2026:** a assinatura passa a ser serviço comum, usado também por documentos administrativos e emitidos. Ver [54](../../../docs/v2/54-gestao-de-documentos-tres-contextos.md), seção 5.

---

#### 1. Estado atual na v2

[17](../../../docs/v2/17-regras-modulos.md), seção 7 tem 6 linhas de entidades, regras e estados. A v1 tem 17 seções, 16 páginas, perfis, abas de cadastro e fluxos. **A v2 não está completa.** Faltam:

- DDL (defeito T-02 em [17](../../../docs/v2/17-regras-modulos.md));
- mapa de contratos por tipo e por portal;
- regras por tipo de contrato;
- fluxo de aprovação com alçadas;
- integração com assinatura;
- monitoramento de obrigações e vigência;
- regra de contrato sensível (dado pessoal, saúde, menor).

---

#### 2. Tipos de contrato e a quem pertencem

A v1 lista 13 tipos (seção 2.1). Eles não têm o mesmo dono. Cada um fica em um portal, com parte e papel definidos:

| Tipo | Parte A | Parte B | Dono | Portal de acesso |
|---|---|---|---|---|
| Contrato de cliente (SaaS) | Plataforma | Entidade | Plataforma | Desenvolvedor |
| Contrato de prestação de serviços educacionais (matrícula) | Entidade | Responsável legal e aluno | Entidade | Gestão; assinatura pelo Responsáveis |
| Contrato de trabalho e termos de pessoal | Entidade | Colaborador | Entidade (RH) | Gestão; ciência pelo Professor |
| Contrato de fornecedor e de serviço | Entidade | Fornecedor | Entidade (Compras) | Gestão; ciência pelo Terceiros |
| Contrato de manutenção, locação e parceria | Entidade | Fornecedor ou parceiro | Entidade | Gestão; ciência pelo Terceiros |
| Convênio e contrato institucional | Entidade | Órgão ou instituição | Entidade (Jurídico) | Gestão |
| Acordo de confidencialidade (NDA) | Plataforma ou entidade | Parte externa | Quem assina | Desenvolvedor ou Gestão |
| Acordo de processamento de dados (DPA) | Entidade ou plataforma | Operador | Jurídico | Gestão ou Desenvolvedor; ciência pelo Terceiros |
| Termo aditivo, distrato, renovação | Mesmas partes do contrato original | — | Dono do contrato original | Mesmo portal do original |
| Contrato guarda-chuva (master agreement) | Entidade | Fornecedor | Entidade (Compras) | Gestão |

**Regra:** o portal de origem é o do contrato original. Aditivo e distrato não mudam de portal.

**Pendência:** o contrato de matrícula (aluno ou responsável) e o contrato de cliente são contratos de consumo ou de prestação civil. A forma e as cláusulas dependem de **(jurídico)** ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 4). Não defino cláusula aqui.

---

#### 3. Ciclo de vida

Etapas da v1 (seção 2.2), com donos:

| Etapa | Dono | Saída |
|---|---|---|
| Solicitação | Quem precisa do contrato | Solicitação contratual |
| Triagem | Gestor de contratos | Aceita, devolvida ou recusada |
| Minuta | Gestor de contratos, com modelo | Minuta versionada |
| Revisão interna | Jurídico | Parecer |
| Negociação externa | Gestor de contratos | Versão negociada |
| Aprovação jurídica | Jurídico | Aprovado ou devolvido |
| Aprovação financeira | Financeiro | Aprovado ou devolvido, conforme faixa |
| Aprovação gestora | Gestor | Aprovado |
| Assinatura | Responsável pelo contrato | Assinado |
| Vigência | Sistema | Alerta de vencimento |
| Monitoramento de obrigações | Responsável pela obrigação | Entregas e SLA |
| Reajuste e renovação | Gestor de contratos, com financeiro | Aditivo |
| Encerramento e arquivamento | Gestor de contratos | Estado final |

**Estados do contrato** (já em [17](../../../docs/v2/17-regras-modulos.md), seção 7.3): `negociacao`, `aprovacao`, `assinado`, `vigente`, `em_renovacao`, `encerrado`, `cancelado`.

**Regras de transição:**

- Contrato `assinado` não é editado. Mudança vira aditivo ([17](../../../docs/v2/17-regras-modulos.md)).
- Ausência de cláusula obrigatória bloqueia envio para assinatura ([17](../../../docs/v2/17-regras-modulos.md), seção 7.2).
- Aprovação jurídica é obrigatória por tipo ([17](../../../docs/v2/17-regras-modulos.md)).
- Quem cria a minuta não aprova a própria minuta (segregação, [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5).

---

#### 4. Alçadas

| Faixa | Aprovação | Valor |
|---|---|---|
| Abaixo da faixa 1 | Gestor da unidade | **Decidido** em 03/11/2026: até R$ 10.000 |
| Faixa 2 | Gestor + financeiro | **Decidido** em 03/11/2026: de R$ 10.000 a R$ 100.000 |
| Acima da faixa 2 | Gestor executivo + financeiro + jurídico | **Decidido** em 03/11/2026: acima de R$ 100.000 |

As faixas acima resolvem a lacuna LAC-01 de [17](../../../docs/v2/17-regras-modulos.md).

---

#### 5. Assinatura

Estados (v1, seção 13.4): não iniciado, preparando envio, enviado, visualizado, parcialmente assinado, assinado, rejeitado, expirado, cancelado.

Regras:

- Assinatura eletrônica com validade jurídica depende do tipo de documento e do nível exigido **(jurídico)** ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 6, e Lei 14.063/2020).
- Assinatura de responsável em contrato de aluno: verificação de identidade do signatário antes do envio ([06](../../../docs/v2/06-identidade-acesso.md)).
- Envelope tem validade. Expirado não é reaberto; novo envelope é criado.
- Assinatura de terceiro: o portal de terceiros mostra só o próprio contrato.
- Documento assinado é guardado com hash e trilha ([21](../../../docs/v2/21-busca-e-armazenamento.md)).

---

#### 6. Obrigações, vigência e renovação

- Obrigação tem responsável, prazo, evidência e SLA. Vencida sem evidência gera alerta.
- Alerta de vencimento: antecedência configurável por tipo de contrato. Antecedência padrão decidida em 03/11/2026: 60 e 30 dias.
- Renovação automática só se o tipo permitir. Renovação sem aprovação não entra em vigor.
- Reajuste aplica índice definido no contrato. Reajuste sem índice exige aditivo.

---

#### 7. Compliance do contrato

A aba de compliance (v1, seção 8.8) guarda: tratamento de dado pessoal, base legal vinculada, DPA anexado, NDA assinado, política de retenção, criticidade do risco, due diligence concluída, documentos regulatórios e data da última revisão.

**Regra:** contrato com tratamento de dado pessoal não é assinado sem DPA anexado. Essa regra é do sistema, não só do processo ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md)).

**Contrato com dado de menor:** exige revisão de privacidade antes da assinatura ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 3.2).

---

#### 8. Perfis

A v1 define nove perfis (seção 4.1): SA, GE, GC, JU, FI, CO, OP, AU e VI. Eles valem **dentro do portal de gestão**. Para os outros portais valem os papéis de [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5.

| Perfil v1 | Papel na v2 | Portal |
|---|---|---|
| SA — Super Admin | Administrador da entidade | Gestão |
| GE — Gestor Executivo | Gestor executivo | Gestão |
| GC — Gestor de Contratos | Gestor de contratos | Gestão |
| JU — Jurídico | Jurídico | Gestão |
| FI — Financeiro | Financeiro | Gestão |
| CO — Compras | Compras | Gestão |
| OP — Operacional | Operacional, somente execução | Gestão |
| AU — Auditor | Auditor | Gestão, somente leitura ([29](../../../docs/v2/29-auditoria.md), seção 5) |
| VI — Visualizador | Consulta restrita conforme escopo | Gestão |

Contratos de cliente (SaaS) são geridos no portal do desenvolvedor pelo papel de comercial e jurídico da plataforma ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 4.1).

---

#### 9. Páginas e portal

A v1 tem 16 páginas (seção 5). Por portal:

| Página v1 | Portal |
|---|---|
| Dashboard de contratos | Gestão |
| Contratos | Gestão |
| Solicitações contratuais | Gestão |
| Minutas e modelos | Gestão (jurídico) |
| Aprovações | Gestão |
| Assinaturas | Gestão |
| Vigência e renovações | Gestão |
| Obrigações e SLAs | Gestão |
| Aditivos e reajustes | Gestão |
| Partes e contrapartes | Gestão |
| Documentos e anexos | Gestão |
| Calendário contratual | Gestão |
| Kanban operacional | Gestão |
| Compliance e riscos | Gestão (jurídico) e Desenvolvedor (contratos de cliente) |
| Auditoria | Gestão (AU) |
| Configurações do módulo | Gestão (SA) |

Portal do desenvolvedor: contratos de cliente, com as mesmas páginas de vigência, aprovação e assinatura.

Portal de terceiros: **somente** os contratos do próprio fornecedor, com estado e vigência. Sem aprovação interna, sem minuta, sem compliance.

Portal de responsáveis: contrato de matrícula do próprio aluno, para assinatura e consulta.

Portal do professor: contrato de trabalho próprio, para ciência. Sem outros contratos.

---

#### 10. Pendências

| # | Pendência | Tipo |
|---|---|---|
| CTR-01 | DDL de contrato, parte, obrigação, aditivo, solicitação, assinatura (T-02) | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 3. Revisão do owner pendente (DDL-01) |
| CTR-02 | Faixas de alçada (seção 4) | **Decidido** em 03/11/2026: até R$ 10.000, de R$ 10.000 a R$ 100.000, e acima, com jurídico |
| CTR-03 | Antecedência padrão de alerta (seção 6) | **Decidido** em 03/11/2026: 60 e 30 dias antes do vencimento |
| CTR-04 | Forma de assinatura por tipo de contrato | (jurídico) |
| CTR-05 | Cláusulas obrigatórias por tipo | (jurídico) |
| CTR-06 | Provedor de assinatura eletrônica | **Decidido** em 03/11/2026: aceitar todos os provedores de terceiros e criar assinatura digital própria, certificada e aprovada pelos órgãos competentes. A assinatura própria depende de credenciamento na ICP-Brasil **(verificar, jurídico)** |
| CTR-07 | Contrato de matrícula: forma, cláusulas e prazo de guarda | (jurídico) |

---

#### 11. Critérios de aceite

- [ ] Cada tipo de contrato da seção 2 tem dono e portal de origem.
- [ ] Transições da seção 3 testadas; contrato assinado não é editado.
- [ ] Alçada aplicada pela aplicação, não só pelo processo.
- [ ] Contrato com dado pessoal não é enviado para assinatura sem DPA.
- [ ] Portal de terceiros e de responsáveis mostram só o próprio contrato.
- [ ] DDL escrito para todas as entidades (CTR-01).
- [ ] Itens **[Decisão do autor]** e **(jurídico)** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).

#### 12. Decisões de 03/11/2026

**CTR-02 (faixas de alçada): aprovado como padrão inicial, ajustável por entidade.**

| Faixa | Valor do contrato | Aprovação |
|---|---|---|
| 1 | Até R$ 10.000,00 | Gestor da unidade |
| 2 | Acima de R$ 10.000,00 até R$ 100.000,00 | Gestor executivo e financeiro |
| 3 | Acima de R$ 100.000,00 | Gestor executivo, financeiro e jurídico |

Prazo total ou valor mensal, o que for maior, define a faixa. Contrato que muda de faixa por aditivo é reaprovado na faixa nova.

**CTR-03 (antecedência de alerta de vencimento): aprovado.** Alerta aos 60 dias e novo alerta aos 30 dias antes do vencimento, para contratos de vigência determinada.

### 13.2 [17](../../../docs/v2/17-regras-modulos.md), seção 7

#### 7. Contratos

##### 7.1 Entidades

Contrato, parte, valor, vigência, cláusula, obrigação, aprovação, assinatura, aditivo, solicitação contratual (sem DDL na v1, ver T-02).

##### 7.2 Regras de negócio (v1, seções 8, 10 e 12)

| Regra | Descrição |
|---|---|
| Edição após assinatura | Bloqueada, exceto por aditivo. |
| Alteração estrutural após assinatura | Gera aditivo. |
| Parte | CPF ou CNPJ válido; duplicidade por documento bloqueada. |
| Contratação | Bloqueada com documentação vencida. |
| Anexo obrigatório | Avanço de etapa bloqueado sem o documento obrigatório. |
| Parecer | Jurídico obrigatório por tipo de contrato. Financeiro obrigatório acima de faixa **[Pendente: faixa]**. |
| Cláusula obrigatória | Lista por tipo de contrato; ausência bloqueia envio para assinatura. |

##### 7.3 Estados

| Entidade | Estados |
|---|---|
| Contrato | `negociacao`, `aprovacao`, `assinado`, `vigente`, `em_renovacao`, `encerrado`, `cancelado` |
| Aditivo | `rascunho`, `aprovado`, `assinado` |
| Solicitação contratual | `aberta`, `em_validacao`, `bloqueada`, `concluida` |

##### 7.4 Validação de datas

- Vigência: data fim posterior à data início.
- Renovação automática: aviso antes do vencimento, com prazo em dias configurável. Padrão de 60 dias, decidido pelo autor em 03/11/2026.

## 14. Conteúdo integral da v1 (absorvido)

### SPEC — Módulo Contratos

Versão: 1.0  
Status: Draft funcional completo  
Módulo: Contracts / Contract Lifecycle Management (CLM)  
Contexto: SaaS multi-entidade, multi-unidade e multi-usuário, com banco segregado por entidade/unidade, padrão id + uuid + code, stack PHP 8 puro + MariaDB + JavaScript + Tailwind CSS 4.2 + Supabase + amCharts 5 [cite:1][cite:2].  

- Language Standard: Global English
Naming técnico: inglês, snake_case, rotas RESTful, payloads JSON [cite:2].

---

#### 1. Objetivo do módulo

O módulo **Contratos** deve centralizar todo o ciclo de vida contratual, desde solicitação, minuta, negociação, aprovação, assinatura, vigência, aditivos, reajustes, renovações, obrigações, SLAs, alertas, encerramento e arquivamento, com rastreabilidade completa [web:16].  
O sistema deve oferecer visibilidade operacional por meio de dashboard, datatables, charts, kanban, drawers CRUD, automações, controles e mecanismos de compliance/auditoria [web:15][web:16].  
O módulo deve suportar contratos de cliente, fornecedor, parceiro, locação, serviço, manutenção, educacional, saúde, tecnologia, convênio e instrumentos internos [web:16].

---

#### 2. Escopo funcional

##### 2.1 Tipos de contrato
- Contrato de cliente.
- Contrato de fornecedor.
- Contrato de prestação de serviços.
- Contrato de manutenção.
- Contrato de locação.
- Contrato de parceria.
- Contrato institucional.
- Convênio.
- Acordo de confidencialidade (NDA).
- Termo aditivo.
- Distrato.
- Termo de renovação.
- Contrato guarda-chuva / master agreement [web:16].

##### 2.2 Etapas do ciclo de vida
- Solicitação.
- Triagem.
- Elaboração da minuta.
- Revisão interna.
- Negociação externa.
- Aprovação jurídica.
- Aprovação financeira.
- Aprovação gestora.
- Assinatura.
- Vigência ativa.
- Monitoramento de obrigações.
- Reajuste.
- Renovação.
- Encerramento.
- Arquivamento [web:16].

##### 2.3 Pilares do módulo
- Repositório central de contratos e anexos [web:16].
- Controle de versões de minuta.
- Workflow configurável de aprovação.
- Dashboard com KPIs contratuais [web:15].
- Alertas de vencimento, renovação e obrigações [web:16].
- Auditoria completa de alterações [web:16].
- Compliance documental e regulatório [web:16].
- Permissões por perfil, unidade e carteira.
- Assinatura eletrônica preparada para integração.
- Automação de tarefas recorrentes.

---

#### 3. Requisitos arquiteturais

- Multi-tenant por entidade/unidade com isolamento lógico por database por tenant [cite:1].
- Todas as tabelas devem seguir o padrão:
  - `id` BIGINT UNSIGNED AUTO_INCREMENT para ordenação.
  - `uuid` CHAR(36) para identificador global.
  - `code` VARCHAR para identificador externo/negócio [cite:2].
- Campos padrão em todas as tabelas de domínio:
  - `entity_id`, `entity_uuid`
  - `unit_id`, `unit_uuid`
  - `is_active`
  - `created_by`, `updated_by`
  - `created_at`, `updated_at`
  - `deleted_at` (soft delete quando aplicável) [cite:1][cite:2].
- Todas as páginas devem respeitar RBAC, escopo por unidade, auditoria e logs de eventos sensíveis [web:16].
- Dados críticos como valor contratual, dados pessoais, anexos sensíveis e dados bancários devem respeitar políticas de proteção e mascaramento por perfil [cite:1].

---

#### 4. Personas e perfis

##### 4.1 Perfis padrão
- SA — Super Admin
- GE — Gestor Executivo
- GC — Gestor de Contratos
- JU — Jurídico
- FI — Financeiro
- CO — Compras
- OP — Operacional
- AU — Auditor
- VI — Visualizador

##### 4.2 Capacidades por perfil
- SA: acesso total multi-entidade/unidade.
- GE: visão executiva, aprovações estratégicas, indicadores globais.
- GC: operação completa de contratos.
- JU: minutas, cláusulas, pareceres, revisões, aprovação jurídica.
- FI: impacto financeiro, reajustes, medições, pagamentos vinculados.
- CO: contratos com fornecedores e suprimentos.
- OP: acompanhamento de execução e obrigações.
- AU: leitura ampla e trilhas.
- VI: consulta restrita conforme escopo.

---

#### 5. Mapa de páginas

1. Dashboard de Contratos  
2. Contratos  
3. Solicitações Contratuais  
4. Minutas e Modelos  
5. Aprovações  
6. Assinaturas  
7. Vigência e Renovações  
8. Obrigações e SLAs  
9. Aditivos e Reajustes  
10. Partes e Contrapartes  
11. Documentos e Anexos  
12. Calendário Contratual  
13. Kanban Operacional  
14. Compliance e Riscos  
15. Auditoria  
16. Configurações do Módulo  

---

#### 6. Dashboard de Contratos

##### 6.1 Objetivo
Fornecer visão executiva e operacional do pipeline contratual, contratos ativos, vencimentos, tempo de ciclo, exposição financeira e compliance, com capacidade de drill-down por tipo, unidade, gestor e status [web:15][web:16].

##### 6.2 Filtros globais
- Período.
- Entidade.
- Unidade.
- Tipo de contrato.
- Status.
- Contraparte.
- Responsável interno.
- Centro de custo.
- Faixa de valor.
- Vigência.
- Contrato com risco.
- Contrato com renovação automática.
- Contrato com LGPD/DPA.
- Contrato com assinatura pendente.

##### 6.3 Widgets KPI
- Total de contratos ativos.
- Contratos em elaboração.
- Contratos aguardando aprovação.
- Contratos aguardando assinatura.
- Contratos próximos do vencimento (30/60/90 dias) [web:15][web:16].
- Contratos vencidos ainda não encerrados.
- Tempo médio de ciclo contratual [web:15].
- Taxa de renovação.
- Valor total contratado ativo.
- Valor a vencer no período.
- Contratos com pendência documental.
- Contratos com SLA em risco.
- Contratos com aditivo em aberto.
- Contratos com reajuste pendente.
- Contratos com obrigações críticas em atraso.

##### 6.4 Charts
- Linha: contratos abertos x concluídos por mês [web:15].
- Linha: tempo médio de conclusão por tipo de contrato [web:15].
- Donut: contratos por tipo.
- Donut: contratos por status.
- Barra horizontal: contratos por faixa de vencimento [web:15].
- Barra agrupada: contratos por unidade x status.
- Heatmap: concentração de vencimentos por mês.
- Área: valor contratado por mês.
- Gauge: percentual de compliance documental.
- Treemap: exposição contratual por contraparte.

##### 6.5 Blocos operacionais
- Próximos vencimentos.
- Pendências de assinatura.
- Aprovações aguardando decisão.
- Obrigações próximas.
- Riscos críticos.
- Últimos contratos alterados.
- Atividade recente do módulo.
- Ranking de contrapartes por valor.
- Ranking de gestores por carteira.

##### 6.6 Ações rápidas
- Novo contrato.
- Nova solicitação.
- Novo aditivo.
- Solicitar renovação.
- Registrar assinatura.
- Subir anexo.
- Exportar dashboard.
- Salvar visão personalizada.

---

#### 7. Página Contratos

##### 7.1 Objetivo
Listar, consultar, segmentar, aprovar, acompanhar e operar todos os contratos do tenant.

##### 7.2 Datatable principal
Colunas padrão:
- ID
- Code
- Título do contrato
- Tipo
- Categoria
- Status
- Fase do ciclo
- Contraparte
- Unidade
- Responsável
- Início de vigência
- Fim de vigência
- Dias para vencer
- Valor total
- Reajuste previsto
- Renovação automática
- SLA crítico
- Compliance documental
- Última atualização

##### 7.3 Recursos da datatable
- Busca global.
- Filtros avançados persistidos.
- Ordenação multi-coluna.
- Paginação.
- Colunas configuráveis.
- Fixação de colunas.
- Exportação CSV/Excel/PDF.
- Visualização salva por usuário.
- Bulk actions.
- Chips de filtros ativos.
- Destaque visual por SLA/vencimento.
- Modo compacto / expandido.
- Refresh manual e automático.

##### 7.4 Filtros avançados
- Tipo de contrato.
- Categoria.
- Status.
- Fase.
- Contraparte.
- Responsável.
- Gestor.
- Unidade.
- Período de assinatura.
- Período de vigência.
- Vencendo em X dias.
- Renovação automática.
- Possui aditivo.
- Possui anexo obrigatório pendente.
- Faixa de valor.
- Possui cláusula LGPD.
- Possui garantia.
- Possui multa.
- Risco alto.
- Assinatura pendente.

##### 7.5 Ações por linha
- Visualizar.
- Editar.
- Duplicar.
- Enviar para aprovação.
- Aprovar / rejeitar.
- Solicitar revisão.
- Registrar assinatura.
- Criar aditivo.
- Criar reajuste.
- Criar obrigação.
- Encerrar.
- Arquivar.
- Download do PDF consolidado.
- Ver trilha de auditoria.

##### 7.6 Bulk actions
- Alterar responsável.
- Alterar categoria.
- Alterar status.
- Exportar seleção.
- Anexar documento padrão.
- Gerar lembretes.
- Encaminhar para aprovação.
- Encerrar em lote.
- Arquivar em lote.

---

#### 8. Drawer CRUD de Contrato

##### 8.1 Abas do drawer
- Geral
- Partes
- Valores
- Vigência
- Cláusulas e condições
- Obrigações
- Anexos
- Aprovação
- Assinatura
- Compliance
- Auditoria

##### 8.2 Campos — Aba Geral
- `contract_type_id`
- `category_id`
- `title`
- `short_description`
- `contract_number`
- `internal_reference`
- `status`
- `phase`
- `owner_user_id`
- `manager_user_id`
- `department_id`
- `cost_center_id`
- `business_area_id`
- `tags`
- `priority`

##### 8.3 Campos — Aba Partes
- Parte contratante.
- Contraparte principal.
- CNPJ/CPF.
- Nome jurídico.
- Nome fantasia.
- Contatos.
- Endereço.
- Representante legal.
- Testemunhas.
- Lista de partes adicionais.
- Papel da parte no contrato.

##### 8.4 Campos — Aba Valores
- `currency_code`
- `contract_value`
- `monthly_value`
- `estimated_value`
- `minimum_commitment_value`
- `maximum_commitment_value`
- `payment_terms`
- `billing_frequency`
- `readjustment_type`
- `readjustment_index`
- `readjustment_base_date`
- `penalty_amount`
- `late_fee_rule`
- `guarantee_required`
- `guarantee_type`
- `guarantee_value`

##### 8.5 Campos — Aba Vigência
- `signature_date`
- `effective_date`
- `start_date`
- `end_date`
- `renewal_type`
- `auto_renewal`
- `renewal_notice_days`
- `termination_notice_days`
- `sunset_date`
- `trial_period_days`

##### 8.6 Campos — Aba Cláusulas
- Objeto.
- Escopo.
- Entregáveis.
- SLA.
- Reajuste.
- Rescisão.
- Confidencialidade.
- Proteção de dados.
- Segurança da informação.
- Foro.
- Penalidades.
- Limitação de responsabilidade.
- Subcontratação.
- Anexo de cláusulas personalizadas.

##### 8.7 Campos — Aba Obrigações
- Obrigações da contratante.
- Obrigações da contraparte.
- Obrigações recorrentes.
- SLA de entrega.
- KPI contratual.
- Evidência obrigatória.
- Frequência de validação.
- Responsável pela cobrança.

##### 8.8 Campos — Aba Compliance
- Possui tratamento de dados pessoais.
- Base legal vinculada.
- DPA anexado.
- NDA assinado.
- Política de retenção.
- Criticidade do risco.
- Due diligence concluída.
- Documentos regulatórios exigidos.
- Data da última revisão de compliance.

##### 8.9 Campos — Aba Aprovação
- Fluxo de aprovação.
- Nível atual.
- Aprovadores obrigatórios.
- Aprovadores opcionais.
- Parecer jurídico.
- Parecer financeiro.
- Motivo de urgência.
- Justificativa de exceção.
- Motivo de rejeição.

##### 8.10 Campos — Aba Assinatura
- Tipo de assinatura.
- Plataforma de assinatura.
- Signatários internos.
- Signatários externos.
- Ordem da assinatura.
- Data de envio.
- Data de conclusão.
- Link/token externo.
- Status da assinatura.

##### 8.11 Regras do drawer
- Auto-save configurável.
- Validação por aba.
- Rascunho salvo automaticamente.
- Controle de versão antes da publicação.
- Bloqueio de edição após assinatura, exceto por aditivo.
- Mascaramento de campos financeiros por permissão.
- Histórico de alterações por campo.

---

#### 9. Página de detalhe do contrato

##### 9.1 Seções
- Cabeçalho com status e ações.
- Resumo executivo.
- Timeline do ciclo de vida.
- Painel financeiro.
- Vigência e alertas.
- Partes.
- Obrigações e SLAs.
- Aprovações.
- Assinaturas.
- Anexos.
- Aditivos.
- Reajustes.
- Riscos.
- Auditoria.

##### 9.2 Cards de resumo
- Status.
- Fase.
- Valor.
- Vigência.
- Dias para vencer.
- Gestor.
- Contraparte.
- Compliance score.
- Obrigações em atraso.
- Último aditivo.
- Próximo reajuste.
- Situação da assinatura.

##### 9.3 Timeline
Eventos:
- Solicitação criada.
- Minuta criada.
- Revisão jurídica.
- Rodada de negociação.
- Aprovação concluída.
- Assinatura enviada.
- Assinatura concluída.
- Início de vigência.
- Geração de obrigação.
- Aditivo publicado.
- Reajuste aplicado.
- Encerramento.

---

#### 10. Solicitações Contratuais

##### 10.1 Objetivo
Gerenciar demandas de novos contratos, renovações, rescisões, aditivos ou revisões antes da criação formal do instrumento [web:16].

##### 10.2 Datatable
- Número da solicitação
- Tipo de demanda
- Solicitante
- Área
- Contraparte
- Tipo de contrato
- Prioridade
- Status
- SLA
- Responsável
- Data de abertura
- Data limite
- Origem

##### 10.3 Drawer CRUD
Campos:
- tipo de demanda
- justificativa
- área solicitante
- contrato relacionado
- contraparte
- urgência
- impacto financeiro
- necessidade de assinatura
- documentos iniciais
- observações
- aprovador inicial

##### 10.4 Status
- Aberta
- Em triagem
- Em elaboração
- Em revisão
- Em aprovação
- Convertida em contrato
- Cancelada
- Concluída

---

#### 11. Minutas e Modelos

##### 11.1 Objetivo
Padronizar criação de contratos com templates, biblioteca de cláusulas e versionamento controlado [web:16].

##### 11.2 Recursos
- Cadastro de templates por tipo.
- Biblioteca de cláusulas.
- Variáveis dinâmicas.
- Geração automática de minuta.
- Versionamento.
- Workflow de homologação de template.
- Templates por unidade/segmento.
- Templates ativos/inativos.
- Comparação entre versões.

##### 11.3 Datatable
- Código
- Nome do template
- Tipo
- Versão
- Status
- Unidade aplicável
- Área dona
- Última revisão
- Publicado por

##### 11.4 Drawer CRUD
- nome
- tipo
- categoria
- corpo base
- cláusulas obrigatórias
- cláusulas opcionais
- placeholders
- versão
- status
- aplicabilidade
- observações legais

---

#### 12. Aprovações

##### 12.1 Objetivo
Controlar fluxo multinível de aprovação conforme valor, risco, tipo e exceção [web:16].

##### 12.2 Widgets
- Minhas aprovações pendentes.
- Aprovações vencidas.
- Aprovações concluídas hoje.
- Tempo médio por aprovador.
- Fluxos com gargalo.

##### 12.3 Datatable
- Protocolo
- Contrato
- Tipo
- Etapa
- Aprovador
- Status
- SLA
- Recebido em
- Decisão em
- Tempo consumido
- Motivo da pendência

##### 12.4 Ações
- Aprovar.
- Rejeitar.
- Solicitar ajuste.
- Delegar.
- Reencaminhar.
- Aprovar com ressalva.
- Adicionar comentário.
- Anexar parecer.

##### 12.5 Regras
- Aprovação por alçada de valor.
- Aprovação adicional por risco alto.
- Parecer jurídico obrigatório por tipo.
- Parecer financeiro obrigatório acima de faixa.
- Log completo de decisão.
- Assinatura só após aprovação final.

---

#### 13. Assinaturas

##### 13.1 Objetivo
Acompanhar o envio, pendência, conclusão, rejeição e expiração de assinaturas eletrônicas ou físicas [web:16].

##### 13.2 Datatable
- Contrato
- Documento
- Tipo de assinatura
- Plataforma
- Status
- Signatários pendentes
- Enviado em
- Concluído em
- Expira em

##### 13.3 Drawer
- método de assinatura
- ordem dos signatários
- mensagem de envio
- lembrete automático
- validade do envelope
- autenticação reforçada
- signatários internos
- signatários externos
- observações

##### 13.4 Status
- Não iniciado
- Preparando envio
- Enviado
- Visualizado
- Parcialmente assinado
- Assinado
- Rejeitado
- Expirado
- Cancelado

---

#### 14. Vigência e Renovações

##### 14.1 Objetivo
Monitorar contratos ativos, proximidade do vencimento, renovação, encerramento e janelas críticas [web:16].

##### 14.2 Widgets
- Vencendo em 30 dias.
- Vencendo em 60 dias.
- Vencendo em 90 dias.
- Renovações automáticas.
- Renovações em decisão.
- Encerramentos pendentes.

##### 14.3 Charts
- Contratos por mês de vencimento.
- Vencimentos por unidade.
- Taxa de renovação por tipo.
- Vencimentos por contraparte.

##### 14.4 Controles
- Abertura automática de tarefa de renovação.
- Congelamento de auto-renovação por decisão.
- Checklist pré-renovação.
- Registro de motivo da não renovação.
- Geração de termo de renovação.

---

#### 15. Obrigações e SLAs

##### 15.1 Objetivo
Garantir execução contratual por meio do controle de obrigações, entregas, evidências e níveis de serviço [web:16].

##### 15.2 Datatable
- Contrato
- Obrigação
- Tipo
- Frequência
- Responsável
- Data limite
- Status
- Evidência
- SLA
- Criticidade

##### 15.3 Kanban de Obrigações
Colunas:
- A iniciar
- Em andamento
- Aguardando evidência
- Em validação
- Concluída
- Em atraso
- Bloqueada

##### 15.4 Drawer CRUD
- título da obrigação
- contrato
- tipo
- descrição
- periodicidade
- data de início
- data limite
- tolerância
- responsável
- área
- evidência obrigatória
- indicador de SLA
- penalidade vinculada
- recorrente

##### 15.5 Ações
- concluir obrigação
- anexar evidência
- reprovar evidência
- reabrir
- escalar
- gerar ocorrência
- notificar responsável

---

#### 16. Aditivos e Reajustes

##### 16.1 Datatable
- Contrato base
- Tipo
- Número do aditivo
- Motivo
- Impacto financeiro
- Impacto de prazo
- Status
- Vigência
- Assinatura
- Publicação

##### 16.2 Tipos
- Prorrogação.
- Reajuste.
- Acréscimo.
- Supressão.
- Alteração de cláusula.
- Mudança de escopo.
- Troca de parte.
- Rescisão parcial.

##### 16.3 Controles
- Toda alteração estrutural após assinatura deve gerar aditivo.
- Reajuste com índice e memória de cálculo.
- Histórico consolidado do contrato + aditivos.
- Reflexo automático no valor vigente e datas.

---

#### 17. Partes e Contrapartes

##### 17.1 Objetivo
Manter cadastro centralizado das partes relacionadas aos contratos.

##### 17.2 Datatable
- Código
- Tipo de pessoa
- Nome jurídico
- Documento
- Categoria
- Risco
- Status cadastral
- Cidade
- UF
- Última due diligence

##### 17.3 Drawer
- tipo de pessoa
- razão social / nome
- nome fantasia
- CPF/CNPJ
- inscrição estadual
- contatos
- endereço
- representantes
- dados bancários
- documentos
- classificação de risco
- status de compliance
- observações

##### 17.4 Controles
- validação de duplicidade por documento.
- bloqueio de contratação com documentação vencida.
- checklist de cadastro.
- vínculo com due diligence.

---

#### 18. Documentos e Anexos

##### 18.1 Tipos
- minuta
- contrato assinado
- anexo técnico
- parecer jurídico
- parecer financeiro
- proposta comercial
- certidões
- DPA
- NDA
- apólice/garantia
- evidência operacional
- termo aditivo

##### 18.2 Funcionalidades
- upload múltiplo
- versionamento
- preview
- assinatura hash/checksum
- classificação documental
- OCR preparado
- retenção por política
- download controlado
- trilha de acesso

##### 18.3 Controles
- antivirus scan na fila.
- restrição por MIME/type.
- tamanho máximo configurável.
- marcação de documento obrigatório.
- bloqueio de avanço sem documento obrigatório.

---

#### 19. Kanban Operacional

##### 19.1 Objetivo
Exibir pipeline contratual por fase com operação drag-and-drop controlada.

##### 19.2 Colunas padrão
- Solicitação
- Em triagem
- Minuta
- Revisão interna
- Negociação
- Aprovação
- Assinatura
- Ativo
- Renovação
- Encerramento

##### 19.3 Cartão do kanban
- código
- título
- contraparte
- tipo
- valor
- prazo
- SLA
- responsável
- badges de risco/compliance
- pendências
- avatar do owner

##### 19.4 Regras
- mover coluna exige permissão.
- movimentos críticos exigem comentário.
- bloqueios por ausência documental.
- bloqueios por aprovação não concluída.
- log completo de transição.
- cores por prioridade e risco.

---

#### 20. Calendário Contratual

##### 20.1 Visões
- mensal
- semanal
- agenda
- timeline

##### 20.2 Eventos
- início de vigência
- fim de vigência
- data de reajuste
- renovação
- obrigação
- SLA
- assinatura
- aprovação
- entrega prevista

##### 20.3 Filtros
- tipo de evento
- unidade
- responsável
- contrato
- criticidade

---

#### 21. Compliance e Riscos

##### 21.1 Objetivo
Acompanhar aderência regulatória, risco contratual, proteção de dados, documentos obrigatórios e exceções [web:16].

##### 21.2 Widgets
- contratos sem DPA
- contratos sem NDA
- contratos com exceção jurídica
- contratos com risco alto
- contratos com documentação vencida
- contratos com cláusula crítica ausente

##### 21.3 Matriz de risco
Eixos:
- impacto financeiro
- impacto regulatório
- impacto operacional
- criticidade de dados
- dependência da contraparte

##### 21.4 Controles
- checklist por tipo de contrato
- score de compliance
- bloqueio por ausência documental crítica
- revisão periódica obrigatória
- revalidação por alteração de escopo

---

#### 22. Auditoria

##### 22.1 Eventos auditáveis
- criação
- edição
- exclusão lógica
- mudança de status
- mudança de fase
- aprovação
- rejeição
- assinatura
- download de arquivo sensível
- alteração de valor
- alteração de vigência
- alteração de cláusula crítica
- alteração de responsável
- exportação
- mudança de permissão

##### 22.2 Datatable de auditoria
- data/hora
- usuário
- ação
- entidade
- registro
- campo alterado
- valor anterior
- valor novo
- IP
- user agent
- origem
- hash do evento

---

#### 23. Configurações do módulo

##### 23.1 Cadastros auxiliares
- tipos de contrato
- categorias
- status
- fases
- motivos de aditivo
- índices de reajuste
- templates
- cláusulas padrão
- fluxos de aprovação
- papéis de assinatura
- tipos de obrigação
- SLAs
- motivos de encerramento
- classificação de risco

##### 23.2 Parâmetros
- dias de alerta de vencimento
- dias de antecedência de renovação
- obrigatoriedade de parecer jurídico
- obrigatoriedade de parecer financeiro
- obrigatoriedade de DPA por categoria
- regra de mascaramento financeiro
- política de retenção documental
- auto-numeração por unidade
- aprovação por alçada
- integração com assinatura

---

#### 24. Automações

##### 24.1 Eventos automáticos
- gerar code do contrato.
- criar timeline inicial.
- notificar aprovadores ao entrar em aprovação.
- abrir tarefa de assinatura após aprovação final.
- criar alertas de vencimento 90/60/30 dias [web:16].
- abrir fluxo de renovação automática antes do vencimento [web:16].
- gerar obrigação recorrente conforme periodicidade.
- alertar documentos vencidos.
- recalcular status de compliance.
- recalcular dias para vencimento diariamente.
- gerar task de reajuste na data-base.
- bloquear avanço quando checklist crítico incompleto.
- encerrar automaticamente contratos expirados conforme política.
- consolidar PDF final do contrato + anexos.

##### 24.2 Jobs agendados
- `contracts_due_alert_job`
- `contracts_renewal_window_job`
- `contracts_obligations_recurrence_job`
- `contracts_readjustment_job`
- `contracts_compliance_recheck_job`
- `contracts_sla_breach_job`
- `contracts_archive_policy_job`

---

#### 25. Controles globais de interface

Todas as páginas do módulo devem oferecer:
- busca global;
- filtros persistidos por usuário;
- exportação;
- colunas configuráveis;
- refresh;
- atalhos de ação;
- contador de registros;
- chips de filtros;
- estados vazios;
- loading states;
- empty/error/retry states;
- auditoria visível quando permitido;
- breadcrumb;
- favoritar página;
- salvar visão;
- compartilhar visão interna.

---

#### 26. Gerenciamentos necessários

- Gerenciamento de contratos.
- Gerenciamento de solicitações.
- Gerenciamento de minutas.
- Gerenciamento de cláusulas.
- Gerenciamento de aprovações.
- Gerenciamento de assinaturas.
- Gerenciamento de vigência.
- Gerenciamento de renovações.
- Gerenciamento de reajustes.
- Gerenciamento de obrigações.
- Gerenciamento de SLAs.
- Gerenciamento de partes.
- Gerenciamento de anexos.
- Gerenciamento de compliance.
- Gerenciamento de riscos.
- Gerenciamento de auditoria.
- Gerenciamento de permissões.
- Gerenciamento de configurações.

---

#### 27. Modelo de dados principal

##### 27.1 Tabelas principais
- `ctr_contracts`
- `ctr_contract_types`
- `ctr_contract_categories`
- `ctr_contract_parties`
- `ctr_contract_party_links`
- `ctr_contract_terms`
- `ctr_contract_versions`
- `ctr_contract_templates`
- `ctr_contract_template_versions`
- `ctr_contract_clauses`
- `ctr_contract_approvals`
- `ctr_contract_approval_steps`
- `ctr_contract_signatures`
- `ctr_contract_signatories`
- `ctr_contract_attachments`
- `ctr_contract_obligations`
- `ctr_contract_sla_rules`
- `ctr_contract_amendments`
- `ctr_contract_readjustments`
- `ctr_contract_renewals`
- `ctr_contract_requests`
- `ctr_contract_risks`
- `ctr_contract_compliance_checks`
- `ctr_contract_events`
- `ctr_contract_audit_logs`

##### 27.2 Exemplo — `ctr_contracts`
Campos mínimos:
- `id`
- `uuid`
- `code`
- `entity_id`
- `entity_uuid`
- `unit_id`
- `unit_uuid`
- `contract_type_id`
- `category_id`
- `request_id`
- `owner_user_id`
- `manager_user_id`
- `counterparty_id`
- `title`
- `short_description`
- `contract_number`
- `status`
- `phase`
- `currency_code`
- `contract_value`
- `estimated_value`
- `signature_date`
- `effective_date`
- `start_date`
- `end_date`
- `auto_renewal`
- `renewal_notice_days`
- `termination_notice_days`
- `has_personal_data`
- `has_dpa`
- `risk_level`
- `compliance_score`
- `is_active`
- `created_by`
- `updated_by`
- `created_at`
- `updated_at`
- `deleted_at`

##### 27.3 Exemplo — `ctr_contract_obligations`
- `id`
- `uuid`
- `code`
- `contract_id`
- `title`
- `description`
- `obligation_type`
- `owner_user_id`
- `frequency`
- `start_date`
- `due_date`
- `completed_at`
- `status`
- `sla_status`
- `criticality`
- `evidence_required`
- `penalty_rule`
- `created_at`
- `updated_at`

---

#### 28. Status e transições

##### 28.1 Status macro do contrato
- Draft
- In Review
- Pending Approval
- Approved
- Pending Signature
- Active
- Suspended
- Expired
- Terminated
- Archived

##### 28.2 Regras
- `Draft` → `In Review`
- `In Review` → `Pending Approval`
- `Pending Approval` → `Approved`
- `Approved` → `Pending Signature`
- `Pending Signature` → `Active`
- `Active` → `Expired` ou `Terminated`
- `Expired` → `Archived`
- `Terminated` → `Archived`

##### 28.3 Bloqueios
- Sem documento obrigatório não sai de draft.
- Sem aprovação final não vai para assinatura.
- Sem assinatura concluída não entra em active.
- Alteração estrutural em active exige aditivo.

---

#### 29. Permissões RBAC

##### 29.1 Permissões de módulo
- `contracts.view`
- `contracts.create`
- `contracts.update`
- `contracts.delete`
- `contracts.export`
- `contracts.approve`
- `contracts.sign.manage`
- `contracts.attachments.manage`
- `contracts.templates.manage`
- `contracts.clauses.manage`
- `contracts.obligations.manage`
- `contracts.renewals.manage`
- `contracts.readjustments.manage`
- `contracts.amendments.manage`
- `contracts.compliance.manage`
- `contracts.audit.view`
- `contracts.settings.manage`

##### 29.2 Escopos
- own
- team
- unit
- entity
- all

---

#### 30. Endpoints REST sugeridos

##### 30.1 Contratos
- `GET /api/v1/contracts`
- `POST /api/v1/contracts`
- `GET /api/v1/contracts/{uuid}`
- `PUT /api/v1/contracts/{uuid}`
- `PATCH /api/v1/contracts/{uuid}/status`
- `POST /api/v1/contracts/{uuid}/submit-approval`
- `POST /api/v1/contracts/{uuid}/approve`
- `POST /api/v1/contracts/{uuid}/reject`
- `POST /api/v1/contracts/{uuid}/send-signature`
- `POST /api/v1/contracts/{uuid}/archive`

##### 30.2 Solicitações
- `GET /api/v1/contract-requests`
- `POST /api/v1/contract-requests`
- `PUT /api/v1/contract-requests/{uuid}`
- `POST /api/v1/contract-requests/{uuid}/convert`

##### 30.3 Aditivos
- `GET /api/v1/contract-amendments`
- `POST /api/v1/contract-amendments`
- `GET /api/v1/contract-amendments/{uuid}`
- `PUT /api/v1/contract-amendments/{uuid}`

##### 30.4 Obrigações
- `GET /api/v1/contract-obligations`
- `POST /api/v1/contract-obligations`
- `PATCH /api/v1/contract-obligations/{uuid}/complete`
- `POST /api/v1/contract-obligations/{uuid}/evidence`

##### 30.5 Templates
- `GET /api/v1/contract-templates`
- `POST /api/v1/contract-templates`
- `PUT /api/v1/contract-templates/{uuid}`
- `POST /api/v1/contract-templates/{uuid}/publish`

---

#### 31. Validações críticas

- `end_date` deve ser maior ou igual a `start_date`.
- Contrato com valor acima da alçada exige aprovação financeira.
- Contrato com tratamento de dados pessoais exige validação de compliance.
- Contrato ativo deve possuir documento assinado.
- Aditivo não pode existir sem contrato base.
- Renovação não pode sobrepor vigência de forma inconsistente.
- Contraparte bloqueada não pode ser vinculada.
- Documento obrigatório pendente deve impedir avanço de fase crítica.

---

#### 32. Segurança e compliance

- RBAC por ação e escopo.
- Soft delete controlado.
- Logs imutáveis de auditoria.
- Mascaramento de dados sensíveis.
- Download auditado de anexos.
- Hash/assinatura lógica de arquivos.
- Proteção contra upload malicioso.
- Revisão de cláusulas críticas.
- Trilha de aprovação completa [web:16].
- Monitoramento de obrigações regulatórias [web:16].

---

#### 33. Relatórios

- Contratos por status.
- Contratos por tipo.
- Contratos por unidade.
- Contratos por contraparte.
- Contratos por gestor.
- Valor contratado por período.
- Contratos a vencer.
- Contratos renovados x encerrados.
- Tempo de ciclo por tipo [web:15].
- Gargalos de aprovação [web:15].
- Pendências de assinatura.
- Obrigações em atraso.
- Compliance documental.
- Contratos com risco alto.

---

#### 34. Checklist de entrega

##### Frontend
- Dashboard completo.
- Datatables com filtros avançados.
- Drawers CRUD.
- Kanban.
- Calendário.
- Página de detalhe.
- Timeline.
- Exportações.
- Estados visuais.
- Responsividade.

##### Backend
- CRUD completo.
- Regras de negócio.
- Jobs.
- Auditoria.
- Permissões.
- API REST.
- Upload de arquivos.
- Versionamento.
- Logs.

##### Governança
- RBAC.
- Compliance.
- Trilha de auditoria.
- Alertas.
- Parametrizações.
- Templates.
- Fluxos de aprovação.

---

#### 35. Resultado esperado

Ao final da implementação, o módulo deve permitir controlar ponta a ponta o ciclo contratual, com visibilidade gerencial, operação assistida, automações e forte governança, alinhado aos princípios de CLM modernos como centralização, workflow, compliance, repositório digital, alertas de marcos e dashboards de desempenho.
