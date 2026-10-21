from contextlib import contextmanager
from threading import BoundedSemaphore

from flask import current_app

from app.errors import TooManySearchesError

_semaphore: BoundedSemaphore | None = None


def get_semaphore() -> BoundedSemaphore:
    global _semaphore
    if _semaphore is None:
        limit = int(current_app.config["CONCURRENT_SEARCH_LIMIT"])
        _semaphore = BoundedSemaphore(limit)
    return _semaphore


@contextmanager
def acquire_search_slot():
    semaphore = get_semaphore()
    if not semaphore.acquire(blocking=False):
        raise TooManySearchesError(
            "Há buscas demais em andamento. Tente novamente em instantes."
        )
    try:
        yield
    finally:
        semaphore.release()
