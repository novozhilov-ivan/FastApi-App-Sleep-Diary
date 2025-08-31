from typing import ClassVar

from dishka import Provider, Scope, WithParents, provide

from src.application.api.sleep_diary.services.diary import Diary
from src.infra.sleep_diary.repository.orm_notes import ORMNotesRepository
from src.infra.sleep_diary.repository.orm_user import ORMUsersRepository


class InfraSleepDiaryProvider(Provider):
    scope: ClassVar[Scope] = Scope.APP

    user_repo = provide(ORMUsersRepository, provides=WithParents[ORMUsersRepository])
    notes_repo = provide(ORMNotesRepository, provides=WithParents[ORMNotesRepository])
    diary = provide(Diary)
