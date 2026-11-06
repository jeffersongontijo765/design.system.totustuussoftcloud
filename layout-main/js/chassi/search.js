// search.js — busca global do header.
//
// Ctrl+K ou ⌘K foca #global-search. Abaixo de 600px a busca vira o botão #btn-search-sm;
// ao tocar, o campo cobre o header (.is-search-open) e fecha com Esc ou ao perder o foco.
import { $ } from "./util.js";

export function initSearch() {
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
