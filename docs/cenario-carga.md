# Cenário de concorrência

O script `backend/scripts/load_test.py` dispara buscas paralelas contra
`/api/servidores`.

Condições registradas para a plataforma de execução:

- mesmo host do Compose;
- workers e threads do Gunicorn conforme `gunicorn.conf.py`;
- limite de buscas simultâneas da API ligado;
- consulta com filtro de UF e outra com padrão de similaridade.
