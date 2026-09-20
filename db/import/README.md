# Importação das bases do dados.gov.br

Os arquivos oficiais não entram no repositório. Baixe os CSVs do Portal Brasileiro
de Dados Abertos e execute o carregador a partir do contêiner do backend ou de
uma máquina com acesso ao PostgreSQL.

Fontes:

- https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal--aposentados
- https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal---carreiras--cargos

Exemplo:

```bash
python import/load_csv.py --aposentados /data/APOSENTADOS.csv --cargos /data/CARGOS.csv
```
