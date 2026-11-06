// sub-sidebar.js — menu do módulo.
//
// initCollapse: #subsidebar-collapse-btn recolhe (classe .collapsed) e
//   #sub-sidebar-expand-btn reabre; o foco acompanha e a escolha fica guardada.
//   No celular o botão de recolher fecha a gaveta.
// initAccordions: .sb-section-btn[aria-controls] abre e fecha a lista da seção.
// initFilter: #subsidebar-filter filtra os links sem considerar acentos; "/" foca o
//   filtro, Esc limpa. Seções sem resultado somem; #subsidebar-empty avisa quando nada sobra.
import { MOBILE, $, $all, store, KEYS, isTyping, normalize } from "./util.js";

export function setSection(btn, expanded) {
  const content = document.getElementById(btn.getAttribute("aria-controls"));
  btn.setAttribute("aria-expanded", String(expanded));
  content?.classList.toggle("is-open", expanded);
  content?.classList.toggle("is-closed", !expanded);
}

export function initCollapse() {
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

export function initAccordions() {
  for (const btn of $all(".sb-section-btn[aria-controls]")) {
    setSection(btn, btn.getAttribute("aria-expanded") !== "false");
    btn.addEventListener("click", () => setSection(btn, btn.getAttribute("aria-expanded") !== "true"));
  }
}

export function initFilter() {
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
