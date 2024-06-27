import pytest
from flask import url_for
from flask.testing import FlaskClient

from src.pydantic_schemas.main import MainPageModel
from src.routes.main import main_endpoint
from src.utils.status_codes import HTTP
from tests.test_api.response import Response


@pytest.mark.main
class TestMainPage:

    def test_main_page_200(self, client: FlaskClient):
        raw_response = client.get(url_for(main_endpoint))
        response = Response(raw_response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(MainPageModel)
        response.assert_data(MainPageModel())
