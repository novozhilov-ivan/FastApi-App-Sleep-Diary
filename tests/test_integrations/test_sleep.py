import pytest
from flask.testing import FlaskClient

from src.pydantic_schemas.notes.sleep_diary import SleepDiaryEntriesModel

from tests.conftest import client
from src.baseclasses.response import Response


@pytest.mark.sleep
@pytest.mark.parametrize(
    ['params', 'status_code'],
    [
        ({'user_id': 1}, 200),
        ({'user_id': 0}, 404),
        ({'user_id': "0"}, 404),
        ({'user_id': "str_not_int"}, 400),
        ({}, 400),
        ({'not_user_id': 0}, 400),
        ({'not_user_id': "0"}, 400),
        ({'not_user_id': "str_not_int"}, 400),
    ]
)
def test_get_all_sleep_notes_by_user_id(
        params: dict,
        status_code: int,
        random_sleep_diary: SleepDiaryEntriesModel,
        client: FlaskClient,
        app
):
    route = "api/sleep"
    response = client.get(route, query_string=params)
    response = Response(response)

    if status_code == 200:
        expectation = random_sleep_diary.model_dump(mode='json')

        response.validate(schema=SleepDiaryEntriesModel)
        response.assert_data(expectation)

    response.assert_status_code(status_code)
