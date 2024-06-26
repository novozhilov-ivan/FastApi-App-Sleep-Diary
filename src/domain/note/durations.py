from datetime import timedelta

from pydantic import computed_field
from typing_extensions import Self

from src.domain.note.base import NoteBase


class NoteDurations(NoteBase):
    @computed_field
    @property
    def _sleep_duration_without_the_no_sleep(self: Self) -> timedelta:
        sleep_duration = timedelta(
            hours=self.woke_up.hour - self.fell_asleep.hour,
            minutes=self.woke_up.minute - self.fell_asleep.minute,
        )
        return timedelta(
            seconds=sleep_duration.seconds,
        )

    @computed_field
    @property
    def _no_sleep_duration(self: Self) -> timedelta:
        return timedelta(
            hours=self.no_sleep.hour,
            minutes=self.no_sleep.minute,
        )
