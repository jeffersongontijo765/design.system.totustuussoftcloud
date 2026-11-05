// Controller da página de referência: dashboard operacional.
// Só o que esta tela faz. Nenhum conhecimento de layout ou de outras páginas.
const root = document.querySelector("[data-ref-dashboard]");
const stamp = document.querySelector("[data-ref-updated]");
const time = new Intl.DateTimeFormat("pt-BR", { hour: "2-digit", minute: "2-digit" });

function markUpdated() {
  if (stamp) stamp.textContent = `Atualizado às ${time.format(new Date())} · dados de exemplo`;
}

document.querySelectorAll("[data-ref-refresh]").forEach((button) => {
  button.addEventListener("click", markUpdated);
});

document.querySelector("[data-ref-theme]")?.addEventListener("click", () => {
  const html = document.documentElement;
  html.dataset.theme = html.dataset.theme === "dark" ? "light" : "dark";
});

// Demonstração de estados: alterna os blocos marcados, provando que vazio,
// carregando e erro existem de verdade (e não só no caminho feliz).
const states = root ? [...root.querySelectorAll("[data-state]")] : [];
function showState(name) {
  for (const block of states) block.hidden = block.dataset.state !== name;
}
window.addEventListener("keydown", (event) => {
  if (event.key !== "F2" || !states.length) return;
  const order = ["loading", "error", "empty", ""];
  const current = states.find((b) => !b.hidden)?.dataset.state ?? "";
  showState(order[(order.indexOf(current) + 1) % order.length]);
});
for (const block of states) block.hidden = true;
