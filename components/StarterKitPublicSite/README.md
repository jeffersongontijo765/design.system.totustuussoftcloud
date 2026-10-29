# StarterKitPublicSite

Kit do site institucional: o render real de `resources/views/web/layouts/main.php` com a landing `web/pages/home.php` — barra de portais, navbar fixa, hero, seções da home, rodapé, gaveta de portais, chat de vendas e consentimento de cookies.

## Quando usar

- Páginas públicas sem login: `/` (home), `/about`, `/contact`, `/plans`, `/modules/{slug}`, `/privacy`, `/terms`, `/checkout` — todas em `resources/views/web/pages/` sobre `web::layouts/main`.
- Landing de campanha (matrículas abertas, evento) dentro do mesmo site.
- Formulário de instalação → [StarterKitInstall](../StarterKitInstall/README.md) (usa este layout). Portal de suporte do cliente → [StarterKitSupportPortal](../StarterKitSupportPortal/README.md) (layout `web/layouts/portal.php`). Telas de login → [StarterKitAuth](../StarterKitAuth/README.md).

## Anatomia

```
topbar (28px)   Portal de Suporte | Portais Rápidos: Aluno Professor Pais Desenvolvedores ........ ● SLA 99,9% Online (lg)
header fixo (top 28px, 64px, backdrop-blur)
  [logo TotusTuus SOFTCLOUD]     Soluções  Planos  Sobre  Contato (md:flex)     [idioma][tema][Login do Portal][Agendar Demonstração]
  #webNavToggle (md:hidden) → #webMobileNav (fixed top 92px)
section('header')  ← faixa extra opcional da página
section('content') ← home: 1 hero · 2 números · 3 módulos (#modulos) · 4 IA · 5 gráficos · 6 ROI/planos · 7 segurança/LGPD · 8 formulário (#formulario)
#portalDrawer (gaveta "Login do Portal" com os 5 portais)
footer (4 colunas + legal)
#leadChatToggle "Falar com vendas" → #leadChatPanel (POST api/leads/capture)
cookie_consent_modal.php · consent-cookie.js · section('scripts')
```

| Parte | Origem real | Obrigatório |
|---|---|---|
| Layout | `web/layouts/main.php` (`$this->layout('web::layouts/main', ['title' => …, 'description' => …])`) | sim |
| SEO | `<title>`, `description`, `canonical`, OpenGraph/Twitter (`media/app/og-image.png`, `twitter-image.png`) | sim |
| Navbar | `header.fixed.top-7` + `nav.hidden.md:flex` + `#webNavToggle` / `#webMobileNav` | sim |
| Idioma | `app/partials/language_selector.php` (`position => 'landing'`) | sim |
| Tema | `#themeToggle` (`[data-theme-icon="moon|sun"]`) | sim |
| Gaveta de portais | `#portalDrawer` (`data-action="open-portal-drawer"` / `close-portal-drawer`) | sim |
| Chat de vendas | `#leadChatToggle`, `#leadChatPanel`, campos `chatLead*` | opcional |
| Consentimento | `app/partials/cookie_consent_modal.php` + `assets/js/consent-cookie.js` | sim |
| Slots | `section('title')`, `section('styles')`, `section('header')`, `section('content')`, `section('scripts')` | — |

## Variantes / Estados

| Estado | Como | Onde ver |
|---|---|---|
| ≥ 1024px | topbar completa com o selo de SLA (`hidden lg:flex`) | Desktop 1440 |
| 768–1023px | navbar completa, sem o selo de SLA | Tablet 1024 |
| < 768px | links da navbar escondidos, `#webNavToggle` abre `#webMobileNav` (`aria-expanded`, `aria-controls`) | Mobile 390 |
| < 640px | "Portais Rápidos" da topbar some (o menu mobile tem "Login do Portal") | Mobile 390 |
| Tema escuro | `html.dark`; lido de `localStorage['ttsc-theme']` (ou o legado `theme`) antes do primeiro paint; o botão grava as duas chaves | alternar tema |
| Cookies | banner até haver decisão em `ttsc_cookie_consent` (o kit já grava `accepted_all`) | — |

## API

| Ponto | Efeito |
|---|---|
| `[data-action="open-portal-drawer"]` / `[data-action="close-portal-drawer"]` | abre/fecha `#portalDrawer` (delegação no `document`) |
| `#webNavToggle` | alterna `#webMobileNav.hidden` e `aria-expanded` |
| `#themeToggle` | alterna `html.dark`, grava `theme` e `ttsc-theme` |
| `#leadChatToggle` / `#leadChatClose` | abre/fecha o chat de vendas; envio `POST {url}/api/leads/capture` (encaminhado ao `OmnichannelRouterService` do SAC) |
| `section('header')` | faixa extra entre o header fixo e o conteúdo |
| `$webTitle`, `$description` | título e meta description; `canonical` montado pela URL atual |

## Acessibilidade

- Header fixo: o conteúdo começa com `pt-44` para não ficar sob a topbar + navbar (28 + 64px).
- Menu mobile com `aria-expanded`/`aria-controls`; o painel tem `nav` com `aria-label`.
- Botão de tema com `aria-label="Alternar tema"` e os dois ícones trocados por CSS (`html.dark [data-theme-icon="moon"]`).
- Imagens do hero e logos com `alt`; ícones decorativos (`fas`/`fa-light`) sem texto lido.
- Verde de destaque do hero (`--color-supa-green`) só em títulos grandes; texto corrido em `--color-text-secondary`.

## Modelos

### HTML

```php
<?php
// resources/views/web/pages/matriculas-2027.php — landing de campanha
$this->layout('web::layouts/main', [
    'title' => 'Matrículas 2027 abertas — TotusTuus SoftCloud',
    'description' => 'Rematrícula on-line, contrato digital e boleto na hora: conheça o módulo de matrículas.',
]);
?>
<?php $this->start('content') ?>
<section class="pt-44 pb-20 relative overflow-hidden bg-[var(--color-bg-base)] transition-colors duration-300">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid lg:grid-cols-2 gap-12 items-center">
    <div>
      <span class="inline-flex items-center gap-2 px-3 py-1 rounded-md border border-[var(--color-border-base)] text-[11px] font-semibold uppercase tracking-wider text-[var(--color-text-secondary)]">
        <span class="w-1.5 h-1.5 rounded-full bg-[var(--color-supa-green)]" aria-hidden="true"></span> Ciclo 2027
      </span>
      <h1 class="mt-6 text-5xl font-medium tracking-tight text-[var(--color-text-primary)]">
        Rematrícula <span class="text-[var(--color-supa-green-link)] font-semibold">sem fila</span> para toda a rede
      </h1>
      <p class="mt-6 text-lg text-[var(--color-text-secondary)]">Contrato assinado no celular, boleto da primeira mensalidade gerado na hora e turma confirmada.</p>
      <div class="mt-8 flex flex-wrap gap-3">
        <a href="#formulario" class="px-6 py-3 rounded-md bg-[var(--color-supa-green)] text-white font-semibold">Falar com um especialista</a>
        <a href="<?= url('/plans') ?>" class="px-6 py-3 rounded-md border border-[var(--color-border-base)] text-[var(--color-text-primary)] font-semibold">Ver planos</a>
      </div>
    </div>
  </div>
</section>
<?php $this->stop() ?>
```

Rota: `$router->get('/matriculas-2027', fn ($request) => view('web::pages/matriculas-2027'));`

### CSS

Ordem real no `<head>`: `fonts/fontawesome.v7.2.0/css/all.css`, `css/tailwind.web.css` (build estático do Tailwind do site — gerado de `assets/css/input.web.css`), `css/web-layout.css`, `css/ttsc.rtl.css`, depois `section('styles')`. O site usa as variáveis próprias `--color-bg-base`, `--color-bg-surface`, `--color-text-primary|secondary|muted`, `--color-border-base|subtle`, `--color-supa-green(-link)` (claro e `html.dark` em `web-layout.css`). Ponte para os tokens do DS ao criar componentes novos:

```css
.web-card {
  background: var(--color-bg-surface, var(--ttsc-surface));
  border: 1px solid var(--color-border-base, var(--ttsc-border));
  border-radius: var(--ttsc-radius-surface);
  color: var(--color-text-primary, var(--ttsc-text));
  box-shadow: var(--ttsc-shadow-sm);
}
.web-card p { color: var(--color-text-secondary, var(--ttsc-text-2)); }
.web-card .web-card__cta { color: var(--color-supa-green-link, var(--ttsc-accent-text)); font-weight: 600; }
```

### JS

Ordem real: scripts inline do layout (tema, menu mobile, gaveta de portais, chat de vendas), `consent-cookie.js`, `section('scripts')`.

```js
// Envio do formulário de interesse da landing para o mesmo endpoint do chat de vendas
(function () {
  var form = document.getElementById('formMatriculas2027');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var btn = form.querySelector('[type="submit"]'); btn.disabled = true;
    fetch(form.action, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
      body: JSON.stringify(Object.fromEntries(new FormData(form)))
    })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function () { form.replaceChildren(Object.assign(document.createElement('p'), { textContent: 'Recebemos seu contato. Retornamos em até 1 dia útil.' })); })
      .catch(function () { btn.disabled = false; alert('Não foi possível enviar agora. Tente novamente em instantes.'); });
  });
})();
```

### SQL

A home é estática; a seção de planos/ROI e a página `/plans` podem ler os planos ativos (banco **master**):

```sql
SELECT uuid, code, name, description, periodicity, base_amount, currency
  FROM billing_plans
 WHERE status = 'active'
   AND deleted_at IS NULL
   AND (valid_until IS NULL OR valid_until >= CURDATE())
 ORDER BY base_amount;
```

O PHP formata `base_amount` com `ttsc_format` (moeda do locale) e entrega a lista à view; os contatos do chat/formulário viram atendimento no SAC via `POST api/leads/capture`.

## Como começar um projeto a partir do kit

1. **Arquivos do kit**: `kit.html` + `assets/css/{tailwind.web.css, web-layout.css, ttsc.rtl.css}`, `assets/js/consent-cookie.js`, `assets/vendors/chartjs/chart.umd.min.js` (gráficos da home), `assets/images/dashboard-academic.png`, `assets/media/` (logo e bandeiras) e `assets/fa.css`. Gerado por `$SPD/dsh/gen_kits.py` a partir de `php $SPD/app/view_harness.php / web::pages/home …`.
2. **Nova página no repo**: view em `resources/views/web/pages/`, `$this->layout('web::layouts/main', ['title' => …, 'description' => …])`, rota GET em `routes/web.php`.
3. **Outro projeto**: copie `web/layouts/main.php`, `app/partials/{locale_init,language_selector,cookie_consent_modal}.php`, `assets/css/{tailwind.web.css,web-layout.css,ttsc.rtl.css}` (ou recompile `input.web.css` com Tailwind v4), `assets/js/consent-cookie.js`, `fonts/fontawesome.v7.2.0/` e `media/app/*`.

## Faça / Não faça

- **Faça:** `title` e `description` próprios por página (SEO e cartões sociais).
- **Faça:** deixe o conteúdo começar abaixo do header fixo (`pt-44` no primeiro bloco).
- **Faça:** use as variáveis `--color-*` do site para manter claro/escuro.
- **Não faça:** carregar `bundle`/CSS do app (`ttsc.design-system.css`) no site — são camadas diferentes.
- **Não faça:** usar o CDN `@tailwindcss/browser`; o site já tem o build estático `tailwind.web.css`.
