from http import HTTPStatus

from flask.testing import FlaskClient

from src.application.api.namespaces.main.schemas import MainEndpointSchema


def test_main_endpoint(client: FlaskClient):
    resp = client.get("api/main")
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == MainEndpointSchema().model_dump()
    assert MainEndpointSchema.model_validate(resp.json)
