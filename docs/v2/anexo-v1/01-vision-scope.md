# SDD 01 — Visão & Escopo (TotusTuus SoftCloud)

> **Documento derivado do SDD mestre** (`docs/sdd-mestre-php8-mvc-saas.md`)
> **Data:** 04/08/2026 · **Status:** vigente

---

## 1. Visão do produto

Plataforma SaaS multi-tenant para ecossistema educacional (multi-entity, multi-unit, multi-user), em PHP 8 puro com MVC próprio, API RESTful versionada, frontend progressivo com `fetch()`, design system Tailwind 4.4 e bibliotecas internas sem dependência de runtime externa.

Três camadas de produto:
1. **Website** — institucional/comercial (SEO, onboarding, central de ajuda).
2. **SaaS Admin** — operação do produto (superadmin, admin entidade, gestor unidade, usuários de negócio).
3. **Developer** — administração técnica (feature flags, API keys, webhooks, observabilidade, auditoria, jobs).

## 2. Objetivos estratégicos

- Segregação forte de dados/configuração/branding por entity.
- Operação descentralizada por unit com controle contextual.
- API REST versionada para web, integrações e automações.
- Segurança, rastreabilidade, auditoria e escalabilidade horizontal desde a base.
- i18n: inglês canônico + en, pt-BR, es, fr, de, it, zh, ja, ru, ar (100% chaves em 10 locales — verificado 04/08/2026).

## 3. Escopo — status real (04/08/2026)

| Escopo | Status | Evidência |
|--------|:------:|-----------|
| Website (home, topbar portais, SAC, FAQ, i18n) | ✅ ~95% | `resources/views/web/pages/home.php` + rotas web 2.461 |
| SaaS Admin (52 controllers admin) | ✅ ~90% | `app/Http/Controllers/Admin/` |
| Developer layer | 🟡 ~55% | `DeveloperController.php` 262 linhas + 8 views |
| API REST v1 | ✅ | `routes/api.php` 380 rotas + Api*Middleware |
| Portais (teacher/student/parents/thirdparty) | ✅ ~90% | 4 controllers + 96 views |
| Autenticação + IAM | ✅ ~90% | 33 classes Security + auth views |
| LGPD/Privacidade | ✅ ~85% | Privacy + PrivacyCompliance + compliance 62 views |
| i18n 10 locales | ✅ 100% chaves | testes I18n* passando |

## 4. Fora do escopo (não incluso nesta versão)

- Aplicativos nativos iOS/Android (mobile web responsivo apenas).
- Integrações de gateway de pagamento em produção (adapters prontos: Asaas, MercadoPago, Pix, Stripe, PagSeguro — ativar via config).
- Infraestrutura cloud específica (documentada em `docs/DEPLOYMENT_TASK_PLAN.md`).

## 5. Critérios de aceite de escopo

- [ ] Todas as rotas referenciam controllers existentes (php -l + smoke).
- [ ] Views renderizam sem warning com dados vazios (`?? []`).
- [ ] Testes PHPUnit dos módulos escopados passam.
- [ ] Nenhum endpoint sem middleware de autorização (default-deny).

## 6. Métricas do projeto (04/08/2026)

| Métrica | Valor |
|---------|:-----:|
| Controllers Admin | 52 (até 5.254 linhas cada) |
| Views app/pages | ~1.600+ em 50+ dirs |
| Rotas | ~3.370 |
| Services | 14 dirs / 22 arquivos Billing |
| Models | 74 |
| Testes | 142+ |
| Middleware | 20 |
| Security classes | 33 |
