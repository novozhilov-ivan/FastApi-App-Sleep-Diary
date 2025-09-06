from dataclasses import dataclass
from datetime import date


@dataclass
class WeekInfo:
    start_date: date
    filled_notes_count: int
