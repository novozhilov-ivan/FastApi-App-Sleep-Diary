from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import func, select

from src.domain.sleep_diary.dtos import Week
from src.domain.sleep_diary.repositories.base import IWeeksRepository
from src.gateways.postgresql.database import Database
from src.gateways.postgresql.models import ORMNote


@dataclass
class ORMWeeksRepository(IWeeksRepository):
    database: Database

    def get_weeks_info(self, owner_oid: UUID) -> list[Week]:
        stmt = (
            select(
                func.dense_rank()
                .over(order_by=func.date_trunc("week", ORMNote.bedtime_date))
                .label("week_rank"),
                func.date_trunc("week", ORMNote.bedtime_date).label("week_start"),
                func.count().label("filled_notes_count"),
            )
            .where(ORMNote.owner_oid == owner_oid)
            .group_by(func.date_trunc("week", ORMNote.bedtime_date))
            .order_by(func.date_trunc("week", ORMNote.bedtime_date))
        )

        with self.database.get_session() as session:
            result = session.execute(stmt)

        return [
            Week(
                number=week_rank,
                start_date=week_start.date(),
                filled_notes_count=filled_notes_count,
            )
            for week_rank, week_start, filled_notes_count in result
        ]
