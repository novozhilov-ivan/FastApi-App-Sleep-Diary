from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init__(self) -> None:
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        raise NotImplementedError
