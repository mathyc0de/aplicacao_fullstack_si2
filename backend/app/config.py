import os


class Config:
    APP_NAME = "API Servidores do Executivo Federal"
    JSON_SORT_KEYS = False
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://app:app@localhost:5432/servidores",
    )
    DB_CONNECT_TIMEOUT = int(os.getenv("DB_CONNECT_TIMEOUT", "5"))
    QUERY_TIMEOUT_MS = int(os.getenv("QUERY_TIMEOUT_MS", "5000"))
    DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", "20"))
    MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE", "100"))
    RATE_LIMIT = os.getenv("RATE_LIMIT", "60 per minute")
    CONCURRENT_SEARCH_LIMIT = int(os.getenv("CONCURRENT_SEARCH_LIMIT", "8"))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
# Timeout alinhado ao requisito de busca com limite de tempo.
