from typing import ClassVar

from dishka import Provider, Scope, provide

from src.application.api.sleep_diary.services.diary import Diary
from src.domain.sleep_diary.services.base import INotesRepository, IUsersRepository
from src.gateways.postgresql.database import Database
from src.infra.sleep_diary.repository.orm_notes import ORMNotesRepository
from src.infra.sleep_diary.repository.orm_user import ORMUsersRepository


class InfraSleepDiaryProvider(Provider):
    scope: ClassVar[Scope] = Scope.APP

    @provide
    def get_users_repository(self, database: Database) -> IUsersRepository:
        return ORMUsersRepository(database=database)

    @provide
    def get_notes_repository(self, database: Database) -> INotesRepository:
        return ORMNotesRepository(database=database)

    @provide
    def get_diary(self, repository: INotesRepository) -> Diary:
        return Diary(repository=repository)
