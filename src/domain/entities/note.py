from dataclasses import dataclass

from src.domain.entities.base import BaseEntity
from src.domain.values import points


@dataclass(eq=False)
class NoteEntity(BaseEntity):
    points: points.Points
