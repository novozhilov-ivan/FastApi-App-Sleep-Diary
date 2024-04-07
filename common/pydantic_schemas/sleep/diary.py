from typing import Annotated

from pydantic import BaseModel, ConfigDict, computed_field, Field

from common.pydantic_schemas.sleep.weeks import SleepDiaryWeekModel, SleepDiaryWeekCompute


class SleepDiaryStatisticModel(BaseModel):
    notes_count: int
    weeks_count: int


class SleepDiaryDataModel(BaseModel):
    weeks: list[SleepDiaryWeekModel]


class SleepDiaryModel(SleepDiaryDataModel, SleepDiaryStatisticModel):
    """Дневника сна пользователя с записями и информацией о количестве записей"""
    model_config = ConfigDict(from_attributes=True)


class SleepDiaryModelEmpty(SleepDiaryModel):
    """Дневника сна без записей"""
    notes_count: int = 0
    weeks_count: int = 0
    weeks: list = []


class SleepDiaryDataCompute(BaseModel):
    weeks: list[SleepDiaryWeekCompute]


class SleepDiaryCompute(SleepDiaryDataCompute):
    @computed_field
    @property
    def notes_count(self) -> int:
        if not self.weeks:
            return 0
        days_in_weeks = map(lambda week: len(week.notes), self.weeks)
        days_count = sum(days_in_weeks)
        return days_count

    @computed_field
    @property
    def weeks_count(self) -> int:
        return len(self.weeks)
