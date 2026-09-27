def build_health_payload(database_ok: bool) -> dict:
    return {
        "status": "ok" if database_ok else "degraded",
        "database": "up" if database_ok else "down",
        "service": "servidores-api",
    }
