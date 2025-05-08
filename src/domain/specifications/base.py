from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self


@dataclass
class BaseSpecification(ABC):
    @abstractmethod
    def __bool__(self: Self) -> bool:
        raise NotImplementedError
