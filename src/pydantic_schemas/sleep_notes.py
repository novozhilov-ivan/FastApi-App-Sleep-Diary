from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field


class SleepNoteDateTimes(BaseModel):
    calendar_date: date | str
    bedtime: time | str
    asleep: time | str
    awake: time | str
    rise: time | str
    time_of_night_awakenings: time | str = Field(
        alias='without_sleep'
    )

    model_config = ConfigDict(from_attributes=True)


class SleepNoteBase(SleepNoteDateTimes):
    id: int
    user_id: int




class WeeklySleepDiaryStatistics(BaseModel):
    average_sleep_efficiency: float
    average_sleep_time: time
    average_time_spent_in_bed: time


class WeeksSleepDiary(BaseModel):
    weekly_statistics: WeeklySleepDiaryStatistics | None
    days: list[SleepNoteBase] = Field(
        max_length=7
    )


class SleepDiaryEntries(BaseModel):
    notes_count: int | None
    weeks_count: int | None
    weeks: list[WeeksSleepDiary]

    model_config = ConfigDict(from_attributes=True)
