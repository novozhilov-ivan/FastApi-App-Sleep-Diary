from dataclasses import dataclass
from datetime import date
from typing import ClassVar

from src.domain.sleep_diary.entities.note import NoteEntity


@dataclass
class WeekInfo:
    start_date: date
    filled_notes_count: int


@dataclass
class WeekNotes:
    notes: list[NoteEntity]


class AboutInfo:
    description: ClassVar[str] = (
        "Ежедневный учет времени отхода ко сну, засыпания, пробуждения и "
        "подъема, а также времени нахождения в кровати без сна. "
        "После заполнения одного дня, будет рассчитано время сна и время "
        "проведенное в кровати, затем на их основе определяется "
        "эффективность сна. Также, при заполнении дневника сна, "
        "рассчитывается средняя эффективность и время сна в рамках "
        "одной недели."
    )
