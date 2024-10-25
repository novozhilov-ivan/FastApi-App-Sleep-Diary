from functools import lru_cache

from punq import Container, Scope

from src.infrastructure.authorization.base import BaseTokenService
from src.infrastructure.authorization.jwt import JWTService
from src.infrastructure.database import Database
from src.infrastructure.repository import BaseDiaryRepository, ORMDiaryRepository
from src.infrastructure.repository.base import BaseUserRepository
from src.infrastructure.repository.orm_user import ORMUserRepository
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

    def init_diary_repository() -> ORMDiaryRepository:
        database = container.resolve(Database)
        return ORMDiaryRepository(database)

    def init_user_repository() -> BaseUserRepository:
        database = container.resolve(Database)
        return ORMUserRepository(database)

    def init_authentication_service() -> BaseUserAuthenticationService:
        repository = container.resolve(BaseUserRepository)
        return UserAuthenticationService(repository)

    def init_diary() -> Diary:
        repository = container.resolve(BaseDiaryRepository)
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
        BaseDiaryRepository,
        factory=init_diary_repository,
        scope=Scope.singleton,
    )
    container.register(
        BaseUserRepository,
        factory=init_user_repository,
        scope=Scope.singleton,
    )
    container.register(Diary, factory=init_diary, scope=Scope.singleton)
    container.register(
        BaseUserAuthenticationService,
        factory=init_authentication_service,
        scope=Scope.singleton,
    )

    return container
