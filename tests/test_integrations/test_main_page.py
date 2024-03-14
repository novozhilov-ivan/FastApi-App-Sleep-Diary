import json

import pytest
from flask.testing import FlaskClient

from tests.conftest import client
from src.pydantic_schemas.main_info import MainPageInfoSchema
from src.baseclasses.response import Response


def main_page(client):
    static_dir = client.application.static_folder
    with open(f"{static_dir}/content/main.json", "r") as f:
        return json.load(f)


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
        expectation: dict,
        follow_redirects: dict,
        client: FlaskClient,
):
    response = client.get(route, **follow_redirects)
    response = Response(response, route)

    if status_code == 200:
        expectation = main_page(client)
        response.validate(
            schema=MainPageInfoSchema
        )

    response.assert_status_code(status_code)
    response.assert_data(expectation)
