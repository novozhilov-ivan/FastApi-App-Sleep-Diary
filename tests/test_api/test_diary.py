import pytest
from flask import url_for
from flask.testing import FlaskClient
from pydantic import ValidationError
from werkzeug.datastructures import Authorization

from api.routes.diary import diary_endpoint
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.generators.diary import SleepDiaryGenerator
from common.pydantic_schemas.errors.message import ErrorResponse
from common.pydantic_schemas.sleep.diary import SleepDiaryModel, SleepDiaryModelEmpty
from common.pydantic_schemas.user import User


@pytest.mark.diary
class TestDiary:

    @pytest.mark.diary_200
    def test_get_diary_200(
        self,
        client: FlaskClient,
        jwt_access: Authorization,
        saved_diary: SleepDiaryGenerator,
    ):
        response = client.get(
            path=url_for(
                endpoint=diary_endpoint,
            ),
            auth=jwt_access,
        )
        response = Response(response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(SleepDiaryModel)
        response.assert_data(saved_diary.diary)

    @pytest.mark.diary_404
    def test_get_empty_diary_404(
        self,
        client: FlaskClient,
        jwt_access: Authorization,
    ):
        response = client.get(
            path=url_for(
                endpoint=diary_endpoint,
            ),
            auth=jwt_access,
        )
        response = Response(response)
        response.assert_status_code(HTTP.NOT_FOUND_404)
        response.validate(SleepDiaryModelEmpty)
        response.assert_data(SleepDiaryModelEmpty())

    @pytest.mark.diary_422
    @pytest.mark.xfail(reason="Изменилась имплементация тестируемого route'а.")
    def test_get_diary_wrong_user_id_422(
        self,
        client: FlaskClient,
        jwt_access: Authorization,
    ):
        response = client.get(
            path=url_for(
                endpoint=diary_endpoint,
            ),
            auth=jwt_access,
        )
        response = Response(response)
        with pytest.raises(ValidationError) as exc_info:
            User(**params)
        errors = ErrorResponse(
            message=exc_info.value.errors(),
        )
        response.assert_status_code(HTTP.UNPROCESSABLE_ENTITY_422)
        response.validate(ErrorResponse)
        response.assert_data(errors)
