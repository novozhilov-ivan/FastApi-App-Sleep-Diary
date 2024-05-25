import pytest
from flask import url_for
from flask.testing import FlaskClient

from api.routes.notes import note_endpoint
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.generators.diary import SleepDiaryGenerator
from common.pydantic_schemas.sleep.notes import SleepNoteWithStats
from tests.test_api.test_auth.conftest import (
    access_token_header,
    exist_db_user_indirect_params,
    user_password_is_hashed,
    user_password_is_hashed_description,
)


@pytest.mark.parametrize(
    "exist_db_user",
    exist_db_user_indirect_params,
    indirect=user_password_is_hashed,
    ids=user_password_is_hashed_description,
)
@pytest.mark.parametrize(
    "generated_diary",
    (7,),
    indirect=True,
)
@pytest.mark.notes
@pytest.mark.notes_delete
class TestNoteDelete:

    @pytest.mark.notes_delete_204
    def test_note_delete_204(
        self,
        client: FlaskClient,
        access_token_header: dict,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        note: SleepNoteWithStats
        exist_note, *_ = saved_diary.notes
        response = client.delete(
            url_for(
                endpoint=note_endpoint,
                id=exist_note.id,
            ),
            headers=access_token_header,
        )
        response = Response(response)
        response.assert_status_code(HTTP.NO_CONTENT_204)
        response.assert_data(None)

    @pytest.mark.notes_delete_404
    def test_note_delete_404(
        self,
        client: FlaskClient,
        access_token_header: dict,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        note: SleepNoteWithStats
        *_, last_note = saved_diary.notes
        non_exist_note_id: int = 666 + last_note.id
        response = client.delete(
            url_for(
                endpoint=note_endpoint,
                id=non_exist_note_id,
            ),
            headers=access_token_header,
        )
        response = Response(response)
        response.assert_status_code(HTTP.NO_CONTENT_204)
        response.assert_data(None)
