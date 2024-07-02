import abc

from pydantic import BaseModel

from src.domain import note


class WeekBase(BaseModel, abc.ABC):
    notes: set[note.NoteValueObjectBase]
