from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, time, timedelta
from typing import TYPE_CHECKING
from uuid import UUID

from src.domain.sleep_diary.entities.note import NoteEntity
from src.domain.sleep_diary.entities.user import UserEntity

if TYPE_CHECKING:
    from src.domain.sleep_diary.values.points import Points


@dataclass
class IDurations(ABC):
    points: "Points"

    @property
    @abstractmethod
    def sleep(self) -> timedelta:
        raise NotImplementedError

    @property
    @abstractmethod
    def sleep_minus_without_sleep(self) -> timedelta:
        raise NotImplementedError

    @property
    @abstractmethod
    def in_bed(self) -> timedelta:
        raise NotImplementedError

    @property
    @abstractmethod
    def without_sleep(self) -> timedelta:
        raise NotImplementedError


@dataclass
class IStatistics(ABC):
    durations: IDurations

    @property
    @abstractmethod
    def sleep(self) -> time:
        raise NotImplementedError

    @property
    @abstractmethod
    def in_bed(self) -> time:
        raise NotImplementedError

    @property
    @abstractmethod
    def sleep_minus_no_sleep(self) -> time:
        raise NotImplementedError

    @property
    @abstractmethod
    def sleep_efficiency(self) -> float:
        raise NotImplementedError


@dataclass
class INotesRepository(ABC):
    @abstractmethod
    def add(self, note: NoteEntity) -> None:
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


@dataclass
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
