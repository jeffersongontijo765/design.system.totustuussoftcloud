# SDD 09 — Implantação & Operação (TotusTuus SoftCloud)

> **Documento derivado do SDD mestre** · **Data:** 04/08/2026

---

## 1. Requisitos de runtime

| Componente | Requisito |
|------------|-----------|
| PHP | 8.2+ (CSP nonce, sodium, JIT opcional) |
| Extensões | pdo_mysql, mbstring, sodium, openssl, fileinfo, intl, json, curl, pcntl (jobs), redis (opcional) |
| Database | MySQL 8 / MariaDB 10.6+ (InnoDB, utf8mb4) |
| Storage | Local (fora do webroot) ou S3-compatível |
| Cache | Redis (recomendado) ou arquivo |
| Queue | `scripts/async_event_worker.php`, `scripts/async_backup.php` (supervisord) |

## 2. Ambiente (config por env)

`APP_ENV=local|staging|production`, `APP_DEBUG` (false em prod), `APP_URL` canônico, HSTS forçado em prod, CORS whitelist por env (`config/cors.php`).

## 3. Deploy

**Pipeline (SLSA ~40% atual → 100% na Onda B):**
1. Lint (php -l) + PHPUnit + composer audit + gitleaks.
2. Build de artefato (phar ou zip) com **SBOM (backlog F-DO-02)** + provenance (SLSA) — plano: `docs/SLSA-IMPLEMENTATION-PLAN.md`.
3. Migrations versionadas (pastas `migrations/` + MigrationController).
4. Post-deploy smoke checks (health endpoints).

Documentação de referência:
- `docs/DEPLOYMENT_TASK_PLAN.md` (planos por nuvem)
- `docs/SLSA-IMPLEMENTATION-PLAN.md` (Onda B)
- `docs/Nova pasta/slsa-build-spec.md` (spec)

## 4. Operação

| Área | Ferramenta |
|------|------------|
| Logs | SystemLogger (estruturado, correlação), ErrorLog |
| Métricas | MetricsCollector |
| Alertas | AlertEngine (brute force, privilege escalation, mass export) |
| Auditoria | AuditLogService + views de auditoria |
| Backup | `scripts/async_backup.php` + policy (7 diários/4 semanais/12 mensais) |
| Jobs | async workers + MigrationExecutionJob |
| Health | health endpoints + runbook de incidentes (`docs/security/incident-response-runbook.md`) |

## 5. Segurança de operação

- Secrets em Vault (FileVault dev; KMS/HashiCorp prod — backlog F-02).
- `.env` fora do versionamento (`.gitignore`).
- PHP `error_reporting(E_ALL)`, `display_errors=0` prod, `log_errors=1`.
- Headers de segurança emitidos por middleware (ver SDD-05).
- Updates: composer audit em CI (obrigatório), revisão semanal.

## 6. Observabilidade (views disponíveis)

- Logger admin (5.254 linhas — maior controller; refatorar na Onda C).
- Metrics views + SSE logger (`SseResponse.php`).
- Integration Hub (699 linhas) para monitorar entregas.

## 7. Checklist de go-live

- [ ] APP_DEBUG=false, display_errors=0
- [ ] HTTPS/HSTS habilitado (cert validado)
- [ ] Vault prod (KMS/HashiCorp) ativado — migrar de FileVault
- [ ] Rate limits configurados por ambiente
- [ ] Backups testados (restore drill)
- [ ] SBOM gerado + assinado
- [ ] Smoke tests pós-deploy verdes
- [ ] Secrets não presentes em repositório (gitleaks limpo)
- [ ] ZAP scan baseline sem abertos ≥ médio
- [ ] Composer audit sem vulnerabilidades
