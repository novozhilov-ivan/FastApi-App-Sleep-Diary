from dataclasses import dataclass
from typing_extensions import Self

import pytest

from src.domain.entities import UserEntity
from src.domain.services import INotesRepository, IUsersRepository
from src.domain.values.points import Points
from src.infra.repository import MemoryNotesRepository, MemoryUsersRepository
from src.project.settings import AuthJWTSettings
from src.service_layer.entities import (
    IPayload,
    TokenType,
    UserPayload,
)
from src.service_layer.services import (
    Diary,
    IUserAuthenticationService,
    UserAuthenticationService,
    UserJWTAuthorizationService,
)
from src.service_layer.services.base import IJWTService, IUserJWTAuthorizationService
from src.service_layer.services.jwt import JWTService


@dataclass(frozen=True)
class FakePoints(Points):
    def validate(self: Self) -> None: ...


@dataclass
class DummyPayload(IPayload):
    hello: str

    def convert_to_dict(self: Self) -> dict:
        return {"hello": self.hello}


@pytest.fixture(scope="session")
def created_user() -> UserEntity:
    return UserEntity(username="correct_username", password="correct_password")


@pytest.fixture(scope="session")
def created_user_with_hashed_password(created_user: UserEntity) -> UserEntity:
    return UserEntity(
        username=created_user.username,
        password=UserAuthenticationService.hash_password(created_user.password),
    )


@pytest.fixture
def user_repository() -> IUsersRepository:
    return MemoryUsersRepository()


@pytest.fixture
def authentication_service(
    user_repository: IUsersRepository,
) -> IUserAuthenticationService:
    return UserAuthenticationService(user_repository)


@pytest.fixture
def notes_repository() -> INotesRepository:
    return MemoryNotesRepository()


@pytest.fixture
def diary(notes_repository: INotesRepository) -> Diary:
    return Diary(notes_repository)


@pytest.fixture(scope="session")
def auth_settings() -> AuthJWTSettings:
    return AuthJWTSettings()


@pytest.fixture(scope="session")
def jwt_service(auth_settings: AuthJWTSettings) -> IJWTService:
    return JWTService(auth_settings)


@pytest.fixture(scope="session")
def created_user_jwt_payload(created_user: UserEntity) -> IPayload:
    return UserPayload(str(created_user.oid), created_user.username)


@pytest.fixture(scope="session")
def created_user_access_jwt(
    jwt_service: IJWTService,
    created_user_jwt_payload: IPayload,
) -> str:

    return jwt_service.create_jwt(TokenType.ACCESS, created_user_jwt_payload)


@pytest.fixture(scope="session")
def created_user_jwt_refresh(
    jwt_service: IJWTService,
    created_user_jwt_payload: IPayload,
) -> str:
    return jwt_service.create_jwt(TokenType.REFRESH, created_user_jwt_payload)


@pytest.fixture(scope="session")
def user_jwt_service_with_none_jwt(
    jwt_service: IJWTService,
) -> IUserJWTAuthorizationService:
    return UserJWTAuthorizationService(jwt_service)


@pytest.fixture(scope="session")
def user_jwt_service_with_user_jwt_access(
    jwt_service: IJWTService,
    created_user_access_jwt: str,
) -> IUserJWTAuthorizationService:
    return UserJWTAuthorizationService(jwt_service, created_user_access_jwt)


@pytest.fixture(scope="session")
def user_jwt_service_with_user_jwt_refresh(
    jwt_service: IJWTService,
    created_user_jwt_refresh: str,
) -> IUserJWTAuthorizationService:
    return UserJWTAuthorizationService(jwt_service, created_user_jwt_refresh)
