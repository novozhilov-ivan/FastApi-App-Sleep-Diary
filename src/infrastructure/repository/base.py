from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Sequence
from typing_extensions import Self
from uuid import UUID

from src.domain.entities.note import NoteEntity
from src.infrastructure.orm import ORMNote


@dataclass
class INoteRepository(ABC):
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
    def get_all(self: Self, owner_oid: UUID) -> set[NoteEntity]:
        raise NotImplementedError


@dataclass
class BaseNoteRepository(INoteRepository, ABC):
    @abstractmethod
    def _add(self: Self, note: NoteEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    def _get(self: Self, oid: UUID) -> ORMNote | None:
        raise NotImplementedError

    @abstractmethod
    def _get_by_bedtime_date(
        self: Self,
        bedtime_date: date,
        owner_oid: UUID,
    ) -> ORMNote | None:
        raise NotImplementedError

    @abstractmethod
    def _get_all(self: Self, owner_oid: UUID) -> Sequence[ORMNote]:
        raise NotImplementedError

    def add(self: Self, note: NoteEntity) -> None:
        self._add(note)

    def get(self: Self, oid: UUID) -> NoteEntity | None:
        note = self._get(oid)
        if isinstance(note, ORMNote):
            return note.to_entity()
        return None

    def get_by_bedtime_date(
        self: Self,
        bedtime_date: date,
        owner_oid: UUID,
    ) -> NoteEntity | None:
        note = self._get_by_bedtime_date(bedtime_date, owner_oid)
        if isinstance(note, ORMNote):
            return note.to_entity()
        return None

    def get_all(self: Self, owner_oid: UUID) -> set[NoteEntity]:
        return {note.to_entity() for note in self._get_all(owner_oid)}


@dataclass
class IUserRepository(ABC):
    pass
