from typing import Iterable
from typing_extensions import Self
from uuid import UUID

import pytest

from src import service_layer
from src.domain.diary import Diary
from src.domain.note import NoteEntity, NoteTimePoints, NoteValueObject
from src.infrastructure.repository import BaseDiaryRepository


class FakeDiaryRepo(BaseDiaryRepository):
    def __init__(self: Self, notes: Iterable[NoteValueObject]) -> None:
        self._notes: set = set(notes)

    def add(self: Self, note: NoteTimePoints) -> None:  # not used, not tested
        new_note = NoteValueObject.model_validate(
            obj=note,
            from_attributes=True,
        )
        self._notes.add(new_note)

    def get(self: Self, oid: UUID) -> NoteEntity:  # not used, not tested
        return next(n for n in self._notes if n.oid == oid)

    def get_by_bedtime_date(self: Self, bedtime_date: str) -> NoteValueObject:
        # 'str(n.bedtime_date)' - str(...) тут как заглушка. нужно переделать
        return next(n for n in self._notes if str(n.bedtime_date) == bedtime_date)

    def get_diary(self: Self) -> Diary:  # used, not tested
        diary = Diary()
        diary._notes = self._notes
        return diary


class FakeSession:
    committed: bool = False

    def commit(self: Self) -> None:
        self.committed = True


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
    repo, session = FakeDiaryRepo([]), FakeSession()
    service_layer.write(
        "2020-12-12",
        "13:00",
        "15:00",
        "23:00",
        "01:00",
        no_sleep,
        repo,
        session,
    )
    note_value_object = repo.get_by_bedtime_date("2020-12-12")
    assert note_value_object is not None
    assert isinstance(note_value_object, NoteValueObject)
    assert session.committed
