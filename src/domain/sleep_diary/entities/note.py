from dataclasses import dataclass
from functools import total_ordering
from operator import eq, gt
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from src.domain.sleep_diary.entities.base import BaseEntity


if TYPE_CHECKING:
    from src.domain.sleep_diary.services.base import IDurations, IStatistics
    from src.domain.sleep_diary.values.points import Points


@total_ordering
@dataclass(eq=False, kw_only=True)
class NoteEntity(BaseEntity):
    owner_oid: UUID
    points: "Points"
    durations: Optional["IDurations"] = None
    statistics_of_points: Optional["IStatistics"] = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NoteEntity):
            return NotImplemented
        return eq(
            (self.points.bedtime_date, self.owner_oid),
            (other.points.bedtime_date, other.owner_oid),
        )

    def __hash__(self) -> int:
        return hash((self.points.bedtime_date, self.owner_oid))

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, NoteEntity):
            return NotImplemented
        return gt(self.points.bedtime_date, other.points.bedtime_date)
