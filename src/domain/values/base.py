from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from typing_extensions import Self


@dataclass(frozen=True)
class BaseValueObject[VTI: Any, VTO: Any](ABC):
    value: VTI

    def __post_init__(self: Self) -> None:
        self.validate()

    @abstractmethod
    def validate(self: Self) -> None:
        raise NotImplementedError

    @abstractmethod
    def as_generic_type(self: Self) -> VTO:
        raise NotImplementedError
