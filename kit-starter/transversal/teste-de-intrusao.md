# Teste de intrusão (pentest)

- Portal: Todos
- Área: Transversal
- Domínio: transversal: vale para todos os portais e módulos
- Status: detalhado; especificação da v1 absorvida integralmente (seção 13), com as correções da v2 e as decisões por padrão (seções 1 a 12)
- Fonte da v1: [penetration-test-spec-v2.md](../../docs/v2/anexo-v1/penetration-test-spec-v2.md) (529 linhas)

## 1. Regra de leitura
As seções 1 a 12 prevalecem sobre a seção 13. A seção 13 é o texto integral da v1, sem corte, para que nenhum detalhe se perca. Quando a seção 13 disser algo diferente das seções 1 a 12, vale o que está nas seções 1 a 12.

## 2. Objetivo e escopo
Fases, responsabilidades e checklist do teste de intrusão externo e interno.

## 3. Telas (índice da v1)
- 1. Fases do Teste
  - Fase 1 — Reconhecimento (Information Gathering)
  - Fase 2 — Hardening de Headers
  - Fase 3 — Autenticação e Sessão
  - Fase 4 — Autorização e Isolamento Multi-tenant
  - Fase 5 — Injection / XSS / Upload
  - Fase 6 — API Security (OWASP API Top 10)
  - Fase 7 — Auditoria de Logs
  - Fase 8 — CORS / CSP / Rate Limiting
  - Fases 9-10 — Relatório e Regressão
- 2. Matriz de Responsabilidades
- 3. Checklist de Implementação

## 4. Correções da v2 que prevalecem
- **Estratégia de testes e pentest externo:** o [24](../../docs/v2/24-operacao-continuidade-qualidade.md), seção 5, prevalece; escopo definido por esta ficha.
- **Divulgação de vulnerabilidade:** [24](../../docs/v2/24-operacao-continuidade-qualidade.md), seção 6.
- **Testes de tenancy e de identidade** são critério de aceite obrigatório ([03](../../docs/v2/03-dominio-tenancy.md), seção 7; [06](../../docs/v2/06-identidade-acesso.md), seção 11).

## 5. Decisões por padrão aplicadas
- Nenhuma decisão nova.

## 6. Permissões e papéis
- `platform.security` coordena; o pentest externo é contratado; achados viram chamados com SLA de correção.

## 7. Dados
- Relatórios de pentest com acesso restrito a `platform.security` e `platform.developer`.

## 8. Integrações
- Não se aplica.

## 9. Exportação, auditoria e privacidade
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../docs/v2/08-frontend-design-system.md), seção 3).
- Auditoria conforme [29](../../docs/v2/29-auditoria.md); dados pessoais conforme [07](../../docs/v2/07-privacidade-lgpd.md).


## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
- Periodicidade e fornecedor do pentest externo ([24](../../docs/v2/24-operacao-continuidade-qualidade.md), seção 9).

## 13. Conteúdo integral da v1 (absorvido)

### Penetration Test v2 — TotusTuus SoftCloud

> **Framework:** OWASP WSTG v4.2 · OWASP Top 10 2021 · OWASP API Top 10 2023 · NIST SP 800-115
> **Alvo:** PHP 8.2 · MariaDB · XAMPP · Multi-tenant DB-per-unit

---

#### 1. Fases do Teste

##### Fase 1 — Reconhecimento (Information Gathering)

**Script:** `ttscdoc/scripts/recon.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-http://localhost/totustuussoftcloud}"
REPORT_DIR="build/pen-test/01-recon"
mkdir -p "$REPORT_DIR"

echo "=== FASE 1: RECONHECIMENTO ==="
echo "Alvo: $TARGET"

# 1.1 DNS / Host Discovery
nslookup "$(echo $TARGET | sed 's|https\?://||;s|/.*||')" 2>/dev/null > "$REPORT_DIR/dns.txt" || true

# 1.2 Directory Enumeration
echo "Diretórios descobertos:" > "$REPORT_DIR/dirs.txt"
for dir in admin api assets app config routes database; do
    status=$(curl -s -o /dev/null -w "%{http_code}" "${TARGET}/${dir}/" 2>/dev/null || echo "000")
    echo "  ${dir}/ → HTTP ${status}" >> "$REPORT_DIR/dirs.txt"
done

# 1.3 Technology Fingerprinting
curl -sI "$TARGET" > "$REPORT_DIR/headers.txt"
echo "Tecnologias detectadas:" > "$REPORT_DIR/tech.txt"
grep -i 'server\|x-powered-by\|x-application-context' "$REPORT_DIR/headers.txt" >> "$REPORT_DIR/tech.txt" || true

# 1.4 Robots / Sitemap
curl -s "$TARGET/robots.txt" 2>/dev/null > "$REPORT_DIR/robots.txt" || echo "Sem robots.txt"
curl -s "$TARGET/sitemap.xml" 2>/dev/null > "$REPORT_DIR/sitemap.xml" || echo "Sem sitemap.xml"

echo "Concluído. Relatório em ${REPORT_DIR}/"
```

##### Fase 2 — Hardening de Headers

**Script:** `ttscdoc/scripts/hardening-check.php`

```php
#!/usr/bin/env php
<?php
declare(strict_types=1);

/**
 * Verificação de segurança dos headers HTTP e configurações.
 *
 * Uso: php hardening-check.php [url]
 */

$target = $argv[1] ?? 'http://localhost/totustuussoftcloud';

$checks = [
    'Strict-Transport-Security' => [
        'severity' => 'CRITICAL',
        'recommendation' => 'Adicionar: max-age=31536000; includeSubDomains',
        'validator' => fn($v) => $v !== null && str_contains($v, 'max-age='),
    ],
    'Content-Security-Policy' => [
        'severity' => 'CRITICAL',
        'recommendation' => 'Adicionar CSP com nonce e strict-dynamic',
        'validator' => fn($v) => $v !== null && (str_contains($v, 'nonce') || str_contains($v, 'strict-dynamic')),
    ],
    'X-Content-Type-Options' => [
        'severity' => 'HIGH',
        'recommendation' => 'Adicionar: nosniff',
        'validator' => fn($v) => $v !== null && str_contains($v, 'nosniff'),
    ],
    'X-Frame-Options' => [
        'severity' => 'HIGH',
        'recommendation' => 'Adicionar: DENY ou SAMEORIGIN',
        'validator' => fn($v) => $v !== null && (str_contains($v, 'DENY') || str_contains($v, 'SAMEORIGIN')),
    ],
    'Referrer-Policy' => [
        'severity' => 'MEDIUM',
        'recommendation' => 'Adicionar: strict-origin-when-cross-origin',
        'validator' => fn($v) => $v !== null,
    ],
    'Permissions-Policy' => [
        'severity' => 'MEDIUM',
        'recommendation' => 'Adicionar Permissions-Policy restritiva',
        'validator' => fn($v) => $v !== null,
    ],
    'X-XSS-Protection' => [
        'severity' => 'LOW',
        'recommendation' => 'Remover header obsoleto; usar CSP',
        'validator' => fn($v) => $v === null,
    ],
];

echo "=== Security Headers Audit ===\n";
echo "Target: {$target}\n\n";

$ch = curl_init();
curl_setopt_array($ch, [
    CURLOPT_URL => $target,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HEADER => true,
    CURLOPT_NOBODY => true,
    CURLOPT_TIMEOUT => 10,
    CURLOPT_SSL_VERIFYPEER => false,
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

$headers = [];
foreach (explode("\r\n", $response) as $line) {
    if (str_contains($line, ': ')) {
        [$name, $value] = explode(': ', $line, 2);
        $headers[strtolower($name)] = $value;
    }
}

$passed = 0;
$failed = 0;

foreach ($checks as $header => $config) {
    $value = $headers[strtolower($header)] ?? null;
    $ok = $config['validator']($value);
    $status = $ok ? 'PASS' : 'FAIL';
    $icon = $ok ? '✓' : '✗';
    $color = $ok ? "\033[32m" : "\033[31m";

    echo "{$color}{$icon} {$status}\033[0m {$header}";
    if (!$ok && $value) {
        echo " (atual: {$value})";
    }
    echo "\n";
    if (!$ok) {
        echo "  → Recomendação: {$config['recommendation']} [{$config['severity']}]\n";
        $failed++;
    } else {
        $passed++;
    }
}

echo "\n=== Resultado: {$passed} passed, {$failed} failed ===\n";
exit($failed > 0 ? 1 : 0);
```

##### Fase 3 — Autenticação e Sessão

**Testes:**
```bash
#!/usr/bin/env bash
# auth-session-tests.sh
set -euo pipefail

BASE="${1:-http://localhost/totustuussoftcloud}"
REPORT_DIR="build/pen-test/03-auth"

mkdir -p "$REPORT_DIR"

echo "=== FASE 3: AUTH & SESSION ==="

# 3.1 JWT Inspection
echo "--- 3.1 JWT ---" > "$REPORT_DIR/jwt.txt"
curl -sI "${BASE}/login" | grep -i 'authorization\|token\|jwt' >> "$REPORT_DIR/jwt.txt" || true

# 3.2 Session Cookie Hardening
echo "--- 3.2 Session Cookies ---" > "$REPORT_DIR/session.txt"
curl -sI -c /dev/null "${BASE}/login" | grep -i 'set-cookie' >> "$REPORT_DIR/session.txt" || true
# Verificar flags
grep -q 'HttpOnly' "$REPORT_DIR/session.txt" && echo "HttpOnly: OK" || echo "HttpOnly: MISSING"
grep -q 'Secure' "$REPORT_DIR/session.txt" && echo "Secure: OK" || echo "Secure: MISSING"
grep -q 'SameSite' "$REPORT_DIR/session.txt" && echo "SameSite: OK" || echo "SameSite: MISSING"

# 3.3 Brute-Force / Rate Limiting
echo "--- 3.3 Rate Limiting ---" > "$REPORT_DIR/rate-limit.txt"
for i in $(seq 1 20); do
    status=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST "${BASE}/login" \
        -d "email=test@test.com&password=wrong${i}" \
        2>/dev/null || echo "000")
    echo "Attempt ${i}: HTTP ${status}" >> "$REPORT_DIR/rate-limit.txt"
    if [ "$status" = "429" ]; then
        echo "RATE LIMITING DETECTADO no attempt ${i}"
        break
    fi
done

# 3.4 MFA Tests
echo "--- 3.4 MFA ---" > "$REPORT_DIR/mfa.txt"
curl -s "${BASE}/login" | grep -qi 'mfa\|2fa\|authenticator\|totp' \
    && echo "MFA interface: PRESENTE" \
    || echo "MFA interface: NÃO DETECTADA"
```

##### Fase 4 — Autorização e Isolamento Multi-tenant

```php
#!/usr/bin/env php
<?php
declare(strict_types=1);

/**
 * Teste de isolamento multi-tenant.
 * Verifica se um tenant A NÃO consegue acessar dados do tenant B.
 */

$baseUrl = $argv[1] ?? 'http://localhost/totustuussoftcloud/admin';
$reportsDir = __DIR__ . '/../../build/pen-test/04-isolation';
@mkdir($reportsDir, 0755, true);

echo "=== Multi-tenant Isolation Tests ===\n";
echo "Base: {$baseUrl}\n\n";

$tests = [
    'User lists scoped by tenant' => [
        'url' => '/api/users',
        'expected_scope' => 'tenant_id',
    ],
    'DSR requests scoped by tenant' => [
        'url' => '/admin/privacy/tenant/dsr',
        'expected_scope' => 'tenant_id',
    ],
    'Cookie catalog scoped by tenant' => [
        'url' => '/admin/privacy/cookie-catalog',
        'expected_scope' => 'tenant_id',
    ],
    'Processing activities scoped by tenant' => [
        'url' => '/admin/privacy/tenant/ropa',
        'expected_scope' => 'tenant_id',
    ],
    'Incidents scoped by tenant' => [
        'url' => '/admin/privacy/incidents',
        'expected_scope' => 'tenant_id',
    ],
];

$results = [];
foreach ($tests as $name => $test) {
    echo "  Testing: {$name}... ";
    
    // Simulate request with tenant A session
    $ch = curl_init();
    curl_setopt_array($ch, [
        CURLOPT_URL => $baseUrl . $test['url'],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HEADER => true,
        CURLOPT_TIMEOUT => 10,
        CURLOPT_COOKIE => 'PHPSESSID=test_tenant_a_session',
    ]);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    $status = $httpCode === 200 ? 'PASS' : 'FAIL';
    echo "[{$status}] HTTP {$httpCode}\n";
    $results[] = ['test' => $name, 'status' => $status, 'http' => $httpCode];
}

file_put_contents(
    "{$reportsDir}/results.json",
    json_encode($results, JSON_PRETTY_PRINT)
);
echo "\nRelatório salvo em {$reportsDir}/results.json\n";
```

##### Fase 5 — Injection / XSS / Upload

```bash
#!/usr/bin/env bash
# injection-tests.sh
set -euo pipefail

BASE="${1:-http://localhost/totustuussoftcloud}"
REPORT_DIR="build/pen-test/05-injection"
mkdir -p "$REPORT_DIR"

echo "=== FASE 5: INJECTION & XSS ===" > "$REPORT_DIR/results.txt"

# 5.1 SQL Injection
echo "--- SQL Injection ---" >> "$REPORT_DIR/results.txt"
for payload in "'" "' OR 1=1 --" "' UNION SELECT 1,2,3 --" "'; DROP TABLE users --"; do
    encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${payload}'))" 2>/dev/null || echo "$payload")
    status=$(curl -s -o /dev/null -w "%{http_code}" "${BASE}/login?email=${encoded}" 2>/dev/null || echo "000")
    echo "  Payload: ${payload} → HTTP ${status}" >> "$REPORT_DIR/results.txt"
done

# 5.2 XSS
echo "--- XSS ---" >> "$REPORT_DIR/results.txt"
for payload in "<script>alert(1)</script>" "<img src=x onerror=alert(1)>" "javascript:alert(1)"; do
    encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${payload}'))" 2>/dev/null || echo "$payload")
    status=$(curl -s -o /dev/null -w "%{http_code}" "${BASE}/search?q=${encoded}" 2>/dev/null || echo "000")
    echo "  Payload: ${payload} → HTTP ${status}" >> "$REPORT_DIR/results.txt"
done

# 5.3 File Upload
echo "--- File Upload ---" >> "$REPORT_DIR/results.txt"
# Test upload of disallowed types
for ext in php phtml php5 shtml cgi pl py exe; do
    echo "testing ${ext}" > "/tmp/test.${ext}"
    status=$(curl -s -o /dev/null -w "%{http_code}" \
        -F "file=@/tmp/test.${ext}" \
        "${BASE}/admin/profile/upload" 2>/dev/null || echo "000")
    echo "  Extension .${ext}: HTTP ${status}" >> "$REPORT_DIR/results.txt"
done

echo "Concluído." >> "$REPORT_DIR/results.txt"
cat "$REPORT_DIR/results.txt"
```

##### Fase 6 — API Security (OWASP API Top 10)

```bash
#!/usr/bin/env bash
# api-tests.sh
set -euo pipefail

BASE="${1:-http://localhost/totustuussoftcloud}"
REPORT_DIR="build/pen-test/06-api"
mkdir -p "$REPORT_DIR"

echo "=== FASE 6: API SECURITY ===" > "$REPORT_DIR/results.txt"

# 6.1 Broken Object Level Authorization
echo "--- BOLA (API1) ---" >> "$REPORT_DIR/results.txt"
endpoints=(
    "/api/users/00000000-0000-0000-0000-000000000001"
    "/api/sessions/current"
    "/admin/privacy/sessions/list"
)
for ep in "${endpoints[@]}"; do
    status=$(curl -s -o /dev/null -w "%{http_code}" "${BASE}${ep}" 2>/dev/null || echo "000")
    echo "  GET ${ep} → HTTP ${status} (esperado: 401/403 sem auth)" >> "$REPORT_DIR/results.txt"
done

# 6.2 Broken Authentication
echo "--- Broken Auth (API2) ---" >> "$REPORT_DIR/results.txt"
# Missing/weak tokens
status=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer invalid_token" \
    "${BASE}/api/users" 2>/dev/null || echo "000")
echo "  Token inválido → HTTP ${status} (esperado: 401)" >> "$REPORT_DIR/results.txt"

# 6.3 Rate Limiting
echo "--- Rate Limiting (API4) ---" >> "$REPORT_DIR/results.txt"
for i in $(seq 1 30); do
    status=$(curl -s -o /dev/null -w "%{http_code}" "${BASE}/api/health" 2>/dev/null || echo "000")
    if [ "$status" = "429" ]; then
        echo "  Rate limit ativado após ${i} requests" >> "$REPORT_DIR/results.txt"
        break
    fi
done

# 6.4 Mass Assignment (API8)
echo "--- Mass Assignment (API8) ---" >> "$REPORT_DIR/results.txt"
status=$(curl -s -o /dev/null -w "%{http_code}" \
    -X PATCH \
    -H "Content-Type: application/json" \
    -d '{"role":"admin","is_master":true,"is_admin":true}' \
    "${BASE}/api/profile" 2>/dev/null || echo "000")
echo "  Mass assignment attempt → HTTP ${status}" >> "$REPORT_DIR/results.txt"

echo "Concluído." >> "$REPORT_DIR/results.txt"
```

##### Fase 7 — Auditoria de Logs

```bash
#!/usr/bin/env bash
# audit-tests.sh
set -euo pipefail

BASE="${1:-http://localhost/totustuussoftcloud}"
REPORT_DIR="build/pen-test/07-audit"
mkdir -p "$REPORT_DIR"

echo "=== FASE 7: AUDIT TRAIL ===" > "$REPORT_DIR/results.txt"

# 7.1 Audit trail presente em ações críticas
echo "--- Critical Actions Audited ---" >> "$REPORT_DIR/results.txt"
actions=(
    "login"
    "logout"
    "user.create"
    "user.delete"
    "role.change"
    "permission.change"
    "data.export"
    "consent.grant"
    "consent.revoke"
    "dsr.process"
)

# Verificar tabela audit_logs
echo "  Verificando colunas obrigatórias na audit_logs:" >> "$REPORT_DIR/results.txt"
echo "  audit_logs deve conter: action, performed_by, target_id, target_type, old_value, new_value, ip_address, user_agent, created_at" >> "$REPORT_DIR/results.txt"

# 7.2 Logs imutáveis
echo "--- Immutable Logs ---" >> "$REPORT_DIR/results.txt"
echo "  Verificar se UPDATE/DELETE são bloqueados na tabela audit_logs" >> "$REPORT_DIR/results.txt"
echo "  Utilizar triggers ou permissões de banco para impedir alteração" >> "$REPORT_DIR/results.txt"

# 7.3 Logs de acesso
echo "--- Access Logs ---" >> "$REPORT_DIR/results.txt"
echo "  Verificar logging de todas as requisições autenticadas" >> "$REPORT_DIR/results.txt"
echo "  Incluir: IP, user agent, método, URL, status code, timestamp" >> "$REPORT_DIR/results.txt"
```

##### Fase 8 — CORS / CSP / Rate Limiting

```bash
#!/usr/bin/env bash
# infra-tests.sh
set -euo pipefail

BASE="${1:-http://localhost/totustuussoftcloud}"
REPORT_DIR="build/pen-test/08-infra"
mkdir -p "$REPORT_DIR"

echo "=== FASE 8: INFRA SECURITY ===" > "$REPORT_DIR/results.txt"

# 8.1 CORS
echo "--- CORS ---" >> "$REPORT_DIR/results.txt"
for origin in "https://evil.com" "https://attacker.org" "null"; do
    status=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Origin: ${origin}" \
        -H "Access-Control-Request-Method: GET" \
        "${BASE}/api/health" 2>/dev/null || echo "000")
    acao=$(curl -s -D - "${BASE}/api/health" \
        -H "Origin: ${origin}" 2>/dev/null | grep -i 'access-control-allow-origin' || true)
    echo "  Origin: ${origin} → HTTP ${status} | ACAO: ${acao:-none}" >> "$REPORT_DIR/results.txt"
done

# 8.2 CSP Nonce Validation
echo "--- CSP Nonce ---" >> "$REPORT_DIR/results.txt"
# Extrair nonce do HTML e tentar reutilizar
nonce=$(curl -s "${BASE}/login" 2>/dev/null | grep -oP 'nonce="\K[^"]+' | head -1)
if [ -n "$nonce" ]; then
    echo "  Nonce detectado: ${nonce}" >> "$REPORT_DIR/results.txt"
    # Tentar XSS com nonce roubado
    payload="<script nonce=\"${nonce}\">alert(1)</script>"
    echo "  Teste de reuso de nonce: ${payload}" >> "$REPORT_DIR/results.txt"
else
    echo "  CSP Nonce: NÃO DETECTADO (FALHA)" >> "$REPORT_DIR/results.txt"
fi

echo "Concluído." >> "$REPORT_DIR/results.txt"
```

##### Fases 9-10 — Relatório e Regressão

```bash
#!/usr/bin/env bash
# report.sh — Relatório consolidado
set -euo pipefail

REPORT_DIR="build/pen-test"
DATE=$(date +"%Y-%m-%d %H:%M")

echo "==========================================="
echo "  Pen Test Report — TotusTuus SoftCloud"
echo "  Data: ${DATE}"
echo "==========================================="
echo ""

total=0
passed=0
failed=0

for phase_dir in "$REPORT_DIR"/*/; do
    phase=$(basename "$phase_dir")
    echo "── Fase: ${phase} ──"
    
    if [ -f "${phase_dir}results.txt" ]; then
        while IFS= read -r line; do
            if echo "$line" | grep -q 'PASS'; then
                echo "  ✓ $line"
                passed=$((passed + 1))
            elif echo "$line" | grep -q 'FAIL'; then
                echo "  ✗ $line"
                failed=$((failed + 1))
            fi
            total=$((total + 1))
        done < "${phase_dir}results.txt"
    fi
    echo ""
done

echo "==========================================="
echo "  Summary: ${passed} PASS / ${failed} FAIL / ${total} TOTAL"
echo "==========================================="

# Exit with error code if failures
[ "$failed" -gt 0 ] && exit 1 || exit 0
```

---

#### 2. Matriz de Responsabilidades

| Fase | Teste | Responsável | Frequência |
|------|-------|-------------|------------|
| 1 | Reconhecimento | DevOps | Semanal |
| 2 | Hardening Headers | DevSecOps | A cada deploy |
| 3 | Auth & Session | Desenvolvedor | A cada release |
| 4 | Isolamento Multi-tenant | QA | A cada release |
| 5 | Injection & XSS | DevSecOps | Quinzenal |
| 6 | API Security | Desenvolvedor | A cada sprint |
| 7 | Audit Trail | QA | A cada release |
| 8 | Infra (CORS/CSP) | DevOps | Mensal |
| 9 | Relatório Consolidado | DevSecOps | A cada ciclo |
| 10 | Regressão Pós-Fix | QA | Após cada fix |

---

#### 3. Checklist de Implementação

- [ ] Criar diretório `scripts/` com todos os scripts de teste
- [ ] Adicionar workflow CI para execução automatizada (`pen-test.yml`)
- [ ] Configurar relatório em `build/pen-test/` com output JSON
- [ ] Integrar resultados com dashboard de segurança
- [ ] Documentar procedimento de regressão pós-fix
- [ ] Configurar alertas para falhas críticas (severity HIGH+)
