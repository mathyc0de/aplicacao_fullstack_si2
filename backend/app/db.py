from contextlib import contextmanager

import psycopg
from flask import current_app, g
from psycopg.rows import dict_row

from app.errors import QueryTimeoutError


def get_connection() -> psycopg.Connection:
    if "db_conn" not in g:
        g.db_conn = psycopg.connect(
            current_app.config["DATABASE_URL"],
            connect_timeout=current_app.config["DB_CONNECT_TIMEOUT"],
            row_factory=dict_row,
            options=f"-c statement_timeout={current_app.config['QUERY_TIMEOUT_MS']}",
        )
    return g.db_conn


def close_connection(_error=None) -> None:
    conn = g.pop("db_conn", None)
    if conn is not None:
        conn.close()


@contextmanager
def db_cursor():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            yield cursor
        conn.commit()
    except psycopg.errors.QueryCanceled as exc:
        conn.rollback()
        raise QueryTimeoutError(
            "A busca excedeu o tempo máximo permitido."
        ) from exc
    except Exception:
        conn.rollback()
        raise
