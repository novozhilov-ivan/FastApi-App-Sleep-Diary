from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init__(self: Self) -> None:
        self.validate()

    @abstractmethod
    def validate(self: Self) -> None:
        raise NotImplementedError
