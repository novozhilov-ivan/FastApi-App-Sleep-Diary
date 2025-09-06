from abc import ABC, abstractmethod
from datetime import time, timedelta


class IDurations(ABC):
    @property
    @abstractmethod
    def sleep(self) -> timedelta:
        raise NotImplementedError

    @property
    @abstractmethod
    def sleep_minus_without_sleep(self) -> timedelta:
        raise NotImplementedError

    @property
    @abstractmethod
    def in_bed(self) -> timedelta:
        raise NotImplementedError

    @property
    @abstractmethod
    def without_sleep(self) -> timedelta:
        raise NotImplementedError


class IStatistics(ABC):
    @property
    @abstractmethod
    def sleep(self) -> time:
        raise NotImplementedError

    @property
    @abstractmethod
    def in_bed(self) -> time:
        raise NotImplementedError

    @property
    @abstractmethod
    def sleep_minus_no_sleep(self) -> time:
        raise NotImplementedError

    @property
    @abstractmethod
    def sleep_efficiency(self) -> float:
        raise NotImplementedError
