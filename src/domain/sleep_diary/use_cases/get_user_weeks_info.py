from dataclasses import dataclass
from uuid import UUID

from src.domain.sleep_diary.dtos import WeekInfo
from src.domain.sleep_diary.repositories.base import IWeeksRepository
from src.domain.sleep_diary.use_cases.base import IGetUserIdentityUseCase


@dataclass
class GetUserWeeksInfoUseCase:
    get_user_identity: IGetUserIdentityUseCase
    weeks_repository: IWeeksRepository

    def __call__(self) -> list[WeekInfo]:
        user_oid = self.get_user_identity()

        return self.weeks_repository.get_weeks_info(UUID(user_oid))
