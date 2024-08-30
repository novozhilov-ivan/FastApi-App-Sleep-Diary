from src.domain.diary import Diary
from src.domain.exceptions import NonUniqueNoteBedtimeDateException
from src.domain.note import NoteTimePoints, NoteValueObject


def write(note: NoteTimePoints, diary: Diary) -> NoteValueObject:
    note_to_write = NoteValueObject.model_validate(
        obj=note,
        from_attributes=True,
    )
    if diary.can_write(note_to_write):
        diary.write(note_to_write)
        return note_to_write
    raise NonUniqueNoteBedtimeDateException(bedtime_date=note.bedtime_date)
