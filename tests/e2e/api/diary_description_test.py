from fastapi import FastAPI
from httpx import Response
from starlette.testclient import TestClient

from src.application.api.routers.diary_description.schemas import (
    SleepDiaryDescriptionSchema,
)


def test_get_diary_description(app: FastAPI, client: TestClient):
    url = app.url_path_for("get_sleep_diary_description")
    response: Response = client.get(url)
    assert response.is_success
    json_data = response.json()
    assert json_data["description"] == SleepDiaryDescriptionSchema().description
