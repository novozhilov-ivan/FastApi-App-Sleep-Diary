from datetime import datetime, timezone

import pytest
from flask import url_for
from flask.testing import FlaskClient

from api.routes.notes import note_endpoint
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.generators.diary import SleepDiaryGenerator
from common.pydantic_schemas.sleep.notes import (
    SleepNote,
    SleepNoteOptional,
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
@pytest.mark.parametrize(
    "generated_diary",
    (7,),
    indirect=True,
)
@pytest.mark.notes
@pytest.mark.notes_update
class TestNoteUpdate:

    # TODO создать тест для ответа с 200
    #  с параметрами:
    #  1. все поля прежние
    #  2. все поля изменены
    #  3. все поля изменены и одно поле отсутствует,
    #  3. так сделать для каждого поля

    new_date = datetime.now(timezone.utc).timestamp() + 60 * 60 * 24 * 666
    new_note = SleepDiaryGenerator().create_note(date_of_note=new_date)

    @pytest.mark.notes_200
    @pytest.mark.notes_update_200
    @pytest.mark.parametrize(
        "exclude_fields",
        (
            {
                "awake",
            },
        ),
    )
    def test_note_update_200(
        self,
        client: FlaskClient,
        exclude_fields: set,
        access_token_header: dict,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        exist_note_with_stats: SleepNoteWithStats
        exist_note_with_stats, *_ = saved_diary.notes
        note_optional_fields: SleepNoteOptional = SleepNoteOptional(
            **exist_note_with_stats.model_dump(),
        )
        note_optional_fields: dict = note_optional_fields.model_dump()
        note_optional_fields.update(self.new_note.model_dump())
        note_optional_fields: SleepNoteOptional = SleepNoteOptional(
            **note_optional_fields,
        )
        payload = note_optional_fields.model_dump(
            mode="json",
            exclude=exclude_fields,
        )
        query = {"id": exist_note_with_stats.user_id}
        print(payload, query)
        # TODO Доделать тест и роут
        response = client.patch(
            url_for(endpoint=note_endpoint),
            json=payload,
            query_string=query,
            headers=access_token_header,
        )
        response = Response(response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(SleepNote)
        response.assert_data(None)

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
