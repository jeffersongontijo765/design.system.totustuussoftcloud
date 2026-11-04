# 49 — Logs de Integração, de Job e de Fila, e Testes por Portal

> Parte do [SDD v2](00-README.md). Estratégia geral de testes em [24](24-operacao-continuidade-qualidade.md), seção 5. Logs técnicos e de aplicação em [10](10-implantacao-operacao.md), seção 7. Eventos de domínio e fila em [14](14-integracao-modulos.md). Auditoria, com o campo `portal`, em [29](29-auditoria.md). Matriz por portal em [31](31-matriz-portais-modulos.md). Dado sensível nos logs, em [07](07-privacidade-lgpd.md).
> **Status:** especificação proposta, criada em 03/11/2026. Fecha LOG-01, LOG-02, TST-01, TST-02 e TST-03 da [31](31-matriz-portais-modulos.md). Os itens **[Decisão do autor]** da seção 6 dependem de resposta.

---

## 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Pergunta | Veredito |
|---|---|
| Logs de integração estão especificados? | **Não.** A [31](31-matriz-portais-modulos.md) marca "sem especificação". Existe só o log técnico geral da [10](10-implantacao-operacao.md) |
| Logs de job e de fila? | **Parcial.** A [10](10-implantacao-operacao.md), seção 8, fala de tentativas e fila de mortos, sem campos nem retenção |
| Testes por portal? | **Não.** A [24](24-operacao-continuidade-qualidade.md) cobre estratégia geral. Não há conjunto por portal nem teste de isolamento por par portal e módulo |
| Logs e testes se misturam com auditoria? | **Não, por decisão.** Auditoria é trilha de negócio e de segurança. Log é diagnóstico técnico. Regras em [29](29-auditoria.md) |

---

## 2. Logs de integração (LOG-01)

Cada chamada a um sistema externo gera um registro. Usado para diagnóstico, não para prova jurídica. Prova de ação de negócio é a auditoria.

| Campo | Regra |
|---|---|
| `integracao_id` | Conector: gateway, fiscal, eSocial, provedor de IA, catraca, provedor de vídeo |
| `direcao` | `saida` (chamada feita pela plataforma) ou `entrada` (webhook recebido) |
| `operacao` | Nome da operação, ex.: `cobranca.criar`, `webhook.pagamento` |
| `status` | `sucesso`, `falha_temporaria`, `falha_permanente`, `recusado` |
| `http_status` e `tempo_ms` | Código e duração |
| `tentativa` | Número da tentativa, com atraso exponencial ([10](10-implantacao-operacao.md), seção 8) |
| `correlation_id` | Liga à operação de negócio e à auditoria ([29](29-auditoria.md), seção 2) |
| `entity_uuid`, `unit_uuid` | Contexto de tenant. Obrigatório ([03](03-dominio-tenancy.md)) |
| `corpo` | **Não gravado.** Só tamanho e hash. Corpo pode conter dado pessoal, dado de pagamento ou dado de saúde |
| `erro_resumo` | Mensagem resumida, sem trecho de resposta que contenha dado |

**Proibido no log:** cabeçalho de autorização, token, segredo, número de cartão, CPF em texto, corpo de resposta com dado pessoal ([14](14-integracao-modulos.md), seção 8).

**Retenção:** 90 dias, decidido pelo autor em 03/11/2026. Depois, expurgo automático.

### 2.1 Conectores com log desde o primeiro lançamento (LOG-05)

Regra: **todo conector que fala com sistema externo por rede grava log de integração desde o primeiro dia**. Não há conector sem log. Troca por arquivo, em que a secretaria baixa e importa, grava log de job (seção 3) na geração e na importação, não log de integração.

| Conector | Escala | Direção | Origem da regra |
|---|---|---|---|
| E-mail e SMS | Plataforma | Saída e retorno de entrega | [16](16-integracoes-externas.md), seção 2; [57](57-notificacoes-por-portal.md) |
| WhatsApp e push do aplicativo | Plataforma | Saída e retorno de entrega | [57](57-notificacoes-por-portal.md), NOT-06 |
| Armazenamento de objeto e antivírus | Plataforma | Saída | [21](21-busca-e-armazenamento.md) |
| Captcha | Plataforma | Saída | [16](16-integracoes-externas.md), seção 2 |
| Cobrança da assinatura SaaS | Plataforma | Saída e webhook | [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 2.2 |
| Backup externo e monitoramento | Plataforma | Saída | [10](10-implantacao-operacao.md) |
| Provedor de modelo de IA | Plataforma, pelo gateway de IA | Saída | [27](27-inteligencia-artificial-e-portais.md), seção 3 |
| Mídia da aula online | Plataforma | Saída | [40](40-aulas-online-por-portal.md) |
| Gateway de pagamento, primário e de contingência | Unidade | Saída e webhook | [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 2.3 |
| NFS-e | Entidade | Saída | [34](34-pagamentos-fiscal-bancos-por-portal.md), seção 5 |
| eSocial | Entidade | Saída e retorno | [39](39-departamento-pessoal-rh-medicina-por-portal.md) |
| SSO da entidade | Entidade | Entrada | [06](06-identidade-acesso.md) |
| Webhook de saída | Unidade (SRC-06) | Saída | [04](04-api.md), seção 7 |
| ERP e sistema legado | Entidade | Saída e entrada | [16](16-integracoes-externas.md), seção 3 |
| Catraca e controle de acesso | Unidade | Entrada e saída | [35](35-acesso-e-seguranca-fisica-por-portal.md) |
| SGP / MEC Gestão Presente e Pé-de-Meia | Unidade | Saída e retorno | [74](74-integracoes-educacionais-oficiais.md), seções 3.3 e 3.5 |
| Sistema municipal por API | Unidade | Saída e entrada | [74](74-integracoes-educacionais-oficiais.md), seção 3.4 |
| Educacenso, SIGEP e sistema municipal por arquivo | Unidade | Log de job, não de integração | [74](74-integracoes-educacionais-oficiais.md) |

Conector novo só entra em produção com o `integracao_id` cadastrado e com o teste de varredura do critério de aceite 1 (sem corpo nem token no log).

---

## 3. Logs de job e de fila (LOG-02)

| Campo | Regra |
|---|---|
| `job_id` e `fila` | Identificador e nome da fila |
| `evento_id` | Chave de idempotência ([14](14-integracao-modulos.md), seção 5). Repetição do mesmo evento não gera efeito duplicado |
| `estado` | `pendente`, `processando`, `processado`, `cancelado`, `rejeitado`. Vai para `rejeitado` após o limite de tentativas ([14](14-integracao-modulos.md)) |
| `tentativas`, `proxima_tentativa_em` | Controle de retentativa |
| `duracao_ms` | Tempo de processamento |
| `erro_resumo` | Mesma regra de dado do log de integração |

**Alertas** (já previstos em [14](14-integracao-modulos.md), seção 9): `rejeitado` acima de zero em evento de dado sensível, e `pendente` com idade acima de 15 minutos.

**Retenção:** 90 dias, igual ao log de integração. Eventos rejeitados ficam até decisão da operação.

---

## 4. Testes por portal (TST-01)

Cada portal tem um conjunto de testes que roda em CI antes de cada deploy.

| Portal | Conjunto mínimo |
|---|---|
| **Desenvolvedor** | Login com MFA. Acesso negado a dado de entidade. Painel de banco sem console SQL aberto ([34](34-pagamentos-fiscal-bancos-por-portal.md), seção 11) |
| **Gestão** | Acesso por papel. Exportação com evento de auditoria. Ação de dado sensível exige motivo |
| **Professor** | Só turmas vinculadas. Nota só pelo professor da turma. Simulado de outra turma recusado |
| **Aluno** | Só o próprio dado. Nota da IA não aparece antes da confirmação |
| **Responsáveis** | Só dependentes com vínculo ativo. Vínculo revogado perde acesso em até 30 segundos ([06](06-identidade-acesso.md)) |
| **Terceiros** | Só o próprio contrato, serviço e unidade. Interseção de filtros ([38](38-portal-de-terceiros-prestadores.md)) |
| **Público** | Consulta de validação sem dado pessoal ([48](48-gerador-de-documentos-por-portal.md), seção 6) |

---

## 5. Teste de isolamento por par (TST-02)

Para cada par portal e módulo da [31](31-matriz-portais-modulos.md), seção 2, há um teste que tenta acessar um objeto de outra entidade, de outra unidade e de outra pessoa do mesmo portal. Resposta esperada: "não encontrado", sem diferença de mensagem ([03](03-dominio-tenancy.md), seção 2).

- Número de pares: uma linha por módulo e por portal, a partir da matriz.
- Executado em CI e em homologação antes da produção.
- Falha bloqueia o deploy.

### 5.1 Geração do conjunto a partir da matriz (TST-05)

O conjunto não é escrito à mão, par a par. Ele é gerado a partir de uma tabela de definição, para que um módulo novo não fique sem teste.

1. **Fonte única.** Um arquivo de definição no repositório lista, para cada módulo, os portais da matriz da [31](31-matriz-portais-modulos.md), seção 2, o tipo de objeto e a rota de leitura. É a versão em código da matriz.
2. **Geração.** Para cada linha, o gerador cria três casos: objeto de outra entidade, de outra unidade da mesma entidade e de outra pessoa do mesmo portal. Os dados vêm de uma massa fixa de teste com duas entidades e duas unidades em cada.
3. **Resposta esperada.** "Não encontrado", com o mesmo código e o mesmo corpo para objeto inexistente e para objeto de outro tenant ([03](03-dominio-tenancy.md), seção 2). O tempo de resposta não pode denunciar a existência do objeto.
4. **Regressão por módulo novo.** O pipeline compara a lista de rotas registradas com o arquivo de definição. Rota de leitura sem linha no arquivo falha o deploy. Assim, um módulo novo não sobe sem entrar na matriz.
5. **Portal de terceiros.** Gera também o caso de interseção: prestador com contrato em outra unidade não lê objeto desta ([38](38-portal-de-terceiros-prestadores.md)).
6. **Relatório.** Cada execução grava quantos pares rodaram, quantos falharam e quais rotas ficaram sem linha. O número de pares tem que ser igual ao da execução anterior, ou maior.

---

## 6. Teste de acessibilidade por portal (TST-03)

| Verificação | Ferramenta e regra |
|---|---|
| Contraste | Mínimo de 4,5:1 para texto normal, em cada tema ([08](08-frontend-design-system.md), seção 4) |
| Teclado | Todo fluxo de criação e edição sem mouse ([08](08-frontend-design-system.md), seção 8) |
| Leitor de tela | Rótulos e anúncios de estado nos fluxos principais |
| Responsividade | Telas de 320, 375 e 1280 px, sem rolagem horizontal |

Ferramenta de varredura automática escolhida em homologação, com versão fixada ([11](11-governanca-qualidade.md)). Varredura automática não substitui teste manual com teclado e leitor de tela.

---

## 7. Pendências

| # | Pendência | Tipo |
|---|---|---|
| LOG-04 | Limite de tentativas de job antes de `rejeitado` | **Decidido** em 03/11/2026: 5 tentativas, com atraso crescente |
| LOG-05 | Lista de conectores com log de integração ativo desde o primeiro lançamento | **Escrito** na seção 2.1 |
| TST-04 | Ferramenta de varredura de acessibilidade, com versão fixada | Operação |
| TST-05 | Conjunto de testes de isolamento gerado a partir da matriz, com teste de regressão a cada novo módulo | **Escrito** na seção 5.1 |

---

## 8. Critérios de aceite

- [ ] Log de integração não contém corpo de resposta nem token (varredura).
- [ ] Log de job com a mesma `evento_id` não gera efeito duplicado (teste de idempotência).
- [ ] Todo portal tem o conjunto da seção 4 rodando em CI (verificação de pipeline).
- [ ] Teste de isolamento de par falha o deploy quando um par vaza dado (teste).
- [ ] Rota de leitura sem linha no arquivo de definição da matriz falha o deploy (verificação de pipeline).
- [ ] Contraste, teclado e responsividade conferidos em cada portal (teste de acessibilidade).
