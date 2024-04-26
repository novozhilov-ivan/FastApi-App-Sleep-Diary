import pytest
from flask.testing import FlaskClient

from tests.conftest import client
from common.pydantic_schemas.main import MainPageModel
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP


@pytest.mark.main
class TestMainPage:
    PARAM = 'route'
    ROUTES_200 = ['/api/', '/api/main']
    ROUTES_404 = ['/api', '/api/main/', '/api/mai', '/main', '/ap']

    @pytest.mark.parametrize(PARAM, ROUTES_200)
    def test_main_page_200(
            self,
            route: str,
            client: FlaskClient,
    ):
        response = client.get(route)
        response = Response(response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(MainPageModel)
        response.assert_data(MainPageModel())

    @pytest.mark.parametrize(PARAM, ROUTES_404)
    def test_main_page_404(self, route: str, client: FlaskClient):
        response = client.get(route)
        response = Response(response)
        response.assert_status_code(HTTP.NOT_FOUND_404)
