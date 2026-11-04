# 75 — Análise por Escopo: Busca, Notificações, Perfil e Integrações

> Parte do [SDD v2](00-README.md). Análise de cobertura dos quatro temas por escopo: portal do desenvolvedor (plataforma), entidade, unidade, módulo e global. Não cria regra nova para o que já está especificado. Aponta o que falta e o que precisa de decisão.
> Documentos de referência: busca e armazenamento em [21](21-busca-e-armazenamento.md); notificações em [57](57-notificacoes-por-portal.md); integrações externas em [16](16-integracoes-externas.md); integrações internas e eventos em [14](14-integracao-modulos.md); identidade, sessões e MFA em [06](06-identidade-acesso.md); preferências de comunicação em [32](32-atendimento-privacidade-por-portal.md), seção 3.2; integrações educacionais em [74](74-integracoes-educacionais-oficiais.md).
> **Status:** análise, criada em 03/11/2026. Todas as decisões do autor desta análise foram respondidas em 03/11/2026 (seção 7).

---

## 1. Resposta direta

> **Leitura (04/11/2026):** esta tabela registra o que existia no SDD antes deste documento ser escrito. Os itens marcados como **Não** ou **Parcial** são especificados nas seções seguintes deste documento, exceto o que estiver listado na seção de pendências.

| Tema | Veredito |
|---|---|
| Busca | **Parcial.** O motor, a permissão e o isolamento estão em [21](21-busca-e-armazenamento.md), seção 6. Não há especificação da busca global por portal nem do que cada perfil pode buscar |
| Notificações | **Coberto** em [57](57-notificacoes-por-portal.md), com canais, preferências, público por escopo e portal. Falta ligar aos eventos dos módulos novos |
| Perfil (conta do usuário) | **Lacuna.** Existe em pedaços: sessões e MFA em [06](06-identidade-acesso.md), consentimentos em [32](32-atendimento-privacidade-por-portal.md), preferências em [57](57-notificacoes-por-portal.md). Não há uma especificação de "meu perfil" |
| Integrações externas | **Coberto para plataforma e entidade** em [16](16-integracoes-externas.md), e para o padrão educacional em [74](74-integracoes-educacionais-oficiais.md). Falta o nível de unidade |
| Integrações internas | **Parcial.** Catálogo de eventos em [14](14-integracao-modulos.md), seção 4, só para RH, SMT, suprimentos, financeiro e contratos. Os módulos acadêmicos, de notificação e de documentos novos não têm eventos |

---

## 2. Busca, por escopo

| Escopo | O que deve existir | Situação | Onde |
|---|---|---|---|
| **Portal do desenvolvedor** | Busca por conta de cliente, entidade e unidade, só por metadados e status. Sem dado de tenant | **Lacuna.** Nada define o que o desenvolvedor pode buscar | [31](31-matriz-portais-modulos.md) diz que não vê dado de entidade. Falta regra de busca |
| **Entidade** | Busca de pessoas, registros e documentos da entidade, conforme o papel | Coberto pela regra geral de permissão | [21](21-busca-e-armazenamento.md), seção 6.3 |
| **Unidade** | Mesmo que entidade, limitado à unidade | Coberto pela regra geral | [21](21-busca-e-armazenamento.md), seção 6.3 |
| **Módulo** | Quais campos cada módulo indexa | Parcial. Seção 6.1 da [21](21-busca-e-armazenamento.md) lista campos gerais. Falta por módulo | Ver [21](21-busca-e-armazenamento.md) e os docs de módulo |
| **Global (topbar, Ctrl+K)** | Busca única que mistura módulos, respeitando permissão | **Lacuna.** A v1 cita "busca global" em quase todos os módulos, sem regra de composição | Ausente na v2 |
| **Por portal** | Professor busca só as turmas dele. Aluno busca só o próprio conteúdo. Responsável busca só dependentes | **Lacuna.** A regra existe em cada portal, mas não há matriz de busca | [31](31-matriz-portais-modulos.md) |

**Pontos a decidir:**
- **SRC-01 Decidido** em 03/11/2026: o portal do desenvolvedor busca entidade e unidade só por nome, CNPJ e status da conta, sem dado pessoal nem acadêmico.
- **SRC-02 Decidido** em 03/11/2026: a busca global agrupa os resultados por módulo, cada um filtrado pela permissão.
- **SRC-03 Mantido:** o log de busca guarda só o hash do termo ([21](21-busca-e-armazenamento.md), seção 6.6).

---

## 3. Notificações, por escopo

| Escopo | Situação | Onde |
|---|---|---|
| Plataforma (desenvolvedor) | Coberto: comunicado de manutenção e cobrança, por e-mail e in-app | [57](57-notificacoes-por-portal.md), seção 4 |
| Entidade | Coberto: público da entidade, com aprovação acima de 500 | [57](57-notificacoes-por-portal.md), seção 3.4 |
| Unidade | Coberto: público da unidade | [57](57-notificacoes-por-portal.md), seção 3.4 |
| Turma | Coberto | [57](57-notificacoes-por-portal.md), seção 3.4 |
| Módulo | Parcial. Os avisos de cada módulo estão nos docs de módulo, mas não há catálogo de avisos por módulo | [57](57-notificacoes-por-portal.md), seção 4 |
| Global | Coberto pelas regras de canal e de silêncio | [57](57-notificacoes-por-portal.md), seção 3.3 |

**Lacuna:** os avisos dos módulos novos (ocorrência, boletim, conselho, estágio, TCC, biblioteca, financeiro novo, censo) não estão no catálogo de eventos da [14](14-integracao-modulos.md). Sem evento, a notificação não dispara. Ver seção 5.

---

## 4. Perfil (conta do usuário)

Hoje o "perfil" está espalhado. Itens existentes:

| Item | Onde está |
|---|---|
| Sessões simultâneas (3 por usuário) | [06](06-identidade-acesso.md), seção 3 |
| Dispositivos confiáveis e token de dispositivo | [06](06-identidade-acesso.md), seção 7 |
| MFA e passkey | [06](06-identidade-acesso.md), seção 5 |
| Recuperação de conta | [06](06-identidade-acesso.md), seção 4 |
| Consentimentos por finalidade | [32](32-atendimento-privacidade-por-portal.md), seção 3.2 |
| Preferências de canal e de silêncio | [57](57-notificacoes-por-portal.md), seção 3.3 |
| Idioma | [09](09-internacionalizacao.md) |

**Lacunas:**
- **PER-01:** não há tela nem regra de "meu perfil": quais dados civis o próprio usuário edita, e quais exigem aprovação (nome, CPF, endereço, responsável).
- **PER-02:** não há foto e avatar, nem a regra de quem vê a foto (ver [35](35-acesso-e-seguranca-fisica-por-portal.md), seção 6, para foto em relatório).
- **PER-03:** não há histórico de alterações do próprio perfil para o usuário ver.

**Pontos a decidir:**
- **PER-04 Decidido** em 03/11/2026: o próprio usuário altera contato e endereço sem aprovação. Nome, CPF e vínculo exigem aprovação da secretaria.
- **PER-05 Decidido** em 03/11/2026: o perfil mostra o histórico de alterações ao próprio usuário, sem valor antigo de dado sensível.

---

## 5. Integrações internas e eventos

Catálogo atual: RH, SMT, suprimentos, financeiro e contratos ([14](14-integracao-modulos.md), seção 4).

**Lacuna:** os módulos novos ainda não têm evento. Lista proposta, para cada um, o evento principal e o consumidor:

| Módulo | Evento | Consumidor | Documento |
|---|---|---|---|
| Acadêmico (matrícula) | `academico.matricula.efetivada` | Financeiro, Notificações, Biblioteca | [46](46-matricula-e-rematricula-por-portal.md) |
| Diário | `diario.falta.registrada` | Notificações (aviso), Boletim | [61](61-diario-escolar-por-portal.md) |
| Boletim | `boletim.resultado.fechado` | Matrícula (rematrícula), Notificações | [62](62-boletim-e-conselho-de-classe-por-portal.md) |
| Ocorrência | `ocorrencia.registrada` (grave) | Notificações, Conselho | [63](63-ocorrencias-disciplinares-por-portal.md) |
| Biblioteca | `biblioteca.multa.gerada` | Financeiro | [68](68-biblioteca-por-portal.md) |
| Financeiro | `financeiro.titulo.pago` | Matrícula (bloqueio parcial), Notificações | [18](18-regras-modulos-2.md) |
| Calendário | `calendario.dia.alterado` | Turmas, Diário, Notificações | [58](58-calendario-e-eventos-por-portal.md) |
| Censo | `relatorio.envio.gerado` | Auditoria | [69](69-relatorios-e-censo-por-portal.md) |

**Regra:** o nome segue o padrão de [14](14-integracao-modulos.md), seção 4: `<modulo>.<entidade>.<fato>`.

**Pontos a decidir:**
- **SRC-04 Decidido** em 03/11/2026: os eventos da lista acima entram nesta versão, no catálogo de [14](14-integracao-modulos.md), seção 4.

---

## 6. Integrações externas, por escopo

| Escopo | Situação | Onde |
|---|---|---|
| Plataforma (desenvolvedor) | Coberto: e-mail, SMS, armazenamento, antivírus, captcha, cobrança, backup, monitoramento | [16](16-integracoes-externas.md), seção 2 |
| Entidade | Coberto: gateway, ERP, NFS-e, eSocial, SSO, webhook, legado | [16](16-integracoes-externas.md), seção 3 |
| Educacional oficial | Coberto: Educacenso, SIGEP, SGP, Pé-de-Meia, sistema municipal (conflito em aberto) | [74](74-integracoes-educacionais-oficiais.md) |
| **Unidade** | Coberto para gateway de pagamento, por decisão SRC-05: um gateway primário por unidade, dentro da entidade. Atualizados [16](16-integracoes-externas.md) e [34](34-pagamentos-fiscal-bancos-por-portal.md). Outras integrações por unidade ainda não especificadas | SRC-05 |
| Módulo | Parcial. Cada módulo fala com o externo do seu jeito (portaria com catraca, TI com monitoramento) | [35](35-acesso-e-seguranca-fisica-por-portal.md), [36](36-tecnologia-da-informacao-por-portal.md) |
| Global | Coberto: webhook de saída | [04](04-api.md), seção 7 |

**Pontos a decidir:**
- **SRC-05 Decidido** em 03/11/2026: um gateway primário por unidade, dentro da entidade.
- **SRC-06 Decidido** em 03/11/2026: o webhook de saída é configurado por unidade, com endpoint e segredo HMAC próprios.

---

## 7. Pendências

| # | Pendência | Tipo |
|---|---|---|
| SRC-01 | Busca do portal do desenvolvedor: só nome, CNPJ e status (seção 2) | **Decidido** em 03/11/2026 |
| SRC-02 | Busca global: agrupa por módulo, cada um filtrado pela permissão (seção 2) | **Decidido** em 03/11/2026 |
| SRC-03 | Termo de busca no log (seção 2) | Mantido: hash |
| SRC-04 | Eventos dos módulos acadêmicos nesta versão (seção 5) | **Decidido** em 03/11/2026: sim |
| SRC-05 | Gateway por unidade ou por entidade (seção 6) | **Decidido** em 03/11/2026: por unidade. Docs 16, 34 e 46 atualizados |
| SRC-06 | Webhook por unidade ou por entidade (seção 6) | **Decidido** em 03/11/2026: por unidade |
| PER-01 | Tela e regra de "meu perfil" (seção 4) | **Escrito** em [76](76-meu-perfil-por-portal.md). Campos decididos em PER-04 |
| PER-02 | Foto e avatar (seção 4) | **Decidido** em 03/11/2026: foto opcional, para a mesma unidade (PER-06 de [76](76-meu-perfil-por-portal.md)) |
| PER-03 | Histórico de alterações do perfil para o usuário (seção 4) | **Escrito** em [76](76-meu-perfil-por-portal.md), seções 2 e 3, a partir de PER-05 |
| PER-04 | Campos civis sem aprovação (seção 4) | **Decidido** em 03/11/2026: contato e endereço. Nome, CPF e vínculo pedem aprovação da secretaria |
| PER-05 | Histórico para o usuário (seção 4) | **Decidido** em 03/11/2026: sim, sem valor antigo de dado sensível |

---

## 8. Critérios de aceite desta análise

- [ ] Cada tema tem uma linha por escopo (plataforma, entidade, unidade, módulo, global).
- [ ] Cada lacuna tem código e está na seção 7.
- [ ] Nenhuma decisão [Decisão do autor] vira regra sem resposta.
