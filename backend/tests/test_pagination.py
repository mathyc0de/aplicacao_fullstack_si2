import pytest

from app.errors import PageNotFoundError
from app.pagination import paginate


def test_paginate_primeira_pagina():
    meta = paginate(45, 1, 20)
    assert meta["last_page"] == 3
    assert meta["offset"] == 0
    assert meta["has_next"] is True
    assert meta["multiplo"] is True


def test_paginate_pagina_inexistente():
    with pytest.raises(PageNotFoundError):
        paginate(10, 5, 20)


def test_paginate_resultado_unico():
    meta = paginate(1, 1, 20)
    assert meta["multiplo"] is False
    assert meta["last_page"] == 1
