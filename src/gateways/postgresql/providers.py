from typing import ClassVar

from dishka import Provider, Scope, provide

from src.gateways.postgresql.database import Database
from src.project.settings import PostgreSQLSettings


class DatabaseProvider(Provider):
    scope: ClassVar[Scope] = Scope.APP

    @provide
    def get_database(self, settings: PostgreSQLSettings) -> Database:
        return Database(url=settings.db_url)


class TestDatabaseProvider(Provider):
    scope: ClassVar[Scope] = Scope.APP

    @provide
    def get_database(self, settings: PostgreSQLSettings) -> Database:
        return Database(url=settings.test_url)
