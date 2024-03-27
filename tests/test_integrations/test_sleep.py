import pytest
from flask.testing import FlaskClient

from src.pydantic_schemas.notes.sleep_diary import SleepDiaryModel

from tests.conftest import client
from src.baseclasses.response import Response


@pytest.mark.sleep
@pytest.mark.parametrize(
    ['params', 'status_code'],
    [
        ({'id': 1}, 200),
        ({'id': 0}, 404),
        ({'id': "0"}, 404),
        ({'id': "str_not_int"}, 400),
        ({}, 400),
        ({'not_id': 0}, 400),
        ({'not_id': "0"}, 400),
        ({'not_id': "str_not_int"}, 400),
    ]
)
def test_get_all_sleep_notes_by_user_id(
        params: dict,
        status_code: int,
        random_sleep_diary: SleepDiaryModel,
        client: FlaskClient,
        app
):
    route = "api/sleep"
    response = client.get(route, query_string=params)
    response = Response(response)

    if status_code == 200:
        expectation = random_sleep_diary.model_dump(mode='json')

        response.validate(schema=SleepDiaryModel)
        response.assert_data(expectation)

    response.assert_status_code(status_code)
