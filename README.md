# Consulta a servidores do Executivo Federal

Aplicação full stack para consultar servidores ativos e aposentados do Poder
Executivo Federal, com dados dos conjuntos abertos de
[aposentados](https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal--aposentados)
e [carreiras/cargos](https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal---carreiras--cargos).

## Subir o ambiente

Na raiz do projeto:

```bash
docker compose up --build
```

- Frontend: http://localhost:8080
- API: http://localhost:8000
- PostgreSQL: localhost:5433 (`app` / `app` / `servidores`)

## Endpoints

```
GET /api/servidores?cargo=<cargo>
GET /api/servidores?uf=<uf>
GET /api/servidores?orgao=<orgao>
GET /api/servidores?nome=<nome>&cargo=<cargo>&uf=<uf>
GET /api/servidores?similar=%NO%ME%&limit=100
GET /api/cargos
GET /api/orgaos
GET /api/ufs
GET /health
```

A API rejeita tentativas de SQL injection, valida UF/cargo/órgão, pagina
resultados múltiplos, aplica timeout de consulta e limita buscas simultâneas.

## Desktop (adicional)

O cliente gráfico em `desktop/` consome a mesma API e não entra no Docker.

```bash
cd desktop
python3 -m pip install -r requirements.txt
python3 app.py
```

## Importação das bases oficiais

Os arquivos oficiais não são versionados. Coloque `APOSENTADOS_*.csv` e
`CARREIRA_*.txt` em `db/data/` antes do `docker compose up --build` e o banco é
carregado automaticamente. Sem os arquivos, sobe com dados de exemplo. Detalhes
em `db/import/README.md`.
## Exemplo de similaridade

`GET /api/servidores?similar=%SILVA%&limit=20`

## Equipe

- Karoline Vieira (KarolineVieiraa) — líder técnica, planejamento, Compose e entrega
- Matheus Silveira (mathyc0de) — contrato e API Flask
- Lara Letittja (Letittja) — interface web e desktop
- Allan Machado Gonçalves (zAllaNz) — dados, PostgreSQL e importação

O período de trabalho vai de 17/08/2026 a 13/10/2026.
