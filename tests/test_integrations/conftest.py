import json

import pytest

from pydantic_settings import SettingsConfigDict

from sleep_diary_api import create_app, db
from sleep_diary_api.Models import Notation, User
from sleep_diary_api.config import Config
from src.generators.sleep_diary import SleepDiaryGenerator
from src.pydantic_schemas.notes.sleep_diary import SleepDiaryModel
from src.pydantic_schemas.notes.sleep_notes import SleepNoteCompute


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


@pytest.fixture(scope="session",  autouse=True)
def app():
    assert test_configuration.TESTING is True
    assert test_configuration.DB_NAME == "test_db"

    app = create_app()
    app.config.from_object(test_configuration)
    with app.app_context():
        db.drop_all()
    with app.app_context():
        db.create_all()
    # other setup can go here
    yield app
    # clean up / reset resources here
    # with app.app_context():
    #     db.drop_all()


@pytest.fixture(scope='session', autouse=True)
def random_notes() -> list[SleepNoteCompute]:
    return SleepDiaryGenerator.create_notes(1, 7)


@pytest.fixture(scope='session', autouse=True)
def random_sleep_diary(random_notes: list[SleepNoteCompute]) -> SleepDiaryModel:
    return SleepDiaryGenerator.build(notes=random_notes)


@pytest.fixture(scope='session', autouse=True)
def create_db_user(app):
    new_user = User()
    new_user.id = 1
    new_user.login = 'login',
    new_user.password = '123'

    with app.app_context():
        db.session.add(new_user)
        db.session.commit()


@pytest.fixture(scope='session', autouse=True)
def add_notes_to_db(app, create_db_user, random_notes: list[SleepNoteCompute]):
    new_notes = map(
        lambda random_note: Notation(
            **random_note.model_dump(
                by_alias=True,
                exclude={
                    "sleep_duration",
                    "time_spent_in_bed",
                    "sleep_efficiency"
                }
            )
        ),
        random_notes
    )
    with app.app_context():
        db.session.add_all(new_notes)
        db.session.commit()
