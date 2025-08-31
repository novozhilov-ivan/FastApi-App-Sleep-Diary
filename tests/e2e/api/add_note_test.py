import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from httpx import Response

from src.domain.sleep_diary.entities.user import UserEntity
from src.domain.sleep_diary.exceptions.base import ApplicationError
from src.domain.sleep_diary.exceptions.note import (
    NoSleepDurationError,
    NoteError,
    TimePointsSequenceError,
)
from src.domain.sleep_diary.exceptions.write import NonUniqueNoteBedtimeDateError
from src.domain.sleep_diary.values.points import Points
from src.infra.sleep_diary.converters import convert_points_to_json
from src.infra.sleep_diary.use_cases.diary import Diary
from tests.conftest import (
    TN,
    T,
    points_order_desc_from_went_to_bed,
    wrong_points_no_sleep_gt_sleep_order_asc_from_went_to_bed,
    wrong_points_went_to_bed_gt_fell_asleep_and_lt_other_time_points,
)
from tests.unit.sleep_diary.conftest import FakePoints


def test_add_note_201(app: FastAPI, authorized_client: TestClient) -> None:
    response: Response = authorized_client.post(
        url=app.url_path_for("add_note"),
        json=convert_points_to_json(Points(*points_order_desc_from_went_to_bed)),
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json() is None


@pytest.mark.parametrize(
    ("points", "exception"),
    [
        (
            wrong_points_went_to_bed_gt_fell_asleep_and_lt_other_time_points,
            TimePointsSequenceError,
        ),
        (
            wrong_points_no_sleep_gt_sleep_order_asc_from_went_to_bed,
            NoSleepDurationError,
        ),
    ],
)
def test_add_note_400_note_exceptions(
    app: FastAPI,
    authorized_client: TestClient,
    points: T | TN,
    exception: NoteError,
) -> None:
    response: Response = authorized_client.post(
        url=app.url_path_for("add_note"),
        json=convert_points_to_json(FakePoints(*points)),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    with pytest.raises(NoteError) as excinfo:
        Points(*points)
    assert excinfo.type is exception
    assert excinfo.value.message == response.json()["detail"]["error"]


def test_add_note_400_write_note_twice_exception(
    app: FastAPI,
    authorized_client: TestClient,
    api_user: UserEntity,
    diary_with_orm: Diary,
) -> None:
    points = Points(*points_order_desc_from_went_to_bed)
    expected_exception = NonUniqueNoteBedtimeDateError

    url = app.url_path_for("add_note")
    authorized_client.post(
        url=url,
        json=convert_points_to_json(points),
    )
    response: Response = authorized_client.post(
        url=url,
        json=convert_points_to_json(points),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()

    with pytest.raises(ApplicationError) as excinfo:
        diary_with_orm.write(api_user.oid, *points_order_desc_from_went_to_bed)

    assert excinfo.type is expected_exception
    assert excinfo.value.message == response.json()["detail"]["error"]
