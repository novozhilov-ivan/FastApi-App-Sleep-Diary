from datetime import date, time
from itertools import chain
from typing import TypeAlias

from src.domain.values.points import Points


date_point: date = date(2020, 12, 12)

T: TypeAlias = tuple[date, time, time, time, time]
TT: TypeAlias = tuple[
    tuple[date, time, time, time, time],
    tuple[date, time, time, time, time],
    tuple[date, time, time, time, time],
    tuple[date, time, time, time, time],
]
# 4 Корректных, последовательных и отсортированных данных для временных точек.
# Все имеют:
# 8 часов сна [fell_asleep:woke_up]
# 2 часа между отходом ко сну и засыпанием [went_to_bed:fell_asleep]
# 2 часа между  пробуждением и подъемом [woke_up:got_up]
# 12 часов между отходом ко сну и подъемом [went_to_bed:got_up]
# Время без сна отсутствует
points_order_desc_from_went_to_bed: T = (
    date_point,
    time(1),
    time(3),
    time(11),
    time(13),
)
points_order_desc_from_got_up: T = (
    date_point,
    time(13),
    time(15),
    time(23),
    time(1),
)
points_order_desc_from_woke_up: T = (
    date_point,
    time(15),
    time(17),
    time(1),
    time(3),
)
points_order_desc_from_fell_asleep: T = (
    date_point,
    time(23),
    time(1),
    time(9),
    time(11),
)
correct_points_4_different_order_of_sequences: TT = (
    points_order_desc_from_went_to_bed,
    points_order_desc_from_got_up,
    points_order_desc_from_woke_up,
    points_order_desc_from_fell_asleep,
)

# went_to_bed is wrong
wrong_points_went_to_bed_gt_fell_asleep_and_lt_other_time_points: T = (
    date_point,
    time(4),
    time(3),
    time(12),
    time(14),
)
wrong_points_went_to_bed_gt_fell_asleep_with_points_after_midnight: T = (
    date_point,
    time(14),
    time(13),
    time(2),
    time(4),
)
wrong_points_went_to_bed_gt_fell_asleep_and_woke_up: T = (
    date_point,
    time(12),
    time(3),
    time(11),
    time(13),
)
wrong_points_went_to_bed_gt_woke_up_and_lt_others_points: T = (
    date_point,
    time(8),
    time(23),
    time(7),
    time(9),
)
wrong_points_where_went_to_bed_is_wrong: TT = (
    wrong_points_went_to_bed_gt_fell_asleep_and_lt_other_time_points,
    wrong_points_went_to_bed_gt_fell_asleep_with_points_after_midnight,
    wrong_points_went_to_bed_gt_fell_asleep_and_woke_up,
    wrong_points_went_to_bed_gt_woke_up_and_lt_others_points,
)
# fell_asleep is wrong
wrong_points_fell_asleep_gt_wok_up_and_lt_got_up: T = (
    date_point,
    time(1),
    time(12),
    time(11),
    time(13),
)
wrong_points_fell_asleep_gt_got_up_and_got_up_lt_went_to_bed: T = (
    date_point,
    time(1),
    time(14),
    time(11),
    time(13),
)
wrong_points_fell_asleep_gt_woke_up_and_lt_went_to_bed: T = (
    date_point,
    time(23),
    time(10),
    time(9),
    time(11),
)
wrong_points_fell_asleep_gt_got_up_and_lt_went_to_bed: T = (
    date_point,
    time(23),
    time(12),
    time(9),
    time(11),
)
wrong_points_where_fell_asleep_is_wrong: TT = (
    wrong_points_fell_asleep_gt_wok_up_and_lt_got_up,
    wrong_points_fell_asleep_gt_got_up_and_got_up_lt_went_to_bed,
    wrong_points_fell_asleep_gt_woke_up_and_lt_went_to_bed,
    wrong_points_fell_asleep_gt_got_up_and_lt_went_to_bed,
)
# woke_up is wrong
wrong_points_woke_up_gt_got_up_while_got_up_gt_other_points: T = (
    date_point,
    time(1),
    time(3),
    time(14),
    time(13),
)
wrong_points_woke_up_gt_got_up_while_got_up_gt_fell_asleep_and_lt_went_to_bed: T = (
    date_point,
    time(23),
    time(1),
    time(12),
    time(11),
)
wrong_points_woke_up_gt_got_up_and_lt_other_points: T = (
    date_point,
    time(13),
    time(15),
    time(2),
    time(1),
)
wrong_points_woke_up_lt_other_points: T = (
    date_point,
    time(13),
    time(15),
    time(1),
    time(23),
)
wrong_points_where_woke_up_is_wrong: TT = (
    wrong_points_woke_up_gt_got_up_while_got_up_gt_other_points,
    wrong_points_woke_up_gt_got_up_while_got_up_gt_fell_asleep_and_lt_went_to_bed,
    wrong_points_woke_up_gt_got_up_and_lt_other_points,
    wrong_points_woke_up_lt_other_points,
)
# got up is wrong
wrong_points_got_up_lt_woke_up_and_gt_other_points: T = (
    date_point,
    time(1),
    time(3),
    time(11),
    time(10),
)
wrong_points_got_up_gt_fell_asleep_and_lt_other_points: T = (
    date_point,
    time(23),
    time(1),
    time(7),
    time(6),
)
wrong_points_got_up_lt_woke_up_while_woke_up_lt_other_points: T = (
    date_point,
    time(15),
    time(17),
    time(2),
    time(1),
)
wrong_points_got_up_lt_fell_asleep_and_gt_other_points: T = (
    date_point,
    time(21),
    time(23),
    time(7),
    time(22),
)
wrong_points_where_got_up_is_wrong: TT = (
    wrong_points_got_up_lt_woke_up_and_gt_other_points,
    wrong_points_got_up_gt_fell_asleep_and_lt_other_points,
    wrong_points_got_up_lt_woke_up_while_woke_up_lt_other_points,
    wrong_points_got_up_lt_fell_asleep_and_gt_other_points,
)
# Все point'ы, в которых не корректная сортировка
all_wrong_points_sequences: chain[TT] = chain.from_iterable(
    (
        wrong_points_where_went_to_bed_is_wrong,
        wrong_points_where_fell_asleep_is_wrong,
        wrong_points_where_woke_up_is_wrong,
        wrong_points_where_got_up_is_wrong,
    ),
)
#  Point'ы, в которых время без сна больше времени сна
TN: TypeAlias = tuple[date, time, time, time, time, time]
TTN: TypeAlias = tuple[
    tuple[date, time, time, time, time, time],
    tuple[date, time, time, time, time, time],
    tuple[date, time, time, time, time, time],
    tuple[date, time, time, time, time, time],
]
wrong_points_no_sleep_gt_sleep_order_asc_from_went_to_bed: TN = (
    date_point,
    time(1),
    time(3),
    time(11),
    time(13),
    time(9),
)
wrong_points_no_sleep_gt_sleep_order_asc_from_got_up: TN = (
    date_point,
    time(13),
    time(15),
    time(23),
    time(1),
    time(9),
)
wrong_points_no_sleep_gt_sleep_order_asc_from_woke_up: TN = (
    date_point,
    time(15),
    time(17),
    time(1),
    time(3),
    time(9),
)
wrong_points_no_sleep_gt_sleep_order_asc_from_fell_asleep: TN = (
    date_point,
    time(23),
    time(1),
    time(9),
    time(11),
    time(9),
)
wrong_points_where_no_sleep_gt_sleep: TTN = (
    wrong_points_no_sleep_gt_sleep_order_asc_from_went_to_bed,
    wrong_points_no_sleep_gt_sleep_order_asc_from_got_up,
    wrong_points_no_sleep_gt_sleep_order_asc_from_woke_up,
    wrong_points_no_sleep_gt_sleep_order_asc_from_fell_asleep,
)
# Временные точки с нулевыми значениями
points_all_zero: T = (
    date_point,
    time(),
    time(),
    time(),
    time(),
)
points_with_zeros_and_some_big_no_sleep: TN = (
    date_point,
    time(),
    time(),
    time(),
    time(),
    time(10),
)
# Корректные временные точки с разными последовательностями и 1 часов без сна
points_order_desc_from_went_to_bed_and_one_hour_no_sleep: TN = (
    date_point,
    time(1),
    time(3),
    time(11),
    time(13),
    time(1),
)
points_order_desc_from_got_up_and_one_hour_no_sleep: TN = (
    date_point,
    time(13),
    time(15),
    time(23),
    time(1),
    time(1),
)
points_order_desc_from_woke_up_and_one_hour_no_sleep: TN = (
    date_point,
    time(15),
    time(17),
    time(1),
    time(3),
    time(1),
)
points_order_desc_from_fell_asleep_and_one_hour_no_sleep: TN = (
    date_point,
    time(23),
    time(1),
    time(9),
    time(11),
    time(1),
)
correct_points_4_different_order_of_sequences_and_one_hour_no_sleep: TTN = (
    points_order_desc_from_went_to_bed_and_one_hour_no_sleep,
    points_order_desc_from_got_up_and_one_hour_no_sleep,
    points_order_desc_from_woke_up_and_one_hour_no_sleep,
    points_order_desc_from_fell_asleep_and_one_hour_no_sleep,
)

all_correct_points_sequences: list[Points] = [
    Points(*points) for points in correct_points_4_different_order_of_sequences
]
