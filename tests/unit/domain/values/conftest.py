from src.domain.values import DatePoint, PointsIn, TimePoint


date_point: DatePoint = DatePoint("2020-12-12")

points_in_with_went_to_bed_is_first = PointsIn(
    bedtime_date=date_point,
    went_to_bed=TimePoint("01:00"),
    fell_asleep=TimePoint("03:00"),
    woke_up=TimePoint("11:00"),
    got_up=TimePoint("13:00"),
)
points_in_with_got_up_is_first = PointsIn(
    bedtime_date=date_point,
    went_to_bed=TimePoint("13:00"),
    fell_asleep=TimePoint("15:00"),
    woke_up=TimePoint("23:00"),
    got_up=TimePoint("01:00"),
)
points_in_with_woke_up_is_first = PointsIn(
    bedtime_date=date_point,
    went_to_bed=TimePoint("15:00"),
    fell_asleep=TimePoint("17:00"),
    woke_up=TimePoint("01:00"),
    got_up=TimePoint("03:00"),
)
points_in_with_fell_asleep_is_first = PointsIn(
    bedtime_date=date_point,
    went_to_bed=TimePoint("23:00"),
    fell_asleep=TimePoint("01:00"),
    woke_up=TimePoint("09:00"),
    got_up=TimePoint("11:00"),
)
