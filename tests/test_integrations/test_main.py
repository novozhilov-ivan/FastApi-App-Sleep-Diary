import pytest
from flask.testing import FlaskClient

from tests.conftest import client
from tests.test_integrations.conftest import main_info
from src.pydantic_schemas.main_info import MainPage
from src.baseclasses.response import Response


@pytest.mark.main
@pytest.mark.parametrize(
    [
        'route',
        'status_code',
        'follow_redirects'
    ],
    [
        ('/api/', 200, {}),
        ('/api/main', 200, {}),
        ('/api', 200, {'follow_redirects': True}),
        ('/api', 308, {'follow_redirects': False}),
        ('/api/main/', 404, {}),
        ('/api/mai', 404, {}),
        ('/ap', 404, {}),
        ('/ma', 404, {}),
    ]
)
def test_main_page(
        route: str,
        status_code: int,
        follow_redirects: dict,
        main_info,
        client: FlaskClient,
):
    response = client.get(route, **follow_redirects)
    response = Response(response)

    expectation = None
    if status_code == 200:
        expectation = main_info
        response.validate(schema=MainPage)

    response.assert_status_code(status_code)
    response.assert_data(expectation)
