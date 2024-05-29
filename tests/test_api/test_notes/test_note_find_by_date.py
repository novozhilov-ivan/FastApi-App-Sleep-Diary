import datetime

import pytest
from flask import url_for
from flask.testing import FlaskClient

from api.routes.notes import note_find_by_date_endpoint
from api.routes.notes.note_find_by_date import response_not_found_404
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.generators.diary import SleepDiaryGenerator
from common.pydantic_schemas.sleep.notes import (
    DateOfSleepNote,
    SleepNote,
    SleepNoteWithStats,
)
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
        note: SleepNoteWithStats
        response = client.get(
            url_for(
                endpoint=note_find_by_date_endpoint,
                sleep_date=note.sleep_date,
            ),
            headers=access_token_header,
        )
        response = Response(response)
        expectation = SleepNote(**note.model_dump())
        response.assert_status_code(HTTP.OK_200)
        response.validate(SleepNote)
        response.assert_data(expectation)

    def test_note_find_by_date_404(
        self,
        client: FlaskClient,
        access_token_header: dict,
    ):
        non_exist_note_date = DateOfSleepNote(
            sleep_date=datetime.date(day=22, month=12, year=2020),
        )
        response = client.get(
            url_for(
                endpoint=note_find_by_date_endpoint,
                sleep_date=non_exist_note_date.sleep_date,
            ),
            headers=access_token_header,
        )
        response = Response(response)
        expectation = {"message": response_not_found_404}
        response.assert_status_code(HTTP.NOT_FOUND_404)
        response.assert_data(expectation)
