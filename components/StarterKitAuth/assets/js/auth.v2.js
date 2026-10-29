/**
 * TTSC - Auth JavaScript
 * Authentication functions: login, validation, toast, etc
 */

(function () {
    'use strict';

    // Helpers that build DOM safely (CSP `require-trusted-types-for 'script'` safe)
    function setButtonState(btn, label, iconClass, loading) {
        if (!btn) return null;
        btn.replaceChildren();
        if (iconClass) {
            var ico = document.createElement('i');
            ico.className = iconClass;
            btn.appendChild(ico);
        }
        if (label) {
            btn.appendChild(document.createTextNode(label));
        }
        btn.disabled = !!loading;
        return btn;
    }

    function setButtonLoading(btn, label, iconClass) {
        if (!btn) return null;
        return setButtonState(btn, label || (window.__ ? window.__('please_wait') : 'Aguarde...'), iconClass || 'fa-light fa-spinner fa-spin mr-2', true);
    }

    function restoreButton(btn, original) {
        if (!btn) return;
        btn.replaceChildren();
        if (original) {
            // We have to parse original markup; safer: keep simple text fallback
            // or use a per-button label. Caller may have stored a "text" snapshot.
            if (typeof original === 'string') {
                btn.appendChild(document.createTextNode(original));
            } else if (original.iconClass && original.label) {
                var ico = document.createElement('i');
                ico.className = original.iconClass;
                btn.appendChild(ico);
                btn.appendChild(document.createTextNode(original.label));
            }
        }
        btn.disabled = false;
    }

    window.setButtonState = setButtonState;
    window.ttscAuthSetButton = setButtonState;
    window.ttscAuthButtonLoading = setButtonLoading;
    window.ttscAuthRestoreButton = restoreButton;
})();

/**
 * Initialize login form. The form is the public registration gate; the
 * actual submit handler is bound in `views/auth/pages/login.php` after
 * install status check. This stub makes the DOMContentLoaded call safe
 * and is a no-op if the form is not present.
 */
function initLoginForm() {
    var loginForm = document.getElementById('loginForm');
    var submitBtn = document.getElementById('submitBtn');
    if (!loginForm || !submitBtn) return;

    function restoreBtn() {
        submitBtn.replaceChildren();
        var ico = document.createElement('i');
        ico.className = 'fa-light fa-sign-in-alt';
        submitBtn.appendChild(ico);
        submitBtn.appendChild(document.createTextNode(' Log in'));
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
    }

    function setLoading() {
        submitBtn.replaceChildren();
        var spn = document.createElement('i');
        spn.className = 'fa-light fa-spinner fa-spin';
        submitBtn.appendChild(spn);
        submitBtn.appendChild(document.createTextNode(' Logging in...'));
        submitBtn.disabled = true;
        submitBtn.style.opacity = '0.7';
    }

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();

        if (typeof window.validateLoginForm === 'function' && !window.validateLoginForm()) {
            return;
        }

        setLoading();

        var basePath = document.querySelector('base')?.getAttribute('href') || '';
        var formData = new FormData(loginForm);

        fetch(basePath + 'login', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            }
        })
        .then(function(res) {
            if (!res.ok) {
                return res.json().then(function(errData) {
                    var err = new Error('HTTP ' + res.status);
                    err.status = res.status;
                    err.code = errData.code || '';
                    err.messageText = errData.error || errData.message || '';
                    throw err;
                }).catch(function(thrown) {
                    if (thrown instanceof Error) throw thrown;
                    var err = new Error('HTTP ' + res.status);
                    err.status = res.status;
                    err.code = '';
                    err.messageText = '';
                    throw err;
                });
            }
            return res.json();
        })
        .then(function(data) {
            if (data.mfa_required) {
                var mfaUser = document.getElementById('mfaUserId');
                if (mfaUser) mfaUser.value = data.user_id || '';
                
                document.getElementById('loginForm').classList.add('auth-hidden');
                
                var socialDiv = document.getElementById('socialDivider');
                if (socialDiv) socialDiv.classList.add('auth-hidden');
                
                var socialBtns = document.getElementById('socialButtons');
                if (socialBtns) socialBtns.classList.add('auth-hidden');
                
                var passkeyBtn = document.getElementById('passkeyBtn');
                if (passkeyBtn) passkeyBtn.classList.add('auth-hidden');
                
                var mfaForm = document.getElementById('mfaForm');
                if (mfaForm) mfaForm.classList.remove('auth-hidden');
                
                if (typeof showToast === 'function') showToast((window.__ ? window.__('mfa_required') : 'Verificação adicional necessária'), 'info');
                restoreBtn();
            } else if (data.success) {
                var redirectUrl = data.redirect || (basePath + 'admin');
                if (typeof showToast === 'function') showToast((window.__ ? window.__('login_successful') : 'Login realizado com sucesso!'), 'success');
                // Redirect immediately for reliability
                setTimeout(function() {
                    try {
                        window.location.href = redirectUrl;
                    } catch(e) {
                        window.location.replace(redirectUrl);
                    }
                }, 300);
            } else {
                restoreBtn();
                if (typeof window.showToast === 'function') {
                    window.showToast(data.message || (window.__ ? window.__('auth_error_invalid_credentials') : 'Credenciais inválidas'), 'error');
                }
            }
        })
        .catch(function(err) {
            restoreBtn();
            if (err.status === 403) {
                if (typeof showToast === 'function') showToast((window.__ ? window.__('session_expired_reload') : 'Sessão expirada. Recarregando a página...'), 'warning');
                setTimeout(function() {
                    window.location.reload();
                }, 2000);
            } else if (err.status === 429) {
                if (typeof showToast === 'function') showToast((window.__ ? window.__('auth_error_rate_limit') : 'Muitas solicitações. Aguarde um momento.'), 'warning');
            } else {
                if (typeof showToast === 'function') showToast((window.__ ? window.__('connection_error') : 'Erro de conexão. Tente novamente.'), 'error');
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    
    // Check if system is installed
    checkInstalledStatus();
    
    // Tab switching
    initTabSwitching();
    
    // CPF Mask
    initCpfMask();
    
    // Toggle Password
    initPasswordToggle();
    
    // Form Submit
    initLoginForm();
    
    // Logout
    initLogoutForm();
    
    // Check for authentication redirect message
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('reason') === 'unauthenticated') {
        showToast(window.__ ? window.__('js_session_expired') : 'Sua sessão expirou ou você precisa fazer login para acessar.', 'error');
    } else if (urlParams.get('reason') === 'forbidden') {
        showToast(window.__ ? window.__('js_access_restricted') : 'Acesso restrito a administradores.', 'error');
    }
});


/**
 * Check if system is already installed
 */
async function checkInstalledStatus() {
    try {
        const basePath = document.querySelector('base')?.getAttribute('href') || '';
        const response = await fetch(basePath + 'api/v1/installed', {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await response.json();
        if (data.installed) {
            const link = document.getElementById('installLink');
            if (link) link.classList.add('hidden');
        }
    } catch (e) {
        console.log('Não foi possível verificar o status da instalação');
    }
}

/**
 * Initialize tab switching
 */
function initTabSwitching() {
    const tabBtns = document.querySelectorAll('.auth-tab');
    if (!tabBtns.length) return;
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update tabs
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Show content
            document.querySelectorAll('.auth-tab-content').forEach(c => {
                c.classList.add('auth-hidden');
                c.classList.remove('active');
            });
            const tabId = btn.dataset.tab;
            const content = document.getElementById('tab-' + tabId);
            if (content) {
                content.classList.remove('auth-hidden');
                content.classList.add('active');
            }
        });
    });
}

/**
 * Initialize CPF mask
 */
function initCpfMask() {
    const cpfField = document.getElementById('cpf');
    if (!cpfField) return;
    
    cpfField.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 11) value = value.slice(0, 11);
        
        if (value.length > 9) {
            value = value.replace(/^(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
        } else if (value.length > 6) {
            value = value.replace(/^(\d{3})(\d{3})(\d{3})/, '$1.$2.$3');
        } else if (value.length > 3) {
            value = value.replace(/^(\d{3})(\d{3})/, '$1.$2');
        }
        e.target.value = value;
    });
}

/**
 * Initialize password toggle
 */
function initPasswordToggle() {
    const toggleBtns = document.querySelectorAll('.auth-toggle-vis');
    
    toggleBtns.forEach(btn => {
        // Remove existing onclick to prevent double firing if present
        btn.removeAttribute('onclick');
        
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const wrap = btn.closest('.auth-input-wrap');
            if (!wrap) return;
            
            const passwordField = wrap.querySelector('input');
            const icon = btn.querySelector('i');
            
            if (passwordField && passwordField.type === 'password') {
                passwordField.type = 'text';
                icon?.classList.replace('fa-eye', 'fa-eye-slash');
            } else if (passwordField) {
                passwordField.type = 'password';
                icon?.classList.replace('fa-eye-slash', 'fa-eye');
            }
        });
    });
}

/**
 * Show field error
 */
function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    if (field) field.classList.add('error');
    showToast(message, 'error');
}

/**
 * Clear field error
 */
function clearFieldError(fieldId) {
    const field = document.getElementById(fieldId);
    if (field) field.classList.remove('error');
}

/**
 * Validate login form
 */
function validateLoginForm() {
    // Handle both tabbed (login.php) and single input (login-teacher.php, etc) cases
    let emailField = document.getElementById('username') || document.getElementById('email') || document.getElementById('cpf');
    let activeTabId = 'username';
    
    const activeTabBtn = document.querySelector('.auth-tab.active');
    if (activeTabBtn) {
        activeTabId = activeTabBtn.dataset.tab;
        emailField = document.getElementById(activeTabId);
    }
    
    const passwordField = document.getElementById('password');
    
    clearFieldError('email');
    clearFieldError('cpf');
    clearFieldError('username');
    clearFieldError('password');
    
    if (!emailField || !emailField.value.trim()) {
        showFieldError(emailField ? emailField.id : activeTabId, window.__ ? window.__('fill_login_field') : 'Preencha o campo de login');
        return false;
    }

    if (activeTabId === 'email' && emailField) {
        const email = emailField.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showFieldError('email', window.__ ? window.__('enter_valid_email') : 'Informe um e-mail válido');
            return false;
        }
    } else if (activeTabId === 'cpf' && emailField) {
        const cpf = emailField.value.replace(/\D/g, '');
        if (cpf.length !== 11) {
            showFieldError('cpf', window.__ ? window.__('cpf_must_11_digits') : 'O CPF deve ter 11 dígitos');
            return false;
        }
    }

    if (!passwordField || !passwordField.value) {
        showFieldError('password', window.__ ? window.__('fill_password') : 'Preencha a senha');
        return false;
    }

    if (passwordField.value.length < 6) {
        showFieldError('password', window.__ ? window.__('password_min_6_chars') : 'A senha deve ter no mínimo 6 caracteres');
        return false;
    }
    
    return true;
}

/**
 * Initialize MFA form
 */
function initMfaForm() {
    const mfaForm = document.getElementById('mfaForm');
    if (!mfaForm) return;
    
    mfaForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const mfaCodeInput = document.getElementById('mfaCode');
        const mfaUserIdInput = document.getElementById('mfaUserId');
        
        if (!mfaCodeInput?.value) {
            showToast(window.__ ? window.__('enter_mfa_code') : 'Informe o código MFA', 'error');
            return;
        }

        const btn = mfaForm.querySelector('button[type="submit"]');
        if (btn) {
            ttscAuthButtonLoading(btn, window.__ ? window.__('verifying') : 'Verifying...', 'fa-light fa-spinner fa-spin mr-2');
            btn.classList.add('opacity-75');
        }
        
        try {
            const basePath = document.querySelector('base')?.getAttribute('href') || '';
            const formData = new FormData(mfaForm);
            
            // Add required values if not in form
            if (!formData.has('mfa_type')) formData.append('mfa_type', 'totp');
            
            const response = await fetch(basePath + 'api/v1/auth/mfa-verify', {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            
            const data = await response.json();
            
            if (data.success) {
                // SEC-010: store only non-sensitive user data (name only).
                // Never store tokens, emails, or IDs in localStorage (accessible via XSS).
                if (data.data && data.data.tokens && data.data.tokens.user) {
                    var safeUser = { name: data.data.tokens.user.name || '' };
                    localStorage.setItem('user_data', JSON.stringify(safeUser));
                }
                
                showToast(window.__ ? window.__('mfa_verified') : 'MFA verificado com sucesso!', 'success');
                var mfaRedirectUrl = data.redirect || (basePath + 'admin');
                setTimeout(function() {
                    try {
                        window.location.href = mfaRedirectUrl;
                    } catch(e) {
                        window.location.replace(mfaRedirectUrl);
                    }
                }, 300);
            } else {
                showToast(data.message || (window.__ ? window.__('invalid_mfa_code') : 'Código MFA inválido'), 'error');
            }
        } catch (error) {
            console.error('Error in MFA request:', error);
            showToast(window.__ ? window.__('connection_error') : 'Erro de conexão. Tente novamente.', 'error');
        } finally {
            if (btn) {
                ttscAuthSetButton(btn, window.__ ? window.__('log_in') : 'Log in', 'fa-light fa-arrow-right-to-bracket mr-2', false);
                btn.classList.remove('opacity-75');
            }
        }
    });
}

/**
 * Initialize logout form
 */
function initLogoutForm() {
    const logoutForm = document.getElementById('logoutForm');
    if (!logoutForm) return;
    
    logoutForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        try {
            const basePath = document.querySelector('base')?.getAttribute('href') || '';
            const formData = new FormData(logoutForm);
            await fetch(basePath + 'logout', {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            window.location.href = basePath + 'login';
        } catch (error) {
            window.location.href = basePath + 'login';
        }
    });
}

/**
 * Toast notification - Global function
 */
function showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = 'position: fixed; top: 1rem; right: 1rem; z-index: 9999; display: flex; flex-direction: column; gap: 0.75rem; pointer-events: none;';
        document.body.appendChild(container);
    }
    
    const config = {
        success: { icon: 'fa-circle-check', title: window.__ ? window.__('toast_title_success') : 'Success', color: '#10b981' },
        error: { icon: 'fa-circle-xmark', title: window.__ ? window.__('toast_title_error') : 'Error', color: '#ef4444' },
        warning: { icon: 'fa-triangle-exclamation', title: window.__ ? window.__('toast_title_warning') : 'Warning', color: '#f59e0b' },
        info: { icon: 'fa-circle-info', title: window.__ ? window.__('toast_title_info') : 'Info', color: '#3b82f6' }
    };
    
    const { icon, title, color } = config[type] || config.info;
    
    const toast = document.createElement('div');
    toast.style.cssText = `
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0,0,0,0.05);
        border-left: 4px solid ${color};
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        gap: 16px;
        min-width: 320px;
        transform: translateX(120%);
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        opacity: 0;
    `;

    // Build the toast content via DOM construction (CSP `require-trusted-types-for 'script'` compliant).
    var iconWrap = document.createElement('div');
    iconWrap.style.cssText = 'background: ' + color + '20; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center;';
    var icoEl = document.createElement('i');
    icoEl.className = 'fas ' + icon;
    icoEl.style.cssText = 'color: ' + color + '; font-size: 1.25rem;';
    iconWrap.appendChild(icoEl);

    var body = document.createElement('div');
    body.style.cssText = 'flex: 1;';
    var titleEl = document.createElement('div');
    titleEl.style.cssText = 'font-weight: 700; font-size: 0.9rem; color: #1e293b;';
    titleEl.textContent = String(title == null ? '' : title);
    var msgEl = document.createElement('div');
    msgEl.style.cssText = 'font-size: 0.8rem; color: #64748b; margin-top: 2px;';
    msgEl.textContent = String(message == null ? '' : message);
    body.appendChild(titleEl);
    body.appendChild(msgEl);

    var closeBtn = document.createElement('button');
    closeBtn.className = 'ttsc-toast-close';
    closeBtn.style.cssText = 'color: #94a3b8; cursor: pointer; padding: 4px; border: none; background: none;';
    var closeIco = document.createElement('i');
    closeIco.className = 'fa-light fa-times';
    closeBtn.appendChild(closeIco);

    toast.appendChild(iconWrap);
    toast.appendChild(body);
    toast.appendChild(closeBtn);

    // Attach close handler programmatically (CSP-compliant) — closeBtn is the
    // element we just created and appended, so use it directly.
    closeBtn.addEventListener('click', function () { toast.remove(); });

    container.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
        toast.style.opacity = '1';
    }, 10);
    
    // Auto remove
    setTimeout(() => {
        if (toast.parentElement) {
            toast.style.transform = 'translateX(120%)';
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 500);
        }
    }, 4000);
}

// Make functions globally available
window.showToast = showToast;
window.showFieldError = showFieldError;
window.clearFieldError = clearFieldError;
window.validateLoginForm = validateLoginForm;
