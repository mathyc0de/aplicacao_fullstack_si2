from flask import Blueprint, jsonify

from app.db import db_cursor

stats_bp = Blueprint("stats", __name__, url_prefix="/api")


@stats_bp.get("/estatisticas")
def estatisticas():
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE situacao = 'ATIVO') AS ativos,
                COUNT(*) FILTER (WHERE situacao = 'APOSENTADO') AS aposentados,
                COUNT(DISTINCT uf) AS ufs,
                COUNT(DISTINCT cargo_id) AS cargos,
                COUNT(DISTINCT orgao_id) AS orgaos
            FROM servidores
            """
        )
        row = cursor.fetchone()
    return jsonify(row)
