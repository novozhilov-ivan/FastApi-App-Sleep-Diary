from typing import Iterable

from pydantic import BaseModel, Field

from src.adapters import orm
from src.adapters.repositories.abstract import AbstractRepository


class FakeRepository(AbstractRepository):

    def __init__(self, notes: Iterable[orm.Note]):
        self._notes: set[orm.Note] = set(notes)

    def add(self, note: orm.Note) -> None:
        self._notes.add(note)

    def get(self, oid):
        return next(n for n in self._notes if n.oid == oid)
