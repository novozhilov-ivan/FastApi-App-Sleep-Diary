import contextlib

from dataclasses import dataclass, field
from typing import Generator
from typing_extensions import Self
from uuid import UUID, uuid4

import pytest

from src import service_layer
from src.domain.diary import Diary
from src.domain.note import NoteValueObject
from src.infrastructure.orm import ORMNote
from src.infrastructure.repository import IDiaryRepository


class FakeORMError(Exception):
    pass


@dataclass
class FakeDatabase:
    committed: bool = False
    session: list[ORMNote] = field(default_factory=lambda: list())  # noqa: C408

    def commit(self: Self) -> None:
        self.committed = True

    @contextlib.contextmanager
    def get_session(self: Self) -> Generator[list[ORMNote], None, None]:
        try:
            yield self.session
        except FakeORMError:
            ...
        else:
            self.commit()
        finally:
            ...


@dataclass
class FakeDiaryRepo(IDiaryRepository):
    database: FakeDatabase

    def add(self: Self, note: ORMNote) -> None:  # used, not tested
        with self.database.get_session() as session:
            session.append(note)

    def get(self: Self, oid: UUID) -> ORMNote | None:  # not used, not tested
        with self.database.get_session() as session:
            return next(note for note in session if note.oid == oid)

    def get_by_bedtime_date(
        self: Self,
        bedtime_date: str,
        owner_id: UUID,
    ) -> ORMNote | None:
        # 'str(n.bedtime_date)' - str(...) тут как заглушка. нужно переделать
        with self.database.get_session() as session:
            return next(
                note
                for note in session
                if (
                    str(note.bedtime_date) == bedtime_date
                    and note.owner_id == owner_id
                )
            )

    def get_diary(self: Self, owner_id: UUID) -> Diary:  # used, not tested
        diary = Diary()
        with self.database.get_session() as session:
            notes = session
        diary._notes = {
            NoteValueObject.model_validate(
                obj=note,
                from_attributes=True,
            )
            for note in notes
            if notes and note.owner_id == owner_id
        }
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
def test_service_write_note(no_sleep: str | None):
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
