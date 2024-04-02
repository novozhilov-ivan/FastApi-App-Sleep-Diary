import json

import pytest

from pydantic_settings import SettingsConfigDict

from sleep_diary_api import create_app, db
from sleep_diary_api.Models import Notation, User
from sleep_diary_api.config import Config
from src.generators.sleep_diary import SleepDiaryGenerator
from src.pydantic_schemas.notes.sleep_diary import SleepDiaryModel


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


@pytest.fixture
def app():
    assert test_configuration.TESTING is True
    assert test_configuration.DB_NAME == "test_db"

    app = create_app()
    app.config.from_object(test_configuration)
    with app.app_context():
        db.drop_all()
    with app.app_context():
        db.create_all()
    yield app


@pytest.fixture(name='db_user_id')
def create_db_user(app) -> int:
    new_user = User()
    new_user.id = 1
    new_user.login = 'login'
    new_user.password = '123'
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
    yield new_user.id


notes_count_for_db = [1, 5, 7, 8, 11, 14, 16, 21, 27, 30]


@pytest.fixture(
    params=notes_count_for_db,
    ids=[f"{i} notes in db " for i in notes_count_for_db]
)
def generate_notes(request, db_user_id) -> SleepDiaryGenerator:
    notes_count = request.param
    return SleepDiaryGenerator(db_user_id, notes_count)


@pytest.fixture
def add_notes_to_db(app, generate_notes: SleepDiaryGenerator):
    new_notes = []
    for note in generate_notes.notes:
        note_model_dump = note.model_dump(
            by_alias=True,
            exclude={
                "sleep_duration",
                "time_spent_in_bed",
                "sleep_efficiency"
            }
        )
        new_notes.append(Notation(**note_model_dump))
    with app.app_context():
        db.session.add_all(new_notes)
        db.session.commit()


@pytest.fixture
def random_sleep_diary(generate_notes: SleepDiaryGenerator, add_notes_to_db) -> SleepDiaryModel:
    return generate_notes.diary
