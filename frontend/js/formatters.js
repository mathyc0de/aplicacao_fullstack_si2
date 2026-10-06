function formatSituacao(value) {
  return value === "APOSENTADO" ? "Aposentado" : "Ativo";
}

function formatMeta(total, page, lastPage) {
  if (total === 1) {
    return "Registro único encontrado.";
  }
  return `${total} registros · página ${page} de ${lastPage}`;
}
