import sqlalchemy
from flask import request, Response
from flask_restx import Resource
from flask_restx.reqparse import Argument

from api.CRUD.notation_queries import create_many_notes
from api.models import Notation
from api.routes.edit import ns_edit
from api.routes.edit.import_file import import_file_payload, import_response_model_201, allowed_file_extensions, \
    import_success_response
from api.routes.sleep import user_id_params
from api.utils.manage_notes import FileDataConverter
from common.baseclasses.status_codes import HTTPStatusCodes
from common.pydantic_schemas.user import User


class EditRouteImport(Resource):
    @ns_edit.doc(description='Импортирование новых записей в дневник сна из файла')
    @ns_edit.expect(user_id_params, import_file_payload)
    @ns_edit.response(**import_response_model_201)
    def post(self):
        payload_arg: Argument
        arg: Argument
        payload_arg, *_ = import_file_payload.args
        args = request.args.to_dict()
        file = request.files.get(payload_arg.name)

        # if MAX_CONTENT_LENGTH > 1024 * 1024: raise http 413 file too large
        if file is None or not args:
            return Response('Not payload', HTTPStatusCodes.STATUS_BAD_REQUEST_400)
        *_, file_extension = file.filename.split('.')
        if file_extension not in allowed_file_extensions:
            return Response('File extension not allowed', HTTPStatusCodes.UNSUPPORTED_MEDIA_TYPE_415)

        user = User(**args)
        new_notes = FileDataConverter(file=file)
        new_notes.to_model(Notation, **user.model_dump(by_alias=True))
        new_notes = new_notes.data

        try:
            create_many_notes(new_notes)
        except sqlalchemy.exc.IntegrityError:
            response = 'Some sleep notes in file already exists. Date of note must be unique!'
            return Response(response, HTTPStatusCodes.CONFLICT_409)

        response = import_success_response
        return Response(response, HTTPStatusCodes.STATUS_CREATED_201)
