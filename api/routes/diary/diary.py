from flask import request
from flask_restx import Resource

from api.CRUD.dream_notes import find_all_user_notes
from api.routes.diary import (
    ns_diary,
    response_model_200,
    response_model_400,
    response_model_404,
    response_model_422,
    user_id_params,
)
from api.utils.manage_notes import (
    convert_db_notes_to_pydantic_model_notes,
    slice_on_week,
)
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.diary import (
    SleepDiaryCompute,
    SleepDiaryModel,
    SleepDiaryModelEmpty,
)
from common.pydantic_schemas.user import User


class DiaryRoute(Resource):
    """Получение всех записей дневника сна"""

    @ns_diary.doc(description=__doc__)
    @ns_diary.expect(user_id_params)
    @ns_diary.response(**response_model_200)
    @ns_diary.response(**response_model_404)
    @ns_diary.response(**response_model_400)
    @ns_diary.response(**response_model_422)
    def get(self):
        user = User(**request.args)
        db_notes = find_all_user_notes(user.id)
        if not db_notes:
            return SleepDiaryModelEmpty().model_dump(), HTTP.NOT_FOUND_404
        pd_notes = convert_db_notes_to_pydantic_model_notes(db_notes)
        pd_weeks = slice_on_week(pd_notes)
        diary = SleepDiaryCompute(weeks=pd_weeks)
        diary = SleepDiaryModel(**diary.model_dump())
        return diary.model_dump(mode="json"), HTTP.OK_200
