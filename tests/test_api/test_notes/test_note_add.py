import pytest
from flask import url_for
from flask.testing import FlaskClient
from pydantic import ValidationError

from api.routes.notes import note_endpoint
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.generators.diary import SleepDiaryGenerator
from common.generators.note import SleepNoteGenerator
from common.pydantic_schemas.errors.message import ErrorResponse
from common.pydantic_schemas.sleep.notes import (
    SleepNote,
    SleepNoteModel,
    SleepNoteWithStats,
)


@pytest.mark.sleep
@pytest.mark.sleep_post
class TestSleepNotesPost:

    @pytest.mark.sleep_201
    @pytest.mark.repeat(10)
    def test_create_new_sleep_note_201(
        self,
        db_user_id: int,
        client: FlaskClient,
    ):
        new_note = SleepDiaryGenerator(db_user_id)
        created_note: SleepNoteWithStats = new_note.create_note()
        response = client.post(
            url_for(
                endpoint=note_endpoint,
                user_id=db_user_id,
            ),
            json=created_note.model_dump(
                mode="json",
                exclude={
                    "user_id",
                    "id",
                },
            ),
        )
        response = Response(response)
        response.assert_status_code(HTTP.CREATED_201)
        response.validate(SleepNoteModel)
        response.assert_data(created_note)

    @pytest.mark.sleep_post_422
    @pytest.mark.repeat(10)
    def test_create_new_sleep_note_422(
        self,
        db_user_id: int,
        client: FlaskClient,
    ):
        random_note_wrong_values = SleepNoteGenerator().wrong_note(
            mode="json",
        )
        response = client.post(
            url_for(
                note_endpoint,
                id=db_user_id,
            ),
            json=random_note_wrong_values,
        )
        response = Response(response)

        with pytest.raises(ValidationError) as exc_info:
            SleepNote(**random_note_wrong_values)
        errors_expectations = ErrorResponse(
            message=exc_info.value.errors(),
        )
        response.assert_status_code(HTTP.UNPROCESSABLE_ENTITY_422)
        response.validate(ErrorResponse)
        response.assert_data(errors_expectations)
