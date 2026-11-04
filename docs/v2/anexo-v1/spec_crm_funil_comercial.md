# SPEC — Módulo CRM e Funil Comercial (Admissions Pipeline)
**Projeto:** TotusTuusSoftCloud — SaaS Multi-Entidade · Multi-Unidade · Multi-Usuário
**Módulo:** CRM / Sales Pipeline / Admissions
**Stack:** PHP 8 puro · MariaDB · Tailwind CSS 4.2 · Supabase · amCharts 5
**Padrão de ID:** `id` (ordenação) · `uuid` (interno) · `code` (externo)
**Status:** Draft — gap identificado (conecta Marketing → Processo Seletivo → Matrícula)

- Language Standard: Global English

---

## 1. Objetivo

Centralizar a jornada comercial completa, do lead gerado (Marketing) até a conversão em cliente/aluno matriculado, com pipeline de vendas, metas por vendedor/unidade, forecast, follow-up automatizado e atribuição de origem. Preenche a lacuna entre o módulo de Marketing (que gera leads) e o módulo Acadêmico (que trata do Processo Seletivo já com candidato inscrito).

## 2. Escopo funcional

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

## 3. Perfis de acesso

| Perfil | Permissões |
|---|---|
| Gestor Comercial | Visão total, metas, relatórios, redistribuição de leads |
| Vendedor/Consultor | Pipeline próprio, atividades, propostas |
| Marketing | Cadastro de campanhas, visão de origem de leads |
| Recepção/SDR | Qualificação inicial de leads (pré-vendas) |
| Financeiro | Consulta de propostas fechadas para faturamento |

## 4. Páginas do módulo

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

## 5. Dashboard

### Widgets
- Total de leads no período.
- Leads não atribuídos.
- Oportunidades abertas.
- Taxa de conversão (lead → matrícula/venda).
- Ticket médio.
- Receita em pipeline (forecast).
- Atividades atrasadas.
- Tempo médio de ciclo de venda.

### Charts
- Funil: Lead → Qualificado → Proposta → Negociação → Fechado.
- Linha: novos leads por semana/mês.
- Donut: leads por origem/campanha.
- Barras: conversão por vendedor.
- Barras: motivos de perda mais frequentes.

## 6. Leads — Datatable

Colunas: nome · telefone/e-mail · origem · campanha · curso/produto de interesse · responsável · status (novo/em contato/qualificado/desqualificado/convertido) · data criação · última interação · ações.

### Drawer CRUD — Lead
- Dados de contato · origem (orgânico/pago/indicação/evento) · campanha vinculada.
- Curso/produto/unidade de interesse.
- Responsável atribuído (manual ou automático por regra).
- Score de qualificação (BANT ou customizado).
- Histórico de interações (timeline).
- Botão "Converter em Oportunidade".

## 7. Pipeline — Kanban de Oportunidades

### Colunas (configuráveis por pipeline)
Novo → Qualificação → Proposta Enviada → Negociação → Fechado Ganho → Fechado Perdido

### Card
- Nome do lead/empresa · valor estimado · responsável · próxima atividade agendada · dias na etapa · badge de prioridade.

### Regras
- Drag and drop com log de transição de etapa.
- Etapa "Fechado Perdido" exige motivo obrigatório (select configurável: preço, concorrência, sem orçamento, timing, outro).
- Etapa "Fechado Ganho" dispara automação de handoff (matrícula ou contrato).
- Múltiplos pipelines por tipo de produto/unidade (ex.: pipeline Educação Básica vs. pipeline Cursos Livres).

## 8. Atividades Comerciais

- Tipos: ligação, e-mail, reunião, WhatsApp, tarefa.
- Agenda por vendedor com lembretes.
- Registro de resultado da atividade (contato feito/não atendeu/reagendado).
- Vínculo obrigatório a um lead ou oportunidade.

## 9. Propostas Comerciais

- Geração de proposta em PDF a partir de template configurável.
- Itens de proposta com valores, descontos e condições.
- Status: rascunho / enviada / visualizada / aceita / recusada / expirada.
- Assinatura eletrônica opcional (integração com módulo de Contratos).

## 10. Metas e Comissionamento

- Meta mensal/trimestral por vendedor e por unidade.
- Acompanhamento de realizado vs. meta (gauge/progress).
- Regra de comissão configurável (percentual fixo, escalonado, por produto).
- Relatório de comissão a pagar (integração com Financeiro/RH).

## 11. Campanhas e Origem

- Cadastro de campanhas com custo, período e canal.
- Cálculo de CAC (custo de aquisição) por campanha.
- Vínculo com módulo de Marketing (UTM, tags de origem).

## 12. Automações

- Atribuir lead automaticamente por regra (round-robin, território, disponibilidade).
- Notificar vendedor de lead sem contato em X horas (SLA de primeiro atendimento).
- Mover oportunidade para "Perdido" automaticamente após N dias sem atividade.
- Disparar e-mail de nutrição para leads não qualificados.
- Ao "Fechado Ganho", criar matrícula (Acadêmico) ou contrato (Contratos) automaticamente com dados da oportunidade.
- Alertar gestor quando meta do vendedor estiver em risco (< 70% aos 20 dias do período).

## 13. Integrações

- **Marketing**: origem de lead, campanhas, UTM.
- **Acadêmico**: handoff para Processo Seletivo/Matrícula ao fechar oportunidade educacional.
- **Contratos**: handoff para geração de contrato ao fechar oportunidade B2B.
- **Financeiro/Billing**: geração de proposta que vira fatura/assinatura.
- **Notificações**: lembretes de atividade, alertas de SLA.
- **Auditoria**: mudança de etapa, atribuição, perda e conversão.

## 14. Modelo de dados mínimo

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

## 15. API REST (principais)

- `GET/POST /api/v1/crm/leads` · `POST /api/v1/crm/leads/{uuid}/convert`
- `GET/POST /api/v1/crm/opportunities` · `PATCH /api/v1/crm/opportunities/{uuid}/stage`
- `POST /api/v1/crm/opportunities/{uuid}/win` · `POST /api/v1/crm/opportunities/{uuid}/lose`
- `GET/POST /api/v1/crm/activities`
- `GET/POST /api/v1/crm/proposals` · `POST /api/v1/crm/proposals/{uuid}/send`
- `GET /api/v1/crm/goals` · `GET /api/v1/crm/reports/funnel`

## 16. Critérios de aceite

- Lead flui do cadastro até a conversão sem perda de contexto.
- Kanban de pipeline reflete mudança de etapa com auditoria.
- Perda de oportunidade sempre exige motivo estruturado.
- Handoff automático para Acadêmico/Contratos funciona ao fechar "Ganho".
- Dashboard exibe funil e conversão em tempo real.
- Metas e comissão calculadas corretamente por vendedor/período.
