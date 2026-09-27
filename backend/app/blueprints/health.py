from flask import Blueprint, jsonify

from app.db import db_cursor
from app.health_payload import build_health_payload

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    try:
        with db_cursor() as cursor:
            cursor.execute("SELECT 1 AS ok")
            cursor.fetchone()
        payload = build_health_payload(True)
    except Exception:
        payload = build_health_payload(False)
    return jsonify(payload)
