import pytest

from src.domain.sleep_diary.services.durations import Durations
from src.domain.sleep_diary.specifications.no_sleep_duration import (
    NoSleepHasValidTime,
)
from tests.conftest import (
    wrong_points_where_no_sleep_gt_sleep,
)
from tests.unit.sleep_diary.conftest import FakePoints


@pytest.mark.parametrize(
    "wrong_points",
    wrong_points_where_no_sleep_gt_sleep,
)
def test_create_points_with_no_sleep_time_gt_sleep_time(wrong_points: tuple) -> None:
    points = FakePoints(*wrong_points)
    specification = NoSleepHasValidTime(Durations(points))
    assert not specification._no_sleep_duration_le_sleep_duration()
    assert bool(specification) is False
    assert not specification
