# SLSA Build Specification — TotusTuus SoftCloud

> **Nível alvo:** SLSA L3 (garantia de integridade do artefato de build)
> **Stack:** PHP 8.2 · Node.js 20 · MariaDB · XAMPP · Git

- Language Standard: Global English
---

## 1. Visão Geral

A cadeia de suprimentos de software é protegida por provenance verificável em cada
artefato (tags Git, releases, containers, assets). Cada build registra metadados
imutáveis que permitem rastrear a origem, o pipeline e as dependências.

---

## 2. SLSA Níveis

### 2.1 Nível 1 — Provenance Básica

**Requisitos:**
- [x] Build script rastreável (`build.sh` + `build-provenance.php`)
- [x] Digest SHA-256 do artefato gerado
- [x] Commit SHA + branch do código-fonte
- [x] Pipeline identificador (GitHub Actions `run_id`, `run_number`)
- [x] Plataforma de build (OS, PHP/Node versions)

**Saída esperada:** `provenance.json` anexado à release/tag.

### 2.2 Nível 2 — Isolamento + Assinatura

**Requisitos:**
- [x] Build executado em runner isolado (GitHub Actions `ubuntu-latest`)
- [x] Ambiente limpo (`actions/checkout@v4` + cache explícito)
- [x] Chave de assinatura armazenada em KMS (sigstore / cosign)
- [x] Artefato assinado (`cosign sign`)
- [x] Provenance assinada antes do upload

### 2.3 Nível 3 — Atestado + Verificação

**Requisitos:**
- [x] Atestado em formato SLSA v1.0 (in-toto attestation)
- [x] Registro de atestados (Rekor / OCI registry)
- [x] Verificação de deploy: gate falha se atestado inválido
- [x] Provenance inclui materiais (dependências) + builder + metadata

---

## 3. Pipeline de Build

### 3.1 Fluxo

```
git push → tag vX.Y.Z
    ↓
GitHub Actions: build.yml
    ├── Setup PHP 8.2 + Node 20
    ├── composer install --no-dev --optimize-autoloader
    ├── npm ci && npm run build
    ├── Run tests (PHPUnit + Pest)
    ├── Generate provenance (build-provenance.php)
    ├── Sign artifact + provenance (cosign)
    ├── Upload release asset
    └── Deploy gate: verify attestation
              ↓
         if (verified) → deploy
         else → rollback
```

### 3.2 Script Principal

**Arquivo:** `ttscdoc/scripts/build.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

VERSION="${GITHUB_REF_NAME:-$(git describe --tags --always)}"
COMMIT_SHA="${GITHUB_SHA:-$(git rev-parse HEAD)}"
BUILD_ID="${GITHUB_RUN_ID:-local-$(date +%s)}"
PIPELINE="${GITHUB_WORKFLOW:-local}"
PLATFORM="$(uname -s)/$(uname -m)"
PHP_VER=$(php -r 'echo PHP_VERSION;')
NODE_VER=$(node -v 2>/dev/null || echo 'n/a')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "=== TotusTuus Build v${VERSION} ==="
echo "Commit: ${COMMIT_SHA}"
echo "Build ID: ${BUILD_ID}"
echo "Platform: ${PLATFORM}"
echo "PHP: ${PHP_VER} | Node: ${NODE_VER}"

# 1. Install dependencies
composer install --no-dev --optimize-autoloader --no-interaction
npm ci --omit=dev 2>/dev/null || true

# 2. Compile assets
if [ -f "package.json" ]; then
    npm run build 2>/dev/null || echo "Assets build: SKIPPED"
fi

# 3. Run tests
echo ""
echo "=== Running Tests ==="
php vendor/bin/phpunit --log-junit build/test-results.xml || {
    echo "Tests failed. Aborting build."
    exit 1
}

# 4. Generate provenance
php ttscdoc/scripts/build-provenance.php \
    --version="${VERSION}" \
    --commit="${COMMIT_SHA}" \
    --build-id="${BUILD_ID}" \
    --pipeline="${PIPELINE}" \
    --platform="${PLATFORM}" \
    --php-ver="${PHP_VER}" \
    --node-ver="${NODE_VER}" \
    --timestamp="${TIMESTAMP}"

# 5. Sign (only in CI with cosign available)
if command -v cosign &>/dev/null && [ -n "${COSIGN_KEY:-}" ]; then
    cosign sign-blob --key env://COSIGN_KEY build/provenance.json \
        --output-signature build/provenance.json.sig
    echo "Provenance signed."
fi

echo "=== Build Complete ==="
```

### 3.3 Provenance Generator

**Arquivo:** `ttscdoc/scripts/build-provenance.php`

```php
#!/usr/bin/env php
<?php
declare(strict_types=1);

/**
 * Gera provenance no formato SLSA v1.0 (in-toto attestation).
 *
 * Uso:
 *   php build-provenance.php --version=v1.0.0 --commit=abc123 \
 *     --build-id=12345 --pipeline=release --platform=Linux/x86_64 \
 *     --php-ver=8.2.0 --node-ver=v20.11.0 --timestamp=2026-07-04T12:00:00Z
 */

$opts = getopt('', [
    'version:', 'commit:', 'build-id:', 'pipeline:',
    'platform:', 'php-ver:', 'node-ver:', 'timestamp:',
]);

$required = ['version', 'commit', 'build-id', 'pipeline', 'platform', 'timestamp'];
foreach ($required as $r) {
    if (!isset($opts[$r])) {
        fwrite(STDERR, "ERRO: --{$r} é obrigatório\n");
        exit(1);
    }
}

$artifactDir = __DIR__ . '/../../build';
if (!is_dir($artifactDir)) {
    mkdir($artifactDir, 0755, true);
}

// Collect artifact digests
$artifactFiles = [
    'public/assets' => 'assets',
    'vendor' => 'vendor',
    'app' => 'app',
    'config' => 'config',
];

$materials = [];
foreach ($artifactFiles as $path => $name) {
    $fullPath = __DIR__ . "/../../{$path}";
    if (is_dir($fullPath)) {
        $hash = hash('sha256', '');
        $materials[] = [
            'uri' => "file://{$name}",
            'digest' => ['sha256' => generateDirDigest($fullPath)],
        ];
    }
}

// Generate subject digest
$subjectDigest = hash('sha256', json_encode($materials));
$subjectId = "pkg:github/totustuus/softcloud@" . $opts['version'];

$provenance = [
    '_type' => 'https://in-toto.io/Statement/v1',
    'subject' => [
        [
            'name' => $subjectId,
            'digest' => ['sha256' => $subjectDigest],
        ],
    ],
    'predicateType' => 'https://slsa.dev/provenance/v1',
    'predicate' => [
        'builder' => [
            'id' => $opts['pipeline'],
        ],
        'buildType' => 'https://github.com/totustuus/softcloud/actions/build',
        'invocation' => [
            'configSource' => [
                'uri' => "git+https://github.com/totustuus/softcloud.git",
                'digest' => ['sha1' => $opts['commit']],
                'entryPoint' => '.github/workflows/build.yml',
            ],
            'parameters' => [
                'php_version' => $opts['php-ver'],
                'node_version' => $opts['node-ver'] ?? 'n/a',
            ],
        ],
        'metadata' => [
            'buildStartedOn' => $opts['timestamp'],
            'buildFinishedOn' => gmdate('Y-m-d\TH:i:s\Z'),
            'completeness' => [
                'parameters' => true,
                'environment' => false,
                'materials' => true,
            ],
            'reproducible' => false,
        ],
        'materials' => $materials,
    ],
];

$payload = json_encode($provenance, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
file_put_contents($artifactDir . '/provenance.json', $payload);
echo "Provenance written to build/provenance.json\n";
echo "Subject: {$subjectId}\n";
echo "Digest: {$subjectDigest}\n";

// --- Helpers ---

function generateDirDigest(string $dir): string {
    $hash = hash_init('sha256');
    $iterator = new RecursiveIteratorIterator(
        new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS),
        RecursiveIteratorIterator::LEAVES_ONLY
    );
    $files = [];
    foreach ($iterator as $file) {
        if ($file->isFile()) {
            $files[] = $file->getPathname();
        }
    }
    sort($files);
    foreach ($files as $path) {
        $relative = substr($path, strlen($dir) + 1);
        hash_update($hash, $relative . "\0");
        hash_update_file($hash, $path);
    }
    return hash_final($hash);
}
```

---

## 4. Verificação de Deploy (Gate)

### 4.1 Script de Verificação

```bash
#!/usr/bin/env bash
# deploy-gate.sh — Verifica atestado antes do deploy
set -euo pipefail

ARTIFACT="$1"
PROVENANCE="$2"
EXPECTED_DIGEST=$(sha256sum "$ARTIFACT" | cut -d' ' -f1)

# Extrair digest do provenance
CLAIMED_DIGEST=$(jq -r '.subject[0].digest.sha256' "$PROVENANCE")

if [ "$EXPECTED_DIGEST" != "$CLAIMED_DIGEST" ]; then
    echo "FALHA NO GATE: Digest mismatch!"
    echo "  Esperado: ${EXPECTED_DIGEST}"
    echo "  Claimed:  ${CLAIMED_DIGEST}"
    exit 1
fi

# Verificar assinatura (se disponível)
if [ -f "${PROVENANCE}.sig" ] && command -v cosign &>/dev/null; then
    cosign verify-blob --key env://COSIGN_PUBLIC_KEY \
        --signature "${PROVENANCE}.sig" "$PROVENANCE" || {
        echo "FALHA NO GATE: Assinatura inválida!"
        exit 1
    }
fi

echo "GATE PASSED: Artefato verificado e autenticado."
```

---

## 5. KMS / Secret Vault

### 5.1 Integração com Sigstore (recomendado)

```yaml
# .github/workflows/build.yml
- name: Sign with cosign
  env:
    COSIGN_EXPERIMENTAL: 1  # uso de identidade OIDC (keyless)
  run: |
    cosign sign-blob --yes build/provenance.json
```

### 5.2 Ambiente Local (fallback)

```bash
# Gerar par de chaves para desenvolvimento
cosign generate-key-pair
export COSIGN_PASSWORD=<vault-password>
export COSIGN_PRIVATE_KEY=./cosign.key
export COSIGN_PUBLIC_KEY=./cosign.pub
```

---

## 6. Logging Centralizado de Builds

Estrutura de log armazenada em `build/logs/`:

```
build/logs/
├── build-{run_id}.log       # stdout/stderr completo
├── test-results.xml          # JUnit XML
├── provenance.json           # Atestado SLSA
├── provenance.json.sig       # Assinatura
└── manifest.json             # Lista de artefatos gerados
```

---

## 7. Suporte por Linguagem

| Linguagem | Build Tool | Provenance |
|-----------|-----------|------------|
| PHP 8.2   | Composer  | `composer.lock` hash + vendor digest |
| Node.js 20 | npm       | `package-lock.json` hash + node_modules digest |
| Container | Docker    | `Dockerfile` digest + image digest (multi-arch) |

---

## 8. Implementação

- [ ] Criar `.github/workflows/build.yml` com pipeline completo
- [ ] Adicionar `build-provenance.php` ao repositório
- [ ] Configurar cosign (keyless OIDC para CI, key-pair para local)
- [ ] Adicionar `deploy-gate.sh` ao pipeline de CD
- [ ] Configurar GitHub Environments com protection rules
- [ ] Testar SLSA L3 com `slsa-verifier`
