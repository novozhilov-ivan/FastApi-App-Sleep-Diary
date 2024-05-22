import pytest
from flask.testing import FlaskClient

from common.generators.diary import SleepDiaryGenerator
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
@pytest.mark.parametrize(
    "generated_diary",
    (7,),
    indirect=True,
)
@pytest.mark.notes
@pytest.mark.notes_update
class TestNoteUpdate:

    @pytest.mark.notes_200
    @pytest.mark.notes_update_200
    def test_note_update_200(
        self,
        client: FlaskClient,
        access_token_header: dict,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        pass

    @pytest.mark.notes_404
    @pytest.mark.notes_update_404
    def test_note_update_404(
        self,
        client: FlaskClient,
        access_token_header: dict,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        pass

    @pytest.mark.notes_422
    @pytest.mark.notes_update_422
    def test_note_update_422(
        self,
        client: FlaskClient,
        access_token_header: dict,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        pass


# TODO Написать тесты
