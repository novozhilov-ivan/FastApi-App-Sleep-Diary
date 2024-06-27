import random
from datetime import date, datetime, time, timezone
from random import randrange
from typing import Literal, Type

from faker import Faker

from src.pydantic_schemas.sleep.notes import SleepNote, SleepNoteWithStats

faker = Faker()


class SleepNoteGenerator:
    def __init__(
        self,
        note_id: int = 1,
        date_of_note: float = datetime.now(timezone.utc).timestamp(),
    ):
        self.note = self.create_note()
        self.note_id: int = note_id
        self.date_of_note: float = date_of_note

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
        user_id: int = 1,
        date_of_note: float = datetime.now(timezone.utc).timestamp(),
        model: Type = SleepNoteWithStats,
    ) -> SleepNoteWithStats:
        rand_bedtime = self._rand_time()
        rand_asleep = self._rand_time(
            start_h=rand_bedtime.hour, start_m=rand_bedtime.minute
        )
        rand_awake = self._rand_time(
            start_h=rand_asleep.hour, start_m=rand_asleep.minute
        )
        rand_rise = self._rand_time(
            start_h=rand_awake.hour, start_m=rand_awake.minute
        )
        rand_time_of_night_awakenings = self._rand_time(
            stop_h=rand_awake.hour - rand_asleep.hour,
            stop_m=rand_awake.minute - rand_asleep.minute,
        )
        return model(
            id=note_id,
            owner_id=user_id,
            sleep_date=date.fromtimestamp(date_of_note),
            went_to_bed=rand_bedtime,
            fell_asleep=rand_asleep,
            woke_up=rand_awake,
            got_up=rand_rise,
            no_sleep=rand_time_of_night_awakenings,
        )

    def wrong_note(
        self,
        errors_count: int | None = None,
        model: Type = SleepNote,
        mode: Literal["json", "python"] | str = "python",
    ) -> dict:
        if not errors_count:
            errors_count = random.randint(1, 5)
        wrong_note = self.create_note(model=model).model_dump(mode=mode)

        keys_for_random_value: set = set()
        all_keys = list(wrong_note.keys())
        if len(all_keys) == errors_count:
            keys_for_random_value.add(*all_keys)
        while len(keys_for_random_value) < errors_count:
            keys_for_random_value.add(random.choice(all_keys))
        for key in keys_for_random_value:
            wrong_note[key] = faker.pyobject(object_type=str)
        return wrong_note
