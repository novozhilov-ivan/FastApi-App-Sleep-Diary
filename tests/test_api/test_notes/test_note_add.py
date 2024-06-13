import pytest
from flask import url_for
from flask.testing import FlaskClient
from pydantic import ValidationError
from werkzeug.datastructures import Authorization

from api.models import UserOrm
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


@pytest.mark.note
@pytest.mark.note_add
class TestNoteAdd:

    @pytest.mark.note_add_201
    @pytest.mark.repeat(10)
    def test_note_add_201(
        self,
        exist_user: UserOrm,
        jwt_access: Authorization,
        client: FlaskClient,
    ):
        notes_generator: SleepDiaryGenerator
        notes_generator = SleepDiaryGenerator(owner_id=exist_user.id)
        new_note_with_stat: SleepNoteWithStats
        new_note_with_stat, *_ = notes_generator.notes
        new_note = SleepNote.model_validate(new_note_with_stat)

        response = client.post(
            path=url_for(
                endpoint=note_endpoint,
            ),
            json=new_note.model_dump(
                mode="json",
            ),
            auth=jwt_access,
        )
        response = Response(response)
        response.assert_status_code(HTTP.CREATED_201)
        response.validate(SleepNoteModel)
        response.assert_data(new_note_with_stat)

    @pytest.mark.note_add_422
    @pytest.mark.repeat(10)
    def test_create_new_sleep_note_422(
        self,
        jwt_access: Authorization,
        client: FlaskClient,
    ):
        notes_generator = SleepNoteGenerator()
        note_with_wrong_values = notes_generator.wrong_note(
            mode="json",
        )
        response = client.post(
            path=url_for(
                endpoint=note_endpoint,
            ),
            json=note_with_wrong_values,
            auth=jwt_access,
        )
        response = Response(response)

        with pytest.raises(ValidationError) as exc_info:
            SleepNote.model_validate(note_with_wrong_values)
        errors_expectations = ErrorResponse(
            message=exc_info.value.errors(),
        )
        response.assert_status_code(HTTP.UNPROCESSABLE_ENTITY_422)
        response.validate(ErrorResponse)
        response.assert_data(errors_expectations)
