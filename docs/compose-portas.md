# Portas e rede do Compose

| Serviço | Porta no host | Papel |
| --- | --- | --- |
| frontend | 8080 | interface |
| backend | 8000 | API Flask/Gunicorn |
| db | 5433 | PostgreSQL |

Os três serviços ficam na mesma rede do Compose. O backend espera o banco
ficar saudável antes de aceitar tráfego.
