import abc

from datetime import time
from typing_extensions import Self

from pydantic import computed_field

from src.domain import note


class NoteStatistic(
    note.NoteValueObjectBase,
    note.NoteDurationsBase,
    note.NoteStatisticBase,
    abc.ABC,
):
    @computed_field  # type: ignore[misc]
    @property
    def time_in_sleep(self: Self) -> time:
        return time(hour=0)

    @computed_field  # type: ignore[misc]
    @property
    def time_in_bed(self: Self) -> time:
        return time(hour=0)

    @computed_field  # type: ignore[misc]
    @property
    def sleep_efficiency(self: Self) -> float:
        return 0.1
