from flask import Blueprint, jsonify

from app.constants import UFS_VALIDAS
from app.repositories.catalogos import list_cargos, list_orgaos, list_ufs

catalogos_bp = Blueprint("catalogos", __name__, url_prefix="/api")


@catalogos_bp.get("/cargos")
def cargos():
    return jsonify({"items": list_cargos()})


@catalogos_bp.get("/orgaos")
def orgaos():
    return jsonify({"items": list_orgaos()})


@catalogos_bp.get("/ufs")
def ufs():
    return jsonify(
        {
            "items": list_ufs(),
            "todas": sorted(UFS_VALIDAS),
        }
    )
