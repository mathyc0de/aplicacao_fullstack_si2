CREATE INDEX idx_servidores_nome_norm ON servidores (nome_normalizado);
CREATE INDEX idx_servidores_nome_trgm ON servidores USING gin (nome_normalizado gin_trgm_ops);
CREATE INDEX idx_servidores_cargo ON servidores (cargo_id);
CREATE INDEX idx_servidores_orgao ON servidores (orgao_id);
CREATE INDEX idx_servidores_uf ON servidores (uf);
CREATE INDEX idx_servidores_situacao ON servidores (situacao);
CREATE INDEX idx_servidores_filtros ON servidores (uf, cargo_id, orgao_id);

CREATE INDEX idx_orgaos_sigla ON orgaos (upper(sigla));
CREATE INDEX idx_orgaos_nome_trgm ON orgaos USING gin (normalize_nome(nome) gin_trgm_ops);
CREATE INDEX idx_cargos_carreira ON cargos (normalize_nome(carreira));
-- Índices usam normalize_nome (IMMUTABLE); unaccent puro não pode ir em índice.
