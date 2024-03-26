from datetime import time, date

from pydantic import AliasChoices, BaseModel, Field, ConfigDict, computed_field


class SleepNote(BaseModel):
    calendar_date: date
    bedtime: time
    asleep: time
    awake: time
    rise: time
    time_of_night_awakenings: time = Field(
        alias='without_sleep',
        validation_alias=AliasChoices(
            "time_of_night_awakenings",
            "without_sleep"
        ),
    )
    model_config = ConfigDict(from_attributes=True)


class SleepNoteStatistics(SleepNote):
    sleep_duration: time
    time_spent_in_bed: time
    sleep_efficiency: float


class SleepNoteMeta(BaseModel):
    id: int
    user_id: int


class SleepNoteModel(
    SleepNoteStatistics,
    SleepNoteMeta
):
    model_config = ConfigDict(from_attributes=True)


class SleepNoteCompute(SleepNote, SleepNoteMeta):
    @staticmethod
    def time_to_minutes(time_point: time) -> int:
        return time_point.hour * 60 + time_point.minute

    @staticmethod
    def time_diff(subtractor: time, subtrahend: time) -> int:
        diff = SleepNoteCompute.time_to_minutes(subtractor)
        diff -= SleepNoteCompute.time_to_minutes(subtrahend)
        return diff

    @staticmethod
    def minutes_to_time(minutes: int) -> time:
        return time(
            hour=minutes // 60,
            minute=minutes % 60
        )

    @computed_field
    @property
    def sleep_duration(self) -> time:
        minutes_of_sleep = self.time_diff(self.awake, self.asleep)
        minutes_of_sleep -= self.time_to_minutes(self.time_of_night_awakenings)
        return self.minutes_to_time(minutes_of_sleep)

    @computed_field
    @property
    def time_spent_in_bed(self) -> time:
        minutes_in_bed = self.time_diff(self.rise, self.bedtime)
        return self.minutes_to_time(minutes_in_bed)

    @computed_field
    @property
    def sleep_efficiency(self) -> float:
        minutes_of_sleep = self.time_to_minutes(self.sleep_duration)
        minutes_in_bed = self.time_to_minutes(self.time_spent_in_bed)
        if minutes_of_sleep == 0:
            return 0
        return round(minutes_of_sleep / minutes_in_bed * 100, 2)
