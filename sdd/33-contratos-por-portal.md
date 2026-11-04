# 33 — Gestão de Contratos, por Portal

> Parte do [SDD v2](00-README.md). Regras atuais em [17](17-regras-modulos.md), seção 7. Matriz de portais em [31](31-matriz-portais-modulos.md). Assinatura e base legal em [26](26-sdd-juridico-regulatorio.md), seção 6. Auditoria em [29](29-auditoria.md). Privacidade em [32](32-atendimento-privacidade-por-portal.md), seção 3.
> **Status:** aprovada pelo autor em 03/11/2026, com as propostas adotadas. Itens sem valor definido continuam pendentes, criada em 03/11/2026 a partir de `spec_gestao_contratos_completo.md` (v1, 1.376 linhas). Itens **[Decisão do autor]** dependem de resposta. Itens **(jurídico)** dependem de parecer. Este documento não é parecer contratual.
> **Atualização de 03/11/2026:** a assinatura passa a ser serviço comum, usado também por documentos administrativos e emitidos. Ver [54](54-gestao-de-documentos-tres-contextos.md), seção 5.

---

## 1. Estado atual na v2

[17](17-regras-modulos.md), seção 7 tem 6 linhas de entidades, regras e estados. A v1 tem 17 seções, 16 páginas, perfis, abas de cadastro e fluxos. **A v2 não está completa.** Faltam:

- DDL (defeito T-02 em [17](17-regras-modulos.md));
- mapa de contratos por tipo e por portal;
- regras por tipo de contrato;
- fluxo de aprovação com alçadas;
- integração com assinatura;
- monitoramento de obrigações e vigência;
- regra de contrato sensível (dado pessoal, saúde, menor).

---

## 2. Tipos de contrato e a quem pertencem

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

**Pendência:** o contrato de matrícula (aluno ou responsável) e o contrato de cliente são contratos de consumo ou de prestação civil. A forma e as cláusulas dependem de **(jurídico)** ([26](26-sdd-juridico-regulatorio.md), seção 4). Não defino cláusula aqui.

---

## 3. Ciclo de vida

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

**Estados do contrato** (já em [17](17-regras-modulos.md), seção 7.3): `negociacao`, `aprovacao`, `assinado`, `vigente`, `em_renovacao`, `encerrado`, `cancelado`.

**Regras de transição:**

- Contrato `assinado` não é editado. Mudança vira aditivo ([17](17-regras-modulos.md)).
- Ausência de cláusula obrigatória bloqueia envio para assinatura ([17](17-regras-modulos.md), seção 7.2).
- Aprovação jurídica é obrigatória por tipo ([17](17-regras-modulos.md)).
- Quem cria a minuta não aprova a própria minuta (segregação, [22](22-crm-canais-e-papeis.md), seção 5).

---

## 4. Alçadas

| Faixa | Aprovação | Valor |
|---|---|---|
| Abaixo da faixa 1 | Gestor da unidade | **Decidido** em 03/11/2026: até R$ 10.000 |
| Faixa 2 | Gestor + financeiro | **Decidido** em 03/11/2026: de R$ 10.000 a R$ 100.000 |
| Acima da faixa 2 | Gestor executivo + financeiro + jurídico | **Decidido** em 03/11/2026: acima de R$ 100.000 |

Sem os valores, a aplicação não tem regra de alçada. Lacuna L-01 em [17](17-regras-modulos.md).

---

## 5. Assinatura

Estados (v1, seção 13.4): não iniciado, preparando envio, enviado, visualizado, parcialmente assinado, assinado, rejeitado, expirado, cancelado.

Regras:

- Assinatura eletrônica com validade jurídica depende do tipo de documento e do nível exigido **(jurídico)** ([26](26-sdd-juridico-regulatorio.md), seção 6, e Lei 14.063/2020).
- Assinatura de responsável em contrato de aluno: verificação de identidade do signatário antes do envio ([06](06-identidade-acesso.md)).
- Envelope tem validade. Expirado não é reaberto; novo envelope é criado.
- Assinatura de terceiro: o portal de terceiros mostra só o próprio contrato.
- Documento assinado é guardado com hash e trilha ([21](21-busca-e-armazenamento.md)).

---

## 6. Obrigações, vigência e renovação

- Obrigação tem responsável, prazo, evidência e SLA. Vencida sem evidência gera alerta.
- Alerta de vencimento: antecedência configurável por tipo de contrato. Antecedência padrão decidida em 03/11/2026: 60 e 30 dias.
- Renovação automática só se o tipo permitir. Renovação sem aprovação não entra em vigor.
- Reajuste aplica índice definido no contrato. Reajuste sem índice exige aditivo.

---

## 7. Compliance do contrato

A aba de compliance (v1, seção 8.8) guarda: tratamento de dado pessoal, base legal vinculada, DPA anexado, NDA assinado, política de retenção, criticidade do risco, due diligence concluída, documentos regulatórios e data da última revisão.

**Regra:** contrato com tratamento de dado pessoal não é assinado sem DPA anexado. Essa regra é do sistema, não só do processo ([26](26-sdd-juridico-regulatorio.md)).

**Contrato com dado de menor:** exige revisão de privacidade antes da assinatura ([32](32-atendimento-privacidade-por-portal.md), seção 3.2).

---

## 8. Perfis

A v1 define nove perfis (seção 4.1): SA, GE, GC, JU, FI, CO, OP, AU e VI. Eles valem **dentro do portal de gestão**. Para os outros portais valem os papéis de [22](22-crm-canais-e-papeis.md), seção 5.

| Perfil v1 | Papel na v2 | Portal |
|---|---|---|
| SA — Super Admin | Administrador da entidade | Gestão |
| GE — Gestor Executivo | Gestor executivo | Gestão |
| GC — Gestor de Contratos | Gestor de contratos | Gestão |
| JU — Jurídico | Jurídico | Gestão |
| FI — Financeiro | Financeiro | Gestão |
| CO — Compras | Compras | Gestão |
| OP — Operacional | Operacional, somente execução | Gestão |
| AU — Auditor | Auditor | Gestão, somente leitura ([29](29-auditoria.md), seção 5) |
| VI — Visualizador | Consulta restrita conforme escopo | Gestão |

Contratos de cliente (SaaS) são geridos no portal do desenvolvedor pelo papel de comercial e jurídico da plataforma ([22](22-crm-canais-e-papeis.md), seção 4.1).

---

## 9. Páginas e portal

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

## 10. Pendências

| # | Pendência | Tipo |
|---|---|---|
| CTR-01 | DDL de contrato, parte, obrigação, aditivo, solicitação, assinatura (T-02) | **Escrito** em [51](51-ddl-modulos-novos.md), seção 3. Revisão do owner pendente (DDL-01) |
| CTR-02 | Faixas de alçada (seção 4) | **Decidido** em 03/11/2026: até R$ 10.000, de R$ 10.000 a R$ 100.000, e acima, com jurídico |
| CTR-03 | Antecedência padrão de alerta (seção 6) | **Decidido** em 03/11/2026: 60 e 30 dias antes do vencimento |
| CTR-04 | Forma de assinatura por tipo de contrato | (jurídico) |
| CTR-05 | Cláusulas obrigatórias por tipo | (jurídico) |
| CTR-06 | Provedor de assinatura eletrônica | **Decidido** em 03/11/2026: aceitar todos os provedores de terceiros e criar assinatura digital própria, certificada e aprovada pelos órgãos competentes. A assinatura própria depende de credenciamento na ICP-Brasil **(verificar, jurídico)** |
| CTR-07 | Contrato de matrícula: forma, cláusulas e prazo de guarda | (jurídico) |

---

## 11. Critérios de aceite

- [ ] Cada tipo de contrato da seção 2 tem dono e portal de origem.
- [ ] Transições da seção 3 testadas; contrato assinado não é editado.
- [ ] Alçada aplicada pela aplicação, não só pelo processo.
- [ ] Contrato com dado pessoal não é enviado para assinatura sem DPA.
- [ ] Portal de terceiros e de responsáveis mostram só o próprio contrato.
- [ ] DDL escrito para todas as entidades (CTR-01).
- [ ] Itens **[Decisão do autor]** e **(jurídico)** respondidos ou marcados como pendentes no [00](00-README.md).

## 12. Decisões de 03/11/2026

**CTR-02 (faixas de alçada): aprovado como padrão inicial, ajustável por entidade.**

| Faixa | Valor do contrato | Aprovação |
|---|---|---|
| 1 | Até R$ 10.000,00 | Gestor da unidade |
| 2 | Acima de R$ 10.000,00 até R$ 100.000,00 | Gestor executivo e financeiro |
| 3 | Acima de R$ 100.000,00 | Gestor executivo, financeiro e jurídico |

Prazo total ou valor mensal, o que for maior, define a faixa. Contrato que muda de faixa por aditivo é reaprovado na faixa nova.

**CTR-03 (antecedência de alerta de vencimento): aprovado.** Alerta aos 60 dias e novo alerta aos 30 dias antes do vencimento, para contratos de vigência determinada.
