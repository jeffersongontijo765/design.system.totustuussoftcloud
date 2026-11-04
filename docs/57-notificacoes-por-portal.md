# 57 — Notificações, por Portal

> Parte do [SDD v2](00-README.md). Eventos que disparam notificação em [14](14-integracao-modulos.md). Canais e provedores de plataforma em [16](16-integracoes-externas.md). Verificação de contato e MFA em [06](06-identidade-acesso.md). Consentimento por canal em [26](26-sdd-juridico-regulatorio.md) e [22](22-crm-canais-e-papeis.md). Regras de envio, estados e dados sensíveis em [18](18-regras-modulos-2.md), seção 3. Auditoria em [29](29-auditoria.md). Idioma em [09](09-internacionalizacao.md). Referência de módulo: `spec_gestao_notificacoes_revisada.md` (v1, 642 linhas) unida a `spec_gestao_notificacoes.md` (v1, 378 linhas), por decisão NOT-01.
> **Veredito:** o módulo de notificações **não está completo como módulo**. Há regras soltas para estados, validação, canais de conta e dado sensível. Falta o módulo em si: templates, regras de envio, preferências do usuário, targeting por portal, fallback entre provedores e painel de operação.

---

## 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| Existe especificação de notificações na v2? | **Não.** O catálogo marca "Revisar", com duas versões na v1 |
| Estados e transições estão definidos? | **Sim**, herdados da v1 revisada e validados em [18](18-regras-modulos-2.md), seção 3.1 |
| Canais estão definidos? | **Parcial.** E-mail e SMS aparecem em [16](16-integracoes-externas.md). WhatsApp, Telegram e chat, em [22](22-crm-canais-e-papeis.md). Push e in-app não aparecem na v2 |
| Preferências do usuário? | **Não.** Só consentimento por finalidade em [32](32-atendimento-privacidade-por-portal.md), seção 3.2 |
| Targeting: quem envia a quem? | **Não.** A v1 lista avisos por portal, mas não diz quem pode enviar para quem |
| Templates e variáveis? | **Não** na v2. A v1 revisada tem o conceito, sem regra de idioma nem de conteúdo |
| Fallback e saúde de provedor? | **Não** na v2. A v1 revisada tem a regra |
| Dado sensível no corpo? | **Sim**, em [18](18-regras-modulos-2.md), seção 3.3 |
| Painel de operação e métricas? | **Não** na v2. A v1 tem, em detalhe |

---

## 2. Lacunas

1. **Módulo sem documento próprio.** As regras estão em cinco docs diferentes. Não há ponto único de consulta.
2. **Canal push e in-app ausentes.** A v1 lista ambos. Sem eles, avisos de aplicativo não têm caminho.
3. **Preferências do usuário ausentes.** Sem tela de preferência, o responsável não escolhe canal, horário ou tipo de aviso.
4. **Horário de silêncio ausente.** Mensagem às 23h para responsável não tem regra.
5. **Targeting ausente.** Não há regra para "todas as famílias da turma X", "responsáveis com dependente com vínculo ativo", "professores da unidade". Sem isso, o envio em massa fica sem controle.
6. **Templates e i18n ausentes.** Texto de aviso precisa de versão por idioma ([09](09-internacionalizacao.md)) e de variáveis validadas.
7. **Fallback entre provedores ausente.** [16](16-integracoes-externas.md) define um provedor por tipo. A v1 prevê vários por canal e troca automática quando um cai.
8. **Painel de operação ausente.** Fila, falhas, reenvio e métricas de entrega não têm tela nem métrica definida. [24](24-operacao-continuidade-qualidade.md) tem só uma meta ("99% em até 5 min"). **Escrito** nas seções 3.8 e 3.9 (NOT-08).
9. **Conflito de versões da v1.** Há `spec_gestao_notificacoes.md` (378 linhas) e a revisada (642 linhas). **Decidido** em 03/11/2026 (NOT-01): as duas são unidas. A revisada dá estados, eventos, reenvio e observabilidade. A original dá as telas e o painel (seções 3.8 e 3.9).
10. **Notificação de saúde.** [18](18-regras-modulos-2.md), seção 3.3, proíbe diagnóstico no corpo. Não há regra de quem pode enviar aviso de saúde, nem para quem.

---

## 3. Modelo proposto

### 3.1 Canais

| Canal | Uso | Dono do envio | Regra |
|---|---|---|---|
| In-app | Avisos internos e de portal | Plataforma | Padrão para aviso que não é urgente |
| E-mail | Verificação, recuperação, comunicado formal | Plataforma (verificação) e entidade (comunicado) | Endereço verificado ([06](06-identidade-acesso.md), D-04). Link de descadastro em marketing ([26](26-sdd-juridico-regulatorio.md)) |
| Push | Aviso de aplicativo, Android e iOS | Plataforma | Depende do aplicativo e de token de dispositivo válido. Decidido pelo autor em 03/11/2026 |
| SMS | Aviso não crítico e opcional | Entidade | Não é fator de MFA ([16](16-integracoes-externas.md)). Desligado por padrão |
| WhatsApp | Aviso com opt-in | Entidade | Opt-in registrado ([22](22-crm-canais-e-papeis.md)). Template aprovado pelo provedor |
| Webhook | Integração com sistema da entidade | Entidade | Assinatura validada na recepção |

### 3.2 Estados

Herdados da v1 revisada e validados em [18](18-regras-modulos-2.md), seção 3.1: `draft`, `in_review`, `scheduled`, `queued`, `processing`, `sent`, `delivered`, `read`, `failed`, `archived`, `cancelled`.

Regra adicional: `read` nunca é gravado pelo envio. É gravado só quando o destinatário abre o aviso.

### 3.3 Preferências do usuário

- Cada pessoa escolhe canal por tipo de aviso: acadêmico, financeiro, comunicado geral.
- Aviso obrigatório não pode ser desligado: verificação, recuperação de conta, MFA, aviso de saúde e comunicado de segurança.
- Horário de silêncio por pessoa, com exceção para aviso obrigatório. Decidido pelo autor em 03/11/2026: 21h às 7h.
- Opt-out de marketing vale em todos os canais ([22](22-crm-canais-e-papeis.md), palavras `PARAR` e `SAIR`).

### 3.4 Targeting

Envio só para um público definido por regra, nunca para lista aberta:

| Público | Regra | Quem pode definir |
|---|---|---|
| Turma | Alunos com matrícula ativa na turma | Professor da turma, coordenação |
| Responsáveis de uma turma | Responsáveis com vínculo ativo a alunos da turma | Coordenação, secretaria |
| Unidade | Todos com vínculo ativo na unidade | Gestão da unidade |
| Entidade | Todos com vínculo ativo na entidade | Direção da entidade. Não pode ser professor |
| Plataforma | Clientes ou equipe da empresa | Equipe da empresa desenvolvedora |

Público com mais de 500 destinatários exige aprovação de segunda pessoa, como em [48](48-gerador-de-documentos-por-portal.md), seção 12. Decidido pelo autor em 03/11/2026.

### 3.5 Templates

- Template tem versão, idioma, variáveis validadas e categoria (acadêmico, financeiro, pastoral, segurança).
- Variável sem valor bloqueia o envio.
- Template de WhatsApp precisa ser aprovado pelo provedor antes de uso.
- Notificação de saúde ou de RH não tem diagnóstico nem salário no corpo ([18](18-regras-modulos-2.md), seção 3.3). Mostra aviso e link autenticado.

### 3.6 Provedores e fallback

- Cada canal pode ter mais de um provedor. Um é primário, e os outros são reserva.
- Health check por provedor. Falhas repetidas tiram o provedor do roteamento automático.
- Troca de provedor é registrada em auditoria.

### 3.7 Retenção

- Corpo da mensagem: prazo configurável por entidade, com padrão a definir **(jurídico)**.
- Registro de entrega (quem, quando, canal, estado): mesmo prazo de log de integração, 90 dias ([49](49-logs-testes-por-portal.md), seção 2).
- Auditoria de envio: prazo de evento de plataforma ([29](29-auditoria.md)).

### 3.8 Telas do módulo

Vêm da versão original da v1 (`spec_gestao_notificacoes.md`, seção 6), unida à revisada por decisão NOT-01. A regra da v2 prevalece quando há conflito: estados de [18](18-regras-modulos-2.md), seção 3.1, aprovação acima de 500 destinatários (NOT-03), silêncio (NOT-02) e permissão por papel.

| Tela | Conteúdo | Regra da v2 |
|---|---|---|
| Painel | Indicadores e gráficos da seção 3.9, com filtro por período, unidade, canal, prioridade e estado | Mostra só o escopo do papel: entidade, unidade ou turma |
| Lista | Tabela com título, tipo, canal, prioridade, unidade, estado, agendada para, enviada em, leitura, tentativas e responsável. Filtros salvos, paginação no servidor, seleção múltipla e exportação | Ação em lote respeita a transição permitida de cada item. Exportação segue a permissão e mascara dado pessoal |
| Criação e edição | Etapas: dados básicos, público, conteúdo, canal, agendamento, regras e revisão final. Prévia das variáveis do template | Sem público válido, não envia. Limite de caracteres por canal. Público acima de 500 vai para aprovação de segunda pessoa |
| Detalhe | Resumo, linha do tempo, entregas por destinatário, interações, log técnico e auditoria | Log técnico só para quem tem papel de operação. Conteúdo de aviso de saúde segue NOT-05 |
| Quadro (kanban) | Colunas por estado: rascunho, em revisão, agendada, processando, enviada, entregue, lida, falhou, arquivada | Arrastar o cartão só faz transição permitida. Estados de entrega (`delivered`, `read`, `failed`) vêm do provedor, não da mão do usuário |
| Automações | Criar, testar, simular, ativar e desativar regra, com versão. Gatilhos: cadastro, mudança de estado, atraso, falha, aniversário, expiração e tarefa pendente | Regra só dispara a partir de evento do catálogo de [14](14-integracao-modulos.md), seção 4. Simulação não envia mensagem |
| Configuração | Canais, provedores, templates, limites de envio, silêncio, política de reenvio, retenção, identidade visual e permissões | Provedor e credencial seguem [16](16-integracoes-externas.md). Retenção segue a seção 3.7 |

Ações por item: ver, editar rascunho, duplicar, reenviar, cancelar agendamento, arquivar e excluir (exclusão lógica). Reenvio de item já entregue pede motivo e fica na auditoria.

### 3.9 Painel, métricas e alertas

União das métricas das duas versões da v1 (original, seção 7; revisada, seção 15). Fecha NOT-08.

| Métrica | Quem vê |
|---|---|
| Total por período, enviadas hoje, pendentes na fila | Gestão e secretaria, no escopo do papel |
| Taxa de entrega e de leitura, por canal | Gestão e secretaria, no escopo do papel |
| Falhas nas últimas 24 horas e reenvios em andamento | Gestão e operação da plataforma |
| Tempo médio até o envio e até a entrega | Operação da plataforma |
| Falhas por provedor e fila por prioridade | Operação da plataforma |
| Prazo cumprido e violado (meta de [24](24-operacao-continuidade-qualidade.md): 99% em até 5 minutos) | Gestão e operação da plataforma |
| Avisos críticos pendentes | Gestão, no escopo do papel |

Gráficos: volume por dia, itens por estado, distribuição por canal, sucesso e falha por canal, e volume por hora e dia da semana.

**Portal do desenvolvedor:** vê só métricas agregadas de operação, sem título, corpo ou destinatário de mensagem de cliente ([31](31-matriz-portais-modulos.md)).

**Alertas para a operação:** falha elevada por provedor, crescimento anormal da fila, aumento de reenvio, prazo violado, worker sem sinal de vida e taxa de erro acima do limite por canal. Os limites são medidos em homologação.

**Rastreio:** o `correlation_id` acompanha evento, regra, fila, worker, provedor e resultado. Log estruturado com dado sensível redigido ([49](49-logs-testes-por-portal.md), seção 3).

---

## 4. Por portal

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
- Notificação de entrada e saída (catraca) só vai ao responsável do dependente, com vínculo ativo ([35](35-acesso-e-seguranca-fisica-por-portal.md)).
- Aviso de saúde ou enfermaria vai ao responsável. Remetentes padrão: secretaria, enfermagem, médico da escola e coordenação. A escola pode incluir ou remover remetentes. Decidido pelo autor em 03/11/2026. Não aparece no portal de terceiros.

---

## 5. Pendências

| # | Pendência | Tipo |
|---|---|---|
| NOT-01 | Versão de referência da v1: revisada ou original | **Decidido** em 03/11/2026: unir as duas. Telas e painel da original nas seções 3.8 e 3.9 |
| NOT-02 | Horário de silêncio padrão (seção 3.3) | **Decidido** em 03/11/2026: 21h às 7h |
| NOT-03 | Aprovação de segunda pessoa para público acima de 500 (seção 3.4) | **Decidido** em 03/11/2026: sim |
| NOT-04 | Prazo de retenção do corpo da mensagem (seção 3.7) | (jurídico) |
| NOT-05 | Remetentes de aviso de saúde ou enfermagem (seção 4) | **Decidido** em 03/11/2026: secretaria, enfermagem, médico da escola e coordenação por padrão. A escola pode incluir ou remover. Parecer do (jurídico) sobre o conteúdo do aviso continua pendente |
| NOT-06 | Canal push | **Decidido** em 03/11/2026: aplicativo próprio para Android e iOS. Canais: app, SMS, e-mail e WhatsApp |
| NOT-07 | DDL das tabelas do módulo: notificação, template, regra, entrega, fila, preferência e provedor | **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.1. Revisão do owner pendente (DDL-01) |
| NOT-08 | Métricas e painel de operação: quais e para quem | **Escrito** na seção 3.9 |
| NOT-09 | Aplicativo Android e iOS: escopo, arquitetura e publicação nas lojas. É um produto novo, fora dos módulos atuais | Documento. **Decidido** em 03/11/2026: entra depois do núcleo |

---

## 6. Critérios de aceite

- [ ] Aviso obrigatório não pode ser desligado pelo usuário (teste).
- [ ] Aviso fora do horário de silêncio é adiado, salvo obrigatório (teste).
- [ ] Professor não envia para público fora da própria turma (teste de isolamento).
- [ ] Responsável não recebe aviso de dependente sem vínculo ativo (teste).
- [ ] Template com variável sem valor não é enviado (teste).
- [ ] Corpo de aviso de saúde não contém diagnóstico (varredura).
- [ ] Provedor com falha repetida sai do roteamento e o aviso segue pelo reserva (teste).
- [ ] Itens **(jurídico)** e **[Decisão do autor]** respondidos ou marcados como pendentes no [00](00-README.md).
