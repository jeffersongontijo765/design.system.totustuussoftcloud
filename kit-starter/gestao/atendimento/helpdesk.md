# Helpdesk

- Portal: Gestão (`gestao.`)
- Área: Atendimento
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2; [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.7; [19](../../../docs/v2/19-regras-modulos-3.md), seção 7
- Fonte da v1: absorvida integralmente em [chamados-dos-clientes.md](../../desenvolvedor/suporte/chamados-dos-clientes.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Atendimento interno e externo da entidade por modelo único de ticket, com SLA, filas e base de conhecimento.

## 3. Telas

- **Tickets** (DataTable e kanban por estado).
- **Ticket — detalhe** (conversa, SLA, histórico).
- **Filas e categorias** (configuração).
- **SLA** (políticas).
- **Base de conhecimento** (artigos).

## 4. Permissões por portal (extraídas do SDD)

Do [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md):

| Portal | Quem abre | Onde é atendido | Visibilidade |
|---|---|---|---|
| Gestão | Equipe da entidade e atendentes | Fila da categoria e da unidade | Conforme permissão da fila |

Do [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md):

| Portal | Recurso de privacidade | Escopo |
|---|---|---|
| Gestão | DPO da entidade, ROPA da entidade, pedidos de titular, consentimentos, termos de imagem, proteção de menores | Entidade e unidades conforme permissão |

Do [31](../../../docs/v2/31-matriz-portais-modulos.md):

| Portal | Teste de isolamento | Teste de permissão | Teste de fluxo principal | Teste de acessibilidade |
|---|---|---|---|---|
| Gestão | Cross-tenant e cross-unidade | Papel sem permissão não vê o módulo | Matrícula, cobrança, emissão de documento | Telas principais |

Do [31](../../../docs/v2/31-matriz-portais-modulos.md):

| Portal | Autenticação | Sessão | Dados e restrições especiais |
|---|---|---|---|
| Gestão | Senha e MFA conforme política da entidade ([06](../../../docs/v2/06-identidade-acesso.md), seção 5) | Padrão | Consulta por CPF com finalidade ([21](../../../docs/v2/21-busca-e-armazenamento.md), seção 6.8) |

## 5. Papéis

- `unit.support`.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Modelo único ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.1); estados ([32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2.2).

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

### 13.1 [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 2

#### 2. Atendimento: Help Desk e SAC

##### 2.1 Modelo único

Um só módulo de atendimento. Help desk é a base. SAC, chat rápido e tickets de canal são **canais ou tipos** do mesmo registro. Cada solicitação tem número de protocolo ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.2).

**Decisão proposta:** ticket é um tipo de protocolo. Todo ticket tem número de protocolo; nem todo protocolo é ticket (ex.: requerimento de 2ª chamada pode ser protocolo sem fila de atendimento). **Decidido** em 03/11/2026: ticket é tipo de protocolo em parte. Pedido com responsável e prazo recebe protocolo.

##### 2.2 Estados do ticket (da v1)

| Estado | Próximos estados permitidos |
|---|---|
| `novo` | `aberto`, `em_triagem`, `cancelado` |
| `aberto` | `em_triagem`, `em_atendimento`, `cancelado` |
| `em_triagem` | `em_atendimento`, `escalonado`, `cancelado` |
| `em_atendimento` | `aguardando_cliente`, `aguardando_terceiro`, `aguardando_aprovacao`, `em_pausa`, `resolvido`, `escalonado` |
| `aguardando_cliente`, `aguardando_terceiro`, `aguardando_aprovacao`, `em_pausa` | `em_atendimento` ou `resolvido` |
| `resolvido` | `fechado`, `reaberto` |
| `fechado` | `reaberto`, dentro da janela configurável |
| `reaberto` | `em_atendimento` |
| `escalonado` | `em_atendimento` |
| `cancelado`, `fechado` (sem reabertura) | Estados finais |

Regras:

- Estado `aguardando_*` pausa o contador de SLA conforme a regra de SLA (abaixo).
- Cada transição grava quem, quando e motivo quando o estado for `cancelado`, `escalonado` ou `reaberto`.
- Transição inválida é recusada pela aplicação ([15](../../../docs/v2/15-validacoes.md), seção 5), não só pela tela.

##### 2.3 SLA

Tipos (da v1): primeira resposta, próxima resposta, resolução, fechamento.

Aplicação: por entidade (tenant), por cliente, por fila, por tipo, por categoria e por prioridade. A regra mais específica vence.

**Proposta de valores iniciais:** definir por entidade, sem padrão universal. Valores padrão decididos em 03/11/2026: de 1 hora a 10 dias úteis por prioridade, ajustáveis por entidade. Sem valor definido, o ticket não recebe prazo, e o painel mostra "sem SLA".

Alerta: 80% do prazo consumido, e prazo estourado. Estouro entra no painel do gestor, não no portal do solicitante.

##### 2.4 Prioridade, categoria e fila

- Prioridade: baixa, média, alta, urgente. Urgente exige categoria que permita ([15](../../../docs/v2/15-validacoes.md)).
- Categoria: lista fechada por entidade. Ex.: secretaria, financeiro, biblioteca, TI, saúde.
- Fila: uma por categoria ou unidade. Atribuição automática por fila; redistribuição pelo coordenador.

##### 2.5 Canais

Conforme [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 2, com estas regras de atendimento:

- Opção "Abrir ticket" sem IA em todo ponto de atendimento (D-18).
- Texto do solicitante é guardado literal, nunca interpretado como instrução ([05](../../../docs/v2/05-seguranca.md)).
- Campos obrigatórios variam por tipo, conforme a v1 ([`SPEC-HELPDESK.md`](../../../docs/v2/anexo-v1/SPEC-HELPDESK.md), seção 7). Lista de campos padrão é fixa para todo tipo.

##### 2.6 Portal do cliente (solicitante)

- Abertura, acompanhamento, anexos, respostas públicas por padrão (v1, seção 12), consulta da base de conhecimento e avaliação do atendimento.
- Resposta interna (nota do atendente) nunca aparece no portal.
- Consulta pública por número e CPF, sem login, com limite de tentativas ([17](../../../docs/v2/17-regras-modulos.md), seção 3).

##### 2.7 Base de conhecimento

- Artigo tem autor, revisor, versão, data de revisão e público (interno, portal ou público).
- Artigo com dado pessoal não é publicado.
- Artigo que a IA sugere ao atendente passa pela regra de [27](../../../docs/v2/27-inteligencia-artificial-e-portais.md) (fonte cadastrada).

##### 2.8 Atendimento por portal

| Portal | Quem abre | Onde é atendido | Visibilidade |
|---|---|---|---|
| Desenvolvedor | Entidades (clientes da plataforma) | Suporte da plataforma | Tickets de clientes; sem dado de aluno sem chamado vinculado ([29](../../../docs/v2/29-auditoria.md), seção 8) |
| Gestão | Equipe da entidade e atendentes | Fila da categoria e da unidade | Conforme permissão da fila |
| Professor | Docente, para materiais, reservas, justificativas | Secretaria ou coordenação | Só o próprio ticket |
| Aluno | Aluno, para segunda chamada, declaração, dúvidas | Secretaria, biblioteca, financeiro | Só o próprio ticket |
| Responsáveis | Responsável legal, pelos dependentes | Secretaria, financeiro, coordenação | Só dependentes com vínculo ativo |
| Terceiros | Fornecedor, para manutenção e acesso | Operacional e compras | Só o próprio ticket |

##### 2.9 Bots

Bot de atendimento segue [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 3 e [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.7. Não resolve ticket de categoria sensível (saúde, denúncia, conflito) sem encaminhar para humano.

##### 2.10 Pendências do atendimento

| # | Pendência | Tipo |
|---|---|---|
| ATD-01 | Ticket como tipo de protocolo (seção 2.1) | **Aprovado em parte** em 03/11/2026: pedido com responsável e prazo recebe protocolo |
| ATD-02 | Valores padrão de SLA (seção 2.3) | **Decidido** em 03/11/2026: 1 hora a 10 dias úteis por prioridade, ajustável por entidade |
| ATD-03 | Retenção de tickets e de transcrição | (jurídico) — ver LAC-24 em [22](../../../docs/v2/22-crm-canais-e-papeis.md) |
| ATD-04 | DDL do módulo de atendimento (estados, SLA, canais, artigos) | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 1. Revisão do owner pendente (DDL-01) |
| ATD-05 | Regra para categoria sensível e encaminhamento | **Decidido** em 03/11/2026: encaminha ao canal da entidade e restringe o acesso |

### 13.2 [31](../../../docs/v2/31-matriz-portais-modulos.md), seção 3.7

##### 3.7 Atendimento: SAC, helpdesk, chat e bots

Há três especificações separadas, todas em "Revisar" no catálogo:

- [`spec_chat_rapido_sac.md`](../../../docs/v2/anexo-v1/spec_chat_rapido_sac.md): chat rápido e abertura de ticket no SAC.
- [`SPEC-HELPDESK.md`](../../../docs/v2/anexo-v1/SPEC-HELPDESK.md): helpdesk com SLA, base de conhecimento e portal do cliente.
- [`spec_gestao_sac_base_conhecimento.md`](../../../docs/v2/anexo-v1/spec_gestao_sac_base_conhecimento.md).

**Decisão proposta (já adotada na v1 do catálogo):** um módulo único de atendimento, com helpdesk como base ([19](../../../docs/v2/19-regras-modulos-3.md), seção 2). Os canais (chat do site, WhatsApp, Telegram, Instagram, Messenger, telefone e presencial) são entradas desse módulo, com as regras de [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 2.

**Bots.** Há dois tipos e não podem ser confundidos:

| Bot | Dono | Regra |
|---|---|---|
| Bot de captação (CRM) | CRM da plataforma ou do tenant | [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 3 |
| Bot de atendimento (SAC) | Atendimento | Mesma regra de IA: fonte cadastrada, humano para o resto, opção "Abrir ticket" sem IA (D-18) |

A reunião global ([`global_meeting_spec_v2_complete.md`](../../../docs/v2/anexo-v1/global_meeting_spec_v2_complete.md)) menciona proteção contra bot em entrada pública, sem módulo de bot. Não é um terceiro tipo.

Pendente: a v2 ainda não tem DDL do atendimento consolidado (T-02 em [19](../../../docs/v2/19-regras-modulos-3.md)).

### 13.3 [19](../../../docs/v2/19-regras-modulos-3.md), seção 7

#### 7. Atendimento (SAC, Chat rápido, Helpdesk)

Três especificações descrevem o mesmo tipo de solicitação. A v1 do Helpdesk cita tenant 23 vezes e define obrigatoriedade dinâmica por tipo (linhas 142 e 340).

Regras do Helpdesk:

| Regra | Detalhe |
|---|---|
| Campos obrigatórios | Variam por tipo de solicitação (linha 142). |
| Campos padrão | Lista fixa para todo tipo (seção 8.1). |
| Retenção | Política e expurgo (linha 791). |
| Canais | Obrigatórios por tipo (seção 6.1). |

**Proposta:** um módulo de atendimento. Helpdesk como base. SAC e Chat rápido viram canais ou tipos de solicitação.

**Pendente:** DDL (T-02).
