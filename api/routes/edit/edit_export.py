from flask import request, Response, send_file
from flask_restx import Resource

from api.CRUD.notation_queries import get_all_notations_of_user
from api.routes.edit import ns_edit, export_response_model_200
from api.routes.sleep import user_id_params
from api.utils.manage_notes import convert_notes
from common.pydantic_schemas.sleep.notes import SleepNote, WriteData
from common.pydantic_schemas.user import User


class EditRouteExport(Resource):
    @ns_edit.doc(description='Экспорт всех записей дневника сна в файл')
    @ns_edit.expect(user_id_params)
    @ns_edit.response(**export_response_model_200)
    def get(self):
        args = request.args.to_dict()
        user = User(**args)
        user_id = user.id
        db_notes = get_all_notations_of_user(user_id)
        if not db_notes:
            status = 404
            response = "Not found"
            return Response(response, status)
        notes: list[SleepNote] = convert_notes(db_notes, SleepNote)
        WriteData.to_file(notes)
        return send_file('static/sleep_diary.csv', download_name='sleep_diary.csv')
