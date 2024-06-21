import pytest
from flask import url_for
from flask.testing import FlaskClient
from werkzeug.datastructures import Authorization

from src.pydantic_schemas.sleep.notes import SleepNote, SleepNoteWithStats
from src.routes.notes import note_find_by_id_endpoint
from src.routes.notes.note_find_by_id import response_not_found_404
from src.utils.status_codes import HTTP
from tests.generators.diary import SleepDiaryGenerator
from tests.test_api.response import Response


@pytest.mark.note
@pytest.mark.note_find
@pytest.mark.note_find_by_id
class TestNoteFindById:

    @pytest.mark.note_find_by_id_200
    @pytest.mark.parametrize(
        "generated_diary",
        (7,),
        indirect=True,
    )
    def test_note_find_by_id_200(
        self,
        client: FlaskClient,
        jwt_access: Authorization,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        note, *_ = saved_diary.notes
        note: SleepNoteWithStats
        response = client.get(
            path=url_for(
                endpoint=note_find_by_id_endpoint,
                id=note.id,
            ),
            auth=jwt_access,
        )
        response = Response(response)
        expectation = SleepNote(**note.model_dump())
        response.assert_status_code(HTTP.OK_200)
        response.validate(SleepNote)
        response.assert_data(expectation)

    @pytest.mark.note_find_by_id_404
    def test_note_find_by_id_404(
        self,
        client: FlaskClient,
        jwt_access: Authorization,
    ):
        non_exist_note_id = 666
        response = client.get(
            path=url_for(
                endpoint=note_find_by_id_endpoint,
                id=non_exist_note_id,
            ),
            auth=jwt_access,
        )
        response = Response(response)
        expectation = {"message": response_not_found_404}
        response.assert_status_code(HTTP.NOT_FOUND_404)
        response.assert_data(expectation)
