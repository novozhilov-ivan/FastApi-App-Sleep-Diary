from datetime import time

from src.domain.values.base import TimePoint


def test_create_time_point_from_time():
    t = time(1, 1)
    time_point = TimePoint[str](str(t))
    assert isinstance(time_point.value, time)
