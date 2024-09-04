import abc

from typing import Collection
from typing_extensions import Self
from uuid import UUID

from src.domain.diary import Diary
from src.domain.note import NoteEntity, NoteTimePoints, NoteValueObject


class IDiaryRepository(abc.ABC):
    @abc.abstractmethod
    def add(self: Self, note: NoteTimePoints, owner_oid: UUID) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self: Self, oid: UUID) -> NoteEntity | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_bedtime_date(
        self: Self,
        bedtime_date: str,
        owner_oid: UUID,
    ) -> NoteEntity | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_diary(self: Self, owner_oid: UUID) -> Diary:
        raise NotImplementedError


class BaseDiaryRepository(IDiaryRepository, abc.ABC):
    @abc.abstractmethod
    def _add(self: Self, note: NoteValueObject, owner_oid: UUID) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self: Self, oid: UUID) -> object | None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_bedtime_date(
        self: Self,
        bedtime_date: str,
        owner_oid: UUID,
    ) -> object | None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_diary(self: Self, owner_oid: UUID) -> Collection:
        raise NotImplementedError

    def add(self: Self, note: NoteTimePoints, owner_oid: UUID) -> None:
        self._add(NoteValueObject.model_validate(note), owner_oid)

    def get(self: Self, oid: UUID) -> NoteEntity | None:
        return NoteEntity.model_validate(self._get(oid))

    def get_by_bedtime_date(
        self: Self,
        bedtime_date: str,
        owner_oid: UUID,
    ) -> NoteEntity | None:
        return NoteEntity.model_validate(
            obj=self._get_by_bedtime_date(bedtime_date, owner_oid),
        )

    def get_diary(self: Self, owner_oid: UUID) -> Diary:
        diary = Diary()
        diary_notes = self._get_diary(owner_oid)
        diary._notes = {
            NoteValueObject.model_validate(note)
            for note in diary_notes
            if diary_notes
        }
        return diary

    # def add_all(self, note):
    # def update(self):
    # def delete(self, oid):
    # def delete_all(self):
