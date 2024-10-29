from functools import lru_cache

from punq import Container, Scope

from src.infra.authorization.base import BaseTokenService
from src.infra.authorization.jwt import JWTService
from src.infra.database import Database
from src.infra.repository import (
    BaseNotesRepository,
    BaseUsersRepository,
    ORMNotesRepository,
    ORMUsersRepository,
)
from src.project.settings import Settings
from src.service_layer import Diary
from src.service_layer.services.base import BaseUserAuthenticationService
from src.service_layer.services.user import UserAuthenticationService


@lru_cache(1)
def get_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)

    def init_token_service() -> BaseTokenService:
        settings = container.resolve(Settings)
        return JWTService(settings)

    def init_database() -> Database:
        settings = container.resolve(Settings)
        return Database(url=settings.POSTGRES_DB_URL)

    def init_notes_repository() -> BaseNotesRepository:
        database = container.resolve(Database)
        return ORMNotesRepository(database)

    def init_users_repository() -> BaseUsersRepository:
        database = container.resolve(Database)
        return ORMUsersRepository(database)

    def init_authentication_service() -> BaseUserAuthenticationService:
        repository = container.resolve(BaseUsersRepository)
        return UserAuthenticationService(repository)

    def init_diary_service() -> Diary:
        repository = container.resolve(BaseNotesRepository)
        return Diary(repository)

    container.register(
        Database,
        factory=init_database,
        scope=Scope.singleton,
    )
    container.register(
        BaseTokenService,
        factory=init_token_service,
        scope=Scope.singleton,
    )
    container.register(
        BaseNotesRepository,
        factory=init_notes_repository,
        scope=Scope.singleton,
    )
    container.register(
        BaseUsersRepository,
        factory=init_users_repository,
        scope=Scope.singleton,
    )
    container.register(Diary, factory=init_diary_service, scope=Scope.singleton)
    container.register(
        BaseUserAuthenticationService,
        factory=init_authentication_service,
        scope=Scope.singleton,
    )

    return container
