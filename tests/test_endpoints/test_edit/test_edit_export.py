import pytest
from flask.testing import FlaskClient

from api.utils.manage_notes import FileDataConverter
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.generators.diary import SleepDiaryGenerator
from common.pydantic_schemas.sleep.notes import SleepNote


@pytest.mark.edit
@pytest.mark.export
class TestEditExportNotes:
    ROUTE = "/api/edit/export"

    @pytest.mark.export_200
    def test_export_notes_200(
            self,
            client: FlaskClient,
            db_user_id: int,
            saved_diary: SleepDiaryGenerator
    ):
        response = client.get(self.ROUTE, query_string={'id': db_user_id})
        response = Response(response)
        str_file = FileDataConverter(saved_diary.notes).to_csv_str()
        response.assert_status_code(HTTP.OK_200)
        response.validate(SleepNote)
        response.assert_data(str_file)
