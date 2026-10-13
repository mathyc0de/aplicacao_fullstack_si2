import pytest

from app.errors import SqlInjectionError
from app.security.sql_guard import reject_sql_payload


@pytest.mark.parametrize(
    "payload",
    [
        "1; DROP TABLE servidores",
        "nome' OR 1=1 --",
        "x UNION SELECT senha FROM usuarios",
    ],
)
def test_rejeita_payloads_suspeitos(payload):
    with pytest.raises(SqlInjectionError):
        reject_sql_payload(payload, "nome")


def test_aceita_nome_comum():
    reject_sql_payload("Maria da Conceição Silva", "nome")
