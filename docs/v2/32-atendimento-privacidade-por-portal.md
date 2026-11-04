# 32 — Atendimento (Help Desk, SAC), Privacidade, LGPD e Encarregado, por Portal

> Parte do [SDD v2](00-README.md). Matriz de portais e fronteiras em [31](31-matriz-portais-modulos.md). Protocolo e canais em [22](22-crm-canais-e-papeis.md) e [31](31-matriz-portais-modulos.md), seção 3.2. Base legal e direitos em [07](07-privacidade-lgpd.md). Incidentes em [07](07-privacidade-lgpd.md), seção 8, e [05](05-seguranca.md), seção 6. Auditoria em [29](29-auditoria.md).
> **Status:** aprovada pelo autor em 03/11/2026, com as propostas adotadas. Itens sem valor definido continuam pendentes, criada em 03/11/2026 a partir das especificações da v1 ([`SPEC-HELPDESK.md`](anexo-v1/SPEC-HELPDESK.md), [`spec_chat_rapido_sac.md`](anexo-v1/spec_chat_rapido_sac.md), [`spec_gestao_sac_base_conhecimento.md`](anexo-v1/spec_gestao_sac_base_conhecimento.md), [`spec_gestao_privacy_global_completo.md`](anexo-v1/spec_gestao_privacy_global_completo.md), [`spec-sub-sidebar-privacidade-lgpd.md`](anexo-v1/spec-sub-sidebar-privacidade-lgpd.md)). Itens **[Decisão do autor]** dependem de resposta. Itens **(jurídico)** dependem de parecer ([25](25-dossie-juridico-e-lacunas.md), [26](26-sdd-juridico-regulatorio.md)).
> **Premissa:** o pedido diz "pdo". Entendi como **DPO (encarregado)**. Se for outra coisa, avise.
> **Atualização de 03/11/2026:** o protocolo passa a ser serviço comum, usado também por documentos recebidos, administrativos e emitidos. Ver [54](54-gestao-de-documentos-tres-contextos.md), seção 5.

---

## 1. Estado atual na v2

| Assunto | O que a v2 tem | Falta |
|---|---|---|
| Help desk / SAC | Só a decisão de unificar em um módulo ([19](19-regras-modulos-3.md), seção 7) e as regras de bot ([22](22-crm-canais-e-papeis.md), seção 3) | Estados, transições, SLA, filas, categorias, portal do cliente, base de conhecimento, DDL |
| Privacidade e LGPD | Compromissos, inventário, bases legais, direitos, retenção, incidentes, métricas ([07](07-privacidade-lgpd.md)) | Fluxo de solicitação do titular com estados e prazo, gestão de consentimento por finalidade, registro de tratamento (ROPA) com DDL, transferência internacional, consentimento parental, painel do DPO |
| Encarregado (DPO) | Papel citado em [22](22-crm-canais-e-papeis.md), seção 5, e em [29](29-auditoria.md), seção 5 | Escopo do papel no sistema, fila de aprovação, relatório de impacto (RIPD), tarefas e prazos |

Conclusão: **nenhum dos quatro assuntos está completo na v2.** Os requisitos da v1 existem, mas não foram trazidos para a v2 com estados, DDL e critério de aceite.

---

## 2. Atendimento: Help Desk e SAC

### 2.1 Modelo único

Um só módulo de atendimento. Help desk é a base. SAC, chat rápido e tickets de canal são **canais ou tipos** do mesmo registro. Cada solicitação tem número de protocolo ([31](31-matriz-portais-modulos.md), seção 3.2).

**Decisão proposta:** ticket é um tipo de protocolo. Todo ticket tem número de protocolo; nem todo protocolo é ticket (ex.: requerimento de 2ª chamada pode ser protocolo sem fila de atendimento). **Decidido** em 03/11/2026: ticket é tipo de protocolo em parte. Pedido com responsável e prazo recebe protocolo.

### 2.2 Estados do ticket (da v1)

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
- Transição inválida é recusada pela aplicação ([15](15-validacoes.md), seção 5), não só pela tela.

### 2.3 SLA

Tipos (da v1): primeira resposta, próxima resposta, resolução, fechamento.

Aplicação: por entidade (tenant), por cliente, por fila, por tipo, por categoria e por prioridade. A regra mais específica vence.

**Proposta de valores iniciais:** definir por entidade, sem padrão universal. Valores padrão decididos em 03/11/2026: de 1 hora a 10 dias úteis por prioridade, ajustáveis por entidade. Sem valor definido, o ticket não recebe prazo, e o painel mostra "sem SLA".

Alerta: 80% do prazo consumido, e prazo estourado. Estouro entra no painel do gestor, não no portal do solicitante.

### 2.4 Prioridade, categoria e fila

- Prioridade: baixa, média, alta, urgente. Urgente exige categoria que permita ([15](15-validacoes.md)).
- Categoria: lista fechada por entidade. Ex.: secretaria, financeiro, biblioteca, TI, saúde.
- Fila: uma por categoria ou unidade. Atribuição automática por fila; redistribuição pelo coordenador.

### 2.5 Canais

Conforme [22](22-crm-canais-e-papeis.md), seção 2, com estas regras de atendimento:

- Opção "Abrir ticket" sem IA em todo ponto de atendimento (D-18).
- Texto do solicitante é guardado literal, nunca interpretado como instrução ([05](05-seguranca.md)).
- Campos obrigatórios variam por tipo, conforme a v1 ([`SPEC-HELPDESK.md`](anexo-v1/SPEC-HELPDESK.md), seção 7). Lista de campos padrão é fixa para todo tipo.

### 2.6 Portal do cliente (solicitante)

- Abertura, acompanhamento, anexos, respostas públicas por padrão (v1, seção 12), consulta da base de conhecimento e avaliação do atendimento.
- Resposta interna (nota do atendente) nunca aparece no portal.
- Consulta pública por número e CPF, sem login, com limite de tentativas ([17](17-regras-modulos.md), seção 3).

### 2.7 Base de conhecimento

- Artigo tem autor, revisor, versão, data de revisão e público (interno, portal ou público).
- Artigo com dado pessoal não é publicado.
- Artigo que a IA sugere ao atendente passa pela regra de [27](27-inteligencia-artificial-e-portais.md) (fonte cadastrada).

### 2.8 Atendimento por portal

| Portal | Quem abre | Onde é atendido | Visibilidade |
|---|---|---|---|
| Desenvolvedor | Entidades (clientes da plataforma) | Suporte da plataforma | Tickets de clientes; sem dado de aluno sem chamado vinculado ([29](29-auditoria.md), seção 8) |
| Gestão | Equipe da entidade e atendentes | Fila da categoria e da unidade | Conforme permissão da fila |
| Professor | Docente, para materiais, reservas, justificativas | Secretaria ou coordenação | Só o próprio ticket |
| Aluno | Aluno, para segunda chamada, declaração, dúvidas | Secretaria, biblioteca, financeiro | Só o próprio ticket |
| Responsáveis | Responsável legal, pelos dependentes | Secretaria, financeiro, coordenação | Só dependentes com vínculo ativo |
| Terceiros | Fornecedor, para manutenção e acesso | Operacional e compras | Só o próprio ticket |

### 2.9 Bots

Bot de atendimento segue [22](22-crm-canais-e-papeis.md), seção 3 e [31](31-matriz-portais-modulos.md), seção 3.7. Não resolve ticket de categoria sensível (saúde, denúncia, conflito) sem encaminhar para humano.

### 2.10 Pendências do atendimento

| # | Pendência | Tipo |
|---|---|---|
| ATD-01 | Ticket como tipo de protocolo (seção 2.1) | **Aprovado em parte** em 03/11/2026: pedido com responsável e prazo recebe protocolo |
| ATD-02 | Valores padrão de SLA (seção 2.3) | **Decidido** em 03/11/2026: 1 hora a 10 dias úteis por prioridade, ajustável por entidade |
| ATD-03 | Retenção de tickets e de transcrição | (jurídico) — ver LAC-24 em [22](22-crm-canais-e-papeis.md) |
| ATD-04 | DDL do módulo de atendimento (estados, SLA, canais, artigos) | **Escrito** em [51](51-ddl-modulos-novos.md), seção 1. Revisão do owner pendente (DDL-01) |
| ATD-05 | Regra para categoria sensível e encaminhamento | **Decidido** em 03/11/2026: encaminha ao canal da entidade e restringe o acesso |

---

## 3. Privacidade e LGPD

### 3.1 Princípio de organização

A privacidade tem **duas escalas**:

- **Plataforma:** governança da própria empresa como controladora (ROPA, RIPD, incidentes, DPO, contratos com clientes).
- **Entidade:** governança do tenant como controlador. A plataforma é operadora. Cada entidade tem o próprio DPO, o próprio registro de tratamento e os próprios pedidos de titular.

Essa separação segue [22](22-crm-canais-e-papeis.md), seção 1, e [31](31-matriz-portais-modulos.md), seção 3.

### 3.2 Consentimento

Cada consentimento registra: finalidade, canal, versão do texto, data de concessão, data de revogação e evidência. Já definido em `crm_consents` ([22](22-crm-canais-e-papeis.md), seção 8). Falta generalizar:

| Regra | Detalhe |
|---|---|
| Finalidade separada | Cada finalidade tem consentimento próprio. Marketing não é condição de matrícula. |
| Revogação simples | Mesmo canal de concessão, sem barreira extra. Efeito imediato. |
| Consentimento não apagado | Revogação preenche `revoked_at`. Histórico fica. |
| Menor de 13 anos | Consentimento parental verificável antes da coleta. Método **(jurídico)**. |
| Menor de 18 e maior de 13 | Regra de [07](07-privacidade-lgpd.md), seção 3. Confirmar base por tipo de dado **(jurídico)**. |
| Termo de imagem | Consentimento específico por finalidade (site, redes, mural). Revogável. |

### 3.3 Solicitação do titular

Fluxo, com estados e prazo (base em [07](07-privacidade-lgpd.md), seção 4):

| Estado | Ação |
|---|---|
| `recebida` | Protocolo gerado; prazo começa no recebimento |
| `identidade_pendente` | Verificação por canal verificado. Sem verificação, não há resposta. |
| `em_analise` | Atribuída a responsável. Avalia exceção legal. |
| `aguardando_dpo` | Pedido sensível ou com exceção: aprovação do DPO |
| `atendida` | Resposta entregue pelo canal verificado |
| `negada_com_motivo` | Recusa fundamentada, com a exceção legal citada **(jurídico)** |
| `encerrada` | Estado final |

Regras:

- Prazo de referência: 15 dias para confirmação e acesso, conforme [07](07-privacidade-lgpd.md), seção 4 **(jurídico)**. O sistema calcula o prazo e alerta com antecedência.
- Pedido de titular que é menor passa pelo responsável legal, com verificação de vínculo ([07](07-privacidade-lgpd.md), seção 4).
- Pedido recebido por atendimento vira ticket e protocolo (seção 2), com categoria `privacidade`.
- Exclusão respeita retenção legal e preservação probatória. Exceção é registrada com motivo ([31](31-matriz-portais-modulos.md)).

### 3.4 Registro de tratamento (ROPA)

Cada tratamento tem: finalidade, base legal, categoria de titular, categoria de dado, operador, prazo de retenção, medida de segurança e local de armazenamento. [07](07-privacidade-lgpd.md), seção 2, exige o registro, mas não define a tabela.

**Pendência:** DDL do ROPA por escala (plataforma e entidade). Documento a criar.

### 3.5 Incidentes

Já definido em [07](07-privacidade-lgpd.md), seção 8, com prazo de três dias úteis **(jurídico)**. Falta o registro estruturado: tipo de dado, volume de titulares, risco, comunicação à ANPD e aos titulares, medidas e lições. Esse é o modelo de [18](18-regras-modulos-2.md), seção 4.

### 3.6 Transferência e operadores

Lista de operadores e contrato de tratamento: [07](07-privacidade-lgpd.md), seção 7. Transferência internacional: **(jurídico)**. A v1 lista jurisdições de vários países ([`spec_gestao_privacy_global_completo.md`](anexo-v1/spec_gestao_privacy_global_completo.md), seção 4); a v2 limita ao Brasil, conforme [07](07-privacidade-lgpd.md), seção 3, até haver cliente fora do país.

### 3.7 Painel do DPO

O DPO precisa de:

- fila de pedidos de titular e de aprovação;
- prazos e alertas;
- incidentes em aberto;
- RIPD em andamento (lacuna G-05 em [25](25-dossie-juridico-e-lacunas.md));
- trilha de decisão.

O DPO **não opera** o módulo que audita ([22](22-crm-canais-e-papeis.md), seção 5). Ele vê o resultado, não altera o dado.

---

## 4. Privacidade por portal

| Portal | Recurso de privacidade | Escopo |
|---|---|---|
| Desenvolvedor | ROPA da plataforma, incidentes da plataforma, DPO da plataforma, contratos de operador com clientes | Plataforma apenas |
| Gestão | DPO da entidade, ROPA da entidade, pedidos de titular, consentimentos, termos de imagem, proteção de menores | Entidade e unidades conforme permissão |
| Professor | Próprias configurações de privacidade, consentimento de uso de imagem de turma | Só o próprio dado |
| Aluno | Dados cadastrais, solicitação LGPD, revogação de consentimento | Só o próprio dado |
| Responsáveis | Consentimento de imagem dos filhos, dados dos filhos, solicitação LGPD pelos dependentes | Só dependentes com vínculo ativo |
| Terceiros | Acordo de tratamento de dados (DPA), termo de confidencialidade | Só a própria empresa |

**Regra:** pedido de titular nunca é atendido por outro portal que não o do próprio titular ou do responsável verificado.

---

## 5. Pendências de privacidade e LGPD

| # | Pendência | Tipo |
|---|---|---|
| LGPD-01 | DDL do ROPA (plataforma e entidade) | **Escrito** em [51](51-ddl-modulos-novos.md), seção 2. Revisão do owner pendente (DDL-01) |
| LGPD-02 | DDL do pedido de titular e seus estados (seção 3.3) | **Escrito** em [51](51-ddl-modulos-novos.md), seção 2. Revisão do owner pendente (DDL-01) |
| LGPD-03 | Método de consentimento parental para menor de 13 anos | (jurídico) |
| LGPD-04 | Bases legais por tipo de dado escolar, incluindo menores | (jurídico), lacuna Q-03 a Q-08 em [25](25-dossie-juridico-e-lacunas.md) |
| LGPD-05 | Transferência internacional, se houver cliente fora do Brasil | (jurídico) |
| LGPD-06 | Painel do DPO e RIPD (G-05) | Documento e (jurídico) |
| LGPD-07 | Quem é o DPO da plataforma e o de cada entidade | **Decidido** em 03/11/2026: plataforma é a empresa desenvolvedora. Entidade designa o seu, podendo contratar a empresa. Nomes a informar |
| LGPD-08 | Prazo de comunicação de incidente (três dias úteis, Resolução 15/2024) | (jurídico) confirmar vigência |

---

## 6. Critérios de aceite

- [ ] Ticket com estados e transições da seção 2.2, testados (transição inválida recusada).
- [ ] SLA aplicado por regra mais específica, com pausa em estados `aguardando_*`.
- [ ] Portal do cliente não mostra nota interna.
- [ ] Consentimento por finalidade, com revogação registrada sem apagar histórico.
- [ ] Pedido de titular com protocolo, prazo calculado e verificação de identidade antes de qualquer resposta.
- [ ] ROPA e incidentes com DDL e relatórios por escala.
- [ ] Cada portal mostra só o recurso da seção 4.
- [ ] Itens **[Decisão do autor]** e **(jurídico)** respondidos ou marcados como pendentes no [00](00-README.md).

## 7. Decisões de 03/11/2026

**ATD-01 (ticket como protocolo): aprovado em parte.**

- Recebe número de protocolo todo pedido que tem responsável e prazo: requerimento, reclamação, solicitação de documento, pedido de titular, chamado de TI, chamado de manutenção.
- Não recebe protocolo a pergunta respondida pelo bot ou pela base de conhecimento, sem fila de atendimento. Se a pergunta virar pedido, recebe protocolo nesse momento.

**ATD-02 (valores padrão de SLA): aprovado.** Padrão inicial, ajustável por entidade dentro do limite do contrato:

| Prioridade | Primeira resposta | Resolução |
|---|---|---|
| Urgente | 1 hora | 4 horas |
| Alta | 4 horas | 2 dias úteis |
| Média | 1 dia útil | 5 dias úteis |
| Baixa | 2 dias úteis | 10 dias úteis |

Fechamento automático 3 dias úteis após `resolvido`, sem resposta do solicitante. Tempo em `aguardando_*` não conta.

**LGPD-07 (DPO): aprovado.**

- DPO da plataforma: a empresa desenvolvedora, por meio do encarregado indicado por ela. Ele aparece no painel do portal do desenvolvedor.
- DPO de cada entidade: designado pela própria entidade, como controladora. A entidade pode designar a empresa desenvolvedora por contrato. **(jurídico)** confirmar a forma de designação e de contato público.
