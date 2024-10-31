from functools import lru_cache

from punq import Container, Scope

from src.domain.services import INotesRepository, IUsersRepository
from src.infra.authorization import IUserTokenService, UserJWTService
from src.infra.database import Database
from src.infra.repository import (
    ORMNotesRepository,
    ORMUsersRepository,
)
from src.project.settings import Settings
from src.service_layer import Diary
from src.service_layer.services.authentication import (
    IUserAuthenticationService,
    UserAuthenticationService,
)


@lru_cache(1)
def get_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)

    def init_token_service() -> IUserTokenService:
        settings = container.resolve(Settings)
        return UserJWTService(settings)

    def init_database() -> Database:
        settings = container.resolve(Settings)
        return Database(url=settings.POSTGRES_DB_URL)

    def init_notes_repository() -> INotesRepository:
        database = container.resolve(Database)
        return ORMNotesRepository(database)

    def init_users_repository() -> IUsersRepository:
        database = container.resolve(Database)
        return ORMUsersRepository(database)

    def init_authentication_service() -> IUserAuthenticationService:
        repository = container.resolve(IUsersRepository)
        return UserAuthenticationService(repository)

    def init_diary_service() -> Diary:
        repository = container.resolve(INotesRepository)
        return Diary(repository)

    container.register(
        Database,
        factory=init_database,
        scope=Scope.singleton,
    )
    container.register(
        IUserTokenService,
        factory=init_token_service,
        scope=Scope.singleton,
    )
    container.register(
        INotesRepository,
        factory=init_notes_repository,
        scope=Scope.singleton,
    )
    container.register(
        IUsersRepository,
        factory=init_users_repository,
        scope=Scope.singleton,
    )
    container.register(Diary, factory=init_diary_service, scope=Scope.singleton)
    container.register(
        IUserAuthenticationService,
        factory=init_authentication_service,
        scope=Scope.transient,
    )

    return container
