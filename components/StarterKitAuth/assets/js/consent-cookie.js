/**
 * TotusTuus SoftCloud - LGPD / Privacy First Cookie Consent Manager
 *
 * Provides persistent, multi-layered consent storage across all portals:
 * - LocalStorage ('ttsc_cookie_consent' & 'ttsc_cookie_consent_data')
 * - Client & Server Cookies ('cookie_consent', 1-year expiration, SameSite=Lax, Secure on HTTPS)
 * - Server-side audit log & user_cookie_consents table sync
 * - Zero-flicker banner suppression when consent was already granted
 * - Safe initialization regardless of script placement or DOM loading state
 */

(function() {
    'use strict';

    var STORAGE_KEY = 'ttsc_cookie_consent';
    var STORAGE_DATA_KEY = 'ttsc_cookie_consent_data';

    var cookieCategories = [];
    var cookiePreferences = {};
    var currentBannerVersionId = null;

    function htmlEscape(str) {
        if (!str) return '';
        var div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function getCookie(name) {
        try {
            var match = document.cookie.match(new RegExp('(^|;\\s*)' + name + '=([^;]+)'));
            return match ? decodeURIComponent(match[2]) : null;
        } catch (e) {
            return null;
        }
    }

    function syncClientCookie(value) {
        try {
            var expires = new Date(Date.now() + 365 * 864e5).toUTCString();
            var isSecure = window.location.protocol === 'https:';
            var cookieStr = 'cookie_consent=' + encodeURIComponent(value) +
                '; path=/; expires=' + expires +
                '; SameSite=Lax' +
                (isSecure ? '; Secure' : '');
            document.cookie = cookieStr;
        } catch (e) {}
    }

    function getStoredConsent() {
        try {
            var local = localStorage.getItem(STORAGE_KEY);
            if (local && local !== 'null' && local !== 'undefined' && local !== '') return local;
        } catch (e) {}

        var cookie = getCookie('cookie_consent');
        if (cookie && cookie !== 'null' && cookie !== 'undefined' && cookie !== '') {
            try { localStorage.setItem(STORAGE_KEY, cookie); } catch (e) {}
            return cookie;
        }

        return null;
    }

    function getStoredConsentData() {
        try {
            var dataStr = localStorage.getItem(STORAGE_DATA_KEY);
            return dataStr ? JSON.parse(dataStr) : null;
        } catch (e) {
            return null;
        }
    }

    function persistConsent(decision, categories) {
        // 1. LocalStorage
        try {
            localStorage.setItem(STORAGE_KEY, decision);
            localStorage.setItem(STORAGE_DATA_KEY, JSON.stringify({
                decision: decision,
                categories: categories || [],
                timestamp: Date.now()
            }));
        } catch (e) {}

        // 2. Client Cookie
        syncClientCookie(decision);

        // 3. Hide UI immediately
        var banner = document.getElementById('cookieConsentBanner');
        if (banner) banner.classList.add('hidden');
        closeCookiePreferences();

        // 4. Dispatch browser event
        try {
            window.dispatchEvent(new CustomEvent('cookie_consent_saved', {
                detail: { decision: decision, categories: categories }
            }));
        } catch (e) {}
    }

    function getCsrfToken() {
        var meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute('content') : '';
    }

    function renderPreferenceList(categories) {
        var prefList = document.getElementById('cookiePreferencesList');
        if (!prefList) return;
        var html = '';
        var savedData = getStoredConsentData();
        var savedCategories = {};

        if (savedData && Array.isArray(savedData.categories)) {
            savedData.categories.forEach(function(c) {
                savedCategories[c.id] = c.granted;
            });
        }

        (categories || []).forEach(function(cat) {
            var isEssential = cat.is_essential === true || cat.is_essential === '1' || cat.is_essential === 1;
            var isChecked = isEssential || (savedCategories[cat.id] !== undefined ? savedCategories[cat.id] : true);

            cookiePreferences[cat.id] = isChecked;

            html += '<div class="cookie-cat-row">';
            html += '<input type="checkbox" class="consent-category-checkbox" data-category-id="' + cat.id + '" ' + (isChecked ? 'checked' : '') + ' ' + (isEssential ? 'disabled' : '') + '>';
            html += '<div class="flex-1 min-w-0">';
            html += '<label class="text-sm font-medium cursor-pointer select-none" style="color:var(--fg,#1c1c1c)">' + htmlEscape(cat.name || '') + '</label>';
            html += '<p class="text-xs mt-0.5" style="color:var(--muted,#6b6b6b);line-height:1.5">' + htmlEscape(cat.description || '') + '</p>';
            html += '</div>';
            if (isEssential) {
                html += '<span class="cookie-badge-essential">Sempre ativo</span>';
            }
            html += '</div>';
        });

        prefList.innerHTML = html;
    }

    function updateCookiePreference(categoryId, granted) {
        cookiePreferences[categoryId] = granted;
    }

    function openCookiePreferences() {
        var banner = document.getElementById('cookieConsentBanner');
        var modal = document.getElementById('cookiePreferencesModal');
        if (banner) banner.classList.add('hidden');
        if (modal) modal.classList.remove('hidden');
    }

    function closeCookiePreferences() {
        var modal = document.getElementById('cookiePreferencesModal');
        if (modal) modal.classList.add('hidden');
    }

    function getCurrentPreferences() {
        var prefs = {};
        var checkboxes = document.querySelectorAll('.consent-category-checkbox');
        checkboxes.forEach(function(cb) {
            prefs[cb.getAttribute('data-category-id')] = cb.checked;
        });
        return prefs;
    }

    async function submitConsent(decision, categories) {
        // Persist immediately on client side (guarantees banner will never reappear even if offline)
        persistConsent(decision, categories);

        if (typeof Toast !== 'undefined' && typeof Toast.show === 'function') {
            Toast.show('Preferências de privacidade salvas com sucesso!', 'success');
        } else if (typeof window.ttscToast === 'function') {
            window.ttscToast('Preferências de privacidade salvas com sucesso!', 'success');
        }

        // Background server sync
        var banner = document.getElementById('cookieConsentBanner');
        var decisionsUrl = (banner ? banner.getAttribute('data-decisions-url') : null) || '/privacy/consent-decisions';

        try {
            var body = { decision: decision, categories: categories || [] };
            if (currentBannerVersionId) {
                body.banner_version_id = currentBannerVersionId;
            }
            await fetch(decisionsUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': getCsrfToken()
                },
                body: JSON.stringify(body)
            });
        } catch (e) {
            // Silently handled: client-side consent is already secure
        }
    }

    function acceptAllCookies() {
        var categories = (cookieCategories || []).map(function(cat) {
            return { id: cat.id, granted: true };
        });
        submitConsent('accepted_all', categories);
    }

    function rejectNonEssential() {
        var categories = (cookieCategories || []).map(function(cat) {
            var isEssential = cat.is_essential === true || cat.is_essential === '1' || cat.is_essential === 1;
            return { id: cat.id, granted: isEssential };
        });
        submitConsent('rejected_non_essential', categories);
    }

    function saveCookiePreferences() {
        var currentPrefs = getCurrentPreferences();
        var categories = (cookieCategories || []).map(function(cat) {
            var isEssential = cat.is_essential === true || cat.is_essential === '1' || cat.is_essential === 1;
            var granted = isEssential ? true : (currentPrefs[cat.id] !== false);
            return { id: cat.id, granted: granted };
        });
        submitConsent('customized', categories);
    }

    // Public API for preference buttons in footers / settings / profile
    window.openCookiePreferences = openCookiePreferences;
    window.closeCookiePreferences = closeCookiePreferences;
    window.resetCookieConsent = function() {
        try {
            localStorage.removeItem(STORAGE_KEY);
            localStorage.removeItem(STORAGE_DATA_KEY);
        } catch (e) {}
        document.cookie = 'cookie_consent=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Lax';
        var banner = document.getElementById('cookieConsentBanner');
        if (banner) banner.classList.remove('hidden');
    };

    async function initConsent() {
        var banner = document.getElementById('cookieConsentBanner');
        if (!banner) return;

        var hasConsent = getStoredConsent();
        if (hasConsent) {
            banner.classList.add('hidden');
            syncClientCookie(hasConsent);
        }

        var configUrl = banner.getAttribute('data-config-url') || '/privacy/consent-config';

        try {
            var r = await fetch(configUrl);
            var data = await r.json();
            if (data && data.success) {
                cookieCategories = data.categories || [];
                renderPreferenceList(data.categories);

                if (data.banner) {
                    currentBannerVersionId = data.banner.id || null;
                    var titleEl = document.getElementById('consentBannerTitle');
                    var textEl = document.getElementById('consentBannerText');
                    var acceptBtn = document.getElementById('consentAcceptAll');
                    var rejectBtn = document.getElementById('consentRejectAll');
                    var customBtn = document.getElementById('consentCustomize');

                    if (titleEl && data.banner.banner_title) titleEl.textContent = data.banner.banner_title;
                    if (textEl && data.banner.banner_text) textEl.textContent = data.banner.banner_text;
                    if (acceptBtn && data.banner.accept_all_label) acceptBtn.textContent = data.banner.accept_all_label;
                    if (rejectBtn && data.banner.reject_all_label) rejectBtn.textContent = data.banner.reject_all_label;
                    if (customBtn && data.banner.customize_label) customBtn.textContent = data.banner.customize_label;
                }

                // If server already has recorded consent for this user/session, adopt it
                if (data.current_consent && data.current_consent.decision) {
                    persistConsent(data.current_consent.decision, data.categories || []);
                    banner.classList.add('hidden');
                    return;
                }

                // If no consent exists anywhere, display banner; otherwise keep hidden
                if (!hasConsent && !data.current_consent) {
                    banner.classList.remove('hidden');
                } else {
                    banner.classList.add('hidden');
                }
            }
        } catch (e) {
            // If offline/error and no consent, show banner as fallback
            if (!hasConsent) {
                banner.classList.remove('hidden');
            }
        }
    }

    // Fast-path check immediately upon script parse
    var immediateConsent = getStoredConsent();
    if (immediateConsent) {
        var existingBanner = document.getElementById('cookieConsentBanner');
        if (existingBanner) existingBanner.classList.add('hidden');
        syncClientCookie(immediateConsent);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initConsent);
    } else {
        initConsent();
    }

    // Delegated click listeners
    document.addEventListener('click', function(e) {
        try {
            if (!e.target || typeof e.target.closest !== 'function') return;
            var target = e.target.closest('[data-consent-action]');
            if (!target) return;

            var action = target.getAttribute('data-consent-action');

            switch (action) {
                case 'accept-all':
                    acceptAllCookies();
                    break;
                case 'reject':
                    rejectNonEssential();
                    break;
                case 'customize':
                    openCookiePreferences();
                    break;
                case 'close-preferences':
                case 'close':
                    closeCookiePreferences();
                    break;
                case 'save-preferences':
                    saveCookiePreferences();
                    break;
            }
        } catch (err) {}
    });

    // Delegated checkbox change listeners
    document.addEventListener('change', function(e) {
        try {
            if (!e.target || typeof e.target.closest !== 'function') return;
            var checkbox = e.target.closest('.consent-category-checkbox');
            if (!checkbox) return;
            var categoryId = checkbox.getAttribute('data-category-id');
            updateCookiePreference(categoryId, checkbox.checked);
        } catch (err) {}
    });
})();
