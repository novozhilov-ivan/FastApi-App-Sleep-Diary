import contextlib

from dataclasses import dataclass, field
from typing import Generator
from typing_extensions import Self
from uuid import UUID, uuid4

import pytest

from src import service_layer
from src.domain.diary import Diary
from src.infrastructure.orm import ORMNote
from src.infrastructure.repository import IDiaryRepository


class FakeORMError(Exception):
    pass


class FakeDatabase:
    committed: bool = False
    _session: set = set()

    def __commit(self: Self) -> None:
        self.committed = True

    @contextlib.contextmanager
    def get_session(self: Self) -> Generator[set, None, None]:
        try:
            yield self._session
        except FakeORMError:
            ...
        else:
            self.__commit()
        finally:
            ...


@dataclass
class FakeDiaryRepo(IDiaryRepository):
    database: FakeDatabase
    notes: set[ORMNote] = field(default_factory=lambda: set())

    def add(self: Self, note: ORMNote) -> None:  # not used, not tested
        self.notes.add(note)

    def get(self: Self, oid: UUID) -> ORMNote | None:  # not used, not tested
        return next(n for n in self.notes if n.oid == oid)

    def get_by_bedtime_date(
        self: Self,
        bedtime_date: str,
        owner_id: UUID,
    ) -> ORMNote | None:
        # 'str(n.bedtime_date)' - str(...) тут как заглушка. нужно переделать
        return next(
            n
            for n in self.notes
            if (str(n.bedtime_date) == bedtime_date and n.owner_id == owner_id)
        )

    def get_diary(self: Self, owner_id: UUID) -> Diary:  # used, not tested
        diary = Diary()
        diary._notes = {n for n in self.notes if n.owner_id == owner_id}
        return diary


@pytest.mark.parametrize(
    "no_sleep",
    [
        None,
        "",
        "00:00",
        "00:22",
    ],
)
def test_service_write_note(no_sleep: str | None) -> None:
    fake_owner_id = uuid4()
    database = FakeDatabase()
    repo = FakeDiaryRepo(database)
    service_layer.write(
        "2020-12-12",
        "13:00",
        "15:00",
        "23:00",
        "01:00",
        no_sleep,
        fake_owner_id,
        repo,
    )
    retrieved = repo.get_by_bedtime_date("2020-12-12", fake_owner_id)
    assert retrieved is not None
    assert isinstance(retrieved, ORMNote)
    assert database.committed
