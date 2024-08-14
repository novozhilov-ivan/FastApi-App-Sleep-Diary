import abc

from typing_extensions import Self

from src.domain.diary import Diary
from src.domain.note import NoteEntity, NoteTimePoints


class BaseDiaryRepository(abc.ABC):
    @abc.abstractmethod
    def add(self: Self, note: NoteTimePoints) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self: Self, oid: int) -> NoteEntity:
        raise NotImplementedError

    @abc.abstractmethod
    def get_diary(self: Self) -> Diary:
        raise NotImplementedError

    # def get_by_sleep_date(self, sleep_date):
    # def get_all(self):
    # def add_all(self, note):
    # def update(self):
    # def delete(self, oid):
    # def delete_all(self):
