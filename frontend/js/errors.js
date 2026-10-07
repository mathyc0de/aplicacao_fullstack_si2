function humanizeApiError(error) {
  const code = error.payload?.error;
  const map = {
    nome_nao_encontrado: "Nenhum servidor com esse nome.",
    uf_invalida: "UF inválida.",
    cargo_invalido: "Cargo não encontrado.",
    orgao_invalido: "Órgão não encontrado.",
    comando_sql_rejeitado: "A consulta foi bloqueada por segurança.",
    excesso_de_buscas: "Muitas buscas ao mesmo tempo.",
    tempo_busca_excedido: "A busca demorou demais.",
    pagina_inexistente: "Essa página não existe.",
  };
  return map[code] || error.message;
}
