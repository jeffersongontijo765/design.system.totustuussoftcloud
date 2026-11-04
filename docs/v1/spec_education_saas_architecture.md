# EDUCATION SAAS PLATFORM ARCHITECTURE SPECIFICATION

- Language Standard: Global English
- Architecture: Multi-entity | Multi-unit | Multi-user
- Stack: PHP 8 pure, fetch + API, no external libraries, Supabase template

---

## 1. Purpose

This document defines the complete architecture specification for an education SaaS platform designed for multiple institutional clients, multiple internal units, and multiple user roles.

The goal is to provide a safe, scalable, maintainable, and enterprise-ready structure that avoids tenant leakage, permission confusion, and future refactoring problems.

---

## 2. Platform Vision

The platform must support educational institutions of different sizes and models, including:

- Schools.
- Colleges.
- Universities.
- Training centers.
- EAD and online programs.
- After-school and prep courses.
- Hybrid institutions.

The platform must provide separate access experiences for internal management, students, parents or guardians, teachers, and third parties.

---

## 3. Core Architecture Principles

### 3.1 Global identity, contextual access

A user is a global identity. Access is never global by default. Access always depends on the active membership context.

### 3.2 Multi-entity

Each customer institution is an entity. An entity is a tenant boundary.

### 3.3 Multi-unit

Each entity may contain multiple units such as campuses, branches, schools, departments, or operational centers.

### 3.4 Multi-user

Multiple users can belong to the same entity and unit, with different portal access and permissions.

### 3.5 Portal separation

Each audience must have a dedicated portal and route structure.

### 3.6 Security by default

The system must enforce least privilege, session isolation, strong authentication, auditability, and explicit access grants.

---

## 4. Main Areas

### 4.1 Management - Developer

This area is for platform administration and technical operations. It must be restricted to internal staff only.

Responsible for:

- Entity administration.
- Unit administration.
- User administration.
- Role and permission management.
- Subscription and feature configuration.
- Audit and security monitoring.
- System settings.
- Integrations.
- Logs and diagnostics.

### 4.2 Management - Clients

This area is for the institution’s operational administrators.

Examples:

- School administration.
- College administration.
- University administration.
- Cursinho and EAD administration.

Responsible for:

- Institution users.
- Units.
- Staff.
- Students.
- Enrollments.
- Operational settings.
- Communication and workflows.

### 4.3 Student Area

This area is for enrolled learners.

Responsible for:

- Dashboard.
- Profile.
- Enrollments.
- Classes.
- Attendance.
- Grades.
- Notifications.
- Documents.
- Requests.

### 4.4 Guardians Area

This area is for parents, guardians, and responsible parties.

Responsible for:

- Student follow-up.
- Academic status.
- Financial or administrative notices, when allowed.
- Authorization and consent flows.
- Communication with the institution.

### 4.5 Teacher Area

This area is for teachers, coordinators, and pedagogical staff.

Responsible for:

- Classes.
- Attendance.
- Grades.
- Planning.
- Communications.
- Materials.
- Reports.

### 4.6 Third-Party Area

This area is for external partners such as accounting, legal, transport, and service providers.

Responsible for:

- Restricted documents.
- Requests.
- Deliverables.
- Contractual tasks.
- Controlled communication.

---

## 5. Tenant Model

### 5.1 Entity definition

An entity represents one client institution or one organizational tenant.

Examples:

- One school chain.
- One university group.
- One training company.
- One EAD provider.

### 5.2 Unit definition

A unit is a substructure of an entity.

Examples:

- Campus.
- Branch.
- School.
- Building.
- Department.
- Administrative office.

### 5.3 Tenant safety rules

- Every record that belongs to a tenant must be linked to an entity.
- Every record that belongs to a unit must also reference its parent entity.
- Cross-tenant access must never be decided in the frontend.
- Database queries must always filter by entity or by allowed global scope.

---

## 6. Identity Model

### 6.1 Global user

A user is a single identity in the platform. One user may have multiple memberships.

### 6.2 Membership

Membership is the bridge between user, entity, unit, portal, and role.

Required membership fields:

- user_uuid.
- entity_uuid.
- unit_uuid.
- portal_code.
- role_code.
- status.
- is_default.
- starts_at.
- ends_at.

### 6.3 Active context

At any time, the authenticated session must have one active membership context.

Active context must define:

- current entity.
- current unit.
- current portal.
- current role.
- current permissions.

### 6.4 Context switching

If the user has more than one valid membership, the system must allow controlled switching through a dedicated endpoint and must log the change.

---

## 7. Portal Structure

### 7.1 Management - Developer portal

Route prefix: /dev

Access: internal platform staff only.

### 7.2 Management - Clients portal

Route prefix: /admin

Access: institutional admins and authorized staff.

### 7.3 Student portal

Route prefix: /student

Access: students only, with possible guardian-linked access to selected features.

### 7.4 Guardians portal

Route prefix: /guardian

Access: parents, guardians, responsible parties.

### 7.5 Teacher portal

Route prefix: /teacher

Access: teachers and pedagogical staff.

### 7.6 Third-party portal

Route prefix: /partner

Access: external partners with limited scope.

---

## 8. Functional Modules

### 8.1 Authentication

- Login.
- Logout.
- Session refresh.
- Password reset.
- Invitation acceptance.
- MFA challenge.
- Recovery flows.

### 8.2 Authorization

- Role-based access.
- Permission-based access.
- Portal-based access.
- Entity-based access.
- Unit-based access.
- Record-level restrictions.

### 8.3 Identity governance

- Create user.
- Update user.
- Suspend user.
- Lock user.
- Restore user.
- Delete soft.
- Archive.
- Reassign memberships.

### 8.4 Audit and security

- Audit logs.
- Failed login tracking.
- Security events.
- Session revocation.
- Device trust.
- Login history.

### 8.5 Operational administration

- Users.
- Roles.
- Permissions.
- Units.
- Memberships.
- Invitations.
- Access requests.
- Notifications.
- Settings.

---

## 9. Data Domains

### 9.1 Platform domain

Contains global platform configuration, internal developer access, feature flags, subscriptions, and tenant administration.

### 9.2 Academic domain

Contains students, guardians, teachers, classes, enrollments, attendance, grades, schedules, and materials.

### 9.3 Institutional domain

Contains departments, administrative flows, staff, documents, internal tasks, and operational processes.

### 9.4 Partner domain

Contains partner records, contracts, delivery flows, and restricted operational requests.

### 9.5 Shared identity domain

Contains users, memberships, roles, permissions, sessions, audit logs, and security events.

---

## 10. Database Architecture

### 10.1 Required core tables

- users.
- entities.
- units.
- portals.
- roles.
- permissions.
- memberships.
- sessions.
- refresh_tokens.
- login_attempts.
- password_resets.
- mfa_factors.
- mfa_backup_codes.
- invitations.
- access_requests.
- audit_logs.
- security_events.
- device_trusts.
- feature_flags.
- settings.

### 10.2 Core tenancy fields

Any tenant-owned table must include:

- entity_uuid.
- unit_uuid when applicable.
- created_at.
- updated_at.
- deleted_at when applicable.

### 10.3 Relationship rules

- Users may exist without immediate membership only if invited or pending.
- Roles and permissions are global definitions.
- Memberships bind roles and permissions to a tenant context.
- Sessions must reference membership context.

---

## 11. Security Architecture

### 11.1 Password handling

- Use Argon2id.
- Never store plaintext.
- Never log passwords.
- Support rehash migration.

### 11.2 Token strategy

- Short-lived access token.
- Rotating refresh token.
- Server-side revocation.
- Reuse detection.

### 11.3 Session protection

- Bind session to context.
- Bind optional device fingerprint.
- Invalidate on logout.
- Invalidate on role or membership revocation.
- Support idle timeout and absolute timeout.

### 11.4 Abuse protection

- Rate limiting.
- Temporary lockouts.
- Failed login tracking.
- Suspicious activity detection.

### 11.5 MFA

- TOTP.
- Backup codes.
- Optional recovery-based second factor.

---

## 12. API Architecture

### 12.1 API principles

- JSON only.
- Versioned routes.
- Predictable response format.
- Clear HTTP status usage.
- Consistent error structure.

### 12.2 Authentication endpoints

- POST /api/v1/auth/login
- POST /api/v1/auth/logout
- POST /api/v1/auth/refresh
- POST /api/v1/auth/forgot_password
- POST /api/v1/auth/reset_password
- POST /api/v1/auth/mfa/enroll
- POST /api/v1/auth/mfa/challenge
- GET /api/v1/auth/me
- GET /api/v1/auth/session
- POST /api/v1/auth/select_entity
- POST /api/v1/auth/select_unit
- POST /api/v1/auth/select_portal

### 12.3 Administrative endpoints

- GET /api/v1/admin/users
- POST /api/v1/admin/users
- PUT /api/v1/admin/users/{uuid}
- GET /api/v1/admin/roles
- POST /api/v1/admin/roles
- GET /api/v1/admin/permissions
- POST /api/v1/admin/permissions
- GET /api/v1/admin/memberships
- POST /api/v1/admin/memberships
- GET /api/v1/admin/sessions
- POST /api/v1/admin/sessions/revoke
- GET /api/v1/admin/audit_logs
- GET /api/v1/admin/security_events

### 12.4 Standard response format

Every response must include:

- success.
- message.
- data.
- errors.
- meta.
- request_id.

---

## 13. Frontend Structure

### 13.1 Portal frontends

Each portal must have its own route prefix, layout, navigation, permissions, and dashboard.

### 13.2 Fetch integration

Frontend requests must use fetch with JSON bodies and standardized error handling.

### 13.3 UI separation

Do not mix developer UI with client UI, student UI, guardian UI, teacher UI, or third-party UI.

### 13.4 Shared components

Shared components may include:

- Input fields.
- Tables.
- Dialogs.
- Drawers.
- Tabs.
- Cards.
- Filters.
- Charts.
- Kanban boards.

---

## 14. Page Structure

### 14.1 Developer area pages

- dashboard.
- tenants.
- entities.
- units.
- users.
- memberships.
- roles.
- permissions.
- sessions.
- audit_logs.
- security_events.
- settings.
- feature_flags.
- integrations.

### 14.2 Client management pages

- dashboard.
- students.
- guardians.
- teachers.
- staff.
- units.
- enrollments.
- classes.
- attendance.
- grades.
- communications.
- documents.
- requests.

### 14.3 Student pages

- home_dashboard.
- profile.
- enrollments.
- schedule.
- attendance.
- grades.
- notifications.
- documents.
- requests.

### 14.4 Guardian pages

- home_dashboard.
- linked_students.
- academic_followup.
- notifications.
- documents.
- requests.
- consent.

### 14.5 Teacher pages

- home_dashboard.
- classes.
- attendance.
- grades.
- planning.
- materials.
- messages.
- reports.

### 14.6 Third-party pages

- home_dashboard.
- requests.
- documents.
- tasks.
- communications.
- history.

---

## 15. Naming Conventions

### 15.1 PHP

- Classes in PascalCase.
- Methods in camelCase.
- Functions in camelCase or snake_case, but consistent.
- Files in snake_case.

### 15.2 Database

- Tables in snake_case.
- Columns in snake_case.
- Foreign keys named with _uuid or _id consistently.

### 15.3 Routes

- Route segments in lower-case snake_case.
- API version prefix required.

### 15.4 UI names

- Pages and components in English.
- No mixed-language identifiers in code.

---

## 16. Implementation Layers

### 16.1 Presentation layer

Responsible for pages, forms, tables, drawers, charts, and user interaction.

### 16.2 API layer

Responsible for request validation, response formatting, auth checks, and orchestration.

### 16.3 Domain layer

Responsible for business rules, memberships, permissions, and workflows.

### 16.4 Infrastructure layer

Responsible for database access, mail, logging, files, security primitives, and integrations.

---

## 17. Governance Rules

### 17.1 Internal governance

Internal staff must be able to review tenants, security events, sessions, and audit logs.

### 17.2 Client governance

Clients must only see their own entity and allowed units.

### 17.3 Educational governance

Student, guardian, teacher, and third-party access must always be constrained by context.

### 17.4 Compliance governance

The platform must support retention, traceability, export, deletion, and privacy-safe handling of personal data.

---

## 18. Non-Functional Requirements

- Secure by default.
- Maintainable code structure.
- High concurrent login performance.
- Easy tenant isolation.
- Extensible for new portals and roles.
- Compatible with multiple database backends.
- Easy to audit.
- Easy to automate.
- Clear separation between platform and client responsibilities.

---

## 19. Acceptance Criteria

The architecture is complete when:

- Every user belongs to a clear identity model.
- Every access is contextual and explicit.
- Every portal is separated.
- Every entity is isolated.
- Every unit is traceable.
- Every session is bound to one context.
- Every security event is logged.
- Every endpoint is versioned.
- Every page has a single audience.
- Every query is tenant-safe.

---

## 20. Recommended Build Order

### Phase 1

- Core identity.
- Entity and unit model.
- Membership model.
- Authentication.
- Authorization.
- API base.
- Developer portal.

### Phase 2

- Client management.
- Student portal.
- Guardian portal.
- Teacher portal.
- Third-party portal.
- Audit and security.

### Phase 3

- Academic modules.
- Operational dashboards.
- Tables, drawers, and workflows.
- Notifications.
- Reports.

### Phase 4

- Automation.
- Analytics.
- Hardening.
- Integrations.
- Advanced governance.
