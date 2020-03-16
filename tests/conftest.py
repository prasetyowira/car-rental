import pytest
from rental_app import create_app


@pytest.fixture(scope="module")
def app():
    return create_app(test=True)


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


@pytest.fixture(scope="module")
def cli(app):
    return app.test_cli_runner()
