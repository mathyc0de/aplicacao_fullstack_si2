# Ajustes depois da carga

Se a rajada gerar 429 de forma contínua:

- rever o semáforo de buscas simultâneas;
- rever timeout de statement no PostgreSQL;
- rever workers e threads do Gunicorn.

Depois do ajuste, o mesmo cenário é repetido. A limitação conhecida é o
tamanho da base sintética de demonstração, menor que o CSV oficial completo.
