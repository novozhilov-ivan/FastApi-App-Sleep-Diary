from dataclasses import dataclass
from datetime import date, time
from uuid import UUID

from src.domain.sleep_diary.entities.note import NoteEntity
from src.domain.sleep_diary.values.points import Points


@dataclass
class EditNoteCommand:
    owner_oid: UUID
    note_date: date
    went_to_bed: time | None = None
    fell_asleep: time | None = None
    woke_up: time | None = None
    got_up: time | None = None
    no_sleep: time | None = None

    def edit_note(self, note_entity: NoteEntity) -> None:
        note_entity.points = Points(
            bedtime_date=note_entity.points.bedtime_date,
            went_to_bed=self.went_to_bed or note_entity.points.went_to_bed,
            fell_asleep=self.fell_asleep or note_entity.points.fell_asleep,
            woke_up=self.woke_up or note_entity.points.woke_up,
            got_up=self.got_up or note_entity.points.got_up,
            no_sleep=self.no_sleep or note_entity.points.no_sleep,
        )


@dataclass
class DeleteNoteCommand:
    owner_oid: UUID
    note_date: date
