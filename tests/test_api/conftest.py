import pytest
from _pytest.fixtures import FixtureRequest
from flask import Flask
from flask.testing import FlaskClient
from pydantic_settings import SettingsConfigDict
from werkzeug.datastructures import Authorization

from api import create_app, db
from api.config import Config
from api.extension import bearer
from api.models import DreamNote, User
from api.utils.auth import hash_password
from api.utils.jwt import create_access_jwt
from common.generators.diary import SleepDiaryGenerator
from common.pydantic_schemas.user import UserCredentials, UserValidate


class TestConfig(Config):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".test.env",
    )
    TESTING: bool


test_configuration = TestConfig()


# TODO оптимизировать фикстуры,
#  распределить фикстуры по файлам,
#  оптимизировать scope'ы.

# TODO оптимизировать тесты,
#  передавать пользователя через header в token'е.

# TODO Зарефакторить тесты в соответствии с актуальной работой кода в роутах.

# @pytest.fixture(scope='module')
# def test_client():
#     app = create_app()
#     with app.test_client() as testing_client:
#         with app.app_context():
#             yield testing_client


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
def user_credentials() -> UserCredentials:
    yield UserCredentials(
        username="test_username",
        password="test_password".encode(),
    )


user_password_is_hashed = True
exist_db_user_indirect_params = (user_password_is_hashed,)
user_password_is_hashed_description = [
    f"User pwd is {'' if pwd_hashed else 'UN'}hashed"
    for pwd_hashed in exist_db_user_indirect_params
]


@pytest.fixture(
    params=exist_db_user_indirect_params,
    ids=user_password_is_hashed_description,
)
def exist_db_user(
    request: FixtureRequest,
    user_credentials: UserCredentials,
    client: FlaskClient,
) -> User:
    pwd_is_hashed: bool = request.param
    new_user = User(**user_credentials.model_dump())
    if pwd_is_hashed:
        new_user.password = hash_password(user_credentials.password)
    with client.application.app_context():
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
    yield new_user


@pytest.fixture
def auth_token(exist_db_user: User) -> Authorization:
    user = UserValidate.model_validate(exist_db_user)
    yield Authorization(
        auth_type=bearer,
        token=create_access_jwt(user),
    )


@pytest.fixture
def exist_user_id(exist_db_user: User) -> int:
    yield exist_db_user.id


notes_count_for_db = [1, 5, 7, 8, 11, 14, 16, 21, 27, 30]


@pytest.fixture(
    params=notes_count_for_db,
    ids=[f"{amount} notes in db " for amount in notes_count_for_db],
)
def generated_diary(
    request: FixtureRequest,
    exist_user_id: int,
    client: FlaskClient,
) -> SleepDiaryGenerator:
    notes_count = request.param
    return SleepDiaryGenerator(
        user_id=exist_user_id,
        notes_count=notes_count,
    )


@pytest.fixture
def add_notes_to_db(
    client: FlaskClient,
    generated_diary: SleepDiaryGenerator,
) -> None:
    new_notes = generated_diary.convert_model(
        DreamNote,
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
