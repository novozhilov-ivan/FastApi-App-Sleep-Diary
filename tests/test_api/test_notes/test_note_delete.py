import pytest
from flask import url_for
from flask.testing import FlaskClient
from werkzeug.datastructures import Authorization

from src.pydantic_schemas.sleep.notes import SleepNoteWithStats
from src.routes.notes import note_endpoint
from src.utils.status_codes import HTTP
from tests.generators.diary import SleepDiaryGenerator
from tests.test_api.response import Response


@pytest.mark.note
@pytest.mark.note_delete
@pytest.mark.parametrize(
    "generated_diary",
    (7,),
    indirect=True,
)
class TestNoteDelete:

    @pytest.mark.note_delete_204
    def test_note_delete_204(
        self,
        client: FlaskClient,
        jwt_access: Authorization,
        saved_diary: SleepDiaryGenerator,
    ):
        note: SleepNoteWithStats
        exist_note, *_ = saved_diary.notes
        raw_response = client.delete(
            path=url_for(
                endpoint=note_endpoint,
                id=exist_note.id,
            ),
            auth=jwt_access,
        )
        response = Response(raw_response)
        response.assert_status_code(HTTP.NO_CONTENT_204)
        response.assert_data(None)

    @pytest.mark.note_delete_404
    def test_note_delete_404(
        self,
        client: FlaskClient,
        jwt_access: Authorization,
        saved_diary: SleepDiaryGenerator,
    ):
        note: SleepNoteWithStats
        *_, last_note = saved_diary.notes
        non_exist_note_id: int = 666 + last_note.id
        raw_response = client.delete(
            path=url_for(
                endpoint=note_endpoint,
                id=non_exist_note_id,
            ),
            auth=jwt_access,
        )
        response = Response(raw_response)
        response.assert_status_code(HTTP.NO_CONTENT_204)
        response.assert_data(None)
