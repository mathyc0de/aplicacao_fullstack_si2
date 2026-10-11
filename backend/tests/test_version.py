from app.version import APP_CODENAME, __version__


def test_versao_semantica():
    assert __version__.count(".") == 2
    assert APP_CODENAME == "servidores-executivo"
