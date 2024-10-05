from dataclasses import InitVar, dataclass, field
from datetime import time, timedelta
from operator import ge, sub
from typing import TYPE_CHECKING
from typing_extensions import Self


if TYPE_CHECKING:
    from src.domain.values.points import Points


@dataclass
class Durations:
    points: InitVar["Points"]

    sleep: timedelta = field(init=False)
    sleep_minus_without_sleep: timedelta = field(init=False)
    in_bed: timedelta = field(init=False)
    without_sleep: timedelta = field(init=False)

    def __post_init__(self: Self, points: "Points") -> None:
        self.sleep = self._get_duration(points.woke_up, points.fell_asleep)
        self.in_bed = self._get_duration(points.got_up, points.went_to_bed)
        self.without_sleep = self._get_duration(points.no_sleep)
        self.sleep_minus_without_sleep = self._get_sub_of_durations(
            self.sleep,
            self.without_sleep,
        )

    @staticmethod
    def _point_time_to_duration(point: time) -> timedelta:
        return timedelta(hours=point.hour, minutes=point.minute)

    @staticmethod
    def _get_duration_seconds_only(duration: timedelta) -> timedelta:
        return timedelta(seconds=duration.seconds)

    def _get_duration_between_two_points(
        self: Self,
        first_point: time,
        second_point: time,
    ) -> timedelta:
        duration = timedelta(
            hours=sub(first_point.hour, second_point.hour),
            minutes=sub(first_point.minute, second_point.minute),
        )
        return self._get_duration_seconds_only(duration)

    def _get_duration(
        self: Self,
        first_point: time,
        second_point: time | None = None,
    ) -> timedelta:
        if second_point is not None:
            duration = self._get_duration_between_two_points(
                first_point,
                second_point,
            )
        else:
            duration = self._point_time_to_duration(first_point)
        return self._get_duration_seconds_only(duration)

    def _get_sub_of_durations(
        self: Self,
        first_duration: timedelta,
        second_duration: timedelta,
    ) -> timedelta:
        if ge(second_duration, first_duration):
            duration = self._get_duration_seconds_only(timedelta())
        else:
            duration = sub(first_duration, second_duration)
        return self._get_duration_seconds_only(duration)
