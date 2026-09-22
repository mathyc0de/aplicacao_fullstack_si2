CREATE TABLE cargos (
    id          SERIAL PRIMARY KEY,
    descricao   VARCHAR(200) NOT NULL,
    classe      VARCHAR(10),
    carreira    VARCHAR(200),
    jornada     VARCHAR(80)
);

CREATE UNIQUE INDEX cargos_descricao_uniq ON cargos (upper(descricao));

COMMENT ON TABLE cargos IS 'Cargos e carreiras do Executivo Federal (dados.gov.br).';
