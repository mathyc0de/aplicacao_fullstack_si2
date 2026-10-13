from app.normalizers import normalize_nome, strip_accents


def test_normalize_remove_acentos():
    assert normalize_nome("José da Conceição") == "JOSE DA CONCEICAO"


def test_normalize_compacta_espacos():
    assert normalize_nome("  Ana   Paula  ") == "ANA PAULA"


def test_strip_accents():
    assert strip_accents("Açaí") == "Acai"
