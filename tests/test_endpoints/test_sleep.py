from typing import Type

import pytest
from flask.testing import FlaskClient
from pydantic import BaseModel, ValidationError

from common.pydantic_schemas.notes.sleep_diary import SleepDiaryModel, SleepDiaryModelEmpty
from common.baseclasses.response import Response
from tests.conftest import client


@pytest.mark.sleep
class TestSleepNotes:
    ROUTE = "/api/sleep"
    STATUS_CODE_OK = 200
    STATUS_CODE_NOT_FOUND = 404
    STATUS_CODE_BAD_REQUEST = 400
    ARGS_NAMES = ['name', 'value', 'status_code', 'expected_schema']
    GET_ALL_NOTES_BY_USER_ID_ARGS = [
        ('id', 1, 200, SleepDiaryModel),
        ('user_id', 1, 200, SleepDiaryModel),
        ('user_id', "1", 200, SleepDiaryModel),
        ('id', 0, 404, SleepDiaryModelEmpty),
        ('id', "0", 404, SleepDiaryModelEmpty),
        ('id', "str_not_int", 400, ValidationError),
        ('not_id', 0, 400, ValidationError),
        ('not_id', "0", 400, ValidationError),
        ('not_id', "str_not_int", 400, ValidationError),
        ("", "", 400, ValidationError),
    ]

    @pytest.mark.parametrize(
        ARGS_NAMES,
        GET_ALL_NOTES_BY_USER_ID_ARGS,
        ids=[f" {arg[0]}|{arg[1]}|{arg[2]}" for arg in GET_ALL_NOTES_BY_USER_ID_ARGS]
    )
    def test_get_all_sleep_notes_by_user_id(
            self,
            name: str,
            value: str | int,
            status_code: int,
            expected_schema: Type[BaseModel] | ValidationError,
            client: FlaskClient,
            random_sleep_diary: SleepDiaryModel
    ):
        response = client.get(self.ROUTE, query_string={name: value})
        response = Response(response)
        if status_code == self.STATUS_CODE_OK:
            expectation = random_sleep_diary.model_dump(mode='json')
            response.assert_data(expectation)
        response.validate(expected_schema)
        response.assert_status_code(status_code)
