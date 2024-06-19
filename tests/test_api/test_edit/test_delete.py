import pytest
from flask import url_for
from flask.testing import FlaskClient
from sqlalchemy import select
from werkzeug.datastructures import Authorization

from src.extension import db
from src.models import SleepNoteOrm, UserOrm
from src.routes.edit.delete_diary import delete_notes_endpoint
from src.utils.status_codes import HTTP
from tests.generators.diary import SleepDiaryGenerator
from tests.response import Response


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
        response = client.delete(
            path=url_for(
                endpoint=delete_notes_endpoint,
            ),
            auth=jwt_access,
        )
        response = Response(response)
        response.assert_status_code(HTTP.NO_CONTENT_204)
        response.assert_data(None)

        with client.application.app_context():
            notes_is_exist = db.session.execute(
                select(SleepNoteOrm).filter_by(
                    owner_id=exist_user.id,
                )
            ).first()

        notes_is_exist = bool(notes_is_exist)
        assert notes_is_exist is False, f"User notes exist now is [{notes_is_exist}]"
