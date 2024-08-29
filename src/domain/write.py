from src.domain.diary import Diary
from src.domain.errors import ErrorNoteAlreadyExist
from src.domain.note import NoteTimePoints, NoteValueObject


def write(note: NoteTimePoints, diary: Diary) -> NoteValueObject:
    note_to_write = NoteValueObject.model_validate(
        obj=note,
        from_attributes=True,
    )
    if diary.can_write(note_to_write):
        diary.write(note_to_write)
        return note_to_write
    raise ErrorNoteAlreadyExist(
        f"Запись о сне с датой {note.bedtime_date} уже существует в дневнике.",
    )
