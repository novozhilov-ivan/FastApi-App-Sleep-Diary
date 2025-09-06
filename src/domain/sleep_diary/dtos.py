from dataclasses import dataclass
from datetime import date


@dataclass
class Week:
    number: int
    start_date: date
    filled_notes_count: int
