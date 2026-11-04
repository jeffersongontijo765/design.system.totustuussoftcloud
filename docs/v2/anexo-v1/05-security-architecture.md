# SDD 05 — Arquitetura de Segurança (TotusTuus SoftCloud)

> **Documento derivado do SDD mestre** · **Data:** 04/08/2026
> **Detalhes completos:** `docs/security/control-matrix.md`, `docs/security/findings-register.md`, `docs/threat-model-STRIDE.md`, `docs/MASTER_AUDIT_REPORT_2026-07-11.md`, `docs/security/audit-2026-07-10.md`

---

## 1. Postura atual

- **Nível de risco: BAIXO** (auditorias 10-11/07/2026, validadas 04/08/2026).
- **36 achados** registrados → **34 FIXED**, 2 backlog (Vault KMS, SBOM).
- **0 críticos / 0 altos / 0 médios abertos.** CVSS residual máx 2.0.

## 2. Principais controles (resumo)

| Área | Controle |
|------|----------|
| Senhas | Argon2id m=65536 (64MiB), t=4, p=2, hash 32B + salt 32B (sodium) + pepper HMAC-SHA256 via Vault |
| MFA | TOTP/WebAuthn/passkey/cert apenas (email/SMS/Tele rejeitados) |
| Tokens | JWT RS256 (HS256 bloqueado), blacklist jti, rotação de chaves, refresh rotativo |
| Sessão | idle 30min, absolute 12h, máx 3 concorrentes, bind IP+UA, regeneração pós-login |
| Cookies | Secure+HttpOnly+SameSite=Strict, rotação 5min |
| Headers | CSP nonce + Trusted Types, HSTS preload, XFO DENY, nosniff, COOP/CORP, Referrer-Policy, Permissions-Policy |
| CSRF | Double-submit + Origin/Referer |
| AuthZ | Default-deny global, BOLA/BFLA/BOPLA, RBAC por permissão, tenant scoping |
| Rate limit | Global + por identificador + por tenant + por IP |
| Uploads | MIME/magic/ext whitelist, rename, fora do webroot |
| Dados | AES-256-GCM + HKDF-SHA256 + envelope versionado |
| Secrets | Vault abstraction (FileVault ativo; KMS/HashiCorp prontos) |
| LGPD | Consentimento, DSR, DPO, breach 72h (ANPDReporter), sem PII em logs |

## 3. Gates de segurança do SDD

| Gate | Momento | Aprovador |
|------|---------|-----------|
| SG-01 | Fechamento arquitetura base | Oracle + Security Auditor v3 |
| SG-02 | Fechamento Auth/ACL/Tenancy | Mantis + Security Auditor v3 |
| SG-03 | Antes de módulos sensíveis | Orchestrator + Mantis + Security Auditor v3 |
| SG-04 | Antes de homologação | Mantis + Fable Judge + Security Auditor v3 |
| SG-05 | Antes de release | Security Council + Security Auditor v3 |

**Estado:** SG-01..SG-04 validados; auditoria contínua e quality gates orientados a CI operando com a skill unificada `totustuus-security-auditor-v3` (`.agents/skills/totustuus-security-auditor-v3/SKILL.md`) cobrindo ASM, SAST, DAST, Argon2id, Multi-Tenancy e LGPD.

## 4. Segurança por camada (implementação real)

- **app/Security/** (33 classes): PasswordManager, Argon2idProfile/Sodium, JWTManager, OAuthManager, WebAuthnManager, MFAManager, Totp, Base32, Csrf, RateLimiter, AuthorizationGuard, SessionSecurityService, RiskEngine, GeoLocationService, ClientIp, CspNonce, DataEncryption, KeyManager, TokenManager, Vault+Providers (File/HashiCorp/AwsKms), TenantCacheVault, ANPDReporter, AssetProtection, ImageProtection, AssetPathMapper, Ulid.
- **Middleware** (20): SecurityHeaders, Security, SessionSecurity, Csrf, Auth, Guest, Admin, Portal, Authorize, StrictAuthorize, ApiAuth, ApiSecurity, ApiSchema, RateLimit, Audit, HmacAuth, Idempotency, InstallToken, LogTruncation.

## 5. Threat model

- STRIDE documentado em `docs/threat-model-STRIDE.md`.
- Superfícies: auth, API, CRUD genérico, uploads, webhooks, admin tools, tenancy.
- Mitigações ativas para cada categoria STRIDE (ver control-matrix).

## 6. Resposta a incidentes

- `docs/security/incident-response-runbook.md` (tempos: crítico 1h, alto 4h, médio 24h, baixo 72h).
- `docs/security/breach-template-anpd.md` (LGPD Art. 48 — 72h ANPD).
- `ANPDReporter::report()` instrumentado.

## 7. Melhorias planejadas (backlog)

| Item | Prioridade |
|------|-----------|
| Ativar AwsKmsVaultProvider/HashiCorpVaultProvider em produção (F-02) | Alta |
| SBOM + provenance no build (SLSA) | Média (Onda B) |
| CAPTCHA real (reCAPTCHA/Turnstile) — config já prevê `captcha_after_attempts` | Média |
| Expansão DAST (ZAP) | Média |
| Auditoria de secrets em CI (gitleaks já) + dependency scanning periódico | Baixa |
