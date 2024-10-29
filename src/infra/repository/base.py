from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing_extensions import Self
from uuid import UUID

from src.domain.entities import NoteEntity, UserEntity


@dataclass
class INotesRepository(ABC):
    @abstractmethod
    def add(self: Self, note: NoteEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self: Self, oid: UUID) -> NoteEntity | None:
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
    def add_user(self: Self, username: str, password: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_user(self: Self, username: str) -> None:
        raise NotImplementedError
