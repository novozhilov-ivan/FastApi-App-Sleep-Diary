from http import HTTPStatus

from flask.testing import FlaskClient

from src.application.api.namespaces.main.schemas import MainEndPointSchema


def test_main_endpoint(client: FlaskClient):
    resp = client.get("api/main")
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == MainEndPointSchema().model_dump()
    assert MainEndPointSchema.model_validate(resp.json)
