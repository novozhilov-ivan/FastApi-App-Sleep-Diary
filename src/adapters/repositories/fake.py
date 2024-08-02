from pydantic import BaseModel

from src.adapters import orm
from src.adapters.repositories.abstract import AbstractRepository


class FakeRepository(AbstractRepository, BaseModel):
    notes: set

    def add(self, note: orm.Note) -> None:
        self.notes.add(note)

    def get(self, oid):
        return next(n for n in self.notes if n.oid == oid)
