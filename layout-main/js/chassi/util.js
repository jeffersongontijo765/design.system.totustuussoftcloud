// util.js — utilitários compartilhados pelos módulos do chassi.

/** Abaixo de 1100px o rail e o sub-sidebar viram gavetas (corte do chassi real). */
export const MOBILE = window.matchMedia("(max-width: 1099px)");

/** Chaves das preferências guardadas no navegador. */
export const KEYS = {
  railPinned: "ttsc.layout.railPinned",
  subCollapsed: "ttsc.layout.subSidebarCollapsed",
  portalGroups: "ttsc.layout.portalGroups",
  theme: "ttsc.layout.theme",
};

/**
 * localStorage com try/catch: em janela privada ou com armazenamento bloqueado
 * o layout funciona igual, só não lembra a escolha.
 */
export const store = {
  get(key) {
    try { return window.localStorage.getItem(key); } catch { return null; }
  },
  set(key, value) {
    try { window.localStorage.setItem(key, value); } catch { /* sem armazenamento */ }
  },
};

export const $ = (sel, root = document) => root.querySelector(sel);
export const $all = (sel, root = document) => [...root.querySelectorAll(sel)];

/** O foco está num campo de digitação? (atalhos de uma tecla não devem disparar) */
export function isTyping(el = document.activeElement) {
  return !!el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName));
}

/** Minúsculas e sem acento, para filtro. */
export function normalize(text) {
  return (text || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
}
