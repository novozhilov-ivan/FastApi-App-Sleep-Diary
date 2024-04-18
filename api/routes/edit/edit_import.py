from flask import request, Response
from flask_restx import Resource

from api.CRUD.notation_queries import create_many_notes
from api.models import Notation
from api.routes.edit import ns_edit, import_response_model_201, import_file_payload
from api.routes.sleep import user_id_params
from api.utils.manage_notes import FileDataConverter
from common.pydantic_schemas.user import User


class EditRouteImport(Resource):
    @ns_edit.doc(description='Импортирование новых записей в дневник сна из файла')
    @ns_edit.expect(user_id_params, import_file_payload)
    @ns_edit.response(**import_response_model_201)
    def post(self):
        imported_notes = request.files.to_dict()
        arg_name = import_file_payload.args[0].name
        file = imported_notes[arg_name]
        args = request.args.to_dict()
        user = User(**args)
        new_notes = FileDataConverter(file=file)
        new_notes.to_model(Notation, **user.model_dump(by_alias=True))
        new_notes = new_notes.data
        create_many_notes(new_notes)
        response = "All imported notes is created."
        status = 201
        return Response(response, status)
