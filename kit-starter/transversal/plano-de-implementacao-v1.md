# Plano de implementação da v1 (fases e checklist)

- Portal: Todos
- Área: Transversal
- Domínio: transversal: vale para todos os portais e módulos
- Status: detalhado; especificação da v1 absorvida integralmente (seção 13), com as correções da v2 e as decisões por padrão (seções 1 a 12)
- Fonte da v1: [TASKS_SPECS.md](../../docs/v2/anexo-v1/TASKS_SPECS.md) (821 linhas)

## 1. Regra de leitura
As seções 1 a 12 prevalecem sobre a seção 13. A seção 13 é o texto integral da v1, sem corte, para que nenhum detalhe se perca. Quando a seção 13 disser algo diferente das seções 1 a 12, vale o que está nas seções 1 a 12.

## 2. Objetivo e escopo
Plano de tarefas da v1 (fases 0 a 3, ordem de dependência e checklist de 18 itens por módulo), guardado integralmente como referência de ordem de construção.

## 3. Telas
- **Fases e tarefas** (lista): fase, tarefa, dependência, situação.
- **Checklist por módulo** (lista): 18 itens de auditoria por módulo.
**Títulos da v1 (referência, não são telas):**

- FASE 0 — Fundações Transversais (prioridade máxima)
  - 0.1 — Soft Delete (Exclusão Lógica)
  - 0.2 — Autenticação e Controle de Acesso ✅ (parcial)
  - 0.3 — Cookies e Sessions ✅
  - 0.4 — Design System (Supabase Pattern) ✅
  - 0.5 — Biblioteca de Componentes UI Enterprise ✅
  - 0.6 — Logger Module v3.0 ✅
  - 0.7 — Auditoria Module ✅
- FASE 1 — Privacidade, Segurança e Compliance
  - 1.1 — Privacy & Global Data Rights ✅
  - 1.2 — Sub-Sidebar Privacidade & LGPD ✅
  - 1.3 — SLSA Build Specification
  - 1.4 — Penetration Test v2
- FASE 2 — Módulos de Negócio (Domínio)
  - 2.1 — Gestão Acadêmica (ACM) ✅
  - 2.2 — Financeiro ✅
  - 2.3 — Billing, Cobrança e Mensalidades ✅
  - 2.4 — Contábil e Fiscal ✅
  - 2.5 — Contratos (CLM) ✅
  - 2.6 — Patrimônio (Asset Management) ✅
  - 2.7 — Suprimentos (Procurement v3) ✅
  - 2.8 — Armazenamento (WMS) ✅
  - 2.9 — Gestão de Pessoas (HCM/RH) ✅
  - 2.10 — Segurança e Medicina do Trabalho (SMT) ✅
  - 2.11 — Frotas (Fleet Management) ✅
  - 2.12 — Gestão de TI (ITSM) ✅
  - 2.13 — SAC / Help Desk / Service Desk ✅ (parcial — audit atualizado jul/2026)
  - 2.14 — Chat Rápido SAC ❌
  - 2.15 — Gestão de Notificações ✅
  - 2.16 — Gestão de Documentos ✅
  - 2.17 — Marketing e Redes Sociais ✅
  - 2.18 — Simulados e Correção de Redações por IA ✅
  - 2.19 — Preceptoria e Autoavaliação Médica ✅
- FASE 3 — Validação e Hardenização
  - 3.1 — Regression Audit (Post-Fix)
  - 3.2 — Security Hardening Final
- Ordem de Dependência Sugerida
- Checklist de Padrões por Módulo — Auditoria (18 itens)
  - Tabela Resumo
  - Lacunas por Item
  - Módulos mais completos (top 5)
  - Módulos menos completos (bottom 5)
- Progresso da Sessão (10/07/2026)

## 4. Correções da v2 que prevalecem
- **Ordem de construção da v2:** fundações transversais (tenancy [03](../../docs/v2/03-dominio-tenancy.md), identidade [06](../../docs/v2/06-identidade-acesso.md), auditoria [29](../../docs/v2/29-auditoria.md), exclusão lógica, privacidade [07](../../docs/v2/07-privacidade-lgpd.md)), depois o acadêmico na ordem do [55](../../docs/v2/55-academico-verificacao-e-lacunas.md), seção 3, e os demais módulos pela matriz [31](../../docs/v2/31-matriz-portais-modulos.md).
- **Definition of Done e gates:** [11](../../docs/v2/11-governanca-qualidade.md), seções 2 e 3.
- **Caminho `C:\Xampp\htdocs\ttscdoc\` e o progresso de 10/07/2026** são da v1 e não valem para a v2.

## 5. Decisões por padrão aplicadas
- Nenhuma decisão nova.

## 6. Permissões e papéis
- Não se aplica.

## 7. Dados
- Não se aplica.

## 8. Integrações
- Não se aplica.

## 9. Exportação, auditoria e privacidade
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../docs/v2/08-frontend-design-system.md), seção 3).
- Auditoria conforme [29](../../docs/v2/29-auditoria.md); dados pessoais conforme [07](../../docs/v2/07-privacidade-lgpd.md).


## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
- Backlog priorizado: [11](../../docs/v2/11-governanca-qualidade.md), seção 8.

## 13. Conteúdo integral da v1 (absorvido)

### TASKS — Implementação de Todos os Specs (ttscdoc)

> **Base path:** `C:\Xampp\htdocs\ttscdoc\`
> **Stack:** PHP 8 puro · MariaDB · Tailwind 4.2 · Supabase · amCharts 5 · Multi-tenant DB-per-unit
> **Padrão de cada módulo:** Dashboard (widgets + charts) → DataTable → CRUD Drawers → Kanban → Automações → Audit Trail → RBAC → REST endpoints → SQL schema → LGPD

- Language Standard: Global English
---

#### FASE 0 — Fundações Transversais (prioridade máxima)

Estas specs afetam todos os módulos. Devem ser implementadas primeiro.

##### 0.1 — Soft Delete (Exclusão Lógica)
- **Spec:** `spec-soft-delete-totustuus.md`
- **Entidades:** Todas as tabelas multi-tenant
- **Tarefas:**
  - [x] Adicionar colunas `deleted_at`, `deleted_by`, `deleted_reason`, `is_deleted` em todas as tabelas
  - [x] Criar composite indexes para queries com `WHERE deleted_at IS NULL`
  - [x] Implementar scopes `withTrashed()` / `onlyTrashed()` no base model
  - [x] Unique-constraint handling (MySQL virtual column / PG partial index)
  - [x] Cascade lógico (soft-delete pai → filhos)
  - [x] Purge job (LGPD retention)
  - [x] REST endpoints: `DELETE`, `/restore`, `?trashed=true`, `/purge`
  - [x] Pre-delete validation chain (HTTP 409 on failure)
  - [x] Migration + seed de teste
- **Implementação:**
  - `app/Exceptions/BusinessRuleException.php` — exceção com rule codes (HTTP 409)
  - `app/Contracts/SoftDeletableRepository.php` — interface padrão (spec 5.1)
  - `app/Services/SoftDeleteService.php` — cadeia de validação, cascata, restore, purge
  - `app/Services/SoftDeleteRegistry.php` — registro de recursos soft-deletáveis
  - `app/Http/Controllers/Api/SoftDeleteController.php` — endpoints REST genéricos
  - `database/migrations/2026_07_04_000001_add_soft_delete_unique_constraints.php` — virtual columns (spec 4.3)
  - `database/migrations/2026_07_04_000002_soft_delete_retention_policies.php` — políticas retenção LGPD + seed
  - `database/migrations/2026_07_04_000003_extend_audit_logs_action_enum.php` — ENUM audit logs
  - `app/Services/RetentionManager.php` — `purgeSoftDeleted()` job LGPD com anonimização
  - `routes/api.php` — rotas `/api/v1/soft-delete/{resource}/{id}` (DELETE/restore/purge/list)
  - `tests/SoftDeleteTest.php` — 19 testes (spec seção 8 + 4.2 + 4.6)

##### 0.2 — Autenticação e Controle de Acesso ✅ (parcial)
- **Spec:** `spec_gestao_autenticacao_completo.md`
- **Entidades:** Users, Entities, Units, Roles, Permissions, Sessions
- **Status:** 7 de 9 tarefas concluídas. Faltam Acessibilidade WCAG 2.1 AA.
- **Tarefas:**
  - [x] **5 portais (Admin, Teacher, Student, Parents, Third-Party) com routing:**
    - PortalMiddleware criado (`app/Http/Middleware/PortalMiddleware.php`) — restringe rotas por tipo de portal
    - Portal armazenado em `$_SESSION['user_portal']` durante o login
    - Cada portal-specific login form (`login-teacher`, `login-student`, `login-parents`, `login-thirdparty`) envia `input hidden name="portal"`
    - POST `/login` lê o portal, armazena na sessão, redireciona para dashboard correto
    - GuestMiddleware redireciona para dashboard do portal em vez de sempre `/admin`
    - select-portal agora inclui o 5º portal "Terceiros"
    - PortalRedirects: `/admin`, `/teacher/dashboard`, `/student/dashboard`, `/parents/dashboard`, `/thirdparty/dashboard`
  - [x] **Login flow: credenciais → contexto (entity/unit) → session/token → routing:**
    - Fluxo corrigido: `/select-portal` (Guest) → portal-specific login → POST `/login` → portal na session → redirect
    - Entity/Unit selection pós-login com API real em vez de dados mockados
    - Select-entity/unit mantidos como AuthMiddleware (pós-login, contexto multi-tenant)
  - [x] **MFA (TOTP):** Completo — RFC 6238, backup codes, AAL tracking, RiskEngine adaptativo
  - [x] **Session rotation + revocation:** Completo — DB-backed, hard+idle timeout, revocation, JWT blacklist
  - [x] **Password policy:** Completo — 12 char min, 3-of-4 classes, Argon2id, rehash transparente
  - [x] **Rate limiting / brute-force protection:** Completo — 3 camadas (global, per-route, per-user)
  - [x] **Audit trail de auth events:** Completo — login_attempts, security_logs, user_session_events, access_logs
  - [x] **Selectors de entity/unit no login:**
    - API real: `EntityUnitController` — `/api/v1/entities`, `/api/v1/entities/{uuid}/units`, `/api/v1/entities/{uuid}/select`, `/api/v1/units/{uuid}/select`, `/api/v1/context`
    - Views `select-entity.php` e `select-unit.php` atualizadas para consumir API em vez de dados mockados
    - Rotas registradas em `routes/api.php`
    - select-portal exibe contexto real via API
  - [ ] Acessibilidade (WCAG 2.1 AA) — pendente

##### 0.3 — Cookies e Sessions ✅
- **Spec:** `spec_gestao_cookies_sessions.md`
- **Entidades:** CookiePolicy, Session, SessionDevice, SessionEvent, SessionRule, SessionAutomation, ConsentRecord, SecurityIncident
- **Status:** Implementado — banco, controllers, views, routes, drawers, JS
- **Tarefas:**
  - [x] **Dashboard KPIs + charts:** Privacy dashboard (`privacy_dashboard.php`) + logger dashboard com widgets de sessões ativas, devices, geolocation
  - [x] **Sessions datatable + drawer CRUD:** `session_manager.php` (PrivacyController), `sessions.php` (LoggerController), drawers: session_details, session_revoke, session_filters, session_export — dados reais de `user_sessions`
  - [x] **Cookie policies datatable + drawer CRUD:** `privacy_cookie_categories` + `privacy_cookie_catalog` tables, `preferenceCenter()` view, `consentConfig()`/`consentDecisions()`/`consentRevoke()` endpoints. Banner consent modal com `consent-cookie.js`
  - [x] **Consents (LGPD banner + granular):** `user_cookie_consents`, `user_cookie_consent_items`, `privacy_consent_events` tables; banner funcional + preference center granular por categoria; consentimento auditado
  - [x] **Rules/automations:** Governance automations (`governance_automations.php`, `apiGovernanceAutomations`) com triggers, actions, agenda, logs
  - [x] **Security rules:** `remember_tokens` (Argon2id, series rotation), `jwt_blacklist`, `rate_limits`; `session-timeout` config (`session_timeout.php`); cookies HttpOnly/Secure/SameSite config via `privacy_cookie_catalog`
  - [x] **Retention policies + immutable audit trail:** `log_retention_policies`, `soft_delete_retention_policies` tables; `drawer-retention-cleanup.php`; `privacy_consent_events` imutável; `ttsc_sensitive_data_access` audit trail

##### 0.4 — Design System (Supabase Pattern) ✅
- **Spec:** `spec_design_system_preview_supabase.md`
- **Status:** Implementado em `assets/css/ttsc.supabase.css` + `ttsc.css`
- **Tarefas:**
  - [x] Color palette: near-black bg (#0f0f0f/#171717) + emerald (#3ecf8e/#00c573)
  - [x] Tipografia: Circular + Source Code Pro
  - [x] HSL-alpha token system
  - [x] Border-defined depth (no shadows)
  - [x] Spacing 8px base, breakpoints mobile-first 600px
  - [x] Componentes: buttons, cards, tabs, links, navigation
  - [x] Dark mode nativo

##### 0.5 — Biblioteca de Componentes UI Enterprise ✅
- **Spec:** `spec_gestao_biblioteca_completo.md`
- **Status:** Implementado — átomos + moléculas + DataTable + Drawer + Saved Views
- **Tarefas:**
  - [x] **Foundations:** Tokens em `ttsc.css` (cores, tipografia, spacing, radius, elevation, motion, z-index)
  - [x] **Átomos (PHP Partials):** `input.php`, `select.php`, `button.php`, `badge.php`, `empty_state.php`, `loading.php`
  - [x] **Moléculas:** `field_group.php` (grid de campos), `pagination.php` (reutilizável com JS embutido)
  - [x] **Organismos:** `drawer.php` (padronizado com 4 tamanhos), `confirm_dialog.php` (com callback JS), `datatable.php` (container HTML)
  - [x] **DataTable Enterprise:** `ttsc.datatable.js` — classe JS completa: server-side fetch, sort, filter, paginação, seleção em massa, export CSV, saved views, row click, actions
  - [x] **Drawer padronizado:** CSS centralizado em `ttsc.supabase.css` com variável `--drawer-width`, template PHP reutilizável
  - [x] **Saved Views:** Tabela `saved_views` (migration), `SavedViewsController` (API REST CRUD), rotas em `api.php`, UI integrada no DataTable JS
  - [ ] Estados loading/empty/error/success — parciais (partials existem, falta integração sistemática)
  - [ ] Telemetry hooks
  - [ ] Security hooks: masking, RBAC, destructive-action confirmation
  - [ ] Domain packs: finance, education, health, CRM, stock, support, compliance

##### 0.6 — Logger Module v3.0 ✅
- **Spec:** `spec_gestao_logger_completo.md`
- **Entidades:** Sessions, AuditTrail, SecurityLogs, LoginAttempts, SystemEvents, DBAudits, Metrics, Alerts, Automations
- **Status:** 27 views completas (LoggerController 5055 linhas), 99 drawer partials, 19 JS modules dedicados com amCharts integrados
- **Tarefas:**
  - [x] **~13 páginas padronizadas:** 27 views seguem Header → Widgets → DataTable → Charts (amCharts 5) → Drawers → JS externo
  - [x] **Widget card template + toolbar batch actions + 7 export formats:** Widget cards em 27/27 views; export 7 formatos em 14+ views; batch actions em 14 views
  - [x] **amCharts destroy/recreate pattern:** Todos os 19 JS modules implementam destroy/recreate via `window._charts[chartId].dispose()` + `am5.Root.new(chartId)` — 44+ instâncias de chart em todo o módulo
  - [x] **Drawer widths padronizados:** Drawers seguem convenção w-400px (filtros), w-600px (CRUD), w-800px (visualização)
  - [ ] **Global events feed datatable:** Pendente (feed de eventos consolidado em dashboard)
  - [x] **Export CSV/XLSX/PDF/JSON/XML/SQL/TXT:** Implementado em 14 views via `exportLogs()` + dropdown JS
  - [x] **CSS prefix `ttsc-`:** Classes `ttsc-` nas views, widget cards, datatables, drawers

##### 0.7 — Auditoria Module ✅
- **Spec:** `spec_gestao_auditoria_completo.md`
- **Entidades:** AuditLog, SecurityLog, AccessLog, ChangeLog, APILog, AutomationLog, IntegrationLog, Evidence, ReviewCase, AuditRule, RetentionPolicy, Exception, CorrelationSession
- **Status:** Módulo completo — implementado dentro do LoggerController (255KB). 35+ views de logger + auditoria em `pages/logger/` incluindo audit_trail, security, change_log, evidence, review, exceptions, audit_rules, retention_policy, correlation, compliance, sessions, login_attempts, api_logs, db_audits, system_events, error_logs, metrics, alerts, kanban, automations e management.
- **Tarefas:**
  - [x] **Dashboard widgets + charts:** Logger dashboard + privacy dashboard com widgets e charts amCharts
  - [x] **Audit Trail datatable com before/after + correlation:** `audit_trail.php` + `correlation.php`
  - [x] **Security Logs:** `security.php` completo
  - [x] **API Logs page:** `api_logs.php` — monitoramento de chamadas REST com charts de métodos HTTP, status code, latência
  - [x] **Change Log page:** `change_log.php` — versionamento de registros críticos com diff antes/depois
  - [x] **Evidence page:** `evidence.php` — centro de evidências (screenshots, PDFs, logs, hashes)
  - [x] **Review Case page:** `review.php` — workflow de revisão com kanban de status + drawers
  - [x] **Exceptions page:** `exceptions.php` — monitoramento de exceções com severidade, fonte, timeline
  - [x] **Audit Rules page:** `audit_rules.php` — regras de auditoria (eventos obrigatórios, limiares, alertas)
  - [x] **Retention Policy page:** `retention_policy.php` — políticas de retenção por tipo de evento com purge agendado
  - [x] **Drawers CRUD:** 99 drawer partials para entidades existentes + drawers para cada nova página
  - [x] **Export/retention:** Export 7 formatos em 14+ views; retenção configurável
  - [x] **LGPD/GDPR controls:** `compliance.php` + `management_compliance.php`

---

#### FASE 1 — Privacidade, Segurança e Compliance

##### 1.1 — Privacy & Global Data Rights ✅
- **Spec:** `spec_gestao_privacy_global_completo.md`
- **Entidades:** RegulatoryCatalog, Consent, DSR (Data Subject Request), RoPA, InternationalTransfer, RetentionPolicy, Incident/Breach, DPO/Governance
- **Status:** Implementado — catálogo de leis, consentimentos, DSR, RoPA, DPIA, DPO, incidentes, transferências, masking, portal público, automações
- **Tarefas:**
  - [x] **8 legislações suportadas (CCPA, COPPA, PIPL, GDPR, LGPD, PDPA, APPI, PIPEDA):** Tabela `privacy_laws` com CRUD completo (`masterLaws`, drawers view/new/edit); aplicabilidade por tenant em `tenant_privacy_laws`; 8 leis seedadas no migration
  - [x] **Dashboard executivo + operacional:** 3 dashboards — `master_dashboard.php` (visão global), `tenant_dashboard.php` (por tenant), `privacy_dashboard.php` (unificado com widgets + charts)
  - [x] **Datatables com colunas/filtros padronizados:** Todas as páginas usam DataTable com paginação, ordenação, filtros e exportação; filtros específicos por lei, unidade, status, período
  - [x] **Incident workflow 72h (GDPR):** `privacy_incidents` table + `incidents.php` view; classificação severidade, notificação regulatória, medidas contenção, playbook; prazos configuráveis por lei
  - [x] **DSR Kanban:** `dsr_requests` + `dsr_history` tables; `dsr.php` view com workflow de status; portal público (`public_portal.php`) para submissão e acompanhamento via protocolo; drawer de processamento (`process_dsr.php`)
  - [x] **Automações de governance:** `governance_automations` + `governance_automation_logs` tables; `governance_automations.php` view com CRUD; triggers para consentimento, DSR, retenção, incidentes, revisões periódicas

##### 1.2 — Sub-Sidebar Privacidade & LGPD ✅
- **Spec:** `spec-sub-sidebar-privacidade-lgpd.md`
- **Status:** Implementado — `sub_sidebar_privacy.php` existente com seções colapsáveis e navegação completa.
- **Tarefas:**
  - [x] Refatorar com `InnerSideMenuCollapsible` / `Trigger` / `Content` / `Item` / `Separator`
  - [x] Grupos colapsáveis: Conformidade Legal, Inventário & Direitos, Consentimentos, Transferências & Incidentes, Políticas, LGPD Masking
  - [x] Tenant/master context selector
  - [x] Novas rotas: `/admin/privacy/{dpia,transfers,incidents}`

##### 1.3 — SLSA Build Specification
- **Spec:** `slsa-build-spec.md`
- **Tarefas:**
  - [ ] SLSA Level 1: provenance generation (artifact digest, commit, pipeline, platform)
  - [ ] SLSA Level 2: build platform isolation + signing service
  - [ ] SLSA Level 3: attestation registry + deploy verification gate
  - [ ] KMS/secret vault integration
  - [ ] Centralized logging de builds
  - [ ] PHP, Node.js e container builds

##### 1.4 — Penetration Test v2
- **Spec:** `penetration-test-spec-v2.md`
- **Tarefas:**
  - [ ] OWASP WSTG / Top 10 / API Top 10 + NIST SP 800-115
  - [ ] 10 fases: recon → hardening → auth/session → authorization/isolation → injection/XSS/upload → API → logs → report
  - [ ] JWT, MFA, CORS, CSP, rate-limiting
  - [ ] Tenant isolation testing
  - [ ] Audit trail validation
  - [ ] Post-fix regression audit

---

#### FASE 2 — Módulos de Negócio (Domínio)

##### 2.1 — Gestão Acadêmica (ACM) ✅
- **Spec:** `spec_gestao_academica_completo.md`
- **Status:** 45+ tabelas, 60+ views, 250+ rotas, AcademicController 2200+ linhas. RBAC 8 perfis, wizard matrícula, QR/geo chamada, workflows completos, portais completos. Sidebar/sub-sidebar em inglês (padrão internacional).
- **Tarefas:**
  - [x] **8 perfis RBAC (SA/AU/CO/SE/PR/AL/RE/CP):** Implementado — migration `2026_07_08_000001_seed_academic_roles_permissions.php` cria 8 roles acadêmicas + 17 permissões granulares + role-permission matrix. Rotas acadêmicas (224) refatoradas para `AuthorizeMiddleware`. `User::hasRole()` corrigido.
  - [x] **Matrículas (manual):** `enrollments.php`, `enrollment_requests.php`, `EnrollmentController` (353 linhas, 19 APIs), fluxo create/submit/approve/reject/confirm/cancel/expire
  - [x] **Matrículas (wizard 6 etapas):** `enrollment_wizard.php` — 6-step wizard (Student Search → Enrollment Data → Guardian → Financial Plan → Documents → Contract & LGPD) com `apiEnrollmentWizardStore` (step-by-step persistence) + `apiStudentSearchCpf` (CPF duplicate detection) + protocol generation
  - [x] **Matrículas (online portal 7 passos):** `StudentEnrollmentController` estendido com 7 novos endpoints: `apiCheckVacancies` (real-time vacancy), `apiWaitlistJoin` (auto waitlist), `apiGetWaitlistPosition`, `apiUploadDocument` (document upload), `apiGetDocuments`, `apiGenerateProtocol` (protocol number), `apiLgpdConsent` (LGPD acceptance)
  - [x] **Transferência:** `enrollment_transfers.php` + `apiEnrollmentTransfer` — origem + destino, justificativa, cria nova matrícula vinculada, request code, atualiza status
  - [x] **Trancamento:** `enrollment_lock.php` + `apiEnrollmentLock` — motivo select (personal/financial/health/military/other), descrição, prazo, gera protocolo + request
  - [x] **Reopção de Curso:** `enrollment_course_change.php` + `apiEnrollmentCourseChange` — análise de equivalência curricular automática, aprovação coordenador, nova matrícula vinculada
  - [x] **Aproveitamento de Estudos:** `enrollment_credit_recognition.php` + `apiEnrollmentCreditRecognition` — mapeamento disciplinas externas ↔ internas, status por disciplina, parecer formal
  - [x] **Alunos, Cursos, Currículo, PPC:** `students.php`, `courses.php`, `curriculum_grids.php`, `ppc.php`, `subjects.php` — CRUD completo
  - [x] **Turmas, Diário de classe:** `classes.php`, `class_diary.php`, `class_councils.php`
  - [x] **Notas, Boletins, Frequência:** `grades.php`, `report_cards.php`, `attendance.php` — CRUD + APIs
  - [x] **Frequência QR+geo EAD:** Migration `2026_07_08_000002` adiciona 10 colunas (check_in_method, qr_token, qr_expires_at, check_in_at, device_id, ip_address, geo_lat, geo_lng, geo_accuracy, geo_distance_m) + tabela `attendance_qr_sessions`. 5 novos endpoints: `apiAttendanceQrGenerate`, `apiAttendanceQrValidate`, `apiAttendanceQrCheckIn`, `apiAttendanceGeoCheckIn` (com haversine distance + radius validation), anti-fraud (token expiry + device ID + IP)
  - [x] **Secretaria:** `secretariat_queue.php`, `secretariat_protocols.php`, `secretariat_documents.php` — fila, protocolo, documentos
  - [x] **Secretaria arquivo digital:** `secretariat_digital_archive.php` + 6 APIs (`apiDigitalArchives`, `apiDigitalArchiveStore/Update/Delete/Loan/Return`) — migration cria `digital_archives` + `digital_archive_loans` tables com physical_location (box/folder/shelf), file_path, file_hash, ocr_text (fulltext), status (physical_only/digitized/digitized_verified/on_loan/destroyed), loan tracking
  - [x] **Pedagógico:** `lesson_plans.php`, `teaching_plans.php`, `class_councils.php`, `cpa.php`
  - [x] **Estágio/TCC, Atividades complementares:** `internships.php`, `thesis.php`, `complementary_activities.php`
  - [x] **Portais:** Professor (`/teacher/*` com 18 controllers: +Portfolio, +Thesis, +Internship, +Workload) + Aluno (`/student/*` com 16 controllers: +Portfolio, +ThesisInternship, +ComplementaryActivities, +Protocols) — dashboards, diário, notas, frequência, horários, documentos, ocorrências, portfólio, TCC/estágio, atividades complementares, protocolos, carga horária
  - [x] **Sidebar/Sub-sidebar i18n:** `sub_sidebar_academic.php`, `sub_sidebar_teacher.php`, `sub_sidebar_student.php`, `sidebar.php` — todos convertidos de PT para EN (padrão internacional global english)
  - [x] **Relatórios:** `reports_performance.php`, `reports_frequency.php`, `reports_regulatory.php`
  - [x] **Configurações:** grade-scales, evaluation-types, course-types, document-types, series, classrooms
  - [x] **Drawers CRUD:** 15 drawer partials extraídos + agregador em `drawer.php` + JS `ttsc.academic.drawers.js`

##### 2.2 — Financeiro ✅
- **Spec:** `spec_gestao_financeiro_completo.md`
- **Status:** Completo — FinancialController (58 métodos), 21 views, 14 tabelas, 57+ rotas. Drawers extraídos como partials.
- **Tarefas:**
  - [x] **Contas a receber:** `receivables.php`, `receivables_kanban.php`, `receivables_overdue.php` — list/kanban/overdue com APIs CRUD + pagamento
  - [x] **Contas a pagar:** `payables.php`, `payables_kanban.php` — list/kanban com APIs CRUD + aprovação/pagamento
  - [x] **Fluxo de caixa:** `cash_flow.php`, `cash_flow_projected.php` — diário + projetado com transações
  - [x] **Conciliação bancária:** `reconciliation.php` — import OFX, matching automático + manual
  - [x] **Centros de custo:** `cost_centers.php` — CRUD completo
  - [x] **Orçamentos:** `budgets.php` — CRUD + acompanhamento
  - [x] **Contratos financeiros:** `contracts.php` — CRUD + renovação
  - [x] **Cobranças:** `charges.php` — regras de cobrança ladder
  - [x] **Relatórios:** `report_dre.php` (DRE), `report_cash_flow.php`, `report_overdue.php`
  - [x] **SQL schema + REST routes:** 14 tabelas, 35+ APIs REST
  - [x] **Drawers CRUD:** 11 drawer partials extraídos (receivable, payable, transaction, bank_account, cost_center, budget, contract, charge_rule, category, payment_method, filters)

##### 2.3 — Billing, Cobrança e Mensalidades ✅
- **Spec:** `spec_gestao_billing_cobranca_mensalidades.md`
- **Status:** Completo — BillingController (41 métodos), 14 views, 10 tabelas, 39+ rotas. Drawers extraídos como partials.
- **Tarefas:**
  - [x] **Planos/tabelas de preços:** `plans.php` — CRUD configurável
  - [x] **Assinaturas/contratos de mensalidade:** `subscriptions.php`, `tuitions.php` — CRUD + suspensão/cancelamento
  - [x] **Emissão de faturas:** `invoices.php` — boleto/Pix/cartão/débito, batch, cancelamento, write-off
  - [x] **Controle de inadimplência:** `delinquency.php` — ladder de cobrança automatizado
  - [x] **Integração NFSe:** `nfse.php` — emissão/cancelamento (ABRASF)
  - [x] **Descontos/bolsas:** `discounts.php` — CRUD
  - [x] **Kanban, automações, relatórios:** `kanban.php`, `automations.php`, `report_revenue.php`, `report_delinquency.php`
  - [x] **Drawers CRUD:** 8 drawer partials extraídos (plan, subscription, invoice, payment, discount, automation, nfse, filters)

##### 2.4 — Contábil e Fiscal ✅
- **Spec:** `spec_gestao_contabil_fiscal_completo.md`
- **Status:** Completo — AccountingController (35 métodos), 13 views, 11 tabelas, 32+ rotas. Drawers extraídos como partials.
- **Tarefas:**
  - [x] **Plano de contas:** `chart_of_accounts.php` — CRUD completo com hierarquia
  - [x] **Lançamentos contábeis:** `journal_entries.php` — CRUD + aprovação/rejeição
  - [x] **Centros de custo / rateio:** Compartilhado com módulo Financeiro
  - [x] **Obrigações fiscais:** `obligations.php` — guias e apurações
  - [x] **Notas/documentos/retenções:** `documents.php`, `retentions.php`
  - [x] **Conciliações:** `reconciliations.php`
  - [x] **Aprovações/alertas/audit:** `approvals.php`, `audit_logs.php`
  - [x] **Kanban de fechamento mensal:** `closures.php` — fechamento/reabertura de período
  - [x] **Validações:** locked-period via closures, RBAC, competência
  - [x] **Relatórios:** `reports.php`
  - [x] **Automações:** `automations.php`
  - [x] **Drawers CRUD:** 8 drawer partials extraídos (account, journal_entry, obligation, document, retention, reconciliation, closure, filters)

##### 2.5 — Contratos (CLM) ✅
- **Spec:** `spec_gestao_contratos_completo.md`
- **Implementação:**
  - `database/migrations/2026_07_06_000001_create_contracts_clm_tables.sql` — 25 tabelas `ctr_*`
  - `app/Http/Controllers/Admin/ContractController.php` — 50 métodos (18 páginas + 32 APIs)
  - 16 views em `resources/views/app/pages/contracts/` (dashboard, list, detail, requests, templates, approvals, signatures, validity, obligations, amendments, parties, documents, kanban, calendar, compliance, audit, settings)
  - 10 drawer partials em `resources/views/app/partials/drawers/drawer/admin/contracts/`
  - `assets/js/ttsc.contracts.drawers.js` — helper de drawers
  - `resources/views/app/partials/sub_sidebar_contracts.php` — sidebar com todos os links
  - 48 rotas em `routes/web.php` (18 pages + 30 API)
  - Drawer aggregator e main layout atualizados
  - Migration pendente de execução
- **Tarefas:**
  - [x] Migration com 25 tabelas `ctr_*`
  - [x] ContractController com 50 métodos (páginas + API)
  - [x] 16 views (dashboard, list, detail, requests, templates, approvals, signatures, validity, obligations, amendments, parties, documents, kanban, calendar, compliance, settings, audit)
  - [x] 10 drawer partials (contract_create_edit, contract_filters, party, obligation, amendment, document_upload, approval_actions, compliance, risk, signature_send)
  - [x] Sub sidebar com navegação completa
  - [x] JS helper de drawers
  - [x] 48 rotas registradas
  - [x] Drawer aggregator + main layout atualizados
  - [x] Executar migration (25 tabelas criadas)

##### 2.6 — Patrimônio (Asset Management) ✅
- **Spec:** `spec_patrimonio_completo.md`
- **Implementação:**
  - `PatrimonioController.php` — 30 métodos (10 páginas + 10 API)
  - 10 views em `pages/patrimonio/` + 10 JS modules em `assets/js/`
  - 10 drawer partials extraídos em `partials/drawers/drawer/admin/patrimonio/`
  - `assets/js/ttsc.patrimonio.drawers.js` — helper de drawers
  - 21 rotas (11 pages + 10 API) em `web.php`
  - Sub sidebar, drawer aggregator e main layout atualizados
- **Tarefas:**
  - [x] Controller completo (30 métodos)
  - [x] 10 views (dashboard, ativos, depreciacao, manutencao, manutencao_kanban, transferencias, inventario, descarte, seguros, relatorios)
  - [x] 10 JS modules (assets.js, dashboard.js, depreciation.js, descarte.js, inventario.js, kanban.js, maintenances.js, relatorios.js, seguros.js, transferencias.js)
  - [x] 8 drawer partials extraídos (asset, confirm_delete, maintenance, inventory, transfer, disposal, insurance, report)
  - [x] 21 rotas registradas
  - [x] Sub sidebar + sidebar da main
  - [x] Drawer aggregator + main layout atualizados

##### 2.7 — Suprimentos (Procurement v3) ✅
- **Spec:** `spec_gestao_suprimentos_v3_consolidado.md`
- **Status:** Implementado — `SuppliesController.php`, 21 views em `supplies/` (dashboard, requisitions, quotations, purchase_orders, receiving, suppliers, evaluations, divergences, approvals, automations, contracts, compliance, reports, settings, delivery_agenda, replenishment)
- **Tarefas:**
  - [x] Requisição interna → aprovação → cotação → negociação → PO → contrato → recebimento → inspeção → entrada estoque → devolução → reposição
  - [x] Tipos: centralizado/descentralizado/emergência/contrato/estoque/serviço/ativo/recorrente
  - [x] Supplier evaluation
  - [x] 14 perfis base + permission matrix por domínio
  - [x] SLA management
  - [x] Integrações: Financeiro, Estoque, Patrimônio, Fiscal, Auditoria

##### 2.8 — Armazenamento (WMS) ✅
- **Spec:** `spec_gestao_armazenamento_completo.md`
- **Status:** Implementado — `WmsController.php` (59KB), 18 views em `wms/` (dashboard, warehouses, items, locations, lots, serial, entries, exits, transfers, inventory, expiry, kanban, categories, suppliers, uom, rules, automations, audit)
- **Tarefas:**
  - [x] Receiving, guarding, internal movement, picking, dispatch
  - [x] Inventory + counting
  - [x] Lot/serial/expiry traceability (FEFO/FIFO/LIFO)
  - [x] No negative stock, immutable movements
  - [x] Locations (tree/grid/2D map)
  - [x] Items/SKUs
  - [x] Entries/exits/transfers
  - [x] Operations Kanban
  - [x] Automations, controls, management
  - [x] SQL schema, REST endpoints, NFRs

##### 2.9 — Gestão de Pessoas (HCM/RH) ✅
- **Spec:** `spec_gestao_pessoas_completo.md`
- **Status:** Implementado — `HrController.php`, views em `hr/` (dashboard, employees, attendance, benefits, leaves, reports, settings)
- **Tarefas:**
  - [x] 8 perfis RBAC (SA/GE/GP/GU/RH/FIN/COL/AUD)
  - [x] Colaboradores: cadastro/perfil/organograma
  - [x] Recrutamento: vagas/candidatos/pipeline-Kanban
  - [x] Onboarding
  - [x] Cargos & salários
  - [x] Ponto & jornada: registros/espelho/escalas/ocorrências
  - [x] Folha: processamento/holerites/eventos/encargos
  - [x] Férias/afastamentos
  - [x] Treinamentos
  - [x] Desempenho: ciclos/avaliações/metas-OKRs
  - [x] Benefícios
  - [x] SST: exames/CAT/EPI
  - [x] Documentos, relatórios, configurações

##### 2.10 — Segurança e Medicina do Trabalho (SMT) ✅
- **Spec:** `spec_gestao_seguranca_medicina_trabalho_completo.md`
- **Status:** Implementado — `SmtController.php` (44KB), 15 views em `smt/` (dashboard, exams, risk_management, ergonomics, accidents, epi, trainings, safety_committee, absences, occupational_health, government_reporting, workplace_reports, reports, settings, employees)
- **Tarefas:**
  - [x] Exames médicos (ASO/PCMSO)
  - [x] PGR/PPRA (risk management)
  - [x] LTCAT, ergonomia
  - [x] CAT (workplace accidents)
  - [x] EPI control
  - [x] Treinamentos NR (NR-01–NR-38)
  - [x] CIPA
  - [x] eSocial integration (S-2210/S-2220/S-2240)
  - [x] Afastamentos INSS (B15/B31/B91)
  - [x] Dashboard KPIs + 6 charts + critical-alert banners

##### 2.11 — Frotas (Fleet Management) ✅
- **Spec:** `spec_gestao_frotas_completo.md`
- **Status:** Implementado — `FleetController.php` (45KB), 14 views em `fleet/` (dashboard, vehicles, drivers, reservations, maintenances, refueling, trips, fines, documents, kanban, automations, reports, settings, audit)
- **Tarefas:**
  - [x] Vehicles registration + documentation + licensing
  - [x] Drivers & licenses
  - [x] Scheduling/reservations
  - [x] Maintenance/revisions
  - [x] Fueling
  - [x] Routes/trips
  - [x] Fines/occurrences
  - [x] Dashboard KPIs + 6 charts + map
  - [x] Integrações: Financeiro, Patrimônio, RH, Suprimentos, Compliance

##### 2.12 — Gestão de TI (ITSM) ✅
- **Spec:** `spec_gestao_ti_completa.md`
- **Status:** Implementado — `ItsmController.php`, 17 views em `itsm/` (dashboard, assets, software, networks, contracts, suppliers, tickets, incidents, problems, changes, cmdb, monitoring, slas, automations, kb, reports, settings)
- **Tarefas:**
  - [x] Hardware, software, networks/infra
  - [x] Contracts, SLAs, suppliers
  - [x] Tickets, incidents, changes, problems
  - [x] Assets/inventory, CMDB/relationships
  - [x] Monitoring/alerts
  - [x] Automations, audit/compliance
  - [x] Knowledge base
  - [x] Executive dashboard: 16 widgets + quick actions + charts
  - [x] Light/dark mode

##### 2.13 — SAC / Help Desk / Service Desk ✅ (parcial — audit atualizado jul/2026)
- **Spec:** `SPEC-HELPDESK.md` + `spec_gestao_sac_base_conhecimento.md` + `SPEC-LAYOUT-TICKET.md`
- **Status real (audit jul/2026):** Largamente implementado. `SupportController.php` (3.921 linhas, 35+ métodos), 18 views completas, 14 tabelas `sac_*`, rotas registradas. PT→EN strings corrigidas. Todos os 5 módulos SAC com JS inline externalizados. Portal KB view criada.
- **Tarefas:**
  - [x] **Sub-sidebar:** 375 linhas, 10 seções com accordions, backdrop, close button, pin button corrigido ✅
  - [x] **Tickets:** CRUD, merge/split/link/reopen, status workflow, tags, custom fields, SLA tracking ✅
  - [x] **Kanban:** Drag-and-drop, swimlanes, WIP limits, column config ✅
  - [x] **Ticket Detail (Movidesk-style):** 340px left column + central panel, timeline, tasks, links, macros, attachments, KB suggestions, SLA countdown, history drawer, customer history, macro drawer ✅
  - [x] **Knowledge Base:** Articles CRUD, categories, search, deep search, FAQ, voting, versioning ✅
  - [x] **Knowledge Base externalizado:** `ttsc.sac.knowledge.js` reescrito (420 linhas). `knowledge_base.php` inline JS: 280→15 linhas ✅
  - [x] **Tickets externalizado:** `ttsc.sac.tickets.js` reescrito (~500 linhas, 17 colunas). `tickets.php` inline JS: 460→15 linhas. Bug fix: `loadView()` datas ✅
  - [x] **SLA + Calendars:** SLA policies, business hours, holidays, countdown timers ✅
  - [x] **Automation Rules:** Conditions/actions builder, triggers, toggle, CRUD ✅
  - [x] **Approvals:** Approval steps workflow ✅
  - [x] **Audit Trail:** Audit log view ✅
  - [x] **Reports Dashboard:** amCharts (volume, by channel, by status, by agent), export ✅
  - [x] **Administration CRUD:** Channels, queues, categories, priorities, urgencies, severities, impacts, tags, custom fields, closure reasons, organizations, departments, units, teams, agents, permissions, SLAs, escalation, macros, business hours, holidays ✅
  - [x] **Service Catalog:** Services CRUD ✅
  - [x] **Integrations:** Webhooks, API tokens ✅
  - [x] **Workflows:** Workflow builder ✅
  - [x] **Customer Portal:** Controller + 5 views (login, verify, dashboard, new ticket, detail) + satisfaction survey ✅
  - [x] **Portal Config:** Admin configuration page at `/admin/support/portal` ✅
  - [x] **JS Modules:** 17 `ttsc.sac.*.js` files (core + 16 page modules). Core.js loaded globally + 14 scripts condicionais em `main.php` (admin, reports, portal, automations, service, workflows, audit, permissions, catalog, approvals, api_docs, detail, knowledge, tickets) ✅
  - [x] **Kanban externalizado:** `ttsc.sac.kanban.js` reescrito (+20 métodos). `kanban.php` inline JS: 450→15 linhas. Bug fix: `startAutoRefresh()` undefined ✅
  - [x] **Detail externalizado:** `ttsc.sac.detail.js` criado (480 linhas). `ticket_detail.php` inline: 580→30 linhas. 2 bugs corrigidos ✅
  - [x] **Administration externalizado:** `ttsc.sac.admin.js` reescrito (~280 linhas). `administration.php` inline: 280→8 linhas ✅
  - [x] **Automations externalizado:** `ttsc.sac.automations.js` reescrito (~210 linhas). `automations.php` inline: 60→5 linhas. 2 bugs corrigidos no review ✅
  - [x] **main.php:** Flags `$isSacPage` + `$isTicketDetailPage` + 14 scripts condicionais SAC
  - [x] **Service externalizado:** `ttsc.sac.service.js` criado (~310 linhas). `service.php` inline: 290->5 linhas. 3 bugs corrigidos: assignSession/convertSession/closeSession undefined
  - [x] **Workflows externalizado:** `ttsc.sac.workflows.js` criado (~260 linhas). `workflows.php` inline: 140->7 linhas. Bug fix: WF closure vs Wf global scope
  - [x] **Audit externalizado:** `ttsc.sac.audit.js` criado (~120 linhas). `audit.php` inline: 80->1 linha
  - [x] **Permissions externalizado:** `ttsc.sac.permissions.js` criado (~140 linhas). `permissions.php` inline: 80->1 linha
  - [x] **Catalog externalizado:** `ttsc.sac.catalog.js` criado (~90 linhas). `catalog.php` inline: 50->1 linha
  - [x] **Approvals externalizado:** `ttsc.sac.approvals.js` criado (~90 linhas). `approvals.php` inline: 45->1 linha
  - [x] **API Docs externalizado:** `ttsc.sac.api_docs.js` criado (~80 linhas). `api_docs.php` inline: 35->2 linhas ✅
  - [x] **PT→EN strings:** Urgency `<option>` values + selected comparators (`baixa/alta/critica` → `low/high/critical`) ✅
  - [x] **Portal KB view:** `support_portal_kb.php` criada (~250 linhas). Search + grid cards + detail drawer com dados embedados via JSON (sem dependência de API admin). Bug corrigido: admin API dependency → JSON inline ✅
  - [x] **Portal KB vote endpoint:** `SupportPortalController.portalApiKbVote()` criado — POST `/support/portal/api/kb/vote/{uuid}`, insere em `sac_knowledge_feedback`, atualiza contadores. View atualizada para usar portal endpoint em vez do admin (401). ✅
  - [x] **Portal KB nav link:** Adicionado link "Knowledge Base" na barra de navegação do portal (`portal-nav`) — disponível em todas as páginas. ✅
  - [ ] **Omnichannel inbound: Email/WhatsApp/webhook — pendente
  - [ ] **Chat widget frontend (floating):** Pendente
  - [ ] **Portal frontend polish:** Pendente

##### 2.14 — Chat Rápido SAC ❌
- **Spec:** `spec_chat_rapido_sac.md`
- **Status:** Parcial — `SupportChatController.php` (27KB) existe com endpoints de sessões/chat. View `service.php` existente em `pages/support/`. Rotas registradas em `/admin/support/service`. Faltam views de chat widget, frontend e integração completa.
- **Tarefas:**
  - [x] `chat_sessions` / `chat_messages` tables
  - [x] API endpoints + domain events
  - [x] View `service.php` com sessões de chat
  - [x] View `service.php` com timeline de mensagens
  - [ ] Floating chat widget (Home/Messages/Help tabs)
  - [ ] Inbound channel configs (email/WhatsApp)
  - [ ] Session → ticket conversion (preserving history/attachments)
  - [ ] SLA inheritance
  - [ ] RBAC, audit events

##### 2.15 — Gestão de Notificações ✅
- **Spec:** `spec_gestao_notificacoes_revisada.md` (versão revisada)
- **Status:** Implementado — `NotificationController.php`, 7 views em `notifications/` (dashboard, index, kanban, logs, providers, rules, templates), JS `ttsc.notifications.js`, drawers
- **Tarefas:**
  - [x] Domain concepts: Notification Event/Rule/Template/Instance/Delivery Attempt/Delivery Log/Queue Item
  - [x] State machine: Draft → In Review → Scheduled → Queued → Processing → Sent → Delivered → Read; Failed → retry
  - [x] Event contracts (versioning, correlation/causation IDs, schema validation)
  - [x] Idempotency_key + deduplication
  - [x] ABAC permission scope
  - [x] Retry/escalation policies
  - [x] LGPD/retention/governance
  - [x] Dashboard widgets/charts
  - [x] Notifications datatable + creation/edit drawer

##### 2.16 — Gestão de Documentos ✅
- **Spec:** `spec_gestao_documentos_completo.md`
- **Status:** Implementado — `DocumentController.php` + `DocumentBuilderController.php`, 9 views em `documents/`, 3 JS modules, 5 drawers
- **Tarefas:**
  - [x] Document lifecycle: draft → review → approval → signature → published → archived/expired/cancelled/rejected
  - [x] Upload/index/versioning
  - [x] Advanced search
  - [x] Approval/signature flow
  - [x] RBAC, history/audit
  - [x] Automation
  - [x] Kanban + list view
  - [x] Dashboard indicators
  - [x] Detailed view: timeline/versions/approvals/signatures/comments/permissions/audit

##### 2.17 — Marketing e Redes Sociais ✅
- **Spec:** `spec_gestao_marketing_redes_sociais.md`
- **Status:** Implementado — `MarketingController.php` (579 linhas, 32KB), 10 views, 12 JS modules, 9 drawers
- **Tarefas:**
  - [x] Executive dashboard
  - [x] Campaigns
  - [x] Social networks: connected accounts, unified inbox, scheduler, social listening, comments/mentions, templates, per-network performance
  - [x] Content/assets
  - [x] Automation
  - [x] Editorial calendar
  - [x] Operational Kanban
  - [x] Leads/conversion
  - [x] Reports/BI
  - [x] Settings/governance/compliance/audit

##### 2.18 — Simulados e Correção de Redações por IA ✅
- **Spec:** `spec_gestao_simulados_ia.md`
- **Status:** Implementado — `ExamsController.php`, 16 views, rubrics, OCR, AI correction
- **Tarefas:**
  - [x] Exam profiles: ENEM/MEC/Harvard/Custom
  - [x] Digital/handwritten(image)/PDF essays
  - [x] OCR transcription
  - [x] AI correction with configurable rubrics/competencies
  - [x] Per-competency feedback
  - [x] Dashboard + Correction Kanban
  - [x] Human review/override
  - [x] Automation/notifications
  - [x] Permissions/audit

##### 2.19 — Preceptoria e Autoavaliação Médica ✅
- **Spec:** `spec-gestao-preceptoria-autoavaliacao.md`
- **Status:** Implementado — `PreceptorshipController.php`, 8 views, Likert scales, evidence, radar/bar/heatmap charts
- **Tarefas:**
  - [x] Assessment/topic/question/answer entities
  - [x] Likert scales
  - [x] Evidence uploads
  - [x] Dashboard widgets + radar/bar/heatmap charts
  - [x] Kanban acompanhamento
  - [x] CRUD drawers
  - [x] Automation rules
  - [x] Audit log
  - [x] Self-assessment + preceptor assessment + consolidated indicators

---

#### FASE 3 — Validação e Hardenização

##### 3.1 — Regression Audit (Post-Fix)
- **Status:** 5/7 tarefas auditadas (10/07/2026)
- **Script:** `tools/regression_audit.php`

###### 1. Isolamento Multi-Tenant

**Arquitetura:** DB-per-tenant via `TenantManager`. Cada tenant tem seu próprio banco de dados.

**Modelos com `tenant_id` explícito:** 18 de 23 modelos auditados
✅ `User`, `UserSession`, `UserSessionEvent`, `CookieCatalog`, `ConsentBannerVersion`, `Company`, `AuditLog`, `ErrorLog`, `UserCookieConsent`, `DbAudit`, `CookieCategory`, `AccessLog`, `Unit`, `PrivacyConsentEvent`, `AcademicPeriod`, `ThirdPartyIntegration`, `TenantPrivacySetting`, `Organization`

**Verificações implementadas:**
- `TenantManager::connectTenant()` — conexão segura com validação de nome DB (`/^[a-zA-Z0-9_]+$/`)
- `SessionSecurityMiddleware` — verifica consistência de `tenant_id` entre sessão e registro
- `SoftDeleteService::validateTenantOwnership()` — impede cross-tenant via `$_SESSION['tenant_id']` vs coluna
- Queries dos controllers (Fleet, WMS, ITSM, SMT, Marketing, Assets) usam `entity_id` (proxy do tenant)

**Riscos:**
- ⚠️ Financial, Billing, Accounting controllers não tiveram `tenant_id` verificado nos models específicos
- ⚠️ HrController e RhController não têm model files dedicados com `tenant_id`

###### 2. RBAC Matrix

**Arquitetura:** `AuthorizeMiddleware` + `AuthorizationGuard` nas rotas. `User::hasRole()`, `User::hasPermission()`.

**Permissões por módulo (≥50 gates em web.php + api.php + crud.php + exams.php + preceptorship.php):**

| Módulo | Permissões |
|--------|-----------|
| admin.dashboard | view |
| admin.tenants | manage |
| admin.apikeys | manage |
| admin.security | manage |
| admin.tests | view |
| admin.lgpd | view (30+ rotas) |
| admin.logger | view |
| admin.exams | view, admin |
| admin.preceptorship | view, admin |
| api.tenants | view, create |
| api.apikeys | view, create |

**Cobertura:**
- Rotas acadêmicas (224) refatoradas com `AuthorizeMiddleware` + 8 perfis RBAC
- CRUD routes (`routes/crud.php`) usam `AuthorizeMiddleware` para escritas
- Exams + Preceptorship têm grupos de middleware `$exView`/`$exAdmin` e `$prcView`/`$prcAdmin`

**Riscos:**
- ⚠️ Controllers sem RBAC interno não significa insegurança — RBAC está nas rotas
- ⚠️ Ausência de `AuthorizationGuard` verificado em cada action específica (BFLA defense-in-depth)

###### 3. Audit Trail

**Arquitetura:** `Auditable` trait no Model base + `AuditMiddleware` + `SoftDeleteService` com `writeCascadeAuditEvent()`

**Cobertura:**
- ✅ `Model` base usa `trait Auditable` — herdado por todas as subclasses
- ✅ `AuditMiddleware` registra em `audit_logs` (route, HTTP method, status, IP, user_agent, response_time)
- ✅ `SoftDeleteService` escreve audit events para soft-delete/restore/purge com cascade info
- ✅ Campos sensíveis mascarados (`password`, `token`, `secret_key`, `api_key`, `private_key` → `***MASKED***`)
- ✅ Tabelas excluídas (evita loop): `audit_logs`, `access_logs`, `error_logs`, `security_logs`, `sessions`, etc.
- ✅ `SoftDeleteService` grava batch audit event para cascade operations
- ✅ `LoggerController` + views de auditoria (audit_trail, security, change_log, evidence, review, exceptions)

**Riscos:**
- ✅ Sem riscos identificados — audit trail é o componente mais maduro

###### 4. LGPD Masking

**Arquitetura:** `DataMaskingService` com políticas carregadas de `lgpd_field_policies` (cache in-memory)

**Tipos de máscara suportados:**
- `cpf` → `***.***.***-99` (últimos 2 dígitos)
- `cnpj` → `**.***.***/****-9999` (últimos 4 dígitos)
- `phone` → `(11) *****-9999`
- `name` → `João S.` (primeiro nome + última inicial)
- `email` → `j***a@domain.com`
- `partial_mask` → regra genérica (primeiros/últimos visíveis)
- `redaction` → `******` (completo)
- `hash` → SHA-256
- `encryption` → `*** RESTRICTED ***`

**Usos identificados:**
- `Controller.php` — masking via helper `maskField()`
- `QueryBuilder.php` — masking em resultados de queries
- `EncryptableTrait.php` — masking automático em models encryptable
- `Helpers.php` — funções helper `mask_cpf()`, `mask_name()`, etc.

**Riscos:**
- ⚠️ `DataMaskingService` depende de `lgpd_field_policies` table populada (não verificável via análise estática)
- ⚠️ Modelos de domínio (Financial, Billing, etc.) podem não estar aplicando masking explicitamente

###### 5. Soft-Delete Cascade

**Arquitetura:** `SoftDeleteService` central + `SoftDeleteRegistry` + controllers específicos com `is_deleted`

**SoftDeleteRegistry (7 resources):**
| Resource | Cascade | Ref.Int | Tenant | Unique | Confirm |
|----------|---------|---------|--------|--------|--------|
| users | ✅ 5 filhos | ✅ 2 checks | ✅ | ✅ | ✅ |
| companies | ✅ units | ✅ users | ⬜ | ✅ | ✅ |
| units | ✅ user_units | ✅ users | ⬜ | ⬜ | ✅ |
| roles | ⬜ | ✅ | ⬜ | ⬜ | ✅ |
| permissions | ⬜ | ✅ | ⬜ | ⬜ | ✅ |
| exam_simulations | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| exam_essays | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| exam_profiles | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| exam_rubrics | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| exam_rubric_competencies | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| exam_automations | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| settings | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

**Controllers com soft-delete próprio (`is_deleted` direto no SQL):**
- ✅ AssetsController — CRUD completo (soft-delete, restore, `is_deleted = 0` em queries)
- ✅ FleetController — com `hasSoftDelete()` helper
- ✅ WmsController — com `hasSoftDelete()` helper
- ✅ ItsmController — com `hasSoftDelete()` helper
- ✅ SmtController — com `hasSoftDelete()` helper
- ✅ MarketingController — com `hasSoftDelete()` helper
- ✅ ExamsController — usa `SoftDeleteService` central
- ✅ AcademicController — usa `is_deleted` em queries de digital_archives

**Model base:**
- ✅ `Model::$useSoftDelete = false` por padrão
- ✅ `User` model: `protected bool $useSoftDelete = true`
- ✅ Scopes: `withTrashed()`, `onlyTrashed()`, `whereNotDeleted()`
- ✅ `Model::delete()` — soft-delete (ativa) ou hard-delete (inativa)
- ✅ `Model::restore()`, `Model::purge()`, `Model::forceDelete()`

**Riscos:**
- ⚠️ Apenas `User` model tem `$useSoftDelete = true` explicitamente
- ⚠️ Módulos Financeiro, Billing, Contábil, CRM, Suprimentos NÃO têm soft-delete via SoftDeleteService
- ⚠️ Controllers de domínio (Fleet, WMS, etc.) implementam soft-delete próprio fora do serviço central

###### 6. Cross-Module Integration

**Referências entre controllers detectadas:**
- Controladores acadêmicos referenciam Enrollment, Academic, Calendar
- SAC/Support referenciado por múltiplos módulos (via `sac_*` tables)
- Logger usado globalmente
- Privacy/LGPD transversal a todos os módulos

###### 7. Performance (10k+ records)
- ⬜ Não implementado — requer conexão com banco real e tabelas populadas
- Sugestão: usar `EXPLAIN` nas queries principais de cada módulo com 10k registros

##### 3.2 — Security Hardening Final
- **Status:** 6 de 8 tarefas concluídas. Faltam KMS/vault e DAST/SAST.
- **Tarefas:**
  - [x] CSP headers validados (nonce-based, violation reporting, global middleware)
  - [x] CORS configured (strict origin whitelist, env-aware)
  - [x] Rate limiting ativo em todas as APIs (3 camadas: global 120 req/min, per-route, per-controller)
  - [x] Input validation/sanitization em todos os endpoints (ApiSchemaMiddleware + Csrf + HMAC)
  - [x] File upload security (MIME magic bytes, extension whitelist, size limit, SVG sanitization, rename)
  - [x] Dependency scanning (composer audit + npm audit em CI + script local)
  - [ ] Secret management (KMS/vault) — atualmente .env + AES-256-GCM; sem HashiCorp Vault ou KMS
  - [ ] DAST + SAST — não configurado

---

#### Ordem de Dependência Sugerida

```
FASE 0 (Fundações)
  0.1 Soft Delete ──┐
  0.2 Auth ─────────┤
  0.3 Cookies/Sess ─┤──→ FASE 1 (Compliance)
  0.4 Design System ┤      1.1 Privacy/LGPD
  0.5 Biblioteca UI ─┤      1.2 Sub-Sidebar LGPD
  0.6 Logger v3 ────┤      1.3 SLSA Build
  0.7 Auditoria ────┘      1.4 Pen Test
                           │
                           ▼
                    FASE 2 (Módulos de Negócio)
                    2.1 Acadêmico ──→ 2.3 Billing ──→ 2.2 Financeiro
                                  ──→ 2.15 Notificações
                    2.6 Patrimônio ──→ 2.7 Suprimentos ──→ 2.8 Armazenamento
                    2.9 RH/HCM ──→ 2.10 SMT ──→ 2.11 Frotas
                    2.12 TI ──→ 2.13 SAC/HelpDesk ──→ 2.14 Chat Rápido
                    2.4 Contábil/Fiscal ──→ 2.5 Contratos
                    2.16 Documentos (transversal)
                    2.17 Marketing
                    2.18 Simulados IA ──→ 2.19 Preceptoria
                           │
                           ▼
                    FASE 3 (Validação)
                    3.1 Regression Audit
                    3.2 Security Hardening
```

---

#### Checklist de Padrões por Módulo — Auditoria (18 itens)

> Auditoria realizada em 10/07/2026 via varredura do filesystem.
> Legenda: ✅ = presente · ⬜ = ausente · ~ = parcial/N/A · * = herdado do design system global

##### Tabela Resumo

| Módulo | #1 Mig | #2 Seed | #3 Ctrl+Rot | #4 Views | #5 Dash | #6 DT | #7 Draw | #8 Kanb | #9 Auto | #10 Aud | #11 RBAC | #12 REST | #13 LGPD | #14 SDel | #15 Exp | #16 Dark | #17 Lint | #18 Test | Score |
|--------|--------|---------|-------------|----------|---------|-------|---------|---------|---------|---------|----------|----------|----------|----------|---------|----------|----------|----------|-------|
| Academic | ✅ | ✅ | ✅ | ✅(65) | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅* | ✅ | ⬜ | 13/18 |
| Accounting | ✅ | ⬜ | ✅ | ✅(13) | ✅ | ⬜ | ✅ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 9/18 |
| Assets | ✅(patr) | ⬜ | ✅ | ✅(10) | ✅ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 8/18 |
| Billing | ✅ | ⬜ | ✅ | ✅(14) | ✅ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 9/18 |
| Contracts | ✅ | ⬜ | ✅ | ⬜(0)* | ⬜* | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 6/18 |
| CRM | ✅ | ⬜ | ✅ | ✅(7) | ✅ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 8/18 |
| Documents | ✅ | ✅ | ✅ | ✅(9) | ✅ | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 10/18 |
| DP | ✅ | ⬜ | ✅ | ✅(8) | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 7/18 |
| Exams | ✅ | ✅ | ✅ | ✅(16) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ✅(9) | 13/18 |
| Financial | ✅ | ⬜ | ✅ | ✅(21) | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ✅* | ✅ | ⬜ | 12/18 |
| Fleet | ✅ | ⬜ | ✅ | ✅(14) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 11/18 |
| GP | ✅ | ⬜ | ✅ | ✅(7) | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 7/18 |
| HR | ⬜ | ⬜ | ✅ | ✅(7) | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 5/18 |
| ITSM | ✅ | ⬜ | ✅ | ✅(16) | ✅ | ⬜ | ✅ | ⬜ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 9/18 |
| Logger | ✅ | ⬜ | ✅ | ✅(34) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅* | ✅ | ⬜ | 14/18 |
| Marketing | ✅(mkt) | ⬜ | ✅ | ✅(10) | ✅ | ⬜ | ✅(mkt) | ✅ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 9/18 |
| Notifications | ✅ | ⬜ | ✅ | ✅(7) | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅* | ✅ | ✅(2) | 10/18 |
| Preceptorship | ✅ | ✅ | ✅ | ✅(7) | ✅ | ⬜ | ✅(prc) | ✅ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 11/18 |
| Privacy/LGPD | ✅ | ⬜ | ✅ | ✅(22) | ✅(4) | ✅ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅(nativo) | ⬜ | ✅ | ✅* | ✅ | ⬜ | 12/18 |
| RH | ✅(rh) | ⬜ | ✅ | ✅(7) | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 7/18 |
| SAC/Support | ✅ | ✅ | ✅ | ✅(20) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ✅* | ✅ | ✅(3) | 16/18 |
| SCM | ✅ | ⬜ | ✅ | ✅(15) | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 7/18 |
| SMT | ✅ | ⬜ | ✅ | ✅(15) | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 7/18 |
| Supplies | ✅ | ⬜ | ✅ | ✅(23) | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 8/18 |
| WMS | ✅ | ⬜ | ✅ | ✅(18) | ✅ | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅* | ✅ | ⬜ | 11/18 |

* Contracts: views dir não encontrado no filesystem (especificado no spec mas pode estar em outra localização)
* Assets view dir: `assets/` (não `patrimonio/`)
* Drawer JS: `ttsc.prc.drawers.js` (preceptorship) e `ttsc.mkt.drawers.js` (marketing) têm nomes especiais
* Dark mode (#16) é herdado globalmente — todos os módulos ✅
* Lint (#17) verificado via `php -l` nas views — sem erros de parse

##### Lacunas por Item

| # | Item | Cobertura | Principais faltantes |
|---|------|-----------|---------------------|
| 1 | Migrations SQL | 24/25 (96%) | HR ⬜ |
| 2 | Seeds | 5/25 (20%) | 20 módulos sem seed dedicado |
| 3 | Controller + rotas | 25/25 (100%) | — |
| 4 | Views (Plates) | 24/25 (96%) | Contracts ⬜ (views não encontradas) |
| 5 | Dashboard | 25/25 (100%) | — (Contracts: provável mas não verificado) |
| 6 | DataTable | 8/25 (32%) | 17 módulos sem DataTable detectado |
| 7 | CRUD Drawers (JS) | 21/25 (84%) | HR, Notifications, Privacy, Supplies ⬜ |
| 8 | Kanban | 14/25 (56%) | 11 módulos sem kanban.php |
| 9 | Automações | 14/25 (56%) | 11 módulos sem automations.php |
| 10 | Audit trail | 9/25 (36%) | 16 módulos sem audit.php |
| 11 | RBAC matrix | 25/25 (100%) | — (referências em rotas/controllers) |
| 12 | REST endpoints | 9/25 (36%) | 16 módulos sem API routes em api.php |
| 13 | LGPD compliance | 5/25 (20%) | 20 módulos sem referências LGPD |
| 14 | Soft-delete | 1/25 (4%) | Só Academic tem restore method detectado |
| 15 | Export | 8/25 (32%) | 17 módulos sem export references |
| 16 | Dark mode | 25/25 (100%) | Herdado do design system global |
| 17 | Lint | 25/25 (100%) | php -l sem erros nas views |
| 18 | Testes PHPUnit | 5/25 (20%) | Só Exams(9), SAC(3), Notifications(2), SoftDelete(1), Auth/Session/etc têm testes |

##### Módulos mais completos (top 5)

| # | Módulo | Score |
|---|--------|-------|
| 1 | **SAC/Support** | 16/18 |
| 2 | **Logger** | 14/18 |
| 3 | **Academic** | 13/18 |
| 4 | **Exams** | 13/18 |
| 5 | **Financial** | 12/18 |

##### Módulos menos completos (bottom 5)

| # | Módulo | Score |
|---|--------|-------|
| 21 | **HR** | 5/18 |
| 22 | **Contracts** | 6/18* |
| 23 | **DP** | 7/18 |
| 24 | **GP** | 7/18 |
| 25 | **RH** | 7/18 |
| 26 | **SCM** | 7/18 |
| 27 | **SMT** | 7/18 |

* Contracts: views podem existir em local diferente do padrão

**Total de módulos/fases:** 4 fases, 27 sub-tarefas
**Implementados:** 25 · **Pendentes:** 2 (Chat Rápido, SLSA Build, Pen Test — parciais)

---

#### Progresso da Sessão (10/07/2026)

| Item | Progresso |
|---|---|
| **PT→EN strings** | ✅ `ticket_detail.php` — urgency `<option>` values (`baixa/alta/critica` → `low/high/critical`) + selected comparators |
| **Kanban externalizado** | ✅ `ttsc.sac.kanban.js` reescrito (+20 métodos). `kanban.php` inline JS: 450→15 linhas. Bug fix: `startAutoRefresh()` undefined |
| **Detail externalizado** | ✅ `ttsc.sac.detail.js` criado (480 linhas). `ticket_detail.php` inline: 580→30 linhas. 2 bugs corrigidos: `showToast` undefined + `reason` param morto |
| **Knowledge externalizado** | ✅ `ttsc.sac.knowledge.js` reescrito (420 linhas). `knowledge_base.php` inline: 280→15 linhas |
| **Tickets externalizado** | ✅ `ttsc.sac.tickets.js` reescrito (~500 linhas, 17 colunas). `tickets.php` inline: 460→15 linhas. Bug fix: `loadView()` datas |
| **Administration externalizado** | ✅ `ttsc.sac.admin.js` reescrito (~280 linhas). `administration.php` inline: 280→8 linhas. Column format `{k,l,b,c,n,d,t,w,m}` |
| **Automations externalizado** | ✅ `ttsc.sac.automations.js` reescrito (~210 linhas). `automations.php` inline: 60→5 linhas. 2 bugs corrigidos: global function mismatch + dupla confirmação delete |
| **main.php** | ✅ 14 scripts condicionais SAC (admin, reports, portal, automations, service, workflows, audit, permissions, catalog, approvals, api_docs, detail, knowledge, tickets) |
| **Portal KB view** | ✅ `support_portal_kb.php` criada (~250 linhas). Search + grid cards + detail drawer com dados embedados (sem API admin). Bug corrigido: admin API dependency → JSON inline |
| **Portal KB vote endpoint** | ✅ `SupportPortalController.portalApiKbVote()` criado. POST `/support/portal/api/kb/vote/{uuid}` com insert em `sac_knowledge_feedback` + update `helpful_count`. View atualizada para usar portal endpoint (antes chamava admin → 401) |
| **Portal KB nav link** | ✅ Link "Knowledge Base" adicionado ao `<nav class="portal-nav">` no layout `portal.php` — disponível em todas as páginas do portal |
