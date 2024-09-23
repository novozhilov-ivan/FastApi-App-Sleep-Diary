from dataclasses import dataclass, field
from typing_extensions import Self

from src.domain.services.note_durations import NoteDurations
from src.domain.values.time_points import Points


@dataclass
class NoSleepHasValidTime:
    points: Points
    durations: NoteDurations = field(init=False)

    def __post_init__(self: Self) -> None:
        self.durations: NoteDurations = NoteDurations(self.points.as_generic_type())

    def __bool__(self: Self) -> bool:
        return self.durations.without_sleep <= self.durations.sleep
