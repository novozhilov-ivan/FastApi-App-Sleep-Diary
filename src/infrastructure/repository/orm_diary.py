from dataclasses import dataclass
from typing import Sequence
from typing_extensions import Self
from uuid import UUID

from sqlalchemy import select

from src.domain.note import NoteValueObject
from src.infrastructure.database import Database
from src.infrastructure.orm import ORMNote
from src.infrastructure.repository.base import BaseDiaryRepository


@dataclass
class ORMDiaryRepository(BaseDiaryRepository):
    database: Database

    def _add(self: Self, note: NoteValueObject, owner_id: UUID) -> None:
        with self.database.get_session() as session:
            session.add(ORMNote.from_time_points(note, owner_id))

    def _get(self: Self, oid: UUID) -> ORMNote | None:
        stmt = select(ORMNote).where(ORMNote.oid == oid).limit(1)
        with self.database.get_session() as session:
            return session.scalar(stmt)

    def _get_by_bedtime_date(
        self: Self,
        bedtime_date: str,
        owner_id: UUID,
    ) -> ORMNote | None:
        stmt = (
            select(ORMNote)
            .where(ORMNote.owner_id == owner_id)
            .where(ORMNote.bedtime_date == bedtime_date)
            .limit(1)
        )
        with self.database.get_session() as session:
            return session.scalar(stmt)

    def _get_diary(self: Self, owner_id: UUID) -> Sequence[ORMNote]:
        stmt = select(ORMNote).where(ORMNote.owner_id == owner_id)
        with self.database.get_session() as session:
            return session.scalars(stmt).all()
