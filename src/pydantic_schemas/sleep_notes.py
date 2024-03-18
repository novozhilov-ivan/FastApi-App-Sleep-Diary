from datetime import date, time

from pydantic import BaseModel


class SleepNoteBase(BaseModel):
    date: date
    bedtime: time
    asleep: time
    awake: time
    rise: time
    time_of_night_awakenings: time


class WeeklySleepDiaryStatistics(BaseModel):
    average_sleep_efficiency: float
    average_sleep_time: time
    average_time_spent_in_bed: time


class WeeksSleepDiary(BaseModel):
    weekly_statistics: WeeklySleepDiaryStatistics | None
    days: list[SleepNoteBase]


class SleepDiaryEntries(BaseModel):
    weeks_count: int | None
    notes_count: int | None
    weeks: list[WeeksSleepDiary]
