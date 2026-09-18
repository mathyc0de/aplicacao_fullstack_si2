# Contrato da API

Base: `http://localhost:8000`.

```
GET /api/servidores
GET /api/cargos
GET /api/orgaos
GET /api/ufs
GET /health
```

Filtros de `/api/servidores`: `nome`, `cargo`, `uf`, `orgao`, `similar`,
`limit`, `page`. Filtros vazios são ignorados. A combinação é um E lógico.
Sem resultados a lista vem vazia, não um erro. Página fora do intervalo
devolve 404 com `last_page`.
