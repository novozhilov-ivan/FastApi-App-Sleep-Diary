from datetime import date, time

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, computed_field


class SleepNote(BaseModel):
    """Запись в дневник сна"""

    calendar_date: date = Field(
        title="Дата",
        examples=["2021-12-13", "2021-12-14", "2021-12-15", "2021-12-16"],
    )
    bedtime: time = Field(
        title="Лег",
        examples=["05:11", "01:55", "01:10", "04:10"],
    )
    asleep: time = Field(
        title="Уснул",
        examples=["05:30", "02:20", "01:30", "04:20"],
    )
    awake: time = Field(
        title="Проснулся",
        examples=["12:00", "07:57", "10:00", "11:50"],
    )
    rise: time = Field(
        title="Встал",
        examples=["12:15", "08:07", "10:30", "12:15"],
    )
    time_of_night_awakenings: time = Field(
        title="Не спал",
        examples=["00:19", "00:32", "00:06", "01:20"],
        alias="without_sleep",
        validation_alias=AliasChoices("time_of_night_awakenings", "without_sleep"),
    )
    model_config = ConfigDict(from_attributes=True)


class ListWithSleepNotes(BaseModel):
    notes: list[SleepNote]


class SleepNoteStatistics(SleepNote):
    sleep_duration: time
    time_spent_in_bed: time
    sleep_efficiency: float


class SleepNoteMeta(BaseModel):
    id: int = Field(title="Идентификатор записи дневника сна")
    user_id: int = Field(title="Идентификатор пользователя дневника сна")


class SleepNoteModel(SleepNoteStatistics, SleepNoteMeta):
    """Запись в дневнике сна со статистикой и идентификаторами пользователя и записи."""

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
        if minutes < 0:
            minutes = 0
        return time(hour=minutes // 60, minute=minutes % 60)

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
