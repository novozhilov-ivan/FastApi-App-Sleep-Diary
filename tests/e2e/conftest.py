from typing import ClassVar

import pytest

from fastapi import FastAPI
from pydantic_settings import SettingsConfigDict
from starlette.testclient import TestClient

from src.application.api.main import create_app
from src.infrastructure.database import Database, get_db
from src.infrastructure.orm import ORMUser, metadata
from src.infrastructure.repository import (
    BaseUserNotesRepository,
    ORMUserNotesRepository,
)
from src.settings import AuthJWTSettings


class TestSettings(AuthJWTSettings):
    PUBLIC_KEY: str
    PRIVATE_KEY: str
    POSTGRES_DB_URL: str = "sqlite:///db.sqlite"

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore",
    )


test_settings = TestSettings()


def _database() -> Database:
    return Database(test_settings.POSTGRES_DB_URL)


@pytest.fixture(scope="session")
def database() -> Database:
    return _database()


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_db] = _database
    return app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def memory_database(database: Database) -> Database:
    metadata.drop_all(database.engine)
    metadata.create_all(database.engine)
    return database


@pytest.fixture
def repository(database: Database, user: ORMUser) -> BaseUserNotesRepository:
    return ORMUserNotesRepository(user.oid, database)


@pytest.fixture
def user(memory_database: Database) -> ORMUser:
    user = ORMUser(
        username="test_user",
        password=b"test_password",
    )
    with memory_database.get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user
