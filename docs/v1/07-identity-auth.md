# SDD 07 — Identidade, Autenticação & Autorização (TotusTuus SoftCloud)

> **Documento derivado do SDD mestre** · **Data:** 04/08/2026
> **Auditado:** 10-11/07/2026 (34/36 fixados) · **Detalhes:** `docs/security/audit-2026-07-10.md`

---

## 1. Identidade

| Identidade | Modelo | Descrição |
|------------|--------|-----------|
| **Super Admin Global (Master)** | `User` (`is_master_user = 1`, `type = 'admin'`) | Gestores globais da software house vinculados à Sede Matriz (`UN-MATRIZ-DEV`), acesso nativo ao Portal do Desenvolvedor |
| Humano (staff/teacher/student/parents) | `User` + `UserProfile*` | nome, avatar, bios, fones, emails, endereço, família, documentos |
| Técnico (serviço) | `OrganizationIntegration`/`ThirdPartyIntegration` | client_id/secret cifrados |
| Invitado | `Invitation` | convite com token de aceite, expiração, role |
| Dispositivo | `DeviceTrust` | confiança de dispositivo para MFA step-up |

## 2. Fluxo de autenticação

```
Login → RateLimit(5/h/identificador) → Argon2id verify + pepper → 
MFA (se exigido) → WebAuthn/TOTP/cert → Session com idle 30min/absolute 12h/max 3
→ Regeneração de session id → AuditLog de login (sucesso e falha)
```

- Passwords com política: comprimento, complexidade, breach-check contra dicionário local, rotatividade.
- Password reset: token single-use, expiração curta, invalidar tokens antigos, lockout por tentativas.
- Logout em todos os dispositivos (blacklist jti + invalidação de sessões).

## 3. MFA (forte)

| Método | Status |
|--------|--------|
| TOTP (app autenticador) | ✅ |
| WebAuthn/passkey | ✅ (WebAuthnManager) |
| Certificado (PKI) | ✅ (CertificateAuth) |
| Email/SMS/Tele | ❌ **rejeitados** (design decision — anti-SIM-swap/phishing) |

- Rate limit por device (5/h), jitter, lockout progressivo.
- Step-up para ações sensíveis (admin ops, mudança de segurança, exports).

## 4. Autorização (RBAC)

- `Role` ↔ `Permission` (sintaxe `admin.<module>.<action>` e `portal.<modulo>.<acao>`).
- `UserMembership` liga user→tenant com role(s).
- `UserUnit` restringe a unidade.
- `AuthorizeMiddleware` (permissão), `StrictAuthorizeMiddleware` (default-deny + BOLA/BFLA/BOPLA), `AdminMiddleware`, `PortalMiddleware`.
- Delegation: `IdentityAutomation` (aprovações automáticas), `AccessRequest` (solicitação de acesso).

## 5. Controles de sessão

- Idle 30 min, absolute 12 h, máx 3 sessões concorrentes, bind IP+UA.
- Cookie Secure+HttpOnly+SameSite=Strict, rotação a cada 5 min.
- JWT: RS256, exp curto, refresh rotativo com rotação de jti, blacklist para revogação.
- `UserSessionEvent` — trilha de eventos de sessão (criação, rotação, término, revogação).

## 6. Padrões a evitar (não-negócios)

- Senhas em texto plano/hash fraco (proibido — Argon2id obrigatório).
- Tokens no JS/localStorage (proibido — cookies HttpOnly).
- HS256 para JWT (proibido — RS256).
- MFA fraca por SMS/email (proibido).
- Cross-tenant login (bloqueado por design — FD-05).

## 7. Testes de identidade (já existentes)

- Autenticação com tenants e privilégios cruzados, reset de senha, guest tokens, device trust, idempotência de login — ver `tests/` (GAP_ANALYSIS_2026-08-04.md).

## 8. Lacunas

| Lacuna | Ação |
|--------|------|
| SSO SAML/OIDC como IdP | Onda C (só SP WebAuthn hoje) |
| FIDO2 discovery (passkeys em browsers) | Melhoria contínua |
| Registro de users por tenant (self-service) | Existe via convite; reforçar rate limit |
