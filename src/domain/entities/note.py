from dataclasses import dataclass

from src.domain.entities.base import BaseEntity
from src.domain.values.time_points import TimePoints


@dataclass(eq=False)
class NoteEntity(BaseEntity):
    time_points: TimePoints
