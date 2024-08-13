from sqlalchemy.orm import Session

from src.domain.note import NoteTimePoints, NoteValueObject
from src.repositories.base import BaseDiaryRepository


def write(
    note_time_points: NoteTimePoints,
    repo: BaseDiaryRepository,
    session: Session,
) -> str:
    new_note = NoteValueObject.model_validate(note_time_points)
    diary = repo.get_all()
