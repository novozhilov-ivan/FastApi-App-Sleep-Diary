# import datetime as dt
#
# import pytest
#
#
#
# note_1 = NoteStatistic(
#     bedtime_date="2024-01-01",
#     went_to_bed="01:00",
#     fell_asleep="03:00",
#     woke_up="11:00",
#     got_up="13:00",
#     no_sleep="00:30",
# )
# note_2 = NoteStatistic(
#     bedtime_date="2024-01-02",
#     went_to_bed="01:00",
#     fell_asleep="03:00",
#     woke_up="12:00",
#     got_up="14:00",
#     no_sleep="01:00",
# )
# note_3 = NoteStatistic(
#     bedtime_date="2024-01-03",
#     went_to_bed="00:00",
#     fell_asleep="00:00",
#     woke_up="00:00",
#     got_up="00:00",
#     no_sleep="00:00",
# )
#
#
# @pytest.mark.xfail(
#     reason="Изменилось формирование класса NoteStatistic. "
#     "Теперь он мутабельный и не хэшируемый.",
# )
# def test_week_statistic_with_one_note() -> None:
#     week = Week({note_1})
#     assert week.weekly_notes_count == 1
#     assert week.average_weekly_time_in_sleep == note_1.time_in_sleep
#     assert week.average_weekly_time_in_bed == note_1.time_in_bed
#     assert week.average_weekly_no_sleep_time == note_1.no_sleep
#     assert (
#         week.average_weekly_time_in_sleep_minus_no_sleep
#         == note_1.time_in_sleep_minus_no_sleep
#     )
#     assert week.average_weekly_sleep_efficiency == note_1.sleep_efficiency
#
#
# @pytest.mark.xfail(
#     reason="Изменилось формирование класса NoteStatistic. "
#     "Теперь он мутабельный и не хэшируемый.",
# )
# def test_week_statistic_with_two_notes() -> None:
#     week = Week({note_1, note_2})
#     assert week.weekly_notes_count == 2
#     assert week.average_weekly_time_in_sleep == dt.time(hour=8, minute=30)
#     assert week.average_weekly_time_in_bed == dt.time(hour=12, minute=30)
#     assert week.average_weekly_no_sleep_time == dt.time(minute=45)
#     assert week.average_weekly_time_in_sleep_minus_no_sleep == dt.time(
#         hour=7,
#         minute=45,
#     )
#     assert week.average_weekly_sleep_efficiency == (0.625 + 0.615) / 2
#
#
# @pytest.mark.xfail(
#     reason="Изменилось формирование класса NoteStatistic. "
#     "Теперь он мутабельный и не хэшируемый.",
# )
# def test_week_statistic_with_three_notes_but_one_is_all_null() -> None:
#     week = Week({note_1, note_2, note_3})
#     assert week.weekly_notes_count == 3
#     assert week.average_weekly_time_in_sleep == dt.time(hour=5, minute=40)
#     assert week.average_weekly_time_in_bed == dt.time(hour=8, minute=20)
#     assert week.average_weekly_no_sleep_time == dt.time(minute=30)
#     assert week.average_weekly_time_in_sleep_minus_no_sleep == dt.time(
#         hour=5,
#         minute=10,
#     )
#     assert week.average_weekly_sleep_efficiency == round(
#         number=(0.625 + 0.615 + 0) / 3,
#         ndigits=2,
#     )
