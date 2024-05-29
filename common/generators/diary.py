from datetime import date, datetime, time, timezone
from random import randrange
from typing import Type

from api.utils.manage_notes import slice_on_week
from common.pydantic_schemas.sleep.diary import SleepDiaryCompute, SleepDiaryModel
from common.pydantic_schemas.sleep.notes import SleepNoteWithStats


class SleepDiaryGenerator:
    def __init__(self, user_id: int = 1, notes_count: int = 1):
        self.user_id: int = user_id
        self.notes_count: int = notes_count
        self.notes: list[SleepNoteWithStats] = self._create_notes()
        self.diary: SleepDiaryModel = self._build_sleep_diary()

    def convert_model(self, model: Type, by_alias=True, **kw):
        converted_notes = []
        for note in self.notes:
            converted_note = model(**note.model_dump(by_alias=by_alias, **kw))
            converted_notes.append(converted_note)
        return converted_notes

    @staticmethod
    def _rand_time(
        start_h: int = 0,
        stop_h: int = 23,
        start_m: int = 0,
        stop_m: int = 59,
    ) -> time:
        hour, minute = 0, 0
        if start_h or stop_h:
            hour = randrange(start_h, stop_h)
        if start_m or stop_m:
            minute = randrange(start_m, stop_m)
        return time(hour, minute)

    def create_note(
        self,
        note_id: int = 1,
        date_of_note: float | None = None,
    ) -> SleepNoteWithStats:
        if date_of_note is None:
            date_of_note = datetime.now(timezone.utc).timestamp()
        rand_went_to_bed = self._rand_time()
        rand_fell_asleep = self._rand_time(
            start_h=rand_went_to_bed.hour, start_m=rand_went_to_bed.minute
        )
        rand_woke_up = self._rand_time(
            start_h=rand_fell_asleep.hour, start_m=rand_fell_asleep.minute
        )
        rand_got_up = self._rand_time(
            start_h=rand_woke_up.hour, start_m=rand_woke_up.minute
        )
        rand_no_sleep = self._rand_time(
            stop_h=rand_woke_up.hour - rand_fell_asleep.hour,
            stop_m=rand_woke_up.minute - rand_fell_asleep.minute,
        )
        return SleepNoteWithStats(
            id=note_id,
            user_id=self.user_id,
            sleep_date=date.fromtimestamp(date_of_note),
            went_to_bed=rand_went_to_bed,
            fell_asleep=rand_fell_asleep,
            woke_up=rand_woke_up,
            got_up=rand_got_up,
            no_sleep=rand_no_sleep,
        )

    def _create_notes(self, start_note_id: int = 1) -> list[SleepNoteWithStats]:
        self.notes = []
        self._generate_notes_data(start_note_id)
        return self.notes

    def _generate_notes_data(self, start_note_id) -> None:
        date_of_note = datetime.now(timezone.utc).timestamp()
        seconds_in_day = 60 * 60 * 24
        for note_id, note in enumerate(range(self.notes_count), start=start_note_id):
            date_of_note += seconds_in_day
            note = self.create_note(note_id, date_of_note)
            self.notes.append(note)

    def _build_sleep_diary(self) -> SleepDiaryModel:
        pd_weeks = slice_on_week(self.notes)
        sleep_diary = SleepDiaryCompute(weeks=pd_weeks)
        return SleepDiaryModel.model_validate(sleep_diary)
