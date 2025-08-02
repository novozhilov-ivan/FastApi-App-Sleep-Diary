from dataclasses import dataclass
from datetime import date, time
from uuid import UUID

from src.domain.sleep_diary.entities.note import NoteEntity
from src.domain.sleep_diary.exceptions.write import NonUniqueNoteBedtimeDateException
from src.domain.sleep_diary.services.base import INotesRepository
from src.domain.sleep_diary.services.diary import DiaryService
from src.domain.sleep_diary.values.points import Points


@dataclass
class Diary:
    repository: INotesRepository

    def write(
        self,
        owner_oid: UUID,
        bedtime_date: date,
        went_to_bed: time,
        fell_asleep: time,
        woke_up: time,
        got_up: time,
        no_sleep: time | None = None,
    ) -> None:
        note = NoteEntity(
            owner_oid=owner_oid,
            points=Points(
                bedtime_date=bedtime_date,
                went_to_bed=went_to_bed,
                fell_asleep=fell_asleep,
                woke_up=woke_up,
                got_up=got_up,
                no_sleep=no_sleep or time(),
            ),
        )
        diary = DiaryService.create(
            notes=self.repository.get_all_notes(owner_oid),
        )

        if not diary.can_write(note):
            raise NonUniqueNoteBedtimeDateException(note.points.bedtime_date)

        diary.write(note)
        self.repository.add(note)
