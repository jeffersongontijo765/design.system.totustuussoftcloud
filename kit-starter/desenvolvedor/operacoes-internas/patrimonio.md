# Patrimônio da empresa

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Operações internas
- Domínio: plataforma (banco master), instância separada do módulo das entidades ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2.1)
- Status: detalhado; especificação da v1 absorvida integralmente (seção 13), com as correções da v2 e as decisões por padrão (seções 1 a 12)
- Fonte da v1: [spec_patrimonio_completo.md](../../../docs/v2/anexo-v1/spec_patrimonio_completo.md) (1309 linhas)

## 1. Regra de leitura
As seções 1 a 12 prevalecem sobre a seção 13. A seção 13 é o texto integral da v1, sem corte, para que nenhum detalhe se perca. Quando a seção 13 disser algo diferente das seções 1 a 12, vale o que está nas seções 1 a 12.

## 2. Objetivo e escopo
Controlar os bens da própria empresa desenvolvedora: cadastro, depreciação, manutenção, transferência, inventário, descarte e seguros.

## 3. Telas (índice da v1)
- Índice
- 1. Visão Geral
  - Subdomínios
- 2. Perfis e Permissões (RBAC)
- 3. Schema do Banco de Dados
  - 3.1 Tabela `pat_asset_categories`
  - 3.2 Tabela `pat_assets`
  - 3.3 Tabela `pat_depreciation_runs`
  - 3.4 Tabela `pat_depreciation_entries`
  - 3.5 Tabela `pat_maintenances`
  - 3.6 Tabela `pat_transfers`
  - 3.7 Tabela `pat_inventories`
  - 3.8 Tabela `pat_inventory_items`
  - 3.9 Tabela `pat_disposals`
  - 3.10 Tabela `pat_insurances`
  - 3.11 Tabela `pat_insurance_assets`
  - 3.12 Tabela `pat_locations`
- 4. Páginas e Componentes
  - 4.1 Dashboard — Patrimônio
  - 4.2 Cadastro de Ativos
  - 4.3 Depreciação
  - 4.4 Manutenção
  - 4.5 Transferências
  - 4.6 Inventário
  - 4.7 Descarte / Alienação
  - 4.8 Seguros
  - 4.9 Kanban — Manutenção
  - 4.10 Relatórios
- 5. Automações
  - 5.1 Depreciação Automática Mensal
  - 5.2 Alerta de Garantia a Vencer
  - 5.3 Alerta de Seguro a Vencer
  - 5.4 Manutenção Preventiva Recorrente
  - 5.5 Alerta de Ativo em Estado Crítico
  - 5.6 Inventário Periódico Automático
  - 5.7 Contabilização Automática de Depreciação
- 6. Integrações
- 7. API REST — Endpoints
  - Assets
  - Depreciação
  - Manutenção
  - Transferências
  - Inventário
  - Descarte
  - Seguros
  - Relatórios
- 8. Audit Log & LGPD
  - 8.1 Eventos Auditados
  - 8.2 Estrutura do Registro
  - 8.3 LGPD — Controles
- 9. Checklist de Entrega
  - Frontend
  - Backend
  - Qualidade

## 4. Correções da v2 que prevalecem
- **T-01:** todas as 12 tabelas recebem `tenant_id` NOT NULL e índice composto ([19](../../../docs/v2/19-regras-modulos-3.md), seção 1; [03](../../../docs/v2/03-dominio-tenancy.md)).
- **T-04:** `current_value` é calculado, não editável. Guardar o último cálculo com data e método; recalcular, não sobrescrever.
- **Regras de campo** ([19](../../../docs/v2/19-regras-modulos-3.md), seção 8.2): `acquisition_value` maior que zero e só alterável por correção com motivo; `residual_value` não negativo e não maior que `acquisition_value`; `dep_method` em `linear`, `accelerated`, `degressive`, `unit`; `dep_rate` entre 0 e 100%; ativo baixado não recebe depreciação nem movimento.
- **Instância da empresa:** sem filtro de unidade, entidade ou filial; dados no banco master; o portal do desenvolvedor não vê o módulo de nenhuma entidade.
- **Perfis da v1 (seção 2 da v1):** substituídos pelos papéis da seção 6 desta ficha.
- **Contabilização automática de depreciação:** gera lançamento no razão da empresa ([razao.md](../contabil-da-plataforma/razao.md)), não no contábil de entidade.

## 5. Decisões por padrão aplicadas
- **DP-02** ([80](../../../docs/v2/80-decisoes-por-padrao.md)): método e taxa por categoria aprovados pelo contábil; categoria sem regra aprovada não deprecia e aparece como pendência no painel.

## 6. Permissões e papéis
- `platform.assets` (nível 1): cadastrar e movimentar bens, registrar manutenção, inventário e seguro.
- `platform.assets.approver` (nível 2): aprovar transferência, descarte e manutenção acima do limite; não aprova o que ele mesmo registrou (DP-03; [78](../../../docs/v2/78-permissoes-e-papeis.md), seção 4.1).

## 7. Dados
- Modelo de dados da v1 (seção 13, "Schema do Banco de Dados"), com as correções T-01 e T-04 da seção 4.

## 8. Integrações
- Contábil da plataforma: lançamento de depreciação e de baixa.
- Financeiro da plataforma: aquisição e venda de bem (contas a pagar e a receber).
- Suprimentos da empresa: entrada de bem comprado.

## 9. Exportação, auditoria e privacidade
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Auditoria conforme [29](../../../docs/v2/29-auditoria.md); dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md).


## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
- Limite de valor que exige aprovação de manutenção: parâmetro obrigatório, configurado pelo `platform.assets.approver`; sem valor configurado, toda manutenção exige aprovação (critério 1 do [80](../../../docs/v2/80-decisoes-por-padrao.md)).
- Regra de depreciação por categoria: configurada pelo contábil (DP-02).

## 13. Conteúdo integral da v1 (absorvido)

### SPEC — Módulo Patrimônio
**Versão:** 1.0.0  
**Status:** Draft Funcional Completo  
**Módulo:** Patrimônio / Asset Management  
**Plataforma:** TotusTuusSoftCloud — SaaS Multi-Entidade · Multi-Unidade · Multi-Usuário  
**Stack:** PHP 8 puro · MariaDB · REST/fetch · Tailwind CSS 4.2 · Supabase · amCharts 5  
**Padrão de Identidade:** `id` (PK auto-increment) · `uuid` (interno) · `code` (externo legível)  
**Compliance:** LGPD · ISO 55000 · NBR 16280  
**Data:** 2026-06-06  

- Language Standard: Global English
---

#### Índice

1. [Visão Geral](#1-visão-geral)
2. [Perfis e Permissões (RBAC)](#2-perfis-e-permissões-rbac)
3. [Schema do Banco de Dados](#3-schema-do-banco-de-dados)
4. [Páginas e Componentes](#4-páginas-e-componentes)
   - 4.1 [Dashboard — Patrimônio](#41-dashboard--patrimônio)
   - 4.2 [Cadastro de Ativos](#42-cadastro-de-ativos)
   - 4.3 [Depreciação](#43-depreciação)
   - 4.4 [Manutenção](#44-manutenção)
   - 4.5 [Transferências](#45-transferências)
   - 4.6 [Inventário](#46-inventário)
   - 4.7 [Descarte / Alienação](#47-descarte--alienação)
   - 4.8 [Seguros](#48-seguros)
   - 4.9 [Kanban — Manutenção](#49-kanban--manutenção)
   - 4.10 [Relatórios](#410-relatórios)
5. [Automações](#5-automações)
6. [Integrações](#6-integrações)
7. [API REST — Endpoints](#7-api-rest--endpoints)
8. [Audit Log & LGPD](#8-audit-log--lgpd)
9. [Checklist de Entrega](#9-checklist-de-entrega)

---

#### 1. Visão Geral

O módulo **Patrimônio** controla todo o ciclo de vida dos ativos fixos e móveis da entidade/unidade:
aquisição, cadastro, valoração, depreciação, manutenção, transferência, inventário e descarte.
Integra-se com os módulos Financeiro, Suprimentos, Contábil e RH.

##### Subdomínios

| Subdomínio | Descrição |
|---|---|
| Ativos | Cadastro completo de bens patrimoniais |
| Depreciação | Cálculo automático linear/acelerada/degressive |
| Manutenção | Preventiva, Corretiva, Preditiva |
| Transferência | Entre unidades/centros de custo/responsáveis |
| Inventário | Contagem física com QR-code / RFID |
| Descarte | Baixa, alienação, doação, sucata |
| Seguros | Apólices vinculadas a ativos |

---

#### 2. Perfis e Permissões (RBAC)

| Permissão | SA | GE | GP | TEC | AUD | FIN | VIS |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| assets.view | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| assets.create | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| assets.edit | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| assets.delete | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| depreciation.run | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| depreciation.adjust | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| maintenance.view | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| maintenance.create | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| maintenance.edit | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| maintenance.approve | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| transfer.create | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| transfer.approve | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| inventory.run | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| inventory.close | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| disposal.create | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| disposal.approve | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| insurance.view | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |
| insurance.manage | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| reports.view | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| reports.export | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |

> **SA** = Super Admin · **GE** = Gestor de Entidade · **GP** = Gestor de Patrimônio · **TEC** = Técnico de Manutenção · **AUD** = Auditor · **FIN** = Financeiro · **VIS** = Visualizador

---

#### 3. Schema do Banco de Dados

##### 3.1 Tabela `pat_asset_categories`
```sql
CREATE TABLE pat_asset_categories (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid        CHAR(36)     NOT NULL UNIQUE DEFAULT (UUID()),
  code        VARCHAR(20)  NOT NULL UNIQUE,
  entity_id   INT UNSIGNED NOT NULL,
  name        VARCHAR(120) NOT NULL,
  description TEXT,
  parent_id   INT UNSIGNED NULL REFERENCES pat_asset_categories(id),
  dep_method  ENUM('linear','accelerated','degressive','unit') DEFAULT 'linear',
  dep_rate    DECIMAL(8,4) NOT NULL DEFAULT 0,
  useful_life INT          NOT NULL DEFAULT 60 COMMENT 'meses',
  is_active   TINYINT(1)   DEFAULT 1,
  created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP,
  updated_at  DATETIME     ON UPDATE CURRENT_TIMESTAMP,
  deleted_at  DATETIME     NULL
);
```

##### 3.2 Tabela `pat_assets`
```sql
CREATE TABLE pat_assets (
  id                INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid              CHAR(36)      NOT NULL UNIQUE DEFAULT (UUID()),
  code              VARCHAR(30)   NOT NULL UNIQUE COMMENT 'Plaqueta patrimonial',
  entity_id         INT UNSIGNED  NOT NULL,
  unit_id           INT UNSIGNED  NOT NULL,
  category_id       INT UNSIGNED  NOT NULL REFERENCES pat_asset_categories(id),
  name              VARCHAR(200)  NOT NULL,
  description       TEXT,
  brand             VARCHAR(100),
  model             VARCHAR(100),
  serial_number     VARCHAR(100),
  supplier_id       INT UNSIGNED  NULL,
  purchase_order_id INT UNSIGNED  NULL,
  acquisition_date  DATE          NOT NULL,
  activation_date   DATE          NULL,
  acquisition_value DECIMAL(15,2) NOT NULL,
  current_value     DECIMAL(15,2) NOT NULL,
  residual_value    DECIMAL(15,2) NOT NULL DEFAULT 0,
  dep_start_date    DATE          NULL,
  dep_method        ENUM('linear','accelerated','degressive','unit') DEFAULT 'linear',
  dep_rate          DECIMAL(8,4)  NOT NULL DEFAULT 0,
  useful_life       INT           NOT NULL DEFAULT 60,
  accumulated_dep   DECIMAL(15,2) NOT NULL DEFAULT 0,
  location_id       INT UNSIGNED  NULL,
  cost_center_id    INT UNSIGNED  NULL,
  responsible_id    INT UNSIGNED  NULL COMMENT 'user_id do responsável',
  status            ENUM('active','maintenance','transferred','disposed','inactive') DEFAULT 'active',
  condition         ENUM('new','good','regular','poor','critical') DEFAULT 'new',
  warranty_expiry   DATE          NULL,
  invoice_number    VARCHAR(60)   NULL,
  invoice_date      DATE          NULL,
  nf_value          DECIMAL(15,2) NULL,
  qr_code           TEXT          NULL,
  rfid_tag          VARCHAR(80)   NULL,
  photo_main        VARCHAR(255)  NULL,
  photos_json       JSON          NULL,
  docs_json         JSON          NULL,
  notes             TEXT          NULL,
  is_active         TINYINT(1)    DEFAULT 1,
  created_by        INT UNSIGNED  NOT NULL,
  updated_by        INT UNSIGNED  NULL,
  created_at        DATETIME      DEFAULT CURRENT_TIMESTAMP,
  updated_at        DATETIME      ON UPDATE CURRENT_TIMESTAMP,
  deleted_at        DATETIME      NULL,
  INDEX idx_entity_unit (entity_id, unit_id),
  INDEX idx_status (status),
  INDEX idx_category (category_id),
  INDEX idx_responsible (responsible_id)
);
```

##### 3.3 Tabela `pat_depreciation_runs`
```sql
CREATE TABLE pat_depreciation_runs (
  id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid          CHAR(36)      NOT NULL UNIQUE DEFAULT (UUID()),
  entity_id     INT UNSIGNED  NOT NULL,
  unit_id       INT UNSIGNED  NOT NULL,
  reference     VARCHAR(7)    NOT NULL COMMENT 'YYYY-MM',
  run_date      DATETIME      NOT NULL,
  total_assets  INT           DEFAULT 0,
  total_dep     DECIMAL(15,2) DEFAULT 0,
  status        ENUM('pending','running','completed','reversed') DEFAULT 'pending',
  run_by        INT UNSIGNED  NOT NULL,
  reversed_by   INT UNSIGNED  NULL,
  reversed_at   DATETIME      NULL,
  notes         TEXT,
  created_at    DATETIME      DEFAULT CURRENT_TIMESTAMP
);
```

##### 3.4 Tabela `pat_depreciation_entries`
```sql
CREATE TABLE pat_depreciation_entries (
  id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36)      NOT NULL UNIQUE DEFAULT (UUID()),
  run_id          INT UNSIGNED  NOT NULL REFERENCES pat_depreciation_runs(id),
  asset_id        INT UNSIGNED  NOT NULL REFERENCES pat_assets(id),
  reference       VARCHAR(7)    NOT NULL,
  opening_value   DECIMAL(15,2) NOT NULL,
  dep_amount      DECIMAL(15,2) NOT NULL,
  accumulated_dep DECIMAL(15,2) NOT NULL,
  closing_value   DECIMAL(15,2) NOT NULL,
  method          ENUM('linear','accelerated','degressive','unit'),
  rate            DECIMAL(8,4),
  is_reversed     TINYINT(1)    DEFAULT 0,
  created_at      DATETIME      DEFAULT CURRENT_TIMESTAMP
);
```

##### 3.5 Tabela `pat_maintenances`
```sql
CREATE TABLE pat_maintenances (
  id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36)      NOT NULL UNIQUE DEFAULT (UUID()),
  code            VARCHAR(30)   NOT NULL UNIQUE,
  entity_id       INT UNSIGNED  NOT NULL,
  unit_id         INT UNSIGNED  NOT NULL,
  asset_id        INT UNSIGNED  NOT NULL REFERENCES pat_assets(id),
  type            ENUM('preventive','corrective','predictive','calibration','inspection') NOT NULL,
  priority        ENUM('low','medium','high','critical') DEFAULT 'medium',
  status          ENUM('requested','approved','scheduled','in_progress','completed','cancelled') DEFAULT 'requested',
  title           VARCHAR(200)  NOT NULL,
  description     TEXT,
  requested_by    INT UNSIGNED  NOT NULL,
  approved_by     INT UNSIGNED  NULL,
  assigned_to     INT UNSIGNED  NULL,
  supplier_id     INT UNSIGNED  NULL,
  scheduled_date  DATETIME      NULL,
  started_at      DATETIME      NULL,
  completed_at    DATETIME      NULL,
  estimated_cost  DECIMAL(12,2) NULL,
  actual_cost     DECIMAL(12,2) NULL,
  invoice_number  VARCHAR(60)   NULL,
  next_due_date   DATE          NULL,
  resolution_notes TEXT,
  photos_json     JSON          NULL,
  docs_json       JSON          NULL,
  is_recurring    TINYINT(1)    DEFAULT 0,
  recurrence_rule VARCHAR(200)  NULL COMMENT 'iCal RRULE',
  created_at      DATETIME      DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME      ON UPDATE CURRENT_TIMESTAMP,
  deleted_at      DATETIME      NULL
);
```

##### 3.6 Tabela `pat_transfers`
```sql
CREATE TABLE pat_transfers (
  id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36)      NOT NULL UNIQUE DEFAULT (UUID()),
  code            VARCHAR(30)   NOT NULL UNIQUE,
  entity_id       INT UNSIGNED  NOT NULL,
  asset_id        INT UNSIGNED  NOT NULL REFERENCES pat_assets(id),
  from_unit_id    INT UNSIGNED  NOT NULL,
  to_unit_id      INT UNSIGNED  NOT NULL,
  from_location   VARCHAR(200)  NULL,
  to_location     VARCHAR(200)  NULL,
  from_responsible INT UNSIGNED NULL,
  to_responsible  INT UNSIGNED  NULL,
  from_cost_center INT UNSIGNED NULL,
  to_cost_center  INT UNSIGNED  NULL,
  transfer_date   DATE          NOT NULL,
  reason          TEXT,
  status          ENUM('pending','approved','rejected','completed') DEFAULT 'pending',
  requested_by    INT UNSIGNED  NOT NULL,
  approved_by     INT UNSIGNED  NULL,
  approved_at     DATETIME      NULL,
  completed_at    DATETIME      NULL,
  notes           TEXT,
  docs_json       JSON          NULL,
  created_at      DATETIME      DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME      ON UPDATE CURRENT_TIMESTAMP
);
```

##### 3.7 Tabela `pat_inventories`
```sql
CREATE TABLE pat_inventories (
  id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36)      NOT NULL UNIQUE DEFAULT (UUID()),
  code            VARCHAR(30)   NOT NULL UNIQUE,
  entity_id       INT UNSIGNED  NOT NULL,
  unit_id         INT UNSIGNED  NOT NULL,
  title           VARCHAR(200)  NOT NULL,
  reference_date  DATE          NOT NULL,
  start_date      DATETIME      NULL,
  end_date        DATETIME      NULL,
  status          ENUM('draft','open','in_progress','closed','audited') DEFAULT 'draft',
  scope           ENUM('full','partial','category','location') DEFAULT 'full',
  category_id     INT UNSIGNED  NULL,
  location_id     INT UNSIGNED  NULL,
  total_expected  INT           DEFAULT 0,
  total_counted   INT           DEFAULT 0,
  total_found     INT           DEFAULT 0,
  total_missing   INT           DEFAULT 0,
  total_extra     INT           DEFAULT 0,
  created_by      INT UNSIGNED  NOT NULL,
  closed_by       INT UNSIGNED  NULL,
  notes           TEXT,
  created_at      DATETIME      DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME      ON UPDATE CURRENT_TIMESTAMP
);
```

##### 3.8 Tabela `pat_inventory_items`
```sql
CREATE TABLE pat_inventory_items (
  id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36)      NOT NULL UNIQUE DEFAULT (UUID()),
  inventory_id    INT UNSIGNED  NOT NULL REFERENCES pat_inventories(id),
  asset_id        INT UNSIGNED  NOT NULL REFERENCES pat_assets(id),
  expected_location VARCHAR(200) NULL,
  found_location  VARCHAR(200)  NULL,
  status          ENUM('pending','found','not_found','extra','divergent') DEFAULT 'pending',
  condition       ENUM('new','good','regular','poor','critical') NULL,
  counted_by      INT UNSIGNED  NULL,
  counted_at      DATETIME      NULL,
  qr_scanned      TINYINT(1)    DEFAULT 0,
  notes           TEXT,
  photo_json      JSON          NULL,
  created_at      DATETIME      DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME      ON UPDATE CURRENT_TIMESTAMP
);
```

##### 3.9 Tabela `pat_disposals`
```sql
CREATE TABLE pat_disposals (
  id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36)      NOT NULL UNIQUE DEFAULT (UUID()),
  code            VARCHAR(30)   NOT NULL UNIQUE,
  entity_id       INT UNSIGNED  NOT NULL,
  asset_id        INT UNSIGNED  NOT NULL REFERENCES pat_assets(id),
  type            ENUM('write_off','sale','donation','scrap','loss','theft') NOT NULL,
  status          ENUM('requested','approved','rejected','completed') DEFAULT 'requested',
  reason          TEXT          NOT NULL,
  disposal_date   DATE          NULL,
  sale_value      DECIMAL(12,2) NULL,
  book_value      DECIMAL(12,2) NOT NULL,
  gain_loss       DECIMAL(12,2) NULL COMMENT 'calculado: sale_value - book_value',
  buyer           VARCHAR(200)  NULL,
  buyer_doc       VARCHAR(20)   NULL,
  requested_by    INT UNSIGNED  NOT NULL,
  approved_by     INT UNSIGNED  NULL,
  approved_at     DATETIME      NULL,
  completed_at    DATETIME      NULL,
  docs_json       JSON          NULL,
  notes           TEXT,
  created_at      DATETIME      DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME      ON UPDATE CURRENT_TIMESTAMP
);
```

##### 3.10 Tabela `pat_insurances`
```sql
CREATE TABLE pat_insurances (
  id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid            CHAR(36)      NOT NULL UNIQUE DEFAULT (UUID()),
  code            VARCHAR(30)   NOT NULL UNIQUE,
  entity_id       INT UNSIGNED  NOT NULL,
  policy_number   VARCHAR(80)   NOT NULL,
  insurer         VARCHAR(200)  NOT NULL,
  type            ENUM('comprehensive','fire','theft','liability','equipment') NOT NULL,
  start_date      DATE          NOT NULL,
  end_date        DATE          NOT NULL,
  insured_value   DECIMAL(15,2) NOT NULL,
  premium         DECIMAL(12,2) NOT NULL,
  deductible      DECIMAL(12,2) DEFAULT 0,
  status          ENUM('active','expired','cancelled','renewing') DEFAULT 'active',
  contact_name    VARCHAR(200)  NULL,
  contact_phone   VARCHAR(20)   NULL,
  contact_email   VARCHAR(150)  NULL,
  docs_json       JSON          NULL,
  notes           TEXT,
  created_by      INT UNSIGNED  NOT NULL,
  created_at      DATETIME      DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME      ON UPDATE CURRENT_TIMESTAMP
);
```

##### 3.11 Tabela `pat_insurance_assets`
```sql
CREATE TABLE pat_insurance_assets (
  id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  insurance_id  INT UNSIGNED NOT NULL REFERENCES pat_insurances(id),
  asset_id      INT UNSIGNED NOT NULL REFERENCES pat_assets(id),
  insured_value DECIMAL(15,2) NOT NULL,
  UNIQUE KEY uk_ins_asset (insurance_id, asset_id)
);
```

##### 3.12 Tabela `pat_locations`
```sql
CREATE TABLE pat_locations (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid        CHAR(36)     NOT NULL UNIQUE DEFAULT (UUID()),
  code        VARCHAR(20)  NOT NULL UNIQUE,
  entity_id   INT UNSIGNED NOT NULL,
  unit_id     INT UNSIGNED NOT NULL,
  name        VARCHAR(120) NOT NULL,
  parent_id   INT UNSIGNED NULL REFERENCES pat_locations(id),
  floor       VARCHAR(20)  NULL,
  building    VARCHAR(80)  NULL,
  description TEXT,
  is_active   TINYINT(1)   DEFAULT 1,
  created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP,
  updated_at  DATETIME     ON UPDATE CURRENT_TIMESTAMP
);
```

---

#### 4. Páginas e Componentes

---

##### 4.1 Dashboard — Patrimônio
**Rota:** `/patrimonio/dashboard`  
**Arquivo:** `pages/patrimonio/dashboard.php`  
**Permissão:** `assets.view`

###### Widgets KPI (linha superior — 6 cards)

| # | Widget | Valor | Variação | Ícone |
|---|---|---|---|---|
| 1 | Total de Ativos | COUNT(active) | vs. mês anterior | `ki-box` |
| 2 | Valor Patrimonial Total | SUM(current_value) | vs. mês anterior | `ki-dollar` |
| 3 | Depreciação Acumulada | SUM(accumulated_dep) | % do valor original | `ki-arrow-down` |
| 4 | Ativos em Manutenção | COUNT(status=maintenance) | vs. mês anterior | `ki-wrench` |
| 5 | Manutenções Abertas | COUNT pendentes+agendadas | vence em 7 dias | `ki-notification` |
| 6 | Seguros a Vencer (30d) | COUNT expiram em 30d | alerta vermelho se > 0 | `ki-shield` |

###### Widgets Operacionais (linha intermediária — 4 cards)

| # | Widget | Conteúdo |
|---|---|---|
| 7 | Ativos por Condição | Donut rápido: new/good/regular/poor/critical |
| 8 | Próximas Manutenções | Lista top-5 por data agendada com badge de prioridade |
| 9 | Últimas Transferências | Lista top-5 com origem → destino e status |
| 10 | Inventário em Aberto | Card com progresso (%contados/esperados) ou placeholder |

###### Charts amCharts 5 (seção inferior)

| # | Chart | Tipo | Dados |
|---|---|---|---|
| C1 | Evolução do Valor Patrimonial | Line + Area dual-axis | valor_bruto vs. valor_liquido por mês (12m) |
| C2 | Depreciação Mensal | Bar clustered | dep_amount por categoria (últimos 6 meses) |
| C3 | Ativos por Categoria | Donut / Pie | COUNT por categoria nível 1 |
| C4 | Distribuição por Localização | TreeMap | COUNT por location_id agrupado por prédio/andar |
| C5 | Manutenções por Tipo | Bar horizontal | COUNT por type + status (últimos 90 dias) |
| C6 | Custo de Manutenção | Line | actual_cost por mês (12m) |

###### Controles do Dashboard

```
[Entidade ▼] [Unidade ▼] [Período ▼: Este Mês / Trimestre / Ano]  [⟳ Atualizar]
```

---

##### 4.2 Cadastro de Ativos
**Rota:** `/patrimonio/ativos`  
**Arquivo:** `pages/patrimonio/ativos.php`  
**Permissão:** `assets.view`

###### Toolbar
```
[🔍 Busca global]  [Categoria ▼]  [Unidade ▼]  [Status ▼]  [Condição ▼]  [+ Novo Ativo]
[Exportar CSV/Excel/PDF]  [Importar]  [Imprimir Etiquetas QR]  [Colunas ⚙]
```

###### DataTable — Colunas

| Coluna | Campo | Tipo | Ordenável | Filtrável |
|---|---|---|:---:|:---:|
| ☐ | Seleção | checkbox | ❌ | ❌ |
| Plaqueta | code | text | ✅ | ✅ |
| Foto | photo_main | thumbnail | ❌ | ❌ |
| Nome | name | text | ✅ | ✅ |
| Categoria | category.name | text | ✅ | ✅ |
| Localização | location.name | text | ✅ | ✅ |
| Responsável | responsible.name | text | ✅ | ✅ |
| Valor Original | acquisition_value | currency | ✅ | range |
| Valor Atual | current_value | currency | ✅ | range |
| Dep. Acumulada | accumulated_dep | currency | ✅ | range |
| Status | status | badge | ✅ | ✅ |
| Condição | condition | badge-color | ✅ | ✅ |
| Garantia | warranty_expiry | date | ✅ | date-range |
| Ações | — | buttons | ❌ | ❌ |

**Ações por linha:** `[👁 Ver]` `[✏ Editar]` `[🔄 Transferir]` `[🔧 Manutenção]` `[⋮ Mais]`

**Ações em lote (seleção múltipla):**
- Transferir em lote
- Imprimir etiquetas QR selecionados
- Exportar selecionados
- Alterar responsável em lote
- Baixar (descarte) em lote

###### CRUD Drawer — Novo/Editar Ativo

**Drawer lateral direito — largura 720px — 6 abas**

**Aba 1: Identificação**

| Campo | Tipo | Obrigatório | Regras |
|---|---|:---:|---|
| Plaqueta (code) | text | ✅ | único, auto-gerado se vazio (PAT-YYYY-NNNNNN) |
| Nome do Bem | text | ✅ | max 200 |
| Descrição | textarea | ❌ | max 1000 |
| Categoria | select2 (árvore) | ✅ | carrega dep_method e dep_rate |
| Marca | text | ❌ | max 100 |
| Modelo | text | ❌ | max 100 |
| Número de Série | text | ❌ | max 100 |
| Tag RFID | text | ❌ | max 80 |
| Condição Inicial | radio | ✅ | new/good/regular/poor/critical |
| Fotos | dropzone multi | ❌ | max 10 · jpg/png/webp · 5MB |

**Aba 2: Aquisição**

| Campo | Tipo | Obrigatório | Regras |
|---|---|:---:|---|
| Data de Aquisição | date | ✅ | ≤ hoje |
| Data de Ativação | date | ❌ | ≥ aquisição |
| Fornecedor | select2 (Suprimentos) | ❌ | |
| Ordem de Compra | select2 (Suprimentos) | ❌ | |
| Valor de Aquisição | currency | ✅ | > 0 |
| Valor Residual | currency | ❌ | ≥ 0; < aquisição |
| Nº Nota Fiscal | text | ❌ | |
| Data NF | date | ❌ | |
| Valor NF | currency | ❌ | |
| Garantia até | date | ❌ | |
| Documentos NF | dropzone | ❌ | pdf/xml · 10MB |

**Aba 3: Localização**

| Campo | Tipo | Obrigatório | Regras |
|---|---|:---:|---|
| Unidade | select2 | ✅ | |
| Localização | select2 (árvore) | ❌ | |
| Prédio | text | ❌ | |
| Andar/Sala | text | ❌ | |
| Centro de Custo | select2 (Financeiro) | ❌ | |
| Responsável | select2 (RH/Usuários) | ❌ | |
| Observações de Local | textarea | ❌ | |

**Aba 4: Depreciação**

| Campo | Tipo | Obrigatório | Regras |
|---|---|:---:|---|
| Método de Depreciação | select | ✅ | linear/acelerada/degressive/unidade |
| Taxa Anual (%) | number | ✅ | 0–100 |
| Vida Útil (meses) | number | ✅ | > 0 |
| Início da Depreciação | date | ❌ | default = ativação |
| Depreciação Acumulada (leitura) | read-only | — | calculada |
| Valor Líquido Atual (leitura) | read-only | — | calculada |
| Histórico de Depreciação | mini-table | — | referência · valor · acumulado |

**Aba 5: Seguros e Vínculos**

| Campo | Tipo | Obrigatório |
|---|---|:---:|
| Apólice(s) vinculada(s) | multi-select | ❌ |
| Valor Segurado | currency (read-only) | — |
| Projetos vinculados | multi-select | ❌ |
| Contratos vinculados | multi-select | ❌ |
| Centro de custo contábil | select2 | ❌ |

**Aba 6: Histórico / Timeline**

- Timeline vertical com todos os eventos do ativo:
  - Aquisição → Ativação → Depreciações → Manutenções → Transferências → Inventários → Descarte
- Cada evento: data · tipo · usuário · descrição resumida · botão "Ver detalhe"

###### Drawer de Visualização Rápida (modo leitura)

- Modal 900px com layout 2 colunas
- Foto principal em destaque + galeria thumbnails
- QR-code gerado dinamicamente (plaqueta)
- Dados de identificação, localização e valores
- Tabs: Depreciação | Manutenções | Transferências | Histórico

---

##### 4.3 Depreciação
**Rota:** `/patrimonio/depreciacao`  
**Arquivo:** `pages/patrimonio/depreciacao.php`  
**Permissão:** `depreciation.run`

###### Toolbar
```
[Unidade ▼]  [Referência (mês/ano) ▼]  [Status ▼]
[▶ Rodar Depreciação]  [↩ Estornar]  [Exportar]
```

###### Painel de Execução — Card de Controle

```
┌─────────────────────────────────────────────────────────┐
│  Referência: [YYYY-MM ▼]   Unidade: [Unidade ▼]        │
│  Ativos elegíveis: 0       Já processado: Não           │
│  Estimativa de depreciação: R$ 0,00                     │
│  [Calcular Prévia]           [▶ Executar Depreciação]   │
└─────────────────────────────────────────────────────────┘
```

###### DataTable — Histórico de Runs

| Coluna | Campo |
|---|---|
| Referência | reference (YYYY-MM) |
| Unidade | unit.name |
| Ativos Processados | total_assets |
| Total Depreciado | total_dep |
| Status | status badge |
| Executado por | run_by.name |
| Data Execução | run_date |
| Ações | Ver Itens · Estornar |

###### DataTable — Itens da Depreciação (drill-down)

| Coluna | Campo |
|---|---|
| Plaqueta | asset.code |
| Nome do Ativo | asset.name |
| Categoria | category.name |
| Valor Abertura | opening_value |
| Depreciação | dep_amount |
| Dep. Acumulada | accumulated_dep |
| Valor Fechamento | closing_value |
| Método | method |
| Taxa | rate |

###### Charts

| # | Chart | Tipo |
|---|---|---|
| C1 | Depreciação por Categoria (referência atual) | Bar horizontal |
| C2 | Evolução da Depreciação Mensal | Line área 12 meses |
| C3 | Valor Bruto vs. Líquido por Categoria | Bar clustered |

---

##### 4.4 Manutenção
**Rota:** `/patrimonio/manutencao`  
**Arquivo:** `pages/patrimonio/manutencao.php`  
**Permissão:** `maintenance.view`

###### Toolbar
```
[🔍 Busca]  [Tipo ▼]  [Prioridade ▼]  [Status ▼]  [Período ▼]  [Técnico ▼]
[+ Nova Manutenção]  [Exportar]  [Ver Kanban]  [Calendário]
```

###### DataTable — Manutenções

| Coluna | Campo | Tipo |
|---|---|---|
| Código | code | text |
| Ativo | asset.name + code | link |
| Tipo | type | badge |
| Prioridade | priority | badge colorido |
| Status | status | badge |
| Título | title | text |
| Responsável | assigned_to.name | text |
| Data Agendada | scheduled_date | datetime |
| Custo Estimado | estimated_cost | currency |
| Custo Real | actual_cost | currency |
| Ações | — | buttons |

**Ações:** `[👁 Ver]` `[✏ Editar]` `[✅ Concluir]` `[❌ Cancelar]`

###### CRUD Drawer — Nova/Editar Manutenção

**Drawer 720px — 4 abas**

**Aba 1: Dados Gerais**

| Campo | Tipo | Obrigatório | Regras |
|---|---|:---:|---|
| Ativo | select2 (busca por código/nome) | ✅ | |
| Tipo | select | ✅ | preventive/corrective/predictive/calibration/inspection |
| Prioridade | radio/select | ✅ | low/medium/high/critical |
| Título | text | ✅ | max 200 |
| Descrição do Problema | textarea | ✅ | |
| Solicitante | read-only (usuário logado) | — | |
| Data de Solicitação | read-only | — | now() |
| Recorrente? | toggle | ❌ | se sim → exibe RRULE builder |
| Regra de Recorrência | RRULE select (semanal/mensal/...) | ❌ | |

**Aba 2: Agendamento**

| Campo | Tipo | Obrigatório |
|---|---|:---:|
| Data Agendada | datetime | ❌ |
| Técnico Responsável | select2 (usuários com perfil TEC) | ❌ |
| Fornecedor Externo | select2 (Suprimentos) | ❌ |
| Estimativa de Custo | currency | ❌ |
| Duração Estimada (horas) | number | ❌ |
| Observações de Agendamento | textarea | ❌ |

**Aba 3: Conclusão**

| Campo | Tipo | Obrigatório |
|---|---|:---:|
| Data de Início | datetime | ❌ |
| Data de Conclusão | datetime | ❌ |
| Custo Real | currency | ❌ |
| Nº Nota Fiscal | text | ❌ |
| Resolução / Laudo | textarea (rich) | ❌ |
| Próxima Manutenção Prevista | date | ❌ |
| Condição do Ativo pós-manutenção | select | ❌ |
| Fotos do serviço | dropzone | ❌ |
| Documentos/Laudos | dropzone | ❌ |

**Aba 4: Histórico do Ativo**

- Mini-timeline de todas as manutenções anteriores do ativo selecionado
- Custo total acumulado em manutenções
- Indicador de frequência de falhas

###### Drawer de Aprovação

- Card resumido com dados da manutenção
- Campo: Observações de aprovação/rejeição
- Botões: `[✅ Aprovar]` `[❌ Rejeitar]`

###### Calendário de Manutenções

- Visão mensal/semanal (FullCalendar ou Supabase Calendar)
- Cor por prioridade: verde=low · amarelo=medium · laranja=high · vermelho=critical
- Clique no evento abre drawer de detalhes

---

##### 4.5 Transferências
**Rota:** `/patrimonio/transferencias`  
**Arquivo:** `pages/patrimonio/transferencias.php`  
**Permissão:** `transfer.create`

###### Toolbar
```
[🔍 Busca]  [Unidade Origem ▼]  [Unidade Destino ▼]  [Status ▼]  [Período ▼]
[+ Nova Transferência]  [Transferência em Lote]  [Exportar]
```

###### DataTable — Transferências

| Coluna | Campo |
|---|---|
| Código | code |
| Ativo | asset.name + plaqueta |
| Unidade Origem | from_unit.name |
| Unidade Destino | to_unit.name |
| Responsável Origem | from_responsible.name |
| Responsável Destino | to_responsible.name |
| Data Transferência | transfer_date |
| Status | status badge |
| Solicitado por | requested_by.name |
| Aprovado por | approved_by.name |
| Ações | Ver · Aprovar · Rejeitar · Concluir |

###### CRUD Drawer — Nova Transferência

| Campo | Tipo | Obrigatório | Regras |
|---|---|:---:|---|
| Ativo(s) | select2 multi (busca) | ✅ | exibe valor atual e localização |
| Unidade Destino | select2 | ✅ | ≠ unidade atual |
| Localização Destino | text | ❌ | |
| Responsável Destino | select2 | ❌ | |
| Centro de Custo Destino | select2 | ❌ | |
| Data Prevista | date | ✅ | ≥ hoje |
| Motivo | textarea | ✅ | |
| Documentos | dropzone | ❌ | |

###### Drawer de Aprovação

- Resumo da transferência com dados do ativo
- Campo: observações
- Botões: `[✅ Aprovar e Concluir]` `[⏳ Aprovar e Aguardar]` `[❌ Rejeitar]`

---

##### 4.6 Inventário
**Rota:** `/patrimonio/inventario`  
**Arquivo:** `pages/patrimonio/inventario.php`  
**Permissão:** `inventory.run`

###### Toolbar
```
[🔍 Busca]  [Status ▼]  [Período ▼]
[+ Novo Inventário]  [Exportar]
```

###### DataTable — Inventários

| Coluna | Campo |
|---|---|
| Código | code |
| Título | title |
| Unidade | unit.name |
| Escopo | scope badge |
| Data Referência | reference_date |
| Início | start_date |
| Fim | end_date |
| Esperados | total_expected |
| Contados | total_counted |
| Encontrados | total_found |
| Faltantes | total_missing |
| % Conclusão | progress bar |
| Status | status badge |
| Ações | Abrir · Ver Itens · Fechar · Exportar |

###### CRUD Drawer — Novo Inventário

| Campo | Tipo | Obrigatório | Regras |
|---|---|:---:|---|
| Título | text | ✅ | |
| Unidade | select2 | ✅ | |
| Data Referência | date | ✅ | |
| Escopo | radio | ✅ | full/partial/category/location |
| Categoria (se parcial) | select2 | cond. | |
| Localização (se parcial) | select2 | cond. | |
| Observações | textarea | ❌ | |

###### Painel de Execução do Inventário

**Subpágina:** `/patrimonio/inventario/{uuid}/executar`

```
┌─────────────────────────────────────────────┐
│  Inventário: INV-2026-001                    │
│  Progresso: ████████░░ 78%  (390/500)        │
│  Encontrados: 385  Faltantes: 5  Extras: 10  │
└─────────────────────────────────────────────┘

[📷 Ler QR-Code]   [🔍 Buscar por Código]   [Filtros ▼]
```

**DataTable de Itens:**

| Coluna | Campo |
|---|---|
| Plaqueta | asset.code |
| Nome | asset.name |
| Localização Esperada | expected_location |
| Localização Encontrada | found_location |
| Condição | condition select |
| Status | status badge |
| Contado por | counted_by.name |
| Data Contagem | counted_at |
| Ações | Marcar Encontrado · Divergência · Foto |

---

##### 4.7 Descarte / Alienação
**Rota:** `/patrimonio/descarte`  
**Arquivo:** `pages/patrimonio/descarte.php`  
**Permissão:** `disposal.create`

###### Toolbar
```
[🔍 Busca]  [Tipo ▼]  [Status ▼]  [Período ▼]
[+ Novo Descarte]  [Exportar]
```

###### DataTable — Descartes

| Coluna | Campo |
|---|---|
| Código | code |
| Ativo | asset.name + plaqueta |
| Tipo Descarte | type badge |
| Valor Contábil | book_value |
| Valor Alienação | sale_value |
| Ganho/Perda | gain_loss (verde/vermelho) |
| Status | status badge |
| Data Descarte | disposal_date |
| Solicitado por | requested_by.name |
| Ações | Ver · Aprovar · Concluir |

###### CRUD Drawer — Novo Descarte

| Campo | Tipo | Obrigatório | Regras |
|---|---|:---:|---|
| Ativo | select2 | ✅ | exibe valor contábil atual |
| Tipo de Descarte | select | ✅ | write_off/sale/donation/scrap/loss/theft |
| Motivo | textarea | ✅ | |
| Data Prevista | date | ❌ | |
| Valor de Alienação | currency | cond. | obrigatório se type=sale |
| Comprador | text | cond. | obrigatório se type=sale |
| CPF/CNPJ Comprador | text | cond. | |
| Valor Contábil (read-only) | currency | — | calculado |
| Ganho/Perda Estimado | currency (read-only) | — | calculado |
| Documentos | dropzone | ❌ | |
| Observações | textarea | ❌ | |

---

##### 4.8 Seguros
**Rota:** `/patrimonio/seguros`  
**Arquivo:** `pages/patrimonio/seguros.php`  
**Permissão:** `insurance.view`

###### Toolbar
```
[🔍 Busca]  [Tipo ▼]  [Status ▼]
[+ Nova Apólice]  [Exportar]
```

###### DataTable — Apólices

| Coluna | Campo |
|---|---|
| Código | code |
| Nº Apólice | policy_number |
| Seguradora | insurer |
| Tipo | type badge |
| Vigência Início | start_date |
| Vigência Fim | end_date |
| Valor Segurado | insured_value |
| Prêmio | premium |
| Ativos Vinculados | COUNT assets |
| Status | status badge |
| Alerta Vencimento | badge (30/60/90 dias) |
| Ações | Ver · Editar · Renovar |

###### CRUD Drawer — Nova/Editar Apólice

**Aba 1: Dados da Apólice**

| Campo | Tipo | Obrigatório |
|---|---|:---:|
| Nº da Apólice | text | ✅ |
| Seguradora | text | ✅ |
| Tipo de Seguro | select | ✅ |
| Data de Início | date | ✅ |
| Data de Término | date | ✅ |
| Valor Segurado Total | currency | ✅ |
| Prêmio Anual | currency | ✅ |
| Franquia | currency | ❌ |
| Contato Nome | text | ❌ |
| Contato Telefone | tel | ❌ |
| Contato E-mail | email | ❌ |
| Documentos | dropzone | ❌ |
| Observações | textarea | ❌ |

**Aba 2: Ativos Vinculados**

- DataTable selecionável dos ativos da entidade
- Coluna extra: Valor Segurado individual
- Totalizador de valor segurado vinculado vs. total da apólice

---

##### 4.9 Kanban — Manutenção
**Rota:** `/patrimonio/manutencao/kanban`  
**Arquivo:** `pages/patrimonio/manutencao_kanban.php`  
**Permissão:** `maintenance.view`

###### Layout Kanban — 6 Colunas

```
┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│  SOLICITADO  │   APROVADO   │  AGENDADO    │ EM PROGRESSO │  CONCLUÍDO   │  CANCELADO   │
│  (requested) │  (approved)  │ (scheduled)  │(in_progress) │ (completed)  │ (cancelled)  │
├──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ Card Maint.  │ Card Maint.  │ Card Maint.  │ Card Maint.  │ Card Maint.  │ Card Maint.  │
│ ...          │ ...          │ ...          │ ...          │ ...          │ ...          │
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

###### Card de Manutenção (Kanban)

```
┌─────────────────────────────────┐
│ 🔴 CRÍTICA   [MAT-2026-0042]    │
│ Título da Manutenção            │
│ 🏷 Ativo: PAT-2024-0012 · Nome  │
│ 🔧 Tipo: Corretiva              │
│ 📅 Agendado: 10/06/2026         │
│ 👤 Técnico: João Silva          │
│ 💰 Estimado: R$ 1.500,00        │
│ [✏ Editar] [➡ Mover] [👁 Ver]  │
└─────────────────────────────────┘
```

###### Controles do Kanban

```
[Unidade ▼]  [Técnico ▼]  [Tipo ▼]  [Prioridade ▼]  [+ Nova Manutenção]
[🔄 Atualizar]  [Lista ↔ Kanban]
```

- **Drag & drop** entre colunas → atualiza status via PATCH `/api/v1/maintenances/{uuid}/status`
- Ao arrastar para "Aprovado" → modal de confirmação de aprovação
- Ao arrastar para "Concluído" → drawer de conclusão (custo real, laudo, próxima manutenção)
- Contador de cards por coluna no header

---

##### 4.10 Relatórios
**Rota:** `/patrimonio/relatorios`  
**Arquivo:** `pages/patrimonio/relatorios.php`  
**Permissão:** `reports.view`

###### Relatórios Disponíveis

| # | Relatório | Filtros | Exportação |
|---|---|---|---|
| R01 | Extrato Completo de Ativos | Unidade · Categoria · Status · Período | CSV · Excel · PDF |
| R02 | Balancete Patrimonial | Período · Unidade · Centro de Custo | Excel · PDF |
| R03 | Depreciação Acumulada por Período | Referência · Método | Excel · PDF |
| R04 | Ativos por Responsável | Unidade · Responsável | CSV · PDF |
| R05 | Histórico de Manutenções | Ativo · Período · Tipo | CSV · PDF |
| R06 | Custo de Manutenção por Ativo/Categoria | Período | Excel · PDF |
| R07 | Transferências por Período | Unidade · Status | CSV · PDF |
| R08 | Relatório de Inventário | Inventário específico | Excel · PDF |
| R09 | Ativos em Garantia | Período de Vencimento | CSV · PDF |
| R10 | Seguros e Vencimentos | Período | CSV · PDF |
| R11 | Ativos em Manutenção | Status · Técnico | CSV · PDF |
| R12 | Ganhos/Perdas em Descartes | Período · Tipo | Excel · PDF |

---

#### 5. Automações

##### 5.1 Depreciação Automática Mensal

```yaml
Automação: auto_depreciation_monthly
Gatilho: Cron — todo dia 1 do mês às 02:00
Ação:
  - Para cada entidade/unidade com ativos ativos e dep_start_date definido
  - Verifica se referência já foi processada
  - Executa cálculo por método (linear/acelerada/degressive)
  - Insere pat_depreciation_entries
  - Atualiza pat_assets.current_value e accumulated_dep
  - Gera pat_depreciation_runs com status=completed
  - Envia notificação ao gestor financeiro
  - Registra em audit_log
```

##### 5.2 Alerta de Garantia a Vencer

```yaml
Automação: alert_warranty_expiry
Gatilho: Cron diário às 08:00
Condição: warranty_expiry BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 30 DAY)
Ação:
  - Notificação in-app para GP e GE
  - E-mail consolidado com lista de ativos
  - Badge vermelho no widget do dashboard
  - Dias configuráveis: 30 · 60 · 90
```

##### 5.3 Alerta de Seguro a Vencer

```yaml
Automação: alert_insurance_expiry
Gatilho: Cron diário às 08:00
Condição: insurance.end_date BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 60 DAY)
Ação:
  - Notificação in-app para GP, GE e FIN
  - E-mail com dados da apólice e valor em risco
  - Atualiza status para 'renewing' se < 30 dias
```

##### 5.4 Manutenção Preventiva Recorrente

```yaml
Automação: maintenance_recurrence
Gatilho: Cron diário às 06:00
Condição: pat_maintenances WHERE is_recurring=1 AND status=completed AND next_due_date <= NOW()+7 dias
Ação:
  - Cria nova manutenção com base na regra RRULE
  - Status: requested
  - Notifica o técnico/responsável designado
  - Vincula à manutenção pai via parent_id
```

##### 5.5 Alerta de Ativo em Estado Crítico

```yaml
Automação: alert_critical_condition
Gatilho: Após salvar pat_assets (hook CRUD)
Condição: condition = 'critical'
Ação:
  - Notificação imediata para GP e GE
  - Cria sugestão automática de manutenção corretiva
  - Badge de alerta no card do ativo no dashboard
```

##### 5.6 Inventário Periódico Automático

```yaml
Automação: auto_inventory_reminder
Gatilho: Cron semestral (1/1 e 1/7 às 09:00)
Ação:
  - Cria pat_inventory em status=draft para cada unidade
  - Notifica GP e GE para iniciar inventário
  - Exibe banner de alerta no dashboard
```

##### 5.7 Contabilização Automática de Depreciação

```yaml
Automação: depreciation_to_accounting
Gatilho: Após conclusão de pat_depreciation_runs
Condição: run.status = 'completed'
Ação:
  - Gera lançamento contábil no módulo Contábil
  - Débito: Conta de Depreciação (configurável por categoria)
  - Crédito: Depreciação Acumulada (configurável por categoria)
  - Histórico: "Depreciação patrimonial ref. YYYY-MM"
```

---

#### 6. Integrações

| Módulo | Tipo | Fluxo |
|---|---|---|
| **Suprimentos** | Bidirecional | Recebimento de compra → cria ativo automaticamente via PO |
| **Financeiro** | Saída | Custo de manutenção → lançamento de despesa |
| **Contábil/Fiscal** | Saída | Depreciação mensal → lançamento contábil automático |
| **RH** | Entrada | Lista de usuários/responsáveis · desligamento → transferência automática |
| **Compliance** | Saída | Descarte → geração de documento fiscal DANFE/laudo |
| **Notificações** | Saída | Webhooks para alertas de garantia, seguro, manutenção |

---

#### 7. API REST — Endpoints

**Base URL:** `/api/v1/`  
**Autenticação:** Bearer JWT  
**Headers obrigatórios:** `X-Entity-ID` · `X-Unit-ID`

##### Assets

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/assets` | Listar ativos (paginado, filtros) | assets.view |
| POST | `/assets` | Criar ativo | assets.create |
| GET | `/assets/{uuid}` | Detalhes do ativo | assets.view |
| PUT | `/assets/{uuid}` | Atualizar ativo | assets.edit |
| DELETE | `/assets/{uuid}` | Soft delete | assets.delete |
| GET | `/assets/{uuid}/history` | Timeline de eventos | assets.view |
| GET | `/assets/{uuid}/depreciations` | Histórico de depreciação | assets.view |
| GET | `/assets/{uuid}/maintenances` | Manutenções do ativo | maintenance.view |
| POST | `/assets/{uuid}/qrcode` | Gerar QR-code | assets.view |
| POST | `/assets/bulk-transfer` | Transferência em lote | transfer.create |
| GET | `/assets/export` | Exportar (CSV/Excel/PDF) | reports.export |

##### Depreciação

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/depreciation/runs` | Histórico de runs | depreciation.run |
| POST | `/depreciation/runs` | Executar depreciação | depreciation.run |
| GET | `/depreciation/runs/{uuid}` | Detalhes do run | depreciation.run |
| GET | `/depreciation/runs/{uuid}/items` | Itens do run | depreciation.run |
| POST | `/depreciation/runs/{uuid}/reverse` | Estornar run | depreciation.adjust |
| GET | `/depreciation/preview` | Prévia sem executar | depreciation.run |

##### Manutenção

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/maintenances` | Listar | maintenance.view |
| POST | `/maintenances` | Criar | maintenance.create |
| GET | `/maintenances/{uuid}` | Detalhes | maintenance.view |
| PUT | `/maintenances/{uuid}` | Atualizar | maintenance.edit |
| PATCH | `/maintenances/{uuid}/status` | Alterar status | maintenance.edit |
| POST | `/maintenances/{uuid}/approve` | Aprovar | maintenance.approve |
| POST | `/maintenances/{uuid}/complete` | Concluir | maintenance.edit |
| POST | `/maintenances/{uuid}/cancel` | Cancelar | maintenance.edit |
| GET | `/maintenances/calendar` | Eventos para calendário | maintenance.view |

##### Transferências

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/transfers` | Listar | transfer.create |
| POST | `/transfers` | Criar | transfer.create |
| GET | `/transfers/{uuid}` | Detalhes | transfer.create |
| POST | `/transfers/{uuid}/approve` | Aprovar | transfer.approve |
| POST | `/transfers/{uuid}/reject` | Rejeitar | transfer.approve |
| POST | `/transfers/{uuid}/complete` | Concluir | transfer.create |

##### Inventário

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/inventories` | Listar | inventory.run |
| POST | `/inventories` | Criar | inventory.run |
| GET | `/inventories/{uuid}` | Detalhes | inventory.run |
| POST | `/inventories/{uuid}/open` | Abrir | inventory.run |
| GET | `/inventories/{uuid}/items` | Listar itens | inventory.run |
| PATCH | `/inventories/{uuid}/items/{item_uuid}` | Contar item | inventory.run |
| POST | `/inventories/{uuid}/close` | Fechar | inventory.close |
| GET | `/inventories/{uuid}/report` | Relatório PDF | reports.export |

##### Descarte

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/disposals` | Listar | disposal.create |
| POST | `/disposals` | Criar | disposal.create |
| GET | `/disposals/{uuid}` | Detalhes | disposal.create |
| POST | `/disposals/{uuid}/approve` | Aprovar | disposal.approve |
| POST | `/disposals/{uuid}/reject` | Rejeitar | disposal.approve |
| POST | `/disposals/{uuid}/complete` | Concluir | disposal.approve |

##### Seguros

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/insurances` | Listar apólices | insurance.view |
| POST | `/insurances` | Criar | insurance.manage |
| GET | `/insurances/{uuid}` | Detalhes | insurance.view |
| PUT | `/insurances/{uuid}` | Atualizar | insurance.manage |
| POST | `/insurances/{uuid}/renew` | Renovar | insurance.manage |
| GET | `/insurances/{uuid}/assets` | Ativos vinculados | insurance.view |
| POST | `/insurances/{uuid}/assets` | Vincular ativos | insurance.manage |

##### Relatórios

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| GET | `/reports/assets/balance` | Balancete patrimonial | reports.view |
| GET | `/reports/assets/depreciation` | Relatório de depreciação | reports.view |
| GET | `/reports/maintenance/costs` | Custos de manutenção | reports.view |
| GET | `/reports/inventory/{uuid}` | Relatório de inventário | reports.view |
| GET | `/reports/disposals/gains-losses` | Ganhos e perdas | reports.view |

---

#### 8. Audit Log & LGPD

##### 8.1 Eventos Auditados

| Tabela | Eventos |
|---|---|
| pat_assets | create · update · delete · view (dados sensíveis) |
| pat_depreciation_runs | create · reverse |
| pat_maintenances | create · update · approve · complete · cancel |
| pat_transfers | create · approve · reject · complete |
| pat_inventories | create · open · close · item_counted |
| pat_disposals | create · approve · reject · complete |
| pat_insurances | create · update · renew |

##### 8.2 Estrutura do Registro

```sql
INSERT INTO audit_logs (
  entity_id, unit_id, user_id, module, action,
  table_name, record_uuid, old_data, new_data,
  ip_address, user_agent, session_id, created_at
) VALUES (...);
```

##### 8.3 LGPD — Controles

| Controle | Implementação |
|---|---|
| Dados pessoais em `responsible_id` | Referência a user_uuid; sem duplicação de CPF/nome |
| Direito de portabilidade | Endpoint `/api/v1/assets/export?format=json` |
| Anonimização | `responsible_id = NULL` + `responsible_name_anon = SHA2(nome,256)` |
| Retenção de dados | Soft delete + purge após 10 anos (configurável) |
| Consentimento para fotos | Flag `consent_photos` em pat_assets |
| Acesso por perfil | RBAC estrito — nenhuma rota sem autenticação |

---

#### 9. Checklist de Entrega

##### Frontend

- [ ] Dashboard com 10 widgets + 6 charts amCharts 5
- [ ] Página Ativos — DataTable completa + CRUD drawer 6 abas
- [ ] Página Depreciação — painel de execução + histórico
- [ ] Página Manutenção — DataTable + CRUD drawer + Calendário
- [ ] Kanban Manutenção — 6 colunas + drag & drop
- [ ] Página Transferências — DataTable + drawer + aprovação
- [ ] Página Inventário — DataTable + execução com QR-code
- [ ] Página Descarte — DataTable + drawer + aprovação
- [ ] Página Seguros — DataTable + drawer + vinculação de ativos
- [ ] Página Relatórios — 12 relatórios com exportação
- [ ] Responsividade mobile para inventário de campo
- [ ] QR-code reader integrado (câmera ou arquivo)

##### Backend

- [ ] 12 tabelas SQL criadas e migradas
- [ ] 60+ endpoints REST documentados
- [ ] Cálculo de depreciação (4 métodos)
- [ ] Engine de automações (7 automações)
- [ ] Geração de QR-code por ativo
- [ ] Exportação PDF/Excel/CSV
- [ ] Integração Suprimentos (auto-criação de ativo por PO)
- [ ] Integração Contábil (lançamento automático de depreciação)
- [ ] Integração Financeiro (custo de manutenção)
- [ ] Sistema de notificações (in-app + e-mail)

##### Qualidade

- [ ] Audit log 100% cobertura em todas as tabelas
- [ ] RBAC validado em todos os endpoints
- [ ] LGPD: anonimização, portabilidade, soft delete
- [ ] Testes de carga em depreciação massiva (10k+ ativos)
- [ ] Validação de formulários client-side (JS) + server-side (PHP)
- [ ] Rate limiting nos endpoints de exportação

---

*Gerado em 2026-06-06 — TotusTuusSoftCloud — Módulo Patrimônio v1.0*
