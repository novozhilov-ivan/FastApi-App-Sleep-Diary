import pytest
from flask import url_for
from flask.testing import FlaskClient
from werkzeug.datastructures import Authorization

from src.extension import bearer
from src.models import UserOrm
from src.pydantic_schemas.sleep.notes import SleepNote
from src.pydantic_schemas.user import UserValidate
from src.routes.edit import response_not_found_404
from src.routes.edit.export_file import export_notes_endpoint
from src.utils.jwt import create_access_jwt
from src.utils.manage_notes import FileDataConverter
from src.utils.status_codes import HTTP
from tests.generators.diary import SleepDiaryGenerator
from tests.test_api.response import Response


@pytest.mark.edit_diary
@pytest.mark.edit_export
class TestEditExportNotes:
    @pytest.mark.xfail(
        reason="DDD Рефакторинг. Убрал Field(title=...) из SleepNote.",
    )
    @pytest.mark.edit_export_200
    @pytest.mark.parametrize(
        "generated_diary",
        (7, 10),
        indirect=True,
    )
    def test_export_notes_200(
        self,
        client: FlaskClient,
        jwt_access: Authorization,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        raw_response = client.get(
            path=url_for(
                endpoint=export_notes_endpoint,
            ),
            auth=jwt_access,
        )
        converter: FileDataConverter = FileDataConverter(data=saved_diary.notes)
        response = Response(raw_response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(SleepNote)
        response.assert_data(converter.to_csv_str())

    @pytest.mark.edit_export_404
    def test_export_notes_404_user_dont_exist(
        self,
        client: FlaskClient,
        exist_user: UserOrm,
    ):
        user = UserValidate.model_validate(exist_user)
        user.id = 999
        jwt_with_non_exist_user_id = Authorization(
            auth_type=bearer,
            token=create_access_jwt(user),
        )
        raw_response = client.get(
            path=url_for(
                endpoint=export_notes_endpoint,
            ),
            auth=jwt_with_non_exist_user_id,
        )
        response = Response(raw_response)
        response.assert_status_code(HTTP.NOT_FOUND_404)
        response.assert_data(response_not_found_404)

    @pytest.mark.edit_export_404
    def test_export_notes_404_notes_dont_exist(
        self,
        client: FlaskClient,
        jwt_access: Authorization,
    ):
        raw_response = client.get(
            path=url_for(
                endpoint=export_notes_endpoint,
            ),
            auth=jwt_access,
        )
        response = Response(raw_response)
        response.assert_status_code(HTTP.NOT_FOUND_404)
        response.assert_data(response_not_found_404)
