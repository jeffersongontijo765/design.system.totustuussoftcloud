# 26 — SDD Jurídico-Regulatório

> Parte do [SDD v2](00-README.md). Complementa [07](07-privacidade-lgpd.md) (privacidade), [18](18-regras-modulos-2.md) (cobrança), [20](20-pagamentos-seguranca.md) (pagamentos), [21](21-busca-e-armazenamento.md) (busca por CPF) e [25](25-dossie-juridico-e-lacunas.md) (perguntas ao jurídico).

> ## Aviso importante
> Este documento foi elaborado como especificação de requisitos regulatórios para o sistema. **Não é parecer jurídico e não substitui advogado habilitado.** Ele organiza as obrigações que o sistema precisa atender, indica onde cada obrigação é tratada no SDD e marca o grau de confiança de cada referência.
>
> **Legenda de confiança:**
> - **[A]** referência consolidada, que o sistema pode implementar. O jurídico confirma a redação vigente.
> - **[V]** referência a verificar antes do uso. Sei da existência da norma, mas o prazo, o alcance ou a redação precisam de conferência.
> - **[P]** ponto que depende de parecer, sem resposta definitiva neste documento.

---

## 1. Mapa de obrigações

| Área | Norma principal | Confiança | Controle no SDD | Documento |
|---|---|---|---|---|
| Proteção de dados pessoais | LGPD (Lei 13.709/2018) | [A] | Bases legais, direitos, incidentes, RIPD | [07](07-privacidade-lgpd.md), [21](21-busca-e-armazenamento.md), [25](25-dossie-juridico-e-lacunas.md) |
| Dados de crianças e adolescentes | LGPD, art. 14; ECA | [A] para art. 14; [V] demais | Consentimento de responsável, minimização | [07](07-privacidade-lgpd.md), seção 1 |
| Registro de acesso a aplicações | Marco Civil da Internet (Lei 12.965/2014), art. 15 | [A] para existência; [V] para o prazo | Registro de acesso separado | [21](21-busca-e-armazenamento.md), seção 6.8 |
| Relação de consumo (mensalidade, serviços) | CDC (Lei 8.078/1990) | [A] | Contrato, cobrança, multa, arrependimento | Este documento, seções 4 e 5 |
| Superendividamento | Lei 14.181/2021 | [A] para existência; [V] para aplicação à régua | Régua com análise de renegociação | [18](18-regras-modulos-2.md), seção 2.6 |
| Anuidades e mensalidades escolares | Lei 9.870/1999 | [V] | Limites de reajuste, multa e juros | Este documento, seção 4 |
| Educação (matrícula, documentos) | LDB (Lei 9.394/1996) e normas do sistema de ensino | [V] | Guarda de registros escolares | Este documento, seção 6 |
| Trabalho e saúde ocupacional | CLT; NRs (NR-1, NR-7 e outras); eSocial | [V] | PCMSO, ASO, CAT, EPI | [17](17-regras-modulos.md), seção 5 |
| Fiscal | LC 116/2003 (ISS); normas municipais; CTN | [A] para ISS; [V] para prazos | NFSe, retenção fiscal | [18](18-regras-modulos-2.md), seção 2.7 |
| Pagamentos | Lei 12.865/2013; normas do Banco Central | [A] para a lei; [V] para as resoluções | Modelo de recebimento | [20](20-pagamentos-seguranca.md), seção 2 |
| Assinatura e contratos eletrônicos | MP 2.200-2/2001; Lei 14.063/2020 | [A] | Assinatura por nível | Este documento, seção 7 |
| Incidentes de segurança | LGPD, art. 48; Resolução CD/ANPD 15/2024 | [A] para o art. 48; [V] para o prazo | Runbook e comunicação | [07](07-privacidade-lgpd.md), seção 8 |
| Acessibilidade | Lei 13.146/2015 (Estatuto da Pessoa com Deficiência) | [A] para existência; [V] para o alcance em sites privados | WCAG 2.2 AA | [08](08-frontend-design-system.md), [24](24-operacao-continuidade-qualidade.md), seção 7 |
| Comunicação por canais | LGPD; regras de uso das plataformas de mensagem | [A] para LGPD; [V] para regras de plataforma | Consentimento por canal | [22](22-crm-canais-e-papeis.md), seção 3 |

---

## 2. Princípios que o sistema adota

1. **Finalidade e necessidade** (LGPD, art. 6º): cada dado tem finalidade declarada. Dado sem finalidade não é coletado.
2. **Registro de tratamento** (LGPD, art. 37): toda operação relevante fica registrada.
3. **Prova de consentimento:** quando o consentimento é a base, o sistema guarda quem consentiu, quando, em que texto (versão), por qual canal e com qual evidência ([22](22-crm-canais-e-papeis.md), `crm_consents`).
4. **Responsabilidade clara:** a entidade é controladora dos dados de seus alunos e colaboradores. A plataforma é operadora quando trata esses dados em nome da entidade. Contrato de tratamento regula essa relação.

---

## 3. Matriz de retenção

Esta matriz define os prazos que o sistema aplica. Cada prazo tem base e grau de confiança. **Nenhum prazo [V] entra em produção sem confirmação.**

| Dado ou registro | Prazo proposto | Base | Confiança | Ação ao fim do prazo |
|---|---|---|---|---|
| Registro de acesso a aplicação (login, IP, sessão) | 6 meses | Marco Civil, art. 15 | [V] | Expurgo |
| Auditoria de consulta por CPF | **24 h (decisão do autor), conflito a resolver** | LGPD, art. 37; [P] | [P] | Expurgo com registro. Ver [25](25-dossie-juridico-e-lacunas.md), Q-01. |
| Registro de tratamento de dados (LGPD, art. 37) | Durante o tratamento e o prazo de prescrição aplicável | LGPD, art. 37 | [V] | Expurgo |
| Prova de consentimento | Enquanto houver tratamento que o consentimento fundamenta, mais o prazo de prescrição | LGPD, art. 8º, §2º | [V] | Expurgo |
| Contrato e cobrança de consumo | 5 anos após o fim do contrato | Prescrição de pretensão de consumo, CDC, art. 27 | [V] | Expurgo ou arquivo |
| Documentos fiscais e de nota | 5 anos | CTN, art. 195 | [V] | Expurgo |
| Documentos trabalhistas | Durante o contrato e 2 anos após o fim (prescrição); FGTS, 30 anos | CF, art. 7º, XXIX; Súmula 362 do TST | [A] para prescrição; [V] para o FGTS | Expurgo ou arquivo |
| ASO, prontuário de saúde ocupacional | 20 anos após o desligamento | NR-7 | [V] | Arquivo com acesso restrito |
| Histórico e registro de vida escolar | Permanente, conforme norma do sistema de ensino | LDB e normas estaduais ou municipais | [V] | Arquivo com acesso restrito |
| Dados de matrícula sem vínculo ativo | Conforme a norma de ensino; depois, expurgo ou anonimização | LGPD, art. 16 | [V] | Anonimização |
| Lead sem consentimento de contato | Até a revogação ou 1 ano sem interação | LGPD, art. 16 | [P] | Expurgo |
| Backup | Conforme [24](24-operacao-continuidade-qualidade.md), seção 1 | Proporcionalidade | [P] | Expurgo com prazo de expiração |

Regras gerais:

- Expurgo e arquivamento são registrados, sem guardar o dado expurgado.
- Dado sob bloqueio legal não é expurgado, mesmo vencido o prazo.
- Dado retido por obrigação legal fica com acesso restrito e finalidade única.

---

## 4. Relação de consumo e cobrança

### 4.1 Contrato e cláusulas

- Contrato de adesão deve ter redação clara e destaque para cláusulas que limitem direitos (CDC, art. 54, §4º) [A].
- Cláusula de rescisão, multa e reajuste devem estar no contrato e na área do cliente, com histórico [A].
- Prática abusiva é vedada (CDC, art. 39) [A]. Exemplo: exigir vantagem sem causa ou condicionar serviço a aceite de cobrança indevida.

### 4.2 Direito de arrependimento em venda online

Quando a matrícula ou a assinatura é contratada fora do estabelecimento, o consumidor tem sete dias para desistir, sem custo (CDC, art. 49) [A]. O sistema:

- Mostra o prazo no fluxo de contratação.
- Registra a data da contratação e a data da desistência.
- Gera estorno integral dentro do prazo do meio de pagamento ([20](20-pagamentos-seguranca.md), seção 11).

### 4.3 Multa, juros e reajuste de mensalidade

- Multa moratória em relação de consumo tem limite de 2% (CDC, art. 52, §1º) [A].
- Anuidades e mensalidades escolares têm regras próprias de reajuste e de cobrança de encargos (Lei 9.870/1999) [V]. O sistema aplica os limites da norma como padrão, e o tenant não pode ultrapassá-los.
- Juros de mora e correção seguem a regra do contrato, dentro dos limites legais [V].

### 4.4 Negativação e comunicação prévia

- A abertura de cadastro de inadimplente exige comunicação por escrito ao consumidor antes da inclusão (CDC, art. 43, §2º) [A].
- O sistema envia a comunicação e registra a data e o canal. A inclusão só ocorre depois do prazo de comunicação, que o jurídico confirma [V].
- Consulta a cadastro de inadimplentes sem finalidade legítima é vedada. Ver [21](21-busca-e-armazenamento.md), seção 6.8, para a regra de finalidade.

### 4.5 Superendividamento e renegociação

- Antes de bloqueios e negativação, o sistema oferece renegociação com plano de pagamento (Lei 14.181/2021) [A para a existência; V para a aplicação à régua].
- Renegociação registra as condições, o consentimento do consumidor e o histórico.

### 4.6 Bloqueio de serviço

- Bloqueio total do portal por inadimplência é vedado para serviço educacional essencial e para menor de idade. O sistema aplica bloqueio parcial: documentos obrigatórios, matrícula de rematrícula e comunicação com a família continuam acessíveis [P].
- Documentos escolares não são retidos como forma de cobrança sem previsão legal [V].

---

## 5. Consentimento e comunicação por canal

| Canal | Base para contato comercial | Base para cobrança | Prova exigida | Observação |
|---|---|---|---|---|
| E-mail | Consentimento [A] | Execução de contrato [V] | Registro do aceite e da versão | Link de descadastro obrigatório em marketing |
| SMS | Consentimento [A] | Execução de contrato [V] | Registro do aceite | Número verificado |
| WhatsApp | Consentimento e regras da plataforma [V] | Execução de contrato [V] | Registro do opt-in | Não enviar mensagem proativa sem opt-in ([22](22-crm-canais-e-papeis.md), seção 3) |
| Telegram | Consentimento e regras da plataforma [V] | Execução de contrato [V] | Registro do opt-in | Mesmo tratamento do WhatsApp |
| Instagram e Messenger | Consentimento e regras da plataforma [V] | Não usado para cobrança | Registro do opt-in | Só conversa iniciada pelo usuário |
| Telefone | Consentimento [A] | Execução de contrato [V] | Aviso de gravação e registro | Gravação só com aviso |

Regras:

- Revogação é tão fácil quanto a concessão. Efeito imediato.
- Menor de idade: consentimento do responsável, específico e em destaque (LGPD, art. 14) [A].
- Mensagem de cobrança segue o horário permitido pelo tenant e o limite de frequência ([18](18-regras-modulos-2.md), seção 2.6).

---

## 6. Educação e documentos escolares

- Matrícula de menor exige a documentação do responsável, com validação do vínculo ([17](17-regras-modulos.md), seção 4) [V para exigências específicas].
- Registros escolares são guardados pelo prazo da norma do sistema de ensino da entidade. Cada entidade informa a norma aplicável e o sistema grava a referência [V].
- Entidade que atende sistemas de ensino diferentes (federal, estadual, municipal) configura a norma por unidade, porque a unidade é a unidade de ensino.
- Documento escolar não é retido como garantia de pagamento [V].

---

## 7. Assinatura e contratos eletrônicos

- Assinatura eletrônica tem três níveis, pela Lei 14.063/2020 [A]:
  - **Simples:** para atos sem exigência de identificação forte. Usada para termos internos e aceites de baixo risco.
  - **Avançada:** identifica o signatário com vínculo, com registro de dados do ato. Usada para contratos de adesão e para matrícula.
  - **Qualificada:** usa certificado ICP-Brasil (MP 2.200-2/2001). Usada para documentos que exigem essa forma, e para os que o contrato exigir [A].
- Cada assinatura guarda o documento, o hash, o momento, o identificador do signatário e a trilha de autenticação.
- Documento assinado não é alterado. Mudança gera aditivo ([17](17-regras-modulos.md), seção 7).

---

## 8. Incidentes de segurança

- Comunicação à ANPD e ao titular quando houver risco ou dano relevante (LGPD, art. 48) [A].
- Prazo de comunicação à ANPD: a Resolução CD/ANPD 15/2024 fixa o prazo em três dias úteis [V]. O runbook usa esse prazo como referência até confirmação.
- A comunicação segue o formulário da ANPD e registra as medidas adotadas.
- Incidente que envolve dado de pagamento aciona também o provedor e a equipe de conformidade ([20](20-pagamentos-seguranca.md), seção 17).

---

## 9. Acessibilidade

- Estatuto da Pessoa com Deficiência (Lei 13.146/2015) estabelece a acessibilidade digital como obrigação em sites e serviços [A para existência; V para o alcance nas relações privadas].
- O sistema adota WCAG 2.2 nível AA ([24](24-operacao-continuidade-qualidade.md), seção 7), o que cobre a referência técnica usual.
- Entidade que contrata a plataforma pode exigir nível superior, sem que o sistema reduza o mínimo.

---

## 10. Pagamentos e arranjo

- Operar arranjo de pagamento, em que a plataforma recebe e repassa valores, depende de autorização conforme a Lei 12.865/2013 e as normas do Banco Central [A para a lei; V para o enquadramento].
- O modelo padrão do SDD não recebe valores por conta própria: o tenant tem conta no gateway ([20](20-pagamentos-seguranca.md), seção 2). Essa escolha é a principal proteção regulatória do projeto.
- Qualquer mudança para recebimento pela plataforma exige parecer prévio ([25](25-dossie-juridico-e-lacunas.md), Q-07).
- O SDD não trata de tributação de pagamento além da NFSe. Qualquer retenção de tributo na fonte deve ser validada por contador [V].

---

## 11. Fiscal

- Nota fiscal de serviço segue o ISS do município (LC 116/2003) [A]. Cada município tem integração própria ([16](16-integracoes-externas.md), seção 3).
- Guarda de documentos fiscais: 5 anos (CTN, art. 195) [V].
- Cancelamento de nota segue as regras do município e registra o motivo.

---

## 12. Trabalho e saúde ocupacional

- Programas de SST: PCMSO (NR-7) e gerenciamento de riscos (NR-1) [V para o alcance e as datas de vigência].
- Registros de eSocial de saúde e segurança (S-2220, S-2230, S-2240) seguem o leiaute vigente [V].
- Dado de saúde ocupacional é sensível (LGPD, art. 11). Acesso restrito a profissional responsável ([17](17-regras-modulos.md), seção 5).
- Colaborador tem acesso ao próprio ASO e aos seus registros de SST.

---

## 13. Contratos da plataforma

| Contrato | Conteúdo mínimo | Confiança |
|---|---|---|
| Termos de uso | Responsabilidades, uso aceitável, suspensão, foro | [A] |
| Contrato de cliente (entidade) | Escopo, SLA, preço, saída, responsabilidades | [A] |
| Contrato de tratamento (operador) | Finalidade, instruções, subcontratados, incidentes, eliminação | [A] |
| Política de privacidade | Dados por canal, finalidades, bases, direitos | [A] |
| Política de cookies | Lista de cookies, finalidade, consentimento | [A] |
| Licença de componentes | Termos de uso do ícone e de bibliotecas, incluindo Font Awesome Pro | [A] para existência; [V] para o alcance da hospedagem |

---

## 14. Perguntas em aberto para o jurídico

Estas perguntas completam as de [25](25-dossie-juridico-e-lacunas.md). Quando a resposta vier, este documento é atualizado.

| # | Pergunta | Referência no SDD |
|---|---|---|
| J-01 | Confirmar o prazo de 6 meses dos registros de acesso e a aplicação ao sistema | Seção 3 |
| J-02 | Confirmar o prazo de comunicação prévia de negativação e a forma | Seção 4.4 |
| J-03 | Confirmar limites de reajuste e de encargos em anuidades (Lei 9.870/1999) | Seção 4.3 |
| J-04 | Confirmar a norma de guarda do histórico escolar por tipo de entidade | Seção 6 |
| J-05 | Confirmar o alcance da acessibilidade digital em relação privada | Seção 9 |
| J-06 | Confirmar a necessidade de autorização para arranjo de pagamento no modelo com split | Seção 10 |
| J-07 | Confirmar o prazo de comunicação à ANPD vigente | Seção 8 |
| J-08 | Confirmar o alcance da licença de componentes de interface em aplicação hospedada | Seção 13 |

---

## 15. Critérios de aceite

- [ ] Cada linha da seção 1 tem controle implementado e referência no SDD.
- [ ] Nenhum prazo [V] ou [P] da seção 3 é usado em produção sem confirmação.
- [ ] Contratos da seção 13 revisados pelo jurídico.
- [ ] Respostas J-01 a J-08 registradas com data e responsável.
