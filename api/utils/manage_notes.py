from typing import Type

from pydantic import TypeAdapter, BaseModel
from sqlalchemy import Sequence

from api.models import Notation
from common.pydantic_schemas.sleep.weeks import SleepDiaryWeekCompute
from common.pydantic_schemas.sleep.notes import SleepNoteCompute, SleepNote


def slice_on_week(days: list[SleepNoteCompute]) -> list[SleepDiaryWeekCompute]:
    weeks = []
    days_count = len(days)
    step = 7
    for f_day in range(0, days_count, step):
        l_day = f_day + step
        if l_day > days_count:
            l_day = days_count
        week = days[f_day:l_day]
        pd_compute_week = SleepDiaryWeekCompute(notes=week)
        weeks.append(pd_compute_week)
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
        titles_row = (field.title for field in self.model.model_fields.values())
        data = (note.model_dump(mode='json') for note in self.data)
        rows_rows = (note.values() for note in data)
        rows_rows = (','.join(row) for row in rows_rows)
        delimiter = '\n'
        result = f"{','.join(titles_row)}\n{delimiter.join(rows_rows)}"
        return result
