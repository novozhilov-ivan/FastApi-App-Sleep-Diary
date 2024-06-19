from datetime import date

import pytest
from flask import url_for
from flask.testing import FlaskClient
from werkzeug.datastructures import Authorization

from src.pydantic_schemas.sleep.notes import (
    SleepNote,
    SleepNoteOptional,
    SleepNoteWithStats,
)
from src.routes.notes import note_find_by_date_endpoint
from src.routes.notes.note_find_by_date import response_not_found_404
from src.utils.status_codes import HTTP
from tests.generators.diary import SleepDiaryGenerator
from tests.response import Response


@pytest.mark.note
@pytest.mark.note_find
@pytest.mark.note_find_by_date
class TestNoteFindByDate:

    @pytest.mark.note_find_by_date_200
    @pytest.mark.parametrize(
        "generated_diary",
        (7,),
        indirect=True,
    )
    def test_note_find_by_date_200(
        self,
        client: FlaskClient,
        jwt_access: Authorization,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        note: SleepNoteWithStats
        note, *_ = saved_diary.notes
        response = client.get(
            path=url_for(
                endpoint=note_find_by_date_endpoint,
                sleep_date=note.sleep_date,
            ),
            auth=jwt_access,
        )
        response = Response(response)

        response.assert_status_code(HTTP.OK_200)
        response.validate(SleepNote)
        expectation = SleepNote.model_validate(
            note.model_dump(
                exclude={
                    "id",
                    "user_id",
                },
            ),
        )
        response.assert_data(expectation)

    @pytest.mark.note_find_by_date_404
    def test_note_find_by_date_404(
        self,
        client: FlaskClient,
        jwt_access: Authorization,
    ):
        non_exist_note_date = date(day=22, month=12, year=2020)
        non_exist_note = SleepNoteOptional(sleep_date=non_exist_note_date)
        response = client.get(
            url_for(
                endpoint=note_find_by_date_endpoint,
                sleep_date=non_exist_note.sleep_date,
            ),
            auth=jwt_access,
        )
        response = Response(response)
        expectation = {"message": response_not_found_404}
        response.assert_status_code(HTTP.NOT_FOUND_404)
        response.assert_data(expectation)
