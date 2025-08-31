from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.application.api.about.schemas import AboutSleepDiarySchema


def test_about(app: FastAPI, client: TestClient) -> None:
    url = app.url_path_for("about_sleep_diary")
    response = client.get(url)

    assert response.is_success
    assert response.json() == AboutSleepDiarySchema().model_dump()
