// pagina-turmas.js — controller da página de exemplo (Acadêmico › Turmas › Lista de turmas).
//
// Só o que esta página faz (≤ 8 KB, R19):
//   - busca na tabela ([data-turmas-search]) com contador e estado "sem resultado";
//   - os quatro estados do bloco de dados, em [data-state]: data | empty | loading | error
//     (nomes em inglês, como nas páginas de referência e no ds-check, R14).
//     No app, o estado vem da resposta do servidor. Aqui dá para ver cada um pela URL:
//     index.html?estado=vazio | ?estado=carregando | ?estado=erro
//   - "Tentar novamente" e "Limpar busca" voltam para os dados.

(function () {
"use strict";
const normalize = (t) => (t || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
const root = document.querySelector("[data-turmas]");

if (root) {
  const blocks = [...root.querySelectorAll("[data-state]")];
  const search = root.querySelector("[data-turmas-search]");
  const rows = [...root.querySelectorAll("[data-turmas-rows] tr")];
  const count = root.querySelector("[data-turmas-count]");
  const noResults = root.querySelector("[data-turmas-no-results]");
  const term = root.querySelector("[data-turmas-term]");

  const show = (state) => {
    for (const block of blocks) block.hidden = block.dataset.state !== state;
    root.setAttribute("aria-busy", String(state === "loading"));
  };

  const filter = () => {
    const q = normalize(search?.value.trim());
    let visible = 0;
    for (const row of rows) {
      const match = !q || normalize(row.textContent).includes(q);
      row.hidden = !match;
      if (match) visible++;
    }
    if (count) count.textContent = `Mostrando ${visible} de ${rows.length}`;
    if (term) term.textContent = search?.value.trim() || "";
    if (noResults) noResults.hidden = visible !== 0;
  };

  search?.addEventListener("input", filter);

  root.addEventListener("click", (e) => {
    const action = e.target.closest("[data-action]")?.dataset.action;
    if (action === "clear-search" && search) { search.value = ""; filter(); search.focus(); }
    if (action === "retry") show("data");
  });

  const PREVIEW = { vazio: "empty", carregando: "loading", erro: "error" };
  const requested = new URLSearchParams(window.location.search).get("estado");
  show(PREVIEW[requested] || "data");
  filter();
}
})();
