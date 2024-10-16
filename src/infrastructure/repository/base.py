from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing_extensions import Self
from uuid import UUID

from src.domain.entities.note import NoteEntity


@dataclass
class BaseUserNotesRepository(ABC):
    owner_oid: UUID

    @abstractmethod
    def add(self: Self, note: NoteEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self: Self, oid: UUID) -> NoteEntity | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_bedtime_date(self: Self, bedtime_date: date) -> NoteEntity | None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self: Self) -> set[NoteEntity]:
        raise NotImplementedError
