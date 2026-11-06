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
import { $all } from "./util.js";

export function initMenus() {
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
