from legacy_src.extension import db
from legacy_tests.generators.diary import SleepDiaryGenerator

import pytest

from flask import url_for
from flask.testing import FlaskClient
from sqlalchemy import select
from werkzeug.datastructures import Authorization

from src.models import (
    SleepNoteOrm,
    UserOrm,
)
from src.routes.edit.delete_diary import delete_notes_endpoint
from src.utils.status_codes import HTTP
from tests.api.response import Response


@pytest.mark.edit_diary
@pytest.mark.edit_delete
class TestEditDeleteAllNotes:
    @pytest.mark.edit_delete_204
    @pytest.mark.parametrize(
        "generated_diary",
        (7, 10),
        indirect=True,
    )
    def test_delete_notes_204(
        self,
        client: FlaskClient,
        exist_user: UserOrm,
        jwt_access: Authorization,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        raw_response = client.delete(
            path=url_for(
                endpoint=delete_notes_endpoint,
            ),
            auth=jwt_access,
        )
        response = Response(raw_response)
        response.assert_status_code(HTTP.NO_CONTENT_204)
        response.assert_data(None)

        with client.application.app_context():
            one_note = db.session.execute(
                select(SleepNoteOrm).filter_by(
                    owner_oid=exist_user.id,
                ),
            ).scalar_one_or_none()
        note_is_exist = isinstance(one_note, SleepNoteOrm)
        assert note_is_exist is False, f"Now user notes is exist = [{note_is_exist}]"
