from app.constants import SQL_INJECTION_MARKERS
from app.errors import SqlInjectionError


def reject_sql_payload(value: str, field: str) -> None:
    lowered = f" {value.lower()} "
    if any(marker in lowered for marker in SQL_INJECTION_MARKERS):
        raise SqlInjectionError(
            "A consulta foi rejeitada porque parece conter um comando SQL.",
            details={"campo": field},
        )
