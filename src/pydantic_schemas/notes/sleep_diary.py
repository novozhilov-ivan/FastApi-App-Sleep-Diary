from typing import Annotated

from pydantic import BaseModel, ConfigDict, computed_field, Field

from src.pydantic_schemas.notes.sleep_diary_week import SleepDiaryWeekModel, SleepDiaryWeekCompute


class SleepDiaryEntriesStats(BaseModel):
    notes_count: int
    weeks_count: int


class SleepDiaryEntriesDataModel(BaseModel):
    weeks: list[SleepDiaryWeekModel]


class SleepDiaryEntriesModel(
    SleepDiaryEntriesDataModel,
    SleepDiaryEntriesStats,
):
    model_config = ConfigDict(from_attributes=True)


class SleepDiaryEntriesData(BaseModel):
    weeks: Annotated[
        list[SleepDiaryWeekCompute],
        Field(
            default=[],
            min_length=1
        )
    ]


class SleepDiaryEntriesStatisticCompute(SleepDiaryEntriesData):
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
