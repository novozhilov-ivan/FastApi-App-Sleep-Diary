from datetime import time, date

from pydantic import AliasChoices, BaseModel, Field, ConfigDict


class SleepNoteMain(BaseModel):
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


class SleepNoteMetaData(BaseModel):
    id: int
    user_id: int


class SleepNoteModel(
    SleepNoteMain,
    SleepNoteMetaData
):
    model_config = ConfigDict(
        from_attributes=True
    )
