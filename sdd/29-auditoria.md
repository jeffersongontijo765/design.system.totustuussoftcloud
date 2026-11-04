# 29 — Auditoria: Registro, Integridade, Acesso e Retenção

> Parte do [SDD v2](00-README.md). Princípios iniciais em [18](18-regras-modulos-2.md), seção 4. Busca por CPF em [21](21-busca-e-armazenamento.md), seção 6.8. Prazos em [26](26-sdd-juridico-regulatorio.md), seção 3. Bancos por entidade e unidade em [03](03-dominio-tenancy.md), seção 1.1.
> **Status:** especificação proposta. Este documento consolida a auditoria, que estava espalhada em 80 menções. Prazos marcados como pendentes dependem do jurídico ([25](25-dossie-juridico-e-lacunas.md)).

---

## 1. O que a auditoria registra

Um evento de auditoria existe para responder: **quem fez o quê, em qual objeto, quando, de onde, com qual resultado e com que contexto.**

| Categoria | Exemplos | Obrigatório |
|---|---|---|
| Autenticação | Login, falha de login, bloqueio, troca de senha, MFA, sessão encerrada | Sim |
| Autorização | Troca de contexto, acesso negado, concessão e revogação de vínculo ou papel | Sim |
| Dado sensível | Leitura de cadastro civil, de ficha de saúde, de salário, de dado bancário | Sim |
| Alteração de dado | Criação, alteração e exclusão lógica ou física, com antes e depois | Sim |
| Exportação e download | Exportação de lista, download de arquivo, envio de relatório | Sim |
| Consulta por CPF | Consulta, resultado e finalidade ([21](21-busca-e-armazenamento.md), seção 6.8) | Sim |
| Configuração | Alteração de política, de MFA, de canal, de integração, de feature flag | Sim |
| Pagamento e estorno | Cobrança, baixa, estorno, aprovação dupla ([20](20-pagamentos-seguranca.md)) | Sim |
| Consentimento | Concessão, revogação e versão do texto aceito | Sim |
| Processo | Job, expurgo, migração, reprocessamento de fila, bloqueio legal | Sim |
| Leitura comum | Abertura de tela sem dado sensível | Não (só amostragem, se medido) |

Regra: se a ação altera estado, lê dado sensível ou tem efeito financeiro, a auditoria é obrigatória e **gravada antes da resposta**. Se a gravação falhar, a ação é recusada.

---

## 2. Formato do evento

Todo evento tem o mesmo esquema, em todos os módulos.

| Campo | Tipo | Regra |
|---|---|---|
| `event_id` | UUIDv4 | Gerado pela aplicação |
| `occurred_at` | DATETIME(6) UTC | Relógio sincronizado por NTP. Desvio acima de 1 s gera alerta. |
| `category` | Enum | Uma das categorias da seção 1 |
| `action` | Texto curto | Ex.: `student.grade.update`, `invoice.refund.approve` |
| `result` | Enum | `sucesso`, `negado`, `erro` |
| `actor_uuid` | UUID | Conta global ([06](06-identidade-acesso.md), seção 12). `NULL` apenas para processos do sistema, com `actor_kind = sistema`. |
| `actor_kind` | Enum | `pessoa`, `sistema`, `integracao`, `suporte` |
| `portal` | Enum | Obrigatório. `desenvolvedor`, `gestao`, `professor`, `aluno`, `responsaveis`, `terceiros`, `publico`, `sistema`. Portal de onde a ação partiu ([31](31-matriz-portais-modulos.md), seção 5). Permite filtrar a auditoria por portal sem ler o objeto |
| `entity_uuid`, `unit_uuid` | UUID | Contexto do evento |
| `session_id` | UUID | Sessão que originou a ação |
| `object_type`, `object_uuid` | Texto e UUID | Objeto afetado |
| `before_hash`, `after_hash` | CHAR(64) | Hash do estado antes e depois. O conteúdo completo fica no campo `diff`, quando permitido. |
| `diff` | JSON | Campos alterados. Campos sensíveis aparecem mascarados ou ausentes. |
| `reason` | Texto | Obrigatório em estorno, reabertura, bloqueio legal, leitura de dado sensível fora da rotina e consulta por CPF com detalhe |
| `ip`, `user_agent` | Texto | User-agent truncado em 200 caracteres |
| `correlation_id` | UUID | Liga eventos de uma mesma operação e ao log técnico ([10](10-implantacao-operacao.md), seção 7) |
| `prev_hash`, `hash` | CHAR(64) | Cadeia de integridade (seção 4) |

Proibido no evento: senha, token, segredo, número de cartão, CVV, conteúdo completo de dado de saúde e CPF em texto. Usar hash HMAC quando for preciso identificar um CPF.

---

## 3. Onde fica

| Auditoria | Banco | Motivo |
|---|---|---|
| Ações de unidade (alunos, notas, financeiro, arquivos) | Banco da unidade | Acompanha o dado. Mesma retenção do dado. |
| Ações de identidade e de vínculo | Master | Autenticação e acesso são globais ([06](06-identidade-acesso.md), seção 12) |
| Leitura de cadastro civil | Banco de identidade da entidade | Acompanha o cadastro ([14](14-integracao-modulos.md), seção 3) |
| Ações da plataforma (Editor de portais, suporte, configuração global) | Master | Operação da plataforma |
| Processos e integrações | Banco da unidade ou master, conforme o escopo | Correlação por `correlation_id` |

Cópia de auditoria para armazenamento de longo prazo é feita por exportação diária assinada. Não é uma segunda fonte de verdade.

---

## 4. Integridade

1. **Cadeia de hash:** cada evento guarda `prev_hash`, o hash do evento anterior do mesmo banco e categoria. `hash = SHA-256(event canônico + prev_hash)`.
2. **Verificação:** job a cada hora recalcula a cadeia do último dia. Quebra gera alerta de segurança.
3. **Ancoragem:** o hash do último evento de cada dia é assinado e enviado a armazenamento separado, com a chave fora do servidor de dados ([05](05-seguranca.md)).
4. **Imutabilidade no banco:** a conta da aplicação tem permissão de `INSERT` e `SELECT` na tabela de auditoria. Não tem `UPDATE` nem `DELETE`. Expurgo usa conta própria de processo de retenção, com registro.
5. **Correção:** erro em evento não é alterado. Gera evento de correção que referencia o original.

---

## 5. Acesso à auditoria

| Papel | Pode ver | Não pode ver |
|---|---|---|
| Auditor interno (segurança) | Todas as categorias, com mascaramento padrão | Conteúdo de dado de saúde, sem motivo registrado |
| Gestor da unidade | Eventos da própria unidade, exceto segurança da plataforma | Eventos de outra unidade |
| Encarregado (DPO) | Consultas por CPF, leituras de cadastro civil, pedidos de titular | Conteúdo de dado de saúde |
| Titular | Relatório sobre o próprio dado: quem consultou ou alterou, sem motivo livre de terceiros | Eventos de outras pessoas |
| Suporte da plataforma | Eventos técnicos e de sessão do chamado | Dado de aluno sem vínculo |

Regras:

- Toda leitura da auditoria gera evento de auditoria (`audit.read`).
- Exportação da auditoria exige MFA recente e motivo.
- Acesso à auditoria de outra entidade é impossível pela aplicação. Só é possível por processo jurídico, com registro fora do sistema.

---

## 6. Mascaramento

- CPF: `***.456.789-**` na listagem. Completo só com motivo.
- E-mail: `j***@d***.com`.
- Telefone: últimos quatro dígitos.
- Dado de saúde: presença e tipo do registro, sem conteúdo.
- Valor salarial: sem valor, só indicação de que foi alterado.

---

## 7. Retenção

| Categoria | Prazo | Situação |
|---|---|---|
| Registro de acesso (login, sessão, IP) | 6 meses | Base: Marco Civil, art. 15. Confirmar ([26](26-sdd-juridico-regulatorio.md), J-01). |
| Consulta por CPF | 24 horas | Decisão do autor. Conflito com o registro de acesso e com o relatório ao titular. Ver [25](25-dossie-juridico-e-lacunas.md), Q-01. |
| Alteração de dado de unidade | Mesma retenção do dado | Ver [26](26-sdd-juridico-regulatorio.md), seção 3 |
| Pagamento e estorno | Prazo fiscal e de consumo | Confirmar ([26](26-sdd-juridico-regulatorio.md), seção 3) |
| Ação de plataforma | 5 anos | **Aprovado pelo autor em 03/11/2026.** Parecer jurídico ainda não registrado ([25](25-dossie-juridico-e-lacunas.md)). |
| Evento de expurgo | Permanente | Registro do expurgo sem o dado |

Expurgo por job, com registro. Bloqueio legal impede expurgo do evento.

---

## 8. Alertas

| Alerta | Condição |
|---|---|
| Quebra de cadeia | Qualquer quebra |
| Gravação falhou | Qualquer falha de gravação de evento obrigatório |
| Leitura em volume | Leitura de dado sensível acima do padrão do usuário |
| Consulta por CPF | Padrão de varredura ([21](21-busca-e-armazenamento.md), seção 6.8) |
| Acesso de suporte a dado de tenant | Qualquer acesso fora de chamado vinculado |
| Desvio de relógio | Mais de 1 s |

### 8.1 Envio para central de segurança (AUD-03)

A integração é **opcional**. A auditoria do banco continua a fonte de verdade. A central de segurança (SIEM) recebe cópia, para correlação e alerta.

| Item | Regra |
|---|---|
| Da plataforma | Eventos de segurança do master (login, MFA, bloqueio, acesso negado, ação de plataforma, acesso de suporte) e os alertas desta seção vão para a central da empresa desenvolvedora |
| Da entidade | A entidade que tem central própria recebe só os eventos de segurança dela, por exportação assinada ou pelo webhook de saída da unidade (SRC-06). Nunca recebe evento de outra entidade nem da plataforma |
| Conteúdo | Evento com o mascaramento da seção 6. Pessoa identificada por `uuid`, sem CPF, e-mail ou nome. Sem dado de saúde, nota, valor salarial ou conteúdo de mensagem |
| Transporte | Só saída, da plataforma para a central, com TLS e assinatura do lote. A central não tem acesso de leitura ao banco |
| Falha | Falha de envio não bloqueia a ação do usuário. Os eventos ficam em fila e são reenviados na ordem, com o hash da cadeia (seção 4), para a central detectar lacuna |
| Log | O conector grava log de integração ([49](49-logs-testes-por-portal.md), seção 2.1) |
| Produto | Escolha do produto e teste de envio ficam para homologação, como em AUD-02 |

---

## 9. Testes obrigatórios

- Ação que altera dado grava evento antes da resposta. Falha na gravação recusa a ação.
- Evento não aceita `UPDATE` nem `DELETE` pela conta da aplicação.
- Quebra de cadeia é detectada.
- Evento não contém senha, token, CPF em texto nem dado de saúde (varredura).
- Usuário de uma unidade não lê auditoria de outra.
- Leitura da auditoria gera evento.
- Relatório ao titular não inclui motivo livre de terceiro.

---

## 10. Lacunas

| # | Lacuna | Dono |
|---|---|---|
| AUD-01 | Prazo de retenção de eventos de plataforma: **5 anos, aprovado pelo autor em 03/11/2026.** Registrar parecer jurídico quando houver ([25](25-dossie-juridico-e-lacunas.md), Q-01). | Jurídico |
| AUD-02 | Armazenamento de longo prazo e ancoragem: **decidido pelo autor em 03/11/2026**, com a exportação diária assinada da seção 3. Escolha do produto concreto e teste de restauração ficam para homologação. | Operação |
| AUD-03 | Integração com central de segurança, se houver | **Escrito** em 03/11/2026, seção 8.1. Escolha do produto em homologação |
| AUD-04 | Campo `portal` no evento | **Feito** em 03/11/2026: incluído na seção 2 |

---

## 11. Critérios de aceite

- [ ] Todas as categorias da seção 1 implementadas e testadas.
- [ ] Esquema da seção 2 aplicado em todos os bancos (unidade, identidade e master).
- [ ] Cadeia de hash verificada diariamente, com alerta.
- [ ] Testes da seção 9 passando em CI.
- [ ] AUD-01 e AUD-02 decididas (03/11/2026). Produto de longo prazo escolhido e restauração testada antes de produção.
