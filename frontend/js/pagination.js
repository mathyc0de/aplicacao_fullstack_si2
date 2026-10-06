const Pagination = {
  page: 1,
  lastPage: 1,
  hasNext: false,
  hasPrev: false,
};

function updatePagination(payload) {
  Pagination.page = payload.page;
  Pagination.lastPage = payload.last_page;
  Pagination.hasNext = payload.has_next;
  Pagination.hasPrev = payload.has_prev;
  const nav = document.getElementById("pagination");
  const label = document.getElementById("page-label");
  const prev = document.getElementById("prev-page");
  const next = document.getElementById("next-page");
  const show = payload.total > payload.per_page;
  nav.hidden = !show;
  label.textContent = `Página ${payload.page} de ${payload.last_page} · ${payload.total} registros`;
  prev.disabled = !payload.has_prev;
  next.disabled = !payload.has_next;
}
