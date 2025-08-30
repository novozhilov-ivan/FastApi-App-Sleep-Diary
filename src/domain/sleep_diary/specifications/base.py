from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseSpecification(ABC):
    @abstractmethod
    def __bool__(self) -> bool:
        raise NotImplementedError
