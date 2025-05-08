from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, time, timedelta
from typing import Self, TYPE_CHECKING
from uuid import UUID

from src.domain.entities import NoteEntity, UserEntity


if TYPE_CHECKING:
    from src.domain.values.points import Points


@dataclass
class IDurations(ABC):
    points: "Points"

    @property
    @abstractmethod
    def sleep(self: Self) -> timedelta:
        raise NotImplementedError

    @property
    @abstractmethod
    def sleep_minus_without_sleep(self: Self) -> timedelta:
        raise NotImplementedError

    @property
    @abstractmethod
    def in_bed(self: Self) -> timedelta:
        raise NotImplementedError

    @property
    @abstractmethod
    def without_sleep(self: Self) -> timedelta:
        raise NotImplementedError


@dataclass
class IStatistics(ABC):
    durations: IDurations

    @property
    @abstractmethod
    def sleep(self: Self) -> time:
        raise NotImplementedError

    @property
    @abstractmethod
    def in_bed(self: Self) -> time:
        raise NotImplementedError

    @property
    @abstractmethod
    def sleep_minus_no_sleep(self: Self) -> time:
        raise NotImplementedError

    @property
    @abstractmethod
    def sleep_efficiency(self: Self) -> float:
        raise NotImplementedError


@dataclass
class INotesRepository(ABC):
    @abstractmethod
    def add(self: Self, note: NoteEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_oid(self: Self, oid: UUID) -> NoteEntity | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_bedtime_date(
        self: Self,
        bedtime_date: date,
        owner_oid: UUID,
    ) -> NoteEntity | None:
        raise NotImplementedError

    @abstractmethod
    def get_all_notes(self: Self, owner_oid: UUID) -> set[NoteEntity]:
        raise NotImplementedError


@dataclass
class IUsersRepository(ABC):
    @abstractmethod
    def get_by_username(self: Self, username: str) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    def add_user(self: Self, user: UserEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_user(self: Self, username: str) -> None:
        raise NotImplementedError
