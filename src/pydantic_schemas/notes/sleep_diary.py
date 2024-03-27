from typing import Annotated

from pydantic import BaseModel, ConfigDict, computed_field, Field

from src.pydantic_schemas.notes.sleep_diary_week import SleepDiaryWeekModel, SleepDiaryWeekCompute


class SleepDiaryStatisticModel(BaseModel):
    notes_count: int
    weeks_count: int


class SleepDiaryDataModel(BaseModel):
    weeks: list[SleepDiaryWeekModel]


class SleepDiaryModel(SleepDiaryDataModel, SleepDiaryStatisticModel):
    model_config = ConfigDict(from_attributes=True)


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
