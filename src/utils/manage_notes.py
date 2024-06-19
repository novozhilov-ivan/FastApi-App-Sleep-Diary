from typing import Iterable, Type

from more_itertools import batched
from pydantic import BaseModel, TypeAdapter
from werkzeug.datastructures import FileStorage

from src.models import SleepNoteOrm
from src.pydantic_schemas.sleep.notes import SleepNote, SleepNoteWithStats
from src.pydantic_schemas.sleep.weeks import SleepDiaryWeekCompute


def slice_on_week(days: list[SleepNoteWithStats]) -> list[SleepDiaryWeekCompute]:
    weeks = []
    week_len = 7
    for notes_batch in batched(days, week_len):
        week = SleepDiaryWeekCompute(notes=[*notes_batch])
        weeks.append(week)
    return weeks


def convert_db_notes_to_pydantic_model_notes(
    db_notes: Iterable[SleepNoteOrm],
    model: Type[SleepNoteWithStats | SleepNote] = SleepNoteWithStats,
) -> list[SleepNoteWithStats | SleepNote]:
    type_adapter = TypeAdapter(list[model])

    return type_adapter.validate_python(db_notes, from_attributes=True)


class FileDataConverter:
    def __init__(
        self,
        data: list[BaseModel] | None = None,
        file: FileStorage | None = None,
        model: SleepNote | Type[BaseModel] = SleepNote,
    ):
        self.data: list | None = data
        self.model: SleepNote | Type[BaseModel] = model
        self._file: FileStorage | None = file

    def to_csv_str(self) -> str:
        rows_delimiter = "\n"
        columns_delimiter = ","
        titles = (field.title for field in self.model.model_fields.values())
        data = (note.model_dump() for note in self.data)
        data = (self.model(**note) for note in data)
        data = (note.model_dump(mode="json") for note in data)
        data = (note.values() for note in data)
        data = (columns_delimiter.join(row) for row in data)
        return (
            f"{columns_delimiter.join(titles)}" f"\n" f"{rows_delimiter.join(data)}"
        )

    def to_model(self, as_model: SleepNote | type = SleepNote, **kwargs) -> None:
        with self._file.stream as file:
            reader: str = file.read().decode()

        lines = (line for line in reader.splitlines())
        lines_split = (line.split(",") for line in lines)
        next(lines_split)
        fields_names = [
            field[1].alias if getattr(field[1], "alias") else field[0]
            for field in self.model.model_fields.items()
        ]
        data_zips = (zip(fields_names, line) for line in lines_split)
        data_dicts = (dict(zipped_data) for zipped_data in data_zips)
        notes = (as_model(**data_dict, **kwargs) for data_dict in data_dicts)
        self.data = list(notes)
