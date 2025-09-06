from datetime import date
from typing import Self

from pydantic import BaseModel

from src.domain.sleep_diary.dtos import WeekInfo


class WeekInfoSchema(BaseModel):
    start_date: date
    filled_notes_count: int

    @classmethod
    def from_week(cls, week: WeekInfo) -> Self:
        return cls(
            start_date=week.start_date,
            filled_notes_count=week.filled_notes_count,
        )


class AllWeeksInfoSchema(BaseModel):
    weeks: list[WeekInfoSchema]

    @classmethod
    def from_week_list(cls, obj: list[WeekInfo]) -> Self:
        return cls(
            weeks=[WeekInfoSchema.from_week(week) for week in obj],
        )
