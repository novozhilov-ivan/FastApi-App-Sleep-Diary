from itertools import chain
from typing import Generator
from typing_extensions import Self

from pydantic import computed_field

from src.domain import diary as dr, note as nt, week as wk


class Diary(dr.BaseDiary):
    @computed_field  # type: ignore[misc]
    @property
    def notes_count(self: Self) -> int:
        return len(self.notes_list())

    @computed_field  # type: ignore[misc]
    @property
    def weeks_count(self: Self) -> int:
        return len(self.weeks)

    def notes_list(self: Self) -> set[nt.NoteValueObject] | set:
        if not self.weeks:
            return set()
        return set(chain.from_iterable(self.weeks))

    def write(self: Self, note: nt.NoteValueObject) -> None:
        if not self.can_write(note):
            return

        week_to_write: Generator[wk.BaseWeek, None, None]
        week_to_write = (w for w in self.weeks if w.is_writable())

        if isinstance(week_to_write, wk.BaseWeek):
            week_to_write.add(note)
        else:
            new_week = wk.Week(note)
            self.weeks.append(new_week)

    def can_write(self: Self, note: nt.NoteValueObject) -> bool:
        return note not in self.notes_list()
