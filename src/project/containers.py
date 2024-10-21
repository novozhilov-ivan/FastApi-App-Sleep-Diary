from functools import lru_cache

from punq import Container, Scope

from src.infrastructure.database import Database
from src.infrastructure.repository import BaseDiaryRepository, ORMDiaryRepository
from src.project.settings import Settings
from src.service_layer import Diary


@lru_cache(1)
def get_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, Settings, scope=Scope.singleton)

    def init_database() -> Database:
        settings = container.resolve(Settings)
        return Database(url=settings.POSTGRES_DB_URL)

    def init_diary_repository() -> ORMDiaryRepository:
        database = container.resolve(Database)
        return ORMDiaryRepository(database)

    def init_diary() -> Diary:
        repository = container.resolve(BaseDiaryRepository)
        return Diary(repository)

    container.register(
        Database,
        scope=Scope.singleton,
        factory=init_database,
    )
    container.register(
        BaseDiaryRepository,
        factory=init_diary_repository,
        scope=Scope.singleton,
    )
    container.register(Diary, factory=init_diary, scope=Scope.singleton)

    return container
