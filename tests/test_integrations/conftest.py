import json

import pytest

from pydantic_settings import SettingsConfigDict

from sleep_diary_api import create_app, db
from sleep_diary_api.config import Config


@pytest.fixture
def main_info(client):
    static_dir = client.application.static_folder
    with open(f"{static_dir}/content/main.json", "r") as f:
        return json.load(f)


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
