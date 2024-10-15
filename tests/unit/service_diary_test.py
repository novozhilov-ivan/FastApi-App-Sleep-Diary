from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import date
from typing import Generator
from typing_extensions import Self
from uuid import UUID, uuid4

import pytest

from src import service_layer
from src.domain.entities.note import NoteEntity
from src.infrastructure.repository import BaseNoteRepository


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
        finally:
            ...


@dataclass
class FakeDiaryRepo(BaseNoteRepository):
    database: FakeDatabase

    def _add(self: Self, note: NoteEntity) -> None:
        with self.database.get_session() as session:
            session.add(note)

    def _get(self: Self, oid: UUID) -> None:
        raise NotImplementedError

    def _get_by_bedtime_date(
        self: Self,
        bedtime_date: date,
        owner_oid: UUID,
    ) -> NoteEntity | None:
        with self.database.get_session() as session:
            try:
                return next(
                    note
                    for note in session
                    if note.bedtime_date == bedtime_date
                    and note.owner_oid == owner_oid
                )
            except StopIteration:
                return None

    def _get_all(self: Self, owner_oid: UUID) -> set[NoteEntity]:
        with self.database.get_session() as session:
            return {note for note in session if note.owner_oid == owner_oid}


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
    fake_owner_oid = uuid4()
    database = FakeDatabase()
    repository: BaseNoteRepository = FakeDiaryRepo(database)

    service_layer.write(
        "2020-12-12",
        "13:00",
        "15:00",
        "23:00",
        "01:00",
        no_sleep,
        fake_owner_oid,
        repository,
    )
    retrieved = repository.get_by_bedtime_date("2020-12-12", fake_owner_oid)
    assert retrieved is not None
    assert isinstance(retrieved, NoteEntity)
    assert database.committed


def test_write_one_note_in_diary():
    diary = Diary()
    note = NoteTimePoints(
        bedtime_date="2024-01-01",
        went_to_bed="01:00",
        fell_asleep="03:00",
        woke_up="11:00",
        got_up="13:00",
    )
    written_note = write(note, diary)
    assert isinstance(written_note, NoteValueObject)
    assert written_note.bedtime_date == note.bedtime_date
    assert written_note.went_to_bed == note.went_to_bed
    assert written_note.fell_asleep == note.fell_asleep
    assert written_note.woke_up == note.woke_up
    assert written_note.got_up == note.got_up


def test_write_note_in_diary_twice():
    diary = Diary()
    note = NoteTimePoints(
        bedtime_date="2024-01-01",
        went_to_bed="01:00",
        fell_asleep="03:00",
        woke_up="11:00",
        got_up="13:00",
    )
    write(note, diary)

    with pytest.raises(NonUniqueNoteBedtimeDateException):
        write(note, diary)


def test_write_different_note_in_diary():
    diary = Diary()
    note_1 = NoteValueObject(
        bedtime_date="2024-01-01",
        went_to_bed="01:00",
        fell_asleep="03:00",
        woke_up="11:00",
        got_up="13:00",
    )
    note_2 = NoteValueObject(
        bedtime_date="2024-01-02",
        went_to_bed="03:00",
        fell_asleep="05:00",
        woke_up="13:00",
        got_up="15:00",
    )
    written_note_1 = write(note_1, diary)
    written_note_2 = write(note_2, diary)

    assert len(diary.notes_list) == 2
    note_in_diary_1, note_in_diary_2, *_ = sorted(diary.notes_list)
    assert note_in_diary_1 == written_note_1
    assert note_in_diary_2 == written_note_2
    assert isinstance(written_note_1, NoteValueObject)
    assert isinstance(written_note_2, NoteValueObject)
    assert written_note_1.bedtime_date == note_1.bedtime_date
    assert written_note_1.went_to_bed == note_1.went_to_bed
    assert written_note_1.fell_asleep == note_1.fell_asleep
    assert written_note_1.woke_up == note_1.woke_up
    assert written_note_1.got_up == note_1.got_up
    assert written_note_2.bedtime_date == note_2.bedtime_date
    assert written_note_2.went_to_bed == note_2.went_to_bed
    assert written_note_2.fell_asleep == note_2.fell_asleep
    assert written_note_2.woke_up == note_2.woke_up
    assert written_note_2.got_up == note_2.got_up
