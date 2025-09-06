from datetime import date
from typing import Self

from pydantic import BaseModel, computed_field

from src.domain.sleep_diary.dtos import Week


class WeekInfoSchema(BaseModel):
    number: int
    start_date: date
    filled_notes_count: int

    @classmethod
    def from_week(cls, week: Week) -> Self:
        return cls(
            number=week.number,
            start_date=week.start_date,
            filled_notes_count=week.filled_notes_count,
        )


class AllWeeksInfoSchema(BaseModel):
    weeks: list[WeekInfoSchema]

    @computed_field
    def total_user_weeks(self) -> int:
        return len(self.weeks)

    @classmethod
    def from_week_list(cls, obj: list[Week]) -> Self:
        return cls(weeks=[WeekInfoSchema.from_week(week) for week in obj])
