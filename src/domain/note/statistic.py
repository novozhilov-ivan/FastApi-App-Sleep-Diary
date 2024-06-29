from datetime import time

from src.domain.note import NoteBase, NoteDurations


class NoteStatistic(NoteDurations, NoteBase):
    sleep_duration: time
    time_spent_in_bed: time
    sleep_efficiency: float
