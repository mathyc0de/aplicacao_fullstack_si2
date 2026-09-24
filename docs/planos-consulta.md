# Planos de consulta

Índices previstos para nome normalizado, cargo, UF e órgão.
A similaridade usa `pg_trgm` com índice GIN no nome normalizado.

Avaliação esperada:

- filtro isolado de UF ou órgão usa índice B-tree;
- padrão com curinga nas duas pontas usa o GIN trigram;
- combinação de filtros reduz o conjunto antes da ordenação paginada.
