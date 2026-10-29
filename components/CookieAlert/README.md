# Cookie Alert

Banner de consentimento de cookies da LGPD (Privacy First) com “Aceitar todos”, “Rejeitar não essenciais” e “Personalizar” por categoria — mesma lógica e chaves de `assets/js/consent-cookie.js` (`ttsc_cookie_consent` + cookie `cookie_consent`).

## Quando usar

- Uma única vez por layout público e autenticado (`resources/views/app/partials/cookie_consent_modal.php`), antes de qualquer cookie não essencial.
- Para reabrir a escolha: link “Preferências de cookies” no rodapé/perfil chamando `window.openCookiePreferences()`.
- **Não use** para avisos gerais ou manutenção: use [Alert](../Alert/README.md) ou [Toast](../Toast/README.md).
- **Não use** para o consentimento de tratamento de dados com base legal específica (termos de matrícula, uso de imagem): isso fica em `consent_records` / `pastoral_consents`, com fluxo próprio.
- Para gravar a preferência de UI depois do consentimento, veja [Cookie](../Cookie/README.md).

## Anatomia

```
#cookieConsentBanner (fixed bottom, role=region)
[ ícone ] [ título #consentBannerTitle · texto #consentBannerText · link política ]  [Rejeitar] [Personalizar] [Aceitar todos]

#cookiePreferencesModal (role=dialog)
  header "Preferências de cookies"
  #cookiePreferencesList → .cookie-cat-row × N  [checkbox .consent-category-checkbox] nome · descrição · "Sempre ativo"
  footer [Salvar preferências]
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Banner | `#cookieConsentBanner` + `data-config-url` + `data-decisions-url` | sim |
| Título / texto | `#consentBannerTitle` · `#consentBannerText` (sobrescritos pela versão do banner) | sim |
| Ações | `data-consent-action="accept-all \| reject \| customize"` em `#consentAcceptAll`, `#consentRejectAll`, `#consentCustomize` | sim |
| Painel | `#cookiePreferencesModal` (`role="dialog"`, `aria-modal`) | sim |
| Lista | `#cookiePreferencesList` → `.cookie-cat-row` | gerado |
| Categoria | `input.consent-category-checkbox[data-category-id]` (`disabled` se essencial) | gerado |
| Salvar / fechar | `data-consent-action="save-preferences"` · `"close-preferences"` | sim |

## Estados

| Estado | Condição | Tokens |
|---|---|---|
| Oculto (sem flicker) | `localStorage.ttsc_cookie_consent` **ou** cookie `cookie_consent` presente no parse do script | — |
| Visível | nenhuma decisão local nem `current_consent` do servidor (ou fetch falhou) | fundo `ttsc-surface`, borda `ttsc-border`, `ttsc-shadow-lg`, z `ttsc-z-toast` |
| Personalizando | `#cookiePreferencesModal` sem `.hidden` | véu `ttsc-scrim` |
| Essencial | checkbox `checked disabled` + badge “Sempre ativo” | badge outline |
| Decidido | `accepted_all` · `rejected_non_essential` · `customized` | — |

## API

| Item | Valor |
|---|---|
| `localStorage` | `ttsc_cookie_consent` = decisão; `ttsc_cookie_consent_data` = `{decision, categories:[{id, granted}], timestamp}` |
| Cookie cliente | `cookie_consent=<decisão>; path=/; expires=+1 ano; SameSite=Lax; Secure` (em HTTPS) — lido pelo `PrivacyController` |
| `GET data-config-url` (`/privacy/consent-config`) | `{success, categories:[{id,name,description,is_essential}], banner:{id, banner_title, banner_text, accept_all_label, reject_all_label, customize_label}, current_consent}` |
| `POST data-decisions-url` (`/privacy/consent-decisions`) | corpo `{decision, categories, banner_version_id}` + `X-CSRF-TOKEN` (endpoint público no `CsrfMiddleware`); decisões válidas: `accepted_all`, `rejected_non_essential`, `customized` |
| `window.openCookiePreferences()` | abre o painel e esconde o banner |
| `window.closeCookiePreferences()` | fecha o painel |
| `window.resetCookieConsent()` | apaga storage e cookie e reexibe o banner |
| Evento `cookie_consent_saved` (window) | `detail: {decision, categories}` — carregue scripts opcionais aqui |

## Acessibilidade

- Banner com `role="region"` + `aria-labelledby="consentBannerTitle"`; painel com `role="dialog"`, `aria-modal="true"`, `aria-labelledby="cookiePrefTitle"` e foco no primeiro checkbox editável ao abrir.
- “Rejeitar” tem o **mesmo peso visual** de “Aceitar” (outline × primary, mesmo tamanho) — exigência de consentimento livre; nada de link cinza minúsculo.
- Cada checkbox tem `<label for>`; essenciais ficam `disabled` com o texto “Sempre ativo” (não só cor).
- Texto em `ttsc-text`/`ttsc-text-muted`; link da política em `ttsc-accent-text`; ícone em `ttsc-accent-text` sobre `ttsc-accent-soft`.

## Modelos

### HTML

```html
<!-- resources/views/app/partials/cookie_consent_modal.php -->
<div id="cookieConsentBanner" class="ttsc-cookie-banner hidden" role="region" aria-labelledby="consentBannerTitle"
     data-config-url="/privacy/consent-config" data-decisions-url="/privacy/consent-decisions">
  <div class="ttsc-cookie-icon" aria-hidden="true"><i class="fa-light fa-cookie-bite"></i></div>
  <div class="ttsc-cookie-text">
    <h3 id="consentBannerTitle"><?= __('privacy_first', 'cookies', 'Sua privacidade em primeiro lugar') ?></h3>
    <p id="consentBannerText">Usamos cookies essenciais para o login e, com sua permissão, cookies de preferências e análise.
      <a href="/privacidade/cookies">Política de cookies</a></p>
  </div>
  <div class="flex flex-wrap gap-2">
    <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-sm" data-consent-action="reject" id="consentRejectAll">Rejeitar não essenciais</button>
    <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-sm" data-consent-action="customize" id="consentCustomize">Personalizar</button>
    <button type="button" class="ttsc-btn ttsc-btn-primary ttsc-btn-sm" data-consent-action="accept-all" id="consentAcceptAll">Aceitar todos</button>
  </div>
</div>

<div id="cookiePreferencesModal" class="hidden" style="position: fixed; inset: 0; z-index: var(--ttsc-z-modal)"
     role="dialog" aria-modal="true" aria-labelledby="cookiePrefTitle">
  <div style="position: fixed; inset: 0; background: var(--ttsc-scrim)" data-consent-action="close-preferences"></div>
  <section class="ttsc-cookie-prefs">
    <header><i class="fa-light fa-sliders"></i> <span id="cookiePrefTitle">Preferências de cookies</span>
      <button type="button" class="ttsc-btn ttsc-btn-ghost ttsc-btn-icon ttsc-btn-sm" aria-label="Fechar" data-consent-action="close-preferences"><i class="fa-light fa-xmark"></i></button>
    </header>
    <div class="cookie-cat-list" id="cookiePreferencesList"></div>
    <footer>
      <button type="button" class="ttsc-btn ttsc-btn-primary ttsc-btn-sm" data-consent-action="save-preferences">Salvar preferências</button>
    </footer>
  </section>
</div>
<script src="/assets/js/consent-cookie.js"></script>
```

### CSS

Versão com tokens do CSS inline do partial (que hoje usa `--bg`, `--sb-surface` e `.dark`):

```css
.ttsc-cookie-banner {
  position: fixed; inset: auto 0 0 0; z-index: var(--ttsc-z-toast);
  display: flex; align-items: center; gap: var(--ttsc-space-4); flex-wrap: wrap; padding: 14px 16px;
  background: var(--ttsc-surface); border-top: 1px solid var(--ttsc-border); box-shadow: var(--ttsc-shadow-lg);
}
.ttsc-cookie-banner.hidden { display: none; }
.ttsc-cookie-icon {
  width: 36px; height: 36px; border-radius: var(--ttsc-radius-control); flex: none;
  display: flex; align-items: center; justify-content: center;
  background: var(--ttsc-accent-soft); color: var(--ttsc-accent-text);
}
.ttsc-cookie-text h3 { font-size: 13px; font-weight: 600; color: var(--ttsc-text); }
.ttsc-cookie-text p  { font-size: 12px; line-height: 1.5; color: var(--ttsc-text-muted); }
.ttsc-cookie-text a  { color: var(--ttsc-accent-text); }
.ttsc-cookie-prefs {
  position: relative; max-width: 560px; margin: 10vh auto 0;
  background: var(--ttsc-surface); border: 1px solid var(--ttsc-border);
  border-radius: var(--ttsc-radius-surface); box-shadow: var(--ttsc-shadow-xl);
}
.cookie-cat-row { display: flex; align-items: flex-start; gap: 12px; padding: 12px; border: 1px solid var(--ttsc-border-soft); border-radius: var(--ttsc-radius-control); }
.cookie-cat-row:hover { background: var(--ttsc-canvas-2); }
```

### JS

Trecho essencial do `assets/js/consent-cookie.js` (não reescreva — inclua o arquivo). Integração recomendada para scripts opcionais:

```js
// Chaves e persistência (consent-cookie.js)
var STORAGE_KEY = 'ttsc_cookie_consent';
var STORAGE_DATA_KEY = 'ttsc_cookie_consent_data';

function syncClientCookie(value) {
  var expires = new Date(Date.now() + 365 * 864e5).toUTCString();
  document.cookie = 'cookie_consent=' + encodeURIComponent(value) + '; path=/; expires=' + expires +
    '; SameSite=Lax' + (location.protocol === 'https:' ? '; Secure' : '');
}

function persistConsent(decision, categories) {
  localStorage.setItem(STORAGE_KEY, decision);
  localStorage.setItem(STORAGE_DATA_KEY, JSON.stringify({ decision, categories: categories || [], timestamp: Date.now() }));
  syncClientCookie(decision);
  document.getElementById('cookieConsentBanner')?.classList.add('hidden');
  closeCookiePreferences();
  window.dispatchEvent(new CustomEvent('cookie_consent_saved', { detail: { decision, categories } }));
}
// acceptAllCookies → 'accepted_all' | rejectNonEssential → 'rejected_non_essential' | saveCookiePreferences → 'customized'
// submitConsent() persiste no cliente primeiro e depois faz POST em data-decisions-url com X-CSRF-TOKEN.

// --- Uso em outros módulos: só carregar analytics com categoria concedida ---
function hasCategory(id) {
  try {
    const data = JSON.parse(localStorage.getItem('ttsc_cookie_consent_data') || 'null');
    return !!data?.categories?.find((c) => c.id === id && c.granted);
  } catch (e) { return false; }
}
function loadAnalytics() { if (hasCategory('analytics')) import('/assets/js/ttsc.analytics-data.js'); }
loadAnalytics();
window.addEventListener('cookie_consent_saved', loadAnalytics);
```

### SQL

Tabelas reais: `privacy_cookie_categories` (catálogo), `privacy_consent_banner_versions` (texto versionado), `user_cookie_consents` (decisão) e `user_cookie_consent_items` (categoria a categoria).

```sql
-- consent-config: categorias ativas do tenant
SELECT c.id, c.code, c.name, c.description, c.is_essential
  FROM privacy_cookie_categories c
 WHERE c.tenant_id = :tenant_id AND c.is_active = 1
 ORDER BY c.sort_order, c.name;

-- consent-config: versão publicada do banner
SELECT b.id, b.version, b.banner_title, b.banner_text,
       b.accept_all_label, b.reject_all_label, b.customize_label, b.privacy_policy_url
  FROM privacy_consent_banner_versions b
 WHERE b.tenant_id = :tenant_id AND b.is_active = 1
 ORDER BY b.published_at DESC
 LIMIT 1;

-- consent-decisions: registro com IP/UA em hash (prova de consentimento)
INSERT INTO user_cookie_consents
       (id, uuid, code, tenant_id, user_id, session_id, banner_version_id, decision,
        ip_address_hash, user_agent_hash, language, consent_proof)
VALUES (:id, :uuid, :code, :tenant_id, :user_id, :session_id, :banner_version_id, :decision,
        SHA2(:ip, 256), SHA2(:user_agent, 256), :language, :consent_proof);

INSERT INTO user_cookie_consent_items (id, uuid, code, consent_id, category_id, granted)
VALUES (:item_id, :item_uuid, :item_code, :consent_id, :category_id, :granted);  -- uma linha por categoria

-- current_consent: última decisão não revogada do usuário/sessão
SELECT uc.id, uc.decision, uc.consented_at, ci.category_id, ci.granted
  FROM user_cookie_consents uc
  LEFT JOIN user_cookie_consent_items ci ON ci.consent_id = uc.id
 WHERE uc.tenant_id = :tenant_id
   AND (uc.user_id = :user_id OR uc.session_id = :session_id)
   AND uc.revoked_at IS NULL
 ORDER BY uc.consented_at DESC
 LIMIT 20;
```

O `PrivacyController::consentConfig` devolve as categorias e o banner em JSON; o JS pinta os textos nos IDs do partial. Revogação (`/privacy/consent-revoke`) grava `revoked_at` e o front chama `resetCookieConsent()`.

## Faça / Não faça

- **Faça:** incluir `consent-cookie.js` o mais cedo possível no `<body>` (fast-path esconde o banner antes do primeiro paint).
- **Faça:** condicionar qualquer script de análise/marketing ao evento `cookie_consent_saved` e à categoria concedida.
- **Faça:** versionar o texto em `privacy_consent_banner_versions` e pedir novo consentimento (`requires_reconsent`) quando a política mudar.
- **Não faça:** pré-marcar categorias não essenciais no servidor sem decisão do titular, nem esconder “Rejeitar”.
- **Não faça:** gravar IP ou User-Agent em claro — só o hash SHA-256.
- **Não faça:** trocar as chaves `ttsc_cookie_consent` / `cookie_consent`: o PHP (`$_COOKIE['cookie_consent']`) depende delas.
