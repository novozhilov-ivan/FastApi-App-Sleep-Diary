from typing import Generator

import pytest

from _pytest.fixtures import FixtureRequest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.datastructures import Authorization

from src.extension import (
    bearer,
    db,
)
from src.flask_app import create_app
from src.models import (
    SleepNoteOrm,
    UserOrm,
)
from src.pydantic_schemas.sleep.notes import SleepNoteWithMeta
from src.pydantic_schemas.user import (
    UserCredentials,
    UserValidate,
)
from src.utils.auth import hash_password
from src.utils.jwt import (
    create_access_jwt,
    create_refresh_jwt,
)
from tests.api_test.config import (
    test_flask_config,
    test_flask_sqlalchemy_config,
)
from tests.generators.diary import SleepDiaryGenerator


# @pytest.fixture(scope="session")
# def test_engine() -> Generator[Engine, None, None]:
#     yield create_engine(**test_sqlalchemy_config.engine_options)


@pytest.fixture(scope="session")
def app() -> Generator[Flask, None, None]:
    app = create_app()
    app.config.from_object(obj=test_flask_config)
    app.config.from_object(obj=test_flask_sqlalchemy_config)
    assert app.config.get("TESTING")
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI")
    assert db_uri
    *_, db_name_in_config = db_uri.split("/")
    assert db_name_in_config == "test_db"
    yield app


@pytest.fixture(scope="session")
def user_credentials() -> Generator[UserCredentials, None, None]:
    yield UserCredentials(
        username="test_username",
        password="test_password".encode(),
    )


@pytest.fixture(scope="session")
def user_hashed_password(
    user_credentials: UserCredentials,
) -> Generator[str, None, None]:
    yield hash_password(pwd_bytes=user_credentials.password)


@pytest.fixture(scope="session")
def user(user_credentials: UserCredentials) -> Generator[UserValidate, None, None]:
    yield UserValidate(
        id=1,
        username=user_credentials.username,
        password=user_credentials.password,
    )


@pytest.fixture(scope="session")
def jwt_access(user: UserValidate) -> Generator[Authorization, None, None]:
    yield Authorization(
        auth_type=bearer,
        token=create_access_jwt(user),
    )


@pytest.fixture(scope="session")
def jwt_refresh(user: UserValidate) -> Generator[Authorization, None, None]:
    yield Authorization(
        auth_type=bearer,
        token=create_refresh_jwt(user),
    )


@pytest.fixture
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    with app.test_request_context(), app.app_context():
        yield app.test_client()


# @pytest.fixture(autouse=True)
# def create_db(
#     test_engine: Engine,
# ) -> None:
#     Base.metadata.drop_all(bind=test_engine)
#     Base.metadata.create_all(bind=test_engine)


@pytest.fixture(autouse=True)
def create_db(client: FlaskClient) -> None:
    with client.application.app_context():
        db.drop_all()
        db.create_all()


@pytest.fixture
def exist_user(
    user: UserValidate,
    user_hashed_password: str,
    client: FlaskClient,
) -> Generator[UserOrm, None, None]:
    new_user = UserOrm(
        id=user.id,
        username=user.username,
        password=user_hashed_password,
    )
    with client.application.app_context():
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
    yield new_user


notes_count_for_db = [1, 5, 7, 8, 11, 14, 16, 21, 27, 30]


@pytest.fixture(
    params=notes_count_for_db,
    ids=[f"{amount} notes in db " for amount in notes_count_for_db],
)
def generated_diary(
    request: FixtureRequest,
    exist_user: UserOrm,
    client: FlaskClient,
) -> SleepDiaryGenerator:
    notes_count = request.param
    return SleepDiaryGenerator(
        owner_id=exist_user.id,
        notes_count=notes_count,
    )


@pytest.fixture
def add_notes_to_db(
    client: FlaskClient,
    generated_diary: SleepDiaryGenerator,
) -> None:
    include_fields: set[str] = set(SleepNoteWithMeta.model_fields)
    new_notes = [
        SleepNoteOrm(**note.model_dump(include=include_fields))
        for note in generated_diary.notes
    ]
    with client.application.app_context():
        db.session.add_all(new_notes)
        db.session.commit()


@pytest.fixture
def saved_diary(
    generated_diary: SleepDiaryGenerator,
    add_notes_to_db: None,
) -> SleepDiaryGenerator:
    return generated_diary
