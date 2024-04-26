import pytest
from flask.testing import FlaskClient

from api.utils.manage_notes import FileDataConverter
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTPStatusCodes
from common.generators.diary import SleepDiaryGenerator
from common.pydantic_schemas.sleep.notes import SleepNote


@pytest.mark.edit
@pytest.mark.export
class TestEditExportNotes(HTTPStatusCodes):
    ROUTE = "/api/edit/export"
    SLEEP_PARAMS_NAMES = ['name', 'value']
    RESPONSE_MODEL_200 = SleepNote
    CORRECT_PARAMS_GET_NOTES_BY_USER_ID = [
        ('id', 1),
        ('user_id', 1),
    ]

    @pytest.mark.export_200
    @pytest.mark.parametrize(
        SLEEP_PARAMS_NAMES,
        CORRECT_PARAMS_GET_NOTES_BY_USER_ID
    )
    def test_export_notes_200(
            self,
            name: str,
            value: str | int,
            client: FlaskClient,
            fake_diary: SleepDiaryGenerator
    ):
        response = client.get(self.ROUTE, query_string={name: value})
        response = Response(response)
        expectation = fake_diary.notes
        expectation = FileDataConverter(expectation).to_csv_str()
        response.assert_status_code(self.STATUS_OK_200)
        response.validate(self.RESPONSE_MODEL_200)
        response.assert_data(expectation)
