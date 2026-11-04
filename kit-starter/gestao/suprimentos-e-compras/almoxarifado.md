# Almoxarifado (estoque)

- Portal: Gestão (`gestao.`)
- Área: Suprimentos e compras
- Domínio: entidade: banco da unidade; toda consulta filtra por entidade e unidade do contexto ativo; nenhum dado de outra entidade ou unidade é visível ([03](../../../docs/v2/03-dominio-tenancy.md), [06](../../../docs/v2/06-identidade-acesso.md), seção 12)
- Status: detalhado; regras da v2 copiadas integralmente (seção 13); especificação da v1 absorvida integralmente (seção 14)
- Fonte da v2: [19](../../../docs/v2/19-regras-modulos-3.md), seção 2; [19](../../../docs/v2/19-regras-modulos-3.md), seção 5; [17](../../../docs/v2/17-regras-modulos.md), seção 6
- Fonte da v1: [spec_gestao_armazenamento_completo.md](../../../docs/v2/anexo-v1/spec_gestao_armazenamento_completo.md) (1380 linhas) — absorvida integralmente na seção 14

## 1. Regra de leitura

As seções 1 a 12 resumem e organizam a implementação. A seção 13 é o texto integral do SDD v2 que rege o módulo e prevalece em caso de dúvida. A seção 14 é o texto integral da v1, guardado para que nenhum detalhe se perca; quando ela disser algo diferente das seções 1 a 13, vale a v2. Decisões tomadas por padrão estão no [80](../../../docs/v2/80-decisoes-por-padrao.md).

## 2. Objetivo e escopo

Estoque da unidade: saldo, lotes, validade, movimentos, inventário e ajustes com aprovação.

## 3. Telas

- **Itens e saldos** (DataTable).
- **Movimentos** (entrada, saída, transferência).
- **Inventário** (contagem e ajuste com motivo e aprovação).
- **Endereçamento** (WMS).

## 4. Permissões por portal (extraídas do SDD)

- O SDD não traz tabela por portal para este módulo; vale o escopo da seção 2 e os papéis abaixo.

## 5. Papéis

- `unit.warehouse`: movimentar.
- `unit.purchasing.approver`: aprovar ajuste.
- Regras transversais: default-deny, separação de funções, step-up para ação sensível e revisão de acesso ([78](../../../docs/v2/78-permissoes-e-papeis.md), seções 2 e 5).

## 6. Regras de negócio essenciais

- Saldo nunca negativo; lote e validade para item controlado ([19](../../../docs/v2/19-regras-modulos-3.md), seção 5).

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

### 13.1 [19](../../../docs/v2/19-regras-modulos-3.md), seção 2

#### 2. Duplicidades a resolver

| Módulo A | Módulo B | Sobreposição | Proposta |
|---|---|---|---|
| Armazenamento (estoque, 17 tabelas) | Suprimentos (almoxarifado) | Saldo, movimento, estoque mínimo, rastreabilidade por lote | Suprimentos é dono de estoque e movimento. Armazenamento é renomeado para sistema de arquivos e documentos, sem estoque. **Decidido** em 03/11/2026. |
| Logger | Auditoria | Registro de eventos, bloqueio de IP, alertas de segurança | Auditoria é dona de trilha de negócio e de segurança ([18](../../../docs/v2/18-regras-modulos-2.md), seção 4). Logger técnico fica em [10](../../../docs/v2/10-implantacao-operacao.md), seção 7. |
| Autenticação (v1, 1.001 linhas) | 06 e 07 | Login, sessão, MFA, senha | Consolidar em [06](../../../docs/v2/06-identidade-acesso.md). A especificação de módulo perde o conteúdo que duplica 06. |
| Privacidade global | 07 e Cookies e sessões | Direitos do titular, consentimento, cookies | Consolidar em [07](../../../docs/v2/07-privacidade-lgpd.md). Cookies e sessões fica em 06. |
| Bancos (administração de banco de dados, 305 linhas) | Financeiro (contas bancárias) | Nenhuma: são assuntos diferentes | Bancos sai do escopo. Dados bancários ficam no Financeiro. Ver [34](../../../docs/v2/34-pagamentos-fiscal-bancos-por-portal.md), seção 4. |
| SAC, Chat rápido, Helpdesk | Entre si | Atendimento e tickets | Um único módulo de atendimento. Helpdesk é a base. Proposta na seção 7. |
| Biblioteca acadêmica e Biblioteca completo | Entre si | Acervo, empréstimo, multa | Uma especificação. Escolher a mais recente como base. |

### 13.2 [19](../../../docs/v2/19-regras-modulos-3.md), seção 5

#### 5. Armazenamento (estoque)

Este módulo é tratado como estoque, por causa do conteúdo. Ver seção 2.

| Regra | Detalhe |
|---|---|
| Saldo | Nunca negativo, bloqueio na API (linha 54). |
| Rastreabilidade | Lote, série ou validade obrigatório para item controlado (linha 57). |
| Bloqueio de item | Status `Bloqueado` impede movimento. Motivo registrado. |
| Movimento | Quantidade obrigatória e maior que zero. |

**Pendente:** os 17 DDL precisam da fronteira com Suprimentos (seção 2) antes de validar.

### 13.3 [17](../../../docs/v2/17-regras-modulos.md), seção 6

#### 6. Suprimentos

##### 6.1 Entidades

Requisição, aprovação, cotação, pedido de compra, recebimento, divergência, almoxarifado, itens críticos, fornecedor, avaliação de fornecedor, contrato e ata (sem DDL na v1, ver T-02).

##### 6.2 Regras de negócio (v1, seções 6.2 e 9)

| Regra | Descrição |
|---|---|
| Autoaprovação | Bloqueada acima da faixa da política. |
| Solicitante e aprovador | Não podem ser a mesma pessoa em cenários sensíveis. |
| Pedido | Só emitido por usuário com permissão. |
| Fornecedor bloqueado | Não recebe pedido nem recebimento quando a política exige. |
| Edição após encerramento | Bloqueada. |
| Cotações | Número mínimo por faixa de valor. Fonte única só com justificativa. Motivo da adjudicação registrado. |
| Comparativo | Snapshot gravado no fechamento da cotação. |
| Estoque | Movimento que deixaria saldo negativo é recusado, salvo item de consumo sob encomenda. |
| Divergência de recebimento | Tipo obrigatório (quantidade, item incorreto, avaria, validade, lote, documento fiscal, atraso). |

##### 6.3 Estados

| Entidade | Estados |
|---|---|
| Requisição | `rascunho`, `em_aprovacao`, `aprovada`, `reprovada`, `cancelada` |
| Pedido | `emitido`, `em_transito`, `recebido_parcial`, `recebido`, `cancelado` |
| Fornecedor | `ativo`, `bloqueado`, `inativo` |

##### 6.4 Campos mínimos a definir

Como a v1 não tem DDL, os campos de requisição, pedido, item e fornecedor precisam ser escritos antes. Lista mínima proposta:

- Requisição: solicitante, unidade, centro de custo, itens (item, quantidade, unidade de medida), valor estimado, justificativa, data limite de SLA.
- Item: código, descrição, unidade de medida, estoque mínimo, estoque atual, fornecedor preferencial.
- Fornecedor: CNPJ válido, situação documental, validade de certificados, situação (`ativo`, `bloqueado`).

## 14. Conteúdo integral da v1 (absorvido)

### SPEC — Módulo Armazenamento
**Versão:** 1.0  
**Status:** Draft Funcional Completo  
**Módulo:** Storage / Warehouse Management System (WMS)  
**Projeto:** TotusTuusSoftCloud (TTSC)  
**Stack:** PHP 8 puro · MariaDB · Tailwind CSS 4.2 · Supabase · amCharts 5 · Fetch API · FontAwesome 7.2.0  
**Contexto:** SaaS multi-entidade · multi-unidade · multi-usuário · banco segregado por entidade/unidade  
**Identidade padrão:** `id` (auto_increment ordenação) · `uuid` (público/API) · `code` (legível humano)

- Language Standard: Global English
---

#### ÍNDICE

1. [Visão Geral](#1-visão-geral)
2. [Arquitetura de Páginas](#2-arquitetura-de-páginas)
3. [Dashboard de Armazenamento](#3-dashboard-de-armazenamento)
4. [Localizações e Estrutura Física](#4-localizações-e-estrutura-física)
5. [Gestão de Itens / SKUs](#5-gestão-de-itens--skus)
6. [Movimentações (Entradas e Saídas)](#6-movimentações-entradas-e-saídas)
7. [Inventário e Contagem](#7-inventário-e-contagem)
8. [Kanban de Operações](#8-kanban-de-operações)
9. [Automações](#9-automações)
10. [Controles e Rastreabilidade](#10-controles-e-rastreabilidade)
11. [Gerenciamentos](#11-gerenciamentos)
12. [Schema SQL](#12-schema-sql)
13. [Endpoints da API](#13-endpoints-da-api)
14. [Permissões RBAC](#14-permissões-rbac)
15. [Requisitos Não Funcionais](#15-requisitos-não-funcionais)
16. [Checklist de Entrega](#16-checklist-de-entrega)

---

#### 1. VISÃO GERAL

##### 1.1 Objetivo
Gerenciar o ciclo completo de armazenamento físico e virtual de itens dentro das entidades/unidades do SaaS TTSC: recebimento, guarda, movimentação interna, separação, expedição, inventário e rastreabilidade por lote/série/validade.

##### 1.2 Perfis de Acesso

| Código | Perfil                | Descrição                                    |
|--------|-----------------------|----------------------------------------------|
| SA     | Super Admin           | Acesso total a todas as entidades/unidades   |
| GE     | Gestor de Entidade    | Acesso total à entidade vinculada            |
| GU     | Gestor de Unidade     | Acesso total à unidade vinculada             |
| ALM    | Almoxarife / Operador | Operação diária: entradas, saídas, contagens |
| AUD    | Auditor               | Leitura completa, sem escrita                |
| FIN    | Financeiro            | Leitura de custos e valorizações             |
| VIS    | Visitante             | Leitura limitada (sem custos/custos ocultos) |

##### 1.3 Regras de Negócio Globais

- Todo item deve ter `uuid` único e `code` alfanumérico imutável após criação.
- Saldo de estoque nunca pode ser negativo (bloqueio a nível de API).
- Toda movimentação gera registro imutável em `stg_movements` (soft-delete proibido).
- Validade (FEFO), FIFO e LIFO são estratégias configuráveis por depósito.
- Rastreabilidade obrigatória: lote, série ou validade (ao menos um) para itens controlados.
- Cada operação é auditada: `user_id`, `ip`, `timestamp`, `action`, `payload_before`, `payload_after`.

---

#### 2. ARQUITETURA DE PÁGINAS

| # | Rota PHP                                | Título da Página               | Tipo       |
|---|-----------------------------------------|-------------------------------|------------|
| 1 | `/storage/dashboard.php`                | Dashboard de Armazenamento    | Dashboard  |
| 2 | `/storage/locations.php`                | Localizações / Estrutura Física| Grid+CRUD  |
| 3 | `/storage/items.php`                    | Itens / SKUs                  | Datatable  |
| 4 | `/storage/movements/entries.php`        | Entradas                      | Datatable  |
| 5 | `/storage/movements/exits.php`          | Saídas                        | Datatable  |
| 6 | `/storage/movements/transfers.php`      | Transferências Internas       | Datatable  |
| 7 | `/storage/inventory.php`                | Inventário e Contagem         | Datatable  |
| 8 | `/storage/kanban.php`                   | Kanban de Operações           | Kanban     |
| 9 | `/storage/automations.php`              | Automações                    | Config     |
|10 | `/storage/controls/expiry.php`          | Controle de Validade          | Datatable  |
|11 | `/storage/controls/lots.php`            | Controle de Lotes             | Datatable  |
|12 | `/storage/controls/serial.php`          | Controle de Série             | Datatable  |
|13 | `/storage/controls/audit.php`           | Trilha de Auditoria           | Datatable  |
|14 | `/storage/management/warehouses.php`    | Gerenciar Depósitos           | CRUD       |
|15 | `/storage/management/categories.php`    | Gerenciar Categorias          | CRUD       |
|16 | `/storage/management/uom.php`           | Unidades de Medida            | CRUD       |
|17 | `/storage/management/suppliers.php`     | Fornecedores                  | CRUD       |
|18 | `/storage/management/rules.php`         | Regras de Estoque             | Config     |

---

#### 3. DASHBOARD DE ARMAZENAMENTO

**Arquivo:** `/storage/dashboard.php`

##### 3.1 Widgets KPI (Topo — Bento Grid 4 colunas)

| Widget                  | Ícone FA           | Cor       | Cálculo                                          |
|-------------------------|--------------------|-----------|--------------------------------------------------|
| Total de Itens Ativos   | fa-boxes-stacked   | azul      | COUNT(stg_items WHERE status = 'active')         |
| Valor Total em Estoque  | fa-dollar-sign     | verde     | SUM(qty * unit_cost) por unidade/entidade        |
| Movimentações Hoje      | fa-arrow-right-arrow-left | laranja | COUNT(stg_movements WHERE DATE = today)    |
| Itens Abaixo do Mínimo  | fa-triangle-exclamation | vermelho | COUNT(stg_stock WHERE qty < min_qty)        |
| Itens com Validade ≤30d | fa-calendar-xmark  | amarelo   | COUNT(stg_lots WHERE expiry_date ≤ today+30)    |
| Ocupação dos Depósitos  | fa-warehouse       | roxo      | SUM(used_positions) / SUM(total_positions) × 100|

> Layout: 3 widgets linha 1 (largura 1/3 cada) + 3 widgets linha 2 (largura 1/3 cada).

##### 3.2 Charts (amCharts 5)

###### Chart 1 — Evolução de Movimentações (Linha, 30 dias)
- Eixo X: data (últimos 30 dias)
- Eixo Y: quantidade de operações
- Séries: Entradas (verde), Saídas (vermelho), Transferências (azul)
- Tooltip: data · tipo · qtd operações · volume total

###### Chart 2 — Distribuição por Categoria (Donut)
- Fatias: categorias de itens
- Legenda lateral com % e valor R$
- Click em fatia → filtra datatable de itens

###### Chart 3 — Top 10 Itens mais Movimentados (Barra Horizontal)
- Eixo Y: nome do item
- Eixo X: total de movimentações no mês
- Cor: gradiente azul claro → azul escuro

###### Chart 4 — Ocupação por Depósito (Barra Empilhada)
- Eixo X: nome do depósito
- Barras: Ocupado (azul) / Livre (cinza claro)
- Linha secundária: % ocupação

###### Chart 5 — Validades Próximas (Timeline/Gantt mini)
- Eixo X: datas (hoje → +90 dias)
- Barras por item: banda colorida por urgência (verde >60d, amarelo 30–60d, vermelho <30d)

##### 3.3 Datatable Resumo — Alertas Críticos

| Coluna           | Tipo     | Notas                          |
|------------------|----------|-------------------------------|
| Código           | text     | link para item                 |
| Item             | text     | nome + SKU                    |
| Depósito         | badge    | nome do depósito               |
| Tipo de Alerta   | badge    | Estoque Mínimo / Validade / Bloqueado |
| Saldo Atual      | number   | qty com unidade de medida      |
| Mínimo Config.   | number   | qty mínima configurada         |
| Validade         | date     | data de validade mais próxima  |
| Ação             | button   | Repor / Ver / Ajustar          |

**Filtros rápidos:** Todos · Estoque mínimo · Validade · Bloqueados  
**Paginação:** 10 / 25 / 50  
**Export:** CSV · XLSX · PDF

---

#### 4. LOCALIZAÇÕES E ESTRUTURA FÍSICA

**Arquivo:** `/storage/locations.php`

##### 4.1 Visão Geral
Gerencia a árvore física: Entidade → Unidade → Depósito → Zona → Corredor → Prateleira → Posição.

##### 4.2 Controles de Página

- **Botão:** `+ Nova Localização` → abre drawer de criação
- **Seletor de Depósito:** dropdown filtra toda a visualização
- **Modo de visualização:** Toggle `Árvore | Grid | Mapa 2D`
- **Campo de busca:** por código ou nome de localização
- **Breadcrumb:** Entidade › Unidade › Depósito › Zona

##### 4.3 Visualização em Árvore (padrão)

```
📦 Depósito Central (CD-01)
  ├── 🔵 Zona A — Frios
  │   ├── Corredor A1
  │   │   ├── Prateleira A1-01 [12/20 posições ocupadas]
  │   │   └── Prateleira A1-02 [8/20 posições ocupadas]
  └── 🟡 Zona B — Seco
      └── Corredor B1
          └── Prateleira B1-01 [20/20 — LOTADA]
```

- Ícone de status por cor: verde (disponível), amarelo (>80%), vermelho (lotado), cinza (inativo)
- Click na posição → abre painel lateral com itens alocados na posição

##### 4.4 Visualização Grid 2D

- Grid CSS representando corredores × prateleiras
- Cada célula = uma posição física
- Cor por ocupação (heatmap)
- Hover → tooltip com conteúdo
- Click → drawer de detalhe da posição

##### 4.5 Datatable de Localizações

| Coluna           | Tipo    |
|------------------|---------|
| Código           | text    |
| Nome             | text    |
| Tipo             | badge   |
| Depósito / Zona  | text    |
| Capacidade       | number  |
| Ocupado          | progress|
| Status           | badge   |
| Ações            | icon    |

##### 4.6 CRUD Drawers — Localização

###### Drawer: Nova / Editar Localização
- **Campos:**
  - `code` — gerado automaticamente, editável, único
  - `name` — nome descritivo
  - `type` — select: Depósito / Zona / Corredor / Prateleira / Posição
  - `parent_id` — select hierárquico (pai desta localização)
  - `warehouse_id` — select do depósito raiz
  - `capacity` — número inteiro (0 = ilimitado)
  - `uom_id` — unidade de medida de capacidade (m², paletes, caixas)
  - `temperature_min/max` — campos numéricos para zonas climatizadas
  - `is_quarantine` — checkbox (itens em quarentena)
  - `is_picking` — checkbox (posição de picking ativo)
  - `status` — toggle ativo/inativo
  - `notes` — textarea
- **Botões:** Salvar · Cancelar · (editar) Desativar

---

#### 5. GESTÃO DE ITENS / SKUs

**Arquivo:** `/storage/items.php`

##### 5.1 Controles da Página

- **Botão:** `+ Novo Item`
- **Filtros:** Categoria · Status · Tipo de Controle · Depósito
- **Busca:** por código, nome, EAN/barcode
- **Ações em Lote:** Ativar · Inativar · Exportar · Realocar depósito
- **Toggle:** Ver apenas abaixo do mínimo

##### 5.2 Datatable Principal de Itens

| Coluna              | Tipo      | Notas                               |
|---------------------|-----------|-------------------------------------|
| #                   | checkbox  | seleção em lote                     |
| Código / SKU        | text      | link para detalhe                   |
| Nome                | text      | nome + descrição curta              |
| EAN/Barcode         | text      | código de barras                    |
| Categoria           | badge     |                                     |
| Unidade de Medida   | text      |                                     |
| Saldo Atual         | number    | qty + unidade                       |
| Saldo Reservado     | number    | qty reservada por pedidos/saídas    |
| Custo Unitário      | currency  | R$ valor                            |
| Valor Total         | currency  | saldo × custo unitário              |
| Controle            | icons     | 🔵 Lote · 🔴 Série · 🟡 Validade    |
| Mín / Máx           | text      | qty mínima / máxima configurada     |
| Status              | badge     | Ativo / Inativo / Bloqueado         |
| Ações               | icon-btn  | Ver · Editar · Movimentar · Excluir |

**Paginação:** 15 / 30 / 50 / 100  
**Export:** CSV · XLSX · PDF · Etiquetas (ZPL)  
**Ordenação:** por qualquer coluna

##### 5.3 CRUD Drawers — Item

###### Drawer: Novo / Editar Item — Aba "Dados Gerais"
- `code` (automático, editável, único)
- `name` (obrigatório)
- `description` (textarea)
- `ean` (barcode — scanner ou digitação)
- `category_id` (select com categorias)
- `subcategory_id` (select dependente)
- `uom_id` (unidade de medida principal)
- `secondary_uom_id` + `conversion_factor` (unidade secundária + fator)
- `item_type` (select: Produto / Insumo / Embalagem / Ferramenta / EPI)
- `status` (toggle)
- `image` (upload de foto — máx 2MB, WebP/JPG)

###### Drawer: Novo / Editar Item — Aba "Estoque"
- `warehouse_id` (depósito padrão)
- `location_id` (posição padrão)
- `min_qty` (estoque mínimo)
- `max_qty` (estoque máximo)
- `reorder_point` (ponto de reposição)
- `reorder_qty` (quantidade de reposição)
- `stock_strategy` (select: FEFO / FIFO / LIFO)
- `is_lot_controlled` (checkbox)
- `is_serial_controlled` (checkbox)
- `is_expiry_controlled` (checkbox)
- `expiry_alert_days` (dias de antecedência para alerta)

###### Drawer: Novo / Editar Item — Aba "Custos"
- `costing_method` (select: Média Ponderada / PEPS / Padrão Fixo)
- `standard_cost` (custo padrão R$)
- `last_purchase_cost` (custo última compra — leitura)
- `average_cost` (custo médio — calculado automaticamente, leitura)
- `currency` (select moeda)

###### Drawer: Detalhe / Visualização do Item
- Todas as informações em modo leitura
- Histórico de movimentações (datatable mini, últimas 10)
- Gráfico de evolução de saldo (linha, 90 dias) — amCharts 5
- Posições onde o item está alocado (lista com qtd por posição)
- Botões: Editar · Movimentar · Gerar Etiqueta · Bloquear

---

#### 6. MOVIMENTAÇÕES (ENTRADAS E SAÍDAS)

##### 6.1 Entradas — `/storage/movements/entries.php`

###### 6.1.1 Controles de Página
- **Botão:** `+ Nova Entrada`
- **Filtros:** Data · Depósito · Tipo de Entrada · Status · Fornecedor
- **Busca:** por número do documento, NF, pedido de compra
- **Ações em Lote:** Confirmar · Cancelar · Exportar

###### 6.1.2 Datatable de Entradas

| Coluna             | Tipo     | Notas                                    |
|--------------------|----------|------------------------------------------|
| Nº Documento       | text     | link para detalhe                        |
| Data               | date     |                                          |
| Tipo               | badge    | NF Entrada / Transferência / Ajuste / Devolução |
| Fornecedor         | text     |                                          |
| Depósito Destino   | text     |                                          |
| Qtd Itens          | number   | total de linhas                          |
| Volume Total       | number   | qtd total movimentada                    |
| Valor Total        | currency | R$                                       |
| Status             | badge    | Rascunho / Aguardando / Confirmada / Cancelada |
| Operador           | text     | usuário que lançou                       |
| Ações              | icon-btn | Ver · Confirmar · Cancelar · Imprimir    |

###### 6.1.3 Drawer: Nova Entrada

**Seção Cabeçalho:**
- `entry_type` (select: NF Entrada / Devolução de Saída / Ajuste Positivo / Transferência Recebida / Inventário)
- `warehouse_id` (depósito destino)
- `supplier_id` (select — visível para NF e Devolução)
- `document_number` (nº NF / nº pedido)
- `document_date` (data emissão)
- `entry_date` (data de entrada — default hoje)
- `notes` (observações)

**Seção Itens (tabela inline editável):**

| Campo            | Tipo      | Notas                             |
|------------------|-----------|-----------------------------------|
| Item             | autocomplete | busca por código/nome/EAN    |
| Qtd              | number    | obrigatório                       |
| Unidade          | text      | preenchido automaticamente        |
| Localização      | select    | posição de guarda no depósito     |
| Lote             | text      | obrigatório se is_lot_controlled  |
| Nº Série         | text      | obrigatório se is_serial_controlled|
| Validade         | date      | obrigatório se is_expiry_controlled|
| Custo Unit.      | currency  | R$                                |
| Subtotal         | currency  | calculado automaticamente         |
| Ação             | icon-btn  | remover linha                     |

- **Botão:** `+ Adicionar Item`
- **Botão:** `Importar da NF (XML)` — parse automático de XML NF-e
- **Rodapé:** Total Itens · Total Volume · Total R$
- **Botões:** Salvar Rascunho · Confirmar Entrada · Cancelar

---

##### 6.2 Saídas — `/storage/movements/exits.php`

###### 6.2.1 Controles de Página
- **Botão:** `+ Nova Saída`
- **Filtros:** Data · Depósito · Tipo de Saída · Status · Destino
- **Busca:** por número do documento, pedido, requisição

###### 6.2.2 Datatable de Saídas

| Coluna             | Tipo     | Notas                                              |
|--------------------|----------|----------------------------------------------------|
| Nº Documento       | text     | link para detalhe                                  |
| Data               | date     |                                                    |
| Tipo               | badge    | Requisição / Venda / Devolução a Fornecedor / Ajuste / Expedição |
| Destino / Solicitante | text  |                                                    |
| Depósito Origem    | text     |                                                    |
| Qtd Itens          | number   |                                                    |
| Valor Total        | currency |                                                    |
| Status             | badge    | Rascunho / Separação / Confirmada / Cancelada      |
| Operador           | text     |                                                    |
| Ações              | icon-btn | Ver · Separar · Confirmar · Cancelar               |

###### 6.2.3 Drawer: Nova Saída

**Seção Cabeçalho:**
- `exit_type` (Requisição Interna / Venda / Expedição / Devolução Fornecedor / Ajuste Negativo)
- `warehouse_id` (depósito origem)
- `requester_id` (usuário/setor solicitante — para requisições internas)
- `destination` (texto livre ou select de destino externo)
- `document_number` · `document_date` · `exit_date`
- `priority` (select: Normal / Urgente / Crítico)
- `notes`

**Seção Itens (tabela inline editável — mesma estrutura da Entrada):**
- Ao selecionar item: sistema sugere automaticamente lotes/posições seguindo estratégia FEFO/FIFO/LIFO do depósito
- Alerta visual se qtd solicitada > saldo disponível
- Bloqueio de confirmação se saldo insuficiente

**Botões:** Salvar Rascunho · Iniciar Separação · Confirmar Saída · Cancelar

---

##### 6.3 Transferências — `/storage/movements/transfers.php`

###### 6.3.1 Datatable de Transferências

| Coluna              | Tipo     | Notas                              |
|---------------------|----------|------------------------------------|
| Nº Transferência    | text     |                                    |
| Data                | date     |                                    |
| Tipo                | badge    | Interna (mesma unidade) / Externa (entre unidades) |
| Depósito Origem     | text     |                                    |
| Depósito Destino    | text     |                                    |
| Qtd Itens           | number   |                                    |
| Status              | badge    | Aguardando · Em Trânsito · Recebida · Cancelada |
| Ações               | icon-btn |                                    |

###### 6.3.2 Drawer: Nova Transferência

- `transfer_type` (Interna / Entre Unidades)
- `origin_warehouse_id` · `origin_location_id`
- `destination_warehouse_id` · `destination_location_id`
- `transfer_date` · `expected_arrival_date`
- `responsible_id` (responsável pelo transporte)
- Tabela de itens com: item · qtd · lote · série · posição origem → posição destino
- **Botões:** Salvar · Iniciar Transferência · Confirmar Recebimento · Cancelar

---

#### 7. INVENTÁRIO E CONTAGEM

**Arquivo:** `/storage/inventory.php`

##### 7.1 Controles da Página

- **Botão:** `+ Novo Inventário`
- **Filtros:** Depósito · Categoria · Status · Data
- **Busca:** por nº de inventário

##### 7.2 Datatable de Inventários

| Coluna           | Tipo     | Notas                                          |
|------------------|----------|------------------------------------------------|
| Nº Inventário    | text     | link para detalhe                              |
| Depósito         | text     |                                                |
| Tipo             | badge    | Geral / Parcial por Zona / Parcial por Categoria / Cíclico |
| Data Início      | date     |                                                |
| Data Fim         | date     |                                                |
| Itens Contados   | progress | x de y itens                                   |
| Divergências     | number   | qtd de itens com diferença                    |
| Valor Diferença  | currency | R$ impacto total das divergências              |
| Status           | badge    | Planejado / Em Andamento / Aguardando Aprovação / Concluído / Cancelado |
| Ações            | icon-btn | Iniciar · Contar · Revisar · Aprovar · Fechar  |

##### 7.3 Drawer: Novo Inventário

- `inventory_type` (Geral / Parcial Zona / Parcial Categoria / Cíclico)
- `warehouse_id` (depósito)
- `zone_id` (opcional — para parcial por zona)
- `category_id` (opcional — para parcial por categoria)
- `start_date` · `end_date`
- `freeze_movements` (checkbox — bloquear movimentações durante inventário)
- `count_method` (select: Simples / Dupla Contagem / Cega)
- `responsible_id` (responsável)
- `notes`
- **Botão:** Criar e Gerar Lista de Contagem

##### 7.4 Página de Contagem (modal full ou página dedicada)

- Lista de itens com: código · nome · localização · qtd sistema (oculta se contagem cega) · qtd contada (input) · diferença (calculada)
- Filtro: Todos · Não contados · Com divergência
- Botão: `Salvar Contagem` (parcial, pode retomar)
- Botão: `Finalizar Contagem`
- Importar contagem via planilha CSV

##### 7.5 Aprovação de Divergências

- Datatable com itens divergentes: qtd sistema · qtd contada · diferença · custo unit. · impacto R$
- Ações por item: Aprovar Ajuste · Recontar · Ignorar
- Aprovação em lote
- Ao aprovar: gera `stg_movements` de tipo `AJUSTE_INVENTARIO` automaticamente

---

#### 8. KANBAN DE OPERAÇÕES

**Arquivo:** `/storage/kanban.php`

##### 8.1 Configuração do Kanban

- **Filtros de topo:** Depósito · Tipo de Operação · Período · Responsável · Prioridade
- **Toggle:** Ver como Kanban / Ver como Lista
- **Botão:** `+ Nova Tarefa Operacional`

##### 8.2 Colunas do Kanban

| Coluna               | Descrição                                      | Cor      |
|----------------------|------------------------------------------------|----------|
| 📥 Aguardando        | Operações criadas, não iniciadas               | cinza    |
| 🔄 Em Separação      | Saídas em processo de picking                  | azul     |
| 🔍 Em Conferência    | Entradas recebidas aguardando conferência      | amarelo  |
| 🚚 Em Trânsito       | Transferências em andamento                    | laranja  |
| ⚠️ Com Pendência     | Divergência, bloqueio ou item faltante         | vermelho |
| ✅ Concluído         | Operações finalizadas hoje                     | verde    |

##### 8.3 Card de Operação (Kanban Card)

```
┌─────────────────────────────────────────┐
│ 🔴 URGENTE  [TRF-2024-0892]             │
│ Transferência: CD-01 → Filial SP        │
│ ─────────────────────────────────────── │
│ 📦 12 itens · 340 unidades              │
│ 👤 João Silva                            │
│ 🕐 Início: 08/06/2026 14:00             │
│ ─────────────────────────────────────── │
│ [Ver] [Mover] [Atribuir]               │
└─────────────────────────────────────────┘
```

**Campos do card:** badge de prioridade · nº documento · tipo operação · depósito origem/destino · qtd itens/volume · responsável · data prevista · botões de ação rápida.

##### 8.4 Drawer: Nova Tarefa / Editar Card

- `task_type` (Entrada / Saída / Transferência / Inventário / Ajuste / Manutenção de Localização)
- `linked_document_uuid` (vincular a documento existente)
- `warehouse_id`
- `priority` (Normal / Urgente / Crítico)
- `responsible_id`
- `due_date` · `due_time`
- `description`
- `checklist` (lista de subtarefas com checkbox)
- **Botões:** Salvar · Mover Para · Concluir · Cancelar

##### 8.5 Regras do Kanban

- Drag-and-drop entre colunas (atualiza status via API PATCH)
- Ao mover para "Concluído": exige confirmação e registro de `completed_at` + `completed_by`
- Cards com `due_date` vencido → highlight vermelho automático
- Contadores no cabeçalho de cada coluna

---

#### 9. AUTOMAÇÕES

**Arquivo:** `/storage/automations.php`

##### 9.1 Lista de Automações Disponíveis

| Automação                        | Gatilho                                  | Ação                                              |
|----------------------------------|------------------------------------------|---------------------------------------------------|
| Alerta de Estoque Mínimo         | Saldo ≤ min_qty após movimentação       | Notificação + Kanban card automático              |
| Alerta de Validade Próxima       | Diário (cron) · expiry_date ≤ hoje+N    | E-mail + notificação in-app + badge no item       |
| Bloqueio de Saldo Negativo       | Antes de confirmar saída                 | Bloqueia operação + mensagem de erro              |
| Reposição Automática             | Saldo ≤ reorder_point                   | Cria rascunho de Solicitação de Compra no módulo Suprimentos |
| Conferência Obrigatória em NF    | Nova entrada tipo NF                     | Bloqueia confirmação até conferência item a item  |
| Auditoria de Movimentação        | Toda movimentação confirmada             | Grava log imutável em stg_audit_log               |
| Inventário Cíclico               | Cron semanal/mensal por configuração     | Cria inventário automático para zonas definidas   |
| Notificação de Transferência     | Status muda para "Em Trânsito"           | Notifica destino com previsão de chegada          |
| Quarentena Automática            | Entrada com lote já existente divergente | Move item para localização de quarentena          |
| Relatório Diário de Estoque      | Cron 23:55 todo dia                      | Gera snapshot diário em stg_stock_snapshots       |

##### 9.2 Controles da Página de Automações

- Datatable com todas as automações: Nome · Tipo (Evento / Cron) · Status (toggle ativo/inativo) · Última execução · Próxima execução · Ações
- **Drawer: Configurar Automação**
  - `automation_name`
  - `trigger_type` (Evento de Movimentação / Cron / Webhook)
  - `cron_expression` (se cron — input com preview legível: "Todo dia às 23:55")
  - `conditions` (builder visual: IF campo OPERADOR valor AND/OR ...)
  - `actions` (checklist: Notificação In-App / E-mail / Criar Tarefa Kanban / Chamar Webhook / Criar Rascunho Suprimentos)
  - `recipients` (usuários / perfis que recebem notificação)
  - `is_active` (toggle)

---

#### 10. CONTROLES E RASTREABILIDADE

##### 10.1 Controle de Validade — `/storage/controls/expiry.php`

###### Datatable de Validades

| Coluna          | Tipo     | Notas                                           |
|-----------------|----------|-------------------------------------------------|
| Item / SKU      | text     |                                                 |
| Lote            | text     |                                                 |
| Depósito / Posição | text  |                                                 |
| Quantidade      | number   |                                                 |
| Validade        | date     | formatada DD/MM/YYYY                            |
| Dias Restantes  | number   | calculado: expiry_date − hoje                   |
| Status          | badge    | 🟢 OK (>60d) · 🟡 Alerta (30–60d) · 🔴 Crítico (<30d) · ⚫ Vencido |
| Valor em Risco  | currency | qty × unit_cost                                 |
| Ações           | icon-btn | Alocar p/ Picking · Quarentena · Baixar · Ver   |

**Filtros:** Depósito · Categoria · Status de Validade · Período  
**Widget Resumo topo:** Total itens vencendo 30d · Valor em risco · Itens já vencidos

---

##### 10.2 Controle de Lotes — `/storage/controls/lots.php`

###### Datatable de Lotes

| Coluna            | Tipo     | Notas                                 |
|-------------------|----------|---------------------------------------|
| Nº Lote           | text     | link → rastreabilidade completa       |
| Item              | text     |                                       |
| Fornecedor        | text     |                                       |
| Data de Entrada   | date     |                                       |
| Validade          | date     |                                       |
| Qtd Inicial       | number   |                                       |
| Qtd Atual         | number   |                                       |
| Qtd Saída         | number   |                                       |
| Posições          | text     | lista de posições onde está alocado   |
| Status            | badge    | Disponível / Quarentena / Esgotado / Bloqueado |
| Ações             | icon-btn | Rastrear · Bloquear · Quarentena · Histórico |

**Drawer: Histórico do Lote** — timeline de todas as movimentações que envolveram o lote: data · tipo · qtd · depósito · operador · documento.

---

##### 10.3 Controle de Série — `/storage/controls/serial.php`

###### Datatable de Números de Série

| Coluna            | Tipo     | Notas                              |
|-------------------|----------|------------------------------------|
| Nº Série          | text     |                                    |
| Item              | text     |                                    |
| Status            | badge    | Em Estoque / Alocado / Expedido / Baixado |
| Depósito / Posição| text     |                                    |
| Data Entrada      | date     |                                    |
| Documento Entrada | text     |                                    |
| Documento Saída   | text     |                                    |
| Destino           | text     |                                    |
| Ações             | icon-btn | Ver histórico · Bloquear           |

---

##### 10.4 Trilha de Auditoria — `/storage/controls/audit.php`

###### Datatable de Auditoria

| Coluna          | Tipo     | Notas                                     |
|-----------------|----------|-------------------------------------------|
| Data/Hora       | datetime | timestamp UTC, exibido no fuso local      |
| Usuário         | text     | nome + perfil                             |
| IP              | text     |                                           |
| Ação            | badge    | CREATE / UPDATE / DELETE / CONFIRM / CANCEL |
| Entidade        | text     | nome da tabela/objeto                     |
| UUID do Registro| text     | link para o registro                      |
| Resumo          | text     | descrição legível da ação                 |
| Payload Antes   | icon-btn | ver JSON                                  |
| Payload Depois  | icon-btn | ver JSON                                  |

**Filtros:** Usuário · Período · Ação · Entidade  
**Exportação:** CSV · XLSX (auditoria nunca exporta payloads completos sem permissão SA/AUD)

---

#### 11. GERENCIAMENTOS

##### 11.1 Depósitos — `/storage/management/warehouses.php`

###### Datatable de Depósitos

| Coluna          | Tipo     |
|-----------------|----------|
| Código          | text     |
| Nome            | text     |
| Unidade         | text     |
| Tipo            | badge    |
| Capacidade      | number   |
| Ocupação        | progress |
| Status          | badge    |
| Ações           | icon-btn |

###### Drawer: Novo / Editar Depósito

- `code` · `name` · `description`
- `unit_id` (unidade vinculada)
- `warehouse_type` (select: Almoxarifado / Centro de Distribuição / Câmara Fria / Farmácia / Arquivo / Externo)
- `address` (endereço físico — opcional)
- `manager_id` (responsável)
- `capacity` · `capacity_uom`
- `default_strategy` (select: FEFO / FIFO / LIFO)
- `is_picking_active` (checkbox)
- `allows_negative` (checkbox — apenas SA pode ativar)
- `status` (toggle)

---

##### 11.2 Categorias — `/storage/management/categories.php`

###### Datatable de Categorias

| Coluna         | Tipo     | Notas              |
|----------------|----------|--------------------|
| Código         | text     |                    |
| Nome           | text     |                    |
| Pai            | text     | categoria pai      |
| Itens          | number   | qtd de itens vinculados |
| Status         | badge    |                    |
| Ações          | icon-btn |                    |

###### Drawer: Nova / Editar Categoria

- `code` · `name` · `parent_id` (hierarquia até 3 níveis) · `description` · `is_active`

---

##### 11.3 Unidades de Medida — `/storage/management/uom.php`

###### Datatable de UOM

| Coluna             | Tipo     |
|--------------------|----------|
| Código             | text     |
| Nome               | text     |
| Tipo               | badge    |
| Fator de Conversão | number   |
| Base               | text     |
| Status             | badge    |
| Ações              | icon-btn |

###### Drawer: Nova / Editar UOM

- `code` · `name` · `uom_type` (Quantidade / Peso / Volume / Comprimento / Área)
- `is_base` (toggle — unidade base do tipo)
- `base_uom_id` · `conversion_factor`
- `decimal_places` (casas decimais permitidas)

---

##### 11.4 Fornecedores — `/storage/management/suppliers.php`

###### Datatable de Fornecedores

| Coluna          | Tipo     |
|-----------------|----------|
| Código          | text     |
| Razão Social    | text     |
| CNPJ / CPF      | text     |
| Contato         | text     |
| Categorias      | badges   |
| Status          | badge    |
| Ações           | icon-btn |

###### Drawer: Novo / Editar Fornecedor

- `code` · `company_name` · `trade_name` · `document` (CNPJ/CPF) · `state_registration`
- `contact_name` · `email` · `phone` · `website`
- `address` (campos separados: logradouro, número, complemento, bairro, cidade, estado, CEP, país)
- `category_ids` (multiselect — categorias de produtos fornecidos)
- `lead_time_days` (prazo médio de entrega)
- `payment_terms` (condições de pagamento)
- `is_preferred` (toggle — fornecedor preferencial)
- `status` (toggle)
- `notes`

---

##### 11.5 Regras de Estoque — `/storage/management/rules.php`

Página de configurações avançadas, sem datatable, estruturada em abas:

**Aba: Estratégias de Saída**
- Por depósito: definir FEFO / FIFO / LIFO individualmente
- Herança: unidade → depósito (checkbox herdar)

**Aba: Alertas**
- Threshold de alerta de mínimo: percentual ou valor absoluto
- Dias de antecedência para alerta de validade: input numérico
- Frequência de envio de alertas: Tempo Real / Resumo Diário / Semanal

**Aba: Bloqueios**
- Bloquear saída se saldo insuficiente: toggle (global por unidade)
- Exigir conferência em entradas: toggle por tipo de entrada
- Exigir dupla contagem em inventário: toggle
- Quarentena automática de lotes com divergência: toggle

**Aba: Integrações**
- Endpoint webhook de alerta externo: input URL + botão testar
- Integração com módulo Suprimentos (reposição automática): toggle + config de perfil aprovador

---

#### 12. SCHEMA SQL

```sql
-- ============================================================
-- MÓDULO: ARMAZENAMENTO (stg_*)
-- Banco: segregado por entidade/unidade
-- ============================================================

CREATE TABLE stg_warehouses (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code            VARCHAR(20) NOT NULL UNIQUE,
    name            VARCHAR(120) NOT NULL,
    description     TEXT,
    unit_id         BIGINT UNSIGNED NOT NULL,
    warehouse_type  ENUM('almoxarifado','cd','camara_fria','farmacia','arquivo','externo') NOT NULL DEFAULT 'almoxarifado',
    address         JSON,
    manager_id      BIGINT UNSIGNED,
    capacity        DECIMAL(14,4) DEFAULT 0,
    capacity_uom_id BIGINT UNSIGNED,
    default_strategy ENUM('fefo','fifo','lifo') NOT NULL DEFAULT 'fefo',
    is_picking_active TINYINT(1) NOT NULL DEFAULT 1,
    allows_negative TINYINT(1) NOT NULL DEFAULT 0,
    status          ENUM('active','inactive') NOT NULL DEFAULT 'active',
    created_by      BIGINT UNSIGNED NOT NULL,
    updated_by      BIGINT UNSIGNED,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_unit (unit_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_locations (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code            VARCHAR(30) NOT NULL,
    name            VARCHAR(120) NOT NULL,
    warehouse_id    BIGINT UNSIGNED NOT NULL,
    parent_id       BIGINT UNSIGNED,
    location_type   ENUM('warehouse','zone','aisle','shelf','position') NOT NULL,
    capacity        DECIMAL(14,4) DEFAULT 0,
    capacity_uom_id BIGINT UNSIGNED,
    temperature_min DECIMAL(6,2),
    temperature_max DECIMAL(6,2),
    is_quarantine   TINYINT(1) NOT NULL DEFAULT 0,
    is_picking      TINYINT(1) NOT NULL DEFAULT 0,
    status          ENUM('active','inactive','blocked') NOT NULL DEFAULT 'active',
    notes           TEXT,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_code_wh (warehouse_id, code),
    INDEX idx_warehouse (warehouse_id),
    INDEX idx_parent (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_item_categories (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid        CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code        VARCHAR(20) NOT NULL UNIQUE,
    name        VARCHAR(100) NOT NULL,
    parent_id   BIGINT UNSIGNED,
    description TEXT,
    is_active   TINYINT(1) NOT NULL DEFAULT 1,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_uom (
    id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid              CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code              VARCHAR(20) NOT NULL UNIQUE,
    name              VARCHAR(80) NOT NULL,
    uom_type          ENUM('quantity','weight','volume','length','area') NOT NULL,
    is_base           TINYINT(1) NOT NULL DEFAULT 0,
    base_uom_id       BIGINT UNSIGNED,
    conversion_factor DECIMAL(20,8) NOT NULL DEFAULT 1.00000000,
    decimal_places    TINYINT NOT NULL DEFAULT 2,
    status            ENUM('active','inactive') NOT NULL DEFAULT 'active',
    created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_items (
    id                    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid                  CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code                  VARCHAR(30) NOT NULL UNIQUE,
    name                  VARCHAR(200) NOT NULL,
    description           TEXT,
    ean                   VARCHAR(30),
    category_id           BIGINT UNSIGNED,
    subcategory_id        BIGINT UNSIGNED,
    uom_id                BIGINT UNSIGNED NOT NULL,
    secondary_uom_id      BIGINT UNSIGNED,
    conversion_factor     DECIMAL(20,8) DEFAULT 1.00000000,
    item_type             ENUM('produto','insumo','embalagem','ferramenta','epi') NOT NULL DEFAULT 'produto',
    default_warehouse_id  BIGINT UNSIGNED,
    default_location_id   BIGINT UNSIGNED,
    min_qty               DECIMAL(14,4) NOT NULL DEFAULT 0,
    max_qty               DECIMAL(14,4) NOT NULL DEFAULT 0,
    reorder_point         DECIMAL(14,4) NOT NULL DEFAULT 0,
    reorder_qty           DECIMAL(14,4) NOT NULL DEFAULT 0,
    stock_strategy        ENUM('fefo','fifo','lifo','inherit') NOT NULL DEFAULT 'inherit',
    is_lot_controlled     TINYINT(1) NOT NULL DEFAULT 0,
    is_serial_controlled  TINYINT(1) NOT NULL DEFAULT 0,
    is_expiry_controlled  TINYINT(1) NOT NULL DEFAULT 0,
    expiry_alert_days     SMALLINT NOT NULL DEFAULT 30,
    costing_method        ENUM('average','peps','standard') NOT NULL DEFAULT 'average',
    standard_cost         DECIMAL(16,4) DEFAULT 0,
    average_cost          DECIMAL(16,4) DEFAULT 0,
    last_purchase_cost    DECIMAL(16,4) DEFAULT 0,
    currency              CHAR(3) NOT NULL DEFAULT 'BRL',
    image_path            VARCHAR(300),
    status                ENUM('active','inactive','blocked') NOT NULL DEFAULT 'active',
    created_by            BIGINT UNSIGNED NOT NULL,
    updated_by            BIGINT UNSIGNED,
    created_at            DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at            DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category_id),
    INDEX idx_status (status),
    INDEX idx_ean (ean)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_stock (
    id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid          CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    item_id       BIGINT UNSIGNED NOT NULL,
    warehouse_id  BIGINT UNSIGNED NOT NULL,
    location_id   BIGINT UNSIGNED,
    lot_id        BIGINT UNSIGNED,
    serial_id     BIGINT UNSIGNED,
    qty_available DECIMAL(14,4) NOT NULL DEFAULT 0,
    qty_reserved  DECIMAL(14,4) NOT NULL DEFAULT 0,
    qty_blocked   DECIMAL(14,4) NOT NULL DEFAULT 0,
    unit_cost     DECIMAL(16,4) NOT NULL DEFAULT 0,
    updated_at    DATETIME ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_stock (item_id, warehouse_id, location_id, lot_id, serial_id),
    INDEX idx_item (item_id),
    INDEX idx_warehouse (warehouse_id),
    CONSTRAINT chk_qty_available CHECK (qty_available >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_lots (
    id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid          CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    lot_number    VARCHAR(80) NOT NULL,
    item_id       BIGINT UNSIGNED NOT NULL,
    supplier_id   BIGINT UNSIGNED,
    entry_date    DATE NOT NULL,
    expiry_date   DATE,
    manufacture_date DATE,
    initial_qty   DECIMAL(14,4) NOT NULL DEFAULT 0,
    status        ENUM('available','quarantine','blocked','exhausted') NOT NULL DEFAULT 'available',
    notes         TEXT,
    created_by    BIGINT UNSIGNED NOT NULL,
    created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_lot_item (item_id, lot_number),
    INDEX idx_item (item_id),
    INDEX idx_expiry (expiry_date),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_serials (
    id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid          CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    serial_number VARCHAR(100) NOT NULL,
    item_id       BIGINT UNSIGNED NOT NULL,
    lot_id        BIGINT UNSIGNED,
    warehouse_id  BIGINT UNSIGNED,
    location_id   BIGINT UNSIGNED,
    status        ENUM('in_stock','allocated','dispatched','written_off','blocked') NOT NULL DEFAULT 'in_stock',
    entry_document_uuid CHAR(36),
    exit_document_uuid  CHAR(36),
    created_by    BIGINT UNSIGNED NOT NULL,
    created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_serial_item (item_id, serial_number),
    INDEX idx_item (item_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_documents (
    id               BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid             CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code             VARCHAR(30) NOT NULL UNIQUE,
    document_type    ENUM('entry','exit','transfer','adjustment','inventory_adjustment') NOT NULL,
    entry_type       ENUM('nf_entrada','devolucao_saida','ajuste_positivo','transferencia_recebida','inventario') NULL,
    exit_type        ENUM('requisicao','venda','expedicao','devolucao_fornecedor','ajuste_negativo') NULL,
    origin_warehouse_id      BIGINT UNSIGNED,
    destination_warehouse_id BIGINT UNSIGNED,
    origin_location_id       BIGINT UNSIGNED,
    destination_location_id  BIGINT UNSIGNED,
    supplier_id      BIGINT UNSIGNED,
    requester_id     BIGINT UNSIGNED,
    document_number  VARCHAR(80),
    document_date    DATE,
    operation_date   DATE NOT NULL,
    priority         ENUM('normal','urgent','critical') NOT NULL DEFAULT 'normal',
    status           ENUM('draft','pending','in_picking','in_transit','confirmed','cancelled') NOT NULL DEFAULT 'draft',
    total_items      INT NOT NULL DEFAULT 0,
    total_qty        DECIMAL(14,4) NOT NULL DEFAULT 0,
    total_value      DECIMAL(16,4) NOT NULL DEFAULT 0,
    notes            TEXT,
    confirmed_by     BIGINT UNSIGNED,
    confirmed_at     DATETIME,
    cancelled_by     BIGINT UNSIGNED,
    cancelled_at     DATETIME,
    cancel_reason    TEXT,
    created_by       BIGINT UNSIGNED NOT NULL,
    updated_by       BIGINT UNSIGNED,
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type (document_type),
    INDEX idx_status (status),
    INDEX idx_operation_date (operation_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_document_items (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    document_id     BIGINT UNSIGNED NOT NULL,
    item_id         BIGINT UNSIGNED NOT NULL,
    lot_id          BIGINT UNSIGNED,
    serial_id       BIGINT UNSIGNED,
    origin_location_id      BIGINT UNSIGNED,
    destination_location_id BIGINT UNSIGNED,
    qty             DECIMAL(14,4) NOT NULL,
    uom_id          BIGINT UNSIGNED NOT NULL,
    unit_cost       DECIMAL(16,4) NOT NULL DEFAULT 0,
    total_cost      DECIMAL(16,4) NOT NULL DEFAULT 0,
    status          ENUM('pending','picked','confirmed','cancelled') NOT NULL DEFAULT 'pending',
    notes           TEXT,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_document (document_id),
    INDEX idx_item (item_id),
    FOREIGN KEY (document_id) REFERENCES stg_documents(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_movements (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    document_item_id BIGINT UNSIGNED,
    document_id     BIGINT UNSIGNED NOT NULL,
    item_id         BIGINT UNSIGNED NOT NULL,
    warehouse_id    BIGINT UNSIGNED NOT NULL,
    location_id     BIGINT UNSIGNED,
    lot_id          BIGINT UNSIGNED,
    serial_id       BIGINT UNSIGNED,
    movement_type   ENUM('IN','OUT','TRANSFER_OUT','TRANSFER_IN','ADJUSTMENT','INVENTORY_ADJUSTMENT','RESERVATION','RESERVATION_CANCEL') NOT NULL,
    qty             DECIMAL(14,4) NOT NULL,
    unit_cost       DECIMAL(16,4) NOT NULL DEFAULT 0,
    total_cost      DECIMAL(16,4) NOT NULL DEFAULT 0,
    qty_before      DECIMAL(14,4) NOT NULL DEFAULT 0,
    qty_after       DECIMAL(14,4) NOT NULL DEFAULT 0,
    moved_by        BIGINT UNSIGNED NOT NULL,
    moved_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes           TEXT,
    INDEX idx_item (item_id),
    INDEX idx_warehouse (warehouse_id),
    INDEX idx_document (document_id),
    INDEX idx_moved_at (moved_at),
    INDEX idx_lot (lot_id),
    INDEX idx_serial (serial_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_inventories (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    code            VARCHAR(30) NOT NULL UNIQUE,
    inventory_type  ENUM('general','partial_zone','partial_category','cyclic') NOT NULL,
    warehouse_id    BIGINT UNSIGNED NOT NULL,
    zone_id         BIGINT UNSIGNED,
    category_id     BIGINT UNSIGNED,
    count_method    ENUM('single','double','blind') NOT NULL DEFAULT 'single',
    freeze_movements TINYINT(1) NOT NULL DEFAULT 0,
    start_date      DATE NOT NULL,
    end_date        DATE,
    status          ENUM('planned','in_progress','awaiting_approval','completed','cancelled') NOT NULL DEFAULT 'planned',
    responsible_id  BIGINT UNSIGNED NOT NULL,
    total_items     INT NOT NULL DEFAULT 0,
    counted_items   INT NOT NULL DEFAULT 0,
    divergent_items INT NOT NULL DEFAULT 0,
    total_diff_value DECIMAL(16,4) NOT NULL DEFAULT 0,
    approved_by     BIGINT UNSIGNED,
    approved_at     DATETIME,
    notes           TEXT,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_inventory_items (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    inventory_id    BIGINT UNSIGNED NOT NULL,
    item_id         BIGINT UNSIGNED NOT NULL,
    location_id     BIGINT UNSIGNED,
    lot_id          BIGINT UNSIGNED,
    qty_system      DECIMAL(14,4) NOT NULL DEFAULT 0,
    qty_count_1     DECIMAL(14,4),
    qty_count_2     DECIMAL(14,4),
    qty_adjusted    DECIMAL(14,4),
    difference      DECIMAL(14,4) GENERATED ALWAYS AS (COALESCE(qty_adjusted, qty_count_1, 0) - qty_system) STORED,
    unit_cost       DECIMAL(16,4) NOT NULL DEFAULT 0,
    diff_value      DECIMAL(16,4) GENERATED ALWAYS AS (difference * unit_cost) STORED,
    status          ENUM('pending','counted','divergent','approved','ignored') NOT NULL DEFAULT 'pending',
    counted_by      BIGINT UNSIGNED,
    counted_at      DATETIME,
    approved_by     BIGINT UNSIGNED,
    notes           TEXT,
    INDEX idx_inventory (inventory_id),
    INDEX idx_item (item_id),
    FOREIGN KEY (inventory_id) REFERENCES stg_inventories(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_kanban_tasks (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    task_type       ENUM('entry','exit','transfer','inventory','adjustment','location_maintenance') NOT NULL,
    linked_document_uuid CHAR(36),
    warehouse_id    BIGINT UNSIGNED NOT NULL,
    kanban_status   ENUM('waiting','in_picking','in_checking','in_transit','with_issue','done') NOT NULL DEFAULT 'waiting',
    priority        ENUM('normal','urgent','critical') NOT NULL DEFAULT 'normal',
    title           VARCHAR(200) NOT NULL,
    description     TEXT,
    responsible_id  BIGINT UNSIGNED,
    due_date        DATE,
    due_time        TIME,
    checklist       JSON,
    completed_by    BIGINT UNSIGNED,
    completed_at    DATETIME,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (kanban_status),
    INDEX idx_warehouse (warehouse_id),
    INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_audit_log (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    user_id         BIGINT UNSIGNED NOT NULL,
    user_profile    VARCHAR(10) NOT NULL,
    ip_address      VARCHAR(45) NOT NULL,
    action          ENUM('CREATE','UPDATE','DELETE','CONFIRM','CANCEL','LOGIN','EXPORT') NOT NULL,
    entity          VARCHAR(60) NOT NULL,
    entity_uuid     CHAR(36) NOT NULL,
    summary         VARCHAR(300) NOT NULL,
    payload_before  JSON,
    payload_after   JSON,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_entity (entity, entity_uuid),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_stock_snapshots (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    snapshot_date   DATE NOT NULL,
    warehouse_id    BIGINT UNSIGNED NOT NULL,
    item_id         BIGINT UNSIGNED NOT NULL,
    qty_available   DECIMAL(14,4) NOT NULL DEFAULT 0,
    qty_reserved    DECIMAL(14,4) NOT NULL DEFAULT 0,
    unit_cost       DECIMAL(16,4) NOT NULL DEFAULT 0,
    total_value     DECIMAL(16,4) NOT NULL DEFAULT 0,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_snapshot (snapshot_date, warehouse_id, item_id),
    INDEX idx_date (snapshot_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stg_automations (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid            CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    automation_name VARCHAR(150) NOT NULL,
    trigger_type    ENUM('movement_event','cron','webhook') NOT NULL,
    cron_expression VARCHAR(100),
    conditions      JSON,
    actions         JSON NOT NULL,
    recipients      JSON,
    is_active       TINYINT(1) NOT NULL DEFAULT 1,
    last_run_at     DATETIME,
    next_run_at     DATETIME,
    run_count       INT NOT NULL DEFAULT 0,
    last_error      TEXT,
    created_by      BIGINT UNSIGNED NOT NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

#### 13. ENDPOINTS DA API

##### 13.1 Depósitos

| Método | Rota                              | Descrição                     | Permissão     |
|--------|-----------------------------------|-------------------------------|---------------|
| GET    | /api/storage/warehouses           | Listar depósitos              | ALM+          |
| GET    | /api/storage/warehouses/{uuid}    | Detalhe do depósito           | ALM+          |
| POST   | /api/storage/warehouses           | Criar depósito                | GU+           |
| PUT    | /api/storage/warehouses/{uuid}    | Editar depósito               | GU+           |
| PATCH  | /api/storage/warehouses/{uuid}/status | Ativar/Inativar           | GE+           |
| DELETE | /api/storage/warehouses/{uuid}    | Excluir depósito vazio        | GE+           |

##### 13.2 Localizações

| Método | Rota                                       | Descrição                    | Permissão |
|--------|--------------------------------------------|------------------------------|-----------|
| GET    | /api/storage/locations                     | Listar localizações          | ALM+      |
| GET    | /api/storage/locations/{uuid}              | Detalhe                      | ALM+      |
| GET    | /api/storage/locations/{uuid}/contents     | Itens na localização         | ALM+      |
| POST   | /api/storage/locations                     | Criar localização            | GU+       |
| PUT    | /api/storage/locations/{uuid}              | Editar                       | GU+       |
| PATCH  | /api/storage/locations/{uuid}/status       | Ativar/Bloquear              | GU+       |

##### 13.3 Itens / SKUs

| Método | Rota                                    | Descrição                     | Permissão |
|--------|-----------------------------------------|-------------------------------|-----------|
| GET    | /api/storage/items                      | Listar itens (paginado)       | ALM+      |
| GET    | /api/storage/items/{uuid}               | Detalhe do item               | ALM+      |
| GET    | /api/storage/items/{uuid}/stock         | Saldo por depósito/posição    | ALM+      |
| GET    | /api/storage/items/{uuid}/movements     | Histórico de movimentações    | ALM+      |
| POST   | /api/storage/items                      | Criar item                    | GU+       |
| PUT    | /api/storage/items/{uuid}               | Editar item                   | GU+       |
| PATCH  | /api/storage/items/{uuid}/status        | Ativar/Bloquear               | GU+       |
| DELETE | /api/storage/items/{uuid}               | Excluir (se sem movimentação) | GE+       |

##### 13.4 Documentos de Movimentação

| Método | Rota                                         | Descrição                    | Permissão |
|--------|----------------------------------------------|------------------------------|-----------|
| GET    | /api/storage/documents                       | Listar documentos            | ALM+      |
| GET    | /api/storage/documents/{uuid}                | Detalhe + itens              | ALM+      |
| POST   | /api/storage/documents                       | Criar documento              | ALM+      |
| PUT    | /api/storage/documents/{uuid}                | Editar rascunho              | ALM+      |
| POST   | /api/storage/documents/{uuid}/confirm        | Confirmar documento          | ALM+      |
| POST   | /api/storage/documents/{uuid}/cancel         | Cancelar documento           | GU+       |
| POST   | /api/storage/documents/{uuid}/start-picking  | Iniciar separação            | ALM+      |
| POST   | /api/storage/documents/import-xml            | Importar NF-e XML            | ALM+      |

##### 13.5 Estoque

| Método | Rota                                             | Descrição                        | Permissão |
|--------|--------------------------------------------------|----------------------------------|-----------|
| GET    | /api/storage/stock                               | Posição de estoque atual         | ALM+      |
| GET    | /api/storage/stock/alerts                        | Alertas críticos                 | ALM+      |
| GET    | /api/storage/stock/valuation                     | Valoração de estoque             | FIN+      |
| GET    | /api/storage/stock/lots                          | Listar lotes                     | ALM+      |
| GET    | /api/storage/stock/lots/{uuid}                   | Detalhe + rastreabilidade do lote| ALM+      |
| PATCH  | /api/storage/stock/lots/{uuid}/status            | Bloquear/Quarentena/Liberar lote | GU+       |
| GET    | /api/storage/stock/serials                       | Listar séries                    | ALM+      |
| GET    | /api/storage/stock/expiry                        | Itens por vencimento             | ALM+      |

##### 13.6 Inventário

| Método | Rota                                              | Descrição                   | Permissão |
|--------|---------------------------------------------------|-----------------------------|-----------|
| GET    | /api/storage/inventories                          | Listar inventários          | GU+       |
| GET    | /api/storage/inventories/{uuid}                   | Detalhe                     | GU+       |
| POST   | /api/storage/inventories                          | Criar inventário            | GU+       |
| POST   | /api/storage/inventories/{uuid}/start             | Iniciar contagem            | ALM+      |
| POST   | /api/storage/inventories/{uuid}/count             | Salvar contagem parcial     | ALM+      |
| POST   | /api/storage/inventories/{uuid}/finish-count      | Finalizar contagem          | ALM+      |
| POST   | /api/storage/inventories/{uuid}/approve           | Aprovar ajustes             | GU+       |
| GET    | /api/storage/inventories/{uuid}/divergences       | Relatório de divergências   | GU+       |

##### 13.7 Kanban

| Método | Rota                                         | Descrição                   | Permissão |
|--------|----------------------------------------------|-----------------------------|-----------|
| GET    | /api/storage/kanban/tasks                    | Listar tarefas              | ALM+      |
| POST   | /api/storage/kanban/tasks                    | Criar tarefa                | ALM+      |
| PUT    | /api/storage/kanban/tasks/{uuid}             | Editar tarefa               | ALM+      |
| PATCH  | /api/storage/kanban/tasks/{uuid}/move        | Mover de coluna             | ALM+      |
| PATCH  | /api/storage/kanban/tasks/{uuid}/complete    | Concluir tarefa             | ALM+      |
| DELETE | /api/storage/kanban/tasks/{uuid}             | Excluir tarefa              | GU+       |

##### 13.8 Automações e Auditoria

| Método | Rota                                        | Descrição                   | Permissão |
|--------|---------------------------------------------|-----------------------------|-----------|
| GET    | /api/storage/automations                    | Listar automações           | GU+       |
| POST   | /api/storage/automations                    | Criar automação             | GE+       |
| PUT    | /api/storage/automations/{uuid}             | Editar automação            | GE+       |
| PATCH  | /api/storage/automations/{uuid}/toggle      | Ativar/Inativar             | GE+       |
| GET    | /api/storage/audit-log                      | Trilha de auditoria         | AUD+      |
| GET    | /api/storage/snapshots                      | Snapshots históricos        | FIN+      |

---

#### 14. PERMISSÕES RBAC

| Permissão                          | SA | GE | GU | ALM | AUD | FIN | VIS |
|------------------------------------|----|----|----|----|-----|-----|-----|
| Ver depósitos / localizações       | ✅ | ✅ | ✅ | ✅ | ✅  | ✅  | ✅  |
| Criar / editar depósitos           | ✅ | ✅ | ✅ | ❌ | ❌  | ❌  | ❌  |
| Excluir depósitos                  | ✅ | ✅ | ❌ | ❌ | ❌  | ❌  | ❌  |
| Ver itens / SKUs                   | ✅ | ✅ | ✅ | ✅ | ✅  | ✅  | ✅  |
| Criar / editar itens               | ✅ | ✅ | ✅ | ❌ | ❌  | ❌  | ❌  |
| Bloquear item                      | ✅ | ✅ | ✅ | ❌ | ❌  | ❌  | ❌  |
| Criar movimentação (rascunho)      | ✅ | ✅ | ✅ | ✅ | ❌  | ❌  | ❌  |
| Confirmar movimentação             | ✅ | ✅ | ✅ | ✅ | ❌  | ❌  | ❌  |
| Cancelar movimentação              | ✅ | ✅ | ✅ | ❌ | ❌  | ❌  | ❌  |
| Ver saldo de estoque               | ✅ | ✅ | ✅ | ✅ | ✅  | ✅  | ✅* |
| Ver custos / valoração             | ✅ | ✅ | ✅ | ❌ | ✅  | ✅  | ❌  |
| Criar / gerir inventário           | ✅ | ✅ | ✅ | ❌ | ❌  | ❌  | ❌  |
| Executar contagem de inventário    | ✅ | ✅ | ✅ | ✅ | ❌  | ❌  | ❌  |
| Aprovar ajustes de inventário      | ✅ | ✅ | ✅ | ❌ | ❌  | ❌  | ❌  |
| Bloquear / quarentena de lote      | ✅ | ✅ | ✅ | ❌ | ❌  | ❌  | ❌  |
| Ver trilha de auditoria            | ✅ | ✅ | ✅ | ❌ | ✅  | ❌  | ❌  |
| Ver payloads de auditoria (JSON)   | ✅ | ❌ | ❌ | ❌ | ✅  | ❌  | ❌  |
| Configurar automações              | ✅ | ✅ | ❌ | ❌ | ❌  | ❌  | ❌  |
| Exportar relatórios                | ✅ | ✅ | ✅ | ✅ | ✅  | ✅  | ❌  |
| Kanban — criar / mover tarefas     | ✅ | ✅ | ✅ | ✅ | ❌  | ❌  | ❌  |
| Ativar `allows_negative`           | ✅ | ❌ | ❌ | ❌ | ❌  | ❌  | ❌  |

> *VIS vê saldo sem ver custos unitários.

---

#### 15. REQUISITOS NÃO FUNCIONAIS

##### 15.1 Performance
- Listagens com paginação: máx 200ms p95 para até 10.000 registros.
- Atualização de saldo após confirmação de documento: máx 500ms.
- Dashboard com widgets e charts: cache de 5 minutos, invalidado em nova movimentação.
- Snapshots diários executados entre 00:00–01:00 (horário da unidade).

##### 15.2 Segurança
- Toda requisição autenticada via JWT (Bearer Token) com expiração de 30 min.
- Refresh Token com rotação a cada uso (HTTPOnly cookie).
- Rate limit: 120 req/min por usuário, 600 req/min por IP.
- Payload de auditoria criptografado em repouso (AES-256) para campos sensíveis.
- Upload de imagens: validação MIME real (não extensão), armazenado fora do webroot.
- SQL: apenas prepared statements / ORM com escape, sem concatenação direta.
- Headers de segurança obrigatórios: CSP · X-Frame-Options · HSTS · Referrer-Policy.

##### 15.3 LGPD / Compliance
- Dados de fornecedores (CNPJ/CPF): mascarados na exibição para VIS e ALM.
- Exportações com dados pessoais registradas em log de auditoria.
- Retenção de logs: 5 anos (configurável por entidade).
- Snapshots de estoque: 1 ano em linha, 5 anos em arquivo frio.

##### 15.4 Acessibilidade e UX
- ARIA labels em todos os botões icon-only.
- Navegação completa por teclado (Tab, Enter, Esc para drawers).
- Feedback de ação: toast de sucesso/erro após toda operação assíncrona.
- Skeleton loaders em datatables e widgets durante carregamento.
- Drawers: abertura com animação slide (300ms), foco automático no primeiro campo.
- Dark mode: variáveis CSS Tailwind configuradas globalmente em `ttsc.css`.

---

#### 16. CHECKLIST DE ENTREGA

##### Fase 1 — Estrutura Base
- [ ] Schema SQL completo aplicado (todas as tabelas stg_*)
- [ ] CRUD de Depósitos (API + PHP)
- [ ] CRUD de Localizações (API + PHP + visualização árvore)
- [ ] CRUD de Categorias e UOM
- [ ] CRUD de Itens / SKUs com abas

##### Fase 2 — Operações Core
- [ ] Entradas: drawer completo + importação XML NF-e
- [ ] Saídas: drawer completo + sugestão FEFO/FIFO/LIFO
- [ ] Transferências: drawer completo (interna + entre unidades)
- [ ] Atualização de saldo (`stg_stock`) após confirmação

##### Fase 3 — Controles e Rastreabilidade
- [ ] Controle de lotes (crud + histórico)
- [ ] Controle de série (crud + histórico)
- [ ] Controle de validade (datatable + alertas)
- [ ] Trilha de auditoria (datatable + payloads)

##### Fase 4 — Inventário
- [ ] Criação e gestão de inventários
- [ ] Tela de contagem (simples + cega + dupla)
- [ ] Aprovação de divergências + geração de ajustes
- [ ] Snapshots diários (cron)

##### Fase 5 — Dashboard, Kanban e Automações
- [ ] Dashboard com 6 widgets KPI
- [ ] 5 charts amCharts 5
- [ ] Datatable de alertas críticos
- [ ] Kanban de operações (drag-and-drop)
- [ ] Configuração de 10 automações

##### Fase 6 — Gerenciamentos e Config
- [ ] Gestão de fornecedores
- [ ] Regras de estoque por depósito/unidade
- [ ] Matriz RBAC completa por perfil
- [ ] Testes de segurança (JWT, rate limit, SQL injection, XSS)
- [ ] Relatórios exportáveis (CSV · XLSX · PDF)
