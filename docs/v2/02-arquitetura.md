# 02 — Arquitetura de Solução

> Parte do [SDD v2](00-README.md).

---

## 1. Estilo

**Monólito modular** com fronteiras explícitas por domínio, preparado para extrair serviços só quando houver motivo medido (escala, equipe ou requisito de isolamento).

Stack declarada na v1: PHP 8.2+, MVC próprio, PDO com MySQL 8 ou MariaDB 10.6+, frontend com `fetch()`, CSS com Tailwind CSS.

## 2. Camadas

```
Navegador (HTML progressivo + fetch, cookies HttpOnly)
  └─ Front controller (public/index.php)
       └─ Roteador  →  cadeia de middleware  →  Controller
            └─ Serviços de domínio (app/Services/<dominio>)
                 └─ Repositórios / Models (app/Models, sempre com escopo de tenant)
                      └─ Acesso a dados (PDO, prepared statements)
```

Regras:

- Controller não executa SQL. Ele chama serviço.
- Serviço não lê `$_SERVER`, `$_COOKIE` nem `$_SESSION` diretamente. Recebe um `RequestContext` (usuário, tenant, unidade, locale).
- Repositório aplica filtro de tenant em toda consulta. Consulta sem filtro falha em teste.

## 3. Ordem da cadeia de middleware

Ordem obrigatória para rotas web. Qualquer alteração exige ADR.

1. `SecurityHeaders` — CSP com nonce, HSTS, X-Frame-Options, nosniff, COOP/CORP, Referrer-Policy, Permissions-Policy.
2. `RequestId` + `LogContext` — correlação de logs (sem PII).
3. `RateLimit` por IP — limite antes da autenticação, para conter tentativas de login e de API.
4. `Csrf` — token sincronizador + validação de `Origin`/`Sec-Fetch-Site`.
5. `SessionSecurity` (idle, absolute, token de dispositivo, D-03) e `Auth` — exige identidade válida (ou rota pública explícita).
6. `TenantContext` — resolve tenant, entidade e unidade; rejeita contexto que o usuário não possui.
7. `Authorize` — permissão `modulo.recurso.acao` (default-deny).
8. `RateLimit` por identificador e por tenant — aplicado pelos serviços de login e de API, depois da identidade (ver [05](05-seguranca.md)).
9. `Audit` — registra ação sensível (sucesso e falha).

Rotas de API adicionam `ApiAuth` (Bearer), `HmacAuth` (webhooks/integrações), `ApiSchema` (validação e limite de payload) e `Idempotency` em operações não idempotentes.

## 4. Componentes

| Componente | Responsabilidade | Local declarado (v1) |
|---|---|---|
| Router | Mapeia método + caminho para controller | `app/Http/Router.php` |
| Middleware | Ver seção 3 | `app/Http/Middleware/` |
| Segurança | Senhas, JWT, MFA, CSRF, rate limit, cifragem | `app/Security/` |
| Tenant | Contexto de tenant por requisição | `app/Tenant/TenantManager.php` |
| Logs e auditoria | `SystemLogger`, `AuditLogService`, `AlertEngine`, `MetricsCollector` | `app/Services/` |
| Filas | Workers assíncronos | `scripts/` (ver [10](10-implantacao-operacao.md)) |
| Armazenamento | Uploads fora do webroot, acesso por controller | `app/Services/Storage` (**[Planejado]** consolidar) |

## 5. Dependências

- **Runtime:** somente pacotes Composer com versão fixada em `composer.lock`. Sem `@latest`.
- **Frontend:** pacotes npm com `package-lock.json`. Build gera CSS e JS locais. Recurso externo só entra se a decisão D-01 o previr, com SRI e domínio da lista aprovada ([08](08-frontend-design-system.md)).
- **Verificação:** `composer audit` e `npm audit` em CI, com falha em severidade alta ou crítica sem exceção registrada.
- **Proibido em pipeline de produção:** `npx <pkg>`, `bunx <pkg>`, `curl | sh` e instaladores que baixam o último release. A v1 citava esses comandos; a v2 os remove do fluxo de deploy.

## 6. ADRs

Data: 02/11/2026. Autor: responsável técnico (a nomear, ver [11](11-governanca-qualidade.md), seção 5). Status por ADR na última coluna.

| ADR | Decisão | Motivo | Status |
|---|---|---|---|
| ADR-01 | Monólito modular, não microsserviços | Menos superfície operacional; fronteiras preservam a extração futura | Aceita |
| ADR-02 | Namespaces PSR-4 `App\` e `TotusTuus\` | Bibliotecas internas testáveis e substituíveis | Aceita |
| ADR-03 | JWT só para clientes de API. Navegador usa sessão opaca no servidor | Revogação imediata e menos segredo exposto no cliente. A v1 usava JWT também no navegador com refresh rotativo | **Aceita por padrão (DP-10, [80](80-decisoes-por-padrao.md)), 04/11/2026** |
| ADR-04 | Algoritmo de JWT fixo em RS256 (rejeitar HS256 e `none`) | Evita confusão de algoritmo | Aceita |
| ADR-05 | Biblioteca própria de cofre (`TotusTuus\Vault`), com a chave-mestra fora do host da aplicação em produção. `FileVault` só em desenvolvimento. | Segredo em arquivo no mesmo host anula a proteção. Biblioteca própria dá controle, mas exige revisão de criptografia (ver [05](05-seguranca.md), seção 2) | **Aceita (D-02). Onde a chave-mestra fica: regra no DP-11 ([80](80-decisoes-por-padrao.md)); o produto concreto sai com a escolha do provedor de nuvem** |
| ADR-06 | Inglês canônico + locales traduzidos | Ver [09](09-internacionalizacao.md) | Aceita |
| ADR-07 | Sem JavaScript inline e sem atributos `on*=` em HTML | Compatível com CSP estrita | Aceita |
| ADR-08 | Um banco master e um banco por unidade (entidade + unidade). Conexão escolhida pela unidade autorizada na requisição. | Isolamento físico de dados entre unidades e entre entidades. Custo: operação de muitos bancos e consolidação por evento | Aceita (D-16, 02/11/2026) |

## 7. Escalabilidade

- Camada web sem estado local. Sessão em banco ou Redis.
- Cache com chave por tenant (`tenant_id` obrigatório na chave).
- Uploads em armazenamento de objetos ou volume dedicado, fora do diretório público.
- Filas com idempotência por chave de evento; reprocessamento não gera efeito duplicado.

## 8. Riscos arquiteturais conhecidos

| Risco | Efeito | Tratamento |
|---|---|---|
| Controllers muito grandes (a v1 cita 5.254 linhas e 4.857 linhas) | Difícil revisar e testar | Extrair serviços; limite de tamanho em revisão de código (ver [11](11-governanca-qualidade.md)) |
| Módulos recentes sem teste | Regressão silenciosa | Gate de cobertura para código novo |
| Cofre de arquivo em produção | Vazamento de segredo com acesso ao host | ADR-05 e D-02 |
| Acoplamento de view com estado de sessão | Vazamento entre usuários em cache | Cache de página com chave de usuário ou sem cache para páginas autenticadas |
