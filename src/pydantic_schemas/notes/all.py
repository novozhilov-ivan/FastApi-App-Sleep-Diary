from datetime import time

from pydantic import BaseModel, conlist, computed_field

from src.pydantic_schemas.notes.sleep_notes import SleepNoteModel


class WeeklySleepDiaryStatistics(BaseModel):
    average_sleep_efficiency: float
    average_sleep_time: time
    average_time_spent_in_bed: time


class WeeksSleepDiary(BaseModel):
    @computed_field
    @property
    def weekly_statistics(self) -> WeeklySleepDiaryStatistics | None:
        return None

    days: conlist(
        SleepNoteModel,
        min_length=1,
        max_length=7
    )





