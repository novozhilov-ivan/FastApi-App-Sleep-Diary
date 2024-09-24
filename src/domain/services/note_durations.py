import operator as op

from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING
from typing_extensions import Self


if TYPE_CHECKING:
    from src.domain.values import PointsOut


@dataclass
class NoteDurations:
    points: "PointsOut"

    @property
    def sleep(self: Self) -> timedelta:
        duration = timedelta(
            hours=op.sub(
                self.points.woke_up.hour,
                self.points.fell_asleep.hour,
            ),
            minutes=op.sub(
                self.points.woke_up.minute,
                self.points.fell_asleep.minute,
            ),
        )
        return timedelta(seconds=duration.seconds)

    @property
    def sleep_minus_without_sleep(self: Self) -> timedelta:
        if self.without_sleep >= self.sleep:
            return timedelta(seconds=0)
        duration = op.sub(self.sleep, self.without_sleep)
        return timedelta(seconds=duration.seconds)

    @property
    def in_bed(self: Self) -> timedelta:
        duration = timedelta(
            hours=op.sub(
                self.points.got_up.hour,
                self.points.went_to_bed.hour,
            ),
            minutes=op.sub(
                self.points.got_up.minute,
                self.points.went_to_bed.minute,
            ),
        )
        return timedelta(seconds=duration.seconds)

    @property
    def without_sleep(self: Self) -> timedelta:
        return timedelta(
            hours=self.points.no_sleep.hour,
            minutes=self.points.no_sleep.minute,
        )
