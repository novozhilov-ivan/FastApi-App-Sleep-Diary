from itertools import chain
from typing_extensions import Self

from pydantic import computed_field

from src.domain import diary as dr


class Diary(dr.BaseDiary):
    @computed_field  # type: ignore[misc]
    @property
    def notes_count(self: Self) -> int:
        if not self.weeks:
            return 0
        notes = tuple(chain.from_iterable(self.weeks))
        return len(notes)

    @computed_field  # type: ignore[misc]
    @property
    def weeks_count(self: Self) -> int:
        return len(self.weeks)
