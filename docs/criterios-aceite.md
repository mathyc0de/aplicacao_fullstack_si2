# Critérios de aceite

- `GET /api/servidores` cobre nome, cargo, UF, órgão e combinações.
- Similaridade respeita os três padrões e o limite informado.
- Página inexistente, parâmetro inválido e tentativa de SQL injection
  devolvem JSON e não alteram o banco.
- Excesso de buscas simultâneas não derruba o processo.
- `docker compose up --build` sobe os três serviços a partir da raiz.
- A entrega não inclui o dump do banco nem credenciais reais.
