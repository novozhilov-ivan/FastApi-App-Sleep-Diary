from typing import Any

from sqlalchemy.orm import Session

from src import domain
from src.domain.note import NoteTimePoints
from src.repositories.base import BaseDiaryRepository


def write(
    note_time_points: NoteTimePoints,
    repo: BaseDiaryRepository,
    session: Session | Any,
) -> None:
    diary = repo.get_diary()
    note_to_adding = domain.write(note_time_points, diary)
    repo.add(note_to_adding)
    session.commit()
