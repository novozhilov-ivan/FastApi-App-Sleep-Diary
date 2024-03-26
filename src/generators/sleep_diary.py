from random import randrange

from datetime import date, time, timezone, datetime

from sleep_diary_api.Utils.manage_notes import slice_on_week
from src.pydantic_schemas.notes.sleep_diary import SleepDiaryEntriesCompute, SleepDiaryEntriesModel
from src.pydantic_schemas.notes.sleep_notes import SleepNoteCompute


class SleepDiaryGenerator:
    @staticmethod
    def rand_time(
            start_h: int = 0, stop_h: int = 23,
            start_m: int = 0, stop_m: int = 59,
    ) -> time:
        hour, minute = 0, 0
        if start_h or stop_h:
            hour = randrange(start_h, stop_h)
        if start_m or stop_m:
            minute = randrange(start_m, stop_m)

        return time(hour, minute)

    @staticmethod
    def create_notes(
            user_id: int,
            notes_count: int,
    ) -> list[SleepNoteCompute]:
        notes = []
        new_date = datetime.now(timezone.utc).timestamp()

        for i in range(notes_count):
            new_date += 60 * 60 * 24
            generate_time = SleepDiaryGenerator.rand_time
            rand_bedtime = generate_time()
            rand_asleep = generate_time(start_h=rand_bedtime.hour, start_m=rand_bedtime.minute)
            rand_awake = generate_time(start_h=rand_asleep.hour, start_m=rand_asleep.minute)
            rand_rise = generate_time(start_h=rand_awake.hour, start_m=rand_awake.minute)
            rand_time_of_night_awakenings = generate_time(
                stop_h=rand_awake.hour - rand_asleep.hour,
                stop_m=rand_awake.minute - rand_asleep.minute
            )
            new_note = SleepNoteCompute(
                id=i,
                user_id=user_id,
                calendar_date=date.fromtimestamp(new_date),
                bedtime=rand_bedtime,
                asleep=rand_asleep,
                awake=rand_awake,
                rise=rand_rise,
                time_of_night_awakenings=rand_time_of_night_awakenings,
            )
            notes.append(new_note)
        return notes

    @staticmethod
    def build(
            user_id: int = 1,
            notes_count: int = 7,
            notes: list[SleepNoteCompute] | None = None,
    ) -> SleepDiaryEntriesModel:
        if notes is None:
            notes = SleepDiaryGenerator.create_notes(user_id, notes_count)

        pd_weeks = slice_on_week(notes)
        sleep_diary = SleepDiaryEntriesCompute(weeks=pd_weeks)
        return SleepDiaryEntriesModel.model_validate(sleep_diary)
