/**
 * TTSC Events Bridge — Centralized event delegation
 *
 * Eliminates inline event handlers (onclick, onchange, etc.) for CSP compliance.
 * Uses DOCUMENT-LEVEL delegation so handlers also fire for elements injected
 * after page load (e.g. list rows rendered from API responses via innerHTML).
 *
 * Usage:
 *   <button data-evt="click" data-fn="fnName" data-args='["arg1"]'>Click</button>
 *
 * Placeholders:
 *   :el   → resolved to the element (with data-evt) at event time
 *   :val  → resolved to the element value at event time
 *   :evt  → resolved to the native event object at event time
 *
 * Non-bubbling events (blur/focus) are mapped to their bubbling twins
 * (focusout/focusin) so delegation still catches them.
 */
(function () {
    'use strict';

    var PREFIX = 'data-';

    // Semantic data-evt name → bubbling DOM event to listen for.
    // Only the non-bubbling events need a mapping; all others match themselves.
    var EVENT_MAP = {
        'blur': 'focusout',
        'focus': 'focusin'
    };

    // Bubbling DOM events we delegate for.
    var ALL_EVENTS = ['click', 'dblclick', 'change', 'input', 'keyup', 'keydown', 'keypress', 'submit', 'focusout', 'focusin', 'mouseover', 'mouseout'];

    // Reverse lookup: DOM event type → data-evt attribute value to match.
    // Build from EVENT_MAP keys first (focusout → 'blur', focusin → 'focus'),
    // then self-map every remaining DOM event (click → 'click', etc.).
    var DOM_TO_ATTR = {};
    Object.keys(EVENT_MAP).forEach(function (semantic) {
        DOM_TO_ATTR[EVENT_MAP[semantic]] = semantic;
    });
    ALL_EVENTS.forEach(function (t) {
        if (!DOM_TO_ATTR[t]) DOM_TO_ATTR[t] = t;
    });

    function parseArgs(raw, el, e) {
        if (!raw) return [];
        var arr;
        try {
            arr = JSON.parse(raw);
        } catch (err) {
            // Tolerate single-quoted arrays like ['abc-123'] (produced by JS
            // template strings) by normalising quotes before retrying.
            try {
                arr = JSON.parse(raw.replace(/'/g, '"'));
            } catch (err2) {
                arr = [raw];
            }
        }
        return arr.map(function (a) {
            if (a === ':el') return el;
            if (a === ':val') return el.value;
            if (a === ':evt') return e;
            return a;
        });
    }

    function resolveFn(name) {
        var parts = name.split('.');
        var ctx = window;
        for (var i = 0; i < parts.length; i++) {
            if (ctx == null || ctx[parts[i]] === undefined) return null;
            ctx = ctx[parts[i]];
        }
        return typeof ctx === 'function' ? ctx : null;
    }

    function handle(e) {
        var attr = DOM_TO_ATTR[e.type];
        if (!attr) return;
        var target = e.target;
        if (!target || typeof target.closest !== 'function') return;
        var el = target.closest('[' + PREFIX + 'evt="' + attr + '"]');
        if (!el) return;
        var fnName = el.getAttribute(PREFIX + 'fn');
        if (!fnName) return;
        var argsRaw = el.getAttribute(PREFIX + 'args');
        var fn = resolveFn(fnName);
        if (!fn) return;
        var args = parseArgs(argsRaw, el, e);
        fn.apply(el, args);
    }

    ALL_EVENTS.forEach(function (t) {
        document.addEventListener(t, handle);
    });
})();
