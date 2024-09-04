from fastapi import FastAPI
from httpx import Response
from starlette import status
from starlette.testclient import TestClient

from src.infrastructure.orm import ORMUser


def test_write_note_201(app: FastAPI, client: TestClient, user: ORMUser):
    data = {
        "bedtime_date": "2020-12-12",
        "went_to_bed": "01:00",
        "fell_asleep": "03:00",
        "woke_up": "11:00",
        "got_up": "13:00",
        "no_sleep": "01:00",
    }
    url = app.url_path_for("write_note")
    response: Response = client.post(
        url=url,
        json=data,
        headers={"owner_oid": str(user.oid)},
        # auth=jwt_access,
    )
    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.json() is None
