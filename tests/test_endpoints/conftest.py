import pytest
from _pytest.fixtures import FixtureRequest
from flask import Flask

from pydantic_settings import SettingsConfigDict

from api import create_app, db
from api.models import Notation, User
from api.config import Config
from common.generators.diary import SleepDiaryGenerator


class TestConfig(Config):
    model_config = SettingsConfigDict(
        env_file=".test.env",
        extra="allow"
    )
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


@pytest.fixture(name='db_user_id')
def create_db_user(app: Flask) -> int:
    new_user = User()
    new_user.id = 1
    new_user.login = 'login'
    new_user.password = '123'
    app = app
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
def generated_diary(
        request: FixtureRequest,
        db_user_id: int,
        app: Flask
) -> SleepDiaryGenerator:
    notes_count = request.param
    return SleepDiaryGenerator(db_user_id, notes_count)


@pytest.fixture
def add_notes_to_db(app: Flask, generated_diary: SleepDiaryGenerator) -> None:
    new_notes = generated_diary.convert_model(
        Notation,
        exclude={"sleep_duration", "time_spent_in_bed", "sleep_efficiency"}
    )
    with app.app_context():
        db.session.add_all(new_notes)
        db.session.commit()


@pytest.fixture
def saved_diary(generated_diary: SleepDiaryGenerator, add_notes_to_db: None) -> SleepDiaryGenerator:
    return generated_diary
