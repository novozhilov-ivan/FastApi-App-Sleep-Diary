from flask_restx import Resource

from src.CRUD.sleep_note_table import find_all_user_notes
from src.pydantic_schemas.sleep.diary import (
    SleepDiaryCompute,
    SleepDiaryModel,
    SleepDiaryModelEmpty,
)
from src.routes.diary import (
    ns_diary,
    response_model_200,
    response_model_400,
    response_model_404,
    response_model_422,
)
from src.utils.auth import UserActions
from src.utils.manage_notes import (
    convert_db_notes_to_pydantic_model_notes,
    slice_on_week,
)
from src.utils.status_codes import HTTP


class DiaryRoute(Resource, UserActions):
    """Получение всех записей дневника сна"""

    @ns_diary.doc(description=__doc__)
    @ns_diary.response(**response_model_200)
    @ns_diary.response(**response_model_404)
    @ns_diary.response(**response_model_400)
    @ns_diary.response(**response_model_422)
    def get(self):
        db_notes = find_all_user_notes(user_id=self.current_user_id)
        if not db_notes:
            return SleepDiaryModelEmpty().model_dump(), HTTP.NOT_FOUND_404
        pd_notes = convert_db_notes_to_pydantic_model_notes(db_notes)
        pd_weeks = slice_on_week(pd_notes)
        diary = SleepDiaryCompute(weeks=pd_weeks)
        diary = SleepDiaryModel(**diary.model_dump())
        return diary.model_dump(mode="json"), HTTP.OK_200
