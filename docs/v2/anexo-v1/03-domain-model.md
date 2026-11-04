# SDD 03 — Modelo de Domínio (TotusTuus SoftCloud)

> **Documento derivado do SDD mestre** · **Data:** 04/08/2026

---

## 1. Entidades nucleares (implementadas — app/Models/, 74 models)

| Entidade | Model | Descrição | Status |
|----------|-------|-----------|:------:|
| Platform | — (contexto global) | Plataforma SaaS | ✅ conceito |
| Entity/Organization | `Organization.php`, `OrganizationProfile.php`, `OrganizationBranding.php`, `OrganizationAddress.php`, `OrganizationUnit.php`, `OrganizationDocument.php`, `OrganizationIntegration.php`, `OrganizationMetric.php`, `OrganizationAuditLog.php` | Cliente com branding/dados isolados | ✅ |
| Unit | `Unit.php` | Subdivisão operacional | ✅ |
| User | `User.php` + perfil (UserProfile*, UserPhone/Email/Address/Family/Identity/Document) | Identidade humana/tech | ✅ |
| Membership | `UserMembership.php`, `UserUnit.php` | Vínculo user/entity/unit | ✅ |
| Role/Permission | `Role.php`, `Permission.php` | RBAC | ✅ |
| Session | `UserSession.php`, `UserSessionEvent.php` | Sessão autenticada web | ✅ |
| ApiClient | (via OrganizationIntegration/ThirdPartyIntegration) | Cliente técnico | ✅ |
| AuditEvent | `AuditLog.php`, `SecurityLog.php`, `SecurityEvent.php`, `DbAudit.php`, `AccessLog.php`, `ErrorLog.php` | Registros imutáveis | ✅ |
| LocalePack | (I18n service + testes) | Recursos de idioma | ✅ |
| FeatureFlag | — | Controle de ativação | 🔲 pendente (Developer layer) |
| WebhookEndpoint | `WebhookDispatcher` (Billing) + HmacAuthMiddleware | Destino de eventos | ✅ (parcial) |
| Job | `MigrationExecutionJob.php`, async_event_worker | Unidade assíncrona | ✅ (parcial) |

## 2. Entidades por domínio (amostra representativa)

| Domínio | Models |
|---------|--------|
| Auth/IAM | User*, Role, Permission, UserMembership, UserUnit, Invitation, DeviceTrust, SecurityEvent, SecurityLog, AccessLog, AccessRequest, IdentityAutomation(+Log) |
| Privacy/LGPD | PrivacyConsentEvent, UserConsent, UserCookieConsent(+Item), CookieCatalog, CookieCategory, ConsentBannerVersion, TenantPrivacySetting |
| Migração | MigrationProject, MigrationSourceTable/Column, MigrationTableMapping/ColumnMapping/ValueMap, MigrationImport, MigrationExecutionJob, MigrationValidationRun, MigrationAuditLog, MigrationTargetTableCache |
| Reuniões | Meeting, MeetingParticipant, MeetingRecording |
| Acadêmico | AcademicPeriod + tables em migrations (cursos, turmas, matrículas, grade, etc.) |
| Billing | tables `billing_*` (plans, subscriptions, invoices, payments, discounts, automations, nfse, gateway config) |
| Notificações | NotificationChannel + tables `notification_*` |

## 3. Convenções de modelo

- **Soft delete**: coluna `deleted_at` + `SoftDeleteService`/`SoftDeleteRegistry` (app/Services/SoftDeleteService.php) — ver `docs/spec-soft-delete-totustuus.md`.
- **UUID**: chaves `uuid` (char 36 ou binary 16) em todas as entidades expostas via API.
- **Tenancy**: coluna `tenant_id` em todas as tabelas multi-tenant (renomeada de `entity_id` em 14/07 — migração `2026_07_14_000003_rename_entity_id_to_tenant_id.php`).
- **Timestamps**: `created_at`/`updated_at` em tudo; `deleted_at` onde aplicável.
- **Auditoria**: `*AuditLog` por domínio sensível (OrganizationAuditLog, UserAuditLog, MigrationAuditLog).

## 4. Falhas de modelo conhecidas

| Item | Ação |
|------|------|
| FeatureFlag não implementado | Criar model + tabela (Onda C — Developer layer) |
| WebhookEndpoint genérico | Billing tem WebhookDispatcher; generalizar para Integration Hub (Onda B) |
| Autofilia (self-reference) em Organization/Unit | Verificar necessidade futura |

## 5. Rastreabilidade

Cada model referenciado nos specs `docs/Nova pasta/spec_gestao_*_completo.md`. O mapeamento spec→tabela é validado em `tests/ClientMigrationSchemaTest.php` (para migração) e nos testes por módulo.
