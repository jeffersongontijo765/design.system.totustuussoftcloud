// Controller da página de referência: lista densa de matrículas.
const search = document.querySelector("[data-ref-search]");
const status = document.querySelector("[data-ref-status]");
const rowsBody = document.querySelector("[data-ref-rows]");
const range = document.querySelector("[data-ref-range]");
const emptyBlock = document.querySelector('[data-state="empty"]');

function rows() {
  return rowsBody ? [...rowsBody.querySelectorAll("tr")] : [];
}

function applyFilters() {
  const term = (search?.value ?? "").trim().toLowerCase();
  const wanted = status?.value ?? "";
  let visible = 0;

  for (const row of rows()) {
    const text = row.textContent.toLowerCase();
    const matchTerm = !term || text.includes(term);
    const matchStatus = !wanted || row.dataset.status === wanted;
    const show = matchTerm && matchStatus;
    row.hidden = !show;
    if (show) visible++;
  }

  if (range) range.textContent = `Mostrando ${visible} de ${rows().length}`;
  if (emptyBlock) emptyBlock.hidden = visible !== 0;
}

search?.addEventListener("input", applyFilters);
status?.addEventListener("change", applyFilters);

document.querySelectorAll("[data-ref-clear]").forEach((button) => {
  button.addEventListener("click", () => {
    if (search) search.value = "";
    if (status) status.value = "";
    applyFilters();
  });
});

document.querySelector("[data-ref-theme]")?.addEventListener("click", () => {
  const html = document.documentElement;
  html.dataset.theme = html.dataset.theme === "dark" ? "light" : "dark";
});

applyFilters();
