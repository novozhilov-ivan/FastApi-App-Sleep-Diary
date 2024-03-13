import json

import pytest
from flask.testing import FlaskClient

from tests.conftest import client


def get_main_page_info(client):
    static_dir = client.application.static_folder
    with open(f"{static_dir}/content/main.json", "r") as f:
        return json.load(f)


@pytest.mark.parametrize(
    [
        'route',
        'status_code',
        'expectation'
    ],
    [
        ('/api/', 200, None),
        ('/api/main', 200, None),
        ('/api', 308, None),
        ('/api/main/', 404, None),
        ('/api/mai', 404, None),
        ('/ap', 404, None),
        ('/ma', 404, None),
    ]
)
def test_main_page_info(
        route: str,
        status_code: int,
        expectation: dict,
        client: FlaskClient,
):
    response = client.get(route)
    if status_code == 200:
        expectation = get_main_page_info(client)

    assert response.status_code == status_code, \
        f'Response status code is {response.status_code}. Expectation status code is {status_code}.'
    assert response.json == expectation, \
        f"Response is {response.json}. Expectation is {expectation}."

