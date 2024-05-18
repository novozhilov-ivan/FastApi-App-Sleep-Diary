import pytest
from flask.testing import FlaskClient

from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.generators.diary import SleepDiaryGenerator
from common.pydantic_schemas.sleep.notes import SleepNote, SleepNoteCompute
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
@pytest.mark.notes
@pytest.mark.notes_find
class TestNoteFind:

    @pytest.mark.notes_200
    @pytest.mark.parametrize(
        "generated_diary",
        (1,),
        indirect=True,
    )
    def test_note_find_by_id_200(
        self,
        client: FlaskClient,
        access_token_header: dict,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        some_note, *_ = saved_diary.notes
        some_note: SleepNoteCompute
        response = client.get(
            # f"{url_for(note_endpoint)}/{some_note.id}",
            "/api/note/1",
            headers=access_token_header,
        )
        response = Response(response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(SleepNote)
        response.assert_data(some_note)
