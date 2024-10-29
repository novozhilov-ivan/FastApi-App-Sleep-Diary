from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from typing import TYPE_CHECKING
from typing_extensions import Self
from uuid import UUID, uuid4


if TYPE_CHECKING:
    from src.domain.values.points import Points


@dataclass(eq=False, kw_only=True)
class BaseEntity(ABC):
    oid: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class IDurations:
    points: "Points"

    @property
    @abstractmethod
    def sleep(self: Self) -> timedelta:
        raise NotImplementedError

    @property
    @abstractmethod
    def sleep_minus_without_sleep(self: Self) -> timedelta:
        raise NotImplementedError

    @property
    @abstractmethod
    def in_bed(self: Self) -> timedelta:
        raise NotImplementedError

    @property
    @abstractmethod
    def without_sleep(self: Self) -> timedelta:
        raise NotImplementedError


@dataclass
class IStatistics:
    durations: IDurations

    @property
    @abstractmethod
    def sleep(self: Self) -> time:
        raise NotImplementedError

    @property
    @abstractmethod
    def in_bed(self: Self) -> time:
        raise NotImplementedError

    @property
    @abstractmethod
    def sleep_minus_no_sleep(self: Self) -> time:
        raise NotImplementedError

    @property
    @abstractmethod
    def sleep_efficiency(self: Self) -> float:
        raise NotImplementedError
