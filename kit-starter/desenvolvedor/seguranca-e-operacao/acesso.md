# Acesso (identidade, autenticação, sessão e autorização)

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Segurança e operação
- Domínio: plataforma (banco master), instância separada do módulo das entidades ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2.1)
- Status: detalhado; especificação da v1 absorvida integralmente (seção 13), com as correções da v2 e as decisões por padrão (seções 1 a 12)
- Fonte da v1: [spec_gestao_autenticacao_completo.md](../../../docs/v2/anexo-v1/spec_gestao_autenticacao_completo.md) (1001 linhas); [spec_gestao_cookies_sessions.md](../../../docs/v2/anexo-v1/spec_gestao_cookies_sessions.md) (474 linhas)

## 1. Regra de leitura
As seções 1 a 12 prevalecem sobre a seção 13. A seção 13 é o texto integral da v1, sem corte, para que nenhum detalhe se perca. Quando a seção 13 disser algo diferente das seções 1 a 12, vale o que está nas seções 1 a 12.

## 2. Objetivo e escopo
Gerir contas, vínculos, papéis, sessões e tokens de toda a plataforma: conta global única, login no domínio de autenticação, RBAC com contexto e contas de plataforma.

## 3. Telas (índice da v1)
**spec_gestao_autenticacao_completo.md**

- 1. Document Purpose
- 2. System Scope
- 3. Platform Standards
  - 3.1 Language standard
  - 3.2 Technology constraints
  - 3.3 Identifier standard
  - 3.4 Allowed PHP built-ins
- 4. Architectural Model
  - 4.1 Multi-entity
  - 4.2 Multi-unit
  - 4.3 Multi-user
  - 4.4 Context-driven access
  - 4.5 Identity separation
  - 4.6 Session isolation
- 5. User Portals
  - 5.1 Administrative portal
  - 5.2 Teacher portal
  - 5.3 Student portal
  - 5.4 Parent portal
  - 5.5 Third-party portal
- 6. Context Rules
  - 6.1 Membership as the source of truth
  - 6.2 Active session context
  - 6.3 Context switching
  - 6.4 Default context resolution
  - 6.5 Selector precedence
- 7. Authentication Flows
  - 7.1 Login flow
  - 7.2 Logout flow
  - 7.3 Password recovery flow
  - 7.4 MFA flow
  - 7.5 Invite flow
- 8. Security Requirements
  - 8.1 Password policy
  - 8.2 Password hashing policy
  - 8.3 Session protection
  - 8.4 Rate limiting
  - 8.5 CSRF and cookies
  - 8.6 CORS policy
  - 8.7 Auditability
- 9. Token and Session Model
  - 9.1 Access token
  - 9.2 Refresh token
  - 9.3 Session record
  - 9.4 Token lifecycle
  - 9.5 Token claims
  - 9.6 Refresh rotation policy
- 10. Authorization Model
  - 10.1 RBAC
  - 10.2 Permission scope
  - 10.3 Sample permissions
  - 10.4 Evaluation order
- 11. MFA Requirements
  - 11.1 Supported methods
  - 11.2 MFA enforcement
  - 11.3 MFA recovery
  - 11.4 Backup codes
- 12. User Lifecycle
  - 12.1 Registration methods
  - 12.2 User profile
  - 12.3 Status lifecycle
  - 12.4 Membership lifecycle
- 13. Data Model
  - 13.1 Core tables
  - 13.2 Mandatory fields pattern
  - 13.3 Key relationships
- 14. Database Rules
  - 14.1 UUID strategy
  - 14.2 Soft delete
  - 14.3 Indexing
  - 14.4 Tenant safety
- 15. API Specification
  - 15.1 Public routes
  - 15.2 Administrative routes
  - 15.3 Standard API response
  - 15.4 Error handling
  - 15.5 API headers
  - 15.6 API contracts
- 16. Frontend Fetch Rules
  - 16.1 Request behavior
  - 16.2 Token storage
  - 16.3 Standard fetch flow
- 17. UI Requirements
  - 17.1 Public pages
  - 17.2 Administrative pages
  - 17.3 Portal pages
- 18. Controls Matrix
  - 18.1 Datatable controls
  - 18.2 Widget controls
  - 18.3 Chart controls
  - 18.4 Drawer controls
  - 18.5 Kanban controls
- 19. Dashboard Requirements
- 20. Automation Requirements
  - 20.1 Authentication automations
  - 20.2 Operational automations
  - 20.3 Governance automations
- 21. Compliance and Privacy
- 22. Non-Functional Requirements
- 23. Acceptance Criteria
- 24. Implementation Priority
  - Phase 1
  - Phase 2
  - Phase 3
  - Phase 4
- 25. Database Entities Appendix
  - 25.1 users
  - 25.2 entities
  - 25.3 units
  - 25.4 memberships
  - 25.5 roles
  - 25.6 permissions
  - 25.7 sessions
  - 25.8 refresh_tokens
  - 25.9 login_attempts
  - 25.10 password_resets
  - 25.11 mfa_factors
  - 25.12 mfa_backup_codes
  - 25.13 audit_logs
  - 25.14 device_trusts
- 26. Final Definition

**spec_gestao_cookies_sessions.md**

- Visão geral
- Objetivos do módulo
- Escopo funcional
  - Entidades principais
  - Perfis de uso
- Requisitos de negócio
- Regras de segurança
- Páginas do módulo
  - 1. Dashboard de sessões
  - 2. Sessões
  - 3. Políticas de cookies
  - 4. Consentimentos
  - 5. Regras e automações
  - 6. Auditoria
- Widgets obrigatórios
- Charts obrigatórios
- Kanban operacional
  - Colunas
  - Cards
  - Ações no card
- Controles gerais
- Ações em lote
- Fluxos principais
  - Login e criação de sessão
  - Revogação de sessão
  - Tratamento de risco
- Automações
- Integrações
- Requisitos de API
  - Endpoints principais
- Modelo de dados mínimo
  - Session
  - CookiePolicy
  - ConsentRecord
- UX/UI
- Validações
- Logs e auditoria
- Permissões
- Critérios de aceite
- Entregáveis esperados
- Observações técnicas

## 4. Correções da v2 que prevalecem
- **O [06](../../../docs/v2/06-identidade-acesso.md) prevalece em tudo** que as especificações da v1 duplicam ([19](../../../docs/v2/19-regras-modulos-3.md), seção 2): tipos de identidade, autenticação, senhas, recuperação de conta, limites de tentativa, sessão, tokens de API, RBAC com contexto, contas de plataforma (break-glass) e conta global com vínculos (seção 12). A v1 fica só com o que é específico de tela.
- **Cookies e sessões** ficam no [06](../../../docs/v2/06-identidade-acesso.md); a especificação de cookies da v1 é aproveitada só no que não contradiz o 06.
- **Conta global por e-mail verificado** (D-21) e **token só com o contexto ativo** (D-20) ([06](../../../docs/v2/06-identidade-acesso.md), seção 12).
- **Login só no domínio de autenticação**, com OIDC e PKCE (D-22, [23](../../../docs/v2/23-dominios-provisionamento-ciclo-de-vida.md), seção 2).
- **Papéis e níveis** conforme o [78](../../../docs/v2/78-permissoes-e-papeis.md); criação de entidade e unidade só por `platform.developer` (L-02).
- **Contas de plataforma:** no máximo 5 ativas, passkey obrigatória, alerta em tempo real a cada uso; break-glass com credencial offline em dois cofres ([06](../../../docs/v2/06-identidade-acesso.md), seção 10).

## 5. Decisões por padrão aplicadas
- Nenhuma decisão nova: regras do [06](../../../docs/v2/06-identidade-acesso.md) e do [78](../../../docs/v2/78-permissoes-e-papeis.md).

## 6. Permissões e papéis
- `platform.security` (papel **Segurança** do [22](../../../docs/v2/22-crm-canais-e-papeis.md), seção 5): investigar, bloquear conta; não concede permissão a si mesmo.
- `platform.manager` e `platform.developer`: conceder papéis conforme o nível ([78](../../../docs/v2/78-permissoes-e-papeis.md), seção 2.1).
- Toda concessão e revogação com justificativa para níveis 3 e acima; revisão trimestral.

## 7. Dados
- Contas e vínculos no master; dados civis no banco de identidade da entidade (D-19). Modelos da v1 (seção 13) só onde não contradizem o [06](../../../docs/v2/06-identidade-acesso.md).

## 8. Integrações
- E-mail transacional da plataforma para verificação e recuperação (D-04, [16](../../../docs/v2/16-integracoes-externas.md), seção 2).
- Captcha após tentativas ([06](../../../docs/v2/06-identidade-acesso.md), seção 6).

## 9. Exportação, auditoria e privacidade
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Auditoria conforme [29](../../../docs/v2/29-auditoria.md); dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md).
- Login, sessão e vínculos registrados na auditoria do master ([29](../../../docs/v2/29-auditoria.md), seção 3).

## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
- Nenhuma além das do [06](../../../docs/v2/06-identidade-acesso.md) e do [45](../../../docs/v2/45-pendencias-consolidadas.md).

## 13. Conteúdo integral da v1 (absorvido)

### Fonte: spec_gestao_autenticacao_completo.md

#### AUTH MODULE SPECIFICATION v2

- Language Standard: Global English
- Architecture: Multi-entity | Multi-unit | Multi-user
- Stack: PHP 8 pure, fetch + API, no external libraries, Supabase template

---

##### 1. Document Purpose

This document defines the complete technical and functional specification for the authentication and access control module of the SaaS platform.

The module must support secure identity management, authentication, session control, authorization, auditability, and compliance-ready lifecycle management in a multi-entity, multi-unit, multi-user environment.

---

##### 2. System Scope

The authentication module is responsible for:

- User registration and invitation flows.
- Login and logout.
- Password recovery and password reset.
- Session management.
- Token issuance and validation.
- Multi-entity and multi-unit context resolution.
- Role-based and permission-based access control.
- Portal routing after authentication.
- Audit logs for all security-sensitive operations.
- Administrative controls for identity governance.

The module must not contain business-domain logic beyond identity, membership, and access control.

---

##### 3. Platform Standards

###### 3.1 Language standard

All namespaces, functions, classes, methods, variables, folders, routes, pages, table names, columns, and string identifiers must use English only.

Database names and route slugs must use snake_case, while PHP class names must use PascalCase.

###### 3.2 Technology constraints

Implementation must use:

- PHP 8.x.
- Native PHP extensions only.
- Fetch for all browser requests.
- API-first architecture.
- Supabase template conventions.
- No external libraries or Composer dependencies unless explicitly approved.

###### 3.3 Identifier standard

Every table should support:

- id: numeric internal primary key.
- uuid: global internal identifier.
- code: external/public identifier.

id must never be exposed in URLs or public-facing identifiers.

###### 3.4 Allowed PHP built-ins

The implementation may use:

- password_hash and password_verify.
- random_bytes.
- hash_hmac.
- hash_equals.
- openssl or sodium when available.
- PDO.
- session_* functions only if session-based support is explicitly enabled.

---

##### 4. Architectural Model

###### 4.1 Multi-entity

Each entity is isolated logically and operationally. A user can belong to more than one entity, but access must always be resolved through an active entity context.

###### 4.2 Multi-unit

Each entity may contain multiple units such as headquarters, branches, campuses, schools, or departments. A user may belong to one or more units, but unit access must always be explicit.

###### 4.3 Multi-user

The system must support many users per entity and unit. One identity may have different memberships, roles, and portal access across different contexts.

###### 4.4 Context-driven access

Every authenticated session must always know:

- Current entity.
- Current unit.
- Current portal.
- Current role.
- Current permission scope.
- Current membership reference.

###### 4.5 Identity separation

Identity data must be separated from business data. Authentication, authorization, membership, and audit must remain in the security layer.

###### 4.6 Session isolation

A session created in one entity or unit must not be valid in another entity or unit unless the active context is explicitly changed through a controlled endpoint and revalidated.

---

##### 5. User Portals

The system must support the following login destinations:

###### 5.1 Administrative portal

Used by:

- Super administrators.
- Entity administrators.
- Unit administrators.
- Managers.
- Support operators.
- Auditors.

###### 5.2 Teacher portal

Used by:

- Teachers.
- Coordinators.
- Academic assistants.
- Pedagogical staff.

###### 5.3 Student portal

Used by:

- Students.
- Apprentices.
- Enrolled learners.

###### 5.4 Parent portal

Used by:

- Parents.
- Guardians.
- Responsible parties.
- Authorized family contacts.

###### 5.5 Third-party portal

Used by:

- Suppliers.
- Transport companies.
- Legal offices.
- Notary offices.
- Service providers.
- Other external partners.

---

##### 6. Context Rules

###### 6.1 Membership as the source of truth

A membership defines where a user can operate. It must bind:

- user
- entity
- unit
- portal
- role

###### 6.2 Active session context

A session must bind to exactly one active context at a time:

- active entity.
- active unit.
- active portal.
- active role.
- active membership.

###### 6.3 Context switching

If a user has multiple valid memberships, the system must allow entity and unit switching through dedicated context-selection endpoints. Every switch must be audited.

###### 6.4 Default context resolution

If only one valid context exists, the system may auto-select it. If multiple valid contexts exist, the user must be prompted to choose.

###### 6.5 Selector precedence

Context resolution order must be:

1. Explicit request parameter.
2. Previously persisted last active context.
3. Default membership.
4. First valid membership by platform rule.

---

##### 7. Authentication Flows

###### 7.1 Login flow

1. User selects or is directed to a portal.
2. User submits credentials.
3. System validates identity, account status, portal eligibility, entity membership, unit membership, and MFA requirements.
4. System resolves valid contexts.
5. System issues session and tokens.
6. System logs the event.
7. System routes the user to the correct dashboard.

###### 7.2 Logout flow

1. User requests logout.
2. Session is revoked.
3. Refresh token is invalidated.
4. Audit entry is created.
5. Client clears state.

###### 7.3 Password recovery flow

1. User requests password recovery.
2. System rate-limits the request.
3. System creates a reset token.
4. Reset token is stored hashed.
5. Reset link is sent.
6. User sets a new password.
7. Old sessions are invalidated.

###### 7.4 MFA flow

1. User enrolls a factor.
2. System verifies initial proof.
3. System stores factor data securely.
4. On challenge, user submits code.
5. System validates and logs the result.

###### 7.5 Invite flow

1. Admin creates invitation.
2. Invitation is linked to entity, unit, portal, and role scope.
3. System sends invitation link.
4. User accepts invitation.
5. User sets password and optionally enrolls MFA.
6. Membership becomes active.

---

##### 8. Security Requirements

###### 8.1 Password policy

Passwords must:

- Have minimum length.
- Reject common passwords.
- Reject recent reuse.
- Be hashed with Argon2id.
- Never be logged or exposed in errors.

###### 8.2 Password hashing policy

The implementation must use password_hash with PASSWORD_ARGON2ID. The spec must allow environment-tuned cost parameters, but the chosen values must be documented in configuration.

###### 8.3 Session protection

The system must:

- Regenerate session after login.
- Invalidate sessions on logout.
- Revoke old tokens after refresh rotation.
- Prevent session fixation.
- Enforce idle and absolute timeout policies.

###### 8.4 Rate limiting

The system must throttle:

- Login attempts.
- Password reset requests.
- MFA attempts.
- Refresh token requests.
- Invitation resend requests.

###### 8.5 CSRF and cookies

If browser cookies are used for auth, they must be HttpOnly, Secure, and SameSite-restricted. State-changing endpoints must use CSRF protection.

###### 8.6 CORS policy

The API must only allow explicitly configured origins. Credentials may only be allowed when the origin is trusted and the request is authenticated by the chosen session model.

###### 8.7 Auditability

Every sensitive action must be logged:

- Login.
- Logout.
- Failed login.
- Password change.
- Password reset.
- MFA enrollment.
- Role change.
- Unit change.
- Entity change.
- Session revocation.
- Permission change.
- Context switch.

---

##### 9. Token and Session Model

###### 9.1 Access token

Use a short-lived access token with only safe claims. It must not expose sensitive personal data.

###### 9.2 Refresh token

Use a rotating refresh token with server-side revocation support. Store only hashed refresh tokens in the database.

###### 9.3 Session record

A session must include:

- user_uuid
- membership_uuid
- entity_uuid
- unit_uuid
- portal_code
- role_code
- device_fingerprint
- ip_address
- user_agent
- created_at
- last_seen_at
- expires_at
- revoked_at

###### 9.4 Token lifecycle

- Access token: short-lived.
- Refresh token: longer-lived, rotated on use.
- Reuse detection: mandatory.
- Revocation: mandatory.

###### 9.5 Token claims

Minimum safe claims:

- sub: user_uuid.
- mem: membership_uuid.
- ent: entity_uuid.
- unit: unit_uuid.
- por: portal_code.
- rol: role_code.
- iat: issued at.
- exp: expiry.
- jti: unique token id.

Sensitive claims must not be included.

###### 9.6 Refresh rotation policy

A refresh token must be single-use. When exchanged, the previous token must be invalidated and a new token issued. Reuse of a rotated token must revoke the entire session family.

---

##### 10. Authorization Model

###### 10.1 RBAC

Authorization must be role-based and permission-based. Deny-by-default is mandatory.

###### 10.2 Permission scope

Permissions may be scoped by:

- Portal.
- Module.
- Action.
- Entity.
- Unit.
- Record ownership.

###### 10.3 Sample permissions

- user_view
- user_create
- user_edit
- user_delete
- user_lock
- role_assign
- session_revoke
- audit_view
- login_force_mfa
- membership_manage

###### 10.4 Evaluation order

Authorization must be evaluated in this order:

1. User status.
2. Membership status.
3. Portal eligibility.
4. Entity scope.
5. Unit scope.
6. Role grants.
7. Permission grants.
8. Record-level constraint.

---

##### 11. MFA Requirements

###### 11.1 Supported methods

Initial supported methods:

- TOTP.
- Backup codes.
- Optional email OTP for recovery only, if policy allows.

###### 11.2 MFA enforcement

MFA is required for:

- Administrators.
- Sensitive actions.
- High-risk logins.
- New device logins.
- Suspicious IP or location changes.

###### 11.3 MFA recovery

MFA recovery must be auditable and stronger than normal login. Recovery must not weaken security controls.

###### 11.4 Backup codes

Backup codes must be generated securely, shown once, stored hashed, and marked as consumed when used.

---

##### 12. User Lifecycle

###### 12.1 Registration methods

- Manual creation.
- Invitation-based registration.
- Self-registration when allowed.
- External identity import.

###### 12.2 User profile

A user profile may contain:

- Personal data.
- Contact data.
- Document data.
- Authentication data.
- Portal eligibility.
- Entity memberships.
- Unit memberships.
- Device list.
- Session history.

###### 12.3 Status lifecycle

Supported statuses:

- Active.
- Pending.
- Invited.
- Suspended.
- Locked.
- Deleted.
- Archived.

###### 12.4 Membership lifecycle

Supported actions:

- Assign entity.
- Assign unit.
- Assign portal.
- Assign role.
- Revoke membership.
- Transfer membership.
- Clone access profile.

---

##### 13. Data Model

###### 13.1 Core tables

- users
- roles
- permissions
- user_roles
- role_permissions
- entities
- units
- memberships
- portals
- sessions
- refresh_tokens
- login_attempts
- password_resets
- mfa_factors
- mfa_backup_codes
- invitations
- access_requests
- audit_logs
- security_events
- device_trusts

###### 13.2 Mandatory fields pattern

Each table should generally include:

- id
- uuid
- code
- created_at
- updated_at
- deleted_at when applicable.

###### 13.3 Key relationships

- memberships links users to entities, units, portals, and roles.
- sessions reference active memberships.
- refresh_tokens reference sessions.
- audit_logs reference actor and target contexts.
- invitations create future memberships.

---

##### 14. Database Rules

###### 14.1 UUID strategy

UUID must be the global cross-context identifier for APIs, logs, and external references.

###### 14.2 Soft delete

Deleted rows must use deleted_at instead of physical deletion when the record must remain auditable.

###### 14.3 Indexing

Indexes must exist for:

- user_uuid.
- entity_uuid.
- unit_uuid.
- portal_code.
- role_code.
- session_token_hash.
- refresh_token_hash.
- created_at.
- status fields.

###### 14.4 Tenant safety

All entity-scoped and unit-scoped queries must include explicit scope filters. Cross-tenant access must never rely on client-side filtering.

---

##### 15. API Specification

###### 15.1 Public routes

- POST /api/v1/auth/login
- POST /api/v1/auth/logout
- POST /api/v1/auth/refresh
- POST /api/v1/auth/forgot_password
- POST /api/v1/auth/reset_password
- POST /api/v1/auth/mfa/enroll
- POST /api/v1/auth/mfa/challenge
- GET /api/v1/auth/session
- GET /api/v1/auth/me
- POST /api/v1/auth/select_entity
- POST /api/v1/auth/select_unit
- POST /api/v1/auth/select_portal

###### 15.2 Administrative routes

- GET /api/v1/admin/users
- POST /api/v1/admin/users
- PUT /api/v1/admin/users/{uuid}
- GET /api/v1/admin/sessions
- POST /api/v1/admin/sessions/revoke
- GET /api/v1/admin/audit_logs
- GET /api/v1/admin/security_events
- GET /api/v1/admin/memberships
- POST /api/v1/admin/roles
- POST /api/v1/admin/permissions

###### 15.3 Standard API response

All responses must include:

- success
- message
- data
- errors
- meta
- request_id

###### 15.4 Error handling

Use standard HTTP codes:

- 400 for validation failures.
- 401 for unauthenticated requests.
- 403 for forbidden requests.
- 404 for not found.
- 409 for conflicts.
- 422 for semantic validation failures.
- 429 for rate limits.
- 500 for unexpected errors.

###### 15.5 API headers

Requests and responses must support:

- Authorization.
- Content-Type.
- Accept.
- X-Request-Id.
- X-CSRF-Token when cookie session is enabled.

###### 15.6 API contracts

The spec must define request and response payloads for login, refresh, logout, forgot password, reset password, MFA challenge, entity selection, unit selection, and portal selection.

---

##### 16. Frontend Fetch Rules

###### 16.1 Request behavior

All frontend authentication requests must use fetch.

###### 16.2 Token storage

If tokens are returned to the browser, the access token must be kept in memory only. Refresh token handling must follow the selected security model and must not expose tokens in unsafe storage unless explicitly accepted by the security policy.

###### 16.3 Standard fetch flow

Each request must:

- Send required headers.
- Handle JSON serialization.
- Read JSON responses.
- React to 401 and 429 consistently.
- Refresh session when needed.

---

##### 17. UI Requirements

###### 17.1 Public pages

- login
- forgot_password
- reset_password
- mfa_challenge
- select_entity
- select_unit
- select_portal
- logout

###### 17.2 Administrative pages

- dashboard
- users
- users_create
- users_edit
- users_detail
- roles
- permissions
- memberships
- sessions
- devices
- login_attempts
- password_policies
- mfa_policies
- access_requests
- invitations
- audit_logs
- security_events
- settings

###### 17.3 Portal pages

- home_dashboard
- profile
- password_change
- session_history
- notifications
- help_center

---

##### 18. Controls Matrix

###### 18.1 Datatable controls

- Search.
- Filter.
- Sort.
- Pagination.
- Column visibility.
- CSV export.
- Bulk select.
- Bulk action.
- Row detail.
- Inline actions.

###### 18.2 Widget controls

- Refresh.
- Time range.
- Drilldown.
- Export.
- Pin.
- Hide.
- Compare.

###### 18.3 Chart controls

- Date range.
- Group by.
- Filter by portal.
- Filter by entity.
- Filter by unit.
- Download image.
- Download data.
- Toggle series.

###### 18.4 Drawer controls

- Open.
- Close.
- Save.
- Validate.
- Reset.
- Duplicate.
- Archive.

###### 18.5 Kanban controls

- Drag and drop.
- Assign user.
- Change state.
- Add note.
- Set priority.
- Resolve.
- Reopen.

---

##### 19. Dashboard Requirements

The dashboard must provide:

- Recent logins.
- Recent password changes.
- Active sessions.
- Pending invitations.
- Access requests.
- Locked accounts.
- MFA enrollment status.
- Audit events.
- Role assignments.
- Unit memberships.

It must also show:

- Total users.
- Active users.
- Suspended users.
- New registrations.
- Failed logins.
- Password reset requests.
- Active devices.
- Sessions by portal.
- Security alerts.
- Pending approvals.

Charts must include:

- Login volume by day.
- Failed login trend.
- Portal access distribution.
- Users by role.
- Users by unit.
- MFA adoption.
- Session activity over time.
- Access request status.

---

##### 20. Automation Requirements

###### 20.1 Authentication automations

- Automatic session expiry.
- Automatic token rotation.
- Automatic logout after inactivity.
- Automatic lock after brute-force threshold.
- Automatic password expiration warning.
- Automatic MFA challenge for risky events.
- Automatic role sync from membership changes.

###### 20.2 Operational automations

- Send email invitation.
- Send password reset email.
- Send approval request.
- Send security alert.
- Send login confirmation.
- Send suspicious login warning.
- Generate audit report.
- Generate access report.

###### 20.3 Governance automations

- Disable unused accounts.
- Flag stale accounts.
- Detect duplicate identities.
- Detect orphan memberships.
- Detect conflicting role assignments.
- Detect invalid portal access.

---

##### 21. Compliance and Privacy

The module must support:

- Least privilege.
- Access traceability.
- Data minimization.
- Session expiration.
- Identity lifecycle control.
- Export of security logs when needed.
- Privacy-safe handling of personal data.
- Retention and deletion policies.
- Data export on request where legally required.

---

##### 22. Non-Functional Requirements

- High performance under concurrent logins.
- Clear separation between auth and business modules.
- Secure by default.
- Maintainable code structure.
- Extensible for future MFA methods.
- Compatible with multi-database deployment.
- Ready for enterprise audit and security review.
- Compatible with Supabase template mapping.
- Compatible with pure PHP API delivery.

---

##### 23. Acceptance Criteria

The module is complete when:

- All portals authenticate correctly.
- Multi-entity and multi-unit selection works.
- Roles and permissions are enforced correctly.
- Sessions are isolated and revocable.
- Audit logs capture all security events.
- CRUD drawers are available for operational management.
- Widgets, charts, and Kanban boards are implemented.
- Security policies are enforced.
- Recovery and fallback flows work.
- All control pages are present and functional.
- API contracts are defined and implemented.
- Database schema is defined and implemented.
- Frontend fetch integration is defined.

---

##### 24. Implementation Priority

###### Phase 1

- Login.
- Logout.
- Session management.
- Password recovery.
- Entity and unit resolution.
- Role-based access.
- Core database schema.
- Core API contracts.

###### Phase 2

- MFA.
- Invitations.
- User management.
- Audit logs.
- Permissions management.
- Context switching.

###### Phase 3

- Widgets.
- Charts.
- CRUD drawers.
- Kanban boards.
- Automations.
- Admin dashboards.

###### Phase 4

- Advanced governance.
- Risk scoring.
- Device trust.
- Security analytics.
- Full operational hardening.

---

##### 25. Database Entities Appendix

###### 25.1 users

Stores identity and authentication profile.

###### 25.2 entities

Stores organization-level tenants.

###### 25.3 units

Stores units belonging to entities.

###### 25.4 memberships

Stores the access relationship between user, entity, unit, portal, and role.

###### 25.5 roles

Stores role definitions.

###### 25.6 permissions

Stores permission definitions.

###### 25.7 sessions

Stores active and revoked sessions.

###### 25.8 refresh_tokens

Stores hashed refresh token records.

###### 25.9 login_attempts

Stores failed and successful authentication attempts.

###### 25.10 password_resets

Stores password recovery flow records.

###### 25.11 mfa_factors

Stores MFA factor metadata.

###### 25.12 mfa_backup_codes

Stores hashed backup codes.

###### 25.13 audit_logs

Stores security and administrative events.

###### 25.14 device_trusts

Stores trusted device metadata.

---

##### 26. Final Definition

This specification is complete enough to serve as the master implementation document for the authentication module under the stated architecture and technology constraints.

### Fonte: spec_gestao_cookies_sessions.md

#### Spec — Cookies e Sessions

- Language Standard: Global English
##### Visão geral
Este documento define a especificação funcional e técnica do módulo **Cookies e Sessions** para uma plataforma SaaS enterprise multi-entity e multi-unit. O objetivo é centralizar o gerenciamento de sessões autenticadas, políticas de cookies, auditoria de acesso, automações de expiração e controles de segurança, com interfaces completas para operação, governança e conformidade LGPD.

##### Objetivos do módulo
- Gerenciar sessões de usuários, dispositivos e tokens de acesso.
- Controlar políticas de cookies por domínio, ambiente, unidade e entidade.
- Permitir auditoria detalhada de login, logout, renovação, revogação e anomalias.
- Oferecer dashboards com métricas, gráficos e widgets operacionais.
- Disponibilizar CRUD completo com drawers para criação, edição, visualização e revisão.
- Suportar Kanban operacional para triagem e tratamento de sessões suspeitas.
- Automatizar ações de expiração, revogação, limpeza e notificação.
- Garantir conformidade com segurança, rastreabilidade e LGPD.

##### Escopo funcional
###### Entidades principais
- CookiePolicy.
- Session.
- SessionDevice.
- SessionEvent.
- SessionRule.
- SessionAutomation.
- ConsentRecord.
- SecurityIncident.

###### Perfis de uso
- Administrador global.
- Administrador de entidade.
- Administrador de unidade.
- Time de segurança.
- Auditor.
- Suporte técnico.
- Usuário final autenticado.

##### Requisitos de negócio
- O sistema deve permitir configuração de políticas de cookies por ambiente, domínio e unidade.
- O sistema deve registrar todas as sessões autenticadas com metadados de dispositivo, IP, geolocalização, user agent e contexto de login.
- O sistema deve permitir revogação manual e automática de sessões.
- O sistema deve permitir visualização de consentimentos de cookies e histórico de aceite.
- O sistema deve suportar políticas de retenção e expiração por tipo de sessão e tipo de cookie.
- O sistema deve registrar ações administrativas em trilha de auditoria imutável.
- O sistema deve permitir bloqueio de sessão por risco, geolocalização incomum, múltiplos logins ou alteração de fingerprint.
- O sistema deve suportar alertas e automações baseadas em regras.

##### Regras de segurança
- Cookies sensíveis devem ser marcados como HttpOnly, Secure e SameSite adequadamente.
- Sessões devem possuir identificador aleatório de alta entropia.
- O sistema deve suportar rotação de sessão após autenticação e elevação de privilégio.
- O sistema deve invalidar sessões após logout, expiração, risco detectado ou revogação administrativa.
- O sistema deve registrar tentativa de uso de sessão expirada ou revogada.
- O sistema deve permitir políticas distintas por ambiente: local, homologação, produção.
- O sistema deve suportar limitação de taxa para operações sensíveis.

##### Páginas do módulo
###### 1. Dashboard de sessões
####### Componentes
- KPIs de sessões ativas, expiradas, revogadas e suspeitas.
- Gráfico de linhas com evolução de sessões por período.
- Gráfico de pizza por tipo de dispositivo.
- Gráfico de barras por unidade, entidade ou domínio.
- Widget de alertas críticos.
- Widget de sessões em risco.
- Widget de consentimentos pendentes.
- Widget de automações executadas hoje.

####### Controles
- Filtro por período.
- Filtro por entidade.
- Filtro por unidade.
- Filtro por ambiente.
- Filtro por status.
- Filtro por tipo de dispositivo.
- Exportar CSV/PDF.
- Atualizar dados.
- Alternar visualização resumida/detalhada.

###### 2. Sessões
####### Datatable
Colunas:
- ID.
- Usuário.
- Entidade.
- Unidade.
- Status.
- IP.
- País.
- Dispositivo.
- Browser.
- Sistema operacional.
- Criada em.
- Última atividade.
- Expira em.
- Risco.
- Ações.

####### Ações de linha
- Visualizar.
- Editar atributos administrativos.
- Revogar sessão.
- Forçar logout.
- Marcar como suspeita.
- Reprocessar risco.
- Ver histórico.

####### Drawer de sessão
Campos:
- Usuário.
- E-mail.
- Token hash.
- Session ID.
- IP inicial.
- IP atual.
- User agent.
- Fingerprint.
- Localização.
- Status.
- Origem do login.
- MFA aplicado.
- Escopo.
- Última renovação.
- Expiração.
- Motivo de revogação.
- Observações.

###### 3. Políticas de cookies
####### Datatable
Colunas:
- Nome.
- Domínio.
- Ambiente.
- Categoria.
- Obrigatório.
- Duração.
- SameSite.
- Secure.
- HttpOnly.
- Ativo.
- Última revisão.
- Ações.

####### Drawer de política
Campos:
- Nome da política.
- Domínio alvo.
- Entidade.
- Unidade.
- Ambiente.
- Categoria do cookie.
- Descrição.
- Duração em dias.
- SameSite.
- Secure.
- HttpOnly.
- Consentimento obrigatório.
- Banner exibido.
- Texto legal.
- Versão.
- Vigência.
- Status.

###### 4. Consentimentos
####### Datatable
Colunas:
- Usuário.
- Política.
- Status.
- Aceite em.
- Revogado em.
- IP.
- Canal.
- Versão.
- Ações.

####### Drawer de consentimento
Campos:
- Identificador do usuário.
- Política relacionada.
- Status.
- Timestamp de aceite.
- Canal de aceite.
- Versão exibida.
- Registro de prova.
- IP.
- User agent.
- Observações.

###### 5. Regras e automações
####### Datatable
Colunas:
- Nome.
- Tipo.
- Condição.
- Ação.
- Severidade.
- Ativo.
- Agenda.
- Última execução.
- Próxima execução.
- Ações.

####### Drawer de automação
Campos:
- Nome.
- Descrição.
- Gatilho.
- Condição lógica.
- Ação executada.
- Escopo.
- Limite de execução.
- Janela de execução.
- Severidade.
- Notificar por.
- Ativo.

###### 6. Auditoria
####### Datatable
Colunas:
- Data/hora.
- Usuário.
- Ação.
- Recurso.
- Resultado.
- IP.
- Origem.
- Correlation ID.
- Ações.

####### Filtros
- Período.
- Usuário.
- Entidade.
- Unidade.
- Ação.
- Resultado.
- IP.
- Recurso.

##### Widgets obrigatórios
- Total de sessões ativas.
- Sessões expirando em breve.
- Sessões suspeitas.
- Cookies obrigatórios ativos.
- Consentimentos pendentes.
- Revogações hoje.
- Alertas de risco.
- Automações falhas.

##### Charts obrigatórios
- Linha: sessões ao longo do tempo.
- Barras: sessões por unidade.
- Pizza: distribuição por dispositivo.
- Área: volume de eventos de sessão.
- Heatmap: horários de maior atividade.
- Funil: login, consentimento, sessão ativa, renovação, logout.

##### Kanban operacional
###### Colunas
- Novas suspeitas.
- Em análise.
- Aguardando ação.
- Revogadas.
- Resolved.
- Ignoradas.

###### Cards
Cada card deve exibir:
- Usuário.
- Tipo de risco.
- Severidade.
- IP.
- Unidade.
- Data/hora.
- Última ação.
- Responsável.

###### Ações no card
- Abrir drawer.
- Mover coluna.
- Reatribuir.
- Marcar como resolvido.
- Revogar sessão.
- Abrir incidente.

##### Controles gerais
- Busca global.
- Filtros avançados.
- Ordenação por qualquer coluna.
- Paginação.
- Seleção múltipla.
- Ações em lote.
- Exportação.
- Importação de regras.
- Atualização automática.
- Toggle de colunas.
- Modo compacto e expandido.
- Painel lateral de contexto.

##### Ações em lote
- Revogar múltiplas sessões.
- Marcar múltiplos consentimentos como revisados.
- Ativar/desativar políticas.
- Executar automações manualmente.
- Exportar evidências.
- Enviar notificações.
- Encaminhar para análise.

##### Fluxos principais
###### Login e criação de sessão
1. Usuário autentica.
2. Sistema valida credenciais e MFA.
3. Sistema cria sessão com fingerprint e metadados.
4. Sistema registra eventos de auditoria.
5. Sistema aplica política de cookies e consentimento.

###### Revogação de sessão
1. Operador seleciona a sessão.
2. Sistema exibe motivo e impacto.
3. Operador confirma revogação.
4. Sistema invalida token.
5. Sistema registra evento e notifica responsáveis.

###### Tratamento de risco
1. Motor de regras identifica anomalia.
2. Sessão é sinalizada.
3. Card é movido para Kanban.
4. Operador analisa dados.
5. Ação final é aplicada e auditada.

##### Automações
- Revogar sessão inativa por X minutos.
- Encerrar sessão após alteração de IP suspeita.
- Notificar login em novo dispositivo.
- Exigir reautenticação em ação crítica.
- Expirar cookies fora da política.
- Bloquear sessão após múltiplas falhas.
- Abrir incidente ao detectar risco alto.
- Enviar resumo diário de sessões e consentimentos.

##### Integrações
- Serviço de autenticação.
- Serviço de auditoria.
- Serviço de notificações.
- Serviço de risco e antifraude.
- Serviço de consentimento LGPD.
- Webhooks para incidentes.
- Logs centralizados.

##### Requisitos de API
###### Endpoints principais
- GET /sessions
- GET /sessions/{id}
- POST /sessions/{id}/revoke
- POST /sessions/{id}/flag
- POST /sessions/{id}/refresh
- GET /cookie-policies
- POST /cookie-policies
- PUT /cookie-policies/{id}
- DELETE /cookie-policies/{id}
- GET /consents
- POST /consents/{id}/revoke
- GET /automations
- POST /automations/{id}/run
- GET /audit-logs

##### Modelo de dados mínimo
###### Session
- id.
- user_id.
- entity_id.
- unit_id.
- status.
- ip_address.
- user_agent.
- device_type.
- browser.
- os.
- fingerprint.
- risk_score.
- created_at.
- last_activity_at.
- expires_at.
- revoked_at.
- revoked_reason.

###### CookiePolicy
- id.
- name.
- domain.
- environment.
- category.
- same_site.
- secure.
- http_only.
- duration_days.
- consent_required.
- banner_enabled.
- version.
- active.

###### ConsentRecord
- id.
- user_id.
- policy_id.
- status.
- accepted_at.
- revoked_at.
- ip_address.
- user_agent.
- evidence_hash.

##### UX/UI
- Layout com sidebar, topbar e área principal.
- Cards com status por cor e ícone.
- Drawers laterais para edição sem sair da página.
- Tabelas responsivas com colunas configuráveis.
- Kanban com drag and drop.
- Gráficos com legenda e tooltip.
- Estados vazios, loading e erro bem definidos.
- Confirmação para ações destrutivas.

##### Validações
- Campos obrigatórios devem ser validados no frontend e backend.
- Duração de cookie deve respeitar limites mínimos e máximos.
- Regra de SameSite deve aceitar apenas valores válidos.
- Revogação exige motivo quando em produção.
- Ações em lote devem exigir confirmação explícita.

##### Logs e auditoria
- Registrar quem executou a ação.
- Registrar data/hora com timezone.
- Registrar origem da requisição.
- Registrar antes e depois quando aplicável.
- Registrar falhas, exceções e tentativas indevidas.

##### Permissões
- Visualizar sessões.
- Revogar sessões.
- Gerenciar políticas.
- Gerenciar consentimentos.
- Executar automações.
- Visualizar auditoria.
- Exportar dados.
- Configurar regras de risco.

##### Critérios de aceite
- O módulo deve exibir dashboards com widgets e gráficos funcionais.
- O módulo deve permitir CRUD completo de cookies, sessões e automações.
- O módulo deve permitir Kanban para tratamento operacional.
- O módulo deve executar automações agendadas e manuais.
- O módulo deve registrar auditoria completa de ações críticas.
- O módulo deve suportar filtros, busca, exportação e ações em lote.
- O módulo deve estar pronto para uso multi-entity e multi-unit.

##### Entregáveis esperados
- Página de dashboard.
- Página de sessões.
- Página de políticas de cookies.
- Página de consentimentos.
- Página de automações.
- Página de auditoria.
- Painel Kanban.
- Drawers de cadastro, edição e detalhe.
- Gráficos e widgets operacionais.
- API backend documentada.

##### Observações técnicas
- Recomenda-se UUID como chave primária.
- Recomenda-se indexação por status, usuário, entidade, unidade e expiração.
- Recomenda-se soft delete para políticas e regras.
- Recomenda-se cache para consultas de dashboard.
- Recomenda-se separação de sessão ativa e evento histórico.
- Recomenda-se versionamento de políticas e consentimentos.
