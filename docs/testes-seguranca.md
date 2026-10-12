# Testes de entrada inválida e SQL injection

- UF, cargo, órgão e página fora do formato devolvem 400;
- payloads com aspas, comentário SQL e `UNION` são rejeitados;
- as consultas permanecem parametrizadas;
- o banco não é alterado por uma busca.
