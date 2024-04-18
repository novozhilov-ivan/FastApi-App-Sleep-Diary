from flask import request, Response
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from api.CRUD.notation_queries import get_all_notations_of_user
from api.routes.edit import ns_edit, import_response_model_200, csv_file_payload
from api.routes.sleep import user_id_params
from api.utils.manage_notes import WriteData
from common.pydantic_schemas.user import User


class EditRouteImport(Resource):
    @ns_edit.doc(description='Импортирование новых записей в дневник сна из файла')
    @ns_edit.expect(user_id_params, csv_file_payload)
    @ns_edit.response(**import_response_model_200)
    def post(self):
        imported_notes = request.files.to_dict()
        file = imported_notes['CSV файл']
        file_ext_allowed = ('csv',)
        if file.filename.split('.')[-1] not in file_ext_allowed:
            raise TypeError
        new_notes = WriteData(file=file)
        new_notes.to_model()
        new_notes = new_notes.data

        args = request.args.to_dict()
        user = User(**args)

        response = "All imported notes is created."
        status = 201
        return Response(response, status)
