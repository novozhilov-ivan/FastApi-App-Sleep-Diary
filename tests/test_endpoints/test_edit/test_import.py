import io

import pytest
from flask.testing import FlaskClient

from api.routes.edit.import_file import (
    response_bad_request_400,
    response_conflict_409,
    response_created_201,
    response_model_201,
    response_model_400,
    response_model_409,
    response_model_415,
    response_unsupported_media_type_415,
)
from api.utils.manage_notes import FileDataConverter
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.generators.diary import SleepDiaryGenerator


@pytest.mark.edit
@pytest.mark.import_notes
class TestEditImportNotes:
    ROUTE = "/api/edit/import"

    @staticmethod
    def import_file(
        str_file, file_name: str = "sleep_diary", file_extension: str = "csv"
    ) -> dict:
        str_bytes = str_file.encode()
        return {
            "file": (
                io.BytesIO(str_bytes),
                f"{file_name}.{file_extension}",
                "text/csv",
            )
        }

    @pytest.mark.import_201
    @pytest.mark.parametrize(
        "generated_diary",
        (7, 10),
        indirect=True,
    )
    def test_import_notes_201(
        self,
        db_user_id: int,
        generated_diary: SleepDiaryGenerator,
        client: FlaskClient,
    ):
        str_file = FileDataConverter(data=generated_diary.notes).to_csv_str()
        response = client.post(
            self.ROUTE,
            query_string={"id": db_user_id},
            data=self.import_file(str_file),
            content_type="multipart/form-data",
        )
        response = Response(response)
        response.assert_status_code(HTTP.CREATED_201)
        response.validate(response_model_201)
        response.assert_data(response_created_201)

    @pytest.mark.import_400
    @pytest.mark.import_wo_args_400
    def test_import_notes_wo_args_400(self, client: FlaskClient):
        random_notes = SleepDiaryGenerator().notes
        str_file = FileDataConverter(data=random_notes).to_csv_str()
        response = client.post(
            self.ROUTE,
            data=self.import_file(str_file),
            content_type="multipart/form-data",
        )
        response = Response(response)
        response.assert_status_code(HTTP.BAD_REQUEST_400)
        response.validate(response_model_400)
        response.assert_data(response_bad_request_400)

    @pytest.mark.import_400
    @pytest.mark.import_wo_payload_400
    def test_import_notes_wo_payload_400(self, db_user_id: int, client: FlaskClient):
        response = client.post(self.ROUTE, query_string={"id": db_user_id})
        response = Response(response)
        response.assert_status_code(HTTP.BAD_REQUEST_400)
        response.validate(response_model_400)
        response.assert_data(response_bad_request_400)

    @pytest.mark.import_415
    @pytest.mark.parametrize("extension", ("json", "xml", "pdf"))
    def test_import_notes_415(
        self, extension: str, db_user_id: int, client: FlaskClient
    ):
        random_notes = SleepDiaryGenerator(user_id=db_user_id).notes
        str_file = FileDataConverter(data=random_notes).to_csv_str()
        response = client.post(
            self.ROUTE,
            query_string={"id": db_user_id},
            data=self.import_file(str_file, file_extension=extension),
            content_type="multipart/form-data",
        )
        response = Response(response)
        response.assert_status_code(HTTP.UNSUPPORTED_MEDIA_TYPE_415)
        response.validate(response_model_415)
        response.assert_data(response_unsupported_media_type_415)

    @pytest.mark.import_409
    @pytest.mark.parametrize(
        "generated_diary",
        (7, 10),
        indirect=True,
    )
    def test_import_notes_409(
        self,
        client: FlaskClient,
        db_user_id: int,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        str_file = FileDataConverter(data=saved_diary.notes).to_csv_str()
        response = client.post(
            self.ROUTE,
            query_string={"id": db_user_id},
            data=self.import_file(str_file),
            content_type="multipart/form-data",
        )
        response = Response(response)
        response.assert_status_code(HTTP.CONFLICT_409)
        response.validate(response_model_409)
        response.assert_data(response_conflict_409)
