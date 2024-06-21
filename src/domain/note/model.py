import abc
from datetime import date, time

from pydantic import BaseModel, Field


class NoteBase(BaseModel, abc.ABC):
    bedtime_date: date = Field(
        title="Дата",
        description="",
        examples=["2021-12-13", "2021-12-14"]
    )
    went_to_bed: time = Field(
        title="Лег",
        description="",
        examples=["05:11", "01:55"]
    )
    fell_asleep: time = Field(
        title="Уснул",
        description="",
        examples=["05:30", "02:20"]
    )
    woke_up: time = Field(
        title="Проснулся",
        description="",
        examples=["12:00", "07:57"]
    )
    got_up: time = Field(
        title="Встал",
        description="",
        examples=["12:15", "08:07"]
    )
    no_sleep: time = Field(
        title="Не спал",
        description="",
        examples=["00:19", "00:32"]
    )


class Note(NoteBase):
    ...
