# SDD 10 — Governança & Entrega (TotusTuus SoftCloud)

> **Documento derivado do SDD mestre** · **Data:** 04/08/2026

---

## 1. Processo de entrega

**Especificação → Implementação → Verificação → Gate → Release**

- Cada módulo tem spec canônica em `docs/Nova pasta/spec_*.md` (39 specs atuais; consolidar duplicados).
- Implementação segue conventions (ver `AGENTS.md` e `docs/agent-stack/`).
- **Verificação obrigatória por entrega:** `php -l` + PHPUnit no módulo tocado.
- Gate de segurança (SG-01..SG-05) antes de cada marco (SDD-05).
- Cada alteração registrada (changelog por módulo em specs).

## 2. Critérios de aceite globais

| Critério | Estado atual |
|----------|--------------|
| Lint limpo (php -l) | ✅ verificado periodicamente |
| PHPUnit verde (142+ testes) | 🟡 verificar na Onda C |
| Sem warnings de deprecation | ✅ |
| Rotas apontam para controllers existentes | ✅ (grep verificado 04/08) |
| Views renderizam com dados vazios | ✅ (`?? []` convention) |
| Segurança: 0 críticos/altos abertos | ✅ (36 achados, 34 FIXED, 2 backlog) |
| i18n 100% chaves 10 locales | ✅ |
| SBOM + provenance (SLSA) | 🔴 pendente (Onda B) |
| PenTest suite completa | 🔴 ~20% (Onda B) |
| Integration Hub completo | 🟡 ~60% (Onda B) |

## 3. Tabela de módulos e responsáveis (RAI)

| Módulo | Dona(o) | Status |
|--------|:-------:|:------:|
| Auth/IAM/Security | Security | ✅ |
| Billing | Billing | ✅ (48 views) |
| Academic/Exams | Academic | ✅ |
| People/HR | People | ✅ |
| Compliance/Privacy | Compliance | ✅ |
| Migration/Import | Migration | ✅ (1.677 linhas) |
| Integration Hub | Integration | 🟡 ~60% |
| Developer/Ops | Developer | 🟡 ~55% |
| SLSA build | DevOps | 🔴 ~40% |
| PenTest suite | Security | 🔴 ~20% |

## 4. Ferramentas de entrega

| Ferramenta | Uso |
|------------|-----|
| Git (branch por feature) | versionamento |
| PHPUnit | testes (142+) |
| php -l | lint |
| composer audit | dependências |
| gitleaks | secrets scan |
| ZAP (nightly) | DAST |
| OpenCode + ag-kit + mantis | revisão/auditoria (docs/agent-stack/) |

## 5. Rotinas

- **Diária:** ZAP baseline em staging; revisão de alertas do AlertEngine.
- **Semanal:** composer audit; revisão de access logs; rotação de chaves quando aplicável.
- **Mensal:** restauração de backup testada; revisão de DSRs abertos; atualização de threat model.
- **Por release:** SBOM + provenance; revisão de findings abertos; gate SG-05.

## 6. Registro de decisões (ADR)

Ver SDD-02 §8 (ADR-01..05). Novas ADRs registradas em `docs/sdd/02-solution-architecture.md`.

## 7. Backlog priorizado (próximas entregas)

1. **Onda B (em andamento):** SLSA build pipeline (~40→100%), PenTest suite (~20→100%), Integration Hub (~60→100%).
2. **Onda C:** lint + PHPUnit nos módulos tocados; consolidar specs duplicados (gestão de bancos, notificações, soft-delete, SAC ×2).
3. **Dívida técnica:** refatorar LoggerController (5.254 linhas) e AcademicController (4.857) em services.
4. **Backlog segurança:** Vault KMS em prod, SBOM, CAPTCHA, DAST expansão.
