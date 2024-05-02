import pytest
from flask import url_for
from flask.testing import FlaskClient

from api.routes.edit import response_not_found_404
from api.routes.edit.export_file import export_notes_endpoint
from api.utils.manage_notes import FileDataConverter
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.generators.diary import SleepDiaryGenerator
from common.pydantic_schemas.sleep.notes import SleepNote


@pytest.mark.edit
@pytest.mark.export
class TestEditExportNotes:
    @pytest.mark.export_200
    @pytest.mark.parametrize(
        "generated_diary",
        (7, 10),
        indirect=True,
    )
    def test_export_notes_200(
        self,
        client: FlaskClient,
        db_user_id: int,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        query = {"id": db_user_id}
        response = client.get(
            url_for(
                export_notes_endpoint,
                **query,
            )
        )
        str_file = FileDataConverter(saved_diary.notes).to_csv_str()
        response = Response(response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(SleepNote)
        response.assert_data(str_file)

    @pytest.mark.export_404
    @pytest.mark.export_404_user
    def test_export_notes_404_user_dont_exist(
        self,
        client: FlaskClient,
    ):
        dont_exist_user_id = 999
        query = {"id": dont_exist_user_id}
        response = client.get(
            url_for(
                export_notes_endpoint,
                **query,
            )
        )
        response = Response(response)
        response.assert_status_code(HTTP.NOT_FOUND_404)
        response.assert_data(response_not_found_404)

    @pytest.mark.export_404
    @pytest.mark.export_404_notes
    def test_export_notes_404_notes_dont_exist(
        self,
        client: FlaskClient,
        db_user_id: int,
    ):
        query = {"id": db_user_id}
        response = client.get(
            url_for(
                export_notes_endpoint,
                **query,
            )
        )
        response = Response(response)
        response.assert_status_code(HTTP.NOT_FOUND_404)
        response.assert_data(response_not_found_404)
