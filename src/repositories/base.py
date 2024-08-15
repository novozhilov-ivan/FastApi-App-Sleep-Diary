import abc

from typing_extensions import Self
from uuid import UUID

from src.domain.diary import Diary
from src.domain.note import NoteEntity, NoteValueObject


class BaseDiaryRepository(abc.ABC):
    @abc.abstractmethod
    def add(self: Self, note: NoteValueObject) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self: Self, oid: UUID) -> NoteEntity:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_bedtime_date(self: Self, bedtime_date: str) -> NoteEntity:
        raise NotImplementedError

    @abc.abstractmethod
    def get_diary(self: Self) -> Diary:
        raise NotImplementedError

    # def add_all(self, note):
    # def update(self):
    # def delete(self, oid):
    # def delete_all(self):
