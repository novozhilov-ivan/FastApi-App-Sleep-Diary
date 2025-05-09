from fastapi import FastAPI
from httpx import Response
from starlette.testclient import TestClient

from src.sleep_diary.infrastructure.api.routers.about.schemas import (
    AboutSleepDiarySchema,
)


def test_about(app: FastAPI, client: TestClient):
    url = app.url_path_for("about_sleep_diary")
    response: Response = client.get(url)
    assert response.is_success
    assert response.json()["description"] == AboutSleepDiarySchema().description
