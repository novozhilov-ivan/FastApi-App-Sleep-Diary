import abc

from pydantic import BaseModel

from src.domain.note.base import NoteBase


class WeekBase(BaseModel, abc.ABC):
    notes: list[NoteBase]
