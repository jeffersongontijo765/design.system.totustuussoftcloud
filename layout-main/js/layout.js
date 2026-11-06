/*
 * layout.js — comportamento do chassi (header, rail, sub-sidebar, container, footer).
 *
 * Carregue no fim do <body> com `defer` (ou como módulo). Sem dependências e sem handlers
 * inline (ADR-07 / ACH-01): todo evento é ligado aqui por addEventListener.
 *
 * Módulos (cada um é uma função init* independente):
 *   initDrawers()       gavetas do rail e do sub-sidebar abaixo de 1100px
 *   initRailPin()       fixar o rail expandido no desktop
 *   initPortalGroups()  grupos <details> do rail lembram aberto/fechado
 *   initSubSidebar()    recolher/expandir o sub-sidebar no desktop
 *   initAccordions()    seções do sub-sidebar (botão .sb-section-btn)
 *   initFilter()        filtro do sub-sidebar e atalho "/"
 *   initSearch()        busca global, atalho Ctrl+K / ⌘K e busca no celular
 *   initMenus()         menus suspensos do header (organização, unidade, período, usuário…)
 *   initTheme()         tema claro/escuro (data-theme no <html>)
 *
 * Preferências ficam em localStorage com try/catch: em janela privada ou com armazenamento
 * bloqueado o layout continua funcionando, só não lembra a escolha.
 */
(function () {
  'use strict';

  var MOBILE = window.matchMedia('(max-width: 1099px)');
  var KEYS = {
    railPinned: 'ttsc.layout.railPinned',
    subCollapsed: 'ttsc.layout.subSidebarCollapsed',
    portalGroups: 'ttsc.layout.portalGroups',
    theme: 'ttsc.layout.theme'
  };

  /* ---------- utilitários ---------- */

  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* sem armazenamento */ } }
  };

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function isTypingTarget(el) {
    return el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName));
  }

  /* ---------- 1. Gavetas (abaixo de 1100px) ---------- */

  function initDrawers() {
    var backdrop = $('#navigation-backdrop');
    var toggles = $all('[data-drawer-toggle]');      // #btn-mobile e #btn-sub-sidebar
    var openDrawer = null;
    var lastTrigger = null;

    function panelOf(btn) { return document.getElementById(btn.getAttribute('aria-controls')); }

    // No celular, gaveta fechada fica fora da ordem do Tab e do leitor de tela (inert).
    function syncInert() {
      toggles.forEach(function (btn) {
        var panel = panelOf(btn);
        if (!panel) return;
        var hidden = MOBILE.matches && !panel.classList.contains('is-mobile-open');
        if (hidden) panel.setAttribute('inert', ''); else panel.removeAttribute('inert');
      });
    }

    function close(returnFocus) {
      if (!openDrawer) return;
      openDrawer.classList.remove('is-mobile-open');
      toggles.forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
      backdrop.hidden = true;
      openDrawer = null;
      syncInert();
      if (returnFocus && lastTrigger) lastTrigger.focus();
    }

    function open(btn) {
      var panel = panelOf(btn);
      if (openDrawer && openDrawer !== panel) close(false);
      panel.classList.add('is-mobile-open');
      btn.setAttribute('aria-expanded', 'true');
      backdrop.hidden = false;
      openDrawer = panel;
      lastTrigger = btn;
      syncInert();
      // Foca o filtro se houver; senão o primeiro link ou botão da gaveta.
      var first = panel.querySelector('input[type="search"]') || panel.querySelector('a[href], button:not([disabled])');
      if (first) first.focus();
    }

    toggles.forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (openDrawer === panelOf(btn)) close(true); else open(btn);
      });
    });

    backdrop.addEventListener('click', function () { close(true); });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && openDrawer) { close(true); }
    });

    // Ao clicar num link dentro da gaveta, ela fecha (a navegação segue normalmente).
    toggles.forEach(function (btn) {
      var panel = panelOf(btn);
      if (!panel) return;
      panel.addEventListener('click', function (e) {
        if (MOBILE.matches && e.target.closest('a[href]')) close(false);
      });
    });

    // Voltando para o desktop, nada fica preso aberto.
    MOBILE.addEventListener('change', function () { close(false); syncInert(); });
    syncInert();
  }

  /* ---------- 2. Fixar o rail expandido (desktop) ---------- */

  function initRailPin() {
    var wrapper = $('#primary-rail-wrapper');
    var btn = $('#btn-rail-pin');
    if (!wrapper || !btn) return;

    function apply(pinned) {
      wrapper.classList.toggle('is-expanded', pinned);
      btn.setAttribute('aria-pressed', String(pinned));
      btn.setAttribute('aria-label', pinned ? 'Recolher menu lateral' : 'Fixar menu lateral expandido');
    }

    apply(store.get(KEYS.railPinned) === '1');
    btn.addEventListener('click', function () {
      var pinned = !wrapper.classList.contains('is-expanded');
      apply(pinned);
      store.set(KEYS.railPinned, pinned ? '1' : '0');
    });
  }

  /* ---------- 3. Grupos do rail (<details>) lembram estado ---------- */

  function initPortalGroups() {
    var saved = {};
    try { saved = JSON.parse(store.get(KEYS.portalGroups) || '{}') || {}; } catch (e) { saved = {}; }

    $all('details.portal-rail-group[data-group]').forEach(function (d) {
      var id = d.getAttribute('data-group');
      if (Object.prototype.hasOwnProperty.call(saved, id)) d.open = !!saved[id];
      // O grupo da página atual sempre abre.
      if (d.querySelector('.is-active')) d.open = true;
      d.addEventListener('toggle', function () {
        saved[id] = d.open;
        store.set(KEYS.portalGroups, JSON.stringify(saved));
      });
    });
  }

  /* ---------- 4. Recolher / expandir o sub-sidebar (desktop) ---------- */

  function initSubSidebar() {
    var panel = $('#sub-sidebar');
    var collapseBtn = $('#subsidebar-collapse-btn');
    var expandBtn = $('#sub-sidebar-expand-btn');
    if (!panel || !collapseBtn || !expandBtn) return;

    function apply(collapsed, moveFocus) {
      panel.classList.toggle('collapsed', collapsed);
      expandBtn.hidden = !collapsed;
      collapseBtn.setAttribute('aria-expanded', String(!collapsed));
      expandBtn.setAttribute('aria-expanded', String(!collapsed));
      if (moveFocus) (collapsed ? expandBtn : collapseBtn).focus();
    }

    apply(store.get(KEYS.subCollapsed) === '1', false);

    collapseBtn.addEventListener('click', function () {
      if (MOBILE.matches) {                       // no celular o botão fecha a gaveta
        var toggle = $('#btn-sub-sidebar');
        if (toggle) toggle.click();
        return;
      }
      apply(true, true);
      store.set(KEYS.subCollapsed, '1');
    });

    expandBtn.addEventListener('click', function () {
      apply(false, true);
      store.set(KEYS.subCollapsed, '0');
    });

    // No celular o botão de reabrir não faz sentido (a gaveta tem o próprio botão).
    function syncMobile() { if (MOBILE.matches) expandBtn.hidden = true; else expandBtn.hidden = !panel.classList.contains('collapsed'); }
    MOBILE.addEventListener('change', syncMobile);
    syncMobile();
  }

  /* ---------- 5. Seções sanfona do sub-sidebar ---------- */

  function setSection(btn, expanded) {
    var content = document.getElementById(btn.getAttribute('aria-controls'));
    btn.setAttribute('aria-expanded', String(expanded));
    if (content) {
      content.classList.toggle('is-open', expanded);
      content.classList.toggle('is-closed', !expanded);
    }
  }

  function initAccordions() {
    $all('.sb-section-btn[aria-controls]').forEach(function (btn) {
      setSection(btn, btn.getAttribute('aria-expanded') !== 'false');
      btn.addEventListener('click', function () {
        setSection(btn, btn.getAttribute('aria-expanded') !== 'true');
      });
    });
  }

  /* ---------- 6. Filtro do sub-sidebar e atalho "/" ---------- */

  function normalize(s) {
    return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  }

  function initFilter() {
    var input = $('#subsidebar-filter');
    var empty = $('#subsidebar-empty');
    if (!input) return;

    var groups = $all('#sub-sidebar .subnav-group');
    var initial = groups.map(function (g) {          // estado das seções antes de filtrar
      var b = $('.sb-section-btn', g);
      return b ? b.getAttribute('aria-expanded') === 'true' : true;
    });

    input.addEventListener('input', function () {
      var q = normalize(input.value.trim());
      var anyVisible = false;

      groups.forEach(function (g, i) {
        var links = $all('.subnav-link', g);
        var visible = 0;
        links.forEach(function (a) {
          var match = !q || normalize(a.textContent).indexOf(q) !== -1;
          a.parentElement.hidden = !match;
          if (match) visible++;
        });
        g.hidden = visible === 0;
        var btn = $('.sb-section-btn', g);
        if (btn) setSection(btn, q ? visible > 0 : initial[i]);   // com filtro, abre quem tem resultado
        if (visible) anyVisible = true;
      });

      if (empty) empty.hidden = anyVisible;
    });

    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && input.value) {
        e.stopPropagation();                          // Esc limpa o filtro antes de fechar a gaveta
        input.value = '';
        input.dispatchEvent(new Event('input'));
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey || isTypingTarget(document.activeElement)) return;
      var panel = $('#sub-sidebar');
      if (MOBILE.matches && !panel.classList.contains('is-mobile-open')) return;
      if (panel.classList.contains('collapsed') && !MOBILE.matches) return;
      e.preventDefault();
      input.focus();
    });
  }

  /* ---------- 7. Busca global (Ctrl+K / ⌘K) ---------- */

  function initSearch() {
    var header = $('.app-header');
    var input = $('#global-search');
    var smBtn = $('#btn-search-sm');
    if (!input) return;

    function openSm() {
      header.classList.add('is-search-open');
      if (smBtn) smBtn.setAttribute('aria-expanded', 'true');
      input.focus();
    }

    function closeSm() {
      if (!header.classList.contains('is-search-open')) return;
      header.classList.remove('is-search-open');
      if (smBtn) { smBtn.setAttribute('aria-expanded', 'false'); smBtn.focus(); }
    }

    if (smBtn) smBtn.addEventListener('click', openSm);

    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { input.blur(); closeSm(); }
    });

    input.addEventListener('blur', function () {
      // Fecha a busca do celular quando o foco sai dela (sem roubar o foco de volta).
      setTimeout(function () {
        if (document.activeElement !== input) header.classList.remove('is-search-open');
        if (smBtn) smBtn.setAttribute('aria-expanded', String(header.classList.contains('is-search-open')));
      }, 0);
    });

    document.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) {
        e.preventDefault();
        if (smBtn && getComputedStyle(smBtn).display !== 'none') openSm(); else input.focus();
      }
    });
  }

  /* ---------- 8. Menus suspensos ---------- */

  function initMenus() {
    var triggers = $all('[data-menu]');               // botão com aria-controls apontando para o .menu
    var current = null;

    function menuOf(btn) { return document.getElementById(btn.getAttribute('aria-controls')); }
    function items(menu) { return $all('.menu__item', menu); }

    function close(focusTrigger) {
      if (!current) return;
      menuOf(current).hidden = true;
      current.setAttribute('aria-expanded', 'false');
      if (focusTrigger) current.focus();
      current = null;
    }

    function open(btn, focusFirst) {
      close(false);
      var menu = menuOf(btn);
      menu.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      current = btn;
      if (focusFirst) { var list = items(menu); if (list[0]) list[0].focus(); }
    }

    triggers.forEach(function (btn) {
      btn.setAttribute('aria-haspopup', 'true');
      btn.setAttribute('aria-expanded', 'false');

      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        if (current === btn) close(false); else open(btn, e.detail === 0);   // teclado: foca o 1º item
      });

      btn.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowDown') { e.preventDefault(); open(btn, true); }
      });

      var menu = menuOf(btn);
      menu.addEventListener('keydown', function (e) {
        var list = items(menu);
        var i = list.indexOf(document.activeElement);
        if (e.key === 'ArrowDown') { e.preventDefault(); list[(i + 1) % list.length].focus(); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); list[(i - 1 + list.length) % list.length].focus(); }
        else if (e.key === 'Home') { e.preventDefault(); list[0].focus(); }
        else if (e.key === 'End') { e.preventDefault(); list[list.length - 1].focus(); }
        else if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); close(true); }
        else if (e.key === 'Tab') { close(false); }
      });

      // Itens de escolha (organização, unidade, período): marca o escolhido e mostra no botão.
      menu.addEventListener('click', function (e) {
        var item = e.target.closest('.menu__item[role="menuitemradio"]');
        if (!item) return;
        $all('.menu__item[role="menuitemradio"]', menu).forEach(function (it) {
          it.setAttribute('aria-checked', String(it === item));
        });
        var label = btn.querySelector('[data-menu-value]');
        if (label) label.textContent = item.getAttribute('data-value') || item.textContent.trim();
        close(true);
        document.dispatchEvent(new CustomEvent('ttsc:context-change', {
          detail: { context: btn.id, value: item.getAttribute('data-value') }
        }));
      });
    });

    document.addEventListener('click', function (e) {
      if (current && !menuOf(current).contains(e.target)) close(false);
    });
  }

  /* ---------- 9. Tema claro/escuro ---------- */

  function initTheme() {
    var btn = $('#btn-theme');
    var root = document.documentElement;
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

    function current() { return root.getAttribute('data-theme') || (prefersDark.matches ? 'dark' : 'light'); }

    function apply(theme) {
      root.setAttribute('data-theme', theme);
      if (btn) {
        btn.setAttribute('aria-pressed', String(theme === 'dark'));
        btn.setAttribute('aria-label', theme === 'dark' ? 'Usar tema claro' : 'Usar tema escuro');
        var use = btn.querySelector('use');
        if (use) use.setAttribute('href', theme === 'dark' ? '#i-sun' : '#i-moon');
      }
    }

    apply(store.get(KEYS.theme) || current());

    if (btn) btn.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      apply(next);
      store.set(KEYS.theme, next);
    });
  }

  /* ---------- início ---------- */

  function init() {
    initTheme();
    initDrawers();
    initRailPin();
    initPortalGroups();
    initSubSidebar();
    initAccordions();
    initFilter();
    initSearch();
    initMenus();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
