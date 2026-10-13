import pytest

from app.errors import InvalidStringError, InvalidUfError, SqlInjectionError
from app.security.sql_guard import reject_sql_payload
from app.validators.nome import validate_nome_exato, validate_similar
from app.validators.uf import validate_uf


def test_validate_uf_aceita_sigla_minuscula():
    assert validate_uf("sp") == "SP"


def test_validate_uf_rejeita_invalida():
    with pytest.raises(InvalidUfError):
        validate_uf("XX")


def test_nome_exato_rejeita_curto():
    with pytest.raises(InvalidStringError):
        validate_nome_exato("A")


def test_similar_exige_curinga():
    with pytest.raises(InvalidStringError):
        validate_similar("SILVA")


def test_similar_aceita_padrao():
    assert validate_similar("%SILVA%SANTOS%") == "%SILVA%SANTOS%"


def test_sql_guard_detecta_union():
    with pytest.raises(SqlInjectionError):
        reject_sql_payload("ana' UNION SELECT 1", "nome")
