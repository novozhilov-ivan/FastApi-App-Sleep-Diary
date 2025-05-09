from functools import lru_cache

from punq import Container, Scope

from src.sleep_diary.config.settings import Settings
from src.sleep_diary.domain.services import INotesRepository, IUsersRepository
from src.sleep_diary.infrastructure.database import Database
from src.sleep_diary.infrastructure.repository import (
    ORMNotesRepository,
    ORMUsersRepository,
)


@lru_cache(1)
def get_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    from src.sleep_diary.application.services import (
        Diary,
        IJWTService,
        IUserAuthenticationService,
        IUserJWTAuthorizationService,
        JWTService,
        UserAuthenticationService,
        UserJWTAuthorizationService,
    )

    container = Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)

    def init_database() -> Database:
        settings = container.resolve(Settings)
        return Database(url=settings.postgres_db_url)

    def init_notes_repository() -> INotesRepository:
        database = container.resolve(Database)
        return ORMNotesRepository(database)

    def init_users_repository() -> IUsersRepository:
        database = container.resolve(Database)
        return ORMUsersRepository(database)

    def init_authentication_service() -> IUserAuthenticationService:
        repository = container.resolve(IUsersRepository)
        return UserAuthenticationService(repository)

    def init_jwt_service() -> IJWTService:
        settings = container.resolve(Settings)
        return JWTService(settings)

    def init_user_jwt_authorization_service() -> IUserJWTAuthorizationService:
        jwt_service = container.resolve(IJWTService)
        return UserJWTAuthorizationService(jwt_service)

    def init_diary_service() -> Diary:
        repository = container.resolve(INotesRepository)
        return Diary(repository)

    container.register(
        Database,
        factory=init_database,
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
    container.register(IJWTService, factory=init_jwt_service, scope=Scope.singleton)
    container.register(
        IUserJWTAuthorizationService,
        factory=init_user_jwt_authorization_service,
        scope=Scope.transient,
    )

    return container
