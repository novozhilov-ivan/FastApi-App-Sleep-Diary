import pytest
from flask import url_for
from flask.testing import FlaskClient
from werkzeug.datastructures import Authorization

from api.extension import bearer
from api.models import UserOrm
from api.routes.edit import response_not_found_404
from api.routes.edit.export_file import export_notes_endpoint
from api.utils.jwt import create_access_jwt
from api.utils.manage_notes import FileDataConverter
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.generators.diary import SleepDiaryGenerator
from common.pydantic_schemas.sleep.notes import SleepNote
from common.pydantic_schemas.user import UserValidate


@pytest.mark.edit_diary
@pytest.mark.edit_export
class TestEditExportNotes:
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
        response = client.get(
            path=url_for(
                endpoint=export_notes_endpoint,
            ),
            auth=jwt_access,
        )
        converter: FileDataConverter = FileDataConverter(data=saved_diary.notes)
        response = Response(response)
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
        response = client.get(
            path=url_for(
                endpoint=export_notes_endpoint,
            ),
            auth=jwt_with_non_exist_user_id,
        )
        response = Response(response)
        response.assert_status_code(HTTP.NOT_FOUND_404)
        response.assert_data(response_not_found_404)

    @pytest.mark.edit_export_404
    def test_export_notes_404_notes_dont_exist(
        self,
        client: FlaskClient,
        jwt_access: Authorization,
    ):
        response = client.get(
            path=url_for(
                endpoint=export_notes_endpoint,
            ),
            auth=jwt_access,
        )
        response = Response(response)
        response.assert_status_code(HTTP.NOT_FOUND_404)
        response.assert_data(response_not_found_404)
