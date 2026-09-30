import re

from app.errors import InvalidStringError
from app.normalizers import compact_spaces


_NAME_RE = re.compile(r"^[A-Za-zÀ-ÿ'\-.\s]+$")
_SIMILAR_RE = re.compile(r"^[A-Za-zÀ-ÿ%' \-.]+$")


def validate_nome_exato(value: str) -> str:
    nome = compact_spaces(value)
    if len(nome) < 2:
        raise InvalidStringError("Nome deve ter pelo menos 2 caracteres.")
    if not _NAME_RE.fullmatch(nome):
        raise InvalidStringError(
            "Nome contém caracteres inválidos. Use apenas letras, espaços, hífen ou apóstrofo."
        )
    return nome


def validate_similar(value: str) -> str:
    pattern = compact_spaces(value.strip().strip('"').strip("'"))
    if not pattern:
        raise InvalidStringError("Padrão de similaridade não pode ser vazio.")
    if "%" not in pattern:
        raise InvalidStringError(
            "Busca por similaridade exige curingas %. Exemplos: %SILVA%, NOME%SOBRENOME."
        )
    if not _SIMILAR_RE.fullmatch(pattern):
        raise InvalidStringError(
            "Padrão de similaridade inválido. Use letras, espaços e o curinga %."
        )
    if pattern.replace("%", "").strip() == "":
        raise InvalidStringError("Informe ao menos uma parte do nome além dos curingas.")
    return pattern
