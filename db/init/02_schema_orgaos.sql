CREATE TABLE orgaos (
    id          SERIAL PRIMARY KEY,
    codigo      VARCHAR(20) UNIQUE,
    nome        VARCHAR(200) NOT NULL,
    sigla       VARCHAR(30),
    uf_sede     CHAR(2) NOT NULL,
    orgao_superior VARCHAR(200),
    CONSTRAINT orgaos_uf_sede_chk CHECK (uf_sede ~ '^[A-Z]{2}$')
);

COMMENT ON TABLE orgaos IS 'Órgãos e instituições do Poder Executivo Federal.';
COMMENT ON COLUMN orgaos.uf_sede IS 'UF da sede do órgão, usada quando o servidor não tem UF de exercício.';
