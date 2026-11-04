# SDD 04 — Padrões de API (TotusTuus SoftCloud)

> **Documento derivado do SDD mestre** · **Data:** 04/08/2026

---

## 1. Contratos

- **Base:** `/api/v1/...`
- **Formato:** JSON.
- **Resposta padrão:**
```json
{ "success": true, "data": { ... }, "message": "ok" }
{ "success": false, "error": "code", "message": "descrição" }
```
- **Status HTTP:** 200/201/204/400/401/403/404/409/422/429/500.
- **Idempotência:** endpoints sensíveis usam `IdempotencyMiddleware` (chave = método+path+body hash) — ver `app/Http/Middleware/IdempotencyMiddleware.php`.

## 2. Autenticação de API

| Mecanismo | Uso | Evidência |
|-----------|-----|-----------|
| Cookies HttpOnly (sessão) | Frontend web — `credentials: 'include'` | `assets/js/api.js` |
| JWT RS256 Bearer | Clientes técnicos | `config/jwt.php` |
| HMAC (X-Signature + X-Nonce ±300s) | Webhooks/integrações SAC | `app/Http/Middleware/HmacAuthMiddleware.php` |
| API keys | Integrações (OrganizationIntegration) | routes/integrations.php |

## 3. Autorização de API

- `ApiAuthMiddleware` → valida autenticação.
- `ApiSecurityMiddleware` → headers/rate limit.
- `ApiSchemaMiddleware` → valida payload (schema, max 1MB).
- `StrictAuthorizeMiddleware` global default-deny; permissões via `AuthorizeMiddleware` (`admin.<module>.<action>`).
- Tenant scoping obrigatório (BOLA check).

## 4. Versionamento e evolução

- Versionado no path (`/api/v1/`). Nova versão quebra → `/api/v2/` com controller dedicado.
- Mudanças aditivas são seguras na v1.
- `docs/api-docs.php` + `docs/api-docs-json.php` geram documentação (ApiDocsController).

## 5. Rate limiting

| Escopo | Limite | Evidência |
|--------|--------|-----------|
| API global | 60/min, burst 10 | config/security.php api |
| Login/MFA/forgot/reset | por identificador (5/h) + IP lockout | RateLimitMiddleware |
| CNPJ/tenant | 10/h user, 60/h tenant, 300/d tenant | TenantRateLimiter |
| JWT | 100/h | config/jwt.php |

## 6. Padrões de erro

- Erros genéricos em prod (`config/security.php` errors: sem stack, sem SQL).
- Códigos de erro estáveis (`validation_failed`, `unauthorized`, `forbidden`, `not_found`, `rate_limited`, `conflict`, `internal`).
- Logs de erro via SystemLogger sem PII.

## 7. Paginação e filtros

- Listas grandes paginadas (`page`, `per_page` máx 100) e filtráveis.
- Ordenação por whitelist de colunas (anti-SQLi).
- Ex.: rotas `GET /api/v1/<resource>?page=1&per_page=50&filter[...]`.

## 8. Webhooks

- Assinatura HMAC obrigatória (X-Signature, X-Nonce dedup → replay protegido, FD-29/FD-30).
- Delivery status rastreado (WebhookDeliveryApiTest).
- Integração com Integration Hub (Onda B) para gerenciamento de endpoints.

## 9. Checklist de aceite de endpoint

- [ ] Autenticação (quando requerida) no middleware da rota.
- [ ] Autorização granular por permissão.
- [ ] Tenant scope explícito na query.
- [ ] Rate limit aplicável configurado.
- [ ] Input validado (schema) + payload ≤ 1MB.
- [ ] Resposta no contrato `{success, data, message}`.
- [ ] Idempotência para ações não-idempotentes.
- [ ] Teste PHPUnit quando crítico.
