# 76 — Meu Perfil, por Portal

> Parte do [SDD v2](00-README.md). Fecha PER-01 da análise do [75](75-busca-notificacoes-perfil-integracoes-por-escopo.md). Cada pessoa tem um perfil, em todos os portais, com a mesma tela. Segurança e sessões em [06](06-identidade-acesso.md). Preferências de canal e silêncio em [57](57-notificacoes-por-portal.md), seção 3.3. Consentimentos em [32](32-atendimento-privacidade-por-portal.md), seção 3.2. Idioma em [09](09-internacionalizacao.md). Pedido de titular em [32](32-atendimento-privacidade-por-portal.md). Auditoria em [29](29-auditoria.md).
> **Status:** especificação proposta, criada em 03/11/2026. Campos editáveis decididos em PER-04 e PER-05 (doc 75). Itens **[Decisão do autor]** ou **(proposta)** indicam o que ainda depende de resposta.

---

## 1. Resposta direta

| Pergunta | Veredito |
|---|---|
| Existe tela de perfil? | **Não na v2.** Os pedaços existem em outros documentos |
| Quem tem perfil? | Toda pessoa com conta, em qualquer portal |
| Quem edita o quê? | Contato e endereço, o próprio usuário. Nome, CPF e vínculo, com aprovação |

---

## 2. Seções

Uma única tela, com estas seções:

| Seção | Conteúdo | Origem |
|---|---|---|
| Dados pessoais | Nome, CPF, nascimento, documento, vínculo | Cadastro civil ([06](06-identidade-acesso.md)) |
| Contato | Telefone e e-mail verificado | [06](06-identidade-acesso.md), seção 4 |
| Endereço | Endereço completo | Cadastro civil |
| Segurança | Senha, MFA, passkey, sessões, dispositivos | [06](06-identidade-acesso.md), seções 3, 5 e 7 |
| Preferências de aviso | Canal por tipo e horário de silêncio | [57](57-notificacoes-por-portal.md), seção 3.3 |
| Consentimentos | Finalidades aceitas e revogação | [32](32-atendimento-privacidade-por-portal.md), seção 3.2 |
| Idioma | Idioma da interface | [09](09-internacionalizacao.md) |
| Histórico de alterações | O que mudou, quando e por quem | Decisão PER-05 |
| Meus dados | Pedido de cópia ou de eliminação | [32](32-atendimento-privacidade-por-portal.md) |

---

## 3. Regras de edição

- **Contato e endereço:** o próprio usuário altera e a mudança vale na hora. Decisão PER-04.
- **Nome, CPF e vínculo:** o usuário pede. A secretaria aprova ou recusa, com motivo, em até 5 dias úteis. Decisões PER-04 e PER-08.
- **E-mail:** alteração exige verificação do novo endereço ([06](06-identidade-acesso.md), seção 4).
- **Histórico:** mostra quando e o que mudou. Não mostra o valor anterior de dado sensível. Decisão PER-05.
- **Auditoria:** toda alteração gera evento, com o campo `portal` ([29](29-auditoria.md)).

---

## 4. Foto

Foto é opcional. Aparece para pessoas com vínculo na mesma unidade. **Decidido** em 03/11/2026 (PER-06). Não aparece em relatório sem consentimento específico ([56](56-configuracoes-e-relatorios-lacunas.md), CFG-02).

---

## 5. Por portal

| Portal | Perfil | Pode editar | Não pode |
|---|---|---|---|
| **Desenvolvedor** | Sim, da equipe da empresa | Contato e segurança da própria conta | Ver perfil de cliente |
| **Gestão, coordenação, secretaria, financeiro** | Sim | Contato e endereço. Pede alteração civil | Editar o perfil de outra pessoa sem papel próprio |
| **Professor** | Sim | Contato, endereço e preferências | Editar dados de vínculo |
| **Aluno** | Sim | Contato, endereço e preferências | Editar dados de vínculo sem pedido |
| **Responsáveis** | Sim | Contato, endereço e preferências | Editar dados do dependente |
| **Terceiros** | Sim, da conta do prestador | Contato e segurança da própria conta | Ver perfil de outro prestador |

---

## 6. Pendências

| # | Pendência | Tipo |
|---|---|---|
| PER-06 | Foto: opcional, para a mesma unidade (seção 4) | **Decidido** em 03/11/2026 |
| PER-07 | DDL: pedido de alteração civil e histórico. **Escrito** em [51](51-ddl-modulos-novos.md), seção 15.18. Revisão do owner pendente | Documento |
| PER-08 | Prazo para a secretaria responder a pedido de alteração civil (seção 3) | **Decidido** em 03/11/2026: 5 dias úteis |

---

## 7. Critérios de aceite

- [ ] Contato alterado pelo próprio usuário vale sem aprovação (teste).
- [ ] Nome, CPF ou vínculo alterado pelo usuário fica pendente de aprovação (teste).
- [ ] Histórico não mostra valor anterior de dado sensível (varredura).
- [ ] Usuário não vê perfil de outra pessoa sem papel próprio (teste de isolamento).
- [ ] Itens **[Decisão do autor]** e **(proposta)** respondidos ou marcados como pendentes no [00](00-README.md).
