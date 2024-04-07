import pytest
from flask.testing import FlaskClient

from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTPStatusCodes
from common.generators.sleep_diary import SleepDiaryGenerator
from common.pydantic_schemas.sleep.notes import SleepNoteModel


@pytest.mark.sleep
@pytest.mark.sleep_post
class TestSleepNotesPost(HTTPStatusCodes):
    ROUTE = "/api/sleep"
    RESPONSE_MODEL_201 = SleepNoteModel

    @pytest.mark.sleep_201
    @pytest.mark.repeat(10)
    def test_create_new_sleep_note_201(self, app, db_user_id: int, client: FlaskClient):
        new_note = SleepDiaryGenerator(db_user_id)
        created_note = new_note.create_note()
        note_to_added = SleepNoteModel(**created_note.model_dump(by_alias=True))
        json_body = note_to_added.model_dump(mode='json')
        response = client.post(self.ROUTE, json=json_body)
        response = Response(response)
        response.assert_status_code(self.STATUS_CREATED)
        response.validate(self.RESPONSE_MODEL_201)
        response.assert_data(created_note)
