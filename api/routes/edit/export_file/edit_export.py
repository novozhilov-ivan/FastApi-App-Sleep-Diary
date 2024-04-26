from flask import request, make_response
from flask_restx import Resource

from api.CRUD.notation_queries import read_all_notations_of_user
from api.exceptions.errors import NotFoundError
from api.routes.edit import ns_edit
from api.routes.edit.export_file import export_response_model_200, export_response_model_404
from api.routes.sleep import user_id_params
from api.utils.manage_notes import convert_db_notes_to_pydantic_model_notes, FileDataConverter
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import SleepNote
from common.pydantic_schemas.user import User


class EditRouteExport(Resource):
    @ns_edit.doc(description='Экспорт всех записей дневника сна в файл')
    @ns_edit.expect(user_id_params)
    @ns_edit.response(**export_response_model_200)
    @ns_edit.response(**export_response_model_404)
    def get(self):
        args = request.args.to_dict()
        user_id = User(**args).id
        db_notes = read_all_notations_of_user(user_id)
        if not db_notes:
            raise NotFoundError
        notes: list[SleepNote] = convert_db_notes_to_pydantic_model_notes(db_notes, SleepNote)
        file_str: str = FileDataConverter(notes).to_csv_str()
        response = make_response(file_str)
        response.status_code = HTTP.OK_200
        response.mimetype = 'text/plain'
        response.headers.set(
            'Content-Disposition',
            'attachment',
            filename='sleep_diary.csv'
        )
        return response
