from dataclasses import dataclass

from src.domain.entities.base import BaseEntity
from src.domain.values.time_points import Points


@dataclass(eq=False)
class NoteEntity(BaseEntity):
    points: Points
