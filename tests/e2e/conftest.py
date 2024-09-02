from typing import Generator

import pytest

from flask import Blueprint, Flask
from flask.testing import FlaskClient

from src.application.api.api import init_api_blueprint
from src.infrastructure.database import Database
from src.infrastructure.orm import ORMUser, metadata
from src.settings import Settings


class TestSettings(Settings):
    TESTING: bool = True
    PUBLIC_KEY: str = "secret"
    PRIVATE_KEY: str = "super_secret"
    SECRET_KEY: str = "secret"


settings = TestSettings()


@pytest.fixture(scope="session")
def api_bp() -> Blueprint:
    return init_api_blueprint()


@pytest.fixture(scope="session")
def app(api_bp: Blueprint) -> Flask:
    app = Flask("test_app")
    app.config.from_object(obj=settings)
    app.register_blueprint(
        blueprint=api_bp,
        url_prefix="/api",
    )
    assert app.config.get("TESTING")
    return app


@pytest.fixture
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    with app.test_request_context(), app.app_context():
        yield app.test_client()


@pytest.fixture
def database() -> Database:
    db = Database(settings.POSTGRES_DB_URL)
    metadata.drop_all(db.engine)
    metadata.create_all(db.engine)
    return db


@pytest.fixture
def user(database: Database) -> ORMUser:
    user = ORMUser(
        username="test_user",
        password=b"test_password",
    )
    with database.get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user
