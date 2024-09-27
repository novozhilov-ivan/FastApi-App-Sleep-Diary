from typing import TypeAlias


date_point: str = "2020-12-12"

T: TypeAlias = tuple[str, str, str, str, str]
TT: TypeAlias = tuple[
    tuple[str, str, str, str, str],
    tuple[str, str, str, str, str],
    tuple[str, str, str, str, str],
    tuple[str, str, str, str, str],
]

points_in_with_went_to_bed_is_first: T = (
    date_point,
    "01:00",
    "03:00",
    "11:00",
    "13:00",
)
points_in_with_got_up_is_first: T = (
    date_point,
    "13:00",
    "15:00",
    "23:00",
    "01:00",
)
points_in_with_woke_up_is_first: T = (
    date_point,
    "15:00",
    "17:00",
    "01:00",
    "03:00",
)
points_in_with_fell_asleep_is_first: T = (
    date_point,
    "23:00",
    "01:00",
    "09:00",
    "11:00",
)
correct_points_ins_4_different_order_of_sequences: TT = (
    points_in_with_went_to_bed_is_first,
    points_in_with_got_up_is_first,
    points_in_with_woke_up_is_first,
    points_in_with_fell_asleep_is_first,
)

# went_to_bed
wrong_points_in_went_to_bed_gt_fell_asleep_and_lt_other_time_points: T = (
    date_point,
    "04:00",
    "03:00",
    "12:00",
    "14:00",
)
wrong_points_in_went_to_bed_gt_fell_asleep_with_points_after_midnight: T = (
    date_point,
    "14:00",
    "13:00",
    "02:00",
    "04:00",
)
wrong_points_in_went_to_bed_gt_fell_asleep_and_woke_up: T = (
    date_point,
    "12:00",
    "03:00",
    "11:00",
    "13:00",
)

wrong_points_in_went_to_bed_gt_woke_up_and_lt_others_points: T = (
    date_point,
    "08:00",
    "23:00",
    "07:00",
    "09:00",
)
wrong_points_ins_where_wen_to_bed_is_wrong: TT = (
    wrong_points_in_went_to_bed_gt_fell_asleep_and_lt_other_time_points,
    wrong_points_in_went_to_bed_gt_fell_asleep_with_points_after_midnight,
    wrong_points_in_went_to_bed_gt_fell_asleep_and_woke_up,
    wrong_points_in_went_to_bed_gt_woke_up_and_lt_others_points,
)
