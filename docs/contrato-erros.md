# Paginação e erros

Metadados: `total`, `page`, `per_page`, `last_page`, `has_next`, `has_prev`.
A ordenação é estável por nome e identificador.

| Situação | HTTP |
| --- | --- |
| Consulta válida | 200 |
| Parâmetro inválido ou SQL injection | 400 |
| Página inexistente | 404 |
| Banco indisponível | 503 |
| Muitas buscas simultâneas | 429 |
| Falha interna | 500, sem detalhe sensível |
