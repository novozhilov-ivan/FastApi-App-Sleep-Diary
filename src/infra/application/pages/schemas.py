from datetime import date, time, timedelta
from typing import Self

from pydantic import BaseModel

from src.domain.sleep_diary.dtos import WeekNotes
from src.domain.sleep_diary.entities.note import NoteEntity


class NoteSchema(BaseModel):
    bedtime_date: date
    went_to_bed: time
    fell_asleep: time
    woke_up: time
    got_up: time
    no_sleep: time

    duration_sleep: timedelta
    duration_in_bed: timedelta
    duration_without_sleep: timedelta
    duration_sleep_minus_without_sleep: timedelta

    statistics_sleep: time
    statistics_in_bed: time
    statistics_sleep_minus_no_sleep: time
    statistics_sleep_efficiency: float

    @classmethod
    def from_entity(cls, note: NoteEntity) -> Self:
        return cls(
            bedtime_date=note.points.bedtime_date,
            went_to_bed=note.points.went_to_bed,
            fell_asleep=note.points.fell_asleep,
            woke_up=note.points.woke_up,
            got_up=note.points.got_up,
            no_sleep=note.points.no_sleep,
            duration_sleep=note.durations.sleep,
            duration_in_bed=note.durations.in_bed,
            duration_without_sleep=note.durations.without_sleep,
            duration_sleep_minus_without_sleep=note.durations.sleep_minus_without_sleep,
            statistics_sleep=note.statistics.sleep,
            statistics_in_bed=note.statistics.in_bed,
            statistics_sleep_minus_no_sleep=note.statistics.sleep_minus_no_sleep,
            statistics_sleep_efficiency=note.statistics.sleep_efficiency,
        )


class WeekNotesListSchema(BaseModel):
    week_notes: list[NoteSchema]

    @classmethod
    def from_week_notes(cls, obj: WeekNotes) -> Self:
        return cls(
            week_notes=[
                NoteSchema.from_entity(note_entity) for note_entity in obj.notes
            ],
        )
