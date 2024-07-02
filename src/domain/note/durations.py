from datetime import timedelta
from typing_extensions import Self

from pydantic import computed_field

from src.domain.note import (
    NoteDurationsBase,
    NoteValueObjectBase,
)


class NoteDurations(
    NoteValueObjectBase,
    NoteDurationsBase,
):
    @computed_field  # type: ignore[misc]
    @property
    def _sleep_duration_without_no_sleep(self: Self) -> timedelta:
        sleep_duration = timedelta(
            hours=self.woke_up.hour - self.fell_asleep.hour,
            minutes=self.woke_up.minute - self.fell_asleep.minute,
        )
        return timedelta(seconds=sleep_duration.seconds)

    @computed_field  # type: ignore[misc]
    @property
    def _in_bed_duration(self: Self) -> timedelta:
        sleep_duration = timedelta(
            hours=self.got_up.hour - self.went_to_bed.hour,
            minutes=self.got_up.minute - self.went_to_bed.minute,
        )
        return timedelta(seconds=sleep_duration.seconds)

    @computed_field  # type: ignore[misc]
    @property
    def _no_sleep_duration(self: Self) -> timedelta:
        return timedelta(
            hours=self.no_sleep.hour,
            minutes=self.no_sleep.minute,
        )
