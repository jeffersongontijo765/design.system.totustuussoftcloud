// theme.js — tema claro/escuro.
//
// O DS lê data-theme no <html> (tokens em [data-theme="light"|"dark"]).
// Na primeira visita segue o sistema operacional; depois, a escolha do botão #btn-theme.
import { $, store, KEYS } from "./util.js";

export function initTheme() {
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
