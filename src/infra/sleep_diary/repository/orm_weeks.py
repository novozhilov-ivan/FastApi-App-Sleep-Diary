from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import func, select

from src.domain.sleep_diary.dtos import WeekInfo, WeekNotes
from src.domain.sleep_diary.repositories.base import IWeeksRepository
from src.gateways.postgresql.database import Database
from src.gateways.postgresql.models import ORMNote


@dataclass
class ORMWeeksRepository(IWeeksRepository):
    database: Database

    def get_weeks_info(self, owner_oid: UUID) -> list[WeekInfo]:
        stmt = (
            select(
                func.date_trunc("week", ORMNote.bedtime_date).label("week_start"),
                func.count().label("filled_notes_count"),
            )
            .where(ORMNote.owner_oid == owner_oid)
            .group_by(func.date_trunc("week", ORMNote.bedtime_date))
            .order_by(func.date_trunc("week", ORMNote.bedtime_date))
        )

        with self.database.get_session() as session:
            result = session.execute(stmt).all()

        return [
            WeekInfo(
                start_date=week_start.date(),
                filled_notes_count=filled_notes_count,
            )
            for week_start, filled_notes_count in result
        ]

    def get_user_week_notes(self, owner_oid: UUID, start_date: date) -> WeekNotes:
        week_end = start_date + timedelta(days=6)

        stmt = (
            select(ORMNote)
            .where(ORMNote.owner_oid == owner_oid)
            .where(ORMNote.bedtime_date >= start_date)
            .where(ORMNote.bedtime_date <= week_end)
            .order_by(ORMNote.bedtime_date)
        )

        with self.database.get_session() as session:
            result: Sequence[ORMNote] = session.execute(stmt).scalars().all()

        notes = [orm_note.to_entity() for orm_note in result]
        return WeekNotes(notes=notes)
