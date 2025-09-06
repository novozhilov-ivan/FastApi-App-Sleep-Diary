from dataclasses import dataclass
from datetime import date

from src.domain.sleep_diary.entities.note import NoteEntity


@dataclass
class WeekInfo:
    start_date: date
    filled_notes_count: int


@dataclass
class WeekNotes:
    notes: list[NoteEntity]
