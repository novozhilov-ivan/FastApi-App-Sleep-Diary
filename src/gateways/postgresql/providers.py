from typing import ClassVar

from dishka import provide, Provider, Scope

from src.gateways.postgresql.database import Database
from src.project.settings import Config


class DatabaseProvider(Provider):
    scope: ClassVar[Scope] = Scope.APP

    @provide
    def get_database(self, config: Config) -> Database:
        return Database(url=config.postgresql.db_url)


class TestDatabaseProvider(Provider):
    scope: ClassVar[Scope] = Scope.APP

    @provide
    def get_database(self, config: Config) -> Database:
        return Database(url=config.postgresql.test_url)
