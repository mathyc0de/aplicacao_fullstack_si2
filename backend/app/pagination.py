from app.errors import PageNotFoundError


def paginate(total: int, page: int, limit: int) -> dict:
    last_page = max(1, (total + limit - 1) // limit)
    if page > last_page and total > 0:
        raise PageNotFoundError(
            f"A página {page} não existe. A última página disponível é {last_page}.",
            details={"page": page, "last_page": last_page, "total": total},
        )
    offset = (page - 1) * limit
    return {
        "total": total,
        "page": page,
        "per_page": limit,
        "last_page": last_page,
        "offset": offset,
        "has_next": page < last_page,
        "has_prev": page > 1,
        "multiplo": total > 1,
    }
