# CRM do tenant (captação, pré-cadastro, inscrição)

- Portal: Gestão (`gestao.`)
- Área: Comercial e admissões
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13); especificação da v1 absorvida integralmente (seção 14)
- Fonte da v2: [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 1; [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 2.2; [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 3; [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 4.2; [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 6.2; [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 7; [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 8; [19](../../../docs/v2/19-regras-modulos-3.md), seção 6; [19](../../../docs/v2/19-regras-modulos-3.md), seção 15
- Fonte da v1: [spec_crm_funil_comercial.md](../../../docs/v2/anexo-v1/spec_crm_funil_comercial.md) (244 linhas); [spec_gestao_marketing_redes_sociais.md](../../../docs/v2/anexo-v1/spec_gestao_marketing_redes_sociais.md) (350 linhas) — absorvida integralmente na seção 14

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. A seção 14 é o texto integral da v1, guardado para que nenhum detalhe se perca; quando ela disser algo diferente das seções 1 a 13, vale a v2. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

CRM de captação de alunos da entidade: canais, leads, funil, formulário embutido, pré-cadastro e inscrição, separado do CRM da plataforma; inclui marketing e redes sociais.

## 3. Telas

- **Funil de captação** (kanban por estado do [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 6.2).
- **Leads** (DataTable).
- **Lead — detalhe** (drawer com interações e consentimentos).
- **Formulários embutidos** (editor e código de incorporação).
- **Campanhas e redes sociais** (lista e agenda).
- **Painel** (conversão por canal).

## 4. Permissões por portal (extraídas do SDD)

- O SDD não traz tabela por portal para este módulo; vale o escopo da seção 2 e os papéis abaixo.

## 5. Papéis

- `unit.commercial`: captação e proposta; não aprova desconto acima da alçada.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Dois CRMs, não um ([22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 1); consentimento por canal ([26](../../../docs/v2/26-sdd-juridico-regulatorio.md), seção 5).

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

### 13.1 [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 1

#### 1. Dois CRMs, não um

Existem dois CRMs com donos, leads e finalidades diferentes. Misturá-los seria erro de dados e de LGPD.

| Aspecto | CRM da plataforma (vendas do SaaS) | CRM do tenant (captação de alunos) |
|---|---|---|
| Quem vende | TotusTuus SoftCloud | Colégio, faculdade ou instituição (tenant) |
| Quem é o lead | Instituição ou empresa que pode contratar o SaaS | Aluno, responsável ou candidato |
| Dono dos dados (controlador, LGPD) | Plataforma | Tenant |
| Papel da plataforma sobre os dados | Controlador | Operadora, quando a plataforma executa o canal para o tenant |
| Funil | Pré-venda, demonstração, proposta, contrato, implantação | Interesse, contato, pré-cadastro, inscrição, documentos, matrícula |
| Dados pessoais típicos | Nome do decisor, e-mail corporativo, telefone comercial | Nome do aluno e do responsável, telefone, e-mail, série de interesse |
| Dados que nunca entram | Dado de aluno de tenant | Dado comercial da plataforma, preço negociado com outro tenant |
| Banco | **Banco master** (`totustuus.matriz.bd`) | **Banco da unidade** (um por entidade + unidade, ver [03](../../../docs/v2/03-dominio-tenancy.md), seção 1.1) |

**Regra de separação:** nenhum registro de tenant aparece no CRM da plataforma, e nenhum registro do CRM da plataforma aparece em tenant. A ligação entre os dois é apenas o contrato comercial.

**Operação pela plataforma de canal de tenant:** quando o chatbot da plataforma atende o aluno de um tenant, a plataforma atua como operadora. Isso exige contrato de tratamento de dados entre plataforma e tenant ([07](../../../docs/v2/07-privacidade-lgpd.md), seção 7).

### 13.2 [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 2.2

##### 2.2 CRM do tenant (captação de alunos)

| Canal | Entrada | Identidade capturada | Atendimento | Consentimento |
|---|---|---|---|---|
| Formulário embutido no site do tenant (iframe ou script) | Página do tenant, com origem permitida | Nome, telefone, e-mail, série de interesse | Equipe de admissões | Aceite com finalidade, na própria página |
| Chatbot WhatsApp do tenant | Número do tenant ([16](../../../docs/v2/16-integracoes-externas.md), D-07) | Número de telefone | Bot do tenant com handoff | Opt-in na primeira mensagem |
| Chatbot Telegram do tenant | Bot do tenant | Identificador e telefone, se fornecido | Bot com handoff | Opt-in |
| Chatbot Instagram do tenant | Conta do tenant | Identificador da conta | Bot com handoff | Opt-in |
| Chatbot Messenger do tenant | Página do tenant | Identificador da página | Bot com handoff | Opt-in |
| Telefone | Central do tenant | Número e nome | Atendente | Aviso de gravação |
| Presencial | Visita, feira, open day | Ficha de inscrição | Atendente | Termo de consentimento na ficha |

**Regra comum a todos os canais:** a captura começa só depois do aviso de finalidade. Lead sem consentimento de contato para a finalidade informada fica em estado `sem_consentimento` e não recebe mensagem de marketing.

### 13.3 [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 3

#### 3. Regras por canal

| Regra | Aplicação |
|---|---|
| Identificação de bot | O chatbot se identifica como automático na primeira mensagem e oferece transferência para humano. |
| Dados que o bot não coleta | Dado de saúde, CPF completo, número de cartão, senha e documento de imagem. Quando necessário para a matrícula, o coleta acontece em formulário autenticado. |
| Pagamento | Nenhum pagamento é feito no chat. O bot envia link de pagamento ([20](../../../docs/v2/20-pagamentos-seguranca.md)). |
| Opt-out | Palavra de saída reconhecida em todos os canais (`PARAR`, `SAIR`). Efeito imediato sobre marketing. |
| Horário e frequência | Limite de mensagens proativas por lead e por dia. Mensagem de cobrança segue a régua de [18](../../../docs/v2/18-regras-modulos-2.md), seção 2.6. |
| Transcrição | Guardada como interação do lead, com retenção configurável por tenant ([07](../../../docs/v2/07-privacidade-lgpd.md), seção 5). |
| Gravação de ligação | Só com aviso no início e registro do consentimento. |
| Mensagem de terceiro | Nunca encaminhar a conversa a outro lead ou a outro tenant. |
| Políticas das plataformas | Cada canal cumpre as regras de uso da plataforma de mensagens (WhatsApp Business, Telegram Bot API, Meta para Instagram e Messenger). Mudança de regra vira tarefa de adequação. |
| Chatbot com IA (D-18) | A IA responde **somente com base em fonte cadastrada** (catálogo de cursos, preços, calendário, FAQ aprovada). Pergunta fora da fonte não recebe resposta inventada: é encaminhada para humano. Preço, bolsa, prazo ou condição nunca saem de fonte não cadastrada. |
| Abertura de ticket sem IA (D-18) | Todo ponto de atendimento oferece a opção "Abrir ticket" por menu fixo, sem interpretação por IA. O ticket é criado no módulo de atendimento ([19](../../../docs/v2/19-regras-modulos-3.md), seção 7) com categoria escolhida no menu e texto digitado pelo contato, guardado como texto literal. Esse caminho funciona mesmo com IA desligada. |
| Injeção de instrução | Texto do lead é dado, nunca instrução ao bot. Teste contra tentativa de alterar o comportamento do bot ([05](../../../docs/v2/05-seguranca.md)). |

### 13.4 [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 4.2

##### 4.2 CRM do tenant

| Papel | Escopo | Pode | Não pode |
|---|---|---|---|
| Atendente de admissões | Leads da unidade | Atender, registrar interação, agendar visita | Exportar base, ver dado de matrícula de outro aluno |
| Coordenador de admissões | Leads de todas as unidades permitidas | Redistribuir, ver funil, configurar régua de contato | Alterar a finalidade de consentimento |
| Gestor comercial da entidade | Entidade | Ver indicadores, configurar canais | Ver dado pessoal além da lista de leads com permissão de exportação |
| Operador de bot do tenant | Conversas do canal | Atender e transferir | Editar a base de conhecimento do bot sem permissão |
| Responsável pela unidade | Unidade | Ver funil da unidade | Ver outra unidade |

### 13.5 [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 6.2

##### 6.2 CRM do tenant

Leads: `interessado` → `contatado` → `pre_cadastro` → `inscrito` → `documentos_pendentes` → `matriculado`.
Estado de saída: `desistente`, `sem_consentimento`, `duplicado`.

Regras:

- "Fechado perdido" exige motivo (preço, concorrência, sem vaga, timing ou outro), como já definido na v1.
- Lead `matriculado` nunca volta a `interessado`. Novo interesse gera novo lead, vinculado ao anterior.
- Vaga do curso é reservada só em `inscrito`, com bloqueio de concorrência ([15](../../../docs/v2/15-validacoes.md), seção 7).

### 13.6 [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 7

#### 7. Captura por formulário embutido

- Origem permitida: lista de domínios cadastrada por tenant. Outro domínio não recebe o envio.
- O formulário é carregado de origem da plataforma com `frame-ancestors` limitado aos domínios permitidos.
- Campos mínimos. A série de interesse é lista fechada.
- Proteção contra robô: desafio antes do envio, sem terceiro não aprovado.
- Aceite de finalidade e de contato antes do envio, com texto e versão registrados.
- Confirmação por e-mail ou WhatsApp quando marketing estiver marcado (duplo opt-in).
- Nenhum script de terceiro na página do formulário além dos aprovados ([08](../../../docs/v2/08-frontend-design-system.md), seção 2).

### 13.7 [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 8

#### 8. Dados

Tabelas mínimas. Todas com `tenant_id` (no CRM da plataforma, `tenant_id` aponta para a própria plataforma).

```sql
CREATE TABLE crm_leads (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36)     NOT NULL,
  tenant_id       CHAR(36)     NOT NULL,
  context         ENUM('plataforma','tenant') NOT NULL,
  origin_channel  ENUM('site','formulario','whatsapp','telegram','instagram','messenger','telefone','presencial','indicacao') NOT NULL,
  owner_uuid      CHAR(36)     NULL,
  unit_id         CHAR(36)     NULL,
  name            VARCHAR(150) NOT NULL,
  phone_e164      VARCHAR(20)  NULL,
  email           VARCHAR(254) NULL,
  email_hash      CHAR(64)     NULL,
  phone_hash      CHAR(64)     NULL,
  status          VARCHAR(40)  NOT NULL,
  lost_reason     VARCHAR(60)  NULL,
  created_at      DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  UNIQUE KEY uk_lead_uuid (uuid),
  INDEX idx_tenant_status (tenant_id, context, status),
  INDEX idx_tenant_phone (tenant_id, phone_hash),
  INDEX idx_tenant_email (tenant_id, email_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE crm_consents (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36)     NOT NULL,
  tenant_id       CHAR(36)     NOT NULL,
  lead_id         BIGINT UNSIGNED NOT NULL,
  purpose         ENUM('contato_comercial','marketing','admissao','cobranca','gravacao_ligacao') NOT NULL,
  channel         VARCHAR(20)  NOT NULL,
  text_version    VARCHAR(40)  NOT NULL,
  granted_at      DATETIME(6)  NOT NULL,
  revoked_at      DATETIME(6)  NULL,
  evidence_ref    VARCHAR(255) NULL,
  UNIQUE KEY uk_consent_uuid (uuid),
  INDEX idx_lead_purpose (tenant_id, lead_id, purpose),
  FOREIGN KEY (lead_id) REFERENCES crm_leads(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Notas:

- `email_hash` e `phone_hash` são HMAC com pepper, para deduplicação e busca exata ([15](../../../docs/v2/15-validacoes.md), seção 2). Dado em claro é cifrado conforme [05](../../../docs/v2/05-seguranca.md).
- Consentimento nunca é apagado. Revogação preenche `revoked_at`.
- Interações (mensagens, ligações, visitas) vão para tabela própria, com canal, direção e referência à transcrição. A transcrição segue a retenção do tenant.
- Deduplicação: mesmo `phone_hash` ou `email_hash` dentro do mesmo `tenant_id` e contexto gera alerta de possível duplicidade, sem fusão automática.

### 13.8 [19](../../../docs/v2/19-regras-modulos-3.md), seção 6

#### 6. CRM e funil comercial

| Entidade | Estados (DDL) | Regra |
|---|---|---|
| Lead | `new`, `contacted`, `qualified`, `disqualified`, `converted` | Conversão cria oportunidade. |
| Oportunidade | `open`, `won`, `lost` | `estimated_value DECIMAL(12,2)`, maior ou igual a zero. |
| Atividade | — | Vínculo obrigatório a lead ou oportunidade (linha 106). |

- "Fechado perdido" exige motivo obrigatório (linha 97): preço, concorrência, sem orçamento, timing ou outro.
- Lead convertido não volta a `new`.
- **Defeito:** sem `tenant_id` (T-01). Lead contém dado pessoal de terceiro. Base legal de contato comercial precisa de parecer ([07](../../../docs/v2/07-privacidade-lgpd.md)).

### 13.9 [19](../../../docs/v2/19-regras-modulos-3.md), seção 15

#### 15. Marketing e redes sociais

| Regra | Detalhe |
|---|---|
| Publicação | Campos de título, texto, rede, data e aprovação obrigatórios (linha 126). |
| Aprovação | Publicação só após aprovação de quem tem permissão (fluxo de aprovação). |
| Datas críticas | Bloqueadas para publicação (linha 214). |
| Palavras bloqueadas | Lista de termos que impede publicação (linha 282). |
| Contato | Bloquear, silenciar ou priorizar contato respeita consentimento ([07](../../../docs/v2/07-privacidade-lgpd.md)). |

**Defeito:** sem DDL (T-02). Sem tenant. **Resolvido em 04/11/2026:** DDL com `unidade_uuid` em [51](../../../docs/v2/51-ddl-modulos-novos.md), seção 19.

## 14. Conteúdo integral da v1 (absorvido)

### Fonte: spec_crm_funil_comercial.md

#### SPEC — Módulo CRM e Funil Comercial (Admissions Pipeline)
**Projeto:** TotusTuusSoftCloud — SaaS Multi-Entidade · Multi-Unidade · Multi-Usuário
**Módulo:** CRM / Sales Pipeline / Admissions
**Stack:** PHP 8 puro · MariaDB · Tailwind CSS 4.2 · Supabase · amCharts 5
**Padrão de ID:** `id` (ordenação) · `uuid` (interno) · `code` (externo)
**Status:** Draft — gap identificado (conecta Marketing → Processo Seletivo → Matrícula)

- Language Standard: Global English

---

##### 1. Objetivo

Centralizar a jornada comercial completa, do lead gerado (Marketing) até a conversão em cliente/aluno matriculado, com pipeline de vendas, metas por vendedor/unidade, forecast, follow-up automatizado e atribuição de origem. Preenche a lacuna entre o módulo de Marketing (que gera leads) e o módulo Acadêmico (que trata do Processo Seletivo já com candidato inscrito).

##### 2. Escopo funcional

- Cadastro e qualificação de leads.
- Pipeline de oportunidades (kanban multi-etapa configurável).
- Atribuição automática de leads por regra (round-robin, território, origem).
- Atividades comerciais: ligações, e-mails, reuniões, tarefas.
- Metas e comissionamento por vendedor/unidade.
- Forecast de conversão e receita.
- Campanhas e origem de leads (integração com Marketing).
- Propostas comerciais e follow-up.
- Perda de oportunidade com motivo estruturado.
- Conversão para matrícula (handoff ao módulo Acadêmico) ou para contrato (handoff ao módulo Contratos).

##### 3. Perfis de acesso

| Perfil | Permissões |
|---|---|
| Gestor Comercial | Visão total, metas, relatórios, redistribuição de leads |
| Vendedor/Consultor | Pipeline próprio, atividades, propostas |
| Marketing | Cadastro de campanhas, visão de origem de leads |
| Recepção/SDR | Qualificação inicial de leads (pré-vendas) |
| Financeiro | Consulta de propostas fechadas para faturamento |

##### 4. Páginas do módulo

```
/crm/dashboard
/crm/leads                    — Lista de leads (datatable)
/crm/leads/:uuid               — Ficha do lead / timeline
/crm/pipeline                  — Kanban de oportunidades
/crm/opportunities             — Lista de oportunidades (datatable)
/crm/opportunities/:uuid       — Detalhe da oportunidade
/crm/activities                — Agenda de atividades comerciais
/crm/proposals                 — Propostas emitidas
/crm/goals                     — Metas e comissionamento
/crm/campaigns                 — Campanhas e origem
/crm/reports                   — Relatórios de funil e conversão
/crm/settings                  — Pipelines, motivos de perda, regras de atribuição
```

##### 5. Dashboard

###### Widgets
- Total de leads no período.
- Leads não atribuídos.
- Oportunidades abertas.
- Taxa de conversão (lead → matrícula/venda).
- Ticket médio.
- Receita em pipeline (forecast).
- Atividades atrasadas.
- Tempo médio de ciclo de venda.

###### Charts
- Funil: Lead → Qualificado → Proposta → Negociação → Fechado.
- Linha: novos leads por semana/mês.
- Donut: leads por origem/campanha.
- Barras: conversão por vendedor.
- Barras: motivos de perda mais frequentes.

##### 6. Leads — Datatable

Colunas: nome · telefone/e-mail · origem · campanha · curso/produto de interesse · responsável · status (novo/em contato/qualificado/desqualificado/convertido) · data criação · última interação · ações.

###### Drawer CRUD — Lead
- Dados de contato · origem (orgânico/pago/indicação/evento) · campanha vinculada.
- Curso/produto/unidade de interesse.
- Responsável atribuído (manual ou automático por regra).
- Score de qualificação (BANT ou customizado).
- Histórico de interações (timeline).
- Botão "Converter em Oportunidade".

##### 7. Pipeline — Kanban de Oportunidades

###### Colunas (configuráveis por pipeline)
Novo → Qualificação → Proposta Enviada → Negociação → Fechado Ganho → Fechado Perdido

###### Card
- Nome do lead/empresa · valor estimado · responsável · próxima atividade agendada · dias na etapa · badge de prioridade.

###### Regras
- Drag and drop com log de transição de etapa.
- Etapa "Fechado Perdido" exige motivo obrigatório (select configurável: preço, concorrência, sem orçamento, timing, outro).
- Etapa "Fechado Ganho" dispara automação de handoff (matrícula ou contrato).
- Múltiplos pipelines por tipo de produto/unidade (ex.: pipeline Educação Básica vs. pipeline Cursos Livres).

##### 8. Atividades Comerciais

- Tipos: ligação, e-mail, reunião, WhatsApp, tarefa.
- Agenda por vendedor com lembretes.
- Registro de resultado da atividade (contato feito/não atendeu/reagendado).
- Vínculo obrigatório a um lead ou oportunidade.

##### 9. Propostas Comerciais

- Geração de proposta em PDF a partir de template configurável.
- Itens de proposta com valores, descontos e condições.
- Status: rascunho / enviada / visualizada / aceita / recusada / expirada.
- Assinatura eletrônica opcional (integração com módulo de Contratos).

##### 10. Metas e Comissionamento

- Meta mensal/trimestral por vendedor e por unidade.
- Acompanhamento de realizado vs. meta (gauge/progress).
- Regra de comissão configurável (percentual fixo, escalonado, por produto).
- Relatório de comissão a pagar (integração com Financeiro/RH).

##### 11. Campanhas e Origem

- Cadastro de campanhas com custo, período e canal.
- Cálculo de CAC (custo de aquisição) por campanha.
- Vínculo com módulo de Marketing (UTM, tags de origem).

##### 12. Automações

- Atribuir lead automaticamente por regra (round-robin, território, disponibilidade).
- Notificar vendedor de lead sem contato em X horas (SLA de primeiro atendimento).
- Mover oportunidade para "Perdido" automaticamente após N dias sem atividade.
- Disparar e-mail de nutrição para leads não qualificados.
- Ao "Fechado Ganho", criar matrícula (Acadêmico) ou contrato (Contratos) automaticamente com dados da oportunidade.
- Alertar gestor quando meta do vendedor estiver em risco (< 70% aos 20 dias do período).

##### 13. Integrações

- **Marketing**: origem de lead, campanhas, UTM.
- **Acadêmico**: handoff para Processo Seletivo/Matrícula ao fechar oportunidade educacional.
- **Contratos**: handoff para geração de contrato ao fechar oportunidade B2B.
- **Financeiro/Billing**: geração de proposta que vira fatura/assinatura.
- **Notificações**: lembretes de atividade, alertas de SLA.
- **Auditoria**: mudança de etapa, atribuição, perda e conversão.

##### 14. Modelo de dados mínimo

```sql
CREATE TABLE crm_leads (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  code VARCHAR(30) NOT NULL UNIQUE,
  entity_id BIGINT UNSIGNED NOT NULL,
  unit_id BIGINT UNSIGNED,
  name VARCHAR(150) NOT NULL,
  email VARCHAR(150),
  phone VARCHAR(30),
  source VARCHAR(60),
  campaign_id BIGINT UNSIGNED NULL,
  interest_product VARCHAR(150),
  owner_user_id BIGINT UNSIGNED,
  score TINYINT UNSIGNED DEFAULT 0,
  status ENUM('new','contacted','qualified','disqualified','converted') DEFAULT 'new',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP,
  deleted_at DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE crm_opportunities (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  code VARCHAR(30) NOT NULL UNIQUE,
  lead_id BIGINT UNSIGNED NOT NULL,
  pipeline_id BIGINT UNSIGNED NOT NULL,
  stage VARCHAR(60) NOT NULL DEFAULT 'new',
  estimated_value DECIMAL(12,2),
  owner_user_id BIGINT UNSIGNED,
  probability TINYINT UNSIGNED DEFAULT 0,
  expected_close_date DATE,
  status ENUM('open','won','lost') DEFAULT 'open',
  lost_reason VARCHAR(120) NULL,
  closed_at DATETIME NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (lead_id) REFERENCES crm_leads(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE crm_activities (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  opportunity_id BIGINT UNSIGNED NULL,
  lead_id BIGINT UNSIGNED NULL,
  type ENUM('call','email','meeting','whatsapp','task') NOT NULL,
  scheduled_at DATETIME,
  completed_at DATETIME NULL,
  outcome VARCHAR(100) NULL,
  owner_user_id BIGINT UNSIGNED,
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE crm_proposals (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  opportunity_id BIGINT UNSIGNED NOT NULL,
  total_value DECIMAL(12,2),
  status ENUM('draft','sent','viewed','accepted','declined','expired') DEFAULT 'draft',
  pdf_path VARCHAR(500),
  sent_at DATETIME NULL,
  responded_at DATETIME NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (opportunity_id) REFERENCES crm_opportunities(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE crm_goals (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
  owner_user_id BIGINT UNSIGNED NOT NULL,
  unit_id BIGINT UNSIGNED,
  period VARCHAR(7) NOT NULL COMMENT 'YYYY-MM',
  target_value DECIMAL(12,2) NOT NULL,
  achieved_value DECIMAL(12,2) DEFAULT 0,
  commission_rule JSON,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

##### 15. API REST (principais)

- `GET/POST /api/v1/crm/leads` · `POST /api/v1/crm/leads/{uuid}/convert`
- `GET/POST /api/v1/crm/opportunities` · `PATCH /api/v1/crm/opportunities/{uuid}/stage`
- `POST /api/v1/crm/opportunities/{uuid}/win` · `POST /api/v1/crm/opportunities/{uuid}/lose`
- `GET/POST /api/v1/crm/activities`
- `GET/POST /api/v1/crm/proposals` · `POST /api/v1/crm/proposals/{uuid}/send`
- `GET /api/v1/crm/goals` · `GET /api/v1/crm/reports/funnel`

##### 16. Critérios de aceite

- Lead flui do cadastro até a conversão sem perda de contexto.
- Kanban de pipeline reflete mudança de etapa com auditoria.
- Perda de oportunidade sempre exige motivo estruturado.
- Handoff automático para Acadêmico/Contratos funciona ao fechar "Ganho".
- Dashboard exibe funil e conversão em tempo real.
- Metas e comissão calculadas corretamente por vendedor/período.

### Fonte: spec_gestao_marketing_redes_sociais.md

#### Spec — Gestão de Marketing e Redes Sociais Integradas

- Language Standard: Global English
##### Objetivo
Definir o módulo completo de Marketing com redes sociais integradas, automação avançada, operação multicanal, governança corporativa e analytics em uma plataforma SaaS multi-empresa e multi-unidade.

##### Escopo
O módulo deve cobrir planejamento, produção, agendamento, publicação, monitoramento, interação, automação, relatórios e governança de marketing e social media em um único ecossistema operacional.

##### Princípios
- Operação omnichannel com visão unificada por empresa, unidade, canal e campanha.
- Execução rápida com datatables, drawers, Kanban e ações em massa.
- Automação orientada a eventos com rastreabilidade total.
- Governança com aprovação, auditoria, compliance e permissões granulares.
- Analytics acionável com widgets, charts e relatórios exportáveis.

##### Páginas do módulo
###### 1. Dashboard Executivo
Visão consolidada com KPIs, funil, performance por canal, alertas, aprovações pendentes e atalhos operacionais.

###### 2. Campanhas
Gestão completa de campanhas de marketing, mídia paga, inbound, outbound e campanhas sociais.

###### 3. Redes Sociais Integradas
Gestão de contas conectadas, publicações, interações, inbox unificada, escuta social e agendamento.

###### 4. Conteúdo e Ativos
Biblioteca de criativos, templates, vídeos, artes, documentos, versões e aprovações.

###### 5. Automação
Fluxos automáticos, regras, eventos, condições, ações, logs e testes.

###### 6. Calendário Editorial
Planejamento de conteúdos, campanhas, posts, stories, reels, lives e eventos.

###### 7. Kanban Operacional
Fluxos de produção, revisão, aprovação, publicação e follow-up.

###### 8. Leads e Conversão
Gestão de leads, qualificação, atribuição, origem, status e conversão.

###### 9. Relatórios e BI
Análises, comparativos, exportações, dashboards analíticos e agendamento de relatórios.

###### 10. Configurações e Governança
Integrações, permissões, tags, listas, compliance, auditoria e parâmetros gerais.

##### Dashboard Executivo
###### Objetivo
Oferecer visão rápida de desempenho e prioridades do marketing e social media.

###### Widgets obrigatórios
- Leads gerados hoje.
- Leads convertidos.
- Campanhas ativas.
- Posts agendados.
- Publicações com falha.
- Menções não respondidas.
- DMs pendentes.
- Aprovações aguardando.
- Orçamento consumido.
- ROI por canal.
- Taxa de abertura e clique.
- Engajamento por rede.

###### Charts
- Linha: evolução de leads, engajamento e conversões.
- Barras: performance por canal, campanha e unidade.
- Funil: jornada do lead.
- Rosca: distribuição por origem, status e rede social.
- Área: orçamento versus gasto ao longo do tempo.
- Heatmap: engajamento por dia e horário.
- Radar: comparação de canais sociais.

###### Controles
- Filtro por período.
- Filtro por empresa, unidade, usuário, canal, campanha e status.
- Comparação com período anterior.
- Atualização manual e automática.
- Exportação PDF, CSV e XLSX.

##### Campanhas
###### Objetivo
Gerenciar campanhas com ciclo completo de criação, aprovação, execução e análise.

###### DataTable
Colunas: nome, tipo, canal, objetivo, público, orçamento, gasto, conversões, ROI, status, responsável, início, fim, atualização, ações.

###### Drawer CRUD
Campos: nome, descrição, tipo, objetivo, canal, empresa, unidade, orçamento, datas, público, tags, responsáveis, mídia vinculada, UTM, aprovação.

###### Controles
- Criar, editar, duplicar e arquivar.
- Pausar e reativar.
- Enviar para aprovação.
- Vincular a posts e automações.
- Ações em massa.
- Observações e anexos.

###### Estados
Rascunho, Em revisão, Aprovada, Ativa, Pausada, Encerrada, Arquivada.

##### Redes Sociais Integradas
###### Objetivo
Centralizar contas sociais, publicações, interações e monitoramento.

###### Subpáginas
- Contas conectadas.
- Inbox unificada.
- Agendador de publicações.
- Social listening.
- Comentários e menções.
- Templates e respostas rápidas.
- Performance por rede.

###### DataTable — Contas Conectadas
Colunas: rede, conta, perfil, unidade, status da conexão, token, validade, permissões, última sincronização, ações.

###### DataTable — Publicações
Colunas: título, rede, tipo, campanha, agendamento, status, autor, aprovador, métricas, ações.

###### DataTable — Inbox Unificada
Colunas: origem, contato, mensagem, tipo, sentimento, prioridade, responsável, status, última interação, ações.

###### Drawer CRUD — Publicação
Campos: título, texto, mídia, legenda, hashtags, link, rede, data/hora, recorrência, campanha, unidade, aprovação, UTM, CTA.

###### Drawer CRUD — Conta
Campos: rede, nome da conta, URL, credenciais/tokens, permissões, webhook, status, unidade, observações.

###### Controles
- Conectar/desconectar conta.
- Renovar token.
- Agendar, publicar agora ou salvar rascunho.
- Reaproveitar conteúdo.
- Responder comentários e DMs.
- Criar resposta rápida.
- Marcar como lido, pendente ou resolvido.
- Transferir atendimento.
- Bloquear, silenciar ou priorizar contato.

###### Estados
Rascunho, Agendado, Em aprovação, Publicado, Falha, Reagendado, Arquivado.

##### Conteúdo e Ativos
###### Objetivo
Gerenciar toda a produção criativa reutilizável.

###### DataTable
Colunas: nome, tipo, formato, tamanho, campanha, versão, status, autor, aprovação, ações.

###### Controles
- Upload múltiplo.
- Pré-visualização.
- Versionamento.
- Aprovação e reprovação.
- Tags e categorias.
- Reutilização em campanhas e posts.

##### Automação
###### Objetivo
Permitir automações completas com eventos, condições e ações multicanal.

###### DataTable
Colunas: nome, gatilho, condição, ação, canal, status, execuções, sucesso, falhas, último disparo.

###### Drawer CRUD — Fluxo
Campos: nome, descrição, evento gatilho, filtros, condições, ramificações, ações, tempo de espera, retries, canal, unidade, aprovação, logs.

###### Gatilhos
- Lead criado.
- Lead qualificado.
- Comentário recebido.
- DM recebida.
- Menção detectada.
- Post publicado.
- Conteúdo aprovado.
- Campanha aprovada.
- Formulário enviado.
- Link clicado.
- Compra realizada.
- Carrinho abandonado.

###### Ações
- Responder automaticamente.
- Criar tarefa.
- Notificar equipe.
- Atribuir responsável.
- Mover Kanban.
- Registrar evento.
- Publicar conteúdo.
- Enviar e-mail, WhatsApp ou notificação.
- Escalar para humano.

###### Controles
- Testar fluxo.
- Ativar, pausar e duplicar.
- Versionar fluxos.
- Simular eventos.
- Ver logs e auditoria.
- Aprovação antes de ativação.

###### Estados
Rascunho, Em teste, Aguardando aprovação, Ativa, Pausada, Erro, Encerrada.

##### Calendário Editorial
###### Objetivo
Planejar publicações, campanhas e eventos por canal e unidade.

###### Controles
- Visões diária, semanal e mensal.
- Arrastar e soltar itens.
- Filtrar por rede, campanha, usuário e status.
- Bloquear datas críticas.
- Vincular ao fluxo de aprovação.
- Reagendar itens com falha.

###### Tipos de item
Post, story, reel, live, vídeo, campanha, evento, lembrete, ação promocional.

##### Kanban Operacional
###### Objetivo
Acompanhar execução de conteúdo, campanhas e aprovações.

###### Colunas sugeridas
Backlog, Em produção, Em revisão, Em aprovação, Agendado, Publicado, Medindo resultados, Encerrado.

###### Controles
- Drag and drop.
- WIP limit.
- Responsável por card.
- Comentários, anexos e checklist.
- Etiquetas e prioridade.
- Histórico de movimentações.

##### Leads e Conversão
###### Objetivo
Gerenciar captação, qualificação e conversão de leads.

###### DataTable
Colunas: nome, empresa, contato, origem, campanha, score, estágio, responsável, prioridade, último contato, próximo passo, status.

###### Drawer CRUD
Campos: nome, email, telefone, empresa, cargo, origem, campanha, tags, score, consentimento, observações, histórico.

###### Controles
- Importar e exportar.
- Deduplicar.
- Qualificar e converter.
- Reatribuir responsável.
- Registrar interações.

##### Relatórios e BI
###### Objetivo
Oferecer análises estratégicas e operacionais.

###### Charts
- Linha de tendência.
- Barras por canal.
- Funil de conversão.
- Rosca por rede social.
- Área de orçamento.
- Heatmap de engajamento.

###### Controles
- Drill-down.
- Filtros avançados.
- Comparação de períodos.
- Exportação agendada.
- Compartilhamento por permissão.

##### Configurações e Governança
###### Objetivo
Garantir padronização, segurança e rastreabilidade.

###### Controles
- Perfis de acesso.
- Permissões por ação e por canal.
- Trilhas de auditoria.
- Integrações externas.
- Webhooks e chaves de API.
- Lista de palavras bloqueadas.
- Regras de consentimento LGPD.
- Templates aprovados.
- Políticas de retenção.

##### Regras de negócio
- Todo registro deve pertencer a empresa e unidade.
- Toda publicação precisa de canal e status de execução.
- Toda automação precisa de log e versionamento.
- Toda interação social precisa de rastreabilidade.
- Alterações críticas exigem auditoria.
- Campanhas com orçamento acima do limite exigem aprovação.
- Exclusão física deve ser evitada; usar arquivamento ou soft delete.

##### Permissões sugeridas
- Visualizar.
- Criar.
- Editar.
- Excluir.
- Aprovar.
- Publicar.
- Responder interações.
- Gerenciar contas sociais.
- Executar automações.
- Gerenciar integrações.
- Exportar relatórios.
- Ver auditoria.

##### Integrações sugeridas
- Instagram.
- Facebook.
- LinkedIn.
- X.
- YouTube.
- TikTok.
- WhatsApp Business.
- CRM.
- E-mail marketing.
- Analytics.
- Webhooks.
- API pública.

##### Estrutura de navegação
- Dashboard.
- Campanhas.
- Redes Sociais.
- Conteúdo.
- Automação.
- Calendário.
- Kanban.
- Leads.
- Relatórios.
- Configurações.

##### Critérios de aceite
- Todas as páginas principais devem existir e estar funcionalmente completas.
- Social media deve permitir contas conectadas, inbox, publicação e monitoramento.
- Automações devem cobrir eventos, condições, ações e logs.
- Widgets e charts devem refletir dados em tempo real ou quase real.
- Kanban e drawers devem permitir operação sem troca de página.
- Relatórios devem exportar e comparar períodos.

##### Entregáveis esperados
- Especificação funcional completa.
- Estrutura de páginas e navegação.
- Lista de componentes UI.
- Regras de negócio e permissões.
- Fluxos de automação e status.
- Base para implementação frontend e backend.
