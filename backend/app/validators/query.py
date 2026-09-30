from dataclasses import dataclass

from flask import current_app

from app.constants import SITUACOES_VALIDAS
from app.errors import InvalidParameterError, InvalidStringError
from app.normalizers import compact_spaces
from app.security.sql_guard import reject_sql_payload
from app.validators.nome import validate_nome_exato, validate_similar
from app.validators.uf import validate_uf


@dataclass(frozen=True)
class SearchParams:
    nome: str | None
    similar: str | None
    cargo: str | None
    uf: str | None
    orgao: str | None
    situacao: str | None
    page: int
    limit: int


def _optional_text(raw: str | None, field: str, *, min_len: int = 2) -> str | None:
    if raw is None or raw == "":
        return None
    reject_sql_payload(raw, field)
    value = compact_spaces(raw)
    if len(value) < min_len:
        raise InvalidStringError(f"O parâmetro {field} deve ter pelo menos {min_len} caracteres.")
    return value


def _positive_int(raw: str | None, field: str, default: int, maximum: int | None = None) -> int:
    if raw is None or raw == "":
        return default
    reject_sql_payload(raw, field)
    if not str(raw).isdigit():
        raise InvalidParameterError(f"O parâmetro {field} deve ser um número inteiro positivo.")
    value = int(raw)
    if value < 1:
        raise InvalidParameterError(f"O parâmetro {field} deve ser maior ou igual a 1.")
    if maximum is not None and value > maximum:
        raise InvalidParameterError(f"O parâmetro {field} não pode ser maior que {maximum}.")
    return value


def parse_search_params(args) -> SearchParams:
    allowed = {"nome", "similar", "cargo", "uf", "orgao", "situacao", "page", "limit", "per_page"}
    unknown = sorted(set(args.keys()) - allowed)
    if unknown:
        raise InvalidParameterError(
            "Parâmetros de busca inválidos.",
            details={"desconhecidos": unknown, "permitidos": sorted(allowed)},
        )

    nome_raw = args.get("nome")
    similar_raw = args.get("similar")
    if nome_raw:
        reject_sql_payload(nome_raw, "nome")
        nome = validate_nome_exato(nome_raw)
    else:
        nome = None
    if similar_raw:
        reject_sql_payload(similar_raw, "similar")
        similar = validate_similar(similar_raw)
    else:
        similar = None
    if nome and similar:
        raise InvalidParameterError("Use apenas um de nome ou similar na mesma consulta.")

    cargo = _optional_text(args.get("cargo"), "cargo")
    orgao = _optional_text(args.get("orgao"), "orgao")
    uf_raw = args.get("uf")
    uf = validate_uf(uf_raw) if uf_raw else None

    situacao_raw = args.get("situacao")
    situacao = None
    if situacao_raw:
        reject_sql_payload(situacao_raw, "situacao")
        situacao = situacao_raw.strip().upper()
        if situacao not in SITUACOES_VALIDAS:
            raise InvalidParameterError(
                "Situação inválida. Use ATIVO ou APOSENTADO.",
                details={"situacao": situacao_raw},
            )

    max_page = current_app.config["MAX_PAGE_SIZE"]
    default_page = current_app.config["DEFAULT_PAGE_SIZE"]
    limit_raw = args.get("limit", args.get("per_page"))
    limit = _positive_int(limit_raw, "limit", default_page, max_page)
    page = _positive_int(args.get("page"), "page", 1)

    if not any([nome, similar, cargo, uf, orgao, situacao]):
        raise InvalidParameterError("Informe ao menos um filtro de busca.")

    return SearchParams(
        nome=nome,
        similar=similar,
        cargo=cargo,
        uf=uf,
        orgao=orgao,
        situacao=situacao,
        page=page,
        limit=limit,
    )
