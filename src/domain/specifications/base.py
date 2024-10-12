from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing_extensions import Self


if TYPE_CHECKING:
    from src.domain.values.points import Points


@dataclass
class BaseSpecification(ABC):
    @abstractmethod
    def __bool__(self: Self) -> bool:
        raise NotImplementedError


@dataclass
class BasePointsSpecification(BaseSpecification, ABC):
    points: "Points"
