from typing import Type

from more_itertools import batched
from pydantic import TypeAdapter, BaseModel
from sqlalchemy import Sequence

from api.models import Notation
from common.pydantic_schemas.sleep.weeks import SleepDiaryWeekCompute
from common.pydantic_schemas.sleep.notes import SleepNoteCompute, SleepNote


def slice_on_week(days: list[SleepNoteCompute]) -> list[SleepDiaryWeekCompute]:
    weeks = []
    week_len = 7
    for notes_batch in batched(days, week_len):
        week = SleepDiaryWeekCompute(notes=[*notes_batch])
        weeks.append(week)
    return weeks


def convert_notes(
        db_notes: Sequence[Notation],
        model: Type[SleepNoteCompute | SleepNote] = SleepNoteCompute
) -> list[SleepNoteCompute | SleepNote]:
    type_adapter = TypeAdapter(list[model])
    return type_adapter.validate_python(db_notes, from_attributes=True)


class WriteData:
    def __init__(
            self,
            data: list[BaseModel],
            model: SleepNote | Type[BaseModel] = SleepNote
    ):
        self.data: list[BaseModel] = data
        self.model: SleepNote | Type[BaseModel] = model

    def to_csv_str(self) -> str:
        rows_delimiter = '\n'
        columns_delimiter = ','
        titles = (field.title for field in self.model.model_fields.values())
        data = (note.model_dump() for note in self.data)
        data = (self.model(**note) for note in data)
        data = (note.model_dump(mode='json') for note in data)
        data = (note.values() for note in data)
        data = (columns_delimiter.join(row) for row in data)
        return (
            f"{columns_delimiter.join(titles)}"
            f"\n"
            f"{rows_delimiter.join(data)}"
        )
