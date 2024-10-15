from datetime import date, datetime, time

from pydantic import UUID4, BaseModel, Field


class CreatePointsSchema(BaseModel):
    bedtime_date: date = Field(
        title="Дата отхода ко сну",
        examples=["2020-12-12", "2021-01-20"],
    )
    went_to_bed: time = Field(
        title="Время отхода ко сну",
        examples=["01:00", "13:00"],
    )
    fell_asleep: time = Field(
        title="Время засыпания",
        examples=["03:00", "15:00"],
    )
    woke_up: time = Field(
        title="Время пробуждения",
        examples=["11:00", "23:00"],
    )
    got_up: time = Field(
        title="Время подъема",
        examples=["13:00", "01:00"],
    )
    no_sleep: time = Field(
        default=time(hour=0, minute=0),
        title="Время отсутствия сна",
        examples=["00:00", "00:20"],
    )


class NoteResponseSchema(BaseModel):
    oid: UUID4
    created_at: datetime
    updated_at: datetime
    owner_oid: UUID4
    points: CreatePointsSchema
