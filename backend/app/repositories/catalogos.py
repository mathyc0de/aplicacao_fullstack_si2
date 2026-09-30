from app.db import db_cursor
from app.serializers import serialize_cargo, serialize_orgao


def list_cargos() -> list[dict]:
    with db_cursor() as cursor:
        cursor.execute(
            "SELECT id, descricao, classe, carreira, jornada FROM cargos ORDER BY descricao"
        )
        return [serialize_cargo(row) for row in cursor.fetchall()]


def list_orgaos() -> list[dict]:
    with db_cursor() as cursor:
        cursor.execute(
            "SELECT id, codigo, nome, sigla, uf_sede, orgao_superior FROM orgaos ORDER BY nome"
        )
        return [serialize_orgao(row) for row in cursor.fetchall()]


def list_ufs() -> list[dict]:
    with db_cursor() as cursor:
        cursor.execute(
            "SELECT uf, COUNT(*) AS total FROM servidores GROUP BY uf ORDER BY uf"
        )
        return [{"uf": row["uf"], "total": row["total"]} for row in cursor.fetchall()]
