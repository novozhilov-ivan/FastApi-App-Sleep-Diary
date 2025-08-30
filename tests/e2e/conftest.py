import pytest

from dishka import Container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.application.api.identity.api.handlers.schemas import SignInRequestSchema
from src.domain.identity.entities import AccessTokenClaims
from src.domain.identity.jwt_processor import JWTProcessor
from src.domain.identity.types import JWTToken
from src.domain.sleep_diary.entities.user import UserEntity
from src.gateways.postgresql.database import Database
from src.infra.identity.access_token_processor import AccessTokenProcessor
from src.infra.identity.authentication import (
    UserAuthenticationService,
)
from src.infra.identity.commands import SignInInputData
from src.infra.identity.sign_in import SignIn
from src.infra.sleep_diary.repository.orm_user import ORMUsersRepository
from src.main import create_app
from src.project.settings import AuthorizationTokenSettings, JWTSettings


@pytest.fixture(scope="session")
def api_user() -> UserEntity:
    return UserEntity(
        username="api_test_user",
        password="api_test_password",
    )


@pytest.fixture(scope="session")
def app(test_container: Container) -> FastAPI:
    app = create_app()
    setup_dishka(test_container, app)
    return app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def auth_settings() -> AuthorizationTokenSettings:
    return AuthorizationTokenSettings()


@pytest.fixture(scope="session")
def jwt_settings() -> JWTSettings:
    return JWTSettings()


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
def sign_in(
    jwt_settings: JWTSettings,
    user_auth_service: UserAuthenticationService,
) -> SignIn:
    return SignIn(
        settings=jwt_settings,
        service=user_auth_service,
    )


@pytest.fixture(scope="session")
def api_user_hashed_password(
    user_auth_service: UserAuthenticationService,
    api_user: UserEntity,
) -> str:
    return user_auth_service.hash_password(api_user.password)


@pytest.fixture(scope="session")
def jwt_processor(jwt_settings: JWTSettings) -> JWTProcessor:
    return JWTProcessor(jwt_settings=jwt_settings)


@pytest.fixture(scope="session")
def token_processor(jwt_processor: JWTProcessor) -> AccessTokenProcessor:
    return AccessTokenProcessor(jwt_processor=jwt_processor)


@pytest.fixture
def register_user(
    api_user: UserEntity,
    api_user_hashed_password: str,
    orm_user_repository: ORMUsersRepository,
) -> None:
    orm_user_repository.add_user(
        UserEntity(
            oid=api_user.oid,
            username=api_user.username,
            password=api_user_hashed_password,
        )
    )


@pytest.fixture
def access_token_claims(
    auth_credentials: dict[str, str],
    sign_in: SignIn,
    register_user: None,
) -> AccessTokenClaims:
    return sign_in(
        command=SignInInputData(**auth_credentials),
    )


@pytest.fixture
def jwt_token(
    token_processor: AccessTokenProcessor,
    access_token_claims: AccessTokenClaims,
) -> JWTToken:
    return token_processor.encode(access_token_claims)


@pytest.fixture
def authorized_client(
    client: TestClient,
    auth_settings: AuthorizationTokenSettings,
    jwt_token: JWTToken,
    register_user: None,
) -> TestClient:
    client.cookies.set(
        name=auth_settings.cookies_key,
        value=jwt_token,
    )

    assert client.cookies.get(auth_settings.cookies_key) == jwt_token
    return client
