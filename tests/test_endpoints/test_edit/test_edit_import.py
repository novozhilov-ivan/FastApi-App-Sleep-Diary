import io

import pytest
from flask import Flask
from flask.testing import FlaskClient

from api.routes.edit.import_file import import_success_response
from api.utils.manage_notes import FileDataConverter
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTPStatusCodes
from common.generators.diary import SleepDiaryGenerator


@pytest.mark.edit
@pytest.mark.import_notes
class TestEditImportNotes(HTTPStatusCodes):
    ROUTE = "/api/edit/import"
    SLEEP_PARAMS_NAMES = ['name', 'value']
    RESPONSE_MODEL_201 = import_success_response
    CORRECT_PARAMS_GET_NOTES_BY_USER_ID = [
        ('id', 1),
        ('user_id', 1),
    ]

    @pytest.mark.import_201
    @pytest.mark.parametrize(
        SLEEP_PARAMS_NAMES,
        CORRECT_PARAMS_GET_NOTES_BY_USER_ID
    )
    def test_export_notes_200(
            self,
            name: str,
            value: str | int,
            app: Flask,
            client: FlaskClient,
            db_user_id: int,
    ):
        random_notes = SleepDiaryGenerator(db_user_id, notes_count=5).notes
        str_file = FileDataConverter(data=random_notes).to_csv_str()
        str_bytes = str_file.encode()
        data = {'file': (io.BytesIO(str_bytes), 'sleep_diary.csv', 'text/csv')}
        response = client.post(
            self.ROUTE,
            query_string={name: value},
            data=data,
            content_type='multipart/form-data'
        )
        response = Response(response)
        response.assert_status_code(self.STATUS_CREATED_201)
        response.validate(self.RESPONSE_MODEL_201)
        response.assert_data(import_success_response)
