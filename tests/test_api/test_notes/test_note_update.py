from datetime import datetime, timezone

import pytest
from flask import url_for
from flask.testing import FlaskClient
from pydantic import ValidationError

from api.models import User
from api.routes.notes import note_endpoint
from api.routes.notes.note_find_by_id import response_not_found_404
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.generators.diary import SleepDiaryGenerator
from common.generators.note import SleepNoteGenerator
from common.pydantic_schemas.errors.message import ErrorResponse
from common.pydantic_schemas.sleep.notes import (
    SleepNote,
    SleepNoteMeta,
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

    new_date = datetime.now(timezone.utc).timestamp() + 60 * 60 * 24 * 666
    new_note = SleepDiaryGenerator().create_note(date_of_note=new_date)
    new_note_dict = new_note.model_dump(exclude={"id", "user_id"})

    sleep_note_fields = tuple({field} for field in SleepNote.model_fields.keys())

    @pytest.mark.notes_200
    @pytest.mark.notes_update_200
    def test_note_update_200_all_values_is_same(
        self,
        client: FlaskClient,
        access_token_header: dict,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        exist_note: SleepNoteWithStats
        exist_note, *_ = saved_diary.notes
        updated_note = SleepNoteOptional.model_validate(exist_note)
        response = client.patch(
            url_for(
                endpoint=note_endpoint,
                id=exist_note.id,
            ),
            headers=access_token_header,
            json=updated_note.model_dump(
                mode="json",
            ),
        )
        response = Response(response)
        response.assert_status_code(HTTP.OK_200)
        expectation = SleepNote.model_validate(updated_note)
        response.validate(SleepNote)
        response.assert_data(expectation)

    @pytest.mark.notes_200
    @pytest.mark.notes_update_200
    def test_update_all_note_fields_200(
        self,
        client: FlaskClient,
        access_token_header: dict,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        exist_note: SleepNoteWithStats
        exist_note, *_ = saved_diary.notes
        exist_note_dict = exist_note.model_dump()
        exist_note_dict.update(self.new_note_dict)
        updated_note = SleepNoteOptional.model_validate(exist_note_dict)
        response = client.patch(
            url_for(
                endpoint=note_endpoint,
                id=exist_note.id,
            ),
            headers=access_token_header,
            json=updated_note.model_dump(
                mode="json",
            ),
        )
        expectation = SleepNote.model_validate(exist_note_dict)

        response = Response(response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(SleepNote)
        response.assert_data(expectation)

    @pytest.mark.notes_200
    @pytest.mark.notes_update_200
    @pytest.mark.parametrize(
        "exclude_fields",
        sleep_note_fields,
    )
    def test_update_all_note_fields_and_remove_one_field_200(
        self,
        client: FlaskClient,
        exclude_fields: set,
        access_token_header: dict,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        exist_note: SleepNoteWithStats
        exist_note, *_ = saved_diary.notes
        exist_note_dict = exist_note.model_dump()
        exist_note_dict.update(self.new_note_dict)
        updated_note = SleepNoteOptional.model_validate(exist_note_dict)
        response = client.patch(
            url_for(
                endpoint=note_endpoint,
                id=exist_note.id,
            ),
            headers=access_token_header,
            json=updated_note.model_dump(
                mode="json",
                exclude=exclude_fields,
            ),
        )
        exclude_field_with_value = exist_note.model_dump(include=exclude_fields)
        exist_note_dict.update(exclude_field_with_value)
        expectation = SleepNote.model_validate(exist_note_dict)

        response = Response(response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(SleepNote)
        response.assert_data(expectation)

    @pytest.mark.notes_404
    @pytest.mark.notes_update_404
    def test_note_update_404(
        self,
        client: FlaskClient,
        access_token_header: dict,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        exist_note: SleepNoteWithStats
        exist_note, *_ = saved_diary.notes
        exist_note.id = 666
        updated_note = SleepNoteOptional.model_validate(exist_note)
        response = client.patch(
            url_for(
                endpoint=note_endpoint,
                id=exist_note.id,
            ),
            headers=access_token_header,
            json=updated_note.model_dump(
                mode="json",
            ),
        )
        response = Response(response)
        response.assert_status_code(HTTP.NOT_FOUND_404)
        expectation = {"message": response_not_found_404}
        response.assert_data(expectation)

    @pytest.mark.notes_422
    @pytest.mark.notes_update_422
    @pytest.mark.parametrize(
        "wrong_note_id",
        (
            ("uid",),
            ("20:20:20",),
            (True,),
            (False,),
            (None,),
            ("[1, 2, 3]",),
            ("{id: 666}",),
        ),
    )
    def test_note_update_wrong_note_id_type_422(
        self,
        client: FlaskClient,
        wrong_note_id: tuple,
        access_token_header: dict,
        exist_db_user: User,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        exist_note: SleepNoteWithStats
        exist_note, *_ = saved_diary.notes
        updated_note = SleepNoteOptional.model_validate(exist_note)
        response = client.patch(
            url_for(
                endpoint=note_endpoint,
                id=wrong_note_id,
            ),
            headers=access_token_header,
            json=updated_note.model_dump(
                mode="json",
            ),
        )
        wrong_note_id_args = response.request.args
        response = Response(response)
        response.assert_status_code(HTTP.UNPROCESSABLE_ENTITY_422)

        with pytest.raises(ValidationError) as exc_info:
            SleepNoteMeta(
                user_id=exist_db_user.id,
                **wrong_note_id_args,
            )
        errors_expectations = ErrorResponse(message=exc_info.value.errors())
        response.assert_status_code(HTTP.UNPROCESSABLE_ENTITY_422)
        response.validate(ErrorResponse)
        response.assert_data(errors_expectations)

    @pytest.mark.notes_422
    @pytest.mark.notes_update_422
    @pytest.mark.parametrize(
        "exclude_fields",
        sleep_note_fields,
    )
    def test_note_update_wrong_payload_422(
        self,
        client: FlaskClient,
        exclude_fields: set,
        access_token_header: dict,
        saved_diary: SleepDiaryGenerator,
        generated_diary: SleepDiaryGenerator,
    ):
        exist_note: SleepNoteWithStats
        exist_note, *_ = saved_diary.notes
        wrong_note_generator = SleepNoteGenerator()
        updated_note_with_random_wrong_values = wrong_note_generator.wrong_note(
            errors_count=3,
            model=SleepNoteOptional,
            mode="json",
        )
        for exclude_field in exclude_fields:
            updated_note_with_random_wrong_values.pop(exclude_field)

        response = client.patch(
            url_for(
                endpoint=note_endpoint,
                id=exist_note.id,
            ),
            headers=access_token_header,
            json=updated_note_with_random_wrong_values,
        )
        response = Response(response)
        response.assert_status_code(HTTP.UNPROCESSABLE_ENTITY_422)

        exclude_field_with_value = exist_note.model_dump(include=exclude_fields)
        updated_note_with_random_wrong_values.update(exclude_field_with_value)
        with pytest.raises(ValidationError) as exc_info:
            SleepNoteOptional(**updated_note_with_random_wrong_values)
        errors_expectations = ErrorResponse(
            message=exc_info.value.errors(),
        )
        response.validate(ErrorResponse)
        response.assert_data(errors_expectations)
