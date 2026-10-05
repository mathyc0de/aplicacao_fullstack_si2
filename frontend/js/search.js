let lastFilters = {};

async function runSearch(page = 1) {
  showAlert("");
  setStatus("idle", "consultando");
  try {
    const payload = await searchServidores({ ...lastFilters, page });
    if (payload.total === 0) {
      renderEmpty("Nenhum registro encontrado para os filtros informados.");
      setStatus("err", "vazio");
      return;
    }
    ui.meta.textContent = payload.multiplo
      ? `${payload.total} registros encontrados, exibidos de forma paginada.`
      : "Um único registro encontrado.";
    if (payload.total === 1) {
      renderSingle(payload.items[0]);
    } else {
      renderTable(payload.items);
    }
    updatePagination(payload);
    setStatus("ok", "ok");
  } catch (error) {
    renderEmpty("Não foi possível concluir a consulta.");
    showAlert(typeof humanizeApiError === "function" ? humanizeApiError(error) : error.message);
    setStatus("err", error.payload?.error || "erro");
  }
}

function bindSearchForm() {
  const form = document.getElementById("search-form");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    try {
      lastFilters = collectFilters(form);
      runSearch(1);
    } catch (error) {
      showAlert(error.message);
      setStatus("err", "filtro");
    }
  });
  form.addEventListener("reset", () => {
    lastFilters = {};
    showAlert("");
    renderEmpty("Informe um filtro para iniciar a consulta.");
    setStatus("idle", "aguardando");
  });
  document.getElementById("prev-page").addEventListener("click", () => {
    if (Pagination.hasPrev) runSearch(Pagination.page - 1);
  });
  document.getElementById("next-page").addEventListener("click", () => {
    if (Pagination.hasNext) runSearch(Pagination.page + 1);
  });
}
