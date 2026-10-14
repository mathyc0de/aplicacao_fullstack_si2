# Validação em ambiente limpo

1. Clonar o repositório em um diretório vazio.
2. Copiar `.env.example` apenas se for preciso sobrescrever portas.
3. Executar `docker compose up --build` na raiz.
4. Abrir `http://localhost:8080` e `GET http://localhost:8000/health`.
5. Buscar um nome presente na carga de demonstração.
6. Confirmar que o volume do Postgres sobrevive a `docker compose stop`
   e some apenas com a remoção explícita do volume.
