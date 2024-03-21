from datetime import time, date

from pydantic import AliasChoices, BaseModel, Field, ConfigDict, computed_field


class SleepNote(BaseModel):
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
    model_config = ConfigDict(from_attributes=True)


class SleepNoteStatistics(SleepNote):
    sleep_duration: time | None = None
    time_spent_in_bed: time | None = None
    sleep_efficiency: float = 0


class SleepNoteMeta(BaseModel):
    id: int
    user_id: int


class SleepNoteModel(
    SleepNoteStatistics,
    SleepNoteMeta
):
    model_config = ConfigDict(from_attributes=True)


class SleepNoteStatisticCompute(SleepNote):
    @computed_field
    @property
    def sleep_duration(self) -> time | None:
        awake = self.awake.hour * 60 + self.awake.minute
        asleep = self.asleep.hour * 60 + self.asleep.minute
        sleep_duration = awake - asleep
        return time(
            hour=sleep_duration // 60,
            minute=sleep_duration % 60
        )

    @computed_field
    @property
    def time_spent_in_bed(self) -> time | None:
        rise = self.rise.hour * 60 + self.rise.minute
        bedtime = self.bedtime.hour * 60 + self.bedtime.minute
        in_bed_duration = rise - bedtime
        return time(
            hour=in_bed_duration // 60,
            minute=in_bed_duration % 60
        )

    @computed_field
    @property
    def sleep_efficiency(self) -> float:
        sleep_duration = self.sleep_duration.hour * 60 + self.sleep_duration.minute
        time_spent_in_bed = self.time_spent_in_bed.hour * 60 + self.time_spent_in_bed.minute
        if sleep_duration == 0:
            return 0
        return round(sleep_duration / time_spent_in_bed * 100, 2)
