from datetime import date, time

from src.domain.values import DatePoint, Points, PointsIn, PointsOut, TimePoint


def test_points_fields_types():
    points = Points[PointsIn, PointsOut](
        PointsIn(
            bedtime_date=DatePoint("2020-12-12"),
            went_to_bed=TimePoint("01:00"),
            fell_asleep=TimePoint("03:00"),
            woke_up=TimePoint("11:00"),
            got_up=TimePoint("13:00"),
            no_sleep=TimePoint("00:00"),
        ),
    )
    points_out: PointsOut = points.as_generic_type()

    assert isinstance(points_out, PointsOut)
    assert isinstance(points_out.bedtime_date, date)
    assert isinstance(points_out.went_to_bed, time)
    assert isinstance(points_out.fell_asleep, time)
    assert isinstance(points_out.woke_up, time)
    assert isinstance(points_out.got_up, time)
    assert isinstance(points_out.no_sleep, time)
