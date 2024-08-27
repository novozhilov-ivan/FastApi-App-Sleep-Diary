from dataclasses import dataclass
from typing_extensions import Self
from uuid import UUID

from sqlalchemy import select

from src.domain.diary import Diary
from src.infrastructure.database import Database
from src.infrastructure.orm import ORMNote
from src.infrastructure.repository.base import IDiaryRepository


@dataclass
class ORMDiaryRepository(IDiaryRepository):
    database: Database

    def add(self: Self, note: ORMNote) -> None:
        with self.database.get_session() as session:
            session.add(note)

    def get(self: Self, oid: UUID) -> ORMNote | None:
        stmt = select(ORMNote).where(ORMNote.oid == oid).limit(1)
        with self.database.get_session() as session:
            return session.scalar(stmt)

    def get_by_bedtime_date(
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

    def get_diary(self: Self, owner_id: UUID) -> Diary:
        diary = Diary()
        stmt = select(ORMNote).where(ORMNote.owner_id == owner_id)
        with self.database.get_session() as session:
            diary._notes = session.scalars(stmt).all()
        return diary
