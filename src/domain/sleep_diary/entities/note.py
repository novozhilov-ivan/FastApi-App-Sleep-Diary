from dataclasses import dataclass
from datetime import date
from functools import total_ordering
from operator import eq, gt
from typing import TYPE_CHECKING
from uuid import UUID

from src.domain.sleep_diary.entities.base import BaseEntity
from src.domain.sleep_diary.services.base import IDurations, IStatistics
from src.domain.sleep_diary.services.durations import Durations
from src.domain.sleep_diary.services.note_statistics import Statistics

if TYPE_CHECKING:
    from src.domain.sleep_diary.values.points import Points


@total_ordering
@dataclass(eq=False, kw_only=True, slots=True)
class NoteEntity(BaseEntity):
    owner_oid: UUID
    points: "Points"

    @property
    def _idempotency_key(self) -> tuple[date, UUID]:
        return self.points.bedtime_date, self.owner_oid

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NoteEntity):
            return NotImplemented
        return eq(self._idempotency_key, other._idempotency_key)

    def __hash__(self) -> int:
        return hash(self._idempotency_key)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, NoteEntity):
            return NotImplemented
        return gt(self.points.bedtime_date, other.points.bedtime_date)

    @property
    def durations(self) -> IDurations:
        return Durations(self.points)

    @property
    def statistics(self) -> IStatistics:
        return Statistics(self.durations)
