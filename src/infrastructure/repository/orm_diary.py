from dataclasses import dataclass
from datetime import date
from typing import Sequence
from typing_extensions import Self
from uuid import UUID

from sqlalchemy import select

from src.domain.entities.note import NoteEntity
from src.infrastructure.database import Database
from src.infrastructure.orm import ORMNote
from src.infrastructure.repository.base import BaseNoteRepository


@dataclass
class ORMNoteRepository(BaseNoteRepository):
    database: Database

    def _add(self: Self, note: NoteEntity) -> None:
        with self.database.get_session() as session:
            session.add(ORMNote.from_entity(note))

    # TODO Добавить получение через фильтр
    def _get(self: Self, oid: UUID) -> ORMNote | None:
        stmt = select(ORMNote).where(ORMNote.oid == oid).limit(1)
        with self.database.get_session() as session:
            return session.scalar(stmt)

    # TODO Добавить получение через фильтр
    def _get_by_bedtime_date(
        self: Self,
        bedtime_date: date,
        owner_oid: UUID,
    ) -> ORMNote | None:
        stmt = (
            select(ORMNote)
            .where(ORMNote.owner_oid == owner_oid)
            .where(ORMNote.bedtime_date == bedtime_date)
            .limit(1)
        )
        with self.database.get_session() as session:
            return session.scalar(stmt)

    def _get_all(self: Self, owner_oid: UUID) -> Sequence[ORMNote]:
        stmt = select(ORMNote).where(ORMNote.owner_oid == owner_oid)
        with self.database.get_session() as session:
            return session.scalars(stmt).all()
