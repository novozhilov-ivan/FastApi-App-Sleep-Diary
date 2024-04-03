from random import randrange

from datetime import date, time, timezone, datetime

from api.utils.manage_notes import slice_on_week
from common.pydantic_schemas.notes.sleep_diary import SleepDiaryCompute, SleepDiaryModel
from common.pydantic_schemas.notes.sleep_notes import SleepNoteCompute


class SleepDiaryGenerator:
    def __init__(self, user_id: int, notes_count: int):
        if notes_count < 1 or user_id < 1:
            raise ValueError(f"notes_count and user_id must be greater or equal 1.")
        if not isinstance(notes_count, int) or not isinstance(user_id, int):
            raise TypeError("notes_count and user_id must be integer.")

        self.user_id: int = user_id
        self.notes_count: int = notes_count
        self.notes: list[SleepNoteCompute] = self.create_notes()
        self.diary: SleepDiaryModel = self.build_sleep_diary()

    @staticmethod
    def _rand_time(
            start_h: int = 0, stop_h: int = 23,
            start_m: int = 0, stop_m: int = 59,
    ) -> time:
        hour, minute = 0, 0
        if start_h or stop_h:
            hour = randrange(start_h, stop_h)
        if start_m or stop_m:
            minute = randrange(start_m, stop_m)
        return time(hour, minute)

    def create_notes(self) -> list[SleepNoteCompute]:
        notes = []
        new_date = datetime.now(timezone.utc).timestamp()
        seconds_in_day = 60 * 60 * 24
        for i in range(self.notes_count):
            new_date += seconds_in_day
            rand_bedtime = self._rand_time()
            rand_asleep = self._rand_time(start_h=rand_bedtime.hour, start_m=rand_bedtime.minute)
            rand_awake = self._rand_time(start_h=rand_asleep.hour, start_m=rand_asleep.minute)
            rand_rise = self._rand_time(start_h=rand_awake.hour, start_m=rand_awake.minute)
            rand_time_of_night_awakenings = self._rand_time(
                stop_h=rand_awake.hour - rand_asleep.hour,
                stop_m=rand_awake.minute - rand_asleep.minute
            )
            new_note = SleepNoteCompute(
                id=i,
                user_id=self.user_id,
                calendar_date=date.fromtimestamp(new_date),
                bedtime=rand_bedtime,
                asleep=rand_asleep,
                awake=rand_awake,
                rise=rand_rise,
                time_of_night_awakenings=rand_time_of_night_awakenings,
            )
            notes.append(new_note)
        return notes

    def build_sleep_diary(self) -> SleepDiaryModel:
        pd_weeks = slice_on_week(self.notes)
        sleep_diary = SleepDiaryCompute(weeks=pd_weeks)
        return SleepDiaryModel.model_validate(sleep_diary)
