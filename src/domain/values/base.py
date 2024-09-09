import abc

from dataclasses import dataclass
from datetime import date, time
from typing_extensions import Self


@dataclass(frozen=True)
class BaseValueObject[VTI: str | time | date, VTO: time | date](abc.ABC):
    value: VTI

    def __post_init__(self: Self) -> None:
        self.validate()

    @abc.abstractmethod
    def validate(self: Self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def as_generic_type(self: Self) -> VTO:
        raise NotImplementedError
