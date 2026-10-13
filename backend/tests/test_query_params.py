import pytest

from app.errors import InvalidParameterError
from app.validators.query import parse_search_params


def test_exige_filtro(app):
    with app.app_context():
        with pytest.raises(InvalidParameterError):
            parse_search_params({})


def test_combina_cargo_e_uf(app):
    with app.app_context():
        params = parse_search_params({"cargo": "Professor", "uf": "MG"})
        assert params.cargo == "Professor"
        assert params.uf == "MG"
        assert params.page == 1


def test_rejeita_parametro_desconhecido(app):
    with app.app_context():
        with pytest.raises(InvalidParameterError):
            parse_search_params({"foo": "bar", "uf": "SP"})
