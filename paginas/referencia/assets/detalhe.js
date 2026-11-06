// Controller da página de referência: mestre/detalhe.
const items = [...document.querySelectorAll("[data-ref-item]")];
const fields = {
  nome: document.querySelector("[data-ref-nome]"),
  codigo: document.querySelector("[data-ref-codigo]"),
  curso: document.querySelector("[data-ref-curso]"),
  status: document.querySelector("[data-ref-status]"),
  title: document.querySelector("[data-ref-title]"),
};
const tones = ["success", "warning", "destructive", "info"];

function select(item) {
  for (const other of items) other.setAttribute("aria-current", String(other === item));
  fields.nome.textContent = item.dataset.nome;
  fields.codigo.textContent = item.dataset.codigo;
  fields.curso.textContent = item.dataset.curso;
  fields.title.textContent = item.dataset.nome;
  fields.status.textContent = item.dataset.status;
  fields.status.classList.remove(...tones.map((tone) => `ttsc-badge-${tone}`));
  fields.status.classList.add(`ttsc-badge-${item.dataset.tone}`);
}

for (const item of items) item.addEventListener("click", () => select(item));

document.querySelector("[data-ref-theme]")?.addEventListener("click", () => {
  const html = document.documentElement;
  html.dataset.theme = html.dataset.theme === "dark" ? "light" : "dark";
});
