# SDD 02 — Arquitetura de Solução (TotusTuus SoftCloud)

> **Documento derivado do SDD mestre** · **Data:** 04/08/2026

---

## 1. Estilo arquitetural

**Monólito modular** com boundaries rígidos entre domínios, preparado para extração seletiva de serviços. PHP 8 puro, MVC próprio (`App\Http\Controllers`, `App\Services`, `App\Models`, `App\View`), REST-first com contratos JSON versionados (`/api/v1/...`).

## 2. Camadas

```
Browser (Tailwind 4.4 + fetch())
  └─ Router (app/Http/Router.php) → Middleware chain (20 middlewares)
       └─ Controllers (app/Http/Controllers/{Admin,Api,Teacher,Student,Parents,Thirdparty})
            └─ Services (app/Services/*  — 14 domínios)
                 └─ Models (app/Models/* — 74)
                      └─ Database (app/Database/Connection — PDO)
```

### Middleware chain (ordem)

`SecurityHeaders → SessionSecurity → Csrf → Auth → Authorize → StrictAuthorize → RateLimit → Audit → ApiSecurity/ApiSchema (API)`

## 3. Tenancy

- `TenantManager::current()` (app/Tenant/TenantManager.php) — contexto global por request.
- Predicados explícitos `tenant_id` em todas as queries multi-tenant.
- `Auth::findUserByIdentifier` tenant-strict (cross-tenant login bloqueado — FD-05).
- `StrictAuthorizeMiddleware` default-deny + validação BOLA/BFLA/BOPLA (config/security.php authorization).
- `TenantRateLimiter` para rate limit por tenant+user.

## 4. Frontend progressivo & Design System Master

- **Página Modelo de Referência Oficial:** `https://localhost/totustuussoftcloud/developer/settings/billing/modules` (view: `resources/views/app/pages/developer/modules.php`).
- **Especificação Canônica Completa de Navegação e Páginas:** `docs/sdd/12-portals-navigation-sidebar-pages-spec.md`.
- **Arquitetura Multi-Portal (6 Portais):**
  - Portal do Desenvolvedor (`docs/portais/portal-do-desenvolvedor-completo.md`)
  - SAAS Acadêmico (`docs/portais/saas-academico-completo.md`)
  - Portal do Professor (`docs/portais/portal-do-professor-completo.md`)
  - Portal do Aluno (`docs/portais/portal-do-aluno-completo.md`)
  - Portal dos Pais e Responsáveis (`docs/portais/portal-dos-pais-responsaveis-completo.md`)
  - Portal de Terceiros (`docs/portais/portal-de-terceiros-completo.md`)
- **Skills Normativas Aplicadas:**
  - `totustuus-layout-design/SKILL.md`: Checklist obrigatória de 21 itens, 5-View TABs (`KPI`, `Data Table`, `Cards/Grid`, `Kanban`, `Analytics/Charts`), 7 formatos de exportação, 3 drawers operacionais, colunas fixas e zero inline JS.
  - `totustuus-security-auditor-v3/SKILL.md`: ASVS Level 2, OWASP Top 10:2025, Attack Surface Management (ASM), AppSec testing (SAST/DAST/SCA), DevSecOps, pentest estruturado, bug bounty/VDP, isolamento tenant-strict, proteção contra BOLA/BFLA, Argon2id (OWASP 2025) e CSP Nonce universal.
- **Design System:** Supabase Theme Dark Emerald com paleta 3-Layer Dark (`#14171c` canvas, `#1a1d24` outer box, `#242832` surface/cards, `#10b981` emerald accent).
- **Padrão de Ícones:** **FontAwesome Pro 7.2 Light (`fa-light`)** em toda a interface (ações, tabelas, dropdowns e drawers).
- **Navegação Segmentada Unificada:** Segmented Pill Tabs (`.ud-tab-segmented`, `.ud-tab-btn`, `.ud-tab-badge`) suportando 5 visões (KPIs, Data Table, Grid/Cards, Kanban Swimlanes com drag-and-drop nativo, Analytics/Charts).
- **Toolbar & Exportação:** Dropdown de 7 formatos (CSV, XLSX, PDF, JSON, XML, SQL, TXT) com ícones uniformes em `fa-light` e badges `.ext`.
- **Ações e Sincronização:** Seção `$this->start('actions')` no cabeçalho (com timestamp `Synced: HH:MM:SS`) e botão de recarregamento AJAX dedicado na toolbar (`[ 🔄 Sincronizar ]`).
- **Bimoeda & i18n:** Suporte bimoeda USD/BRL e matriz de 10 locales (`en`, `pt-br`, `es`, `fr`, `de`, `it`, `zh`, `ja`, `ru`, `ar`) com auto-tradução.
- **Drawers Seguros:** Padrão Supabase com backdrop blur, validação em tempo real e destravamento por palavra-chave para ações críticas (`DELETE`/`ARCHIVE`).
- **Comunicação Assíncrona:** Requisições via `fetch()` nativo com cookies HttpOnly (`credentials: 'include'`), sem tokens no JS (A-001/A-004), e Nonce CSP em todos os scripts.

## 5. Segurança (resumo)

Ver `docs/security/control-matrix.md` e `docs/security/findings-register.md`. Destaques: Argon2id OWASP 2025, JWT RS256, CSP+Trusted Types, MFA forte, LGPD instrumentado, audit trail completo, CI com composer audit + gitleaks + ZAP nightly.

## 6. Observabilidade

- `SystemLogger` (app/Services/SystemLogger.php) — logs estruturados por correlação.
- `AuditLogService` — trilha de auditoria de negócio.
- `AlertEngine` — alertas (brute force, privilege escalation, mass export).
- `MetricsCollector` — métricas de sistema.
- `app/Http/SseResponse.php` — streaming de eventos (SSE) para logger em tempo real.

## 7. Escalabilidade

- App stateless no layer web; sessões prontas para backend compartilhado (driver database).
- Filas assíncronas: `scripts/async_event_worker.php`, `scripts/async_backup.php`.
- Cache por contexto/tenant (`app/Services/Cache/`, `app/Security/TenantCacheVault.php`).
- Storage externalizável (uploads fora do webroot; imagens via `AssetPathMapper`).

## 8. Decisões arquiteturais chave (ADR resumido)

| ADR | Decisão | Motivo |
|-----|---------|--------|
| ADR-01 | Monólito modular vs microservices | Reduz complexidade inicial, preserva boundaries para extração |
| ADR-02 | PSR-4 App\ + TotusTuus\ vendor/custom | Bibliotecas internas testáveis e substituíveis |
| ADR-03 | JWT RS256 obrigatório (HS256 bloqueado) | Previne forgery de token simétrico |
| ADR-04 | Vault abstraction (File→KMS/HashiCorp) | Secrets fora do código e do .env |
| ADR-05 | i18n inglês canônico + 10 locales | Internacionalização desde a base |

## 9. Riscos arquiteturais atuais

| Risco | Mitigação |
|-------|-----------|
| Controllers gigantes (Logger 5.254, Academic 4.857) | Refatoração incremental em services — Onda C (dívida técnica) |
| Migration/IntegrationHub recém-criados sem testes | Criar testes — Onda C |
| Vault file-backed em prod | Ativar KMS/HashiCorp provider (backlog F-02) |
