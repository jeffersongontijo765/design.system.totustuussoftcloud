# SDD 06 — Tenancy & Multi-Entity (TotusTuus SoftCloud)

> **Documento derivado do SDD mestre** · **Data:** 04/08/2026

---

## 1. Hierarquia de contexto e Modelo de 3 Níveis

O TotusTuus SoftCloud adota uma arquitetura hierárquica multi-camadas que desacopla a **Provedora do SaaS (Host/Tenant 0)** das **Redes e Colégios Contratantes (Tenants Clientes)**:

```
Platform Host (TotusTuus SoftCloud — Provedora / Tenant 0)
 ├── Client (Mantenedora / Grupo Educacional / Pessoa Jurídica Contratante)
 │    └── Entity (Instituição de Ensino / Colégio / Razão Social Escolar)
 │         └── Unit (Filial Física / Campus / Polo Educacional)
 │              └── Users / Memberships / Roles (Escopo Escolar Local)
 └── Master Super Admins (Usuários de Plataforma — is_master_user = 1)
      └── Vínculo formal com a Unidade Matriz da Desenvolvedora (UN-MATRIZ-DEV)
```

---

## 2. Cadastro Oficial da Empresa Desenvolvedora (Tenant 0 / Host Matriz)

A empresa operadora da nuvem e desenvolvedora da plataforma é cadastrada formalmente no banco Master (`totustuusdb`) sob identificadores criptográficos permanentes:

| Nível Hierárquico | Código | Razão Social / Nome | Tipo / Papel | UUIDv4 Criptográfico (RFC 4122) |
| :--- | :--- | :--- | :--- | :--- |
| **Cliente Provedor** | `CLI-TOTUSTUUS` | **TotusTuus SoftCloud Tecnologia da Informação Ltda** | Provedora do SaaS / Mantenedora | `d6930191-8bf9-42c4-88f6-a75ed8ba9bc1` |
| **Entidade da Desenvolvedora** | `ENT-DEV-MATRIZ` | **TotusTuus SoftCloud - Engenharia & Plataforma** | `developer` (Plataforma Tecnológica) | `8b5892fd-0fa3-4cff-ba81-80dd7cda0f65` |
| **Unidade Matriz** | `UN-MATRIZ-DEV` | **Sede Matriz - TotusTuus SoftCloud** | `headquarters` (Sede Operacional) | `6d16eac3-0d76-4549-8d86-f04582ad7ed5` |
| **Tenant Master** | `TNT-TOTUSTUUS` | **TotusTuus SoftCloud** | Banco Master (`totustuusdb`) | `4965aa14-484d-4965-8dcb-bff3f18ae6f2` |

### Vínculo dos Superadministradores da Plataforma
* **Usuários:** `admin@totustuussoftcloud.com`, `jefferson@totustuussoftcloud.com`, `dev@totustuussoftcloud.com`.
* **Identidade:** `is_master_user = 1`, `type = 'admin'`, role `ROLE_ADMIN`.
* **Membros e Unidade:** Vinculados à Unidade Matriz (`UN-MATRIZ-DEV`) e Tenant Master (`TNT-TOTUSTUUS`) via `user_memberships` (persona: `ADMIN`) e `user_units` (acesso: `full`).
* **Acesso Direto:** Redirecionamento nativo para o Portal do Desenvolvedor (`/developer/dashboard`) sem necessidade de seleção de tenant escolar.

---

## 3. Segurança de Identificadores (Mitigação de IDOR / OWASP)

* **Proibição de UUIDs Previsíveis/Nil (CWE-330):** É estritamente proibido o uso de UUIDs estáticos ou sequenciais como `00000000-0000-0000-0000-000000000001` no banco de dados Master ou em tenants. Todos os UUIDs devem ser gerados com **128 bits de entropia criptográfica** através de `\App\Support\Uuid::v4()`.
* **Proteção contra Enumeração:** A adoção de UUIDv4 randômicos impede que invasores tentem forjar requisições de API (`X-Tenant-ID`) adivinhando o identificador do tenant master.

---

## 4. Mecanismos de tenancy implementados

| Mecanismo | Implementação | Evidência |
|-----------|---------------|-----------|
| Contexto global | `TenantManager::current()` (singleton por request) | `app/Tenant/TenantManager.php` |
| Isolamento de dados | `tenant_id` (renomeado de `entity_id` em 14/07) em todas as tabelas multi-tenant | migrations `2026_07_14_*_rename_entity_id_to_tenant_id.php` |
| Scoping automático | Predicados explícitos em services/querys (não confiar em default global) | `app/Services/*` |
| Auth tenant-strict | `Auth::findUserByIdentifier` valida membership do tenant alvo; cross-tenant login bloqueado | FD-05 fix |
| Autorização por tenant | `StrictAuthorizeMiddleware` + checks BOLA/BFLA/BOPLA | config/security.php `authorization` |
| Rate limit por tenant | `TenantRateLimiter` (user 10/h, tenant 60/h, tenant 300/d) | config/security.php `rate_limiting` |
| Cache por tenant | `TenantCacheVault` | `app/Security/TenantCacheVault.php` |
| Branding por tenant | `OrganizationBranding` (logo, cores, favicon, portal domains) | `app/Models/OrganizationBranding.php` |
| Domínios custom | Portal domains mapeados por tenant (www → tenant) | `OrganizationBranding` + routes |
| i18n por tenant | locale por tenant + por user | `TenantLocale`/i18n service |
| Auditoria por tenant | Logs de entidade com `tenant_id` | `OrganizationAuditLog`, `AuditLog` |

---

## 5. Configurações por tenant

| Config | Model/Service |
|--------|---------------|
| Segurança | `TenantPrivacySetting` (mfa_required, session_timeout, lockout, password_policy) |
| Billing | `BillingSettings` + gateway config por tenant |
| Notificações | `NotificationChannel` por tenant |
| Integrações | `OrganizationIntegration` + `ThirdPartyIntegration` (credentials cifradas) |
| Feature flags | 🔲 pendente (Developer layer — Onda C) |

---

## 6. Regras de negócio tenancy

1. **Dados**: nenhuma query multi-tenant sem `tenant_id` do contexto (auditável).
2. **Auth**: usuário só acessa tenancy onde tem membership ativa.
3. **Admin**: superadmin (plataforma) tem visão cruzada limitada e auditada; admin de entity não cruza entities.
4. **Uploads**: assets referenciados por tenant; path contém tenant-id ofuscado via `AssetPathMapper`.
5. **Import/Export**: migração (MigrationController) opera estritamente dentro do tenant origem/destino.
6. **Provisionamento de Colégios**: cada nova escola contratada gera um banco isolado (`tt_tenant_{short_id}`) e seus usuários acadêmicos residem estritamente dentro do respectivo banco de dados da escola.

---

## 7. Testes de tenancy

- `tests/` — cobertura BOLA/BFLA/BOPLA.
- `tests/DeveloperPortalE2eTest.php` — 46 testes cobrindo navegação, autenticação e rotas administrativas do developer portal.
- `tests/TenantProvisioningHierarchyTest.php` — validação da hierarquia completa Client > Entity > Unit > TenantDatabase.
- `tests/ApiCrossTenantTest.php` — cobre proteção contra acesso cross-tenant na API.
