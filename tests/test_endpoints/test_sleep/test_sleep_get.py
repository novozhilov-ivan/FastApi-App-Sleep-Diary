import pytest
from flask import url_for
from flask.testing import FlaskClient
from pydantic import ValidationError

from api.routes.sleep.diary import diary_endpoint
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.generators.diary import SleepDiaryGenerator
from common.pydantic_schemas.errors.message import ErrorResponse
from common.pydantic_schemas.sleep.diary import SleepDiaryModel, SleepDiaryModelEmpty
from common.pydantic_schemas.user import User
from tests.conftest import client


@pytest.mark.sleep
@pytest.mark.sleep_get
class TestSleepNotesGET:
    RESPONSE_MODEL_200 = SleepDiaryModel
    RESPONSE_MODEL_404 = SleepDiaryModelEmpty
    RESPONSE_MODEL_422 = ErrorResponse
    EMPTY_SLEEP_DIARY = SleepDiaryModelEmpty()
    SLEEP_PARAMS_NAMES = ["name", "value"]
    CORRECT_PARAMS_GET_NOTES_BY_USER_ID = [
        ("id", 1),
        ("id", "1"),
        ("user_id", 1),
        ("user_id", "1"),
    ]
    INCORRECT_PARAMETERS_GET_NOTES_BY_USER_ID = [
        ("id", "str_not_int"),
        ("user_id", "str_not_int"),
        ("not_id", 1),
        ("not_id", 0),
        ("not_id", "1"),
        ("not_id", "0"),
        ("not_id", "str_not_int"),
        ("", ""),
    ]

    @pytest.mark.sleep_200
    @pytest.mark.parametrize(
        SLEEP_PARAMS_NAMES,
        CORRECT_PARAMS_GET_NOTES_BY_USER_ID,
    )
    def test_get_all_sleep_notes_by_user_id_200(
        self,
        name: str,
        value: str | int,
        client: FlaskClient,
        saved_diary: SleepDiaryGenerator,
    ):
        response = client.get(
            url_for(diary_endpoint),
            query_string={name: value},
        )
        response = Response(response)
        expectation = saved_diary.diary
        response.assert_status_code(HTTP.OK_200)
        response.validate(self.RESPONSE_MODEL_200)
        response.assert_data(expectation)

    @pytest.mark.sleep_404
    @pytest.mark.parametrize(
        SLEEP_PARAMS_NAMES,
        CORRECT_PARAMS_GET_NOTES_BY_USER_ID,
    )
    def test_get_all_sleep_notes_by_user_id_404(
        self, name: str, value: str | int, client: FlaskClient
    ):
        response = client.get(
            url_for(diary_endpoint),
            query_string={name: value},
        )
        response = Response(response)
        response.assert_status_code(HTTP.NOT_FOUND_404)
        response.validate(self.RESPONSE_MODEL_404)
        response.assert_data(self.EMPTY_SLEEP_DIARY)

    @pytest.mark.sleep_get_422
    @pytest.mark.parametrize(
        SLEEP_PARAMS_NAMES, INCORRECT_PARAMETERS_GET_NOTES_BY_USER_ID
    )
    def test_get_all_sleep_notes_by_user_id_422(
        self, name: str, value: str | int, client: FlaskClient
    ):
        params = {name: value}
        response = client.get(
            url_for(diary_endpoint),
            query_string=params,
        )
        response = Response(response)
        with pytest.raises(ValidationError) as exc_info:
            User(**params)
        errors = self.RESPONSE_MODEL_422(message=exc_info.value.errors())
        response.assert_status_code(HTTP.UNPROCESSABLE_ENTITY_422)
        response.validate(self.RESPONSE_MODEL_422)
        response.assert_data(errors)
