from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing_extensions import Self


if TYPE_CHECKING:
    from src.domain.values.points import PointsOut


@dataclass(eq=False)
class BaseSpecification(ABC):
    points: "PointsOut"

    @abstractmethod
    def __bool__(self: Self) -> bool:
        raise NotImplementedError
