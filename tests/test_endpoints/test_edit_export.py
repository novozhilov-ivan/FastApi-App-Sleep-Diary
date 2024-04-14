import pytest
from flask.testing import FlaskClient

from api.utils.manage_notes import WriteData
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTPStatusCodes
from common.pydantic_schemas.sleep.notes import SleepNoteCompute, SleepNote


@pytest.mark.edit
@pytest.mark.export
class TestExportNotes(HTTPStatusCodes):
    ROUTE = "/api/edit/export"
    SLEEP_PARAMS_NAMES = ['name', 'value']
    CORRECT_PARAMS_GET_NOTES_BY_USER_ID = [
        ('id', 1),
        ('id', "1"),
        ('user_id', 1),
        ('user_id', "1")
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
            sleep_diary_notes: list[SleepNoteCompute]
    ):
        response = client.get(self.ROUTE, query_string={name: value})
        response = Response(response)
        expectation = sleep_diary_notes
        expectation = WriteData(expectation).to_csv_str()
        response.assert_status_code(self.STATUS_OK_200)
        response.validate(SleepNote)
        response.assert_data(expectation)
