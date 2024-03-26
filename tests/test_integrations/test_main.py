import pytest
from flask.testing import FlaskClient

from tests.conftest import client
from tests.test_integrations.conftest import main_page_info
from src.pydantic_schemas.main_info import MainPage
from src.baseclasses.response import Response


@pytest.mark.parametrize(
    [
        'route',
        'status_code',
        'expectation',
        'follow_redirects'
    ],
    [
        ('/api/', 200, None, {}),
        ('/api/main', 200, None, {}),
        ('/api', 200, None, {'follow_redirects': True}),
        ('/api', 308, None, {'follow_redirects': False}),
        ('/api/main/', 404, None, {}),
        ('/api/mai', 404, None, {}),
        ('/ap', 404, None, {}),
        ('/ma', 404, None, {}),
    ]
)
def test_main_page(
        route: str,
        status_code: int,
        expectation: dict | None,
        follow_redirects: dict,
        main_page_info,
        client: FlaskClient,
):
    response = client.get(route, **follow_redirects)
    response = Response(response, route)

    if status_code == 200:
        expectation = main_page_info
        response.validate(
            schema=MainPage
        )

    response.assert_status_code(status_code)
    response.assert_data(expectation)
