# Instalação e uso

Pré-requisitos: Docker, Docker Compose e, para o desktop, Python 3.

```bash
docker compose up --build
```

- Interface: http://localhost:8080
- API: http://localhost:8000/health
- Postgres no host: localhost:5433

Exemplo:

```
GET /api/servidores?uf=DF&page=1
GET /api/servidores?similar=%SILVA%&limit=20
```

Fontes e importação: `db/import/README.md`. Não há senha de produção neste
arquivo.
