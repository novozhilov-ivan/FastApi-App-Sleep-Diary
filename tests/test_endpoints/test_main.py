import pytest
from flask.testing import FlaskClient

from tests.conftest import client
from tests.test_endpoints.conftest import main_info
from common.pydantic_schemas.main_info import MainPageModel
from common.baseclasses.response import Response


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
        # ('/api', 200, {'follow_redirects': True}),
        # ('/api', 308, {'follow_redirects': False}),
        ('/api/main/', 404, {}),
        ('/api/mai', 404, {}),
        ('/ap', 404, {}),
        ('/ma', 404, {}),
    ]
)
def test_main_page(
        main_info,
        client: FlaskClient,
        route: str,
        status_code: int,
        follow_redirects: dict,
):
    response = client.get(route, **follow_redirects)
    response = Response(response)

    expectation = None
    if status_code == 200:
        expectation = main_info
        response.validate(schema=MainPageModel)

    response.assert_status_code(status_code)
    response.assert_data(expectation)
