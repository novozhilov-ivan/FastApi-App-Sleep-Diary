from datetime import date, time
from functools import reduce

from pydantic import BaseModel, ConfigDict, Field, AliasChoices, conlist, computed_field


class SleepNoteDateTimes(BaseModel):
    calendar_date: date | str
    bedtime: time | str
    asleep: time | str
    awake: time | str
    rise: time | str
    time_of_night_awakenings: time | str = Field(
        validation_alias=AliasChoices(
            "time_of_night_awakenings",
            "without_sleep"
        ),
    )
    model_config = ConfigDict(
        from_attributes=True
    )


class SleepNote(SleepNoteDateTimes):
    id: int
    user_id: int


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
        SleepNote,
        min_length=1,
        max_length=7
    )





