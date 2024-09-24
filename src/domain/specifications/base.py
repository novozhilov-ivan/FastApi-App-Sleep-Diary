from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing_extensions import Self

from src.domain.values.time_points import PointsOut


@dataclass
class BaseSpecification(ABC):
    points: PointsOut

    @abstractmethod
    def __bool__(self: Self) -> bool:
        raise NotImplementedError
