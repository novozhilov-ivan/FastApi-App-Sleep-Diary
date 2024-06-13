import io

import pytest
from flask import url_for
from flask.testing import FlaskClient
from werkzeug.datastructures import Authorization

from api.models import UserOrm
from api.routes.edit.import_file import (
    import_notes_endpoint,
    response_bad_request_400,
    response_conflict_409,
    response_created_201,
    response_unsupported_media_type_415,
)
from api.utils.manage_notes import FileDataConverter
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.generators.diary import SleepDiaryGenerator


@pytest.mark.edit_diary
@pytest.mark.edit_import
class TestImportNotes:
    content_type = "multipart/form-data"

    @staticmethod
    def import_file(
        str_file,
        file_name: str = "sleep_diary",
        file_extension: str = "csv",
    ) -> dict:
        str_bytes = str_file.encode()
        return {
            "file": (
                io.BytesIO(str_bytes),
                f"{file_name}.{file_extension}",
                "text/csv",
            )
        }

    @pytest.mark.edit_import_201
    @pytest.mark.parametrize(
        "generated_diary",
        (7, 10),
        indirect=True,
    )
    def test_import_notes_201(
        self,
        generated_diary: SleepDiaryGenerator,
        client: FlaskClient,
        jwt_access: Authorization,
    ):
        str_file = FileDataConverter(
            data=generated_diary.notes,
        ).to_csv_str()
        response = client.post(
            path=url_for(
                endpoint=import_notes_endpoint,
            ),
            auth=jwt_access,
            content_type=self.content_type,
            data=self.import_file(
                str_file=str_file,
            ),
        )
        response = Response(response)
        response.assert_status_code(HTTP.CREATED_201)
        response.assert_data(response_created_201)

    @pytest.mark.edit_import_400
    def test_import_notes_400(
        self,
        client: FlaskClient,
        jwt_access: Authorization,
    ):
        response = client.post(
            path=url_for(
                endpoint=import_notes_endpoint,
            ),
            auth=jwt_access,
        )
        response = Response(response)
        response.assert_status_code(HTTP.BAD_REQUEST_400)
        response.assert_data(response_bad_request_400)

    @pytest.mark.edit_import_409
    @pytest.mark.parametrize(
        "generated_diary",
        (7, 10),
        indirect=True,
    )
    def test_import_notes_409(
        self,
        client: FlaskClient,
        jwt_access: Authorization,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        str_file = FileDataConverter(data=saved_diary.notes).to_csv_str()
        response = client.post(
            path=url_for(
                endpoint=import_notes_endpoint,
            ),
            auth=jwt_access,
            content_type=self.content_type,
            data=self.import_file(
                str_file=str_file,
            ),
        )
        response = Response(response)
        response.assert_status_code(HTTP.CONFLICT_409)
        response.assert_data(response_conflict_409)

    @pytest.mark.edit_import_415
    @pytest.mark.parametrize("extension", ("json", "xml", "pdf"))
    def test_import_notes_415(
        self,
        extension: str,
        exist_user: UserOrm,
        client: FlaskClient,
        jwt_access: Authorization,
    ):
        diary_generator = SleepDiaryGenerator(owner_id=exist_user.id)
        str_file = FileDataConverter(data=diary_generator.notes).to_csv_str()
        response = client.post(
            path=url_for(
                endpoint=import_notes_endpoint,
            ),
            auth=jwt_access,
            content_type=self.content_type,
            data=self.import_file(
                str_file=str_file,
                file_extension=extension,
            ),
        )
        response = Response(response)
        response.assert_status_code(HTTP.UNSUPPORTED_MEDIA_TYPE_415)
        response.assert_data(response_unsupported_media_type_415)
