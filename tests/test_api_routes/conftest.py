import pytest
from _pytest.fixtures import FixtureRequest
from flask import Flask
from flask.testing import FlaskClient
from pydantic_settings import SettingsConfigDict

from api import create_app, db
from api.config import Config
from api.models import Notation, User
from api.utils.auth import hash_password
from common.generators.diary import SleepDiaryGenerator
from common.pydantic_schemas.user import UserCredentials


class TestConfig(Config):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".test.env",
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


@pytest.fixture
def client(app) -> FlaskClient:
    with app.test_request_context():
        yield app.test_client()


@pytest.fixture(name="user_credentials")
def create_user_credentials() -> UserCredentials:
    yield UserCredentials(
        login="test_login",
        password="test_password".encode(),
    )


user_password_is_hashed = False
exist_db_user_indirect_params = (user_password_is_hashed,)
user_password_is_hashed_description = [
    f"User pwd is {'' if pwd_hashed else 'UN'}hashed"
    for pwd_hashed in exist_db_user_indirect_params
]


@pytest.fixture(
    name="exist_db_user",
    params=exist_db_user_indirect_params,
    ids=user_password_is_hashed_description,
)
def create_db_user(
    request: FixtureRequest,
    user_credentials: UserCredentials,
    client: FlaskClient,
) -> User:
    pwd_is_hashed: bool = request.param
    new_user = User(**user_credentials.model_dump(by_alias=True))
    if pwd_is_hashed:
        new_user.password = hash_password(user_credentials.password)
    with client.application.app_context():
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
    yield new_user


@pytest.fixture(name="db_user_id")
def read_id_of_exist_user(exist_db_user: User) -> int:
    yield exist_db_user.id


notes_count_for_db = [1, 5, 7, 8, 11, 14, 16, 21, 27, 30]


@pytest.fixture(
    params=notes_count_for_db,
    ids=[f"{amount} notes in db " for amount in notes_count_for_db],
)
def generated_diary(
    request: FixtureRequest,
    db_user_id: int,
    client: FlaskClient,
) -> SleepDiaryGenerator:
    notes_count = request.param
    return SleepDiaryGenerator(db_user_id, notes_count)


@pytest.fixture
def add_notes_to_db(
    client: FlaskClient,
    generated_diary: SleepDiaryGenerator,
) -> None:
    new_notes = generated_diary.convert_model(
        Notation,
        exclude={
            "sleep_duration",
            "time_spent_in_bed",
            "sleep_efficiency",
        },
    )
    with client.application.app_context():
        db.session.add_all(new_notes)
        db.session.commit()


@pytest.fixture
def saved_diary(
    generated_diary: SleepDiaryGenerator,
    add_notes_to_db: None,
) -> SleepDiaryGenerator:
    return generated_diary
