import pytest
from pydantic_settings import SettingsConfigDict

from sleep_diary_api import create_app, db
from sleep_diary_api.config import Config


class TestConfig(Config):
    model_config = SettingsConfigDict(
        env_file=".test.env",
        extra="allow"
    )

    # Flask Testing Config
    TESTING: bool


test_configuration = TestConfig()


@pytest.fixture(
    scope="function",
    autouse=True
)
def app():
    assert test_configuration.TESTING is True
    assert test_configuration.DB_NAME == "test_db"

    app = create_app()
    app.config.from_object(test_configuration)
    with app.app_context():
        db.create_all()
    # other setup can go here
    yield app
    # clean up / reset resources here
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
