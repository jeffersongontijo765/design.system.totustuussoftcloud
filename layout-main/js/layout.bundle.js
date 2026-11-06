// layout.bundle.js — GERADO por js/build.mjs a partir de js/chassi/*.js. Não edite aqui.
(function () {
"use strict";
// ---- chassi/util.js ----
// util.js — utilitários compartilhados pelos módulos do chassi.

/** Abaixo de 1100px o rail e o sub-sidebar viram gavetas (corte do chassi real). */
const MOBILE = window.matchMedia("(max-width: 1099px)");

/** Chaves das preferências guardadas no navegador. */
const KEYS = {
  railPinned: "ttsc.layout.railPinned",
  subCollapsed: "ttsc.layout.subSidebarCollapsed",
  portalGroups: "ttsc.layout.portalGroups",
  theme: "ttsc.layout.theme",
};

/**
 * localStorage com try/catch: em janela privada ou com armazenamento bloqueado
 * o layout funciona igual, só não lembra a escolha.
 */
const store = {
  get(key) {
    try { return window.localStorage.getItem(key); } catch { return null; }
  },
  set(key, value) {
    try { window.localStorage.setItem(key, value); } catch { /* sem armazenamento */ }
  },
};

const $ = (sel, root = document) => root.querySelector(sel);
const $all = (sel, root = document) => [...root.querySelectorAll(sel)];

/** O foco está num campo de digitação? (atalhos de uma tecla não devem disparar) */
function isTyping(el = document.activeElement) {
  return !!el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName));
}

/** Minúsculas e sem acento, para filtro. */
function normalize(text) {
  return (text || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
}

// ---- chassi/theme.js ----
// theme.js — tema claro/escuro.
//
// O DS lê data-theme no <html> (tokens em [data-theme="light"|"dark"]).
// Na primeira visita segue o sistema operacional; depois, a escolha do botão #btn-theme.

function initTheme() {
  const root = document.documentElement;
  const btn = $("#btn-theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)");

  const apply = (theme) => {
    root.dataset.theme = theme;
    if (!btn) return;
    btn.setAttribute("aria-pressed", String(theme === "dark"));
    btn.setAttribute("aria-label", theme === "dark" ? "Usar tema claro" : "Usar tema escuro");
    btn.querySelector("use")?.setAttribute("href", theme === "dark" ? "#i-sun" : "#i-moon");
  };

  apply(store.get(KEYS.theme) || (prefersDark.matches ? "dark" : "light"));

  btn?.addEventListener("click", () => {
    const next = root.dataset.theme === "dark" ? "light" : "dark";
    apply(next);
    store.set(KEYS.theme, next);
  });
}

// ---- chassi/drawers.js ----
// drawers.js — rail e sub-sidebar como gavetas abaixo de 1100px.
//
// Botões com [data-drawer-toggle][aria-controls] abrem o painel apontado.
// Abrir: .is-mobile-open no painel, aria-expanded="true", fundo visível, foco no filtro
// (ou no primeiro link). Fechar: Esc, clique no fundo, clique num link ou no mesmo botão;
// o foco volta ao botão. Gaveta fechada recebe `inert` (fora do Tab e do leitor de tela).
// Cada abertura ou fechamento dispara "ttsc:drawer-change" { panel, open } no document.

function initDrawers() {
  const backdrop = $("#navigation-backdrop");
  const toggles = $all("[data-drawer-toggle]");
  if (!backdrop || !toggles.length) return;

  const panelOf = (btn) => document.getElementById(btn.getAttribute("aria-controls"));
  let openPanel = null;
  let trigger = null;

  function announce(panel, open) {
    document.dispatchEvent(new CustomEvent("ttsc:drawer-change", { detail: { panel: panel.id, open } }));
  }

  function syncInert() {
    for (const btn of toggles) {
      const panel = panelOf(btn);
      if (!panel) continue;
      const hidden = MOBILE.matches && !panel.classList.contains("is-mobile-open");
      panel.toggleAttribute("inert", hidden);
    }
  }

  function close(returnFocus) {
    if (!openPanel) return;
    const panel = openPanel;
    panel.classList.remove("is-mobile-open");
    toggles.forEach((b) => b.setAttribute("aria-expanded", "false"));
    backdrop.hidden = true;
    openPanel = null;
    syncInert();
    announce(panel, false);
    if (returnFocus && trigger) trigger.focus();
  }

  function open(btn) {
    const panel = panelOf(btn);
    if (!panel) return;
    if (openPanel && openPanel !== panel) close(false);   // uma gaveta por vez
    panel.classList.add("is-mobile-open");
    btn.setAttribute("aria-expanded", "true");
    backdrop.hidden = false;
    openPanel = panel;
    trigger = btn;
    syncInert();
    announce(panel, true);
    const first = panel.querySelector('input[type="search"]') || panel.querySelector("a[href], button:not([disabled])");
    first?.focus();
  }

  for (const btn of toggles) {
    btn.addEventListener("click", () => (openPanel === panelOf(btn) ? close(true) : open(btn)));
    panelOf(btn)?.addEventListener("click", (e) => {
      if (MOBILE.matches && e.target.closest("a[href]")) close(false);
    });
  }

  backdrop.addEventListener("click", () => close(true));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && openPanel) close(true);
  });

  // Voltando para o desktop, nada fica preso aberto.
  MOBILE.addEventListener("change", () => { close(false); syncInert(); });
  syncInert();

  return { close };
}

// ---- chassi/rail.js ----
// rail.js — rail principal (60px → 288px).
//
// Expande sozinho no hover e no foco (CSS do chassi no bundle: .sb-app #primary-rail…).
// .is-expanded no wrapper abre os rótulos de vez; vale em dois casos:
//   - desktop: o botão #btn-rail-pin fixou o rail (preferência salva);
//   - celular: a gaveta do rail está aberta (evento "ttsc:drawer-change" do drawers.js).
// Os grupos <details data-group> lembram se estavam abertos; o grupo que contém a
// página atual (.is-active) sempre abre.

function initRailPin() {
  const wrapper = $("#primary-rail-wrapper");
  const btn = $("#btn-rail-pin");
  if (!wrapper || !btn) return;

  let pinned = store.get(KEYS.railPinned) === "1";

  const sync = () => {
    const drawerOpen = MOBILE.matches && wrapper.classList.contains("is-mobile-open");
    wrapper.classList.toggle("is-expanded", drawerOpen || (pinned && !MOBILE.matches));
    btn.setAttribute("aria-pressed", String(pinned));
    btn.setAttribute("aria-label", pinned ? "Soltar menu lateral" : "Fixar menu lateral expandido");
  };

  btn.addEventListener("click", () => {
    pinned = !pinned;
    store.set(KEYS.railPinned, pinned ? "1" : "0");
    sync();
  });
  document.addEventListener("ttsc:drawer-change", sync);
  MOBILE.addEventListener("change", sync);
  sync();
}

function initPortalGroups() {
  let saved = {};
  try { saved = JSON.parse(store.get(KEYS.portalGroups) || "{}") || {}; } catch { saved = {}; }

  for (const group of $all("details.portal-rail-group[data-group]")) {
    const id = group.dataset.group;
    if (Object.hasOwn(saved, id)) group.open = Boolean(saved[id]);
    if (group.querySelector(".is-active")) group.open = true;
    group.addEventListener("toggle", () => {
      saved[id] = group.open;
      store.set(KEYS.portalGroups, JSON.stringify(saved));
    });
  }
}

// ---- chassi/sub-sidebar.js ----
// sub-sidebar.js — menu do módulo.
//
// initCollapse: #subsidebar-collapse-btn recolhe (classe .collapsed) e
//   #sub-sidebar-expand-btn reabre; o foco acompanha e a escolha fica guardada.
//   No celular o botão de recolher fecha a gaveta.
// initAccordions: .sb-section-btn[aria-controls] abre e fecha a lista da seção.
// initFilter: #subsidebar-filter filtra os links sem considerar acentos; "/" foca o
//   filtro, Esc limpa. Seções sem resultado somem; #subsidebar-empty avisa quando nada sobra.

function setSection(btn, expanded) {
  const content = document.getElementById(btn.getAttribute("aria-controls"));
  btn.setAttribute("aria-expanded", String(expanded));
  content?.classList.toggle("is-open", expanded);
  content?.classList.toggle("is-closed", !expanded);
}

function initCollapse() {
  const panel = $("#sub-sidebar");
  const collapseBtn = $("#subsidebar-collapse-btn");
  const expandBtn = $("#sub-sidebar-expand-btn");
  if (!panel || !collapseBtn || !expandBtn) return;

  const apply = (collapsed, moveFocus) => {
    panel.classList.toggle("collapsed", collapsed);
    expandBtn.hidden = MOBILE.matches || !collapsed;
    collapseBtn.setAttribute("aria-expanded", String(!collapsed));
    expandBtn.setAttribute("aria-expanded", String(!collapsed));
    if (moveFocus) (collapsed ? expandBtn : collapseBtn).focus();
  };

  apply(store.get(KEYS.subCollapsed) === "1", false);

  collapseBtn.addEventListener("click", () => {
    if (MOBILE.matches) { $("#btn-sub-sidebar")?.click(); return; }
    apply(true, true);
    store.set(KEYS.subCollapsed, "1");
  });

  expandBtn.addEventListener("click", () => {
    apply(false, true);
    store.set(KEYS.subCollapsed, "0");
  });

  MOBILE.addEventListener("change", () => apply(panel.classList.contains("collapsed"), false));
}

function initAccordions() {
  for (const btn of $all(".sb-section-btn[aria-controls]")) {
    setSection(btn, btn.getAttribute("aria-expanded") !== "false");
    btn.addEventListener("click", () => setSection(btn, btn.getAttribute("aria-expanded") !== "true"));
  }
}

function initFilter() {
  const input = $("#subsidebar-filter");
  const empty = $("#subsidebar-empty");
  const panel = $("#sub-sidebar");
  if (!input || !panel) return;

  const groups = $all(".subnav-group", panel);
  const initial = groups.map((g) => $(".sb-section-btn", g)?.getAttribute("aria-expanded") !== "false");

  input.addEventListener("input", () => {
    const q = normalize(input.value.trim());
    let any = false;
    groups.forEach((group, i) => {
      let visible = 0;
      for (const link of $all(".subnav-link", group)) {
        const match = !q || normalize(link.textContent).includes(q);
        link.parentElement.hidden = !match;
        if (match) visible++;
      }
      group.hidden = visible === 0;
      const btn = $(".sb-section-btn", group);
      if (btn) setSection(btn, q ? visible > 0 : initial[i]);   // com filtro, abre quem tem resultado
      if (visible) any = true;
    });
    if (empty) empty.hidden = any;
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && input.value) {
      e.stopPropagation();                                      // limpa antes de fechar a gaveta
      input.value = "";
      input.dispatchEvent(new Event("input"));
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key !== "/" || e.ctrlKey || e.metaKey || e.altKey || isTyping()) return;
    const usable = MOBILE.matches ? panel.classList.contains("is-mobile-open") : !panel.classList.contains("collapsed");
    if (!usable) return;
    e.preventDefault();
    input.focus();
  });
}

// ---- chassi/search.js ----
// search.js — busca global do header.
//
// Ctrl+K ou ⌘K foca #global-search. Abaixo de 600px a busca vira o botão #btn-search-sm;
// ao tocar, o campo cobre o header (.is-search-open) e fecha com Esc ou ao perder o foco.

function initSearch() {
  const header = $(".app-header");
  const input = $("#global-search");
  const smBtn = $("#btn-search-sm");
  if (!header || !input) return;

  const smVisible = () => smBtn && getComputedStyle(smBtn).display !== "none";

  const setOpen = (open) => {
    header.classList.toggle("is-search-open", open);
    smBtn?.setAttribute("aria-expanded", String(open));
  };

  smBtn?.addEventListener("click", () => { setOpen(true); input.focus(); });

  input.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    const wasOpen = header.classList.contains("is-search-open");
    input.blur();
    setOpen(false);
    if (wasOpen) smBtn?.focus();
  });

  input.addEventListener("blur", () => {
    setTimeout(() => { if (document.activeElement !== input) setOpen(false); }, 0);
  });

  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      if (smVisible()) setOpen(true);
      input.focus();
    }
  });
}

// ---- chassi/menus.js ----
// menus.js — menus suspensos do header (ttsc-dropdown-menu do DS).
//
// Botão: [data-menu][aria-controls="id-do-menu"]. O menu aparece com a classe .open
// (regra do bundle: .ttsc-dropdown-menu:not(.open){display:none}).
// Teclado: ↓ no botão abre e foca o 1º item; ↑ ↓ Home End navegam; Esc fecha e volta
// o foco; Tab fecha. Clique fora fecha.
//
// Itens de contexto: [role=menuitemradio][data-context][data-value]. Escolher um item
// marca aria-checked em todos os menus com o mesmo data-context (o seletor do desktop e
// o menu de contexto do celular ficam iguais), troca os textos [data-context-value] e
// dispara o evento "ttsc:context-change" { context, value } no document.

function initMenus() {
  const triggers = $all("[data-menu][aria-controls]");
  const menuOf = (btn) => document.getElementById(btn.getAttribute("aria-controls"));
  const itemsOf = (menu) => $all('.ttsc-dropdown-menu-link:not([hidden])', menu);
  let current = null;

  function close(focusTrigger) {
    if (!current) return;
    menuOf(current)?.classList.remove("open");
    current.setAttribute("aria-expanded", "false");
    if (focusTrigger) current.focus();
    current = null;
  }

  function open(btn, focusFirst) {
    close(false);
    menuOf(btn).classList.add("open");
    btn.setAttribute("aria-expanded", "true");
    current = btn;
    if (focusFirst) itemsOf(menuOf(btn))[0]?.focus();
  }

  function choose(item) {
    const { context, value } = item.dataset;
    for (const it of $all(`[role="menuitemradio"][data-context="${context}"]`)) {
      it.setAttribute("aria-checked", String(it.dataset.value === value));
    }
    for (const label of $all(`[data-context-value="${context}"]`)) label.textContent = value;
    document.dispatchEvent(new CustomEvent("ttsc:context-change", { detail: { context, value } }));
  }

  for (const btn of triggers) {
    const menu = menuOf(btn);
    if (!menu) continue;
    btn.setAttribute("aria-haspopup", "menu");
    btn.setAttribute("aria-expanded", "false");

    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      if (current === btn) close(false);
      else open(btn, e.detail === 0);                       // ativado por teclado: foca o 1º item
    });

    btn.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); open(btn, true); }
    });

    menu.addEventListener("keydown", (e) => {
      const list = itemsOf(menu);
      const i = list.indexOf(document.activeElement);
      const go = (n) => { e.preventDefault(); list[(n + list.length) % list.length]?.focus(); };
      if (e.key === "ArrowDown") go(i + 1);
      else if (e.key === "ArrowUp") go(i - 1);
      else if (e.key === "Home") go(0);
      else if (e.key === "End") go(list.length - 1);
      else if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); close(true); }
      else if (e.key === "Tab") close(false);
    });

    menu.addEventListener("click", (e) => {
      const item = e.target.closest('[role="menuitemradio"][data-context]');
      if (!item) return;
      choose(item);
      close(true);
    });
  }

  document.addEventListener("click", (e) => {
    if (current && !menuOf(current).contains(e.target)) close(false);
  });
}

// ---- início (js/layout.js) ----
window.TTSCLayout = { normalize };
  initTheme();
  initDrawers();
  initRailPin();
  initPortalGroups();
  initCollapse();
  initAccordions();
  initFilter();
  initSearch();
  initMenus();
})();
