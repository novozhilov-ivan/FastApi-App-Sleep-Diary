from datetime import time


from src.domain.note.base import NoteBase
from src.domain.note.durations import NoteDurations


class NoteStatistic(NoteDurations, NoteBase):
    sleep_duration: time
    time_spent_in_bed: time
    sleep_efficiency: float
