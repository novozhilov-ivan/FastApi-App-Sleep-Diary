from typing import Any

from sqlalchemy.orm import Session

from src import domain
from src.domain.note import NoteTimePoints
from src.repository.base import BaseDiaryRepository


def write(
    note_time_points: NoteTimePoints,
    repo: BaseDiaryRepository,
    session: Session | Any,
) -> None:
    diary = repo.get_diary()
    domain.write(note_time_points, diary)
    session.commit()
