from typing import Sequence
from typing_extensions import Self
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.diary import Diary
from src.domain.note import NoteEntity, NoteTimePoints, NoteValueObject
from src.orm import NoteORM
from src.repositories.base import BaseDiaryRepository


class SQLAlchemyDiaryRepository(BaseDiaryRepository):
    def __init__(
        self: Self,
        session: Session,
        owner_id: UUID,
    ) -> None:
        self.session: Session = session
        self.owner_id: UUID = owner_id

    def add(self: Self, note: NoteTimePoints) -> None:
        self.session.add(
            NoteORM.from_time_points(
                obj=note,
                owner_id=self.owner_id,
            ),
        )

    def get(self: Self, oid: UUID) -> NoteEntity:  # or raise NoResult
        query = (
            select(NoteORM)
            .where(NoteORM.owner_id == self.owner_id)
            .where(NoteORM.oid == oid)
        )
        result: NoteORM = self.session.execute(query).scalar_one()
        return result.to_entity()

    def get_by_bedtime_date(self: Self, bedtime_date: str) -> NoteEntity:
        query = (
            select(NoteORM)
            .where(NoteORM.owner_id == self.owner_id)
            .where(NoteORM.bedtime_date == bedtime_date)
        )
        result: NoteORM = self.session.execute(query).scalar_one()
        return result.to_entity()

    def get_diary(self: Self) -> Diary:
        diary = Diary()
        query = select(NoteORM).where(NoteORM.owner_id == self.owner_id)
        results: Sequence[NoteORM] = self.session.execute(query).scalars().all()
        diary._notes = {
            NoteValueObject.model_validate(
                obj=note,
                from_attributes=True,
            )
            for note in results
        }
        return diary
