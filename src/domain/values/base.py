from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, time
from typing import Any
from typing_extensions import Self


@dataclass(frozen=True)
class BaseValueObject[VTDI: Any, VTTI: Any, VTDO: Any, VTTO: Any](ABC):
    def __post_init__(self: Self) -> None:
        self.validate()

    @abstractmethod
    def validate(self: Self) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class BaseDateTimeValueObject[
    VTDI: (str, date),
    VTTI: (str, time),
    VTDO: date,
    VTTO: time,
](BaseValueObject, ABC):
    value: VTDI | VTTI

    @abstractmethod
    def as_generic_type(self: Self) -> VTDO | VTTO:
        raise NotImplementedError
