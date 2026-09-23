CREATE VIEW vw_servidores AS
SELECT
    s.id,
    s.id_portal,
    s.nome,
    s.nome_normalizado,
    s.cpf_mascarado,
    s.matricula,
    s.uf,
    s.situacao,
    s.tipo_aposentadoria,
    s.data_aposentadoria,
    s.regime_juridico,
    s.jornada,
    c.id AS cargo_id,
    c.descricao AS cargo,
    c.classe AS cargo_classe,
    c.carreira,
    o.id AS orgao_id,
    o.nome AS orgao,
    o.sigla AS orgao_sigla,
    o.uf_sede,
    o.orgao_superior
FROM servidores s
JOIN cargos c ON c.id = s.cargo_id
JOIN orgaos o ON o.id = s.orgao_id;
