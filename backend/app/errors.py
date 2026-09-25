class ApiError(Exception):
    status_code = 400
    code = "erro_requisicao"

    def __init__(self, message: str, *, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_dict(self) -> dict:
        payload = {"error": self.code, "message": self.message}
        if self.details:
            payload["details"] = self.details
        return payload


class InvalidParameterError(ApiError):
    code = "parametro_invalido"


class InvalidStringError(ApiError):
    code = "string_invalida"


class SqlInjectionError(ApiError):
    status_code = 400
    code = "comando_sql_rejeitado"


class NameNotFoundError(ApiError):
    status_code = 404
    code = "nome_nao_encontrado"


class InvalidCargoError(ApiError):
    status_code = 400
    code = "cargo_invalido"


class InvalidUfError(ApiError):
    status_code = 400
    code = "uf_invalida"


class InvalidOrgaoError(ApiError):
    status_code = 400
    code = "orgao_invalido"


class PageNotFoundError(ApiError):
    status_code = 404
    code = "pagina_inexistente"


class QueryTimeoutError(ApiError):
    status_code = 504
    code = "tempo_busca_excedido"


class TooManySearchesError(ApiError):
    status_code = 429
    code = "excesso_de_buscas"
