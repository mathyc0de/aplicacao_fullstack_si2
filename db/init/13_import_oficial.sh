importar_oficial() {
    local apos="" carr="" f

    for f in /data/APOSENTADOS*.csv; do
        if [ -f "$f" ]; then apos="$f"; break; fi
    done
    for f in /data/CARREIRA*.txt /data/CARREIRA*.csv; do
        if [ -f "$f" ]; then carr="$f"; break; fi
    done

    if [ -z "$apos" ] && [ -z "$carr" ]; then
        echo "import_oficial: nenhum arquivo em db/data, mantendo os dados de exemplo"
        return 0
    fi

    echo "import_oficial: aposentados=${apos:-nenhum} carreiras=${carr:-nenhum}"

    local vars=()
    [ -n "$apos" ] && vars+=(-v "apos_file=$apos")
    [ -n "$carr" ] && vars+=(-v "carr_file=$carr")

    PGHOST= PGHOSTADDR= psql -v ON_ERROR_STOP=1 --no-psqlrc --no-password \
        --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
        --single-transaction "${vars[@]}" -f - <<'SQL'
SET maintenance_work_mem = '512MB';

CREATE FUNCTION pg_temp.limpa(t text) RETURNS text
LANGUAGE sql IMMUTABLE AS $$
    SELECT NULLIF(btrim(regexp_replace(coalesce(t, ''), '\s+', ' ', 'g')), '')
$$;

CREATE FUNCTION pg_temp.data_br(t text) RETURNS date
LANGUAGE plpgsql AS $$
BEGIN
    IF t !~ '^[0-9]{8}$' THEN
        RETURN NULL;
    END IF;
    RETURN to_date(t, 'DDMMYYYY');
EXCEPTION WHEN others THEN
    RETURN NULL;
END
$$;

DROP INDEX IF EXISTS idx_servidores_nome_norm, idx_servidores_nome_trgm,
    idx_servidores_cargo, idx_servidores_orgao, idx_servidores_uf,
    idx_servidores_situacao, idx_servidores_filtros, idx_orgaos_sigla,
    idx_orgaos_nome_trgm, idx_cargos_carreira;

TRUNCATE servidores, cargos, orgaos RESTART IDENTITY;

\if :{?apos_file}
CREATE TEMP TABLE raw_apos (linha text) ON COMMIT DROP;
COPY raw_apos FROM :'apos_file'
    WITH (FORMAT csv, DELIMITER E'\x02', QUOTE E'\x01', HEADER true, ENCODING 'LATIN1');

CREATE TEMP TABLE apos ON COMMIT DROP AS
SELECT left(pg_temp.limpa(f[1]), 200)                               AS nome,
       left(pg_temp.limpa(f[2]), 14)                                AS cpf,
       left(pg_temp.limpa(f[3]), 20)                                AS matricula,
       left(coalesce(pg_temp.limpa(f[4]), 'NAO INFORMADO'), 200)    AS orgao,
       left(pg_temp.limpa(f[5]), 30)                                AS sigla,
       left(pg_temp.limpa(f[6]), 200)                               AS orgao_sup,
       left(coalesce(pg_temp.limpa(f[7]), 'NAO INFORMADO'), 200)    AS cargo,
       left(pg_temp.limpa(f[8]), 10)                                AS classe,
       left(pg_temp.limpa(f[12]), 80)                               AS tipo,
       pg_temp.data_br(pg_temp.limpa(f[15]))                        AS dt
FROM (SELECT string_to_array(linha, ';') AS f FROM raw_apos) x
WHERE length(pg_temp.limpa(f[1])) >= 2;

INSERT INTO cargos (descricao, classe)
SELECT DISTINCT ON (upper(cargo)) cargo, classe FROM apos ORDER BY upper(cargo)
ON CONFLICT (upper(descricao)) DO NOTHING;

INSERT INTO orgaos (nome, sigla, uf_sede, orgao_superior)
SELECT DISTINCT ON (upper(a.orgao)) a.orgao, a.sigla, 'DF', a.orgao_sup
FROM apos a
WHERE NOT EXISTS (SELECT 1 FROM orgaos o WHERE upper(o.nome) = upper(a.orgao))
ORDER BY upper(a.orgao);

INSERT INTO servidores (
    nome, cpf_mascarado, matricula, cargo_id, orgao_id, uf, situacao,
    tipo_aposentadoria, data_aposentadoria, regime_juridico
)
SELECT a.nome, a.cpf, a.matricula, c.id, o.id, o.uf_sede, 'APOSENTADO',
       a.tipo, a.dt, 'Regime Jurídico Único'
FROM apos a
JOIN cargos c ON upper(c.descricao) = upper(a.cargo)
JOIN orgaos o ON upper(o.nome) = upper(a.orgao);
\endif

\if :{?carr_file}
CREATE TEMP TABLE raw_carr (linha text) ON COMMIT DROP;
COPY raw_carr FROM :'carr_file'
    WITH (FORMAT csv, DELIMITER E'\x02', QUOTE E'\x01', HEADER true, ENCODING 'LATIN1');

CREATE TEMP TABLE carr ON COMMIT DROP AS
SELECT left(pg_temp.limpa(f[1]), 200)                               AS nome,
       left(pg_temp.limpa(f[2]), 14)                                AS cpf,
       left(pg_temp.limpa(f[3]), 200)                               AS carreira,
       left(coalesce(pg_temp.limpa(f[4]), 'NAO INFORMADO'), 200)    AS cargo,
       CASE WHEN upper(pg_temp.limpa(f[5])) ~ '^[A-Z]{2}$'
            THEN upper(pg_temp.limpa(f[5])) END                     AS uf,
       left(coalesce(pg_temp.limpa(f[6]), 'NAO INFORMADO'), 200)    AS orgao
FROM (SELECT string_to_array(linha, ';') AS f FROM raw_carr) x
WHERE length(pg_temp.limpa(f[1])) >= 2;

INSERT INTO cargos (descricao, carreira)
SELECT DISTINCT ON (upper(cargo)) cargo, carreira FROM carr ORDER BY upper(cargo)
ON CONFLICT (upper(descricao)) DO NOTHING;

INSERT INTO orgaos (nome, uf_sede)
SELECT min(c.orgao), coalesce(mode() WITHIN GROUP (ORDER BY c.uf), 'DF')
FROM carr c
WHERE NOT EXISTS (SELECT 1 FROM orgaos o WHERE upper(o.nome) = upper(c.orgao))
GROUP BY upper(c.orgao);

INSERT INTO servidores (nome, cpf_mascarado, cargo_id, orgao_id, uf, situacao)
SELECT c2.nome, c2.cpf, c.id, o.id, coalesce(c2.uf, o.uf_sede), 'ATIVO'
FROM carr c2
JOIN cargos c ON upper(c.descricao) = upper(c2.cargo)
JOIN orgaos o ON upper(o.nome) = upper(c2.orgao);
\endif

\i /docker-entrypoint-initdb.d/06_indexes.sql
ANALYZE servidores;
ANALYZE cargos;
ANALYZE orgaos;
SQL
}

importar_oficial || echo "import_oficial: falhou, mantendo os dados de exemplo"
