from typing import Iterable
from typing_extensions import Self

from src import services
from src.domain.diary import Diary
from src.domain.note import NoteEntity, NoteTimePoints, NoteValueObject
from src.repositories import BaseDiaryRepository


class FakeDiaryRepo(BaseDiaryRepository):
    def __init__(self: Self, notes: Iterable[NoteEntity]) -> None:
        self._notes: set = set(notes)

    def add(self: Self, note: NoteTimePoints) -> None:
        self._notes.add(note)

    def get(self: Self, oid: int) -> NoteEntity:
        return next(n for n in self._notes if n.oid == oid)

    def get_by_bedtime_date(self: Self, bedtime_date: str) -> NoteEntity:
        return next(n for n in self._notes if str(n.bedtime_date) == bedtime_date)

    def get_diary(self: Self) -> Diary:
        diary = Diary()
        diary._notes = self._notes
        return diary


class FakeSession:
    committed: bool = False

    def commit(self: Self) -> None:
        self.committed = True


def test_service_write_note() -> None:
    repo, session = FakeDiaryRepo([]), FakeSession()
    note = NoteTimePoints(
        bedtime_date="2020-12-12",
        went_to_bed="13:00",
        fell_asleep="15:00",
        woke_up="23:00",
        got_up="01:00",
    )
    services.write(note, repo, session)
    assert repo.get_by_bedtime_date("2020-12-12") is not None
    assert repo.get_by_bedtime_date(
        bedtime_date="2020-12-12",
    ) == NoteValueObject.model_validate(
        obj=note,
        from_attributes=True,
    )
    assert session.committed
