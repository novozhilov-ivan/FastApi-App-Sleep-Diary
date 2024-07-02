import abc

from datetime import time

from pydantic import computed_field

from src.domain.note import (
    NoteDurationsBase,
    NoteStatisticBase,
    NoteValueObjectBase,
)


class NoteStatistic(
    NoteValueObjectBase,
    NoteDurationsBase,
    NoteStatisticBase,
    abc.ABC,
):
    @computed_field
    @property
    def time_in_sleep(self) -> time:
        return time(hour=0)

    @computed_field
    @property
    def time_in_bed(self) -> time:
        return time(hour=0)

    @computed_field
    @property
    def sleep_efficiency(self) -> float:
        return 0.1
