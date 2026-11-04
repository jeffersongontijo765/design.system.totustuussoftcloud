# Logger Module — Spec Completo v3.0
> **Projeto:** TotusTuusSoftCloud Premium V2  
> **Stack:** PHP 8 puro · Tailwind CSS 4.2 · Supabase · amCharts 5 · FontAwesome 7.2  
> **Padrão de IDs:** `id` (ordenação/JOINs) · `uuid` (interno entre bancos) · `code` (externo/APIs/URLs)  

- Language Standard: Global English
> **Última atualização:** 2026-06-08

---

## Índice de Páginas

| # | Página | Rota | Arquivo PHP |
|---|--------|------|-------------|
| 1 | Dashboard | /admin/logger | logger/dashboard.php |
| 2 | Sessões de Usuários | /admin/logger/sessions | logger/sessions.php |
| 3 | Audit Trail | /admin/logger/audit-trail | logger/audit-trail.php |
| 4 | Security Logs | /admin/logger/security | logger/security.php |
| 5 | Login Attempts | /admin/logger/login-attempts | logger/login-attempts.php |
| 6 | System Events | /admin/logger/system-events | logger/system-events.php |
| 7 | Database Audits | /admin/logger/db-audits | logger/db-audits.php |
| 8 | Metrics | /admin/logger/metrics | logger/metrics.php |
| 9 | Alerts | /admin/logger/alerts | logger/alerts.php |
| 10 | **Kanban de Alertas** | /admin/logger/kanban | logger/kanban.php |
| 11 | **Automações** | /admin/logger/automations | logger/automations.php |
| 12 | **Controles** | /admin/logger/controls | logger/controls.php |
| 13 | **Gerenciamentos** | /admin/logger/management | logger/management.php |

---

## Regras Globais de Padronização

### Estrutura de Blocos por View (ordem obrigatória)
```
1. Header        → breadcrumb + título + botões de ação
2. Widgets       → 4 a 8 cards KPI com progress bar
3. DataTable     → toolbar + tabela + paginação + footer
4. Charts        → grid de gráficos amCharts 5
5. Drawers       → filtros, criação, edição, visualização
6. JS include    → <script src="/assets/js/logger/ttsc.admin.logger.{page}.js">
```

### Padrão de Widget Card
```html
<div id="widget-{id}" class="ttsc-card ttsc-card-widget">
  <div class="ttsc-card-body d-flex align-items-center gap-3">
    <span class="ttsc-icon-wrap ttsc-bg-{color}-soft">
      <i class="fa-solid fa-{icon} ttsc-text-{color}"></i>
    </span>
    <div class="flex-grow-1">
      <div class="ttsc-widget-value" id="widget-{id}-value">—</div>
      <div class="ttsc-widget-label">{Label}</div>
      <div class="progress mt-1" style="height:4px">
        <div class="progress-bar bg-{color}" id="widget-{id}-bar" style="width:0%"></div>
      </div>
      <small class="ttsc-text-muted" id="widget-{id}-hint">{hint}</small>
    </div>
  </div>
</div>
```

### Padrão de Toolbar DataTable
```html
<div class="ttsc-datatable-toolbar d-flex flex-wrap align-items-center gap-2">
  <!-- Busca -->
  <input type="search" id="search-{page}" class="form-control form-control-sm w-200px"
         placeholder="Buscar...">
  <!-- Filtros rápidos (chips/select) -->
  <select id="filter-{field}" class="form-select form-select-sm w-auto">...</select>
  <!-- Batch Actions (aparece ao selecionar linhas) -->
  <div id="batch-actions-{page}" class="d-none d-flex gap-2">
    <button class="btn btn-sm btn-light-danger" id="batch-delete-{page}">
      <i class="fa-solid fa-trash"></i> Excluir selecionados
    </button>
    <button class="btn btn-sm btn-light-primary" id="batch-export-{page}">
      <i class="fa-solid fa-file-export"></i> Exportar selecionados
    </button>
  </div>
  <!-- Exportar -->
  <div class="dropdown ms-auto">
    <button class="btn btn-sm btn-light dropdown-toggle">
      <i class="fa-solid fa-download"></i> Exportar
    </button>
    <ul class="dropdown-menu dropdown-menu-end">
      <li><a class="dropdown-item" data-export="csv">CSV</a></li>
      <li><a class="dropdown-item" data-export="xlsx">XLSX</a></li>
      <li><a class="dropdown-item" data-export="pdf">PDF</a></li>
      <li><a class="dropdown-item" data-export="json">JSON</a></li>
      <li><a class="dropdown-item" data-export="xml">XML</a></li>
      <li><a class="dropdown-item" data-export="sql">SQL</a></li>
      <li><a class="dropdown-item" data-export="txt">TXT</a></li>
    </ul>
  </div>
  <!-- Filtro Avançado -->
  <button class="btn btn-sm btn-light" data-drawer-toggle="drawer-filter-{page}">
    <i class="fa-solid fa-sliders"></i> Filtros
  </button>
</div>
```

### Padrão amCharts 5 — Destroy/Recreate
```javascript
// Sempre destruir antes de recriar
if (window._charts && window._charts['{chartId}']) {
  window._charts['{chartId}'].dispose();
}
const root = am5.Root.new('{chartId}');
root.setThemes([am5themes_Animated.new(root)]);
window._charts = window._charts || {};
window._charts['{chartId}'] = root;
```

### Padrão de Drawer (filtro/CRUD)
- **Pasta:** `/resources/app/partials/drawers/drawer/admin/logger/`
- **Include em:** `/resources/app/partials/drawer.php`
- **Largura:** `w-400px` (filtros) · `w-600px` (criação/edição) · `w-800px` (visualização/kanban)
- **Footer obrigatório:** botões Cancelar + Aplicar/Salvar com IDs `btn-{drawer}-cancel` e `btn-{drawer}-submit`

---

## 1. Dashboard Logger

### Header
- **Ícone:** `fa-solid fa-gauge-high` · cor `ttsc-text-primary`
- **Título:** Painel de Logger
- **Subtítulo:** Visão geral de todos os módulos de log e auditoria
- **Botões:** `Atualizar` (fa-rotate-right) · `Configurações` → drawer-config-dashboard

### Widgets (linha 1 — visão geral)
| ID | Ícone | Título | Cor | Progress Label |
|----|-------|--------|-----|----------------|
| widget-sessions-active | fa-users | Sessões Ativas | primary | % do pico diário |
| widget-alerts-critical | fa-triangle-exclamation | Alertas Críticos | danger | % sem resolução |
| widget-login-failed-24h | fa-lock | Falhas de Login 24h | warning | % do limite |
| widget-events-today | fa-bolt | Eventos Hoje | info | vs. média diária |

### Widgets (linha 2 — status dos módulos)
| ID | Ícone | Título | Cor | Progress Label |
|----|-------|--------|-----|----------------|
| widget-audit-records | fa-file-shield | Registros Audit Trail | success | % capacidade DB |
| widget-security-events | fa-shield-halved | Eventos de Segurança | danger | últimas 24h |
| widget-db-queries | fa-database | Queries Auditadas | secondary | % slow queries |
| widget-metrics-score | fa-chart-line | Score de Saúde | success | índice geral |

### DataTable — Últimos Eventos (Feed Global)
| Coluna | Tipo | Alinhamento | Notas |
|--------|------|-------------|-------|
| # | checkbox | center | seleção batch |
| Módulo | badge | left | Sessions/Audit/Security/etc. |
| Tipo | badge-soft | left | info/warning/error/critical |
| Descrição | texto truncado | left | max 80 chars, tooltip full |
| Entidade | texto | left | entity_code |
| Usuário | avatar+texto | left | user_code + nome |
| IP | mono | center | — |
| Data/Hora | datetime | center | formato DD/MM/YYYY HH:mm:ss |
| Ações | botões | center | Ver, Ir ao módulo |

**SORT_FIELDS:** `module, type, user_code, ip_address, created_at`
**Filter Keys:** `module, type, date_range, user_uuid, entity_uuid`

### Charts
| ID | Tipo amCharts 5 | Título | Grid |
|----|-----------------|--------|------|
| chart-events-timeline | XYChart (LineSeries) | Linha do Tempo de Eventos | col-12 |
| chart-modules-donut | PieChart (donut) | Eventos por Módulo | col-md-6 |
| chart-severity-bar | XYChart (ColumnSeries) | Eventos por Severidade | col-md-6 |

### Drawers
- `drawer-config-dashboard.php` — ID: `drawer-config-dashboard` · w-400px
  - Período padrão de exibição (select: 24h/7d/30d)
  - Módulos visíveis (checkboxes)
  - Auto-refresh (toggle + intervalo em segundos)
  - Limite de registros no feed (number input)

---

## 2. Sessões de Usuários

### Header
- **Ícone:** `fa-solid fa-users` · cor `ttsc-text-primary`
- **Título:** Sessões de Usuários
- **Subtítulo:** Monitoramento de sessões ativas e históricas
- **Botões:** `Encerrar Todas` (fa-right-from-bracket, btn-danger) · `Filtros` → drawer-filter-sessions

### Widgets
| ID | Ícone | Título | Cor | Progress Label |
|----|-------|--------|-----|----------------|
| widget-sessions-now | fa-circle-dot | Sessões Ativas Agora | success | % do pico |
| widget-sessions-today | fa-calendar-day | Sessões Hoje | primary | vs. ontem |
| widget-sessions-avg | fa-clock | Duração Média | info | min por sessão |
| widget-sessions-devices | fa-mobile-screen | Dispositivos Únicos | secondary | mobile vs. desktop |

### DataTable
| Coluna | Tipo | Alinhamento | Notas |
|--------|------|-------------|-------|
| # | checkbox | center | — |
| code | mono | center | session code (externo) |
| Usuário | avatar+texto | left | user_code + nome completo |
| IP | mono | center | com flag de país |
| Dispositivo | ícone+texto | left | fa-mobile/fa-desktop/fa-tablet |
| Navegador | ícone+texto | left | — |
| Sistema Op. | texto | left | — |
| Início | datetime | center | — |
| Último Acesso | datetime | center | badge "Agora" se < 2min |
| Duração | timer | center | HH:mm:ss |
| Status | badge | center | Ativa/Encerrada/Expirada |
| Ações | botões | center | Ver Detalhes, Encerrar |

**SORT_FIELDS:** `code, user_code, ip_address, started_at, last_seen_at, duration, status`
**Filter Keys:** `status, device_type, date_range, user_uuid, ip_address`
**Batch Actions:** Encerrar Selecionadas · Exportar

### Charts
| ID | Tipo | Título | Grid |
|----|------|--------|------|
| chart-sessions-active-line | XYChart (SmoothedXLineSeries) | Sessões Ativas por Hora | col-12 |
| chart-sessions-devices | PieChart (donut) | Sessões por Dispositivo | col-md-4 |
| chart-sessions-browsers | PieChart (donut) | Sessões por Navegador | col-md-4 |
| chart-sessions-os | PieChart (donut) | Sessões por Sistema Op. | col-md-4 |

### Drawers
- `drawer-filter-sessions.php` — ID: `drawer-filter-sessions` · w-400px
  - Status (checkboxes: Ativa/Encerrada/Expirada)
  - Tipo de dispositivo (select)
  - Período (date range picker)
  - Usuário (input autocomplete → user_code)
  - IP (text input)
  - Footer: Limpar | Aplicar

- `drawer-view-session.php` — ID: `drawer-view-session` · w-800px
  - Informações completas da sessão
  - Timeline de ações na sessão
  - Mapa de geolocalização do IP
  - Botão Encerrar Sessão

---

## 3. Audit Trail

### Header
- **Ícone:** `fa-solid fa-file-shield` · cor `ttsc-text-success`
- **Título:** Audit Trail
- **Subtítulo:** Registro imutável de todas as ações no sistema
- **Botões:** `Exportar Relatório` (fa-file-export) · `Filtros` → drawer-filter-audit

### Widgets
| ID | Ícone | Título | Cor | Progress Label |
|----|-------|--------|-----|----------------|
| widget-audit-total | fa-file-lines | Total de Registros | primary | crescimento mensal |
| widget-audit-today | fa-calendar-day | Ações Hoje | info | vs. média |
| widget-audit-creates | fa-plus-circle | Criações | success | % do total |
| widget-audit-deletes | fa-trash | Exclusões | danger | % do total |

### DataTable
| Coluna | Tipo | Alinhamento | Notas |
|--------|------|-------------|-------|
| # | checkbox | center | — |
| code | mono | center | audit code externo |
| Usuário | avatar+texto | left | user_code + nome |
| Ação | badge | center | CREATE/UPDATE/DELETE/VIEW/EXPORT |
| Módulo | texto | left | — |
| Entidade | mono | left | entity_code |
| IP | mono | center | — |
| Antes | btn icon | center | fa-eye → abre modal diff |
| Depois | btn icon | center | fa-eye → abre modal diff |
| Data/Hora | datetime | center | — |
| Ações | botões | center | Ver Diff, Ver Detalhes |

**SORT_FIELDS:** `code, user_code, action, module, entity_code, created_at`
**Filter Keys:** `action, module, date_range, user_uuid, entity_uuid, entity_code`
**Batch Actions:** Exportar · Arquivar

### Charts
| ID | Tipo | Título | Grid |
|----|------|--------|------|
| chart-audit-actions-bar | XYChart (ColumnSeries grouped) | Ações por Tipo (CREATE/UPDATE/DELETE) | col-md-8 |
| chart-audit-modules-donut | PieChart (donut) | Auditoria por Módulo | col-md-4 |
| chart-audit-timeline | XYChart (LineSeries) | Volume de Ações por Dia | col-12 |

### Drawers
- `drawer-filter-audit.php` — w-400px
  - Ação (checkboxes multi)
  - Módulo (select)
  - Entidade (text input → entity_code)
  - Usuário (autocomplete)
  - Período (date range)
  - Footer: Limpar | Aplicar

- `drawer-view-audit.php` — w-800px
  - Header: ícone + código + badge de ação
  - Info do usuário + IP + timestamp
  - Diff visual: tabela Before/After com highlight de mudanças
  - JSON raw colapsável

---

## 4. Security Logs

### Header
- **Ícone:** `fa-solid fa-shield-halved` · cor `ttsc-text-danger`
- **Título:** Security Logs
- **Subtítulo:** Eventos de segurança, ameaças e anomalias detectadas
- **Botões:** `Criar Regra` → drawer-create-security-rule · `Filtros` → drawer-filter-security

### Widgets
| ID | Ícone | Título | Cor | Progress Label |
|----|-------|--------|-----|----------------|
| widget-sec-critical | fa-skull-crossbones | Eventos Críticos | danger | últimas 24h |
| widget-sec-high | fa-triangle-exclamation | Eventos Alto | warning | últimas 24h |
| widget-sec-blocked | fa-ban | IPs Bloqueados | dark | total ativo |
| widget-sec-resolved | fa-circle-check | Resolvidos Hoje | success | % do total |

### DataTable
| Coluna | Tipo | Alinhamento | Notas |
|--------|------|-------------|-------|
| # | checkbox | center | — |
| code | mono | center | — |
| Tipo de Evento | badge | left | Brute Force/SQLi/XSS/CSRF/etc. |
| Severidade | badge-soft | center | Critical/High/Medium/Low |
| IP Origem | mono | center | — |
| Usuário | texto | left | user_code ou "Anônimo" |
| Módulo Alvo | texto | left | — |
| Descrição | texto truncado | left | tooltip full |
| Status | badge | center | Aberto/Em Análise/Resolvido/Ignorado |
| Data/Hora | datetime | center | — |
| Ações | botões | center | Ver, Resolver, Ignorar, Bloquear IP |

**SORT_FIELDS:** `code, event_type, severity, ip_origin, user_code, status, created_at`
**Filter Keys:** `severity, event_type, status, date_range, ip_origin, user_uuid`
**Batch Actions:** Resolver Selecionados · Ignorar · Bloquear IPs · Exportar

### Charts
| ID | Tipo | Título | Grid |
|----|------|--------|------|
| chart-sec-severity-donut | PieChart (donut) | Eventos por Severidade | col-md-4 |
| chart-sec-types-bar | XYChart (ColumnSeries) | Top 10 Tipos de Ataques | col-md-8 |
| chart-sec-timeline | XYChart (LineSeries stacked) | Eventos de Segurança por Dia | col-12 |

### Drawers
- `drawer-filter-security.php` — w-400px
- `drawer-view-security.php` — w-800px (detalhes + timeline de análise)
- `drawer-create-security-rule.php` — w-600px
  - Nome da regra, Tipo de evento, Severidade
  - Condição (IP range, user_uuid, módulo alvo)
  - Ação automática (bloquear IP / criar alerta / notificar admin)
  - Status (ativo/inativo)
  - Footer: Cancelar | Salvar Regra

---

## 5. Login Attempts

### Header
- **Ícone:** `fa-solid fa-right-to-bracket` · cor `ttsc-text-warning`
- **Título:** Tentativas de Login
- **Subtítulo:** Monitoramento de acessos autenticados e falhos
- **Botões:** `Bloquear IP` → drawer-create-block · `Filtros` → drawer-filter-login

### Widgets
| ID | Ícone | Título | Cor | Progress Label |
|----|-------|--------|-----|----------------|
| widget-login-success | fa-circle-check | Logins com Sucesso | success | hoje |
| widget-login-failed | fa-circle-xmark | Logins com Falha | danger | hoje |
| widget-login-blocked | fa-ban | IPs em Bloqueio | dark | total ativo |
| widget-login-rate | fa-percent | Taxa de Sucesso | info | % geral hoje |

### DataTable
| Coluna | Tipo | Alinhamento | Notas |
|--------|------|-------------|-------|
| # | checkbox | center | — |
| code | mono | center | — |
| Usuário/Email | texto | left | tentativa de login |
| IP | mono | center | com flag |
| País | texto | left | via geo-IP |
| Tipo | badge | center | Sucesso/Falha/Bloqueado |
| Motivo da Falha | texto | left | Senha inválida/Conta bloqueada/2FA/etc. |
| User Agent | texto truncado | left | — |
| Tentativas Consec. | número badge | center | badge danger se > 3 |
| Data/Hora | datetime | center | — |
| Ações | botões | center | Ver, Bloquear IP, Liberar |

**SORT_FIELDS:** `code, user_identifier, ip_address, type, consecutive_attempts, created_at`
**Filter Keys:** `type, date_range, ip_address, user_identifier, country`
**Batch Actions:** Bloquear IPs · Exportar

### Charts
| ID | Tipo | Título | Grid |
|----|------|--------|------|
| chart-login-success-fail | XYChart (ColumnSeries grouped) | Sucesso vs. Falha por Hora | col-md-8 |
| chart-login-countries | MapChart | Tentativas por País | col-md-4 |
| chart-login-timeline | XYChart (LineSeries) | Volume de Tentativas por Dia | col-12 |

### Drawers
- `drawer-filter-login.php` — w-400px
- `drawer-view-login.php` — w-600px
- `drawer-create-block.php` — w-400px
  - IP ou range CIDR, Motivo, Duração (horas/dias/permanente), Observação

---

## 6. System Events

### Header
- **Ícone:** `fa-solid fa-bolt` · cor `ttsc-text-info`
- **Título:** System Events
- **Subtítulo:** Eventos internos do sistema, cron jobs e processos automatizados
- **Botões:** `Registrar Evento Manual` → drawer-create-event · `Filtros` → drawer-filter-events

### Widgets
| ID | Ícone | Título | Cor | Progress Label |
|----|-------|--------|-----|----------------|
| widget-events-today | fa-bolt | Eventos Hoje | info | vs. ontem |
| widget-events-errors | fa-circle-exclamation | Erros de Sistema | danger | últimas 24h |
| widget-events-cron | fa-clock-rotate-left | Cron Jobs Executados | secondary | hoje |
| widget-events-pending | fa-hourglass-half | Eventos Pendentes | warning | fila atual |

### DataTable
| Coluna | Tipo | Alinhamento | Notas |
|--------|------|-------------|-------|
| # | checkbox | center | — |
| code | mono | center | — |
| Tipo | badge | left | CRON/SYSTEM/APP/DEPLOY/MAINTENANCE |
| Categoria | badge-soft | left | Info/Warning/Error/Critical |
| Fonte | mono | left | nome do processo/serviço |
| Descrição | texto truncado | left | — |
| Duração | mono | center | ms ou segundos |
| Status | badge | center | Sucesso/Falha/Em execução |
| Data/Hora | datetime | center | — |
| Ações | botões | center | Ver Detalhes, Reexecutar |

**SORT_FIELDS:** `code, type, category, source, status, duration, created_at`
**Filter Keys:** `type, category, status, source, date_range`
**Batch Actions:** Exportar · Marcar como Lido · Excluir

### Charts
| ID | Tipo | Título | Grid |
|----|------|--------|------|
| chart-events-type-donut | PieChart (donut) | Eventos por Tipo | col-md-4 |
| chart-events-status-bar | XYChart (ColumnSeries) | Status por Tipo de Evento | col-md-8 |
| chart-events-timeline | XYChart (LineSeries) | Volume de Eventos por Dia | col-12 |

### Drawers
- `drawer-filter-events.php` — w-400px
- `drawer-view-event.php` — w-800px (stack trace, payload, logs detalhados)
- `drawer-create-event.php` — w-600px
  - Tipo, Categoria, Fonte, Descrição, Payload JSON (textarea), Status

---

## 7. Database Audits

### Header
- **Ícone:** `fa-solid fa-database` · cor `ttsc-text-secondary`
- **Título:** Database Audits
- **Subtítulo:** Auditoria de queries, alterações de schema e acessos diretos ao banco
- **Botões:** `Configurar Auditoria` → drawer-config-db · `Filtros` → drawer-filter-db

### Widgets
| ID | Ícone | Título | Cor | Progress Label |
|----|-------|--------|-----|----------------|
| widget-db-queries-total | fa-magnifying-glass | Queries Hoje | primary | volume total |
| widget-db-slow-queries | fa-snail | Slow Queries | warning | acima de 500ms |
| widget-db-schema-changes | fa-table-list | Mudanças de Schema | danger | últimas 24h |
| widget-db-direct-access | fa-terminal | Acessos Diretos | dark | fora da app |

### DataTable
| Coluna | Tipo | Alinhamento | Notas |
|--------|------|-------------|-------|
| # | checkbox | center | — |
| code | mono | center | — |
| Tipo | badge | center | SELECT/INSERT/UPDATE/DELETE/DDL |
| Tabela(s) | texto | left | tabelas envolvidas |
| Usuário DB | mono | left | usuário de conexão |
| Usuário App | texto | left | user_code |
| Duração | mono+badge | center | badge danger se slow |
| Rows Afetadas | número | center | — |
| Query | código truncado | left | click → drawer view |
| Data/Hora | datetime | center | — |
| Ações | botões | center | Ver Query, Analisar |

**SORT_FIELDS:** `code, type, table_name, db_user, app_user_code, duration, rows_affected, created_at`
**Filter Keys:** `type, table_name, is_slow, db_user, app_user_uuid, date_range`
**Batch Actions:** Exportar · Marcar como Revisado

### Charts
| ID | Tipo | Título | Grid |
|----|------|--------|------|
| chart-db-query-types | PieChart (donut) | Queries por Tipo (DML/DDL) | col-md-4 |
| chart-db-slow-timeline | XYChart (LineSeries) | Slow Queries ao Longo do Dia | col-md-8 |
| chart-db-tables-bar | XYChart (BarSeries horizontal) | Top 10 Tabelas Mais Acessadas | col-12 |

### Drawers
- `drawer-filter-db.php` — w-400px
- `drawer-view-db-query.php` — w-800px (query formatada, EXPLAIN plan, contexto)
- `drawer-config-db.php` — w-600px
  - Capturar slow queries (toggle + threshold ms)
  - Capturar DDL (toggle)
  - Capturar acessos diretos (toggle)
  - Tabelas excluídas da auditoria (multi-select)
  - Usuários DB auditados (multi-select)

---

## 8. Metrics

### Header
- **Ícone:** `fa-solid fa-chart-line` · cor `ttsc-text-success`
- **Título:** Metrics
- **Subtítulo:** Performance, disponibilidade e saúde do sistema
- **Botões:** `Configurar Alertas` → drawer-config-metrics · `Período` → dropdown (1h/24h/7d/30d)

### Widgets
| ID | Ícone | Título | Cor | Progress Label |
|----|-------|--------|-----|----------------|
| widget-metrics-uptime | fa-circle-check | Uptime | success | % disponibilidade |
| widget-metrics-response | fa-gauge | Tempo Médio Resposta | info | ms média |
| widget-metrics-errors-rate | fa-circle-exclamation | Taxa de Erros | danger | % requisições |
| widget-metrics-throughput | fa-arrows-up-down | Throughput | primary | req/min |

### DataTable — Snapshots de Métricas
| Coluna | Tipo | Alinhamento | Notas |
|--------|------|-------------|-------|
| # | checkbox | center | — |
| code | mono | center | — |
| Métrica | texto | left | nome da métrica |
| Valor | número+unidade | right | com unidade (ms/%, req/s) |
| Threshold Warning | número | right | amarelo se ultrapassado |
| Threshold Critical | número | right | vermelho se ultrapassado |
| Status | badge | center | Normal/Warning/Critical |
| Coletado em | datetime | center | — |
| Ações | botões | center | Ver Histórico, Configurar |

**SORT_FIELDS:** `code, metric_name, value, status, collected_at`
**Filter Keys:** `status, metric_name, date_range`

### Charts
| ID | Tipo | Título | Grid |
|----|------|--------|------|
| chart-metrics-response-time | XYChart (AreaSeries) | Tempo de Resposta (ms) | col-12 |
| chart-metrics-error-rate | XYChart (LineSeries) | Taxa de Erros % | col-md-6 |
| chart-metrics-throughput | XYChart (ColumnSeries) | Throughput (req/min) | col-md-6 |
| chart-metrics-uptime-gauge | RadarChart (gauge) | Score de Uptime | col-md-4 |
| chart-metrics-cpu-memory | XYChart (LineSeries dual) | CPU vs. Memória % | col-md-8 |

### Drawers
- `drawer-config-metrics.php` — w-600px
  - Lista de métricas ativas com thresholds configuráveis
  - Intervalo de coleta (select: 30s/1min/5min)
  - Alertas por métrica (toggle + threshold + canal de notificação)

---

## 9. Alerts

### Header
- **Ícone:** `fa-solid fa-bell` · cor `ttsc-text-warning`
- **Título:** Alerts
- **Subtítulo:** Central de alertas disparados e regras de monitoramento
- **Botões:** `Nova Regra` → drawer-create-alert-rule · `Filtros` → drawer-filter-alerts

### Widgets
| ID | Ícone | Título | Cor | Progress Label |
|----|-------|--------|-----|----------------|
| widget-alerts-open | fa-bell-ring | Alertas Abertos | danger | sem resolução |
| widget-alerts-critical | fa-skull | Críticos | danger | alta prioridade |
| widget-alerts-resolving | fa-spinner | Em Resolução | warning | em andamento |
| widget-alerts-resolved-today | fa-bell-slash | Resolvidos Hoje | success | % do total |

### DataTable
| Coluna | Tipo | Alinhamento | Notas |
|--------|------|-------------|-------|
| # | checkbox | center | — |
| code | mono | center | — |
| Regra | texto | left | nome da regra disparada |
| Severidade | badge | center | Critical/High/Medium/Low |
| Módulo Origem | badge-soft | left | — |
| Descrição | texto truncado | left | — |
| Responsável | avatar+texto | left | quem está resolvendo |
| Status | badge | center | Aberto/Em Análise/Resolvido/Ignorado |
| Disparado em | datetime | center | — |
| Resolvido em | datetime | center | — se aberto |
| Ações | botões | center | Ver, Assumir, Resolver, Ignorar |

**SORT_FIELDS:** `code, rule_name, severity, module, status, fired_at, resolved_at`
**Filter Keys:** `severity, status, module, rule_name, date_range, responsible_uuid`
**Batch Actions:** Resolver Selecionados · Ignorar · Atribuir Responsável · Exportar

### Charts
| ID | Tipo | Título | Grid |
|----|------|--------|------|
| chart-alerts-severity | PieChart (donut) | Alertas por Severidade | col-md-4 |
| chart-alerts-modules | XYChart (BarSeries horizontal) | Alertas por Módulo | col-md-8 |
| chart-alerts-sla | XYChart (ColumnSeries) | Tempo Médio de Resolução (SLA) | col-12 |

### Drawers
- `drawer-filter-alerts.php` — w-400px
- `drawer-view-alert.php` — w-800px (timeline de análise, responsáveis, histórico)
- `drawer-create-alert-rule.php` — w-600px
  - Nome da regra, Módulo, Condição (tipo evento / threshold / regex)
  - Severidade, Canais de notificação (email/webhook/slack)
  - Cooldown (evitar spam), Status (ativo/inativo)
  - Footer: Cancelar | Salvar Regra

---

## 10. Kanban de Alertas

### Header
- **Ícone:** `fa-solid fa-table-columns` · cor `ttsc-text-primary`
- **Título:** Kanban de Alertas
- **Subtítulo:** Gestão visual do fluxo de resolução de alertas
- **Botões:** `Filtrar` → drawer-filter-kanban · `Criar Alerta` → drawer-create-alert · `Exportar` dropdown

### Widgets (topo)
| ID | Ícone | Título | Cor |
|----|-------|--------|-----|
| widget-kanban-open | fa-inbox | Abertos | danger |
| widget-kanban-analysis | fa-magnifying-glass | Em Análise | warning |
| widget-kanban-solving | fa-wrench | Em Resolução | info |
| widget-kanban-done | fa-circle-check | Concluídos Hoje | success |

### Layout Kanban
```
┌─────────────────────────────────────────────────────────────────┐
│  [🔴 Abertos N]  [🟡 Em Análise N]  [🔵 Em Resolução N]  [✅ Resolvidos N]  [⚫ Ignorados N]
├──────────────┬────────────────┬──────────────────┬─────────────┬──────────────┤
│  Card Alert  │   Card Alert   │   Card Alert     │ Card Alert  │ Card Alert   │
│  Card Alert  │   Card Alert   │                  │ Card Alert  │              │
│  Card Alert  │                │                  │             │              │
│  [+ Adicionar]│               │                  │             │              │
└──────────────┴────────────────┴──────────────────┴─────────────┴──────────────┘
```

### Card de Alerta (Kanban)
```html
<div class="ttsc-kanban-card" data-alert-uuid="{uuid}" draggable="true">
  <div class="d-flex justify-content-between align-items-start">
    <span class="ttsc-badge ttsc-badge-{severity}">{severity}</span>
    <span class="ttsc-text-muted fs-8">{code}</span>
  </div>
  <div class="ttsc-kanban-card-title mt-2">{rule_name}</div>
  <div class="ttsc-text-muted fs-8 mt-1">{module_origin}</div>
  <div class="ttsc-kanban-card-desc mt-1">{description truncated}</div>
  <hr class="my-2">
  <div class="d-flex justify-content-between align-items-center">
    <div class="ttsc-avatar-group"><!-- responsáveis --></div>
    <span class="fs-8 ttsc-text-muted"><i class="fa-regular fa-clock"></i> {fired_at}</span>
  </div>
  <div class="d-flex gap-1 mt-2">
    <button class="btn btn-xs btn-light" data-action="view"><i class="fa-solid fa-eye"></i></button>
    <button class="btn btn-xs btn-light-primary" data-action="assign"><i class="fa-solid fa-user-plus"></i></button>
    <button class="btn btn-xs btn-light-success" data-action="resolve"><i class="fa-solid fa-check"></i></button>
  </div>
</div>
```

### Drag & Drop
- Arrastar card entre colunas muda `status` via API REST (PATCH /api/logger/alerts/{uuid}/status)
- Confirmação visual: animação de drop + toast de sucesso
- Restrição: não pode mover de "Resolvido" para "Aberto" sem permissão de superadmin

### Drawers Kanban
- `drawer-filter-kanban.php` — w-400px
  - Severidade, Módulo, Responsável, Período
- `drawer-create-alert.php` — w-600px (igual ao drawer-create-alert da página Alerts)
- `drawer-view-alert-kanban.php` — w-800px (idêntico ao drawer-view-alert)

---

## 11. Automações

### Header
- **Ícone:** `fa-solid fa-robot` · cor `ttsc-text-primary`
- **Título:** Automações
- **Subtítulo:** Regras automáticas de resposta a eventos do logger
- **Botões:** `Nova Automação` → drawer-create-automation · `Logs de Execução` → drawer-automation-logs

### Widgets
| ID | Ícone | Título | Cor | Progress Label |
|----|-------|--------|-----|----------------|
| widget-auto-active | fa-circle-play | Automações Ativas | success | total configuradas |
| widget-auto-triggered | fa-bolt | Disparadas Hoje | primary | vs. ontem |
| widget-auto-success | fa-circle-check | Executadas com Sucesso | success | % do total |
| widget-auto-failed | fa-circle-xmark | Com Falha | danger | necessitam atenção |

### DataTable — Regras de Automação
| Coluna | Tipo | Alinhamento | Notas |
|--------|------|-------------|-------|
| # | checkbox | center | — |
| code | mono | center | — |
| Nome | texto | left | nome da automação |
| Gatilho | badge | left | tipo de evento que dispara |
| Condição | texto truncado | left | lógica da condição |
| Ação | badge-soft | left | bloquear IP/criar alerta/notificar/webhook |
| Módulo | texto | left | módulo alvo |
| Execuções | número | center | total histórico |
| Última Exec. | datetime | center | — |
| Status | toggle | center | ativo/inativo (edita inline) |
| Ações | botões | center | Editar, Testar, Logs, Excluir |

**SORT_FIELDS:** `code, name, trigger_type, action_type, module, executions, last_executed_at, status`
**Filter Keys:** `status, trigger_type, action_type, module`
**Batch Actions:** Ativar · Desativar · Excluir · Exportar

### Charts
| ID | Tipo | Título | Grid |
|----|------|--------|------|
| chart-auto-triggers | PieChart (donut) | Automações por Tipo de Gatilho | col-md-4 |
| chart-auto-timeline | XYChart (ColumnSeries) | Execuções por Dia | col-md-8 |
| chart-auto-success-rate | XYChart (LineSeries) | Taxa de Sucesso ao Longo do Tempo | col-12 |

### Drawers Automações
- `drawer-filter-automations.php` — w-400px
- `drawer-create-automation.php` — w-700px
  - **Seção: Identificação** — Nome, Descrição
  - **Seção: Gatilho** — Tipo de evento (select), Módulo alvo, Severidade mínima
  - **Seção: Condição** — Editor de condição (campo + operador + valor, multi-linha com AND/OR)
  - **Seção: Ação** — Tipo de ação (select múltipla):
    - Bloquear IP (duração)
    - Criar alerta (severidade)
    - Notificar por email (destinatários)
    - Webhook (URL + payload JSON)
    - Encerrar sessão do usuário
    - Executar cron específico
  - **Seção: Controle** — Cooldown entre disparos (min), Limite diário de execuções, Status (toggle)
  - Footer: Cancelar | Testar Regra | Salvar Automação

- `drawer-edit-automation.php` — w-700px (idêntico ao create com campos preenchidos)
- `drawer-automation-logs.php` — w-800px
  - DataTable de execuções: código, automação, gatilho, status, duração, data
  - Filtros: automação, status, período

---

## 12. Controles

### Header
- **Ícone:** `fa-solid fa-sliders` · cor `ttsc-text-dark`
- **Título:** Controles do Logger
- **Subtítulo:** Configurações de captura, retenção e controle de acesso ao módulo
- **Botões:** `Salvar Configurações` (fa-floppy-disk) · `Resetar Padrões` (fa-rotate-left, btn-light-warning)

### Widgets
| ID | Ícone | Título | Cor | Progress Label |
|----|-------|--------|-----|----------------|
| widget-ctrl-storage | fa-hard-drive | Uso de Armazenamento | info | % utilizado |
| widget-ctrl-retention | fa-calendar-xmark | Retenção Ativa | secondary | dias configurados |
| widget-ctrl-modules | fa-toggle-on | Módulos Ativos | success | N de M módulos |
| widget-ctrl-last-cleanup | fa-broom | Última Limpeza | primary | data e hora |

### Seções da Página de Controles

#### 12.1 Captura por Módulo
```
Tabela de toggles por módulo:
| Módulo | Capturar | Severidade Mín. | Sampling % | Ações |
```
- Toggle de ativação por módulo
- Select de severidade mínima para captura
- Slider de sampling (0-100%) para logs de alto volume
- Botão "Configurar" → drawer específico do módulo

#### 12.2 Políticas de Retenção
```
Tabela de retenção:
| Módulo | Retenção (dias) | Auto-archive | Auto-delete | Última Limpeza |
```
- Input numérico de retenção por módulo (1-3650 dias)
- Toggle de auto-archive (move para cold storage)
- Toggle de auto-delete (exclui após retenção)
- Botão "Executar Limpeza Agora" (abre confirmação)

#### 12.3 Controle de Acesso (ACL)
```
Tabela de permissões por role:
| Role | Dashboard | Sessions | Audit Trail | Security | DB Audits | ... |
```
- Checkbox grid: pode Visualizar / Exportar / Gerenciar por módulo por role
- Roles: SuperAdmin / Admin Tenant / Gestor / Auditor (read-only)

#### 12.4 Configurações Globais
- Timezone para timestamps dos logs (select)
- Formato de data na UI (DD/MM/YYYY ou YYYY-MM-DD)
- Nível de verbosidade global (Debug/Info/Warning/Error)
- Habilitar mascaramento de dados sensíveis nos logs (toggle + regex patterns)
- Habilitar LGPD compliance mode (toggle) → activa anonimização automática de IPs após X dias

### DataTable — Histórico de Alterações de Controles
| Coluna | Tipo | Alinhamento |
|--------|------|-------------|
| Admin | avatar+texto | left |
| Configuração Alterada | texto | left |
| Valor Anterior | código | center |
| Novo Valor | código | center |
| Data/Hora | datetime | center |

### Drawers Controles
- `drawer-module-capture-config.php` — w-600px (configuração detalhada por módulo)
- `drawer-retention-cleanup.php` — w-500px (confirmação de limpeza com estimativa de registros a excluir)
- `drawer-acl-role-detail.php` — w-700px (permissões detalhadas por role)

---

## 13. Gerenciamentos

### Header
- **Ícone:** `fa-solid fa-gears` · cor `ttsc-text-secondary`
- **Título:** Gerenciamento do Logger
- **Subtítulo:** Manutenção, exportações em massa, integrações e saúde do módulo
- **Botões:** `Exportar Tudo` → drawer-bulk-export · `Diagnóstico` → drawer-diagnostics

### Widgets
| ID | Ícone | Título | Cor | Progress Label |
|----|-------|--------|-----|----------------|
| widget-mgmt-total-records | fa-table | Total de Registros | primary | todos os módulos |
| widget-mgmt-db-size | fa-database | Tamanho do BD Logger | info | GB utilizado |
| widget-mgmt-last-backup | fa-box-archive | Último Backup | success | data e hora |
| widget-mgmt-integrations | fa-plug | Integrações Ativas | secondary | N configuradas |

### Abas da Página (tabs)
```html
<ul class="nav nav-tabs" id="mgmt-tabs">
  <li><a data-tab="backups">Backups & Arquivos</a></li>
  <li><a data-tab="integrations">Integrações</a></li>
  <li><a data-tab="scheduled">Tarefas Agendadas</a></li>
  <li><a data-tab="health">Saúde do Sistema</a></li>
  <li><a data-tab="lgpd">LGPD/Compliance</a></li>
</ul>
```

#### Aba: Backups & Arquivos
DataTable de backups:
| Coluna | Tipo | Notas |
|--------|------|-------|
| code | mono | — |
| Nome do Arquivo | texto | — |
| Módulo(s) | badges | quais módulos incluídos |
| Tamanho | texto | KB/MB/GB |
| Tipo | badge | Full/Incremental/Module |
| Status | badge | Completo/Falhou/Em Progresso |
| Criado em | datetime | — |
| Ações | botões | Download, Restaurar, Excluir |

Botões: `Novo Backup` → drawer-create-backup

#### Aba: Integrações
DataTable de integrações:
| Coluna | Tipo | Notas |
|--------|------|-------|
| code | mono | — |
| Nome | texto | — |
| Tipo | badge | Webhook/Syslog/SIEM/Email/Slack |
| URL/Endpoint | mono truncado | — |
| Eventos Enviados | badge | quais tipos de evento |
| Último Envio | datetime | — |
| Status | toggle | ativo/inativo |
| Ações | botões | Editar, Testar, Excluir |

Botões: `Nova Integração` → drawer-create-integration

#### Aba: Tarefas Agendadas
DataTable de cron jobs do logger:
| Coluna | Tipo | Notas |
|--------|------|-------|
| code | mono | — |
| Tarefa | texto | descrição da tarefa |
| Expressão Cron | mono | ex: 0 2 * * * |
| Próxima Exec. | datetime | — |
| Última Exec. | datetime | — |
| Status Último | badge | Sucesso/Falha |
| Status | toggle | ativo/inativo |
| Ações | botões | Editar, Executar Agora, Histórico |

#### Aba: Saúde do Sistema
- Checklist visual de status: banco, disco, integrações, crons, backups
- Cada item: ícone (fa-circle-check verde / fa-circle-xmark vermelho / fa-circle-half-stroke amarelo)
- Charts:
  - `chart-health-db-size` — XYChart (AreaSeries) — crescimento do BD ao longo de 30 dias
  - `chart-health-records-growth` — XYChart (LineSeries) — crescimento de registros por módulo

#### Aba: LGPD/Compliance
- Status de conformidade LGPD por módulo (tabela com badges Verde/Amarelo/Vermelho)
- Configuração de anonimização automática (IPs, emails, user agents após N dias)
- Relatório de titulares de dados (exportação de logs por user_uuid para direito de portabilidade)
- Registro de solicitações de exclusão (direito ao esquecimento): DataTable com solicitações, status, executor

### Drawers Gerenciamento
- `drawer-bulk-export.php` — w-600px
  - Módulos a exportar (checkboxes)
  - Período (date range)
  - Formato (CSV/XLSX/JSON/XML/SQL)
  - Filtros adicionais por módulo
  - Footer: Cancelar | Gerar Exportação

- `drawer-diagnostics.php` — w-800px
  - Resultado de diagnóstico em tempo real (progress bars + status checks)
  - Sugestões automáticas de manutenção

- `drawer-create-backup.php` — w-500px
  - Módulos, tipo (Full/Incremental), compressão, destino

- `drawer-create-integration.php` — w-700px
  - Tipo, Nome, URL/endpoint, Headers, Eventos a enviar, Formato de payload, Autenticação

- `drawer-edit-integration.php` — w-700px

- `drawer-create-cron.php` — w-600px
  - Nome, Descrição, Expressão cron (com helper visual), Comando/função PHP, Timeout, Notificar em falha

---

## Referência Global de Ícones (FontAwesome 7.2)

| Contexto | Classe FA |
|----------|-----------|
| Dashboard | fa-solid fa-gauge-high |
| Sessões | fa-solid fa-users |
| Audit Trail | fa-solid fa-file-shield |
| Security | fa-solid fa-shield-halved |
| Login Attempts | fa-solid fa-right-to-bracket |
| System Events | fa-solid fa-bolt |
| DB Audits | fa-solid fa-database |
| Metrics | fa-solid fa-chart-line |
| Alerts | fa-solid fa-bell |
| Kanban | fa-solid fa-table-columns |
| Automações | fa-solid fa-robot |
| Controles | fa-solid fa-sliders |
| Gerenciamento | fa-solid fa-gears |
| Criar/Adicionar | fa-solid fa-plus |
| Editar | fa-solid fa-pen-to-square |
| Excluir | fa-solid fa-trash |
| Ver/Detalhes | fa-solid fa-eye |
| Filtrar | fa-solid fa-sliders |
| Exportar | fa-solid fa-download |
| Importar | fa-solid fa-upload |
| Resolver/OK | fa-solid fa-circle-check |
| Bloquear | fa-solid fa-ban |
| Alerta/Warning | fa-solid fa-triangle-exclamation |
| Erro | fa-solid fa-circle-exclamation |
| Sucesso | fa-solid fa-circle-check |
| Info | fa-solid fa-circle-info |
| Encerrar sessão | fa-solid fa-right-from-bracket |
| IP/Rede | fa-solid fa-network-wired |
| Webhook | fa-solid fa-webhook |
| Backup | fa-solid fa-box-archive |
| LGPD | fa-solid fa-user-shield |
| Drag handle | fa-solid fa-grip-vertical |

---

## Includes do drawer.php

```php
<?php
// Logger Module Drawers — /resources/app/partials/drawer.php
// ============================================================

// Dashboard
$this->fetch('drawers/drawer/admin/logger/drawer-config-dashboard.php');

// Sessions
$this->fetch('drawers/drawer/admin/logger/drawer-filter-sessions.php');
$this->fetch('drawers/drawer/admin/logger/drawer-view-session.php');

// Audit Trail
$this->fetch('drawers/drawer/admin/logger/drawer-filter-audit.php');
$this->fetch('drawers/drawer/admin/logger/drawer-view-audit.php');

// Security Logs
$this->fetch('drawers/drawer/admin/logger/drawer-filter-security.php');
$this->fetch('drawers/drawer/admin/logger/drawer-view-security.php');
$this->fetch('drawers/drawer/admin/logger/drawer-create-security-rule.php');

// Login Attempts
$this->fetch('drawers/drawer/admin/logger/drawer-filter-login.php');
$this->fetch('drawers/drawer/admin/logger/drawer-view-login.php');
$this->fetch('drawers/drawer/admin/logger/drawer-create-block.php');

// System Events
$this->fetch('drawers/drawer/admin/logger/drawer-filter-events.php');
$this->fetch('drawers/drawer/admin/logger/drawer-view-event.php');
$this->fetch('drawers/drawer/admin/logger/drawer-create-event.php');

// DB Audits
$this->fetch('drawers/drawer/admin/logger/drawer-filter-db.php');
$this->fetch('drawers/drawer/admin/logger/drawer-view-db-query.php');
$this->fetch('drawers/drawer/admin/logger/drawer-config-db.php');

// Metrics
$this->fetch('drawers/drawer/admin/logger/drawer-config-metrics.php');

// Alerts
$this->fetch('drawers/drawer/admin/logger/drawer-filter-alerts.php');
$this->fetch('drawers/drawer/admin/logger/drawer-view-alert.php');
$this->fetch('drawers/drawer/admin/logger/drawer-create-alert-rule.php');

// Kanban
$this->fetch('drawers/drawer/admin/logger/drawer-filter-kanban.php');
$this->fetch('drawers/drawer/admin/logger/drawer-create-alert.php');
$this->fetch('drawers/drawer/admin/logger/drawer-view-alert-kanban.php');

// Automações
$this->fetch('drawers/drawer/admin/logger/drawer-filter-automations.php');
$this->fetch('drawers/drawer/admin/logger/drawer-create-automation.php');
$this->fetch('drawers/drawer/admin/logger/drawer-edit-automation.php');
$this->fetch('drawers/drawer/admin/logger/drawer-automation-logs.php');

// Controles
$this->fetch('drawers/drawer/admin/logger/drawer-module-capture-config.php');
$this->fetch('drawers/drawer/admin/logger/drawer-retention-cleanup.php');
$this->fetch('drawers/drawer/admin/logger/drawer-acl-role-detail.php');

// Gerenciamento
$this->fetch('drawers/drawer/admin/logger/drawer-bulk-export.php');
$this->fetch('drawers/drawer/admin/logger/drawer-diagnostics.php');
$this->fetch('drawers/drawer/admin/logger/drawer-create-backup.php');
$this->fetch('drawers/drawer/admin/logger/drawer-create-integration.php');
$this->fetch('drawers/drawer/admin/logger/drawer-edit-integration.php');
$this->fetch('drawers/drawer/admin/logger/drawer-create-cron.php');
?>
```

---

## Checklist de Implementação por Página

- [ ] Header com breadcrumb, título, subtítulo e botões de ação
- [ ] 4 widgets KPI com IDs únicos, ícones, cores e progress bar
- [ ] Toolbar: busca + filtros rápidos + batch actions + dropdown de exportação (7 formatos) + botão Filtros
- [ ] DataTable com todas as colunas especificadas, paginação e footer de contagem
- [ ] Todos os gráficos amCharts 5 com destroy pattern antes de recriar
- [ ] Todos os drawers criados na pasta correta e incluídos no drawer.php
- [ ] Arquivo JS IIFE separado: `/assets/js/logger/ttsc.admin.logger.{page}.js`
- [ ] SORT_FIELDS e filter keys declarados no JS
- [ ] Badges usando classe `ttsc-badge-soft` para estados
- [ ] IDs seguem padrão: `id` (interno) · `uuid` (referências) · `code` (exposto na UI/API)
- [ ] Compliance LGPD: dados sensíveis mascarados conforme configuração de Controles
- [ ] Permissões ACL verificadas antes de renderizar ações (editar/excluir/exportar)
