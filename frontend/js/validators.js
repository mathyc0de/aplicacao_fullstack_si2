function collectFilters(form) {
  const data = new FormData(form);
  const filters = {};
  for (const [key, value] of data.entries()) {
    const trimmed = String(value).trim();
    if (trimmed) {
      filters[key] = trimmed;
    }
  }
  if (filters.nome && filters.similar) {
    throw new Error("Use apenas nome exato ou similaridade, não os dois.");
  }
  if (!filters.nome && !filters.similar && !filters.cargo && !filters.orgao && !filters.uf && !filters.situacao) {
    throw new Error("Informe ao menos um filtro de busca.");
  }
  if (filters.limit) {
    const limit = Number(filters.limit);
    if (!Number.isInteger(limit) || limit < 1 || limit > 100) {
      throw new Error("O limite deve ser um inteiro entre 1 e 100.");
    }
  }
  return filters;
}
