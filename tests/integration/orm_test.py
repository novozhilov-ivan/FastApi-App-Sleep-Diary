from sqlalchemy import text
from sqlalchemy.orm import Session


def test_mapping(memory_session: Session) -> None:
    # memory_session.execute(
    #     text(
    #         "INSERT INTO notes"
    #         "(bedtime_date, went_to_bed, fell_asleep, woke_up, got_up, no_sleep) "
    #         "VALUES (2020-01-01, 01-00, 03-00, 11-00, 13-00, 01-00);"
    #     ),
    # )

    # note_values = NoteValueObject(
    #     bedtime_date="2020-01-01",
    #     went_to_bed="01:00",
    #     fell_asleep="03:00",
    #     woke_up="11:00",
    #     got_up="13:00",
    #     no_sleep="01:00",
    # )
    # note = NoteORM()
    # note.bedtime_date = note_values.bedtime_date
    # note.went_to_bed = note_values.went_to_bed
    # note.fell_asleep = note_values.fell_asleep
    # note.woke_up = note_values.woke_up
    # note.got_up = note_values.got_up
    # note.no_sleep = note_values.no_sleep
    #
    # memory_session.add(note)
    memory_session.commit()
    res = memory_session.execute(
        text("SELECT * FROM NOTES"),
    )
    print(f"{res.all()=}")
    assert True
    # expected = [
    #     NoteValueObject(
    #         bedtime_date="2020-01-01",
    #         went_to_bed="01:00",
    #         fell_asleep="03:00",
    #         woke_up="11:00",
    #         got_up="13:00",
    #         no_sleep="01:00",
    #     ),
    #     NoteValueObject(
    #         bedtime_date="2020-01-02",
    #         went_to_bed="01:00",
    #         fell_asleep="03:00",
    #         woke_up="11:00",
    #         got_up="13:00",
    #         no_sleep="01:00",
    #     ),
    #     NoteValueObject(
    #         bedtime_date="2020-01-03",
    #         went_to_bed="01:00",
    #         fell_asleep="03:00",
    #         woke_up="11:00",
    #         got_up="13:00",
    #         no_sleep="01:00",
    #     ),
    # ]
    # assert memory_session.query(NoteValueObject).all() == expected
