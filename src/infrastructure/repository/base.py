import abc

from typing_extensions import Self
from uuid import UUID

from src.domain.diary import Diary
from src.infrastructure.orm import ORMNote


class IDiaryRepository(abc.ABC):
    @abc.abstractmethod
    def add(self: Self, note: ORMNote) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self: Self, oid: UUID) -> ORMNote | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_bedtime_date(
        self: Self,
        bedtime_date: str,
        owner_id: UUID,
    ) -> ORMNote | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_diary(self: Self, owner_id: UUID) -> Diary:
        raise NotImplementedError

    # def add_all(self, note):
    # def update(self):
    # def delete(self, oid):
    # def delete_all(self):
