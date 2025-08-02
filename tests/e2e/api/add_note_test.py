from uuid import UUID

import pytest

from fastapi import FastAPI
from httpx import Response
from starlette import status
from starlette.testclient import TestClient

from src.application.api.sleep_diary.services.diary import Diary
from src.domain.sleep_diary.exceptions.base import ApplicationException
from src.domain.sleep_diary.exceptions.note import (
    NoSleepDurationException,
    NoteException,
    TimePointsSequenceException,
)
from src.domain.sleep_diary.exceptions.write import NonUniqueNoteBedtimeDateException
from src.domain.sleep_diary.values.points import Points
from src.infra.sleep_diary.converters import convert_points_to_json
from tests.conftest import (
    points_order_desc_from_went_to_bed,
    T,
    TN,
    wrong_points_no_sleep_gt_sleep_order_asc_from_went_to_bed,
    wrong_points_went_to_bed_gt_fell_asleep_and_lt_other_time_points,
)
from tests.unit.sleep_diary.conftest import FakePoints


def test_add_note_201(app: FastAPI, client: TestClient, user_oid: str) -> None:
    response: Response = client.post(
        url=app.url_path_for("add_note"),
        json=convert_points_to_json(Points(*points_order_desc_from_went_to_bed)),
        headers={"owner_oid": user_oid},
    )
    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json() is None


@pytest.mark.parametrize(
    ("points", "exception"),
    [
        (
            wrong_points_went_to_bed_gt_fell_asleep_and_lt_other_time_points,
            TimePointsSequenceException,
        ),
        (
            wrong_points_no_sleep_gt_sleep_order_asc_from_went_to_bed,
            NoSleepDurationException,
        ),
    ],
)
def test_add_note_400_note_exceptions(
    app: FastAPI,
    client: TestClient,
    user_oid: str,
    points: T | TN,
    exception: NoteException,
) -> None:
    response: Response = client.post(
        url=app.url_path_for("add_note"),
        json=convert_points_to_json(FakePoints(*points)),
        headers={"owner_oid": user_oid},
    )
    assert status.HTTP_400_BAD_REQUEST == response.status_code
    with pytest.raises(NoteException) as excinfo:
        Points(*points)
    assert excinfo.type is exception
    assert excinfo.value.message == response.json()["detail"]["error"]


def test_add_note_400_write_note_twice_exception(
    app: FastAPI,
    client: TestClient,
    user_oid: str,
    diary: Diary,
) -> None:
    points = Points(*points_order_desc_from_went_to_bed)
    expected_exception = NonUniqueNoteBedtimeDateException

    url = app.url_path_for("add_note")
    client.post(
        url=url,
        json=convert_points_to_json(points),
        headers={"owner_oid": user_oid},
    )
    response: Response = client.post(
        url=url,
        json=convert_points_to_json(points),
        headers={"owner_oid": user_oid},
    )

    assert status.HTTP_400_BAD_REQUEST == response.status_code, response.json()

    with pytest.raises(ApplicationException) as excinfo:
        diary.write(UUID(user_oid), *points_order_desc_from_went_to_bed)

    assert excinfo.type is expected_exception
    assert excinfo.value.message == response.json()["detail"]["error"]
