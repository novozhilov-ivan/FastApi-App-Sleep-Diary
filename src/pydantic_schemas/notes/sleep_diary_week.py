from datetime import time
from typing_extensions import Annotated

from pydantic import BaseModel, computed_field, Field, ConfigDict

from src.pydantic_schemas.notes.sleep_notes import SleepNoteModel, SleepNoteStatisticCompute


class SleepDiaryWeeklyStatistic(BaseModel):
    days_count: int
    average_sleep_duration: time | None = None
    average_time_spent_in_bed: time | None = None
    average_sleep_efficiency: float


class SleepDiaryWeeklyNotesModel(BaseModel):
    notes: list[SleepNoteModel]


class SleepDiaryWeekModel(
    SleepDiaryWeeklyNotesModel,
    SleepDiaryWeeklyStatistic,
):
    model_config = ConfigDict(from_attributes=True)


class SleepDiaryWeeklyNotes(BaseModel):
    notes: Annotated[
        list[SleepNoteStatisticCompute],
        Field(
            default=[],
            min_length=1,
            max_length=7
        )
    ]


class SleepDiaryWeekCompute(SleepDiaryWeeklyNotes):
    @computed_field
    @property
    def days_count(self) -> int:
        return len(self.notes)

    @computed_field
    @property
    def average_sleep_duration(self) -> time | None:
        if not self.notes:
            return None
        sleep_duration = 0
        for note in self.notes:
            sleep_duration += note.sleep_duration.hour * 60 + note.sleep_duration.minute
        average = sleep_duration // self.days_count
        return time(
            hour=average // 60,
            minute=average % 60
        )

    @computed_field
    @property
    def average_time_spent_in_bed(self) -> time | None:
        if not self.notes:
            return time(0, 0)
        in_bed_duration = 0
        for note in self.notes:
            in_bed_duration += note.time_spent_in_bed.hour * 60 + note.time_spent_in_bed.minute
        average = in_bed_duration // self.days_count
        return time(
            hour=average // 60,
            minute=average % 60
        )

    @computed_field
    @property
    def average_sleep_efficiency(self) -> float:
        sleep_duration = self.average_sleep_duration.hour * 60 + self.average_sleep_duration.minute
        if sleep_duration == 0:
            return 0
        time_spent_in_bed = self.average_time_spent_in_bed.hour * 60 + self.average_time_spent_in_bed.minute

        return round(sleep_duration / time_spent_in_bed * 100, 2)
