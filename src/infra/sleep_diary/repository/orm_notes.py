from dataclasses import dataclass
from datetime import date
from uuid import UUID

from sqlalchemy import select

from src.domain.sleep_diary.entities.note import NoteEntity
from src.domain.sleep_diary.repositories.base import INotesRepository
from src.gateways.postgresql.database import Database
from src.gateways.postgresql.models.note import ORMNote


@dataclass
class ORMNotesRepository(INotesRepository):
    database: Database

    def add(self, note: NoteEntity) -> None:
        with self.database.get_session() as session:
            session.add(ORMNote.from_entity(note))

    def get_by_oid(self, oid: UUID) -> NoteEntity | None:
        stmt = select(ORMNote).where(ORMNote.oid == oid).limit(1)

        with self.database.get_session() as session:
            result = session.scalar(stmt)

        if isinstance(result, ORMNote):
            return result.to_entity()
        return None

    def get_by_bedtime_date(
        self,
        bedtime_date: date,
        owner_oid: UUID,
    ) -> NoteEntity | None:
        stmt = (
            select(ORMNote)
            .where(ORMNote.owner_oid == owner_oid)
            .where(ORMNote.bedtime_date == bedtime_date)
            .limit(1)
        )
        with self.database.get_session() as session:
            result = session.scalar(stmt)

        if isinstance(result, ORMNote):
            return result.to_entity()
        return None

    def get_all_notes(self, owner_oid: UUID) -> set[NoteEntity]:
        stmt = select(ORMNote).where(ORMNote.owner_oid == owner_oid)

        with self.database.get_session() as session:
            result = session.scalars(stmt).all()

        return {note.to_entity() for note in result}
