import pytest

from app.errors import InvalidStringError
from app.validators.nome import validate_nome_exato, validate_similar


def test_nome_com_apostrofo():
    assert validate_nome_exato("D'Ávila Costa") == "D'Ávila Costa"


def test_similar_rejeita_so_curinga():
    with pytest.raises(InvalidStringError):
        validate_similar("%%%")
