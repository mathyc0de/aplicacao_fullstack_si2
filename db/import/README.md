# Importação das bases do dados.gov.br

Os arquivos oficiais (150–200 MB cada) não entram no repositório nem no ZIP.

Fontes:

- https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal--aposentados
- https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal---carreiras--cargos

| Arquivo | Conteúdo | Formato |
| --- | --- | --- |
| `APOSENTADOS_*.csv` | aposentados (18 colunas) | `;`, ISO-8859-1, com cabeçalho |
| `CARREIRA_*.txt` | servidores ativos (8 colunas) | `;`, ISO-8859-1, com cabeçalho |

## Carga automática (recomendada)

Copie os dois arquivos para `db/data/` e suba o ambiente a partir de um volume
novo:

```bash
docker compose down -v
docker compose up --build
```

Na primeira inicialização, `db/init/13_import_oficial.sh` apaga os dados de
exemplo, importa os arquivos em uma única transação e recria os índices. Se a
pasta estiver vazia, o banco fica com os dados de exemplo. Se a importação
falhar, os dados de exemplo permanecem e o motivo aparece no log do `db`.

A carga de ~1,5 milhão de registros leva alguns minutos; o `db` só fica
saudável quando termina.

## Carga manual (alternativa)

Com o banco já no ar e Python com `psycopg`:

```bash
python db/import/load_csv.py --check --aposentados A.csv --carreiras C.txt
export DATABASE_URL=postgresql://app:app@localhost:5433/servidores
python db/import/load_csv.py --replace --aposentados A.csv --carreiras C.txt
```

Opções: `--limit N`, `--dry-run`, `--replace`, `--check` (sem banco).

O arquivo de aposentados não traz UF; os registros usam a UF-sede do órgão
(`DF` para órgãos novos).
