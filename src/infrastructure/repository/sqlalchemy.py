from typing import Sequence
from typing_extensions import Self
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.diary import Diary
from src.domain.note import NoteEntity, NoteTimePoints, NoteValueObject
from src.infrastructure.orm import ORMNote
from src.infrastructure.repository.base import BaseDiaryRepository


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
            ORMNote.from_time_points(
                obj=note,
                owner_id=self.owner_id,
            ),
        )

    def get(self: Self, oid: UUID) -> NoteEntity:
        query = (
            select(ORMNote)
            .where(ORMNote.owner_id == self.owner_id)
            .where(ORMNote.oid == oid)
        )
        result: ORMNote = self.session.execute(query).scalar_one()
        # or raise NoResult
        return result.to_entity()

    def get_by_bedtime_date(self: Self, bedtime_date: str) -> NoteEntity:
        query = (
            select(ORMNote)
            .where(ORMNote.owner_id == self.owner_id)
            .where(ORMNote.bedtime_date == bedtime_date)
        )
        result: ORMNote = self.session.execute(query).scalar_one()
        # or raise NoResult
        return result.to_entity()

    def get_diary(self: Self) -> Diary:
        diary = Diary()
        query = select(ORMNote).where(ORMNote.owner_id == self.owner_id)
        results: Sequence[ORMNote] = self.session.execute(query).scalars().all()
        diary._notes = {
            NoteValueObject.model_validate(
                obj=note,
                from_attributes=True,
            )
            for note in results
        }
        return diary
