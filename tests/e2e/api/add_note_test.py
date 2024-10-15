import pytest

from fastapi import FastAPI
from httpx import Response
from starlette import status
from starlette.testclient import TestClient

from src import service_layer
from src.domain.exceptions import (
    ApplicationException,
    NonUniqueNoteBedtimeDateException,
    NoSleepDurationException,
    NoteException,
    TimePointsSequenceException,
)
from src.infrastructure.orm import ORMUser
from src.infrastructure.repository import BaseNoteRepository


def test_add_note_201(app: FastAPI, client: TestClient, user: ORMUser):
    data = {
        "bedtime_date": "2020-12-12",
        "went_to_bed": "01:00",
        "fell_asleep": "03:00",
        "woke_up": "11:00",
        "got_up": "13:00",
        "no_sleep": "01:00",
    }
    url = app.url_path_for("Добавить запись")
    response: Response = client.post(
        url=url,
        json=data,
        headers={"owner_oid": str(user.oid)},
        # auth=jwt_access,
    )
    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json() is None


@pytest.mark.parametrize(
    ("data", "expected_exception"),
    [
        (
            {
                "bedtime_date": "2020-12-12",
                "went_to_bed": "01:00",
                "fell_asleep": "00:00",
                "woke_up": "11:00",
                "got_up": "13:00",
                "no_sleep": "01:00",
            },
            TimePointsSequenceException,
        ),
        (
            {
                "bedtime_date": "2020-12-12",
                "went_to_bed": "01:00",
                "fell_asleep": "03:00",
                "woke_up": "11:00",
                "got_up": "13:00",
                "no_sleep": "09:00",
            },
            NoSleepDurationException,
        ),
    ],
)
def test_add_note_400_note_exceptions(
    app: FastAPI,
    client: TestClient,
    user: ORMUser,
    data: dict,
    expected_exception: NoteException,
):
    url = app.url_path_for("Добавить запись")
    response: Response = client.post(
        url=url,
        json=data,
        headers={"owner_oid": str(user.oid)},
        # auth=jwt_access,
    )
    assert status.HTTP_400_BAD_REQUEST == response.status_code
    with pytest.raises(NoteException) as excinfo:
        NoteTimePoints.model_validate(data)
    assert excinfo.type is expected_exception
    assert excinfo.value.message == response.json()["detail"]["error"]


def test_add_note_400_write_note_twice_exception(
    app: FastAPI,
    client: TestClient,
    user: ORMUser,
    repository: BaseNoteRepository,
):
    data = {
        "bedtime_date": "2020-12-12",
        "went_to_bed": "01:00",
        "fell_asleep": "03:00",
        "woke_up": "11:00",
        "got_up": "13:00",
        "no_sleep": "01:00",
    }
    expected_exception = NonUniqueNoteBedtimeDateException

    url = app.url_path_for("Добавить запись")
    client.post(
        url=url,
        json=data,
        headers={"owner_oid": str(user.oid)},
        # auth=jwt_access,
    )
    response: Response = client.post(
        url=url,
        json=data,
        headers={"owner_oid": str(user.oid)},
        # auth=jwt_access,
    )

    assert status.HTTP_400_BAD_REQUEST == response.status_code, response.json()

    with pytest.raises(ApplicationException) as excinfo:
        service_layer.write(**data, owner_oid=user.oid, repository=repository)
    assert excinfo.type is expected_exception
    assert excinfo.value.message == response.json()["detail"]["error"]
