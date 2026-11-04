# Configurações do sistema

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Segurança e operação
- Domínio: plataforma (banco master), instância separada do módulo das entidades ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2.1)
- Status: detalhado; especificação da v1 absorvida integralmente (seção 13), com as correções da v2 e as decisões por padrão (seções 1 a 12)
- Fonte da v1: [language_locale_selector_spec.md](../../../docs/v2/anexo-v1/language_locale_selector_spec.md) (387 linhas); [06-i18n-l10n.md](../../../docs/v2/anexo-v1/06-i18n-l10n.md) (223 linhas)

## 1. Regra de leitura
As seções 1 a 12 prevalecem sobre a seção 13. A seção 13 é o texto integral da v1, sem corte, para que nenhum detalhe se perca. Quando a seção 13 disser algo diferente das seções 1 a 12, vale o que está nas seções 1 a 12.

## 2. Objetivo e escopo
Manter as configurações globais da plataforma, agrupadas pelo documento do SDD que define cada regra, com mudança auditada e reversível.

## 3. Telas (índice da v1)
**language_locale_selector_spec.md**

- 1. Overview
- 2. Problem Statement
- 3. Design Principles
- 4. Data Model
  - Exemplo de catálogo
- 5. Component Structure
  - Anatomia do item de lista
- 6. Behavior Rules
- 7. Accessibility Requirements
- 8. Visual Design Guidelines
  - Antes vs Depois
- 9. Separation of Concerns
- 10. Frontend Implementation (Vanilla JS + PHP)
- 11. API Specification
  - Get available locales
  - Update user locale preference
  - Get translation bundle
- 12. Translation File Structure
- 13. RTL Support Checklist
- 14. Acceptance Criteria
- 15. Rollout Plan

**06-i18n-l10n.md**

- 1. Executive Summary
  - Current State vs Spec
- 2. Architecture
  - 2.1 Current Architecture
  - 2.2 Target Architecture (per spec)
- 3. Data Model Gaps
  - 3.1 Current `TranslationService::LOCALES`
  - 3.2 Required Data Model (per spec)
  - 3.3 Migration Required
- 4. API Endpoints Missing
  - 4.1 `GET /api/v1/system/locales`
  - 4.2 `PATCH /api/v1/users/me/locale`
  - 4.3 `GET /api/v1/i18n/bundles/{locale}`
- 5. RTL Support Gaps
- 6. Accessibility Gaps
- 7. Separation of Concerns
- 8. Translation Governance Gaps
- 9. Implementation Plan
  - Priority Order

## 4. Correções da v2 que prevalecem
- **Idiomas e locale:** o [09](../../../docs/v2/09-internacionalizacao.md) prevalece; as especificações da v1 de idioma e seletor de locale estão consolidadas nele ([12](../../../docs/v2/12-catalogo-modulos.md)).
- **Grupos de configuração** (DP-04): idiomas e formatos ([09](../../../docs/v2/09-internacionalizacao.md)); senha, sessão e MFA ([06](../../../docs/v2/06-identidade-acesso.md)); limites de API ([04](../../../docs/v2/04-api.md)); e-mail e integrações ([16](../../../docs/v2/16-integracoes-externas.md)); cache ([30](../../../docs/v2/30-cache.md)); manutenção ([24](../../../docs/v2/24-operacao-continuidade-qualidade.md)); tokens e webhooks ([04](../../../docs/v2/04-api.md), [16](../../../docs/v2/16-integracoes-externas.md)).
- **Valor fora do limite** do documento de origem é recusado (por exemplo, sessão mais longa que o máximo do 06).
- Configurações de entidade (feriados, fuso, campos personalizados) ficam no portal de gestão ([56](../../../docs/v2/56-configuracoes-e-relatorios-lacunas.md), seção 2).

## 5. Decisões por padrão aplicadas
- **DP-04** ([80](../../../docs/v2/80-decisoes-por-padrao.md)): grupos pelo documento de origem; toda mudança com step-up, motivo, auditoria e versão com rollback.

## 6. Permissões e papéis
- `platform.developer`: alterar configurações de segurança e de limites.
- `platform.ops`: alterar configurações operacionais (cache, manutenção).
- Toda mudança vista por `platform.auditor`.

## 7. Dados
- Configurações versionadas no master: chave, valor, versão, autor, motivo, data.

## 8. Integrações
- Cache: invalidação na mudança de configuração ([30](../../../docs/v2/30-cache.md)).

## 9. Exportação, auditoria e privacidade
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Auditoria conforme [29](../../../docs/v2/29-auditoria.md); dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md).


## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
- Nenhuma além das do [09](../../../docs/v2/09-internacionalizacao.md).

## 13. Conteúdo integral da v1 (absorvido)

### Fonte: language_locale_selector_spec.md

#### SPEC — Language & Locale Selector Component (i18n/l10n)

##### 1. Overview

```yaml
component_name: LanguageLocaleSelector
type: ui_component
category: internationalization
scope: global_navbar
reusable: true
base_language: en
```

Componente global de seleção de idioma e localidade, usado no cabeçalho de todos os painéis do SaaS (Developer Panel, Client SaaS Panel, Third-Party Portal). Segue boas práticas de UX que separam **idioma** de **país/bandeira**, evitando o erro comum de mapear bandeira 1:1 com idioma.

---

##### 2. Problem Statement

- Bandeiras representam países, não idiomas.
- Espanhol é falado em mais de 20 países; árabe em dezenas — uma única bandeira apaga essa diversidade.
- Usuários podem preferir um idioma diferente do associado à bandeira do seu país (ex: imigrante, expatriado, preferência pessoal).
- Guias oficiais de design (USWDS) recomendam não usar bandeira nem código de país como indicador principal de idioma.

---

##### 3. Design Principles

```yaml
principles:
  - label_in_native_language
  - flag_as_secondary_visual_only
  - disambiguate_regional_variants
  - persist_user_choice
  - correct_lang_and_hreflang_attributes
  - decouple_locale_from_country_and_currency
  - accessible_keyboard_and_screen_reader_support
```

---

##### 4. Data Model

```yaml
Locale:
  code: string            # ISO 639-1 (ex: pt, en, es)
  region_code: string|null # ISO 3166-1 alpha-2 (ex: BR, US, PT)
  bcp47_tag: string        # ex: pt-BR, en-US, es-ES
  native_name: string      # ex: "Português", "English", "Español"
  english_name: string     # ex: "Portuguese", "English", "Spanish"
  direction: ltr|rtl
  flag_icon: string|null   # opcional, uso apenas decorativo
  currency_code: string|null   # ISO 4217, independente do locale
  date_format: string
  number_format: string
  is_default: boolean
  status: active|beta|deprecated
```

###### Exemplo de catálogo

```json
[
  { "code": "pt", "region_code": "BR", "bcp47_tag": "pt-BR", "native_name": "Português (Brasil)", "direction": "ltr" },
  { "code": "en", "region_code": "US", "bcp47_tag": "en-US", "native_name": "English (US)", "direction": "ltr" },
  { "code": "es", "region_code": "ES", "bcp47_tag": "es-ES", "native_name": "Español (España)", "direction": "ltr" },
  { "code": "fr", "region_code": "FR", "bcp47_tag": "fr-FR", "native_name": "Français (France)", "direction": "ltr" },
  { "code": "de", "region_code": "DE", "bcp47_tag": "de-DE", "native_name": "Deutsch (Deutschland)", "direction": "ltr" },
  { "code": "it", "region_code": "IT", "bcp47_tag": "it-IT", "native_name": "Italiano (Italia)", "direction": "ltr" },
  { "code": "zh", "region_code": "CN", "bcp47_tag": "zh-CN", "native_name": "中文（简体）", "direction": "ltr" },
  { "code": "ja", "region_code": "JP", "bcp47_tag": "ja-JP", "native_name": "日本語", "direction": "ltr" },
  { "code": "ru", "region_code": "RU", "bcp47_tag": "ru-RU", "native_name": "Русский", "direction": "ltr" },
  { "code": "ar", "region_code": "SA", "bcp47_tag": "ar-SA", "native_name": "العربية", "direction": "rtl" }
]
```

---

##### 5. Component Structure

```yaml
component_tree:
  - LanguageSelectorTrigger
      - current_locale_badge
      - dropdown_icon
  - LanguageSelectorDropdown
      - search_input (optional, for 10+ locales)
      - locale_list
          - locale_item
              - flag_icon (decorative, aria-hidden)
              - native_name_label
              - checkmark_if_selected
      - footer_link_to_full_settings (optional)
```

###### Anatomia do item de lista

```html
<button role="option" lang="pt-BR" aria-selected="true">
  <img src="/flags/br.svg" alt="" aria-hidden="true" class="flag-icon" />
  <span class="locale-code">PT</span>
  <span class="locale-native-name">Português (Brasil)</span>
</button>
```

---

##### 6. Behavior Rules

```yaml
behavior:
  default_locale_resolution_order:
    - user_saved_preference
    - browser_accept_language_header
    - tenant_default_locale
    - system_default_locale (en)

  on_change:
    - update_html_lang_attribute
    - update_html_dir_attribute_if_rtl
    - persist_to_user_profile
    - persist_to_local_storage
    - reload_translated_strings
    - do_not_reload_full_page_when_possible
    - emit_locale_changed_event

  persistence:
    priority_1: authenticated_user_profile
    priority_2: cookie_or_local_storage
    priority_3: session_default

  fallback:
    missing_translation_key: fallback_to_english
    missing_locale_asset: fallback_to_base_language
```

---

##### 7. Accessibility Requirements

```yaml
accessibility:
  - role: listbox_and_option_pattern
  - aria-label: "Select language"
  - aria-selected_on_active_item
  - keyboard_navigation:
      - arrow_up_down_to_navigate
      - enter_to_select
      - escape_to_close
      - tab_to_focus_trigger
  - flag_icons_must_have_empty_alt_or_aria-hidden
  - text_labels_are_the_primary_accessible_name
  - lang_attribute_per_option
  - contrast_ratio_minimum: 4.5:1
```

---

##### 8. Visual Design Guidelines

```yaml
visual_guidelines:
  flag_role: decorative_secondary_only
  primary_label: native_language_name
  secondary_label: iso_code (optional, small caps)
  selected_state: checkmark_or_highlighted_background
  hover_state: subtle_background_change
  rtl_support: mirror_layout_for_ar_he_fa
  max_visible_items_before_scroll: 8
  search_enabled_threshold: locales_count > 8
```

###### Antes vs Depois

| Aspecto | Padrão atual (bandeira + código país) | Padrão recomendado |
|---|---|---|
| Rótulo principal | Código de país (BR, US, ES) | Nome nativo do idioma |
| Papel da bandeira | Indicador primário | Apenas decorativo |
| Ambiguidade | Alta (país ≠ idioma) | Baixa (nome nativo é claro) |
| Acessibilidade | Depende da bandeira | Baseada em texto e `lang` |
| Variantes regionais | Não diferenciadas | Diferenciadas (pt-BR vs pt-PT) |

---

##### 9. Separation of Concerns

```yaml
independent_settings:
  interface_language: locale.bcp47_tag
  document_language: invoice_or_content_locale
  currency: currency_code
  timezone: iana_timezone
  date_format: locale.date_format
  number_format: locale.number_format
```

O idioma da interface, o idioma de documentos gerados (ex: invoices), a moeda e o fuso horário devem ser configuráveis de forma independente, permitindo, por exemplo, interface em inglês com documento fiscal em português e moeda em reais.

---

##### 10. Frontend Implementation (Vanilla JS + PHP)

```javascript
class LanguageLocaleSelector {
  constructor(config) {
    this.locales = config.locales;
    this.current = this.resolveInitialLocale(config);
    this.onChangeCallback = config.onChange;
  }

  resolveInitialLocale(config) {
    return config.userPreference
      || this.parseAcceptLanguage(navigator.language)
      || config.tenantDefault
      || 'en';
  }

  parseAcceptLanguage(navigatorLang) {
    const match = this.locales.find(l => l.bcp47_tag === navigatorLang);
    return match ? match.bcp47_tag : null;
  }

  select(bcp47Tag) {
    const locale = this.locales.find(l => l.bcp47_tag === bcp47Tag);
    if (!locale) return;

    this.current = locale.bcp47_tag;
    document.documentElement.lang = locale.code;
    document.documentElement.dir = locale.direction;

    localStorage.setItem('preferred_locale', locale.bcp47_tag);
    this.persistToProfile(locale.bcp47_tag);

    document.dispatchEvent(new CustomEvent('locale:changed', {
      detail: { locale: locale.bcp47_tag }
    }));

    if (this.onChangeCallback) {
      this.onChangeCallback(locale);
    }
  }

  async persistToProfile(bcp47Tag) {
    await fetch('/api/v1/users/me/locale', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ locale: bcp47Tag })
    });
  }
}
```

---

##### 11. API Specification

###### Get available locales

```http
GET /api/v1/system/locales
```

```json
{
  "data": [
    { "bcp47_tag": "en-US", "native_name": "English (US)", "status": "active" },
    { "bcp47_tag": "pt-BR", "native_name": "Português (Brasil)", "status": "active" }
  ]
}
```

###### Update user locale preference

```http
PATCH /api/v1/users/me/locale
```

```json
{ "locale": "pt-BR" }
```

###### Get translation bundle

```http
GET /api/v1/i18n/bundles/{locale}
```

```json
{
  "locale": "pt-BR",
  "version": "2026.08.28",
  "strings": {
    "nav.dashboard": "Painel",
    "action.save": "Salvar",
    "invoicing.status.authorized": "Autorizada"
  }
}
```

---

##### 12. Translation File Structure

```text
/lang
  /en
    common.json
    navigation.json
    invoicing.json
    validation.json
  /pt-BR
    common.json
    navigation.json
    invoicing.json
    validation.json
  /es
    common.json
    ...
  /ar
    common.json
    ...
```

```yaml
translation_governance:
  source_of_truth: en
  translation_workflow: professional_or_reviewed_machine_translation
  missing_key_behavior: fallback_to_en_and_log_warning
  versioning: per_bundle_timestamp
  automated_key_extraction: true
  ci_check: fail_build_on_missing_keys
```

---

##### 13. RTL Support Checklist

```yaml
rtl_checklist:
  - html_dir_attribute_set_to_rtl
  - mirrored_navigation_and_dropdown
  - mirrored_icons_where_directional
  - text_alignment_right
  - number_and_date_formatting_preserved_ltr_within_rtl_context
  - form_field_alignment_mirrored
  - tested_with_arabic_and_hebrew_content
```

---

##### 14. Acceptance Criteria

- O rótulo principal de cada opção exibe o nome do idioma em sua própria língua, não o código do país.
- A bandeira aparece apenas como elemento visual decorativo (`aria-hidden`), nunca como único identificador.
- Variantes regionais do mesmo idioma (pt-BR, pt-PT / en-US, en-GB) são exibidas de forma distinta.
- A escolha do usuário é persistida no perfil e recuperada em qualquer dispositivo após login.
- A troca de idioma não recarrega a página inteira quando technicamente viável.
- O atributo `lang` do HTML é atualizado corretamente a cada troca.
- Idiomas RTL (árabe) espelham corretamente o layout.
- Chaves de tradução ausentes fazem fallback para inglês sem quebrar a interface.
- O componente é navegável inteiramente via teclado e compatível com leitores de tela.
- Moeda, fuso horário e idioma podem ser configurados de forma independente pelo usuário ou pela entidade.

---

##### 15. Rollout Plan

```yaml
phase_1:
  - implement_component_with_en_pt_BR_es
  - persist_preference_in_profile_and_local_storage
  - basic_keyboard_accessibility

phase_2:
  - add_fr_de_it
  - add_search_input_for_dropdown
  - add_ci_check_for_missing_translation_keys

phase_3:
  - add_zh_ja_ru
  - performance_audit_for_bundle_loading

phase_4:
  - add_ar_with_full_rtl_support
  - accessibility_audit_wcag_2_2
  - full_regression_test_across_all_locales
```

### Fonte: 06-i18n-l10n.md

#### SDD 06 — Internationalization & Localization (i18n/l10n)

> **Derived from:** `sdd-mestre-php8-mvc-saas.md` (Section: Artefatos derivados obrigatórios)
> **Spec reference:** `docs/language_locale_selector_spec.md`
> **Date:** 2026-08-28
> **Status:** Implementation gaps identified — plan below

---

##### 1. Executive Summary

The TotusTuus SoftCloud platform supports 10 locales (en, pt-BR, es, fr, de, it, zh, ja, ru, ar) with a database-driven translation system. The `language_locale_selector_spec.md` defines the ideal UX/architecture for language selection, but the current implementation has significant gaps that must be addressed.

###### Current State vs Spec

| Aspect | Spec Requirement | Current State | Gap |
|--------|-----------------|---------------|-----|
| Component class | `LanguageLocaleSelector` JS class | Not implemented | 🔴 Full |
| Data model | `bcp47_tag`, `native_name`, `english_name`, `direction`, `flag_icon`, `currency_code`, `date_format`, `number_format`, `is_default`, `status` | `LOCALES` constant with `name`, `flag`, `dir` only | 🔴 Partial |
| Flag usage | Decorative only (`aria-hidden`) | Primary identifier in UI | 🔴 Inverted |
| API: GET locales | `GET /api/v1/system/locales` | Not implemented | 🔴 Full |
| API: PATCH user locale | `PATCH /api/v1/users/me/locale` | Not implemented | 🔴 Full |
| API: GET translation bundle | `GET /api/v1/i18n/bundles/{locale}` | Not implemented (DB-driven) | 🟡 Architecture different |
| Persistence | Profile > localStorage > session | Session + DB only | 🟡 Partial |
| RTL support | Full checklist (mirror nav, icons, forms) | Basic `dir` attribute | 🟡 Partial |
| Accessibility | Keyboard nav, ARIA, screen reader | Basic dropdown | 🟡 Partial |
| Separation of concerns | Language, currency, timezone, date format independent | Language only | 🔴 Missing |
| Search input | For 10+ locales | Not implemented | 🔴 Missing |
| Translation governance | CI check, missing key fallback, versioning | CI check exists, no versioning | 🟡 Partial |

---

##### 2. Architecture

###### 2.1 Current Architecture

```
TranslationService (Singleton)
  ├── LOCALES constant (10 locales)
  ├── DB-driven translations (translations table)
  ├── __() helper function
  ├── Cache in-memory per request
  └── language_selector.php partial (flag-based dropdown)
```

###### 2.2 Target Architecture (per spec)

```
LanguageLocaleSelector (JS Class)
  ├── Locale Catalog (enhanced data model)
  ├── Dropdown Component (search, keyboard, ARIA)
  ├── Persistence Layer (profile → localStorage → session)
  ├── API Layer (GET /locales, PATCH /me/locale)
  ├── Event System (locale:changed custom event)
  └── html lang/dir attribute sync

TranslationService (PHP Singleton)
  ├── DB-driven translations (existing)
  ├── __() helper (existing)
  ├── Bundle API endpoint (new)
  └── Locale resolution order (new)
```

---

##### 3. Data Model Gaps

###### 3.1 Current `TranslationService::LOCALES`

```php
public const LOCALES = [
    'en' => ['name' => 'English', 'flag' => 'united-states', 'dir' => 'ltr'],
    'pt-br' => ['name' => 'Português', 'flag' => 'brazil', 'dir' => 'ltr'],
    // ...
];
```

###### 3.2 Required Data Model (per spec)

```php
public const LOCALES = [
    'pt-BR' => [
        'code' => 'pt',
        'region_code' => 'BR',
        'bcp47_tag' => 'pt-BR',
        'native_name' => 'Português (Brasil)',
        'english_name' => 'Portuguese (Brazil)',
        'direction' => 'ltr',
        'flag_icon' => 'br',           // decorative only
        'currency_code' => 'BRL',
        'date_format' => 'd/m/Y',
        'number_format' => '#.##0,00',
        'is_default' => false,
        'status' => 'active',
    ],
    // ...
];
```

###### 3.3 Migration Required

Add columns to `translations` table or create new `locales` table:
- `bcp47_tag` (primary key)
- `native_name`
- `english_name`
- `currency_code`
- `date_format`
- `number_format`
- `is_default`
- `status`

---

##### 4. API Endpoints Missing

###### 4.1 `GET /api/v1/system/locales`

Returns active locales for the public catalog.

```json
{
  "data": [
    { "bcp47_tag": "en-US", "native_name": "English (US)", "status": "active" },
    { "bcp47_tag": "pt-BR", "native_name": "Português (Brasil)", "status": "active" }
  ]
}
```

###### 4.2 `PATCH /api/v1/users/me/locale`

Updates authenticated user's locale preference.

```json
{ "locale": "pt-BR" }
```

###### 4.3 `GET /api/v1/i18n/bundles/{locale}`

Returns translation bundle for client-side use (optional, for SPA-like behavior).

```json
{
  "locale": "pt-BR",
  "version": "2026.08.28",
  "strings": {
    "nav.dashboard": "Painel",
    "action.save": "Salvar"
  }
}
```

---

##### 5. RTL Support Gaps

Current implementation sets `dir="rtl"` on `<html>` for Arabic. Per spec, the following are missing:

- [ ] Mirror navigation and dropdowns
- [ ] Mirror directional icons
- [ ] Text alignment right
- [ ] Number/date formatting preserved LTR within RTL context
- [ ] Form field alignment mirrored
- [ ] Tested with Arabic and Hebrew content

---

##### 6. Accessibility Gaps

Current `language_selector.php` is a basic dropdown. Per spec:

- [ ] `role="listbox"` and `role="option"` pattern
- [ ] `aria-label="Select language"` on trigger
- [ ] `aria-selected` on active item
- [ ] Keyboard: arrow up/down, enter to select, escape to close
- [ ] Flag icons with `alt=""` and `aria-hidden="true"`
- [ ] `lang` attribute per option
- [ ] Contrast ratio minimum 4.5:1

---

##### 7. Separation of Concerns

The spec requires independent configuration of:

| Setting | Current | Required |
|---------|---------|----------|
| Interface language | ✅ Via profile | ✅ |
| Document language (invoices) | ❌ Not separate | Must be configurable |
| Currency | ❌ Tied to locale | Must be independent |
| Timezone | ❌ Not configurable | Must be independent |
| Date format | ❌ Tied to locale | Must be configurable |
| Number format | ❌ Tied to locale | Must be configurable |

---

##### 8. Translation Governance Gaps

| Requirement | Current | Gap |
|-------------|---------|-----|
| Source of truth: en | ✅ | — |
| Missing key fallback to en | ✅ | — |
| Missing key logging | ❌ | Add warning log |
| Versioning per bundle | ❌ | Add timestamp version |
| Automated key extraction | ✅ (tools exist) | — |
| CI check: fail on missing keys | ✅ (ci-i18n-check.php) | — |

---

##### 9. Implementation Plan

See `docs/i18n-LANGUAGE_SELECTOR_IMPLEMENTATION.md` for the complete to-do list.

###### Priority Order

1. **Phase 1: Data Model** — Enhance LOCALES constant, add missing fields
2. **Phase 2: API Endpoints** — Create `/locales`, `/me/locale`, `/bundles/{locale}`
3. **Phase 3: Component Rewrite** — Rewrite `language_selector.php` per spec
4. **Phase 4: JS Class** — Implement `LanguageLocaleSelector` class
5. **Phase 5: Persistence** — Profile → localStorage → session cascade
6. **Phase 6: RTL** — Full RTL support checklist
7. **Phase 7: Accessibility** — WCAG 2.2 compliance
8. **Phase 8: Separation** — Independent currency/timezone/date settings
9. **Phase 9: Testing** — Cross-locale regression tests
