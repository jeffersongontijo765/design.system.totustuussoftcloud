# 25 — Dossiê Jurídico e Análise das Lacunas

> Parte do [SDD v2](00-README.md). Lacunas G-01 a G-20 em [24](24-operacao-continuidade-qualidade.md), seção 9.
> **Aviso:** este documento não é parecer jurídico. Ele organiza as perguntas que precisam de parecer, apresenta a posição atual do SDD, lista as normas a verificar e aponta os riscos de cada resposta. Quem responde juridicamente é advogado habilitado. Os números de artigo e de resolução citados devem ser conferidos no texto vigente antes de qualquer uso.

---

## 1. Como usar este dossiê

1. Enviar ao jurídico as perguntas da seção 3, na ordem de prioridade.
2. Para cada pergunta, o jurídico responde com uma das saídas: confirma a posição atual, aponta outra posição ou pede informação adicional.
3. A resposta vira decisão registrada no SDD, com data e nome do responsável técnico do parecer.

---

## 2. Análise das lacunas

| Lacuna | Situação atual | Diagnóstico | Ação |
|---|---|---|---|
| G-01 | Resolvida | D-22 a D-24 aprovadas em 02/11/2026 | Nenhuma |
| G-02 | Aberta | A retenção de 24 h da auditoria de consultas por CPF conflita com o relatório ao titular e pode conflitar com regra de guarda de registros de acesso (seção 3, Q-01) | **Prioridade máxima** |
| G-03 | Aberta | A matriz de base legal tem linhas com base proposta e sem análise de necessidade. Algumas bases dependem de teste formal (legítimo interesse) | Q-03 a Q-06 |
| G-04 | Resolvida | Limite de MFA: a entidade reduz livremente; aumenta até R$ 5.000, com aprovação da plataforma; acima disso não é permitido. Decidido pelo autor em 03/11/2026 | Nenhuma |
| G-05 | Aberta | RIPD da busca por CPF e do cadastro civil. Obrigatório quando o tratamento é de alto risco ou quando a ANPD pedir | Elaborar com o DPO (seção 4) |
| G-06 | Aberta | DDL de módulos ausentes. Não é jurídica | Owners dos módulos |
| G-07 | Aberta | Regras campo a campo. Não é jurídica | Owners dos módulos |
| G-08 | Aberta | Duplicidade de estoque. Não é jurídica | Produto |
| G-09 | Aberta | Fronteira RH/Pessoas. Não é jurídica | Produto |
| G-10 | Aberta | Módulo de atendimento. Não é jurídica | Produto |
| G-11 | Aberta | Motor de OCR e ADR. Não é jurídica | Responsável técnico |
| G-12 | Aberta | Prazo de retenção de backups. Tem reflexo jurídico | Q-10 |
| G-13 | Aberta | Guarda para retenção legal na saída de cliente. Depende de norma setorial | Q-09 |
| G-14 | Aberta | Termos, contrato, política de privacidade e de cookies. Precisam de revisão jurídica | Q-11 |
| G-15 | Aberta | SLA contratual. Depende de decisão comercial | Autor |
| G-16 | Aberta | Matriz de isolamento automatizada. Não é jurídica | Segurança |
| G-17 | Aberta | Plano de continuidade para o cliente. Não é jurídica | Operação |
| G-18 | Aberta | Declaração de acessibilidade. Verificar exigência legal aplicável | Q-12 |
| G-19 | Aberta | Jurisdições fora do Brasil. Só relevante se houver cliente fora | Q-13 |
| G-20 | Aberta | Revisão de regras pendentes. Não é jurídica | Owners |

Dos 20 itens, cinco dependem de parecer. Os outros são decisões técnicas, comerciais ou de produto.

---

## 3. Perguntas para o jurídico

Cada pergunta traz a posição atual, as normas a verificar e o risco da resposta errada.

### Q-01 — Retenção dos registros de acesso e da auditoria de consultas por CPF (G-02)

**Posição atual:** 24 horas para a auditoria de consulta por CPF ([21](21-busca-e-armazenamento.md), seção 6.8), decidida pelo autor.

**Pontos de atenção:**

- **Marco Civil da Internet, art. 15:** provedor de aplicação que exerce atividade organizada e com fins econômicos deve manter os registros de acesso a aplicações pelo prazo que a lei fixa, em regra seis meses. O jurídico deve confirmar se os registros de login e de acesso ao sistema da plataforma se enquadram.
- **LGPD, art. 37:** o controlador e o operador devem manter registro das operações de tratamento. A lei não fixa prazo, mas o registro precisa existir durante o período de necessidade.
- **LGPD, art. 18 e art. 19:** o titular pode pedir confirmação e acesso. O relatório de quem consultou o CPF dele só cobre o que existir no banco.

**Risco da resposta errada:** se o registro de acesso for guardado por menos do que a lei exige, há infração e perda da prova em incidente. Se for guardado por mais do que o necessário, há excesso de tratamento.

**Proposta de trabalho para o jurídico:** separar dois registros.

| Registro | Conteúdo | Prazo a confirmar |
|---|---|---|
| Registro de acesso (login, IP, sessão) | Quem acessou o sistema e quando | Provavelmente seis meses (Marco Civil, art. 15); confirmar |
| Auditoria de consulta por CPF | Quem consultou qual CPF, com finalidade e motivo | Definir com base na finalidade e no direito do titular |

A decisão de 24 horas, se mantida para a auditoria de consulta por CPF, não pode ser estendida ao registro de acesso sem parecer.

### Q-02 — Relatório ao titular sobre consultas (G-02)

**Pergunta:** o relatório de quem consultou o CPF do titular precisa cobrir todo o período de tratamento, ou pode cobrir só o período de guarda?

**Risco:** se o período de guarda for menor que o período que o titular pode pedir, o direito fica sem efeito.

### Q-03 — Base legal da matriz (G-03)

**Posição atual:** matriz em [07](07-privacidade-lgpd.md), seção 3, com bases propostas por finalidade. Cada linha precisa de confirmação.

**Pontos a confirmar:**

- Matrícula e vínculo acadêmico (art. 7º, II e V).
- Cobrança de mensalidades (art. 7º, V e VI). Confirmar também o Código de Defesa do Consumidor.
- Folha e RH (art. 7º, II). Confirmar as normas trabalhistas e do eSocial.
- Segurança e medicina do trabalho (art. 11, II). Confirmar as NRs aplicáveis.
- Marketing (art. 7º, I, consentimento). Confirmar a forma de registro.
- Logs e segurança (art. 7º, IX, legítimo interesse). Exige teste de balanceamento (Q-04).

### Q-04 — Legítimo interesse (G-03)

**Pergunta:** a base de segurança e logs pode ser legítimo interesse? A ANPD publicou guia sobre legítimo interesse, que deve ser consultado.

**O que é preciso:** registro do teste de finalidade, necessidade e balanceamento com os direitos do titular. Sem esse teste, a base não se sustenta.

### Q-05 — Cobrança e canais de mensagem

**Posição atual:** a régua de cobrança ([18](18-regras-modulos-2.md), seção 2.6) prevê negativação aos 30 dias e mensagens por SMS, WhatsApp e ligação.

**Pontos de atenção:**

- **Código de Defesa do Consumidor, art. 43, §2º:** a abertura de cadastro de inadimplente deve ser comunicada por escrito ao consumidor antes da inclusão. Confirmar o texto vigente e o prazo de comunicação.
- **Superendividamento:** Lei 14.181/2021 altera o CDC e trata de prevenção e de tratamento do superendividamento. Confirmar a aplicação à régua.
- **Bloqueio do portal aos 90 dias:** a régua prevê bloqueio do acesso ao portal. O jurídico deve avaliar se o bloqueio afeta serviço essencial, se atinge menor de idade e se atinge documentos obrigatórios. A proposta do SDD é bloqueio parcial ([18](18-regras-modulos-2.md), seção 2.6).
- **Consentimento para mensagens:** confirmar a base para SMS, WhatsApp e Telegram em cobrança e em marketing.

### Q-06 — Dados de crianças e adolescentes

**Posição atual:** tratamento de dados de menores com consentimento de responsável e minimização ([07](07-privacidade-lgpd.md), seção 1).

**Norma:** LGPD, art. 14, que exige consentimento específico e em destaque de pelo menos um dos pais ou responsável legal.

**Pergunta:** qual a base para o tratamento de dados de aluno menor nas finalidades de matrícula, de cobrança e de comunicação com a família? Quais dados exigem consentimento e quais dispensam?

### Q-07 — Pagamentos e arranjo de pagamento (D-10)

**Posição atual:** conta do tenant no gateway, sem custódia pela plataforma. Gateway da plataforma só com parecer.

**Norma a verificar:** Lei 12.865/2013, sobre arranjos e instituições de pagamento. Verificar também as resoluções do Banco Central aplicáveis.

**Pergunta:** a plataforma que recebe o pagamento e repassa ao tenant precisa de autorização do Banco Central? O modelo de split, em que o provedor divide o valor, muda a análise?

**Risco:** operar arranjo sem autorização. Esta é a pergunta de maior risco regulatório do projeto.

### Q-08 — Retenção de documentos escolares e de RH

**Pergunta:** qual o prazo de guarda, por tipo de documento, para:

- Histórico escolar e registros de vida escolar. Normas de ensino aplicáveis.
- Documentos trabalhistas. CLT, prazo prescricional, e FGTS, Súmula 362 do TST (confirmar).
- Registros de SST, como ASO e PCMSO. NRs aplicáveis.

**Risco:** guardar menos do que a lei exige, ou guardar indefinidamente sem base.

### Q-09 — Retenção legal na saída de cliente (G-13)

**Pergunta:** quais dados de uma entidade que sai da plataforma precisam ser mantidos por obrigação legal, e por quanto tempo? Quem é o responsável por essa guarda, a entidade ou a plataforma?

**Posição atual:** a plataforma guarda em banco de retenção, com acesso restrito ([23](23-dominios-provisionamento-ciclo-de-vida.md), seção 5). O contrato precisa dizer quem é o responsável.

### Q-10 — Backups e direito de eliminação (G-12)

**Pergunta:** quando um titular pede eliminação, qual o prazo aceitável para que o dado saia dos backups? Há exigência legal para o prazo de backup?

**Posição atual:** backups expiram conforme a política, com prazo a definir. Ver [24](24-operacao-continuidade-qualidade.md), seção 1.

### Q-11 — Documentos contratuais e de privacidade (G-14)

**Documentos a revisar:**

- Termos de uso da plataforma.
- Contrato de cliente, com SLA e saída.
- Contrato de tratamento de dados, entre plataforma e entidade, quando a plataforma age como operadora.
- Política de privacidade do site e dos canais.
- Política de cookies.
- Política de segurança para fornecedores.

**Pergunta:** a estrutura de responsabilidades (controlador e operador) está correta para o modelo de canais de [22](22-crm-canais-e-papeis.md)?

### Q-12 — Acessibilidade (G-18)

**Pergunta:** há exigência legal de acessibilidade para plataforma educacional e para serviços públicos contratados? Confirmar a norma aplicável e o nível exigido. A proposta é WCAG 2.2 AA.

### Q-13 — Jurisdições fora do Brasil (G-19)

**Pergunta:** há cliente fora do Brasil? Se houver, quais normas de proteção de dados se aplicam? Sem cliente fora do Brasil, este item fica fechado.

---

## 4. Decisões que não são jurídicas

Estes itens dependem do autor ou do DPO, não do jurídico.

| Item | Pergunta | Recomendação |
|---|---|---|
| G-04 — piso do limite de MFA | Qual o valor máximo que um tenant pode configurar? | Sugestão: tenant reduz livremente; aumento até R$ 5.000,00, com aprovação da plataforma. Acima disso, não permitido. |
| G-05 — RIPD | Quem elabora e quando? | DPO elabora antes da produção, para busca por CPF e para cadastro civil. Revisão anual. |
| G-15 — SLA | Qual SLA entra no contrato? | Usar as metas de [24](24-operacao-continuidade-qualidade.md), seção 2, como ponto de partida, ajustadas ao preço. |

---

## 5. Pontos de melhoria no SDD que dependem desta análise

| Documento | Melhoria | Motivo |
|---|---|---|
| [21](21-busca-e-armazenamento.md), seção 6.8 | Separar registro de acesso e auditoria de consulta por CPF | Q-01 |
| [07](07-privacidade-lgpd.md), seção 3 | Marcar legítimo interesse como exigindo teste formal | Q-04 |
| [18](18-regras-modulos-2.md), seção 2.6 | Incluir comunicação prévia do CDC e a análise de superendividamento | Q-05 |
| [20](20-pagamentos-seguranca.md), seção 2 | Vincular gateway da plataforma à resposta de Q-07 | Q-07 |
| [23](23-dominios-provisionamento-ciclo-de-vida.md), seção 5 | Definir responsável pela guarda legal na saída | Q-09 |

---

## 6. Critérios de encerramento

- [ ] Q-01 a Q-08 respondidas por escrito pelo jurídico, com data e nome do responsável.
- [ ] Matriz de base legal atualizada com a resposta.
- [ ] Registro de acesso e auditoria de CPF com prazos definidos.
- [ ] Gateway da plataforma: decisão sobre arranjo registrada (D-10).
- [ ] RIPD aprovado pelo DPO para busca por CPF e para cadastro civil.
- [ ] Contratos da seção 8 de [24](24-operacao-continuidade-qualidade.md) revisados.
