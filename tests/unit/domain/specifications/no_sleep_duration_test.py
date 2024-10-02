import pytest

from src.domain.specifications import NoSleepHasValidTime
from tests.unit.domain.conftest import wrong_points_where_no_sleep_gt_sleep
from tests.unit.domain.specifications.conftest import FakePoints


@pytest.mark.parametrize(
    "wrong_points",
    wrong_points_where_no_sleep_gt_sleep,
)
def test_(wrong_points: tuple):
    points_out = FakePoints(*wrong_points)
    specification = NoSleepHasValidTime(points_out)
    assert not specification.no_sleep_duration_le_sleep_duration()
    assert bool(specification) is False
    assert not specification
