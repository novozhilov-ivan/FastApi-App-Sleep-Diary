from pydantic import BaseModel, ConfigDict, computed_field

from src.pydantic_schemas.notes.all import WeeksSleepDiary


class SleepDiaryEntriesStats(BaseModel):
    notes_count: int | None
    weeks_count: int | None


class SleepDiaryEntriesData(BaseModel):
    weeks: list[WeeksSleepDiary]


class SleepDiaryEntriesModel(
    SleepDiaryEntriesData,
    SleepDiaryEntriesStats,
):
    model_config = ConfigDict(from_attributes=True)


class SleepDiaryEntriesComputeStatistic(SleepDiaryEntriesData):
    @computed_field
    @property
    def notes_count(self) -> int | None:
        if not self.weeks:
            return None
        days_in_weeks = map(lambda week: len(week.days), self.weeks)
        days_count = sum(days_in_weeks)
        return days_count

    @computed_field
    @property
    def weeks_count(self) -> int | None:
        if not self.weeks:
            return None
        return len(self.weeks)
