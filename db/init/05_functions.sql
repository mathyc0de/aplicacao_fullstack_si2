CREATE OR REPLACE FUNCTION normalize_nome(valor TEXT)
RETURNS TEXT
LANGUAGE sql
IMMUTABLE
STRICT
AS $$
    SELECT regexp_replace(upper(public.unaccent(trim(valor))), '\s+', ' ', 'g');
$$;

CREATE OR REPLACE FUNCTION servidores_set_nome_normalizado()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.nome_normalizado := normalize_nome(NEW.nome);
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_servidores_nome_norm
BEFORE INSERT OR UPDATE OF nome ON servidores
FOR EACH ROW
EXECUTE FUNCTION servidores_set_nome_normalizado();
