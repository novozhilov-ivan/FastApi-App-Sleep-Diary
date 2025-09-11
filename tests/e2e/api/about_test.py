from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.application.api.about.schemas import AboutSleepDiarySchema
from src.domain.sleep_diary.dtos import AboutInfo


def test_about(app: FastAPI, client: TestClient) -> None:
    url = app.url_path_for("about_sleep_diary")
    response = client.get(url)

    expected_json = AboutSleepDiarySchema.model_validate(
        AboutInfo,
        from_attributes=True,
    ).model_dump()
    assert response.is_success
    assert response.json() == expected_json
