# Qualidade dos dados

Antes da carga:

- trim e colapso de espaços em nome, cargo e órgão;
- UF em duas letras maiúsculas;
- registros sem nome são descartados e contados;
- duplicidade é avaliada por identificador do portal e por nome+órgão+cargo;
- uma amostra é conferida contra o CSV de origem.

A transformação fica no script de importação, não numa edição manual do CSV.
