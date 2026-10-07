async function hydrateCatalogs() {
  const [ufs, cargos, orgaos] = await Promise.all([
    fetchUfs().catch(() => ({ todas: [] })),
    fetchCargos().catch(() => ({ items: [] })),
    fetchOrgaos().catch(() => ({ items: [] })),
  ]);
  fillSelect(
    document.getElementById("uf"),
    ufs.todas || [],
    (uf) => uf,
    (uf) => uf
  );
  fillDatalist(
    document.getElementById("cargos-list"),
    (cargos.items || []).map((item) => item.descricao)
  );
  fillDatalist(
    document.getElementById("orgaos-list"),
    (orgaos.items || []).flatMap((item) => [item.sigla, item.nome].filter(Boolean))
  );
}

document.addEventListener("DOMContentLoaded", async () => {
  bindSearchForm();
  await hydrateCatalogs();
});
