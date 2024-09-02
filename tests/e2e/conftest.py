from typing import ClassVar, Generator

import pytest

from flask import Blueprint, Flask
from flask.testing import FlaskClient
from pydantic_core import MultiHostUrl
from pydantic_settings import SettingsConfigDict

from src.application.api.api import init_api_blueprint
from src.infrastructure.database import Database
from src.infrastructure.orm import ORMUser, metadata
from src.settings import AuthJWTSettings, FlaskSettings


class TestSettings(FlaskSettings, AuthJWTSettings):
    TESTING: bool = True
    SECRET_KEY: str = "secret"
    PUBLIC_KEY: str = "secret"
    PRIVATE_KEY: str = "super_secret"
    POSTGRES_DB_URL: str | MultiHostUrl = "sqlite:///db.sqlite"

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore",
    )


@pytest.fixture(scope="session")
def api_bp() -> Blueprint:
    return init_api_blueprint()


@pytest.fixture(scope="session")
def app(api_bp: Blueprint) -> Flask:
    app = Flask("test_app")
    app.config.from_object(obj=TestSettings())
    app.register_blueprint(
        blueprint=api_bp,
        url_prefix="/api",
    )
    assert (db_url := app.config.get("POSTGRES_DB_URL"))
    assert "sqlite" in db_url
    assert app.config.get("TESTING")
    return app


@pytest.fixture
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    with app.test_request_context(), app.app_context():
        yield app.test_client()


@pytest.fixture(scope="session")
def database(app: Flask) -> Database:
    db = Database(app.config.get("POSTGRES_DB_URL"))
    assert db
    return db


@pytest.fixture
def restart_database(database: Database) -> Database:
    metadata.drop_all(database.engine)
    metadata.create_all(database.engine)
    return database


@pytest.fixture
def user(restart_database: Database) -> ORMUser:
    user = ORMUser(
        username="test_user",
        password=b"test_password",
    )
    with restart_database.get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user
