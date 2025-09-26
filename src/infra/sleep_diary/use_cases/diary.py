from dataclasses import dataclass
from datetime import date, time
from uuid import UUID

from src.domain.sleep_diary.entities.note import NoteEntity
from src.domain.sleep_diary.exceptions.write import (
    NonUniqueNoteBedtimeDateError,
    NoteNotFoundError,
)
from src.domain.sleep_diary.repositories.base import INotesRepository
from src.domain.sleep_diary.services.diary import DiaryService
from src.domain.sleep_diary.values.points import Points
from src.infra.sleep_diary.commands import DeleteNoteCommand, EditNoteCommand


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
            raise NonUniqueNoteBedtimeDateError(note.points.bedtime_date)

        diary.write(note)
        self.repository.add(note)

    def edit(self, command: EditNoteCommand) -> None:
        note: NoteEntity | None = self.repository.get_by_bedtime_date(
            bedtime_date=command.note_date,
            owner_oid=command.owner_oid,
        )
        if note is None:
            raise NoteNotFoundError

        command.edit_note(note)

        self.repository.update(note)

    def delete(self, command: DeleteNoteCommand) -> None:
        note: NoteEntity | None = self.repository.get_by_bedtime_date(
            bedtime_date=command.note_date,
            owner_oid=command.owner_oid,
        )

        if note:
            self.repository.delete(note)
