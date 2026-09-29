from flask import Blueprint, jsonify, request

from app.errors import InvalidParameterError, PageNotFoundError
from app.repositories.servidores import get_servidor, search_servidores
from app.security.concurrency import acquire_search_slot
from app.validators.query import parse_search_params

servidores_bp = Blueprint("servidores", __name__, url_prefix="/api")


@servidores_bp.get("/servidores")
def list_servidores():
    params = parse_search_params(request.args)
    with acquire_search_slot():
        payload = search_servidores(params)
    return jsonify(payload)


@servidores_bp.get("/servidores/<int:servidor_id>")
def show_servidor(servidor_id: int):
    if servidor_id < 1:
        raise InvalidParameterError("Identificador de servidor inválido.")
    item = get_servidor(servidor_id)
    if item is None:
        raise PageNotFoundError("Servidor não encontrado.", details={"id": servidor_id})
    return jsonify(item)
