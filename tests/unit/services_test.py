import contextlib

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Generator
from typing_extensions import Self
from uuid import UUID, uuid4

import pytest

from src import service_layer
from src.domain.note import NoteEntity, NoteValueObject
from src.infrastructure.repository import BaseDiaryRepository


class FakeDatabaseError(Exception):
    pass


@dataclass
class FakeDatabase:
    committed: bool = False
    session: set[tuple[NoteValueObject, UUID]] = field(
        default_factory=lambda: set(),
    )  # noqa: C408

    def commit(self: Self) -> None:
        self.committed = True

    @contextlib.contextmanager
    def get_session(
        self: Self,
    ) -> Generator[set[tuple[NoteValueObject, UUID]], None, None]:
        try:
            yield self.session
        except FakeDatabaseError:
            ...
        else:
            self.commit()
        finally:
            ...


@dataclass
class FakeDiaryRepo(BaseDiaryRepository):
    database: FakeDatabase

    def _add(self: Self, note: NoteValueObject, owner_id: UUID) -> None:
        with self.database.get_session() as session:
            session.add((note, owner_id))

    def _get(self: Self, oid: UUID) -> None:
        raise NotImplementedError

    def _get_by_bedtime_date(
        self: Self,
        bedtime_date: str,
        owner_id: UUID,
    ) -> dict | None:
        # 'str(n.bedtime_date)' - str(...) тут как заглушка. нужно переделать
        with self.database.get_session() as session:
            for note, oid in session:
                if str(note.bedtime_date) == bedtime_date and oid == owner_id:
                    break
            return {
                **note.model_dump(),
                "oid": uuid4(),
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC),
            }

    def _get_diary(self: Self, owner_id: UUID) -> set:
        with self.database.get_session() as session:
            notes: set = set()
            for note_and_oid in session:
                note, oid = note_and_oid
                if oid == owner_id:
                    notes.add(note)
            return notes


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
    repo: BaseDiaryRepository = FakeDiaryRepo(database)
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
    assert isinstance(retrieved, NoteEntity)
    assert database.committed
