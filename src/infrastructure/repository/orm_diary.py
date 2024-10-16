from dataclasses import dataclass
from datetime import date
from typing_extensions import Self
from uuid import UUID

from sqlalchemy import select

from src.domain.entities.note import NoteEntity
from src.infrastructure.database import Database
from src.infrastructure.orm import ORMNote
from src.infrastructure.repository.base import (
    BaseUserNotesRepository,
)


@dataclass
class ORMUserNotesRepository(BaseUserNotesRepository):
    database: Database

    def add(self: Self, note: NoteEntity) -> None:
        with self.database.get_session() as session:
            session.add(ORMNote.from_entity(note))

    def get(self: Self, oid: UUID) -> NoteEntity | None:
        stmt = select(ORMNote).where(ORMNote.oid == oid).limit(1)

        with self.database.get_session() as session:
            result = session.scalar(stmt)

        if isinstance(result, ORMNote):
            return result.to_entity()
        return None

    def get_by_bedtime_date(self: Self, bedtime_date: date) -> NoteEntity | None:
        stmt = (
            select(ORMNote)
            .where(ORMNote.owner_oid == self.owner_oid)
            .where(ORMNote.bedtime_date == bedtime_date)
            .limit(1)
        )
        with self.database.get_session() as session:
            result = session.scalar(stmt)

        if isinstance(result, ORMNote):
            return result.to_entity()
        return None

    def get_all(self: Self) -> set[NoteEntity]:
        stmt = select(ORMNote).where(ORMNote.owner_oid == self.owner_oid)

        with self.database.get_session() as session:
            result = session.scalars(stmt).all()

        return {note.to_entity() for note in result if isinstance(note, ORMNote)}
