from typing import Generator

import pytest

from flask import Blueprint, Flask
from flask.testing import FlaskClient

from src.application.api.api import init_api_blueprint
from src.settings import AuthJWTSettings, FlaskSettings


class TestSettings(FlaskSettings, AuthJWTSettings):
    TESTING: bool = True
    PUBLIC_KEY: str = "secret"
    PRIVATE_KEY: str = "super_secret"
    SECRET_KEY: str = "secret"


@pytest.fixture(scope="session")
def api_bp() -> Blueprint:
    return init_api_blueprint()


@pytest.fixture(scope="session")
def app(api_bp: Blueprint) -> Flask:
    app = Flask("test_app")
    app.config.from_object(obj=TestSettings())
    app.register_blueprint(
        blueprint=api_bp,
        url_prefix="/api",
    )
    assert app.config.get("TESTING")
    return app


@pytest.fixture
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    with app.test_request_context(), app.app_context():
        yield app.test_client()
