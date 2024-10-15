from dataclasses import dataclass
from operator import eq
from typing import TYPE_CHECKING
from typing_extensions import Self
from uuid import UUID

from src.domain.entities.base import BaseEntity
from src.domain.services.base import BaseDurations, BaseStatistics


if TYPE_CHECKING:
    from src.domain.values.points import Points


@dataclass(eq=False, kw_only=True)
class NoteEntity(BaseEntity):
    owner_oid: UUID
    points: "Points"
    durations: BaseDurations | None = None
    statistics_of_points: BaseStatistics | None = None

    def __eq__(self: Self, other: object) -> bool:
        if not isinstance(other, NoteEntity):
            return NotImplemented
        return eq(
            (self.points.bedtime_date, self.owner_oid),
            (other.points.bedtime_date, other.owner_oid),
        )

    def __hash__(self: Self) -> int:
        return hash((self.points.bedtime_date, self.owner_oid))
