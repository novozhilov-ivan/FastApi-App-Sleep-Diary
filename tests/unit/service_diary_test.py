from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import date, time
from typing import Generator
from typing_extensions import Self
from uuid import UUID, uuid4

import pytest

from src import service_layer
from src.domain.entities.note import NoteEntity
from src.domain.exceptions import NonUniqueNoteBedtimeDateException
from src.infrastructure.repository import BaseUserNotesRepository
from tests.unit.conftest import points_order_desc_from_went_to_bed


class FakeDatabaseError(Exception):
    pass


@dataclass
class FakeDatabase:
    committed: bool = False
    session: set[NoteEntity] = field(default_factory=set)

    def commit(self: Self) -> None:
        self.committed = True

    @contextmanager
    def get_session(
        self: Self,
    ) -> Generator[set[NoteEntity], None, None]:
        try:
            yield self.session
        except FakeDatabaseError:
            ...
        else:
            self.commit()


@dataclass
class FakeUserNotesRepository(BaseUserNotesRepository):
    database: FakeDatabase

    def add(self: Self, note: NoteEntity) -> None:
        with self.database.get_session() as session:
            session.add(note)

    def get(self: Self, oid: UUID) -> None:
        raise NotImplementedError

    def get_by_bedtime_date(self: Self, bedtime_date: date) -> NoteEntity | None:
        with self.database.get_session() as session:
            try:
                return next(
                    note
                    for note in session
                    if note.points.bedtime_date == bedtime_date
                )
            except StopIteration:
                return None

    def get_all(self: Self) -> set[NoteEntity]:
        with self.database.get_session() as session:
            return session


@pytest.mark.parametrize(
    "no_sleep",
    [
        None,
        time(),
        time(0, 22),
    ],
)
def test_service_diary_can_write_with_different_value_in_no_sleep(
    no_sleep: time | None,
):
    fake_owner_oid = uuid4()
    database = FakeDatabase()
    repository: BaseUserNotesRepository = FakeUserNotesRepository(
        database=database,
        owner_oid=fake_owner_oid,
    )
    diary = service_layer.Diary(repository=repository)
    points = (*points_order_desc_from_went_to_bed, no_sleep)

    diary.write(*points)

    expected_bedtime_date, *_ = points
    retrieved = repository.get_by_bedtime_date(expected_bedtime_date)
    assert retrieved is not None
    assert isinstance(retrieved, NoteEntity)
    assert database.committed


def test_write_one_note_in_diary():
    fake_owner_oid = uuid4()
    database = FakeDatabase()
    repository: BaseUserNotesRepository = FakeUserNotesRepository(
        database=database,
        owner_oid=fake_owner_oid,
    )
    diary = service_layer.Diary(repository=repository)

    points = points_order_desc_from_went_to_bed
    diary.write(*points)

    expected_bedtime_date, *_ = points_order_desc_from_went_to_bed
    written_note = repository.get_by_bedtime_date(expected_bedtime_date)

    assert isinstance(written_note, NoteEntity)
    assert written_note.points.bedtime_date in points
    assert written_note.points.went_to_bed in points
    assert written_note.points.fell_asleep in points
    assert written_note.points.woke_up in points
    assert written_note.points.got_up in points


def test_write_note_in_diary_twice():
    fake_owner_oid = uuid4()
    database = FakeDatabase()
    repository: BaseUserNotesRepository = FakeUserNotesRepository(
        database=database,
        owner_oid=fake_owner_oid,
    )
    diary = service_layer.Diary(repository=repository)

    points = points_order_desc_from_went_to_bed
    diary.write(*points)

    with pytest.raises(NonUniqueNoteBedtimeDateException):
        diary.write(*points)


def test_write_different_note_in_diary():
    fake_owner_oid = uuid4()
    database = FakeDatabase()
    repository: BaseUserNotesRepository = FakeUserNotesRepository(
        fake_owner_oid,
        database,
    )
    diary = service_layer.Diary(repository)

    first_bedtime_date: date
    first_bedtime_date, *time_points = points_order_desc_from_went_to_bed

    second_bedtime_date = date(
        first_bedtime_date.year,
        first_bedtime_date.month,
        first_bedtime_date.day + 1,
    )

    points_1 = points_order_desc_from_went_to_bed
    points_2 = (second_bedtime_date, *time_points)

    diary.write(*points_1)
    diary.write(*points_2)

    notes = repository.get_all()
    assert len(notes) == 2
    note_in_diary_1, note_in_diary_2, *_ = sorted(notes)

    assert note_in_diary_1.points.bedtime_date in points_1
    assert note_in_diary_1.points.went_to_bed in points_1
    assert note_in_diary_1.points.fell_asleep in points_1
    assert note_in_diary_1.points.woke_up in points_1
    assert note_in_diary_1.points.got_up in points_1

    assert note_in_diary_2.points.bedtime_date in points_2
    assert note_in_diary_2.points.went_to_bed in points_2
    assert note_in_diary_2.points.fell_asleep in points_2
    assert note_in_diary_2.points.woke_up in points_2
    assert note_in_diary_2.points.got_up in points_2
