import pytest

from app import create_app
from app.config import Config


class TestConfig(Config):
    TESTING = True
    RATE_LIMIT = "1000 per minute"
    CONCURRENT_SEARCH_LIMIT = 8


@pytest.fixture
def app():
    return create_app(TestConfig)


@pytest.fixture
def client(app):
    return app.test_client()
