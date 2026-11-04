# SST (segurança e medicina do trabalho)

- Portal: Gestão (`gestao.`)
- Área: Pessoas e RH
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13)
- Fonte da v2: [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 5; [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 7; [52](../../../docs/v2/52-medicina-do-trabalho-especificacao.md) (integral); [17](../../../docs/v2/17-regras-modulos.md), seção 5
- Fonte da v1: absorvida integralmente em [medicina-e-seguranca-do-trabalho-da-empresa.md](../../desenvolvedor/pessoas-da-plataforma/medicina-e-seguranca-do-trabalho-da-empresa.md) (mesma especificação, uma única cópia no kit)

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

ASO, exames, CAT, EPI, NR e PGR da unidade, com sigilo médico.

## 3. Telas

- **ASO e exames** (lista; resultado só pelo médico).
- **CAT** (registro).
- **EPI** (entregas).
- **PGR e NR** (documentos e prazos).

## 4. Permissões por portal (extraídas do SDD)

Do [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md):

| Portal | Departamento pessoal | Recursos humanos | Medicina e SST |
|---|---|---|---|
| Gestão | Completo, por permissão ([17](../../../docs/v2/17-regras-modulos.md), seção 3) | Completo, por permissão | Apto, inapto, restrição, EPI, NR, CAT, afastamento. **Sem CID nem prontuário** |

Do [52](../../../docs/v2/52-medicina-do-trabalho-especificacao.md):

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Gestão** | Ver PGR e plano de ação, ver CIPA e atas, ver o resultado de ASO sem motivo clínico, aprovar plano de ação | Ver CID, prontuário ou diagnóstico | E |

## 5. Papéis

- `unit.sst.doctor`: ASO completo, prontuário, CID.
- `unit.sst.technician`: CAT, EPI, NR, PGR; sem diagnóstico.
- RH e gestão veem só apto ou inapto, sem CID.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Medicina do trabalho ([52](../../../docs/v2/52-medicina-do-trabalho-especificacao.md)); permissões SST ([39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 7).

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

### 13.1 [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 5

#### 5. Medicina e segurança do trabalho

##### 5.1 Regra central de privacidade

**O RH e a gestão não veem diagnóstico, CID ou prontuário.** A v1 dá a eles a permissão "SST — Gerenciar" e mostra CID no cadastro de exame. Correção proposta:

| Papel | Vê | Não vê |
|---|---|---|
| Médico do trabalho | ASO completo, prontuário, CID, restrição detalhada | Nada de outros médicos sem vínculo |
| Técnico de segurança (SESMT) | Ocorrências, EPI, NR, PGR, CAT sem diagnóstico | CID, prontuário |
| RH e gestão | Apto, inapto ou apto com restrição; data de validade do ASO; restrição funcional **sem motivo clínico**; afastamento sem CID | CID, diagnóstico, prontuário |
| Colaborador | O próprio ASO e o próprio resultado | Dado de outro colaborador |
| Auditor | Acesso de leitura com motivo ([29](../../../docs/v2/29-auditoria.md), seção 5) | Conteúdo de dado de saúde |

**Base:** LGPD, art. 11, e o princípio de necessidade ([07](../../../docs/v2/07-privacidade-lgpd.md), seção 1). A CAT exige CID para o INSS, e isso é emitido pelo médico, não pela gestão **(verificar)**.

**Correção necessária na v1:** a permissão "SST — Gerenciar" deixa de ser concedida por nome de cargo a RH e gestão. Cada portal ou papel que precisa gerir SST recebe a sua própria permissão, limitada ao que esse papel faz (ver seção 11).

##### 5.2 Exames ocupacionais (ASO)

- Tipos: admissional, periódico, retorno ao trabalho, mudança de função e demissional ([17](../../../docs/v2/17-regras-modulos.md), seção 5.2).
- Vencimento calculado pelo tipo e pela NR aplicável **(verificar)**. Alerta aos 30 dias.
- ASO só é emitido por médico com CRM válido.

##### 5.3 PCMSO, PGR e LTCAT

**Ausentes na v2.** Proposta:

- **PCMSO:** programa anual, com exames e calendário por grupo de risco. Responsável médico.
- **PGR:** inventário de riscos por setor (GHE). Plano de ação com prazo e responsável. Versão vigente única por unidade.
- **LTCAT:** laudo técnico de exposição, com validade. Base de cálculo de adicional de insalubridade e aposentadoria especial **(verificar)**.

Estados do plano de ação: `aberto`, `em_andamento`, `concluido`, `vencido` (calculado, [17](../../../docs/v2/17-regras-modulos.md), seção 5.3).

##### 5.4 CAT, acidente e afastamento

- CAT com data não futura, testemunhas por CPF válido e ocorrência registrada ([17](../../../docs/v2/17-regras-modulos.md), seção 5.2).
- CID do acidente vai só para a CAT e para o médico.
- Afastamento gerado pela CAT é do RH ([14](../../../docs/v2/14-integracao-modulos.md), seção 2).
- Envio da CAT ao INSS **(verificar)** o canal e o prazo.

##### 5.5 EPI

Entrega com assinatura. CA com validade. Estoque não negativo ([17](../../../docs/v2/17-regras-modulos.md), seção 5.2). A entrega é registrada no HCM, e o estoque fica no Suprimentos ([18](../../../docs/v2/18-regras-modulos-2.md), seção 6).

##### 5.6 CIPA e ergonomia

**Ausentes.** Proposta: eleição, composição e atas da CIPA **(verificar)** conforme NR-5. Laudo de ergonomia com versão e responsável técnico.

##### 5.7 Treinamento em NR

Validade por NR, com alerta. Treinamento vencido bloqueia a função que exige a NR **(verificar)**.

### 13.2 [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 7

#### 7. Permissões

A matriz da v1 (seção 20 de [`spec_gestao_pessoas_completo.md`](../../../docs/v2/anexo-v1/spec_gestao_pessoas_completo.md)) é aproveitada, com estas correções:

| Permissão | v1 | Proposta |
|---|---|---|
| SST — Gerenciar | Por papel e portal que precisa (seção 11). RH e gestão não recebem essa permissão | SESMT e médico do trabalho, cada um com escopo próprio. RH e gestão só veem o resultado sem CID |
| Folha — Processar e aprovar | GE, GP, SA | Mantido. Quem processa não aprova ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5) |
| Ponto — Ajuste manual | RH e GP | Mantido, com motivo obrigatório |
| Audit Log | SA, GE, GP, AUD | Mantido. Leitura do audit log gera evento ([29](../../../docs/v2/29-auditoria.md), seção 5) |
| Holerite próprio | Todos | Mantido |

### 13.3 [52 — Medicina e Segurança do Trabalho: PCMSO, PGR, LTCAT, CIPA e Ergonomia](../../../docs/v2/52-medicina-do-trabalho-especificacao.md) (documento integral)

> Parte do [SDD v2](../../../docs/v2/00-README.md). Regras já existentes de ASO, CAT, EPI e NR em [17](../../../docs/v2/17-regras-modulos.md), seção 5, e análise por portal em [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 5. Dado de saúde e CID em [07](../../../docs/v2/07-privacidade-lgpd.md) e no padrão de [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 5.1. Armazenamento de laudo em [21](../../../docs/v2/21-busca-e-armazenamento.md). Auditoria em [29](../../../docs/v2/29-auditoria.md). Fecha HCM-07.
> **Status:** especificação proposta, criada em 03/11/2026. Os nomes e as exigências de cada programa (PCMSO, PGR, LTCAT, CIPA e ergonomia) vêm das normas regulamentadoras e da legislação previdenciária. Cada exigência marcada **(verificar)** precisa de conferência do responsável por norma antes da implementação ([50](../../../docs/v2/50-pacote-juridico-e-norma.md), seção 6).

---

#### 1. Resposta direta

| Programa | Base | O que o sistema faz | Dono |
|---|---|---|---|
| PCMSO | NR-7 **(verificar)** | Planeja e registra exames médicos ocupacionais por função e risco | Médico do trabalho |
| PGR | NR-1 e NR-9 **(verificar)** | Registra riscos ocupacionais, medidas de controle e plano de ação | SESMT e gestão |
| LTCAT | Previdência social **(verificar)** | Laudo técnico de exposição a agentes nocivos, com validade | SESMT |
| CIPA | NR-5 **(verificar)** | Eleição, composição, mandato e atas | Gestão e empregados |
| Ergonomia | NR-17 **(verificar)** | Análise ergonômica do posto e recomendações | SESMT |

---

#### 2. PCMSO

- **Programa anual**, com cronograma de exames por função e por exposição.
- Exames previstos: admissional, periódico, de retorno ao trabalho, de mudança de função e demissional (regras já em [17](../../../docs/v2/17-regras-modulos.md), seção 5.2).
- **Vencimento** de cada exame é calculado pela periodicidade da NR-7, item 7.5.8. Alerta aos 30 dias. Conferido em 03/11/2026 no texto oficial da NR-7 (gov.br, versão atualizada de 2022):

| Exame | Prazo |
|---|---|
| Admissional | Antes de o empregado assumir as atividades (7.5.8, I) |
| Periódico, exposto a risco do PGR ou com doença crônica que aumente a suscetibilidade | A cada ano ou em intervalo menor, a critério do médico responsável (7.5.8, II, a) |
| Periódico, demais empregados | A cada dois anos (7.5.8, II, b) |
| Retorno ao trabalho | Antes de reassumir, quando ausente por 30 dias ou mais por doença ou acidente, ocupacional ou não (7.5.9) |
| Mudança de risco | Antes da data da mudança (7.5.10) |
| Demissional | Até 10 dias após o término do contrato. Dispensado se o último exame clínico tiver menos de 135 dias (grau de risco 1 e 2) ou menos de 90 dias (grau de risco 3 e 4) (7.5.11) |
| Anexos da NR-7 | Periodicidade própria, por exemplo audiometria e espirometria, configurada por risco |

- **ASO:** emitido pelo médico que fez o exame e disponibilizado ao empregado, em papel quando ele pedir (7.5.19). Conteúdo mínimo: organização, nome, CPF e função do empregado, riscos do PGR, exames feitos, apto ou inapto, médico responsável pelo PCMSO e médico examinador (7.5.19.1). O ASO não traz diagnóstico. "Apto com restrição" é registro interno do sistema: no ASO, a aptidão para atividade específica é anotada quando a NR exigir (7.5.19.2).
- **Prontuário:** sob responsabilidade do médico responsável pelo PCMSO (7.6.1). A organização guarda por **no mínimo 20 anos após o desligamento**, salvo prazo diverso nos anexos (7.6.1.1). Na troca de médico, a organização transfere formalmente os prontuários ao sucessor (7.6.1.2). Prontuário eletrônico segue as exigências do Conselho Federal de Medicina (7.6.1.3).
- **Relatório analítico:** anual, pelo médico responsável pelo PCMSO, contado do último relatório (7.6.2).
- **Dispensa:** MEI, ME e EPP de grau de risco 1 e 2 que declararem as informações digitais e não tiverem exposição a agente físico, químico, biológico ou ergonômico ficam dispensadas do PCMSO, mas não dos exames nem do ASO (NR-1, 1.8.6 e 1.8.7.1).
- **Quem vê o quê:** o médico do trabalho acessa o prontuário e o CID. Gestão e RH veem só apto, inapto, apto com restrição e validade ([39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 5.1).
- Exame sem médico com CRM válido não é emitido.

Estados do exame: `agendado` → `realizado` → `apto`, `apto_com_restricao` ou `inapto`, e `vencido` calculado por data.

---

#### 3. PGR

- **Inventário de riscos** por setor e função: físico, químico, biológico, ergonômico, de acidentes e **fatores de risco psicossociais relacionados ao trabalho**, incluídos no GRO pela Portaria MTE nº 1.419/2024, com o capítulo 1.5 da NR-1 em vigor desde 26/05/2026.
- Cada risco tem **medida de controle**, responsável e prazo.
- **Plano de ação** com estados `aberto`, `em_andamento`, `concluido` e `vencido` (calculado por prazo, como em [17](../../../docs/v2/17-regras-modulos.md), seção 5).
- Revisão do PGR com data e versão. Versão vigente não muda, e mudança gera nova versão.
- **Prazo de revisão:** a avaliação de riscos é contínua e revista a cada dois anos, ou até 3 anos se a organização tiver certificação em sistema de gestão de SST (NR-1, 1.5.4.4.6 e 1.5.4.4.6.1). Revisão antecipada quando: medida de prevenção implantada, mudança de tecnologia, ambiente, processo ou organização do trabalho, medida ineficaz, acidente ou doença do trabalho, mudança de requisito legal, ou pedido justificado dos trabalhadores ou da CIPA. O sistema calcula o vencimento e abre a revisão quando um desses fatos é registrado.
- **Histórico:** o inventário fica atualizado, e o histórico das atualizações é guardado por no mínimo 20 anos (NR-1, 1.5.7.3.3 e 1.5.7.3.3.1).
- **Dispensa:** o MEI não elabora PGR (1.8.1), mas a contratante o inclui no próprio PGR quando ele atua nas dependências dela (1.8.1.1). ME e EPP de grau de risco 1 e 2 sem exposição a agente físico, químico ou biológico, que declararem as informações digitais, ficam dispensadas do PGR (1.8.4).
- Ocorrência ligada a um risco do inventário. Acidente de trabalho gera CAT ([39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md), seção 5).

---

#### 4. LTCAT

- Laudo por função e setor, com agentes nocivos, intensidade e tempo de exposição.
- **Validade:** a lei não fixa prazo de validade. A empresa mantém o laudo **atualizado**, sob pena da lei (Lei 8.213/1991, art. 58, § 3º). O sistema não calcula vencimento: abre revisão do laudo quando o PGR registra mudança de ambiente, processo ou agente, e lembra a revisão a cada ano como prática de controle. O laudo é expedido por médico do trabalho ou engenheiro de segurança do trabalho (art. 58, § 1º) e diz se há proteção coletiva ou individual que reduza o agente ao limite de tolerância (art. 58, § 2º).
- **PPP:** a empresa mantém o perfil profissiográfico atualizado e entrega cópia ao trabalhador na rescisão (art. 58, § 4º). A entrega por meio eletrônico pelo eSocial **(verificar)**.
- Base para adicional de insalubridade e para aposentadoria especial. Cálculo do adicional é do módulo de folha, a partir do laudo, não do laudo em si.
- O laudo guarda o responsável técnico e o registro profissional.

---

#### 5. CIPA

- Nome atual: **Comissão Interna de Prevenção de Acidentes e de Assédio** (NR-5, Portaria MTP nº 4.219/2022).
- **Composição:** por estabelecimento, com representantes da organização e dos empregados, conforme o Quadro I da NR-5 (5.4.1). Os representantes da organização são designados por ela (5.4.3). Estabelecimento fora do Quadro I e sem SESMT nomeia um representante da NR-5 entre os empregados (5.4.13). O MEI está dispensado (5.4.13.2). O número de membros por faixa vem do Quadro I e fica como tabela configurável, carregada a partir do texto oficial.
- **Mandato:** um ano, com uma reeleição (5.4.6). O eleito para cargo de direção não pode ser dispensado sem justa causa desde o registro da candidatura até um ano após o fim do mandato (5.4.12). O sistema marca essa estabilidade no vínculo, para o módulo de pessoal avisar antes de uma rescisão.
- **Eleição:** convocada pelo empregador pelo menos 60 dias antes do fim do mandato (5.5.1), e realizada pelo menos 30 dias antes (5.5.3, f). Inscrição individual por pelo menos 15 dias corridos (5.5.3, b). A eleição vale com participação de pelo menos um terço dos empregados. Abaixo disso, a votação é prorrogada (5.5.4 e 5.5.4.1).
- **Reuniões:** ordinárias mensais, em calendário prévio (5.6.1). Em ME e EPP de grau de risco 1 e 2, podem ser bimestrais (5.6.1.1). Extraordinária em acidente grave ou fatal, ou a pedido de uma das representações (5.6.4).
- **Treinamento:** 8, 12, 16 ou 20 horas, para grau de risco 1, 2, 3 ou 4, com no máximo 8 horas por dia (5.7.4 e 5.7.4.1). Feito antes da posse (5.7.1). Na CIPA em primeiro mandato, em até 30 dias da posse (5.7.1.1).
- **Ata** de cada reunião, assinada pelos presentes e disponível a todos os membros (5.6.3 e 5.6.3.1). Deliberações divulgadas a todos os empregados (5.6.3.2).
- Os encaminhamentos viram plano de ação do PGR, quando houver risco envolvido.
- Eleitor e candidato são empregados do quadro, com vínculo ativo na data da eleição.

---

#### 6. Ergonomia

- Análise do posto de trabalho com data, função, responsável técnico e recomendações.
- Recomendação vira ação do plano do PGR, com prazo.
- Afastamento por motivo ergonômico segue a regra de afastamento de [17](../../../docs/v2/17-regras-modulos.md), seção 5, sem CID para a gestão.

---

#### 7. Por portal

| Portal | Pode | Não pode | Origem |
|---|---|---|---|
| **Desenvolvedor** | Nada sobre dado de entidade | Ver PCMSO, PGR, LTCAT, CIPA ou laudo | P |
| **Gestão** | Ver PGR e plano de ação, ver CIPA e atas, ver o resultado de ASO sem motivo clínico, aprovar plano de ação | Ver CID, prontuário ou diagnóstico | E |
| **Médico do trabalho** | Gerir PCMSO, ASO, prontuário e CID dos pacientes da entidade | Ver prontuário de outra entidade | E |
| **SESMT (técnico de segurança)** | Gerir PGR, LTCAT, ergonomia, CAT, EPI e ocorrências, sem diagnóstico | Ver CID ou prontuário | E |
| **RH** | Ver apto, inapto, restrição e validade. Receber afastamento | Ver CID, diagnóstico ou prontuário | E |
| **Colaborador** | Ver o próprio ASO e o resultado | Ver dado de outro colaborador | E |
| **Membro da CIPA** | Ver a própria ata e as atas da CIPA | Ver dado de saúde | E |
| **Terceiros** | Clínica de ASO recebe o agendamento e devolve o resultado ([38](../../../docs/v2/38-portal-de-terceiros-prestadores.md)) | Ver PGR, CIPA ou outros colaboradores | E |

---

#### 8. Eventos e integrações

| Evento | Produtor | Consumidor | Efeito |
|---|---|---|---|
| `smt.exame.vencendo` | Medicina | Gestão e RH | Alerta de renovação |
| `smt.cat.criada` | SESMT | RH | Abre afastamento, conforme [14](../../../docs/v2/14-integracao-modulos.md) |
| `smt.exame.resultado` | Medicina | RH | Só apto, inapto, restrição e validade. Sem motivo clínico |

Eventos de SST não levam CID no payload ([14](../../../docs/v2/14-integracao-modulos.md), seção 8).

---

#### 9. DDL proposto

```sql
CREATE TABLE smt_pcmso_versoes (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  ano             SMALLINT UNSIGNED NOT NULL,
  versao          INT UNSIGNED NOT NULL,
  medico_uuid     CHAR(36) NOT NULL,
  crm_registro    VARCHAR(30) NOT NULL,
  estado          ENUM('rascunho','vigente','substituido') NOT NULL,
  UNIQUE KEY ux_pcmso_ano_versao (unidade_uuid, ano, versao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE smt_pgr_riscos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  setor           VARCHAR(120) NOT NULL,
  funcao          VARCHAR(120) NULL,
  tipo_risco      ENUM('fisico','quimico','biologico','ergonomico','acidente') NOT NULL,
  descricao       VARCHAR(500) NOT NULL,
  medida_controle VARCHAR(500) NOT NULL,
  responsavel_uuid CHAR(36) NOT NULL,
  prazo_em        DATE NULL,
  estado          ENUM('aberto','em_andamento','concluido') NOT NULL,
  versao_pgr      INT UNSIGNED NOT NULL,
  INDEX ix_risco_setor (unidade_uuid, setor, estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE smt_ltcat (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  funcao          VARCHAR(120) NOT NULL,
  agente_nocivo   VARCHAR(120) NOT NULL,
  intensidade     VARCHAR(60) NOT NULL,
  tempo_exposicao VARCHAR(60) NOT NULL,
  responsavel_tecnico_uuid CHAR(36) NOT NULL,
  registro_profissional VARCHAR(30) NOT NULL,
  emitido_em      DATE NOT NULL,
  valido_ate      DATE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE smt_cipa_mandatos (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  inicio_em       DATE NOT NULL,
  fim_em          DATE NOT NULL,
  estado          ENUM('eleicao','vigente','encerrado') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE smt_cipa_membros (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  mandato_id      BIGINT UNSIGNED NOT NULL,
  pessoa_uuid     CHAR(36) NOT NULL,
  papel           ENUM('titular','suplente','presidente','vice','secretario') NOT NULL,
  representacao   ENUM('empregador','empregados') NOT NULL,
  UNIQUE KEY ux_cipa_membro (mandato_id, pessoa_uuid),
  CONSTRAINT fk_cipa_mandato FOREIGN KEY (mandato_id) REFERENCES smt_cipa_mandatos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE smt_cipa_atas (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  mandato_id      BIGINT UNSIGNED NOT NULL,
  realizada_em    DATETIME(3) NOT NULL,
  pauta           TEXT NOT NULL,
  encaminhamentos TEXT NULL,
  arquivo_uuid    CHAR(36) NULL,
  CONSTRAINT fk_ata_mandato FOREIGN KEY (mandato_id) REFERENCES smt_cipa_mandatos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE smt_ergonomia_analises (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36) NOT NULL UNIQUE,
  unidade_uuid    CHAR(36) NOT NULL,
  funcao          VARCHAR(120) NOT NULL,
  analisado_em    DATE NOT NULL,
  responsavel_tecnico_uuid CHAR(36) NOT NULL,
  recomendacoes   TEXT NOT NULL,
  plano_risco_uuid CHAR(36) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

#### 10. Pendências

| # | Pendência | Tipo |
|---|---|---|
| SST-01 | Periodicidade de exames por função e risco (seção 2) | **Conferido** em 03/11/2026: NR-7, itens 7.5.8 a 7.5.11 |
| SST-02 | Validade do LTCAT e alerta (seção 4) | **Conferido** em 03/11/2026: sem prazo fixo, laudo mantido atualizado (Lei 8.213/1991, art. 58). PPP pelo eSocial **(verificar)** |
| SST-03 | Eleição e composição da CIPA por porte da entidade (seção 5) | **Conferido** em 03/11/2026: NR-5, itens 5.4 a 5.7. Os números do Quadro I entram como tabela configurável |
| SST-04 | Forma de atualização do PGR e prazo de revisão (seção 3) | **Conferido** em 03/11/2026: NR-1, itens 1.5.4.4.6 e 1.5.7.3.3 |
| SST-05 | Revisão de prazo de guarda de PCMSO e de prontuário (HCM-08) | Norma conferida em 03/11/2026: 20 anos após o desligamento (NR-7, 7.6.1.1). Parecer do (jurídico) sobre outros documentos de SST pendente |

---

#### 11. Critérios de aceite

- [ ] Perfil de RH e de gestão não recebe CID nem prontuário (varredura de resposta, já em [39](../../../docs/v2/39-departamento-pessoal-rh-medicina-por-portal.md)).
- [ ] Exame sem médico com CRM válido não é emitido (teste).
- [ ] Laudo de LTCAT vencido gera alerta (teste).
- [ ] Versão vigente de PGR não é alterada, e revisão gera nova versão (teste).
- [ ] Ata da CIPA é visível só aos membros e à gestão (teste de isolamento).

### 13.4 [17](../../../docs/v2/17-regras-modulos.md), seção 5

#### 5. SMT (Segurança e Medicina do Trabalho)

##### 5.1 Entidades

Funcionário e ASO, PCMSO, PGR/GHE, LTCAT, CAT, EPI, treinamentos NR, afastamentos, CIPA.

##### 5.2 Campos e regras (v1, seções 4 a 12)

| Campo | Regra |
|---|---|
| Ficha de saúde | Dado sensível. Criptografado. Acesso restrito a profissional de saúde e ao próprio colaborador. |
| ASO | Tipo (admissional, periódico, retorno, mudança, demissional) obrigatório. Resultado somente por profissional responsável. |
| CAT | Data do acidente não futura. Testemunhas por CPF válido. Emissão exige ocorrência registrada. |
| EPI | CA com validade. Entrega com registro de assinatura (FIEPI). Estoque não negativo. |
| Treinamento NR | Validade obrigatória quando a NR exige reciclagem. |
| Afastamento | Data fim não anterior à início. Sobreposição com afastamento ativo é recusada. |
| GHE | Pertence a um PGR ativo do tenant. |

##### 5.3 Estados

| Entidade | Estados |
|---|---|
| CAT | `emitida`, `em_investigacao`, `encerrada` |
| EPI (entrega) | `entregue`, `devolvido`, `extraviado` |
| Plano de ação | `aberto`, `em_andamento`, `concluido`, `vencido` (calculado por prazo) |

##### 5.4 Integrações

- SMT consome `hcm.employee.created` para agendar exame admissional.
- SMT publica `smt.exam.performed`, `smt.cat.created`, `smt.training.expired` ([14](../../../docs/v2/14-integracao-modulos.md), seção 4).
- Transmissão de eSocial (S-2220, S-2230, S-2240) conforme decisão D-08 ([16](../../../docs/v2/16-integracoes-externas.md), seção 6).
