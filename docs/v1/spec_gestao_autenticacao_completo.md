# AUTH MODULE SPECIFICATION v2

- Language Standard: Global English
- Architecture: Multi-entity | Multi-unit | Multi-user
- Stack: PHP 8 pure, fetch + API, no external libraries, Supabase template

---

## 1. Document Purpose

This document defines the complete technical and functional specification for the authentication and access control module of the SaaS platform.

The module must support secure identity management, authentication, session control, authorization, auditability, and compliance-ready lifecycle management in a multi-entity, multi-unit, multi-user environment.

---

## 2. System Scope

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

## 3. Platform Standards

### 3.1 Language standard

All namespaces, functions, classes, methods, variables, folders, routes, pages, table names, columns, and string identifiers must use English only.

Database names and route slugs must use snake_case, while PHP class names must use PascalCase.

### 3.2 Technology constraints

Implementation must use:

- PHP 8.x.
- Native PHP extensions only.
- Fetch for all browser requests.
- API-first architecture.
- Supabase template conventions.
- No external libraries or Composer dependencies unless explicitly approved.

### 3.3 Identifier standard

Every table should support:

- id: numeric internal primary key.
- uuid: global internal identifier.
- code: external/public identifier.

id must never be exposed in URLs or public-facing identifiers.

### 3.4 Allowed PHP built-ins

The implementation may use:

- password_hash and password_verify.
- random_bytes.
- hash_hmac.
- hash_equals.
- openssl or sodium when available.
- PDO.
- session_* functions only if session-based support is explicitly enabled.

---

## 4. Architectural Model

### 4.1 Multi-entity

Each entity is isolated logically and operationally. A user can belong to more than one entity, but access must always be resolved through an active entity context.

### 4.2 Multi-unit

Each entity may contain multiple units such as headquarters, branches, campuses, schools, or departments. A user may belong to one or more units, but unit access must always be explicit.

### 4.3 Multi-user

The system must support many users per entity and unit. One identity may have different memberships, roles, and portal access across different contexts.

### 4.4 Context-driven access

Every authenticated session must always know:

- Current entity.
- Current unit.
- Current portal.
- Current role.
- Current permission scope.
- Current membership reference.

### 4.5 Identity separation

Identity data must be separated from business data. Authentication, authorization, membership, and audit must remain in the security layer.

### 4.6 Session isolation

A session created in one entity or unit must not be valid in another entity or unit unless the active context is explicitly changed through a controlled endpoint and revalidated.

---

## 5. User Portals

The system must support the following login destinations:

### 5.1 Administrative portal

Used by:

- Super administrators.
- Entity administrators.
- Unit administrators.
- Managers.
- Support operators.
- Auditors.

### 5.2 Teacher portal

Used by:

- Teachers.
- Coordinators.
- Academic assistants.
- Pedagogical staff.

### 5.3 Student portal

Used by:

- Students.
- Apprentices.
- Enrolled learners.

### 5.4 Parent portal

Used by:

- Parents.
- Guardians.
- Responsible parties.
- Authorized family contacts.

### 5.5 Third-party portal

Used by:

- Suppliers.
- Transport companies.
- Legal offices.
- Notary offices.
- Service providers.
- Other external partners.

---

## 6. Context Rules

### 6.1 Membership as the source of truth

A membership defines where a user can operate. It must bind:

- user
- entity
- unit
- portal
- role

### 6.2 Active session context

A session must bind to exactly one active context at a time:

- active entity.
- active unit.
- active portal.
- active role.
- active membership.

### 6.3 Context switching

If a user has multiple valid memberships, the system must allow entity and unit switching through dedicated context-selection endpoints. Every switch must be audited.

### 6.4 Default context resolution

If only one valid context exists, the system may auto-select it. If multiple valid contexts exist, the user must be prompted to choose.

### 6.5 Selector precedence

Context resolution order must be:

1. Explicit request parameter.
2. Previously persisted last active context.
3. Default membership.
4. First valid membership by platform rule.

---

## 7. Authentication Flows

### 7.1 Login flow

1. User selects or is directed to a portal.
2. User submits credentials.
3. System validates identity, account status, portal eligibility, entity membership, unit membership, and MFA requirements.
4. System resolves valid contexts.
5. System issues session and tokens.
6. System logs the event.
7. System routes the user to the correct dashboard.

### 7.2 Logout flow

1. User requests logout.
2. Session is revoked.
3. Refresh token is invalidated.
4. Audit entry is created.
5. Client clears state.

### 7.3 Password recovery flow

1. User requests password recovery.
2. System rate-limits the request.
3. System creates a reset token.
4. Reset token is stored hashed.
5. Reset link is sent.
6. User sets a new password.
7. Old sessions are invalidated.

### 7.4 MFA flow

1. User enrolls a factor.
2. System verifies initial proof.
3. System stores factor data securely.
4. On challenge, user submits code.
5. System validates and logs the result.

### 7.5 Invite flow

1. Admin creates invitation.
2. Invitation is linked to entity, unit, portal, and role scope.
3. System sends invitation link.
4. User accepts invitation.
5. User sets password and optionally enrolls MFA.
6. Membership becomes active.

---

## 8. Security Requirements

### 8.1 Password policy

Passwords must:

- Have minimum length.
- Reject common passwords.
- Reject recent reuse.
- Be hashed with Argon2id.
- Never be logged or exposed in errors.

### 8.2 Password hashing policy

The implementation must use password_hash with PASSWORD_ARGON2ID. The spec must allow environment-tuned cost parameters, but the chosen values must be documented in configuration.

### 8.3 Session protection

The system must:

- Regenerate session after login.
- Invalidate sessions on logout.
- Revoke old tokens after refresh rotation.
- Prevent session fixation.
- Enforce idle and absolute timeout policies.

### 8.4 Rate limiting

The system must throttle:

- Login attempts.
- Password reset requests.
- MFA attempts.
- Refresh token requests.
- Invitation resend requests.

### 8.5 CSRF and cookies

If browser cookies are used for auth, they must be HttpOnly, Secure, and SameSite-restricted. State-changing endpoints must use CSRF protection.

### 8.6 CORS policy

The API must only allow explicitly configured origins. Credentials may only be allowed when the origin is trusted and the request is authenticated by the chosen session model.

### 8.7 Auditability

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

## 9. Token and Session Model

### 9.1 Access token

Use a short-lived access token with only safe claims. It must not expose sensitive personal data.

### 9.2 Refresh token

Use a rotating refresh token with server-side revocation support. Store only hashed refresh tokens in the database.

### 9.3 Session record

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

### 9.4 Token lifecycle

- Access token: short-lived.
- Refresh token: longer-lived, rotated on use.
- Reuse detection: mandatory.
- Revocation: mandatory.

### 9.5 Token claims

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

### 9.6 Refresh rotation policy

A refresh token must be single-use. When exchanged, the previous token must be invalidated and a new token issued. Reuse of a rotated token must revoke the entire session family.

---

## 10. Authorization Model

### 10.1 RBAC

Authorization must be role-based and permission-based. Deny-by-default is mandatory.

### 10.2 Permission scope

Permissions may be scoped by:

- Portal.
- Module.
- Action.
- Entity.
- Unit.
- Record ownership.

### 10.3 Sample permissions

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

### 10.4 Evaluation order

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

## 11. MFA Requirements

### 11.1 Supported methods

Initial supported methods:

- TOTP.
- Backup codes.
- Optional email OTP for recovery only, if policy allows.

### 11.2 MFA enforcement

MFA is required for:

- Administrators.
- Sensitive actions.
- High-risk logins.
- New device logins.
- Suspicious IP or location changes.

### 11.3 MFA recovery

MFA recovery must be auditable and stronger than normal login. Recovery must not weaken security controls.

### 11.4 Backup codes

Backup codes must be generated securely, shown once, stored hashed, and marked as consumed when used.

---

## 12. User Lifecycle

### 12.1 Registration methods

- Manual creation.
- Invitation-based registration.
- Self-registration when allowed.
- External identity import.

### 12.2 User profile

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

### 12.3 Status lifecycle

Supported statuses:

- Active.
- Pending.
- Invited.
- Suspended.
- Locked.
- Deleted.
- Archived.

### 12.4 Membership lifecycle

Supported actions:

- Assign entity.
- Assign unit.
- Assign portal.
- Assign role.
- Revoke membership.
- Transfer membership.
- Clone access profile.

---

## 13. Data Model

### 13.1 Core tables

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

### 13.2 Mandatory fields pattern

Each table should generally include:

- id
- uuid
- code
- created_at
- updated_at
- deleted_at when applicable.

### 13.3 Key relationships

- memberships links users to entities, units, portals, and roles.
- sessions reference active memberships.
- refresh_tokens reference sessions.
- audit_logs reference actor and target contexts.
- invitations create future memberships.

---

## 14. Database Rules

### 14.1 UUID strategy

UUID must be the global cross-context identifier for APIs, logs, and external references.

### 14.2 Soft delete

Deleted rows must use deleted_at instead of physical deletion when the record must remain auditable.

### 14.3 Indexing

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

### 14.4 Tenant safety

All entity-scoped and unit-scoped queries must include explicit scope filters. Cross-tenant access must never rely on client-side filtering.

---

## 15. API Specification

### 15.1 Public routes

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

### 15.2 Administrative routes

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

### 15.3 Standard API response

All responses must include:

- success
- message
- data
- errors
- meta
- request_id

### 15.4 Error handling

Use standard HTTP codes:

- 400 for validation failures.
- 401 for unauthenticated requests.
- 403 for forbidden requests.
- 404 for not found.
- 409 for conflicts.
- 422 for semantic validation failures.
- 429 for rate limits.
- 500 for unexpected errors.

### 15.5 API headers

Requests and responses must support:

- Authorization.
- Content-Type.
- Accept.
- X-Request-Id.
- X-CSRF-Token when cookie session is enabled.

### 15.6 API contracts

The spec must define request and response payloads for login, refresh, logout, forgot password, reset password, MFA challenge, entity selection, unit selection, and portal selection.

---

## 16. Frontend Fetch Rules

### 16.1 Request behavior

All frontend authentication requests must use fetch.

### 16.2 Token storage

If tokens are returned to the browser, the access token must be kept in memory only. Refresh token handling must follow the selected security model and must not expose tokens in unsafe storage unless explicitly accepted by the security policy.

### 16.3 Standard fetch flow

Each request must:

- Send required headers.
- Handle JSON serialization.
- Read JSON responses.
- React to 401 and 429 consistently.
- Refresh session when needed.

---

## 17. UI Requirements

### 17.1 Public pages

- login
- forgot_password
- reset_password
- mfa_challenge
- select_entity
- select_unit
- select_portal
- logout

### 17.2 Administrative pages

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

### 17.3 Portal pages

- home_dashboard
- profile
- password_change
- session_history
- notifications
- help_center

---

## 18. Controls Matrix

### 18.1 Datatable controls

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

### 18.2 Widget controls

- Refresh.
- Time range.
- Drilldown.
- Export.
- Pin.
- Hide.
- Compare.

### 18.3 Chart controls

- Date range.
- Group by.
- Filter by portal.
- Filter by entity.
- Filter by unit.
- Download image.
- Download data.
- Toggle series.

### 18.4 Drawer controls

- Open.
- Close.
- Save.
- Validate.
- Reset.
- Duplicate.
- Archive.

### 18.5 Kanban controls

- Drag and drop.
- Assign user.
- Change state.
- Add note.
- Set priority.
- Resolve.
- Reopen.

---

## 19. Dashboard Requirements

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

## 20. Automation Requirements

### 20.1 Authentication automations

- Automatic session expiry.
- Automatic token rotation.
- Automatic logout after inactivity.
- Automatic lock after brute-force threshold.
- Automatic password expiration warning.
- Automatic MFA challenge for risky events.
- Automatic role sync from membership changes.

### 20.2 Operational automations

- Send email invitation.
- Send password reset email.
- Send approval request.
- Send security alert.
- Send login confirmation.
- Send suspicious login warning.
- Generate audit report.
- Generate access report.

### 20.3 Governance automations

- Disable unused accounts.
- Flag stale accounts.
- Detect duplicate identities.
- Detect orphan memberships.
- Detect conflicting role assignments.
- Detect invalid portal access.

---

## 21. Compliance and Privacy

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

## 22. Non-Functional Requirements

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

## 23. Acceptance Criteria

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

## 24. Implementation Priority

### Phase 1

- Login.
- Logout.
- Session management.
- Password recovery.
- Entity and unit resolution.
- Role-based access.
- Core database schema.
- Core API contracts.

### Phase 2

- MFA.
- Invitations.
- User management.
- Audit logs.
- Permissions management.
- Context switching.

### Phase 3

- Widgets.
- Charts.
- CRUD drawers.
- Kanban boards.
- Automations.
- Admin dashboards.

### Phase 4

- Advanced governance.
- Risk scoring.
- Device trust.
- Security analytics.
- Full operational hardening.

---

## 25. Database Entities Appendix

### 25.1 users

Stores identity and authentication profile.

### 25.2 entities

Stores organization-level tenants.

### 25.3 units

Stores units belonging to entities.

### 25.4 memberships

Stores the access relationship between user, entity, unit, portal, and role.

### 25.5 roles

Stores role definitions.

### 25.6 permissions

Stores permission definitions.

### 25.7 sessions

Stores active and revoked sessions.

### 25.8 refresh_tokens

Stores hashed refresh token records.

### 25.9 login_attempts

Stores failed and successful authentication attempts.

### 25.10 password_resets

Stores password recovery flow records.

### 25.11 mfa_factors

Stores MFA factor metadata.

### 25.12 mfa_backup_codes

Stores hashed backup codes.

### 25.13 audit_logs

Stores security and administrative events.

### 25.14 device_trusts

Stores trusted device metadata.

---

## 26. Final Definition

This specification is complete enough to serve as the master implementation document for the authentication module under the stated architecture and technology constraints.
