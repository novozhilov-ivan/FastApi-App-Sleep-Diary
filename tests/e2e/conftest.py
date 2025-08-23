from collections.abc import Generator
from uuid import uuid4

import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.application.api.identity.api.handlers.schemas import SignInRequestSchema
from src.domain.sleep_diary.entities.user import UserEntity
from src.gateways.postgresql.database import Database
from src.infra.identity.authentication import (
    UserAuthenticationService,
)
from src.infra.sleep_diary.repository.orm_user import ORMUsersRepository
from src.main import create_app
from src.project.settings import AuthorizationTokenSettings


@pytest.fixture(scope="session")
def api_user() -> UserEntity:
    return UserEntity(
        oid=uuid4(),
        username="api_test_user",
        password="api_test_password",
    )


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return create_app()


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def auth_settings() -> AuthorizationTokenSettings:
    return AuthorizationTokenSettings()


@pytest.fixture(scope="session")
def auth_credentials(api_user: UserEntity) -> dict[str, str]:
    return SignInRequestSchema(
        username=api_user.username,
        password=api_user.password,
    ).model_dump()


@pytest.fixture(scope="session")
def orm_user_repository(database: Database) -> ORMUsersRepository:
    return ORMUsersRepository(
        database=database,
    )


@pytest.fixture(scope="session")
def user_auth_service(
    orm_user_repository: ORMUsersRepository,
) -> UserAuthenticationService:
    return UserAuthenticationService(
        repository=orm_user_repository,
    )


@pytest.fixture(scope="session")
def register_user(
    api_user: UserEntity,
    user_auth_service: UserAuthenticationService,
) -> Generator[None]:

    user_auth_service.register(
        username=api_user.username,
        password=api_user.password,
    )

    try:
        yield
    finally:
        user_auth_service.unregister(username=api_user.username)


@pytest.fixture(scope="session")
def authorized_client(
    app: FastAPI,
    client: TestClient,
    auth_credentials: dict[str, str],
    auth_settings: AuthorizationTokenSettings,
    register_user: None,
) -> TestClient:
    url = app.url_path_for("sign_in")
    client.post(url=url, data=auth_credentials)

    assert client.cookies.get(auth_settings.cookies_key)
    return client
