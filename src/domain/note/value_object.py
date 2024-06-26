from src.domain.note.base import NoteBase
from src.domain.note.validators import NoteFieldsValidators


class NoteValueObject(
    NoteFieldsValidators,
    NoteBase,
): ...
