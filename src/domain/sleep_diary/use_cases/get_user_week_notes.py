from dataclasses import dataclass
from datetime import date
from uuid import UUID

from src.domain.sleep_diary.dtos import WeekNotes
from src.domain.sleep_diary.repositories.base import IWeeksRepository
from src.domain.sleep_diary.use_cases.base import IGetUserIdentityUseCase


@dataclass
class GetUserWeekNotesUseCase:
    get_user_identity: IGetUserIdentityUseCase
    weeks_repository: IWeeksRepository

    def __call__(self, start_date: date) -> WeekNotes:
        user_oid = self.get_user_identity()

        return self.weeks_repository.get_user_week_notes(
            owner_oid=UUID(user_oid),
            start_date=start_date,
        )
