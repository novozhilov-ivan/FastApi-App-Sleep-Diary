import pytest
from flask import url_for
from flask.testing import FlaskClient

from api.routes.notes import note_find_by_date_endpoint
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
@pytest.mark.notes_find_by_date
class TestNoteFindByDate:

    @pytest.mark.notes_200
    @pytest.mark.parametrize(
        "generated_diary",
        (7,),
        indirect=True,
    )
    def test_note_find_by_date_200(
        self,
        client: FlaskClient,
        access_token_header: dict,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        note, *_ = saved_diary.notes
        note: SleepNoteCompute
        response = client.get(
            url_for(
                endpoint=note_find_by_date_endpoint,
                calendar_date=note.calendar_date,
            ),
            headers=access_token_header,
        )
        response = Response(response)
        expectation = SleepNote(**note.model_dump())
        response.assert_status_code(HTTP.OK_200)
        response.validate(SleepNote)
        response.assert_data(expectation)
