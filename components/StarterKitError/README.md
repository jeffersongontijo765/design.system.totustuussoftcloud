# StarterKitError

Kit das páginas de erro reais: 404 e 500 renderizadas dentro do shell (`errors/pages/404.php` e `500.php` sobre `app/layouts/main.php`), a página genérica independente `errors/pages/error.php` (usada aqui com 503) e o `errors/404.html` estático do servidor web.

## Quando usar

| Situação | Página | Quem renderiza |
|---|---|---|
| Rota inexistente ou exceção 404 com sessão | `errors::pages/404` (dentro do shell) | `Router` (rota sem match) e `Exceptions\Handler::renderProduction()` |
| Exceção não tratada (500) | `errors::pages/500` (dentro do shell) | `Exceptions\Handler::renderProduction()` |
| Outros códigos (403, 419, 429, 503) ou quando a página dedicada não existe | `errors::pages/error` (HTML próprio, sem shell) | `Handler` (fallback) e `Router` |
| PHP fora do ar / erro antes do app subir | `resources/views/errors/404.html`, `500.html` (estáticos) | servidor web (`ErrorDocument`/`error_page`) |
| Erro de um campo, de uma consulta ou de um bloco | não é página de erro → [Alert](../Alert/README.md) ou [EmptyState](../EmptyState/README.md) | — |

- **Manutenção:** o repositório não tem página de manutenção dedicada (nenhuma view, rota ou middleware de 503). A variante "Genérico (503)" do kit é `error.php` renderizado com `code=503` e textos de manutenção — é o caminho recomendado até existir uma página própria.
- `errors/pages/admin-error.php` só delega para 404/500.

## Anatomia

```
404/500 no shell (app/layouts/main.php)            error.php / 404.html (página própria)
header + rail (sem sub-sidebar)                    [tema] (fixo, canto superior direito)
main  .error-shell-overlay (min-h 100vh-120px)     .error-bg-shapes (decorativo, aria-hidden)
      .error-container (máx. 520px)                .error-container
        .error-code  ● STATUS 404                    .error-code._404|._500  ● Status 503
        .error-icon  (88px, brilho)                  .error-icon > .glow + i.fa-light
        h1 título · p descrição                      h1.error-title · p.error-desc
        .error-suggestions (3 links)                 .error-suggestions (Início, Painel, Contato)
        [Voltar] [Painel]                            .error-actions [Voltar] [Início]
        ID do Erro: 8 hex                            .error-footer (ID do erro · copyright)
footer
```

| Parte | Classe / origem | Obrigatório |
|---|---|---|
| Selo do código | `.error-code` (+ `._404` âmbar / `._500` vermelho em `error.php`) | sim |
| Ícone | `.error-icon > .glow + i.fa-light` (`fa-map-signs` no 404, `fa-triangle-exclamation` nos demais) | sim |
| Título / descrição | `h1` + `p` (`$title`, `$description` ou `$message`) | sim |
| Sugestões | `.error-suggestions` > `a.error-suggestion-link` | sim |
| Ações | `.error-btn.error-btn-secondary` (`history.back()`) + `.error-btn.error-btn-primary` | sim |
| ID do erro | `strtoupper(substr(md5(time().rand()), 0, 8))` — aleatório, não ligado ao log | opcional |
| CSS | estilos inline no próprio 404/500.php; `assets/css/error-layout.css` no `error.php` | sim |

## Variantes / Estados

| Variante (botão) | Arquivo | Dados passados pelo Handler |
|---|---|---|
| 404 no shell | `errors/pages/404.php` | `code=404`, `title='Página Não Encontrada'`, `description`, `exception`, `debug` |
| 500 no shell | `errors/pages/500.php` | `code=500`, `title='Erro do Servidor'`, `description` |
| Genérico (503) | `errors/pages/error.php` | `status`, `code`, `title="Erro {status}"`, `message` (o kit usa "Em manutenção") |
| Estático 404 | `errors/404.html` | nenhum (textos traduzidos por JS conforme `?locale=` / idioma do navegador) |
| Tema | 404/500: o do shell (`html.dark`); `error.php` e `404.html`: `data-theme` + `localStorage['ttsc-theme']` | |
| Responsivo | shell: regras do [StarterKitAppShell](../StarterKitAppShell/README.md); páginas próprias: coluna única de até 520px | |

O contraste do botão primário "Painel" no tema escuro foi corrigido no repo (commit `243e7a45c` fix(views)); o kit já mostra o texto escuro sobre o verde.

## API

| Ponto | Efeito |
|---|---|
| `App\Exceptions\Handler::render()` | produção → `renderProduction()` (páginas acima); debug → página com stack trace |
| `Handler::logException()` → `ErrorLogger::capture($e, 'error'|'critical')` | grava em `error_logs` |
| Escolha do layout | `renderProduction()` testa `$engine->exists("errors::pages/{$status}")`; senão `errors::pages/error` |
| `$isAdmin` (prefixo da rota) | decide se o erro é da área logada ou pública (`/about`, `/login`, `/install`…) |
| `toggle` de tema em `error.php` | `#themeToggle` alterna `data-theme` e grava `ttsc-theme` |

## Acessibilidade

- O título do erro é o `h1` da página; o código fica no selo como texto ("Status 404"), não só cor.
- Ações são `button`/`a` reais com rótulo ("Voltar", "Início"); a ação primária leva a um lugar seguro.
- Formas decorativas e brilho com `aria-hidden`; ícone `fa-light` sem texto alternativo (o título já diz o erro).
- Não exponha mensagem de exceção ao usuário em produção — `debug=false` mostra só o texto genérico.

## Modelos

### HTML

```php
<?php
// Nova página dedicada: resources/views/errors/pages/503.php (o Handler a escolhe sozinho por existir)
$codeStr = (string) ($code ?? '503');
$titleText = $this->e($title ?? 'Sistema em manutenção');
$description = $description ?? 'Estamos atualizando o TotusTuus. As matrículas e os lançamentos voltam em alguns minutos.';
?>
<?php $this->layout('app::layouts/main', ['title' => $titleText, 'hideSubSidebar' => true, 'pageHasHeader' => true]) ?>
<?php $this->start('content') ?>
<div class="error-shell-overlay">
  <div class="error-container" role="alert">
    <div class="error-code"><span class="dot" aria-hidden="true"></span> Status <?= $this->e($codeStr) ?></div>
    <div class="error-icon"><i class="fa-light fa-screwdriver-wrench" aria-hidden="true"></i></div>
    <h1 class="error-title"><?= $titleText ?></h1>
    <p class="error-desc"><?= $this->e($description) ?></p>
    <div class="error-actions">
      <button type="button" class="error-btn error-btn-secondary" onclick="location.reload()">
        <i class="fa-light fa-arrows-rotate" aria-hidden="true"></i> Tentar de novo
      </button>
      <a href="<?= url('/dashboard') ?>" class="error-btn error-btn-primary">
        <i class="fa-light fa-gauge-high" aria-hidden="true"></i> Painel
      </a>
    </div>
  </div>
</div>
<?php $this->stop() ?>
```

### CSS

```css
/* Extensão com tokens para as páginas de erro no shell (substitui as cores fixas #eab308 / rgba) */
.error-shell-overlay { display: flex; align-items: center; justify-content: center; min-height: calc(100vh - 120px); padding: var(--ttsc-space-10) var(--ttsc-space-6); }
.error-container { max-width: 520px; width: 100%; text-align: center; }
.error-code { display: inline-flex; align-items: center; gap: var(--ttsc-space-2); padding: var(--ttsc-space-2) var(--ttsc-space-5);
  border-radius: var(--ttsc-radius-pill); border: 1px solid var(--ttsc-warning); color: var(--ttsc-warning-text);
  background: color-mix(in srgb, var(--ttsc-warning) 10%, transparent); font-weight: 700; letter-spacing: .05em; text-transform: uppercase; }
.error-code .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--ttsc-warning); }
.error-btn-primary { background: var(--ttsc-accent); color: var(--ttsc-accent-on); }   /* corrige o verde-sobre-verde do escuro */
.error-btn-secondary { background: var(--ttsc-surface); color: var(--ttsc-text); border: 1px solid var(--ttsc-border); }
```

### JS

```js
// Página 503: tenta voltar sozinha quando o sistema responder (GET leve, sem cache)
(function () {
  var tries = 0, base = (document.querySelector('base') || {}).href || '/';
  function ping() {
    fetch(base + 'api/v1/installed', { cache: 'no-store', headers: { 'Accept': 'application/json' } })
      .then(function (r) { if (r.ok) location.reload(); else schedule(); })
      .catch(schedule);
  }
  function schedule() { tries += 1; setTimeout(ping, Math.min(60000, 5000 * tries)); }
  schedule();
})();
```

### SQL

O erro é gravado por `ErrorLogger` (banco master); a página não consulta nada. Para o painel de erros (developer/logger) e para o suporte localizar um ocorrido:

```sql
SELECT uuid, level, module, message, url, method, created_at
  FROM error_logs
 WHERE level IN ('error', 'critical')
   AND created_at > DATE_SUB(NOW(), INTERVAL 24 HOUR)
 ORDER BY created_at DESC
 LIMIT 50;
```

A migração `2026_10_22_000004` (commit `a2b03b61a`) acrescentou à `error_logs` as colunas de rastreio que o `ErrorLogger::capture()` grava (`code`, `fingerprint`, `occurrences`, `status`…), e a consulta acima continua válida. Ainda vale: o "ID do Erro" mostrado na tela é um hash aleatório (`md5(time().rand())`), sem relação com o `uuid`/`code` do log.

## Como começar um projeto a partir do kit

1. **Arquivos do kit**: `kit.html` (404 no shell), `kit-500.html`, `kit-generic.html` (+ `assets/css/error-layout.css`), `kit-static-404.html`, `assets/fa.css`; gerados por `$SPD/dsh/gen_kits.py` a partir de `php $SPD/app/view_harness.php /x errors::pages/404 …` (PlatesEngine real, mesmos dados do Handler).
2. **No repo**: uma página nova por código em `resources/views/errors/pages/<código>.php` — o Handler a encontra por `exists()`; páginas com sessão herdam `app::layouts/main`, públicas seguem `error.php`.
3. **Outro projeto**: copie `errors/pages/{404,500,error}.php`, `errors/404.html`, `errors/500.html`, `assets/css/error-layout.css` e a lógica de escolha do `Handler::renderProduction()`; 404/500 também precisam dos arquivos do [StarterKitAppShell](../StarterKitAppShell/README.md#como-começar-um-projeto-a-partir-do-kit). Configure o servidor web para servir os `.html` estáticos quando o PHP falhar.

## Faça / Não faça

- **Faça:** sempre uma saída segura (Voltar + Painel/Início) e texto sem jargão.
- **Faça:** registre a exceção (`ErrorLogger`) antes de renderizar; mostre ao usuário um código que o suporte encontre no log.
- **Faça:** páginas estáticas sem dependência de PHP, banco ou CDN.
- **Não faça:** carregar CSS/JS de CDN em página de erro nem mostrar stack trace fora do modo debug.
- **Não faça:** responder 200 com página de erro — o status HTTP deve ser o do erro.
