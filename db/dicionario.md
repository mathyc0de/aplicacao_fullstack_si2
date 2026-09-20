# Dicionário sintetizado

Campos usados na aplicação, alinhados aos cadastros do Portal da Transparência
e aos CSVs de aposentados do dados.gov.br.

| Campo | Origem | Uso |
| --- | --- | --- |
| nome | NOME | Busca exata e similaridade |
| nome_normalizado | derivado | Índice e `LIKE` |
| cpf_mascarado | CPF | Exibição |
| matricula | MATRICULA | Exibição |
| cargo | DESCRICAO_CARGO | Filtro de cargo/carreira |
| orgao | ORGAO_LOTACAO / órgão de origem | Filtro de instituição |
| uf | UF_EXERCICIO ou sede do órgão | Filtro de estado |
| situacao | derivado | ATIVO ou APOSENTADO |
| tipo_aposentadoria | TIPO_APOSENTADORIA | Detalhe do inativo |
| regime_juridico | REGIME_JURIDICO | Detalhe do vínculo |
| jornada | JORNADA_DE_TRABALHO | Detalhe da carga horária |
