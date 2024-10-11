from abc import ABC, abstractmethod
from dataclasses import InitVar, dataclass, field
from datetime import time, timedelta
from typing import TYPE_CHECKING
from typing_extensions import Self


if TYPE_CHECKING:
    from src.domain.values.points import Points


@dataclass
class BaseDurations(ABC):
    points: InitVar["Points"]

    sleep: timedelta = field(init=False)
    sleep_minus_without_sleep: timedelta = field(init=False)
    in_bed: timedelta = field(init=False)
    without_sleep: timedelta = field(init=False)

    @abstractmethod
    def __post_init__(self: Self, points: "Points") -> None:
        raise NotImplementedError


@dataclass
class BaseStatistics(ABC):
    durations: InitVar[BaseDurations]

    sleep: time = field(init=False)
    in_bed: time = field(init=False)
    sleep_minus_no_sleep: time = field(init=False)
    sleep_efficiency: float = field(init=False)

    @abstractmethod
    def __post_init__(self: Self, durations: BaseDurations) -> None:
        raise NotImplementedError
