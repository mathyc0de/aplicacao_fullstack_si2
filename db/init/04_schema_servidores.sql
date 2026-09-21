CREATE TABLE servidores (
    id                  SERIAL PRIMARY KEY,
    id_portal           BIGINT,
    nome                VARCHAR(200) NOT NULL,
    nome_normalizado    VARCHAR(200) NOT NULL,
    cpf_mascarado       VARCHAR(14),
    matricula           VARCHAR(20),
    cargo_id            INTEGER NOT NULL REFERENCES cargos (id),
    orgao_id            INTEGER NOT NULL REFERENCES orgaos (id),
    uf                  CHAR(2) NOT NULL,
    situacao            VARCHAR(20) NOT NULL,
    tipo_aposentadoria  VARCHAR(80),
    data_aposentadoria  DATE,
    regime_juridico     VARCHAR(80),
    jornada             VARCHAR(80),
    CONSTRAINT servidores_uf_chk CHECK (uf ~ '^[A-Z]{2}$'),
    CONSTRAINT servidores_situacao_chk CHECK (situacao IN ('ATIVO', 'APOSENTADO'))
);

COMMENT ON TABLE servidores IS 'Cadastro unificado de servidores ativos e aposentados.';
COMMENT ON COLUMN servidores.nome_normalizado IS 'Nome em maiúsculas sem acento, para busca exata e por similaridade.';
-- Situações aceitas pela API: ATIVO e APOSENTADO.
