from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from src.domain.sleep_diary.dtos import WeekInfo, WeekNotes
from src.domain.sleep_diary.entities.note import NoteEntity
from src.domain.sleep_diary.entities.user import UserEntity


class INotesRepository(ABC):
    @abstractmethod
    def add(self, note: NoteEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, note: NoteEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, note: NoteEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_oid(self, oid: UUID) -> NoteEntity | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_bedtime_date(
        self,
        bedtime_date: date,
        owner_oid: UUID,
    ) -> NoteEntity | None:
        raise NotImplementedError

    @abstractmethod
    def get_all_notes(self, owner_oid: UUID) -> set[NoteEntity]:
        raise NotImplementedError


class IUsersRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    def add_user(self, user: UserEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_user(self, username: str) -> None:
        raise NotImplementedError


class IWeeksRepository(ABC):
    @abstractmethod
    def get_weeks_info(self, owner_oid: UUID) -> list[WeekInfo]:
        raise NotImplementedError

    @abstractmethod
    def get_user_week_notes(self, owner_oid: UUID, start_date: date) -> WeekNotes:
        raise NotImplementedError
