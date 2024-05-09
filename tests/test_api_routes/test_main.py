import pytest
from flask import url_for
from flask.testing import FlaskClient

from api.routes.main import main_endpoint
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.main import MainPageModel


@pytest.mark.main
class TestMainPage:
    ROUTES_404 = ["/api", "/api/main/", "/api/mai", "/main", "/ap"]

    def test_main_page_200(self, client: FlaskClient):
        response = client.get(url_for(main_endpoint))
        response = Response(response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(MainPageModel)
        response.assert_data(MainPageModel())

    @pytest.mark.parametrize("route", ROUTES_404)
    def test_main_page_404(self, route: str, client: FlaskClient):
        response = client.get(route)
        response = Response(response)
        response.assert_status_code(HTTP.NOT_FOUND_404)
