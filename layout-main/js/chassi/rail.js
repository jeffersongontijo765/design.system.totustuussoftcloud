// rail.js — rail principal (60px → 288px).
//
// Expande sozinho no hover e no foco (CSS do chassi no bundle: .sb-app #primary-rail…).
// .is-expanded no wrapper abre os rótulos de vez; vale em dois casos:
//   - desktop: o botão #btn-rail-pin fixou o rail (preferência salva);
//   - celular: a gaveta do rail está aberta (evento "ttsc:drawer-change" do drawers.js).
// Os grupos <details data-group> lembram se estavam abertos; o grupo que contém a
// página atual (.is-active) sempre abre.
import { MOBILE, $, $all, store, KEYS } from "./util.js";

export function initRailPin() {
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

export function initPortalGroups() {
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
