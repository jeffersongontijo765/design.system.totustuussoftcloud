// drawers.js — rail e sub-sidebar como gavetas abaixo de 1100px.
//
// Botões com [data-drawer-toggle][aria-controls] abrem o painel apontado.
// Abrir: .is-mobile-open no painel, aria-expanded="true", fundo visível, foco no filtro
// (ou no primeiro link). Fechar: Esc, clique no fundo, clique num link ou no mesmo botão;
// o foco volta ao botão. Gaveta fechada recebe `inert` (fora do Tab e do leitor de tela).
// Cada abertura ou fechamento dispara "ttsc:drawer-change" { panel, open } no document.
import { MOBILE, $, $all } from "./util.js";

export function initDrawers() {
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
