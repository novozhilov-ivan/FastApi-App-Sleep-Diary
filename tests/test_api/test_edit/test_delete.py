import pytest
from flask import url_for
from flask.testing import FlaskClient
from sqlalchemy import select

from api import db
from api.models import DreamNote
from api.routes.edit.delete_diary import delete_notes_endpoint
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.generators.diary import SleepDiaryGenerator


@pytest.mark.edit
@pytest.mark.delete
class TestEditDeleteAllNotes:
    @pytest.mark.delete_200
    @pytest.mark.parametrize(
        "generated_diary",
        (7, 10),
        indirect=True,
    )
    def test_delete_notes_200(
        self,
        client: FlaskClient,
        exist_user_id: int,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        query = {"id": exist_user_id}
        response = client.delete(
            url_for(
                delete_notes_endpoint,
                **query,
            )
        )
        expectation = None
        response = Response(response)
        response.assert_status_code(HTTP.NO_CONTENT_204)
        response.assert_data(expectation)

        with client.application.app_context():
            notes_is_exist = db.session.execute(
                select(
                    DreamNote,
                ).where(
                    DreamNote.user_id == exist_user_id,
                )
            ).first()
        notes_is_exist = bool(notes_is_exist)
        assert notes_is_exist is False, f"User notes exist now is [{notes_is_exist}]"
