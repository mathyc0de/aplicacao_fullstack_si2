from app.db import db_cursor
from app.errors import InvalidCargoError, InvalidOrgaoError, NameNotFoundError
from app.normalizers import normalize_nome
from app.pagination import paginate
from app.serializers import serialize_servidor
from app.validators.query import SearchParams


_BASE_FROM = "FROM vw_servidores s"


def _filters(params: SearchParams) -> tuple[list[str], list]:
    clauses: list[str] = []
    values: list = []

    if params.nome:
        clauses.append("s.nome_normalizado = %s")
        values.append(normalize_nome(params.nome))
    if params.similar:
        clauses.append("s.nome_normalizado LIKE %s")
        values.append(normalize_nome(params.similar))
    if params.cargo:
        clauses.append("(unaccent(s.cargo) ILIKE unaccent(%s) OR unaccent(s.carreira) ILIKE unaccent(%s))")
        like = f"%{params.cargo}%"
        values.extend([like, like])
    if params.orgao:
        clauses.append(
            "(unaccent(s.orgao) ILIKE unaccent(%s) OR unaccent(s.orgao_sigla) ILIKE unaccent(%s))"
        )
        like = f"%{params.orgao}%"
        values.extend([like, like])
    if params.uf:
        clauses.append("s.uf = %s")
        values.append(params.uf)
    if params.situacao:
        clauses.append("s.situacao = %s")
        values.append(params.situacao)

    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    return [where], values


def search_servidores(params: SearchParams) -> dict:
    where_parts, values = _filters(params)
    where = where_parts[0]

    with db_cursor() as cursor:
        if params.cargo:
            cursor.execute(
                "SELECT 1 FROM cargos WHERE unaccent(descricao) ILIKE unaccent(%s) "
                "OR unaccent(carreira) ILIKE unaccent(%s) LIMIT 1",
                (f"%{params.cargo}%", f"%{params.cargo}%"),
            )
            if cursor.fetchone() is None:
                raise InvalidCargoError(
                    f"Cargo ou carreira não encontrado: {params.cargo}.",
                    details={"cargo": params.cargo},
                )
        if params.orgao:
            cursor.execute(
                "SELECT 1 FROM orgaos WHERE unaccent(nome) ILIKE unaccent(%s) "
                "OR unaccent(sigla) ILIKE unaccent(%s) LIMIT 1",
                (f"%{params.orgao}%", f"%{params.orgao}%"),
            )
            if cursor.fetchone() is None:
                raise InvalidOrgaoError(
                    f"Instituição ou órgão não encontrado: {params.orgao}.",
                    details={"orgao": params.orgao},
                )

        cursor.execute(f"SELECT COUNT(*) AS total {_BASE_FROM}{where}", values)
        total = cursor.fetchone()["total"]

        if total == 0 and params.nome:
            raise NameNotFoundError(
                "Nenhum servidor encontrado com esse nome.",
                details={"nome": params.nome},
            )

        meta = paginate(total, params.page, params.limit)
        cursor.execute(
            f"SELECT * {_BASE_FROM}{where} ORDER BY s.nome LIMIT %s OFFSET %s",
            [*values, params.limit, meta["offset"]],
        )
        items = [serialize_servidor(row) for row in cursor.fetchall()]

    return {
        "total": meta["total"],
        "page": meta["page"],
        "per_page": meta["per_page"],
        "last_page": meta["last_page"],
        "has_next": meta["has_next"],
        "has_prev": meta["has_prev"],
        "multiplo": meta["multiplo"],
        "items": items,
    }


def get_servidor(servidor_id: int) -> dict | None:
    with db_cursor() as cursor:
        cursor.execute(f"SELECT * {_BASE_FROM} WHERE s.id = %s", (servidor_id,))
        row = cursor.fetchone()
    return serialize_servidor(row) if row else None
