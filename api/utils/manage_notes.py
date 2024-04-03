from pydantic import TypeAdapter
from sqlalchemy import Sequence

from api.models import Notation
from common.pydantic_schemas.notes.sleep_diary_week import SleepDiaryWeekCompute
from common.pydantic_schemas.notes.sleep_notes import SleepNoteCompute


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


def convert_notes(db_notes: Sequence[Notation]) -> list[SleepNoteCompute]:
    type_adapter = TypeAdapter(list[SleepNoteCompute])
    return type_adapter.validate_python(db_notes, from_attributes=True)
