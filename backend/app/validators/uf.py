from app.constants import UFS_VALIDAS
from app.errors import InvalidUfError


def validate_uf(value: str) -> str:
    uf = value.strip().upper()
    if uf not in UFS_VALIDAS:
        raise InvalidUfError(
            f"UF inválida: {value!r}. Informe uma sigla da federação, como SP ou DF.",
            details={"uf": value, "permitidas": sorted(UFS_VALIDAS)},
        )
    return uf
