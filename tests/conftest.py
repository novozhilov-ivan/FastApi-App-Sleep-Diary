import pytest
from flask import Flask
from flask.testing import FlaskCliRunner, FlaskClient
from pydantic_settings import SettingsConfigDict

from api import create_app, db
from api.config import Config


class TestConfig(Config):
    model_config = SettingsConfigDict(env_file=".test.env", extra="allow")
    TESTING: bool


test_configuration = TestConfig()


@pytest.fixture
def app() -> Flask:
    assert test_configuration.TESTING is True
    app = create_app()
    app.config.from_object(test_configuration)
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield app


@pytest.fixture
def client(app) -> FlaskClient:
    with app.test_request_context():
        yield app.test_client()


@pytest.fixture
def runner(app) -> FlaskCliRunner:
    return app.test_cli_runner()
