from flask import make_response
from flask_restx import Resource

from src.CRUD.sleep_note_table import find_all_user_notes
from src.pydantic_schemas.sleep.notes import SleepNote
from src.routes.edit import (
    ns_edit,
    response_model_404,
    response_model_422,
    response_not_found_404,
)
from src.routes.edit.export_file import response_model_200
from src.utils.auth import UserActions
from src.utils.manage_notes import (
    FileDataConverter,
    convert_db_notes_to_pydantic_model_notes,
)
from src.utils.status_codes import HTTP


class EditRouteExport(Resource, UserActions):
    """Экспорт всех записей дневника сна в файл"""

    @ns_edit.doc(description=__doc__)
    @ns_edit.response(**response_model_200)
    @ns_edit.response(**response_model_404)
    @ns_edit.response(**response_model_422)
    def get(self):
        db_notes = find_all_user_notes(user_id=self.current_user_id)
        if not db_notes:
            return response_not_found_404, HTTP.NOT_FOUND_404
        notes: list[SleepNote] = convert_db_notes_to_pydantic_model_notes(
            db_notes, SleepNote
        )
        file_str: str = FileDataConverter(notes).to_csv_str()
        response = make_response(file_str)
        response.status_code = HTTP.OK_200
        response.mimetype = "text/plain"
        response.headers.set(
            "Content-Disposition",
            "attachment",
            filename="sleep_diary.csv",
        )
        return response
