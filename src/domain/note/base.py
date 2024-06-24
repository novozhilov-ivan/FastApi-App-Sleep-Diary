import abc
from datetime import date, time
from typing import Annotated

from pydantic import BaseModel, Field

bedtime_date_type = Annotated[
    date,
    Field(
        title="Дата",
        description="",
        examples=[
            "2020-12-12",
            "2021-12-13",
        ],
    ),
]
went_to_bed_type = Annotated[
    time,
    Field(
        title="Лег",
        description="",
        examples=[
            "00:10",
            "01:55",
        ],
    ),
]
fell_asleep_type = Annotated[
    time,
    Field(
        title="Уснул",
        description="",
        examples=[
            "00:30",
            "02:20",
        ],
    ),
]
woke_up_type = Annotated[
    time,
    Field(
        title="Проснулся",
        description="",
        examples=[
            "08:40",
            "07:57",
        ],
    ),
]
got_up_type = Annotated[
    time,
    Field(
        title="Встал",
        description="",
        examples=[
            "09:00",
            "08:07",
        ],
    ),
]
no_sleep_type = Annotated[
    time,
    Field(
        default=time(
            hour=0,
            minute=0,
        ),
        title="Не спал",
        description="",
        examples=[
            "00:10",
            "00:32",
        ],
    ),
]


class NoteBase(BaseModel, abc.ABC):
    bedtime_date: bedtime_date_type
    went_to_bed: went_to_bed_type
    fell_asleep: fell_asleep_type
    woke_up: woke_up_type
    got_up: got_up_type
    no_sleep: no_sleep_type
