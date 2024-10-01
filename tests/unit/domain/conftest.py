from datetime import date, time
from typing import TypeAlias


date_point: date = date(220, 12, 12)

T: TypeAlias = tuple[date, time, time, time, time]
TT: TypeAlias = tuple[
    tuple[date, time, time, time, time],
    tuple[date, time, time, time, time],
    tuple[date, time, time, time, time],
    tuple[date, time, time, time, time],
]

points_with_went_to_bed_is_first: T = (
    date_point,
    time(1, 0),
    time(3, 0),
    time(11, 0),
    time(13, 0),
)
points_with_got_up_is_first: T = (
    date_point,
    time(13, 0),
    time(15, 0),
    time(23, 0),
    time(1, 0),
)
points_with_woke_up_is_first: T = (
    date_point,
    time(15, 0),
    time(17, 0),
    time(1, 0),
    time(3, 0),
)
points_with_fell_asleep_is_first: T = (
    date_point,
    time(23, 0),
    time(1, 0),
    time(9, 0),
    time(11, 0),
)
correct_points_4_different_order_of_sequences: TT = (
    points_with_went_to_bed_is_first,
    points_with_got_up_is_first,
    points_with_woke_up_is_first,
    points_with_fell_asleep_is_first,
)

# went_to_bed
wrong_points_went_to_bed_gt_fell_asleep_and_lt_other_time_points: T = (
    date_point,
    time(4, 0),
    time(3, 0),
    time(12, 0),
    time(14, 0),
)
wrong_points_went_to_bed_gt_fell_asleep_with_points_after_midnight: T = (
    date_point,
    time(14, 0),
    time(13, 0),
    time(2, 0),
    time(4, 0),
)
wrong_points_went_to_bed_gt_fell_asleep_and_woke_up: T = (
    date_point,
    time(12, 0),
    time(3, 0),
    time(11, 0),
    time(13, 0),
)

wrong_points_went_to_bed_gt_woke_up_and_lt_others_points: T = (
    date_point,
    time(8, 0),
    time(23, 0),
    time(7, 0),
    time(9, 0),
)
wrong_points_where_wen_to_bed_is_wrong: TT = (
    wrong_points_went_to_bed_gt_fell_asleep_and_lt_other_time_points,
    wrong_points_went_to_bed_gt_fell_asleep_with_points_after_midnight,
    wrong_points_went_to_bed_gt_fell_asleep_and_woke_up,
    wrong_points_went_to_bed_gt_woke_up_and_lt_others_points,
)
