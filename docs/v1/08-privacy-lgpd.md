# SDD 08 — Privacidade & LGPD (TotusTuus SoftCloud)

> **Documento derivado do SDD mestre** · **Data:** 04/08/2026

---

## 1. Compromisso

Tratamento de dados pessoais em conformidade com LGPD (Lei 13.709/2018), com bases legais, consentimento granular, DSR e instrumentação de incidentes 72h.

## 2. Instrumentação implementada

| Funcionalidade | Implementação |
|----------------|---------------|
| Consentimento | `UserConsent`, `PrivacyConsentEvent` (consentimento explícito, revogável, com versão) |
| Cookie consent | `UserCookieConsent` + `UserCookieConsentItem`, `CookieCatalog`, `CookieCategory`, `ConsentBannerVersion` |
| Preferências de privacidade | `UserPrivacyPreferences`, `PrivacyPreference` |
| Config por tenant | `TenantPrivacySetting` (retenção, mfa_required, etc.) |
| DSR (dados pessoais) | `PrivacyDataSubjectRequest` + workflow (acesso, correção, portabilidade, eliminação, revogação, opor) |
| DPO | `PrivacyOfficer` (nome/contato por tenant) |
| Auditoria | `PrivacyAuditLog` + `PrivacyComplianceController` (compliance 62 views) |
| Incidentes | `ANPDReporter` + `docs/security/breach-template-anpd.md` (Art. 48, 72h) |
| Minimização | Logs sem PII (LogTruncation), retenção configurável |

## 3. Bases legais (implementadas)

- Consentimento explícito (consent records versionados).
- Contrato/legítimo interesse (termos + política, com histórico).
- Obrigação legal (retenção fiscal, ANPD).
- Direitos: acesso, correção, portabilidade, eliminação, revogação, oposição, não-decisão automatizada.

## 4. Ciclo de vida de dados

```
Coleta (consent/bases) → Armazenamento (cifrado AES-256-GCM; backups) →
Uso (tenant-scoped) → Compartilhamento (somente com consentimento; integrações) →
Retenção (config por tenant) → Eliminação (soft/hard delete; DSR)
```

## 5. Dados pessoais sensíveis

- Biométricos (WebAuthn credenciais → cifradas em vault-adjacent storage).
- Documentos (upload com AccessControl + cifragem).
- Saúde/educação (grade, matrículas — tenant-scoped).
- Minors: consentimento parental (modelos `*Parent*`).

## 6. Prazos de retenção (configurável por tenant)

- Sessões/logs: config (default em `config/security.php`).
- DSR: registro por 5 anos (obrigação legal).
- Dados não necessários: eliminados após DSR.

## 7. Métricas

- **~85% implementado** (GAP_ANALYSIS_2026-08-04.md).
- Compliance views: 62 (módulo compliance).
- Testes: Privacy/Consent/Cookie/DSR test classes (ver tests/).

## 8. Lacunas

| Lacuna | Ação |
|--------|------|
| DSR workflow de ponta-a-ponta com interface | Reforçar views (algumas existem) |
| Minimização automática (pseudo-anonimização) | Melhoria contínua |
| Mapeamento de dados (records of processing) | Criar documento de registro de operações (ROPA) |
| ANPD contactos por tenant preenchidos | Validar dados de `PrivacyOfficer` por tenant |
