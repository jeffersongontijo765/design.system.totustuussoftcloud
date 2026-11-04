# Notificações

- Portal: Gestão (`gestao.`)
- Área: Configuração e acesso
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13); especificação da v1 absorvida integralmente (seção 14)
- Fonte da v2: [57](../../../docs/v2/57-notificacoes-por-portal.md) (integral); [18](../../../docs/v2/18-regras-modulos-2.md), seção 3; [75](../../../docs/v2/75-busca-notificacoes-perfil-integracoes-por-escopo.md), seção 3
- Fonte da v1: [spec_gestao_notificacoes_revisada.md](../../../docs/v2/anexo-v1/spec_gestao_notificacoes_revisada.md) (642 linhas); [spec_gestao_notificacoes.md](../../../docs/v2/anexo-v1/spec_gestao_notificacoes.md) (378 linhas) — absorvida integralmente na seção 14

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. A seção 14 é o texto integral da v1, guardado para que nenhum detalhe se perca; quando ela disser algo diferente das seções 1 a 13, vale a v2. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Modelos, canais, preferências e regras de envio de notificações da entidade.

## 3. Telas

- **Modelos** (lista e editor por canal).
- **Regras de envio** (eventos × público × canal).
- **Envios** (log com estado).
- **Preferências padrão** (por portal).

## 4. Permissões por portal (extraídas do SDD)

Do [57](../../../docs/v2/57-notificacoes-por-portal.md):

| Portal | Quem envia | Para quem | Canais | Exemplos de aviso (da v1) |
|---|---|---|---|---|
| **Gestão** | Direção, gestor de unidade | Público da entidade ou da unidade | In-app, e-mail, SMS, WhatsApp, push | Comunicado da direção, aviso geral |

## 5. Papéis

- `unit.manager`: regras e modelos.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- [57](../../../docs/v2/57-notificacoes-por-portal.md); estados e validações ([18](../../../docs/v2/18-regras-modulos-2.md), seção 3); consentimento por canal ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 5).

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

### 13.1 [57 — Notificações, por Portal](../../../docs/v2/57-notificacoes-por-portal.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Eventos que disparam notificação em [14](../../../docs/v2/14-integracao-modulos.md). Canais e provedores de plataforma em [16](../../../docs/v2/16-integracoes-externas.md). Verificação de contato e MFA em [06](../../../docs/v2/06-identidade-acesso.md). Consentimento por canal em [26](../../../docs/v2/26-sdd-juridico-regulatorio.md) e [22](../../../docs/v2/22-crm-canais-e-papeis.md). Regras de envio, estados e dados sensíveis em [18](../../../docs/v2/18-regras-modulos-2.md), seção 3. Auditoria em [29](../../../docs/v2/29-auditoria.md). Idioma em [09](../../../docs/v2/09-internacionalizacao.md). Referência de módulo: [`spec_gestao_notificacoes_revisada.md`](../../../docs/v2/anexo-v1/spec_gestao_notificacoes_revisada.md) (v1, 642 linhas) unida a [`spec_gestao_notificacoes.md`](../../../docs/v2/anexo-v1/spec_gestao_notificacoes.md) (v1, 378 linhas), por decisão NOT-01.
> **Veredito:** o módulo de notificações **não está completo como módulo**. Há regras soltas para estados, validação, canais de conta e dado sensível. Falta o módulo em si: templates, regras de envio, preferências do usuário, targeting por portal, fallback entre provedores e painel de operação.

---

#### 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Existe especificação de notificações na v2? | **Não.** O catálogo marca "Revisar", com duas versões na v1 |
| Estados e transições estão definidos? | **Sim**, herdados da v1 revisada e validados em [18](../../../docs/v2/18-regras-modulos-2.md), seção 3.1 |
| Canais estão definidos? | **Parcial.** E-mail e SMS aparecem em [16](../../../docs/v2/16-integracoes-externas.md). WhatsApp, Telegram e chat, em [22](../../../docs/v2/22-crm-canais-e-papeis.md). Push e in-app não aparecem na v2 |
| Preferências do usuário? | **Não.** Só consentimento por finalidade em [32](../../../docs/v2/32-atendimento-privacidade-por-portal.md), seção 3.2 |
| Targeting: quem envia a quem? | **Não.** A v1 lista avisos por portal, mas não diz quem pode enviar para quem |
| Templates e variáveis? | **Não** na v2. A v1 revisada tem o conceito, sem regra de idioma nem de conteúdo |
| Fallback e saúde de provedor? | **Não** na v2. A v1 revisada tem a regra |
| Dado sensível no corpo? | **Sim**, em [18](../../../docs/v2/18-regras-modulos-2.md), seção 3.3 |
| Painel de operação e métricas? | **Não** na v2. A v1 tem, em detalhe |

---

#### 2. Lacunas

1. **Módulo sem documento próprio.** As regras estão em cinco docs diferentes. Não há ponto único de consulta.
2. **Canal push e in-app ausentes.** A v1 lista ambos. Sem eles, avisos de aplicativo não têm caminho.
3. **Preferências do usuário ausentes.** Sem tela de preferência, o responsável não escolhe canal, horário ou tipo de aviso.
4. **Horário de silêncio ausente.** Mensagem às 23h para responsável não tem regra.
5. **Targeting ausente.** Não há regra para "todas as famílias da turma X", "responsáveis com dependente com vínculo ativo", "professores da unidade". Sem isso, o envio em massa fica sem controle.
6. **Templates e i18n ausentes.** Texto de aviso precisa de versão por idioma ([09](../../../docs/v2/09-internacionalizacao.md)) e de variáveis validadas.
7. **Fallback entre provedores ausente.** [16](../../../docs/v2/16-integracoes-externas.md) define um provedor por tipo. A v1 prevê vários por canal e troca automática quando um cai.
8. **Painel de operação ausente.** Fila, falhas, reenvio e métricas de entrega não têm tela nem métrica definida. [24](../../../docs/v2/24-operacao-continuidade-qualidade.md) tem só uma meta ("99% em até 5 min"). **Escrito** nas seções 3.8 e 3.9 (NOT-08).
9. **Conflito de versões da v1.** Há [`spec_gestao_notificacoes.md`](../../../docs/v2/anexo-v1/spec_gestao_notificacoes.md) (378 linhas) e a revisada (642 linhas). **Decidido** em 03/11/2026 (NOT-01): as duas são unidas. A revisada dá estados, eventos, reenvio e observabilidade. A original dá as telas e o painel (seções 3.8 e 3.9).
10. **Notificação de saúde.** [18](../../../docs/v2/18-regras-modulos-2.md), seção 3.3, proíbe diagnóstico no corpo. Não há regra de quem pode enviar aviso de saúde, nem para quem.

---

#### 3. Modelo proposto

##### 3.1 Canais

| Canal | Uso | Dono do envio | Regra |
|---|---|---|---|
| In-app | Avisos internos e de portal | Plataforma | Padrão para aviso que não é urgente |
| E-mail | Verificação, recuperação, comunicado formal | Plataforma (verificação) e entidade (comunicado) | Endereço verificado ([06](../../../docs/v2/06-identidade-acesso.md), D-04). Link de descadastro em marketing ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md)) |
| Push | Aviso de aplicativo, Android e iOS | Plataforma | Depende do aplicativo e de token de dispositivo válido. Decidido pelo autor em 03/11/2026 |
| SMS | Aviso não crítico e opcional | Entidade | Não é fator de MFA ([16](../../../docs/v2/16-integracoes-externas.md)). Desligado por padrão |
| WhatsApp | Aviso com opt-in | Entidade | Opt-in registrado ([22](../../../docs/v2/22-crm-canais-e-papeis.md)). Template aprovado pelo provedor |
| Webhook | Integração com sistema da entidade | Entidade | Assinatura validada na recepção |

##### 3.2 Estados

Herdados da v1 revisada e validados em [18](../../../docs/v2/18-regras-modulos-2.md), seção 3.1: `draft`, `in_review`, `scheduled`, `queued`, `processing`, `sent`, `delivered`, `read`, `failed`, `archived`, `cancelled`.

Regra adicional: `read` nunca é gravado pelo envio. É gravado só quando o destinatário abre o aviso.

##### 3.3 Preferências do usuário

- Cada pessoa escolhe canal por tipo de aviso: acadêmico, financeiro, comunicado geral.
- Aviso obrigatório não pode ser desligado: verificação, recuperação de conta, MFA, aviso de saúde e comunicado de segurança.
- Horário de silêncio por pessoa, com exceção para aviso obrigatório. Decidido pelo autor em 03/11/2026: 21h às 7h.
- Opt-out de marketing vale em todos os canais ([22](../../../docs/v2/22-crm-canais-e-papeis.md), palavras `PARAR` e `SAIR`).

##### 3.4 Targeting

Envio só para um público definido por regra, nunca para lista aberta:

| Público | Regra | Quem pode definir |
|---|---|---|
| Turma | Alunos com matrícula ativa na turma | Professor da turma, coordenação |
| Responsáveis de uma turma | Responsáveis com vínculo ativo a alunos da turma | Coordenação, secretaria |
| Unidade | Todos com vínculo ativo na unidade | Gestão da unidade |
| Entidade | Todos com vínculo ativo na entidade | Direção da entidade. Não pode ser professor |
| Plataforma | Clientes ou equipe da empresa | Equipe da empresa desenvolvedora |

Público com mais de 500 destinatários exige aprovação de segunda pessoa, como em [48](../../../docs/v2/48-gerador-de-documentos-por-portal.md), seção 12. Decidido pelo autor em 03/11/2026.

##### 3.5 Templates

- Template tem versão, idioma, variáveis validadas e categoria (acadêmico, financeiro, pastoral, segurança).
- Variável sem valor bloqueia o envio.
- Template de WhatsApp precisa ser aprovado pelo provedor antes de uso.
- Notificação de saúde ou de RH não tem diagnóstico nem salário no corpo ([18](../../../docs/v2/18-regras-modulos-2.md), seção 3.3). Mostra aviso e link autenticado.

##### 3.6 Provedores e fallback

- Cada canal pode ter mais de um provedor. Um é primário, e os outros são reserva.
- Health check por provedor. Falhas repetidas tiram o provedor do roteamento automático.
- Troca de provedor é registrada em auditoria.

##### 3.7 Retenção

- Corpo da mensagem: prazo configurável por entidade, com padrão a definir **(jurídico)**.
- Registro de entrega (quem, quando, canal, estado): mesmo prazo de log de integração, 90 dias ([49](../../../docs/v2/49-logs-testes-por-portal.md), seção 2).
- Auditoria de envio: prazo de evento de plataforma ([29](../../../docs/v2/29-auditoria.md)).

##### 3.8 Telas do módulo

Vêm da versão original da v1 ([`spec_gestao_notificacoes.md`](../../../docs/v2/anexo-v1/spec_gestao_notificacoes.md), seção 6), unida à revisada por decisão NOT-01. A regra da v2 prevalece quando há conflito: estados de [18](../../../docs/v2/18-regras-modulos-2.md), seção 3.1, aprovação acima de 500 destinatários (NOT-03), silêncio (NOT-02) e permissão por papel.

| Tela | Conteúdo | Regra da v2 |
|---|---|---|
| Painel | Indicadores e gráficos da seção 3.9, com filtro por período, unidade, canal, prioridade e estado | Mostra só o escopo do papel: entidade, unidade ou turma |
| Lista | Tabela com título, tipo, canal, prioridade, unidade, estado, agendada para, enviada em, leitura, tentativas e responsável. Filtros salvos, paginação no servidor, seleção múltipla e exportação | Ação em lote respeita a transição permitida de cada item. Exportação segue a permissão e mascara dado pessoal |
| Criação e edição | Etapas: dados básicos, público, conteúdo, canal, agendamento, regras e revisão final. Prévia das variáveis do template | Sem público válido, não envia. Limite de caracteres por canal. Público acima de 500 vai para aprovação de segunda pessoa |
| Detalhe | Resumo, linha do tempo, entregas por destinatário, interações, log técnico e auditoria | Log técnico só para quem tem papel de operação. Conteúdo de aviso de saúde segue NOT-05 |
| Quadro (kanban) | Colunas por estado: rascunho, em revisão, agendada, processando, enviada, entregue, lida, falhou, arquivada | Arrastar o cartão só faz transição permitida. Estados de entrega (`delivered`, `read`, `failed`) vêm do provedor, não da mão do usuário |
| Automações | Criar, testar, simular, ativar e desativar regra, com versão. Gatilhos: cadastro, mudança de estado, atraso, falha, aniversário, expiração e tarefa pendente | Regra só dispara a partir de evento do catálogo de [14](../../../docs/v2/14-integracao-modulos.md), seção 4. Simulação não envia mensagem |
| Configuração | Canais, provedores, templates, limites de envio, silêncio, política de reenvio, retenção, identidade visual e permissões | Provedor e credencial seguem [16](../../../docs/v2/16-integracoes-externas.md). Retenção segue a seção 3.7 |

Ações por item: ver, editar rascunho, duplicar, reenviar, cancelar agendamento, arquivar e excluir (exclusão lógica). Reenvio de item já entregue pede motivo e fica na auditoria.

##### 3.9 Painel, métricas e alertas

União das métricas das duas versões da v1 (original, seção 7; revisada, seção 15). Fecha NOT-08.

| Métrica | Quem vê |
|---|---|
| Total por período, enviadas hoje, pendentes na fila | Gestão e secretaria, no escopo do papel |
| Taxa de entrega e de leitura, por canal | Gestão e secretaria, no escopo do papel |
| Falhas nas últimas 24 horas e reenvios em andamento | Gestão e operação da plataforma |
| Tempo médio até o envio e até a entrega | Operação da plataforma |
| Falhas por provedor e fila por prioridade | Operação da plataforma |
| Prazo cumprido e violado (meta de [24](../../../docs/v2/24-operacao-continuidade-qualidade.md): 99% em até 5 minutos) | Gestão e operação da plataforma |
| Avisos críticos pendentes | Gestão, no escopo do papel |

Gráficos: volume por dia, itens por estado, distribuição por canal, sucesso e falha por canal, e volume por hora e dia da semana.

**Portal do desenvolvedor:** vê só métricas agregadas de operação, sem título, corpo ou destinatário de mensagem de cliente ([31](../../../docs/v2/31-matriz-portais-modulos.md)).

**Alertas para a operação:** falha elevada por provedor, crescimento anormal da fila, aumento de reenvio, prazo violado, worker sem sinal de vida e taxa de erro acima do limite por canal. Os limites são medidos em homologação.

**Rastreio:** o `correlation_id` acompanha evento, regra, fila, worker, provedor e resultado. Log estruturado com dado sensível redigido ([49](../../../docs/v2/49-logs-testes-por-portal.md), seção 3).

---

#### 4. Por portal

| Portal | Quem envia | Para quem | Canais | Exemplos de aviso (da v1) |
|---|---|---|---|---|
| **Desenvolvedor** | Equipe da empresa | Clientes e equipe | E-mail, in-app | Aviso de manutenção, cobrança da assinatura |
| **Gestão** | Direção, gestor de unidade | Público da entidade ou da unidade | In-app, e-mail, SMS, WhatsApp, push | Comunicado da direção, aviso geral |
| **Professor** | Professor e coordenação | Turma, responsáveis da turma | In-app, push, e-mail | Mensagem para turma, lembrete de prova, aviso de conteúdo |
| **Aluno** | Ninguém envia | Recebe | In-app, push | Aviso de professor e da coordenação, lembrete de prova |
| **Responsáveis** | Não envia comunicado geral | Recebe | In-app, push, SMS, WhatsApp, e-mail | Aviso da diretoria, aviso de saúde ou enfermaria, notificação de entrada e saída, lembrete de reunião |
| **Terceiros** | Não envia comunicado geral | Recebe aviso do próprio contrato | E-mail, in-app | Aviso de vencimento de contrato, de nota recebida, de ordem de compra |

**Regras de portal:**

- Aluno não envia notificação a colega. Professor não envia para público fora da própria turma.
- Responsável não envia para outros responsáveis.
- Notificação de entrada e saída (catraca) só vai ao responsável do dependente, com vínculo ativo ([35](../../../docs/v2/35-acesso-e-seguranca-fisica-por-portal.md)).
- Aviso de saúde ou enfermaria vai ao responsável. Remetentes padrão: secretaria, enfermagem, médico da escola e coordenação. A escola pode incluir ou remover remetentes. Decidido pelo autor em 03/11/2026. Não aparece no portal de terceiros.

---

#### 5. Pendências

| # | Pendência | Tipo |
|---|---|---|
| NOT-01 | Versão de referência da v1: revisada ou original | **Decidido** em 03/11/2026: unir as duas. Telas e painel da original nas seções 3.8 e 3.9 |
| NOT-02 | Horário de silêncio padrão (seção 3.3) | **Decidido** em 03/11/2026: 21h às 7h |
| NOT-03 | Aprovação de segunda pessoa para público acima de 500 (seção 3.4) | **Decidido** em 03/11/2026: sim |
| NOT-04 | Prazo de retenção do corpo da mensagem (seção 3.7) | (jurídico) |
| NOT-05 | Remetentes de aviso de saúde ou enfermagem (seção 4) | **Decidido** em 03/11/2026: secretaria, enfermagem, médico da escola e coordenação por padrão. A escola pode incluir ou remover. Parecer do (jurídico) sobre o conteúdo do aviso continua pendente |
| NOT-06 | Canal push | **Decidido** em 03/11/2026: aplicativo próprio para Android e iOS. Canais: app, SMS, e-mail e WhatsApp |
| NOT-07 | DDL das tabelas do módulo: notificação, template, regra, entrega, fila, preferência e provedor | **Escrito** em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 15.1. Revisão do owner pendente (DDL-01) |
| NOT-08 | Métricas e painel de operação: quais e para quem | **Escrito** na seção 3.9 |
| NOT-09 | Aplicativo Android e iOS: escopo, arquitetura e publicação nas lojas. É um produto novo, fora dos módulos atuais | Documento. **Decidido** em 03/11/2026: entra depois do núcleo |

---

#### 6. Critérios de aceite

- [ ] Aviso obrigatório não pode ser desligado pelo usuário (teste).
- [ ] Aviso fora do horário de silêncio é adiado, salvo obrigatório (teste).
- [ ] Professor não envia para público fora da própria turma (teste de isolamento).
- [ ] Responsável não recebe aviso de dependente sem vínculo ativo (teste).
- [ ] Template com variável sem valor não é enviado (teste).
- [ ] Corpo de aviso de saúde não contém diagnóstico (varredura).
- [ ] Provedor com falha repetida sai do roteamento e o aviso segue pelo reserva (teste).
- [ ] Itens **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](../../../docs/v2/00-README.md).

### 13.2 [18](../../../docs/v2/18-regras-modulos-2.md), seção 3

#### 3. Notificações

##### 3.1 Estados (v1, seção 6, validada)

A v1 define: `draft`, `in_review`, `scheduled`, `queued`, `processing`, `sent`, `delivered`, `read`, `failed`, `archived`, `cancelled`.

As transições da v1 estão corretas e são adotadas. Regras adicionais:

| Regra | Detalhe |
|---|---|
| Estados terminais | `read`, `archived`, `cancelled` não voltam sem ação explícita autorizada. |
| Reenvio | Cria nova tentativa. Não sobrescreve a anterior. |
| Cancelamento | Preserva histórico e auditoria. |
| Falha | Classificada por tipo: validação, transporte, provedor, conteúdo, autorização, timeout ou desconhecida. Só transporte e timeout são retentados. |

##### 3.2 Validações de envio

- Campos obrigatórios por canal validados antes do envio: e-mail exige endereço verificado; SMS e WhatsApp exigem número em E.164 ([15](../../../docs/v2/15-validacoes.md), seção 2).
- Conteúdo sem público-alvo válido é bloqueado.
- Anexo validado por tamanho, tipo e política de segurança ([15](../../../docs/v2/15-validacoes.md), seção 4.3).
- Toda operação de envio é idempotente pela `idempotency_key`.
- Payload validado por schema. Campo obrigatório documentado por tipo de evento.

##### 3.3 Dados sensíveis

- Notificação de saúde ou de RH não mostra diagnóstico nem valor de salário no corpo. Mostra aviso e link autenticado.
- Corpo de mensagem guardado com retenção configurável ([07](../../../docs/v2/07-privacidade-lgpd.md)).

### 13.3 [75](../../../docs/v2/75-busca-notificacoes-perfil-integracoes-por-escopo.md), seção 3

#### 3. Notificações, por escopo

| Escopo | Situação | Onde |
|---|---|---|
| Plataforma (desenvolvedor) | Coberto: comunicado de manutenção e cobrança, por e-mail e in-app | [57](../../../docs/v2/57-notificacoes-por-portal.md), seção 4 |
| Entidade | Coberto: público da entidade, com aprovação acima de 500 | [57](../../../docs/v2/57-notificacoes-por-portal.md), seção 3.4 |
| Unidade | Coberto: público da unidade | [57](../../../docs/v2/57-notificacoes-por-portal.md), seção 3.4 |
| Turma | Coberto | [57](../../../docs/v2/57-notificacoes-por-portal.md), seção 3.4 |
| Módulo | Parcial. Os avisos de cada módulo estão nos docs de módulo, mas não há catálogo de avisos por módulo | [57](../../../docs/v2/57-notificacoes-por-portal.md), seção 4 |
| Global | Coberto pelas regras de canal e de silêncio | [57](../../../docs/v2/57-notificacoes-por-portal.md), seção 3.3 |

**Lacuna:** os avisos dos módulos novos (ocorrência, boletim, conselho, estágio, TCC, biblioteca, financeiro novo, censo) não estão no catálogo de eventos da [14](../../../docs/v2/14-integracao-modulos.md). Sem evento, a notificação não dispara. Ver seção 5.

## 14. Conteúdo integral da v1 (absorvido)

### Fonte: spec_gestao_notificacoes_revisada.md

#### Spec Funcional e Técnica — Gestão de Notificações

##### 1. Objetivo
A Gestão de Notificações centraliza a criação, segmentação, distribuição, acompanhamento e automação de notificações da plataforma multi-entity/multi-unit. O módulo deve suportar notificações operacionais, transacionais, informativas, críticas e automatizadas, com visão por entidade, unidade, canal, status, prioridade e origem do evento.

- Language Standard: Global English
##### 2. Princípios de Produto
- O módulo deve ser assíncrono por padrão.
- Toda notificação deve ser rastreável do evento de origem até o resultado final.
- O sistema deve ser seguro por padrão e configurável por escopo.
- A operação deve ser rápida, com baixa fricção para criação, revisão, envio e auditoria.
- O comportamento em falhas deve ser previsível, idempotente e observável.

##### 3. Escopo
O módulo cobre:
- Criação e disparo de notificações manuais e automáticas.
- Gestão de filas, agendamentos, regras, canais, templates e provedores.
- Monitoramento de entrega, leitura, falhas, retry e escalonamento.
- Organização em board Kanban por estágio operacional.
- Dashboards com widgets, métricas, alertas e gráficos analíticos.
- CRUD completo em drawers para operação rápida.
- Controles de segurança, auditoria, LGPD, governança e retenção.

##### 4. Perfis de Acesso
- Super Admin.
- Admin da Entidade.
- Gestor da Unidade.
- Operador.
- Auditor/Compliance.
- Usuário Final.

###### 4.1 Escopo de Permissão
O acesso deve considerar:
- Entidade.
- Unidade.
- Canal.
- Tipo de notificação.
- Ação permitida.
- Status do objeto.
- Sensibilidade do conteúdo.

###### 4.2 Regras Gerais de Acesso
- Toda ação sensível deve ser auditada.
- Usuário final só pode visualizar notificações permitidas ao seu contexto.
- Operador não pode alterar políticas globais sem permissão explícita.
- Auditor/Compliance deve ter acesso de leitura ampliado e sem poder de mutação.
- A API deve aplicar RBAC e, quando necessário, ABAC.

##### 5. Conceitos do Domínio
###### 5.1 Notification Event
Evento de domínio que dispara ou alimenta uma automação. Exemplo: novo cadastro, mudança de status, atraso, falha de processamento, mensagem recebida, tarefa pendente, aniversário, expiração.

###### 5.2 Notification Rule
Regra que associa eventos, condições e ações. Pode criar notificações, escalar, abrir tarefa, registrar log, acionar retry ou notificar em canal específico.

###### 5.3 Notification Template
Modelo parametrizado para título, assunto, corpo e variáveis por canal.

###### 5.4 Notification Instance
Registro concreto de uma notificação criada a partir de evento manual ou automático.

###### 5.5 Delivery Attempt
Tentativa individual de envio da notificação em um canal/provedor específico.

###### 5.6 Delivery Log
Registro técnico de processamento, bloqueio, envio, resposta do provedor, erro, retry e conclusão.

###### 5.7 Queue Item
Item enfileirado para processamento assíncrono com bloqueio, prioridade, agendamento e política de retry.

##### 6. Estados e Transições
###### 6.1 Estados Principais
- Draft.
- In Review.
- Scheduled.
- Queued.
- Processing.
- Sent.
- Delivered.
- Read.
- Failed.
- Archived.
- Cancelled.

###### 6.2 Transições Permitidas
- Draft -> In Review.
- In Review -> Scheduled.
- In Review -> Queued.
- Scheduled -> Queued.
- Queued -> Processing.
- Processing -> Sent.
- Sent -> Delivered.
- Delivered -> Read.
- Any active state -> Cancelled.
- Failed -> Queued quando houver retry válido.
- Any non-terminal state -> Archived quando permitido.

###### 6.3 Regras de Transição
- Transições inválidas devem ser rejeitadas com erro padronizado.
- Estados terminais não devem ser reabertos sem ação explícita autorizada.
- Cancelamento deve preservar histórico e auditoria.
- Reenvio deve criar nova tentativa sem sobrescrever evidências da tentativa anterior.

##### 7. Regras Gerais
- Toda notificação deve possuir entidade, unidade, tipo, canal, prioridade, status e responsável.
- O sistema deve permitir escopo global, por entidade, por unidade e por público segmentado.
- Notificações críticas devem exigir confirmação de leitura quando aplicável.
- Notificações com falha devem entrar em fila de retry com política configurável.
- Toda alteração relevante deve ser registrada em auditoria.
- Campos sensíveis devem respeitar LGPD, mascaramento e retenção configurável.
- Toda operação de envio deve ser idempotente.
- Toda entrega deve ser observável de ponta a ponta.

##### 8. Contratos de Evento
###### 8.1 Identificação do Evento
Cada evento deve possuir:
- event_name.
- event_version.
- event_id.
- source.
- occurred_at.
- entity_id.
- unit_id.
- actor_id.
- correlation_id.
- causation_id.
- payload.

###### 8.2 Versionamento
- Todo evento deve ter versão explícita.
- Alterações incompatíveis exigem nova versão.
- Consumidores devem suportar coexistência de versões por período de migração.

###### 8.3 Schema de Payload
- O payload deve ser validado por schema.
- Campos obrigatórios devem ser documentados por tipo de evento.
- Campos opcionais devem ter comportamento de fallback definido.
- O schema deve ser versionado junto ao evento.

###### 8.4 Convenção de Nomes
Exemplos:
- student.created.
- enrollment.status_changed.
- payment.overdue.
- message.received.
- task.assigned.
- automation.rule_triggered.

##### 9. Idempotência e Deduplicação
- Toda requisição de criação, disparo ou reprocessamento deve aceitar uma idempotency_key.
- Se a mesma chave for reapresentada, o sistema deve retornar o resultado anterior sem criar duplicidade.
- O worker deve deduplicar por combinação de event_id, notification_template_id e target context quando aplicável.
- Em reprocessamento, a tentativa anterior deve permanecer preservada como evidência.
- A deduplicação deve respeitar janela configurável por tipo de evento e canal.

##### 10. Retry, Backoff e Reprocessamento
- O sistema deve suportar retry configurável por notificação, canal e provedor.
- O backoff deve suportar estratégia fixa, exponencial ou híbrida.
- Deve existir limite máximo de tentativas por política.
- O retry deve respeitar janelas de silêncio, rate limits e prioridade.
- Falhas permanentes devem ser classificadas por tipo: validação, transporte, provedor, conteúdo, autorização, timeout ou desconhecida.

###### 10.1 Política de Retry
Campos mínimos:
- retry_policy_id.
- max_attempts.
- initial_delay_seconds.
- backoff_strategy.
- max_delay_seconds.
- jitter_enabled.
- active.

##### 11. Entidades Principais
###### 11.1 Notification
Campos mínimos:
- id.
- uuid.
- entity_id.
- unit_id.
- event_id.
- title.
- subject.
- message.
- type.
- category.
- priority.
- channel.
- target_audience.
- sender_type.
- sender_id.
- status.
- scheduled_at.
- queued_at.
- processing_at.
- sent_at.
- delivered_at.
- read_at.
- failed_at.
- expires_at.
- cancelled_at.
- retry_count.
- max_retries.
- idempotency_key.
- correlation_id.
- metadata.
- created_by.
- updated_by.
- created_at.
- updated_at.
- deleted_at.

###### 11.2 Notification Template
- id.
- uuid.
- entity_id.
- unit_id.
- name.
- code.
- channel.
- subject_template.
- body_template.
- variables_schema.
- locale.
- active.
- version.
- created_at.
- updated_at.

###### 11.3 Notification Rule / Automation
- id.
- uuid.
- entity_id.
- unit_id.
- name.
- trigger_event.
- trigger_version.
- conditions.
- actions.
- cooldown.
- priority.
- active.
- version.
- created_at.
- updated_at.

###### 11.4 Notification Delivery Log
- id.
- notification_id.
- channel.
- provider.
- recipient.
- status.
- response_code.
- response_payload.
- attempt.
- sent_at.
- delivered_at.
- read_at.
- locked_at.
- worker_id.
- error_type.
- error_message.
- created_at.

###### 11.5 Notification Queue
- id.
- notification_id.
- scheduled_at.
- processed_at.
- locked_at.
- lock_expires_at.
- worker_id.
- status.
- retry_count.
- priority.
- partition_key.
- created_at.
- updated_at.

###### 11.6 Notification Subscription
- id.
- uuid.
- entity_id.
- unit_id.
- user_id.
- channel.
- topic.
- consent_status.
- opt_in_at.
- opt_out_at.
- source.
- created_at.
- updated_at.

###### 11.7 Notification Provider
- id.
- uuid.
- name.
- code.
- channel.
- endpoint.
- credentials_ref.
- active.
- rate_limit.
- health_status.
- last_checked_at.
- created_at.
- updated_at.

##### 12. Validações de Dados
- Campos obrigatórios por canal devem ser validados antes do envio.
- Limites de caracteres por canal devem ser respeitados.
- Variáveis do template devem ser resolvidas antes do envio.
- Conteúdo sem público-alvo válido deve ser bloqueado.
- Anexos devem ser validados por tamanho, tipo e política de segurança.
- Conteúdo sensível deve ser mascarado quando aplicável.
- Datas devem respeitar timezone da entidade/unidade e timezone do usuário quando relevante.

##### 13. Canais e Provedores
###### 13.1 Canais Suportados
- In-app.
- Email.
- SMS.
- Push.
- WhatsApp, quando habilitado.
- Webhook interno, quando necessário.

###### 13.2 Regras por Canal
- In-app pode ser padrão para avisos internos.
- Email e SMS exigem validações adicionais de entrega e opt-in conforme política.
- Push depende de dispositivo/token válido.
- WhatsApp depende de provedor e template compatível.
- Webhook deve assinar a requisição e validar assinatura na recepção, quando aplicável.

###### 13.3 Gestão de Provedores
- Cada canal pode ter múltiplos provedores.
- Deve existir health check por provedor.
- Deve existir fallback configurável entre provedores do mesmo canal.
- Falhas repetidas devem desativar o roteamento automático para o provedor com health crítico.

##### 14. Fluxos Principais
###### 14.1 Fluxo Manual
1. Usuário cria notificação.
2. Define público, canal e conteúdo.
3. Sistema valida regras e permissões.
4. Notificação entra em fila ou é enviada imediatamente.
5. Logs, métricas e auditoria são atualizados.

###### 14.2 Fluxo Automático
1. Evento dispara automação.
2. Motor avalia condições e versão da regra.
3. Sistema gera notificação baseada em template.
4. Envio ocorre pelo canal definido.
5. Status, logs e auditoria são persistidos.

###### 14.3 Fluxo de Falha
1. Provider retorna erro ou timeout.
2. Sistema registra falha categorizada.
3. Retry é agendado conforme política.
4. Se exceder o limite, status vira falhou definitivo.
5. Caso crítico, abrir alerta interno e opcionalmente escalar.

###### 14.4 Fluxo de Cancelamento
1. Usuário autorizado solicita cancelamento.
2. Sistema valida se o estado permite cancelamento.
3. Itens ainda não processados são retirados da fila quando possível.
4. Logs preservam histórico da tentativa de cancelamento.
5. Auditoria registra autor, motivo e horário.

##### 15. Observabilidade
###### 15.1 Logs
- Todo processamento deve gerar logs estruturados.
- Logs devem incluir correlation_id, event_id, notification_id, provider e worker_id.
- Dados sensíveis devem ser redigidos.

###### 15.2 Métricas
- Total por período.
- Enviadas hoje.
- Pendentes na fila.
- Taxa de entrega.
- Taxa de leitura.
- Falhas últimas 24h.
- Retries em andamento.
- Tempo médio até envio.
- Tempo médio até entrega.
- Falhas por provedor.
- SLA cumprido versus violado.

###### 15.3 Tracing
- O tracing deve permitir acompanhar evento -> regra -> fila -> worker -> provedor -> resultado.
- O correlation_id deve ser propagado em toda a cadeia.

###### 15.4 Alertas
- Falha elevada por provedor.
- Crescimento anormal da fila.
- Aumento de retry.
- SLA violado.
- Worker parado ou sem heartbeat.
- Taxa de erro acima do limiar por canal.

##### 16. Segurança e Compliance
- Mascaramento de dados sensíveis.
- Criptografia em repouso e em trânsito.
- Controle de acesso por perfil e escopo.
- Consentimento e base legal quando aplicável.
- Direito de exclusão/anonimização conforme LGPD.
- Registros de acesso e alteração.
- Bloqueio de canais não autorizados.
- Rotação de segredos e credenciais.
- Segredos devem ser armazenados fora do código-fonte.
- Logs não devem expor tokens, documentos pessoais ou payload sensível completo.
- Anexos devem ser validados contra malware quando aplicável.

##### 17. Requisitos Não Funcionais
- Escalabilidade horizontal.
- Baixa latência na fila.
- Processamento assíncrono.
- Alta disponibilidade.
- Tolerância a falhas de provedor.
- Reprocessamento controlado.
- Compatibilidade com multi-entity e multi-unit.
- Auditoria completa com retenção configurável.
- Suporte a internacionalização, fuso horário e formatos locais.
- Backpressure sob carga elevada.
- Deploy sem downtime sempre que possível.

##### 18. Arquitetura de Execução
###### 18.1 Componentes
- API de gestão.
- API de automação.
- Worker de fila.
- Scheduler.
- Provider adapters.
- Rules engine.
- Audit logger.
- Metrics exporter.

###### 18.2 Separação de Responsabilidades
- A API valida e persiste intenções.
- O worker processa envio e retry.
- O scheduler dispara agendamentos.
- O rules engine avalia eventos e condições.
- Os adapters encapsulam integrações externas.

###### 18.3 Backpressure
- Quando a fila exceder limite, o sistema deve priorizar notificações críticas.
- Notificações de baixa prioridade podem ser adiadas conforme política.
- O sistema deve registrar saturação e acionar alerta operacional.

##### 19. API Suggested
###### 19.1 Endpoints Principais
- GET /notifications
- POST /notifications
- GET /notifications/{id}
- PUT /notifications/{id}
- DELETE /notifications/{id}
- POST /notifications/{id}/resend
- POST /notifications/{id}/cancel
- POST /notifications/{id}/mark-read
- GET /notification-templates
- POST /notification-templates
- GET /notification-rules
- POST /notification-rules
- GET /notification-queue
- GET /notification-logs
- GET /notification-dashboard
- GET /notification-subscriptions
- POST /notification-subscriptions
- GET /notification-providers
- POST /notification-providers

###### 19.2 Padrões de API
- Paginação server-side.
- Filtros normalizados.
- Erros padronizados.
- IDs UUID.
- Auditoria automática.
- Suporte a idempotency-key.
- Suporte a correlation-id.
- Respostas consistentes por endpoint.

###### 19.3 Erros Padronizados
- invalid_payload.
- unauthorized.
- forbidden.
- not_found.
- conflict.
- rate_limited.
- provider_unavailable.
- template_validation_failed.
- duplicate_request.
- retry_exhausted.

###### 19.4 Exemplo de Resposta
```json
{
  "success": false,
  "error": {
    "code": "template_validation_failed",
    "message": "Variável required_name ausente.",
    "details": {
      "field": "required_name"
    }
  },
  "correlation_id": "c-123"
}
```

##### 20. Modelos de Payload
###### 20.1 Evento de Exemplo
```json
{
  "event_name": "student.created",
  "event_version": "1.0",
  "event_id": "evt_01",
  "source": "core-school",
  "occurred_at": "2026-07-02T20:00:00-03:00",
  "entity_id": 10,
  "unit_id": 3,
  "actor_id": 99,
  "correlation_id": "cor_001",
  "causation_id": "cause_001",
  "payload": {
    "student_id": 123,
    "name": "Aluno Exemplo"
  }
}
```

###### 20.2 Criação de Notificação
```json
{
  "title": "Novo aluno cadastrado",
  "subject": "Aluno criado com sucesso",
  "message": "O aluno {{name}} foi cadastrado.",
  "type": "informational",
  "category": "academic",
  "priority": "normal",
  "channel": ["in_app", "email"],
  "target_audience": {
    "role": ["admin", "manager"]
  },
  "scheduled_at": null,
  "idempotency_key": "idem_001",
  "metadata": {
    "event_name": "student.created"
  }
}
```

###### 20.3 Regra de Automação
```json
{
  "name": "Boas-vindas novo aluno",
  "trigger_event": "student.created",
  "trigger_version": "1.0",
  "conditions": [
    { "field": "unit_id", "operator": "in", "value": [3, 4] }
  ],
  "actions": [
    { "type": "create_notification", "template_code": "student_welcome" }
  ],
  "cooldown": 300,
  "priority": 50,
  "active": true,
  "version": 1
}
```

##### 21. Testabilidade
###### 21.1 Tipos de Teste
- Testes unitários de validação, template e regra.
- Testes de integração com API, fila e banco.
- Testes de contrato para eventos e payloads.
- Testes de ponta a ponta para fluxos críticos.
- Testes de carga para fila, worker e dashboard.
- Testes de falha com provedor indisponível.
- Testes de segurança para autenticação, autorização e mascaramento.

###### 21.2 Cenários Mínimos
- Criar notificação manual.
- Agendar notificação.
- Disparar automação por evento.
- Validar template com variável ausente.
- Processar retry.
- Cancelar agendamento.
- Marcar como lida.
- Falha de provedor com fallback.
- Rate limit excedido.
- Idempotency key duplicada.

###### 21.3 Ambiente de Homologação
- Deve existir sandbox para provedores.
- Deve existir mock para envio e leitura.
- Deve existir dataset de teste com múltiplas entidades e unidades.
- Deve existir modo seguro para simular automações sem envio real.

##### 22. Critérios de Aceite
- Criar, editar, agendar, reenviar, cancelar, marcar como lida e arquivar notificações.
- Visualizar notificações em tabela, cards e Kanban.
- Operar automações baseadas em eventos com versionamento.
- Monitorar entrega, leitura, erro, retry e SLA.
- Gerenciar templates, regras, canais, provedores e permissões.
- Exibir dashboards com widgets e charts atualizados.
- Registrar auditoria e obedecer políticas de segurança e LGPD.
- Processar eventos de forma idempotente e observável.
- Suportar falha de provedor com retry e fallback.

##### 23. Componentes Frontend
- NotificationDashboard.
- NotificationDatatable.
- NotificationDrawerForm.
- NotificationKanbanBoard.
- NotificationWidgets.
- NotificationCharts.
- NotificationAutomationBuilder.
- NotificationTemplateManager.
- NotificationDeliveryLogTable.
- NotificationSettingsPanel.
- NotificationSubscriptionPanel.
- NotificationProviderPanel.

##### 24. Layout UI Recomendado
- Topbar com busca global, filtros rápidos e ações primárias.
- Sidebar com Dashboard, Lista, Kanban, Automação, Templates, Logs, Provedores e Configurações.
- Área central com cards, datatable e gráficos.
- Drawers laterais para CRUD rápido.
- Modal apenas para confirmações críticas.
- Estado de carregamento, vazio, erro e parcial devem ser tratados explicitamente.

##### 25. Prioridades de Implementação
###### Fase 1
- Lista, drawer CRUD, detalhes, dashboard básico, templates e logs.

###### Fase 2
- Kanban, automações, retry, alertas, provedores e métricas avançadas.

###### Fase 3
- SLA, auditoria ampliada, fallback multi-provedor, integrações externas e observabilidade avançada.

##### 26. Observações Finais
O módulo deve ser projetado para operação intensiva, com foco em governança, produtividade, rastreabilidade e resiliência. A interface precisa permitir navegação rápida entre visão analítica, ação operacional e configuração administrativa, sem perder consistência entre entidade e unidade. O comportamento técnico deve permanecer previsível sob falha, carga elevada e mudanças de versão.

### Fonte: spec_gestao_notificacoes.md

#### Spec Funcional e Técnica — Gestão de Notificações

- Language Standard: Global English
##### 1. Objetivo
A Gestão de Notificações centraliza a criação, segmentação, distribuição, acompanhamento e automação de notificações da plataforma multi-entity/multi-unit. O módulo deve suportar notificações operacionais, transacionais, informativas, críticas e automatizadas, com visão por entidade, unidade, canal, status e prioridade.

##### 2. Escopo
O módulo cobre:
- Criação e disparo de notificações manuais e automáticas.
- Gestão de filas, agendamentos, regras, canais e templates.
- Monitoramento de entrega, leitura, falhas e retry.
- Organização em board Kanban por estágio operacional.
- Dashboards com widgets e gráficos analíticos.
- CRUD completo em drawers para operação rápida.
- Controles de segurança, auditoria, LGPD e governança.

##### 3. Perfis de Acesso
- Super Admin.
- Admin da Entidade.
- Gestor da Unidade.
- Operador.
- Auditor/Compliance.
- Usuário Final.

##### 4. Regras Gerais
- Toda notificação deve possuir entidade, unidade, tipo, canal, prioridade, status e responsável.
- O sistema deve permitir escopo global, por entidade, por unidade e por público segmentado.
- Notificações críticas devem exigir confirmação de leitura quando aplicável.
- Notificações com falha devem entrar em fila de retry com política configurável.
- Toda alteração relevante deve ser registrada em auditoria.
- Campos sensíveis devem respeitar LGPD, mascaramento e retenção configurável.

##### 5. Entidades Principais
###### 5.1 Notification
Campos mínimos:
- id
- uuid
- entity_id
- unit_id
- title
- subject
- message
- type
- category
- priority
- channel
- target_audience
- sender_type
- sender_id
- status
- scheduled_at
- sent_at
- delivered_at
- read_at
- failed_at
- expires_at
- retry_count
- max_retries
- metadata
- created_by
- updated_by
- created_at
- updated_at
- deleted_at

###### 5.2 Notification Template
- id, uuid, entity_id, unit_id, name, code, channel, subject_template, body_template, variables_schema, active, created_at, updated_at.

###### 5.3 Notification Rule / Automation
- id, uuid, entity_id, unit_id, name, trigger_event, conditions, actions, cooldown, active, priority, created_at, updated_at.

###### 5.4 Notification Delivery Log
- id, notification_id, channel, provider, recipient, status, response_code, response_payload, attempt, sent_at, delivered_at, read_at, error_message.

###### 5.5 Notification Queue
- id, notification_id, scheduled_at, processed_at, locked_at, worker_id, status, retry_count.

##### 6. Páginas do Módulo
###### 6.1 Dashboard Geral
Objetivo: mostrar visão executiva das notificações.
Controles obrigatórios:
- Filtro por período.
- Filtro por entidade.
- Filtro por unidade.
- Filtro por canal.
- Filtro por prioridade.
- Filtro por status.
- Busca global.
- Exportação CSV/PDF.

Widgets obrigatórios:
- Total de notificações.
- Enviadas hoje.
- Pendentes na fila.
- Taxa de entrega.
- Taxa de leitura.
- Falhas últimas 24h.
- Retries em andamento.
- Notificações críticas.

Charts obrigatórios:
- Linha: volume por dia.
- Barra: notificações por status.
- Pizza ou donut: distribuição por canal.
- Barras empilhadas: sucesso vs falha por canal.
- Heatmap: volume por hora/dia.

###### 6.2 Lista de Notificações
Componente principal: datatable avançada.
Colunas:
- seleção.
- título.
- tipo.
- canal.
- prioridade.
- entidade.
- unidade.
- status.
- agendada para.
- enviada em.
- leitura.
- tentativas.
- responsável.
- ações.

Controles da datatable:
- pesquisa textual.
- filtros avançados.
- ordenação por coluna.
- paginação server-side.
- seleção múltipla.
- ações em lote.
- colunas configuráveis.
- densidade de visualização.
- salvar filtros favoritos.
- exportar lista.
- atualizar em tempo real.

Ações por linha:
- visualizar.
- editar.
- duplicar.
- reenviar.
- cancelar.
- marcar como lida.
- arquivar.
- excluir lógico.

###### 6.3 Criação e Edição
Formato: drawer lateral com etapas.
Seções obrigatórias:
- Dados básicos.
- Público-alvo.
- Conteúdo.
- Canal.
- Agendamento.
- Regras e automações.
- Revisão final.

Campos obrigatórios:
- título.
- assunto.
- mensagem.
- canal.
- prioridade.
- entidades/unidades de destino.
- tipo de disparo.
- data e hora agendada, se aplicável.
- template.
- anexos, se suportado.
- confirmação de leitura.
- expiração.

Validações:
- campos obrigatórios por canal.
- limite de caracteres por canal.
- preview de variáveis do template.
- bloqueio de envio sem público válido.

###### 6.4 Detalhe da Notificação
Conteúdo da página:
- resumo geral.
- timeline de eventos.
- histórico de entrega.
- destinatários.
- respostas e interações.
- logs técnicos.
- auditoria completa.
- dados de automação relacionada.

Ações:
- reenviar.
- cancelar agendamento.
- editar rascunho.
- gerar cópia.
- abrir incidente se falha crítica.

###### 6.5 Kanban Operacional
Colunas recomendadas:
- Rascunho.
- Em revisão.
- Agendada.
- Processando.
- Enviada.
- Entregue.
- Lida.
- Falhou.
- Arquivada.

Controles do Kanban:
- drag and drop.
- filtros por responsável, canal e prioridade.
- cards compactos e expandíveis.
- badges de status.
- contadores por coluna.
- ações rápidas no card.
- WIP limit por coluna.

###### 6.6 Automações
Página dedicada para regras automáticas.
Funcionalidades:
- criar automação.
- testar regra.
- simular disparo.
- habilitar/desabilitar.
- versionar regra.
- visualizar dependências.

Tipos de gatilhos:
- evento de cadastro.
- mudança de status.
- atraso.
- falha de processamento.
- aniversário.
- expiração.
- tarefa pendente.

Ações suportadas:
- criar notificação.
- notificar por canal específico.
- escalar para superior.
- abrir tarefa.
- registrar log.
- enviar para fila de retry.

###### 6.7 Controles e Governança
Página de configuração global.
Seções:
- canais habilitados.
- provedores externos.
- templates.
- limites de envio.
- rate limit.
- janelas de silêncio.
- política de retry.
- retenção de logs.
- assinatura e branding.
- permissões por perfil.
- políticas LGPD.
- trilha de auditoria.

##### 7. Widgets do Painel
Widgets mínimos obrigatórios:
- cards KPI com tendência.
- gráfico de leitura por canal.
- falhas por provedor.
- fila por prioridade.
- notificações críticas pendentes.
- tempo médio de entrega.
- SLA cumprido vs violado.
- atividade recente.

##### 8. Fluxos Principais
###### 8.1 Fluxo Manual
1. Usuário cria notificação.
2. Define público, canal e conteúdo.
3. Sistema valida regras.
4. Notificação entra em fila ou é enviada imediatamente.
5. Logs e métricas são atualizados.

###### 8.2 Fluxo Automático
1. Evento dispara automação.
2. Motor avalia condições.
3. Sistema gera notificação baseada em template.
4. Envio ocorre pelo canal definido.
5. Status e auditoria são persistidos.

###### 8.3 Fluxo de Falha
1. Provider retorna erro.
2. Sistema registra falha.
3. Retry é agendado conforme política.
4. Se exceder o limite, status vira falhou definitivo.
5. Caso crítico, abrir alerta interno.

##### 9. Requisitos Não Funcionais
- Escalabilidade horizontal.
- Baixa latência na fila.
- Processamento assíncrono.
- Observabilidade com logs, métricas e tracing.
- Segurança por JWT, CSRF, rate limiting e RBAC.
- Compatibilidade com multi-entity e multi-unit.
- Auditoria completa com retenção configurável.
- Suporte a internacionalização, fuso horário e formatos locais.

##### 10. Segurança e Compliance
- Mascaramento de dados sensíveis.
- Criptografia em repouso e em trânsito.
- Controle de acesso por perfil e escopo.
- Consentimento e base legal quando aplicável.
- Direito de exclusão/anonimização conforme LGPD.
- Registros de acesso e alteração.
- Bloqueio de canais não autorizados.

##### 11. API Suggested
###### Endpoints principais
- GET /notifications
- POST /notifications
- GET /notifications/{id}
- PUT /notifications/{id}
- DELETE /notifications/{id}
- POST /notifications/{id}/resend
- POST /notifications/{id}/cancel
- POST /notifications/{id}/mark-read
- GET /notification-templates
- POST /notification-templates
- GET /notification-rules
- POST /notification-rules
- GET /notification-queue
- GET /notification-logs
- GET /notification-dashboard

###### Padrões de resposta
- Paginação server-side.
- Filtros normalizados.
- Erros padronizados.
- IDs UUID.
- Auditoria automática.

##### 12. Layout UI Recomendado
- Topbar com busca global, filtros rápidos e ações primárias.
- Sidebar com Dashboard, Lista, Kanban, Automação, Templates, Logs e Configurações.
- Área central com cards, datatable e gráficos.
- Drawers laterais para CRUD rápido.
- Modal apenas para confirmações críticas.

##### 13. Critérios de Aceite
- Criar, editar, agendar, reenviar, cancelar e arquivar notificações.
- Visualizar notificações em tabela, cards e Kanban.
- Operar automações baseadas em eventos.
- Monitorar entrega, leitura, erro e retry.
- Gerenciar templates, regras, canais e permissões.
- Exibir dashboards com widgets e charts atualizados.
- Registrar auditoria e obedecer políticas de segurança e LGPD.

##### 14. Componentes Frontend
- NotificationDashboard
- NotificationDatatable
- NotificationDrawerForm
- NotificationKanbanBoard
- NotificationWidgets
- NotificationCharts
- NotificationAutomationBuilder
- NotificationTemplateManager
- NotificationDeliveryLogTable
- NotificationSettingsPanel

##### 15. Prioridades de Implementação
###### Fase 1
- Lista, drawer CRUD, detalhes, dashboard básico.

###### Fase 2
- Kanban, automações, templates, logs e alertas.

###### Fase 3
- métricas avançadas, SLA, auditoria ampliada, integrações externas.

##### 16. Observações Finais
O módulo deve ser projetado para operação intensiva, com foco em governança, produtividade e rastreabilidade. A interface precisa permitir navegação rápida entre visão analítica, ação operacional e configuração administrativa, sem perder consistência entre entidade e unidade.
