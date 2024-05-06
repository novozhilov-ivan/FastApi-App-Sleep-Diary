from flask import make_response, request
from flask_restx import Resource

from api.CRUD.notations import read_all_user_notes
from api.routes.edit import (
    ns_edit,
    response_model_404,
    response_model_422,
    response_not_found_404,
)
from api.routes.edit.export_file import response_model_200
from api.routes.sleep import user_id_params
from api.utils.manage_notes import (
    FileDataConverter,
    convert_db_notes_to_pydantic_model_notes,
)
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import SleepNote
from common.pydantic_schemas.user import User


class EditRouteExport(Resource):
    """Экспорт всех записей дневника сна в файл"""

    @ns_edit.doc(description=__doc__)
    @ns_edit.expect(user_id_params)
    @ns_edit.response(**response_model_200)
    @ns_edit.response(**response_model_404)
    @ns_edit.response(**response_model_422)
    def get(self):
        user = User(**request.args)
        db_notes = read_all_user_notes(user.id)
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
