import re
import unicodedata


_SPACE_RE = re.compile(r"\s+")


def strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def normalize_nome(value: str) -> str:
    cleaned = _SPACE_RE.sub(" ", strip_accents(value).strip())
    return cleaned.upper()


def compact_spaces(value: str) -> str:
    return _SPACE_RE.sub(" ", value).strip()
